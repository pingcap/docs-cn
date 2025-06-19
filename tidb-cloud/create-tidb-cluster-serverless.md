---
title: 创建 TiDB Cloud Serverless 集群
summary: 了解如何创建 TiDB Cloud Serverless 集群。
---

# 创建 TiDB Cloud Serverless 集群

本文档介绍如何在 [TiDB Cloud 控制台](https://tidbcloud.com/)中创建 TiDB Cloud Serverless 集群。

> **提示：**
>
> 要了解如何创建 TiDB Cloud Dedicated 集群，请参见[创建 TiDB Cloud Dedicated 集群](/tidb-cloud/create-tidb-cluster.md)。

## 开始之前

如果您还没有 TiDB Cloud 账户，请点击[此处](https://tidbcloud.com/signup)注册账户。

- 您可以使用电子邮件和密码注册，这样您就可以使用 TiDB Cloud 管理您的密码，也可以使用您的 Google、GitHub 或 Microsoft 账户注册。
- 对于 AWS Marketplace 用户，您也可以通过 AWS Marketplace 注册。为此，在 [AWS Marketplace](https://aws.amazon.com/marketplace) 中搜索 `TiDB Cloud`，订阅 TiDB Cloud，然后按照屏幕上的说明设置您的 TiDB Cloud 账户。
- 对于 Azure Marketplace 用户，您也可以通过 Azure Marketplace 注册。为此，在 [Azure Marketplace](https://azuremarketplace.microsoft.com) 中搜索 `TiDB Cloud`，订阅 TiDB Cloud，然后按照屏幕上的说明设置您的 TiDB Cloud 账户。
- 对于 Google Cloud Marketplace 用户，您也可以通过 Google Cloud Marketplace 注册。为此，在 [Google Cloud Marketplace](https://console.cloud.google.com/marketplace) 中搜索 `TiDB Cloud`，订阅 TiDB Cloud，然后按照屏幕上的说明设置您的 TiDB Cloud 账户。

## 步骤

如果您是 `Organization Owner` 或 `Project Owner` 角色，您可以按照以下步骤创建 TiDB Cloud Serverless 集群：

1. 登录 [TiDB Cloud 控制台](https://tidbcloud.com/)，然后导航到[**集群**](https://tidbcloud.com/project/clusters)页面。

2. 点击**创建集群**。

3. 在**创建集群**页面上，默认选择 **Serverless**。

4. TiDB Cloud Serverless 的云服务提供商是 AWS。您可以选择要托管集群的 AWS 区域。

5. 如有必要，更新默认的集群名称。

6. 选择集群方案。TiDB Cloud Serverless 提供两种[集群方案](/tidb-cloud/select-cluster-tier.md#cluster-plans)：**免费集群**和**可扩展集群**。您可以从免费集群开始，随着需求增长再升级到可扩展集群。要创建可扩展集群，您需要指定**每月支出限额**并添加信用卡。

    > **注意：**
    >
    > 对于 TiDB Cloud 中的每个组织，默认情况下您最多可以创建五个[免费集群](/tidb-cloud/select-cluster-tier.md#free-cluster-plan)。要创建更多 TiDB Cloud Serverless 集群，您需要添加信用卡并创建[可扩展集群](/tidb-cloud/select-cluster-tier.md#scalable-cluster-plan)。

7. 点击**创建**。

    集群创建过程开始，您的 TiDB Cloud 集群将在大约 30 秒内创建完成。

## 下一步

集群创建完成后，按照[通过公共端点连接到 TiDB Cloud Serverless](/tidb-cloud/connect-via-standard-connection-serverless.md)中的说明为您的集群创建密码。

> **注意：**
>
> 如果您不设置密码，将无法连接到集群。
