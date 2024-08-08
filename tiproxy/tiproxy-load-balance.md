---
title: TiProxy 负载均衡策略
summary: 介绍 TiProxy 的负载均衡策略及其适用场景。
---

# TiProxy 负载均衡策略

在 TiProxy v1.0.0 中，TiProxy 仅支持基于 TiDB server 状态和连接数的负载均衡策略。从 v1.1.0 开始，TiProxy 新增了四种可独立配置的负载均衡策略：基于健康度、内存、CPU 和地理位置。

TiProxy 默认启用所有策略，优先级从高到低依次为：

1. 基于状态的负载均衡：当某个 TiDB server 正在关闭时，TiProxy 将连接从该 TiDB server 迁移到在线的 TiDB server。
2. 基于健康度的负载均衡：当某个 TiDB server 的健康度异常时，TiProxy 将连接从该 TiDB server 迁移到健康度正常的 TiDB server。
3. 基于内存的负载均衡：当某个 TiDB server 存在 Out of Memory (OOM) 风险时，TiProxy 将连接从该 TiDB server 迁移到内存使用量较低的 TiDB server。
4. 基于 CPU 的负载均衡：当某个 TiDB server 的 CPU 使用率远高于其他 TiDB server 时，TiProxy 将连接从该 TiDB server 迁移到 CPU 使用率较低的 TiDB server。
5. 基于地理位置的负载均衡：优先将请求路由到地理位置上距离 TiProxy 较近的 TiDB server。
6. 基于连接数的负载均衡：当某个 TiDB server 的连接数远高于其他 TiDB server 时，TiProxy 将连接从该 TiDB server 迁移到连接数较少的 TiDB server。

