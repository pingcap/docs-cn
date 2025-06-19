---
title: EXPLAIN 使用教程
summary: 通过示例语句学习如何使用 EXPLAIN
---

# `EXPLAIN` 使用教程

由于 SQL 是一种声明式语言，你无法自动判断查询是否高效执行。你必须首先使用 [`EXPLAIN`](/sql-statements/sql-statement-explain.md) 语句来了解当前的执行计划。

<CustomContent platform="tidb">

以下语句来自 [bikeshare 示例数据库](/import-example-data.md)，用于统计 2017 年 7 月 1 日发生的行程数量：

</CustomContent>

<CustomContent platform="tidb-cloud">

以下语句来自 [bikeshare 示例数据库](/tidb-cloud/import-sample-data.md)，用于统计 2017 年 7 月 1 日发生的行程数量：

</CustomContent>

{{< copyable "sql" >}}

```sql
EXPLAIN SELECT count(*) FROM trips WHERE start_date BETWEEN '2017-07-01 00:00:00' AND '2017-07-01 23:59:59';
```

```sql
+------------------------------+----------+-----------+---------------+------------------------------------------------------------------------------------------------------------------------+
| id                           | estRows  | task      | access object | operator info                                                                                                          |
+------------------------------+----------+-----------+---------------+------------------------------------------------------------------------------------------------------------------------+
| StreamAgg_20                 | 1.00     | root      |               | funcs:count(Column#13)->Column#11                                                                                      |
| └─TableReader_21             | 1.00     | root      |               | data:StreamAgg_9                                                                                                       |
|   └─StreamAgg_9              | 1.00     | cop[tikv] |               | funcs:count(1)->Column#13                                                                                              |
|     └─Selection_19           | 250.00   | cop[tikv] |               | ge(bikeshare.trips.start_date, 2017-07-01 00:00:00.000000), le(bikeshare.trips.start_date, 2017-07-01 23:59:59.000000) |
|       └─TableFullScan_18     | 10000.00 | cop[tikv] | table:trips   | keep order:false, stats:pseudo                                                                                         |
+------------------------------+----------+-----------+---------------+------------------------------------------------------------------------------------------------------------------------+
5 rows in set (0.00 sec)
```

从子运算符 `└─TableFullScan_18` 开始回溯，你可以看到其执行过程如下，目前这个执行计划并不是最优的：

1. 协处理器（TiKV）通过 `TableFullScan` 操作读取整个 `trips` 表。然后将读取的行传递给仍在 TiKV 中的 `Selection_19` 运算符。
2. `WHERE start_date BETWEEN ..` 谓词在 `Selection_19` 运算符中进行过滤。估计约有 `250` 行满足这个选择条件。注意，这个数字是根据统计信息和运算符的逻辑估算的。`└─TableFullScan_18` 运算符显示 `stats:pseudo`，这表示该表没有实际的统计信息。在运行 `ANALYZE TABLE trips` 收集统计信息后，预计统计数据会更准确。
3. 对满足选择条件的行应用 `count` 函数。这也在仍在 TiKV 中的 `StreamAgg_9` 运算符内完成（`cop[tikv]`）。TiKV 协处理器可以执行多个 MySQL 内置函数，`count` 就是其中之一。
4. `StreamAgg_9` 的结果然后发送到现在位于 TiDB 服务器内（任务为 `root`）的 `TableReader_21` 运算符。该运算符的 `estRows` 列值为 `1`，这表示运算符将从每个要访问的 TiKV Region 接收一行。有关这些请求的更多信息，请参见 [`EXPLAIN ANALYZE`](/sql-statements/sql-statement-explain-analyze.md)。
5. `StreamAgg_20` 运算符然后对来自 `└─TableReader_21` 运算符的每一行应用 `count` 函数，从 [`SHOW TABLE REGIONS`](/sql-statements/sql-statement-show-table-regions.md) 可以看到大约有 56 行。由于这是根运算符，它随后将结果返回给客户端。

> **注意：**
>
> 要查看表包含的 Region 的概览，请执行 [`SHOW TABLE REGIONS`](/sql-statements/sql-statement-show-table-regions.md)。

## 评估当前性能

