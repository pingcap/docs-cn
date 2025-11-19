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
+--------------------------------+----------+-----------+------------------------------+---------------------------------------------------------------------------------------------------------------------------+
| id                             | estRows  | task      | access object                | operator info                                                                                                             |
+--------------------------------+----------+-----------+------------------------------+---------------------------------------------------------------------------------------------------------------------------+
| IndexJoin_15                   | 21.11    | root      |                              | inner join, inner:TableReader_12, outer key:test.t2.t1_id, inner key:test.t1.id, equal cond:eq(test.t2.t1_id, test.t1.id) |
| ├─StreamAgg_44(Build)          | 21.11    | root      |                              | group by:test.t2.t1_id, funcs:firstrow(test.t2.t1_id)->test.t2.t1_id                                                      |
| │ └─IndexReader_45             | 21.11    | root      |                              | index:StreamAgg_34                                                                                                        |
| │   └─StreamAgg_34             | 21.11    | cop[tikv] |                              | group by:test.t2.t1_id,                                                                                                   |
| │     └─IndexFullScan_26       | 90000.00 | cop[tikv] | table:t2, index:t1_id(t1_id) | keep order:true                                                                                                           |
| └─TableReader_12(Probe)        | 21.11    | root      |                              | data:TableRangeScan_11                                                                                                    |
|   └─TableRangeScan_11          | 21.11    | cop[tikv] | table:t1                     | range: decided by [test.t2.t1_id], keep order:false                                                                       |
+--------------------------------+----------+-----------+------------------------------+---------------------------------------------------------------------------------------------------------------------------+

```

由上述查询结果可知，TiDB 通过索引连接操作 `IndexJoin_15` 将子查询做了连接转化。该执行计划首先在 TiKV 侧通过索引扫描算子 `└─IndexFullScan_26` 读取 `t2.t1_id` 列的值，然后由 `└─StreamAgg_34` 算子的部分任务在 TiKV 中对 `t1_id` 值进行去重，然后采用 `├─StreamAgg_44(Build)` 算子的部分任务在 TiDB 中对 `t1_id` 值再次进行去重，去重操作由聚合函数 `firstrow(test.t2.t1_id)` 执行；之后将操作结果与 `t1` 表的主键相连接，连接条件是 `eq(test.t1.id, test.t2.t1_id)`。

## Inner join（有 `UNIQUE` 约束的子查询）

在上述示例中，为了确保 `t1_id` 值在与表 `t1` 连接前具有唯一性，需要执行聚合运算。在以下示例中，由于 `UNIQUE` 约束已能确保 `t3.t1_id` 列值的唯一：

```sql
EXPLAIN SELECT * FROM t1 WHERE id IN (SELECT t1_id FROM t3);
```

```sql
+-----------------------------+---------+-----------+------------------------------+---------------------------------------------------------------------------------------------------------------------------+
| id                          | estRows | task      | access object                | operator info                                                                                                             |
+-----------------------------+---------+-----------+------------------------------+---------------------------------------------------------------------------------------------------------------------------+
| IndexJoin_18                | 999.00  | root      |                              | inner join, inner:TableReader_15, outer key:test.t3.t1_id, inner key:test.t1.id, equal cond:eq(test.t3.t1_id, test.t1.id) |
| ├─IndexReader_41(Build)     | 999.00  | root      |                              | index:IndexFullScan_40                                                                                                    |
| │ └─IndexFullScan_40        | 999.00  | cop[tikv] | table:t3, index:t1_id(t1_id) | keep order:false                                                                                                          |
| └─TableReader_15(Probe)     | 999.00  | root      |                              | data:TableRangeScan_14                                                                                                    |
|   └─TableRangeScan_14       | 999.00  | cop[tikv] | table:t1                     | range: decided by [test.t3.t1_id], keep order:false                                                                       |
+-----------------------------+---------+-----------+------------------------------+---------------------------------------------------------------------------------------------------------------------------+

