---
title: Data Migration 高可用机制
---

# Data Migration 高可用机制

为了保障迁移服务的连续性，DM 中的组件 DM Master 和 DM Worker 均实现了高可用机制，避免单点故障。本文将详述其高可用机制的内部机制，以及对迁移任务的影响。

在详细了解之前，首先要了解 DM 整体架构以及各个关键组件的作用，请参考 [DM 架构](/dm/dm-arch.md)。

## DM Master 内部组成

![dm-ha-1](/media/dm/dm-ha-1.png)

- **Grpc 和 Http 接口。** DM Master 对外提供 Grpc 以及 Http 接口给其他组件，如 dmctl，WebUI，DM worker调用，DM Master 的 Follower 节点，收到 Grpc 和 Http 请求也会 redirect 给 DM Master 的 Leader 节点进行处理。

- **ETCD。** DM Master 内部嵌入 ETCD 来组成集群，DM Master 的 Grpc 和 Http 接口 attach 到 ETCD 中，同时，ETCD 也作为 DM Master, DM Worker, Source, Task 等配置或者状态的存储介质。

- **Election。** Election 周期调用 ETCD 的 campaign 接口进行选举，若为 Leader 节点，则启动 DM Master的其他组件，如 Scheduler, Pessimist, Optimist等，各组件的启动会读取 ETCD 中保存的信息，实现相关任务的接续执行，若为 Follower，则不启动其他组件，若为 Leader 切换回 Follower，则会关闭其他组件。

- **Scheduler。** 负责注册及监听 DM Worker 状态，安排分配 Source 以及 Task，可参考 DM Worker 任务分配的相关文档进一步了解

- **Pessimist 和 Optimist。** DM Master 实现对 DDL 进行悲观协调以及乐观协调的模块

- **Dmctl/WebUI 调用流程。** Dmctl 和 WebUI 分别调用DM Master grpc 和 http 接口，若非 Leader 节点，则进行 redirect 给 Leader 节点，若 Dmctl 和 WebUI 请求需要调用 DM Worker 进行信息收集或者操作，则通过 DM Master 的 Scheduler 模块通过 Grpc 接口调用 DM Worker。

- **DM Master 与 DM Worker 调用流程。** DM Worker 启动时会 grpc 调用 DM Master 来注册 worker 信息，DM Master 主要调用 Scheduler 模块实现相关的逻辑，其中，Scheduler 会将 worker 信息写入到 ETCD，并对其进行监听，DM Worker注册之后，DM Worker 会通过 ETCD 实现 Keep-Alive，若 DM Worker 发生故障，DM Master 的 Scheduler 模块的监听会发现该 DM Worker 出现故障，从而将该 DM Worker 上的相关任务进行转移。

## DM Master 高可用机制

### DM Master 服务恢复

从上文 DM Master 的架构可以看出，DM Master 的高可用实际上主要依赖内嵌的 ETCD 实现，若某一 DM Master 节点发生故障，DM Master 的 Election 模块会使用 ETCD 选举出新的 Leader 节点，新的 Leader 节点会启动 DM Master 相关组件，且组件启动会读取保存于 ETCD 中的信息，做到接续执行。

### 其他组件恢复访问

DM Master 之外的组件，如 dmctl, DM Worker, 调用 DM Master 接口，可采用传入多 endpoint 的方式，避免只配置单个 endpoint 同时该节点出现故障而无法访问的问题。其他组件，如 WebUI，遇到访问节点挂掉时，等 DM Master 集群恢复后，可以切换节点继续访问。若非访问节点发生故障，DM Master 集群恢复后可以继续访问。

### DM Master 恢复主要受到哪些影响，恢复速度主要取决于哪些因素 

由上文可知，DM Master 集群的 Leader 出现节点故障之后，会由 Election 模块重新选举一个 Leader, 此过程主要受到 ETCD 性能影响，新的 Leader 需要重新启动 Scheduler，Pessimist 和 Optimist 等模块，此过程主要需要读取保存于 ETCD 中的各模块信息，实现接续执行，但此过程只是内存中实例构建，耗时不大，因此，耗时主要取决于 ETCD 集群的恢复时间。

## DM Worker 高可用机制

当部署的 DM Worker 节点数超过上游 MySQL/MariaDB 节点数时，超出上游节点数的相关 DM Worker 节点默认将处于空闲状态。若某个 DM Worker 节点下线或与 DM Master 发生网络中断，DM Worker 向 DM Master 发送的 keepalive 心跳将中断，DM Master 会自动将与原 DM Worker 节点相关的数据迁移任务调度到其他空闲的 DM Worker 节点上并继续运行。架构图如下所示：

![dm-ha-2](/media/dm/dm-ha-2.png)

在介绍调度策略前先介绍几个 DM 中的概念：

