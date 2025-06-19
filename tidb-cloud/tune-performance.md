---
title: 分析和调优性能
summary: 了解如何分析和调优 TiDB Cloud 集群的性能。
---

# 分析和调优性能

TiDB Cloud 提供[慢查询](#slow-query)、[SQL 语句分析](#statement-analysis)、[Key Visualizer](#key-visualizer) 和 [Index Insight (beta)](#index-insight-beta) 来分析性能。

- 慢查询让你可以搜索和查看 TiDB 集群中的所有慢查询，并通过查看其执行计划、SQL 执行信息和其他详细信息来探索每个慢查询的瓶颈。

- SQL 语句分析使你能够直接在页面上观察 SQL 执行情况，无需查询系统表即可轻松定位性能问题。

- Key Visualizer 帮助你观察 TiDB 的数据访问模式和数据热点。

- Index Insight 为你提供有意义且可操作的索引建议。

> **注意：**
>
> 目前，[TiDB Cloud Serverless](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless) 集群不支持 **Key Visualizer** 和 **Index Insight (beta)**。

## 查看诊断页面

1. 在项目的 [**集群**](https://tidbcloud.com/project/clusters) 页面上，点击目标集群的名称以进入其概览页面。

    > **提示：**
    >
    > 你可以使用左上角的组合框在组织、项目和集群之间切换。

2. 在左侧导航栏中，点击 **监控** > **诊断**。

## 慢查询

默认情况下，执行时间超过 300 毫秒的 SQL 查询被视为慢查询。

要查看集群中的慢查询，请执行以下步骤：

1. 导航到集群的[**诊断**](#view-the-diagnosis-page)页面。

2. 点击**慢查询**标签页。

3. 点击列表中的任何慢查询以显示其详细执行信息。

4. （可选）你可以根据目标时间范围、相关数据库和 SQL 关键字过滤慢查询。你还可以限制要显示的慢查询数量。

结果以表格形式显示，你可以按不同列对结果进行排序。

更多信息，请参阅 [TiDB Dashboard 中的慢查询](https://docs.pingcap.com/tidb/stable/dashboard-slow-query)。

## SQL 语句分析

要使用 SQL 语句分析，请执行以下步骤：

1. 导航到集群的[**诊断**](#view-the-diagnosis-page)页面。

2. 点击 **SQL 语句**标签页。

3. 在时间间隔框中选择要分析的时间段。然后你可以获取该时间段内所有数据库的 SQL 语句执行统计信息。

4. （可选）如果你只关心某些数据库，可以在下一个框中选择相应的 schema 来过滤结果。

结果以表格形式显示，你可以按不同列对结果进行排序。

更多信息，请参阅 [TiDB Dashboard 中的 SQL 语句执行详情](https://docs.pingcap.com/tidb/stable/dashboard-statement-details)。

## Key Visualizer

> **注意：**
>
> Key Visualizer 仅适用于 [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群。

要查看键分析，请执行以下步骤：

1. 导航到集群的[**诊断**](#view-the-diagnosis-page)页面。

2. 点击 **Key Visualizer** 标签页。

在 **Key Visualizer** 页面上，一个大型热力图显示了访问流量随时间的变化。热力图每个轴的平均值显示在下方和右侧。左侧是表名、索引名和其他信息。

更多信息，请参阅 [Key Visualizer](https://docs.pingcap.com/tidb/stable/dashboard-key-visualizer)。

## Index Insight (beta)

TiDB Cloud 中的 Index Insight 功能通过为未有效利用索引的慢查询提供推荐索引，提供了强大的查询性能优化能力。

> **注意：**
>
> Index Insight 目前处于 beta 阶段，仅适用于 [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群。

更多信息，请参阅 [Index Insight](/tidb-cloud/index-insight.md)。
