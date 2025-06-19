---
title: 配置 IP 访问列表
summary: 了解如何配置允许访问 TiDB Cloud Dedicated 集群的 IP 地址。
---

# 配置 IP 访问列表

对于 TiDB Cloud 中的每个 TiDB Cloud Dedicated 集群，您可以配置 IP 访问列表来过滤尝试访问集群的互联网流量，其工作方式类似于防火墙访问控制列表。配置完成后，只有 IP 地址在 IP 访问列表中的客户端和应用程序才能连接到您的 TiDB Cloud Dedicated 集群。

> **注意：**
>
> 本文适用于 [**TiDB Cloud Dedicated**](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)。有关配置 **TiDB Cloud Serverless** IP 访问列表的说明，请参见[为公共端点配置 TiDB Cloud Serverless 防火墙规则](/tidb-cloud/configure-serverless-firewall-rules-for-public-endpoints.md)。

要为 TiDB Cloud Dedicated 集群配置 IP 访问列表，请执行以下步骤：

1. 导航到[**集群**](https://tidbcloud.com/project/clusters)页面，然后点击目标集群的名称以进入其概览页面。

    > **提示：**
    >
    > 您可以使用左上角的组合框在组织、项目和集群之间切换。

2. 在左侧导航栏中，点击**设置** > **网络**。
3. 在**网络**页面上，点击**添加 IP 地址**。
4. 在显示的对话框中，选择以下选项之一：

    - **允许来自任何地方的访问**：允许所有 IP 地址访问 TiDB Cloud。此选项将您的集群完全暴露在互联网上，风险很高。
    - **使用 IP 地址**（推荐）：您可以添加允许通过 SQL 客户端访问 TiDB Cloud 的 IP 和 CIDR 地址列表。

5. 如果您选择**使用 IP 地址**，请添加 IP 地址或 CIDR 范围，并可选择添加描述。对于每个 TiDB Cloud Dedicated 集群，您最多可以添加 100 个 IP 地址。
6. 点击**确认**以保存更改。
