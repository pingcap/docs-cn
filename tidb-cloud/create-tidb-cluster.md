---
title: 创建 TiDB Cloud Dedicated 集群
summary: 了解如何创建 TiDB Cloud Dedicated 集群。
---

# 创建 TiDB Cloud Dedicated 集群

本教程将指导您注册并创建 TiDB Cloud Dedicated 集群。

> **提示：**
>
> 如需了解如何创建 TiDB Cloud Serverless 集群，请参阅[创建 TiDB Cloud Serverless 集群](/tidb-cloud/create-tidb-cluster-serverless.md)。

## 开始之前

如果您还没有 TiDB Cloud 账号，请点击[此处](https://tidbcloud.com/signup)注册账号。

- 您可以使用电子邮件和密码注册，这样可以通过 TiDB Cloud 管理密码，也可以使用 Google、GitHub 或 Microsoft 账号注册。
- 对于 AWS Marketplace 用户，您也可以通过 AWS Marketplace 注册。只需在 [AWS Marketplace](https://aws.amazon.com/marketplace) 中搜索 `TiDB Cloud`，订阅 TiDB Cloud，然后按照屏幕上的说明设置您的 TiDB Cloud 账号。
- 对于 Azure Marketplace 用户，您也可以通过 Azure Marketplace 注册。只需在 [Azure Marketplace](https://azuremarketplace.microsoft.com) 中搜索 `TiDB Cloud`，订阅 TiDB Cloud，然后按照屏幕上的说明设置您的 TiDB Cloud 账号。
- 对于 Google Cloud Marketplace 用户，您也可以通过 Google Cloud Marketplace 注册。只需在 [Google Cloud Marketplace](https://console.cloud.google.com/marketplace) 中搜索 `TiDB Cloud`，订阅 TiDB Cloud，然后按照屏幕上的说明设置您的 TiDB Cloud 账号。

## （可选）步骤 1. 使用默认项目或创建新项目

登录 [TiDB Cloud 控制台](https://tidbcloud.com/)后，您会有一个默认的[项目](/tidb-cloud/tidb-cloud-glossary.md#project)。当您的组织中只有一个项目时，您的集群将在该项目中创建。有关项目的更多信息，请参阅[组织和项目](/tidb-cloud/manage-user-access.md#organizations-and-projects)。

如果您是组织所有者，可以根据需要按照以下步骤重命名默认项目或为集群创建新项目：

1. 在 [TiDB Cloud 控制台](https://tidbcloud.com/)中，点击左上角的组合框。将显示您的默认组织和项目。

2. 点击您组织的名称，然后点击左侧导航栏中的**项目**。

3. 在**项目**页面上，执行以下操作之一：

    - 要重命名默认项目，请在**操作**列中点击 **...** > **重命名**。
    - 要创建项目，请点击**创建新项目**，输入项目名称，然后点击**确认**。

4. 要转到项目的集群列表页面，请在**项目**页面上点击项目名称。

## 步骤 2. 创建 TiDB Cloud Dedicated 集群

如果您是`组织所有者`或`项目所有者`角色，可以按照以下步骤创建 TiDB Cloud Dedicated 集群：

1. 导航到项目的[**集群**](https://tidbcloud.com/project/clusters)页面。

    > **提示：**
    >
    > 您可以使用左上角的组合框在组织、项目和集群之间切换。

2. 点击**创建集群**。

3. 在**创建集群**页面上，选择 **Dedicated**，然后按如下配置集群信息：

    1. 选择云服务提供商和区域。

        > **注意：**
        >
        > - 目前，Azure 上的 TiDB Cloud Dedicated 支持处于公开预览阶段。
        > - 如果您通过 [AWS Marketplace](https://aws.amazon.com/marketplace) 注册了 TiDB Cloud，云服务提供商为 AWS，且无法在 TiDB Cloud 中更改。
        > - 如果您通过 [Azure Marketplace](https://azuremarketplace.microsoft.com) 注册了 TiDB Cloud，云服务提供商为 Azure Cloud，且无法在 TiDB Cloud 中更改。
        > - 如果您通过 [Google Cloud Marketplace](https://console.cloud.google.com/marketplace) 注册了 TiDB Cloud，云服务提供商为 Google Cloud，且无法在 TiDB Cloud 中更改。

    2. 分别为 TiDB、TiKV 和 TiFlash（可选）配置[集群大小](/tidb-cloud/size-your-cluster.md)。
    3. 如有必要，更新默认的集群名称和端口号。
    4. 如果尚未为该区域配置 CIDR，则需要设置 CIDR。如果您没有看到**项目 CIDR**字段，则表示该区域已配置 CIDR。

        > **注意：**
        >
        > - 当在此区域创建第一个集群时，TiDB Cloud 将使用此 CIDR 创建一个 VPC。同一项目在此区域的所有后续集群都将使用此 VPC。
        > - 设置 CIDR 时，避免与应用程序所在 VPC 的 CIDR 发生冲突。VPC 创建后无法修改 CIDR。

4. 确认右侧的集群和计费信息。

5. 如果您尚未添加付款方式，请点击右下角的**添加信用卡**。

    > **注意：**
    >
    > 如果您通过 [AWS Marketplace](https://aws.amazon.com/marketplace)、[Azure Marketplace](https://azuremarketplace.microsoft.com) 或 [Google Cloud Marketplace](https://console.cloud.google.com/marketplace) 注册了 TiDB Cloud，您可以直接通过 AWS 账号、Azure 账号或 Google Cloud 账号付款，但无法在 TiDB Cloud 控制台中添加付款方式或下载发票。

6. 点击**创建**。

    您的 TiDB Cloud 集群将在大约 20 到 30 分钟内创建完成。

## 步骤 3. 设置 root 密码

集群创建完成后，按照以下步骤设置 root 密码：

1. 在集群概览页面的右上角，点击 **...** 并选择**密码设置**。

2. 设置连接集群的 root 密码，然后点击**保存**。

    您可以点击**自动生成密码**生成随机密码。生成的密码不会再次显示，请将密码保存在安全的位置。

## 下一步

在 TiDB Cloud 上创建集群后，您可以通过[连接到 TiDB Cloud Dedicated 集群](/tidb-cloud/connect-to-tidb-cluster.md)中提供的方法连接到集群。
