---
title: 从窗口函数中推导 TopN 或 Limit
summary: 介绍从窗口函数中推导 TopN 或 Limit 的优化规则，以及如何开启该规则。
---

# 从窗口函数中推导 TopN 或 Limit

[窗口函数](/functions-and-operators/window-functions.md)是一种常见的 SQL 函数。对于 `ROW_NUMBER()` 或者 `RANK()` 等编号相关的窗口函数，一种常见的用法是在进行窗口函数求值之后，对求值的结果进行过滤，例如：

```sql
SELECT * FROM (SELECT ROW_NUMBER() OVER (ORDER BY a) AS rownumber FROM t) dt WHERE rownumber <= 3
```

按照正常的 SQL 执行流程，TiDB 需要先对 `t` 表的所有数据进行排序，然后为每一行都求得相应的 `ROW_NUMBER()` 结果，最后再进行 `rownumber <= 3` 的过滤。 

从 v7.0.0 开始，TiDB 支持从窗口函数中推导 TopN 或 Limit 算子。通过该优化规则，TiDB 可以将原始 SQL 等价改写成以下形式：

```sql
WITH t_topN AS (SELECT a FROM t1 ORDER BY a LIMIT 3) SELECT * FROM (SELECT ROW_NUMBER() OVER (ORDER BY a) AS rownumber FROM t_topN) dt WHERE rownumber <= 3
```

可以看出，改写后，TiDB 可以从窗口函数与后续的过滤条件中推导出一个 TopN 算子，相比于原始 SQL 中的 Sort 算子（对应 `ORDER BY`），TopN 算子的运行效率远高于 Sort 算子，而且 TiKV 和 TiFlash 均支持 TopN 算子的下推，因此能进一步提升改写后的 SQL 的性能。

