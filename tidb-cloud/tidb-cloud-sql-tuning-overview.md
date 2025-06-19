---
title: SQL 调优概述
summary: 了解如何在 TiDB Cloud 中调优 SQL 性能。
---

# SQL 调优概述

本文介绍如何在 TiDB Cloud 中调优 SQL 性能。要获得最佳的 SQL 性能，您可以执行以下操作：

- 调优 SQL 性能。有许多方法可以优化 SQL 性能，例如分析查询语句、优化执行计划和优化全表扫描。
- 优化模式设计。根据您的业务工作负载类型，您可能需要优化模式以避免事务冲突或热点。

## 调优 SQL 性能

要提高 SQL 语句的性能，请考虑以下原则。

- 最小化扫描数据的范围。最佳实践始终是只扫描最小范围的数据，避免扫描所有数据。
- 使用适当的索引。对于 SQL 语句中 `WHERE` 子句中的每个列，确保有相应的索引。否则，`WHERE` 子句将扫描全表并导致性能不佳。
- 使用适当的连接类型。根据查询中每个表的大小和相关性，选择正确的连接类型非常重要。通常，TiDB 中的基于成本的优化器会自动选择最优的连接类型。但是，在某些情况下，您可能需要手动指定连接类型。详情请参见[解释使用连接的语句](/explain-joins.md)。
- 使用适当的存储引擎。对于混合事务和分析处理（HTAP）工作负载，建议使用 TiFlash 存储引擎。请参见 [HTAP 查询](/develop/dev-guide-hybrid-oltp-and-olap-queries.md)。

TiDB Cloud 提供了几个工具来帮助您分析集群上的慢查询。以下部分描述了优化慢查询的几种方法。

### 使用诊断页面上的 Statement

