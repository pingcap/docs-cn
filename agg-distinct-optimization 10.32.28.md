---
title: Distinct 优化
aliases: ['/docs-cn/dev/agg-distinct-optimization/']
---

# Distinct 优化

本文档介绍可用于 `DISTINCT` 的优化，包括简单 `DISTINCT` 和聚合函数 `DISTINCT` 的优化。

## 简单 DISTINCT

通常简单的 `DISTINCT` 会被优化成 GROUP BY 来执行。例如：

```sql
mysql> explain select DISTINCT a from t;
+--------------------------+---------+-----------+---------------+-------------------------------------------------------+
| id                       | estRows | task      | access object | operator info                                         |
+--------------------------+---------+-----------+---------------+-------------------------------------------------------+
| HashAgg_6                | 2.40    | root      |               | group by:test.t.a, funcs:firstrow(test.t.a)->test.t.a |
| └─TableReader_11         | 3.00    | root      |               | data:TableFullScan_10                                 |
|   └─TableFullScan_10     | 3.00    | cop[tikv] | table:t       | keep order:false, stats:pseudo                        |
+--------------------------+---------+-----------+---------------+-------------------------------------------------------+
3 rows in set (0.00 sec)
```

## 聚合函数 DISTINCT

通常来说，带有 `DISTINCT` 的聚合函数会单线程的在 TiDB 侧执行。使用系统变量 [`tidb_opt_distinct_agg_push_down`](/system-variables.md#tidb_opt_distinct_agg_push_down) 或者 TiDB 的配置项 [distinct-agg-push-down](/tidb-configuration-file.md#distinct-agg-push-down) 控制优化器是否执行带有 `DISTINCT` 的聚合函数（比如 `select count(distinct a) from t`）下推到 Coprocessor 的优化操作。

在以下示例中，`tidb_opt_distinct_agg_push_down` 开启前，TiDB 需要从 TiKV 读取所有数据，并在 TiDB 侧执行 `disctinct`。`tidb_opt_distinct_agg_push_down` 开启后，`distinct a` 被下推到了 Coprocessor，在 `HashAgg_5` 里新增了一个 `group by` 列 `test.t.a`。

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