`EXPLAIN` 只返回查询执行计划但不执行查询。要获取实际执行时间，你可以执行查询或使用 `EXPLAIN ANALYZE`：

{{< copyable "sql" >}}

```sql
EXPLAIN ANALYZE SELECT count(*) FROM trips WHERE start_date BETWEEN '2017-07-01 00:00:00' AND '2017-07-01 23:59:59';
```

```sql
+------------------------------+----------+----------+-----------+---------------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+------------------------------------------------------------------------------------------------------------------------+-----------+------+
| id                           | estRows  | actRows  | task      | access object | execution info                                                                                                                                                                                                                                    | operator info                                                                                                          | memory    | disk |
+------------------------------+----------+----------+-----------+---------------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+------------------------------------------------------------------------------------------------------------------------+-----------+------+
| StreamAgg_20                 | 1.00     | 1        | root      |               | time:1.031417203s, loops:2                                                                                                                                                                                                                        | funcs:count(Column#13)->Column#11                                                                                      | 632 Bytes | N/A  |
| └─TableReader_21             | 1.00     | 56       | root      |               | time:1.031408123s, loops:2, cop_task: {num: 56, max: 782.147269ms, min: 5.759953ms, avg: 252.005927ms, p95: 609.294603ms, max_proc_keys: 910371, p95_proc_keys: 704775, tot_proc: 11.524s, tot_wait: 580ms, rpc_num: 56, rpc_time: 14.111932641s} | data:StreamAgg_9                                                                                                       | 328 Bytes | N/A  |
|   └─StreamAgg_9              | 1.00     | 56       | cop[tikv] |               | proc max:640ms, min:8ms, p80:276ms, p95:480ms, iters:18695, tasks:56                                                                                                                                                                              | funcs:count(1)->Column#13                                                                                              | N/A       | N/A  |
|     └─Selection_19           | 250.00   | 11409    | cop[tikv] |               | proc max:640ms, min:8ms, p80:276ms, p95:476ms, iters:18695, tasks:56                                                                                                                                                                              | ge(bikeshare.trips.start_date, 2017-07-01 00:00:00.000000), le(bikeshare.trips.start_date, 2017-07-01 23:59:59.000000) | N/A       | N/A  |
|       └─TableFullScan_18     | 10000.00 | 19117643 | cop[tikv] | table:trips   | proc max:612ms, min:8ms, p80:248ms, p95:460ms, iters:18695, tasks:56                                                                                                                                                                              | keep order:false, stats:pseudo                                                                                         | N/A       | N/A  |
+------------------------------+----------+----------+-----------+---------------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+------------------------------------------------------------------------------------------------------------------------+-----------+------+
5 rows in set (1.03 sec)
```

上面的示例查询执行需要 `1.03` 秒，这并不是理想的性能。

从上面 `EXPLAIN ANALYZE` 的结果中，`actRows` 表明一些估计值（`estRows`）不准确（预期 1 万行但实际找到 1900 万行），这在 `└─TableFullScan_18` 的 `operator info`（`stats:pseudo`）中已经有所提示。如果你先运行 [`ANALYZE TABLE`](/sql-statements/sql-statement-analyze-table.md) 然后再次运行 `EXPLAIN ANALYZE`，你会看到估计值更接近实际值：

{{< copyable "sql" >}}

```sql
ANALYZE TABLE trips;
EXPLAIN ANALYZE SELECT count(*) FROM trips WHERE start_date BETWEEN '2017-07-01 00:00:00' AND '2017-07-01 23:59:59';
```