如需调整负载均衡策略的优先级，请参考[负载均衡策略配置](#负载均衡策略配置)。

## 基于状态的负载均衡

TiProxy 定时通过 SQL 端口和状态端口检查 TiDB 是否已下线或正在关闭。

## 基于健康度的负载均衡

TiProxy 查询 TiDB server 的错误数来判断 TiDB server 的健康度，当某个 TiDB server 的健康度异常而其他 TiDB server 正常时，TiProxy 将该 TiDB server 的连接迁移到其他 TiDB server 上，实现自动故障转移。

该策略适用于以下场景：

- TiDB server 向 TiKV 发送请求频繁失败，导致执行 SQL 频繁失败。
- TiDB server 向 PD 发送请求频繁失败，导致执行 SQL 频繁失败。

## 基于内存的负载均衡

TiProxy 查询 TiDB server 的内存使用率，当某个 TiDB server 内存快速上升或使用率很高时，TiProxy 将该 TiDB server 的连接迁移到其他 TiDB server 上，避免 OOM 导致不必要的连接断开。TiProxy 并不保证各个 TiDB server 的内存使用率接近，该策略仅在 TiDB server 存在 OOM 风险时生效。

当 TiDB server 出现 OOM 风险时，TiProxy 会尽量迁移该 TiDB server 的所有连接。通常情况下，如果 OOM 是由 Runaway Query 引起的，由于连接需等到事务结束才能迁移，因此正在执行中的 Runaway Query 不会迁移到其他 TiDB server 上重新执行。

该策略有以下限制：

- 当 TiDB server 的内存使用增长过快，在 30 秒内出现 OOM 时，TiProxy 可能无法及时判断 TiDB server 的 OOM 风险，因此仍可能断开连接。
- TiProxy 的目的是保持客户端连接不断开，而不是降低 TiDB server 的内存使用率以避免 OOM，因此 TiDB server 仍可能出现 OOM。
- 仅支持 v8.0.0 及以上版本的 TiDB server，当使用较低版本的 TiDB server 时该策略不生效。

## 基于 CPU 的负载均衡

TiProxy 查询 TiDB server 的 CPU 使用率，将连接从 CPU 使用率较高的 TiDB server 迁移到使用率较低的 TiDB server 上，降低整体的查询延迟。TiProxy 并不会保证各个 TiDB server 的 CPU 使用率完全一致，仅确保 CPU 使用率的差异不会过大。

该策略适用于以下场景：

- 当有后台任务（例如 Analyze）占用较多 CPU 资源时，执行后台任务的 TiDB server 的 CPU 使用率更高。
- 当不同连接上的工作负载差异较大时，即使各个 TiDB server 上的连接数接近，但 CPU 使用率差异较大。
- 当集群内 TiDB server 的 CPU 资源配置不同时，即使连接数均衡，实际的 CPU 使用率也不均衡。

## 基于地理位置的负载均衡

TiProxy 根据自身与 TiDB server 的地理位置，将连接优先路由到距离 TiProxy 较近的 TiDB server。

该策略适用于以下场景：

- 当 TiDB 集群在云上跨可用区部署时，为了降低 TiProxy 与 TiDB server 之间的跨可用区流量费用，TiProxy 优先将请求路由到同一可用区的 TiDB server 上。
- 当 TiDB 集群跨数据中心部署时，为了降低 TiProxy 与 TiDB server 之间的网络延迟，TiProxy 优先将请求路由到同一数据中心的 TiDB server 上。

该策略的优先级默认低于基于健康度、内存和 CPU 的负载均衡策略，你可以通过设置 [`policy`](/tiproxy/tiproxy-configuration.md#policy) 为 `location` 来提升该策略优先级，但建议确保同一地理位置的 TiDB server 至少有三台，以保证可用性和性能。

TiProxy 根据自身和 TiDB server 的 `zone` 标签确定各自的地理位置。你需要同时设置以下配置项：

- 在 TiDB server 的 [`labels`](/tidb-configuration-file.md#labels) 配置项中将 `zone` 设置为当前可用区。配置方式请参阅[设置 TiDB 的 `labels`](/schedule-replicas-by-topology-labels.md#设置-tidb-的-labels可选)。
- 在 TiProxy 的 [`labels`](/tiproxy/tiproxy-configuration.md#labels) 配置项中将 `zone` 设置为当前可用区。

如果是使用 TiDB Operator 部署的集群，请参考[数据的高可用](https://docs.pingcap.com/zh/tidb-in-kubernetes/stable/configure-a-tidb-cluster#数据的高可用)进行配置。

以下是一个集群配置的示例：

```yaml
component_versions:
  tiproxy: "v1.1.0"
server_configs:
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
    port: 20160
  - host: tikv-host-2
    port: 20160
  - host: tikv-host-3
    port: 20160
```

在以上配置中，`tiproxy-host-1` 与 `tidb-host-1` 的 `zone` 配置相同，因此 `tiproxy-host-1` 上的 TiProxy 会优先将请求路由到 `tidb-host-1` 上的 TiDB server。同理，`tiproxy-host-2` 上的 TiProxy 会优先将请求路由到 `tidb-host-2` 上的 TiDB server。

## 基于连接数的负载均衡

TiProxy 将连接从连接数较多的 TiDB server 迁移到连接数较少的 TiDB server。该策略不可配置且优先级最低。

TiProxy 通常根据 CPU 使用率来识别 TiDB server 的负载。该策略通常在以下场景下生效：

- TiDB 集群刚启动，所有 TiDB server 的 CPU 使用率接近 0，此时该策略防止启动时负载不均。
- 未启用[基于 CPU 的负载均衡](#基于-cpu-的负载均衡)时，使用该策略确保负载均衡。

## 负载均衡策略配置

TiProxy 支持通过配置项 [`policy`](/tiproxy/tiproxy-configuration.md#policy) 配置上述负载均衡策略的组合和优先级。

- `resource`：资源优先策略，优先级顺序依次为基于状态、健康度、内存、CPU、地理位置、连接数的负载均衡。
- `location`：地理优先策略，优先级顺序依次为基于状态、地理位置、健康度、内存、CPU、连接数的负载均衡。
- `connection`：最小连接数策略，优先级顺序依次为基于状态、连接数的负载均衡。

## 资源

关于 TiProxy 负载均衡策略更详细的信息，请参阅[设计文档](https://github.com/pingcap/tiproxy/blob/main/docs/design/2024-02-01-multi-factor-based-balance.md)。