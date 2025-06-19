---
title: 什么是 TiDB Cloud
summary: 了解 TiDB Cloud 及其架构。
category: intro
---

# 什么是 TiDB Cloud

[TiDB Cloud](https://www.pingcap.com/tidb-cloud/) 是一个全托管的数据库即服务（DBaaS），它将开源的混合事务和分析处理（HTAP）数据库 [TiDB](https://docs.pingcap.com/tidb/stable/overview) 带入云端。TiDB Cloud 提供了一种简单的方式来部署和管理数据库，让您可以专注于应用程序开发，而不是数据库的复杂性。您可以创建 TiDB Cloud 集群，在 Amazon Web Services (AWS)、Google Cloud 和 Microsoft Azure 上快速构建关键任务应用。

![TiDB Cloud 概览](/media/tidb-cloud/tidb-cloud-overview.png)

## 为什么选择 TiDB Cloud

TiDB Cloud 使您无需或仅需少量培训就能轻松处理复杂的任务，如基础设施管理和集群部署。

- 开发人员和数据库管理员（DBA）可以轻松处理大量在线流量，并快速分析跨多个数据集的大量数据。

- 各种规模的企业都可以轻松部署和管理 TiDB Cloud，无需预付费用即可适应业务增长。

观看以下视频了解更多关于 TiDB Cloud 的信息：

<iframe width="600" height="450" src="https://www.youtube.com/embed/skCV9BEmjbo?enablejsapi=1" title="Why TiDB Cloud?" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

使用 TiDB Cloud，您可以获得以下关键特性：

- **快速且可定制的扩展**

    在保持 ACID 事务的同时，可以弹性且透明地扩展到数百个节点以支持关键工作负载。无需考虑分片。您可以根据业务需求分别扩展性能节点和存储节点。

- **MySQL 兼容性**

    借助 TiDB 的 MySQL 兼容性，提高生产力并缩短应用程序的上市时间。无需重写代码即可轻松从现有 MySQL 实例迁移数据。

- **高可用性和可靠性**

    设计上天然具备高可用性。跨多个可用区的数据复制、每日备份和自动故障转移确保业务连续性，无论是硬件故障、网络分区还是数据中心故障。

- **实时分析**

    通过内置分析引擎获得实时分析查询结果。TiDB Cloud 可以在不影响关键任务应用的情况下，对当前数据运行一致的分析查询。

- **企业级安全**

    在专用网络和机器中保护您的数据，支持传输中和静态数据加密。TiDB Cloud 已通过 SOC 2 Type 2、ISO 27001:2013、ISO 27701 认证，并完全符合 GDPR。

- **全托管服务**

    通过易于使用的基于 Web 的管理平台，只需点击几下即可部署、扩展、监控和管理 TiDB 集群。

- **多云支持**

    保持灵活性，避免云厂商锁定。TiDB Cloud 目前可在 AWS、Azure 和 Google Cloud 上使用。

- **简单的定价方案**

    只需为您使用的部分付费，价格透明且无隐藏费用。

- **世界级支持**

    通过我们的支持门户、<a href="mailto:tidbcloud-support@pingcap.com">电子邮件</a>、聊天或视频会议获得世界级支持。

## 部署选项

TiDB Cloud 提供以下两种部署选项：

- [TiDB Cloud Serverless](https://www.pingcap.com/tidb-cloud-serverless)

    TiDB Cloud Serverless 是一个全托管的多租户 TiDB 产品。它提供即时、自动扩展的 MySQL 兼容数据库，并提供慷慨的免费额度，超出免费限制后按使用量计费。

- [TiDB Cloud Dedicated](https://www.pingcap.com/tidb-cloud-dedicated)

    TiDB Cloud Dedicated 适用于生产环境，具有跨可用区高可用性、水平扩展和 [HTAP](https://en.wikipedia.org/wiki/Hybrid_transactional/analytical_processing) 的优势。

有关 TiDB Cloud Serverless 和 TiDB Cloud Dedicated 的功能比较，请参阅 [TiDB：先进的开源分布式 SQL 数据库](https://www.pingcap.com/get-started-tidb)。

## 架构

![TiDB Cloud 架构](/media/tidb-cloud/tidb-cloud-architecture.png)

- TiDB VPC（虚拟私有云）

    对于每个 TiDB Cloud 集群，所有 TiDB 节点和辅助节点（包括 TiDB Operator 节点和日志节点）都部署在同一个 VPC 中。

- TiDB Cloud 中央服务

    中央服务（包括计费、告警、元数据存储、仪表板 UI）是独立部署的。您可以通过互联网访问仪表板 UI 来操作 TiDB 集群。

- 您的 VPC

    您可以通过私有端点连接或 VPC 对等连接来连接您的 TiDB 集群。详情请参阅[设置私有端点连接](/tidb-cloud/set-up-private-endpoint-connections.md)或[设置 VPC 对等连接](/tidb-cloud/set-up-vpc-peering-connections.md)。
