---
title: Store Limit
summary: 介绍 Store Limit 功能。
aliases: ['/docs-cn/dev/configure-store-limit/']
---

# Store Limit

Store Limit 是一个 PD 特性，旨在更精细地控制调度速度，以在不同场景下实现更好的性能。

## 实现原理

PD 的调度是以 operator 为单位执行的。一个 operator 可能包含多个调度操作。示例如下；

```
"replace-down-replica {mv peer: store [2] to [3]} (kind:region,replica, region:10(4,5), createAt:2020-05-18 06:40:25.775636418 +0000 UTC m=+2168762.679540369, startAt:2020-05-18 06:40:25.775684648 +0000 UTC m=+2168762.679588599, currentStep:0, steps:[add learner peer 20 on store 3, promote learner peer 20 on store 3 to voter, remove peer on store 2])"
```

以上示例中，`replace-down-replica` 这个 operator 具体包含以下操作：

1. 在 `store 3` 上添加一个 learner peer，ID 为 `20`。
2. 将 `store 3` 上 ID 为 `20` 的 learner peer 提升为 voter。
3. 删除 `store 2` 上的 peer。

Store Limit 是通过在内存中维护了一个 store ID 到令牌桶的映射，来实现 store 级别的限速。这里不同的操作对应不同的令牌桶，目前仅支持限制添加 learner/peer 和删除 peer 两种操作的速度，即对应于每个 store 存在两种类型的令牌桶。

每次 operator 产生后会检查所包含的操作对应的令牌桶中是否有足够的 token。如果 token 充足才会将该 operator 加入到调度的队列中，同时从令牌桶中拿走对应的 token，否则该 operator 被丢弃。令牌桶会按照固定的速率补充 token，从而实现限速的目的。

Store Limit 与 PD 其他 limit 相关的参数（如 `region-schedule-limit`，`leader-schedule-limit` 等）不同的是，Store Limit 限制的主要是 operator 的消费速度，而其他的 limit 主要是限制 operator 的产生速度。引入 Store Limit 特性之前，调度的限速主要是全局的，所以即使限制了全局的速度，但还是有可能存在调度都集中在部分 store 上面，因而影响集群的性能。而 Store Limit 通过将限速的粒度进一步细化，可以更好的控制调度的行为。

Store Limit 定义了每分钟操作的最大数量。假设 Store Limit 为每分钟 5 次操作，向集群添加新节点将以每分钟 5 个 Region（`add-peer` 操作）的速度进行。如果需要为 15 个 Region 执行 `add-peer`，则该操作将需要 3 分钟 (15 / 5 = 3)，并且如果每个 Region 为 96 MiB，将消耗最高 8 MiB/s ((5 × 96) / 60 = 8)。

## 使用方法

Store Limit 相关的参数可以通过 [`PD Control`](/pd-control.md) 进行设置。

### 查看当前 store 的 limit 设置

查看当前 store 的 limit 示例如下：

```bash
tiup ctl:v<CLUSTER_VERSION> pd store limit             // 显示所有 store 添加和删除 peer 的速度上限。
tiup ctl:v<CLUSTER_VERSION> pd store limit add-peer    // 显示所有 store 添加 peer 的速度上限。
tiup ctl:v<CLUSTER_VERSION> pd store limit remove-peer // 显示所有 store 删除 peer 的速度上限。
```

### 设置全部 store 的 limit

设置全部 store 的 limit 示例如下：

```bash
tiup ctl:v<CLUSTER_VERSION> pd store limit all 5                   // 设置所有 store 添加和删除 peer 的速度上限为每分钟 5 个。
tiup ctl:v<CLUSTER_VERSION> pd store limit all 5 add-peer          // 设置所有 store 添加 peer 的速度上限为每分钟 5 个。
tiup ctl:v<CLUSTER_VERSION> pd store limit all 5 remove-peer       // 设置所有 store 删除 peer 的速度上限为每分钟 5 个。
```

### 设置单个 store 的 limit

设置单个 store 的 limit 示例如下：

```bash
tiup ctl:v<CLUSTER_VERSION> pd store limit 1 5                     // 设置 store 1 添加和删除 peer 的速度上限为每分钟 5 个。
tiup ctl:v<CLUSTER_VERSION> pd store limit 1 5 add-peer            // 设置 store 1 添加 peer 的速度上限为每分钟 5 个。
tiup ctl:v<CLUSTER_VERSION> pd store limit 1 5 remove-peer         // 设置 store 1 删除 peer 的速度上限为每分钟 5 个。
```

## Store Limit v2 原理

当 [`store-limit-version`](/pd-configuration-file.md#store-limit-version-从-v710-版本开始引入) 设置为 `v2` 时，Store Limit v2 生效。在此模式下，Operator 调度限制将根据 TiKV Snapshot 执行情况进行动态调整。当 TiKV 积压的任务较少时，PD 会增加其调度任务。相反，PD 会减少对该节点的调度任务。此时，你无需关注如何设置 `store limit` 以加快调度进度。

在该模式下，TiKV 执行速度成为迁移进度的主要瓶颈。你可以通过 **TiKV Details** > **Snapshot** > **Snapshot Speed** 面板判断当前调度速度是否达到 TiKV 限流设置。通过调整 TiKV Snapshot Limit ([`snap-io-max-bytes-per-sec`](/tikv-configuration-file.md#snap-io-max-bytes-per-sec)) 来增加或减少该节点的调度速度。
