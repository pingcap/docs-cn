---
title: 海量 Region 集群调优最佳实践
summary: 了解海量 Region 导致性能问题的原因和优化方法。
aliases: ['/docs-cn/v2.1/best-practices/massive-regions-best-practices/','/docs-cn/v2.1/reference/best-practices/massive-regions/']
---

# 海量 Region 集群调优最佳实践

在 TiDB 的架构中，所有数据以一定 key range 被切分成若干 Region 分布在多个 TiKV 实例上。随着数据的写入，一个集群中会产生上百万个甚至千万个 Region。单个 TiKV 实例上产生过多的 Region 会给集群带来较大的负担，影响整个集群的性能表现。

本文将介绍 TiKV 核心模块 Raftstore 的工作流程，海量 Region 导致性能问题的原因，以及优化性能的方法。

## Raftstore 的工作流程

一个 TiKV 实例上有多个 Region。Region 消息是通过 Raftstore 模块驱动 Raft 状态机来处理的。这些消息包括 Region 上读写请求的处理、Raft log 的持久化和复制、Raft 的心跳处理等。但是，Region 数量增多会影响整个集群的性能。为了解释这一点，需要先了解 TiKV 的核心模块 Raftstore 的工作流程。

![图 1 Raftstore 处理流程示意图](/media/best-practices/raft-process.png)

> **注意：**
>
> 该图仅为示意，不代表代码层面的实际结构。

上图是 Raftstore 处理流程的示意图。如图所示，从 TiDB 发来的请求会通过 gRPC 和 storage 模块变成最终的 KV 读写消息，并被发往相应的 Region，而这些消息并不会被立即处理而是被暂存下来。Raftstore 会轮询检查每个 Region 是否有需要处理的消息。如果 Region 有需要处理的消息，那么 Raftstore 会驱动 Raft 状态机去处理这些消息，并根据这些消息所产生的状态变更去进行后续操作。例如，在有写请求时，Raft 状态机需要将日志落盘并且将日志发送给其他 Region 副本；在达到心跳间隔时，Raft 状态机需要将心跳信息发送给其他 Region 副本。

## 性能问题

从 Raftstore 处理流程示意图可以看出，需要依次处理各个 Region 的消息。那么在 Region 数量较多的情况下，Raftstore 需要花费一些时间去处理大量 Region 的心跳，从而带来一些延迟，导致某些读写请求得不到及时处理。如果读写压力较大，Raftstore 线程的 CPU 使用率容易达到瓶颈，导致延迟进一步增加，进而影响性能表现。

通常在有负载的情况下，如果 Raftstore 的 CPU 使用率达到了 85% 以上，即可视为达到繁忙状态且成为了瓶颈，同时 `propose wait duration` 可能会高达百毫秒级别。

> **注意：**
>
> + Raftstore 的 CPU 使用率是指单线程的情况。如果是多线程 Raftstore，可等比例放大使用率。
> + 由于 Raftstore 线程中有 I/O 操作，所以 CPU 使用率不可能达到 100%。

### 性能监控

可在 Grafana 的 TiKV 面板下查看相关的监控 metrics：

+ Thread-CPU 下的 `Raft store CPU`

    参考值：低于 `raftstore.store-pool-size * 85%`。在 v2.1 版本中无此配置项，因此在 v2.1 中可视为 `raftstore.store-pool-size = 1`。

    ![图 2 查看 Raftstore CPU](/media/best-practices/raft-store-cpu.png)

+ Raft Propose 下的 `Propose wait duration`

    `Propose wait duration` 是从发送请求给 Raftstore，到 Raftstore 真正开始处理请求之间的延迟时间。如果该延迟时间较长，说明 Raftstore 比较繁忙或者处理 append log 比较耗时导致 Raftstore 不能及时处理请求。

    参考值：低于 50-100ms。

    ![图 3 查看 Propose wait duration](/media/best-practices/propose-wait-duration.png)

## 性能优化方法

找到性能问题的根源后，可从以下两个方向来解决性能问题：

+ 减少单个 TiKV 实例的 Region 数
+ 减少单个 Region 的消息数

v2.1 版本中的 Raftstore 为单线程。因此 Region 数超过 10 万后，Raftstore 线程的 CPU 使用率会逐渐成为瓶颈。

### 方法一：增加 TiKV 实例

如果 I/O 资源和 CPU 资源都比较充足，可在单台机器上部署多个 TiKV 实例，以减少单个 TiKV 实例上的 Region 个数；或者增加 TiKV 集群的机器数。

### 方法二：开启 `Region Merge`

