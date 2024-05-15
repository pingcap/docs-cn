---
title: 概览
summary: 介绍 TiDB 的 SQL 性能调优概览。
---

# 概览

本章内容描述了如何在 TiDB 中优化 SQL 语句的性能。为了获得更好的性能，你可以从以下方面入手：

- SQL 性能调优。
- Schema 设计：根据你的业务负载类型，为了避免事务冲突或者是热点，你可能需要对表的 Schema 做出一些调整。

## SQL 性能调优

为了让 SQL 语句的性能更好，可以遵循以下原则：

- 扫描的数据越少越好，最好能只扫描需要的数据，避免扫描多余的数据。
- 使用合适的索引，对于 SQL 中的 `WHERE` 子句中的 Column，需要保证有相应索引，否则这将是一个全表扫的语句，性能会很差。
- 使用合适的 Join 类型。根据查询中各个表的大小和关联性，选择合适的 Join 类型也会非常重要。一般情况下，TiDB 的 cost-based 优化器会自动选择最优的 Join 类型。但在少数情况下，用户手动指定 Join 类型可能会更好。
- 使用合适的存储引擎。对于 OLTP 和 OLAP 混合类型的负载，推荐使用 TiFlash 查询引擎，具体可以参考 [HTAP 查询](/develop/dev-guide-hybrid-oltp-and-olap-queries.md)。

## Schema 设计

如果根据[SQL 性能调优](#sql-性能调优)调优后任然无法获得较好的性能，你可能需要检查你的 Schema 设计和数据读取模型，来确保避免以下问题：

- 事务冲突。关于如何定位和解决事务冲突，请参考[TiDB 锁冲突问题处理](/troubleshoot-lock-conflicts.md)。
- 热点。关于如何定位和解决热点，请参考[TiDB 热点问题处理](/troubleshoot-hot-spot-issues.md)。

## 推荐阅读

- [SQL 性能调优](/sql-tuning-overview.md)。