从窗口函数中推导 TopN 或 Limit 默认关闭。你可以通过将 session 变量 [tidb_opt_derive_topn](/system-variables.md#tidb_opt_derive_topn-从-v700-版本开始引入) 设置为 `ON` 开启该功能。

开启后，如需关闭，可以进行以下操作之一：

* 设置 session 变量 [tidb_opt_derive_topn](/system-variables.md#tidb_opt_derive_topn-从-v700-版本开始引入) 为 `false`。
* 可参照[优化规则及表达式下推的黑名单](/blocklist-control-plan.md)中的关闭方法。

## 限制

* 目前仅 `ROW_NUMBER()` 窗口函数支持 SQL 语句改写。
* 只有当 SQL 语句的过滤条件是针对 `ROW_NUMBER()` 结果而且过滤条件为 `<` 或者 `<=` 时，TiDB 才支持改写 SQL 语句。

## 示例

以下通过一些例子对该优化规则进行说明。

### 不包含 PARTITION BY 的窗口函数

#### 示例 1：不包含 ORDER BY 的窗口函数

```sql
CREATE TABLE t(id int, value int);
SET tidb_opt_derive_topn=on;
EXPLAIN SELECT * FROM (SELECT ROW_NUMBER() OVER () AS rownumber FROM t) dt WHERE rownumber <= 3;
```

```
+----------------------------------+---------+-----------+---------------+-----------------------------------------------------------------------+
| id                               | estRows | task      | access object | operator info                                                         |
+----------------------------------+---------+-----------+---------------+-----------------------------------------------------------------------+
| Projection_9                     | 2.40    | root      |               | Column#5                                                              |
| └─Selection_10                   | 2.40    | root      |               | le(Column#5, 3)                                                       |
|   └─Window_11                    | 3.00    | root      |               | row_number()->Column#5 over(rows between current row and current row) |
|     └─Limit_15                   | 3.00    | root      |               | offset:0, count:3                                                     |
|       └─TableReader_26           | 3.00    | root      |               | data:Limit_25                                                         |
|         └─Limit_25               | 3.00    | cop[tikv] |               | offset:0, count:3                                                     |
|           └─TableFullScan_24     | 3.00    | cop[tikv] | table:t       | keep order:false, stats:pseudo                                        |
+----------------------------------+---------+-----------+---------------+-----------------------------------------------------------------------+
```

在该查询中，优化器从窗口函数中推导出来了 Limit 并将它下推给了 TiKV。

#### 示例 2：包含 ORDER BY 的窗口函数

```sql
CREATE TABLE t(id int, value int);
SET tidb_opt_derive_topn=on;
EXPLAIN SELECT * FROM (SELECT ROW_NUMBER() OVER (ORDER BY value) AS rownumber FROM t) dt WHERE rownumber <= 3;
```

```
+----------------------------------+----------+-----------+---------------+---------------------------------------------------------------------------------------------+
| id                               | estRows  | task      | access object | operator info                                                                               |
+----------------------------------+----------+-----------+---------------+---------------------------------------------------------------------------------------------+
| Projection_10                    | 2.40     | root      |               | Column#5                                                                                    |
| └─Selection_11                   | 2.40     | root      |               | le(Column#5, 3)                                                                             |
|   └─Window_12                    | 3.00     | root      |               | row_number()->Column#5 over(order by test.t.value rows between current row and current row) |
|     └─TopN_13                    | 3.00     | root      |               | test.t.value, offset:0, count:3                                                             |
|       └─TableReader_25           | 3.00     | root      |               | data:TopN_24                                                                                |
|         └─TopN_24                | 3.00     | cop[tikv] |               | test.t.value, offset:0, count:3                                                             |
|           └─TableFullScan_23     | 10000.00 | cop[tikv] | table:t       | keep order:false, stats:pseudo                                                              |
+----------------------------------+----------+-----------+---------------+---------------------------------------------------------------------------------------------+
```

在该查询中，优化器从窗口函数中推导出来了 TopN 并将它下推给了 TiKV。

### 包含 PARTITION BY 的窗口函数

> **注意：**
>
> 当窗口函数包含 PARTITION BY 时，该优化规则仅在 partition 列是主键的前缀且主键是聚簇索引的时候才能生效。

#### 示例 3：不包含 ORDER BY 的窗口函数

```sql
CREATE TABLE t(id1 int, id2 int, value1 int, value2 int, primary key(id1,id2) clustered);
SET tidb_opt_derive_topn=on;
EXPLAIN SELECT * FROM (SELECT ROW_NUMBER() OVER (PARTITION BY id1) AS rownumber FROM t) dt WHERE rownumber <= 3;
```

```
+------------------------------------+---------+-----------+---------------+-----------------------------------------------------------------------------------------------+
| id                                 | estRows | task      | access object | operator info                                                                                 |
+------------------------------------+---------+-----------+---------------+-----------------------------------------------------------------------------------------------+
| Projection_10                      | 2.40    | root      |               | Column#6                                                                                      |
| └─Selection_11                     | 2.40    | root      |               | le(Column#6, 3)                                                                               |
|   └─Shuffle_26                     | 3.00    | root      |               | execution info: concurrency:2, data sources:[TableReader_24]                                  |
|     └─Window_12                    | 3.00    | root      |               | row_number()->Column#6 over(partition by test.t.id1 rows between current row and current row) |
|       └─Sort_25                    | 3.00    | root      |               | test.t.id1                                                                                    |
|         └─TableReader_24           | 3.00    | root      |               | data:Limit_23                                                                                 |
|           └─Limit_23               | 3.00    | cop[tikv] |               | partition by test.t.id1, offset:0, count:3                                                    |
|             └─TableFullScan_22     | 3.00    | cop[tikv] | table:t       | keep order:false, stats:pseudo                                                                |
+------------------------------------+---------+-----------+---------------+-----------------------------------------------------------------------------------------------+
```

在该查询中，优化器从窗口函数中推导出来了 Limit 并将它下推给了 TiKV。值得一提的是这个 Limit 其实是 partition Limit，也就是说对于每个相同 `id1` 值组成的一组数据上都会进行一次 Limit。

#### 示例 4：包含 ORDER BY 的窗口函数

```sql
CREATE TABLE t(id1 int, id2 int, value1 int, value2 int, primary key(id1,id2) clustered);
SET tidb_opt_derive_topn=on;
EXPLAIN SELECT * FROM (SELECT ROW_NUMBER() OVER (PARTITION BY id1 ORDER BY value1) AS rownumber FROM t) dt WHERE rownumber <= 3;
```

```
+------------------------------------+----------+-----------+---------------+----------------------------------------------------------------------------------------------------------------------+
| id                                 | estRows  | task      | access object | operator info                                                                                                        |
+------------------------------------+----------+-----------+---------------+----------------------------------------------------------------------------------------------------------------------+
| Projection_10                      | 2.40     | root      |               | Column#6                                                                                                             |
| └─Selection_11                     | 2.40     | root      |               | le(Column#6, 3)                                                                                                      |
|   └─Shuffle_23                     | 3.00     | root      |               | execution info: concurrency:3, data sources:[TableReader_21]                                                         |
|     └─Window_12                    | 3.00     | root      |               | row_number()->Column#6 over(partition by test.t.id1 order by test.t.value1 rows between current row and current row) |
|       └─Sort_22                    | 3.00     | root      |               | test.t.id1, test.t.value1                                                                                            |
|         └─TableReader_21           | 3.00     | root      |               | data:TopN_19                                                                                                         |
|           └─TopN_19                | 3.00     | cop[tikv] |               | partition by test.t.id1 order by test.t.value1, offset:0, count:3                                                    |
|             └─TableFullScan_18     | 10000.00 | cop[tikv] | table:t       | keep order:false, stats:pseudo                                                                                       |
+------------------------------------+----------+-----------+---------------+----------------------------------------------------------------------------------------------------------------------+
```

在该查询中，优化器从窗口函数中推导出来了 TopN 并将它下推给了 TiKV。需要注意的是，这个 TopN 其实是 partition 的 TopN, 也就是说对于每个相同 `id1` 值组成的一组数据上都会进行一次 TopN。

#### 示例 5：PARTITION BY 列不是主键的前缀

```sql
CREATE TABLE t(id1 int, id2 int, value1 int, value2 int, primary key(id1,id2) clustered);
SET tidb_opt_derive_topn=on;
EXPLAIN SELECT * FROM (SELECT ROW_NUMBER() OVER (PARTITION BY value1) AS rownumber FROM t) dt WHERE rownumber <= 3;
```

```
+----------------------------------+----------+-----------+---------------+--------------------------------------------------------------------------------------------------+
| id                               | estRows  | task      | access object | operator info                                                                                    |
+----------------------------------+----------+-----------+---------------+--------------------------------------------------------------------------------------------------+
| Projection_9                     | 8000.00  | root      |               | Column#6                                                                                         |
| └─Selection_10                   | 8000.00  | root      |               | le(Column#6, 3)                                                                                  |
|   └─Shuffle_15                   | 10000.00 | root      |               | execution info: concurrency:5, data sources:[TableReader_13]                                     |
|     └─Window_11                  | 10000.00 | root      |               | row_number()->Column#6 over(partition by test.t.value1 rows between current row and current row) |
|       └─Sort_14                  | 10000.00 | root      |               | test.t.value1                                                                                    |
|         └─TableReader_13         | 10000.00 | root      |               | data:TableFullScan_12                                                                            |
|           └─TableFullScan_12     | 10000.00 | cop[tikv] | table:t       | keep order:false, stats:pseudo                                                                   |
+----------------------------------+----------+-----------+---------------+--------------------------------------------------------------------------------------------------+
```

在该查询中，因为 partition 的列不是主键的前缀，所以 SQL 没有被改写。

#### 示例 6：PARTITION BY 列是主键的前缀，但主键不是聚簇索引

```sql
CREATE TABLE t(id1 int, id2 int, value1 int, value2 int, primary key(id1,id2) nonclustered);
SET tidb_opt_derive_topn=on;
EXPLAIN SELECT * FROM (SELECT ROW_NUMBER() OVER (PARTITION BY id1) AS rownumber FROM t use index()) dt WHERE rownumber <= 3;
```

```
+----------------------------------+----------+-----------+---------------+-----------------------------------------------------------------------------------------------+
| id                               | estRows  | task      | access object | operator info                                                                                 |
+----------------------------------+----------+-----------+---------------+-----------------------------------------------------------------------------------------------+
| Projection_9                     | 8000.00  | root      |               | Column#7                                                                                      |
| └─Selection_10                   | 8000.00  | root      |               | le(Column#7, 3)                                                                               |
|   └─Shuffle_15                   | 10000.00 | root      |               | execution info: concurrency:5, data sources:[TableReader_13]                                  |
|     └─Window_11                  | 10000.00 | root      |               | row_number()->Column#7 over(partition by test.t.id1 rows between current row and current row) |
|       └─Sort_14                  | 10000.00 | root      |               | test.t.id1                                                                                    |
|         └─TableReader_13         | 10000.00 | root      |               | data:TableFullScan_12                                                                         |
|           └─TableFullScan_12     | 10000.00 | cop[tikv] | table:t       | keep order:false, stats:pseudo                                                                |
+----------------------------------+----------+-----------+---------------+-----------------------------------------------------------------------------------------------+
```

在该查询中，即使 PARTITION 的列是主键的前缀，但是因为主键不是聚簇索引，所以 SQL 没被改写。
