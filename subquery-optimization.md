---
title: 子查询相关的优化
summary: 了解子查询相关的优化。
---

# 子查询相关的优化

本文主要介绍子查询相关的优化。

通常会遇到如下情况的子查询：

- `NOT IN (SELECT ... FROM ...)`
- `NOT EXISTS (SELECT ... FROM ...)`
- `IN (SELECT ... FROM ..)`
- `EXISTS (SELECT ... FROM ...)`
- `... >/>=/</<=/=/!= (SELECT ... FROM ...)`

有时，子查询中包含了非子查询中的列，如 `select * from t where t.a in (select * from t2 where t.b=t2.b)` 中，子查询中的 `t.b` 不是子查询中的列，而是从子查询外面引入的列。这种子查询通常会被称为`关联子查询`，外部引入的列会被称为`关联列`，关联子查询相关的优化参见[关联子查询去关联](/correlated-subquery-optimization.md)。本文主要关注不涉及关联列的子查询。

子查询默认会以[理解 TiDB 执行计划](/explain-overview.md)中提到的 `semi join` 作为默认的执行方式，同时对于一些特殊的子查询，TiDB 会做一些逻辑上的替换使得查询可以获得更好的执行性能。

## `... < ALL (SELECT ... FROM ...)` 或者 `... > ANY (SELECT ... FROM ...)`

对于这种情况，可以将 `ALL` 或者 `ANY` 用 `MAX` 以及 `MIN` 来代替。不过由于在表为空时，`MAX(EXPR)` 以及 `MIN(EXPR)` 的结果会为 `NULL`，其表现形式和 `EXPR` 是有 `NULL` 值的结果一样。以及外部表达式结果为 `NULL` 时也会影响表达式的最终结果，因此这里完整的改写会是如下的形式：

- `t.id < all(select s.id from s)` 会被改写为 `t.id < min(s.id) and if(sum(s.id is null) != 0, null, true)`。
- `t.id < any (select s.id from s)` 会被改写为 `t.id < max(s.id) or if(sum(s.id is null) != 0, null, false)`。

## `... != ANY (SELECT ... FROM ...)`

对于这种情况，当子查询中不同值的个数只有一种的话，那只要和这个值对比就即可。如果子查询中不同值的个数多于 1 个，那么必然会有不相等的情况出现。因此这样的子查询可以采取如下的改写手段：

- `select * from t where t.id != any (select s.id from s)` 会被改写为 `select t.* from t, (select s.id, count(distinct s.id) as cnt_distinct from s) where (t.id != s.id or cnt_distinct > 1)`

## `... = ALL (SELECT ... FROM ...)`

对于这种情况，当子查询中不同值的个数多于一种的话，那么这个表达式的结果必然为假。因此这样的子查询在 TiDB 中会改写为如下的形式：

- `select * from t where t.id = all (select s.id from s)` 会被改写为 `select t.* from t, (select s.id, count(distinct s.id) as cnt_distinct from s) where (t.id = s.id and cnt_distinct <= 1)`

## `... IN (SELECT ... FROM ...)`

对于这种情况，会将其 `IN` 的子查询改写为 `SELECT ... FROM ... GROUP ...` 的形式，然后将 `IN` 改写为普通的 `JOIN` 的形式。如 `select * from t1 where t1.a in (select t2.a from t2)` 会被改写为 `select t1.* from t1, (select distinct(a) a from t2) t2 where t1.a = t2.a` 的形式。同时这里的 `DISTINCT` 可以在 `t2.a` 具有 `UNIQUE` 属性时被自动消去。

{{< copyable "sql" >}}

```sql
explain select * from t1 where t1.a in (select t2.a from t2);
```

```sql
+------------------------------+---------+-----------+------------------------+----------------------------------------------------------------------------+
| id                           | estRows | task      | access object          | operator info                                                              |
+------------------------------+---------+-----------+------------------------+----------------------------------------------------------------------------+
| IndexJoin_12                 | 9990.00 | root      |                        | inner join, inner:TableReader_11, outer key:test.t2.a, inner key:test.t1.a |
| ├─HashAgg_21(Build)          | 7992.00 | root      |                        | group by:test.t2.a, funcs:firstrow(test.t2.a)->test.t2.a                   |
| │ └─IndexReader_28           | 9990.00 | root      |                        | index:IndexFullScan_27                                                     |
| │   └─IndexFullScan_27       | 9990.00 | cop[tikv] | table:t2, index:idx(a) | keep order:false, stats:pseudo                                             |
| └─TableReader_11(Probe)      | 1.00    | root      |                        | data:TableRangeScan_10                                                     |
|   └─TableRangeScan_10        | 1.00    | cop[tikv] | table:t1               | range: decided by [test.t2.a], keep order:false, stats:pseudo              |
+------------------------------+---------+-----------+------------------------+----------------------------------------------------------------------------+
```

这个改写会在 `IN` 子查询相对较小，而外部查询相对较大时产生更好的执行性能。因为不经过改写的情况下，我们无法使用以 t2 为驱动表的 `index join`。同时这里的弊端便是，当改写删成的聚合无法被自动消去且 `t2` 表比较大时，反而会影响查询的性能。目前 TiDB 中使用 [tidb\_opt\_insubq\_to\_join\_and\_agg](/system-variables.md#tidb_opt_insubq_to_join_and_agg) 变量来控制这个优化的打开与否。当遇到不合适这个优化的情况可以手动关闭。

## `EXISTS` 子查询以及 `... >/>=/</<=/=/!= (SELECT ... FROM ...)`

当前对于这种场景的子查询，当它不是关联子查询时，TiDB 会在优化阶段提前展开它，将其直接替换为一个结果集直接判断结果。如下图中，`EXISTS` 会提前在优化阶段被执行为 `TRUE`，从而不会在最终的执行结果中看到它。

{{< copyable "sql" >}}

```sql
create table t1(a int);
create table t2(a int);
insert into t2 values(1);
explain select * from t where exists (select * from t2);
```

```sql
+------------------------+----------+-----------+---------------+--------------------------------+
| id                     | estRows  | task      | access object | operator info                  |
+------------------------+----------+-----------+---------------+--------------------------------+
| TableReader_12         | 10000.00 | root      |               | data:TableFullScan_11          |
| └─TableFullScan_11     | 10000.00 | cop[tikv] | table:t       | keep order:false, stats:pseudo |
+------------------------+----------+-----------+---------------+--------------------------------+
```
