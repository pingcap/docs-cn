---
title: 通过公共端点连接到 TiDB Cloud Serverless
summary: 了解如何通过公共端点连接到您的 TiDB Cloud Serverless 集群。
---

# 通过公共端点连接到 TiDB Cloud Serverless

本文介绍如何通过公共端点从您的计算机使用 SQL 客户端连接到 TiDB Cloud Serverless 集群，以及如何禁用公共端点。

## 通过公共端点连接

> **提示：**
>
> 要了解如何通过公共端点连接到 TiDB Cloud Dedicated 集群，请参见[通过公共连接连接到 TiDB Cloud Dedicated](/tidb-cloud/connect-via-standard-connection.md)。

要通过公共端点连接到 TiDB Cloud Serverless 集群，请执行以下步骤：

1. 导航到[**集群**](https://tidbcloud.com/project/clusters)页面，然后点击目标集群的名称进入其概览页面。

2. 点击右上角的**连接**。将显示连接对话框。

3. 在对话框中，保持连接类型的默认设置为 `Public`，并选择您首选的连接方法和操作系统以获取相应的连接字符串。

    > **注意：**
    >
    > - 将连接类型保持为 `Public` 意味着通过标准 TLS 连接进行连接。更多信息，请参见[到 TiDB Cloud Serverless 的 TLS 连接](/tidb-cloud/secure-connections-to-serverless-clusters.md)。
    > - 如果您在**连接类型**下拉列表中选择**私有端点**，则表示通过私有端点进行连接。更多信息，请参见[通过私有端点连接到 TiDB Cloud Serverless](/tidb-cloud/set-up-private-endpoint-connections-serverless.md)。

4. TiDB Cloud Serverless 允许您为集群创建[分支](/tidb-cloud/branch-overview.md)。创建分支后，您可以通过**分支**下拉列表选择连接到该分支。`main` 代表集群本身。

5. 如果您还没有设置密码，点击**生成密码**生成随机密码。生成的密码不会再次显示，因此请将密码保存在安全的位置。

6. 使用连接字符串连接到您的集群。

    > **注意：**
    >
    > 当您连接到 TiDB Cloud Serverless 集群时，必须在用户名中包含集群的前缀，并用引号将名称括起来。更多信息，请参见[用户名前缀](/tidb-cloud/select-cluster-tier.md#用户名前缀)。
    > 您的客户端 IP 必须在集群公共端点的允许 IP 规则中。更多信息，请参见[为公共端点配置 TiDB Cloud Serverless 防火墙规则](/tidb-cloud/configure-serverless-firewall-rules-for-public-endpoints.md)。

## 禁用公共端点

如果您不需要使用 TiDB Cloud Serverless 集群的公共端点，可以禁用它以防止来自互联网的连接：

1. 导航到[**集群**](https://tidbcloud.com/project/clusters)页面，然后点击目标集群的名称进入其概览页面。

2. 在左侧导航栏中，点击**设置** > **网络**。

3. 在**网络**页面上，点击**禁用**。将显示确认对话框。

4. 在确认对话框中点击**禁用**。

禁用公共端点后，连接对话框中**连接类型**下拉列表中的 `Public` 条目将被禁用。如果用户仍然尝试从公共端点访问集群，他们将收到错误。

> **注意：**
>
> 禁用公共端点不会影响现有连接。它只会阻止来自互联网的新连接。

禁用后，您可以重新启用公共端点：

1. 导航到[**集群**](https://tidbcloud.com/project/clusters)页面，然后点击目标集群的名称进入其概览页面。

2. 在左侧导航栏中，点击**设置** > **网络**。

3. 在**网络**页面上，点击**启用**。

## 下一步

成功连接到 TiDB 集群后，您可以[使用 TiDB 探索 SQL 语句](/basic-sql-operations.md)。
