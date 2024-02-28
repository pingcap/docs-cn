---
title: 使用 PD 微服务提高服务质量
summary: 介绍如何开启 PD 微服务模式提高服务质量。
---

# 使用 PD 微服务模式

从 v8.0.0 开始，PD 支持微服务模式。该模式可将 PD 的时间戳分配和集群调度功能拆分为以下微服务单独部署，从而与 PD 的路由功能解耦，让 PD 专注于元数据的路由服务。

- TSO 微服务：为整个集群提供单调递增的时间戳分配。
- Scheduling 微服务：为整个集群提供调度功能，包括但不限于负载均衡、热点处理、副本修复、副本放置等。

每种微服务都以独立进程的方式部署，当相应服务设置的副本数量大于 1 时，提供主备的容灾模式。

## 使用场景

PD 微服务通常用于解决 PD 出现性能瓶颈的问题，提高 PD 服务质量。利用该特性，你可以避免以下问题：

- PD 集群压力过大而导致 TSO 分配的长尾或者抖动现象
- 调度模块故障导致整个集群服务不可用的问题
- PD 自身单点瓶颈的问题

此外，调度模块的变更可以单独更新 Scheduling 微服务，不需要再对 PD 进行重启，进而不会影响集群的整体服务。

> **注意：**
>
> 如果性能瓶颈本身不在 PD，则无需开启微服务。微服务本身会增加组件数量，提高运维成本。

## 使用限制

- TSO 微服务目前不支持动态启停，开启或关闭需要重启 PD 集群。
- 只有 TiDB 通过服务发现直接连接 TSO 微服务，其他的组件是通过请求转发的方式，将请求通过 PD 转发到 TSO 微服务获取时间戳。
- 当前微服务与 [同步部署模式 (DR Auto-Sync) ](/two-data-centers-in-one-city-deployment.md#简介) 特性不兼容。
- 与 TiDB 系统变量 `tidb_enable_tso_follower_proxy` 不兼容。
- 由于静默 region 的关系，Scheduling 微服务在进行主备切换时，为避免冗余调度，集群或存在至多五分钟没有调度的现象。

## 使用方法

目前 PD 微服务仅支持通过 TiDB Operator 进行部署。

开启微服务并重启 PD 后，PD 不再提供 TSO 分配功能，需要在集群中部署 TSO 微服务。此外，如果集群中部署了 scheduling 微服务，则由 scheduling 微服务提供调度功能，否则，由 PD 提供调度功能。

> **注意：**
>
> Scheduling 微服务支持动态切换，即如果 Scheduling 微服务进程关闭后，PD 默认会继续提供调度的服务。如果 Scheduling 微服务和 PD 使用不同的 binary 版本，为防止调度逻辑出现变化，可以通过设置 `pd-ctl config set enable-scheduling-fallback false` 禁止 Scheduling 微服务进程关闭后 PD 提供调度服务, 但是可能在 Scheduling 微服务进程重新启动前，集群将无法提供调度服务。该参数默认为 `true`。

## 工具兼容性

微服务不影响数据导入导出以及其他同步工具的正常使用。

## 常见问题

- 如何判断 PD 是否达到了性能瓶颈?

  在集群自身状态正常的前提下，可以查看 Grafana PD 面板中的监控指标。如果 `TiDB - PD server TSO handle time` 指标出现明显延迟上涨或 `Heartbeat - TiKV side heartbeat statistics` 指标出现大量 pending，说明 PD 达到了性能瓶颈。

## 另请参阅

TODO
