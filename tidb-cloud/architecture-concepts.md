---
title: 架构
summary: 了解 TiDB Cloud 的架构概念。
---

# 架构

TiDB Cloud 是一个全托管的数据库即服务（DBaaS），它将开源 HTAP（混合事务和分析处理）数据库 [TiDB](https://docs.pingcap.com/tidb/stable/overview) 的灵活性和强大功能带到了 AWS、Azure 和 Google Cloud 平台。

TiDB 兼容 MySQL，这使得迁移和使用现有应用程序变得容易，同时提供无缝扩展能力，可以处理从小型工作负载到大规模高性能集群的各种场景。它在一个系统中同时支持事务处理（OLTP）和分析处理（OLAP）工作负载，简化了运维并实现了实时数据洞察。

TiDB Cloud 提供两种部署选项：**TiDB Cloud Serverless**，用于自动扩展、成本效益高的工作负载，以及 **TiDB Cloud Dedicated**，用于具有专用资源和高级功能的企业级应用。TiDB Cloud 让您能够轻松扩展数据库、处理复杂的管理任务，并专注于开发可靠、高性能的应用程序。

## TiDB Cloud Serverless

TiDB Cloud Serverless 是一个全托管的无服务器解决方案，提供与传统 TiDB 类似的 HTAP 功能，同时提供自动扩展功能，以减轻用户在容量规划和管理复杂性方面的负担。它包含一个基础使用的免费层级，对超出免费限制的使用采用基于消费的计费方式。TiDB Cloud Serverless 提供两种高可用性选项以满足不同的运维需求。

默认情况下，使用可用区高可用性选项的集群将所有组件都部署在同一个可用区内，这样可以降低网络延迟。

![TiDB Cloud Serverless 可用区高可用性](/media/tidb-cloud/serverless-zonal-high-avaliability-aws.png)

对于需要最大基础设施隔离和冗余的应用，区域高可用性选项会将节点分布在多个可用区中。

![TiDB Cloud Serverless 区域高可用性](/media/tidb-cloud/serverless-regional-high-avaliability-aws.png)

## TiDB Cloud Dedicated

TiDB Cloud Dedicated 专为关键业务而设计，提供跨多个可用区的高可用性、水平扩展和完整的 HTAP 功能。

它基于隔离的云资源构建，如 VPC、虚拟机、托管 Kubernetes 服务和云存储，充分利用主要云服务提供商的基础设施。TiDB Cloud Dedicated 集群支持完整的 TiDB 功能集，支持快速扩展、可靠备份、在特定 VPC 中部署以及地理级别的灾难恢复。

![TiDB Cloud Dedicated 架构](/media/tidb-cloud/tidb-cloud-dedicated-architecture.png)

## TiDB Cloud 控制台

[TiDB Cloud 控制台](https://tidbcloud.com/)是 TiDB Cloud Serverless 和 TiDB Cloud Dedicated 的基于 Web 的管理界面。它提供了管理集群、导入或迁移数据、监控性能指标、配置备份、设置安全控制以及与其他云服务集成的工具，所有这些都可以在一个用户友好的平台上完成。

## TiDB Cloud CLI（Beta）

TiDB Cloud CLI（`ticloud`）允许您通过简单的命令直接从终端管理 TiDB Cloud Serverless 和 TiDB Cloud Dedicated。您可以执行以下任务：

- 创建、删除和列出集群。
- 向集群导入数据。
- 从集群导出数据。

更多信息，请参见 [TiDB Cloud CLI 参考](/tidb-cloud/cli-reference.md)。

## TiDB Cloud API（Beta）

TiDB Cloud API 是一个基于 REST 的接口，提供了对 TiDB Cloud Serverless 和 TiDB Cloud Dedicated 资源进行编程访问的能力。它支持自动化和高效处理任务，如管理项目、集群、备份、恢复、数据导入、计费以及 [TiDB Cloud 数据服务](/tidb-cloud/data-service-overview.md)中的其他资源。

更多信息，请参见 [TiDB Cloud API 概述](/tidb-cloud/api-overview.md)。

## 节点

在 TiDB Cloud 中，每个集群由 TiDB、TiKV 和 TiFlash 节点组成。

- 在 TiDB Cloud Dedicated 集群中，您可以根据性能需求完全管理专用 TiDB、TiKV 和 TiFlash 节点的数量和大小。更多信息，请参见[可扩展性](/tidb-cloud/scalability-concepts.md)。
- 在 TiDB Cloud Serverless 集群中，TiDB、TiKV 和 TiFlash 节点的数量和大小是自动管理的。这确保了无缝扩展，无需用户处理节点配置或管理任务。

### TiDB 节点

[TiDB 节点](/tidb-computing.md)是一个无状态的 SQL 层，使用 MySQL 兼容的端点连接应用程序。它处理 SQL 查询的解析、优化和创建分布式执行计划等任务。

您可以部署多个 TiDB 节点以实现水平扩展并管理更高的工作负载。这些节点与负载均衡器（如 TiProxy 或 HAProxy）配合使用，提供无缝接口。TiDB 节点本身不存储数据——它们将数据请求转发到 TiKV 节点进行行式存储或 TiFlash 节点进行列式存储。

### TiKV 节点

[TiKV 节点](/tikv-overview.md)是 TiDB 架构中数据存储的核心，作为分布式事务性键值存储引擎，提供可靠性、可扩展性和高可用性。

**主要特性：**

- **基于 Region 的数据存储**

    - 数据被划分为多个 [Region](https://docs.pingcap.com/tidb/dev/glossary#regionpeerraft-group)，每个 Region 覆盖特定的键范围（左闭右开区间：从 `StartKey` 到 `EndKey`）。
    - 每个 TiKV 节点中共存多个 Region，确保高效的数据分布。

- **事务支持**

    - TiKV 节点在键值层面提供原生分布式事务支持，默认隔离级别为快照隔离。
    - TiDB 节点将 SQL 执行计划转换为对 TiKV 节点 API 的调用，实现无缝的 SQL 级事务支持。

- **高可用性**

    - TiKV 节点中的所有数据都会被复制（默认三副本）以确保持久性。
    - TiKV 确保原生高可用性并支持自动故障转移，防止节点故障。

- **可扩展性和可靠性**

    - TiKV 节点设计用于处理不断扩大的数据集，同时保持分布式一致性和容错性。

### TiFlash 节点

[TiFlash 节点](/tiflash/tiflash-overview.md)是 TiDB 架构中的一种专门存储节点。与普通的 TiKV 节点不同，TiFlash 采用列式存储模型，专为分析加速而设计。

**主要特性：**

- **列式存储**

    TiFlash 节点以列式格式存储数据，这使其针对分析查询进行了优化，显著提高了读密集型工作负载的性能。

- **向量搜索索引支持**

    向量搜索索引功能使用表的 TiFlash 副本，支持高级搜索功能，提高复杂分析场景的效率。
