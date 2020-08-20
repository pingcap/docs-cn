---
title: SQL 性能调优
aliases: ['/docs-cn/dev/sql-tuning-overview/']
---

# SQL 性能调优

在上一章节”故障诊断“中，介绍了可以通过一些手段定位到对集群造成影响的一些查询，或是 DBA 主动发现某些查询的执行时间不符合原本的预期，这时就需要对查询的执行情况进行分析。在本章中主要有以下三个部分，介绍了如何针对一个具体的查询进行调优：

- 第一部分[理解 TiDB 执行计划](/query-execution-plan.md)中，会介绍如何使用 `EXPLAIN` 以及 `EXPLAIN ANALYZE` 语句来理解 TiDB 是如何执行某个查询的。
- 第二部分[SQL 优化流程简介](/sql-optimization-concepts.md)中，会介绍 TiDB 内部会使用的优化，其中会涉及一些等价的 SQL 变换以及物理计划的选择，来方便读者理解 TiDB 是如何生成最终的执行计划的。
- 第三部分[控制执行计划](/control-execution-plan.md)中，会介绍如何通过一些手段来控制执行计划的生成来提升查询的执行速度，减少它对集群整体性能或者业务的影响情况。
