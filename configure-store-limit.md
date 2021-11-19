---
title: Store Limit
summary: 介绍 Store Limit 功能。
---

# Store Limit

Store Limit 是 PD 在 3.0 版本引入的特性，旨在能够更加细粒度地控制调度的速度，针对不同调度场景进行调优。

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

## 使用方法

Store Limit 相关的参数可以通过 `pd-ctl` 进行设置。

### 查看当前 store 的 limit 设置

查看当前 store 的 limit 示例如下：

{{< copyable "shell-regular" >}}

```bash
store limit                         // 显示所有 store 添加和删除 peer 的速度上限。
store limit add-peer                // 显示所有 store 添加 peer 的速度上限。
store limit remove-peer             // 显示所有 store 删除 peer 的速度上限。
```

### 设置全部 store 的 limit

设置全部 store 的 limit 示例如下：

{{< copyable "shell-regular" >}}

```bash
store limit all 5                   // 设置所有 store 添加和删除 peer 的速度上限为每分钟 5 个。
store limit all 5 add-peer          // 设置所有 store 添加 peer 的速度上限为每分钟 5 个。
store limit all 5 remove-peer       // 设置所有 store 删除 peer 的速度上限为每分钟 5 个。
```

### 设置单个 store 的 limit

设置单个 store 的 limit 示例如下：

{{< copyable "shell-regular" >}}

```bash
store limit 1 5                     // 设置 store 1 添加和删除 peer 的速度上限为每分钟 5 个。
store limit 1 5 add-peer            // 设置 store 1 添加 peer 的速度上限为每分钟 5 个。
store limit 1 5 remove-peer         // 设置 store 1 删除 peer 的速度上限为每分钟 5 个。
```
