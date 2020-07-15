---
title: Decorrelation of Correlated Subquery
summary: Understand how to decorrelate correlated subqueries.
---

# Decorrelation of Correlated Subquery

[Subquery related optimizations](/subquery-optimization.md) describes how TiDB handles subqueries when there are no correlated columns. Because decorrelation of correlated subquery is complex, this article introduces some simple scenarios and the scope to which the optimization rule applies.

## Introduction

Take `select * from t1 where t1.a < (select sum(t2.a) from t2 where t2.b = t1.b)` as an example. The subquery `t1.a < (select sum(t2.a) from t2 where t2.b = t1.b)` here refers to the correlated column in the query condition `t2.b=t1.b`, this condition happens to be an equivalent condition, so the query can be rewritten as `select t1.* from t1, (select b, sum(a) sum_a from t2 group by b) t2 where t1.b = t2.b and t1.a < t2.sum_a;`. In this way, a correlated subquery is rewritten into `JOIN`.

The reason why TiDB needs to do this rewriting is that the correlated subquery is bound to its external query result every time the subquery is executed. In the above example, if `t1.a` has 10 million values, this subquery would repeat 10 million times, because the condition `t2.b=t1.b` varies with the value of `t1.a`. When the correlation is lifted somehow, this subquery would execute only once.

## Restrictions

The disadvantage of this rewriting is that when the correlation is not lifted, the optimizer can use the index on the correlated column. That is, although this subquery may repeat many times, the index can be used to filter data each time. After using the rewriting rule, the position of the correlated column usually changes. Although the subquery is only executed once, the single execution time would be longer than that without decorrelation.

Therefore, when there are few external values, do not perform decorrelation, because it may bring better execution performance. At present, this optimization can be disabled by setting `subquery decorrelation` optimization rules in [blocklist of optimization rules and expression pushdown](/blocklist-control-plan.md).

## Example

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

The above is an example where the optimization takes effect. `HashJoin_11` is a normal `inner join`.

Then, turn off the subquery decorrelation rules:

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

After disabling the subquery decorrelation rule, you can see `range: decided by [eq(test.t2.b, test.t1.b)]` in `operator info` of `IndexRangeScan_25(Build)`. It means that the decorrelation of correlated subquery is not performed and TiDB uses the index range query.
