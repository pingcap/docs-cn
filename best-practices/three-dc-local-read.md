---
title: 在三数据中心下就近读取数据
summary: 了解通过 Stale Read 功能在三数据中心下就近读取数据，减少跨数据中心请求。
---

# 在三数据中心下就近读取数据

在三数据中心模式下，Region 的三个副本都会隔离在各个数据中心里。然而在强一致读的要求下，tidb 的每一个查询都需要访问对应数据的 Leader 副本，而查询的来源可能和 Leader 所在的数据中心不一致，这就会引起跨数据中心的数据访问，从而造成访问的延迟上升。本文主要介绍使用 [Stale Read](/stale-read.md) 功能，以牺牲数据实时性的方式，避免跨数据中心的访问，从而降低访问的延迟。

## 部署三数据中心的 TiDB 集群

部署三数据中心的方法，参考[同城多数据中心部署 TiDB](/multi-data-centers-in-one-city-deployment.md)。

请注意，如果 TiKV 和 TiDB 都有 `labels` 配置项，在给 TiKV 和 TiDB 配置标签时，同一个数据中心下的 TiKV 和 TiDB 应该配置相同的 `zone` 标签。假设 TiKV 和 TiDB 都在 `dc-1` 数据中心下，那么两者都需要配置如下标签:

```
[labels]
zone=dc-1
```

## 使用 Stale Read 就近读取数据

[Stale Read](/stale-read.md) 为用户提供了一种读取历史数据的一种机制。使用 Stale Read 功能，你能从指定时间点或时间范围内读取对应的历史数据，从而避免数据同步带来延迟。在部分跨数据中心部署的场景中使用 Stale Read 功能，通过牺牲一定的实时性，TiDB 可就近访问对应数据所在当前中心的副本，避免跨数据中心的网络延迟，降低整体查询的访问延迟。

当 TiDB 收到 Stale Read 查询时，假如对应的 TiDB 配置了 `zone` 标签，就会将请求发送到对应数据副本所在 TiKV 拥有相同的 `zone` 标签的节点上。

如何使用 Stale Read 查询，参考[使用 AS OF TIMESTAMP 语法读取历史数据](/as-of-timestamp.md)。
