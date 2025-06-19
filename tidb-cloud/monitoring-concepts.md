---
title: 监控
summary: 了解 TiDB Cloud 的监控概念。
---

# 监控

TiDB Cloud 的监控功能提供了工具和集成，使你能够监督集群性能、跟踪活动并及时响应问题。

## 内置指标

内置指标是指 TiDB Cloud 在**指标**页面上收集和展示的一整套集群标准指标。通过这些指标，你可以轻松识别性能问题，并确定当前的数据库部署是否满足你的需求。

更多信息，请参阅 [TiDB Cloud 内置指标](/tidb-cloud/built-in-monitoring.md)。

## 内置告警

内置告警是指 TiDB Cloud 提供的集群告警机制，用于帮助你监控集群。目前，TiDB Cloud 提供以下三种类型的告警：

- 资源使用告警

- 数据迁移告警

- Changefeed 告警

在 TiDB Cloud 控制台的告警页面，你可以查看集群的告警、编辑告警规则，以及订阅告警通知邮件。

更多信息，请参阅 [TiDB Cloud 内置告警](/tidb-cloud/monitor-built-in-alerting.md)。

## 集群事件

在 TiDB Cloud 中，事件表示 TiDB Cloud 集群的变更。TiDB Cloud 在集群级别记录历史事件，以帮助你跟踪集群活动。你可以在**事件**页面查看记录的事件，包括事件类型、状态、消息、触发时间和触发用户。

更多信息，请参阅 [TiDB Cloud 集群事件](/tidb-cloud/tidb-cloud-events.md)。

## 第三方指标集成（Beta）

TiDB Cloud 允许你集成以下任何第三方指标服务，以接收 TiDB Cloud 告警并查看 TiDB 集群的性能指标。

- Datadog 集成

- Prometheus 和 Grafana 集成

- New Relic 集成

目前，这些第三方指标集成处于 beta 阶段。

更多信息，请参阅[第三方指标集成（Beta）](/tidb-cloud/third-party-monitoring-integrations.md)。
