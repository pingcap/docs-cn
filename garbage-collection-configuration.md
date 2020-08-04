---
title: GC 配置
aliases: ['/docs-cn/dev/garbage-collection-configuration/','/docs-cn/dev/reference/garbage-collection/configuration/']
---

# GC 配置

TiDB 的 GC 相关的配置存储于 `mysql.tidb` 系统表中，可以通过 SQL 语句对这些参数进行查询和更改：

{{< copyable "sql" >}}

```sql
select VARIABLE_NAME, VARIABLE_VALUE from mysql.tidb where VARIABLE_NAME like "tikv_gc%";
```

```
+--------------------------+----------------------------------------------------------------------------------------------------+
| VARIABLE_NAME            | VARIABLE_VALUE                                                                                     |
+--------------------------+----------------------------------------------------------------------------------------------------+
| tikv_gc_leader_uuid      | 5afd54a0ea40005                                                                                    |
| tikv_gc_leader_desc      | host:tidb-cluster-tidb-0, pid:215, start at 2019-07-15 11:09:14.029668932 +0000 UTC m=+0.463731223 |
| tikv_gc_leader_lease     | 20190715-12:12:14 +0000                                                                            |
| tikv_gc_enable           | true                                                                                               |
| tikv_gc_run_interval     | 10m0s                                                                                              |
| tikv_gc_life_time        | 10m0s                                                                                              |
| tikv_gc_last_run_time    | 20190715-12:09:14 +0000                                                                            |
| tikv_gc_safe_point       | 20190715-11:59:14 +0000                                                                            |
| tikv_gc_auto_concurrency | true                                                                                               |
| tikv_gc_mode             | distributed                                                                                        |
+--------------------------+----------------------------------------------------------------------------------------------------+
13 rows in set (0.00 sec)
```

例如，如果需要将 GC 调整为保留最近一天以内的数据，只需执行下列语句即可：

{{< copyable "sql" >}}

```sql
update mysql.tidb set VARIABLE_VALUE="24h" where VARIABLE_NAME="tikv_gc_life_time";
```

> **注意：**
>
> `mysql.tidb` 系统表中除了下文列出的 GC 的配置以外，还包含一些 TiDB 用于储存部分集群状态（包括 GC 状态）的记录。请勿手动更改这些记录。其中，与 GC 有关的记录如下：
>
> - `tikv_gc_leader_uuid`，`tikv_gc_leader_desc` 和 `tikv_gc_leader_lease` 用于记录 GC leader 的状态
> - `tikv_gc_last_run_time`：最近一次 GC 运行的时间（每轮 GC 开始时更新）
> - `tikv_gc_safe_point`：当前的 safe point （每轮 GC 开始时更新）

## `tikv_gc_enable`

- 控制是否启用 GC。
- 默认值：`true`

## `tikv_gc_run_interval`

- 指定 GC 运行时间间隔。Duration 类型，使用 Go 的 Duration 字符串格式，如 `"1h30m"`，`"15m"` 等。
- 默认值：`"10m0s"`

## `tikv_gc_life_time`

- 每次 GC 时，保留数据的时限。Duration 类型。每次 GC 时将以当前时间减去该配置的值作为 safe point。
- 默认值：`"10m0s"`

> **注意：**
>
> - 在数据更新频繁的场景下，如果将 `tikv_gc_life_time` 设置得比较大（如数天甚至数月），可能会有一些潜在的问题，如：
>     - 磁盘空间占用较多。
>     - 大量的历史版本会在一定程度上影响性能，尤其是范围查询（如 `select count(*) from t`）。
> - 如果存在运行时间很长、超过了 `tikv_gc_life_time` 的事务，那么在 GC 时，会保留自该事务的开始时间 (start_ts) 以来的数据，以允许该事务继续运行。例如，如果 `tikv_gc_life_time` 配置为 10 分钟，而某次 GC 时，集群中正在运行的事务中开始时间最早的一个事务已经运行了 15 分钟，那么本次 GC 便会保留最近 15 分钟的数据。

## `tikv_gc_mode`

指定 GC 模式。可选值如下：

