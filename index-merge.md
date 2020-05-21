---
title: 使用 Index Merge 方式访问表
category: reference
aliases: ['/docs-cn/dev/reference/performance/index-merge/']
---

# 使用 Index Merge 方式访问表

`IndexMerge` 是在 TiDB 4.0 引入的一种对表的新访问方式。在 `IndexMerge` 访问方式下，优化器可以选择对一张表使用多个索引，并将每个索引的返回结果进行合并。在某些场景下，这种访问方式能够减少大量不必要的数据扫描，提升查询的执行效率。

本文介绍了 `IndexMerge` 的适用场景、实际用例以及开启方法。

## 适用场景

对于 SQL 查询中涉及的每一张表，以前的 TiDB 优化器在物理优化阶段，会根据代价估算从以下三种表访问方式中选择一种：

- `TableScan`：以 `_tidb_rowid` 为 key 对表数据进行扫描；
- `IndexScan`：以索引列的值为 key 对索引数据进行扫描；
- `IndexLookUp`：先用索引列的值为 key 从索引获取到 `_tidb_rowid` 集合，再回表取出对应的数据行；

这三种方式对每张表最多只能使用一个索引，在有些情况下选出的执行计划并不是最优的，比如：

{{< copyable "sql" >}}

```sql
create table t(a int, b int, c int, unique key(a), unique key(b));
explain select * from t where a = 1 or b = 1;
```

由于查询的过滤条件是一个通过 `OR` 连接的表达式，我们在只能对每张表使用一个索引的限制下，无法将 `a = 1` 下推到索引 `a` 上，或将 `b = 1` 下推到索引 `b` 上，因此为了保证结果正确性，对这个查询只能生成 `TableScan` 的执行计划：

```
+-------------------------+----------+-----------+---------------+--------------------------------------+
| id                      | estRows  | task      | access object | operator info                        |
+-------------------------+----------+-----------+---------------+--------------------------------------+
| TableReader_7           | 8000.00  | root      |               | data:Selection_6                     |
| └─Selection_6           | 8000.00  | cop[tikv] |               | or(eq(test.t.a, 1), eq(test.t.b, 1)) |
|   └─TableFullScan_5     | 10000.00 | cop[tikv] | table:t       | keep order:false, stats:pseudo       |
+-------------------------+----------+-----------+---------------+--------------------------------------+
```

当 `t` 的数据量很大时，全表扫描的效率会很低，但这条查询最多却只会返回两行记录。针对这类场景，TiDB 引入了对表的新访问方式 `IndexMerge`。

## 实际用例

在 `IndexMerge` 访问方式下，优化器可以选择对一张表使用多个索引，并将每个索引的返回结果进行集合并操作。以上面查询为例，生成的执行计划将会变为：

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

`IndexMerge` 执行计划的结构和 `IndexLookUp` 很接近，都可以分为索引扫描和全表扫描两部分，只是 `IndexMerge` 的索引扫描部分可以包含多个 `IndexScan`，当表的主键索引是整数类型时，索引扫描部分甚至可能包含一个 `TableScan`，比如：

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

值得注意的是，目前 `IndexMerge` 被限定为只在无法使用单个索引时候才会被考虑，假如上述查询中的条件变为 `a = 1 and b = 1`，优化器只会考虑使用索引 `a` 或 `b` 访问，而不会选择 `IndexMerge`。

## 开启方法

默认设置下，`IndexMerge` 是关闭的，开启的方法有两种：

- 设置系统变量 `tidb_enable_index_merge` 为 1；
- 在查询中使用 SQL Hint [`USE_INDEX_MERGE`](/optimizer-hints.md#use_index_merget1_name-idx1_name--idx2_name-)；

    > **注意：**
    >
    > SQL Hint 的优先级高于系统变量。
