---
title: Access Tables Using `IndexMerge`
summary: Learn how to access tables using the `IndexMerge` query execution plan.
aliases: ['/docs/dev/index-merge/','/docs/dev/reference/performance/index-merge/']
---

# Access Tables Using `IndexMerge`

`IndexMerge` is a method introduced in TiDB v4.0 to access tables. Using this method, the TiDB optimizer can use multiple indexes per table and merge the results returned by each index. In some scenarios, this method makes the query more efficient by avoiding full table scans.

This document introduces the applicable scenarios, a use case, and how to enable `IndexMerge`.

## Applicable scenarios

For each table involved in the SQL query, the TiDB optimizer during the physical optimization used to choose one of the following three access methods based on the cost estimation:

- `TableScan`: Scans the table data, with `_tidb_rowid` as the key.
- `IndexScan`: Scans the index data, with the index column values as the key.
- `IndexLookUp`: Gets the `_tidb_rowid` set from the index, with the index column values as the key, and then retrieves the corresponding data rows of the tables.

The above methods can use only one index per table. In some cases, the selected execution plan is not optimal. For example:

{{< copyable "sql" >}}

```sql
create table t(a int, b int, c int, unique key(a), unique key(b));
explain select * from t where a = 1 or b = 1;
```

In the above query, the filter condition is a `WHERE` clause that uses `OR` as the connector. Because you can use only one index per table, `a = 1` cannot be pushed down to the index `a`; neither can `b = 1` be pushed down to the index `b`. To ensure that the result is correct, the execution plan of `TableScan` is generated for the query:

```
+-------------------------+----------+-----------+---------------+--------------------------------------+
| id                      | estRows  | task      | access object | operator info                        |
+-------------------------+----------+-----------+---------------+--------------------------------------+
| TableReader_7           | 8000.00  | root      |               | data:Selection_6                     |
| └─Selection_6           | 8000.00  | cop[tikv] |               | or(eq(test.t.a, 1), eq(test.t.b, 1)) |
|   └─TableFullScan_5     | 10000.00 | cop[tikv] | table:t       | keep order:false, stats:pseudo       |
+-------------------------+----------+-----------+---------------+--------------------------------------+
```

The full table scan is inefficient when a huge volume of data exists in `t`, but the query returns only two rows at most. To handle such a scenario, `IndexMerge` is introduced in TiDB to access tables.

## Use case

`IndexMerge` allows the optimizer to use multiple indexes per table, and merge the results returned by each index before further operation. Take the [above query](#applicable-scenarios) as an example, the generated execution plan is shown as follows:

```
+--------------------------------+---------+-----------+---------------------+---------------------------------------------+
| id                             | estRows | task      | access object       | operator info                               |
+--------------------------------+---------+-----------+---------------------+---------------------------------------------+
| IndexMerge_11                  | 2.00    | root      |                     |                                             |
| ├─IndexRangeScan_8(Build)      | 1.00    | cop[tikv] | table:t, index:a(a) | range:[1,1], keep order:false, stats:pseudo |
| ├─IndexRangeScan_9(Build)      | 1.00    | cop[tikv] | table:t, index:b(b) | range:[1,1], keep order:false, stats:pseudo |
| └─TableRowIDScan_10(Probe)     | 2.00    | cop[tikv] | table:t             | keep order:false, stats:pseudo              |
+--------------------------------+---------+-----------+---------------------+---------------------------------------------+
```

The structure of the `IndexMerge` execution plan is similar to that of the `IndexLookUp`, both of which consist of index scans and full table scans. However, the index scan part of `IndexMerge` might include multiple `IndexScan`s. When the primary key index of the table is the integer type, index scans might even include `TableScan`. For example:

{{< copyable "sql" >}}

```sql
create table t(a int primary key, b int, c int, unique key(b));
```

```
Query OK, 0 rows affected (0.01 sec)
```

{{< copyable "sql" >}}

```sql
explain select * from t where a = 1 or b = 1;
```

```
+--------------------------------+---------+-----------+---------------------+---------------------------------------------+
| id                             | estRows | task      | access object       | operator info                               |
+--------------------------------+---------+-----------+---------------------+---------------------------------------------+
| IndexMerge_11                  | 2.00    | root      |                     |                                             |
| ├─TableRangeScan_8(Build)      | 1.00    | cop[tikv] | table:t             | range:[1,1], keep order:false, stats:pseudo |
| ├─IndexRangeScan_9(Build)      | 1.00    | cop[tikv] | table:t, index:b(b) | range:[1,1], keep order:false, stats:pseudo |
| └─TableRowIDScan_10(Probe)     | 2.00    | cop[tikv] | table:t             | keep order:false, stats:pseudo              |
+--------------------------------+---------+-----------+---------------------+---------------------------------------------+
4 rows in set (0.01 sec)
```

Note that `IndexMerge` is used only when the optimizer cannot use a single index to access the table. If the condition in the query expression is `a = 1 and b = 1`, the optimizer uses the index `a` or the index `b`, instead of `IndexMerge`, to access the table.

## Enable `IndexMerge`

`IndexMerge` is disabled by default. Enable the `IndexMerge` in one of two ways:

- Set the `tidb_enable_index_merge` system variable to `1`;
- Use the SQL Hint [`USE_INDEX_MERGE`](/optimizer-hints.md#use_index_merget1_name-idx1_name--idx2_name-) in the query.

    > **Note:**
    >
    > The SQL Hint has a higher priority over the system variable.
