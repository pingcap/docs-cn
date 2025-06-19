---
title: TiDB 中的超时机制
summary: 了解 TiDB 中的超时机制，以及解决错误的方案。
---

# TiDB 中的超时机制

本文档描述了 TiDB 中的各种超时机制，帮助您排查错误。

## GC 超时

TiDB 的事务实现使用 MVCC（多版本并发控制）机制。当新写入的数据覆盖旧数据时，旧数据不会被替换，而是与新写入的数据一起保留。版本通过时间戳来区分。TiDB 使用定期垃圾回收（GC）机制来清理不再需要的旧数据。

- 对于早于 v4.0 的 TiDB 版本：

    默认情况下，每个 MVCC 版本（一致性快照）保留 10 分钟。读取时间超过 10 分钟的事务将收到错误 `GC life time is shorter than transaction duration`。

- 对于 TiDB v4.0 及更高版本：

    对于执行时间不超过 24 小时的运行中事务，垃圾回收（GC）在事务执行期间会被阻塞。不会出现错误 `GC life time is shorter than transaction duration`。

如果在某些情况下临时需要更长的读取时间，您可以增加 MVCC 版本的保留时间：

- 对于早于 v5.0 的 TiDB 版本：在 TiDB 的 `mysql.tidb` 表中调整 `tikv_gc_life_time`。
- 对于 TiDB v5.0 及更高版本：调整系统变量 [`tidb_gc_life_time`](/system-variables.md#tidb_gc_life_time-new-in-v50)。

请注意，系统变量配置会立即全局生效。增加其值会增加所有现有快照的生命周期，减少其值会立即缩短所有快照的生命周期。过多的 MVCC 版本会影响 TiDB 集群的性能。因此，您需要及时将此变量改回之前的设置。

<CustomContent platform="tidb">

> **提示：**
>
> 具体来说，当 Dumpling 从 TiDB 导出数据（小于 1 TB）时，如果 TiDB 版本是 v4.0.0 或更高版本，并且 Dumpling 可以访问 TiDB 集群的 PD 地址和 [`INFORMATION_SCHEMA.CLUSTER_INFO`](/information-schema/information-schema-cluster-info.md) 表，Dumpling 会自动调整 GC 安全点以阻止 GC，而不影响原始集群。
>
> 但是，在以下任一情况下，Dumpling 无法自动调整 GC 时间：
>
> - 数据量非常大（超过 1 TB）。
> - Dumpling 无法直接连接到 PD，例如，TiDB 集群在 TiDB Cloud 上或在与 Dumpling 分离的 Kubernetes 上。
>
> 在这种情况下，您必须提前手动延长 GC 时间，以避免在导出过程中因 GC 而导致导出失败。
>
> 更多详细信息，请参见[手动设置 TiDB GC 时间](/dumpling-overview.md#manually-set-the-tidb-gc-time)。

</CustomContent>

<CustomContent platform="tidb-cloud">

> **提示：**
>
> 具体来说，当 Dumpling 从 TiDB 导出数据（小于 1 TB）时，如果 TiDB 版本大于或等于 v4.0.0，并且 Dumpling 可以访问 TiDB 集群的 PD 地址，Dumpling 会自动延长 GC 时间，而不影响原始集群。
>
> 但是，在以下任一情况下，Dumpling 无法自动调整 GC 时间：
>
> - 数据量非常大（超过 1 TB）。
> - Dumpling 无法直接连接到 PD，例如，TiDB 集群在 TiDB Cloud 上或在与 Dumpling 分离的 Kubernetes 上。
>
> 在这种情况下，您必须提前手动延长 GC 时间，以避免在导出过程中因 GC 而导致导出失败。
>
> 更多详细信息，请参见[手动设置 TiDB GC 时间](https://docs.pingcap.com/tidb/stable/dumpling-overview#manually-set-the-tidb-gc-time)。

</CustomContent>

有关 GC 的更多信息，请参见 [GC 概述](/garbage-collection-overview.md)。

## 事务超时

在事务已启动但既未提交也未回滚的场景中，您可能需要更细粒度的控制和更短的超时时间，以防止长时间持有锁。在这种情况下，您可以使用 [`tidb_idle_transaction_timeout`](/system-variables.md#tidb_idle_transaction_timeout-new-in-v760)（在 TiDB v7.6.0 中引入）来控制用户会话中事务的空闲超时。

GC 不会影响正在进行的事务。但是，可以运行的悲观事务数量仍有上限，事务超时和事务使用的内存都有限制。您可以通过 TiDB 配置文件中 `[performance]` 类别下的 `max-txn-ttl` 修改事务超时时间，默认为 `60` 分钟。

像 `INSERT INTO t10 SELECT * FROM t1` 这样的 SQL 语句不受 GC 影响，但超过 `max-txn-ttl` 后会因超时而回滚。

## SQL 执行超时

TiDB 还提供了一个系统变量（`max_execution_time`，默认为 `0`，表示无限制）来限制单个 SQL 语句的执行时间。目前，该系统变量仅对只读 SQL 语句生效。`max_execution_time` 的单位是 `ms`，但实际精度是 `100ms` 级别而不是毫秒级别。

## JDBC 查询超时

MySQL JDBC 的 `setQueryTimeout()` 查询超时设置对 TiDB **_不_**起作用，因为当客户端检测到超时时，会向数据库发送 `KILL` 命令。但是，tidb-server 是负载均衡的，它不会执行这个 `KILL` 命令，以避免在错误的 tidb-server 上终止连接。您需要使用 `MAX_EXECUTION_TIME` 来检查查询超时效果。

TiDB 提供以下与 MySQL 兼容的超时控制参数。

- **wait_timeout**，控制与 Java 应用程序的非交互式空闲超时。从 TiDB v5.4 开始，`wait_timeout` 的默认值是 `28800` 秒，即 8 小时。对于早于 v5.4 的 TiDB 版本，默认值是 `0`，表示超时时间无限制。
- **interactive_timeout**，控制与 Java 应用程序的交互式空闲超时。默认值为 `8` 小时。
- **max_execution_time**，控制连接中 SQL 执行的超时时间，仅对只读 SQL 语句有效。默认值为 `0`，允许连接无限忙碌，即 SQL 语句可以无限长时间执行。

但是，在实际生产环境中，空闲连接和无限执行的 SQL 语句对数据库和应用程序都有负面影响。您可以通过在应用程序的连接字符串中配置这两个会话级变量来避免空闲连接和无限执行的 SQL 语句。例如，设置以下内容：

- `sessionVariables=wait_timeout=3600`（1 小时）
- `sessionVariables=max_execution_time=300000`（5 分钟）

## 需要帮助？

<CustomContent platform="tidb">

在 [Discord](https://discord.gg/DQZ2dy3cuc?utm_source=doc) 或 [Slack](https://slack.tidb.io/invite?team=tidb-community&channel=everyone&ref=pingcap-docs) 上询问社区，或[提交支持工单](/support.md)。

</CustomContent>

<CustomContent platform="tidb-cloud">

在 [Discord](https://discord.gg/DQZ2dy3cuc?utm_source=doc) 或 [Slack](https://slack.tidb.io/invite?team=tidb-community&channel=everyone&ref=pingcap-docs) 上询问社区，或[提交支持工单](https://tidb.support.pingcap.com/)。

</CustomContent>
