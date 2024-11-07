---
title: Region 性能调优
summary: 了解如何通过调整 Region 大小等方法对 Region 进行性能调优以及如何在大 Region 下使用 bucket 进行并发查询优化。
---

# Region 性能调优

本文介绍了如何通过调整 Region 大小等方法对 Region 进行性能调优以及如何在大 Region 下使用 bucket 进行并发查询优化。同时，本文还介绍了通过开启 Active PD Follower 特性来提升 PD 为 TiDB 节点提供 Region 信息的服务能力。

## 概述

TiKV 自动将底层数据进行[分片](/best-practices/tidb-best-practices.md#数据分片)，所有数据按照 key 的范围划分为若干个 Region。当某个 Region 的大小超过一定限制后，TiKV 会将它分裂为多个 Region。

在大量数据的场景下，如果 Region 较小，可能会出现 Region 数量过多的情况，从而带来更多的资源开销和导致[性能回退](/best-practices/massive-regions-best-practices.md#性能问题)的问题。

> **说明：**
>
> - 在 v6.1.0 中，TiDB 支持设置自定义的 Region 大小，该特性为实验特性。
> - 从 v6.5.0 开始，该特性成为正式功能（GA）。
> - 从 v8.4.0 开始，Region 默认的大小从 96 MiB 调整为 256 MiB，将其调大可以减少 Region 个数。

开启 [Hibernate Region](/best-practices/massive-regions-best-practices.md#方法四开启-hibernate-region-功能) 或 [`Region Merge`](/best-practices/massive-regions-best-practices.md#方法五开启-region-merge) 也可以减少过多 Region 带来的性能开销。

## 使用 `region-split-size` 调整 Region 大小

> **注意：**
>
> Region 大小的推荐范围为 [48 MiB, 256 MiB]，常用的大小包括 96 MiB、128 MiB、256 MiB。不推荐将 Region 大小设置超过 1 GiB，强烈建议不超过 10 GiB。过大的 Region 可能带来以下影响：
>
> + 性能抖动。
> + 查询性能回退，尤其是大范围数据查询的性能会有回退。
> + 调度变慢。

Region 的大小可以通过 [`coprocessor.region-split-size`](/tikv-configuration-file.md#region-split-size) 进行设置。如果你使用了 TiFlash 或 Dumpling 工具，则 Region 大小不能超过 1 GiB。Region 调大以后，使用 Dumpling 工具时，需要降低并发，否则 TiDB 会有 OOM 的风险。

## 使用 bucket 增加并发

> **警告：**
>
> 当前该功能为实验特性，不建议在生产环境中使用。

Region 调大以后，如需进一步提高查询的并发度，可以设置 [`coprocessor.enable-region-bucket`](/tikv-configuration-file.md#enable-region-bucket-从-v610-版本开始引入) 为 `true`。这个配置会将每个 Region 划分为更小的区间 bucket，并且以这个更小的区间作为并发查询单位，以提高扫描数据的并发度。bucket 的大小通过 [`coprocessor.region-bucket-size`](/tikv-configuration-file.md#region-bucket-size-从-v610-版本开始引入) 来控制。

## 通过 Active PD Follower 提升 PD Region 信息查询服务的扩展能力

当集群的 Region 数量较多时，PD leader 处理心跳和调度任务的开销也较大，可能导致 CPU 资源紧张。如果同时集群中的 TiDB 实例数量较多，查询 Region 信息请求并发量较大，PD leader CPU 压力将变得更大，可能会造成 PD 服务不可用。

为确保服务的高可用性，PD leader 会将 Region 信息实时同步给 PD follower。PD follower 在内存中维护保存 Region 信息，从而具备处理 Region 信息请求的能力。你可以通过设置系统变量 [`pd_enable_follower_handle_region`](/system-variables.md#pd_enable_follower_handle_region-从-v760-版本开始引入) 开启 Active PD Follower 特性。启用该特性后，TiDB 在获取 Region 信息时会将请求均匀地发送到所有 PD 节点上，使 PD follower 也可以直接处理 Region 请求，从而降低减轻 PD leader 的 CPU 压力。

PD 通过维护 Region 同步流的状态，并结合 TiKV client-go 的 fallback 机制，确保 TiDB 中的 Region 信息始终是最新的。

- 当 PD leader 与 follower 之间网络不稳定或 follower 不可用导致 Region 同步流断开时，PD follower 将拒绝处理 Region 请求。此时，TiDB 会自动向 PD leader 重试请求，并将该 follower 暂时标记为不可用状态。
- 当网络稳定时，由于 PD leader 和 follower 之间的同步可能存在延迟，从 follower 获取的部分 Region 信息可能是过时的。在这种情况下，如果 Region 对应的 KV Request 失败，TiDB 会重新向 PD leader 请求最新的 Region 信息，并再次向 TiKV 发送 KV Request。