---
title: DISTINCT 优化
summary: 介绍 TiDB 查询优化器中的 `distinct` 优化。
---

# DISTINCT 优化

本文档介绍 TiDB 查询优化器中的 `distinct` 优化，包括 `SELECT DISTINCT` 和聚合函数中的 `DISTINCT`。

## `SELECT` 语句中的 `DISTINCT` 修饰符

`DISTINCT` 修饰符用于从结果集中删除重复的行。`SELECT DISTINCT` 会被转换为 `GROUP BY`，例如：

```sql
mysql> explain SELECT DISTINCT a from t;
+--------------------------+---------+-----------+---------------+-------------------------------------------------------+
| id                       | estRows | task      | access object | operator info                                         |
+--------------------------+---------+-----------+---------------+-------------------------------------------------------+
| HashAgg_6                | 2.40    | root      |               | group by:test.t.a, funcs:firstrow(test.t.a)->test.t.a |
| └─TableReader_11         | 3.00    | root      |               | data:TableFullScan_10                                 |
|   └─TableFullScan_10     | 3.00    | cop[tikv] | table:t       | keep order:false, stats:pseudo                        |
+--------------------------+---------+-----------+---------------+-------------------------------------------------------+
3 rows in set (0.00 sec)
```

## 聚合函数中的 `DISTINCT` 选项

通常，带有 `DISTINCT` 选项的聚合函数在 TiDB 层使用单线程执行模型执行。

<CustomContent platform="tidb">

[`tidb_opt_distinct_agg_push_down`](/system-variables.md#tidb_opt_distinct_agg_push_down) 系统变量或 TiDB 中的 [`distinct-agg-push-down`](/tidb-configuration-file.md#distinct-agg-push-down) 配置项控制是否重写 distinct 聚合查询并将其下推到 TiKV 或 TiFlash Coprocessor。

</CustomContent>

<CustomContent platform="tidb-cloud">

TiDB 中的 [`tidb_opt_distinct_agg_push_down`](/system-variables.md#tidb_opt_distinct_agg_push_down) 系统变量控制是否重写 distinct 聚合查询并将其下推到 TiKV 或 TiFlash Coprocessor。

</CustomContent>

以下面的查询为例说明这个优化。`tidb_opt_distinct_agg_push_down` 默认是禁用的，这意味着聚合函数在 TiDB 层执行。通过将其值设置为 `1` 启用此优化后，`count(distinct a)` 中的 `distinct a` 部分会被下推到 TiKV 或 TiFlash Coprocessor：在 TiKV Coprocessor 中有一个 HashAgg_5 用于删除列 a 上的重复值。这可能会减少 TiDB 层 `HashAgg_8` 的计算开销。

```sql
mysql> desc select count(distinct a) from test.t;
+-------------------------+----------+-----------+---------------+------------------------------------------+
| id                      | estRows  | task      | access object | operator info                            |
+-------------------------+----------+-----------+---------------+------------------------------------------+
| StreamAgg_6             | 1.00     | root      |               | funcs:count(distinct test.t.a)->Column#4 |
| └─TableReader_10        | 10000.00 | root      |               | data:TableFullScan_9                     |
|   └─TableFullScan_9     | 10000.00 | cop[tikv] | table:t       | keep order:false, stats:pseudo           |
+-------------------------+----------+-----------+---------------+------------------------------------------+
3 rows in set (0.01 sec)

mysql> set session tidb_opt_distinct_agg_push_down = 1;
Query OK, 0 rows affected (0.00 sec)

mysql> desc select count(distinct a) from test.t;
+---------------------------+----------+-----------+---------------+------------------------------------------+
| id                        | estRows  | task      | access object | operator info                            |
+---------------------------+----------+-----------+---------------+------------------------------------------+
| HashAgg_8                 | 1.00     | root      |               | funcs:count(distinct test.t.a)->Column#3 |
| └─TableReader_9           | 1.00     | root      |               | data:HashAgg_5                           |
|   └─HashAgg_5             | 1.00     | cop[tikv] |               | group by:test.t.a,                       |
|     └─TableFullScan_7     | 10000.00 | cop[tikv] | table:t       | keep order:false, stats:pseudo           |
+---------------------------+----------+-----------+---------------+------------------------------------------+
4 rows in set (0.00 sec)
```
