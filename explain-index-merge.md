---
title: 使用索引合并的 EXPLAIN 语句
summary: 了解 TiDB 中 `EXPLAIN` 语句返回的执行计划信息。
---

# 使用索引合并的 EXPLAIN 语句

索引合并是 TiDB v4.0 引入的一种表访问方法。使用此方法时，TiDB 优化器可以在每个表上使用多个索引，并合并每个索引返回的结果。在某些场景下，这种方法通过避免全表扫描使查询更加高效。

TiDB 中的索引合并有两种类型：交集类型和并集类型。前者适用于 `AND` 表达式，而后者适用于 `OR` 表达式。并集类型的索引合并在 TiDB v4.0 中作为实验特性引入，并在 v5.4.0 中正式发布（GA）。交集类型在 TiDB v6.5.0 中引入，只有在指定 [`USE_INDEX_MERGE`](/optimizer-hints.md#use_index_merget1_name-idx1_name--idx2_name-) 提示时才能使用。

## 启用索引合并

在 TiDB v5.4.0 或更高版本中，索引合并默认启用。在其他情况下，如果索引合并未启用，你需要将变量 [`tidb_enable_index_merge`](/system-variables.md#tidb_enable_index_merge-new-in-v40) 设置为 `ON` 来启用此功能。

```sql
SET session tidb_enable_index_merge = ON;
```

## 示例

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

在上述查询中，过滤条件是使用 `OR` 作为连接符的 `WHERE` 子句。在没有索引合并的情况下，每个表只能使用一个索引。`a = 1` 不能下推到索引 `a`，`b = 1` 也不能下推到索引 `b`。当表 `t` 中存在大量数据时，全表扫描效率很低。为了处理这种情况，TiDB 引入了索引合并来访问表。

对于上述查询，优化器选择使用并集类型的索引合并来访问表。索引合并允许优化器在每个表上使用多个索引，合并每个索引返回的结果，并生成上述输出中的后一个执行计划。

在输出中，`IndexMerge_8` 算子的 `operator info` 中的 `type: union` 信息表明这个算子是并集类型的索引合并。它有三个子节点。`IndexRangeScan_5` 和 `IndexRangeScan_6` 根据范围扫描满足条件的 `RowID`，然后 `TableRowIDScan_7` 算子根据这些 `RowID` 准确读取所有满足条件的数据。

对于在特定数据范围内执行的扫描操作，如 `IndexRangeScan`/`TableRangeScan`，结果中的 `operator info` 列与其他扫描操作（如 `IndexFullScan`/`TableFullScan`）相比，有关于扫描范围的额外信息。在上面的例子中，`IndexRangeScan_5` 算子中的 `range:(1,+inf]` 表示该算子扫描从 1 到正无穷的数据。

```sql
EXPLAIN SELECT /*+ NO_INDEX_MERGE() */ * FROM t WHERE a > 1 AND b > 1 AND c = 1;  -- 不使用索引合并

+--------------------------------+---------+-----------+-------------------------+---------------------------------------------+
| id                             | estRows | task      | access object           | operator info                               |
+--------------------------------+---------+-----------+-------------------------+---------------------------------------------+
| IndexLookUp_19                 | 1.11    | root      |                         |                                             |
| ├─IndexRangeScan_16(Build)     | 10.00   | cop[tikv] | table:t, index:idx_c(c) | range:[1,1], keep order:false, stats:pseudo |
| └─Selection_18(Probe)          | 1.11    | cop[tikv] |                         | gt(test.t.a, 1), gt(test.t.b, 1)            |
|   └─TableRowIDScan_17          | 10.00   | cop[tikv] | table:t                 | keep order:false, stats:pseudo              |
+--------------------------------+---------+-----------+-------------------------+---------------------------------------------+

EXPLAIN SELECT /*+ USE_INDEX_MERGE(t, idx_a, idx_b, idx_c) */ * FROM t WHERE a > 1 AND b > 1 AND c = 1;  -- 使用索引合并
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

从上面的例子可以看出，过滤条件是使用 `AND` 作为连接符的 `WHERE` 子句。在启用索引合并之前，优化器只能选择三个索引（`idx_a`、`idx_b` 或 `idx_c`）中的一个。

如果其中一个过滤条件的选择性较低，优化器会直接选择相应的索引来实现理想的执行效率。但是，如果数据分布满足以下三个条件，你可以考虑使用交集类型的索引合并：

- 整个表的数据量很大，直接读取整个表效率不高。
- 对于三个过滤条件中的每一个，各自的选择性都很高，所以使用单个索引的 `IndexLookUp` 的执行效率不理想。
- 三个过滤条件的整体选择性较低。

在使用交集类型的索引合并访问表时，优化器可以选择在一个表上使用多个索引，并合并每个索引返回的结果，生成上述示例输出中后一个 `IndexMerge` 的执行计划。`IndexMerge_9` 算子的 `operator info` 中的 `type: intersection` 信息表明这个算子是交集类型的索引合并。执行计划的其他部分与前面的并集类型索引合并示例类似。

> **注意：**
>
> - 从 v5.4.0 开始，索引合并功能默认启用。也就是说，[`tidb_enable_index_merge`](/system-variables.md#tidb_enable_index_merge-new-in-v40) 为 `ON`。
>
> - 你可以使用 SQL 提示 [`USE_INDEX_MERGE`](/optimizer-hints.md#use_index_merget1_name-idx1_name--idx2_name-) 强制优化器应用索引合并，而不考虑 `tidb_enable_index_merge` 的设置。当过滤条件包含无法下推的表达式时，你必须使用 SQL 提示 [`USE_INDEX_MERGE`](/optimizer-hints.md#use_index_merget1_name-idx1_name--idx2_name-)。
>
> - 如果优化器可以为查询计划选择单索引扫描方法（而不是全表扫描），优化器将不会自动使用索引合并。要使优化器使用索引合并，你需要使用优化器提示。从 v8.1.0 开始，你可以通过设置[优化器修复控制 52869](/optimizer-fix-controls.md#52869-new-in-v810) 来移除这个限制。移除这个限制可以让优化器在更多查询中自动选择索引合并，但可能会导致优化器忽略最优执行计划。因此，建议在移除这个限制之前，对实际使用场景进行充分测试，以确保不会导致性能下降。
>
> - 目前[临时表](/temporary-tables.md)不支持索引合并。
>
> - 交集类型的索引合并不会被优化器自动选择。你必须使用 [`USE_INDEX_MERGE`](/optimizer-hints.md#use_index_merget1_name-idx1_name--idx2_name-) 提示指定**表名和索引名**才能选择它。
