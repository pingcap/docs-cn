---
title: Explain Statements That Use Aggregation
summary: Learn about the execution plan information returned by the `EXPLAIN` statement in TiDB.
---

# Explain Statements Using Aggregation

When aggregating data, the SQL Optimizer will select either a Hash Aggregation or Stream Aggregation operator. To improve query efficiency, aggregation is performed at both the coprocessor and TiDB layers. Consider the following example:

{{< copyable "sql" >}}

```sql
CREATE TABLE t1 (id INT NOT NULL PRIMARY KEY auto_increment, pad1 BLOB, pad2 BLOB, pad3 BLOB);
INSERT INTO t1 SELECT NULL, RANDOM_BYTES(1024), RANDOM_BYTES(1024), RANDOM_BYTES(1024) FROM dual;
INSERT INTO t1 SELECT NULL, RANDOM_BYTES(1024), RANDOM_BYTES(1024), RANDOM_BYTES(1024) FROM t1 a JOIN t1 b JOIN t1 c LIMIT 10000;
INSERT INTO t1 SELECT NULL, RANDOM_BYTES(1024), RANDOM_BYTES(1024), RANDOM_BYTES(1024) FROM t1 a JOIN t1 b JOIN t1 c LIMIT 10000;
INSERT INTO t1 SELECT NULL, RANDOM_BYTES(1024), RANDOM_BYTES(1024), RANDOM_BYTES(1024) FROM t1 a JOIN t1 b JOIN t1 c LIMIT 10000;
INSERT INTO t1 SELECT NULL, RANDOM_BYTES(1024), RANDOM_BYTES(1024), RANDOM_BYTES(1024) FROM t1 a JOIN t1 b JOIN t1 c LIMIT 10000;
INSERT INTO t1 SELECT NULL, RANDOM_BYTES(1024), RANDOM_BYTES(1024), RANDOM_BYTES(1024) FROM t1 a JOIN t1 b JOIN t1 c LIMIT 10000;
INSERT INTO t1 SELECT NULL, RANDOM_BYTES(1024), RANDOM_BYTES(1024), RANDOM_BYTES(1024) FROM t1 a JOIN t1 b JOIN t1 c LIMIT 10000;
INSERT INTO t1 SELECT NULL, RANDOM_BYTES(1024), RANDOM_BYTES(1024), RANDOM_BYTES(1024) FROM t1 a JOIN t1 b JOIN t1 c LIMIT 10000;
INSERT INTO t1 SELECT NULL, RANDOM_BYTES(1024), RANDOM_BYTES(1024), RANDOM_BYTES(1024) FROM t1 a JOIN t1 b JOIN t1 c LIMIT 10000;
INSERT INTO t1 SELECT NULL, RANDOM_BYTES(1024), RANDOM_BYTES(1024), RANDOM_BYTES(1024) FROM t1 a JOIN t1 b JOIN t1 c LIMIT 10000;
INSERT INTO t1 SELECT NULL, RANDOM_BYTES(1024), RANDOM_BYTES(1024), RANDOM_BYTES(1024) FROM t1 a JOIN t1 b JOIN t1 c LIMIT 10000;
INSERT INTO t1 SELECT NULL, RANDOM_BYTES(1024), RANDOM_BYTES(1024), RANDOM_BYTES(1024) FROM t1 a JOIN t1 b JOIN t1 c LIMIT 10000;
INSERT INTO t1 SELECT NULL, RANDOM_BYTES(1024), RANDOM_BYTES(1024), RANDOM_BYTES(1024) FROM t1 a JOIN t1 b JOIN t1 c LIMIT 10000;
INSERT INTO t1 SELECT NULL, RANDOM_BYTES(1024), RANDOM_BYTES(1024), RANDOM_BYTES(1024) FROM t1 a JOIN t1 b JOIN t1 c LIMIT 10000;
INSERT INTO t1 SELECT NULL, RANDOM_BYTES(1024), RANDOM_BYTES(1024), RANDOM_BYTES(1024) FROM t1 a JOIN t1 b JOIN t1 c LIMIT 10000;
INSERT INTO t1 SELECT NULL, RANDOM_BYTES(1024), RANDOM_BYTES(1024), RANDOM_BYTES(1024) FROM t1 a JOIN t1 b JOIN t1 c LIMIT 10000;
SELECT SLEEP(1);
ANALYZE TABLE t1;
```

From the output of [`SHOW TABLE REGIONS`](/sql-statements/sql-statement-show-table-regions.md), you can see that this table is split into multiple Regions:

