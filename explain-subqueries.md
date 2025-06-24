---
title: 解释使用子查询的语句
summary: 了解 TiDB 中 EXPLAIN 语句返回的执行计划信息。
---

# 解释使用子查询的语句

TiDB 执行[多种优化](/subquery-optimization.md)来提高子查询的性能。本文档描述了一些常见子查询的优化方法，以及如何解释 `EXPLAIN` 的输出。

本文档中的示例基于以下示例数据：

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

## 内连接（非唯一子查询）

在以下示例中，`IN` 子查询从表 `t2` 中搜索 ID 列表。为了语义正确性，TiDB 需要保证列 `t1_id` 是唯一的。使用 `EXPLAIN`，您可以看到用于删除重复项并执行 `INNER JOIN` 操作的执行计划：

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

从上面的查询结果中，您可以看到 TiDB 使用索引连接操作 `IndexJoin_15` 来连接和转换子查询。在执行计划中，执行过程如下：

1. TiKV 端的索引扫描算子 `└─IndexFullScan_26` 读取 `t2.t1_id` 列的值。
2. TiKV 中的 `└─StreamAgg_34` 算子任务对 `t1_id` 的值进行去重。
3. TiDB 中的 `├─StreamAgg_44(Build)` 算子任务对 `t1_id` 的值进行去重。去重是通过聚合函数 `firstrow(test.t2.t1_id)` 完成的。
4. 操作结果与 `t1` 表的主键进行连接。连接条件是 `eq(test.t1.id, test.t2.t1_id)`。

## 内连接（唯一子查询）

在前面的示例中，在与表 `t1` 连接之前需要聚合以确保 `t1_id` 的值是唯一的。但在以下示例中，由于 `UNIQUE` 约束，`t3.t1_id` 已经保证是唯一的：

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

从语义上讲，因为 `t3.t1_id` 保证是唯一的，所以它可以直接作为 `INNER JOIN` 执行。

## 半连接（相关子查询）

在前面的两个示例中，TiDB 能够在子查询中的数据变得唯一（通过 `StreamAgg`）或保证唯一后执行 `INNER JOIN` 操作。两个连接都使用索引连接执行。

在这个示例中，TiDB 选择了不同的执行计划：

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

从上面的结果中，您可以看到 TiDB 使用了 `Semi Join` 算法。半连接与内连接不同：半连接只允许右键（`t2.t1_id`）上的第一个值，这意味着重复项作为连接算子任务的一部分被消除。连接算法也是归并连接，就像一个高效的拉链合并，因为算子按排序顺序从左右两侧读取数据。

原始语句被认为是一个_相关子查询_，因为子查询引用了子查询外部存在的列（`t1.int_col`）。但是，`EXPLAIN` 的输出显示了应用[子查询去相关优化](/correlated-subquery-optimization.md)后的执行计划。条件 `t1_id != t1.int_col` 被重写为 `t1.id != t1.int_col`。TiDB 可以在读取表 `t1` 的数据时在 `└─Selection_21` 中执行此操作，因此这种去相关和重写使执行效率更高。

## 反半连接（`NOT IN` 子查询）

在以下示例中，查询语义上返回表 `t3` 中的所有行，_除非_ `t3.t1_id` 在子查询中：

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

这个查询首先读取表 `t3`，然后根据 `PRIMARY KEY` 探测表 `t1`。连接类型是一个_反半连接_；反是因为这个示例是针对值的不存在（`NOT IN`），半连接是因为只需要第一行匹配就可以拒绝连接。

## 空值感知半连接（`IN` 和 `= ANY` 子查询）

`IN` 或 `= ANY` 集合运算符的值是三值的（`true`、`false` 和 `NULL`）。对于从这两个运算符转换而来的连接类型，TiDB 需要感知连接键两侧的 `NULL` 并以特殊方式处理。

