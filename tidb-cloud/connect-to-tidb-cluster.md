---
title: 连接到您的 TiDB Cloud Dedicated 集群
summary: 了解如何通过不同方法连接到您的 TiDB Cloud Dedicated 集群。
---

# 连接到您的 TiDB Cloud Dedicated 集群

本文档介绍连接到您的 TiDB Cloud Dedicated 集群的方法。

> **提示：**
>
> 要了解如何连接到 TiDB Cloud Serverless 集群，请参见[连接到您的 TiDB Cloud Serverless 集群](/tidb-cloud/connect-to-tidb-cluster-serverless.md)。

在 TiDB Cloud 上创建 TiDB Cloud Dedicated 集群后，您可以通过以下方法之一连接到它：

- 直接连接

    直接连接使用基于 TCP 的 MySQL 原生连接系统。您可以使用任何支持 MySQL 连接的工具连接到您的 TiDB Cloud Dedicated 集群，例如 [MySQL 命令行客户端](https://dev.mysql.com/doc/refman/8.0/en/mysql.html)。TiDB Cloud 还提供 [SQL Shell](/tidb-cloud/connect-via-sql-shell.md)，使您能够尝试 TiDB SQL，快速测试 TiDB 与 MySQL 的兼容性，并管理用户权限。

    TiDB Cloud Dedicated 提供三种网络连接类型：

    - [公共连接](/tidb-cloud/connect-via-standard-connection.md)

        公共连接暴露一个带有流量过滤器的公共端点，因此您可以通过笔记本电脑上的 SQL 客户端连接到您的 TiDB 集群。您可以使用 TLS 连接到您的 TiDB 集群，这确保了从您的应用程序到 TiDB 集群的数据传输安全。更多信息，请参见[通过公共连接连接到 TiDB Cloud Dedicated](/tidb-cloud/connect-via-standard-connection.md)。

    - 私有端点（推荐）

        私有端点连接提供一个私有端点，允许您 VPC 中的 SQL 客户端安全地访问 TiDB Cloud Dedicated 集群。这使用不同云服务提供商提供的私有链接服务，通过简化的网络管理提供高度安全的单向数据库服务访问。

        - 对于托管在 AWS 上的 TiDB Cloud Dedicated 集群，私有端点连接使用 AWS PrivateLink。更多信息，请参见[通过 AWS PrivateLink 连接到 TiDB Cloud Dedicated 集群](/tidb-cloud/set-up-private-endpoint-connections.md)。
        - 对于托管在 Azure 上的 TiDB Cloud Dedicated 集群，私有端点连接使用 Azure Private Link。更多信息，请参见[通过 Azure Private Link 连接到 TiDB Cloud Dedicated 集群](/tidb-cloud/set-up-private-endpoint-connections-on-azure.md)。
        - 对于托管在 Google Cloud 上的 TiDB Cloud Dedicated 集群，私有端点连接使用 Google Cloud Private Service Connect。更多信息，请参见[通过 Google Cloud Private Service Connect 连接到 TiDB Cloud Dedicated 集群](/tidb-cloud/set-up-private-endpoint-connections-on-google-cloud.md)。

    - [VPC 对等连接](/tidb-cloud/set-up-vpc-peering-connections.md)

        如果您想要更低的延迟和更高的安全性，请设置 VPC 对等连接，并通过您云账户中相应云服务提供商的虚拟机实例使用私有端点进行连接。更多信息，请参见[通过 VPC 对等连接连接到 TiDB Cloud Dedicated](/tidb-cloud/set-up-vpc-peering-connections.md)。

- [内置 SQL 编辑器](/tidb-cloud/explore-data-with-chat2query.md)

    > **注意：**
    >
    > 要在 [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群上使用 SQL 编辑器，请联系 [TiDB Cloud 支持](/tidb-cloud/tidb-cloud-support.md)。

    如果您的集群托管在 AWS 上，且集群的 TiDB 版本是 v6.5.0 或更高版本，您可以在 [TiDB Cloud 控制台](https://tidbcloud.com/)中使用 AI 辅助的 SQL 编辑器来最大化您的数据价值。

    在 SQL 编辑器中，您可以手动编写 SQL 查询，或者在 macOS 上简单地按 <kbd>⌘</kbd> + <kbd>I</kbd>（在 Windows 或 Linux 上按 <kbd>Control</kbd> + <kbd>I</kbd>）来指示 [Chat2Query (beta)](/tidb-cloud/tidb-cloud-glossary.md#chat2query) 自动生成 SQL 查询。这使您无需本地 SQL 客户端即可对数据库运行 SQL 查询。您可以直观地以表格或图表形式查看查询结果，并轻松检查查询日志。

## 下一步

成功连接到您的 TiDB 集群后，您可以[使用 TiDB 探索 SQL 语句](/basic-sql-operations.md)。
