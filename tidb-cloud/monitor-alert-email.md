---
title: 通过电子邮件订阅
summary: 了解如何通过电子邮件接收告警通知来监控您的 TiDB 集群。
---

# 通过电子邮件订阅

TiDB Cloud 为您提供了一种简单的方式来通过电子邮件、[Slack](/tidb-cloud/monitor-alert-slack.md) 和 [Zoom](/tidb-cloud/monitor-alert-zoom.md) 订阅告警通知。本文档介绍如何通过电子邮件订阅告警通知。

> **注意：**
>
> 目前，告警订阅功能仅适用于 [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群。

## 前提条件

- 要订阅 TiDB Cloud 的告警通知，您必须拥有组织的 `Organization Owner` 访问权限或目标项目的 `Project Owner` 访问权限。

## 订阅告警通知

> **提示：**
>
> 告警订阅适用于当前项目中的所有告警。如果您在项目中有多个集群，您只需订阅一次。

要获取项目中集群的告警通知，请按照以下步骤操作：

1. 在 [TiDB Cloud 控制台](https://tidbcloud.com)中，使用左上角的下拉框切换到目标项目。
2. 在左侧导航栏中，点击 **Project Settings** > **Alert Subscription**。
3. 在 **Alert Subscription** 页面，点击右上角的 **Add Subscriber**。
4. 从 **Subscriber Type** 下拉列表中选择 **Email**。
5. 输入您的电子邮件地址。
6. 点击 **Test Connection**。

    - 如果测试成功，将显示 **Save** 按钮。
    - 如果测试失败，将显示错误消息。请按照消息提示排除问题，然后重试连接。

7. 点击 **Save** 完成订阅。

另外，您也可以在集群的 [**Alert**](/tidb-cloud/monitor-built-in-alerting.md#view-alerts) 页面右上角点击 **Subscribe**。您将被引导至 **Alert Subscriber** 页面。

如果告警条件保持不变，告警将每三小时发送一次电子邮件通知。

## 取消告警通知订阅

如果您不再希望接收项目中集群的告警通知，请按照以下步骤操作：

1. 在 [TiDB Cloud 控制台](https://tidbcloud.com)中，使用左上角的下拉框切换到目标项目。
2. 在左侧导航栏中，点击 **Project Settings** > **Alert Subscription**。
3. 在 **Alert Subscription** 页面，找到要删除的目标订阅者所在行，然后点击 **...** > **Unsubscribe**。
4. 点击 **Unsubscribe** 确认取消订阅。
