---
title: 用 EXPLAIN 查看子查询的执行计划
summary: 了解 TiDB 中 EXPLAIN 语句返回的执行计划信息。
---

# 用 EXPLAIN 查看子查询的执行计划

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

由上述查询结果可知，TiDB 通过索引连接操作 `| IndexJoin_14` 将子查询做了连接转化。该执行计划首先在 TiKV 侧通过索引扫描算子 `└─IndexFullScan_31` 读取 `t2.t1_id` 列的值，然后由 `└─StreamAgg_39` 算子的部分任务在 TiKV 中对 `t1_id` 值进行去重，然后采用 `├─StreamAgg_49(Build)` 算子的部分任务在 TiDB 中对 `t1_id` 值再次进行去重，去重操作由聚合函数 `firstrow(test.t2.t1_id)` 执行；之后将操作结果与 `t1` 表的主键相连接，连接条件是 `eq(test.t1.id, test.t2.t1_id)`。

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

在前两个示例中，通过 `StreamAgg` 聚合操作或通过 `UNIQUE` 约束保证子查询数据的唯一性之后，TiDB 才能够执行 `Inner Join` 操作。这两种连接均使用了 `Index Join`。

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

## Null Aware Semi Join （`IN`, `= ANY` 子查询）

`IN`, `= ANY` 的集合运算符号具有特殊的三值属性（true、false、NULL）。这也意味这在其所转化得到的 join 类型中需要对 join key 两侧的 null 进行特殊的感知和处理。

对于 `IN`, `= ANY` 算子而言，其所引导的子查询，会对应的转为 Semi Join 和 Left Outer Semi Join，在上述 Semi Join 小节中， 由于其 join key 的两侧列 test.t1.id 和 test.t2.t1_id 都是 not null 属性的，所以 semi join 本身不需要 null aware 的性质来辅助运算。当前 TiDB 对于 Null Aware Semi Join 没有特定的优化，其实现本质都是基于笛卡尔积加 filter 的模式。以下为 null aware 的例子：

```sql
create table t(a int, b int);
create table s(a int, b int);
explain select (a,b) in (select * from s) from t;
explain select * from t where (a,b) in (select * from s);
```

```sql
tidb> explain select (a,b) in (select * from s) from t;
+-----------------------------+---------+-----------+---------------+-------------------------------------------------------------------------------------------+
| id                          | estRows | task      | access object | operator info                                                                             |
+-----------------------------+---------+-----------+---------------+-------------------------------------------------------------------------------------------+
| HashJoin_8                  | 1.00    | root      |               | CARTESIAN left outer semi join, other cond:eq(test.t.a, test.s.a), eq(test.t.b, test.s.b) |
| ├─TableReader_12(Build)     | 1.00    | root      |               | data:TableFullScan_11                                                                     |
| │ └─TableFullScan_11        | 1.00    | cop[tikv] | table:s       | keep order:false, stats:pseudo                                                            |
| └─TableReader_10(Probe)     | 1.00    | root      |               | data:TableFullScan_9                                                                      |
|   └─TableFullScan_9         | 1.00    | cop[tikv] | table:t       | keep order:false, stats:pseudo                                                            |
+-----------------------------+---------+-----------+---------------+-------------------------------------------------------------------------------------------+
5 rows in set (0.00 sec)

tidb> explain select * from t where (a,b) in (select * from s);
+------------------------------+---------+-----------+---------------+-----------------------------------------------------------------------------------------------------+
| id                           | estRows | task      | access object | operator info                                                                                       |
+------------------------------+---------+-----------+---------------+-----------------------------------------------------------------------------------------------------+
| HashJoin_11                  | 1.00    | root      |               | inner join, equal:[eq(test.t.a, test.s.a) eq(test.t.b, test.s.b)]                                   |
| ├─TableReader_14(Build)      | 1.00    | root      |               | data:Selection_13                                                                                   |
| │ └─Selection_13             | 1.00    | cop[tikv] |               | not(isnull(test.t.a)), not(isnull(test.t.b))                                                        |
| │   └─TableFullScan_12       | 1.00    | cop[tikv] | table:t       | keep order:false, stats:pseudo                                                                      |
| └─HashAgg_17(Probe)          | 1.00    | root      |               | group by:test.s.a, test.s.b, funcs:firstrow(test.s.a)->test.s.a, funcs:firstrow(test.s.b)->test.s.b |
|   └─TableReader_24           | 1.00    | root      |               | data:Selection_23                                                                                   |
|     └─Selection_23           | 1.00    | cop[tikv] |               | not(isnull(test.s.a)), not(isnull(test.s.b))                                                        |
|       └─TableFullScan_22     | 1.00    | cop[tikv] | table:s       | keep order:false, stats:pseudo                                                                      |
+------------------------------+---------+-----------+---------------+-----------------------------------------------------------------------------------------------------+
8 rows in set (0.01 sec)
```