开启 `Region Merge` 也能减少 Region 的个数。与 `Region Split` 相反，`Region Merge` 是通过调度把相邻的小 Region 合并的过程。在集群中删除数据或者执行 `Drop Table`/`Truncate Table` 语句后，可以将小 Region 甚至空 Region 进行合并以减少资源的消耗。

通过 pd-ctl 设置以下参数即可开启 `Region Merge`：

{{< copyable "" >}}

```
>> pd-ctl config set max-merge-region-size 20
>> pd-ctl config set max-merge-region-keys 200000
>> pd-ctl config set merge-schedule-limit 8
```

> **注意：**
>
> `Region Merge` 已在 TiDB v3.0 中默认开启。

详情请参考[如何配置 Region Merge](https://github.com/tikv/tikv/blob/master/docs/how-to/configure/region-merge.md)。

同时，默认配置的 `Region Merge` 的参数设置较为保守，可以根据需求参考 [PD 调度策略最佳实践](/best-practices/pd-scheduling-best-practices.md#region-merge-速度慢) 中提供的方法加快 `Region Merge` 过程的速度。

#### 方法三：调整 `raft-base-tick-interval`

除了减少 Region 个数外，还可以通过减少 Region 单位时间内的消息数量来减小 Raftstore 的压力。例如，在 TiKV 配置中适当调大 `raft-base-tick-interval`：

{{< copyable "" >}}

```
[raftstore]
raft-base-tick-interval = "2s"
```

`raft-base-tick-interval` 是 Raftstore 驱动每个 Region 的 Raft 状态机的时间间隔，也就是每隔该时长就需要向 Raft 状态机发送一个 tick 消息。增加该时间间隔，可以有效减少 Raftstore 的消息数量。

需要注意的是，该 tick 消息的间隔也决定了 `election timeout` 和 `heartbeat` 的间隔。示例如下：

{{< copyable "" >}}

```
raft-election-timeout = raft-base-tick-interval * raft-election-timeout-ticks
raft-heartbeat-interval = raft-base-tick-interval * raft-heartbeat-ticks
```

如果 Region Follower 在 `raft-election-timeout` 间隔内未收到来自 Leader 的心跳，就会判断 Leader 出现故障而发起新的选举。`raft-heartbeat-interval` 是 Leader 向 Follower 发送心跳的间隔，因此调大 `raft-base-tick-interval` 可以减少单位时间内 Raft 发送的网络消息，但也会让 Raft 检测到 Leader 故障的时间更长。

## 其他问题和解决方案

### 切换 PD Leader 的速度慢

PD 需要将 Region Meta 信息持久化在 etcd 上，以保证切换 PD Leader 节点后 PD 能快速继续提供 Region 路由服务。随着 Region 数量的增加，etcd 出现性能问题，使得 PD 在切换 Leader 时从 etcd 获取 Region Meta 信息的速度较慢。在百万 Region 量级时，从 etcd 获取信息的时间可能需要十几秒甚至几十秒。

因此在 v3.0 版本中，PD 默认开启配置项 `use-region-storage`，将 Region Meta 信息存在本地的 LevelDB 中，并通过其他机制同步 PD 节点间的信息。如果在 v2.1 版本中碰到类似问题，建议升级到 v3.0。

### PD 路由信息更新不及时

在 TiKV 中，pd-worker 模块将 Region Meta 信息定期上报给 PD，在 TiKV 重启或者切换 Region Leader 时需要通过统计信息重新计算 Region 的 `approximate size/keys`。因此在 Region 数量较多的情况下，pd-worker 单线程可能成为瓶颈，造成任务得不到及时处理而堆积起来。因此 PD 不能及时获取某些 Region Meta 信息以致路由信息更新不及时。该问题不会影响实际的读写，但可能导致 PD 调度不准确以及 TiDB 更新 Region cache 时需要多几次 round-trip。

可在 TiKV Grafana 面板中查看 Task 下的 Worker pending tasks 来确定 pd-worker 是否有任务堆积。通常来说，pending tasks 应该维持在一个比较低的值。

![图 4 查看 pd-worker](/media/best-practices/pd-worker-metrics.png)

目前已经在 [TiKV master](https://github.com/tikv/tikv/tree/master) 上对 pd-worker 进行了[效率优化](https://github.com/tikv/tikv/pull/5620)。[TiDB v3.0.5](https://pingcap.com/docs-cn/stable/releases/3.0.5/) 中已带上该优化。如果碰到类似问题，建议升级至 v3.0.5。

### Prometheus 查询 metrics 的速度慢

在大规模集群中，随着 TiKV 实例数的增加，Prometheus 查询 metrics 时的计算压力较大，导致 Grafana 查看 metrics 的速度较慢。v3.0 版本中设置了一些 metrics 的预计算，让这个问题有所缓解。
