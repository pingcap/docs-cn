---
title: TiDB 调度
summary: 介绍 TiDB 集群中的 PD 调度组件。
---

# TiDB 调度

Placement Driver ([PD](https://github.com/tikv/pd)) 作为 TiDB 集群的管理者，同时也负责集群中的 Region 调度。本文介绍了 PD 调度组件的设计和核心概念。

## 调度场景

TiKV 是 TiDB 使用的分布式键值存储引擎。在 TiKV 中，数据被组织为 Region，并在多个节点上进行复制。在所有副本中，leader 负责读写，而 follower 负责从 leader 复制 Raft 日志。

现在考虑以下场景：

* 为了高效利用存储空间，同一个 Region 的多个副本需要根据 Region 大小合理地分布在不同节点上；
* 对于多数据中心的拓扑结构，一个数据中心的故障应该只会导致所有 Region 的一个副本失效；
* 当新增 TiKV 节点时，可以将数据重新平衡到新节点；
* 当 TiKV 节点发生故障时，PD 需要考虑：
    * 故障节点的恢复时间。
        * 如果时间较短（例如服务重启），是否需要调度。
        * 如果时间较长（例如磁盘故障导致数据丢失），如何进行调度。
    * 所有 Region 的副本。
        * 如果某些 Region 的副本数不足，PD 需要补充副本。
        * 如果某些 Region 的副本数超出预期（例如，故障节点恢复后重新加入集群），PD 需要删除多余的副本。
* 读写操作在 leader 上进行，不能只分布在少数几个节点上；
* 并非所有 Region 都是热点，因此需要平衡所有 TiKV 节点的负载；
* 在 Region 进行均衡时，数据传输会占用大量网络/磁盘流量和 CPU 时间，这可能会影响在线服务。

这些场景可能同时发生，这使得问题更难解决。此外，整个系统是动态变化的，因此需要一个调度器来收集集群的所有信息，然后对集群进行调整。因此，PD 被引入到 TiDB 集群中。

## 调度需求

上述场景可以分为两类：

1. 作为一个分布式高可用存储系统必须满足的需求：

    * 副本数量正确。
    * 副本需要根据不同的拓扑结构分布在不同的机器上。
    * 集群能够自动从 TiKV 节点故障中恢复。

2. 作为一个良好的分布式系统需要的优化：

    * 所有 Region 的 leader 在节点间均匀分布；
    * 所有 TiKV 节点的存储容量均衡；
    * 热点均衡；
    * Region 负载均衡的速度需要限制，以确保在线服务的稳定性；
    * 运维人员能够手动上下线节点。

满足第一类需求后，系统将具有容错能力。满足第二类需求后，资源将被更有效地利用，系统将具有更好的可扩展性。

为了实现这些目标，PD 首先需要收集信息，如节点状态、Raft 组信息和访问节点的统计信息。然后我们需要为 PD 指定一些策略，使 PD 能够根据这些信息和策略制定调度计划。最后，PD 向 TiKV 节点分发一些操作指令来完成调度计划。

## 基本调度操作

所有调度计划包含三种基本操作：

* 添加新副本
* 删除副本
* 在 Raft 组内的副本之间转移 Region leader

这些操作通过 Raft 命令 `AddReplica`、`RemoveReplica` 和 `TransferLeader` 来实现。

## 信息收集

调度基于信息收集。简而言之，PD 调度组件需要知道所有 TiKV 节点和所有 Region 的状态。TiKV 节点向 PD 报告以下信息：

- 每个 TiKV 节点报告的状态信息：

    每个 TiKV 节点定期向 PD 发送心跳。PD 不仅检查节点是否存活，还在心跳消息中收集 [`StoreState`](https://github.com/pingcap/kvproto/blob/release-8.1/proto/pdpb.proto#L473)。`StoreState` 包括：

    * 总磁盘空间
    * 可用磁盘空间
    * Region 数量
    * 数据读写速度
    * 发送/接收的快照数量（数据可能通过快照在副本之间复制）
    * 节点是否过载
    * 标签（参见[拓扑感知](https://docs.pingcap.com/tidb/stable/schedule-replicas-by-topology-labels)）

    你可以使用 PD control 检查 TiKV 节点的状态，状态可以是 Up、Disconnect、Offline、Down 或 Tombstone。以下是所有状态及其关系的描述。

    + **Up**：TiKV 节点正在服务中。
    + **Disconnect**：PD 和 TiKV 节点之间的心跳消息丢失超过 20 秒。如果丢失时间超过 `max-store-down-time` 指定的时间，状态 "Disconnect" 会变为 "Down"。
    + **Down**：PD 和 TiKV 节点之间的心跳消息丢失时间超过 `max-store-down-time`（默认 30 分钟）。在此状态下，TiKV 节点开始在存活的节点上补充每个 Region 的副本。
    + **Offline**：TiKV 节点通过 PD Control 手动下线。这只是节点下线过程的中间状态。处于此状态的节点会将其所有 Region 迁移到满足重定位条件的其他 "Up" 状态的节点。当 `leader_count` 和 `region_count`（通过 PD Control 获取）都显示为 `0` 时，节点状态从 "Offline" 变为 "Tombstone"。在 "Offline" 状态下，**不要**禁用节点服务或节点所在的物理服务器。在节点下线过程中，如果集群没有目标节点来重定位 Region（例如，集群中没有足够的节点来存放副本），节点将一直处于 "Offline" 状态。
    + **Tombstone**：TiKV 节点完全下线。你可以使用 `remove-tombstone` 接口安全地清理处于此状态的 TiKV。从 v6.5.0 开始，如果不手动处理，PD 会在节点转换为 Tombstone 一个月后自动删除内部存储的 Tombstone 记录。

    ![TiKV 节点状态关系](/media/tikv-store-status-relationship.png)

- Region leader 报告的信息：

    每个 Region leader 定期向 PD 发送心跳以报告 [`RegionState`](https://github.com/pingcap/kvproto/blob/release-8.1/proto/pdpb.proto#L312)，包括：

    * leader 自身的位置
    * 其他副本的位置
    * 离线副本的数量
    * 数据读写速度

PD 通过这两种心跳收集集群信息，然后基于这些信息做出决策。

此外，PD 可以通过扩展接口获取更多信息来做出更精确的决策。例如，如果节点的心跳中断，PD 无法知道该节点是暂时还是永久下线。它只会等待一段时间（默认 30 分钟），如果仍然没有收到心跳，就将该节点视为离线。然后 PD 会将该节点上的所有 Region 平衡到其他节点。

但有时节点是由运维人员手动下线的，因此运维人员可以通过 PD control 接口告知 PD。这样 PD 就可以立即开始平衡所有 Region。

## 调度策略

收集信息后，PD 需要一些策略来制定调度计划。

**策略 1：Region 的副本数量需要正确**

PD 可以从 Region leader 的心跳中知道某个 Region 的副本数量是否不正确。如果发生这种情况，PD 可以通过添加/删除副本来调整副本数量。副本数量不正确的原因可能是：

* 节点故障导致某些 Region 的副本数量少于预期；
* 故障节点恢复后，某些 Region 的副本数量可能多于预期；
* [`max-replicas`](https://github.com/pingcap/pd/blob/v4.0.0-beta/conf/config.toml#L95) 被修改。

**策略 2：Region 的副本需要位于不同位置**

注意这里的"位置"与"机器"是不同的。通常 PD 只能确保一个 Region 的副本不在同一个节点上，以避免该节点的故障导致多个副本丢失。但在生产环境中，你可能有以下需求：

* 多个 TiKV 节点在同一台机器上；
* TiKV 节点分布在多个机架上，即使一个机架故障系统也能保持可用；
* TiKV 节点分布在多个数据中心，即使一个数据中心故障系统也能保持可用；

这些需求的关键是节点可以有相同的"位置"，这是容错的最小单位。一个 Region 的副本不能在同一个单位内。因此，我们可以为 TiKV 节点配置 [labels](https://github.com/tikv/tikv/blob/v4.0.0-beta/etc/config-template.toml#L140)，并在 PD 上设置 [location-labels](https://github.com/pingcap/pd/blob/v4.0.0-beta/conf/config.toml#L100) 来指定哪些标签用于标记位置。

**策略 3：副本需要在节点之间保持均衡**

Region 副本的大小限制是固定的，因此在节点之间保持副本均衡有助于数据大小的均衡。

**策略 4：leader 需要在节点之间保持均衡**

根据 Raft 协议，读写操作在 leader 上执行，因此 PD 需要将 leader 分散到整个集群而不是集中在几个节点上。

**策略 5：热点需要在节点之间保持均衡**

PD 可以从节点心跳和 Region 心跳中检测热点，从而分散热点。

**策略 6：存储大小需要在节点之间保持均衡**

TiKV 节点启动时会报告存储 `capacity`，这表示节点的空间限制。PD 在调度时会考虑这一点。

**策略 7：调整调度速度以稳定在线服务**

调度会占用 CPU、内存、网络和 I/O 流量。过多的资源使用会影响在线服务。因此，PD 需要限制并发调度任务的数量。默认情况下这个策略是保守的，但如果需要更快的调度可以进行调整。

## 调度实现

PD 从节点心跳和 Region 心跳收集集群信息，然后根据信息和策略制定调度计划。调度计划是一系列基本操作的序列。每次 PD 从 Region leader 收到 Region 心跳时，它会检查该 Region 是否有待处理的操作。如果 PD 需要向 Region 分派新的操作，它会将操作放入心跳响应中，并通过检查后续的 Region 心跳来监控操作的执行情况。

注意这里的"操作"只是对 Region leader 的建议，Region 可以选择跳过。Region 的 leader 可以根据其当前状态决定是否跳过调度操作。
