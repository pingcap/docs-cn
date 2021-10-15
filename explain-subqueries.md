---
title: 用 EXPLAIN 查看使用子查询的执行计划
summary: 了解 TiDB 中 EXPLAIN 语句返回的执行计划信息。
---

# 用 EXPLAIN 查看使用子查询的执行计划

TiDB 会执行多种[子查询相关的优化](/subquery-optimization.md)，以提升子查询的执行性能。本文档介绍一些常见子查询的优化方式，以及如何解读 `EXPLAIN` 语句返回的执行计划信息。

本文档所使用的示例表数据如下：

```sql
CREATE TABLE t1 (id BIGINT NOT NULL PRIMARY KEY auto_increment, pad1 BLOB, pad2 BLOB, pad3 BLOB, int_col INT NOT NULL DEFAULT 0);
CREATE TABLE t2 (id BIGINT NOT NULL PRIMARY KEY auto_increment, t1_id BIGINT NOT NULL, pad1 BLOB, pad2 BLOB, pad3 BLOB, INDEX(t1_id));
CREATE TABLE t3 (
 id INT NOT NULL PRIMARY KEY auto_increment,
 t1_id INT NOT NULL,
 UNIQUE (t1_id)
);

INSERT INTO t1 SELECT NULL, RANDOM_BYTES(1024), RANDOM_BYTES(1024), RANDOM_BYTES(1024), 0 FROM dual;
INSERT INTO t1 SELECT NULL, RANDOM_BYTES(1024), RANDOM_BYTES(1024), RANDOM_BYTES(1024), 0 FROM t1 a JOIN t1 b JOIN t1 c LIMIT 10000;
INSERT INTO t1 SELECT NULL, RANDOM_BYTES(1024), RANDOM_BYTES(1024), RANDOM_BYTES(1024), 0 FROM t1 a JOIN t1 b JOIN t1 c LIMIT 10000;
INSERT INTO t1 SELECT NULL, RANDOM_BYTES(1024), RANDOM_BYTES(1024), RANDOM_BYTES(1024), 0 FROM t1 a JOIN t1 b JOIN t1 c LIMIT 10000;
INSERT INTO t1 SELECT NULL, RANDOM_BYTES(1024), RANDOM_BYTES(1024), RANDOM_BYTES(1024), 0 FROM t1 a JOIN t1 b JOIN t1 c LIMIT 10000;
INSERT INTO t1 SELECT NULL, RANDOM_BYTES(1024), RANDOM_BYTES(1024), RANDOM_BYTES(1024), 0 FROM t1 a JOIN t1 b JOIN t1 c LIMIT 10000;
INSERT INTO t1 SELECT NULL, RANDOM_BYTES(1024), RANDOM_BYTES(1024), RANDOM_BYTES(1024), 0 FROM t1 a JOIN t1 b JOIN t1 c LIMIT 10000;
INSERT INTO t1 SELECT NULL, RANDOM_BYTES(1024), RANDOM_BYTES(1024), RANDOM_BYTES(1024), 0 FROM t1 a JOIN t1 b JOIN t1 c LIMIT 10000;
INSERT INTO t1 SELECT NULL, RANDOM_BYTES(1024), RANDOM_BYTES(1024), RANDOM_BYTES(1024), 0 FROM t1 a JOIN t1 b JOIN t1 c LIMIT 10000;
INSERT INTO t1 SELECT NULL, RANDOM_BYTES(1024), RANDOM_BYTES(1024), RANDOM_BYTES(1024), 0 FROM t1 a JOIN t1 b JOIN t1 c LIMIT 10000;
INSERT INTO t1 SELECT NULL, RANDOM_BYTES(1024), RANDOM_BYTES(1024), RANDOM_BYTES(1024), 0 FROM t1 a JOIN t1 b JOIN t1 c LIMIT 10000;
INSERT INTO t2 SELECT NULL, a.id, RANDOM_BYTES(1024), RANDOM_BYTES(1024), RANDOM_BYTES(1024) FROM t1 a JOIN t1 b JOIN t1 c LIMIT 10000;
INSERT INTO t2 SELECT NULL, a.id, RANDOM_BYTES(1024), RANDOM_BYTES(1024), RANDOM_BYTES(1024) FROM t1 a JOIN t1 b JOIN t1 c LIMIT 10000;
INSERT INTO t2 SELECT NULL, a.id, RANDOM_BYTES(1024), RANDOM_BYTES(1024), RANDOM_BYTES(1024) FROM t1 a JOIN t1 b JOIN t1 c LIMIT 10000;
INSERT INTO t2 SELECT NULL, a.id, RANDOM_BYTES(1024), RANDOM_BYTES(1024), RANDOM_BYTES(1024) FROM t1 a JOIN t1 b JOIN t1 c LIMIT 10000;
INSERT INTO t2 SELECT NULL, a.id, RANDOM_BYTES(1024), RANDOM_BYTES(1024), RANDOM_BYTES(1024) FROM t1 a JOIN t1 b JOIN t1 c LIMIT 10000;
INSERT INTO t2 SELECT NULL, a.id, RANDOM_BYTES(1024), RANDOM_BYTES(1024), RANDOM_BYTES(1024) FROM t1 a JOIN t1 b JOIN t1 c LIMIT 10000;
INSERT INTO t2 SELECT NULL, a.id, RANDOM_BYTES(1024), RANDOM_BYTES(1024), RANDOM_BYTES(1024) FROM t1 a JOIN t1 b JOIN t1 c LIMIT 10000;
INSERT INTO t2 SELECT NULL, a.id, RANDOM_BYTES(1024), RANDOM_BYTES(1024), RANDOM_BYTES(1024) FROM t1 a JOIN t1 b JOIN t1 c LIMIT 10000;
INSERT INTO t2 SELECT NULL, a.id, RANDOM_BYTES(1024), RANDOM_BYTES(1024), RANDOM_BYTES(1024) FROM t1 a JOIN t1 b JOIN t1 c LIMIT 10000;
UPDATE t1 SET int_col = 1 WHERE pad1 = (SELECT pad1 FROM t1 ORDER BY RAND() LIMIT 1);
INSERT INTO t3 SELECT NULL, id FROM t1 WHERE id < 1000;

SELECT SLEEP(1);
ANALYZE TABLE t1, t2, t3;
```

