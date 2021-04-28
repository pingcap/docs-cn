---
title: 用 EXPLAIN 查看开启 IndexMerge 的 SQL 执行计划
summary: 了解 TiDB 中 EXPLAIN 语句返回的执行计划信息。
---

# 用 EXPLAIN 查看开启 IndexMerge 的 SQL 执行计划

`IndexMerge` 是 TiDB v4.0 中引入的一种对表的新访问方式。在这种访问方式下，TiDB 优化器可以选择对一张表使用多个索引，并将每个索引的返回结果进行合并。在某些场景下，这种访问方式能够减少大量不必要的数据扫描，提升查询的执行效率。

```sql
EXPLAIN SELECT * from t where a = 1 or b = 1;
+-------------------------+----------+-----------+---------------+--------------------------------------+
| id                      | estRows  | task      | access object | operator info                        |
+-------------------------+----------+-----------+---------------+--------------------------------------+
| TableReader_7           | 8000.00  | root      |               | data:Selection_6                     |
| └─Selection_6           | 8000.00  | cop[tikv] |               | or(eq(test.t.a, 1), eq(test.t.b, 1)) |
|   └─TableFullScan_5     | 10000.00 | cop[tikv] | table:t       | keep order:false, stats:pseudo       |
+-------------------------+----------+-----------+---------------+--------------------------------------+
set @@tidb_enable_index_merge = 1;
explain select * from t use index(idx_a, idx_b) where a > 1 or b > 1;
+--------------------------------+---------+-----------+-------------------------+------------------------------------------------+
| id                             | estRows | task      | access object           | operator info                                  |
+--------------------------------+---------+-----------+-------------------------+------------------------------------------------+
| IndexMerge_16                  | 6666.67 | root      |                         |                                                |
| ├─IndexRangeScan_13(Build)     | 3333.33 | cop[tikv] | table:t, index:idx_a(a) | range:(1,+inf], keep order:false, stats:pseudo |
| ├─IndexRangeScan_14(Build)     | 3333.33 | cop[tikv] | table:t, index:idx_b(b) | range:(1,+inf], keep order:false, stats:pseudo |
| └─TableRowIDScan_15(Probe)     | 6666.67 | cop[tikv] | table:t                 | keep order:false, stats:pseudo                 |
+--------------------------------+---------+-----------+-------------------------+------------------------------------------------+
```

例如，在上述示例中，过滤条件是使用 `OR` 条件连接的 `WHERE` 子句。在启用 `IndexMerge` 前，每个表只能使用一个索引，不能将 `a = 1` 下推到索引 `a`，也不能将 `b = 1` 下推到索引 `b`。当 `t` 中存在大量数据时，全表扫描的效率会很低。针对这类场景，TiDB 引入了对表的新访问方式 `IndexMerge`。

在 `IndexMerge` 访问方式下，优化器可以选择对一张表使用多个索引，并将每个索引的返回结果进行合并，生成以上示例中后一个 `IndexMerge` 的执行计划。此时的 `IndexMerge_16` 算子有三个子节点，其中 `IndexRangeScan_13` 和 `IndexRangeScan_14` 根据范围扫描得到符合条件的所有 `RowID`，再由 `TableRowIDScan_15` 算子根据这些 `RowID` 精确地读取所有满足条件的数据。

其中对于 `IndexRangeScan`/`TableRangeScan` 一类按范围进行的扫表操作，`EXPLAIN` 表中 `operator info` 列相比于其他扫表操作，多了被扫描数据的范围这一信息。比如上面的例子中，`IndexRangeScan_13` 算子中的 `range:(1,+inf]` 这一信息表示该算子扫描了从 1 到正无穷这个范围的数据。

> **注意：**
>
> 目前，TiDB 的 `IndexMerge` 特性在 TiDB 4.0.0-rc.1 版本中默认关闭。同时 4.0 版本中的 `IndexMerge` 目前支持的场景仅限于析取范式（`or` 连接的表达式），暂不支持合取范式（`and` 连接的表达式）。开启 `IndexMerge` 特性有以下方法：
>
> - 设置系统变量 `tidb_enable_index_merge=1`；
>
> - 在查询中使用 SQL 优化器 Hint [`USE_INDEX_MERGE`](/optimizer-hints.md#use_index_merget1_name-idx1_name--idx2_name-)。
>
> SQL Hint 的优先级高于系统变量。

## 其他类型查询的执行计划

+ [MPP 模式查询的执行计划](/explain-mpp.md)
+ [索引查询的执行计划](/explain-indexes.md)
+ [Join 查询的执行计划](/explain-joins.md)
+ [子查询的执行计划](/explain-subqueries.md)
+ [聚合查询的执行计划](/explain-aggregation.md)
+ [视图查询的执行计划](/explain-views.md)
+ [分区查询的执行计划](/explain-partitions.md)
