---
title: 通过 Slack 订阅
summary: 了解如何通过 Slack 获取告警通知来监控 TiDB 集群。
---

# 通过 Slack 订阅

TiDB Cloud 为您提供了一种通过 [Slack](https://slack.com/)、[电子邮件](/tidb-cloud/monitor-alert-email.md)和 [Zoom](/tidb-cloud/monitor-alert-zoom.md) 订阅告警通知的简便方法。本文档介绍如何通过 Slack 订阅告警通知。

以下截图显示了两个示例告警。

![TiDB Cloud 在 Slack 中的告警](/media/tidb-cloud/tidb-cloud-alert-subscription.png)

> **注意：**
>
> 目前，告警订阅仅适用于 [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群。

## 前提条件

- 通过 Slack 订阅的功能仅适用于订阅了**企业版**或**高级版**支持计划的组织。

- 要订阅 TiDB Cloud 的告警通知，您必须拥有 TiDB Cloud 中组织的 `Organization Owner` 访问权限或目标项目的 `Project Owner` 访问权限。

## 订阅告警通知

### 步骤 1. 生成 Slack webhook URL

1. 如果您还没有 Slack 应用，请[创建一个 Slack 应用](https://api.slack.com/apps/new)。点击**创建新应用**，然后选择**从头开始**。输入名称，选择要与应用关联的工作区，然后点击**创建应用**。
2. 转到应用的设置页面。您可以通过[应用管理仪表板](https://api.slack.com/apps)加载其设置。
3. 点击 **Incoming Webhooks** 标签，然后将 **Activate Incoming Webhooks** 切换为 **ON**。
4. 点击 **Add New Webhook to Workspace**。
5. 选择您想要接收告警通知的频道，然后选择**授权**。如果您需要将传入的 webhook 添加到私有频道，您必须先加入该频道。

您可以在 **Webhook URLs for Your Workspace** 部分看到一个新条目，格式如下：`https://hooks.slack.com/services/T00000000/B00000000/XXXXXXXXXXXXXXXXXXXXXXXX`。

### 步骤 2. 从 TiDB Cloud 订阅

> **提示：**
>
> 告警订阅适用于当前项目中的所有告警。如果您在项目中有多个集群，只需订阅一次即可。

1. 在 [TiDB Cloud 控制台](https://tidbcloud.com)中，使用左上角的组合框切换到目标项目。
2. 在左侧导航栏中，点击**项目设置** > **告警订阅**。
3. 在**告警订阅**页面，点击右上角的**添加订阅者**。
4. 从**订阅者类型**下拉列表中选择 **Slack**。
5. 在**名称**字段中输入名称，在 **URL** 字段中输入您的 Slack webhook URL。
6. 点击**测试连接**。

    - 如果测试成功，将显示**保存**按钮。
    - 如果测试失败，将显示错误消息。按照消息提示排除问题并重试连接。

7. 点击**保存**完成订阅。

或者，您也可以点击集群**告警**页面右上角的**订阅**。您将被引导至**告警订阅者**页面。

如果告警条件保持不变，告警会每三小时发送一次通知。

## 取消订阅告警通知

如果您不再想接收项目中集群的告警通知，请执行以下步骤：

1. 在 [TiDB Cloud 控制台](https://tidbcloud.com)中，使用左上角的组合框切换到目标项目。
2. 在左侧导航栏中，点击**项目设置** > **告警订阅**。
3. 在**告警订阅**页面，找到要删除的目标订阅者所在行，然后点击 **...** > **取消订阅**。
4. 点击**取消订阅**确认取消订阅。
