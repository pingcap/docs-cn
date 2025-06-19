---
title: 通过 VPC 对等连接连接到 TiDB Cloud Dedicated
summary: 了解如何通过 VPC 对等连接连接到 TiDB Cloud Dedicated。
---

# 通过 VPC 对等连接连接到 TiDB Cloud Dedicated

> **注意：**
>
> VPC 对等连接仅适用于在 AWS 和 Google Cloud 上托管的 TiDB Cloud Dedicated 集群。您无法使用 VPC 对等连接连接到在 Azure 上托管的 [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群和 [TiDB Cloud Serverless](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless) 集群。

要通过 VPC 对等连接将应用程序连接到 TiDB Cloud，您需要与 TiDB Cloud 建立 [VPC 对等连接](/tidb-cloud/tidb-cloud-glossary.md#vpc-peering)。本文档将指导您在 [AWS](#在-aws-上设置-vpc-对等连接) 和 [Google Cloud](#在-google-cloud-上设置-vpc-对等连接) 上设置 VPC 对等连接，并通过 VPC 对等连接连接到 TiDB Cloud。

VPC 对等连接是两个 VPC 之间的网络连接，使您能够使用私有 IP 地址在它们之间路由流量。任一 VPC 中的实例都可以相互通信，就像它们在同一网络中一样。

目前，同一项目中同一区域的 TiDB 集群都创建在同一个 VPC 中。因此，一旦在项目的某个区域中设置了 VPC 对等连接，该项目中同一区域创建的所有 TiDB 集群都可以在您的 VPC 中连接。VPC 对等连接的设置因云服务提供商而异。

> **提示：**
>
> 要将应用程序连接到 TiDB Cloud，您还可以与 TiDB Cloud 建立[私有端点连接](/tidb-cloud/set-up-private-endpoint-connections.md)，这种连接方式安全且私密，不会将您的数据暴露在公共互联网上。建议使用私有端点而不是 VPC 对等连接。

## 前提条件：为区域设置 CIDR

CIDR（无类域间路由）是用于为 TiDB Cloud Dedicated 集群创建 VPC 的 CIDR 块。

在向区域添加 VPC 对等连接请求之前，您必须为该区域设置 CIDR 并在该区域创建初始的 TiDB Cloud Dedicated 集群。一旦创建了第一个 Dedicated 集群，TiDB Cloud 将创建该集群的 VPC，允许您建立与应用程序 VPC 的对等连接。

您可以在创建第一个 TiDB Cloud Dedicated 集群时设置 CIDR。如果您想在创建集群之前设置 CIDR，请执行以下操作：

1. 在 [TiDB Cloud 控制台](https://tidbcloud.com)中，使用左上角的组合框切换到目标项目。
2. 在左侧导航栏中，点击**项目设置** > **网络访问**。
3. 在**网络访问**页面，点击**项目 CIDR** 标签页，然后根据您的云服务提供商选择 **AWS** 或 **Google Cloud**。
4. 在右上角，点击**创建 CIDR**。在**创建 AWS CIDR** 或**创建 Google Cloud CIDR** 对话框中指定区域和 CIDR 值，然后点击**确认**。

    ![Project-CIDR4](/media/tidb-cloud/Project-CIDR4.png)

    > **注意：**
    >
    > - 为避免与应用程序所在 VPC 的 CIDR 发生冲突，您需要在此字段中设置不同的项目 CIDR。
    > - 对于 AWS 区域，建议配置 `/16` 到 `/23` 之间的 IP 范围大小。支持的网络地址包括：
    >     - 10.250.0.0 - 10.251.255.255
    >     - 172.16.0.0 - 172.31.255.255
    >     - 192.168.0.0 - 192.168.255.255
    > - 对于 Google Cloud 区域，建议配置 `/19` 到 `/20` 之间的 IP 范围大小。如果您想配置 `/16` 到 `/18` 之间的 IP 范围大小，请联系 [TiDB Cloud 支持团队](/tidb-cloud/tidb-cloud-support.md)。支持的网络地址包括：
    >     - 10.250.0.0 - 10.251.255.255
    >     - 172.16.0.0 - 172.17.255.255
    >     - 172.30.0.0 - 172.31.255.255
    > - TiDB Cloud 根据区域的 CIDR 块大小限制项目中某个区域的 TiDB Cloud 节点数量。

5. 查看云服务提供商和特定区域的 CIDR。

    CIDR 默认处于非活动状态。要激活 CIDR，您需要在目标区域创建一个集群。当区域 CIDR 处于活动状态时，您可以为该区域创建 VPC 对等连接。

    ![Project-CIDR2](/media/tidb-cloud/Project-CIDR2.png)

## 在 AWS 上设置 VPC 对等连接

本节介绍如何在 AWS 上设置 VPC 对等连接。对于 Google Cloud，请参见[在 Google Cloud 上设置 VPC 对等连接](#在-google-cloud-上设置-vpc-对等连接)。

### 步骤 1. 添加 VPC 对等连接请求

您可以在 TiDB Cloud 控制台中的项目级**网络访问**页面或集群级**网络**页面上添加 VPC 对等连接请求。

<SimpleTab>
<div label="在项目级网络访问页面设置 VPC 对等连接">

1. 在 [TiDB Cloud 控制台](https://tidbcloud.com)中，使用左上角的组合框切换到目标项目。
2. 在左侧导航栏中，点击**项目设置** > **网络访问**。
3. 在**网络访问**页面，点击 **VPC 对等连接**标签页，然后点击 **AWS** 子标签页。

    默认显示 **VPC 对等连接**配置。

4. 在右上角，点击**创建 VPC 对等连接**，选择 **TiDB Cloud VPC 区域**，然后填写您现有 AWS VPC 的必需信息：

    - 您的 VPC 区域
    - AWS 账户 ID
    - VPC ID
    - VPC CIDR

    您可以从 [AWS 管理控制台](https://console.aws.amazon.com/) 的 VPC 详情页面获取此类信息。TiDB Cloud 支持在同一区域或不同区域的 VPC 之间创建 VPC 对等连接。

    ![VPC peering](/media/tidb-cloud/vpc-peering/vpc-peering-creating-infos.png)

5. 点击**创建**发送 VPC 对等连接请求，然后在 **VPC 对等连接** > **AWS** 标签页上查看 VPC 对等连接信息。新创建的 VPC 对等连接状态为**系统检查中**。

6. 要查看新创建的 VPC 对等连接的详细信息，请在**操作**列中点击 **...** > **查看**。此时会显示 **VPC 对等连接详情**页面。

</div>
<div label="在集群级网络页面设置 VPC 对等连接">

1. 打开目标集群的概览页面。

    1. 登录 [TiDB Cloud 控制台](https://tidbcloud.com/)并导航到项目的[**集群**](https://tidbcloud.com/project/clusters)页面。

        > **提示：**
        >
        > 您可以使用左上角的组合框在组织、项目和集群之间切换。

    2. 点击目标集群的名称以进入其概览页面。

2. 在左侧导航栏中，点击**设置** > **网络**。

3. 在**网络**页面，点击**创建 VPC 对等连接**，然后填写您现有 AWS VPC 的必需信息：

    - 您的 VPC 区域
    - AWS 账户 ID
    - VPC ID
    - VPC CIDR

    您可以从 [AWS 管理控制台](https://console.aws.amazon.com/) 的 VPC 详情页面获取此类信息。TiDB Cloud 支持在同一区域或不同区域的 VPC 之间创建 VPC 对等连接。

    ![VPC peering](/media/tidb-cloud/vpc-peering/vpc-peering-creating-infos.png)

4. 点击**创建**发送 VPC 对等连接请求，然后在**网络** > **AWS VPC 对等连接**部分查看 VPC 对等连接信息。新创建的 VPC 对等连接状态为**系统检查中**。

5. 要查看新创建的 VPC 对等连接的详细信息，请在**操作**列中点击 **...** > **查看**。此时会显示 **AWS VPC 对等连接详情**页面。

</div>
</SimpleTab>

### 步骤 2. 批准并配置 VPC 对等连接

您可以使用 AWS CLI 或 AWS 控制台批准和配置 VPC 对等连接。

<SimpleTab>
<div label="使用 AWS CLI">

1. 安装 AWS 命令行界面 (AWS CLI)。

    {{< copyable "shell-regular" >}}

    ```bash
    curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
    unzip awscliv2.zip
    sudo ./aws/install
    ```

2. 根据您的账户信息配置 AWS CLI。要获取 AWS CLI 所需的信息，请参见 [AWS CLI 配置基础知识](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-quickstart.html)。

    {{< copyable "shell-regular" >}}

    ```bash
    aws configure
    ```

3. 用您的账户信息替换以下变量值。

    {{< copyable "shell-regular" >}}

    ```bash
    # 设置相关变量。
    pcx_tidb_to_app_id="<TiDB peering id>"
    app_region="<APP Region>"
    app_vpc_id="<Your VPC ID>"
    tidbcloud_project_cidr="<TiDB Cloud Project VPC CIDR>"
    ```

    例如：

    ```
    # 设置相关变量
    pcx_tidb_to_app_id="pcx-069f41efddcff66c8"
    app_region="us-west-2"
    app_vpc_id="vpc-0039fb90bb5cf8698"
    tidbcloud_project_cidr="10.250.0.0/16"
    ```

4. 运行以下命令。

    {{< copyable "shell-regular" >}}

    ```bash
    # 接受 VPC 对等连接请求。
    aws ec2 accept-vpc-peering-connection --vpc-peering-connection-id "$pcx_tidb_to_app_id"
    ```

    {{< copyable "shell-regular" >}}

    ```bash
    # 创建路由表规则。
    aws ec2 describe-route-tables --region "$app_region" --filters Name=vpc-id,Values="$app_vpc_id" --query 'RouteTables[*].RouteTableId' --output text | tr "\t" "\n" | while read row
    do
        app_route_table_id="$row"
        aws ec2 create-route --region "$app_region" --route-table-id "$app_route_table_id" --destination-cidr-block "$tidbcloud_project_cidr" --vpc-peering-connection-id "$pcx_tidb_to_app_id"
    done
    ```

    > **注意：**
    >
    > 有时即使路由表规则创建成功，您可能仍会收到 `An error occurred (MissingParameter) when calling the CreateRoute operation: The request must contain the parameter routeTableId` 错误。在这种情况下，您可以检查已创建的规则并忽略该错误。

    {{< copyable "shell-regular" >}}

    ```bash
    # 修改 VPC 属性以启用 DNS 主机名和 DNS 支持。
    aws ec2 modify-vpc-attribute --vpc-id "$app_vpc_id" --enable-dns-hostnames
    aws ec2 modify-vpc-attribute --vpc-id "$app_vpc_id" --enable-dns-support
    ```

完成配置后，VPC 对等连接已创建。您可以[连接到 TiDB 集群](#连接到-tidb-集群)以验证结果。

</div>
<div label="使用 AWS 控制台">

您也可以使用 AWS 控制台配置 VPC 对等连接。

1. 在 [AWS 管理控制台](https://console.aws.amazon.com/)中确认接受对等连接请求。

    1. 登录 [AWS 管理控制台](https://console.aws.amazon.com/)，点击顶部菜单栏的**服务**。在搜索框中输入 `VPC` 并进入 VPC 服务页面。

        ![AWS dashboard](/media/tidb-cloud/vpc-peering/aws-vpc-guide-1.jpg)

    2. 从左侧导航栏打开**对等连接**页面。在**创建对等连接**标签页上，有一个处于**等待接受**状态的对等连接。

    3. 确认请求者所有者和请求者 VPC 与 [TiDB Cloud 控制台](https://tidbcloud.com) 的 **VPC 对等连接详情**页面上的 **TiDB Cloud AWS 账户 ID** 和 **TiDB Cloud VPC ID** 匹配。右键点击对等连接并在**接受 VPC 对等连接请求**对话框中选择**接受请求**。

        ![AWS VPC peering requests](/media/tidb-cloud/vpc-peering/aws-vpc-guide-3.png)

2. 为每个 VPC 子网路由表添加到 TiDB Cloud VPC 的路由。

    1. 从左侧导航栏打开**路由表**页面。

    2. 搜索属于您的应用程序 VPC 的所有路由表。

        ![Search all route tables related to VPC](/media/tidb-cloud/vpc-peering/aws-vpc-guide-4.png)

    3. 右键点击每个路由表并选择**编辑路由**。在编辑页面上，添加一个目标为 TiDB Cloud CIDR（通过查看 TiDB Cloud 控制台中的 **VPC 对等连接**配置页面）的路由，并在**目标**列中填写您的对等连接 ID。

        ![Edit all route tables](/media/tidb-cloud/vpc-peering/aws-vpc-guide-5.png)

3. 确保已为您的 VPC 启用私有 DNS 托管区域支持。

    1. 从左侧导航栏打开**您的 VPC** 页面。

    2. 选择您的应用程序 VPC。

    3. 右键点击所选的 VPC。显示设置下拉列表。

    4. 从设置下拉列表中，点击**编辑 DNS 主机名**。启用 DNS 主机名并点击**保存**。

    5. 从设置下拉列表中，点击**编辑 DNS 解析**。启用 DNS 解析并点击**保存**。

现在您已成功设置 VPC 对等连接。接下来，[通过 VPC 对等连接连接到 TiDB 集群](#连接到-tidb-集群)。

</div>
</SimpleTab>

## 在 Google Cloud 上设置 VPC 对等连接

### 步骤 1. 添加 VPC 对等连接请求

您可以在 TiDB Cloud 控制台中的项目级**网络访问**页面或集群级**网络**页面上添加 VPC 对等连接请求。

<SimpleTab>
<div label="在项目级网络访问页面设置 VPC 对等连接">

1. 在 [TiDB Cloud 控制台](https://tidbcloud.com)中，使用左上角的组合框切换到目标项目。
2. 在左侧导航栏中，点击**项目设置** > **网络访问**。
3. 在**网络访问**页面，点击 **VPC 对等连接**标签页，然后点击 **Google Cloud** 子标签页。

    默认显示 **VPC 对等连接**配置。

4. 在右上角，点击**创建 VPC 对等连接**，选择 **TiDB Cloud VPC 区域**，然后填写您现有 Google Cloud VPC 的必需信息：

    > **提示：**
    >
    > 您可以按照 **Google Cloud 项目 ID** 和 **VPC 网络名称**字段旁边的说明查找项目 ID 和 VPC 网络名称。

    - Google Cloud 项目 ID
    - VPC 网络名称
    - VPC CIDR

5. 点击**创建**发送 VPC 对等连接请求，然后在 **VPC 对等连接** > **Google Cloud** 标签页上查看 VPC 对等连接信息。新创建的 VPC 对等连接状态为**系统检查中**。

6. 要查看新创建的 VPC 对等连接的详细信息，请在**操作**列中点击 **...** > **查看**。此时会显示 **VPC 对等连接详情**页面。

</div>
<div label="在集群级网络页面设置 VPC 对等连接">

1. 打开目标集群的概览页面。

    1. 登录 [TiDB Cloud 控制台](https://tidbcloud.com/)并导航到项目的[**集群**](https://tidbcloud.com/project/clusters)页面。

        > **提示：**
        >
        > 您可以使用左上角的组合框在组织、项目和集群之间切换。

    2. 点击目标集群的名称以进入其概览页面。

2. 在左侧导航栏中，点击**设置** > **网络**。

3. 在**网络**页面，点击**创建 VPC 对等连接**，然后填写您现有 Google Cloud VPC 的必需信息：

    > **提示：**
    >
    > 您可以按照 **Google Cloud 项目 ID** 和 **VPC 网络名称**字段旁边的说明查找项目 ID 和 VPC 网络名称。

    - Google Cloud 项目 ID
    - VPC 网络名称
    - VPC CIDR

4. 点击**创建**发送 VPC 对等连接请求，然后在**网络** > **Google Cloud VPC 对等连接**部分查看 VPC 对等连接信息。新创建的 VPC 对等连接状态为**系统检查中**。

5. 要查看新创建的 VPC 对等连接的详细信息，请在**操作**列中点击 **...** > **查看**。此时会显示 **Google Cloud VPC 对等连接详情**页面。

</div>
</SimpleTab>

### 步骤 2. 批准 VPC 对等连接

执行以下命令完成 VPC 对等连接的设置：

```bash
gcloud beta compute networks peerings create <your-peer-name> --project <your-project-id> --network <your-vpc-network-name> --peer-project <tidb-project-id> --peer-network <tidb-vpc-network-name>
```

> **注意：**
>
> 您可以根据喜好命名 `<your-peer-name>`。

现在您已成功设置 VPC 对等连接。接下来，[通过 VPC 对等连接连接到 TiDB 集群](#连接到-tidb-集群)。

## 连接到 TiDB 集群

1. 在项目的[**集群**](https://tidbcloud.com/project/clusters)页面，点击目标集群的名称以进入其概览页面。

2. 点击右上角的**连接**，从**连接类型**下拉列表中选择 **VPC 对等连接**。

    等待 VPC 对等连接状态从**系统检查中**变为**活动**（大约需要 5 分钟）。

3. 在**连接方式**下拉列表中，选择您首选的连接方法。对话框底部将显示相应的连接字符串。

4. 使用连接字符串连接到您的集群。
