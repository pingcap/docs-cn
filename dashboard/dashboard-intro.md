---
title: TiDB Dashboard 介绍
aliases: ['/docs-cn/dev/dashboard/dashboard-intro/']
---

# TiDB Dashboard 介绍

TiDB Dashboard 是 TiDB 自 4.0 版本起提供的图形化界面，可用于监控及诊断 TiDB 集群。TiDB Dashboard 内置于 TiDB 的 PD 组件中，无需独立部署。

![界面](/media/dashboard/dashboard-intro.gif)

TiDB Dashboard 在 GitHub 上[开源](https://github.com/pingcap-incubator/tidb-dashboard)。

以下列出了 TiDB Dashboard 的主要功能，可分别点击小节内的链接进一步了解详情。

## 了解集群整体运行概况

查看集群整体 QPS 数值、执行耗时、消耗资源最多的几类 SQL 语句等概况信息。

参阅[概况页面](/dashboard/dashboard-overview.md)了解详情。

## 查看组件及主机运行状态

查看整个集群中 TiDB、TiKV、PD、TiFlash 组件的运行状态及其所在主机的运行状态。

参阅[集群信息页面](/dashboard/dashboard-cluster-info.md)了解详情。

## 分析集群读写流量分布及趋势变化

通过热力图形式可视化地展示整个集群中读写流量随时间的变化情况，及时发现业务模式的变化，或定位性能不均衡的热点所在。

参阅[流量可视化页面](/dashboard/dashboard-key-visualizer.md)了解详情。

## 列出所有 SQL 查询的耗时等执行信息

列出所有 SQL 语句在集群上执行情况，了解各个阶段的执行时间、总运行次数等信息，帮助用户分析和定位集群中最消耗资源的查询，优化整体性能。

参阅 [SQL 语句分析页面](/dashboard/dashboard-statement-list.md)了解详情。

## 详细了解耗时较长的 SQL 语句的执行信息

列出所有耗时较长的 SQL 语句文本及其执行信息，帮助用户定位 SQL 语句性能缓慢或发生性能抖动的原因。

参阅[慢查询页面](/dashboard/dashboard-slow-query.md)了解详情。

## 诊断常见集群问题并生成报告

自动判断集群中是否存在一些常见的风险（如配置不一致）或问题，生成报告并给出操作建议，或对比集群在不同时间段的各个指标状态，供用户分析可能存在问题的方向。

参阅[集群诊断页面](/dashboard/dashboard-diagnostics-access.md)了解详情。

## 查询所有组件日志

按关键字、时间范围等条件快速搜索集群中所有运行实例的日志，并可打包下载到本地。

参阅[日志搜索页面](/dashboard/dashboard-log-search.md)了解详情。

## 收集分析各个组件的性能数据

高级调试功能：无需第三方工具，在线地对各个组件进行性能分析，剖析组件实例在分析时间段内执行的各种内部操作及比例。

参阅[实例性能分析页面](/dashboard/dashboard-profiling.md)了解详情。

> **注意：**
>
> TiDB Dashboard 默认会收集使用情况信息，并将这些信息分享给 PingCAP 用于改善产品。若要了解所收集的信息详情及如何禁用该行为，请参见[遥测](/telemetry.md)。
