---
title: 通过 Azure Private Link 连接到 TiDB Cloud Dedicated 集群
summary: 了解如何通过 Azure Private Link 连接到 TiDB Cloud Dedicated 集群。
---

# 通过 Azure Private Link 连接到 TiDB Cloud Dedicated 集群

本文档介绍如何通过 [Azure Private Link](https://learn.microsoft.com/en-us/azure/private-link/private-link-overview) 连接到 TiDB Cloud Dedicated 集群。

> **提示：**
>
> - 要了解如何通过 AWS 私有端点连接到 TiDB Cloud Dedicated 集群，请参见[通过 AWS PrivateLink 连接到 TiDB Cloud Dedicated 集群](/tidb-cloud/set-up-private-endpoint-connections.md)。
> - 要了解如何通过 Google Cloud 私有端点连接到 TiDB Cloud Dedicated 集群，请参见[通过 Google Cloud Private Service Connect 连接到 TiDB Cloud Dedicated 集群](/tidb-cloud/set-up-private-endpoint-connections-on-google-cloud.md)。
> - 要了解如何通过私有端点连接到 TiDB Cloud Serverless 集群，请参见[通过私有端点连接到 TiDB Cloud Serverless](/tidb-cloud/set-up-private-endpoint-connections-serverless.md)。

TiDB Cloud 支持通过 [Azure Private Link](https://learn.microsoft.com/en-us/azure/private-link/private-link-overview) 对托管在 Azure 虚拟网络中的 TiDB Cloud 服务进行高度安全和单向访问，就像该服务在您自己的虚拟网络中一样。您可以在您的虚拟网络中创建私有端点，然后通过具有权限的端点连接到 TiDB Cloud 服务。

在 Azure Private Link 的支持下，端点连接是安全和私密的，不会将您的数据暴露在公共互联网上。此外，端点连接支持 CIDR 重叠，并且更易于网络管理。

Azure Private Link 的架构如下：[^1]

![Azure Private Link 架构](/media/tidb-cloud/azure-private-endpoint-arch.png)

有关私有端点和端点服务的更详细定义，请参见以下 Azure 文档：

- [什么是 Azure Private Link](https://learn.microsoft.com/en-us/azure/private-link/private-link-overview)
- [什么是私有端点](https://learn.microsoft.com/en-us/azure/private-link/private-endpoint-overview)
- [创建私有端点](https://learn.microsoft.com/en-us/azure/private-link/create-private-endpoint-portal?tabs=dynamic-ip)

## 限制

- 只有 `Organization Owner` 和 `Project Owner` 角色可以创建私有端点。
- 私有端点和要连接的 TiDB 集群必须位于同一区域。

## 使用 Azure Private Link 设置私有端点

要通过私有端点连接到 TiDB Cloud Dedicated 集群，请完成以下步骤：

1. [选择 TiDB 集群](#步骤-1-选择-tidb-集群)
2. [创建 Azure 私有端点](#步骤-2-创建-azure-私有端点)
3. [接受端点](#步骤-3-接受端点)
4. [连接到 TiDB 集群](#步骤-4-连接到-tidb-集群)

如果您有多个集群，则需要对每个要使用 Azure Private Link 连接的集群重复这些步骤。

### 步骤 1. 选择 TiDB 集群

1. 在项目的[**集群**](https://tidbcloud.com/project/clusters)页面，点击目标 TiDB 集群的名称进入其概览页面。
2. 点击右上角的**连接**。将显示连接对话框。
3. 在**连接类型**下拉列表中，选择**私有端点**，然后点击**创建私有端点连接**打开**创建 Azure 私有端点连接**对话框。

> **注意：**
>
> 如果您已经创建了私有端点连接，活动端点将显示在连接对话框中。要创建其他私有端点连接，请点击左侧导航栏中的**设置** > **网络**导航到**网络**页面。

### 步骤 2. 创建 Azure 私有端点

1. 在**创建 Azure 私有端点连接**对话框中，复制私有链接服务的 TiDB Cloud 资源 ID，并保持对话框打开以供后续使用。

    > **注意：**
    >
    > 对于每个 TiDB Cloud Dedicated 集群，相应的端点服务会在集群创建后 3 到 4 分钟自动创建。

2. 登录 [Azure 门户](https://portal.azure.com/)，然后使用复制的 TiDB Cloud 资源 ID 为您的集群创建私有端点，具体步骤如下：

    1. 在 Azure 门户中，搜索**私有端点**，然后在结果中选择**私有端点**。
    2. 在**私有端点**页面，点击**+ 创建**。
    3. 在**基本信息**标签页中，填写项目和实例信息，然后点击**下一步：资源**。
    4. 在**资源**标签页中，选择**通过资源 ID 或别名连接到 Azure 资源**作为**连接方法**，并将 TiDB Cloud 资源 ID 粘贴到**资源 ID 或别名**字段中。
    5. 继续点击**下一步**浏览其余配置标签页并完成所需设置。然后，点击**创建**以创建和部署私有端点。Azure 可能需要几秒钟才能完成部署。更多信息，请参见 Azure 文档中的[创建私有端点](https://learn.microsoft.com/en-us/azure/private-link/create-private-endpoint-portal?tabs=dynamic-ip#create-a-private-endpoint)。

3. 私有端点创建和部署后，点击**转到资源**，然后执行以下操作：

     - 点击左侧导航栏中的**设置** > **属性**，复制其**资源 ID**以供后续使用。

         ![Azure 私有端点资源 ID](/media/tidb-cloud/azure-private-endpoint-resource-id.png)

     - 点击左侧导航栏中的**设置** > **DNS 配置**，然后复制其 **IP 地址**以供后续使用。

         ![Azure 私有端点 DNS IP](/media/tidb-cloud/azure-private-endpoint-dns-ip.png)

### 步骤 3. 接受端点

1. 返回 TiDB Cloud 控制台中的**创建 Azure 私有端点连接**对话框，然后将复制的**资源 ID** 和 **IP 地址**粘贴到相应字段中。
2. 点击**验证端点**以验证私有端点访问。如果遇到任何错误，请按照错误消息进行故障排除，然后重试。
3. 验证成功后，点击**接受端点**以批准来自私有端点的连接。

### 步骤 4. 连接到 TiDB 集群

接受端点连接后，您将被重定向回连接对话框。

1. 等待私有端点连接状态变为**活动**（大约 5 分钟）。要检查状态，请点击左侧导航栏中的**设置** > **网络**导航到**网络**页面。
2. 在**连接方式**下拉列表中，选择您首选的连接方法。对话框底部将显示相应的连接字符串。
3. 使用连接字符串连接到您的集群。

### 私有端点状态参考

要查看私有端点或私有端点服务的状态，请点击左侧导航栏中的**设置** > **网络**导航到**网络**页面。

私有端点的可能状态说明如下：

- **已发现**：TiDB Cloud 可以在接受请求之前自动检测与端点服务关联的私有端点，以避免需要创建另一个端点。
- **等待中**：等待处理。
- **活动**：您的私有端点已准备就绪可以使用。您无法编辑此状态的私有端点。
- **删除中**：正在删除私有端点。
- **失败**：私有端点创建失败。您可以点击该行的**编辑**重试创建。

私有端点服务的可能状态说明如下：

- **创建中**：正在创建端点服务，这需要 3 到 5 分钟。
- **活动**：端点服务已创建，无论是否已创建私有端点。

## 故障排除

### TiDB Cloud 无法创建端点服务。我该怎么办？

端点服务在您打开**创建 Azure 私有端点**页面并选择 TiDB 集群后自动创建。如果显示失败或长时间保持在**创建中**状态，请[提交支持工单](/tidb-cloud/tidb-cloud-support.md)寻求帮助。

### 如果我在设置过程中取消操作，在接受私有端点之前应该怎么做？

Azure 私有端点连接功能可以自动检测您的私有端点。这意味着在 Azure 门户中[创建 Azure 私有端点](#步骤-2-创建-azure-私有端点)后，如果您在 TiDB Cloud 控制台的**创建 Azure 私有端点连接**对话框中点击**取消**，您仍然可以在**网络**页面上查看已创建的端点。如果取消是无意的，您可以继续配置端点以完成设置。如果取消是有意的，您可以直接在 TiDB Cloud 控制台中删除端点。

[^1]: Azure Private Link 架构图来自 Azure 文档中的 [What is Azure Private Link service](https://learn.microsoft.com/en-us/azure/private-link/private-link-service-overview) 文档（[GitHub 上的源文件](https://github.com/MicrosoftDocs/azure-docs/blob/main/articles/private-link/private-link-service-overview.md)），根据 Creative Commons Attribution 4.0 International 许可证授权。
