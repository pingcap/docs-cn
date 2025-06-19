---
title: SQL Prepared 执行计划缓存
summary: 了解 TiDB 中的 SQL Prepared 执行计划缓存。
---

# SQL Prepared 执行计划缓存

TiDB 支持对 `Prepare` 和 `Execute` 查询的执行计划缓存。这包括两种形式的预处理语句：

- 使用 `COM_STMT_PREPARE` 和 `COM_STMT_EXECUTE` 协议特性。
- 使用 SQL 语句 `PREPARE` 和 `EXECUTE`。

TiDB 优化器以相同的方式处理这两种类型的查询：在准备阶段，将参数化查询解析为 AST（抽象语法树）并缓存；在后续执行时，基于存储的 AST 和具体参数值生成执行计划。

当启用执行计划缓存时，每个 `Prepare` 语句在首次执行时会检查当前查询是否可以使用执行计划缓存，如果可以使用，则将生成的执行计划放入由 LRU（最近最少使用）链表实现的缓存中。在后续的 `Execute` 查询中，从缓存中获取执行计划并检查其可用性。如果检查成功，则跳过生成执行计划的步骤。否则，重新生成执行计划并保存在缓存中。

TiDB 还支持对某些非 `PREPARE` 语句的执行计划缓存，类似于 `Prepare`/`Execute` 语句。更多详情，请参考[非预处理执行计划缓存](/sql-non-prepared-plan-cache.md)。

在当前版本的 TiDB 中，如果 `Prepare` 语句满足以下任一条件，则不会缓存查询或计划：