{{< copyable "sql" >}}

```sql
SHOW TABLE t1 REGIONS;
```

```sql
+-----------+--------------+--------------+-----------+-----------------+-------+------------+---------------+------------+----------------------+------------------+
| REGION_ID | START_KEY    | END_KEY      | LEADER_ID | LEADER_STORE_ID | PEERS | SCATTERING | WRITTEN_BYTES | READ_BYTES | APPROXIMATE_SIZE(MB) | APPROXIMATE_KEYS |
+-----------+--------------+--------------+-----------+-----------------+-------+------------+---------------+------------+----------------------+------------------+
|        64 | t_64_        | t_64_r_31766 |        65 |               1 | 65    |          0 |          1325 |  102033520 |                   98 |            52797 |
|        66 | t_64_r_31766 | t_64_r_63531 |        67 |               1 | 67    |          0 |          1325 |   72522521 |                  104 |            78495 |
|        68 | t_64_r_63531 | t_64_r_95296 |        69 |               1 | 69    |          0 |          1325 |          0 |                  104 |            95433 |
|         2 | t_64_r_95296 |              |         3 |               1 | 3     |          0 |          1501 |          0 |                   81 |            63211 |
+-----------+--------------+--------------+-----------+-----------------+-------+------------+---------------+------------+----------------------+------------------+
4 rows in set (0.00 sec)
```

Using `EXPLAIN` with the following aggregation statement, you can see that `└─StreamAgg_8` is first performed on each Region inside TiKV. Each TiKV Region will then send one row back to TiDB, which aggregates the data from each Region in `StreamAgg_16`:

{{< copyable "sql" >}}

```sql
EXPLAIN SELECT COUNT(*) FROM t1;
```

```sql
+----------------------------+-----------+-----------+---------------+---------------------------------+
| id                         | estRows   | task      | access object | operator info                   |
+----------------------------+-----------+-----------+---------------+---------------------------------+
| StreamAgg_16               | 1.00      | root      |               | funcs:count(Column#7)->Column#5 |
| └─TableReader_17           | 1.00      | root      |               | data:StreamAgg_8                |
|   └─StreamAgg_8            | 1.00      | cop[tikv] |               | funcs:count(1)->Column#7        |
|     └─TableFullScan_15     | 242020.00 | cop[tikv] | table:t1      | keep order:false                |
+----------------------------+-----------+-----------+---------------+---------------------------------+
4 rows in set (0.00 sec)
```

This is easiest to observe in `EXPLAIN ANALYZE`, where the `actRows` matches the number of Regions from `SHOW TABLE REGIONS` because a `TableFullScan` is being used and there are no secondary indexes:

```sql
EXPLAIN ANALYZE SELECT COUNT(*) FROM t1;
```

```sql
+----------------------------+-----------+---------+-----------+---------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+---------------------------------+-----------+------+
| id                         | estRows   | actRows | task      | access object | execution info                                                                                                                                                                                                                                  | operator info                   | memory    | disk |
+----------------------------+-----------+---------+-----------+---------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+---------------------------------+-----------+------+
| StreamAgg_16               | 1.00      | 1       | root      |               | time:12.609575ms, loops:2                                                                                                                                                                                                                       | funcs:count(Column#7)->Column#5 | 372 Bytes | N/A  |
| └─TableReader_17           | 1.00      | 4       | root      |               | time:12.605155ms, loops:2, cop_task: {num: 4, max: 12.538245ms, min: 9.256838ms, avg: 10.895114ms, p95: 12.538245ms, max_proc_keys: 31765, p95_proc_keys: 31765, tot_proc: 48ms, rpc_num: 4, rpc_time: 43.530707ms, copr_cache_hit_ratio: 0.00} | data:StreamAgg_8                | 293 Bytes | N/A  |
|   └─StreamAgg_8            | 1.00      | 4       | cop[tikv] |               | proc max:12ms, min:12ms, p80:12ms, p95:12ms, iters:122, tasks:4                                                                                                                                                                                 | funcs:count(1)->Column#7        | N/A       | N/A  |
|     └─TableFullScan_15     | 242020.00 | 121010  | cop[tikv] | table:t1      | proc max:12ms, min:12ms, p80:12ms, p95:12ms, iters:122, tasks:4                                                                                                                                                                                 | keep order:false                | N/A       | N/A  |
+----------------------------+-----------+---------+-----------+---------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+---------------------------------+-----------+------+
4 rows in set (0.01 sec)
```

## Hash Aggregation

