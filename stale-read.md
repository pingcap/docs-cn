---
title: Stale Read 功能的使用场景
summary: 介绍 Stale Read 功能和使用场景。
---

# Stale Read 功能的使用场景

本文档介绍 Stale Read 的使用场景。Stale Read 是一种读取历史数据版本的机制，读取 TiDB 中存储的历史数据版本。通过 Stale Read 功能，你能从指定时间点或时间范围内读取对应的历史数据，从而避免数据同步带来延迟。当使用 Stale Read 时，TiDB 默认会随机选择一个副本来读取数据，因此能利用所有副本。如果你的应用程序不能容忍读到非实时的数据，请勿使用 Stale Read，否则读到的数据可能不是最新成功写入的数据。

## 场景描述

+ 场景一：如果一个事务仅涉及只读操作，并且一定程度上可容忍牺牲实时性，你可以使用 Stale Read 功能来读取历史数据。由于牺牲了一定的实时性，使用 Stale Read 后，TiDB 可以让请求分发到任一个副本上，使得查询的执行获得更大的吞吐量。特别是在一些小表的查询场景中，如果使用了强一致性读，Leader 可能集中在某一个存储节点上，导致查询压力集中在该节点，成为整个查询的瓶颈。通过 Stale Read，可以提升了查询整体的吞吐能力，从而显著提升查询性能。

+ 场景二：在部分跨数据中心部署的场景中，如果使用了强一致性的 Follower 读，为了读到的数据与 Leader 上的数据一致，会产生跨数据中心获取 `Readindex` 来校验的请求，导致整体查询的访问延迟增加。通过使用 Stale Read 功能，可以牺牲一定的实时性，就近访问对应数据所在当前中心的副本，避免跨数据中心的网络延迟，降低整体查询的访问延迟。详情参考[在三数据中心下就近读取数据](/best-practices/three-dc-local-read.md)。

## 使用方法

TiDB 提供语句级别、会话级别以及全局级别的 Stale Read 使用方式，具体使用方法如下：

- 语句级别：
    - 指定一个精确的时间点（**推荐**）：如需 TiDB 读取一个时间点上保证全局事务记录一致性的数据并且不破坏隔离级别，你可以指定这个时间点对应的时间戳。要使用该方式，请参阅 [`AS OF TIMESTAMP` 语法](/as-of-timestamp.md#语法方式)文档。
    - 指定时间范围：如需 TiDB 读取在一个时间范围内尽可能新的数据并且不破坏隔离级别，你可以指定一个时间范围。在指定时间范围内，TiDB 会选择一个合适的时间戳，该时间戳能保证所访问的副本上不存在开始于这个时间戳之前且还没有提交的相关事务，即能保证在所访问的可用副本上可执行读取操作而且不会被阻塞。要使用该方式，请参阅 [`AS OF TIMESTAMP` 语法](/as-of-timestamp.md#语法方式)文档和该文档中 [`TIDB_BOUNDED_STALENESS` 函数](/as-of-timestamp.md#语法方式)部分的介绍。
- 会话级别：
    - 指定时间范围：在会话级别中，如需 TiDB 在后续的查询中读取一个时间范围内尽可能新的数据并且不破坏隔离级别，你可以通过设置一个 session 变量 `tidb_read_staleness` 来指定一个时间范围。要使用该方式，请参阅[通过系统变量 `tidb_read_staleness` 读取历史数据](/tidb-read-staleness.md)。

除此以外，你也可以通过设置系统变量 [`tidb_external_ts`](/system-variables.md#tidb_external_ts-从-v640-版本开始引入) 和 [`tidb_enable_external_ts_read`](/system-variables.md#tidb_enable_external_ts_read-从-v640-版本开始引入) 来在某一会话或全局范围读取某一时间点前的历史数据。要使用该方式，请参阅[通过系统变量 `tidb_external_ts` 读取历史数据](/tidb-external-ts.md)。

### 减少 Stale Read 延时

Stale Read 功能会定期推进 TiDB 集群的 Resolved TS 时间戳，该时间戳能保证 TiDB 读到满足事务一致性的数据。当 Stale Read 使用的时间戳（比如 `AS OF TIMESTAMP '2016-10-08 16:45:26'`）大于 Resolved TS 时，Stale Read 会先触发 TiDB 推进 Resolved TS，等待推进完成后再读取数据，从而导致延时上升。

通过调整下面 TiKV 的配置项，你可以使 TiDB 加快 Resolved TS 推进，以减少 Stale Read 延时：

```toml
[resolved-ts]
advance-ts-interval = "20s" # 默认为 20 秒，可适当调小该值以加快 Resolved TS 推进，比如调整为 1 秒。
```

> **注意：**
>
> 调小该参数会增加 TiKV CPU 使用率和各节点之间的流量。

关于 Resolved TS 的内部原理和诊断方法，请参阅[理解 TiKV 中的 Stale Read 和 safe-ts](/troubleshoot-stale-read.md)。

## 限制

当对表的 Stale Read 查询下推到 TiFlash 时，如果该表在 Stale Read 所指定的读取时间戳之后执行过 DDL 操作，此查询将会报错。原因是 TiFlash 只支持从最新的表结构读取数据。

例如：

```sql
create table t1(id int);
alter table t1 set tiflash replica 1;
```

一分钟后进行 DDL 操作：

```sql
alter table t1 add column c1 int not null;
```

然后使用 Stale Read 读取一分钟前的数据：

```sql
set @@session.tidb_enforce_mpp=1;
select * from t1 as of timestamp NOW() - INTERVAL 1 minute;
```

此时 TiFlash 会报错：

```
ERROR 1105 (HY000): other error for mpp stream: From MPP<query:<query_ts:1673950975508472943, local_query_id:18, server_id:111947, start_ts:438816196526080000>,task_id:1>: Code: 0, e.displayText() = DB::TiFlashException: Table 323 schema version 104 newer than query schema version 100, e.what() = DB::TiFlashException,
```

把 Stale Read 指定的读取时间戳改成 DDL 操作完成之后的时间，即可避免该错误。
