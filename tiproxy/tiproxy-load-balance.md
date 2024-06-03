---
title: TiProxy 负载均衡策略
summary: 介绍 TiProxy 的负载均衡策略。
---

# TiProxy 负载均衡策略简介

在 TiProxy v1.0.0 中，TiProxy 只根据 TiDB 的健康状态和连接数来迁移连接。从 v1.1.0 版本开始，增加了 4 种负载均衡策略，并且可以分别设置是否启用。

默认启用所有策略，且优先级的顺序依次为 `error`, `memory`, `cpu`, `location`，它的含义为：

1. 当有 TiDB server 的错误指标异常时，把连接从该 TiDB server 迁移到错误指标正常的 TiDB server。
2. 当以上情况不存在，且有 TiDB server 有 OOM 风险时，把连接从该 TiDB server 迁移到内存使用量较低的 TiDB server。
3. 当以上情况不存在，且有 TiDB server 的 CPU 使用率远高于其他 TiDB server 时，把连接从该 TiDB server 迁移到 CPU 使用率较低的 TiDB server。
4. 当以上情况不存在，则优先把请求路由到离 TiProxy 较近的 TiDB server。

# 负载均衡策略类型

> **注意：**
>
> 基于错误率、内存、CPU 的负载均衡都依赖于 Prometheus，因此请确保 Prometheus 可用，否则这些负载均衡策略将不生效。

## 基于错误率的负载均衡

TiProxy 通过从 Prometheus 查询 TiDB server 的错误速率，当一台 TiDB server 的每分钟错误数过高而其他 TiDB server 正常时，TiProxy 将该 TiDB server 的连接迁移到其他 TiDB server 上，实现自动故障转移。

该策略适用于以下场景：

- TiDB server 向 TiKV 发送请求频繁失败，导致执行 SQL 频繁失败
- TiDB server 向 PD 发送请求频繁失败，导致执行 SQL 频繁失败

## 基于内存的负载均衡

TiProxy 通过从 Prometheus 查询 TiDB server 的内存使用率，当 TiDB server 内存快速上升或使用率很高时，TiProxy 将该 TiDB server 的连接迁移到其他 TiDB server 上，避免因为 TiDB server 出现 OOM 导致不必要的连接断开。TiProxy 并不保证各个 TiDB server 的内存使用率接近，而是仅在 TiDB server 有 OOM 风险时才生效。

在 TiDB server 出现 OOM 风险时，TiProxy 会尽量迁移所有连接。OOM 通常是 Runaway Query 引起的，由于连接要等到事务结束才能迁移，因此正在执行中的 Runaway Query 不会迁移到其他 TiDB server 上重新执行。

该策略有以下限制：

- 当 TiDB server 内存增长过快，在 30s 内就出现 OOM 时，TiProxy 不能及时判断 TiDB server 的 OOM 风险，因此仍然可能断开连接
- TiProxy 的目的是保持客户端连接不断开，而不是降低 TiDB server 的内存使用率以避免 OOM，因此 TiDB server 仍会 OOM
- 仅支持 v8.0.0 及以上版本的 TiDB server，当使用更低版本的 TiDB server 时该策略不生效

## 基于 CPU 的负载均衡

TiProxy 通过从 Prometheus 查询 TiDB server 的 CPU 使用率，将连接从 CPU 使用率较高的 TiDB server 迁移到使用率较低的 TiDB server 上，降低整体的查询延迟。TiProxy 并不会保证各个 TiDB server 的 CPU 使用率完全一致，而是保证 CPU 使用率的差异不会过大。

该策略适用于以下场景：

- 当有后台任务（例如 Analyze）占用较多 CPU 资源时，执行后台任务的 TiDB server 的 CPU 使用率更高
- 当不同连接上的工作负载差异较大时，尽管各个 TiDB server 上的连接数接近，但 CPU 使用率差异较大
- 当集群内 TiDB server 的 CPU 资源配置不同时，即使连接数均衡，实际的 CPU 使用率也不均衡

当没有启用该策略，或 CPU 使用率已经均衡时，TiProxy 使用基于最少连接数的负载均衡策略，且该策略的优先级低于其他策略。

## 基于地理位置的负载均衡

TiProxy 根据自身和 TiDB server 的地理位置，将连接优先路由到本地的 TiDB server。

该策略适用于以下场景：

- TiDB 集群在云上跨可用区部署时，为了降低 TiProxy 与 TiDB server 之间的跨可用区流量费，TiProxy 优先将请求路由到同可用区的 TiDB server 上
- TiDB 集群跨数据中心部署时，为了降低 TiProxy 与 TiDB server 之间的网络延迟，TiProxy 优先将请求路由到同数据中心的 TiDB server 上

该策略的优先级默认最低，以优先保证可用性和性能。你可以通过设置 [`location-first`](/tiproxy/tiproxy-configuration.md#location-first) 为 `true` 来使该策略的优先级高于其他策略，但建议保证同一地理位置的 TiDB server 至少为三台，以保证可用性和性能。

TiProxy 根据自身和 TiDB server 的标签确定各自的地理位置。你需要同时设置以下配置项：

- 在 PD 的 [`location-labels`](/pd-configuration-file.md#location-labels) 中设置用于标识地理位置的标签。配置方式请参阅[设置 PD 的 `location-labels` 配置](/schedule-replicas-by-topology-labels.md#设置-pd-的-location-labels-配置)。
- 设置 TiDB server 用于标识地理位置的 [`labels`](/tidb-configuration-file.md#labels) 。配置方式请参阅[设置 TiDB 的 `labels`](/schedule-replicas-by-topology-labels.md#设置-tidb-的-labels可选)。
- 设置 TiProxy 用于标识地理位置的 [`labels`](/tiproxy/tiproxy-configuration.md#labels) 。

例如，假如根据 `zone` 标识地理位置，则如下配置集群：

```yaml
component_versions:
  tiproxy: "v1.1.0"
server_configs:
  pd:
    replication.location-labels: ["zone"]
  tidb:
    graceful-wait-before-shutdown: 15
tiproxy_servers:
  - host: tiproxy-host-1
    config:
      labels:
        zone: east
  - host: tiproxy-host-2
    config:
      labels:
        zone: west
tidb_servers:
  - host: tidb-host-1
    config:
      labels:
        zone: east
  - host: tidb-host-2
    config:
      labels:
        zone: west
tikv_servers:
  - host: tikv-host-1
    port：20160
  - host: tikv-host-2
    port：20160
  - host: tikv-host-3
    port：20160
```

在以上配置中，`tiproxy-host-1` 上的 TiProxy 优先路由到 `tidb-host-1` 上的 TiDB server，`tiproxy-host-2` 上的 TiProxy 优先路由到 `tidb-host-2` 上的 TiDB server。