```

从语义上看，因为约束保证了 `t3.t1_id` 列值的唯一性，TiDB 可以直接执行 `INNER JOIN` 查询。

## Semi Join（关联查询）

在前两个示例中，通过 `StreamAgg` 聚合操作或通过 `UNIQUE` 约束保证子查询数据的唯一性之后，TiDB 才能够执行 `Inner Join` 操作。这两种连接均使用了 `Index Join`。

下面的例子中，TiDB 优化器则选择了一种不同的执行计划：

```sql
EXPLAIN SELECT * FROM t1 WHERE id IN (SELECT t1_id FROM t2 WHERE t1_id != t1.int_col);
```

```sql
+-----------------------------+----------+-----------+------------------------------+--------------------------------------------------------------------------------------------------------+
| id                          | estRows  | task      | access object                | operator info                                                                                          |
+-----------------------------+----------+-----------+------------------------------+--------------------------------------------------------------------------------------------------------+
| MergeJoin_9                 | 45446.40 | root      |                              | semi join, left key:test.t1.id, right key:test.t2.t1_id, other cond:ne(test.t2.t1_id, test.t1.int_col) |
| ├─IndexReader_24(Build)     | 90000.00 | root      |                              | index:IndexFullScan_23                                                                                 |
| │ └─IndexFullScan_23        | 90000.00 | cop[tikv] | table:t2, index:t1_id(t1_id) | keep order:true                                                                                        |
| └─TableReader_22(Probe)     | 56808.00 | root      |                              | data:Selection_21                                                                                      |
|   └─Selection_21            | 56808.00 | cop[tikv] |                              | ne(test.t1.id, test.t1.int_col)                                                                        |
|     └─TableFullScan_20      | 71010.00 | cop[tikv] | table:t1                     | keep order:true                                                                                        |
+-----------------------------+----------+-----------+------------------------------+--------------------------------------------------------------------------------------------------------+
```

由上述查询结果可知，TiDB 执行了 `Semi Join`。不同于 `Inner Join`，`Semi Join` 仅允许右键 (`t2.t1_id`) 上的第一个值，也就是该操作将去除 `Join` 算子任务中的重复数据。`Join` 算法也包含 `Merge Join`，会按照排序顺序同时从左侧和右侧读取数据，这是一种高效的 `Zipper Merge`。

可以将原语句视为*关联子查询*，因为它引入了子查询外的 `t1.int_col` 列。然而，`EXPLAIN` 语句的返回结果显示的是[关联子查询去关联](/correlated-subquery-optimization.md)后的执行计划。条件 `t1_id != t1.int_col` 会被重写为 `t1.id != t1.int_col`。TiDB 可以从表 `t1` 中读取数据并且在 `└─Selection_21` 中执行此操作，因此这种去关联和重写操作会极大提高执行效率。

## Anti Semi Join（`NOT IN` 子查询）

在以下示例中，*除非*子查询中存在 `t3.t1_id`，否则该查询将（从语义上）返回表 `t3` 中的所有行：

```sql
EXPLAIN SELECT * FROM t3 WHERE t1_id NOT IN (SELECT id FROM t1 WHERE int_col < 100);
```

```sql
+-----------------------------+---------+-----------+---------------+-------------------------------------------------------------------------------------------------------------------------------+
| id                          | estRows | task      | access object | operator info                                                                                                                 |
+-----------------------------+---------+-----------+---------------+-------------------------------------------------------------------------------------------------------------------------------+
| IndexJoin_16                | 799.20  | root      |               | anti semi join, inner:TableReader_12, outer key:test.t3.t1_id, inner key:test.t1.id, equal cond:eq(test.t3.t1_id, test.t1.id) |
| ├─TableReader_28(Build)     | 999.00  | root      |               | data:TableFullScan_27                                                                                                         |
| │ └─TableFullScan_27        | 999.00  | cop[tikv] | table:t3      | keep order:false                                                                                                              |
| └─TableReader_12(Probe)     | 999.00  | root      |               | data:Selection_11                                                                                                             |
|   └─Selection_11            | 999.00  | cop[tikv] |               | lt(test.t1.int_col, 100)                                                                                                      |
|     └─TableRangeScan_10     | 999.00  | cop[tikv] | table:t1      | range: decided by [test.t3.t1_id], keep order:false                                                                           |
+-----------------------------+---------+-----------+---------------+-------------------------------------------------------------------------------------------------------------------------------+
```

上述查询首先读取了表 `t3`，然后根据主键开始探测 (probe) 表 `t1`。连接类型是 _anti semi join_，即反半连接：之所以使用 _anti_，是因为上述示例有不存在匹配值（即 `NOT IN`）的情况；使用 `Semi Join` 则是因为仅需要匹配第一行后就可以停止查询。

## Null-Aware Semi Join（`IN` 和 `= ANY` 子查询）

`IN` 和 `= ANY` 的集合运算符号具有特殊的三值属性（`true`、`false` 和 `NULL`）。这意味着在该运算符所转化得到的 Join 类型中需要对 Join key 两侧的 `NULL` 进行特殊的感知和处理。

`IN` 和 `= ANY` 算子引导的子查询会分别转为 Semi Join 和 Left Outer Semi Join。在上述 [Semi Join](#semi-join关联查询) 小节中，示例中 Join key 两侧的列 `test.t1.id` 和 `test.t2.t1_id` 都为 `not NULL` 属性，所以 Semi Join 本身不需要 Null-Aware 的性质来辅助运算，即不需要特殊处理 `NULL`。当前 TiDB 对于 Null-Aware Semi Join 没有特定的优化，其实现本质都是基于笛卡尔积加过滤 (filter) 的模式。以下为 Null-Aware Semi Join 的例子：

```sql
CREATE TABLE t(a INT, b INT);
CREATE TABLE s(a INT, b INT);
EXPLAIN SELECT (a,b) IN (SELECT * FROM s) FROM t;
EXPLAIN SELECT * FROM t WHERE (a,b) IN (SELECT * FROM s);
```

```sql
tidb> EXPLAIN SELECT (a,b) IN (SELECT * FROM s) FROM t;
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

