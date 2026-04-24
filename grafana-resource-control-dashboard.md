---
title: 资源管控 (Resource Control) 监控指标详解
summary: 了解资源管控 (Resource Control) 的 Grafana Dashboard 中所展示的关键指标。
---

# 资源管控 (Resource Control) 监控指标详解

使用 TiUP 部署 TiDB 集群时，可以一键部署监控系统 (Prometheus & Grafana)。监控架构请参见 [TiDB 监控框架概述](/tidb-monitoring-framework.md)。

目前 Grafana Dashboard 整体分为 PD、TiDB、TiKV、Node_exporter、Overview、Performance_overview 等。

如果你的集群配置了 [Resource Control](/tidb-resource-control-ru-groups.md) ，通过观察 Resource Control 面板上的 Metrics，你可以了解当前集群整体的资源消耗状态。

TiDB 使用[令牌桶算法](https://en.wikipedia.org/wiki/Token_bucket)做流控，正如资源管控实现机制 ([RFC: Global Resource Control in TiDB](https://github.com/pingcap/tidb/blob/master/docs/design/2022-11-25-global-resource-control.md#distributed-token-buckets)) 中所描述：一个 TiDB 节点可能存在多个 Resource Group（资源组），将在 PD 端的 GAC（Global Admission Control）进行流控。每个 TiDB 节点中的本地令牌桶（Local Token Buckets）将定期（默认 5 秒）与 PD 端的 GAC 进行通信，以重新配置本地令牌。其中的本地令牌桶（Local Token Buckets）具体实现为 Resource Controller Client。

以下为 **Resource Control** 关键监控指标的说明。

## Request Unit 相关指标

- RU：以 Resource Group（资源组）为单位进行实时统计的 [Request Unit (RU)](/tidb-resource-control-ru-groups.md#什么是-request-unit-ru) 消耗信息。`total` 为当前所有 Resource Group 消耗的 Request Unit 之和。每个 Resource Group 的 Request Unit 消耗等于其读消耗 (Read Request Unit) 和写消耗 (Write Request Unit) 之和。
- RU Per Query：平均每个 SQL 语句消耗的 Request Unit 数量。计算方法是将前述 Request Unit 监控指标除以当前每秒执行的 SQL 语句数量。
- RRU：以 Resource Group 为单位进行实时统计的读请求 Read Request Unit 消耗信息。`total` 为当前所有 Resource Group 消耗的 Read Request Unit 之和。
- RRU Per Query：平均每个 SQL 语句消耗的 Read Request Unit 数量。计算方法是将前述 Read Request Unit 监控指标除以当前每秒执行的 SQL 语句数量。
- WRU：以 Resource Group 为单位进行实时统计的写请求 Write Request Unit 消耗信息。`total` 为当前所有 Resource Group 消耗的 Write Request Unit 之和。
- WRU Per Query：平均每个 SQL 语句消耗的 Write Request Unit 数量。计算方法是将前述 Write Request Unit 监控指标除以当前每秒执行的 SQL 语句数量。
- Available RU：以 Resource Group 为单位显示 RU 令牌桶内可用的 token。当指标为 0 时，该 Resource Group 将以 `RU_PER_SEC` 指定的速度消耗 token，可以认为处于限速状态。
- Query Max Duration：以 Resource Group 为单位统计的最大 Query Duration。

## Resource 相关指标

- KV Request Count：以 Resource Group（资源组）为单位进行实时统计的 KV 请求数量，区分了读和写两种类型。`total` 为当前所有 Resource Group 涉及的 KV 请求数量之和。
- KV Request Count Per Query：平均每个 SQL 语句涉及的读写 KV 请求数量。计算方法是将前述 KV Request Count 监控指标除以当前每秒执行的 SQL 语句数量。
- Bytes Read：以 Resource Group 为单位进行实时统计的读取数据量。`total` 为当前所有 Resource Group 读取数据量之和。
- Bytes Read Per Query：平均每个 SQL 语句的读取数据量。将前述 Bytes Read 监控指标除以当前每秒执行的 SQL 语句数量。
- Bytes Written：以 Resource Group 为单位进行实时统计的写入数据量。`total` 为当前所有 Resource Group 写入数据量之和。
- Bytes Written Per Query：平均每个 SQL 语句的写入数据量。计算方法是将前述 Bytes Written 监控指标除以当前每秒执行的 SQL 语句数量。
- KV CPU Time：以 Resource Group 为单位进行实时统计的 KV 层 CPU 时间消耗。`total` 为当前所有 Resource Group 消耗 KV 层 CPU 时间之和。
- SQL CPU Time：以 Resource Group 为单位进行实时统计的 SQL 层 CPU 时间消耗。`total` 为当前所有 Resource Group 消耗 SQL 层 CPU 时间之和。

## Resource Controller Client 相关指标

- Active Resource Groups：实时统计各个 Resource Controller Client 的 Resource Groups 数量。
- Total KV Request Count：以 Resource Group 为单位，实时统计各个 Resource Controller Client 的 KV 请求数量。`total` 为 Resource Controller Client 下 KV 请求数量之和。
- Failed KV Request Count：以 Resource Group 为单位，实时统计各个 Resource Controller Client 的 KV 失败请求数量。`total` 为 Resource Controller Client 下 KV 失败请求数量之和。
- Successful KV Request Count：以 Resource Group 为单位，实时统计各个 Resource Controller Client 的 KV 成功请求数量。`total` 为 Resource Controller Client 下 KV 成功请求数量之和。
- Successful KV Request Wait Duration (99/90)：以 Resource Group 为单位，实时统计各个 Resource Controller Client 成功 KV 请求的等待时间（不同百分位）。
- Token Request Handle Duration (999/99)：以 Resource Group 为单位，实时统计各个 Resource Controller Client 向 Server 端申请 Token 等待的响应时间（不同百分位）。
- Token Request Count：以 Resource Group 为单位，实时统计各个 Resource Controller Client 向 Server 端申请 Token 的次数。`successful` 和 `failed` 分别为 Resource Controller Client 下申请 Token 成功和失败数量之和。
