---
title: 通过 Zoom 订阅
summary: 了解如何通过 Zoom 获取告警通知来监控您的 TiDB 集群。
---

# 通过 Zoom 订阅

TiDB Cloud 为您提供了一种通过 [Zoom](https://www.zoom.com/)、[Slack](/tidb-cloud/monitor-alert-slack.md) 和[电子邮件](/tidb-cloud/monitor-alert-email.md)订阅告警通知的简便方法。本文介绍如何通过 Zoom 订阅告警通知。

> **注意：**
>
> 目前，告警订阅仅适用于 [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群。

## 前提条件

- 通过 Zoom 订阅功能仅适用于订阅了**企业版**或**高级版**支持计划的组织。

- 要订阅 TiDB Cloud 的告警通知，您必须在 TiDB Cloud 中拥有组织的 `Organization Owner` 访问权限或目标项目的 `Project Owner` 访问权限。

- 要在 Zoom 中添加和配置传入 Webhook 聊天机器人，您需要在 Zoom 账户上拥有管理员权限。

## 订阅告警通知

### 步骤 1. 添加 Zoom 传入 Webhook 应用

1. 以账户管理员身份登录 [Zoom App Marketplace](https://marketplace.zoom.us/)。
2. 在 Zoom App Marketplace 中转到 [Incoming Webhook App](https://marketplace.zoom.us/apps/eH_dLuquRd-VYcOsNGy-hQ) 页面，然后点击**添加**以添加此应用。如果应用未预先批准，请联系您的 Zoom 管理员为您的账户批准此应用。更多信息，请参见[批准应用和管理应用请求](https://support.zoom.us/hc/en-us/articles/360027829671)。
3. 确认应用所需的权限，然后点击**授权**以添加传入 Webhook 应用。

### 步骤 2. 生成 Zoom webhook URL

1. 登录 Zoom 桌面客户端。
2. 点击**团队聊天**标签。
3. 在**应用**下，找到并选择**传入 Webhook**，或从上方选择您想要接收消息的聊天频道。
4. 输入以下命令以创建新连接。您需要将 `${connectionName}` 替换为您想要的连接名称，例如 `tidbcloud-alerts`：

    ```shell
    /inc connect ${connectionName}
    ```

5. 命令将返回以下详细信息：

   - **端点**。它将提供格式为 `https://integrations.zoom.us/chat/webhooks/incomingwebhook/XXXXXXXXXXXXXXXXXXXXXXXX` 的 webhook URL。
   - **验证令牌**

### 步骤 3. 从 TiDB Cloud 订阅

> **提示：**
>
> 告警订阅适用于当前项目中的所有告警。如果您在项目中有多个集群，您只需订阅一次。

1. 在 [TiDB Cloud 控制台](https://tidbcloud.com)中，使用左上角的组合框切换到您的目标项目。
2. 在左侧导航栏中，点击**项目设置** > **告警订阅**。
3. 在**告警订阅**页面上，点击右上角的**添加订阅者**。
4. 从**订阅者类型**下拉列表中选择 **Zoom**。
5. 在**名称**字段中输入名称，在 **URL** 字段中输入您的 Zoom webhook URL，在**令牌**字段中输入验证令牌。
6. 点击**测试连接**。

    - 如果测试成功，将显示**保存**按钮。
    - 如果测试失败，将显示错误消息。按照消息进行故障排除并重试连接。

7. 点击**保存**完成订阅。

或者，您也可以点击集群**告警**页面右上角的**订阅**。您将被引导至**告警订阅者**页面。

如果告警条件保持不变，告警每三小时发送一次通知。

## 取消订阅告警通知

如果您不再想接收项目中集群的告警通知，请执行以下步骤：

1. 在 [TiDB Cloud 控制台](https://tidbcloud.com)中，使用左上角的组合框切换到您的目标项目。
2. 在左侧导航栏中，点击**项目设置** > **告警订阅**。
3. 在**告警订阅**页面上，找到要删除的目标订阅者所在的行，然后点击 **...** > **取消订阅**。
4. 点击**取消订阅**确认取消订阅。
