---
title: 优化 TiDB Cloud Dedicated 的资源分配
summary: 了解如何优化 TiDB Cloud Dedicated 集群的资源分配。
---

# 优化 TiDB Cloud Dedicated 的资源分配

作为一个混合事务和分析处理（HTAP）数据库，[TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群可以支持多个业务应用，每个应用都有不同的服务质量（QoS）要求。在某些情况下，你可能需要为高优先级应用分配更多资源以维持可接受的延迟水平。

TiDB Cloud Dedicated 提供资源优化功能，包括[资源控制](/tidb-resource-control.md)和 [TiDB 节点组](/tidb-cloud/tidb-node-group-overview.md)功能。这些功能帮助你在多业务场景中高效分配资源。

## 使用资源控制

[资源控制](/tidb-resource-control.md)允许你将 TiDB Cloud Dedicated 集群的存储节点（TiKV 或 TiFlash）划分为多个逻辑组。在混合工作负载的系统中，你可以将工作负载分配到不同的资源组，以确保资源隔离并满足 QoS 要求。

如果集群出现意外的 SQL 性能问题，你可以使用 [SQL 绑定](/sql-statements/sql-statement-create-binding.md)或[管理失控查询](/tidb-resource-control.md#manage-queries-that-consume-more-resources-than-expected-runaway-queries)，配合资源组来临时限制特定 SQL 语句的资源消耗。

通过有效使用资源控制，你可以减少集群数量，简化运维，并降低管理成本。

## 使用 TiDB 节点组

[TiDB 节点组](/tidb-cloud/tidb-node-group-overview.md)功能将 TiDB Cloud Dedicated 集群的计算节点（TiDB 层）物理分组。每个组配置特定数量的 TiDB 节点，确保组之间计算资源的物理隔离。

你可以根据业务需求将计算节点划分为多个 TiDB 节点组，并为每个组分配唯一的连接端点。你的应用程序通过各自的端点连接到集群，请求路由到相应的节点组进行处理。这确保了一个组中的资源过度使用不会影响其他组。

## 在资源控制和 TiDB 节点组之间选择

你可以根据应用需求和预算使用资源控制、TiDB 节点组功能或两者的组合来实现资源隔离。

下表比较了资源控制和 TiDB 节点组的功能特点：

| 比较项           | 资源控制         | TiDB 节点组         |
|--------------------------|---------------------------|------------------------|
| 隔离级别   | TiKV 或 TiFlash 逻辑层    | TiDB 节点物理层   |
| 流量控制        | 根据资源组设置的配额控制用户读写请求的流量。 | 不支持。 |
| 配置方式  | 使用 SQL 语句配置  | 通过 TiDB Cloud 控制台配置 |
| 区分工作负载 | 支持在以下级别绑定资源：<ul><li>用户级别。</li><li>会话级别（每个会话设置资源组）。</li><li>语句级别（每个语句设置资源组）。</li></ul>| 为不同工作负载提供不同的连接端点。   |
| 成本       | 无额外成本     | 添加 TiDB 节点会产生相关成本，但创建 TiDB 节点组本身不产生额外成本。       |
