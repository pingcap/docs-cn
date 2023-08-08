---
title: 逻辑优化
---

# 逻辑优化

本章节将对一些比较关键的逻辑改写进行说明，帮助大家理解 TiDB 如何生成最终的查询计划。比如在 TiDB 输入 `select * from t where t.a in (select t1.a from t1 where t1.b=t.b)` 这个查询时，在最终的执行计划中将看不到这个 `t.a in (select t1.a from t1 where t1.b=t.b)` 这个 `IN` 子查询的存在，这便是因为 TiDB 对这里进行了一些改写。

本章节会介绍如下几个关键改写：

- [子查询相关的优化](/subquery-optimization.md)
- [列裁剪](/column-pruning.md)
- [关联子查询去关联](/correlated-subquery-optimization.md)
- [Max/Min 消除](/max-min-eliminate.md)
- [谓词下推](/predicate-push-down.md)
- [分区裁剪](/partition-pruning.md)
- [TopN 和 Limit 下推](/topn-limit-push-down.md)
- [Join Reorder](/join-reorder.md)
