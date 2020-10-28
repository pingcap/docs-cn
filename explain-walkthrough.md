---
title: EXPLAIN Walkthrough
summary: Learn how to use EXPLAIN by walking through an example statement
---

# `EXPLAIN` Walkthrough

Because SQL is a declarative language, you cannot automatically tell whether a query is executed efficiently. You must first use the [`EXPLAIN`](/sql-statements/sql-statement-explain.md) statement to learn the current execution plan.

The following statement from the [bikeshare example database](/import-example-data.md) counts how many trips were taken on the 1st July 2017:

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

From the child operator `└─TableFullScan_18` back, you can see its execution process as follows, which is currently suboptimal:

1. The coprocessor (TiKV) reads the entire `trips` table as a `TableFullScan` operation. It then passes the rows that it reads to the `Selection_19` operator, which is still within TiKV.
2. The `WHERE start_date BETWEEN ..` predicate is then filtered in the `Selection_19` operator. Approximately `250` rows are estimated to meet this selection. Note that this number is estimated according to the statistics and the operator's logic. The `└─TableFullScan_18` operator shows `stats:pseudo`, which means that the table does not have the actual statistical information. After running `ANALYZE TABLE trips` to collect statistical information, the statistics are expected to be more accurate.
3. The rows that meet the selection criteria then have a `count` function applied to them. This is also completed inside the `StreamAgg_9` operator, which is still inside TiKV (`cop[tikv]`). The TiKV coprocessor can execute a number of MySQL built-in functions, `count` being one of them.
4. The results from `StreamAgg_9` are then sent to the `TableReader_21` operator which is now inside the TiDB server (the task of `root`). The `estRows` column value for this operator is `1`, which means that the operator will receive one row from each of the TiKV Regions to be accessed. For more information about these requests, see [`EXPLAIN ANALYZE`](/sql-statements/sql-statement-explain-analyze.md).
5. The `StreamAgg_20` operator then applies a `count` function to each of the rows from the `└─TableReader_21` operator, which you can see from [`SHOW TABLE REGIONS`](/sql-statements/sql-statement-show-table-regions.md) and will be about 56 rows. Because this is the root operator, it then returns results to the client.

> **Note:**
>
> For a general view of the Regions that a table contains, execute [`SHOW TABLE REGIONS`](/sql-statements/sql-statement-show-table-regions.md).

## Assess the current performance

`EXPLAIN` only returns the query execution plan but does not execute the query. To get the actual execution time, you can either execute the query or use `EXPLAIN ANALYZE`:

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

The example query above takes `1.03` seconds to execute, which is an ideal performance.

From the result of `EXPLAIN ANALYZE` above, `actRows` indicates that some of the estimates (`estRows`) are inaccurate (expecting 10 thousand rows but finding 19 million rows), which is already indicated in the `operator info` (`stats:pseudo`) of `└─TableFullScan_18`. If you run [`ANALYZE TABLE`](/sql-statements/sql-statement-analyze-table.md) first and then `EXPLAIN ANALYZE` again, you can see that the estimates are much closer:

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

After `ANALYZE TABLE` is executed, you can see that the estimated rows for the `└─TableFullScan_18` operator is accurate and the estimate for `└─Selection_19` is now also much closer. In the two cases above, although the execution plan (the set of operators TiDB uses to execute this query) has not changed, quite frequently sub-optimal plans are caused by outdated statistics.

In addition to `ANALYZE TABLE`, TiDB automatically regenerates statistics as a background operation after the threshold of [`tidb_auto_analyze_ratio`](/system-variables.md#tidb_auto_analyze_ratio) is reached. You can see how close TiDB is to this threshold (how healthy TiDB considers the statistics to be) by executing the [`SHOW STATS_HEALTHY`](/sql-statements/sql-statement-show-stats-healthy.md) statement:

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

## Identify optimizations

The current execution plan is efficient in the following aspects:

* Most of the work is handled inside the TiKV coprocessor. Only 56 rows need to be sent across the network back to TiDB for processing. Each of these rows is short and contains only the count that matches the selection.

* Aggregating the count of rows both in TiDB (`StreamAgg_20`) and in TiKV (`└─StreamAgg_9`) uses the stream aggregation, which is very efficient in its memory usage.

The biggest issue with the current execution plan is that the predicate `start_date BETWEEN '2017-07-01 00:00:00' AND '2017-07-01 23:59:59'` does not apply immediately. All rows are read first with a `TableFullScan` operator, and then a selection is applied afterwards. You can find out the cause from the output of `SHOW CREATE TABLE trips`:

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

There is **NO** index on `start_date`. You would need an index in order to push this predicate into an index reader operator. Add an index as follows:

{{< copyable "sql" >}}

```sql
ALTER TABLE trips ADD INDEX (start_date);
```

```sql
Query OK, 0 rows affected (2 min 10.23 sec)
```

> **Note:**
>
> You can monitor the progress of DDL jobs using the [`ADMIN SHOW DDL JOBS`](/sql-statements/sql-statement-admin.md) command. The defaults in TiDB are carefully chosen so that adding an index does not impact production workloads too much. For testing environments, consider increasing the [`tidb_ddl_reorg_batch_size`](/system-variables.md#tidb_ddl_reorg_batch_size) and [`tidb_ddl_reorg_worker_cnt`](/system-variables.md#tidb_ddl_reorg_worker_cnt) values. On a reference system, a batch size of `10240` and worker count of `32` can achieve a 10x performance improvement over the defaults.

After adding an index, you can then repeat the query in `EXPLAIN`. In the following output, you can see that a new execution plan is chosen, and the `TableFullScan` and `Selection` operators have been eliminated:

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

To compare the actual execution time, you can again use [`EXPLAIN ANALYZE`](/sql-statements/sql-statement-explain-analyze.md):

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

From the result above, the query time has reduced from 1.03 seconds to 0.0 seconds.

> **Note:**
>
> Another optimization that applies here is the coprocessor cache. If you are unable to add indexes, consider enabling the [coprocessor cache](/coprocessor-cache.md). When it is enabled, as long as the Region has not been modified since the operator is last executed, TiKV will return the value from the cache. This will also help reduce much of the cost of the expensive `TableFullScan` and `Selection` operators.
