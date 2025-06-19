---
title: 可扩展性
summary: 了解 TiDB Cloud 的可扩展性概念。
---

# 可扩展性

TiDB Cloud Dedicated 允许你分别调整其计算和存储资源，以适应数据量或工作负载的变化。TiDB Cloud Dedicated 可以在不中断服务的情况下进行扩展。这种灵活性使组织能够在保持高性能和高可用性的同时优化其基础设施成本。

> **注意：**
>
> [TiDB Cloud Serverless](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless) 会根据应用程序的工作负载变化自动扩展。但是，你不能手动扩展 TiDB Cloud Serverless 集群。

> **提示：**
>
> 有关如何确定 TiDB Cloud Dedicated 集群大小的信息，请参见[确定 TiDB 大小](/tidb-cloud/size-your-cluster.md)。

## 垂直和水平扩展

TiDB Cloud Dedicated 支持垂直（向上扩展）和水平（向外扩展）扩展。

- 水平扩展是向专用集群添加节点以分配工作负载的过程。
- 垂直扩展是为专用集群增加 vCPU 和内存的过程。

TiDB Cloud Dedicated 也支持垂直和水平扩展的组合。

## TiDB 可扩展性

TiDB 仅用于计算，不存储数据。你可以配置 TiDB 的节点数量、vCPU 和内存。

通常，TiDB 性能随着 TiDB 节点数量的增加而线性增长。

## TiKV 可扩展性

TiKV 负责存储行式数据。你可以配置 TiKV 的节点数量、vCPU 和内存以及存储。TiKV 节点数量应至少为 1 组（3 个不同可用区中的 3 个节点），并以 3 个节点为单位增加。

TiDB Cloud 将 TiKV 节点均匀部署在你选择的区域中的 3 个可用区，以实现持久性和高可用性。在典型的 3 副本设置中，你的数据在所有可用区的 TiKV 节点之间均匀分布，并持久化到每个 TiKV 节点的磁盘上。虽然 TiKV 主要用于数据存储，但 TiKV 节点的性能也会根据不同的工作负载而变化。

## TiFlash 可扩展性

TiFlash 负责存储列式数据。TiFlash 实时从 TiKV 同步数据，并开箱即支持实时分析工作负载。你可以配置 TiFlash 的节点数量、vCPU 和内存以及存储。

TiDB Cloud 将 TiFlash 节点均匀部署在区域内的不同可用区。建议在每个 TiDB Cloud 集群中至少配置两个 TiFlash 节点，并在生产环境中为数据创建至少两个副本以实现高可用性。
