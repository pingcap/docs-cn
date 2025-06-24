---
title: TiDB Cloud 内置告警
summary: 了解如何通过获取 TiDB Cloud 的告警通知来监控你的 TiDB 集群。
---

# TiDB Cloud 内置告警

TiDB Cloud 为你提供了一种简单的方式来查看告警、编辑告警规则和订阅告警通知。

本文介绍如何执行这些操作，并提供 TiDB Cloud 内置告警条件供你参考。

> **注意：**
>
> 目前，告警功能仅适用于 [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群。

## 查看告警

在 TiDB Cloud 中，你可以在**告警**页面查看活动和已关闭的告警。

1. 在 [TiDB Cloud 控制台](https://tidbcloud.com/)中，导航到项目的[**集群**](https://tidbcloud.com/project/clusters)页面。

    > **提示：**
    >
    > 你可以使用左上角的组合框在组织、项目和集群之间切换。

2. 点击目标集群的名称。此时会显示集群概览页面。
3. 在左侧导航栏中点击**告警**。
4. **告警**页面默认显示活动告警。你可以查看每个活动告警的信息，如告警名称、触发时间和持续时间。
5. 如果你也想查看已关闭的告警，只需点击**状态**下拉列表并选择**已关闭**或**全部**。

## 编辑告警规则

在 TiDB Cloud 中，你可以通过禁用或启用告警或更新告警阈值来编辑告警规则。

1. 在**告警**页面，点击**编辑规则**。
2. 根据需要禁用或启用告警规则。
3. 点击**编辑**来更新告警规则的阈值。

    > **提示：**
    >
    > 目前，TiDB Cloud 提供有限的告警规则编辑功能。某些告警规则不支持编辑。如果你想配置不同的触发条件或频率，或让告警自动触发下游服务（如 [PagerDuty](https://www.pagerduty.com/docs/guides/datadog-integration-guide/)）中的操作，请考虑使用[第三方监控和告警集成](/tidb-cloud/third-party-monitoring-integrations.md)。

## 订阅告警通知

在 TiDB Cloud 中，你可以通过以下方法之一订阅告警通知：

- [电子邮件](/tidb-cloud/monitor-alert-email.md)
- [Slack](/tidb-cloud/monitor-alert-slack.md)
- [Zoom](/tidb-cloud/monitor-alert-zoom.md)

## TiDB Cloud 内置告警条件

下表提供了 TiDB Cloud 内置告警条件和相应的建议操作。

> **注意：**
>
> - 虽然这些告警条件不一定意味着存在问题，但它们通常是新出现问题的早期预警指标。因此，建议采取建议的操作。
> - 你可以在 TiDB Cloud 控制台上编辑告警的阈值。
> - 某些告警规则默认是禁用的。你可以根据需要启用它们。

### 资源使用告警

| 条件 | 建议操作 |
|:--- |:--- |
| 集群中 TiDB 节点的总内存使用率超过 70% 持续 10 分钟 | 考虑增加 TiDB 的节点数量或节点大小，以减少当前工作负载的内存使用百分比。|
| 集群中 TiKV 节点的总内存使用率超过 70% 持续 10 分钟 | 考虑增加 TiKV 的节点数量或节点大小，以减少当前工作负载的内存使用百分比。 |
| 集群中 TiFlash 节点的总内存使用率超过 70% 持续 10 分钟 | 考虑增加 TiFlash 的节点数量或节点大小，以减少当前工作负载的内存使用百分比。 |
| TiDB 节点的总 CPU 使用率超过 80% 持续 10 分钟 | 考虑增加 TiDB 的节点数量或节点大小，以减少当前工作负载的 CPU 使用百分比。|
| TiKV 节点的总 CPU 使用率超过 80% 持续 10 分钟 | 考虑增加 TiKV 的节点数量或节点大小，以减少当前工作负载的 CPU 使用百分比。 |
| TiFlash 节点的总 CPU 使用率超过 80% 持续 10 分钟 | 考虑增加 TiFlash 的节点数量或节点大小，以减少当前工作负载的 CPU 使用百分比。 |
| TiKV 存储使用率超过 80% | 考虑增加 TiKV 的节点数量或节点存储大小以增加存储容量。 |
| TiFlash 存储使用率超过 80% | 考虑增加 TiFlash 的节点数量或节点存储大小以增加存储容量。 |
| TiDB 节点中的最大内存使用率超过 70% 持续 10 分钟 | 考虑检查集群中是否存在任何[热点问题](/tidb-cloud/tidb-cloud-sql-tuning-overview.md#hotspot-issues)，或增加 TiDB 的节点数量或节点大小，以减少当前工作负载的内存使用百分比。 |
| TiKV 节点中的最大内存使用率超过 70% 持续 10 分钟 | 考虑检查集群中是否存在任何[热点问题](/tidb-cloud/tidb-cloud-sql-tuning-overview.md#hotspot-issues)，或增加 TiKV 的节点数量或节点大小，以减少当前工作负载的内存使用百分比。 |
| TiDB 节点中的最大 CPU 使用率超过 80% 持续 10 分钟 | 考虑检查集群中是否存在任何[热点问题](/tidb-cloud/tidb-cloud-sql-tuning-overview.md#hotspot-issues)，或增加 TiDB 的节点数量或节点大小，以减少当前工作负载的 CPU 使用百分比。 |
| TiKV 节点中的最大 CPU 使用率超过 80% 持续 10 分钟 | 考虑检查集群中是否存在任何[热点问题](/tidb-cloud/tidb-cloud-sql-tuning-overview.md#hotspot-issues)，或增加 TiKV 的节点数量或节点大小，以减少当前工作负载的 CPU 使用百分比。 |

### 数据迁移告警

| 条件 | 建议操作 |
|:--- |:--- |
| 数据导出期间数据迁移任务遇到错误 | 检查错误并参阅[故障排除数据迁移](/tidb-cloud/tidb-cloud-dm-precheck-and-troubleshooting.md#migration-errors-and-solutions)获取帮助。 |
| 数据导入期间数据迁移任务遇到错误 | 检查错误并参阅[故障排除数据迁移](/tidb-cloud/tidb-cloud-dm-precheck-and-troubleshooting.md#migration-errors-and-solutions)获取帮助。 |
| 增量迁移期间数据迁移任务遇到错误 | 检查错误并参阅[故障排除数据迁移](/tidb-cloud/tidb-cloud-dm-precheck-and-troubleshooting.md#migration-errors-and-solutions)获取帮助。 |
| 增量迁移期间数据迁移任务已暂停超过 6 小时 | 数据增量迁移期间数据迁移任务已暂停超过 6 小时。上游数据库中的 binlog 可能已被清除（取决于你的数据库 binlog 清除策略）并可能导致增量迁移失败。参阅[故障排除数据迁移](/tidb-cloud/tidb-cloud-dm-precheck-and-troubleshooting.md#migration-errors-and-solutions)获取帮助。 |
| 复制延迟大于 10 分钟且持续增加超过 20 分钟 | 参阅[故障排除数据迁移](/tidb-cloud/tidb-cloud-dm-precheck-and-troubleshooting.md#migration-errors-and-solutions)获取帮助。 |

### Changefeed 告警

| 条件                                   | 建议操作                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |
|:--------------------------------------------|:---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Changefeed 延迟超过 600 秒。 | 在 TiDB Cloud 控制台的 **Changefeed** 页面和 **Changefeed 详情**页面上检查 changefeed 状态，你可以在那里找到一些错误消息来帮助诊断此问题。<br/> 可能触发此告警的原因包括：<ul><li>上游的整体流量增加，导致现有的 changefeed 规格不足以处理。如果流量增加是暂时的，changefeed 延迟会在流量恢复正常后自动恢复。如果流量增加是持续的，你需要扩容 changefeed。</li><li>下游或网络异常。在这种情况下，首先解决这种异常。</li><li>如果下游是 RDS，表缺少索引可能会导致写入性能低和延迟高。在这种情况下，你需要在上游或下游添加必要的索引。</li></ul>如果问题无法从你这边解决，你可以联系 [TiDB Cloud 支持团队](/tidb-cloud/tidb-cloud-support.md)寻求进一步帮助。 |
| Changefeed 状态为 `FAILED`。                 | 在 TiDB Cloud 控制台的 **Changefeed** 页面和 **Changefeed 详情**页面上检查 changefeed 状态，你可以在那里找到一些错误消息来帮助诊断此问题。<br/> 如果问题无法从你这边解决，你可以联系 [TiDB Cloud 支持团队](/tidb-cloud/tidb-cloud-support.md)寻求进一步帮助。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              |
| Changefeed 状态为 `WARNING`。              | 在 TiDB Cloud 控制台的 **Changefeed** 页面和 **Changefeed 详情**页面上检查 changefeed 状态，你可以在那里找到一些错误消息来帮助诊断此问题。<br/> 如果问题无法从你这边解决，你可以联系 [TiDB Cloud 支持团队](/tidb-cloud/tidb-cloud-support.md)寻求进一步帮助。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              |
