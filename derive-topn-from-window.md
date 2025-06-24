---
title: 从窗口函数推导 TopN 或 Limit
summary: 介绍从窗口函数推导 TopN 或 Limit 的优化规则以及如何启用此规则。
---

# 从窗口函数推导 TopN 或 Limit

[窗口函数](/functions-and-operators/window-functions.md)是一种常见的 SQL 函数。当您使用窗口函数进行行编号时，例如 `ROW_NUMBER()` 或 `RANK()`，通常会在窗口函数计算后对结果进行过滤。例如：

```sql
SELECT * FROM (SELECT ROW_NUMBER() OVER (ORDER BY a) AS rownumber FROM t) dt WHERE rownumber <= 3
```

在典型的 SQL 执行过程中，TiDB 首先对表 `t` 中的所有数据进行排序，然后为每一行计算 `ROW_NUMBER()` 结果，最后使用 `rownumber <= 3` 进行过滤。

从 v7.0.0 开始，TiDB 支持从窗口函数推导 TopN 或 Limit 运算符。通过此优化规则，TiDB 可以将原始 SQL 重写为以下等价形式：

```sql
WITH t_topN AS (SELECT a FROM t1 ORDER BY a LIMIT 3) SELECT * FROM (SELECT ROW_NUMBER() OVER (ORDER BY a) AS rownumber FROM t_topN) dt WHERE rownumber <= 3
```

重写后，TiDB 可以从窗口函数和后续的过滤条件推导出 TopN 运算符。与原始 SQL 中的 Sort 运算符（`ORDER BY`）相比，TopN 运算符具有更高的执行效率。此外，TiKV 和 TiFlash 都支持下推 TopN 运算符，这进一步提高了重写后 SQL 的性能。

从窗口函数推导 TopN 或 Limit 默认是禁用的。要启用此功能，您可以将会话变量 [tidb_opt_derive_topn](/system-variables.md#tidb_opt_derive_topn-new-in-v700) 设置为 `ON`。

启用此功能后，您可以通过执行以下操作之一来禁用它：

* 将会话变量 [tidb_opt_derive_topn](/system-variables.md#tidb_opt_derive_topn-new-in-v700) 设置为 `OFF`。
* 按照[优化规则和表达式下推的黑名单](/blocklist-control-plan.md)中描述的步骤操作。

## 限制

* 仅支持对 `ROW_NUMBER()` 窗口函数进行 SQL 重写。
* TiDB 只能在对 `ROW_NUMBER()` 结果进行过滤且过滤条件为 `<` 或 `<=` 时重写 SQL。

## 使用示例

以下示例演示如何使用此优化规则。

### 不带 PARTITION BY 的窗口函数

#### 示例 1：不带 ORDER BY 的窗口函数

```sql
CREATE TABLE t(id int, value int);
SET tidb_opt_derive_topn=on;
EXPLAIN SELECT * FROM (SELECT ROW_NUMBER() OVER () AS rownumber FROM t) dt WHERE rownumber <= 3;
```

结果如下：

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

在此查询中，优化器从窗口函数推导出 Limit 运算符并将其下推到 TiKV。

#### 示例 2：带 ORDER BY 的窗口函数

```sql
CREATE TABLE t(id int, value int);
SET tidb_opt_derive_topn=on;
EXPLAIN SELECT * FROM (SELECT ROW_NUMBER() OVER (ORDER BY value) AS rownumber FROM t) dt WHERE rownumber <= 3;
```

结果如下：

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

在此查询中，优化器从窗口函数推导出 TopN 运算符并将其下推到 TiKV。

### 带 PARTITION BY 的窗口函数

> **注意：**
>
> 对于包含 `PARTITION BY` 的窗口函数，只有当分区列是主键的前缀且主键是聚簇索引时，优化规则才会生效。

#### 示例 3：不带 ORDER BY 的窗口函数

```sql
CREATE TABLE t(id1 int, id2 int, value1 int, value2 int, primary key(id1,id2) clustered);
SET tidb_opt_derive_topn=on;
EXPLAIN SELECT * FROM (SELECT ROW_NUMBER() OVER (PARTITION BY id1) AS rownumber FROM t) dt WHERE rownumber <= 3;
```

结果如下：

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

在此查询中，优化器从窗口函数推导出 Limit 运算符并将其下推到 TiKV。注意，这个 Limit 实际上是一个分区 Limit，这意味着 Limit 将应用于具有相同 `id1` 值的每组数据。

#### 示例 4：带 ORDER BY 的窗口函数

```sql
CREATE TABLE t(id1 int, id2 int, value1 int, value2 int, primary key(id1,id2) clustered);
SET tidb_opt_derive_topn=on;
EXPLAIN SELECT * FROM (SELECT ROW_NUMBER() OVER (PARTITION BY id1 ORDER BY value1) AS rownumber FROM t) dt WHERE rownumber <= 3;
```

结果如下：

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

在此查询中，优化器从窗口函数推导出 TopN 运算符并将其下推到 TiKV。注意，这个 TopN 实际上是一个分区 TopN，这意味着 TopN 将应用于具有相同 `id1` 值的每组数据。

#### 示例 5：PARTITION BY 列不是主键的前缀

```sql
CREATE TABLE t(id1 int, id2 int, value1 int, value2 int, primary key(id1,id2) clustered);
SET tidb_opt_derive_topn=on;
EXPLAIN SELECT * FROM (SELECT ROW_NUMBER() OVER (PARTITION BY value1) AS rownumber FROM t) dt WHERE rownumber <= 3;
```

结果如下：

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

在此查询中，由于 `PARTITION BY` 列不是主键的前缀，SQL 没有被重写。

#### 示例 6：PARTITION BY 列是主键的前缀但不是聚簇索引

```sql
CREATE TABLE t(id1 int, id2 int, value1 int, value2 int, primary key(id1,id2) nonclustered);
SET tidb_opt_derive_topn=on;
EXPLAIN SELECT * FROM (SELECT ROW_NUMBER() OVER (PARTITION BY id1) AS rownumber FROM t use index()) dt WHERE rownumber <= 3;
```

结果如下：

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

在此查询中，虽然 `PARTITION BY` 列是主键的前缀，但由于主键不是聚簇索引，SQL 没有被重写。
