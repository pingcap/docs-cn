---
title: 使用聚合的 EXPLAIN 语句
summary: 了解 TiDB 中 `EXPLAIN` 语句返回的执行计划信息。
---

# 使用聚合的 EXPLAIN 语句

在进行数据聚合时，SQL 优化器会选择使用 Hash 聚合或者流式聚合操作符。为了提高查询效率，聚合操作会同时在 coprocessor 和 TiDB 层进行。考虑以下示例：

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

从 [`SHOW TABLE REGIONS`](/sql-statements/sql-statement-show-table-regions.md) 的输出可以看到，该表被分割成多个 Region：

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

使用 `EXPLAIN` 查看以下聚合语句，可以看到 `└─StreamAgg_8` 首先在 TiKV 的每个 Region 内执行。然后每个 TiKV Region 会向 TiDB 返回一行数据，TiDB 在 `StreamAgg_16` 中聚合来自每个 Region 的数据：

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

这在 `EXPLAIN ANALYZE` 中最容易观察到，其中 `actRows` 与 `SHOW TABLE REGIONS` 中的 Region 数量匹配，因为使用了 `TableFullScan` 且没有二级索引：

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

## Hash 聚合

Hash 聚合算法使用哈希表来存储执行聚合时的中间结果。它使用多个线程并行执行，但比流式聚合消耗更多内存。

以下是 `HashAgg` 操作符的示例：

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

`operator info` 显示用于聚合数据的哈希函数是 `funcs:count(1)->Column#6`。

## 流式聚合

流式聚合算法通常比 Hash 聚合消耗更少的内存。但是，这个操作符要求数据是有序发送的，这样它才能在数据到达时进行流式处理并应用聚合。

考虑以下示例：

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

在这个示例中，通过在 `col1` 上添加索引可以消除 `└─Sort_13` 操作符。一旦添加了索引，数据就可以按顺序读取，`└─Sort_13` 操作符就被消除了：

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

## 使用 ROLLUP 进行多维数据聚合

从 v7.4.0 版本开始，TiDB 的 `GROUP BY` 子句支持 `WITH ROLLUP` 修饰符。

在 `GROUP BY` 子句中，你可以指定一个或多个列作为分组列表，并在列表后添加 `WITH ROLLUP` 修饰符。然后，TiDB 将基于分组列表中的列进行多维度降序分组，并在输出中为你提供每个分组的汇总结果。

> **注意：**
>
> 目前，TiDB 不支持 Cube 语法，并且 TiDB 仅在 TiFlash MPP 模式下支持为 `WITH ROLLUP` 语法生成有效的执行计划。

```sql
explain SELECT year, month, grouping(year), grouping(month), SUM(profit) AS profit FROM bank GROUP BY year, month WITH ROLLUP;
+----------------------------------------+---------+--------------+---------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| id                                     | estRows | task         | access object | operator info                                                                                                                                                                                                                        |
+----------------------------------------+---------+--------------+---------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| TableReader_44                         | 2.40    | root         |               | MppVersion: 2, data:ExchangeSender_43                                                                                                                                                                                                |
| └─ExchangeSender_43                    | 2.40    | mpp[tiflash] |               | ExchangeType: PassThrough                                                                                                                                                                                                            |
|   └─Projection_8                       | 2.40    | mpp[tiflash] |               | Column#6->Column#12, Column#7->Column#13, grouping(gid)->Column#14, grouping(gid)->Column#15, Column#9->Column#16                                                                                                                    |
|     └─Projection_38                    | 2.40    | mpp[tiflash] |               | Column#9, Column#6, Column#7, gid                                                                                                                                                                                                    |
|       └─HashAgg_36                     | 2.40    | mpp[tiflash] |               | group by:Column#6, Column#7, gid, funcs:sum(test.bank.profit)->Column#9, funcs:firstrow(Column#6)->Column#6, funcs:firstrow(Column#7)->Column#7, funcs:firstrow(gid)->gid, stream_count: 8                                           |
|         └─ExchangeReceiver_22          | 3.00    | mpp[tiflash] |               | stream_count: 8                                                                                                                                                                                                                      |
|           └─ExchangeSender_21          | 3.00    | mpp[tiflash] |               | ExchangeType: HashPartition, Compression: FAST, Hash Cols: [name: Column#6, collate: binary], [name: Column#7, collate: utf8mb4_bin], [name: gid, collate: binary], stream_count: 8                                                  |
|             └─Expand_20                | 3.00    | mpp[tiflash] |               | level-projection:[test.bank.profit, <nil>->Column#6, <nil>->Column#7, 0->gid],[test.bank.profit, Column#6, <nil>->Column#7, 1->gid],[test.bank.profit, Column#6, Column#7, 3->gid]; schema: [test.bank.profit,Column#6,Column#7,gid] |
|               └─Projection_16          | 3.00    | mpp[tiflash] |               | test.bank.profit, test.bank.year->Column#6, test.bank.month->Column#7                                                                                                                                                                |
|                 └─TableFullScan_17     | 3.00    | mpp[tiflash] | table:bank    | keep order:false, stats:pseudo                                                                                                                                                                                                       |
+----------------------------------------+---------+--------------+---------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
10 rows in set (0.05 sec)
```

根据上述语句中的 `GROUP BY year, month WITH ROLLUP` 语法，该 SQL 语句的聚合结果可以按照 `{year, month}`、`{year}` 和 `{}` 三个分组分别计算并连接。

更多信息，请参见 [GROUP BY 修饰符](/functions-and-operators/group-by-modifier.md)。
