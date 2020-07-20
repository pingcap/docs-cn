---
title: Understand the Query Execution Plan
summary: Learn about the execution plan information returned by the `EXPLAIN` statement in TiDB.
aliases: ['/docs/dev/query-execution-plan/','/docs/dev/reference/performance/understanding-the-query-execution-plan/']
---

# Understand the Query Execution Plan

Based on the details of your tables, the TiDB optimizer chooses the most efficient query execution plan, which consists of a series of operators. This document details the execution plan information returned by the `EXPLAIN` statement in TiDB.

## `EXPLAIN` overview

The result of the `EXPLAIN` statement provides information about how TiDB executes SQL queries:

- `EXPLAIN` works together with statements such as `SELECT` and `DELETE`.
- When you execute the `EXPLAIN` statement, TiDB returns the final optimized physical execution plan. In other words, `EXPLAIN` displays the complete information about how TiDB executes the SQL statement, such as in which order, how tables are joined, and what the expression tree looks like.
- For more information about each column of `EXPLAIN`, see [`EXPLAIN` Output Format](/sql-statements/sql-statement-explain.md).

The results of `EXPLAIN` shed light on how to index the data tables so that the execution plan can use the index to speed up the execution of SQL statements. You can also use `EXPLAIN` to check if the optimizer chooses the optimal order to join tables.

## Operator execution order

The execution plan in TiDB has a tree structure, with each node of the tree as an operator. Considering the concurrent execution of multiple threads in each operator, all operators consume CPU and memory resources to process data during the execution of a SQL statement. From this point of view, there is no execution order for the operator.

However, from the perspective of which operators process a row of data first, the execution of a piece of data is in order. The following rule roughly summarizes this order:

**`Build` is always executed before `Probe` and always appears before `Probe`.**

The first half of this rule means: if an operator has multiple child nodes, the operator with the `Build` keyword at the end of the child node ID is always executed before the operator with the `Probe` keyword. The second half means: when TiDB shows the execution plan, the `Build` side always appears first, followed by the `Probe` side.

The following examples illustrate this rule:

{{< copyable "sql" >}}

```sql
explain select * from t use index(idx_a) where a = 1;
```

```sql
+-------------------------------+---------+-----------+-------------------------+---------------------------------------------+
| id                            | estRows | task      | access object           | operator info                               |
+-------------------------------+---------+-----------+-------------------------+---------------------------------------------+
| IndexLookUp_7                 | 10.00   | root      |                         |                                             |
| ├─IndexRangeScan_5(Build)     | 10.00   | cop[tikv] | table:t, index:idx_a(a) | range:[1,1], keep order:false, stats:pseudo |
| └─TableRowIDScan_6(Probe)     | 10.00   | cop[tikv] | table:t                 | keep order:false, stats:pseudo              |
+-------------------------------+---------+-----------+-------------------------+---------------------------------------------+
3 rows in set (0.00 sec)
```

The `IndexLookUp_7` operator has two child nodes: `IndexRangeScan_5 (Build)` and `TableRowIDScan_6 (Probe)`. `IndexRangeScan_5 (Build)` appears first.

To get a piece of data, first, you need to execute `IndexRangeScan_5 (Build)` to get a RowID. Then, use `TableRowIDScan_6 (Probe)` to get a complete row of data based on the RowID.

The implication of the above rule is: for nodes at the same level, the operator that appears first might be executed first, and the operator that appears last might be executed last. This can be illustrated in the following example:

{{< copyable "sql" >}}

```sql
explain select * from t t1 use index(idx_a) join t t2 use index() where t1.a = t2.a;
```

