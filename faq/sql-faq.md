---
title: SQL 操作常见问题
summary: 介绍 SQL 操作相关的常见问题。
aliases: ['/docs-cn/dev/faq/sql-faq/']
---

# SQL 操作常见问题

本文档介绍 TiDB 中常见的 SQL 操作问题。

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

如果 `ORDER BY` 中使用的列不是唯一列，该语句就不确定返回结果的顺序。以下示例中，`a` 列有重复值，因此只有 `ORDER BY a, b` 能确定返回结果的顺序。

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

```sql
> select * from t order by a; -- 能确定 a 列的顺序，不确定 b 列的顺序
+------+------+
| a    | b    |
+------+------+
|    1 |    1 |
|    2 |    2 |
|    2 |    1 |
+------+------+
3 rows in set (0.00 sec)
```

## TiDB 是否支持 `SELECT FOR UPDATE`？

支持。当 TiDB 使用悲观锁（自 TiDB v3.0 起默认使用）时，TiDB 中 `SELECT FOR UPDATE` 的行为与 MySQL 中的基本一致。

当 TiDB 使用乐观锁时，`SELECT FOR UPDATE` 不会在事务启动时对数据加锁，而是在提交事务时检查冲突。如果检查出冲突，会回滚待提交的事务。

## TiDB 的 codec 能保证 UTF8 的字符串是 memcomparable 的吗？我们的 key 需要支持 UTF8，有什么编码建议吗？

TiDB 字符集默认就是 UTF8 而且目前只支持 UTF8，字符串就是 memcomparable 格式的。

## 一个事务中的语句数量最大是多少？

一个事务中的语句数量，默认限制最大为 5000 条。

## TiDB 中，为什么出现后插入数据的自增 ID 反而小？

