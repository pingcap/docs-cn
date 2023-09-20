---
title: Explain Statements Using Index Merge
summary: Learn about the execution plan information returned by the `EXPLAIN` statement in TiDB.
---

# Explain Statements Using Index Merge

Index merge is a method introduced in TiDB v4.0 to access tables. Using this method, the TiDB optimizer can use multiple indexes per table and merge the results returned by each index. In some scenarios, this method makes the query more efficient by avoiding full table scans.

Index merge in TiDB has two types: the intersection type and the union type. The former applies to the `AND` expression, while the latter applies to the `OR` expression. The union-type index merge is introduced in TiDB v4.0 as an experimental feature and has become GA in v5.4.0. The intersection type is introduced in TiDB v6.5.0, and can be used only when the [`USE_INDEX_MERGE`](/optimizer-hints.md#use_index_merget1_name-idx1_name--idx2_name-) hint is specified.

## Enable index merge

In v5.4.0 or a later TiDB version, index merge is enabled by default. In other situations, if index merge is not enabled, you need to set the variable [`tidb_enable_index_merge`](/system-variables.md#tidb_enable_index_merge-new-in-v40) to `ON` to enable this feature.

```sql
SET session tidb_enable_index_merge = ON;
```

## Examples

```sql
CREATE TABLE t(a int, b int, c int, d int, INDEX idx_a(a), INDEX idx_b(b), INDEX idx_c(c), INDEX idx_d(d));
```

```sql
EXPLAIN SELECT /*+ NO_INDEX_MERGE() */ * FROM t WHERE a = 1 OR b = 1;

+-------------------------+----------+-----------+---------------+--------------------------------------+
| id                      | estRows  | task      | access object | operator info                        |
+-------------------------+----------+-----------+---------------+--------------------------------------+
| TableReader_7           | 19.99    | root      |               | data:Selection_6                     |
| └─Selection_6           | 19.99    | cop[tikv] |               | or(eq(test.t.a, 1), eq(test.t.b, 1)) |
|   └─TableFullScan_5     | 10000.00 | cop[tikv] | table:t       | keep order:false, stats:pseudo       |
+-------------------------+----------+-----------+---------------+--------------------------------------+
EXPLAIN SELECT /*+ USE_INDEX_MERGE(t) */ * FROM t WHERE a > 1 OR b > 1;
+-------------------------------+---------+-----------+-------------------------+------------------------------------------------+
| id                            | estRows | task      | access object           | operator info                                  |
+-------------------------------+---------+-----------+-------------------------+------------------------------------------------+
| IndexMerge_8                  | 5555.56 | root      |                         | type: union                                    |
| ├─IndexRangeScan_5(Build)     | 3333.33 | cop[tikv] | table:t, index:idx_a(a) | range:(1,+inf], keep order:false, stats:pseudo |
| ├─IndexRangeScan_6(Build)     | 3333.33 | cop[tikv] | table:t, index:idx_b(b) | range:(1,+inf], keep order:false, stats:pseudo |
| └─TableRowIDScan_7(Probe)     | 5555.56 | cop[tikv] | table:t                 | keep order:false, stats:pseudo                 |
+-------------------------------+---------+-----------+-------------------------+------------------------------------------------+
```

In the preceding query, the filter condition is a `WHERE` clause that uses `OR` as the connector. Without index merge, you can use only one index per table. `a = 1` cannot be pushed down to the index `a`; neither can `b = 1` be pushed down to the index `b`. The full table scan is inefficient when a huge volume of data exists in `t`. To handle such a scenario, index merge is introduced in TiDB to access tables.

For the preceding query, the optimizer chooses the union-type index merge to access the table. Index merge allows the optimizer to use multiple indexes per table, to merge the results returned by each index, and to generate the latter execution plan in the preceding output.

In the output, the `type: union` information in `operator info` of the `IndexMerge_8` operator indicates that this operator is a union-type index merge. It has three child nodes. `IndexRangeScan_5` and `IndexRangeScan_6` scan the `RowID`s that meet the condition according to the range, and then the `TableRowIDScan_7` operator accurately reads all the data that meets the condition according to these `RowID`s.

For the scan operation that is performed on a specific range of data, such as `IndexRangeScan`/`TableRangeScan`, the `operator info` column in the result has additional information about the scan range compared with other scan operations like `IndexFullScan`/`TableFullScan`. In the above example, the `range:(1,+inf]` in the `IndexRangeScan_5` operator indicates that the operator scans the data from 1 to positive infinity.

```sql
EXPLAIN SELECT /*+ NO_INDEX_MERGE() */ * FROM t WHERE a > 1 AND b > 1 AND c = 1;  -- Does not use index merge

+--------------------------------+---------+-----------+-------------------------+---------------------------------------------+
| id                             | estRows | task      | access object           | operator info                               |
+--------------------------------+---------+-----------+-------------------------+---------------------------------------------+
| IndexLookUp_19                 | 1.11    | root      |                         |                                             |
| ├─IndexRangeScan_16(Build)     | 10.00   | cop[tikv] | table:t, index:idx_c(c) | range:[1,1], keep order:false, stats:pseudo |
| └─Selection_18(Probe)          | 1.11    | cop[tikv] |                         | gt(test.t.a, 1), gt(test.t.b, 1)            |
|   └─TableRowIDScan_17          | 10.00   | cop[tikv] | table:t                 | keep order:false, stats:pseudo              |
+--------------------------------+---------+-----------+-------------------------+---------------------------------------------+

EXPLAIN SELECT /*+ USE_INDEX_MERGE(t, idx_a, idx_b, idx_c) */ * FROM t WHERE a > 1 AND b > 1 AND c = 1;  -- Uses index merge
+-------------------------------+---------+-----------+-------------------------+------------------------------------------------+
| id                            | estRows | task      | access object           | operator info                                  |
+-------------------------------+---------+-----------+-------------------------+------------------------------------------------+
| IndexMerge_9                  | 1.11    | root      |                         | type: intersection                             |
| ├─IndexRangeScan_5(Build)     | 3333.33 | cop[tikv] | table:t, index:idx_a(a) | range:(1,+inf], keep order:false, stats:pseudo |
| ├─IndexRangeScan_6(Build)     | 3333.33 | cop[tikv] | table:t, index:idx_b(b) | range:(1,+inf], keep order:false, stats:pseudo |
| ├─IndexRangeScan_7(Build)     | 10.00   | cop[tikv] | table:t, index:idx_c(c) | range:[1,1], keep order:false, stats:pseudo    |
| └─TableRowIDScan_8(Probe)     | 1.11    | cop[tikv] | table:t                 | keep order:false, stats:pseudo                 |
+-------------------------------+---------+-----------+-------------------------+------------------------------------------------+
```

From the preceding example, you can see that the filter condition is a `WHERE` clause that uses `AND` as the connector. Before index merge is enabled, the optimizer can only choose one of the three indexes (`idx_a`, `idx_b`, or `idx_c`).

If one of the filter conditions has a low selectivity, the optimizer directly chooses the corresponding index to achieve the ideal execution efficiency. However, if the data distribution meets all of the following three conditions, you can consider using the intersection-type index merge:

- The data size of the whole table is large, and directly reading the whole table is inefficient.
- For each one of the three filter conditions, the respective selectivity is very high, so the execution efficiency of `IndexLookUp` using a single index is not ideal.
- The overall selectivity of the three filter conditions is low.

When using the intersection-type index merge to access tables, the optimizer can choose to use multiple indexes on a table, and merge the results returned by each index to generate the execution plan of the latter `IndexMerge` in the preceding example output. The `type: intersection` information in the `operator info` of the `IndexMerge_9` operator indicates that this operator is an intersection-type index merge. The other parts of the execution plan are similar to the preceding union-type index merge example.

> **Note:**
>
> - The Index Merge feature is enabled by default from v5.4.0. That is, [`tidb_enable_index_merge`](/system-variables.md#tidb_enable_index_merge-new-in-v40) is `ON`.
>
> - You can use the SQL hint [`USE_INDEX_MERGE`](/optimizer-hints.md#use_index_merget1_name-idx1_name--idx2_name-) to force the optimizer to apply Index Merge, regardless of the setting of `tidb_enable_index_merge`. To enable Index Merge when the filtering conditions contain expressions that cannot be pushed down, you must use the SQL hint [`USE_INDEX_MERGE`](/optimizer-hints.md#use_index_merget1_name-idx1_name--idx2_name-).
>
> - If the optimizer can choose the single index scan method (other than full table scan) for a query plan, the optimizer will not automatically use index merge. For the optimizer to use index merge, you need to use the optimizer hint.
>
> - Index Merge is not supported in [tempoaray tables](/temporary-tables.md) for now.
>
> - The intersection-type index merge will not automatically be selected by the optimizer. You must specify the **table name and index name** using the [`USE_INDEX_MERGE`](/optimizer-hints.md#use_index_merget1_name-idx1_name--idx2_name-) hint for it to be selected.
