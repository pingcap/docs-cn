---
title: Derive TopN or Limit from Window Functions
summary: Introduce the optimization rule of deriving TopN or Limit from window functions and how to enable this rule.
---

# Derive TopN or Limit from Window Functions

[Window Functions](/functions-and-operators/window-functions.md) are a common type of SQL function. When you use a window function for row numbering, such as `ROW_NUMBER()` or `RANK()`, it is common to filter the results after the window function is evaluated. For example:

```sql
SELECT * FROM (SELECT ROW_NUMBER() OVER (ORDER BY a) AS rownumber FROM t) dt WHERE rownumber <= 3
```

In a typical SQL execution process, TiDB first sorts all data in the table `t`, then calculates the `ROW_NUMBER()` result for each row, and finally filters with `rownumber <= 3`.

Starting from v7.0.0, TiDB supports deriving the TopN or Limit operator from window functions. With this optimization rule, TiDB can rewrite the original SQL into an equivalent form as follows:

```sql
WITH t_topN AS (SELECT a FROM t1 ORDER BY a LIMIT 3) SELECT * FROM (SELECT ROW_NUMBER() OVER (ORDER BY a) AS rownumber FROM t_topN) dt WHERE rownumber <= 3
```

After rewriting, TiDB can derive a TopN operator from the window function and the subsequent filter condition. Compared with the Sort operator in the original SQL (`ORDER BY`), the TopN operator has a much higher execution efficiency. In addition, both TiKV and TiFlash support pushing down the TopN operator, which further improves the performance of the rewritten SQL.

Deriving TopN or Limit from window functions is disabled by default. To enable this feature, you can set the session variable [tidb_opt_derive_topn](/system-variables.md#tidb_opt_derive_topn-new-in-v700) to `ON`.

After enabling this feature, you can disable it by performing one of the following operations:

* Set the session variable [tidb_opt_derive_topn](/system-variables.md#tidb_opt_derive_topn-new-in-v700) to `OFF`.
* Follow the steps described in [The blocklist of optimization rules and expression pushdown](/blocklist-control-plan.md).

## Limitations

* Only the `ROW_NUMBER()` window function is supported for SQL rewriting.
* TiDB can only rewrite SQL when filtering on the `ROW_NUMBER()` results and the filter condition is `<` or `<=`.

## Usage examples

The following examples demonstrate how to use the optimization rule.

### Window functions without PARTITION BY

#### Example 1: window functions without ORDER BY

```sql
CREATE TABLE t(id int, value int);
SET tidb_opt_derive_topn=on;
EXPLAIN SELECT * FROM (SELECT ROW_NUMBER() OVER () AS rownumber FROM t) dt WHERE rownumber <= 3;
```

The result is as follows:

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

In this query, the optimizer derives the Limit operator from the window function and pushes it down to TiKV.

#### Example 2: window functions with ORDER BY

```sql
CREATE TABLE t(id int, value int);
SET tidb_opt_derive_topn=on;
EXPLAIN SELECT * FROM (SELECT ROW_NUMBER() OVER (ORDER BY value) AS rownumber FROM t) dt WHERE rownumber <= 3;
```

The result is as follows:

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

In this query, the optimizer derives the TopN operator from the window function and pushes it down to TiKV.

### Window functions with PARTITION BY

> **Note:**
>
> For a window function containing `PARTITION BY`, the optimization rule only takes effect when the partition column is a prefix of the primary key and the primary key is a clustered index.

#### Example 3: window functions without ORDER BY

```sql
CREATE TABLE t(id1 int, id2 int, value1 int, value2 int, primary key(id1,id2) clustered);
SET tidb_opt_derive_topn=on;
EXPLAIN SELECT * FROM (SELECT ROW_NUMBER() OVER (PARTITION BY id1) AS rownumber FROM t) dt WHERE rownumber <= 3;
```

The result is as follows:

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

In this query, the optimizer derives the Limit operator from the window function and pushes it down to TiKV. Note that this Limit is actually a partition Limit, which means that the Limit will be applied to each group of data with the same `id1` value.

#### Example 4: window functions with ORDER BY

```sql
CREATE TABLE t(id1 int, id2 int, value1 int, value2 int, primary key(id1,id2) clustered);
SET tidb_opt_derive_topn=on;
EXPLAIN SELECT * FROM (SELECT ROW_NUMBER() OVER (PARTITION BY id1 ORDER BY value1) AS rownumber FROM t) dt WHERE rownumber <= 3;
```

The result is as follows:

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

In this query, the optimizer derives the TopN operator from the window function and pushes it down to TiKV. Note that this TopN is actually a partition TopN, which means that the TopN will be applied to each group of data with the same `id1` value.

#### Example 5: PARTITION BY column is not a prefix of the primary key

```sql
CREATE TABLE t(id1 int, id2 int, value1 int, value2 int, primary key(id1,id2) clustered);
SET tidb_opt_derive_topn=on;
EXPLAIN SELECT * FROM (SELECT ROW_NUMBER() OVER (PARTITION BY value1) AS rownumber FROM t) dt WHERE rownumber <= 3;
```

The result is as follows:

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

In this query, the SQL is not rewritten because the `PARTITION BY` column is not a prefix of the primary key.

#### Example 6: PARTITION BY column is a prefix of the primary key but not a clustered index

```sql
CREATE TABLE t(id1 int, id2 int, value1 int, value2 int, primary key(id1,id2) nonclustered);
SET tidb_opt_derive_topn=on;
EXPLAIN SELECT * FROM (SELECT ROW_NUMBER() OVER (PARTITION BY id1) AS rownumber FROM t use index()) dt WHERE rownumber <= 3;
```

The result is as follows:

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

In this query, although the `PARTITION BY` column is a prefix of the primary key, the SQL is not rewritten because the primary key is not a clustered index.