```sql
+----------------------------------+----------+-----------+--------------------------+------------------------------------------------------------------+
| id                               | estRows  | task      | access object            | operator info                                                    |
+----------------------------------+----------+-----------+--------------------------+------------------------------------------------------------------+
| HashJoin_22                      | 12487.50 | root      |                          | inner join, inner:TableReader_26, equal:[eq(test.t.a, test.t.a)] |
| ├─TableReader_26(Build)          | 9990.00  | root      |                          | data:Selection_25                                                |
| │ └─Selection_25                 | 9990.00  | cop[tikv] |                          | not(isnull(test.t.a))                                            |
| │   └─TableFullScan_24           | 10000.00 | cop[tikv] | table:t2                 | keep order:false, stats:pseudo                                   |
| └─IndexLookUp_29(Probe)          | 9990.00  | root      |                          |                                                                  |
|   ├─IndexFullScan_27(Build)      | 9990.00  | cop[tikv] | table:t1, index:idx_a(a) | keep order:false, stats:pseudo                                   |
|   └─TableRowIDScan_28(Probe)     | 9990.00  | cop[tikv] | table:t1                 | keep order:false, stats:pseudo                                   |
+----------------------------------+----------+-----------+--------------------------+------------------------------------------------------------------+
7 rows in set (0.00 sec)
```

To complete the `HashJoin_22` operation, you need to execute `TableReader_26(Build)`, and then execute `IndexLookUp_29(Probe)`.

When executing `IndexLookUp_29(Probe)`, you need to execute `IndexFullScan_27(Build)` and `TableRowIDScan_28(Probe)` one by one. Therefore, from the perspective of the whole execution link, `TableRowIDScan_28(Probe)` is the last one awoken to be executed.

### Task overview

Currently, calculation tasks of TiDB can be divided into two categories: cop tasks and root tasks. The cop tasks are performed by the Coprocessor in TiKV, and the root tasks are performed in TiDB.

One of the goals of SQL optimization is to push the calculation down to TiKV as much as possible. The Coprocessor in TiKV supports most of the built-in SQL functions (including the aggregate functions and the scalar functions), SQL `LIMIT` operations, index scans, and table scans. However, all `Join` operations can only be performed as root tasks in TiDB.

### Range query

In the `WHERE`/`HAVING`/`ON` conditions, the TiDB optimizer analyzes the result returned by the primary key query or the index key query. For example, these conditions might include comparison operators of the numeric and date type, such as `>`, `<`, `=`, `>=`, `<=`, and the character type such as `LIKE`.

> **Note:**
>
> - Currently, TiDB only supports the case where a comparison operator is connected by a column (at one end) and a constant value (at the other end), or the case that the calculation result is a constant. You cannot use query conditions like `year(birth_day) < 1992` as the index.
> - It is recommended to compare data of the same type; otherwise, additional `cast` operations are introduced, which causes the index to be unavailable. For example, regarding the condition `user_id = 123456`, if `user_id` is a string, you must define `123456` as a string constant.

You can also use `AND` (intersection) and `OR` (union) to combine the range query conditions of one column. For a multi-dimensional composite index, you can use conditions in multiple columns. For example, regarding the composite index `(a, b, c)`:

- When `a` is an equivalent query, continue to figure out the query range of `b`; when `b` is also an equivalent query, continue to figure out the query range of `c`.
- Otherwise, if `a` is a non-equivalent query, you can only figure out the range of `a`.

## Operator overview

Different operators output different information after the `EXPLAIN` statement is executed. This section focuses on the execution plan of different operators, ranging from table scans, table aggregation, to table join.

You can use optimizer hints to control the behavior of the optimizer, and thereby controlling the selection of the physical operators. For example, `/*+ HASH_JOIN(t1, t2) */` means that the optimizer uses the `Hash Join` algorithm. For more details, see [Optimizer Hints](/optimizer-hints.md).

### Read the execution plan of table scans

The operators that perform table scans (of the disk or the TiKV Block Cache) are listed as follows:

- **TableFullScan**: Full table scan.
- **TableRangeScan**: Table scans with the specified range.
- **TableRowIDScan**: Accurately scans the table data based on the RowID passed down from the upper layer.
- **IndexFullScan**: Another type of "full table scan", except that the index data is scanned, rather than the table data.
- **IndexRangeScan**: Index scans with the specified range.