- 查询包含除 `SELECT`、`UPDATE`、`INSERT`、`DELETE`、`Union`、`Intersect` 和 `Except` 之外的 SQL 语句。
- 查询访问临时表，或包含生成列的表，或使用静态模式（即 [`tidb_partition_prune_mode`](/system-variables.md#tidb_partition_prune_mode-new-in-v51) 设置为 `static`）访问分区表。
- 查询包含非相关子查询，如 `SELECT * FROM t1 WHERE t1.a > (SELECT 1 FROM t2 WHERE t2.b < 1)`。
- 查询包含在执行计划中带有 `PhysicalApply` 算子的相关子查询，如 `SELECT * FROM t1 WHERE t1.a > (SELECT a FROM t2 WHERE t1.b > t2.b)`。
- 查询包含 `ignore_plan_cache` 或 `set_var` 提示，如 `SELECT /*+ ignore_plan_cache() */ * FROM t` 或 `SELECT /*+ set_var(max_execution_time=1) */ * FROM t`。
- 查询包含除 `?` 之外的变量（包括系统变量或用户定义变量），如 `select * from t where a>? and b>@x`。
- 查询包含无法缓存的函数：`database()`、`current_user`、`current_role`、`user`、`connection_id`、`last_insert_id`、`row_count`、`version` 和 `like`。
- 查询使用变量作为 `LIMIT` 参数（如 `LIMIT ?` 和 `LIMIT 10, ?`）且变量值大于 10000。
- 查询在 `Order By` 后包含 `?`，如 `Order By ?`。这类查询基于 `?` 指定的列进行排序。如果针对不同列的查询使用相同的执行计划，结果将会错误。因此，这类查询不会被缓存。但是，如果查询是常见的，如 `Order By a+?`，则会被缓存。
- 查询在 `Group By` 后包含 `?`，如 `Group By?`。这类查询基于 `?` 指定的列进行分组。如果针对不同列的查询使用相同的执行计划，结果将会错误。因此，这类查询不会被缓存。但是，如果查询是常见的，如 `Group By a+?`，则会被缓存。
- 查询在窗口函数的 `Window Frame` 定义中包含 `?`，如 `(partition by year order by sale rows ? preceding)`。如果 `?` 出现在窗口函数的其他位置，则查询会被缓存。
- 查询包含用于比较 `int` 和 `string` 的参数，如 `c_int >= ?` 或 `c_int in (?, ?)`，其中 `?` 表示字符串类型，如 `set @x='123'`。为确保查询结果与 MySQL 兼容，需要在每次查询时调整参数，因此这类查询不会被缓存。
- 计划尝试访问 `TiFlash`。
- 在大多数情况下，包含 `TableDual` 的计划不会被缓存，除非当前 `Prepare` 语句没有参数。
- 查询访问 TiDB 系统视图，如 `information_schema.columns`。不建议使用 `Prepare` 和 `Execute` 语句访问系统视图。

TiDB 对查询中的 `?` 数量有限制。如果查询包含超过 65535 个 `?`，将报错 `Prepared statement contains too many placeholders`。

LRU 链表被设计为会话级缓存，因为 `Prepare`/`Execute` 不能跨会话执行。LRU 列表的每个元素都是一个键值对。值是执行计划，键由以下部分组成：

- 执行 `Execute` 的数据库名称
- `Prepare` 语句的标识符，即 `PREPARE` 关键字后的名称
- 当前的 schema 版本，每次成功执行 DDL 语句后都会更新
- 执行 `Execute` 时的 SQL 模式
- 当前时区，即 `time_zone` 系统变量的值
- `sql_select_limit` 系统变量的值

上述信息的任何变化（例如，切换数据库、重命名 `Prepare` 语句、执行 DDL 语句或修改 SQL 模式/`time_zone` 的值），或 LRU 缓存淘汰机制都会导致执行时执行计划缓存未命中。

从缓存中获取执行计划后，TiDB 首先检查执行计划是否仍然有效。如果当前 `Execute` 语句在显式事务中执行，并且在事务前序语句中修改了引用的表，则访问该表的缓存执行计划不包含 `UnionScan` 算子，因此无法执行。

通过验证测试后，根据当前参数值调整执行计划的扫描范围，然后用于执行数据查询。

关于执行计划缓存和查询性能，有几点值得注意：

- 无论执行计划是否被缓存，它都会受到 SQL 绑定的影响。对于未缓存的执行计划（第一次 `Execute`），这些计划受现有 SQL 绑定的影响。对于已缓存的执行计划，如果创建了新的 SQL 绑定，这些计划将变为无效。
- 缓存的计划不受统计信息、优化规则和表达式下推黑名单变化的影响。
- 考虑到 `Execute` 的参数不同，执行计划缓存禁止了一些与特定参数值密切相关的激进查询优化方法，以确保适应性。这导致查询计划可能对某些参数值不是最优的。例如，查询的过滤条件是 `where a > ? And a < ?`，第一次 `Execute` 语句的参数分别是 `2` 和 `1`。考虑到这两个参数在下次执行时可能是 `1` 和 `2`，优化器不会生成针对当前参数值的最优 `TableDual` 执行计划；
- 如果不考虑缓存失效和淘汰，执行计划缓存适用于各种参数值，这在理论上也会导致某些值的执行计划不是最优的。例如，如果过滤条件是 `where a < ?` 且第一次执行使用的参数值是 `1`，那么优化器会生成最优的 `IndexScan` 执行计划并将其放入缓存。在后续执行中，如果值变为 `10000`，`TableScan` 计划可能是更好的选择。但由于执行计划缓存，会使用之前生成的 `IndexScan` 进行执行。因此，执行计划缓存更适合于查询简单（编译比例高）且执行计划相对固定的应用场景。

从 v6.1.0 开始，执行计划缓存默认启用。你可以通过系统变量 [`tidb_enable_prepared_plan_cache`](/system-variables.md#tidb_enable_prepared_plan_cache-new-in-v610) 控制预处理计划缓存。

> **注意：**
>
> [`tidb_enable_prepared_plan_cache`](/system-variables.md#tidb_enable_prepared_plan_cache-new-in-v610) 系统变量仅控制 `Prepare`/`Execute` 查询的执行计划缓存，不控制普通查询的执行计划缓存。关于普通查询的执行计划缓存，请参见[SQL 非预处理执行计划缓存](/sql-non-prepared-plan-cache.md)。

启用执行计划缓存功能后，你可以使用会话级系统变量 [`last_plan_from_cache`](/system-variables.md#last_plan_from_cache-new-in-v40) 查看上一个 `Execute` 语句是否使用了缓存的执行计划，例如：

{{< copyable "sql" >}}

```sql
MySQL [test]> create table t(a int);
Query OK, 0 rows affected (0.00 sec)
MySQL [test]> prepare stmt from 'select * from t where a = ?';
Query OK, 0 rows affected (0.00 sec)
MySQL [test]> set @a = 1;
Query OK, 0 rows affected (0.00 sec)

-- 第一次执行生成执行计划并保存在缓存中。
MySQL [test]> execute stmt using @a;
Empty set (0.00 sec)
MySQL [test]> select @@last_plan_from_cache;
+------------------------+
| @@last_plan_from_cache |
+------------------------+
| 0                      |
+------------------------+
1 row in set (0.00 sec)

-- 第二次执行命中缓存。
MySQL [test]> execute stmt using @a;
Empty set (0.00 sec)
MySQL [test]> select @@last_plan_from_cache;
+------------------------+
| @@last_plan_from_cache |
+------------------------+
| 1                      |
+------------------------+
1 row in set (0.00 sec)
```

如果你发现某个 `Prepare`/`Execute` 由于执行计划缓存而出现意外行为，可以使用 `ignore_plan_cache()` SQL 提示跳过当前语句的执行计划缓存。仍以上述语句为例：

{{< copyable "sql" >}}

```sql
MySQL [test]> prepare stmt from 'select /*+ ignore_plan_cache() */ * from t where a = ?';
Query OK, 0 rows affected (0.00 sec)
MySQL [test]> set @a = 1;
Query OK, 0 rows affected (0.00 sec)
MySQL [test]> execute stmt using @a;
Empty set (0.00 sec)
MySQL [test]> select @@last_plan_from_cache;
+------------------------+
| @@last_plan_from_cache |
+------------------------+
| 0                      |
+------------------------+
1 row in set (0.00 sec)
MySQL [test]> execute stmt using @a;
Empty set (0.00 sec)
MySQL [test]> select @@last_plan_from_cache;
+------------------------+
| @@last_plan_from_cache |
+------------------------+
| 0                      |
+------------------------+
1 row in set (0.00 sec)
```

## 预处理计划缓存的诊断

某些查询或计划无法被缓存。你可以使用 `SHOW WARNINGS` 语句检查查询或计划是否被缓存。如果未被缓存，你可以在结果中查看失败的原因。例如：

```sql
mysql> PREPARE st FROM 'SELECT * FROM t WHERE a > (SELECT MAX(a) FROM t)';  -- 查询包含子查询，无法缓存。

Query OK, 0 rows affected, 1 warning (0.01 sec)

mysql> show warnings;  -- 检查查询计划无法缓存的原因。

+---------+------+-----------------------------------------------+
| Level   | Code | Message                                       |
+---------+------+-----------------------------------------------+
| Warning | 1105 | skip plan-cache: sub-queries are un-cacheable |
+---------+------+-----------------------------------------------+
1 row in set (0.00 sec)

mysql> prepare st from 'select * from t where a<?';

Query OK, 0 rows affected (0.00 sec)

mysql> set @a='1';

Query OK, 0 rows affected (0.00 sec)

mysql> execute st using @a;  -- 优化将非 INT 类型转换为 INT 类型，执行计划可能随参数变化而变化，所以 TiDB 不缓存该计划。

Empty set, 1 warning (0.01 sec)

mysql> show warnings;

+---------+------+----------------------------------------------+
| Level   | Code | Message                                      |
+---------+------+----------------------------------------------+
| Warning | 1105 | skip plan-cache: '1' may be converted to INT |
+---------+------+----------------------------------------------+
1 row in set (0.00 sec)
```

## 预处理计划缓存的内存管理

<CustomContent platform="tidb">

使用预处理计划缓存会产生内存开销。要查看每个 TiDB 实例中所有会话的缓存执行计划的总内存消耗，你可以使用 Grafana 中的 [**Plan Cache Memory Usage** 监控面板](/grafana-tidb-dashboard.md)。

> **注意：**
>
> 由于 Golang 的内存回收机制和一些未计数的内存结构，Grafana 中显示的内存不等于实际的堆内存使用量。经测试，Grafana 中显示的内存与实际堆内存使用量之间存在约 ±20% 的偏差。

要查看每个 TiDB 实例中缓存的执行计划总数，你可以使用 Grafana 中的 [**Plan Cache Plan Num** 面板](/grafana-tidb-dashboard.md)。

以下是 Grafana 中 **Plan Cache Memory Usage** 和 **Plan Cache Plan Num** 面板的示例：

![grafana_panels](/media/planCache-memoryUsage-planNum-panels.png)

从 v7.1.0 开始，你可以通过配置系统变量 [`tidb_session_plan_cache_size`](/system-variables.md#tidb_session_plan_cache_size-new-in-v710) 来控制每个会话中可以缓存的计划的最大数量。对于不同的环境，建议值如下，你可以根据监控面板进行调整：

</CustomContent>

<CustomContent platform="tidb-cloud">

使用预处理计划缓存会产生一些内存开销。在内部测试中，每个缓存的计划平均消耗 100 KiB 内存。由于计划缓存目前是在 `SESSION` 级别，总内存消耗大约是 `会话数 * 每个会话中缓存的平均计划数 * 100 KiB`。

例如，当前 TiDB 实例有 50 个并发会话，每个会话大约有 100 个缓存的计划。总内存消耗大约是 `50 * 100 * 100 KiB` = `512 MB`。

你可以通过配置系统变量 [`tidb_session_plan_cache_size`](/system-variables.md#tidb_session_plan_cache_size-new-in-v710) 来控制每个会话中可以缓存的计划的最大数量。对于不同的环境，建议值如下：

</CustomContent>

- 当 TiDB 服务器实例的内存阈值 <= 64 GiB 时，将 `tidb_session_plan_cache_size` 设置为 `50`。
- 当 TiDB 服务器实例的内存阈值 > 64 GiB 时，将 `tidb_session_plan_cache_size` 设置为 `100`。

从 v7.1.0 开始，你可以使用系统变量 [`tidb_plan_cache_max_plan_size`](/system-variables.md#tidb_plan_cache_max_plan_size-new-in-v710) 控制可以缓存的计划的最大大小。默认值为 2 MB。如果计划的大小超过此值，则不会缓存该计划。

当 TiDB 服务器的未使用内存小于某个阈值时，会触发计划缓存的内存保护机制，通过该机制将驱逐一些缓存的计划。

你可以通过配置系统变量 `tidb_prepared_plan_cache_memory_guard_ratio` 来控制阈值。阈值默认为 0.1，这意味着当 TiDB 服务器的未使用内存小于总内存的 10%（90% 的内存已使用）时，将触发内存保护机制。

<CustomContent platform="tidb">

由于内存限制，计划缓存有时可能会未命中。你可以通过查看 Grafana 仪表板中的 [`Plan Cache Miss OPS` 指标](/grafana-tidb-dashboard.md)来检查状态。

</CustomContent>

<CustomContent platform="tidb-cloud">

由于内存限制，计划缓存有时可能会未命中。

</CustomContent>

## 清除执行计划缓存

你可以通过执行 `ADMIN FLUSH [SESSION | INSTANCE] PLAN_CACHE` 语句来清除执行计划缓存。

在此语句中，`[SESSION | INSTANCE]` 指定是清除当前会话还是整个 TiDB 实例的计划缓存。如果未指定范围，则上述语句默认应用于 `SESSION` 缓存。

以下是清除 `SESSION` 执行计划缓存的示例：

{{< copyable "sql" >}}

```sql
MySQL [test]> create table t (a int);
Query OK, 0 rows affected (0.00 sec)

MySQL [test]> prepare stmt from 'select * from t';
Query OK, 0 rows affected (0.00 sec)

MySQL [test]> execute stmt;
Empty set (0.00 sec)

MySQL [test]> execute stmt;
Empty set (0.00 sec)

MySQL [test]> select @@last_plan_from_cache; -- 选择缓存的计划
+------------------------+
| @@last_plan_from_cache |
+------------------------+
|                      1 |
+------------------------+
1 row in set (0.00 sec)

MySQL [test]> admin flush session plan_cache; -- 清除当前会话的缓存计划
Query OK, 0 rows affected (0.00 sec)

MySQL [test]> execute stmt;
Empty set (0.00 sec)

MySQL [test]> select @@last_plan_from_cache; -- 无法再次选择缓存的计划，因为它已被清除
+------------------------+
| @@last_plan_from_cache |
+------------------------+
|                      0 |
+------------------------+
1 row in set (0.00 sec)
```

目前，TiDB 不支持清除 `GLOBAL` 执行计划缓存。这意味着你无法清除整个 TiDB 集群的缓存计划。如果你尝试清除 `GLOBAL` 执行计划缓存，将报告以下错误：

{{< copyable "sql" >}}

```sql
MySQL [test]> admin flush global plan_cache;
ERROR 1105 (HY000): Do not support the 'admin flush global scope.'
```

## 忽略 `COM_STMT_CLOSE` 命令和 `DEALLOCATE PREPARE` 语句

为了减少 SQL 语句的语法解析成本，建议你运行一次 `prepare stmt`，然后多次运行 `execute stmt`，最后运行 `deallocate prepare`：

{{< copyable "sql" >}}

```sql
MySQL [test]> prepare stmt from '...'; -- 准备一次
MySQL [test]> execute stmt using ...;  -- 执行一次
MySQL [test]> ...
MySQL [test]> execute stmt using ...;  -- 执行多次
MySQL [test]> deallocate prepare stmt; -- 释放预处理语句
```

在实际操作中，你可能习惯于每次运行 `execute stmt` 后都运行 `deallocate prepare`，如下所示：

{{< copyable "sql" >}}

```sql
MySQL [test]> prepare stmt from '...'; -- 准备一次
MySQL [test]> execute stmt using ...;
MySQL [test]> deallocate prepare stmt; -- 释放预处理语句
MySQL [test]> prepare stmt from '...'; -- 准备两次
MySQL [test]> execute stmt using ...;
MySQL [test]> deallocate prepare stmt; -- 释放预处理语句
```

在这种情况下，第一个执行语句获得的计划无法被第二个执行语句重用。

为了解决这个问题，你可以将系统变量 [`tidb_ignore_prepared_cache_close_stmt`](/system-variables.md#tidb_ignore_prepared_cache_close_stmt-new-in-v600) 设置为 `ON`，这样 TiDB 就会忽略关闭 `prepare stmt` 的命令：

{{< copyable "sql" >}}

```sql
mysql> set @@tidb_ignore_prepared_cache_close_stmt=1;  -- 启用变量
Query OK, 0 rows affected (0.00 sec)

mysql> prepare stmt from 'select * from t'; -- 准备一次
Query OK, 0 rows affected (0.00 sec)

mysql> execute stmt;                        -- 执行一次
Empty set (0.00 sec)

mysql> deallocate prepare stmt;             -- 第一次执行后释放
Query OK, 0 rows affected (0.00 sec)

mysql> prepare stmt from 'select * from t'; -- 准备两次
Query OK, 0 rows affected (0.00 sec)

mysql> execute stmt;                        -- 执行两次
Empty set (0.00 sec)

mysql> select @@last_plan_from_cache;       -- 重用上一个计划
+------------------------+
| @@last_plan_from_cache |
+------------------------+
|                      1 |
+------------------------+
1 row in set (0.00 sec)
```

### 监控

<CustomContent platform="tidb">

在 TiDB 页面的 **Executor** 部分的 [Grafana 仪表板](/grafana-tidb-dashboard.md)中，有 "Queries Using Plan Cache OPS" 和 "Plan Cache Miss OPS" 图表。这些图表可用于检查 TiDB 和应用程序是否都正确配置以允许 SQL 计划缓存正常工作。同一页面的 **Server** 部分提供了 "Prepared Statement Count" 图表。如果应用程序使用预处理语句（这是 SQL 计划缓存正常工作所必需的），此图表会显示非零值。

![`sql_plan_cache`](/media/performance/sql_plan_cache.png)

</CustomContent>

<CustomContent platform="tidb-cloud">

在 [TiDB Cloud 控制台](https://tidbcloud.com/) 的[**监控**](/tidb-cloud/built-in-monitoring.md)页面上，你可以查看 `Queries Using Plan Cache OPS` 指标，以获取所有 TiDB 实例中每秒使用或未命中计划缓存的查询数。

</CustomContent>
