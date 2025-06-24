---
title: Connected Care 概述
summary: 介绍新一代 TiDB Cloud 支持服务 - Connected Care。
aliases: ['/tidbcloud/connected-care-announcement']
---

# Connected Care 概述

随着各种规模的客户继续在 TiDB Cloud 上扩展用例和运营，TiDB Cloud 致力于重新构想其支持服务，以适应客户不断发展的需求。为了提供更大的价值和无缝体验，TiDB Cloud 很高兴宣布在 **2025 年 2 月 17 日**推出新的支持服务 **Connected Care**。

作为此次转型的一部分，从 **2025 年 2 月 17 日**起，当前的支持计划将不再提供购买，并被归类为传统支持计划。但是，TiDB Cloud 将继续为订阅传统计划的客户提供全面支持，直至其各自的[退役日期](#迁移到-connected-care)。

为确保平稳过渡并获取最新功能，TiDB Cloud 鼓励客户迁移并采用 Connected Care 服务。

## Connected Care

Connected Care 服务旨在通过现代通信工具、主动支持和先进的 AI 功能加强您与 TiDB Cloud 的连接，提供无缝和以客户为中心的体验。

在 Connected Care 服务中，有四种支持计划：**Basic**、**Developer**（对应传统的 **Standard** 计划）、**Enterprise** 和 **Premium**。

> **注意**
>
> 虽然 **Basic**、**Enterprise** 和 **Premium** 支持计划使用与传统计划相同的计划名称，但它们指的是具有不同服务承诺的不同计划。

下表概述了 Connected Care 服务中的每个支持计划。更多信息，请参见 [Connected Care 详情](/tidb-cloud/connected-care-detail.md)。

| 支持计划                                                                                                                                                                                                                       | Basic                        | Developer                                    | Enterprise                                     | Premium                                   |
|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|:-----------------------------|:---------------------------------------------|:-----------------------------------------------|:------------------------------------------|
| 推荐工作负载                                                                                                                                                                                                              | 个人或入门项目 | 开发中的工作负载                  | 生产中的工作负载                     | 生产中的关键业务工作负载 |
| 账单和账户支持                                                                                                                                                                                                        | ✔                            | ✔                                            | ✔                                              | ✔                                         |
| 技术支持                                                                                                                                                                                                                  | -                            | ✔                                            | ✔                                              | ✔                                         |
| 初始响应时间                                                                                                                                                                                                              | -                            | 工作时间                               | 7x24                                           | 7x24                                      |
| [Connected：诊所服务](/tidb-cloud/tidb-cloud-clinic.md)                                                                                                                                                                      | -                            | -                                            | ✔                                              | ✔                                         |
| [Connected：即时通讯中的 AI 聊天](/tidb-cloud/connected-ai-chat-in-im.md)                                                                                                                                                 | -                            | -                                            | ✔                                              | ✔                                         |
| Connected：TiDB Cloud 告警的即时通讯订阅（[Slack](/tidb-cloud/monitor-alert-slack.md)、[Zoom](/tidb-cloud/monitor-alert-zoom.md)）                                                                                          | -                            | -                                            | ✔                                              | ✔                                         |
| Connected：工单创建和更新订阅（[Slack](/tidb-cloud/connected-slack-ticket-creation.md)、[Lark](/tidb-cloud/connected-lark-ticket-creation.md)） | -                            | -                                            | ✔                                              | ✔                                         |
| Connected：支持工单的即时通讯交互（[Slack](/tidb-cloud/connected-slack-ticket-interaction.md)、[Lark](/tidb-cloud/connected-lark-ticket-interaction.md)）   | -                            | -                                            | -                                              | ✔                                         |
| 技术客户经理                                                                                                                                                                                                          | -                            | -                                            | -                                              | ✔                                         |

> **注意**
>
> 所有四种支持计划的客户都可以访问 [PingCAP 支持门户](https://tidb.support.pingcap.com/)进行服务请求。

## 传统支持服务与 Connected Care 支持服务的区别

Connected Care 服务中的支持计划引入了一套全新的功能，如下所示：

- Connected：诊所服务

    此功能提供先进的监控和诊断服务 Clinic，旨在帮助您通过详细分析和可操作的见解快速识别性能问题、优化数据库并提高整体性能。更多信息，请参见 [Connected：诊所服务](/tidb-cloud/tidb-cloud-clinic.md)。

- Connected：即时通讯中的 AI 聊天

    此功能使您能够通过即时通讯（IM）工具与 AI 助手聊天，立即获得问题的答案。更多信息，请参见 [Connected：即时通讯中的 AI 聊天](/tidb-cloud/connected-ai-chat-in-im.md)。

- Connected：TiDB Cloud 告警的即时通讯订阅

    此功能为您提供了一种通过即时通讯工具订阅告警通知的简便方法，让您随时了解重要更新。更多信息，请参见[通过 Slack 订阅](/tidb-cloud/monitor-alert-slack.md)和[通过 Zoom 订阅](/tidb-cloud/monitor-alert-zoom.md)。

- Connected：工单创建和更新订阅

    此功能使您能够通过即时通讯工具创建支持工单并订阅工单更新。更多信息，请参见[通过 Slack 创建工单和订阅工单更新](/tidb-cloud/connected-slack-ticket-creation.md)和[通过 Lark 创建工单和订阅工单更新](/tidb-cloud/connected-lark-ticket-creation.md)。

- Connected：支持工单的即时通讯交互

    此功能使您能够通过即时通讯工具快速创建和处理支持工单，实现流畅的沟通。更多信息，请参见[通过 Slack 与支持工单交互](/tidb-cloud/connected-slack-ticket-interaction.md)和[通过 Lark 与支持工单交互](/tidb-cloud/connected-lark-ticket-interaction.md)。

通过这些新功能，Connected Care 服务为不同客户需求提供更好的连接性、更个性化的支持和更具成本效益的解决方案。

- 新的 **Enterprise** 和 **Premium** 计划：通过 Clinic 中的高级监控服务、TiDB Cloud 告警的即时通讯订阅、工单更新的即时通讯订阅、即时通讯中的 AI 聊天以及支持工单的即时通讯交互，将客户与现代通信工具和先进的 AI 功能连接起来。

- 新的 **Developer** 计划：客户除了享有与 **Basic** 计划相同的社区和 [TiDB.AI](https://tidb.ai/) 帮助外，还可以直接获得无限制的技术支持。

- 新的 **Basic** 计划：客户将被引导加入活跃的社区渠道，在那里他们可以与其他社区成员互动，并与 [TiDB.AI](https://tidb.ai/) 进行技术交流。

## 迁移到 Connected Care

下表列出了传统支持计划的关闭时间表：

| 支持计划                        | 关闭日期 |
|:----------------------------------------|:--------------|
| 传统 **Basic** 计划                     | 2025 年 2 月 17 日  |
| 传统 **Standard** 计划                           | 2025 年 2 月 17 日  |
| 传统 **Enterprise** 和 **Premium** 计划 | 2026 年 1 月 15 日  |

一旦传统支持计划关闭，TiDB Cloud 将不再支持它。如果您在相关关闭日期之前没有迁移到 Connected Care 中的任何支持计划，您将自动迁移到 Connected Care 中的 **Basic** 支持计划。

## 常见问题

### 如何查看或更改我当前的支持计划？

在 [TiDB Cloud 控制台](https://tidbcloud.com/)中，点击左下角的**支持**。将显示**支持**页面，您当前的支持计划会用 **CURRENT** 标签突出显示。

您可以在**支持**页面上迁移到新的支持计划，但 **Premium** 支持计划除外。要升级到 **Premium** 计划，请[联系销售](https://www.pingcap.com/contact-us)。

### 我需要为类似的服务支付更多费用吗？

虽然新的 Connected Care 服务提供了更全面和功能更丰富的支持体验，但定价仍与之前的产品保持一致。TiDB Cloud 仍然致力于提供更多价值，以更好地支持您的发展历程。

### 传统 **Basic** 计划关闭后，我如何获得技术支持？

您仍然可以获得[账单和账户支持](/tidb-cloud/tidb-cloud-support.md#create-an-account-or-billing-support-ticket)。对于技术支持，请考虑购买 Connected Care 服务中的支持计划。建议您从包含一个月免费试用的 **Developer** 计划开始。
