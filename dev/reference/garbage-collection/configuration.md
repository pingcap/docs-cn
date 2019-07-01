---
title: GC 配置
category: reference
---

# GC 配置

TiDB 的 GC 相关的配置存储于 `mysql.tidb` 系统表中，以下列出这些参数及其含义。可以通过 SQL 语句对这些参数进行查询和更改。例如，如果需要将 GC 调整为每 30 分钟执行一次，只需执行下列语句即可：

```sql
update mysql.tidb set VARIABLE_VALUE="30m" where VARIABLE_NAME="tikv_gc_run_interval";
```

> **注意：**
>
> `mysql.tidb` 系统表中除了下文将要列出列出的 GC 的配置以外，还包含一些 TiDB 用于储存部分集群状态（包括 GC 状态）的记录。请勿手动更改这些记录。其中，与 GC 有关的记录如下：
>
> - `tikv_gc_leader_uuid`，`tikv_gc_leader_desc` 和 `tikv_gc_leader_lease` 用于记录 GC leader 的状态和进行 GC leader 的选举
> - `tikv_gc_last_run_time`：上次 GC 运行时间
> - `tikv_gc_safe_point`：当前的 GC safe point

## `tikv_gc_enable`

- 控制是否启用 GC。
- 默认值：`true`

## `tikv_gc_run_interval`

- 指定 GC 运行时间间隔。Duration 类型，使用 Go 的 Duration 字符串格式，如 `"1h30m"`，`"15m"` 等。
- 默认值：10 分钟（`"10m0s"`）

## `tikv_gc_life_time`

- 每次 GC 时，保留数据的时限。Duration 类型。每次 GC 时将以当前时间减去该配置的值作为 safe point。
- 默认值：10 分钟（`"10m0s"`）

> **注意：**
>
> - `tikv_gc_life_time` 的值必须大于 TiDB 的配置文件中的 [`max-txn-time-use`](/reference/configuration/tidb-server/configuration-file/#max-txn-time-use) 的值至少 10 秒，且不低于 10 分钟。
>
> - 在数据更新频繁的场景下，如果将 `tikv_gc_life_time` 设置得比较大（如数天甚至数月），可能会有一些潜在的问题，如：
>    - 磁盘空间占用较多；
>    - 大量的历史版本会在一定程度上影响性能，尤其是范围查询（`如 select count(*) from t`）。

## `tikv_gc_mode`

指定 GC 模式。可选值如下：

- `"distributed"`（默认）: GC 的第三阶段 ，GC leader 向 PD 发送 safe point 即可结束，每个 TiKV 节点各自获取该 safe point 并对所有 leader 在本机上的 Region 进行 GC。请参考 [GC 机制简介](/reference/garbage-collection/overview.md)。

- `"central"`：GC 的第三阶段采用 2.X 版本所使用的旧的 GC 方式，即由 GC leader 向所有的 Region 发送 GC 请求。

## `tikv_gc_auto_concurrency`

控制是否由 TiDB 自动决定 GC concurrency，即同时进行 GC 的线程数。 。

GC concurrency 将用于 [Resolve Locks](/reference/garbage-collection/overview.md#resolve-locks)。当 [`tikv_gc_mode`](#tikv_gc_mode) 配置为 `"central"` 时，也将被用于 [Do GC](/reference/garbage-collection/overview.md#do-gc) 阶段。

- `true`(默认): TiDB 将以 TiKV 节点的个数作为 GC concurrency
- `false`: 使用 [`tikv_gc_concurrency`](#tikv_gc_concurrency) 的值作为 GC concurrency

## `tikv_gc_concurrency`

- V3.0 起，当 [`tikv_gc_auto_concurrency`](#tikv_gc_auto_concurrency) 为 `false` 时，将使用该值作为 GC concurrency。对于 2.x 版本，将直接使用该值作为 GC concurrency。
- 默认值：2