包含 `IN` 和 `= ANY` 运算符的子查询分别转换为半连接和左外半连接。在前面的[半连接](#半连接相关子查询)示例中，由于连接键两侧的列 `test.t1.id` 和 `test.t2.t1_id` 都是 `not NULL`，因此半连接不需要考虑空值感知（不需要特殊处理 `NULL`）。TiDB 基于笛卡尔积和过滤器处理空值感知半连接，没有特殊优化。以下是一个示例：

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

在第一个查询语句 `EXPLAIN SELECT (a,b) IN (SELECT * FROM s) FROM t;` 中，由于表 `t` 和 `s` 的列 `a` 和 `b` 都是 NULLABLE，由 `IN` 子查询转换的左外半连接是空值感知的。具体来说，首先计算笛卡尔积，然后将由 `IN` 或 `= ANY` 连接的列作为普通相等查询放入其他条件中进行过滤。

在第二个查询语句 `EXPLAIN SELECT * FROM t WHERE (a,b) IN (SELECT * FROM s);` 中，由于表 `t` 和 `s` 的列 `a` 和 `b` 都是 NULLABLE，`IN` 子查询应该转换为空值感知半连接。但是 TiDB 通过将半连接转换为内连接和聚合来优化它。这是因为对于非标量输出，`IN` 子查询中的 `NULL` 和 `false` 是等价的。下推过滤器中的 `NULL` 行导致 `WHERE` 子句的负面语义。因此，可以提前忽略这些行。

> **注意：**
>
> `Exists` 运算符也转换为半连接，但它不是空值感知的。

## 空值感知反半连接（`NOT IN` 和 `!= ALL` 子查询）

`NOT IN` 或 `!= ALL` 集合运算符的值是三值的（`true`、`false` 和 `NULL`）。对于从这两个运算符转换而来的连接类型，TiDB 需要感知连接键两侧的 `NULL` 并以特殊方式处理。

包含 `NOT IN` 和 `!= ALL` 运算符的子查询分别转换为反半连接和反左外半连接。在前面的[反半连接](#反半连接not-in-子查询)示例中，由于连接键两侧的列 `test.t3.t1_id` 和 `test.t1.id` 都是 `not NULL`，因此反半连接不需要考虑空值感知（不需要特殊处理 `NULL`）。

TiDB v6.3.0 对空值感知反连接（NAAJ）进行了以下优化：

- 使用空值感知相等条件（NA-EQ）构建哈希连接

    集合运算符引入了相等条件，该条件需要对运算符两侧的 `NULL` 值进行特殊处理。需要空值感知的相等条件称为 NA-EQ。与早期版本不同，TiDB v6.3.0 不再像以前那样处理 NA-EQ，而是将其放在连接后的其他条件中，然后在匹配笛卡尔积后确定结果集的合法性。

    从 TiDB v6.3.0 开始，仍然使用 NA-EQ（一个弱化的相等条件）来构建哈希连接。这减少了需要遍历的匹配数据量，加快了匹配过程。当构建表的 `DISTINCT()` 值总百分比接近 100% 时，加速效果更显著。

- 利用 `NULL` 的特殊属性加快匹配结果的返回

    由于反半连接是合取范式（CNF），连接任一侧的 `NULL` 都会导致确定的结果。可以利用这个属性来加快整个匹配过程的返回。

以下是一个示例：

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

在第一个查询语句 `EXPLAIN SELECT (a, b) NOT IN (SELECT * FROM s) FROM t;` 中，由于表 `t` 和 `s` 的列 `a` 和 `b` 都是 NULLABLE，由 `NOT IN` 子查询转换的左外半连接是空值感知的。不同之处在于 NAAJ 优化也使用 NA-EQ 作为哈希连接条件，这大大加快了连接计算。

在第二个查询语句 `EXPLAIN SELECT * FROM t WHERE (a, b) NOT IN (SELECT * FROM s);` 中，由于表 `t` 和 `s` 的列 `a` 和 `b` 都是 NULLABLE，由 `NOT IN` 子查询转换的反半连接是空值感知的。不同之处在于 NAAJ 优化也使用 NA-EQ 作为哈希连接条件，这大大加快了连接计算。

目前，TiDB 只能对反半连接和反左外半连接进行空值感知。只支持哈希连接类型，并且其构建表应固定为右表。

> **注意：**
>
> `Not Exists` 运算符也转换为反半连接，但它不是空值感知的。

## 解释使用其他类型子查询的语句

+ [解释 MPP 模式下的语句](/explain-mpp.md)
+ [解释使用索引的语句](/explain-indexes.md)
+ [解释使用连接的语句](/explain-joins.md)
+ [解释使用聚合的语句](/explain-aggregation.md)
+ [解释使用视图的语句](/explain-views.md)
+ [解释使用分区的语句](/explain-partitions.md)
+ [解释使用索引合并的语句](/explain-index-merge.md)
