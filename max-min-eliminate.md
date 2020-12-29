---
title: Max/Min 函数消除规则
---

# Max/Min 函数消除规则

在 SQL 中包含了 `max`/`min` 函数时，查询优化器会尝试使用 `max`/`min` 消除优化规则来将 `max`/`min` 聚合函数转换为 TopN 算子，从而能够有效地利用索引进行查询。

根据 `select` 语句中 `max`/`min` 函数的个数，这一优化规则有以下两种表现形式：

+ [只有一个 max/min 函数时的优化规则](#只有一个-maxmin-函数时的优化规则)
+ [存在多个 max/min 函数时的优化规则](#存在多个-maxmin-函数时的优化规则)

## 只有一个 max/min 函数时的优化规则

当一个 SQL 满足以下条件时，就会应用这个规则：

+ 只有一个聚合函数，且为 `max` 或者 `min` 函数。
+ 聚合函数没有相应的 `group by` 语句。

例如：

{{< copyable "sql" >}}

```sql
select max(a) from t
```

这时 `max`/`min` 消除优化规则会将其重写为：

{{< copyable "sql" >}}

```sql
select max(a) from (select a from t where a is not null order by a desc limit 1) t
```

这个新的 SQL 语句在 `a` 列存在索引（或 `a` 列是某个联合索引的前缀）时，能够利用索引只扫描一行数据来得到最大或者最小值，从而避免对整个表的扫描。

上述例子最终得到的执行计划如下:

```
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

## 存在多个 max/min 函数时的优化规则

当一个 SQL 满足以下条件时，就会应用这个规则：

+ 有多个聚合函数，且所有的聚合函数都是 max/min
+ 聚合函数没有相应的 `group by` 语句。
+ 每个 `max`/`min` 聚合函数参数中的列都有索引能够保序。

下面是一个简单的例子：

{{< copyable "sql" >}}

```sql
select max(a) - min(a) from t
```

优化规则会先检查 `a` 列是否存在索引能够为其保序，如果存在，这个 SQL 会先被重写为两个子查询的笛卡尔积：

{{< copyable "sql" >}}

```sql
select max_a - min_a
from
    (select max(a) as max_a from t) t1,
    (select min(a) as min_a from t) t2
```

这样，两个子句中的 `max`/`min` 函数就可以使用上述“只有一个 `max`/`min` 函数时的优化规则”分别进行优化，最终重写为：

{{< copyable "sql" >}}

```sql
select max_a - min_a
from
    (select max(a) as max_a from (select a from t where a is not null order by a desc limit 1) t) t1,
    (select min(a) as min_a from (select a from t where a is not null order by a asc limit 1) t) t2
```

同样的，如果 `a` 列能够使用索引保序，那这个优化只会扫描两行数据，避免了对整个表的扫描。但如果 `a` 列没有可以保序的索引，这个变换会使原本只需一次的全表扫描变成两次，因此这个规则就不会被应用。

最后得到的执行计划：

```
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