```sql
Query OK, 0 rows affected (10.22 sec)

+------------------------------+-------------+----------+-----------+---------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+------------------------------------------------------------------------------------------------------------------------+-----------+------+
| id                           | estRows     | actRows  | task      | access object | execution info                                                                                                                                                                                                                                   | operator info                                                                                                          | memory    | disk |
+------------------------------+-------------+----------+-----------+---------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+------------------------------------------------------------------------------------------------------------------------+-----------+------+
| StreamAgg_20                 | 1.00        | 1        | root      |               | time:926.393612ms, loops:2                                                                                                                                                                                                                       | funcs:count(Column#13)->Column#11                                                                                      | 632 Bytes | N/A  |
| └─TableReader_21             | 1.00        | 56       | root      |               | time:926.384792ms, loops:2, cop_task: {num: 56, max: 850.94424ms, min: 6.042079ms, avg: 234.987725ms, p95: 495.474806ms, max_proc_keys: 910371, p95_proc_keys: 704775, tot_proc: 10.656s, tot_wait: 904ms, rpc_num: 56, rpc_time: 13.158911952s} | data:StreamAgg_9                                                                                                       | 328 Bytes | N/A  |
|   └─StreamAgg_9              | 1.00        | 56       | cop[tikv] |               | proc max:592ms, min:4ms, p80:244ms, p95:480ms, iters:18695, tasks:56                                                                                                                                                                             | funcs:count(1)->Column#13                                                                                              | N/A       | N/A  |
|     └─Selection_19           | 432.89      | 11409    | cop[tikv] |               | proc max:592ms, min:4ms, p80:244ms, p95:480ms, iters:18695, tasks:56                                                                                                                                                                             | ge(bikeshare.trips.start_date, 2017-07-01 00:00:00.000000), le(bikeshare.trips.start_date, 2017-07-01 23:59:59.000000) | N/A       | N/A  |
|       └─TableFullScan_18     | 19117643.00 | 19117643 | cop[tikv] | table:trips   | proc max:564ms, min:4ms, p80:228ms, p95:456ms, iters:18695, tasks:56                                                                                                                                                                             | keep order:false                                                                                                       | N/A       | N/A  |
+------------------------------+-------------+----------+-----------+---------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+------------------------------------------------------------------------------------------------------------------------+-----------+------+
5 rows in set (0.93 sec)
```

执行 `ANALYZE TABLE` 后，你可以看到 `└─TableFullScan_18` 运算符的估计行数是准确的，`└─Selection_19` 的估计值现在也更接近实际值。在上述两种情况下，虽然执行计划（TiDB 用于执行此查询的运算符集）没有改变，但不理想的执行计划通常是由过时的统计信息导致的。