tidb> EXPLAIN SELECT * FROM t WHERE (a,b) IN (SELECT * FROM s);
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

第一个查询 `EXPLAIN SELECT (a,b) IN (SELECT * FROM s) FROM t;` 中，由于 `t` 表和 `s` 表的 `a`、`b` 列都是 NULLABLE 的，所以 `IN` 子查询所转化的 Left Outer Semi Join 是具有 Null-Aware 性质的。具体实现是先进行笛卡尔积，然后将 `IN` 或 `= ANY` 所连接的列作为普通等值条件放到 other condition 进行过滤（filter）。

第二个查询 `EXPLAIN SELECT * FROM t WHERE (a,b) IN (SELECT * FROM s);` 中，由于 `t` 表和 `s` 表的 `a`、`b` 列都是 NULLABLE 的，`IN` 子查询本应该转为具有 Null-Aware 性质的 Semi Join，但当前 TiDB 进行了优化，直接将 Semi Join 转为了 Inner Join + Aggregate 的方式来实现。这是因为在非 scalar 输出的 `IN` 子查询中，`NULL` 和 `false` 是等效的。下推过滤的 `NULL` 行导致了 `WHERE` 子句的否定语义，因此可以事先忽略这些行。

> **注意：**
>
> `Exists` 操作符也会被转成 Semi Join，但是 `Exists` 操作符号本身不具有集合运算 Null-Aware 的性质。

## Null-Aware Anti Semi Join（`NOT IN` 和 `!= ALL` 子查询）

`NOT IN` 和 `!= ALL` 的集合运算运算具有特殊的三值属性（`true`、`false` 和 `NULL`）。这意味着在其所转化得到的 Join 类型中需要对 Join key 两侧的 `NULL` 进行特殊的感知和处理。

