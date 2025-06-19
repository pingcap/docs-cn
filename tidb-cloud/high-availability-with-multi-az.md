---
title: TiDB Cloud Dedicated 中的高可用性
summary: TiDB Cloud Dedicated 通过多可用区部署支持高可用性。
---

# TiDB Cloud Dedicated 中的高可用性

TiDB 使用 Raft 共识算法确保数据在 Raft 组中的存储具有高可用性和安全复制。数据在存储节点之间冗余复制，并放置在不同的可用区中，以防止机器或数据中心故障。通过自动故障转移，TiDB 确保您的服务始终在线。

TiDB Cloud Dedicated 集群由三个主要组件组成：TiDB 节点、TiKV 节点和 TiFlash 节点。TiDB Cloud Dedicated 中各组件的高可用性实现如下：

* **TiDB 节点**

    TiDB 仅用于计算，不存储数据。它支持水平扩展。TiDB Cloud Dedicated 将 TiDB 节点均匀部署到区域内的不同可用区。当用户执行 SQL 请求时，请求首先通过部署在多个可用区的负载均衡器，然后负载均衡器将请求分发到不同的 TiDB 节点执行。建议每个 TiDB Cloud Dedicated 集群至少有两个 TiDB 节点以实现高可用性。

* **TiKV 节点**

    [TiKV](https://docs.pingcap.com/tidb/stable/tikv-overview) 是 TiDB Cloud Dedicated 集群的行存储层，支持水平扩展。TiDB Cloud Dedicated 集群的最小 TiKV 节点数为 3。TiDB Cloud Dedicated 将 TiKV 节点均匀部署到您选择的区域中的所有可用区（至少 3 个）以实现持久性和高可用性。在典型的 3 副本设置中，您的数据在所有可用区的 TiKV 节点之间均匀分布，并持久化到每个 TiKV 节点的磁盘中。

* **TiFlash 节点**

    [TiFlash](https://docs.pingcap.com/tidb/stable/tiflash-overview) 作为 TiKV 的列式存储扩展，是使 TiDB 成为混合事务/分析处理（HTAP）数据库的关键组件。在 TiFlash 中，列式副本根据 Raft Learner 共识算法异步复制。TiDB Cloud Dedicated 将 TiFlash 节点均匀部署到区域内的不同可用区。建议在每个 TiDB Cloud Dedicated 集群中至少配置两个 TiFlash 节点，并在生产环境中为数据创建至少两个副本以实现高可用性。
