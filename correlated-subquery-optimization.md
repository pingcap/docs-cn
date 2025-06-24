---
title: 相关子查询去关联化
summary: 了解如何对相关子查询进行去关联化。
---

# 相关子查询去关联化

[子查询相关优化](/subquery-optimization.md)描述了 TiDB 如何处理没有相关列的子查询。由于相关子查询的去关联化比较复杂，本文介绍一些简单的场景以及优化规则的适用范围。

## 简介

以 `select * from t1 where t1.a < (select sum(t2.a) from t2 where t2.b = t1.b)` 为例。这里的子查询 `t1.a < (select sum(t2.a) from t2 where t2.b = t1.b)` 在查询条件 `t2.b=t1.b` 中引用了相关列，这个条件恰好是一个等价条件，所以可以将查询重写为 `select t1.* from t1, (select b, sum(a) sum_a from t2 group by b) t2 where t1.b = t2.b and t1.a < t2.sum_a;`。通过这种方式，相关子查询被重写为 `JOIN`。

TiDB 需要进行这种重写的原因是，相关子查询每次执行时都会绑定到其外部查询结果。在上面的例子中，如果 `t1.a` 有 1000 万个值，这个子查询就会重复 1000 万次，因为条件 `t2.b=t1.b` 会随着 `t1.a` 的值而变化。当以某种方式去除关联后，这个子查询只需执行一次。

## 限制

这种重写的缺点是，当关联没有被去除时，优化器可以使用相关列上的索引。也就是说，虽然这个子查询可能重复多次，但每次都可以使用索引来过滤数据。使用重写规则后，相关列的位置通常会发生变化。虽然子查询只执行一次，但单次执行时间可能会比不去关联化时更长。

因此，当外部值较少时，不执行去关联化可能会带来更好的执行性能。在这种情况下，您可以使用 [`NO_DECORRELATE`](/optimizer-hints.md#no_decorrelate) 优化器提示或在[优化规则和表达式下推的黑名单](/blocklist-control-plan.md)中禁用"子查询去关联化"优化规则。在大多数情况下，建议将优化器提示与 [SQL 计划管理](/sql-plan-management.md)结合使用来禁用去关联化。

## 示例

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

上面是优化生效的示例。`HashJoin_11` 是一个普通的 `inner join`。

然后，您可以使用 `NO_DECORRELATE` 优化器提示来告诉优化器不要对子查询进行去关联化：

{{< copyable "sql" >}}

```sql
explain select * from t1 where t1.a < (select /*+ NO_DECORRELATE() */ sum(t2.a) from t2 where t2.b = t1.b);
```

```sql
+------------------------------------------+-----------+-----------+------------------------+--------------------------------------------------------------------------------------+
| id                                       | estRows   | task      | access object          | operator info                                                                        |
+------------------------------------------+-----------+-----------+------------------------+--------------------------------------------------------------------------------------+
| Projection_10                            | 10000.00  | root      |                        | test.t1.a, test.t1.b                                                                 |
| └─Apply_12                               | 10000.00  | root      |                        | CARTESIAN inner join, other cond:lt(cast(test.t1.a, decimal(10,0) BINARY), Column#7) |
|   ├─TableReader_14(Build)                | 10000.00  | root      |                        | data:TableFullScan_13                                                                |
|   │ └─TableFullScan_13                   | 10000.00  | cop[tikv] | table:t1               | keep order:false, stats:pseudo                                                       |
|   └─MaxOneRow_15(Probe)                  | 10000.00  | root      |                        |                                                                                      |
|     └─StreamAgg_20                       | 10000.00  | root      |                        | funcs:sum(Column#14)->Column#7                                                       |
|       └─Projection_45                    | 100000.00 | root      |                        | cast(test.t2.a, decimal(10,0) BINARY)->Column#14                                     |
|         └─IndexLookUp_44                 | 100000.00 | root      |                        |                                                                                      |
|           ├─IndexRangeScan_42(Build)     | 100000.00 | cop[tikv] | table:t2, index:idx(b) | range: decided by [eq(test.t2.b, test.t1.b)], keep order:false, stats:pseudo         |
|           └─TableRowIDScan_43(Probe)     | 100000.00 | cop[tikv] | table:t2               | keep order:false, stats:pseudo                                                       |
+------------------------------------------+-----------+-----------+------------------------+--------------------------------------------------------------------------------------+
```

禁用去关联化规则也可以达到相同的效果：

{{< copyable "sql" >}}

```sql
insert into mysql.opt_rule_blacklist values("decorrelate");
admin reload opt_rule_blacklist;
explain select * from t1 where t1.a < (select sum(t2.a) from t2 where t2.b = t1.b);
```

```sql
+------------------------------------------+-----------+-----------+------------------------+--------------------------------------------------------------------------------------+
| id                                       | estRows   | task      | access object          | operator info                                                                        |
+------------------------------------------+-----------+-----------+------------------------+--------------------------------------------------------------------------------------+
| Projection_10                            | 10000.00  | root      |                        | test.t1.a, test.t1.b                                                                 |
| └─Apply_12                               | 10000.00  | root      |                        | CARTESIAN inner join, other cond:lt(cast(test.t1.a, decimal(10,0) BINARY), Column#7) |
|   ├─TableReader_14(Build)                | 10000.00  | root      |                        | data:TableFullScan_13                                                                |
|   │ └─TableFullScan_13                   | 10000.00  | cop[tikv] | table:t1               | keep order:false, stats:pseudo                                                       |
|   └─MaxOneRow_15(Probe)                  | 10000.00  | root      |                        |                                                                                      |
|     └─StreamAgg_20                       | 10000.00  | root      |                        | funcs:sum(Column#14)->Column#7                                                       |
|       └─Projection_45                    | 100000.00 | root      |                        | cast(test.t2.a, decimal(10,0) BINARY)->Column#14                                     |
|         └─IndexLookUp_44                 | 100000.00 | root      |                        |                                                                                      |
|           ├─IndexRangeScan_42(Build)     | 100000.00 | cop[tikv] | table:t2, index:idx(b) | range: decided by [eq(test.t2.b, test.t1.b)], keep order:false, stats:pseudo         |
|           └─TableRowIDScan_43(Probe)     | 100000.00 | cop[tikv] | table:t2               | keep order:false, stats:pseudo                                                       |
+------------------------------------------+-----------+-----------+------------------------+--------------------------------------------------------------------------------------+
```

禁用子查询去关联化规则后，您可以在 `IndexRangeScan_42(Build)` 的 `operator info` 中看到 `range: decided by [eq(test.t2.b, test.t1.b)]`。这意味着没有执行相关子查询的去关联化，TiDB 使用了索引范围查询。
