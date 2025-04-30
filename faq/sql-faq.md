---
title: SQL 操作常见问题
summary: 介绍 SQL 操作相关的常见问题。
---

# SQL 操作常见问题

本文档介绍 TiDB 中常见的 SQL 操作问题。

## TiDB 是否支持二级键？

支持。你可以在具有唯一[二级索引](/develop/dev-guide-create-secondary-indexes.md)的非主键列上设置 [`NOT NULL` 约束](/constraints.md#非空约束)。在这种情况下，该列用作二级键。

## TiDB 在对大表执行 DDL 操作时，性能表现如何？

TiDB 在对大表执行 DDL 操作时，一般不会有什么问题。TiDB 支持在线 DDL 操作，且这些 DDL 操作不会阻塞 DML 操作。

对于添加列、删除列或删除索引等 DDL 操作，TiDB 可以快速完成这些操作。

对于添加索引等 DDL 操作，TiDB 需要进行回填 (backfill) 操作，这个过程需要较长的时间（取决于表的大小）和额外的资源消耗。对在线业务的影响可调节。TiDB 可以通过多线程进行 backfill，资源消耗可通过以下系统变量进行设置：

- [`tidb_ddl_reorg_worker_cnt`](/system-variables.md#tidb_ddl_reorg_worker_cnt)
- [`tidb_ddl_reorg_priority`](/system-variables.md#tidb_ddl_reorg_priority)
- [`tidb_ddl_error_count_limit`](/system-variables.md#tidb_ddl_error_count_limit)
- [`tidb_ddl_reorg_batch_size`](/system-variables.md#tidb_ddl_reorg_batch_size)

## 如何选择正确的查询计划？是否需要使用优化器提示？还是可以使用提示？

TiDB 包含一个基于成本的优化器。在大多数情况下，优化器会为你选择最优的查询计划。如果优化器工作欠佳，你可以使用[优化器提示](/optimizer-hints.md)来干预优化器。

另外，你还可以使用[执行计划绑定](/sql-plan-management.md#执行计划绑定-sql-binding)来为特定的 SQL 语句固定查询计划。

## 如何阻止特定的 SQL 语句执行（或者将某个 SQL 语句加入黑名单）？

对于 v7.5.0 及以上版本，你可以使用 [`QUERY WATCH`](/sql-statements/sql-statement-query-watch.md) 语句将特定的 SQL 查询加入黑名单。具体使用方法参见[管理资源消耗超出预期的查询 (Runaway Queries)](/tidb-resource-control-runaway-queries.md#query-watch-语句说明)。

对于 v7.5.0 之前版本，你可以使用 [`MAX_EXECUTION_TIME`](/optimizer-hints.md#max_execution_timen) Hint 来创建 [SQL 绑定](/sql-plan-management.md#执行计划绑定-sql-binding)，将特定语句的执行时间限制为一个较小的值（例如 1ms）。这样，语句就会在超过限制时自动终止。

例如，要阻止执行 `SELECT * FROM t1, t2 WHERE t1.id = t2.id`，可以使用以下 SQL 绑定将语句的执行时间限制为 1ms：

```sql
CREATE GLOBAL BINDING for
    SELECT * FROM t1, t2 WHERE t1.id = t2.id
USING
    SELECT /*+ MAX_EXECUTION_TIME(1) */ * FROM t1, t2 WHERE t1.id = t2.id;
```

> **注意：**
>
> `MAX_EXECUTION_TIME` 的精度大约为 100ms。在 TiDB 终止 SQL 语句之前，TiKV 中的任务可能已经开始执行。为了减少这种情况下 TiKV 的资源消耗，建议将系统变量 [`tidb_enable_paging`](/system-variables.md#tidb_enable_paging-从-v540-版本开始引入) 的值设置为 `ON`。

删除该 SQL 绑定可以移除限制。

```sql
DROP GLOBAL BINDING for
    SELECT * FROM t1, t2 WHERE t1.id = t2.id;
```

## TiDB 对哪些 MySQL variables 兼容？

详细可参考[系统变量](/system-variables.md)。

## 省略 `ORDER BY` 条件时 TiDB 中返回结果的顺序与 MySQL 中的不一致

这不是 bug。返回结果的顺序视不同情况而定，不保证顺序统一。

MySQL 中，返回结果的顺序可能较为固定，因为查询是通过单线程执行的。但升级到新版本后，查询计划也可能变化。无论是否期待返回结果有序，都推荐使用 `ORDER BY` 条件。

[ISO/IEC 9075:1992, Database Language SQL- July 30, 1992](http://www.contrib.andrew.cmu.edu/~shadow/sql/sql1992.txt) 对此有如下表述：

> If an `<order by clause>` is not specified, then the table specified by the `<cursor specification>` is T and the ordering of rows in T is implementation-dependent.（如果未指定 `<order by 条件>`，通过 `<cursor specification>` 指定的表为 T，那么 T 表中的行顺序视执行情况而定。）

以下两条查询的结果都是合法的：

```sql
> select * from t;
+------+------+
| a    | b    |
+------+------+
|    1 |    1 |
|    2 |    2 |
+------+------+
2 rows in set (0.00 sec)
```

```sql
> select * from t; -- 不确定返回结果的顺序
+------+------+
| a    | b    |
+------+------+
|    2 |    2 |
|    1 |    1 |
+------+------+
2 rows in set (0.00 sec)
```

如果 `ORDER BY` 中使用的列不是唯一列，就无法确定该语句返回结果的顺序。在以下示例中，`a` 列有重复值，因此只有 `ORDER BY a, b` 能确定返回结果的顺序。

```sql
> select * from t order by a;
+------+------+
| a    | b    |
+------+------+
|    1 |    1 |
|    2 |    1 |
|    2 |    2 |
+------+------+
3 rows in set (0.00 sec)
```

在以下示例中，`order by a` 能确定 a 列的顺序，但不能确定 b 列的顺序。

```sql
> select * from t order by a;
+------+------+
| a    | b    |
+------+------+
|    1 |    1 |
|    2 |    2 |
|    2 |    1 |
+------+------+
3 rows in set (0.00 sec)
```

在 TiDB 中，你还可以使用系统变量 [`tidb_enable_ordered_result_mode`](/system-variables.md#tidb_enable_ordered_result_mode) 来指定是否对最终的输出结果进行自动排序。

## TiDB 是否支持 `SELECT FOR UPDATE`？

支持。当 TiDB 使用悲观锁（自 TiDB v3.0.8 起默认使用）时，TiDB 中 `SELECT FOR UPDATE` 的行为与 MySQL 中的基本一致。

当 TiDB 使用乐观锁时，`SELECT FOR UPDATE` 不会在事务启动时对数据加锁，而是在提交事务时检查冲突。如果检查出冲突，会回滚待提交的事务。

详情参考 [SELECT 语句语法元素说明](/sql-statements/sql-statement-select.md#语法元素说明)。

## TiDB 的 codec 能保证 UTF8 的字符串是 memcomparable 的吗？我们的 key 需要支持 UTF8，有什么编码建议吗？

TiDB 的默认字符集是 `utf8mb4`，字符串是 memcomparable 格式。关于字符集的更多信息，参见[字符集和排序规则](/character-set-and-collation.md)。

## 一个事务中的语句数量最大是多少？

一个事务中的语句数量，默认限制最大为 5000 条。

在使用乐观事务并开启事务重试的情况下，默认限制 5000，可通过 [`stmt-count-limit`](/tidb-configuration-file.md#stmt-count-limit) 调整。

## TiDB 中，为什么出现后插入数据的自增 ID 反而小？

TiDB 的自增 ID (`AUTO_INCREMENT`) 只保证自增且唯一，并不保证连续分配。TiDB 目前采用批量分配的方式，所以如果在多台 TiDB server 上同时插入数据，分配的自增 ID 会不连续。当多个线程并发往不同的 TiDB server 插入数据的时候，有可能会出现后插入的数据自增 ID 小的情况。此外，TiDB 允许给整型类型的字段指定 AUTO_INCREMENT，且一个表只允许一个属性为 `AUTO_INCREMENT` 的字段。详情可参考[自增 ID](/mysql-compatibility.md#自增-id)和 [AUTO_INCREMENT](/auto-increment.md)。

## 如何在 TiDB 中修改 `sql_mode`？

TiDB 支持在会话或全局作用域上修改 [`sql_mode`](/system-variables.md#sql_mode) 系统变量。

- 对全局作用域变量的修改，设置后将作用于集群中的其它服务器，并且重启后更改依然有效。因此，你无需在每台 TiDB 服务器上都更改 `sql_mode` 的值。
- 对会话作用域变量的修改，设置后只影响当前会话，重启后更改消失。

## 用 Sqoop 批量写入 TiDB 数据，虽然配置了 `--batch` 选项，但还是会遇到 `java.sql.BatchUpdateException:statement count 5001 exceeds the transaction limitation` 的错误，该如何解决？

问题原因：在 Sqoop 中，`--batch` 是指每个批次提交 100 条 statement，但是默认每个 statement 包含 100 条 SQL 语句，所以此时 100 * 100 = 10000 条 SQL 语句，超出了 TiDB 的事务限制 5000 条。

解决办法：

- 增加选项 `-Dsqoop.export.records.per.statement=10`，完整的用法如下：

    ```bash
    sqoop export \
        -Dsqoop.export.records.per.statement=10 \
        --connect jdbc:mysql://mysql.example.com/sqoop \
        --username sqoop ${user} \
        --password ${passwd} \
        --table ${tab_name} \
        --export-dir ${dir} \
        --batch
    ```

- 也可以选择增大 TiDB 的单个事物语句数量限制，不过此操作会导致内存增加。详情参见 [SQL 语句的限制](/tidb-limitations.md#sql-statements-的限制)。

## TiDB 有像 Oracle 那样的 Flashback Query 功能么，DDL 支持么？

有，也支持 DDL。详细参考[使用 AS OF TIMESTAMP 语法读取历史数据](/as-of-timestamp.md)。

## TiDB 中删除数据后会立即释放空间吗？

在 TiDB 中使用 `DELETE`，`TRUNCATE` 和 `DROP` 语句删除数据都不会立即释放空间。对于 `TRUNCATE` 和 `DROP` 操作，在达到 TiDB 的 GC (garbage collection) 时间后（默认 10 分钟），TiDB 的 GC 机制会删除数据并释放空间。对于 DELETE 操作，TiDB 的 GC 机制会删除数据，但不会立即释放空间，而是等到后续进行 compaction 时释放空间。

## 删除数据后查询速度为何会变慢？

删除大量数据后，会有很多无用的 key 存在，影响查询效率。要解决该问题，可以尝试开启 [Region Merge](/best-practices/massive-regions-best-practices.md#方法五开启-region-merge) 功能，具体可参考[最佳实践](https://pingcap.com/blog-cn/tidb-best-practice/)中的删除数据部分。

## 对数据做删除操作之后，空间回收比较慢，如何处理？

TiDB 采用了多版本并发控制 (MVCC) 机制，当新写入的数据覆盖旧的数据时，旧的数据不会被替换掉，而是与新写入的数据同时保留，并以时间戳来区分版本。为了使并发事务能查看到早期版本的数据，删除数据时 TiDB 不会立即回收空间，而是等待一段时间后再进行垃圾回收 (GC)。要配置历史数据的保留时限，你可以修改系统变量 [`tidb_gc_life_time`](/system-variables.md#tidb_gc_life_time-从-v50-版本开始引入)的值（默认值为 `10m0s`）。

## `SHOW PROCESSLIST` 是否显示系统进程号？

TiDB 中的 `SHOW PROCESSLIST` 与 MySQL 中的 `SHOW PROCESSLIST` 显示内容基本一致，不会显示系统进程号。而返回结果中的 ID 表示当前的 session ID。其中 TiDB 的 `SHOW PROCESSLIST` 和 MySQL 的 `SHOW PROCESSLIST` 区别如下：

+ 由于 TiDB 是分布式数据库，TiDB server 实例是无状态的 SQL 解析和执行引擎（详情可参考 [TiDB 整体架构](/tidb-architecture.md)），用户使用 MySQL 客户端登录的是哪个 TiDB server，`SHOW PROCESSLIST` 就会显示当前连接的这个 TiDB server 中执行的 session 列表，不是整个集群中运行的全部 session 列表；而 MySQL 是单机数据库，`SHOW PROCESSLIST` 列出的是当前整个 MySQL 数据库的全部执行 SQL 列表。

+ 在查询执行期间，TiDB 中的 `State` 列不会持续更新。由于 TiDB 支持并行查询，每个语句可能同时处于多个状态，因此很难显示为某一种状态。

## 在 TiDB 中如何控制或改变 SQL 提交的执行优先级？

TiDB 支持改变[全局](/system-variables.md#tidb_force_priority)或单个语句的优先级。优先级包括：

- `HIGH_PRIORITY`：该语句为高优先级语句，TiDB 在执行阶段会优先处理这条语句
- `LOW_PRIORITY`：该语句为低优先级语句，TiDB 在执行阶段会降低这条语句的优先级
- `DELAYED`：该语句为正常优先级语句，TiDB 不强制改变这条语句的优先级，与 `tidb_force_priority` 设置为 `NO_PRIORITY` 相同

> **注意：**
>
> TiDB 从 v6.6.0 版本开始支持[使用资源管控 (Resource Control) 实现资源组限制和流控](/tidb-resource-control-ru-groups.md)功能。该功能可以将不同优先级的语句放在不同的资源组中执行，并为这些资源组分配不同的配额和优先级，可以达到更好的资源管控效果。在开启资源管控功能后，语句的调度主要受资源组的控制，`PRIORITY` 将不再生效。建议在支持资源管控的版本优先使用资源管控功能。

以上两种参数可以结合 TiDB 的 DML 语言进行使用，使用方法举例如下：

1. 通过在数据库中写 SQL 的方式来调整优先级：

    ```sql
    SELECT HIGH_PRIORITY | LOW_PRIORITY | DELAYED COUNT(*) FROM table_name;
    INSERT HIGH_PRIORITY | LOW_PRIORITY | DELAYED INTO table_name insert_values;
    DELETE HIGH_PRIORITY | LOW_PRIORITY | DELAYED FROM table_name;
    UPDATE HIGH_PRIORITY | LOW_PRIORITY | DELAYED table_reference SET assignment_list WHERE where_condition;
    REPLACE HIGH_PRIORITY | LOW_PRIORITY | DELAYED INTO table_name;
    ```

2. 全表扫会自动调整为低优先级，[`ANALYZE`](/sql-statements/sql-statement-analyze-table.md) 也是默认低优先级。

## 在 TiDB 中 `auto analyze` 的触发策略是怎样的？

当一张表或分区表的单个分区达到 1000 条记录，且表或分区的（修改数/当前总行数）比例大于 [`tidb_auto_analyze_ratio`](/system-variables.md#tidb_auto_analyze_ratio) 的时候，会自动触发 [`ANALYZE`](/sql-statements/sql-statement-analyze-table.md) 语句。

`tidb_auto_analyze_ratio` 的默认值为 `0.5`，即默认开启触发 `auto analyze`。注意该变量值不建议大于等于 [`pseudo-estimate-ratio`](/tidb-configuration-file.md#pseudo-estimate-ratio)（默认值为 `0.8`），否则优化器可能会使用 pseudo 统计信息。TiDB 从 v5.3.0 开始引入 [`tidb_enable_pseudo_for_outdated_stats`](/system-variables.md#tidb_enable_pseudo_for_outdated_stats-从-v530-版本开始引入) 变量，当设置为 `OFF` 时，即使统计信息过期也不会使用 pseudo 统计信息。

你可以用系统变量 [`tidb_enable_auto_analyze`](/system-variables.md#tidb_enable_auto_analyze-从-v610-版本开始引入) 关闭 `auto analyze`。

## 可以使用 Optimizer Hints 控制优化器行为吗？

在 TiDB 中，你可以用多种方法控制查询优化器的默认行为，包括使用 [Optimizer Hints](/optimizer-hints.md) 和 [SQL 执行计划管理 (SPM)](/sql-plan-management.md)。基本用法同 MySQL 中的一致，还包含若干 TiDB 特有的用法，例如：`select column_name from table_name use index（index_name）where where_condition;`。

## DDL 执行

本节列出了 DDL 语句执行的相关问题。DDL 执行原理的详细说明，参见 [TiDB 中 DDL 执行原理及最佳实践](/ddl-introduction.md)。

### 各类 DDL 操作的预估耗时是多长？

假设 DDL 操作没有被阻塞，各个 TiDB server 能够正常更新 Schema 版本，DDL Owner 节点正常运行。在此情况下，各类 DDL 操作的预估耗时如下：

| DDL 操作类型                                                                                                                                                                    | 预估耗时                   |
|:------------------------------------------------------------------------------------------------------------------------------------------------------------------------|:-----------------------|
| Reorg DDL：例如 `ADD INDEX`、`MODIFY COLUMN`（Reorg 类型的数据更改）                                                                                                                      | 取决于数据量、系统负载以及 DDL 参数的设置 |
| General DDL（除 Reorg DDL 外的 DDL 类型）：例如 `CREATE DATABASE`、`CREATE TABLE`、`DROP DATABASE`、`DROP TABLE`、`TRUNCATE TABLE`、`ALTER TABLE ADD`、`ALTER TABLE DROP`、`MODIFY COLUMN`（只更改元数据）、`DROP INDEX` | 1 秒左右                   |

> **注意：**
>
> 以上为各类操作的预估耗时，请以实际操作耗时为准。

## 执行 DDL 会慢的可能原因

- 在一个用户会话中，DDL 语句之前有非 auto-commit 的 DML 语句，并且该 DML 语句的提交操作比较慢，会导致 DDL 语句执行慢。即执行 DDL 语句前，会先提交之前没有提交的 DML 语句。
- 多个 DDL 语句一起执行的时候，后面的几个 DDL 语句可能会比较慢，因为可能需要排队等待。排队场景包括：
    - 同一类型 DDL 语句需要排队（例如 `CREATE TABLE` 和 `CREATE DATABASE` 都是 General DDL，两个操作同时执行时，需要排队）。自 TiDB v6.2.0 起，支持并行 DDL 语句，但为了避免 DDL 使用过多 TiDB 的计算资源，也有并发度限制，因此会有一定的排队情况。
    - 对同一张表上执行的 DDL 操作存在依赖关系，后面的 DDL 语句需要等待前面的 DDL 操作完成。
- 在集群正常启动后，第一个 DDL 操作的执行时间可能会比较久，可能是因为 DDL 模块在进行 DDL Owner 的选举。

- 终止 TiDB 时，TiDB 不能与 PD 正常通信（包括停电的情况），或者用 `kill -9` 命令终止 TiDB 导致 TiDB 没有及时从 PD 清理注册数据。
- 集群中某个 TiDB 与 PD 或者 TiKV 之间发生通信问题，即 TiDB 不能及时获取最新版本信息。

### 触发 Information schema is changed 错误的原因？

TiDB 在执行 SQL 语句时，会根据隔离级别确定一个对象的 `schema` 版本来处理该 SQL 语句，而且 TiDB 支持在线异步变更 DDL。那么，在执行 DML 的时候可能有 DDL 语句也在执行，而你需要确保每个 SQL 语句在同一个 `schema` 上执行。所以当执行 DML 时，如果遇到正在执行中的 DDL 操作，TiDB 可能会报 `Information schema is changed` 的错误。

从 v6.4.0 开始，TiDB 实现了[元数据锁机制](/metadata-lock.md)，可以让 DML 语句的执行和 DDL Schema 变更协同进行，可以避免大部分 `Information schema is changed` 错误的发生。

报错的可能原因如下：

- 原因 1：正在执行的 DML 所涉及的表和集群中正在执行的 DDL 的表有相同的，那么这个 DML 语句就会报此错。可以通过命令 `admin show ddl job` 查看正在执行的 DDL 操作。
- 原因 2：这个 DML 执行时间很久，而这段时间内执行了很多 DDL 语句，导致中间 `schema` 版本变更次数超过 1024 （此为默认值，可以通过 `tidb_max_delta_schema_count` 变量修改）。
- 原因 3：接受 DML 请求的 TiDB 长时间不能加载到 `schema information`（TiDB 与 PD 或 TiKV 之间的网络连接故障等会导致此问题），而这段时间内执行了很多 DDL 语句，导致中间 `schema` 版本变更次数超过 100。
- 原因 4：TiDB 重启后执行第一个 DDL 操作前，执行 DML 操作，并且在执行过程中遇到了第 1 个 DDL 操作（即在执行第 1 个 DDL 操作前，启动该 DML 对应的事务，且在该 DDL 变更第一个 `schema` 版本后，提交该 DML 对应的事务），那么这个 DML 会报此错。

以上原因中，只有原因 1 与表有关。原因 1 和原因 2 都不会导致业务问题，相应的 DML 会在失败后重试。对于原因 3，需要检查 TiDB 实例和 PD 及 TiKV 的网络情况。

> **注意：**
>
> + 目前 TiDB 未缓存所有的 `schema` 版本信息。
> + 对于每个 DDL 操作，`schema` 版本变更的数量与对应 `schema state` 变更的次数一致。
> + 不同的 DDL 操作版本变更次数不一样。例如，`create table` 操作会有 1 次 `schema` 版本变更；`add column` 操作有 4 次 `schema` 版本变更。

### 触发 Information schema is out of date 错误的原因？

当执行 DML 时，TiDB 超过一个 DDL lease 时间（默认 45s）没能加载到最新的 schema 就可能会报 `Information schema is out of date` 的错误。遇到此错的可能原因如下：

- 执行此 DML 的 TiDB 被 kill 后准备退出，且此 DML 对应的事务执行时间超过一个 DDL lease，在事务提交时会报这个错误。
- TiDB 在执行此 DML 时，有一段时间内连不上 PD 或者 TiKV，导致 TiDB 超过一个 DDL lease 时间没有 load schema，或者导致 TiDB 断开与 PD 之间带 keep alive 设置的连接。

### 高并发情况下执行 DDL 时报错的原因？

高并发场景下执行 DDL 语句（比如批量建表）时，极少部分的 DDL 语句可能会由于并发执行时 key 冲突而执行失败。

并发执行 DDL 语句时，建议将 DDL 语句数量保持在 20 以下，否则你需要在应用端重试失败的 DDL 语句。

### DDL 执行被阻塞的原因

在 TiDB v6.2.0 前，TiDB 按照 DDL 语句类型将 DDL 分配到两个先入先出的队列中，即 Reorg DDL 进入 Reorg 队列中，General DDL 进入 general 队列中。由于先入先出以及同一张表上的 DDL 语句需要串行执行，多个 DDL 语句在执行过程中可能会出现阻塞的问题。

例如对于以下 DDL 语句：

- DDL 1：`CREATE INDEX idx on t(a int);`
- DDL 2：`ALTER TABLE t ADD COLUMN b int;`
- DDL 3：`CREATE TABLE t1(a int);`

由于队列先入先出的限制，DDL 3 需要等待 DDL 2 执行。同时又因为同一张表上的 DDL 语句需要串行执行，DDL 2 需要等待 DDL 1 执行。因此，DDL 3 需要等待 DDL 1 先执行完，即使它们操作在不同的表上。

在 TiDB v6.2.0 及之后的版本中，TiDB DDL 模块采用了并发框架。在并发的框架下，不再有同一个队列先进先出的问题，而是从所有 DDL 任务中选出可以执行的 DDL 来执行。并且对 Reorg worker 的数量进行了扩充，大概为节点 `CPU/4`，这使得在并发框架中 TiDB 可以同时为多张表建索引。

无论是新集群还是从旧版本升级的集群，在 TiDB v6.2 及以上版本中，TiDB 都会自动使用并发框架，用户无需进行调整。

### 定位 DDL 执行卡住的问题

1. 先排除 DDL 语句通常执行慢的可能原因。
2. 使用以下任一方法找出 DDL owner 节点：
    + 通过 `curl http://{TiDBIP}:10080/info/all` 获取当前集群的 Owner
    + 通过监控 **DDL** > **DDL META OPM** 查看某个时间段的 Owner

- 如果 Owner 不存在，尝试手动触发 Owner 选举：`curl -X POST http://{TiDBIP}:10080/ddl/owner/resign`。
- 如果 Owner 存在，导出 Goroutine 堆栈并检查可能卡住的地方。

## JDBC 连接所使用的排序规则

本节列出了 JDBC 连接排序规则的相关问题。关于 TiDB 支持的字符集和排序规则，请参考[字符集和排序规则](/character-set-and-collation.md)。

### 当 JDBC URL 中未配置 `connectionCollation` 时，JDBC 连接使用什么排序规则？

当 JDBC URL 中未配置 `connectionCollation` 时，有以下两种场景：

**场景一**：JDBC URL 中 `connectionCollation` 和 `characterEncoding` 均未配置

- 对于 Connector/J8.0.25 及之前版本，JDBC 驱动程序将尝试使用服务器的默认字符集。因为 TiDB 的默认字符集为 `utf8mb4`，驱动程序将使用 `utf8mb4_bin` 作为连接排序规则。
- 对于 Connector/J8.0.26 及之后版本，JDBC 驱动程序将使用 `utf8mb4` 字符集，并根据 `SELECT VERSION()` 的返回值自动选择排序规则。

    - 当返回值小于 `8.0.1` 时，驱动程序使用 `utf8mb4_general_ci` 作为连接排序规则。TiDB 将遵循驱动程序，使用 `utf8mb4_general_ci` 作为排序规则。
    - 当返回值大于等于 `8.0.1` 时，驱动程序使用 `utf8mb4_0900_ai_ci` 作为连接排序规则。v7.4.0 及之后版本的 TiDB 将遵循驱动程序，使用 `utf8mb4_0900_ai_ci` 作为排序规则，而 v7.4.0 之前版本的 TiDB 由于不支持 `utf8mb4_0900_ai_ci` 排序规则，将回退到使用默认的排序规则 `utf8mb4_bin`。

**场景二**：JDBC URL 中配置了 `characterEncoding=utf8` 但未配置 `connectionCollation`，JDBC 驱动程序将按照映射规则使用 `utf8mb4` 字符集，并按照场景一中的描述选择排序规则。

### 如何解决 TiDB 升级后排序规则变化带来的问题？

在 TiDB v7.4 及之前版本中，如果 JDBC URL 中未配置 `connectionCollation`，且 `characterEncoding` 未配置或配置为 `UTF-8`，TiDB [`collation_connection`](/system-variables.md#collation_connection) 变量将默认使用 `utf8mb4_bin` 排序规则。

从 TiDB v7.4 开始，如果 JDBC URL 中未配置 `connectionCollation`，且 `characterEncoding` 未配置或配置为 `UTF-8`，[`collation_connection`](/system-variables.md#collation_connection) 变量值取决于 JDBC 驱动版本。例如，对于 Connector/J8.0.26 及之后版本，JDBC 驱动程序默认使用 `utf8mb4` 字符集，使用 `utf8mb4_general_ci` 作为连接排序规则，TiDB 将遵循驱动程序，[`collation_connection`](/system-variables.md#collation_connection) 变量将使用 `utf8mb4_0900_ai_ci` 排序规则。详情请参考[JDBC 连接的排序规则](#当-jdbc-url-中未配置-connectioncollation-时jdbc-连接使用什么排序规则)。

当从较低版本升级到 v7.4 或更高版本时（例如，从 v6.5 升级到 v7.5），如需保持 JDBC 连接的 `collation_connection` 为 `utf8mb4_bin`，建议在 JDBC URL 中配置 `connectionCollation` 参数。

以下为 TiDB v6.5 中常见的 JDBC URL 配置：

```
spring.datasource.url=JDBC:mysql://{TiDBIP}:{TiDBPort}/{DBName}?characterEncoding=UTF-8&useSSL=false&useServerPrepStmts=true&cachePrepStmts=true&prepStmtCacheSqlLimit=10000&prepStmtCacheSize=1000&useConfigs=maxPerformance&rewriteBatchedStatements=true&defaultFetchSize=-2147483648&allowMultiQueries=true
```

升级到 TiDB v7.4 或更高版本后，建议在 JDBC URL 中配置 `connectionCollation` 参数：

```
spring.datasource.url=JDBC:mysql://{TiDBIP}:{TiDBPort}/{DBName}?characterEncoding=UTF-8&connectionCollation=utf8mb4_bin&useSSL=false&useServerPrepStmts=true&cachePrepStmts=true&prepStmtCacheSqlLimit=10000&prepStmtCacheSize=1000&useConfigs=maxPerformance&rewriteBatchedStatements=true&defaultFetchSize=-2147483648&allowMultiQueries=true
```

### `utf8mb4_bin` 与 `utf8mb4_0900_ai_ci` 排序规则有何区别？

| 排序规则             | 是否区分大小写 | 是否忽略末尾空格 | 是否区分重音 | 比较方式               |
|----------------------|----------------|------------------|--------------|------------------------|
| `utf8mb4_bin`        | 区分           | 忽略             | 区分         | 按二进制编码值比较     |
| `utf8mb4_0900_ai_ci` | 不区分         | 不忽略           | 不区分       | 使用 Unicode 排序算法 |

例如：

```sql
-- utf8mb4_bin 区分大小写
SELECT 'apple' = 'Apple' COLLATE utf8mb4_bin;  -- 返回 0 (FALSE)

-- utf8mb4_0900_ai_ci 不区分大小写
SELECT 'apple' = 'Apple' COLLATE utf8mb4_0900_ai_ci;  -- 返回 1 (TRUE)

-- utf8mb4_bin 忽略末尾空格
SELECT 'Apple ' = 'Apple' COLLATE utf8mb4_bin; -- 返回 1 (TRUE)

-- utf8mb4_0900_ai_ci 不忽略末尾空格
SELECT 'Apple ' = 'Apple' COLLATE utf8mb4_0900_ai_ci; -- 返回 0 (FALSE)

-- utf8mb4_bin 区分重音
SELECT 'café' = 'cafe' COLLATE utf8mb4_bin;  -- 返回 0 (FALSE)

-- utf8mb4_0900_ai_ci 不区分重音
SELECT 'café' = 'cafe' COLLATE utf8mb4_0900_ai_ci;  -- 返回 1 (TRUE)
```

## SQL 优化

### TiDB 执行计划解读

详细解读[理解 TiDB 执行计划](/explain-overview.md)。

### 统计信息收集

详细解读[常规统计信息](/statistics.md)。

### Count 如何加速？

Count 就是暴力扫表，提高并发度能显著提升扫表速度。如要调整并发度，可以使用 `tidb_distsql_scan_concurrency` 变量，但调整并发度需要同时考虑 CPU 和 I/O 资源。TiDB 每次执行查询时，都要访问 TiKV。在数据量小的情况下，MySQL 的数据都在内存里，而 TiDB 还需要进行一次网络访问。

加速建议：

- 提升硬件配置，可以参考[部署建议](/hardware-and-software-requirements.md)。
- 提升并发度，默认是 10，可以尝试提升到 50，但是一般提升幅度在 2-4 倍之间。
- 测试大数据量的 count。
- 调优 TiKV 配置，可以参考[性能调优](/tune-tikv-memory-performance.md)。
- 参考[下推计算结果缓存](/coprocessor-cache.md)。

### 查看当前 DDL 的进度？

通过 `ADMIN SHOW DDL` 语句查看当前 job 进度。操作如下：

```sql
ADMIN SHOW DDL;
```

```sql
*************************** 1. row ***************************
  SCHEMA_VER: 140
       OWNER: 1a1c4174-0fcd-4ba0-add9-12d08c4077dc
RUNNING_JOBS: ID:121, Type:add index, State:running, SchemaState:write reorganization, SchemaID:1, TableID:118, RowCount:77312, ArgLen:0, start time: 2018-12-05 16:26:10.652 +0800 CST, Err:<nil>, ErrCount:0, SnapshotVersion:404749908941733890
     SELF_ID: 1a1c4174-0fcd-4ba0-add9-12d08c4077dc
```

从以上返回结果可知，当前正在处理的是 `ADD INDEX` 操作。且从 `RUNNING_JOBS` 列的 `RowCount` 字段可以知道当前 `ADD INDEX` 操作已经添加了 77312 行索引。

### 如何查看 DDL job？

可以使用 `ADMIN SHOW DDL` 语句查看正在运行的 DDL 作业。

- `ADMIN SHOW DDL JOBS`：用于查看当前 DDL 作业队列中的所有结果（包括正在运行以及等待运行的任务）以及已执行完成的 DDL 作业队列中的最近十条结果。
- `ADMIN SHOW DDL JOBS QUERIES 'job_id' [, 'job_id'] ...`：用于显示 `job_id` 对应的 DDL 任务的原始 SQL 语句。此 `job_id` 只搜索正在执行中的任务以及 DDL 历史作业队列中的最近十条结果。

### TiDB 是否支持基于 COST 的优化 (CBO)？如果支持，实现到什么程度？

是的，TiDB 基于成本的优化器 (CBO) 对代价模型、统计信息进行持续优化。除此之外，TiDB 还支持 hash join、sort-merge join 等 join 算法。

### 如何确定某张表是否需要做 analyze ？

可以通过 `SHOW STATS_HEALTHY` 来查看 Healthy 字段，一般该字段值小于等于 60 的表需要做 analyze。

### SQL 的执行计划展开成了树，ID 的序号有什么规律吗？这棵树的执行顺序会是怎么样的？

ID 没什么规律，只要是唯一就行。不过在生成执行计划时，有一个计数器，生成一个计划 ID 后序号就加 1，执行的顺序和序号无关。整个执行计划是一颗树，执行时从根节点开始，不断地向上返回数据。要理解执行计划，请参考[理解 TiDB 执行计划](/explain-overview.md)。

### TiDB 执行计划中，task cop 在一个 root 下，这个是并行的吗？

目前 TiDB 的计算任务隶属于两种不同的 task：cop task 和 root task。cop task 是指被下推到 KV 端分布式执行的计算任务，root task 是指在 TiDB 端单点执行的计算任务。

一般来讲 root task 的输入数据是来自于 cop task 的，但是 root task 在处理数据的时候，TiKV 上的 cop task 也可以同时处理数据，等待 TiDB 的 root task 拉取。所以从这个过程来看，root task 和 cop task 是并行的，同时存在数据上下游关系。

在执行的过程中，某些时间段也可能是并行的，第一个 cop task 在处理 [100, 200] 的数据，第二个 cop task 在处理 [1, 100] 的数据。执行计划的理解，请参考[理解 TiDB 执行计划](/explain-overview.md)。

## 数据库优化

### TiDB 参数及调整

详情参考 [TiDB 配置参数](/command-line-flags-for-tidb-configuration.md)。

### 如何避免热点问题并实现负载均衡？TiDB 中是否有热分区或热范围问题？

要了解热点问题的场景，请参考[常见热点问题](/troubleshoot-hot-spot-issues.md#常见热点场景)。TiDB 的以下特性旨在帮助解决热点问题：

- [`SHARD_ROW_ID_BITS`](/troubleshoot-hot-spot-issues.md#使用-shard_row_id_bits-处理热点表) 属性。设置该属性后，行 ID 会被打散并写入多个 Region，以缓解写入热点问题。
- [`AUTO_RANDOM`](/troubleshoot-hot-spot-issues.md#使用-auto_random-处理自增主键热点表) 属性，用于解决自增主键带来的热点问题。
- [Coprocessor Cache](/coprocessor-cache.md)，针对小表的读热点问题。
- [Load Base Split](/configure-load-base-split.md)，针对因 Region 访问不均衡（例如小表全表扫）而导致的热点问题。
- [缓存表](/cached-tables.md)，针对被频繁访问但更新较少的小热点表。

如果你遇到因热点引起的性能问题，可参考[处理热点问题](/troubleshoot-hot-spot-issues.md)。

### TiKV 性能参数调优

详情参考 [TiKV 性能参数调优](/tune-tikv-memory-performance.md)。