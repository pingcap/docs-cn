---
title: Follower Read
summary: 本文介绍 Follower Read 的使用和实现机制。
---

# Follower Read

当 Region 出现读热点时，Region leader 可能成为整个系统的读取瓶颈。在这种情况下，启用 Follower Read 功能可以显著减轻 leader 的负载，通过在多个 follower 之间平衡负载来提高整个系统的吞吐量。本文介绍 Follower Read 的使用和实现机制。

## 概述

Follower Read 功能是指在保证强一致性读的前提下，使用 Region 的任意 follower 副本来处理读取请求。该功能可以提高 TiDB 集群的吞吐量并减轻 leader 的负载。它包含一系列负载均衡机制，将 TiKV 的读取负载从 Region 的 leader 副本转移到 follower 副本。TiKV 的 Follower Read 实现为用户提供强一致性读取。

> **注意：**
>
> 为了实现强一致性读取，follower 节点目前需要向 leader 节点请求当前的执行进度（即 `ReadIndex`），这会导致额外的网络请求开销。因此，Follower Read 的主要优势在于隔离集群中的读写请求，并提高整体读取吞吐量。

## 使用方法

要启用 TiDB 的 Follower Read 功能，请按如下方式修改 `tidb_replica_read` 变量的值：

{{< copyable "sql" >}}

```sql
set [session | global] tidb_replica_read = '<目标值>';
```

作用域：SESSION | GLOBAL

默认值：leader

该变量用于设置期望的数据读取模式。

- 当 `tidb_replica_read` 的值设置为 `leader` 或空字符串时，TiDB 保持其默认行为，将所有读取操作发送给 leader 副本执行。
- 当 `tidb_replica_read` 的值设置为 `follower` 时，TiDB 选择 Region 的一个 follower 副本来执行所有读取操作。
- 当 `tidb_replica_read` 的值设置为 `leader-and-follower` 时，TiDB 可以选择任意副本来执行读取操作。在此模式下，读取请求在 leader 和 follower 之间进行负载均衡。
- 当 `tidb_replica_read` 的值设置为 `prefer-leader` 时，TiDB 优先选择 leader 副本来执行读取操作。如果 leader 副本在处理读取操作时明显变慢（例如由磁盘或网络性能抖动导致），TiDB 将选择其他可用的 follower 副本来执行读取操作。
- 当 `tidb_replica_read` 的值设置为 `closest-replicas` 时，TiDB 优先选择同一可用区内的副本来执行读取操作，可以是 leader 或 follower。如果同一可用区内没有副本，TiDB 将从 leader 副本读取。
- 当 `tidb_replica_read` 的值设置为 `closest-adaptive` 时：

    - 如果读取请求的预估结果大于或等于 [`tidb_adaptive_closest_read_threshold`](/system-variables.md#tidb_adaptive_closest_read_threshold-new-in-v630) 的值，TiDB 优先选择同一可用区内的副本进行读取操作。为了避免读取流量在可用区之间分布不均衡，TiDB 会动态检测所有在线 TiDB 和 TiKV 节点的可用区分布。在每个可用区中，`closest-adaptive` 配置生效的 TiDB 节点数量是有限制的，始终与拥有最少 TiDB 节点的可用区中的 TiDB 节点数量相同，其他 TiDB 节点自动从 leader 副本读取。例如，如果 TiDB 节点分布在 3 个可用区（A、B 和 C）中，其中 A 和 B 各包含 3 个 TiDB 节点，C 只包含 2 个 TiDB 节点，则每个可用区中 `closest-adaptive` 配置生效的 TiDB 节点数量为 2，A 和 B 可用区中的其他 TiDB 节点自动选择 leader 副本进行读取操作。
    - 如果读取请求的预估结果小于 [`tidb_adaptive_closest_read_threshold`](/system-variables.md#tidb_adaptive_closest_read_threshold-new-in-v630) 的值，TiDB 只能选择 leader 副本进行读取操作。

- 当 `tidb_replica_read` 的值设置为 `learner` 时，TiDB 从 learner 副本读取数据。如果 Region 中没有 learner 副本，TiDB 将返回错误。

<CustomContent platform="tidb">

> **注意：**
>
> 当 `tidb_replica_read` 的值设置为 `closest-replicas` 或 `closest-adaptive` 时，你需要配置集群以确保副本按照指定配置分布在可用区中。要为 PD 配置 `location-labels` 并为 TiDB 和 TiKV 设置正确的 `labels`，请参考[通过拓扑 label 进行副本调度](/schedule-replicas-by-topology-labels.md)。TiDB 依赖 `zone` 标签来匹配同一可用区内的 TiKV 节点，因此你需要确保 `zone` 标签包含在 PD 的 `location-labels` 中，并且 `zone` 包含在每个 TiDB 和 TiKV 节点的配置中。如果你的集群是使用 TiDB Operator 部署的，请参考[数据的高可用](https://docs.pingcap.com/tidb-in-kubernetes/v1.4/configure-a-tidb-cluster#high-availability-of-data)。

</CustomContent>

## 实现机制

在引入 Follower Read 功能之前，TiDB 采用强 leader 原则，将所有读写请求提交给 Region 的 leader 节点处理。虽然 TiKV 可以在多个物理节点上均匀分布 Region，但对于每个 Region，只有 leader 可以提供外部服务。其他 follower 除了接收来自 leader 复制的数据并准备在故障转移时进行 leader 选举投票外，无法处理读取请求。

为了允许在 follower 节点进行数据读取而不违反线性一致性或影响 TiDB 的快照隔离，follower 节点需要使用 Raft 协议的 `ReadIndex` 来确保读取请求可以读取到已在 leader 上提交的最新数据。在 TiDB 层面，Follower Read 功能只需要根据负载均衡策略将 Region 的读取请求发送到 follower 副本即可。

### 强一致性读取

当 follower 节点处理读取请求时，它首先使用 Raft 协议的 `ReadIndex` 与 Region 的 leader 交互，以获取当前 Raft 组的最新提交索引。在 leader 的最新提交索引在本地应用到 follower 后，才开始处理读取请求。

### Follower 副本选择策略

由于 Follower Read 功能不影响 TiDB 的快照隔离事务隔离级别，TiDB 采用轮询策略来选择 follower 副本。目前，对于 coprocessor 请求，Follower Read 负载均衡策略的粒度是在连接级别。对于连接到特定 Region 的 TiDB 客户端，选择的 follower 是固定的，只有在失败或调整调度策略时才会切换。

然而，对于非 coprocessor 请求，如点查询，Follower Read 负载均衡策略的粒度是在事务级别。对于特定 Region 上的 TiDB 事务，选择的 follower 是固定的，只有在失败或调度策略调整时才会切换。如果一个事务同时包含点查询和 coprocessor 请求，这两种类型的请求会根据前述调度策略分别进行读取调度。在这种情况下，即使 coprocessor 请求和点查询针对同一个 Region，TiDB 也会将它们作为独立事件处理。