第一个查询中，由于 t 表和 s 表的 a，b 列都是 nullable 的，所以其所转化 left outer semi join 是具有 null aware 性质的。其实现是先通过笛卡尔乘积，然后将 `IN` 或者 `= ANY` 所连接的列作为普通等值条件放到 other condition 做过滤（笛卡尔积之后的 filter）实现的。

第二个查询中，由于 t 表和 s 表的 a，b 列都是 nullable 的，`IN` 属性本应该转为 null aware 性质的 semi join，但当前 TiDB 会有一层优化，会直接将 semi 转为了 inner join + aggregate 的方式来实现。（因为在非 scalar 输出的 `IN` sub-query 中，NULL 和 false 具有等效结果，其下推过滤的 NULL 行，就其本身来说都是导致 where 子句的否定语义，因此可以事先忽略这些行）

注意：`Exists` 操作符也会转成 Semi Join，但是 Exists 操作符号本身不具有集合运算 null-aware 的性质。

## Null Aware Anti Semi Join （`NOT IN`, `!= ALL` 子查询）

`NOT IN`, `!= ALL` 的集合运算运算具有特殊的三值属性（true、false、NULL）。这也意味这在其所转化得到的 join 类型中需要对 join key 两侧的 null 进行特殊的感知和处理。

对于 `NOT IN`, `!= ALL` 算子而言，其所引导的子查询，会对应的转为 Anti Semi Join 和 Anti Left Outer Semi Join。在上述的 Anti Semi Join 小节中，由于其 join key 的两侧列 test.t3.t1_id 和 test.t1.id 都是 not null 属性的，所以 Anti Semi Join 本身不需要 null aware 的性质来辅助计算。在 TiDB v6.3 及后续的版本中，TiDB 引入了针对 Null Aware Anti Join 的特殊优化，1：利用 NA-EQ 构建哈希连接； 2：利用两侧数据源 null 值的特殊性质加速匹配结果的返回。由于集合操作符引入的等值需要对等值两侧操作符数的 null 值做特殊处理，这里称需要 null-aware 的等值条件为 NA-EQ 条件。不同以往的是，TiDB 不会再将 NA-EQ 条件处理成普通 EQ 条件，专门放置于 join 后置的 other condition 中，匹配完笛卡尔积之后再去判断结果集的合法性。在本次优化中，NA-EQ 这种弱化的等值条件会依然会被用来构建哈希值（hash join）加速匹配过程，大大简略了匹配时候所需要遍历的数据量，在 build 表 distinct 值很大的时候，效果会有质的提升。此外，由于 Anti Semi Join 自身具有 CNF 表达式的属性，其任何一侧出现的 null 值都会导致结果的确定性，利用这种性质我们可以来整个加速匹配过程的返回。 以下为 null aware 的例子：

```sql
create table t(a int, b int);
create table s(a int, b int);
explain select  (a, b) not in (select * from s) from t;
explain select * from t where (a, b) not in (select * from s);
```

