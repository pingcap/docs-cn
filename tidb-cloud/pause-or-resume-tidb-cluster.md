---
title: 暂停或恢复 TiDB Cloud Dedicated 集群
summary: 了解如何暂停或恢复 TiDB Cloud Dedicated 集群。
---

# 暂停或恢复 TiDB Cloud Dedicated 集群

在 TiDB Cloud 中，您可以轻松地暂停和恢复不需要持续运行的 TiDB Cloud Dedicated 集群。

暂停操作不会影响集群中存储的数据，仅会停止收集监控信息和计算资源的消耗。暂停后，您可以随时恢复集群。

与备份和恢复相比，暂停和恢复集群所需时间更短，并且可以保留集群信息（包括集群版本、集群配置和 TiDB 用户账户）。

> **注意：**
>
> 您不能暂停 [TiDB Cloud Serverless 集群](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless)。

## 限制条件

- 只有当集群处于 **Available**（可用）状态时，您才能暂停集群。如果集群处于其他状态（如 **Modifying**），您必须等待当前操作完成后才能暂停集群。
- 当数据导入任务正在进行时，您不能暂停集群。您可以等待导入任务完成或取消导入任务。
- 当备份任务正在进行时，您不能暂停集群。您可以等待当前备份任务完成或[删除正在运行的备份任务](/tidb-cloud/backup-and-restore.md#delete-a-running-backup-job)。
- 如果集群有任何 [changefeeds](/tidb-cloud/changefeed-overview.md)，您不能暂停集群。您需要在暂停集群之前[删除现有的 changefeeds](/tidb-cloud/changefeed-overview.md#delete-a-changefeed)。

## 暂停 TiDB 集群

暂停时长和行为取决于您的组织创建日期：

- 2024 年 11 月 12 日之后创建的组织遵循标准暂停行为，最长暂停时间为 7 天。
- 2024 年 11 月 12 日或之前创建的组织遵循兼容暂停行为，允许更长的暂停时间。这些组织将逐步过渡到标准的 7 天限制。

<SimpleTab>
<div label="标准暂停行为">

当集群被暂停时，请注意以下几点：

- TiDB Cloud 停止收集集群的监控信息。
- 您无法从集群读取或写入数据。
- 您无法导入或备份数据。
- 仅收取以下费用：

    - 节点存储费用
    - 数据备份费用

- TiDB Cloud 停止集群的[自动备份](/tidb-cloud/backup-and-restore.md#turn-on-auto-backup)。
- 最长暂停时间为 7 天。如果您在 7 天内没有手动恢复集群，TiDB Cloud 将自动恢复它。
- 您可以在集群概览页面查看自动恢复计划。TiDB Cloud 将在集群自动恢复前 24 小时向组织所有者和项目所有者发送通知邮件。

</div>
<div label="兼容暂停行为">

> **注意：**
>
> 如果您的组织是在 2024 年 11 月 12 日之前创建的，您的集群仍然遵循兼容暂停行为。TiDB Cloud 将在过渡到新的标准暂停行为之前通知您。

当集群被暂停时，请注意以下几点：

- TiDB Cloud 停止收集集群的监控信息。
- 您无法从集群读取或写入数据。
- 您无法导入或备份数据。
- TiDB Cloud 不会自动恢复已暂停的集群。
- 仅收取以下费用：

    - 节点存储费用
    - 数据备份费用

- TiDB Cloud 停止集群的[自动备份](/tidb-cloud/backup-and-restore.md#turn-on-auto-backup)。

</div>
</SimpleTab>

要暂停集群，请按照以下步骤操作：

1. 在 TiDB Cloud 控制台中，导航到项目的 [**Clusters**](https://tidbcloud.com/project/clusters) 页面。
2. 在要暂停的集群所在行，点击 **...**。

    > **提示：**
    >
    > 或者，您可以在 **Clusters** 页面上点击要暂停的集群名称，然后点击右上角的 **...**。

3. 在下拉菜单中点击 **Pause**。

    此时会显示 **Pause your cluster** 对话框。

4. 在对话框中，点击 **Pause** 确认您的选择。

    点击 **Pause** 后，集群将首先进入 **Pausing** 状态。一旦暂停操作完成，集群将转换为 **Paused** 状态。

您也可以使用 TiDB Cloud API 暂停集群。目前，TiDB Cloud API 仍处于测试阶段。更多信息，请参见 [TiDB Cloud API 文档](https://docs.pingcap.com/tidbcloud/api/v1beta)。

## 恢复 TiDB 集群

暂停的集群恢复后，请注意以下几点：

- TiDB Cloud 恢复收集集群的监控信息，您可以从集群读取或写入数据。
- TiDB Cloud 恢复收取计算和存储费用。
- TiDB Cloud 恢复集群的[自动备份](/tidb-cloud/backup-and-restore.md#turn-on-auto-backup)。

要恢复已暂停的集群，请按照以下步骤操作：

1. 在 TiDB Cloud 控制台中，导航到项目的 [**Clusters**](https://tidbcloud.com/project/clusters) 页面。
2. 对于要恢复的集群，点击 **Resume**。此时会显示 **Resume your cluster** 对话框。

    > **注意：**
    >
    > 您不能恢复处于 **Pausing** 状态的集群。

3. 在对话框中，点击 **Resume** 确认您的选择。集群状态将变为 **Resuming**。

根据集群大小，恢复集群可能需要几分钟时间。集群恢复后，集群状态将从 **Resuming** 变为 **Available**。

您也可以使用 TiDB Cloud API 恢复集群。目前，TiDB Cloud API 仍处于测试阶段。更多信息，请参见 [TiDB Cloud API 文档](https://docs.pingcap.com/tidbcloud/api/v1beta)。
