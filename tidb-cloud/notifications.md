---
title: TiDB Cloud 控制台中的通知
summary: 了解 TiDB Cloud 控制台中的通知，包括通知类型、用途以及如何查看它们。
---

# TiDB Cloud 控制台中的通知

[TiDB Cloud 控制台](https://tidbcloud.com/)提供通知功能，让你了解重要更新、系统消息、产品变更、账单提醒和其他相关信息。这些通知帮助你在不离开控制台的情况下及时了解最新情况并采取必要的操作。

## 通知类型

你可能会在 TiDB Cloud 控制台中收到不同类型的通知，例如：

- **信息通知**

    提供有用的更新信息，如功能使用提示、应用变更或即将发生的事件提醒。

- **操作通知**

   提示你执行特定操作，如添加信用卡。

- **警报通知**

    通知你需要立即关注的重要问题或紧急事件，如系统错误、安全警告或重要更新。

- **账单通知**

    提供有关账单相关活动的更新，如信用额度和折扣更新。

- **反馈通知**

    请求你对某个功能的使用体验提供反馈，如对最近的交互进行评分或完成调查。

## 通知列表

下表列出了 TiDB Cloud 中可用的通知，以及它们的触发事件和接收者：

| 通知 | 触发事件 | 通知接收者 |
| --- | --- | --- |
| TiDB Cloud Serverless 集群创建 | 创建了一个 [TiDB Cloud Serverless](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless) 集群。 | 所有项目成员 |
| TiDB Cloud Serverless 集群删除 | 删除了一个 TiDB Cloud Serverless 集群。 | 所有项目成员 |
| TiDB Cloud Dedicated 集群创建 | 创建了一个 [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群。 | 所有项目成员 |
| TiDB Cloud Dedicated 集群删除 | 删除了一个 TiDB Cloud Dedicated 集群。 | 所有项目成员 |
| 组织预算阈值警报 | 达到组织[预算阈值](/tidb-cloud/tidb-cloud-budget.md)。 | `组织所有者`、`组织账单管理员`和`组织账单查看者` |
| 项目预算阈值警报 | 达到项目[预算阈值](/tidb-cloud/tidb-cloud-budget.md)。 | `组织所有者`、`组织账单管理员`、`组织账单查看者`和`项目所有者` |
| Serverless 集群支出限额阈值警报 | 达到组织中 TiDB Cloud Serverless 集群的[支出限额阈值](/tidb-cloud/manage-serverless-spend-limit.md)。 | `组织所有者`、`组织账单管理员`、`组织账单查看者`和`项目所有者` |
| 信用额度更新 | 组织的[信用额度](/tidb-cloud/tidb-cloud-billing.md#credits)被应用、完全使用、收回或过期。 | `组织所有者`、`组织账单管理员`和`组织账单查看者` |
| 折扣更新 | 组织的[折扣](/tidb-cloud/tidb-cloud-billing.md#discounts)被应用、收回或过期。 | `组织所有者`、`组织账单管理员`和`组织账单查看者` |
| 云市场更新 | 组织通过云服务提供商市场进行订阅或取消订阅。 | 所有组织成员 |
| 支持计划更新 | 组织的支持计划订阅发生变更。 | 所有组织成员 |

## 查看通知

要查看通知，请点击 [TiDB Cloud 控制台](https://tidbcloud.com/)左下角的**通知**。

当有新通知时，**通知**旁边会显示一个数字，表示有多少条未读通知。