```sql
tidb> explain select  (a, b) not in (select * from s) from t;
+-----------------------------+---------+-----------+---------------+---------------------------------------------------------------------------------------+
| id                          | estRows | task      | access object | operator info                                                                         |
+-----------------------------+---------+-----------+---------------+---------------------------------------------------------------------------------------+
| HashJoin_8                  | 1.00    | root      |               | NAAJ anti left outer semi join, equal:[eq(test.t.b, test.s.b) eq(test.t.a, test.s.a)] |
| ├─TableReader_12(Build)     | 1.00    | root      |               | data:TableFullScan_11                                                                 |
| │ └─TableFullScan_11        | 1.00    | cop[tikv] | table:s       | keep order:false, stats:pseudo                                                        |
| └─TableReader_10(Probe)     | 1.00    | root      |               | data:TableFullScan_9                                                                  |
|   └─TableFullScan_9         | 1.00    | cop[tikv] | table:t       | keep order:false, stats:pseudo                                                        |
+-----------------------------+---------+-----------+---------------+---------------------------------------------------------------------------------------+
5 rows in set (0.00 sec)

tidb> explain select * from t where (a, b) not in (select * from s);
+-----------------------------+---------+-----------+---------------+----------------------------------------------------------------------------+
| id                          | estRows | task      | access object | operator info                                                              |
+-----------------------------+---------+-----------+---------------+----------------------------------------------------------------------------+
| HashJoin_8                  | 0.80    | root      |               | NAAJ anti semi join, equal:[eq(test.t.b, test.s.b) eq(test.t.a, test.s.a)] |
| ├─TableReader_12(Build)     | 1.00    | root      |               | data:TableFullScan_11                                                      |
| │ └─TableFullScan_11        | 1.00    | cop[tikv] | table:s       | keep order:false, stats:pseudo                                             |
| └─TableReader_10(Probe)     | 1.00    | root      |               | data:TableFullScan_9                                                       |
|   └─TableFullScan_9         | 1.00    | cop[tikv] | table:t       | keep order:false, stats:pseudo                                             |
+-----------------------------+---------+-----------+---------------+----------------------------------------------------------------------------+
5 rows in set (0.00 sec)
```

第一个查询中，由于 t 表和 s 表的 a，b 列都是 nullable 的，所以其所转化的 left outer semi join 是具有 null aware 性质的。不同的是，NAAJ 优化会将 NA-EQ 等值条件也作为了 hash join 的连接条件，大大加速的了 join 的计算。

第二个查询中，由于 t 表和 s 表的 a，b 列都是 nullable 的，所以其所转化的 anti semi join 是具有 null aware 性质的。不同的是，NAAJ 优化将 NA-EQ 等值条件也作为了 hash join 的连接条件，大大加速的了 join 的计算。

当前 TiDB 仅针对 Anti Semi Join 和 Anti Left Outer Semi Join 实现了 null 感知，当前仅支持 Hash Join 类型且其 build 表只能固定为右侧表。NAAJ 摒弃了之前基于笛卡尔乘积和 other condition filter 的实现方式，利用 NA-EQ 构建哈希连接，并利用 null 值在 Anti Join 集合运算中的快速返回的性质加速了整个 join 的匹配过程。

注意：`Not Exists` 操作符也会转成 Anti Semi Join，但是 `Not Exists` 符号本身不具有集合运算 null-aware 的性质。

## 其他类型查询的执行计划

+ [MPP 模式查询的执行计划](/explain-mpp.md)
+ [索引查询的执行计划](/explain-indexes.md)
+ [Join 查询的执行计划](/explain-joins.md)
+ [聚合查询的执行计划](/explain-aggregation.md)
+ [视图查询的执行计划](/explain-views.md)
+ [分区查询的执行计划](/explain-partitions.md)
+ [索引合并查询的执行计划](/explain-index-merge.md)
