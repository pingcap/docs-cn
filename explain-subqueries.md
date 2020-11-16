---
title: 用 Explain 查看使用子查询的执行计划
summary: 了解 TiDB 中 EXPLAIN 语句返回的执行计划信息。
---

# 用 Explain 查看使用子查询的执行计划

TiDB 会执行多种[子查询相关的优化](/subquery-optimization.md)，以提升子查询的执行性能。本文档介绍了一些常见的子查询优化方式，以及如何解读 `EXPLAIN` 语句返回的执行计划信息。

本文档所使用的示例数据如下:

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

## Inner Join（无 `UNIQUE` 约束的子查询）

在如下示例中，`IN` 子查询从表 `t2` 中搜索 id 列。考虑到语义正确性，TiDB 需要保证 `t1_id` 列是唯一的。可以使用 `EXPLAIN` 语句查看用于删除重复项并执行 `Inner Join` 操作的执行计划：

```sql
EXPLAIN SELECT * FROM t1 WHERE id IN (SELECT t1_id FROM t2);
```

```sql
+--------------------------------+----------+-----------+------------------------------+---------------------------------------------------------------------------------+
| id                             | estRows  | task      | access object                | operator info                                                                   |
+--------------------------------+----------+-----------+------------------------------+---------------------------------------------------------------------------------+
| IndexMergeJoin_19              | 45.00    | root      |                              | inner join, inner:TableReader_14, outer key:test.t2.t1_id, inner key:test.t1.id |
| ├─HashAgg_38(Build)            | 45.00    | root      |                              | group by:test.t2.t1_id, funcs:firstrow(test.t2.t1_id)->test.t2.t1_id            |
| │ └─IndexReader_39             | 45.00    | root      |                              | index:HashAgg_31                                                                |
| │   └─HashAgg_31               | 45.00    | cop[tikv] |                              | group by:test.t2.t1_id,                                                         |
| │     └─IndexFullScan_37       | 90000.00 | cop[tikv] | table:t2, index:t1_id(t1_id) | keep order:false                                                                |
| └─TableReader_14(Probe)        | 1.00     | root      |                              | data:TableRangeScan_13                                                          |
|   └─TableRangeScan_13          | 1.00     | cop[tikv] | table:t1                     | range: decided by [test.t2.t1_id], keep order:true                              |
+--------------------------------+----------+-----------+------------------------------+---------------------------------------------------------------------------------+
7 rows in set (0.00 sec)
```

由上面的查询结果可知，TiDB 首先执行 `Index Join`（`Merge Join` 的变体）操作，开始读取 `t2.t1_id` 列的索引。`t1_id` 的值会作为 `└─HashAgg_31` 算子任务的一部分，先是在 TiKV 内进行重复数据删除；然后作为 `├─HashAgg_38（Build）` 算子任务的一部分，在 TiDB 中再次进行重复数据删除。这项重复数据删除操作由聚合函数 `firstrow（test.t2.t1_id）` 执行，将结果与 `t1` 表的 `PRIMARY KEY` 约束连接在一起。

## Inner join（有 `UNIQUE` 约束的子查询）

在上述示例中，为了确保在与表 `t1` 连接之前的 `t1_id` 值是唯一的，需要执行聚合操作。但是在以下示例中，由于有 `UNIQUE` 约束，可以确保 `t3.t1_id` 是唯一的：

```sql
EXPLAIN SELECT * FROM t1 WHERE id IN (SELECT t1_id FROM t3);
```

