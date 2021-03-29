---
title: 执行计划缓存
aliases: ['/docs-cn/dev/sql-prepare-plan-cache/']
---

# 执行计划缓存

TiDB 支持对 `Prepare` / `Execute` 请求的执行计划缓存。其中包括以下两种形式的预处理语句：

- 使用 `COM_STMT_PREPARE` 和 `COM_STMT_EXECUTE` 的协议功能；
- 执行 `Prepare` / `Execute` SQL 语句查询；

TiDB 优化器对这两类查询的处理是一样的：`Prepare` 时将参数化的 SQL 查询解析成 AST（抽象语法树），每次 `Execute` 时根据保存的 AST 和具体的参数值生成执行计划。

当开启执行计划缓存后，每条 `Prepare` 语句的第一次 `Execute` 会检查当前查询是否可以使用执行计划缓存，如果可以则将生成的执行计划放进一个由 LRU 链表构成的缓存中；在后续的 `Execute` 中，会先从缓存中获取执行计划，并检查是否可用，如果获取和检查成功则跳过生成执行计划这一步，否则重新生成执行计划并放入缓存中。

在当前版本中，当 `Prepare` 语句符合以下条件任何一条，查询不能使用执行计划缓存：

- 查询包含除 `?` 外的变量（系统变量或用户自定义变量）；
- 查询包含子查询；
- 查询包含不能被缓存的函数表达式，如 `current_user()`、`database()`、`last_insert_id()` 等；
- 查询的 `Order By` 语句中包含 `?`；
- 查询的 `Group By` 语句中包含 `?`；
- 查询的 `Limit [Offset]` 语句中包含 `?`；
- 查询包含的 `Window` 函数的 window frame 定义含有 `?`；
- 查询引用了分区表；

LRU 链表是设计成 session 级别的缓存，因为 `Prepare` / `Execute` 不能跨 session 执行。LRU 链表的每个元素是一个 key-value 对，value 是执行计划，key 由如下几部分组成：

- 执行 `Execute` 时所在数据库的名字；
- `Prepare` 语句的标识符，即紧跟在 `PREPARE` 关键字后的名字；
- 当前的 schema 版本，每条执行成功的 DDL 语句会修改 schema 版本；
- 执行 `Execute` 时的 SQL Mode；
- 当前设置的时区，即系统变量 `time_zone` 的值；

key 中任何一项变动（如切换数据库，重命名 `Prepare` 语句，执行 DDL，或修改 SQL Mode / `time_zone` 的值），或 LRU 淘汰机制触发都会导致 `Execute` 时无法命中执行计划缓存。

成功从缓存中获取到执行计划后，TiDB 会先检查执行计划是否依然合法，如果当前 `Execute` 在显式事务里执行，并且引用的表在事务前序语句中被修改，而缓存的执行计划对该表访问不包含 `UnionScan` 算子，则它不能被执行。

在通过合法性检测后，会根据当前最新参数值，对执行计划的扫描范围做相应调整，再用它执行获取数据。

关于执行计划缓存和查询性能有两点值得注意：

- 考虑到不同 `Execute` 的参数会不同，执行计划缓存为了保证适配性会禁止一些和具体参数值密切相关的激进查询优化手段，导致对特定的一些参数值，查询计划可能不是最优。比如查询的过滤条件为 `where a > ? and a < ?`，第一次 `Execute` 时参数分别为 2 和 1，考虑到这两个参数下次执行时可能会是 1 和 2，优化器不会生成对当前参数最优的 `TableDual` 执行计划。
- 如果不考虑缓存失效和淘汰，一份执行计划缓存会对应各种不同的参数取值，理论上也会导致某些取值下执行计划非最优。比如查询过滤条件为 `where a < ?`，假如第一次执行 `Execute` 时用的参数值为 1，此时优化器生成最优的 `IndexScan` 执行计划放入缓存，在后续执行 `Exeucte` 时参数变为 10000，此时 `TableScan` 可能才是更优执行计划，但由于执行计划缓存，执行时还是会使用先前生成的 `IndexScan`。因此执行计划缓存更适用于查询较为简单（查询编译耗时占比较高）且执行计划较为固定的业务场景。

目前执行计划缓存功能默认关闭，可以通过打开配置文件中 [`prepare-plan-cache` 项](/tidb-configuration-file.md#prepared-plan-cache)启用这项功能。

> **注意：**
>
> 执行计划缓存功能仅针对 `Prepare` / `Execute` 请求，对普通查询无效。

在开启了执行计划缓存功能后，可以通过 session 级别的系统变量 `last_plan_from_cache` 查看上一条 `Execute` 语句是否使用了缓存的执行计划，例如：

{{< copyable "sql" >}}

```sql
MySQL [test]> create table t(a int);
Query OK, 0 rows affected (0.00 sec)

MySQL [test]> prepare stmt from 'select * from t where a = ?';
Query OK, 0 rows affected (0.00 sec)

MySQL [test]> set @a = 1;
Query OK, 0 rows affected (0.00 sec)

-- 第一次 execute 生成执行计划放入缓存
MySQL [test]> execute stmt using @a;
Empty set (0.00 sec)

MySQL [test]> select @@last_plan_from_cache;
+------------------------+
| @@last_plan_from_cache |
+------------------------+
| 0                      |
+------------------------+
1 row in set (0.00 sec)

-- 第二次 execute 命中缓存
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

如果发现某一组 `Prepare` / `Execute` 由于执行计划缓存导致了非预期行为，可以通过 SQL Hint `ignore_plan_cache()` 让该组语句不使用缓存。还是用上述的 `stmt` 为例：

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
