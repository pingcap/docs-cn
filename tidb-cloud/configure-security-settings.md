---
title: 配置集群密码设置
summary: 了解如何配置连接到集群的 root 密码。
---

# 配置集群密码设置

对于 TiDB Cloud Dedicated 集群，你可以配置 root 密码和允许的 IP 地址来连接到你的集群。

> **注意：**
>
> 对于 TiDB Cloud Serverless 集群，本文档不适用，你可以参考 [TiDB Cloud Serverless 的 TLS 连接](/tidb-cloud/secure-connections-to-serverless-clusters.md)。

1. 在 TiDB Cloud 控制台中，导航到项目的[**集群**](https://tidbcloud.com/project/clusters)页面。

    > **提示：**
    >
    > 你可以使用左上角的组合框在组织、项目和集群之间切换。

2. 在目标集群所在行，点击 **...** 并选择**密码设置**。
3. 设置连接到集群的 root 密码，然后点击**保存**。

    你可以点击**自动生成密码**生成随机密码。生成的密码不会再次显示，因此请将密码保存在安全的位置。

> **提示：**
>
> 如果你正在查看集群的概览页面，也可以点击页面右上角的 **...**，选择**密码设置**，并配置这些设置。
