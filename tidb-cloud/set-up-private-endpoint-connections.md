---
title: 通过 AWS PrivateLink 连接到 TiDB Cloud Dedicated 集群
summary: 了解如何通过 AWS 私有端点连接到 TiDB Cloud 集群。
---

# 通过 AWS PrivateLink 连接到 TiDB Cloud Dedicated 集群

本文介绍如何通过 [AWS PrivateLink](https://aws.amazon.com/privatelink) 连接到 TiDB Cloud Dedicated 集群。

> **提示：**
>
> - 要了解如何通过私有端点连接到 TiDB Cloud Serverless 集群，请参见[通过私有端点连接到 TiDB Cloud Serverless](/tidb-cloud/set-up-private-endpoint-connections-serverless.md)。
> - 要了解如何通过 Azure 私有端点连接到 TiDB Cloud Dedicated 集群，请参见[通过 Azure Private Link 连接到 TiDB Cloud Dedicated 集群](/tidb-cloud/set-up-private-endpoint-connections-on-azure.md)。
> - 要了解如何通过 Google Cloud 私有端点连接到 TiDB Cloud Dedicated 集群，请参见[通过 Google Cloud Private Service Connect 连接到 TiDB Cloud Dedicated 集群](/tidb-cloud/set-up-private-endpoint-connections-on-google-cloud.md)。

TiDB Cloud 支持通过 [AWS PrivateLink](https://aws.amazon.com/privatelink) 安全地单向访问托管在 AWS VPC 中的 TiDB Cloud 服务，就像该服务在您自己的 VPC 中一样。私有端点会在您的 VPC 中公开，您可以通过具有权限的端点连接到 TiDB Cloud 服务。

由 AWS PrivateLink 提供支持的端点连接是安全和私密的，不会将您的数据暴露在公共互联网上。此外，端点连接支持 CIDR 重叠，更易于网络管理。

私有端点的架构如下：

![私有端点架构](/media/tidb-cloud/aws-private-endpoint-arch.png)

有关私有端点和端点服务的更详细定义，请参见以下 AWS 文档：

- [什么是 AWS PrivateLink？](https://docs.aws.amazon.com/vpc/latest/privatelink/what-is-privatelink.html)
- [AWS PrivateLink 概念](https://docs.aws.amazon.com/vpc/latest/privatelink/concepts.html)

## 限制

- 只有 `Organization Owner` 和 `Project Owner` 角色可以创建私有端点。
- 私有端点和要连接的 TiDB 集群必须位于同一区域。

在大多数情况下，建议使用私有端点连接而不是 VPC 对等连接。但是，在以下情况下，您应该使用 VPC 对等连接而不是私有端点连接：

- 您正在使用 [TiCDC](https://docs.pingcap.com/tidb/stable/ticdc-overview) 集群将数据从源 TiDB 集群复制到跨区域的目标 TiDB 集群，以获得高可用性。目前，私有端点不支持跨区域连接。
- 您正在使用 TiCDC 集群将数据复制到下游集群（如 Amazon Aurora、MySQL 和 Kafka），但您无法自行维护端点服务。
- 您正在直接连接到 PD 或 TiKV 节点。

## 前提条件

确保在 AWS VPC 设置中启用了 DNS 主机名和 DNS 解析。在 [AWS 管理控制台](https://console.aws.amazon.com/) 中创建 VPC 时，这些功能默认是禁用的。

## 设置私有端点连接并连接到集群

要通过私有端点连接到 TiDB Cloud Dedicated 集群，请完成以下步骤：

1. [选择 TiDB 集群](#步骤-1-选择-tidb-集群)
2. [创建 AWS 接口端点](#步骤-2-创建-aws-接口端点)
3. [创建私有端点连接](#步骤-3-创建私有端点连接)
4. [启用私有 DNS](#步骤-4-启用私有-dns)
5. [连接到 TiDB 集群](#步骤-5-连接到-tidb-集群)

如果您有多个集群，则需要对要使用 AWS PrivateLink 连接的每个集群重复这些步骤。

### 步骤 1. 选择 TiDB 集群

1. 在项目的[**集群**](https://tidbcloud.com/project/clusters)页面上，点击目标 TiDB 集群的名称以进入其概览页面。
2. 点击右上角的**连接**。此时会显示连接对话框。
3. 在**连接类型**下拉列表中，选择**私有端点**，然后点击**创建私有端点连接**。

> **注意：**
>
> 如果您已经创建了私有端点连接，活动端点将显示在连接对话框中。要创建其他私有端点连接，请点击左侧导航栏中的**设置** > **网络**，导航到**网络**页面。

### 步骤 2. 创建 AWS 接口端点

> **注意：**
>
> 对于 2023 年 3 月 28 日之后创建的每个 TiDB Cloud Dedicated 集群，相应的端点服务会在集群创建后 3 到 4 分钟内自动创建。

如果您看到 `TiDB Private Link Service is ready` 消息，则相应的端点服务已准备就绪。您可以提供以下信息来创建端点。

1. 填写**您的 VPC ID** 和**您的子网 ID** 字段。您可以从 [AWS 管理控制台](https://console.aws.amazon.com/) 找到这些 ID。对于多个子网，请输入以空格分隔的 ID。
2. 点击**生成命令**以获取以下端点创建命令。

    ```bash
    aws ec2 create-vpc-endpoint --vpc-id ${your_vpc_id} --region ${your_region} --service-name ${your_endpoint_service_name} --vpc-endpoint-type Interface --subnet-ids ${your_application_subnet_ids}
    ```

然后，您可以使用 AWS CLI 或 [AWS 管理控制台](https://aws.amazon.com/console/) 创建 AWS 接口端点。

<SimpleTab>
<div label="使用 AWS CLI">

要使用 AWS CLI 创建 VPC 接口端点，请执行以下步骤：

1. 复制生成的命令并在终端中运行。
2. 记录您刚刚创建的 VPC 端点 ID。

> **提示：**
>
> - 运行命令之前，您需要安装并配置 AWS CLI。有关详细信息，请参见 [AWS CLI 配置基础知识](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-quickstart.html)。
>
> - 如果您的服务跨越超过三个可用区（AZ），您将收到一条错误消息，指示 VPC 端点服务不支持子网的可用区。当您选择的区域中除了 TiDB 集群所在的可用区外还有额外的可用区时，就会出现此问题。在这种情况下，您可以联系 [PingCAP 技术支持](https://docs.pingcap.com/tidbcloud/tidb-cloud-support)。

</div>
<div label="使用 AWS 控制台">

要使用 AWS 管理控制台创建 VPC 接口端点，请执行以下步骤：

1. 登录 [AWS 管理控制台](https://aws.amazon.com/console/)，并在 [https://console.aws.amazon.com/vpc/](https://console.aws.amazon.com/vpc/) 打开 Amazon VPC 控制台。
2. 在导航窗格中点击**端点**，然后点击右上角的**创建端点**。

    此时会显示**创建端点**页面。

    ![验证端点服务](/media/tidb-cloud/private-endpoint/create-endpoint-2.png)

3. 在**端点设置**区域，如果需要，填写名称标签，然后选择**使用 NLB 和 GWLB 的端点服务**选项。
4. 在**服务设置**区域，输入生成的命令中的服务名称 `${your_endpoint_service_name}`（`--service-name ${your_endpoint_service_name}`）。
5. 点击**验证服务**。
6. 在**网络设置**区域，从下拉列表中选择您的 VPC。
7. 在**子网**区域，选择 TiDB 集群所在的可用区。

    > **提示：**
    >
    > 如果您的服务跨越超过三个可用区（AZ），您可能无法在**子网**区域中选择可用区。当您选择的区域中除了 TiDB 集群所在的可用区外还有额外的可用区时，就会出现此问题。在这种情况下，请联系 [PingCAP 技术支持](https://docs.pingcap.com/tidbcloud/tidb-cloud-support)。

8. 在**安全组**区域，正确选择您的安全组。

    > **注意：**
    >
    > 确保所选安全组允许来自 EC2 实例的端口 4000 或客户定义端口的入站访问。

9. 点击**创建端点**。

</div>
</SimpleTab>

### 步骤 3. 创建私有端点连接

1. 返回 TiDB Cloud 控制台。
2. 在**创建 AWS 私有端点连接**页面，输入您的 VPC 端点 ID。
3. 点击**创建私有端点连接**。

> **提示：**
>
> 您可以在以下两个页面查看和管理私有端点连接：
>
> - 集群级别的**网络**页面：使用左上角的组合框切换到目标集群，然后点击左侧导航栏中的**设置** > **网络**。
> - 项目级别的**网络访问**页面：使用左上角的组合框切换到目标项目，然后点击左侧导航栏中的**项目设置** > **网络访问**。

### 步骤 4. 启用私有 DNS

在 AWS 中启用私有 DNS。您可以使用 AWS CLI 或 AWS 管理控制台。

<SimpleTab>
<div label="使用 AWS CLI">

要使用 AWS CLI 启用私有 DNS，请从**创建私有端点连接**页面复制以下 `aws ec2 modify-vpc-endpoint` 命令并在 AWS CLI 中运行。

```bash
aws ec2 modify-vpc-endpoint --vpc-endpoint-id ${your_vpc_endpoint_id} --private-dns-enabled
```

或者，您可以在集群的**网络**页面上找到该命令。找到私有端点，然后在**操作**列中点击 **...*** > **启用 DNS**。

</div>
<div label="使用 AWS 控制台">

要在 AWS 管理控制台中启用私有 DNS：

1. 转到 **VPC** > **端点**。
2. 右键点击您的端点 ID，然后选择**修改私有 DNS 名称**。
3. 选中**为此端点启用**复选框。
4. 点击**保存更改**。

    ![启用私有 DNS](/media/tidb-cloud/private-endpoint/enable-private-dns.png)

</div>
</SimpleTab>

### 步骤 5. 连接到 TiDB 集群

接受私有端点连接后，您将被重定向回连接对话框。

1. 等待私有端点连接状态从**系统检查中**变为**活动**（大约 5 分钟）。
2. 在**连接方式**下拉列表中，选择您首选的连接方法。对话框底部将显示相应的连接字符串。
3. 使用连接字符串连接到您的集群。

> **提示：**
>
> 如果无法连接到集群，原因可能是 AWS 中 VPC 端点的安全组设置不正确。有关解决方案，请参见[此常见问题](#故障排除)。

### 私有端点状态参考

使用私有端点连接时，私有端点或私有端点服务的状态会显示在以下页面上：

- 集群级别的**网络**页面：使用左上角的组合框切换到目标集群，然后点击左侧导航栏中的**设置** > **网络**。
- 项目级别的**网络访问**页面：使用左上角的组合框切换到目标项目，然后点击左侧导航栏中的**项目设置** > **网络访问**。

私有端点的可能状态说明如下：

- **未配置**：已创建端点服务但尚未创建私有端点。
- **等待中**：等待处理。
- **活动**：您的私有端点已准备就绪。您无法编辑此状态的私有端点。
- **删除中**：正在删除私有端点。
- **失败**：私有端点创建失败。您可以点击该行的**编辑**重试创建。

私有端点服务的可能状态说明如下：

- **创建中**：正在创建端点服务，需要 3 到 5 分钟。
- **活动**：已创建端点服务，无论是否创建了私有端点。
- **删除中**：正在删除端点服务或集群，需要 3 到 5 分钟。

## 故障排除

### 启用私有 DNS 后无法通过私有端点连接到 TiDB 集群。为什么？

您可能需要在 AWS 管理控制台中为 VPC 端点正确设置安全组。转到 **VPC** > **端点**。右键点击您的 VPC 端点，然后选择适当的**管理安全组**。适当的安全组应该是您 VPC 中允许来自 EC2 实例的端口 4000 或客户定义端口的入站访问的安全组。

![管理安全组](/media/tidb-cloud/private-endpoint/manage-security-groups.png)
