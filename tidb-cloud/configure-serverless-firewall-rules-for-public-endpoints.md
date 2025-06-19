---
title: 为 TiDB Cloud Serverless 公共端点配置防火墙规则
summary: 了解如何安全地配置和管理 TiDB Cloud Serverless 集群的公共访问防火墙规则。
---

# 为 TiDB Cloud Serverless 公共端点配置防火墙规则

本文档介绍 TiDB Cloud Serverless 的公共连接选项。你将了解通过互联网安全管理 TiDB Cloud Serverless 集群访问的关键概念。

> **注意：**
>
> 本文档适用于 **TiDB Cloud Serverless**。有关配置 **TiDB Cloud Dedicated** IP 访问列表的说明，请参阅[为 TiDB Cloud Dedicated 配置 IP 访问列表](/tidb-cloud/configure-ip-access-list.md)。

## 公共端点

在 TiDB Cloud Serverless 集群上配置公共访问允许通过公共端点访问集群。也就是说，可以通过互联网访问集群。公共端点是一个可公开解析的 DNS 地址。"授权网络"是指你选择允许访问集群的 IP 地址范围。这些权限通过**防火墙规则**强制执行。

### 公共访问的特点

- 只有指定的 IP 地址可以访问 TiDB Cloud Serverless。
    - 默认情况下，允许所有 IP 地址（`0.0.0.0 - 255.255.255.255`）。
    - 你可以在集群创建后更新允许的 IP 地址。
- 你的集群有一个可公开解析的 DNS 名称。
- 进出集群的网络流量通过**公共互联网**而不是私有网络路由。

### 防火墙规则

通过**防火墙规则**授予对 IP 地址的访问权限。如果连接尝试来自未经批准的 IP 地址，客户端将收到错误。

你最多可以创建 200 条 IP 防火墙规则。

### 允许 AWS 访问

你可以通过参考官方 [AWS IP 地址列表](https://docs.aws.amazon.com/vpc/latest/userguide/aws-ip-ranges.html)启用来自**所有 AWS IP 地址**的访问。

TiDB Cloud 定期更新此列表，并使用保留的 IP 地址 **169.254.65.87** 代表所有 AWS IP 地址。

## 创建和管理防火墙规则

本节介绍如何管理 TiDB Cloud Serverless 集群的防火墙规则。使用公共端点时，对 TiDB Cloud Serverless 集群的连接仅限于防火墙规则中指定的 IP 地址。

要向 TiDB Cloud Serverless 集群添加防火墙规则，请执行以下步骤：

1. 导航到[**集群**](https://tidbcloud.com/project/clusters)页面，然后点击目标集群的名称以进入其概览页面。

2. 在左侧导航栏中，点击**设置** > **网络**。

3. 在**网络**页面上，如果**公共端点**已禁用，请启用它。在**授权网络**中，点击**+ 添加当前 IP**。这将自动创建一条包含你的计算机公共 IP 地址（由 TiDB Cloud 感知）的防火墙规则。

    > **注意：**
    >
    > 在某些情况下，TiDB Cloud 控制台观察到的 IP 地址与访问互联网时使用的 IP 地址不同。因此，你可能需要更改起始和结束 IP 地址，以使规则按预期运行。你可以使用搜索引擎或其他在线工具检查自己的 IP 地址。例如，搜索"我的 IP 是什么"。

4. 点击**添加规则**以添加更多地址范围。在显示的窗口中，你可以指定单个 IP 地址或 IP 地址范围。如果要将规则限制为单个 IP 地址，请在**起始 IP 地址**和**结束 IP 地址**字段中输入相同的 IP 地址。打开防火墙后，管理员、用户和应用程序可以访问你的 TiDB Cloud Serverless 集群上拥有有效凭据的任何数据库。点击**提交**以添加防火墙规则。

## 下一步

- [通过公共端点连接到 TiDB Cloud Serverless](/tidb-cloud/connect-via-standard-connection-serverless.md)