TiDB aggregates the data or calculation results scanned from TiKV/TiFlash. The data aggregation operators can be divided into the following categories:

- **TableReader**: Aggregates the data obtained by the underlying operators like `TableFullScan` or `TableRangeScan` in TiKV.
- **IndexReader**: Aggregates the data obtained by the underlying operators like `IndexFullScan` or `IndexRangeScan` in TiKV.
- **IndexLookUp**: First aggregates the RowID (in TiKV) scanned by the `Build` side. Then at the `Probe` side, accurately reads the data from TiKV based on these RowIDs. At the `Build` side, there are operators like `IndexFullScan` or `IndexRangeScan`; at the `Probe` side, there is the `TableRowIDScan` operator.
- **IndexMerge**: Similar to `IndexLookUp`. `IndexMerge` can be seen as an extension of `IndexLookupReader`. `IndexMerge` supports reading multiple indexes at the same time. There are many `Build`s and one `Probe`. The execution process of `IndexMerge` the same as that of `IndexLookUp`.

#### Table data and index data

Table data refers to the original data of a table stored in TiKV. For each row of the table data, its `key` is a 64-bit integer called `RowID`. If a primary key of a table is an integer, TiDB uses the value of the primary key as the `RowID` of the table data; otherwise, the system automatically generates `RowID`. The `value` of the table data is encoded from all the data in this row. When reading table data, data is returned in the order of increasing `RowID`s.

Similar to the table data, the index data is also stored in TiKV. Its `key` is the ordered bytes encoded from the index column. `value` is the `RowID` corresponding to a row of index data. The non-index column of the row can be read using `RowID`. When reading index data, TiKV returns data in ascending order of index columns. If there are multiple index columns, firstly, ensure that the first column is incremented; if the i-th column is equivalent, make sure that the (i+1)-th column is incremented.

#### `IndexLookUp` example

{{< copyable "sql" >}}

```sql
explain select * from t use index(idx_a);
```

```sql
+-------------------------------+----------+-----------+-------------------------+--------------------------------+
| id                            | estRows  | task      | access object           | operator info                  |
+-------------------------------+----------+-----------+-------------------------+--------------------------------+
| IndexLookUp_6                 | 10000.00 | root      |                         |                                |
| ├─IndexFullScan_4(Build)      | 10000.00 | cop[tikv] | table:t, index:idx_a(a) | keep order:false, stats:pseudo |
| └─TableRowIDScan_5(Probe)     | 10000.00 | cop[tikv] | table:t                 | keep order:false, stats:pseudo |
+-------------------------------+----------+-----------+-------------------------+--------------------------------+
3 rows in set (0.00 sec)
```

The `IndexLookUp_6` operator has two child nodes: `IndexFullScan_4(Build)` and `TableRowIDScan_5(Probe)`.

+ `IndexFullScan_4(Build)` performs an index full scan and scans all the data of index `a`. Because it is a full scan, this operation gets the `RowID` of all the data in the table.
+ `TableRowIDScan_5(Probe)` scans all table data using `RowID`s.

This execution plan is not as efficient as using `TableReader` to perform a full table scan, because `IndexLookUp` performs an extra index scan (which comes with additional overhead), apart from the table scan.

#### `TableReader` example

{{< copyable "sql" >}}

```sql
explain select * from t where a > 1 or b >100;
```

```sql
+-------------------------+----------+-----------+---------------+----------------------------------------+
| id                      | estRows  | task      | access object | operator info                          |
+-------------------------+----------+-----------+---------------+----------------------------------------+
| TableReader_7           | 8000.00  | root      |               | data:Selection_6                       |
| └─Selection_6           | 8000.00  | cop[tikv] |               | or(gt(test.t.a, 1), gt(test.t.b, 100)) |
|   └─TableFullScan_5     | 10000.00 | cop[tikv] | table:t       | keep order:false, stats:pseudo         |
+-------------------------+----------+-----------+---------------+----------------------------------------+
3 rows in set (0.00 sec)
```

