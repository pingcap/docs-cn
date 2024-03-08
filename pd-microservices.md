---
title: 使用 PD 微服务提高服务质量
summary: 介绍如何开启 PD 微服务模式提高服务质量。
---

# 使用 PD 微服务模式

从 v8.0.0 开始，PD 支持微服务模式。该模式可将 PD 的时间戳分配和集群调度功能拆分为以下微服务单独部署，从而与 PD 的路由功能解耦，让 PD 专注于元数据的路由服务。

- TSO 微服务：为整个集群提供单调递增的时间戳分配。
- Scheduling 微服务：为整个集群提供调度功能，包括但不限于负载均衡、热点处理、副本修复、副本放置等。

每个微服务都以独立进程的方式部署。当设置某个微服务的副本数大于 1 时，该微服务会自动实现主备的容灾模式，以确保服务的高可用性和可靠性。

## 使用场景

PD 微服务通常用于解决 PD 出现性能瓶颈的问题，提高 PD 服务质量。利用该特性，你可以避免以下问题：

- PD 集群压力过大而导致 TSO 分配的长尾或者抖动现象
- 调度模块故障导致整个集群服务不可用的问题
- PD 自身单点瓶颈的问题

此外，当调度模块发生变更时，你可以单独更新 Scheduling 微服务，无需再对 PD 进行重启，进而不会影响集群的整体服务。

> **注意：**
>
> 如果性能瓶颈本身不在 PD，则无需开启微服务。微服务本身会增加组件数量，提高运维成本。

## 使用限制

- TSO 微服务目前不支持动态启停，开启或关闭 TSO 微服务需要重启 PD 集群。
- 只有 TiDB 组件支持通过服务发现直接连接 TSO 微服务，其他的组件是通过请求转发的方式，将请求通过 PD 转发到 TSO 微服务以获取时间戳。
- 当前微服务与[同步部署模式 (DR Auto-Sync) ](/two-data-centers-in-one-city-deployment.md#简介) 特性不兼容。
- 与 TiDB 系统变量 `tidb_enable_tso_follower_proxy` 不兼容。
- 由于集群中可能存在静默 Region，Scheduling 微服务在进行主备切换时，为避免冗余调度，集群可能存在最多五分钟内没有调度的现象。

## 使用方法

目前 PD 微服务仅支持通过 TiDB Operator 进行部署。部署方法请参考 [TiDB Operator 文档](https://docs.pingcap.com/zh/tidb-in-kubernetes/dev/configure-a-tidb-cluster#部署-pd-微服务)。

- 开启微服务并重启 PD 后，PD 不再提供 TSO 分配功能，因此需要在集群中部署 TSO 微服务。
- 如果集群中部署了 Scheduling 微服务，调度功能将由 Scheduling 微服务提供。如果没有部署 Scheduling 微服务，调度功能仍然由 PD 提供。
- Scheduling 微服务支持动态切换功能。该功能默认开启（`enable-scheduling-fallback` 默认为 `true`)。如果 Scheduling 微服务进程关闭，PD 默认会继续为集群提供调度服务。

> **注意：**
>
> 如果 Scheduling 微服务和 PD 使用的 binary 版本不同，为防止调度逻辑出现变化，可以通过执行 `pd-ctl config set enable-scheduling-fallback false` 关闭 Scheduling 微服务动态切换功能。关闭后，如果 Scheduling 微服务的进程关闭，PD 将不会接管调度服务。这意味着，在 Scheduling 微服务重新启动前，集群将无法提供调度服务。

## 工具兼容性

微服务不影响数据导入导出以及其他同步工具的正常使用。

## 常见问题

- 如何判断 PD 是否达到了性能瓶颈?

  在集群自身状态正常的前提下，可以查看 Grafana PD 面板中的监控指标。如果 `TiDB - PD server TSO handle time` 指标出现明显延迟上涨或 `Heartbeat - TiKV side heartbeat statistics` 指标出现大量 pending，说明 PD 达到了性能瓶颈。

## 另请参阅

- [部署 PD 微服务](https://docs.pingcap.com/zh/tidb-in-kubernetes/dev/configure-a-tidb-cluster#部署-pd-微服务)
- [配置 PD 微服务](https://docs.pingcap.com/zh/tidb-in-kubernetes/dev/configure-a-tidb-cluster#配置-pd-微服务)
- [修改 PD 微服务](https://docs.pingcap.com/zh/tidb-in-kubernetes/dev/modify-tidb-configuration#配置-pd-微服务)
- [扩缩容 PD 微服务组件](https://docs.pingcap.com/zh/tidb-in-kubernetes/dev/scale-a-tidb-cluster#扩缩容-pd-微服务组件)