- `"distributed"`（默认）：分布式 GC 模式。在此模式下，[Do GC](/garbage-collection-overview.md#do-gc进行-gc-清理) 阶段由 TiDB 上的 GC leader 向 PD 发送 safe point，每个 TiKV 节点各自获取该 safe point 并对所有当前节点上作为 leader 的 Region 进行 GC。此模式于 TiDB 3.0 引入。

- `"central"`：集中 GC 模式。在此模式下，[Do GC](/garbage-collection-overview.md#do-gc进行-gc-清理) 阶段由 GC leader 向所有的 Region 发送 GC 请求。TiDB 2.1 及更早版本采用此 GC 模式。

## `tikv_gc_auto_concurrency`

控制是否由 TiDB 自动决定 GC concurrency，即同时进行 GC 的线程数。

当 `tikv_gc_mode` 设为 `"distributed"`，GC concurrency 将应用于 [Resolve Locks](/garbage-collection-overview.md#resolve-locks清理锁) 阶段。当 [`tikv_gc_mode`](#tikv_gc_mode) 设为 `"central"` 时，GC concurrency 将应用于 Resolve Locks 以及 [Do GC](/garbage-collection-overview.md#do-gc进行-gc-清理) 两个阶段。

- `true`（默认）：自动以 TiKV 节点的个数作为 GC concurrency
- `false`：使用 [`tikv_gc_concurrency`](#tikv_gc_concurrency) 的值作为 GC 并发数

## `tikv_gc_concurrency`

- 手动设置 GC concurrency。要使用该参数，必须将 [`tikv_gc_auto_concurrency`](#tikv_gc_auto_concurrency) 设为 `false` 。
- 默认值：2

## `tikv_gc_scan_lock_mode`

> **警告：**
>
> Green GC 目前是实验性功能，不建议在生产环境中使用。

设定 GC 的 Resolve Locks 阶段中，扫描锁的方式，即是否开启 Green GC（实验性特性）。Resolve Locks 阶段需要扫描整个集群的锁。在不开启 Green GC 的情况下，TiDB 会以 Region 为单位进行扫描。Green GC 提供了“物理扫描”的功能，即每台 TiKV 节点分别绕过 Raft 层直接扫描数据。该功能可以有效缓解 [Hibernate Region](/tikv-configuration-file.md#raftstorehibernate-regions-实验特性) 功能开启时，GC 唤醒全部 Region 的现象，并一定程度上提升 Resolve Locks 阶段的执行速度。

- `"legacy"`（默认）：使用旧的扫描方式，即关闭 Green GC。
- `"physical"`：使用物理扫描的方式，即开启 Green GC。

> **注意：**
> 
> 该项配置是隐藏配置。首次开启需要执行：
> 
> {{< copyable "sql" >}}
> 
> ```sql
> insert into mysql.tidb values ('tikv_gc_scan_lock_mode', 'legacy', '');
> ```

## 关于 GC 流程的说明

从 TiDB 3.0 版本起，由于对分布式 GC 模式和并行 Resolve Locks 的支持，部分配置选项的作用发生了变化。可根据下表理解不同版本中这些配置的区别：

| 版本/配置          |  Resolve Locks          |  Do GC  |
|-------------------|---------------|----------------|
| 2.x               | 串行 | 并行 |
| 3.0 <br/> `tikv_gc_mode = centered` <br/> `tikv_gc_auto_concurrency = false` | 并行 | 并行 |
| 3.0 <br/> `tikv_gc_mode = centered` <br/> `tikv_gc_auto_concurrency = true` | 自动并行 | 自动并行 |
| 3.0 <br/> `tikv_gc_mode = distributed` <br/> `tikv_gc_auto_concurrency = false` | 并行 | 分布式 |
| 3.0 <br/> `tikv_gc_mode = distributed` <br/> `tikv_gc_auto_concurrency = true` <br/> （默认配置） | 自动并行 | 分布式 |

表格内容说明：

- 串行：由 TiDB 逐个向 Region 发送请求。
- 并行：使用 `tikv_gc_concurrency` 选项所指定的线程数，并行地向每个 Region 发送请求。
- 自动并行：使用 TiKV 节点的个数作为线程数，并行地向每个 Region 发送请求。
- 分布式：无需 TiDB 通过对 TiKV 发送请求的方式来驱动，而是每台 TiKV 自行工作。

另外，如果 Green GC （实验特性）开启（即 [`tikv_gc_scan_lock_mode`](#tikv_gc_scan_lock_mode) 配置项设为 `"physical"`），Resolve Lock 的执行将不受上述并行配置的影响。

## 流控

TiKV 在 3.0.6 版本开始支持 GC 流控，可通过配置 `gc.max-write-bytes-per-sec` 限制 GC worker 每秒数据写入量，降低对正常请求的影响，`0` 为关闭该功能。该配置可通过 tikv-ctl 动态修改：

{{< copyable "shell-regular" >}}

```bash
tikv-ctl --host=ip:port modify-tikv-config -m server -n gc.max_write_bytes_per_sec -v 10MB
```
