---
title: 通过 Slack 与支持工单交互
summary: 介绍 Slack 支持工单交互的详细信息。
---

# 通过 Slack 与支持工单交互

对于订阅了 **Premium** [支持计划](/tidb-cloud/connected-care-detail.md)的客户，TiDB Cloud 在 [Slack](https://slack.com/) 中提供了一个名为 **PingCAP Support Bot** 的工单机器人，以支持更全面的支持工单交互和管理。

> **注意：**
>
> Slack 的工单支持功能需要申请才能使用。如果您有兴趣尝试此功能，请通过 <a href="mailto:support@pingcap.com">support@pingcap.com</a> 联系 TiDB Cloud 支持团队，或联系您的技术客户经理（TAM）。

您可以使用 **PingCAP Support Bot** 在 Slack 中创建支持工单：

![在 Slack 中创建支持工单](/media/tidb-cloud/connected-slack-ticket-interaction-creation.gif)

您也可以直接在 Slack 中回复支持工单：

![在 Slack 中回复支持工单](/media/tidb-cloud/connected-slack-ticket-interaction-reply.gif)

## 与支持工单交互

在 Slack 支持频道中，您只需要在消息中提及 **PingCAP Support Bot** 并描述问题。然后，机器人会向您发送一条带有**提出请求**按钮的消息。

![slack-ticket-interaction-1](/media/tidb-cloud/connected-slack-ticket-interaction-1.png)

点击**提出请求**打开表单，根据问题填写表单，然后点击**创建**提交工单。

![slack-ticket-interaction-2](/media/tidb-cloud/connected-slack-ticket-interaction-2.png)

提交后，机器人会在消息线程中发送一条确认消息，其中包含工单链接。

![slack-ticket-interaction-3](/media/tidb-cloud/connected-slack-ticket-interaction-3.png)

对于订阅了 **Premium** [支持计划](/tidb-cloud/connected-care-detail.md)的客户，支持 Slack 和工单系统之间的双向信息同步。

支持工程师在工单上的评论将同步到 Slack 消息线程中，用户无需跳转到支持门户即可查看。用户可以直接在此消息线程中回复，这些回复将同步到工单系统。

通过这种方式，订阅了 **Premium** 支持计划的客户无需离开 Slack 即可快速创建、响应和管理工单。

![slack-ticket-interaction-4](/media/tidb-cloud/connected-slack-ticket-interaction-4.png)

## 常见问题

- 如何查看我的工单状态？

    使用创建工单时使用的电子邮件地址登录 [PingCAP 帮助中心](https://tidb.support.pingcap.com/servicedesk/customer/user/requests)。您可以查看当前账户的所有历史工单及其状态。

## 联系支持

如需帮助或有任何问题，请通过 <a href="mailto:support@pingcap.com">support@pingcap.com</a> 联系我们的支持团队。