TiDB Cloud 控制台在[**诊断**](/tidb-cloud/tune-performance.md#view-the-diagnosis-page)页面上提供了 [**SQL Statement**](/tidb-cloud/tune-performance.md#statement-analysis) 标签页。它收集集群上所有数据库的 SQL 语句的执行统计信息。您可以使用它来识别和分析总执行时间或单次执行时间较长的 SQL 语句。

请注意，在此页面上，具有相同结构的 SQL 查询（即使查询参数不匹配）会被归类为同一个 SQL 语句。例如，`SELECT * FROM employee WHERE id IN (1, 2, 3)` 和 `select * from EMPLOYEE where ID in (4, 5)` 都属于同一个 SQL 语句 `select * from employee where id in (...)`。

您可以在 **SQL Statement** 中查看一些关键信息。

- **SQL 模板**：包括 SQL 摘要、SQL 模板 ID、当前查看的时间范围、执行计划数量和执行所在的数据库。

    ![Details0](/media/dashboard/dashboard-statement-detail0.png)

- 执行计划列表：如果一个 SQL 语句有多个执行计划，则显示列表。您可以选择不同的执行计划，所选执行计划的详细信息将显示在列表底部。如果只有一个执行计划，则不会显示列表。

    ![Details1](/media/dashboard/dashboard-statement-detail1.png)

- 执行计划详情：显示所选执行计划的详细信息。它从多个角度收集每种 SQL 类型的执行计划和相应的执行时间，以帮助您获取更多信息。请参见[执行计划](https://docs.pingcap.com/tidb/stable/dashboard-statement-details#execution-plans)。

    ![Details2](/media/dashboard/dashboard-statement-detail2.png)

- 相关慢查询

除了 **Statement** 仪表板中的信息外，以下部分还描述了一些 TiDB Cloud 的 SQL 最佳实践。

### 检查执行计划

您可以使用 [`EXPLAIN`](/explain-overview.md) 检查 TiDB 在编译期间为语句计算的执行计划。换句话说，TiDB 估算数百或数千种可能的执行计划，并选择一个消耗最少资源且执行最快的最优执行计划。

如果 TiDB 选择的执行计划不是最优的，您可以使用 EXPLAIN 或 [`EXPLAIN ANALYZE`](/sql-statements/sql-statement-explain-analyze.md) 进行诊断。

### 优化执行计划

在通过 `parser` 解析原始查询文本并进行基本有效性验证后，TiDB 首先对查询进行一些逻辑等价变换。更多信息，请参见 [SQL 逻辑优化](/sql-logical-optimization.md)。

通过这些等价变换，查询在逻辑执行计划中可能变得更容易处理。等价变换后，TiDB 获得一个与原始查询等价的查询计划结构，然后根据数据分布和运算符的具体执行开销获得最终的执行计划。更多信息，请参见 [SQL 物理优化](/sql-physical-optimization.md)。

此外，TiDB 可以选择启用执行计划缓存，以在执行 `PREPARE` 语句时减少执行计划的创建开销，如[预处理执行计划缓存](/sql-prepared-plan-cache.md)中所介绍。

### 优化全表扫描

慢 SQL 查询最常见的原因是 `SELECT` 语句执行全表扫描或使用了错误的索引。您可以使用 EXPLAIN 或 EXPLAIN ANALYZE 查看查询的执行计划并找出执行慢的原因。有[三种方法](/develop/dev-guide-optimize-sql.md)可以进行优化。

- 使用二级索引
- 使用覆盖索引
- 使用主键索引

### DML 最佳实践

请参见 [DML 最佳实践](/develop/dev-guide-optimize-sql-best-practices.md#dml-最佳实践)。

### 选择主键时的 DDL 最佳实践

请参见[选择主键时需要遵循的准则](/develop/dev-guide-create-table.md#选择主键时需要遵循的准则)。

### 索引最佳实践

[索引最佳实践](/develop/dev-guide-index-best-practice.md)包括创建索引和使用索引的最佳实践。

创建索引的速度默认是保守的，在某些场景下可以通过[修改变量](/develop/dev-guide-optimize-sql-best-practices.md#添加索引最佳实践)来加快索引创建过程。

<!--
### 使用慢日志内存映射表

您可以通过查询 [INFORMATION_SCHEMA.SLOW_QUERY](/identify-slow-queries.md#慢日志中的内存映射) 表来查询慢查询日志的内容，并在 [`SLOW_QUERY`](/information-schema/information-schema-slow-query.md) 表中找到结构。使用此表，您可以使用不同的字段执行查询以找出潜在问题。

推荐的慢查询分析过程如下。

1. [识别查询的性能瓶颈](/analyze-slow-queries.md#识别查询的性能瓶颈)。即识别查询过程中耗时较长的部分。
2. [分析系统问题](/analyze-slow-queries.md#分析系统问题)。根据瓶颈点，结合当时的监控、日志等信息找出可能的原因。
3. [分析优化器问题](/analyze-slow-queries.md#分析优化器问题)。分析是否存在更好的执行计划。
-->

## 优化模式设计

如果基于 SQL 性能调优仍然无法获得更好的性能，您可能需要检查您的模式设计和数据读取模型，以避免事务冲突和热点。

### 事务冲突

有关如何定位和解决事务冲突的更多信息，请参见[排查锁冲突问题](https://docs.pingcap.com/tidb/stable/troubleshoot-lock-conflicts#排查锁冲突问题)。

### 热点问题

您可以使用 [Key Visualizer](/tidb-cloud/tune-performance.md#key-visualizer) 分析热点问题。

您可以使用 Key Visualizer 分析 TiDB 集群的使用模式并排查流量热点。此页面提供了 TiDB 集群随时间变化的流量的可视化表示。

您可以在 Key Visualizer 中观察以下信息。您可能需要先了解一些[基本概念](https://docs.pingcap.com/tidb/stable/dashboard-key-visualizer#基本概念)。

- 显示整体流量随时间变化的大型热力图
- 热力图上某个坐标的详细信息
- 左侧显示的表和索引等标识信息

在 Key Visualizer 中，有[四种常见的热力图结果](https://docs.pingcap.com/tidb/stable/dashboard-key-visualizer#常见热力图类型)。

- 均匀分布的工作负载：理想结果
- X 轴（时间）上明暗交替：需要检查高峰时期的资源
- Y 轴上明暗交替：需要检查生成的热点聚集程度
- 明亮的对角线：需要检查业务模型

在 X 轴和 Y 轴明暗交替的情况下，都需要解决读写压力。

有关 SQL 性能优化的更多信息，请参见 SQL 常见问题中的 [SQL 优化](https://docs.pingcap.com/tidb/stable/sql-faq#sql-优化)。
