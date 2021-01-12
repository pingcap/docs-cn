---
title: SQL 性能调优
aliases: ['/docs-cn/dev/sql-tuning-overview/']
---

# SQL 性能调优

SQL 是一种声明性语言。一条 SQL 语句描述的是最终结果应该如何，而非按顺序执行的步骤。TiDB 会优化 SQL 语句的执行，语义上允许以任何顺序执行查询的各部分，前提是能正确返回语句所描述的最终结果。

SQL 性能优化的过程，可以理解为 GPS 导航的过程。你提供地址后，GPS 软件利用各种统计信息（例如以前的行程、速度限制等元数据，以及实时交通信息）规划出一条最省时的路线。这与 TiDB 中的 SQL 性能优化过程相对应。

本章节包括以下文档，可帮助你更好地理解查询执行计划：

- [理解 TiDB 执行计划](/explain-overview.md)介绍如何使用 `EXPLAIN` 语句来理解 TiDB 是如何执行某个查询的。
- [SQL 优化流程概览](/sql-optimization-concepts.md)介绍 TiDB 可以使用的几种优化，以提高查询性能。
- [控制执行计划](/control-execution-plan.md)介绍如何控制执行计划的生成。TiDB 的执行计划非最优时，建议控制执行计划。
