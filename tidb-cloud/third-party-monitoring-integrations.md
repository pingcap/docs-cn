---
title: 第三方指标集成（Beta）
summary: 了解如何使用第三方指标集成。
---

# 第三方指标集成（Beta）

您可以将 TiDB Cloud 与第三方指标服务集成，以接收 TiDB Cloud 警报并使用指标服务查看 TiDB 集群的性能指标。第三方指标集成目前处于 beta 阶段。

## 所需权限

要编辑第三方集成设置，您必须是组织的 `Organization Owner` 角色或目标项目的 `Project Owner` 角色。

## 查看或修改第三方集成

1. 在 [TiDB Cloud 控制台](https://tidbcloud.com)中，使用左上角的组合框切换到您的目标项目。
2. 在左侧导航栏中，点击**项目设置** > **集成**。

此时会显示可用的第三方集成。

## 限制

- 对于 [TiDB Cloud Serverless](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless) 集群，不支持第三方指标集成。

- 当集群状态为**创建中**、**恢复中**、**已暂停**或**恢复中**时，第三方指标集成不可用。

## 可用集成

### Datadog 集成（beta）

通过 Datadog 集成，您可以配置 TiDB Cloud 将 TiDB 集群的指标数据发送到 [Datadog](https://www.datadoghq.com/)，并在 Datadog 仪表板中查看这些指标。

有关详细的集成步骤和 Datadog 跟踪的指标列表，请参考[将 TiDB Cloud 与 Datadog 集成](/tidb-cloud/monitor-datadog-integration.md)。

### Prometheus 和 Grafana 集成（beta）

通过 Prometheus 和 Grafana 集成，您可以从 TiDB Cloud 获取 Prometheus 的 `scrape_config` 文件，并使用该文件中的内容配置 Prometheus。您可以在 Grafana 仪表板中查看这些指标。

有关详细的集成步骤和 Prometheus 跟踪的指标列表，请参见[将 TiDB Cloud 与 Prometheus 和 Grafana 集成](/tidb-cloud/monitor-prometheus-and-grafana-integration.md)。

### New Relic 集成（beta）

通过 New Relic 集成，您可以配置 TiDB Cloud 将 TiDB 集群的指标数据发送到 [New Relic](https://newrelic.com/)，并在 New Relic 仪表板中查看这些指标。

有关详细的集成步骤和 New Relic 跟踪的指标列表，请参见[将 TiDB Cloud 与 New Relic 集成](/tidb-cloud/monitor-new-relic-integration.md)。