The Hash Aggregation algorithm uses a hash table to store intermediate results while performing aggregation. It executes in parallel using multiple threads but consumes more memory than Stream Aggregation.

The following is an example of the `HashAgg` operator:

{{< copyable "sql" >}}

```sql
EXPLAIN SELECT /*+ HASH_AGG() */ count(*) FROM t1;
```

```sql
+---------------------------+-----------+-----------+---------------+---------------------------------+
| id                        | estRows   | task      | access object | operator info                   |
+---------------------------+-----------+-----------+---------------+---------------------------------+
| HashAgg_9                 | 1.00      | root      |               | funcs:count(Column#6)->Column#5 |
| └─TableReader_10          | 1.00      | root      |               | data:HashAgg_5                  |
|   └─HashAgg_5             | 1.00      | cop[tikv] |               | funcs:count(1)->Column#6        |
|     └─TableFullScan_8     | 242020.00 | cop[tikv] | table:t1      | keep order:false                |
+---------------------------+-----------+-----------+---------------+---------------------------------+
4 rows in set (0.00 sec)
```

The `operator info` shows that the hashing function used to aggregate the data is `funcs:count(1)->Column#6`.

## Stream Aggregation

The Stream Aggregation algorithm usually consumes less memory than Hash Aggregation. However, this operator requires that data is sent ordered so that it can _stream_ and apply the aggregation on values as they arrive.

Consider the following example:

{{< copyable "sql" >}}

```sql
CREATE TABLE t2 (id INT NOT NULL PRIMARY KEY, col1 INT NOT NULL);
INSERT INTO t2 VALUES (1, 9),(2, 3),(3,1),(4,8),(6,3);
EXPLAIN SELECT /*+ STREAM_AGG() */ col1, count(*) FROM t2 GROUP BY col1;
```

```sql
Query OK, 0 rows affected (0.11 sec)

Query OK, 5 rows affected (0.01 sec)
Records: 5  Duplicates: 0  Warnings: 0

+------------------------------+----------+-----------+---------------+---------------------------------------------------------------------------------------------+
| id                           | estRows  | task      | access object | operator info                                                                               |
+------------------------------+----------+-----------+---------------+---------------------------------------------------------------------------------------------+
| Projection_4                 | 8000.00  | root      |               | test.t2.col1, Column#3                                                                      |
| └─StreamAgg_8                | 8000.00  | root      |               | group by:test.t2.col1, funcs:count(1)->Column#3, funcs:firstrow(test.t2.col1)->test.t2.col1 |
|   └─Sort_13                  | 10000.00 | root      |               | test.t2.col1                                                                                |
|     └─TableReader_12         | 10000.00 | root      |               | data:TableFullScan_11                                                                       |
|       └─TableFullScan_11     | 10000.00 | cop[tikv] | table:t2      | keep order:false, stats:pseudo                                                              |
+------------------------------+----------+-----------+---------------+---------------------------------------------------------------------------------------------+
5 rows in set (0.00 sec)
```

In this example, the `└─Sort_13` operator can be eliminated by adding an index on `col1`. Once the index is added, the data can be read in order and the `└─Sort_13` operator is eliminated:

{{< copyable "sql" >}}

```sql
ALTER TABLE t2 ADD INDEX (col1);
EXPLAIN SELECT /*+ STREAM_AGG() */ col1, count(*) FROM t2 GROUP BY col1;
```

```sql
Query OK, 0 rows affected (0.28 sec)

+------------------------------+---------+-----------+----------------------------+----------------------------------------------------------------------------------------------------+
| id                           | estRows | task      | access object              | operator info                                                                                      |
+------------------------------+---------+-----------+----------------------------+----------------------------------------------------------------------------------------------------+
| Projection_4                 | 4.00    | root      |                            | test.t2.col1, Column#3                                                                             |
| └─StreamAgg_14               | 4.00    | root      |                            | group by:test.t2.col1, funcs:count(Column#4)->Column#3, funcs:firstrow(test.t2.col1)->test.t2.col1 |
|   └─IndexReader_15           | 4.00    | root      |                            | index:StreamAgg_8                                                                                  |
|     └─StreamAgg_8            | 4.00    | cop[tikv] |                            | group by:test.t2.col1, funcs:count(1)->Column#4                                                    |
|       └─IndexFullScan_13     | 5.00    | cop[tikv] | table:t2, index:col1(col1) | keep order:true, stats:pseudo                                                                      |
+------------------------------+---------+-----------+----------------------------+----------------------------------------------------------------------------------------------------+
5 rows in set (0.00 sec)
```
