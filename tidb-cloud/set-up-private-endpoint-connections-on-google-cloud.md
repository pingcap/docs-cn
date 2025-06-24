---
title: 通过 Google Cloud Private Service Connect 连接到 TiDB Cloud Dedicated 集群
summary: 了解如何通过 Google Cloud Private Service Connect 连接到 TiDB Cloud 集群。
---

# 通过 Google Cloud Private Service Connect 连接到 TiDB Cloud Dedicated 集群

本文介绍如何通过 [Private Service Connect](https://cloud.google.com/vpc/docs/private-service-connect) 连接到 TiDB Cloud Dedicated 集群。Google Cloud Private Service Connect 是 Google Cloud 提供的私有端点服务。

> **提示：**
>
> - 要了解如何通过 AWS 私有端点连接到 TiDB Cloud Dedicated 集群，请参阅[通过 AWS PrivateLink 连接到 TiDB Cloud Dedicated 集群](/tidb-cloud/set-up-private-endpoint-connections.md)。
> - 要了解如何通过 Azure 私有端点连接到 TiDB Cloud Dedicated 集群，请参阅[通过 Azure Private Link 连接到 TiDB Cloud Dedicated 集群](/tidb-cloud/set-up-private-endpoint-connections-on-azure.md)。
> - 要了解如何通过私有端点连接到 TiDB Cloud Serverless 集群，请参阅[通过私有端点连接到 TiDB Cloud Serverless](/tidb-cloud/set-up-private-endpoint-connections-serverless.md)。

TiDB Cloud 支持通过 [Private Service Connect](https://cloud.google.com/vpc/docs/private-service-connect) 安全地单向访问托管在 Google Cloud VPC 中的 TiDB Cloud 服务。你可以创建一个端点并使用它连接到 TiDB Cloud 服务。

在 Google Cloud Private Service Connect 的支持下，端点连接是安全和私密的，不会将你的数据暴露给公共互联网。此外，端点连接支持 CIDR 重叠，更易于网络管理。

Google Cloud Private Service Connect 的架构如下：[^1]

![Private Service Connect 架构](/media/tidb-cloud/google-cloud-psc-endpoint-overview.png)

有关私有端点和端点服务的更详细定义，请参阅以下 Google Cloud 文档：

- [Private Service Connect](https://cloud.google.com/vpc/docs/private-service-connect)
- [通过端点访问已发布的服务](https://cloud.google.com/vpc/docs/configure-private-service-connect-services)

## 限制

- 此功能适用于 2023 年 4 月 13 日之后创建的 TiDB Cloud Dedicated 集群。对于较旧的集群，请联系 [TiDB Cloud 支持团队](/tidb-cloud/tidb-cloud-support.md)寻求帮助。
- 只有 `Organization Owner` 和 `Project Owner` 角色可以创建 Google Cloud Private Service Connect 端点。
- 每个 TiDB 集群最多可以处理来自 10 个端点的连接。
- 每个 Google Cloud 项目最多可以有 10 个端点连接到一个 TiDB 集群。
- 在配置了端点服务的项目中，你最多可以创建 8 个托管在 Google Cloud 上的 TiDB Cloud Dedicated 集群。
- 私有端点和要连接的 TiDB 集群必须位于同一区域。
- 出站防火墙规则必须允许流量到达端点的内部 IP 地址。[默认允许出站防火墙规则](https://cloud.google.com/firewall/docs/firewalls#default_firewall_rules)允许出站流量到达任何目标 IP 地址。
- 如果你在 VPC 网络中创建了出站拒绝防火墙规则，或者创建了修改默认允许出站行为的分层防火墙策略，可能会影响对端点的访问。在这种情况下，你需要创建特定的出站允许防火墙规则或策略，以允许流量到达端点的内部目标 IP 地址。

在大多数情况下，建议使用私有端点连接而不是 VPC 对等连接。但是，在以下情况下，你应该使用 VPC 对等连接而不是私有端点连接：

- 你正在使用 [TiCDC](https://docs.pingcap.com/tidb/stable/ticdc-overview) 集群跨区域将数据从源 TiDB 集群复制到目标 TiDB 集群，以获得高可用性。目前，私有端点不支持跨区域连接。
- 你正在使用 TiCDC 集群将数据复制到下游集群（如 Amazon Aurora、MySQL 和 Kafka），但你无法自行维护下游的端点服务。

## 使用 Google Cloud Private Service Connect 设置私有端点

要通过私有端点连接到 TiDB Cloud Dedicated 集群，请完成[前提条件](#前提条件)并按照以下步骤操作：

1. [选择 TiDB 集群](#步骤-1-选择-tidb-集群)
2. [创建 Google Cloud 私有端点](#步骤-2-创建-google-cloud-私有端点)
3. [接受端点访问](#步骤-3-接受端点访问)
4. [连接到 TiDB 集群](#步骤-4-连接到-tidb-集群)

如果你有多个集群，需要对每个要使用 Google Cloud Private Service Connect 连接的集群重复这些步骤。

### 前提条件

在开始创建端点之前：

- 在你的 Google Cloud 项目中[启用](https://console.cloud.google.com/apis/library/compute.googleapis.com)以下 API：
    - [Compute Engine API](https://cloud.google.com/compute/docs/reference/rest/v1)
    - [Service Directory API](https://cloud.google.com/service-directory/docs/reference/rest)
    - [Cloud DNS API](https://cloud.google.com/dns/docs/reference/v1)

- 准备以下具有创建端点所需权限的 [IAM 角色](https://cloud.google.com/iam/docs/understanding-roles)。

    - 任务：
        - 创建端点
        - 自动或手动配置端点的 [DNS 条目](https://cloud.google.com/vpc/docs/configure-private-service-connect-services#dns-endpoint)
    - 所需的 IAM 角色：
        - [Compute Network Admin](https://cloud.google.com/iam/docs/understanding-roles#compute.networkAdmin) (roles/compute.networkAdmin)
        - [Service Directory Editor](https://cloud.google.com/iam/docs/understanding-roles#servicedirectory.editor) (roles/servicedirectory.editor)

### 步骤 1：选择 TiDB 集群

1. 在项目的[**集群**](https://tidbcloud.com/project/clusters)页面，点击目标 TiDB 集群的名称进入其概览页面。你可以选择具有以下任一状态的集群：

    - **可用**
    - **恢复中**
    - **修改中**
    - **导入中**

2. 点击右上角的**连接**。此时会显示一个连接对话框。

3. 在**连接类型**下拉列表中，选择**私有端点**，然后点击**创建私有端点连接**。

    > **注意：**
    >
    > 如果你已经创建了私有端点连接，活动端点将显示在连接对话框中。要创建其他私有端点连接，请点击左侧导航栏中的**设置** > **网络**导航到**网络**页面。

### 步骤 2：创建 Google Cloud 私有端点

1. 提供以下信息以生成私有端点创建命令：
    - **Google Cloud 项目 ID**：与你的 Google Cloud 账户关联的项目 ID。你可以在 [Google Cloud **仪表板**页面](https://console.cloud.google.com/home/dashboard)找到该 ID。
    - **Google Cloud VPC 名称**：指定项目中的 VPC 名称。你可以在 [Google Cloud **VPC 网络**页面](https://console.cloud.google.com/networking/networks/list)找到它。
    - **Google Cloud 子网名称**：指定 VPC 中的子网名称。你可以在 **VPC 网络详情**页面找到它。
    - **Private Service Connect 端点名称**：为要创建的私有端点输入一个唯一名称。
2. 输入信息后，点击**生成命令**。
3. 复制生成的命令。
4. 打开 [Google Cloud Shell](https://console.cloud.google.com/home/dashboard) 并执行命令以创建私有端点。

### 步骤 3：接受端点访问

在 Google Cloud Shell 中成功执行命令后，返回 TiDB Cloud 控制台，然后点击**接受端点访问**。

如果你看到错误 `not received connection request from endpoint`，请确保你已正确复制命令并在 Google Cloud Shell 中成功执行。

### 步骤 4：连接到 TiDB 集群

接受私有端点连接后，你将被重定向回连接对话框。

1. 等待私有端点连接状态从**系统检查中**变为**活动**（大约 5 分钟）。
2. 在**连接方式**下拉列表中，选择你偏好的连接方法。对话框底部将显示相应的连接字符串。
3. 使用连接字符串连接到你的集群。

### 私有端点状态参考

使用私有端点连接时，私有端点或私有端点服务的状态会显示在[**私有端点**页面](#前提条件)上。

私有端点的可能状态说明如下：

- **等待中**：等待处理。
- **活动**：你的私有端点已准备就绪可以使用。你无法编辑此状态的私有端点。
- **删除中**：正在删除私有端点。
- **失败**：私有端点创建失败。你可以点击该行的**编辑**重试创建。

私有端点服务的可能状态说明如下：

- **创建中**：正在创建端点服务，需要 3 到 5 分钟。
- **活动**：端点服务已创建，无论私有端点是否创建。

## 故障排除

### TiDB Cloud 无法创建端点服务。我该怎么办？

在你打开**创建 Google Cloud 私有端点连接**页面并选择 TiDB 集群后，端点服务会自动创建。如果显示失败或长时间保持在**创建中**状态，请[提交支持工单](/tidb-cloud/tidb-cloud-support.md)寻求帮助。

### 在 Google Cloud 中创建端点失败。我该怎么办？

要排查问题，你需要查看在 Google Cloud Shell 中执行私有端点创建命令后返回的错误消息。如果是权限相关的错误，你必须在重试之前授予必要的权限。

### 我取消了一些操作。在接受端点访问之前，如何处理取消？

已取消操作的未保存草稿不会被保留或显示。下次在 TiDB Cloud 控制台创建新的私有端点时，你需要重复每个步骤。

如果你已经在 Google Cloud Shell 中执行了创建私有端点的命令，你需要在 Google Cloud 控制台中手动[删除相应的端点](https://cloud.google.com/vpc/docs/configure-private-service-connect-services#delete-endpoint)。

### 为什么我在 TiDB Cloud 控制台中看不到通过直接复制服务附件生成的端点？

在 TiDB Cloud 控制台中，你只能查看通过**创建 Google Cloud 私有端点连接**页面生成的命令创建的端点。

但是，通过直接复制服务附件生成的端点（即不是通过 TiDB Cloud 控制台生成的命令创建的）不会显示在 TiDB Cloud 控制台中。

[^1]: Google Cloud Private Service Connect 架构图来自 Google Cloud 文档中的 [Private Service Connect](https://cloud.google.com/vpc/docs/private-service-connect) 文档，根据 Creative Commons Attribution 4.0 International 许可。