除了 `ANALYZE TABLE`，TiDB 还会在达到 [`tidb_auto_analyze_ratio`](/system-variables.md#tidb_auto_analyze_ratio) 阈值后自动在后台重新生成统计信息。你可以通过执行 [`SHOW STATS_HEALTHY`](/sql-statements/sql-statement-show-stats-healthy.md) 语句来查看 TiDB 距离这个阈值有多近（TiDB 认为统计信息的健康程度）：

{{< copyable "sql" >}}

```sql
SHOW STATS_HEALTHY;
```

```sql
+-----------+------------+----------------+---------+
| Db_name   | Table_name | Partition_name | Healthy |
+-----------+------------+----------------+---------+
| bikeshare | trips      |                |     100 |
+-----------+------------+----------------+---------+
1 row in set (0.00 sec)
```

## 识别优化机会

当前执行计划在以下方面是高效的：

* 大部分工作在 TiKV 协处理器内处理。只有 56 行数据需要通过网络发送回 TiDB 进行处理。每一行都很短，只包含匹配选择条件的计数。

* 在 TiDB (`StreamAgg_20`) 和 TiKV (`└─StreamAgg_9`) 中聚合行数都使用了流式聚合，这在内存使用上非常高效。

当前执行计划最大的问题是谓词 `start_date BETWEEN '2017-07-01 00:00:00' AND '2017-07-01 23:59:59'` 没有立即应用。所有行都先通过 `TableFullScan` 运算符读取，然后才应用选择条件。你可以从 `SHOW CREATE TABLE trips` 的输出中找出原因：

{{< copyable "sql" >}}

```sql
SHOW CREATE TABLE trips\G
```

```sql
*************************** 1. row ***************************
       Table: trips
Create Table: CREATE TABLE `trips` (
  `trip_id` bigint(20) NOT NULL AUTO_INCREMENT,
  `duration` int(11) NOT NULL,
  `start_date` datetime DEFAULT NULL,
  `end_date` datetime DEFAULT NULL,
  `start_station_number` int(11) DEFAULT NULL,
  `start_station` varchar(255) DEFAULT NULL,
  `end_station_number` int(11) DEFAULT NULL,
  `end_station` varchar(255) DEFAULT NULL,
  `bike_number` varchar(255) DEFAULT NULL,
  `member_type` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`trip_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin AUTO_INCREMENT=20477318
1 row in set (0.00 sec)
```

`start_date` 列上**没有**索引。你需要一个索引才能将这个谓词推入索引读取运算符。添加索引的方法如下：

{{< copyable "sql" >}}

```sql
ALTER TABLE trips ADD INDEX (start_date);
```

```sql
Query OK, 0 rows affected (2 min 10.23 sec)
```

> **注意：**
>
> 你可以使用 [`ADMIN SHOW DDL JOBS`](/sql-statements/sql-statement-admin-show-ddl.md) 命令监控 DDL 作业的进度。TiDB 的默认设置经过精心选择，以确保添加索引不会对生产工作负载产生太大影响。对于测试环境，考虑增加 [`tidb_ddl_reorg_batch_size`](/system-variables.md#tidb_ddl_reorg_batch_size) 和 [`tidb_ddl_reorg_worker_cnt`](/system-variables.md#tidb_ddl_reorg_worker_cnt) 的值。在参考系统上，批量大小为 `10240` 和工作线程数为 `32` 可以实现比默认值高 10 倍的性能提升。

添加索引后，你可以再次使用 `EXPLAIN` 查询。在下面的输出中，你可以看到选择了一个新的执行计划，`TableFullScan` 和 `Selection` 运算符已被消除：

{{< copyable "sql" >}}

```sql
EXPLAIN SELECT count(*) FROM trips WHERE start_date BETWEEN '2017-07-01 00:00:00' AND '2017-07-01 23:59:59';
```

```sql
+-----------------------------+---------+-----------+-------------------------------------------+-------------------------------------------------------------------+
| id                          | estRows | task      | access object                             | operator info                                                     |
+-----------------------------+---------+-----------+-------------------------------------------+-------------------------------------------------------------------+
| StreamAgg_17                | 1.00    | root      |                                           | funcs:count(Column#13)->Column#11                                 |
| └─IndexReader_18            | 1.00    | root      |                                           | index:StreamAgg_9                                                 |
|   └─StreamAgg_9             | 1.00    | cop[tikv] |                                           | funcs:count(1)->Column#13                                         |
|     └─IndexRangeScan_16     | 8471.88 | cop[tikv] | table:trips, index:start_date(start_date) | range:[2017-07-01 00:00:00,2017-07-01 23:59:59], keep order:false |
+-----------------------------+---------+-----------+-------------------------------------------+-------------------------------------------------------------------+
4 rows in set (0.00 sec)
```

要比较实际执行时间，你可以再次使用 [`EXPLAIN ANALYZE`](/sql-statements/sql-statement-explain-analyze.md)：

{{< copyable "sql" >}}

```sql
EXPLAIN ANALYZE SELECT count(*) FROM trips WHERE start_date BETWEEN '2017-07-01 00:00:00' AND '2017-07-01 23:59:59';
```

```sql
+-----------------------------+---------+---------+-----------+-------------------------------------------+------------------------------------------------------------------------------------------------------------------+-------------------------------------------------------------------+-----------+------+
| id                          | estRows | actRows | task      | access object                             | execution info                                                                                                   | operator info                                                     | memory    | disk |
+-----------------------------+---------+---------+-----------+-------------------------------------------+------------------------------------------------------------------------------------------------------------------+-------------------------------------------------------------------+-----------+------+
| StreamAgg_17                | 1.00    | 1       | root      |                                           | time:4.516728ms, loops:2                                                                                         | funcs:count(Column#13)->Column#11                                 | 372 Bytes | N/A  |
| └─IndexReader_18            | 1.00    | 1       | root      |                                           | time:4.514278ms, loops:2, cop_task: {num: 1, max:4.462288ms, proc_keys: 11409, rpc_num: 1, rpc_time: 4.457148ms} | index:StreamAgg_9                                                 | 238 Bytes | N/A  |
|   └─StreamAgg_9             | 1.00    | 1       | cop[tikv] |                                           | time:4ms, loops:12                                                                                               | funcs:count(1)->Column#13                                         | N/A       | N/A  |
|     └─IndexRangeScan_16     | 8471.88 | 11409   | cop[tikv] | table:trips, index:start_date(start_date) | time:4ms, loops:12                                                                                               | range:[2017-07-01 00:00:00,2017-07-01 23:59:59], keep order:false | N/A       | N/A  |
+-----------------------------+---------+---------+-----------+-------------------------------------------+------------------------------------------------------------------------------------------------------------------+-------------------------------------------------------------------+-----------+------+
4 rows in set (0.00 sec)
```

从上面的结果可以看出，查询时间从 1.03 秒减少到了 0.0 秒。

> **注意：**
>
> 这里还有另一个优化选项是协处理器缓存。如果你无法添加索引，可以考虑启用[协处理器缓存](/coprocessor-cache.md)。启用后，只要自上次执行运算符以来 Region 没有被修改，TiKV 就会返回缓存中的值。这也将有助于减少昂贵的 `TableFullScan` 和 `Selection` 运算符的大部分开销。

## 禁用子查询的提前执行

在查询优化过程中，TiDB 会提前执行可以直接计算的子查询。例如：

```sql
CREATE TABLE t1(a int);
INSERT INTO t1 VALUES(1);
CREATE TABLE t2(a int);
EXPLAIN SELECT * FROM t2 WHERE a = (SELECT a FROM t1);
```

```sql
+--------------------------+----------+-----------+---------------+--------------------------------+
| id                       | estRows  | task      | access object | operator info                  |
+--------------------------+----------+-----------+---------------+--------------------------------+
| TableReader_14           | 10.00    | root      |               | data:Selection_13              |
| └─Selection_13           | 10.00    | cop[tikv] |               | eq(test.t2.a, 1)               |
|   └─TableFullScan_12     | 10000.00 | cop[tikv] | table:t2      | keep order:false, stats:pseudo |
+--------------------------+----------+-----------+---------------+--------------------------------+
3 rows in set (0.00 sec)
```

在上面的例子中，`a = (SELECT a FROM t1)` 子查询在优化过程中被计算并重写为 `t2.a=1`。这允许在优化过程中进行更多优化，如常量传播和折叠。但是，这会影响 `EXPLAIN` 语句的执行时间。当子查询本身需要很长时间执行时，`EXPLAIN` 语句可能无法完成，这可能会影响在线故障排除。

从 v7.3.0 开始，TiDB 引入了 [`tidb_opt_enable_non_eval_scalar_subquery`](/system-variables.md#tidb_opt_enable_non_eval_scalar_subquery-new-in-v730) 系统变量，用于控制是否在 `EXPLAIN` 中禁用此类子查询的提前执行。该变量的默认值为 `OFF`，表示会提前计算子查询。你可以将此变量设置为 `ON` 来禁用子查询的提前执行：

```sql
SET @@tidb_opt_enable_non_eval_scalar_subquery = ON;
EXPLAIN SELECT * FROM t2 WHERE a = (SELECT a FROM t1);
```

```sql
+---------------------------+----------+-----------+---------------+---------------------------------+
| id                        | estRows  | task      | access object | operator info                   |
+---------------------------+----------+-----------+---------------+---------------------------------+
| Selection_13              | 8000.00  | root      |               | eq(test.t2.a, ScalarQueryCol#5) |
| └─TableReader_15          | 10000.00 | root      |               | data:TableFullScan_14           |
|   └─TableFullScan_14      | 10000.00 | cop[tikv] | table:t2      | keep order:false, stats:pseudo  |
| ScalarSubQuery_10         | N/A      | root      |               | Output: ScalarQueryCol#5        |
| └─MaxOneRow_6             | 1.00     | root      |               |                                 |
|   └─TableReader_9         | 1.00     | root      |               | data:TableFullScan_8            |
|     └─TableFullScan_8     | 1.00     | cop[tikv] | table:t1      | keep order:false, stats:pseudo  |
+---------------------------+----------+-----------+---------------+---------------------------------+
7 rows in set (0.00 sec)
```

如你所见，标量子查询在执行过程中没有被展开，这使得更容易理解此类 SQL 的具体执行过程。

> **注意：**
>
> [`tidb_opt_enable_non_eval_scalar_subquery`](/system-variables.md#tidb_opt_enable_non_eval_scalar_subquery-new-in-v730) 只影响 `EXPLAIN` 语句的行为，`EXPLAIN ANALYZE` 语句仍然会提前执行子查询。
