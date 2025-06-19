---
title: TiDB Cloud 常见问题
summary: 了解关于 TiDB Cloud 的最常见问题（FAQ）。
---

# TiDB Cloud 常见问题

<!-- markdownlint-disable MD026 -->

本文列出了关于 TiDB Cloud 的最常见问题。

## 一般问题

### 什么是 TiDB Cloud？

TiDB Cloud 通过完全托管的云实例使部署、管理和维护 TiDB 集群变得更加简单，你可以通过直观的控制台来控制它。你可以轻松地在 Amazon Web Services (AWS)、Google Cloud 或 Microsoft Azure 上部署，快速构建关键任务应用程序。

TiDB Cloud 使得几乎不需要培训的开发人员和 DBA 也能轻松处理曾经复杂的任务，如基础设施管理和集群部署，从而专注于你的应用程序，而不是数据库的复杂性。通过简单的点击按钮即可扩展或收缩 TiDB 集群，你不再浪费昂贵的资源，因为你可以根据需要的容量和时间来配置数据库。

### TiDB 和 TiDB Cloud 之间是什么关系？

TiDB 是一个开源数据库，是希望在自己的数据中心、自管理的云环境或两者混合环境中运行 TiDB Self-Managed 的组织的最佳选择。

TiDB Cloud 是 TiDB 的完全托管的云数据库即服务。它具有易于使用的基于 Web 的管理控制台，让你可以管理关键任务生产环境的 TiDB 集群。

### TiDB Cloud 是否与 MySQL 兼容？

目前，TiDB Cloud 支持大部分 MySQL 5.7 和 MySQL 8.0 语法，但不支持触发器、存储过程和用户定义函数。更多详细信息，请参见[与 MySQL 的兼容性](/mysql-compatibility.md)。

### 我可以使用哪些编程语言来使用 TiDB Cloud？

你可以使用任何支持 MySQL 客户端或驱动程序的语言。

### 我可以在哪里运行 TiDB Cloud？

TiDB Cloud 目前可在 Amazon Web Services (AWS)、Google Cloud 和 Microsoft Azure 上使用。

### TiDB Cloud 是否支持不同云服务提供商之间的 VPC 对等连接？

不支持。

### TiDB Cloud 支持哪些版本的 TiDB？

