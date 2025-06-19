---
title: 通过私有端点连接到 TiDB Cloud Serverless
summary: 了解如何通过私有端点连接到您的 TiDB Cloud 集群。
---

# 通过私有端点连接到 TiDB Cloud Serverless

本文档介绍如何通过私有端点连接到您的 TiDB Cloud Serverless 集群。

> **提示：**
>
> - 要了解如何通过 AWS 私有端点连接到 TiDB Cloud Dedicated 集群，请参阅[通过 AWS PrivateLink 连接到 TiDB Cloud Dedicated 集群](/tidb-cloud/set-up-private-endpoint-connections.md)。
> - 要了解如何通过 Azure 私有端点连接到 TiDB Cloud Dedicated 集群，请参阅[通过 Azure Private Link 连接到 TiDB Cloud Dedicated 集群](/tidb-cloud/set-up-private-endpoint-connections-on-azure.md)。
> - 要了解如何通过 Google Cloud 私有端点连接到 TiDB Cloud Dedicated 集群，请参阅[通过 Google Cloud Private Service Connect 连接到 TiDB Cloud Dedicated 集群](/tidb-cloud/set-up-private-endpoint-connections-on-google-cloud.md)。

TiDB Cloud 支持通过 [AWS PrivateLink](https://aws.amazon.com/privatelink/?privatelink-blogs.sort-by=item.additionalFields.createdDate&privatelink-blogs.sort-order=desc) 对托管在 AWS VPC 中的 TiDB Cloud 服务进行高度安全的单向访问，就像该服务在您自己的 VPC 中一样。私有端点会在您的 VPC 中公开，您可以通过获得授权的端点连接到 TiDB Cloud 服务。

在 AWS PrivateLink 的支持下，端点连接是安全且私密的，不会将您的数据暴露在公共互联网上。此外，端点连接支持 CIDR 重叠，更便于网络管理。

私有端点的架构如下：

![私有端点架构](/media/tidb-cloud/aws-private-endpoint-arch.png)

有关私有端点和端点服务的更详细定义，请参阅以下 AWS 文档：

- [什么是 AWS PrivateLink？](https://docs.aws.amazon.com/vpc/latest/privatelink/what-is-privatelink.html)
- [AWS PrivateLink 概念](https://docs.aws.amazon.com/vpc/latest/privatelink/concepts.html)

## 限制

- 目前，TiDB Cloud 仅在端点服务托管在 AWS 时支持通过私有端点连接到 TiDB Cloud Serverless。如果服务托管在 Google Cloud 上，则不适用私有端点。
- 不支持跨区域的私有端点连接。

## 前提条件

确保在您的 AWS VPC 设置中启用了 DNS 主机名和 DNS 解析。在 [AWS 管理控制台](https://console.aws.amazon.com/) 中创建 VPC 时，这些功能默认是禁用的。

## 使用 AWS 设置私有端点

要通过私有端点连接到您的 TiDB Cloud Serverless 集群，请按照以下步骤操作：

1. [选择 TiDB 集群](#步骤-1-选择-tidb-集群)
2. [创建 AWS 接口端点](#步骤-2-创建-aws-接口端点)
3. [连接到您的 TiDB 集群](#步骤-3-连接到您的-tidb-集群)

### 步骤 1. 选择 TiDB 集群

1. 在[**集群**](https://tidbcloud.com/project/clusters)页面，点击目标 TiDB Cloud Serverless 集群的名称以进入其概览页面。
2. 点击右上角的**连接**。将显示连接对话框。
3. 在**连接类型**下拉列表中，选择**私有端点**。
4. 记下**服务名称**、**可用区 ID** 和**区域 ID**。

    > **注意：**
    >
    > 每个 AWS 区域只需要创建一个私有端点，该端点可以由位于同一区域的所有 TiDB Cloud Serverless 集群共享。

### 步骤 2. 创建 AWS 接口端点

<SimpleTab>
<div label="使用 AWS 控制台">

要使用 AWS 管理控制台创建 VPC 接口端点，请执行以下步骤：

1. 登录 [AWS 管理控制台](https://aws.amazon.com/console/)，并在 [https://console.aws.amazon.com/vpc/](https://console.aws.amazon.com/vpc/) 打开 Amazon VPC 控制台。
2. 在导航窗格中点击**端点**，然后点击右上角的**创建端点**。

    将显示**创建端点**页面。

    ![验证端点服务](/media/tidb-cloud/private-endpoint/create-endpoint-2.png)

3. 选择**使用 NLB 和 GWLB 的端点服务**。
4. 输入您在[步骤 1](#步骤-1-选择-tidb-集群)中找到的服务名称。
5. 点击**验证服务**。
6. 在下拉列表中选择您的 VPC。展开**其他设置**并选中**启用 DNS 名称**复选框。
7. 在**子网**区域，选择您的 TiDB 集群所在的可用区，并选择子网 ID。
8. 在**安全组**区域中正确选择您的安全组。

    > **注意：**
    >
    > 确保所选安全组允许来自您的 EC2 实例在端口 4000 上的入站访问。

9. 点击**创建端点**。

</div>
<div label="使用 AWS CLI">

要使用 AWS CLI 创建 VPC 接口端点，请执行以下步骤：

1. 要获取 **VPC ID** 和**子网 ID**，导航到您的 AWS 管理控制台，并在相关部分找到它们。确保填写您在[步骤 1](#步骤-1-选择-tidb-集群)中找到的**可用区 ID**。
2. 复制下面提供的命令，用您获得的信息替换相关参数，然后在终端中执行它。

```bash
aws ec2 create-vpc-endpoint --vpc-id ${your_vpc_id} --region ${region_id} --service-name ${service_name} --vpc-endpoint-type Interface --subnet-ids ${your_subnet_id}
```

> **提示：**
>
> 在运行命令之前，您需要安装并配置 AWS CLI。有关详细信息，请参阅 [AWS CLI 配置基础知识](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-quickstart.html)。

</div>
</SimpleTab>

然后，您可以使用私有 DNS 名称连接到端点服务。

### 步骤 3：连接到您的 TiDB 集群

创建接口端点后，返回 TiDB Cloud 控制台并执行以下步骤：

1. 在[**集群**](https://tidbcloud.com/project/clusters)页面，点击目标集群的名称以进入其概览页面。
2. 点击右上角的**连接**。将显示连接对话框。
3. 在**连接类型**下拉列表中，选择**私有端点**。
4. 在**连接方式**下拉列表中，选择您首选的连接方法。对话框底部将显示相应的连接字符串。
5. 使用连接字符串连接到您的集群。

> **提示：**
>
> 如果您无法连接到集群，原因可能是您在 AWS 中的 VPC 端点的安全组设置不正确。请参阅[此常见问题](#故障排除)获取解决方案。
>
> 创建 VPC 端点时，如果遇到错误 `private-dns-enabled cannot be set because there is already a conflicting DNS domain for gatewayXX-privatelink.XX.prod.aws.tidbcloud.com in the VPC vpc-XXXXX`，这是因为已经创建了私有端点，无需创建新的端点。

## 故障排除

### 启用私有 DNS 后无法通过私有端点连接到 TiDB 集群。为什么？

您可能需要在 AWS 管理控制台中为 VPC 端点正确设置安全组。转到 **VPC** > **端点**。右键单击您的 VPC 端点并选择合适的**管理安全组**。合适的安全组应该是您 VPC 内允许来自 EC2 实例在端口 4000 或客户定义端口上的入站访问的安全组。

![管理安全组](/media/tidb-cloud/private-endpoint/manage-security-groups.png)
