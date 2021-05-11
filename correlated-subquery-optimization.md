---
title: 关联子查询去关联
summary: 了解如何给关联子查询解除关联。
aliases: ['/docs-cn/dev/correlated-subquery-optimization/']
---

# 关联子查询去关联

[子查询相关的优化](/subquery-optimization.md)中介绍了当没有关联列时，TiDB 是如何处理子查询的。由于为关联子查询解除关联依赖比较复杂，本文档中会介绍一些简单的场景以及这个优化规则的适用范围。

## 简介

以 `select * from t1 where t1.a < (select sum(t2.a) from t2 where t2.b = t1.b)` 为例，这里子查询 `t1.a < (select sum(t2.a) from t2 where t2.b = t1.b)` 中涉及了关联列上的条件 `t2.b=t1.b`，不过恰好由于这是一个等值条件，因此可以将其等价的改写为 `select t1.* from t1, (select b, sum(a) sum_a from t2 group by b) t2 where t1.b = t2.b and t1.a < t2.sum_a;`。这样，一个关联子查询就被重新改写为 `JOIN` 的形式。

TiDB 之所以要进行这样的改写，是因为关联子查询每次子查询执行时都是要和它的外部查询结果绑定的。在上面的例子中，如果 `t1.a` 有一千万个值，那这个子查询就要被重复执行一千万次，因为 `t2.b=t1.b` 这个条件会随着 `t1.a` 值的不同而发生变化。当通过一些手段将关联依赖解除后，这个子查询就只需要被执行一次了。

## 限制

这种改写的弊端在于，在关联没有被解除时，优化器是可以使用关联列上的索引的。也就是说，虽然这个子查询可能被重复执行多次，但是每次都可以使用索引过滤数据。而解除关联的变换上，通常是会导致关联列的位置发生改变而导致虽然子查询只被执行了一次，但是单次执行的时间会比没有解除关联时的单次执行时间长。

因此，在外部的值比较少的情况下，不解除关联依赖反而可能对执行性能更优帮助。这时可以通过[优化规则及表达式下推的黑名单](/blocklist-control-plan.md)中关闭`子查询去关联`优化规则的方式来关闭这个优化。

## 样例

{{< copyable "sql" >}}

```sql
create table t1(a int, b int);
create table t2(a int, b int, index idx(b));
explain select * from t1 where t1.a < (select sum(t2.a) from t2 where t2.b = t1.b);
```

```sql
+----------------------------------+----------+-----------+---------------+-----------------------------------------------------------------------------------------+
| id                               | estRows  | task      | access object | operator info                                                                           |
+----------------------------------+----------+-----------+---------------+-----------------------------------------------------------------------------------------+
| HashJoin_11                      | 9990.00  | root      |               | inner join, equal:[eq(test.t1.b, test.t2.b)], other cond:lt(cast(test.t1.a), Column#7)  |
| ├─HashAgg_23(Build)              | 7992.00  | root      |               | group by:test.t2.b, funcs:sum(Column#8)->Column#7, funcs:firstrow(test.t2.b)->test.t2.b |
| │ └─TableReader_24               | 7992.00  | root      |               | data:HashAgg_16                                                                         |
| │   └─HashAgg_16                 | 7992.00  | cop[tikv] |               | group by:test.t2.b, funcs:sum(test.t2.a)->Column#8                                      |
| │     └─Selection_22             | 9990.00  | cop[tikv] |               | not(isnull(test.t2.b))                                                                  |
| │       └─TableFullScan_21       | 10000.00 | cop[tikv] | table:t2      | keep order:false, stats:pseudo                                                          |
| └─TableReader_15(Probe)          | 9990.00  | root      |               | data:Selection_14                                                                       |
|   └─Selection_14                 | 9990.00  | cop[tikv] |               | not(isnull(test.t1.b))                                                                  |
|     └─TableFullScan_13           | 10000.00 | cop[tikv] | table:t1      | keep order:false, stats:pseudo                                                          |
+----------------------------------+----------+-----------+---------------+-----------------------------------------------------------------------------------------+

```

上面是优化生效的情况，可以看到 `HashJoin_11` 是一个普通的 `inner join`。

接下来，关闭关联规则：

{{< copyable "sql" >}}

```sql
insert into mysql.opt_rule_blacklist values("decorrelate");
admin reload opt_rule_blacklist;
explain select * from t1 where t1.a < (select sum(t2.a) from t2 where t2.b = t1.b);
```

```sql
+----------------------------------------+----------+-----------+------------------------+------------------------------------------------------------------------------+
| id                                     | estRows  | task      | access object          | operator info                                                                |
+----------------------------------------+----------+-----------+------------------------+------------------------------------------------------------------------------+
| Projection_10                          | 10000.00 | root      |                        | test.t1.a, test.t1.b                                                         |
| └─Apply_12                             | 10000.00 | root      |                        | CARTESIAN inner join, other cond:lt(cast(test.t1.a), Column#7)               |
|   ├─TableReader_14(Build)              | 10000.00 | root      |                        | data:TableFullScan_13                                                        |
|   │ └─TableFullScan_13                 | 10000.00 | cop[tikv] | table:t1               | keep order:false, stats:pseudo                                               |
|   └─MaxOneRow_15(Probe)                | 1.00     | root      |                        |                                                                              |
|     └─HashAgg_27                       | 1.00     | root      |                        | funcs:sum(Column#10)->Column#7                                               |
|       └─IndexLookUp_28                 | 1.00     | root      |                        |                                                                              |
|         ├─IndexRangeScan_25(Build)     | 10.00    | cop[tikv] | table:t2, index:idx(b) | range: decided by [eq(test.t2.b, test.t1.b)], keep order:false, stats:pseudo |
|         └─HashAgg_17(Probe)            | 1.00     | cop[tikv] |                        | funcs:sum(test.t2.a)->Column#10                                              |
|           └─TableRowIDScan_26          | 10.00    | cop[tikv] | table:t2               | keep order:false, stats:pseudo                                               |
+----------------------------------------+----------+-----------+------------------------+------------------------------------------------------------------------------+
```

在执行了关闭关联规则的语句后，可以在 `IndexRangeScan_25(Build)` 的 `operator info` 中看到 `range: decided by [eq(test.t2.b, test.t1.b)]`。这部分信息就是关联依赖未被解除时，TiDB 使用关联条件进行索引范围查询的显示结果。
