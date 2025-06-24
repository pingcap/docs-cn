---
title: Stale Read 的使用场景
summary: 了解 Stale Read 及其使用场景。
---

# Stale Read 的使用场景

本文介绍 Stale Read 的使用场景。Stale Read 是 TiDB 用于读取存储在 TiDB 中的历史版本数据的机制。使用此机制，你可以读取特定时间点或指定时间范围内的相应历史数据，从而节省存储节点之间数据复制带来的延迟。

当你使用 Stale Read 时，TiDB 会随机选择一个副本进行数据读取，这意味着所有副本都可用于数据读取。如果你的应用程序无法容忍读取非实时数据，请不要使用 Stale Read；否则，从副本读取的数据可能不是写入 TiDB 的最新数据。

## 场景示例

<CustomContent platform="tidb">

+ 场景一：如果一个事务只涉及读操作，并且在一定程度上可以容忍数据不是最新的，你可以使用 Stale Read 来获取历史数据。使用 Stale Read 时，TiDB 以牺牲一定实时性能为代价，将查询请求发送到任意副本，从而提高查询执行的吞吐量。特别是在一些小表查询的场景中，如果使用强一致性读取，leader 可能会集中在某个存储节点上，导致查询压力也集中在该节点上。因此，该节点可能成为整个查询的瓶颈。而 Stale Read 可以提高整体查询吞吐量，显著提升查询性能。

+ 场景二：在一些地理分布式部署的场景中，如果使用强一致性的 follower 读取，为了确保从 Follower 读取的数据与存储在 Leader 中的数据一致，TiDB 需要从不同数据中心请求 `Readindex` 进行验证，这增加了整个查询过程的访问延迟。使用 Stale Read，TiDB 以牺牲一定实时性能为代价，访问当前数据中心的副本来读取相应数据，避免了跨中心连接带来的网络延迟，减少了整个查询的访问延迟。更多信息，请参见[三中心部署下的本地读取](/best-practices/three-dc-local-read.md)。

</CustomContent>

<CustomContent platform="tidb-cloud">

如果一个事务只涉及读操作，并且在一定程度上可以容忍数据不是最新的，你可以使用 Stale Read 来获取历史数据。使用 Stale Read 时，TiDB 以牺牲一定实时性能为代价，将查询请求发送到任意副本，从而提高查询执行的吞吐量。特别是在一些小表查询的场景中，如果使用强一致性读取，leader 可能会集中在某个存储节点上，导致查询压力也集中在该节点上。因此，该节点可能成为整个查询的瓶颈。而 Stale Read 可以提高整体查询吞吐量，显著提升查询性能。

</CustomContent>

## 使用方法

TiDB 提供以下语句级别、会话级别和全局级别的 Stale Read 方法：

- 语句级别
    - 指定精确时间点（**推荐**）：如果你需要 TiDB 读取特定时间点的全局一致数据，且不违反隔离级别，可以在查询语句中指定该时间点的对应时间戳。详细用法请参见 [`AS OF TIMESTAMP` 子句](/as-of-timestamp.md#语法)。
    - 指定时间范围：如果你需要 TiDB 在指定时间范围内读取尽可能新的数据，且不违反隔离级别，可以在查询语句中指定时间范围。在指定的时间范围内，TiDB 选择一个合适的时间戳来读取相应的数据。"合适"意味着在访问的副本上没有在此时间戳之前开始且尚未提交的事务，即 TiDB 可以在访问的副本上执行读取操作，且读取操作不会被阻塞。详细用法请参见 [`AS OF TIMESTAMP` 子句](/as-of-timestamp.md#语法)和 [`TIDB_BOUNDED_STALENESS` 函数](/as-of-timestamp.md#语法)的介绍。
- 会话级别
    - 指定时间范围：在会话中，如果你需要 TiDB 在后续查询中读取指定时间范围内尽可能新的数据，且不违反隔离级别，可以通过设置 `tidb_read_staleness` 系统变量来指定时间范围。详细用法请参见 [`tidb_read_staleness`](/tidb-read-staleness.md)。

此外，TiDB 还提供了通过设置 [`tidb_external_ts`](/system-variables.md#tidb_external_ts-new-in-v640) 和 [`tidb_enable_external_ts_read`](/system-variables.md#tidb_enable_external_ts_read-new-in-v640) 系统变量在会话或全局级别指定精确时间点的方式。详细用法请参见[使用 `tidb_external_ts` 进行 Stale Read](/tidb-external-ts.md)。

### 降低 Stale Read 延迟

Stale Read 功能会定期推进 TiDB 集群的 Resolved TS 时间戳，以确保 TiDB 读取满足事务一致性的数据。如果 Stale Read 使用的时间戳（例如 `AS OF TIMESTAMP '2016-10-08 16:45:26'`）大于 Resolved TS，Stale Read 会先触发 TiDB 推进 Resolved TS，并等待推进完成后再读取数据，导致延迟增加。

为了降低 Stale Read 延迟，你可以修改以下 TiKV 配置项，使 TiDB 更频繁地推进 Resolved TS 时间戳：

```toml
[resolved-ts]
advance-ts-interval = "20s" # 默认值为 "20s"。你可以设置为更小的值，如 "1s"，以更频繁地推进 Resolved TS 时间戳。
```

> **注意：**
>
> 减小上述 TiKV 配置项会导致 TiKV CPU 使用率和节点间流量增加。

<CustomContent platform="tidb">

关于 Resolved TS 的内部原理和诊断技术的更多信息，请参见[理解 TiKV 中的 Stale Read 和 safe-ts](/troubleshoot-stale-read.md)。

</CustomContent>

## 限制

当对表的 Stale Read 查询下推到 TiFlash 时，如果该表在查询指定的读取时间戳之后执行了较新的 DDL 操作，查询将返回错误。这是因为 TiFlash 仅支持读取具有最新 schema 的表的数据。

以下面的表为例：

```sql
create table t1(id int);
alter table t1 set tiflash replica 1;
```

一分钟后执行以下 DDL 操作：

```sql
alter table t1 add column c1 int not null;
```

然后，使用 Stale Read 查询一分钟前的数据：

```sql
set @@session.tidb_enforce_mpp=1;
select * from t1 as of timestamp NOW() - INTERVAL 1 minute;
```

TiFlash 将报告如下错误：

```
ERROR 1105 (HY000): other error for mpp stream: From MPP<query:<query_ts:1673950975508472943, local_query_id:18, server_id:111947, start_ts:438816196526080000>,task_id:1>: Code: 0, e.displayText() = DB::TiFlashException: Table 323 schema version 104 newer than query schema version 100, e.what() = DB::TiFlashException,
```

为避免此错误，你可以将 Stale Read 指定的读取时间戳更改为 DDL 操作之后的时间。
