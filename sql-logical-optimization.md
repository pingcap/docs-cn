---
title: SQL Logical Optimization
---

# SQL Logical Optimization

This chapter explains some key logic rewrites to help you understand how TiDB generates the final query plan. For example, when you execute the `select * from t where t.a in (select * from t1 where t1.b=t.b)` query in TiDB, you will find that the `IN` sub-query `t.a in (select t1.a from t1 where t1.b=t.b` does not exist because TiDB has made some rewrites here.

This chapter introduces the following key rewrites:

- [Subquery Related Optimizations](/subquery-optimization.md)
- [Column Pruning](/column-pruning.md)
- [Decorrelation of Correlated Subquery](/correlated-subquery-optimization.md)
- [Eliminate Max/Min](/max-min-eliminate.md)
- [Predicates Push Down](/predicate-push-down.md)
- [Partition Pruning](/partition-pruning.md)
- [TopN and Limit Operator Push Down](/topn-limit-push-down.md)
- [Join Reorder](/join-reorder.md)