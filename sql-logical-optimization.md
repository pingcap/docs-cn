---
title: SQL 逻辑优化
summary: SQL 逻辑优化章节解释了 TiDB 查询计划生成中的关键逻辑重写。例如，由于 TiDB 的重写，`IN` 子查询 `t.a in (select t1.a from t1 where t1.b=t.b)` 不会存在。关键重写包括子查询相关优化、列裁剪、相关子查询去关联化、消除 Max/Min、谓词下推、分区裁剪、TopN 和 Limit 算子下推以及连接重排序。
---

# SQL 逻辑优化

本章节解释了一些关键的逻辑重写，帮助您理解 TiDB 如何生成最终的查询计划。例如，当您在 TiDB 中执行 `select * from t where t.a in (select t1.a from t1 where t1.b=t.b)` 查询时，您会发现 `IN` 子查询 `t.a in (select t1.a from t1 where t1.b=t.b)` 不存在，这是因为 TiDB 在这里进行了一些重写。

本章节介绍以下关键重写：

- [子查询相关优化](/subquery-optimization.md)
- [列裁剪](/column-pruning.md)
- [相关子查询去关联化](/correlated-subquery-optimization.md)
- [消除 Max/Min](/max-min-eliminate.md)
- [谓词下推](/predicate-push-down.md)
- [分区裁剪](/partition-pruning.md)
- [TopN 和 Limit 算子下推](/topn-limit-push-down.md)
- [连接重排序](/join-reorder.md)
- [从窗口函数中推导 TopN 或 Limit](/derive-topn-from-window.md)
