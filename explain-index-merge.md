---
title: 用 EXPLAIN 查看索引合并的 SQL 执行计划
summary: 了解 TiDB 中 EXPLAIN 语句返回的执行计划信息。
---

# 用 EXPLAIN 查看索引合并的 SQL 执行计划

索引合并是从 TiDB v4.0 起引入的一种新的表访问方式。在这种访问方式下，TiDB 优化器可以选择对一张表使用多个索引，并将每个索引的返回结果进行合并。在某些场景下，这种访问方式能够减少大量不必要的数据扫描，提升查询的执行效率。

TiDB 中的索引合并分为交集型和并集型两种类型，分别适用于由 `AND` 连接的表达式和由 `OR` 连接的表达式。其中，并集型索引合并在 TiDB v4.0 作为实验功能引入，在 v5.4.0 成为正式功能 (GA)。交集型索引合并从 TiDB v6.5.0 起引入，且必须使用 [`USE_INDEX_MERGE`](/optimizer-hints.md#use_index_merget1_name-idx1_name--idx2_name-) Hint 指定才能使用。

## 开启索引合并

在 v5.4.0 及以上版本的新建集群中，索引合并默认开启。在其他情况下如果未开启，可将 `tidb_enable_index_merge` 的值设为 `ON` 来开启索引合并功能。

{{< copyable "sql" >}}

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

例如，在上述示例中，过滤条件是使用 `OR` 连接的 `WHERE` 子句。在启用索引合并前，每个表只能使用一个索引，不能将 `a = 1` 下推到索引 `a`，也不能将 `b = 1` 下推到索引 `b`。当 `t` 中存在大量数据时，全表扫描的效率会很低。

对于以上查询语句，优化器选择了并集型索引合并的方式访问表。在这种访问方式下，优化器可以选择对一张表使用多个索引，并将每个索引的返回结果进行合并，生成以上两个示例中的后一个执行计划。此时的 `IndexMerge_8` 算子的 `operator info` 中的 `type: union` 表示该算子是一个并集型索引合并算子。它有三个子节点，其中 `IndexRangeScan_5` 和 `IndexRangeScan_6` 根据范围扫描得到符合条件的所有 `RowID`，再由 `TableRowIDScan_7` 算子根据这些 `RowID` 精确地读取所有满足条件的数据。

其中对于 `IndexRangeScan`/`TableRangeScan` 一类按范围进行的扫表操作，`EXPLAIN` 表中 `operator info` 列相比于其他扫表操作，多了被扫描数据的范围这一信息。比如上面的例子中，`IndexRangeScan_5` 算子中的 `range:(1,+inf]` 这一信息表示该算子扫描了从 1 到正无穷这个范围的数据。

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

在如上示例中，过滤条件是使用 `AND` 连接的 `WHERE` 子句。在启用索引合并前，只能选择使用 `idx_a`、`idx_b` 或 `idx_c` 三个索引中的一个。

如果三个过滤条件中的其中一个的过滤性非常好，直接选择对应的索引即可达到理想的执行效率。但如果数据分布同时满足以下三种情形，可以考虑使用交集型索引合并：

- 全表的数据量相当大，导致直接读全表的执行效率非常低下
- 每个过滤条件单独的过滤性都不够好，导致 `IndexLookUp` 使用单个索引的执行效率也不够理想
- 三个过滤条件整体的过滤性非常好

在交集型索引合并访问方式下，优化器可以选择对一张表使用多个索引，并将每个索引的返回结果取交集，生成以上两个示例中的后一个执行计划。此时的 `IndexMerge_9` 算子的 `operator info` 中的 `type: intersection` 表示该算子是一个交集型索引合并算子。该执行计划的其它部分和上述并集型索引合并示例类似。

> **注意：**
>
> - TiDB 的索引合并特性在 v5.4.0 及之后的版本默认开启，即 [`tidb_enable_index_merge`](/system-variables.md#tidb_enable_index_merge-从-v40-版本开始引入) 为 `ON`。
> - 如果查询中使用了 SQL 优化器 Hint [`USE_INDEX_MERGE`](/optimizer-hints.md#use_index_merget1_name-idx1_name--idx2_name-)，无论 `tidb_enable_index_merge` 开关是否开启，都会强制使用索引合并特性。当过滤条件中有无法下推的表达式时，必须使用 Hint [`USE_INDEX_MERGE`](/optimizer-hints.md#use_index_merget1_name-idx1_name--idx2_name-) 才能开启索引合并。
> - 如果查询有除了全表扫描以外的单索引扫描方式可以选择，优化器不会自动选择索引合并，只能通过 Hint 指定使用索引合并。从 v8.1.0 开始，这个限制可以通过 [Optimizer Fix Control 52869](/optimizer-fix-controls.md#52869-从-v810-版本开始引入) 解除。解除此限制能让优化器在更多查询中自动选择索引合并，但也有可能忽略其他更好的执行计划，因此建议在解除此限制前针对实际场景进行充分测试，确保不会带来性能回退。
> - 索引合并目前无法在临时表上使用。
> - 交集型索引合并目前不会被优化器自动选择，必须使用 [`USE_INDEX_MERGE`](/optimizer-hints.md#use_index_merget1_name-idx1_name--idx2_name-) Hint 指定**表名和索引名**时才会被选择。

## 其他类型查询的执行计划

+ [MPP 模式查询的执行计划](/explain-mpp.md)
+ [索引查询的执行计划](/explain-indexes.md)
+ [Join 查询的执行计划](/explain-joins.md)
+ [子查询的执行计划](/explain-subqueries.md)
+ [聚合查询的执行计划](/explain-aggregation.md)
+ [视图查询的执行计划](/explain-views.md)
+ [分区查询的执行计划](/explain-partitions.md)
