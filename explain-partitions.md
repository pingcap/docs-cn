---
title: 用 EXPLAIN 查看 SQL 语句需要访问的分区
summary: 了解 TiDB 中 EXPLAIN 语句返回的执行计划信息。
---

# 用 EXPLAIN 查看 SQL 语句需要访问的分区

使用 `EXPLAIN` 语句可以查看 TiDB 在执行查询时需要访问的分区。由于存在[分区裁剪](/partition-pruning.md)，所显示的分区通常只是所有分区的一个子集。本文档介绍了常见分区表的一些优化方式，以及如何解读 `EXPLAIN` 语句返回的执行计划信息。

本文档所使用的示例数据如下:

{{< copyable "sql" >}}

```sql
CREATE TABLE t1 (
 id BIGINT NOT NULL auto_increment,
 d date NOT NULL,
 pad1 BLOB,
 pad2 BLOB,
 pad3 BLOB,
 PRIMARY KEY (id,d)
) PARTITION BY RANGE (YEAR(d)) (
 PARTITION p2016 VALUES LESS THAN (2017),
 PARTITION p2017 VALUES LESS THAN (2018),
 PARTITION p2018 VALUES LESS THAN (2019),
 PARTITION p2019 VALUES LESS THAN (2020),
 PARTITION pmax VALUES LESS THAN MAXVALUE
);

INSERT INTO t1 (d, pad1, pad2, pad3) VALUES
 ('2016-01-01', RANDOM_BYTES(1024), RANDOM_BYTES(1024), RANDOM_BYTES(1024)),
 ('2016-06-01', RANDOM_BYTES(1024), RANDOM_BYTES(1024), RANDOM_BYTES(1024)),
 ('2016-09-01', RANDOM_BYTES(1024), RANDOM_BYTES(1024), RANDOM_BYTES(1024)),
 ('2017-01-01', RANDOM_BYTES(1024), RANDOM_BYTES(1024), RANDOM_BYTES(1024)),
 ('2017-06-01', RANDOM_BYTES(1024), RANDOM_BYTES(1024), RANDOM_BYTES(1024)),
 ('2017-09-01', RANDOM_BYTES(1024), RANDOM_BYTES(1024), RANDOM_BYTES(1024)),
 ('2018-01-01', RANDOM_BYTES(1024), RANDOM_BYTES(1024), RANDOM_BYTES(1024)),
 ('2018-06-01', RANDOM_BYTES(1024), RANDOM_BYTES(1024), RANDOM_BYTES(1024)),
 ('2018-09-01', RANDOM_BYTES(1024), RANDOM_BYTES(1024), RANDOM_BYTES(1024)),
 ('2019-01-01', RANDOM_BYTES(1024), RANDOM_BYTES(1024), RANDOM_BYTES(1024)),
 ('2019-06-01', RANDOM_BYTES(1024), RANDOM_BYTES(1024), RANDOM_BYTES(1024)),
 ('2019-09-01', RANDOM_BYTES(1024), RANDOM_BYTES(1024), RANDOM_BYTES(1024)),
 ('2020-01-01', RANDOM_BYTES(1024), RANDOM_BYTES(1024), RANDOM_BYTES(1024)),
 ('2020-06-01', RANDOM_BYTES(102), RANDOM_BYTES(1024), RANDOM_BYTES(1024)),
 ('2020-09-01', RANDOM_BYTES(1024), RANDOM_BYTES(1024), RANDOM_BYTES(1024));

INSERT INTO t1 SELECT NULL, a.d, RANDOM_BYTES(1024), RANDOM_BYTES(1024), RANDOM_BYTES(1024) FROM t1 a JOIN t1 b JOIN t1 c LIMIT 10000;
INSERT INTO t1 SELECT NULL, a.d, RANDOM_BYTES(1024), RANDOM_BYTES(1024), RANDOM_BYTES(1024) FROM t1 a JOIN t1 b JOIN t1 c LIMIT 10000;
INSERT INTO t1 SELECT NULL, a.d, RANDOM_BYTES(1024), RANDOM_BYTES(1024), RANDOM_BYTES(1024) FROM t1 a JOIN t1 b JOIN t1 c LIMIT 10000;
INSERT INTO t1 SELECT NULL, a.d, RANDOM_BYTES(1024), RANDOM_BYTES(1024), RANDOM_BYTES(1024) FROM t1 a JOIN t1 b JOIN t1 c LIMIT 10000;

SELECT SLEEP(1);
ANALYZE TABLE t1;
```

以下示例解释了基于新建分区表 `t1` 的一条语句：

{{< copyable "sql" >}}

```sql
EXPLAIN SELECT COUNT(*) FROM t1 WHERE d = '2017-06-01';
```

```sql
+------------------------------+---------+-----------+---------------------------+-------------------------------------------+
| id                           | estRows | task      | access object             | operator info                             |
+------------------------------+---------+-----------+---------------------------+-------------------------------------------+
| StreamAgg_21                 | 1.00    | root      |                           | funcs:count(Column#8)->Column#6           |
| └─TableReader_22             | 1.00    | root      |                           | data:StreamAgg_10                         |
|   └─StreamAgg_10             | 1.00    | cop[tikv] |                           | funcs:count(1)->Column#8                  |
|     └─Selection_20           | 8.87    | cop[tikv] |                           | eq(test.t1.d, 2017-06-01 00:00:00.000000) |
|       └─TableFullScan_19     | 8870.00 | cop[tikv] | table:t1, partition:p2017 | keep order:false                          |
+------------------------------+---------+-----------+---------------------------+-------------------------------------------+
5 rows in set (0.01 sec)
```

