---
title: 将 AWS DMS 连接到 TiDB Cloud 集群
summary: 了解如何使用 AWS Database Migration Service (AWS DMS) 从 TiDB Cloud 迁移数据或将数据迁移到 TiDB Cloud。
---

# 将 AWS DMS 连接到 TiDB Cloud 集群

[AWS Database Migration Service (AWS DMS)](https://aws.amazon.com/dms/) 是一项云服务，可用于迁移关系数据库、数据仓库、NoSQL 数据库和其他类型的数据存储。你可以使用 AWS DMS 从 TiDB Cloud 集群迁移数据或将数据迁移到 TiDB Cloud 集群。本文档描述如何将 AWS DMS 连接到 TiDB Cloud 集群。

## 前提条件

### 具有足够访问权限的 AWS 账户

你需要拥有具有足够权限来管理 DMS 相关资源的 AWS 账户。如果没有，请参考以下 AWS 文档：

- [注册 AWS 账户](https://docs.aws.amazon.com/dms/latest/userguide/CHAP_GettingStarted.SettingUp.html#sign-up-for-aws)
- [AWS Database Migration Service 的身份和访问管理](https://docs.aws.amazon.com/dms/latest/userguide/security-iam.html)

### TiDB Cloud 账户和 TiDB 集群

你需要拥有 TiDB Cloud 账户和 TiDB Cloud Serverless 或 TiDB Cloud Dedicated 集群。如果没有，请参考以下文档创建：

- [创建 TiDB Cloud Serverless 集群](/tidb-cloud/create-tidb-cluster-serverless.md)
- [创建 TiDB Cloud Dedicated 集群](/tidb-cloud/create-tidb-cluster.md)

## 配置网络

在创建 DMS 资源之前，你需要正确配置网络以确保 DMS 可以与 TiDB Cloud 集群通信。如果你不熟悉 AWS，请联系 AWS 支持。以下提供了几种可能的配置供参考。

<SimpleTab>

<div label="TiDB Cloud Serverless">

对于 TiDB Cloud Serverless，客户端可以通过公共端点或私有端点连接到集群。

- 要[通过公共端点连接到 TiDB Cloud Serverless 集群](/tidb-cloud/connect-via-standard-connection-serverless.md)，请执行以下操作之一以确保 DMS 复制实例可以访问互联网。

    - 在公共子网中部署复制实例并启用**公共可访问**。更多信息，请参见[互联网访问配置](https://docs.aws.amazon.com/vpc/latest/userguide/VPC_Internet_Gateway.html#vpc-igw-internet-access)。

    - 在私有子网中部署复制实例并将私有子网中的流量路由到公共子网。在这种情况下，你需要至少三个子网，两个私有子网和一个公共子网。这两个私有子网形成一个复制实例所在的子网组。然后，你需要在公共子网中创建一个 NAT 网关，并将两个私有子网的流量路由到 NAT 网关。更多信息，请参见[从私有子网访问互联网](https://docs.aws.amazon.com/vpc/latest/userguide/nat-gateway-scenarios.html#public-nat-internet-access)。

- 要通过私有端点连接到 TiDB Cloud Serverless 集群，请先[设置私有端点](/tidb-cloud/set-up-private-endpoint-connections-serverless.md)，然后在私有子网中部署复制实例。

</div>

<div label="TiDB Cloud Dedicated">

对于 TiDB Cloud Dedicated，客户端可以通过公共端点、私有端点或 VPC 对等连接连接到集群。

- 要[通过公共端点连接到 TiDB Cloud Dedicated 集群](/tidb-cloud/connect-via-standard-connection.md)，请执行以下操作之一以确保 DMS 复制实例可以访问互联网。此外，你需要将复制实例或 NAT 网关的公共 IP 地址添加到集群的 [IP 访问列表](/tidb-cloud/configure-ip-access-list.md)中。

    - 在公共子网中部署复制实例并启用**公共可访问**。更多信息，请参见[互联网访问配置](https://docs.aws.amazon.com/vpc/latest/userguide/VPC_Internet_Gateway.html#vpc-igw-internet-access)。

    - 在私有子网中部署复制实例并将私有子网中的流量路由到公共子网。在这种情况下，你需要至少三个子网，两个私有子网和一个公共子网。这两个私有子网形成一个复制实例所在的子网组。然后，你需要在公共子网中创建一个 NAT 网关，并将两个私有子网的流量路由到 NAT 网关。更多信息，请参见[从私有子网访问互联网](https://docs.aws.amazon.com/vpc/latest/userguide/nat-gateway-scenarios.html#public-nat-internet-access)。

- 要通过私有端点连接到 TiDB Cloud Dedicated 集群，请先[设置私有端点](/tidb-cloud/set-up-private-endpoint-connections.md)，然后在私有子网中部署复制实例。

- 要通过 VPC 对等连接连接到 TiDB Cloud Dedicated 集群，请先[设置 VPC 对等连接](/tidb-cloud/set-up-vpc-peering-connections.md)，然后在私有子网中部署复制实例。

</div>
</SimpleTab>

## 创建 AWS DMS 复制实例

1. 在 AWS DMS 控制台中，转到[**复制实例**](https://console.aws.amazon.com/dms/v2/home#replicationInstances)页面并切换到相应的区域。建议使用与 TiDB Cloud 相同的区域。

   ![创建复制实例](/media/tidb-cloud/aws-dms-tidb-cloud/aws-dms-connect-replication-instances.png)

2. 点击**创建复制实例**。

3. 填写实例名称、ARN 和描述。

4. 在**实例配置**部分，配置实例：
    - **实例类**：选择适当的实例类。更多信息，请参见[选择复制实例类型](https://docs.aws.amazon.com/dms/latest/userguide/CHAP_ReplicationInstance.Types.html)。
    - **引擎版本**：保持默认配置。
    - **高可用性**：根据业务需求选择**多可用区**或**单可用区**。

5. 在**分配存储 (GiB)** 字段中配置存储。

6. 配置连接和安全。你可以参考[前一节](#配置网络)进行网络配置。

    - **网络类型 - 新**：选择 **IPv4**。
    - **虚拟私有云 (VPC) for IPv4**：选择你需要的 VPC。
    - **复制子网组**：为你的复制实例选择一个子网组。
    - **公共可访问**：根据你的网络配置进行设置。

    ![连接和安全](/media/tidb-cloud/aws-dms-tidb-cloud/aws-dms-connect-connectivity-security.png)

7. 根据需要配置**高级设置**、**维护**和**标签**部分，然后点击**创建复制实例**完成实例创建。

> **注意：**
>
> AWS DMS 还支持无服务器复制。详细步骤请参见[创建无服务器复制](https://docs.aws.amazon.com/dms/latest/userguide/CHAP_Serverless.Components.html#CHAP_Serverless.create)。与复制实例不同，AWS DMS 无服务器复制不提供**公共可访问**选项。

## 创建 TiDB Cloud DMS 端点

对于连接性，将 TiDB Cloud 集群用作源或目标的步骤类似，但 DMS 对源和目标的数据库设置要求有所不同。更多信息，请参见[使用 MySQL 作为源](https://docs.aws.amazon.com/dms/latest/userguide/CHAP_Source.MySQL.html)或[使用 MySQL 作为目标](https://docs.aws.amazon.com/dms/latest/userguide/CHAP_Target.MySQL.html)。将 TiDB Cloud 集群用作源时，你只能**迁移现有数据**，因为 TiDB 不支持 MySQL binlog。

1. 在 AWS DMS 控制台中，转到[**端点**](https://console.aws.amazon.com/dms/v2/home#endpointList)页面并切换到相应的区域。

    ![创建端点](/media/tidb-cloud/aws-dms-tidb-cloud/aws-dms-connect-create-endpoint.png)

2. 点击**创建端点**以创建目标数据库端点。

3. 在**端点类型**部分，选择**源端点**或**目标端点**。

4. 在**端点配置**部分，填写**端点标识符**和 ARN 字段。然后，选择 **MySQL** 作为**源引擎**或**目标引擎**。

5. 对于**访问端点数据库**字段，选中**手动提供访问信息**复选框，并按如下方式填写集群信息：

    <SimpleTab>

    <div label="TiDB Cloud Serverless">

    - **服务器名称**：TiDB Cloud Serverless 集群的 `HOST`。
    - **端口**：TiDB Cloud Serverless 集群的 `PORT`。
    - **用户名**：用于迁移的 TiDB Cloud Serverless 集群用户。确保它满足 DMS 要求。
    - **密码**：TiDB Cloud Serverless 集群用户的密码。
    - **安全套接字层 (SSL) 模式**：如果通过公共端点连接，强烈建议将模式设置为 **verify-full** 以确保传输安全。如果通过私有端点连接，可以将模式设置为 **none**。
    - （可选）**CA 证书**：使用 [ISRG Root X1 证书](https://letsencrypt.org/certs/isrgrootx1.pem)。更多信息，请参见[到 TiDB Cloud Serverless 的 TLS 连接](/tidb-cloud/secure-connections-to-serverless-clusters.md)。

    </div>

    <div label="TiDB Cloud Dedicated">

    - **服务器名称**：TiDB Cloud Dedicated 集群的 `HOST`。
    - **端口**：TiDB Cloud Dedicated 集群的 `PORT`。
    - **用户名**：用于迁移的 TiDB Cloud Dedicated 集群用户。确保它满足 DMS 要求。
    - **密码**：TiDB Cloud Dedicated 集群用户的密码。
    - **安全套接字层 (SSL) 模式**：如果通过公共端点连接，强烈建议将模式设置为 **verify-full** 以确保传输安全。如果通过私有端点连接，可以将其设置为 **none**。
    - （可选）**CA 证书**：根据[到 TiDB Cloud Dedicated 的 TLS 连接](/tidb-cloud/tidb-cloud-tls-connect-to-dedicated.md)获取 CA 证书。

    </div>
    </SimpleTab>

     ![手动提供访问信息](/media/tidb-cloud/aws-dms-tidb-cloud/aws-dms-connect-configure-endpoint.png)

6. 如果要将端点创建为**目标端点**，展开**端点设置**部分，选中**使用端点连接属性**复选框，然后将**额外连接属性**设置为 `Initstmt=SET FOREIGN_KEY_CHECKS=0;`。

7. 根据需要配置 **KMS 密钥**和**标签**部分。点击**创建端点**完成实例创建。