- 从 2025 年 1 月 2 日起，新建 TiDB Cloud Dedicated 集群的默认 TiDB 版本是 [v8.1.2](https://docs.pingcap.com/tidb/v8.1/release-8.1.2)。
- 从 2024 年 2 月 21 日起，TiDB Cloud Serverless 集群的 TiDB 版本是 [v7.1.3](https://docs.pingcap.com/tidb/v7.1/release-7.1.3)。

更多信息，请参见 [TiDB Cloud 发布说明](/tidb-cloud/tidb-cloud-release-notes.md)。

### 哪些公司在生产环境中使用 TiDB 或 TiDB Cloud？

TiDB 受到全球超过 1500 家企业的信任，涉及金融服务、游戏和电子商务等各个行业。我们的用户包括 Square（美国）、Shopee（新加坡）和中国银联（中国）。具体详情请参见我们的[案例研究](https://www.pingcap.com/customers/)。

### SLA 是什么样的？

TiDB Cloud 提供 99.99% 的 SLA。详情请参见 [TiDB Cloud 服务的服务级别协议](https://www.pingcap.com/legal/service-level-agreement-for-tidb-cloud-services/)。

### TiDB Cloud 中的 BETA 是什么意思？

BETA 是 TiDB Cloud 功能或产品在正式发布（GA）之前的公开预览阶段。

### 如何了解更多关于 TiDB Cloud 的信息？

了解 TiDB Cloud 的最好方法是按照我们的分步教程进行操作。查看以下主题以开始：

- [TiDB Cloud 简介](/tidb-cloud/tidb-cloud-intro.md)
- [开始使用](/tidb-cloud/tidb-cloud-quickstart.md)
- [创建 TiDB Cloud Serverless 集群](/tidb-cloud/create-tidb-cluster-serverless.md)

### 删除集群时提到的 `XXX's Org/default project/Cluster0` 是什么意思？

在 TiDB Cloud 中，集群由组织名称、项目名称和集群名称的组合唯一标识。为确保你删除的是预期的集群，你需要提供该集群的完全限定名称，例如 `XXX's Org/default project/Cluster0`。

## 架构问题

### 我的 TiDB 集群中有不同的组件。TiDB、TiKV 和 TiFlash 节点是什么？

TiDB 是 SQL 计算层，用于聚合从 TiKV 或 TiFlash 存储返回的查询数据。TiDB 可以水平扩展；增加 TiDB 节点数量将增加集群可以处理的并发查询数量。

TiKV 是用于存储 OLTP 数据的事务存储。TiKV 中的所有数据都自动维护多个副本（默认为三个副本），因此 TiKV 具有原生高可用性并支持自动故障转移。TiKV 可以水平扩展；增加事务存储数量将增加 OLTP 吞吐量。

TiFlash 是分析存储，它实时从事务存储（TiKV）复制数据，并支持实时 OLAP 工作负载。与 TiKV 不同，TiFlash 以列式存储数据以加速分析处理。TiFlash 也可以水平扩展；增加 TiFlash 节点将增加 OLAP 存储和计算能力。

PD（Placement Driver）是整个 TiDB 集群的"大脑"，因为它存储了集群的元数据。它根据 TiKV 节点实时报告的数据分布状态向特定的 TiKV 节点发送数据调度命令。在 TiDB Cloud 中，每个集群的 PD 由 PingCAP 管理，你无法看到或维护它。

### TiDB 如何在 TiKV 节点之间复制数据？

TiKV 将键值空间划分为键范围，每个键范围被视为一个"Region"。在 TiKV 中，数据分布在集群中的所有节点上，并使用 Region 作为基本单位。PD 负责将 Region 尽可能均匀地分布（调度）到集群中的所有节点上。

TiDB 使用 Raft 共识算法按 Region 复制数据。存储在不同节点上的 Region 的多个副本形成一个 Raft Group。

每个数据更改都记录为一个 Raft 日志。通过 Raft 日志复制，数据被安全可靠地复制到 Raft Group 的多个节点上。

## 高可用性问题

### TiDB Cloud 如何确保高可用性？

TiDB 使用 Raft 共识算法确保数据在 Raft Groups 中的存储具有高可用性和安全复制。数据在 TiKV 节点之间冗余复制，并放置在不同的可用区中，以防止机器或数据中心故障。通过自动故障转移，TiDB 确保你的服务始终在线。

作为软件即服务（SaaS）提供商，我们非常重视数据安全。我们已经建立了 [Service Organization Control (SOC) 2 Type 1 合规](https://www.pingcap.com/press-release/pingcap-successfully-completes-soc-2-type-1-examination-for-tidb-cloud/) 所要求的严格信息安全政策和程序。这确保了你的数据是安全、可用和保密的。

## 迁移问题

### 是否有从其他 RDBMS 迁移到 TiDB Cloud 的简单途径？

TiDB 与 MySQL 高度兼容。你可以从任何 MySQL 兼容的数据库平滑迁移数据到 TiDB，无论数据是来自自托管的 MySQL 实例还是公共云提供的 RDS 服务。更多信息，请参见[使用数据迁移将 MySQL 兼容数据库迁移到 TiDB Cloud](/tidb-cloud/migrate-from-mysql-using-data-migration.md)。

## 备份和恢复问题

### TiDB Cloud 是否支持增量备份？

不支持。如果你需要将数据恢复到集群备份保留期内的任意时间点，你可以使用 PITR（时间点恢复）。更多信息，请参见[在 TiDB Cloud Dedicated 集群中使用 PITR](/tidb-cloud/backup-and-restore.md#turn-on-auto-backup) 或[在 TiDB Cloud Serverless 集群中使用 PITR](/tidb-cloud/backup-and-restore-serverless.md#restore)。

## HTAP 问题

### 如何利用 TiDB Cloud 的 HTAP 功能？

传统上，有两种类型的数据库：在线事务处理（OLTP）数据库和在线分析处理（OLAP）数据库。OLTP 和 OLAP 请求通常在不同的独立数据库中处理。使用这种传统架构，将数据从 OLTP 数据库迁移到数据仓库或数据湖进行 OLAP 是一个漫长且容易出错的过程。

作为混合事务分析处理（HTAP）数据库，TiDB Cloud 通过在 OLTP（TiKV）存储和 OLAP（TiFlash）存储之间自动可靠地复制数据，帮助你简化系统架构，降低维护复杂性，并支持对事务数据进行实时分析。典型的 HTAP 用例包括用户个性化、AI 推荐、欺诈检测、商业智能和实时报告。

有关更多 HTAP 场景，请参考[我们如何构建一个简化数据平台的 HTAP 数据库](https://pingcap.com/blog/how-we-build-an-htap-database-that-simplifies-your-data-platform)。

### 我可以直接将数据导入到 TiFlash 吗？

不可以。当你将数据导入到 TiDB Cloud 时，数据会被导入到 TiKV。导入完成后，你可以使用 SQL 语句指定要复制到 TiFlash 的表。然后，TiDB 会相应地在 TiFlash 中创建指定表的副本。更多信息，请参见[创建 TiFlash 副本](/tiflash/create-tiflash-replicas.md)。

### 我可以将 TiFlash 数据以 CSV 格式导出吗？

不可以。TiFlash 数据无法导出。

## 安全问题

### TiDB Cloud 是否安全？

在 TiDB Cloud 中，所有静态数据都经过加密，所有网络流量都使用传输层安全性（TLS）加密。

- 静态数据加密使用加密存储卷自动完成。
- 客户端和集群之间传输中的数据加密使用 TiDB Cloud Web 服务器 TLS 和 TiDB 集群 TLS 自动完成。

### TiDB Cloud 如何加密我的业务数据？

TiDB Cloud 默认使用存储卷加密来保护你的静态业务数据，包括你的数据库数据和备份数据。TiDB Cloud 要求对传输中的数据使用 TLS 加密，并要求对数据库集群中 TiDB、PD、TiKV 和 TiFlash 之间的数据进行组件级 TLS 加密。

要获取有关 TiDB Cloud 中业务数据加密的更多具体信息，请联系 [TiDB Cloud 支持](/tidb-cloud/tidb-cloud-support.md)。

### TiDB Cloud 支持哪些版本的 TLS？

TiDB Cloud 支持 TLS 1.2 或 TLS 1.3。

### 我可以在我的 VPC 中运行 TiDB Cloud 吗？

不可以。TiDB Cloud 是数据库即服务（DBaaS），只能在 TiDB Cloud VPC 中运行。作为云计算托管服务，TiDB Cloud 提供数据库访问，无需设置物理硬件和安装软件。

### 我的 TiDB 集群是否安全？

在 TiDB Cloud 中，你可以根据需要使用 TiDB Cloud Dedicated 集群或 TiDB Cloud Serverless 集群。

对于 TiDB Cloud Dedicated 集群，TiDB Cloud 通过以下措施确保集群安全：

- 为每个集群创建独立的子账户和 VPC。
- 设置防火墙规则以隔离外部连接。
- 为每个集群创建服务器端 TLS 证书和组件级 TLS 证书，以加密传输中的集群数据。
- 为每个集群提供 IP 访问规则，确保只有允许的源 IP 地址才能访问你的集群。

对于 TiDB Cloud Serverless 集群，TiDB Cloud 通过以下措施确保集群安全：

- 为每个集群创建独立的子账户。
- 设置防火墙规则以隔离外部连接。
- 提供集群服务器 TLS 证书以加密传输中的集群数据。

### 如何连接到 TiDB 集群中的数据库？

<SimpleTab>
<div label="TiDB Cloud Dedicated">

对于 TiDB Cloud Dedicated 集群，连接到集群的步骤简化如下：

1. 授权你的网络。
2. 设置数据库用户和登录凭据。
3. 下载并配置集群服务器的 TLS。
4. 选择一个 SQL 客户端，获取 TiDB Cloud UI 上显示的自动生成的连接字符串，然后使用该字符串通过 SQL 客户端连接到你的集群。

更多信息，请参见[连接到你的 TiDB Cloud Dedicated 集群](/tidb-cloud/connect-to-tidb-cluster.md)。

</div>

<div label="TiDB Cloud Serverless">

对于 TiDB Cloud Serverless 集群，连接到集群的步骤简化如下：

1. 设置数据库用户和登录凭据。
2. 选择一个 SQL 客户端，获取 TiDB Cloud UI 上显示的自动生成的连接字符串，然后使用该字符串通过 SQL 客户端连接到你的集群。

更多信息，请参见[连接到你的 TiDB Cloud Serverless 集群](/tidb-cloud/connect-to-tidb-cluster-serverless.md)。

</div>
</SimpleTab>

## 支持问题

### 为客户提供哪些支持？

TiDB Cloud 由 TiDB 背后的同一团队提供支持，该团队已经为金融服务、电子商务、企业应用和游戏等行业的 1500 多家全球企业运行关键任务用例。TiDB Cloud 为每个用户提供免费的基本支持计划，你可以升级到付费计划以获得扩展服务。更多信息，请参见 [TiDB Cloud 支持](/tidb-cloud/tidb-cloud-support.md)。

### 如何检查 TiDB Cloud 是否宕机？

你可以在[系统状态](https://status.tidbcloud.com/)页面上检查 TiDB Cloud 的当前运行时间状态。