由上述 `EXPLAIN` 结果可知，从最末尾的 `—TableFullScan_19` 算子开始，再返回到根部的 `StreamAgg_21` 算子的执行过程如下：

* TiDB 成功地识别出只需要访问一个分区（`p2017`），并将该信息在 `access object` 列中注明。
* `└─TableFullScan_19` 算子先对整个分区进行扫描，然后执行 `└─Selection_20` 算子筛选起始日期为 `2017-06-01 00:00:00.000000` 的行。
* 之后，`└─Selection_20` 算子匹配的行在 Coprocessor 中进行流式聚合，Coprocessor 本身就可以理解聚合函数 `count`。
* 每个 Coprocessor 请求会发送一行数据给 TiDB 的 `└─TableReader_22` 算子，然后将数据在 `StreamAgg_21` 算子下进行流式聚合，再将一行数据返回给客户端。

以下示例中，分区裁剪不会消除任何分区：

{{< copyable "sql" >}}

```sql
EXPLAIN SELECT COUNT(*) FROM t1 WHERE YEAR(d) = 2017;
```

```sql
+------------------------------------+----------+-----------+---------------------------+----------------------------------+
| id                                 | estRows  | task      | access object             | operator info                    |
+------------------------------------+----------+-----------+---------------------------+----------------------------------+
| HashAgg_20                         | 1.00     | root      |                           | funcs:count(Column#7)->Column#6  |
| └─PartitionUnion_21                | 5.00     | root      |                           |                                  |
|   ├─StreamAgg_36                   | 1.00     | root      |                           | funcs:count(Column#9)->Column#7  |
|   │ └─TableReader_37               | 1.00     | root      |                           | data:StreamAgg_25                |
|   │   └─StreamAgg_25               | 1.00     | cop[tikv] |                           | funcs:count(1)->Column#9         |
|   │     └─Selection_35             | 6000.00  | cop[tikv] |                           | eq(year(test.t1.d), 2017)        |
|   │       └─TableFullScan_34       | 7500.00  | cop[tikv] | table:t1, partition:p2016 | keep order:false                 |
|   ├─StreamAgg_55                   | 1.00     | root      |                           | funcs:count(Column#11)->Column#7 |
|   │ └─TableReader_56               | 1.00     | root      |                           | data:StreamAgg_44                |
|   │   └─StreamAgg_44               | 1.00     | cop[tikv] |                           | funcs:count(1)->Column#11        |
|   │     └─Selection_54             | 14192.00 | cop[tikv] |                           | eq(year(test.t1.d), 2017)        |
|   │       └─TableFullScan_53       | 17740.00 | cop[tikv] | table:t1, partition:p2017 | keep order:false                 |
|   ├─StreamAgg_74                   | 1.00     | root      |                           | funcs:count(Column#13)->Column#7 |
|   │ └─TableReader_75               | 1.00     | root      |                           | data:StreamAgg_63                |
|   │   └─StreamAgg_63               | 1.00     | cop[tikv] |                           | funcs:count(1)->Column#13        |
|   │     └─Selection_73             | 3977.60  | cop[tikv] |                           | eq(year(test.t1.d), 2017)        |
|   │       └─TableFullScan_72       | 4972.00  | cop[tikv] | table:t1, partition:p2018 | keep order:false                 |
|   ├─StreamAgg_93                   | 1.00     | root      |                           | funcs:count(Column#15)->Column#7 |
|   │ └─TableReader_94               | 1.00     | root      |                           | data:StreamAgg_82                |
|   │   └─StreamAgg_82               | 1.00     | cop[tikv] |                           | funcs:count(1)->Column#15        |
|   │     └─Selection_92             | 20361.60 | cop[tikv] |                           | eq(year(test.t1.d), 2017)        |
|   │       └─TableFullScan_91       | 25452.00 | cop[tikv] | table:t1, partition:p2019 | keep order:false                 |
|   └─StreamAgg_112                  | 1.00     | root      |                           | funcs:count(Column#17)->Column#7 |
|     └─TableReader_113              | 1.00     | root      |                           | data:StreamAgg_101               |
|       └─StreamAgg_101              | 1.00     | cop[tikv] |                           | funcs:count(1)->Column#17        |
|         └─Selection_111            | 8892.80  | cop[tikv] |                           | eq(year(test.t1.d), 2017)        |
|           └─TableFullScan_110      | 11116.00 | cop[tikv] | table:t1, partition:pmax  | keep order:false                 |
+------------------------------------+----------+-----------+---------------------------+----------------------------------+
27 rows in set (0.00 sec)
```

由上述 `EXPLAIN` 结果可知：

* TiDB 认为需要访问所有分区 `(p2016..pMax)`。这是因为 TiDB 将谓词 `YEAR（d）= 2017` 视为 [non-sargable](https://en.wikipedia.org/wiki/Sargable)。这个问题并非是 TiDB 特有的。
* 在扫描每个分区时，`Selection` 算子将筛选出年份不为 2017 的行。
* 在每个分区上会执行流式聚合，以计算匹配的行数。
* `└─PartitionUnion_21` 算子会合并访问每个分区后的结果。
