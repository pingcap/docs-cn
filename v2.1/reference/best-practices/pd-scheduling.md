---
title: PD 调度策略最佳实践
summary: 了解 PD 调度策略的最佳实践和调优方式
category: reference
---

# PD 调度策略最佳实践

本文将详细介绍 PD 调度系统的原理，并通过几个典型场景的分析和处理方式，分享调度策略的最佳实践和调优方式，帮助大家在使用过程中快速定位问题。本文假定你对 TiDB，TiKV 以及 PD 已经有一定的了解，相关核心概念如下：

- [Leader/Follower/Learner](/v2.1/glossary.md#leaderfollowerlearner)
- [Operator](/v2.1/glossary.md#operator)
- [Operator Step](/v2.1/glossary.md#operator-step)
- [Pending/Down](/v2.1/glossary.md#pendingdown)
- [Region/Peer/Raft Group](/v2.1/glossary.md#regionpeerraft-group)
- [Region Split](/v2.1/glossary.md#region-split)
- [Scheduler](/v2.1/glossary.md#scheduler)
- [Store](/v2.1/glossary.md#store)

> **注意：**
>
> 本文内容基于 TiDB 3.0 版本，更早的版本（2.x）缺少部分功能的支持，但是基本原理类似，也可以以本文作为参考。

## PD 调度原理

该部分介绍调度系统涉及到的相关原理和流程。

### 调度流程

宏观上来看，调度流程大体可划分为 3 个部分：

1. 信息收集

    TiKV 节点周期性地向 PD 上报 `StoreHeartbeat` 和 `RegionHeartbeat` 两种心跳消息。其中 `StoreHeartbeat` 包含了 Store 的基本信息、容量、剩余空间、读写流量等数据；`RegionHeartbeat` 包含了 Region 的范围、副本分布、副本状态、数据量、以及读写流量等数据。PD 将这些信息梳理并转存供调度来决策。

2. 生成调度

    不同的调度器从自身的逻辑和需求出发，考虑各种限制和约束后生成待执行的 Operator。这里所说的限制和约束包括但不限于：

     - 不往断连中、下线中、繁忙、空间不足、在大量收发 snapshot 等各种异常状态的 Store 添加副本
     - Balance 时不选择状态异常的 Region
     - 不尝试把 Leader 转移给 Pending Peer
     - 不尝试直接移除 Leader
     - 不破坏 Region 各种副本的物理隔离
     - 不破坏 Label property 等约束

3. 执行调度

    生成的 Operator 不会立即开始执行，而是首先会进入一个由 OperatorController 管理的一个等待队列。OperatorController 会根据配置以一定的并发量从等待队列中取出 Operator 并执行。执行的过程就是依次把每个 Operator Step 下发给对应 Region 的 Leader。最终 Operator 执行完毕会被标记为 finish 状态或者超时被标记为 timeout，并被从执行列表中移除。

### 负载均衡

Region 负载均衡调度主要依赖 `balance-leader` 和 `balance-region` 这两个调度器。这二者的调度目标是将 Region 均匀地分散在集群中的所有 Store 上，但它们的侧重点又有所不同：`balance-leader` 关注 Region 的 Leader，目的是分散处理客户端请求的压力；`balance-region` 关注 Region 的各个 Peer，目的是分散存储的压力，同时避免出现爆盘等状况。

`balance-leader` 与 `balance-region` 有着相似的调度流程，首先根据不同 Store 的对应资源量的情况分别打分，然后不断从得分较高的 Store 选择 Leader 或 Peer 迁移到得分较低的 Store 上。这两者的分数计算上也有一定差异：`balance-leader` 比较简单，使用 Store 上所有 Leader 所对应的 Region Size 加和作为得分。`balance-region` 得分因为不同节点存储容量可能不一致，会分以下三种情况：

- 当空间富余时使用数据量计算得分（使不同节点数据量基本上均衡）
- 当空间不足时由使用剩余空间计算得分（使不同节点剩余空间基本均衡）
- 处于中间态时则同时考虑两个因素做加权和当作得分

此外，为了应对不同节点可能在性能等方面存在差异的问题，还可为 Store 设置负载均衡的权重。`leader-weight` 和 `region-weight` 分别用于控制 Leader 权重以及 Region 权重（默认值都为 1）。假如把某个 Store 的 `leader-weight` 设为 2，调度稳定后，则该节点的 leader 数量约为普通节点的 2 倍；假如把某个 Store 的 `region-weight` 设为 0.5，那么调度稳定后该节点的 Region 数量约为其他节点的一半。

### 热点调度

热点调度对应的调度器是 hot-region-scheduler。目前 3.0 版本统计热点 Region 的方式比较单一，就是根据 Store 上报的信息，统计出持续一段时间读或写流量超过一定阈值的 Region，然后再用与负载均衡类似的方式把这些 Region 分散开来。

对于写热点，热点调度会同时尝试打散热点 Region 的 Peer 和 Leader；对于读热点，由于只有 Leader 承载读压力，热点调度会尝试将热点 Region 的 Leader 打散。

### 集群拓扑感知

让 PD 感知不同节点分布的拓扑是为了通过调度使不同 Region 的各个副本尽可能分散，保证高可用和容灾。PD 会在后台不断扫描所有 Region，当发现 Region 的分布不是当前的最优化状态时，会生成调度以替换 Peer，将 Region 调整至最佳状态。

负责这个检查的组件叫 `replicaChecker`（跟 Scheduler 类似，但是不可关闭）。它依赖于 `location-labels` 配置项来进行调度。比如配置 `[zone, rack, host]` 定义了三层的拓扑结构：集群分为多个 zone（可用区），每个 zone 下有多个 rack（机架），每个 rack 下有多个 host（主机）。PD 在调度时首先会尝试将 Region 的 Peer 放置在不同的 zone，假如无法满足（比如配置 3 副本但总共只有 2 个 zone）则保证放置在不同的 rack；假如 rack 的数量也不足以保证隔离，那么再尝试 host 级别的隔离，以此类推。

### 缩容及故障恢复

缩容是指预备将某个 Store 下线，通过命令将该 Store 标记为 Offline 状态，此时 PD 通过调度将待下线节点上的 Region 迁移至其他节点。故障恢复是指当有 Store 发生故障且无法恢复时，有 Peer 分布在对应 Store 上的 Region 会产生缺少副本的状况，此时 PD 需要在其他节点上为这些 Region 补副本。

这两种情况的处理过程基本上是一样的。由 `replicaChecker` 检查到 Region 存在异常状态的 Peer，然后生成调度在健康的 Store 创建新副本替换掉异常的。

### Region merge

Region merge 指的是为了避免删除数据后大量小甚至空的 Region 消耗系统资源，通过调度把相邻的小 Region 合并的过程。Region merge 由 `mergeChecker` 负责，其过程与 `replicaChecker` 类似，也是在后台遍历，发现连续的小 Region 后发起调度。

## 查询调度状态

查看调度系统状态的手段主要包括 Metrics，pd-ctl 和日志，这里介绍 Metrics 和 pd-ctl 两种方式。更具体的信息可以参考官方文档中 [PD 监控](/v2.1/reference/key-monitoring-metrics/pd-dashboard.md)以及 [PD Control 使用](/v2.1/reference/key-monitoring-metrics/pd-dashboard.md)的章节。

### Operator 状态

**Grafana PD/Operator** 页面展示了 Operator 的相关统计。其中比较重要的有：

- Schedule Operator Create：Operator 的创建情况。从名称可以知道 Operator 创建的目标调度器以及创建原因。
- Operator finish duration：Operator 执行耗时的情况
- Operator Step duration：不同 Operator Step 执行耗时的情况

查询 Operator 的 pd-ctl 命令有：

- `operator show`：查询当前调度生成的所有 Operator
- `operator show [admin | leader | region]`：按照类型查询 Operator

### Balance 状态

**Grafana PD/Statistics - Balance** 页面展示了负载均衡相关的统计信息，其中比较重要的有：

- Store Leader/Region score：每个 Store 的得分
- Store Leader/Region count：每个 Store 的 Leader/Region 数量
- Store available：每个 Store 的剩余空间

使用 pd-ctl 的 store 命令可以查询 Store 的得分，数量，剩余空间，weight 等信息。

### 热点调度状态

**Grafana PD/Statistics - hotspot** 页面展示了热点 Region 的相关统计，其中比较重要的有：

- Hot write Region’s leader/peer distribution：写热点 Region 的 Leader/Peer 分布情况
- Hot read Region’s leader distribution：读热点 Region 的 Leader 分布情况

使用 pd-ctl 同样可以查询上述信息，可以使用的命令有：

- `hot read`：查询读热点 Region 信息
- `hot write`：查询写热点 Region 信息
- `hot store`：按 Store 统计热点分布情况
- `region topread [limit]`：查询当前读流量最大的 Region
- `region topwrite [limit]`：查询当前写流量最大的 Region

### Region 健康度

**Grafana PD/Cluster/Region health** 面板展示了异常状态 Region 数的统计，其中包括 Pending Peer，Down Peer，Offline Peer，以及副本数过多或过少的 Region。

通过 pd-ctl 的 region check 命令可以查看具体异常的 Region 列表：

- `region check miss-peer`：缺副本的 Region
- `region check extra-peer`：多副本的 Region
- `region check down-peer`：有副本状态为 Down 的 Region
- `region check pending-peer`：有副本状态为 Pending 的 Region

## 调度策略控制

在线调整调度策略主要使用 pd-ctl 工具来完成，可以通过以下三个方面来控制 PD 的调度行为。更具体的信息可以参考 [PD Control](/v2.1/reference/tools/pd-control.md)。

### 启停调度器

pd-ctl 支持动态创建和删除 Scheduler 的功能，我们可以通过这些操作来控制 PD 的调度行为，如下所示：

- `scheduler show`：显示当前系统中的 Scheduler
- `scheduler remove balance-leader-scheduler`：删除（停用）balance leader 调度器
- `scheduler add evict-leader-scheduler-1`：添加移除 Store 1 的所有 Leader 的调度器

### 手动添加 Operator

PD 还支持绕过调度器，直接通过 pd-ctl 来创建或删除 Operator，如下所示：

- `operator add add-peer 2 5`：在 Store 5 上为 Region 2 添加 Peer
- `operator add transfer-leader 2 5`：将 Region 2 的 Leader 迁移至 Store 5
- `operator add split-region 2`：将 Region 2 拆分为 2 个大小相当的 Region
- `operator remove 2`：取消 Region 2 当前待执行的 Operator

### 调度参数调整

使用 pd-ctl 执行 `config show` 命令可以查看所有的调度参数，执行 `config set {key} {value}` 可以调整对应参数的值。常见调整如下：

- `leader-schedule-limit`：控制 Transfer Leader 调度的并发数
- `region-schedule-limit`：控制增删 Peer 调度的并发数
- `disable-replace-offline-replia`：停止处理节点下线的调度
- `disable-location-replacement`：停止处理调整 Region 隔离级别相关的调度
- `max-snapshot-count`：每个 Store 允许的最大收发 Snapshot 的并发数

## 典型场景分析与处理

该部分通过几个典型场景及其应对方式说明 PD 调度策略的最佳实践。

### Leader/Region 分布不均衡

PD 的打分机制决定了一般情况下，不同 Store 的 Leader Count 和 Region Count 不能完全说明负载均衡状态，需要从 TiKV 的实际负载或者存储空间占用来判断是否有负载不均衡的状况。

确认存在 Leader/Region 分布不均衡的现象后，首先要观察不同 Store 的打分情况。

如果不同 Store 的打分是接近的，说明 PD 认为此时已经是均衡状态了，可能的原因有：

- 存在热点导致负载不均衡。需要根据热点调度相关的信息进一步分析，可以参考下文热点调度的部分。
- 存在大量的空 Region 或小 Region，导致不同 Store 的 Leader 数量差别特别大，导致 raftstore 负担过重。需要开启 Region Merge 并尽可能加速合并，可以参考下文关于 Region Merge 的部分。
- 不同 Store 的软硬件环境存在差异。可以酌情调整 `leader-weight` 和 `region-weight` 来控制 Leader/Region 的分布。
- 其他不明原因。可以使用调整权重这个兜底的方法，通过调整 `leader-weight` 和 `region-weight` 来调整至用户觉得合理的分布。

如果不同 Store 的打分差异较大，需要进一步检查 Operator 相关 Metrics，特别关注 Operator 的生成和执行情况，这时大体上又分两种情况:

- 一种情况是生成的调度是正常的，但是调度的速度很慢。可能的原因有：

    - 调度速度受限于 limit 配置。PD 默认配置的 limit 比较保守，在不对正常业务造成显著影响的前提下，可以酌情将 `leader-schedule-limit` 或 `region-schedule-limit` 调大一些。此外， `max-pending-peer-count` 以及 `max-snapshot-count` 限制也可以放宽。
    - 系统中同时运行有其它的调度任务产生竞争，导致 balance 速度上不去。这种情况下如果 balance 调度的优先级更高，可以先停掉其他的调度或者限制其他调度的速度。例如 Region 没均衡的情况下做下线节点操作，下线的调度与 Region Balance 会抢占 `region-schedule-limit` 配额，此时我们可以把 `replica-schedule-limit` 调小将下线调度的速度限制住，或者干脆设置 `disable-replace-offline-replica = true` 来暂时关闭下线流程。
    - 调度执行得太慢。可以检查 Operator Step 的耗时来进行判断。通常不涉及到收发 Snapshot 的 Step（比如 TransferLeader，RemovePeer，PromoteLearner 等）的完成时间应该在毫秒级，涉及到 Snapshot 的 Step（如 AddLearner，AddPeer 等）的完成时间为数十秒。如果耗时明显过高，可能是 TiKV 压力过大或者网络等方面的瓶颈导致的，需要具体情况具体分析。

- 另一种情况是没能生成对应的 balance 调度。可能的原因有：

    - 调度器未被启用。比如对应的 Scheduler 被删除了，或者 limit 被设置为 0。
    由于其它约束无法进行调度。比如系统中有 evict-leader-scheduler，此时无法把 Leader 迁移至对应的 Store。再比如设置了 Label property，也会导致部分 Store 不接受 Leader。
    - 集群拓扑的限制导致无法均衡。比如 3 副本 3 数据中心的集群，由于副本隔离的限制，每个 Region 的 3 个副本都分别分布在不同的数据中心，假如这 3 个数据中心的 Store 数不一样，最后调度就会收敛在每个数据中心均衡，但是全局不均衡的状态。

### 节点下线速度慢

这个场景需要从 Operator 相关的 Metrics 入手，分析 Operator 的生成执行情况。

如果调度在正常生成，只是速度很慢，可能的原因有：

- 调度速度受限于 limit 配置。下线对应的 limit 参数是 `replica-schedule-limit`，可以把它适当调大。与 Balance 类似，`max-pending-peer-count` 以及 `max-snapshot-count` 限制同样也可以放宽。
- 系统中同时运行有其它的调度任务产生竞争，或者调度执行得太慢了。处理方法在上一节已经介绍过了，不再赘述。
- 下线单个节点时，由于待操作的 Region 有很大一部分（3 副本配置下约 1/3）的 Leader 都集中在下线的节点上，下线速度会受限于这个单点生成 Snapshot 的速度。可以通过手动给这个节点添加一个 evict-leader 调度迁走 Leader 来加速。

如果没有对应的 Operator 调度生成，可能的原因有：

- 下线调度被关闭，或者 `replica-schedule-limit` 被设为 0。
- 找不到节点来转移 Region。例如相同 Label 的替代节点容量都大于 80%，PD 为了避免爆盘的风险会停止调度。这种情况需要添加更多节点，或者删除一些数据释放空间。

### 节点上线速度慢

目前 PD 没有对节点上线特殊处理。节点上线实际上是依靠 balance region 机制来调度的，所以参考前面 Region 分布不均衡的排查步骤即可。

### 热点分布不均匀

热点调度的问题大体上可以分为以下几种情况：

- 从 PD 的 metrics 能看出来有不少 hot Region，但是调度速度跟不上，不能及时地把热点 Region 分散开来。

   **解决方法**：加大 `hot-region-schedule-limit`，并减少其他调度器的 limit 配额，从而加快热点调度的速度。还可调小 `hot-region-cache-hits-threshold` 以使 PD 对流量的变化更快做出反应。

- 单一 Region 形成热点，比如大量请求频繁 scan 一个小表，这个可以从业务角度或者 metrics 统计的热点信息看出来。由于单 Region 热点现阶段无法使用打散的手段来消除，需要确认热点 Region 后手动添加 `split-region` 调度将这样的 Region 拆开。

- 从 PD 的统计来看没有热点，但是从 TiKV 的相关 metrics 可以看出部分节点负载明显高于其他节点，成为整个系统的瓶颈。这是因为目前 PD 统计热点 Region 的维度比较单一，仅针对流量进行分析，在某些场景下无法准备定位出热点。例如部分 Region 有大量的点查请求，从流量上来看并不显著，但是过高的 QPS 导致关键模块达到瓶颈。

    **解决方法**：首先从业务层面确定形成热点的 table，然后添加 `scatter-range-scheduler` 来使得这个 table 的所有 Region 均匀分布。TiDB 也在其 HTTP API 中提供了相关接口来简化这个操作，具体可以参考 [TiDB HTTP API](https://github.com/pingcap/tidb/blob/master/docs/tidb_http_api.md) 文档。

### Region Merge 速度慢

与前面讨论过的调度慢的问题类似，Region Merge 速度慢也很有可能是受到 limit 配置的限制（`merge-schedule-limit` 及 `region-schedule-limit`），或者是与其他调度器产生了竞争。具体来说，可有如下处理方式：

- 假如已经从统计得知系统中有大量的空 Region，这时可以通过把 `max-merge-region-size` 和 `max-merge-region-keys` 调整为较小值来加快 Merge 速度。这是因为 Merge 的过程涉及到副本迁移，于是 Merge 的 Region 越小，速度就越快。如果 Merge Operator 生成的速度已经有几百 opm，想进一步加快 Region Merge 过程，还可以把 `patrol-region-interval` 调整为 "10ms" ，这个能加快巡检 Region 的速度，但是会消耗更多的 CPU。

- 曾经创建过大量 Table 然后又清空了（truncate 操作也算创建 Table）。此时如果开启了 split table 特性，这些空 Region 是无法合并的，此时需要调整以下参数关闭这个特性：

    - TiKV: `split-region-on-table` 设为 false
    - PD: `namespace-classifier` 设为 “”

- 对于 3.0.4 和 2.1.16 以前的版本，Region 的统计 approximate_keys 在特定情况下（大部分发生在 drop table 之后）统计不准确，造成 keys 的统计值很大，无法满足 `max-merge-region-keys` 的约束，可以把 `max-merge-region-keys` 这个条件放开，调成很大的值来绕过这个问题。

### TiKV 节点故障处理策略

没有人工介入时，PD 处理 TiKV 节点故障的默认行为是，等待半小时之后（可通过 `max-store-down-time` 配置调整），将此节点设置为 Down 状态，并开始为涉及到的 Region 补充副本。

实践中，如果能确定这个节点的故障是不可恢复的，可以立即做下线处理，这样 PD 能尽快补齐副本，降低数据丢失的风险。与之相对，如果确定这个节点是能恢复的，但可能半小时之内来不及，则可以把 `max-store-down-time` 临时调整为比较大的值，这样能避免超时之后产生不必要的副本补充，造成资源浪费。
