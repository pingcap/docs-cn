---
title: 逻辑优化
category: performance
---

# 逻辑优化

在这个章节中，我们会对一些比较关键的逻辑改写进行一些说明。来方便大家能够更好的理解 TiDB 如何生成最终的查询计划。比如当我们向 TiDB 输入 `select * from t where t.a in (select * from t1 where t1.b=t.b)` 这个查询时，我们会在最终的执行计划中看不到这个 `t.a in (select t1.a from t1 where t1.b=t.b` 这个 `IN` 子查询的存在。这便是因为 TiDB 对这里进行了一些改写。这个章节会介绍如下的几个关键改写：

- [子查询相关的优化](/subquery-optimization.md)
- [列裁剪](/column-pruning.md)
- [关联子查询去关联](/correlated-subquery-optimization.md)
- [Max/Min 消除](/max-min-eliminate.md)
- [谓词下推](/predicate-push-down.md)
- [分区裁剪](/partition-pruning.md)
- [TopN 和 Limit 下推](/topn-limit-push-down.md)
- [Join Reorder](/join-reorder.md)