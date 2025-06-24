---
title: TiDB Cloud 诊所
summary: 了解如何使用 TiDB Cloud 诊所进行高级监控和诊断。
---

# TiDB Cloud 诊所

TiDB Cloud 诊所在 TiDB Cloud 上提供高级监控和诊断功能，旨在帮助您通过详细分析和可操作的见解，快速识别性能问题、优化数据库并提升整体性能。

![tidb-cloud-clinic](/media/tidb-cloud/tidb-cloud-clinic.png)

> **注意：**
>
> 目前，TiDB Cloud 诊所仅适用于 [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群。

## 前提条件

TiDB Cloud 诊所仅适用于订阅了**企业版**或**高级版**支持计划的组织。

## 查看集群页面

要查看**集群**页面，请按照以下步骤操作：

1. 登录 [TiDB Cloud 诊所控制台](https://clinic.pingcap.com/)，选择**使用 TiDB 账号继续**进入 TiDB Cloud 登录页面。

2. 从组织列表中选择目标组织。将显示所选项目中的集群。

3. 点击目标集群的名称。将显示集群概览页面，您可以在此查看集群的详细信息，包括：

    - 高级指标
    - 慢查询排行（仅支持 TiDB 版本为 v8.1.1 或更高版本，v7.5.4 或更高版本的集群）
    - TopSQL（仅支持 TiDB 版本为 v8.1.1 或更高版本，v7.5.4 或更高版本的集群）
    - 基准测试报告

## 监控高级指标

TiDB Cloud 诊所使用 Grafana 为 TiDB 集群提供全面的指标集。高级指标的保留策略为 90 天。

要查看指标仪表板，请按照以下步骤操作：

1. 在 [TiDB Cloud 诊所控制台](https://clinic.pingcap.com/)中，导航到集群的**集群**页面。

2. 点击**指标**。

3. 点击您想要查看的仪表板名称。将显示该仪表板。

仪表板及其内容可能会发生变化。目前提供以下仪表板：

- Backup & Import
- DM-Professional
- DM-Standard
- Lightning
- Performance-Overview
- TiCDC-Summary
- TiDB
- TiDB-Resource-Control
- TiFlash-Summary
- TiKV-Details
- User-Node-Info

## 分析慢查询排行

默认情况下，执行时间超过 300 毫秒的 SQL 查询被视为慢查询。

在 TiDB Cloud 控制台的默认[**慢查询**](/tidb-cloud/tune-performance.md#slow-query)页面上，特别是在具有大量慢查询的集群中，识别影响性能的查询可能比较困难。TiDB Cloud 诊所中的**慢查询排行**功能基于慢查询日志提供聚合分析。通过此功能，您可以轻松定位存在性能问题的查询，将整体性能调优时间至少减少一半。

慢查询排行按 SQL 指纹聚合显示前 10 个查询，并按以下维度排序：

- 总延迟
- 最大延迟
- 平均延迟
- 总内存
- 最大内存
- 平均内存
- 总次数

要查看集群中的慢查询，请按照以下步骤操作：

1. 在 [TiDB Cloud 诊所控制台](https://clinic.pingcap.com/)中，导航到集群的**集群**页面。

2. 点击**慢查询**。

3. 慢查询排行将以表格形式显示。您可以按不同列进行排序。

4. （可选）点击列表中的任何慢查询以查看其详细执行信息。

5. （可选）按时间范围、数据库或语句类型筛选慢查询。

慢查询的保留策略为 7 天。

更多信息，请参阅 [TiDB Dashboard 中的慢查询](https://docs.pingcap.com/tidb/stable/dashboard-slow-query)。

## 监控 TopSQL

TiDB Cloud 诊所提供 TopSQL 信息，使您能够实时监控和可视化探索数据库中每个 SQL 语句的 CPU 开销。这有助于您优化和解决数据库性能问题。

要查看 TopSQL，请按照以下步骤操作：

1. 在 [TiDB Cloud 诊所控制台](https://clinic.pingcap.com/)中，导航到集群的**集群**页面。

2. 点击 **TopSQL**。

3. 选择特定的 TiDB 或 TiKV 实例以观察其负载。您可以使用时间选择器或在图表中选择时间范围来细化分析。

4. 分析 TopSQL 显示的图表和表格。

更多信息，请参阅 [TiDB Dashboard 中的 TopSQL](https://docs.pingcap.com/tidb/stable/top-sql)。

## 生成基准测试报告

**基准测试报告**功能帮助您在性能测试期间识别 TiDB 集群中的性能问题。完成压力测试后，您可以生成基准测试报告来分析集群的性能。该报告突出显示已识别的瓶颈并提供优化建议。应用这些建议后，您可以运行另一轮压力测试并生成新的基准测试报告以比较性能改进。

要生成基准测试报告，请按照以下步骤操作：

1. 在 [TiDB Cloud 诊所控制台](https://clinic.pingcap.com/)中，导航到集群的**集群**页面。

2. 点击**基准测试报告**。

3. 选择要在基准测试报告中分析的时间范围。

4. 点击**创建报告**以生成基准测试报告。

5. 等待报告生成完成。报告准备就绪后，点击**查看**以打开报告。
