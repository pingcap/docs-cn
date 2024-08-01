---
title: TiDB 中的各种超时
summary: 简单介绍 TiDB 中的各种超时，为排查错误提供依据。
---

# TiDB 中的各种超时

本章将介绍 TiDB 中的各种超时，为排查错误提供依据。

## GC 超时

TiDB 的事务的实现采用了 MVCC（多版本并发控制）机制，当新写入的数据覆盖旧的数据时，旧的数据不会被替换掉，而是与新写入的数据同时保留，并以时间戳来区分版本。TiDB 通过定期 GC 的机制来清理不再需要的旧数据。

- TiDB v4.0 之前的版本：

    默认情况下，TiDB 可以确保每个 MVCC 版本（一致性快照）保存 10 分钟。读取时间超过 10 分钟的事务，会收到报错 `GC life time is shorter than transaction duration`。

- TiDB v4.0 及之后的版本：

    正在运行的事务，如果持续时间不超过 24 小时，在运行期间 GC 会被阻塞，不会出现 `GC life time is shorter than transaction duration` 报错。

如果你确定在临时特殊场景中需要更长的读取时间，可以通过以下方式调大 MVCC 版本保留时间：

- TiDB v5.0 之前的版本 ：调整 `mysql.tidb` 表中的 `tikv_gc_life_time`。
- TiDB v5.0 及之后的版本：调整系统变量 [`tidb_gc_life_time`](/system-variables.md#tidb_gc_life_time-从-v50-版本开始引入)。

需要注意的是，此变量的配置是立刻影响全局的，调大它会增加当前所有快照的生命时长，调小它也会立即缩短所有快照的生命时长。过多的 MVCC 版本会影响 TiDB 的集群性能，因此在使用后，需要及时把此变量调整回之前的设置。

> **Tip:**
>
> 特别地，在 Dumpling 备份时，如果导出的数据量少于 1 TB 且导出的 TiDB 版本为 v4.0.0 或更新版本，并且 Dumpling 可以访问 TiDB 集群的 PD 地址以及 [`INFORMATION_SCHEMA.CLUSTER_INFO`](/information-schema/information-schema-cluster-info.md) 表，Dumpling 会自动调整 GC 的 safe point 从而阻塞 GC 且不会对原集群造成影响。以下场景除外：
>
> - 数据量非常大（超过 1 TB）。
> - Dumpling 无法直接连接到 PD，例如 TiDB 集群运行在 TiDB Cloud 上，或者 TiDB 集群运行在 Kubernetes 上且与 Dumpling 分离。
>
> 在这些场景中，你必须使用 `tikv_gc_life_time` 提前手动调长 GC 时间，以避免因为导出过程中发生 GC 导致导出失败。详见 TiDB 工具 Dumpling 的[手动设置 TiDB GC 时间](/dumpling-overview.md#手动设置-tidb-gc-时间)。

更多关于 GC 的信息，请参考 [GC 机制简介](https://pingcap.com/docs-cn/stable/reference/garbage-collection/overview/)文档。

## 事务超时

垃圾回收 (GC) 不会影响到正在执行的事务。但悲观事务的运行仍有上限，有基于事务超时的限制（TiDB 配置文件 [performance] 类别下的 `max-txn-ttl` 修改，默认为 60 分钟）和 基于事务使用内存的限制。

形如 `INSERT INTO t10 SELECT * FROM t1` 的 SQL 语句，不会受到 GC 的影响，但超过了 `max-txn-ttl` 的时间后，会由于超时而回滚。

## SQL 执行时间超时

TiDB 还提供了一个系统变量来限制单条 SQL 语句的执行时间：max_execution_time，它的默认值为 0，表示无限制。`max_execution_time` 目前对所有类型的 statement 生效，并非只对 SELECT 语句生效。其单位为 ms，但实际精度在 100ms 级别，而非更准确的毫秒级别。

## JDBC 查询超时

MySQL jdbc 的查询超时设置 `setQueryTimeout()` 对 TiDB 不起作用。这是因为现实客户端感知超时时，向数据库发送一个 KILL 命令。但是由于 tidb-server 是负载均衡的， 为防止在错误的 tidb-server 上终止连接， tidb-server 不会执行这个 KILL。这时就要用 `MAX_EXECUTION_TIME` 实现查询超时的效果。

TiDB 提供了三个与 MySQL 兼容的超时控制参数：

- **wait_timeout**，控制与 Java 应用连接的非交互式空闲超时时间。在 TiDB v5.4 及以上版本中，默认值为 `28800` 秒，即空闲超时为 8 小时。在 v5.4 之前，默认值为 `0`，即没有时间限制。
- **interactive_timeout**，控制与 Java 应用连接的交互式空闲超时时间，默认值为 8 小时。
- **max_execution_time**，控制连接中 SQL 执行的超时时间，默认值是 0，即允许连接无限忙碌（一个 SQL 语句执行无限的长的时间）。

但在实际生产环境中，空闲连接和一直无限执行的 SQL 对数据库和应用都有不好的影响。你可以通过在应用的连接字符串中配置这两个 session 级的变量来避免空闲连接和执行时间过长的 SQL 语句。例如，设置 `sessionVariables=wait_timeout=3600（1 小时）`和 `sessionVariables=max_execution_time=300000（5 分钟）`。
