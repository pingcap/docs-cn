---
title: SQL 优化过程
summary: 了解 TiDB 中 SQL 的逻辑优化和物理优化。
---

# SQL 优化过程

在 TiDB 中，从输入查询到根据最终执行计划获得执行结果的过程如下图所示：

![SQL 优化过程](/media/sql-optimization.png)

在通过 `parser` 解析原始查询文本并进行一些简单的有效性检查后，TiDB 首先对查询进行一些逻辑等价的变换。有关详细变换，请参见 [SQL 逻辑优化](/sql-logical-optimization.md)。

通过这些等价变换，该查询在逻辑执行计划中变得更容易处理。完成等价变换后，TiDB 获得一个与原始查询等价的查询计划结构，然后基于数据分布和操作符的具体执行成本获得最终的执行计划。有关详细信息，请参见 [SQL 物理优化](/sql-physical-optimization.md)。

同时，当 TiDB 执行 [`PREPARE`](/sql-statements/sql-statement-prepare.md) 语句时，您可以选择启用缓存以减少在 TiDB 中生成执行计划的成本。有关详细信息，请参见[执行计划缓存](/sql-prepared-plan-cache.md)。
