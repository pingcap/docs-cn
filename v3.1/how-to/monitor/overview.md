---
title: TiDB 监控框架概述
category: how-to
---

# TiDB 监控框架概述

TiDB 使用开源时序数据库 [Prometheus](https://prometheus.io) 作为监控和性能指标信息存储方案，使用 [Grafana](https://grafana.com/grafana) 作为可视化组件进行展示。

## Prometheus 在 TiDB 中的应用

Prometheus 是一个拥有多维度数据模型的、灵活的查询语句的时序数据库。Prometheus 作为热门的开源项目，拥有活跃的社区及众多的成功案例。

Prometheus 提供了多个组件供用户使用。目前，TiDB 使用了以下组件：

- Prometheus Server：用于收集和存储时间序列数据。
- Client 代码库：用于定制程序中需要的 Metric。
- Alertmanager：用于实现报警机制。

其结构如下图所示：

![Prometheus in TiDB](/media/prometheus-in-tidb.png)

## Grafana 在 TiDB 中的应用

Grafana 是一个开源的 metric 分析及可视化系统。TiDB 使用 Grafana 来展示 TiDB 的各项性能指标。如下图所示：

![Grafana in TiDB](/media/grafana-screenshot.png)