```sql
+-----------------------------+---------+-----------+------------------------------+---------------------------------------------------------------------------------+
| id                          | estRows | task      | access object                | operator info                                                                   |
+-----------------------------+---------+-----------+------------------------------+---------------------------------------------------------------------------------+
| IndexMergeJoin_20           | 999.00  | root      |                              | inner join, inner:TableReader_15, outer key:test.t3.t1_id, inner key:test.t1.id |
| ├─IndexReader_39(Build)     | 999.00  | root      |                              | index:IndexFullScan_38                                                          |
| │ └─IndexFullScan_38        | 999.00  | cop[tikv] | table:t3, index:t1_id(t1_id) | keep order:false                                                                |
| └─TableReader_15(Probe)     | 1.00    | root      |                              | data:TableRangeScan_14                                                          |
|   └─TableRangeScan_14       | 1.00    | cop[tikv] | table:t1                     | range: decided by [test.t3.t1_id], keep order:true                              |
+-----------------------------+---------+-----------+------------------------------+---------------------------------------------------------------------------------+
5 rows in set (0.00 sec)
```

从语义上看，因为保证了 `t3.t1_id` 的唯一性，TiDB 可以直接执行 `INNER JOIN` 查询。

## Semi Join（关联查询）

在前两个示例中，通过 `HashAgg` 聚合操作来保证子查询中的数据唯一性或有 `UNIQUE` 约束之后，TiDB 能够执行 `INNER JOIN` 操作。两种连接均使用 `Index Join`（`Merge Join` 的变体）执行。

下面的例子中，TiDB 选择了一种不同的执行计划：

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

由上述查询结果可知，TiDB 执行了 `Semi Join` 算法。不同于 `Inner Join`，`Semi Join` 仅认可右键（`t2.t1_id`）上的第一个值，也就是该算法将删除作为 `Join` 算子任务一部分的重复项。`Join` 算法也是 `Merge Join`，所以会按照排序顺序同时从左侧和右侧读取数据，这是一种高效的 `Zipper Merge`。

可以认为原语句为*关联子查询*，因为它引用了存在于子查询外的一列 `t1.int_col`。然而，`EXPLAIN` 语句的返回结果显示了应用[关联子查询去关联](/correlated-subquery-optimization.md)后的执行计划。条件 `t1_id != t1.int_col` 重写为 `t1.id != t1.int_col`。TiDB 可以从表 `t1` 中读取数据并且在 `└─Selection_21` 中执行此操作，因此这种去相关和重写使执行效率大大提高。

## Anti Semi Join （`NOT IN` 子查询）

在下面的示例中，*除非*子查询中存在 `t3.t1_id`，否则查询时将从语义上返回表 `t3` 中的所有行：

```sql
EXPLAIN SELECT * FROM t3 WHERE t1_id NOT IN (SELECT id FROM t1 WHERE int_col < 100);
```

```sql
+-----------------------------+---------+-----------+---------------+-------------------------------------------------------------------------------------+
| id                          | estRows | task      | access object | operator info                                                                       |
+-----------------------------+---------+-----------+---------------+-------------------------------------------------------------------------------------+
| IndexMergeJoin_20           | 1598.40 | root      |               | anti semi join, inner:TableReader_15, outer key:test.t3.t1_id, inner key:test.t1.id |
| ├─TableReader_28(Build)     | 1998.00 | root      |               | data:TableFullScan_27                                                               |
| │ └─TableFullScan_27        | 1998.00 | cop[tikv] | table:t3      | keep order:false                                                                    |
| └─TableReader_15(Probe)     | 1.00    | root      |               | data:Selection_14                                                                   |
|   └─Selection_14            | 1.00    | cop[tikv] |               | lt(test.t1.int_col, 100)                                                            |
|     └─TableRangeScan_13     | 1.00    | cop[tikv] | table:t1      | range: decided by [test.t3.t1_id], keep order:true                                  |
+-----------------------------+---------+-----------+---------------+-------------------------------------------------------------------------------------+
6 rows in set (0.00 sec)
```

上述查询中，首先读取了表 `t3`，然后根据主键开始查询表 `t1`。join 类型是 _anti semi join_：之所以使用 _anti_，是因为上述示例有不存在匹配值（即 `NOT IN`）的情况；`Semi Join` 则是因为在仅需要匹配第一行后就可以停止 `Join` 查询了。