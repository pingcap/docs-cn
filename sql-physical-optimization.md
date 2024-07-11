---
title: 物理优化
aliases: ['/docs-cn/dev/sql-physical-optimization/']
summary: 物理优化是基于代价的优化，为逻辑执行计划制定物理执行计划。优化器根据数据统计信息选择时间复杂度、资源消耗和物理属性最小的物理执行计划。TiDB 执行计划文档介绍了索引选择、统计信息、错误索引解决方案、Distinct 优化和代价模型。
---

# 物理优化

物理优化是基于代价的优化，为上一阶段产生的逻辑执行计划制定物理执行计划。这一阶段中，优化器会为逻辑执行计划中的每个算子选择具体的物理实现。逻辑算子的不同物理实现有着不同的时间复杂度、资源消耗和物理属性等。在这个过程中，优化器会根据数据的统计信息来确定不同物理实现的代价，并选择整体代价最小的物理执行计划。

[理解 TiDB 执行计划](/explain-overview.md)文档中对每个物理算子进行了一些介绍，本章节重点介绍以下方面：

- [索引的选择](/choose-index.md)：介绍在一张表有多个索引时，TiDB 如何选择最优的索引来访问表。
- [常规统计信息](/statistics.md)：介绍 TiDB 收集了哪些常规统计信息来获得表的数据分布情况。
- [扩展统计信息](/extended-statistics.md)：介绍如何使用扩展统计信息指导优化器。
- [错误索引的解决方案](/wrong-index-solution.md)：介绍当发现 TiDB 索引选错时，你应该使用哪些手段使其使用正确的索引。
- [Distinct 优化](/agg-distinct-optimization.md)：介绍有关 `DISTINCT` 关键字的优化，包括其优缺点以及如何使用它。
- [代价模型](/cost-model.md)：介绍在物理优化时，TiDB 怎么通过代价模型来选择一个最优的执行计划。
- [Runtime Filter](/runtime-filter.md)：介绍如何通过动态生成 Filter 提升 MPP 场景下 Hash Join 的性能。