---
title: 通过公共连接连接到 TiDB Cloud Dedicated
summary: 了解如何通过公共连接连接到 TiDB Cloud 集群。
---

# 通过公共连接连接到 TiDB Cloud Dedicated

本文档介绍如何通过公共连接连接到 TiDB Cloud Dedicated 集群。公共连接暴露了一个带有流量过滤器的公共端点，因此你可以通过笔记本电脑上的 SQL 客户端连接到 TiDB Cloud Dedicated 集群。

> **提示：**
>
> 要了解如何通过公共连接连接到 TiDB Cloud Serverless 集群，请参阅[通过公共端点连接到 TiDB Cloud Serverless](/tidb-cloud/connect-via-standard-connection-serverless.md)。

## 前提条件：配置 IP 访问列表

对于公共连接，TiDB Cloud Dedicated 只允许来自 IP 访问列表中地址的客户端连接。如果你尚未配置 IP 访问列表，请在首次连接之前按照[配置 IP 访问列表](/tidb-cloud/configure-ip-access-list.md)中的步骤进行配置。

## 连接到集群

要通过公共连接连接到 TiDB Cloud Dedicated 集群，请执行以下步骤：

1. 打开目标集群的概览页面。

    1. 登录 [TiDB Cloud 控制台](https://tidbcloud.com/)，导航到项目的[**集群**](https://tidbcloud.com/project/clusters)页面。

        > **提示：**
        >
        > 你可以使用左上角的组合框在组织、项目和集群之间切换。

    2. 点击目标集群的名称以进入其概览页面。

2. 点击右上角的**连接**。此时会显示一个连接对话框。

3. 在连接对话框中，从**连接类型**下拉列表中选择**公共**。

    如果你尚未配置 IP 访问列表，请点击**配置 IP 访问列表**或按照[配置 IP 访问列表](/tidb-cloud/configure-ip-access-list.md)中的步骤进行配置，然后再进行首次连接。

4. 点击 **CA 证书**下载用于 TLS 连接到 TiDB 集群的 CA 证书。CA 证书默认支持 TLS 1.2 版本。

5. 选择你喜欢的连接方式，然后参考选项卡上的连接字符串和示例代码连接到你的集群。

## 下一步

成功连接到 TiDB 集群后，你可以[使用 TiDB 探索 SQL 语句](/basic-sql-operations.md)。
