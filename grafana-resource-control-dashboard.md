---
title: 资源管控 (Resource Control) 监控指标详解
summary: 了解资源管控 (Resource Control) 的 Grafana Dashboard 中所展示的关键指标。
---

# 资源管控 (Resource Control) 监控指标详解

使用 TiUP 部署 TiDB 集群时，可以一键部署监控系统 (Prometheus & Grafana)。监控架构请参见 [TiDB 监控框架概述](/tidb-monitoring-framework.md)。

目前 Grafana Dashboard 整体分为 PD、TiDB、TiKV、Node_exporter、Overview、Performance_overview 等。

如果你的集群配置了 [Resource Control](/tidb-resource-control.md) ，通过观察 Resource Control 面板上的 Metrics，你可以了解当前集群整体的资源消耗状态。

以下为 **Resource Control** 关键监控指标的说明。

## Request Unit 相关指标

- RU：以 Resource Group 为单位进行实时统计的 [Request Unit (RU)](/tidb-resource-control.md#什么是-request-unit-ru) 消耗信息。`total` 为当前所有 Resource Group 消耗的 Request Unit 之和。每个 Resource Group 的 Request Unit 消耗等于其读消耗 (Read Request Unit) 和写消耗 (Write Request Unit) 之和。
- RU Per Query：平均每个 SQL 语句消耗的 Request Unit 数量。计算方法是将前述 Request Unit 监控指标除以当前每秒执行的 SQL 语句数量。
- RRU：以 Resource Group 为单位进行实时统计的读请求 Read Request Unit 消耗信息。`total` 为当前所有 Resource Group 消耗的 Read Request Unit 之和。
- RRU Per Query：平均每个 SQL 语句消耗的 Read Request Unit 数量。计算方法是将前述 Read Request Unit 监控指标除以当前每秒执行的 SQL 语句数量。
- WRU：以 Resource Group 为单位进行实时统计的写请求 Write Request Unit 消耗信息。`total` 为当前所有 Resource Group 消耗的 Write Request Unit 之和。
- WRU Per Query：平均每个 SQL 语句消耗的 Write Request Unit 数量。计算方法是将前述 Write Request Unit 监控指标除以当前每秒执行的 SQL 语句数量。

## 资源相关指标

- KV Request Count：以 Resource Group 为单位进行实时统计的 KV 请求数量，区分了读和写两种类型。`total` 为当前所有 Resource Group 涉及的 KV 请求数量之和。
- KV Request Count Per Query：平均每个 SQL 语句涉及的读写 KV 请求数量。计算方法是将前述 KV Request Count 监控指标除以当前每秒执行的 SQL 语句数量。
- Bytes Read：以 Resource Group 为单位进行实时统计的读取数据量。`total` 为当前所有 Resource Group 读取数据量之和。
- Bytes Read Per Query：平均每个 SQL 语句的读取数据量。将前述 Bytes Read 监控指标除以当前每秒执行的 SQL 语句数量。
- Bytes Written：以 Resource Group 为单位进行实时统计的写入数据量。`total` 为当前所有 Resource Group 写入数据量之和。
- Bytes Written Per Query：平均每个 SQL 语句的写入数据量。计算方法是将前述 Bytes Written 监控指标除以当前每秒执行的 SQL 语句数量。
- KV CPU Time：以 Resource Group 为单位进行实时统计的 KV 层 CPU 时间消耗。`total` 为当前所有 Resource Group 消耗 KV 层 CPU 时间之和。
- KV CPU Time Per Query：平均每个 SQL 语句的 KV 层 CPU 时间消耗之和。计算方法是将前述 KV CPU Time 监控指标除以当前每秒执行的 SQL 语句数量。
- SQL CPU Time：以 Resource Group 为单位进行实时统计的 SQL 层 CPU 时间消耗。`total` 为当前所有 Resource Group 消耗 SQL 层 CPU 时间之和。
- SQL CPU Time Per Query：平均每个 SQL 语句的 SQL 层 CPU 时间消耗之和。计算方法是将前述 SQL CPU Time 监控除以当前每秒执行的 SQL 语句数量。
