---
title: TiDB 监控 API 概览
summary: 了解 TiDB 监控服务的 API。
---

# TiDB 监控 API 概览

TiDB 的监控框架基于 [Prometheus](https://prometheus.io) 和 [Grafana](https://grafana.com/grafana) 这两个开源项目。TiDB 使用 Prometheus 存储监控和性能指标，使用 Grafana 可视化展示这些指标，并提供内置的 [TiDB Dashboard](/dashboard/dashboard-intro.md) 图形化界面，用于监控及诊断 TiDB 集群。

你可以使用以下 API 监控 TiDB 集群状态：

- [状态接口](/tidb-monitoring-api.md#使用状态接口)：监控当前 TiDB Server 的[运行状态](/tidb-monitoring-api.md#运行状态)，以及某张表的[存储信息](/tidb-monitoring-api.md#存储信息)。
- [Metrics 接口](/tidb-monitoring-api.md#使用-metrics-接口)：获取各组件中不同操作的详细指标信息，可通过 Grafana 查看这些指标。

关于各个 API 的请求参数、响应示例与使用说明，请参阅 [TiDB 监控 API](/tidb-monitoring-api.md)。
