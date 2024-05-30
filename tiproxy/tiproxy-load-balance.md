---
title: TiProxy 负载均衡策略
summary: 介绍 TiProxy 的负载均衡策略。
---

# TiProxy 负载均衡策略简介

在 TiProxy v1.0.0 中，TiProxy 只根据 TiDB 的健康状态和连接数来迁移连接。从 v1.1.0 版本开始，增加了 4 种负载均衡策略，并且可以配置它们的组合与优先级。

你可以通过配置项 [`priority-order`](/tiproxy/tiproxy-configuration.md#priority-order) 配置这些负载均衡策略是否启用、优先级顺序。例如：

- `["location", "cpu"]` 指根据地理位置和 CPU 使用率来负载均衡。TiProxy 就近路由到同地理位置的 TiDB server，同地理位置的 TiDB server 之间再根据 CPU 使用率来负载均衡。
- `["memory", "cpu", "location"]` 指根据内存、CPU 使用率、地理位置来负载均衡。当有 TiDB server 出现 OOM 风险时，优先根据内存迁移连接；当没有 TiDB server 有 OOM 风险时，根据 CPU 使用率负载均衡；当没有 TiDB server 有 OOM 风险且 CPU 使用率差异较小时，优先把连接路由到本地的 TiDB server。

# 负载均衡策略类型

> **注意：**
>
> 基于错误率、内存、CPU 的负载均衡都依赖于 Prometheus，因此请确保 Prometheus 可用，否则这些负载均衡策略将不生效。

## 基于错误率的负载均衡

TiProxy 通过从 Prometheus 查询 TiDB server 的错误速率，当一台 TiDB server 的每分钟错误数过高而其他 TiDB server 正常时，TiProxy 将该 TiDB server 的连接迁移到其他 TiDB server 上，实现自动故障转移。

该策略通过 [`indicators`](/tiproxy/tiproxy-configuration.md#indicators) 配置错误指标。默认的指标包含了 TiDB server 连接 PD、TiKV 失败的错误。

迁移连接的规则为：

- 当一台 TiDB server 的其中一个指标的 `query-expr` 查询结果超过 `fail-threshold` 时，认为该 TiDB server 出现异常。
- 当一台 TiDB server 的所有指标的 `query-expr` 查询结果低于 `recover-threshold` 时，认为该 TiDB server 正常。
- 当一台 TiDB server 出现异常，且另一台 TiDB server 正常时，TiProxy 会将连接从异常的 TiDB server 迁移到正常的 TiDB server。
- 当 TiDB server 从异常状态转为正常状态时，TiProxy 会根据其他的负载均衡策略（例如基于 CPU 的负载均衡）将连接迁移回该 TiDB server。

指标的选择应当遵循以下规则：

- 当 TiDB server 异常但该 TiDB server 上没有连接时，`query-expr` 查询结果应该大于 `fail-threshold`，否则 TiProxy 误以为该 TiDB server 恢复正常并将连接迁移回该 TiDB server。例如当 TiDB server 与 PD 断开连接时，由于后台任务连接 PD 失败，`tidb_tikvclient_backoff_seconds_count{type="pdRPC"}` 的值仍然大于 `fail-threshold`，因此 TiProxy 不会将连接迁移回来。
- 当 TiDB server 正常但 QPS 很高时，`query-expr` 查询结果应该小于 `recover-threshold`，否则 TiProxy 会误以为该 TiDB server 出错并将连接迁移到其他 TiDB server。

建议将 `indicators` 保持默认值。

## 基于内存的负载均衡

TiProxy 通过从 Prometheus 查询 TiDB server 的内存使用率，当 TiDB server 内存快速上升或使用率很高时，TiProxy 将该 TiDB server 的连接迁移到其他 TiDB server 上，避免因为 TiDB server 出现 OOM 导致不必要的连接断开。TiProxy 并不保证各个 TiDB server 的内存使用率接近，而是仅在 TiDB server 有 OOM 风险时才生效。

该策略有以下限制：

- 当 TiDB server 内存增长过快，在 30s 内就出现 OOM 时，TiProxy 不能及时判断 TiDB server 的 OOM 风险，因此仍然可能断开连接
- TiProxy 的目的是保持客户端连接不断开，而不是降低 TiDB server 的内存使用率以避免 OOM，因此 TiDB server 仍会 OOM
- 仅支持 v8.0.0 及以上版本的 TiDB server，当使用更低版本的 TiDB server 时该策略不生效

## 基于 CPU 的负载均衡

TiProxy 通过从 Prometheus 查询 TiDB server 的 CPU 使用率，将连接从 CPU 使用率较高的 TiDB server 迁移到使用率较低的 TiDB server 上，降低整体的查询延迟。TiProxy 并不会保证各个 TiDB server 的 CPU 使用率完全一致，而是保证 CPU 使用率的差异不会过大。

该策略适用于以下场景：

- 当有后台任务（例如 Analyze）占用较多 CPU 资源时，执行后台任务的 TiDB server 的 CPU 使用率更高，导致查询延迟更高
- 当不同连接上的工作负载差异较大时，尽管各个 TiDB server 上的连接数接近，但 CPU 使用率差异较大

当没有启用该策略时，TiProxy 根据连接数来实现负载均衡。

## 基于地理位置的负载均衡

TiProxy 根据自身和 TiDB server 的地理位置，将连接优先路由到本地的 TiDB server。该策略的优先级默认最低，以优先保证可用性和性能。如果需要调高它的优先级，建议保证同一地理位置的 TiDB server 至少为三台。

该策略适用于以下场景：

- TiDB 集群在云上跨可用区部署时，为了降低 TiProxy 与 TiDB server 之间的跨可用区流量费，TiProxy 优先将请求路由到同可用区的 TiDB server 上
- TiDB 集群跨数据中心部署时，为了降低 TiProxy 与 TiDB server 之间的网络延迟，TiProxy 优先将请求路由到同数据中心的 TiDB server 上

TiProxy 根据自身和 TiDB server 的标签确定各自的地理位置。你需要设置以下配置项：

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
        zone: z1
  - host: tiproxy-host-2
    config:
      labels:
        zone: z2
tidb_servers:
  - host: tidb-host-1
    config:
      labels:
        zone: z1
  - host: tidb-host-2
    config:
      labels:
        zone: z2
tikv_servers:
  - host: tikv-host-1
    port：20160
  - host: tikv-host-2
    port：20160
  - host: tikv-host-3
    port：20160
```

在以上配置中，`tiproxy-host-1` 上的 TiProxy 优先路由到 `tidb-host-1` 上的 TiDB server，`tiproxy-host-2` 上的 TiProxy 优先路由到 `tidb-host-2` 上的 TiDB server。