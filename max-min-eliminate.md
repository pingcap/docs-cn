---
title: 消除 Max/Min
summary: 介绍消除 Max/Min 函数的规则。
---

# 消除 Max/Min

当 SQL 语句中包含 `max`/`min` 函数时，查询优化器会尝试通过应用 `max`/`min` 优化规则将 `max`/`min` 聚合函数转换为 TopN 算子。通过这种方式，TiDB 可以通过索引更高效地执行查询。

根据 `select` 语句中 `max`/`min` 函数的数量，这个优化规则分为以下两种类型：

- [只有一个 `max`/`min` 函数的语句](#one-maxmin-function)
- [有多个 `max`/`min` 函数的语句](#multiple-maxmin-functions)

## 一个 `max`/`min` 函数

当 SQL 语句满足以下条件时，会应用此规则：

- 语句只包含一个聚合函数，该函数是 `max` 或 `min`。
- 该聚合函数没有相关的 `group by` 子句。

例如：

{{< copyable "sql" >}}

```sql
select max(a) from t
```

优化规则将语句重写如下：

{{< copyable "sql" >}}

```sql
select max(a) from (select a from t where a is not null order by a desc limit 1) t
```

当列 `a` 有索引，或者列 `a` 是某个复合索引的前缀时，在索引的帮助下，新的 SQL 语句只需扫描一行数据就能找到最大值或最小值。这种优化避免了全表扫描。

示例语句的执行计划如下：

```sql
mysql> explain select max(a) from t;
+------------------------------+---------+-----------+-------------------------+-------------------------------------+
| id                           | estRows | task      | access object           | operator info                       |
+------------------------------+---------+-----------+-------------------------+-------------------------------------+
| StreamAgg_13                 | 1.00    | root      |                         | funcs:max(test.t.a)->Column#4       |
| └─Limit_17                   | 1.00    | root      |                         | offset:0, count:1                   |
|   └─IndexReader_27           | 1.00    | root      |                         | index:Limit_26                      |
|     └─Limit_26               | 1.00    | cop[tikv] |                         | offset:0, count:1                   |
|       └─IndexFullScan_25     | 1.00    | cop[tikv] | table:t, index:idx_a(a) | keep order:true, desc, stats:pseudo |
+------------------------------+---------+-----------+-------------------------+-------------------------------------+
5 rows in set (0.00 sec)
```

## 多个 `max`/`min` 函数

当 SQL 语句满足以下条件时，会应用此规则：

- 语句包含多个聚合函数，这些函数都是 `max` 或 `min` 函数。
- 所有聚合函数都没有相关的 `group by` 子句。
- 每个 `max`/`min` 函数中的列都有保序的索引。

例如：

{{< copyable "sql" >}}

```sql
select max(a) - min(a) from t
```

优化规则首先检查列 `a` 是否有保序的索引。如果有，SQL 语句会被重写为两个子查询的笛卡尔积：

{{< copyable "sql" >}}

```sql
select max_a - min_a
from
    (select max(a) as max_a from t) t1,
    (select min(a) as min_a from t) t2
```

通过重写，优化器可以分别对两个子查询应用只有一个 `max`/`min` 函数的语句规则。然后语句被重写如下：

{{< copyable "sql" >}}

```sql
select max_a - min_a
from
    (select max(a) as max_a from (select a from t where a is not null order by a desc limit 1) t) t1,
    (select min(a) as min_a from (select a from t where a is not null order by a asc limit 1) t) t2
```

同样，如果列 `a` 有保序的索引，优化后的执行只需扫描两行数据而不是整个表。但是，如果列 `a` 没有保序的索引，这个规则会导致两次全表扫描，而不重写的话只需要一次全表扫描。因此，在这种情况下不会应用此规则。

最终的执行计划如下：

```sql
mysql> explain select max(a)-min(a) from t;
+------------------------------------+---------+-----------+-------------------------+-------------------------------------+
| id                                 | estRows | task      | access object           | operator info                       |
+------------------------------------+---------+-----------+-------------------------+-------------------------------------+
| Projection_17                      | 1.00    | root      |                         | minus(Column#4, Column#5)->Column#6 |
| └─HashJoin_18                      | 1.00    | root      |                         | CARTESIAN inner join                |
|   ├─StreamAgg_45(Build)            | 1.00    | root      |                         | funcs:min(test.t.a)->Column#5       |
|   │ └─Limit_49                     | 1.00    | root      |                         | offset:0, count:1                   |
|   │   └─IndexReader_59             | 1.00    | root      |                         | index:Limit_58                      |
|   │     └─Limit_58                 | 1.00    | cop[tikv] |                         | offset:0, count:1                   |
|   │       └─IndexFullScan_57       | 1.00    | cop[tikv] | table:t, index:idx_a(a) | keep order:true, stats:pseudo       |
|   └─StreamAgg_24(Probe)            | 1.00    | root      |                         | funcs:max(test.t.a)->Column#4       |
|     └─Limit_28                     | 1.00    | root      |                         | offset:0, count:1                   |
|       └─IndexReader_38             | 1.00    | root      |                         | index:Limit_37                      |
|         └─Limit_37                 | 1.00    | cop[tikv] |                         | offset:0, count:1                   |
|           └─IndexFullScan_36       | 1.00    | cop[tikv] | table:t, index:idx_a(a) | keep order:true, desc, stats:pseudo |
+------------------------------------+---------+-----------+-------------------------+-------------------------------------+
12 rows in set (0.01 sec)
```