`NOT IN` 和 `!= ALL` 算子引导的子查询会对应地转为 Anti Semi Join 和 Anti Left Outer Semi Join。在上述的 [Anti Semi Join](#anti-semi-joinnot-in-子查询) 小节中，由于示例中 Join key 两侧的列 `test.t3.t1_id` 和 `test.t1.id` 都是 `not NULL` 属性的，所以 Anti Semi Join 本身不需要 Null-Aware 的性质来辅助计算，即不需要特殊处理 `NULL`。

在 TiDB v6.3.0 版本，TiDB 引入了针对 Null-Aware Anti Join (NAAJ) 的如下特殊优化：

- 利用 Null-Aware 的等值条件 (NA-EQ) 构建哈希连接

    由于集合操作符引入的等值需要对等值两侧操作符数的 `NULL` 值做特殊处理，这里称需要 Null-Aware 的等值条件为 NA-EQ 条件。与 v6.3.0 之前版本不同的是，TiDB 不会再将 NA-EQ 条件处理成普通 EQ 条件，而是专门放置于 Join 后置的 other condition 中，匹配笛卡尔积后再判断结果集的合法性。

    在 TiDB v6.3.0 版本中，NA-EQ 这种弱化的等值条件依然会被用来构建哈希值 (Hash Join)，大大减少了匹配时所需遍历的数据量，加速匹配过程。在 build 表 `DISTINCT` 值比例趋近 1 的时候，加速效果更为显著。

- 利用两侧数据源 `NULL` 值的特殊性质加速匹配过程的返回

    由于 Anti Semi Join 自身具有 CNF (Conjunctive normal form) 表达式的属性，其任何一侧出现的 `NULL` 值都会导致确定的结果。利用这个性质可以来加速整个匹配过程。

以下为 Null-Aware Anti Semi Join 的例子：

```sql
CREATE TABLE t(a INT, b INT);
CREATE TABLE s(a INT, b INT);
EXPLAIN SELECT (a, b) NOT IN (SELECT * FROM s) FROM t;
EXPLAIN SELECT * FROM t WHERE (a, b) NOT IN (SELECT * FROM s);
```

```sql
tidb> EXPLAIN SELECT (a, b) NOT IN (SELECT * FROM s) FROM t;
+-----------------------------+----------+-----------+---------------+---------------------------------------------------------------------------------------------+
| id                          | estRows  | task      | access object | operator info                                                                               |
+-----------------------------+----------+-----------+---------------+---------------------------------------------------------------------------------------------+
| HashJoin_8                  | 10000.00 | root      |               | Null-aware anti left outer semi join, equal:[eq(test.t.b, test.s.b) eq(test.t.a, test.s.a)] |
| ├─TableReader_12(Build)     | 10000.00 | root      |               | data:TableFullScan_11                                                                       |
| │ └─TableFullScan_11        | 10000.00 | cop[tikv] | table:s       | keep order:false, stats:pseudo                                                              |
| └─TableReader_10(Probe)     | 10000.00 | root      |               | data:TableFullScan_9                                                                        |
|   └─TableFullScan_9         | 10000.00 | cop[tikv] | table:t       | keep order:false, stats:pseudo                                                              |
+-----------------------------+----------+-----------+---------------+---------------------------------------------------------------------------------------------+
5 rows in set (0.00 sec)

tidb> EXPLAIN SELECT * FROM t WHERE (a, b) NOT IN (SELECT * FROM s);
+-----------------------------+----------+-----------+---------------+----------------------------------------------------------------------------------+
| id                          | estRows  | task      | access object | operator info                                                                    |
+-----------------------------+----------+-----------+---------------+----------------------------------------------------------------------------------+
| HashJoin_8                  | 8000.00  | root      |               | Null-aware anti semi join, equal:[eq(test.t.b, test.s.b) eq(test.t.a, test.s.a)] |
| ├─TableReader_12(Build)     | 10000.00 | root      |               | data:TableFullScan_11                                                            |
| │ └─TableFullScan_11        | 10000.00 | cop[tikv] | table:s       | keep order:false, stats:pseudo                                                   |
| └─TableReader_10(Probe)     | 10000.00 | root      |               | data:TableFullScan_9                                                             |
|   └─TableFullScan_9         | 10000.00 | cop[tikv] | table:t       | keep order:false, stats:pseudo                                                   |
+-----------------------------+----------+-----------+---------------+----------------------------------------------------------------------------------+
5 rows in set (0.00 sec)
```

第一个查询 `EXPLAIN SELECT (a, b) NOT IN (SELECT * FROM s) FROM t;` 中，由于 `t` 表和 `s` 表的 `a`、`b` 列都是 NULLABLE 的，所以 `NOT IN` 子查询所转化的 Left Outer Semi Join 是具有 Null-Aware 性质的。不同的是，NAAJ 优化将 NA-EQ 条件也作为了 Hash Join 的连接条件，大大加速了 Join 的计算。

第二个查询 `EXPLAIN SELECT * FROM t WHERE (a, b) NOT IN (SELECT * FROM s);` 中，由于 `t` 表和 `s` 表的 `a`、`b` 列都是 NULLABLE 的，所以 `NOT IN` 子查询所转化的 Anti Semi Join 是具有 Null-Aware 性质的。不同的是，NAAJ 优化将 NA-EQ 条件也作为了 Hash Join 的连接条件，大大加速了 Join 的计算。

当前 TiDB 仅针对 Anti Semi Join 和 Anti Left Outer Semi Join 实现了 `NULL` 感知。目前仅支持 Hash Join 类型且其 build 表只能固定为右侧表。

> **注意：**
>
> `Not Exists` 操作符也会被转成 Anti Semi Join，但是 `Not Exists` 符号本身不具有集合运算 Null-Aware 的性质。

## `... < ALL (SELECT ... FROM ...)` 或者 `... > ANY (SELECT ... FROM ...)`

对于这种情况，可以将 `ALL` 或者 `ANY` 用 `MAX` 以及 `MIN` 来代替。不过由于在表为空时，`MAX(EXPR)` 以及 `MIN(EXPR)` 的结果会为 `NULL`，其表现形式和 `EXPR` 有 `NULL` 值的结果一样。同时，外部表达式结果为 `NULL` 时也会影响表达式的最终结果，因此完整的改写为如下形式：

- `t.id < all(select s.id from s)` 会被改写为 `t.id < min(s.id) and if(sum(s.id is null) != 0, null, true)`。
- `t.id > any (select s.id from s)` 会被改写为 `t.id > max(s.id) or if(sum(s.id is null) != 0, null, false)`。

示例如下：

```
CREATE TABLE products (
    product_id INT PRIMARY KEY,
    product_name VARCHAR(100),
    unit_price DECIMAL(10, 2)
);

CREATE TABLE order_details (
    order_id INT,
    product_id INT,
    quantity INT,
    discount_price DECIMAL(10, 2)
);
```

```
tidb> EXPLAIN SELECT product_id, product_name, unit_price FROM products WHERE unit_price < ALL (SELECT DISTINCT discount_price FROM order_details  ); 
+------------------------------+----------+-----------+---------------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| id                           | estRows  | task      | access object       | operator info                                                                                                                                                                        |
+------------------------------+----------+-----------+---------------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| HashJoin_27                  | 10000.00 | root      |                     | CARTESIAN inner join, other cond:or(and(lt(test.products.unit_price, Column#9), if(ne(Column#10, 0), NULL, 1)), or(eq(Column#11, 0), if(isnull(test.products.unit_price), NULL, 0))) |
| ├─HashAgg_55(Build)          | 1.00     | root      |                     | funcs:min(Column#16)->Column#9, funcs:sum(Column#17)->Column#10, funcs:count(1)->Column#11                                                                                           |
| │ └─Projection_82            | 8000.00  | root      |                     | test.order_details.discount_price->Column#16, cast(isnull(test.order_details.discount_price), decimal(20,0) BINARY)->Column#17                                                       |
| │   └─HashAgg_66             | 8000.00  | root      |                     | group by:test.order_details.discount_price, funcs:firstrow(test.order_details.discount_price)->test.order_details.discount_price                                                     |
| │     └─TableReader_67       | 8000.00  | root      |                     | data:HashAgg_59                                                                                                                                                                      |
| │       └─HashAgg_59         | 8000.00  | cop[tikv] |                     | group by:test.order_details.discount_price,                                                                                                                                          |
| │         └─TableFullScan_65 | 10000.00 | cop[tikv] | table:order_details | keep order:false, stats:pseudo                                                                                                                                                       |
| └─TableReader_30(Probe)      | 10000.00 | root      |                     | data:TableFullScan_29                                                                                                                                                                |
|   └─TableFullScan_29         | 10000.00 | cop[tikv] | table:products      | keep order:false, stats:pseudo                                                                                                                                                       |
+------------------------------+----------+-----------+---------------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+

tidb> EXPLAIN SELECT product_id, product_name, unit_price FROM products WHERE unit_price > ALL (SELECT DISTINCT discount_price FROM order_details  ); 
+------------------------------+----------+-----------+---------------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| id                           | estRows  | task      | access object       | operator info                                                                                                                                                                        |
+------------------------------+----------+-----------+---------------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| HashJoin_27                  | 10000.00 | root      |                     | CARTESIAN inner join, other cond:or(and(gt(test.products.unit_price, Column#9), if(ne(Column#10, 0), NULL, 1)), or(eq(Column#11, 0), if(isnull(test.products.unit_price), NULL, 0))) |
| ├─HashAgg_55(Build)          | 1.00     | root      |                     | funcs:max(Column#16)->Column#9, funcs:sum(Column#17)->Column#10, funcs:count(1)->Column#11                                                                                           |
| │ └─Projection_82            | 8000.00  | root      |                     | test.order_details.discount_price->Column#16, cast(isnull(test.order_details.discount_price), decimal(20,0) BINARY)->Column#17                                                       |
| │   └─HashAgg_66             | 8000.00  | root      |                     | group by:test.order_details.discount_price, funcs:firstrow(test.order_details.discount_price)->test.order_details.discount_price                                                     |
| │     └─TableReader_67       | 8000.00  | root      |                     | data:HashAgg_59                                                                                                                                                                      |
| │       └─HashAgg_59         | 8000.00  | cop[tikv] |                     | group by:test.order_details.discount_price,                                                                                                                                          |
| │         └─TableFullScan_65 | 10000.00 | cop[tikv] | table:order_details | keep order:false, stats:pseudo                                                                                                                                                       |
| └─TableReader_30(Probe)      | 10000.00 | root      |                     | data:TableFullScan_29                                                                                                                                                                |
|   └─TableFullScan_29         | 10000.00 | cop[tikv] | table:products      | keep order:false, stats:pseudo                                                                                                                                                       |
+------------------------------+----------+-----------+---------------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
```

## `... IN (SELECT ... FROM ...)`

对于这种情况，TiDB 会将其 `IN` 的子查询改写为 `SELECT ... FROM ... GROUP ...` 的形式，然后将 `IN` 改写为普通的 `JOIN` 的形式。如 `SELECT * FROM t1 WHERE t1.a IN (SELECT t2.a FROM t2)` 会被改写为 `SELECT t1.* FROM t1, (SELECT DISTINCT a AS a FROM t2) t2 WHERE t1.a = t2.a` 的形式。同时这里的 `DISTINCT` 可以在 `t2.a` 具有 `UNIQUE` 属性时被自动消去。

```sql
EXPLAIN SELECT * FROM t1 WHERE t1.a IN (SELECT t2.a FROM t2);
```

```sql
+------------------------------+---------+-----------+------------------------+----------------------------------------------------------------------------+
| id                           | estRows | task      | access object          | operator info                                                              |
+------------------------------+---------+-----------+------------------------+----------------------------------------------------------------------------+
| IndexJoin_12                 | 9990.00 | root      |                        | inner join, inner:TableReader_11, outer key:test.t2.a, inner key:test.t1.a |
| ├─HashAgg_21(Build)          | 7992.00 | root      |                        | group by:test.t2.a, funcs:firstrow(test.t2.a)->test.t2.a                   |
| │ └─IndexReader_28           | 9990.00 | root      |                        | index:IndexFullScan_27                                                     |
| │   └─IndexFullScan_27       | 9990.00 | cop[tikv] | table:t2, index:idx(a) | keep order:false, stats:pseudo                                             |
| └─TableReader_11(Probe)      | 7992.00 | root      |                        | data:TableRangeScan_10                                                     |
|   └─TableRangeScan_10        | 7992.00 | cop[tikv] | table:t1               | range: decided by [test.t2.a], keep order:false, stats:pseudo              |
+------------------------------+---------+-----------+------------------------+----------------------------------------------------------------------------+
```

这个改写会在 `IN` 子查询相对较小、而外部查询相对较大时产生更好的执行性能。因为不经过改写的情况下，TiDB 无法使用以 `t2` 为驱动表的 `index join`。需要注意，当改写生成的聚合无法被自动消去且 `t2` 表比较大时，反而会影响查询的性能。你可以使用 [`tidb_opt_insubq_to_join_and_agg`](/system-variables.md#tidb_opt_insubq_to_join_and_agg) 变量来控制该优化。当遇到适用的情况，可以手动关闭。

## 其他类型查询的执行计划

+ [MPP 模式查询的执行计划](/explain-mpp.md)
+ [索引查询的执行计划](/explain-indexes.md)
+ [Join 查询的执行计划](/explain-joins.md)
+ [聚合查询的执行计划](/explain-aggregation.md)
+ [视图查询的执行计划](/explain-views.md)
+ [分区查询的执行计划](/explain-partitions.md)
+ [索引合并查询的执行计划](/explain-index-merge.md)