## Inner join（无 `UNIQUE` 约束的子查询）

以下示例中，`IN` 子查询会从表 `t2` 中搜索一列 ID。为保证语义正确性，TiDB 需要保证 `t1_id` 列的值具有唯一性。使用 `EXPLAIN` 可查看到该查询的执行计划去掉重复项并执行 `Inner Join` 内连接操作：

```sql
EXPLAIN SELECT * FROM t1 WHERE id IN (SELECT t1_id FROM t2);
```

```sql
+----------------------------------+----------+-----------+------------------------------+---------------------------------------------------------------------------------------------------------------------------+
| id                               | estRows  | task      | access object                | operator info                                                                                                             |
+----------------------------------+----------+-----------+------------------------------+---------------------------------------------------------------------------------------------------------------------------+
| IndexJoin_14                     | 5.00     | root      |                              | inner join, inner:IndexLookUp_13, outer key:test.t2.t1_id, inner key:test.t1.id, equal cond:eq(test.t2.t1_id, test.t1.id) |
| ├─StreamAgg_49(Build)            | 5.00     | root      |                              | group by:test.t2.t1_id, funcs:firstrow(test.t2.t1_id)->test.t2.t1_id                                                      |
| │ └─IndexReader_50               | 5.00     | root      |                              | index:StreamAgg_39                                                                                                        |
| │   └─StreamAgg_39               | 5.00     | cop[tikv] |                              | group by:test.t2.t1_id,                                                                                                   |
| │     └─IndexFullScan_31         | 50000.00 | cop[tikv] | table:t2, index:t1_id(t1_id) | keep order:true                                                                                                           |
| └─IndexLookUp_13(Probe)          | 1.00     | root      |                              |                                                                                                                           |
|   ├─IndexRangeScan_11(Build)     | 1.00     | cop[tikv] | table:t1, index:PRIMARY(id)  | range: decided by [eq(test.t1.id, test.t2.t1_id)], keep order:false                                                       |
|   └─TableRowIDScan_12(Probe)     | 1.00     | cop[tikv] | table:t1                     | keep order:false                                                                                                          |
+----------------------------------+----------+-----------+------------------------------+---------------------------------------------------------------------------------------------------------------------------+
8 rows in set (0.00 sec)
```