TiDB 的自增 ID (`AUTO_INCREMENT`) 只保证自增且唯一，并不保证连续分配。TiDB 目前采用批量分配的方式，所以如果在多台 TiDB 上同时插入数据，分配的自增 ID 会不连续。当多个线程并发往不同的 TiDB-server 插入数据的时候，有可能会出现后插入的数据自增 ID 小的情况。此外，TiDB 允许给整型类型的字段指定 AUTO_INCREMENT，且一个表只允许一个属性为 `AUTO_INCREMENT` 的字段。详情可参考 [CREATE TABLE 语法](/mysql-compatibility.md#自增-id)。

## 如何在 TiDB 中修改 `sql_mode`？

TiDB 支持将 [`sql_mode`](/sql-mode.md) 作为[系统变量](/system-variables.md#sql_mode)修改，与 MySQL 一致。目前，TiDB 不支持在配置文件中修改 `sql_mode`，但使用 [`SET GLOBAL`](/sql-statements/sql-statement-set-variable.md) 对系统变量的修改将应用于集群中的所有 TiDB server，并且重启后更改依然有效。

## 用 Sqoop 批量写入 TiDB 数据，虽然配置了 `--batch` 选项，但还是会遇到 `java.sql.BatchUpdateExecption:statement count 5001 exceeds the transaction limitation` 的错误，该如何解决？

- 在 Sqoop 中，`--batch` 是指每个批次提交 100 条 statement，但是默认每个 statement 包含 100 条 SQL 语句，所以此时 100 * 100 = 10000 条 SQL 语句，超出了 TiDB 的事务限制 5000 条，可以增加选项 `-Dsqoop.export.records.per.statement=10` 来解决这个问题，完整的用法如下：

    {{< copyable "shell-regular" >}}

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

- 也可以选择增大 TiDB 的单个事物语句数量限制，不过此操作会导致内存增加。

## TiDB 有像 Oracle 那样的 Flashback Query 功能么，DDL 支持么？

有，也支持 DDL。详细参考 [TiDB 历史数据回溯](/read-historical-data.md)。

## TiDB 中删除数据后会立即释放空间吗？

DELETE，TRUNCATE 和 DROP 都不会立即释放空间。对于 TRUNCATE 和 DROP 操作，在达到 TiDB 的 GC (garbage collection) 时间后（默认 10 分钟），TiDB 的 GC 机制会删除数据并释放空间。对于 DELETE 操作 TiDB 的 GC 机制会删除数据，但不会立即释放空间，而是当后续进行 compaction 时释放空间。


## TiDB 是否支持 `REPLACE INTO` 语法？

支持，例外是当前 `LOAD DATA` 不支持 `REPLACE INTO` 语法。

## 数据删除后查询速度为何会变慢？

大量删除数据后，会有很多无用的 key 存在，影响查询效率。可以尝试开启 [Region Merge](/best-practices/massive-regions-best-practices.md#方法五开启-region-merge) 功能，具体看参考[最佳实践](https://pingcap.com/blog-cn/tidb-best-practice/)中的删除数据部分。

## 对数据做删除操作之后，空间回收比较慢，如何处理？

TiDB 采用了多版本并发控制 (MVCC)，为了使并发事务能查看到早期版本的数据，删除数据不会立即回收空间，而是推迟一段时间后再进行垃圾回收 (GC)。你可以通过修改系统变量 [`tidb_gc_life_time`](/system-variables.md#tidb_gc_life_time-从-v50-版本开始引入)的值（默认值为 `10m0s`）配置历史数据的保留时限。

## `SHOW PROCESSLIST` 是否显示系统进程号？

TiDB 的 `SHOW PROCESSLIST` 与 MySQL 的 `SHOW PROCESSLIST` 显示内容基本一样，不会显示系统进程号，而 ID 表示当前的 session ID。其中 TiDB 的 `show processlist` 和 MySQL 的 `show processlist` 区别如下：

+ 由于 TiDB 是分布式数据库，TiDB server 实例是无状态的 SQL 解析和执行引擎（详情可参考 [TiDB 整体架构](/tidb-architecture.md)），用户使用 MySQL 客户端登录的是哪个 TiDB server ，`show processlist` 就会显示当前连接的这个 TiDB server 中执行的 session 列表，不是整个集群中运行的全部 session 列表；而 MySQL 是单机数据库，`show processlist` 列出的是当前整个 MySQL 数据库的全部执行 SQL 列表。

+ 在查询执行期间，TiDB 中的 `State` 列不会持续更新。由于 TiDB 支持并行查询，每个语句可能同时处于多个状态，因此很难显示为某一种状态。

## 在 TiDB 中如何控制或改变 SQL 提交的执行优先级？

TiDB 支持改变 [per-session](/system-variables.md#tidb_force_priority)、[全局](/tidb-configuration-file.md#force-priority)或单个语句的优先级。优先级包括：

- HIGH_PRIORITY：该语句为高优先级语句，TiDB 在执行阶段会优先处理这条语句
- LOW_PRIORITY：该语句为低优先级语句，TiDB 在执行阶段会降低这条语句的优先级

以上两种参数可以结合 TiDB 的 DML 语言进行使用，使用方法举例如下：

1. 通过在数据库中写 SQL 的方式来调整优先级：

    {{< copyable "sql" >}}

    ```sql
    select HIGH_PRIORITY | LOW_PRIORITY count(*) from table_name;
    insert HIGH_PRIORITY | LOW_PRIORITY into table_name insert_values;
    delete HIGH_PRIORITY | LOW_PRIORITY from table_name;
    update HIGH_PRIORITY | LOW_PRIORITY table_reference set assignment_list where where_condition;
    replace HIGH_PRIORITY | LOW_PRIORITY into table_name;
    ```

2. 全表扫会自动调整为低优先级，analyze 也是默认低优先级。

## 在 TiDB 中 auto analyze 的触发策略是怎样的？

触发策略：新表达到 1000 条，并且在 1 分钟内没有写入，会自动触发。

当表的（修改数/当前总行数）大于 `tidb_auto_analyze_ratio` 的时候，会自动触发 `analyze` 语句。`tidb_auto_analyze_ratio` 的默认值为 0.5，即默认开启此功能。为了保险起见，在开启此功能的时候，保证了其最小值为 0.3。但是不能大于等于 `pseudo-estimate-ratio`（默认值为 0.8），否则会有一段时间使用 pseudo 统计信息，建议设置值为 0.5。

## 可以使用 Hints 控制优化器行为吗？

在 TiDB 中，你可以用多种方法控制查询优化器的默认行为，包括使用 [Optimizer Hints](/optimizer-hints.md) 和 [SQL 执行计划管理 (SPM)](/sql-plan-management.md)。基本用法同 MySQL 中的一致，还包含若干 TiDB 特有的用法，示例如下：`select column_name from table_name use index（index_name）where where_condition;`

## 触发 Information schema is changed 错误的原因？

TiDB 在执行 SQL 语句时，会使用当时的 `schema` 来处理该 SQL 语句，而且 TiDB 支持在线异步变更 DDL。那么，在执行 DML 的时候可能有 DDL 语句也在执行，而你需要确保每个 SQL 语句在同一个 `schema` 上执行。所以当执行 DML 时，遇到正在执行中的 DDL 操作就可能会报 `Information schema is changed` 的错误。为了避免太多的 DML 语句报错，已做了一些优化。

现在会报此错的可能原因如下（只有第一个报错原因与表有关）：

- 执行的 DML 语句中涉及的表和集群中正在执行的 DDL 的表有相同的，那么这个 DML 语句就会报此错。
- 这个 DML 执行时间很久，而这段时间内执行了很多 DDL 语句，导致中间 `schema` 版本变更次数超过 1024 （此为默认值，可以通过 `tidb_max_delta_schema_count` 变量修改）。
- 接受 DML 请求的 TiDB 长时间不能加载到 `schema information`（TiDB 与 PD 或 TiKV 之间的网络连接故障等会导致此问题），而这段时间内执行了很多 DDL 语句，导致中间 `schema` 版本变更次数超过 100。
- TiDB 重启后执行第一个 DDL 操作前，执行 DML 操作，并且在执行过程中遇到了第 1 个 DDL 操作（即在执行第 1 个 DDL 操作前，启动该 DML 对应的事务，且在该 DDL 变更第一个 `schema` 版本后，提交该 DML 对应的事务），那么这个 DML 会报此错。

> **注意：**
>
> + 目前 TiDB 未缓存所有的 `schema` 版本信息。
> + 对于每个 DDL 操作，`schema` 版本变更的数量与对应 `schema state` 变更的次数一致。
> + 不同的 DDL 操作版本变更次数不一样。例如，`create table` 操作会有 1 次 `schema` 版本变更；`add column` 操作有 4 次 `schema` 版本变更。

## 触发 Information schema is out of date 错误的原因？

当执行 DML 时，TiDB 超过一个 DDL lease 时间（默认 45s）没能加载到最新的 schema 就可能会报 `Information schema is out of date` 的错误。遇到此错的可能原因如下：

- 执行此 DML 的 TiDB 被 kill 后准备退出，且此 DML 对应的事务执行时间超过一个 DDL lease，在事务提交时会报这个错误。
- TiDB 在执行此 DML 时，有一段时间内连不上 PD 或者 TiKV，导致 TiDB 超过一个 DDL lease 时间没有 load schema，或者导致 TiDB 断开与 PD 之间带 keep alive 设置的连接。

## 高并发情况下执行 DDL 时报错的原因？

高并发情况下执行 DDL（比如批量建表）时，极少部分 DDL 可能会由于并发执行时 key 冲突而执行失败。

并发执行 DDL 时，建议将 DDL 数量保持在 20 以下，否则你需要在应用端重试失败的 DDL 语句。

## SQL 优化

### TiDB 执行计划解读

详细解读[理解 TiDB 执行计划](/explain-overview.md)。

### 统计信息收集

详细解读[统计信息](/statistics.md)。

### Count 如何加速？

Count 就是暴力扫表，提高并发度能显著的提升速度，修改并发度可以参考 `tidb_distsql_scan_concurrency` 变量，但是也要看 CPU 和 I/O 资源。TiDB 每次查询都要访问 TiKV，在数据量小的情况下，MySQL 都在内存里，TiDB 还需要进行一次网络访问。

提升建议：

- 建议提升硬件配置，可以参考[部署建议](/hardware-and-software-requirements.md)。
- 提升并发度，默认是 10，可以提升到 50 试试，但是一般提升在 2-4 倍之间。
- 测试大数据量的 count。
- 调优 TiKV 配置，可以参考[性能调优](/tune-tikv-memory-performance.md)。
- 可以参考[下推计算结果缓存](/coprocessor-cache.md)。

### 查看当前 DDL 的进度？

通过 `admin show ddl` 查看当前 job 进度。操作如下：

{{< copyable "sql" >}}

```sql
admin show ddl;
```

```sql
*************************** 1. row ***************************
  SCHEMA_VER: 140
       OWNER: 1a1c4174-0fcd-4ba0-add9-12d08c4077dc
RUNNING_JOBS: ID:121, Type:add index, State:running, SchemaState:write reorganization, SchemaID:1, TableID:118, RowCount:77312, ArgLen:0, start time: 2018-12-05 16:26:10.652 +0800 CST, Err:<nil>, ErrCount:0, SnapshotVersion:404749908941733890
     SELF_ID: 1a1c4174-0fcd-4ba0-add9-12d08c4077dc
```

从上面操作结果可知，当前正在处理的是 `add index` 操作。且从 `RUNNING_JOBS` 列的 `RowCount` 字段可以知道当前 `add index` 操作已经添加了 77312 行索引。

### 如何查看 DDL job？

可以使用 `admin show ddl` 语句查看正在运行的 DDL 作业。

- `admin show ddl jobs`：用于查看当前 DDL 作业队列中的所有结果（包括正在运行以及等待运行的任务）以及已执行完成的 DDL 作业队列中的最近十条结果。
- `admin show ddl job queries 'job_id' [, 'job_id'] ...`：用于显示 `job_id` 对应的 DDL 任务的原始 SQL 语句。此 `job_id` 只搜索正在执行中的任务以及 DDL 历史作业队列中的最近十条结果。

### TiDB 是否支持基于 COST 的优化 (CBO)，如果支持，实现到什么程度？

是的，TiDB 使用的是基于成本的优化器 (CBO)，会对代价模型、统计信息持续优化。除此之外，TiDB 还支持 hash join、soft-merge join 等 join 算法。

### 如何确定某张表是否需要做 analyze ？

可以通过 `show stats_healthy` 来查看 Healthy 字段，一般小于等于 60 的表需要做 analyze。

### SQL 的执行计划展开成了树，ID 的序号有什么规律吗？这棵树的执行顺序会是怎么样的？

ID 没什么规律，只要是唯一就行。不过生成的时候，是有一个计数器，生成一个 plan 就加一，执行的顺序和序号无关。整个执行计划是一颗树，执行时从根节点开始，不断地向上返回数据。执行计划的理解，请参考[理解 TiDB 执行计划](/explain-overview.md)。

### TiDB 执行计划中，task cop 在一个 root 下，这个是并行的么？

目前 TiDB 的计算任务隶属于两种不同的 task：cop task 和 root task。cop task 是指被下推到 KV 端分布式执行的计算任务，root task 是指在 TiDB 端单点执行的计算任务。

一般来讲 root task 的输入数据是来自于 cop task 的，但是 root task 在处理数据的时候，TiKV 上的 cop task 也可以同时处理数据，等待 TiDB 的 root task 拉取。所以从上述观点来看，他们是并行的，同时存在数据上下游关系。

在执行的过程中，某些时间段其实也是并行的，第一个 cop task 在处理 [100, 200] 的数据，第二个 cop task 在处理 [1, 100] 的数据。执行计划的理解，请参考[理解 TiDB 执行计划](/explain-overview.md)。

## 数据库优化

### TiDB 参数及调整

详情参考 [TiDB 配置参数](/command-line-flags-for-tidb-configuration.md)。

### 如何打散热点

TiDB 中以 Region 分片来管理数据库，通常来讲，TiDB 的热点指的是 Region 的读写访问热点。而 TiDB 中对于非整数主键或没有主键的表，可以通过设置 `SHARD_ROW_ID_BITS` 来适度分解 Region 分片，以达到打散 Region 热点的效果。详情可参考官网 [SHARD_ROW_ID_BITS](/shard-row-id-bits.md) 中的介绍。

### TiKV 性能参数调优

详情参考 [TiKV 性能参数调优](/tune-tikv-memory-performance.md)。