- source：上游数据库源实例，例如一个 MySQL 实例。
- task：数据迁移任务，负责将一个或多个 source 同步到单个下游数据库。
- subtask：数据迁移子任务，单个子任务负责将一个上游数据库同步到一个下游数据库，子任务的集合组成了 task。
- bound：DM Worker 与 source 的绑定关系，一个 DM Worker 同时仅能处理一个 source 的迁移任务。当 DM Worker 拉取某个 source 的 relay log 后，它将不能再处理其他 source 的迁移任务。

DM Worker 负责的任务以上游源数据库（简称 source）为调度单位，即一个 DM Worker 仅能服务一个 source。多个 task 可能需要同步同一个 source，此时该 source 所处 worker 将为每个 task 派生 subtask。

当 DM Worker 向 DM Master 发送心跳中断超过 [TTL](/dm/dm-ha.md#DM Worker 与 DM Master 保持心跳的超时时间及配置) 后，DM Master 会将该 DM Worker 负责的 source 与对应 subtask 调度给没有绑定的 source 的 DM Worker，调度的优先级从高到低为：

1. 该 source 之前在该 DM Worker 上存在未完成的全量导入任务。
2. 该 source 上次由该 DM Worker 处理且 DM Worker 开启了该 source 的 relay log。
3. 该 DM Worker 开启了该 source 的 relay log。
4. 该 source 上次由该 DM Worker 处理。
5. 任一空闲状态的 DM Worker。

如果没有处于空闲状态的 DM Worker，则该 source 的 subtasks 将被暂时挂起，直到原先的 DM Worker 恢复或者新的 DM Worker 节点加入。当 DM Master 收到 DM Worker 的重新上线心跳或是新的 DM Worker 节点的 heartbeat 信息时，DM Master 会按和前文一样的优先级顺序寻找处于未绑定 DM Worker 的 source 进行绑定。

### 特殊任务调度

从上文可以看出，DM Master 只会为 source 试图绑定处于未绑定状态的 DM Worker。但仅有一种情况存在例外，即 source 在某个 DM Worker 存在未完成的全量导入任务。这样的调度策略是因为 On-Premises 环境中， DM Worker 全量导出阶段导出的数据均保留在本地盘，大部分时候进行全量导入任务必须要在对应的 DM Worker 才能正确进行，否则需要重新导出一遍数据，会增加大量不必要开销。

举个例子说明此场景，假设：

- worker1 绑定 source1 ，subtask 处于 dump 阶段；
- worker2 绑定 source2， subtask 处于 sync 阶段；
- worker3 空闲；

当 worker1 发生故障下线后，DM Master 扫描所有 worker，并采取以下行为：

- 判断 worker2 上是否存在 source1 未完成的全量迁移；
    - 若存在。解绑 source2 ，worker2 绑定 source1 ，worker3 绑定 source2；
    - 若不存在。worker2 绑定 source2 无变化，worker3 绑定 source1。

DM Worker 重新上线也与上述流程基本一致，如果寻找到符合条件的 source，会进行换绑并为 source 先前绑定的 DM Worker 尝试重新绑定新的 source。

### 当 DM Worker 恢复后，source 是否会再迁回来

在两种情况下 source 将再迁回：

1. 如果 DM Worker 之前连接的 source 在下线期间没有被调度到其他 DM Worker （例如没有空闲 Worker）；
2. 如果 source 之前在该 DM Worker 上有未完成的 load 阶段任务，且 source 在其他 DM Worker 上仍处于 dump 阶段。

假如 DM Worker 恢复后，原 source 不符合上述条件并未自动迁回，如何手动干预？

这种情况下，我们可以使用`transfer source`功能，将 source 重新绑定到该 DM Worker。

### DM Worker 与 DM Master 保持心跳的超时时间及配置

在 DM v2.0.1 及之前版本，DM Worker 的超时时间为 10 秒，在 DM v2.0.2 及更新版本中超时时间为 60s。该值可以通过修改 DM Worker 的 `keepalive-ttl` 配置，单位为秒。

在 DM v2.0.2 及更新版本中，DM Worker 为 source 开启 relay-log 后，其超时时间将变为 1800 秒。该值可以通过修改 DM Worker 的 `relay-keepalive-ttl` 配置，单位为秒。

## DM 集群跨区域高可用

由上文可知，DM Master 的高可用依赖于 ETCD 实现，而 ETCD 高可用需要过半数节点存活。若仅考虑最大服务可用性，建议部署时选择奇数（≥3）个 Region/AZ 部署。DM Master 每个 Region/AZ 至少部署 1 个以避免单个 Region/AZ 故障导致 DM 集群无法服务。

由于单个 worker 仅能服务一个 source，因此每个 Region/AZ 还需要部署足够数量的空闲 worker，当某个 Region/AZ 故障时足以容纳该  Region/AZ 的所有 source。

> **注意：**
>
> 当跨 Region/AZ 部署时尤其需要注意其产生的流量等费用。