由上述查询结果可知，TiDB 首先执行 `Index Join` 索引连接操作，开始读取 `t2.t1_id` 列的索引。先是 `└─HashAgg_31` 算子的部分任务在 TiKV 中对 `t1_id` 值进行去重，然后`├─HashAgg_38(Build)` 算子的部分任务在 TiDB 中对 `t1_id` 值再次进行去重。去重操作由聚合函数 `firstrow(test.t2.t1_id)` 执行，之后会将操作结果与 `t1` 表的主键相连接。

## Inner join（有 `UNIQUE` 约束的子查询）

在上述示例中，为了确保 `t1_id` 值在与表 `t1` 连接前具有唯一性，需要执行聚合运算。在以下示例中，由于 `UNIQUE` 约束已能确保 `t3.t1_id` 列值的唯一：

```sql
EXPLAIN SELECT * FROM t1 WHERE id IN (SELECT t1_id FROM t3);
```

```sql
+----------------------------------+---------+-----------+-----------------------------+---------------------------------------------------------------------------------------------------------------------------+
| id                               | estRows | task      | access object               | operator info                                                                                                             |
+----------------------------------+---------+-----------+-----------------------------+---------------------------------------------------------------------------------------------------------------------------+
| IndexJoin_17                     | 1978.13 | root      |                             | inner join, inner:IndexLookUp_16, outer key:test.t3.t1_id, inner key:test.t1.id, equal cond:eq(test.t3.t1_id, test.t1.id) |
| ├─TableReader_44(Build)          | 1978.00 | root      |                             | data:TableFullScan_43                                                                                                     |
| │ └─TableFullScan_43             | 1978.00 | cop[tikv] | table:t3                    | keep order:false                                                                                                          |
| └─IndexLookUp_16(Probe)          | 1.00    | root      |                             |                                                                                                                           |
|   ├─IndexRangeScan_14(Build)     | 1.00    | cop[tikv] | table:t1, index:PRIMARY(id) | range: decided by [eq(test.t1.id, test.t3.t1_id)], keep order:false                                                       |
|   └─TableRowIDScan_15(Probe)     | 1.00    | cop[tikv] | table:t1                    | keep order:false                                                                                                          |
+----------------------------------+---------+-----------+-----------------------------+---------------------------------------------------------------------------------------------------------------------------+
6 rows in set (0.01 sec)
```

从语义上看，因为约束保证了 `t3.t1_id` 列值的唯一性，TiDB 可以直接执行 `INNER JOIN` 查询。

## Semi Join（关联查询）

在前两个示例中，通过 `HashAgg` 聚合操作或通过 `UNIQUE` 约束保证子查询数据的唯一性之后，TiDB 才能够执行 `Inner Join` 操作。这两种连接均使用了 `Index Join`。

下面的例子中，TiDB 优化器则选择了一种不同的执行计划：

```sql
EXPLAIN SELECT * FROM t1 WHERE id IN (SELECT t1_id FROM t2 WHERE t1_id != t1.int_col);
```

