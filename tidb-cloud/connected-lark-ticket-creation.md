---
title: 通过 Lark 创建工单和订阅工单更新
summary: 介绍 Lark 工单创建和更新订阅的详细信息。
---

# 通过 Lark 创建工单和订阅工单更新

对于订阅了 **Enterprise** [支持计划](/tidb-cloud/connected-care-detail.md)的客户，TiDB Cloud 在 [Lark](https://www.larksuite.com/) 中提供了一个名为 **PingCAP Support Bot** 的工单机器人，用于管理支持工单系统中的工单创建和更新。

> **注意：**
>
> Lark 的工单支持功能需要申请才能使用。如果您有兴趣尝试此功能，请通过 <a href="mailto:support@pingcap.com">support@pingcap.com</a> 联系 TiDB Cloud 支持团队，或联系您的技术客户经理（TAM）。

## 创建支持工单

在 **Customer Support Group** Lark 群组中，在消息中输入 `@PingCAP Support Bot create ticket`。然后，**PingCAP Support Bot** 将回复一个用于创建工单的 Lark 消息卡片。

![lark-ticket-creation-1](/media/tidb-cloud/connected-lark-ticket-creation-1.png)

填写必填字段并点击**提交**。提交后，卡片将更新为**工单已提交**，表示您的请求正在处理中。

![lark-ticket-creation-2](/media/tidb-cloud/connected-lark-ticket-creation-2.png)

支持工单创建后，**工单已提交**卡片将更新为**支持工单已创建**卡片，提供工单名称和查看工单的链接。

![lark-ticket-creation-3](/media/tidb-cloud/connected-lark-ticket-creation-3.png)

## 订阅工单更新

每当 PingCAP 支持工程师在工单上发表评论时，**PingCAP Support Bot** 将向 Lark 群组发送一个**工单新评论**卡片。

![connected-lark-ticket-creation-4](/media/tidb-cloud/connected-lark-ticket-creation-4.png)

## 常见问题

- 如何查看我的工单状态？

    使用创建工单时使用的电子邮件地址登录 [PingCAP 帮助中心](https://tidb.support.pingcap.com/servicedesk/customer/user/requests)。您可以查看当前账户的所有历史工单及其状态。

## 联系支持

如需帮助或有任何问题，请通过 <a href="mailto:support@pingcap.com">support@pingcap.com</a> 联系我们的支持团队。
