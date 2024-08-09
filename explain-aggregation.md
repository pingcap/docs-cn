---
title: 用 EXPLAIN 查看聚合查询的执行计划
summary: 了解 TiDB 中 EXPLAIN 语句返回的执行计划信息。
---

# 用 EXPLAIN 查看聚合查询执行计划

SQL 查询中可能会使用聚合计算，可以通过 `EXPLAIN` 语句来查看聚合查询的执行计划。本文提供多个示例，以帮助用户理解聚合查询是如何执行的。

SQL 优化器会选择以下任一算子实现数据聚合：

- Hash Aggregation
- Stream Aggregation

为了提高查询效率，数据聚合在 Coprocessor 层和 TiDB 层均会执行。现有示例如下：

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

以上示例创建表格 `t1` 并插入数据后，再执行 [`SHOW TABLE REGIONS`](/sql-statements/sql-statement-show-table-regions.md) 语句。从以下 `SHOW TABLE REGIONS` 的执行结果可知，表 `t1` 被切分为多个 Region：

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

使用 `EXPLAIN` 查看以下聚合语句的执行计划。可以看到 `└─StreamAgg_8` 算子先执行在 TiKV 内每个 Region 上，然后 TiKV 的每个 Region 会返回一行数据给 TiDB，TiDB 在 `StreamAgg_16` 算子上对每个 Region 返回的数据进行聚合：

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

同样，通过执行 `EXPLAIN ANALYZE` 语句可知，`actRows` 与 `SHOW TABLE REGIONS` 返回结果中的 Region 数匹配，这是因为执行使用了 `TableFullScan` 全表扫并且没有二级索引：

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

Hash Aggregation 算法在执行聚合时使用 Hash 表存储中间结果。此算法采用多线程并发优化，执行速度快，但与 Stream Aggregation 算法相比会消耗较多内存。

下面是一个使用 Hash Aggregation（即 `HashAgg` 算子）的例子：

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

`operator info` 列显示，用于聚合数据的 Hash 函数为 `funcs:count(1)->Column#6`。

## Stream Aggregation

Stream Aggregation 算法通常会比 Hash Aggregation 算法占用更少的内存。但是此算法要求数据按顺序发送，以便对依次到达的值实现流式数据聚合。

下面是一个使用 Stream Aggregation 的例子：

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

以上示例中，可以在 `col1` 上添加索引来消除 `└─Sort_13` 算子。添加索引后，TiDB 就可以按顺序读取数据并消除 `└─Sort_13` 算子。

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

## 多维度数据聚合 ROLLUP

自 v7.4.0 起，TiDB 的 `GROUP BY` 子句支持 `WITH ROLLUP` 修饰符。

你可以在 `GROUP BY` 子句中指定一个或多个列，形成一个分组列表，然后添加 `WITH ROLLUP` 修饰符。TiDB 将会按照分组列表中的列进行多维度的递减分组，并在输出中为你提供各个分组数据的汇总结果。

> **注意**
>
> TiDB 暂不支持 Cube 语法。

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

该语句的 SQL 聚合可以按照 `GROUP BY year, month WITH ROLLUP` 语法在 {year, month}、{year}、{} 这 3 个分组中分别计算并连接结果。

更多信息，请参考 [GROUP BY 修饰符](/functions-and-operators/group-by-modifier.md)。

## 其他类型查询的执行计划

+ [MPP 模式查询的执行计划](/explain-mpp.md)
+ [索引查询的执行计划](/explain-indexes.md)
+ [Join 查询的执行计划](/explain-joins.md)
+ [子查询的执行计划](/explain-subqueries.md)
+ [视图查询的执行计划](/explain-views.md)
+ [分区查询的执行计划](/explain-partitions.md)
+ [索引合并查询的执行计划](/explain-index-merge.md)
