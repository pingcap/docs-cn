---
title: TiDB 节点组概览
summary: 了解 TiDB 节点组功能的实现和使用场景。
---

# TiDB 节点组概览

你可以为 [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群创建 TiDB 节点组。TiDB 节点组在物理上对集群的计算节点（TiDB 层）进行分组，每个组包含特定数量的 TiDB 节点。这种配置提供了组之间计算资源的物理隔离，使多业务场景下的资源分配更加高效。

通过 TiDB 节点组，你可以根据业务需求将计算节点划分为多个 TiDB 节点组，并为每个 TiDB 节点组配置唯一的连接端点。你的应用程序通过各自的端点连接到集群，请求会路由到相应的节点组进行处理。这确保了一个组中的资源过度使用不会影响其他组。

> **注意**：
>
> TiDB 节点组功能**不适用于** TiDB Cloud Serverless 集群。

## 实现原理

TiDB 节点组管理 TiDB 节点的分组，并维护端点与其对应 TiDB 节点之间的映射关系。

每个 TiDB 节点组都关联一个专用的负载均衡器。当用户向 TiDB 节点组的端点发送 SQL 请求时，请求首先通过该组的负载均衡器，然后仅路由到该组内的 TiDB 节点。

下图说明了 TiDB 节点组功能的实现原理。

![TiDB 节点组功能的实现原理](/media/tidb-cloud/implementation-of-tidb-node-group.png)

TiDB 节点组中的所有节点都响应来自相应端点的请求。你可以执行以下任务：

- 创建 TiDB 节点组并为其分配 TiDB 节点。
- 为每个组设置连接端点。支持的连接类型包括[公共连接](/tidb-cloud/tidb-node-group-management.md#connect-via-public-connection)、[私有端点](/tidb-cloud/tidb-node-group-management.md#connect-via-private-endpoint)和 [VPC 对等连接](/tidb-cloud/tidb-node-group-management.md#connect-via-vpc-peering)。
- 通过使用不同的端点将应用程序路由到特定组，实现资源隔离。

## 使用场景

TiDB 节点组功能显著增强了 TiDB Cloud Dedicated 集群的资源分配能力。TiDB 节点专门用于计算，不存储数据。通过将节点组织成多个物理组，该功能确保一个组中的资源过度使用不会影响其他组。

使用此功能，你可以：

- 将来自不同系统的多个应用程序整合到一个 TiDB Cloud Dedicated 集群中。随着应用程序工作负载的增长，它不会影响其他应用程序的正常运行。TiDB 节点组功能确保事务应用程序的响应时间不会受到数据分析或批处理应用程序的影响。

- 在 TiDB Cloud Dedicated 集群上执行导入或 DDL 任务，而不影响现有生产工作负载的性能。你可以为导入或 DDL 任务创建一个单独的 TiDB 节点组。即使这些任务消耗大量 CPU 或内存资源，它们也只使用自己 TiDB 节点组中的资源，确保其他 TiDB 节点组中的工作负载不受影响。

- 将所有测试环境合并到一个 TiDB 集群中，或将资源密集型批处理任务组合到一个专用的 TiDB 节点组中。这种方法提高了硬件利用率，降低了运营成本，并确保关键应用程序始终能够访问必要的资源。

此外，TiDB 节点组易于扩容或缩容。对于具有高性能要求的关键应用程序，你可以根据需要为该组分配 TiDB 节点。对于要求较低的应用程序，你可以从少量 TiDB 节点开始，并根据需要进行扩容。高效使用 TiDB 节点组功能可以减少集群数量，简化运维，并降低管理成本。

## 限制和配额

目前，TiDB 节点组功能是免费的。以下是限制和配额：

- 你只能为 AWS 或 Google Cloud 上的 TiDB Cloud Dedicated 集群创建 TiDB 节点组。对其他云提供商的支持计划在不久的将来推出。
- 具有 4 个 vCPU 和 16 GiB 内存的 TiDB 集群不支持 TiDB 节点组功能。
- 默认情况下，你最多可以为一个 TiDB Cloud Dedicated 集群创建五个 TiDB 节点组。如果你需要更多组，请联系 [TiDB Cloud 支持团队](/tidb-cloud/tidb-cloud-support.md)。
- 每个 TiDB 节点组必须至少包含一个 TiDB 节点。虽然一个组中的节点数量没有限制，但 TiDB Cloud Dedicated 集群中的 TiDB 节点总数不得超过 150 个。
- TiDB Cloud 在 TiDB owner 节点上运行自动统计信息收集任务，不考虑节点组边界。这些任务无法在单个 TiDB 节点组内隔离。
- 对于早于 v8.1.2 版本的 TiDB 集群，`ADD INDEX` 任务无法在单个 TiDB 节点组内隔离。

## SLA 影响

根据 TiDB Cloud [服务级别协议 (SLA)](https://www.pingcap.com/legal/service-level-agreement-for-tidb-cloud-services/)，具有多个 TiDB 节点部署的 TiDB Cloud Dedicated 集群的每月正常运行时间百分比可达到 99.99%。但是，在引入 TiDB 节点组后，如果你创建多个 TiDB 节点组，每个组只有 1 个 TiDB 节点，你将失去这些组的高可用性，你的集群的每月正常运行时间百分比将降级为单个 TiDB 节点部署模式（即最高 99.9%）。

为了实现高可用性，建议为每个 TiDB 节点组配置至少两个 TiDB 节点。