In the above example, the child node of the `TableReader_7` operator is `Selection_6`. The subtree rooted at this child node is seen as a `Cop Task` and is delivered to the corresponding TiKV. This `Cop Task` uses the `TableFullScan_5` operator to perform the table scan. `Selection` represents the selection condition in the SQL statement, namely, the `WHERE`/`HAVING`/`ON` clause.

`TableFullScan_5` performs a full table scan, and the load on the cluster increases accordingly, which might affect other queries running in the cluster. If an appropriate index is built and the `IndexMerge` operator is used, these will greatly improve query performance and reduce load on the cluster.

#### `IndexMerge` example

{{< copyable "sql" >}}

```sql
set @@tidb_enable_index_merge = 1;
explain select * from t use index(idx_a, idx_b) where a > 1 or b > 1;
```

```sql
+------------------------------+---------+-----------+-------------------------+------------------------------------------------+
| id                           | estRows | task      | access object           | operator info                                  |
+------------------------------+---------+-----------+-------------------------+------------------------------------------------+
| IndexMerge_16                | 6666.67 | root      |                         |                                                |
| ├─IndexRangeScan_13(Build)   | 3333.33 | cop[tikv] | table:t, index:idx_a(a) | range:(1,+inf], keep order:false, stats:pseudo |
| ├─IndexRangeScan_14(Build)   | 3333.33 | cop[tikv] | table:t, index:idx_b(b) | range:(1,+inf], keep order:false, stats:pseudo |
| └─TableRowIDScan_15(Probe)   | 6666.67 | cop[tikv] | table:t                 | keep order:false, stats:pseudo                 |
+------------------------------+---------+-----------+-------------------------+------------------------------------------------+
4 rows in set (0.00 sec)
```

`IndexMerge` makes it possible that multiple indexes are used during table scans. In the above example, the `IndexMerge_16` operator has three child nodes, among which `IndexRangeScan_13` and `IndexRangeScan_14` get all the `RowID`s that meet the conditions based on the result of range scan, and then the `TableRowIDScan_15` operator accurately reads all the data that meet the conditions according to these `RowID`s.

> **Note:**
>
> At present, the `IndexMerge` feature is disabled by default in TiDB 4.0.0-rc.1. In addition, the currently supported scenarios of `IndexMerge` in TiDB 4.0 are limited to the disjunctive normal form (expressions connected by `or`). The conjunctive normal form (expressions connected by `and`) will be supported in later versions.
>
> You can enable `IndexMerge` by configuring the `session` or `global` variables: execute the `set @@tidb_enable_index_merge = 1;` statement in the client.

### Read the aggregated execution plan

Aggregation algorithms in TiDB include the following categories:

