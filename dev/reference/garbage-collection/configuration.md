---
title: GC 配置
category: reference
---

# GC 配置

TiDB 的 GC 相关的配置存储于 `mysql.tidb` 系统表中，可以通过 SQL 语句对这些参数进行查询和更改：

```plain
mysql> select VARIABLE_NAME, VARIABLE_VALUE from mysql.tidb;
+--------------------------+----------------------------------------------------------------------------------------------------+
| VARIABLE_NAME            | VARIABLE_VALUE                                                                                     |
+--------------------------+----------------------------------------------------------------------------------------------------+
| bootstrapped             | True                                                                                               |
| tidb_server_version      | 33                                                                                                 |
| system_tz                | UTC                                                                                                |
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

```sql
update mysql.tidb set VARIABLE_VALUE="24h" where VARIABLE_NAME="tikv_gc_life_time";
```

> **注意：**
>
> `mysql.tidb` 系统表中除了下文将要列出的 GC 的配置以外，还包含一些 TiDB 用于储存部分集群状态（包括 GC 状态）的记录。请勿手动更改这些记录。其中，与 GC 有关的记录如下：
>
> - `tikv_gc_leader_uuid`，`tikv_gc_leader_desc` 和 `tikv_gc_leader_lease` 用于记录 GC leader 的状态
> - `tikv_gc_last_run_time`：上次 GC 运行时间
> - `tikv_gc_safe_point`：当前 GC 的 safe point

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
> - `tikv_gc_life_time` 的值必须大于 TiDB 的配置文件中的 [`max-txn-time-use`](/dev/reference/configuration/tidb-server/configuration-file.md#max-txn-time-use) 的值至少 10 秒，且不低于 10 分钟。
>
> - 在数据更新频繁的场景下，如果将 `tikv_gc_life_time` 设置得比较大（如数天甚至数月），可能会有一些潜在的问题，如：
>     - 磁盘空间占用较多。
>     - 大量的历史版本会在一定程度上影响性能，尤其是范围查询（如 `select count(*) from t`）。

## `tikv_gc_mode`

指定 GC 模式。可选值如下：

- `"distributed"`（默认）：分布式 GC 模式。在此模式下，[Do GC](/dev/reference/garbage-collection/overview.md#do-gc) 阶段由 TiDB 上的 GC leader 向 PD 发送 safe point，每个 TiKV 节点各自获取该 safe point 并对所有当前节点上作为 leader 的 Region 进行 GC。此模式于 TiDB 3.0 引入。

- `"central"`：集中 GC 模式。在此模式下，[Do GC](/dev/reference/garbage-collection/overview.md#do-gc) 阶段由 GC leader 向所有的 Region 发送 GC 请求。TiDB 2.1 及更早版本采用此 GC 模式。

## `tikv_gc_auto_concurrency`

控制是否由 TiDB 自动决定 GC concurrency，即同时进行 GC 的线程数。

当 `tikv_gc_mode` 设为 `"distributed"`，GC concurrency 将应用于 [Resolve Locks](/dev/reference/garbage-collection/overview.md#resolve-locks) 阶段。当 [`tikv_gc_mode`](#tikv_gc_mode) 设为 `"central"` 时，GC concurrency 将应用于 Resolve Locks 以及 [Do GC](/dev/reference/garbage-collection/overview.md#do-gc) 两个阶段。

- `true`（默认）：自动以 TiKV 节点的个数作为 GC concurrency
- `false`：使用 [`tikv_gc_concurrency`](#tikv_gc_concurrency) 的值作为 GC 并发数

## `tikv_gc_concurrency`

- 手动设置 GC concurrency。要使用该参数，必须将 [`tikv_gc_auto_concurrency`](#tikv_gc_auto_concurrency) 设为 `false` 。
- 默认值：2