```sql
+-----------------------------+-----------+-----------+------------------------------+--------------------------------------------------------------------------------------------------------+
| id                          | estRows   | task      | access object                | operator info                                                                                          |
+-----------------------------+-----------+-----------+------------------------------+--------------------------------------------------------------------------------------------------------+
| MergeJoin_9                 | 45446.40  | root      |                              | semi join, left key:test.t1.id, right key:test.t2.t1_id, other cond:ne(test.t2.t1_id, test.t1.int_col) |
| ├─IndexReader_24(Build)     | 180000.00 | root      |                              | index:IndexFullScan_23                                                                                 |
| │ └─IndexFullScan_23        | 180000.00 | cop[tikv] | table:t2, index:t1_id(t1_id) | keep order:true                                                                                        |
| └─TableReader_22(Probe)     | 56808.00  | root      |                              | data:Selection_21                                                                                      |
|   └─Selection_21            | 56808.00  | cop[tikv] |                              | ne(test.t1.id, test.t1.int_col)                                                                        |
|     └─TableFullScan_20      | 71010.00  | cop[tikv] | table:t1                     | keep order:true                                                                                        |
+-----------------------------+-----------+-----------+------------------------------+--------------------------------------------------------------------------------------------------------+
6 rows in set (0.00 sec)
```

由上述查询结果可知，TiDB 执行了 `Semi Join`。不同于 `Inner Join`，`Semi Join` 仅允许右键 (`t2.t1_id`) 上的第一个值，也就是该操作将去除 `Join` 算子任务中的重复数据。`Join` 算法也包含 `Merge Join`，会按照排序顺序同时从左侧和右侧读取数据，这是一种高效的 `Zipper Merge`。

可以将原语句视为*关联子查询*，因为它引入了子查询外的 `t1.int_col` 列。然而，`EXPLAIN` 语句的返回结果显示的是[关联子查询去关联](/correlated-subquery-optimization.md)后的执行计划。条件 `t1_id != t1.int_col` 会被重写为 `t1.id != t1.int_col`。TiDB 可以从表 `t1` 中读取数据并且在 `└─Selection_21` 中执行此操作，因此这种去关联和重写操作会极大提高执行效率。

## Anti Semi Join （`NOT IN` 子查询）

在以下示例中，*除非*子查询中存在 `t3.t1_id`，否则该查询将（从语义上）返回表 `t3` 中的所有行：

```sql
EXPLAIN SELECT * FROM t3 WHERE t1_id NOT IN (SELECT id FROM t1 WHERE int_col < 100);
```

```sql
+----------------------------------+---------+-----------+-----------------------------+-------------------------------------------------------------------------------------------------------------------------------+
| id                               | estRows | task      | access object               | operator info                                                                                                                 |
+----------------------------------+---------+-----------+-----------------------------+-------------------------------------------------------------------------------------------------------------------------------+
| IndexJoin_14                     | 1582.40 | root      |                             | anti semi join, inner:IndexLookUp_13, outer key:test.t3.t1_id, inner key:test.t1.id, equal cond:eq(test.t3.t1_id, test.t1.id) |
| ├─TableReader_35(Build)          | 1978.00 | root      |                             | data:TableFullScan_34                                                                                                         |
| │ └─TableFullScan_34             | 1978.00 | cop[tikv] | table:t3                    | keep order:false                                                                                                              |
| └─IndexLookUp_13(Probe)          | 1.00    | root      |                             |                                                                                                                               |
|   ├─IndexRangeScan_10(Build)     | 1.00    | cop[tikv] | table:t1, index:PRIMARY(id) | range: decided by [eq(test.t1.id, test.t3.t1_id)], keep order:false                                                           |
|   └─Selection_12(Probe)          | 1.00    | cop[tikv] |                             | lt(test.t1.int_col, 100)                                                                                                      |
|     └─TableRowIDScan_11          | 1.00    | cop[tikv] | table:t1                    | keep order:false                                                                                                              |
+----------------------------------+---------+-----------+-----------------------------+-------------------------------------------------------------------------------------------------------------------------------+
7 rows in set (0.00 sec)
```

上述查询首先读取了表 `t3`，然后根据主键开始探测 (probe) 表 `t1`。连接类型是 _anti semi join_，即反半连接：之所以使用 _anti_，是因为上述示例有不存在匹配值（即 `NOT IN`）的情况；使用 `Semi Join` 则是因为仅需要匹配第一行后就可以停止查询。