- [Hash Aggregate](#hash-aggregate-example)
- [Stream Aggregate](#stream-aggregate-example)

#### `Hash Aggregate` example

The `Hash Aggregation` operator is optimized in multi-threaded concurrency. It is quick to execute at the cost of more memory usage. The following is an example of `Hash Aggregate`:

{{< copyable "sql" >}}

```sql
explain select /*+ HASH_AGG() */ count(*) from t;
```

```sql
+---------------------------+----------+-----------+---------------+---------------------------------+
| id                        | estRows  | task      | access object | operator info                   |
+---------------------------+----------+-----------+---------------+---------------------------------+
| HashAgg_11                | 1.00     | root      |               | funcs:count(Column#7)->Column#4 |
| └─TableReader_12          | 1.00     | root      |               | data:HashAgg_5                  |
|   └─HashAgg_5             | 1.00     | cop[tikv] |               | funcs:count(1)->Column#7        |
|     └─TableFullScan_8     | 10000.00 | cop[tikv] | table:t       | keep order:false, stats:pseudo  |
+---------------------------+----------+-----------+---------------+---------------------------------+
4 rows in set (0.00 sec)
```

Generally speaking, `Hash Aggregate` is executed in two stages.

- One is on the Coprocessor of TiKV/TiFlash, with the intermediate results of the aggregation function calculated when the table scan operator reads the data.
- The other is at the TiDB layer, with the final result calculated through aggregating the intermediate results of all Coprocessor Tasks.

#### `Stream Aggregate` example

The `Stream Aggregation` operator usually takes up less memory than `Hash Aggregate`. In some scenarios, `Stream Aggregation` executes faster than `Hash Aggregate`. In the case of a large amount of data or insufficient system memory, it is recommended to use the `Stream Aggregate` operator. An example is as follows:

{{< copyable "sql" >}}

```sql
explain select /*+ STREAM_AGG() */ count(*) from t;
```

```sql
+----------------------------+----------+-----------+---------------+---------------------------------+
| id                         | estRows  | task      | access object | operator info                   |
+----------------------------+----------+-----------+---------------+---------------------------------+
| StreamAgg_16               | 1.00     | root      |               | funcs:count(Column#7)->Column#4 |
| └─TableReader_17           | 1.00     | root      |               | data:StreamAgg_8                |
|   └─StreamAgg_8            | 1.00     | cop[tikv] |               | funcs:count(1)->Column#7        |
|     └─TableFullScan_13     | 10000.00 | cop[tikv] | table:t       | keep order:false, stats:pseudo  |
+----------------------------+----------+-----------+---------------+---------------------------------+
4 rows in set (0.00 sec)
```

Similar to `Hash Aggregate`, `Stream Aggregate` is executed in two stages.

- One is on the Coprocessor of TiKV/TiFlash, with the intermediate results of the aggregation function calculated when the table scan operator reads the data.
- The other is at the TiDB layer, with the final result calculated through aggregating the intermediate results of all Coprocessor Tasks.

### Read the `Join` execution plan

The `Join` algorithms in TiDB consist of the following categories:

- [Hash Join](#hash-join-example)
- [Merge Join](#merge-join-example)
- [Index Join (Index Nested Loop Join)](#index-join-example)
- [Index Hash Join (Index Nested Loop Hash Join)](#index-hash-join-example)
- [Index Merge Join (Index Nested Loop Merge Join)](#index-merge-join-example)

The following are examples of the execution processes of these `Join` algorithms.

#### `Hash Join` example

The `Hash Join` operator uses multi-thread. Its execution speed is fast at the cost of more memory usage. An example of `Hash Join` is as follows:

{{< copyable "sql" >}}

```sql
EXPLAIN SELECT /*+ HASH_JOIN(t1, t2) */ * FROM t1, t2 WHERE t1.id = t2.id;
```

```sql
+-----------------------------+----------+-----------+------------------------+------------------------------------------------+
| id                          | estRows  | task      | access object          | operator info                                  |
+-----------------------------+----------+-----------+------------------------+------------------------------------------------+
| HashJoin_30                 | 12487.50 | root      |                        | inner join, equal:[eq(test.t1.id, test.t2.id)] |
| ├─IndexReader_35(Build)     | 9990.00  | root      |                        | index:IndexFullScan_34                         |
| │ └─IndexFullScan_34        | 9990.00  | cop[tikv] | table:t2, index:id(id) | keep order:false, stats:pseudo                 |
| └─IndexReader_33(Probe)     | 9990.00  | root      |                        | index:IndexFullScan_32                         |
|   └─IndexFullScan_32        | 9990.00  | cop[tikv] | table:t1, index:id(id) | keep order:false, stats:pseudo                 |
+-----------------------------+----------+-----------+------------------------+------------------------------------------------+
5 rows in set (0.01 sec)
```

The execution process of `Hash Join` is as follows:

1. Cache the data of the `Build` side in memory.
2. Construct a Hash Table on the `Build` side based on the cached data.
3. Read the data at the `Probe` side.
4. Use the data of the `Probe` side to probe the Hash Table.
5. Return qualified data to the user.

#### `Merge Join` example

The `Merge Join` operator usually uses less memory than `Hash Join`. However, `Merge Join` might take longer to be executed. When the amount of data is large, or the system memory is insufficient, it is recommended to use `Merge Join`. The following is an example:

{{< copyable "sql" >}}

```sql
EXPLAIN SELECT /*+ MERGE_JOIN(t1, t2) */ * FROM t1, t2 WHERE t1.id = t2.id;
```

```sql
+-----------------------------+----------+-----------+------------------------+-------------------------------------------------------+
| id                          | estRows  | task      | access object          | operator info                                         |
+-----------------------------+----------+-----------+------------------------+-------------------------------------------------------+
| MergeJoin_7                 | 12487.50 | root      |                        | inner join, left key:test.t1.id, right key:test.t2.id |
| ├─IndexReader_12(Build)     | 9990.00  | root      |                        | index:IndexFullScan_11                                |
| │ └─IndexFullScan_11        | 9990.00  | cop[tikv] | table:t2, index:id(id) | keep order:true, stats:pseudo                         |
| └─IndexReader_10(Probe)     | 9990.00  | root      |                        | index:IndexFullScan_9                                 |
|   └─IndexFullScan_9         | 9990.00  | cop[tikv] | table:t1, index:id(id) | keep order:true, stats:pseudo                         |
+-----------------------------+----------+-----------+------------------------+-------------------------------------------------------+
5 rows in set (0.01 sec)
```

The execution of the `Merge Join` operator is as follows:

1. Read all the data of a Join Group from the `Build` side into the memory
2. Read the data of the `Probe` side.
3. Compare whether each row of data on the `Probe` side matches a complete Join Group on the `Build` side. Apart from equivalent conditions, there are non-equivalent conditions. Here "match" mainly refers to checking whether non-equivalent conditions are met. Join Group refers to the data with the same value among all Join Keys.

#### `Index Join` example

If the result set (obtained after the outer tables are filtered by the `WHERE` condition) is small, it is recommended to use `Index Join`. Here "small" means data is less than 10,000 rows.

{{< copyable "sql" >}}

```sql
EXPLAIN SELECT /*+ INL_JOIN(t1, t2) */ * FROM t1, t2 WHERE t1.id = t2.id;
```

```sql
+-----------------------------+----------+-----------+------------------------+--------------------------------------------------------------------------------+
| id                          | estRows  | task      | access object          | operator info                                                                  |
+-----------------------------+----------+-----------+------------------------+--------------------------------------------------------------------------------+
| IndexJoin_11                | 12487.50 | root      |                        | inner join, inner:IndexReader_10, outer key:test.t1.id, inner key:test.t2.id   |
| ├─IndexReader_31(Build)     | 9990.00  | root      |                        | index:IndexFullScan_30                                                         |
| │ └─IndexFullScan_30        | 9990.00  | cop[tikv] | table:t1, index:id(id) | keep order:false, stats:pseudo                                                 |
| └─IndexReader_10(Probe)     | 1.00     | root      |                        | index:Selection_9                                                              |
|   └─Selection_9             | 1.00     | cop[tikv] |                        | not(isnull(test.t2.id))                                                        |
|     └─IndexRangeScan_8      | 1.00     | cop[tikv] | table:t2, index:id(id) | range: decided by [eq(test.t2.id, test.t1.id)], keep order:false, stats:pseudo |
+-----------------------------+----------+-----------+------------------------+--------------------------------------------------------------------------------+
6 rows in set (0.00 sec)
```

#### `Index Hash Join` example

`Index Hash Join` uses the same conditions as `Index Join`. However, `Index Hash Join` saves more memory in some scenarios.

{{< copyable "sql" >}}

```sql
EXPLAIN SELECT /*+ INL_HASH_JOIN(t1, t2) */ * FROM t1, t2 WHERE t1.id = t2.id;
```

```sql
+-----------------------------+----------+-----------+------------------------+--------------------------------------------------------------------------------+
| id                          | estRows  | task      | access object          | operator info                                                                  |
+-----------------------------+----------+-----------+------------------------+--------------------------------------------------------------------------------+
| IndexHashJoin_18            | 12487.50 | root      |                        | inner join, inner:IndexReader_10, outer key:test.t1.id, inner key:test.t2.id   |
| ├─IndexReader_31(Build)     | 9990.00  | root      |                        | index:IndexFullScan_30                                                         |
| │ └─IndexFullScan_30        | 9990.00  | cop[tikv] | table:t1, index:id(id) | keep order:false, stats:pseudo                                                 |
| └─IndexReader_10(Probe)     | 1.00     | root      |                        | index:Selection_9                                                              |
|   └─Selection_9             | 1.00     | cop[tikv] |                        | not(isnull(test.t2.id))                                                        |
|     └─IndexRangeScan_8      | 1.00     | cop[tikv] | table:t2, index:id(id) | range: decided by [eq(test.t2.id, test.t1.id)], keep order:false, stats:pseudo |
+-----------------------------+----------+-----------+------------------------+--------------------------------------------------------------------------------+
6 rows in set (0.00 sec)
```

#### `Index Merge Join` example

`Index Merge Join` is used in similar scenarios as Index Join. However, the index prefix used by the inner table is the inner table column collection in the join keys. `Index Merge Join` saves more memory than `INL_JOIN`.

{{< copyable "sql" >}}

```sql
EXPLAIN SELECT /*+ INL_MERGE_JOIN(t1, t2) */ * FROM t1, t2 WHERE t1.id = t2.id;
```

```sql
+-----------------------------+----------+-----------+------------------------+-------------------------------------------------------------------------------+
| id                          | estRows  | task      | access object          | operator info                                                                 |
+-----------------------------+----------+-----------+------------------------+-------------------------------------------------------------------------------+
| IndexMergeJoin_16           | 12487.50 | root      |                        | inner join, inner:IndexReader_14, outer key:test.t1.id, inner key:test.t2.id  |
| ├─IndexReader_31(Build)     | 9990.00  | root      |                        | index:IndexFullScan_30                                                        |
| │ └─IndexFullScan_30        | 9990.00  | cop[tikv] | table:t1, index:id(id) | keep order:false, stats:pseudo                                                |
| └─IndexReader_14(Probe)     | 1.00     | root      |                        | index:Selection_13                                                            |
|   └─Selection_13            | 1.00     | cop[tikv] |                        | not(isnull(test.t2.id))                                                       |
|     └─IndexRangeScan_12     | 1.00     | cop[tikv] | table:t2, index:id(id) | range: decided by [eq(test.t2.id, test.t1.id)], keep order:true, stats:pseudo |
+-----------------------------+----------+-----------+------------------------+-------------------------------------------------------------------------------+
6 rows in set (0.00 sec)
```

## Optimization example

For more details, refer to [bikeshare example database](/import-example-data.md).

{{< copyable "sql" >}}

```sql
EXPLAIN SELECT count(*) FROM trips WHERE start_date BETWEEN '2017-07-01 00:00:00' AND '2017-07-01 23:59:59';
```

```sql
+------------------------------+----------+-----------+---------------+------------------------------------------------------------------------------------------------------------------------+
| id                           | estRows  | task      | access object | operator info                                                                                                          |
+------------------------------+----------+-----------+---------------+------------------------------------------------------------------------------------------------------------------------+
| StreamAgg_20                 | 1.00        | root      |               | funcs:count(Column#13)->Column#11                                                                                      |
| └─TableReader_21             | 1.00        | root      |               | data:StreamAgg_9                                                                                                       |
|   └─StreamAgg_9              | 1.00        | cop[tikv] |               | funcs:count(1)->Column#13                                                                                              |
|     └─Selection_19           | 8166.73     | cop[tikv] |               | ge(bikeshare.trips.start_date, 2017-07-01 00:00:00.000000), le(bikeshare.trips.start_date, 2017-07-01 23:59:59.000000) |
|       └─TableFullScan_18     | 19117643.00 | cop[tikv] | table:trips   | keep order:false, stats:pseudo                                                                                         |
+------------------------------+----------+-----------+---------------+------------------------------------------------------------------------------------------------------------------------+
```

The execution process of the above example can be illustrated as follows:

1. Coprocessor reads the data on the trips table (executed by `TableScan_18`).
2. Find data that meets the `start_date BETWEEN '2017-07-01 00:00:00' AND '2017-07-01 23:59:59'` condition (executed by `Selection_19`).
3. Calculate the number of rows that satisfy the condition, and return the result to TiDB (executed by `StreamAgg_9`).
4. TiDB aggregates the results returned by each Coprocessor (executed by `TableReader_21`).
5. TiDB calculates the number of rows of all data (`StreamAgg_20`), and finally returns the results to the client.

In the above query, TiDB estimates the number of rows in the output of `TableScan_18` as 19117643.00, based on the statistics of the `trips` table. The number of rows that meet the `start_date BETWEEN '2017-07-01 00:00:00' AND '2017-07-01 23:59:59'` condition is 8168.73. After the aggregation operation, there is only 1 result.

The execution as illustrated in the above example is not efficient enough, though most of the calculation logic is pushed down to the TiKV Coprocessor. You can add an appropriate index to eliminate the full table scan on `trips` by `TableScan_18`, thereby accelerating the execution of the query:

{{< copyable "sql" >}}

```sql
ALTER TABLE trips ADD INDEX (start_date);
```

{{< copyable "sql" >}}

```sql
EXPLAIN SELECT count(*) FROM trips WHERE start_date BETWEEN '2017-07-01 00:00:00' AND '2017-07-01 23:59:59';
```

```sql
+-----------------------------+---------+-----------+-------------------------------------------+---------------------------------------------------------------------------------+
| id                          | estRows | task      | access object                             | operator info                                                                   |
+-----------------------------+---------+-----------+-------------------------------------------+---------------------------------------------------------------------------------+
| StreamAgg_17                | 1.00    | root      |                                           | funcs:count(Column#13)->Column#11                                               |
| └─IndexReader_18            | 1.00    | root      |                                           | index:StreamAgg_9                                                               |
|   └─StreamAgg_9             | 1.00    | cop[tikv] |                                           | funcs:count(1)->Column#13                                                       |
|     └─IndexRangeScan_16     | 8166.73 | cop[tikv] | table:trips, index:start_date(start_date) | range:[2017-07-01 00:00:00,2017-07-01 23:59:59], keep order:false, stats:pseudo |
+-----------------------------+---------+-----------+-------------------------------------------+---------------------------------------------------------------------------------+
4 rows in set (0.00 sec)
```

After adding the index, use `IndexScan_24` to directly read the data that meets the `start_date BETWEEN '2017-07-01 00:00:00' AND '2017-07-01 23:59:59'` condition. The estimated number of rows to be scanned decreases from 19117643.00 to 8166.73. In the test environment, the execution time of this query decreases from 50.41 seconds to 0.01 seconds.

## See also

* [EXPLAIN](/sql-statements/sql-statement-explain.md)
* [EXPLAIN ANALYZE](/sql-statements/sql-statement-explain-analyze.md)
* [ANALYZE TABLE](/sql-statements/sql-statement-analyze-table.md)
* [TRACE](/sql-statements/sql-statement-trace.md)
