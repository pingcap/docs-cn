---
title: TiDB Workload Repository
summary: 介绍用于收集和存储 TiDB 集群历史工作负载数据的 Workload Repository 系统。
---

# TiDB Workload Repository

Workload Repository 是一个用于收集和存储 TiDB 集群历史工作负载数据的系统。它会定期采样各种系统表，以跟踪集群的性能和使用模式。

## 启用 Workload Repository 

要启用 Workload Repository，可以设置 [`tidb_workload_repository_dest`](/system-variables.md#tidb_workload_repository_dest-从-v900-版本开始引入) 系统变量：

```sql
SET GLOBAL tidb_workload_repository_dest = 'table';
```

要禁用它，执行以下语句：

```sql
SET GLOBAL tidb_workload_repository_dest = '';
```

## 数据收集

Workload Repository 将数据存储在 `WORKLOAD_SCHEMA` 数据库下的表中。它通过两种不同的方法收集数据：

- 快照采样过程，按可配置的时间间隔运行，默认为每小时一次，也可以手动触发。
- 基于时间的采样过程，按较短的时间间隔运行，通常为每 5 秒一次。

## 快照采样过程（默认每小时）

快照采样过程每 15 分钟到 2 小时运行一次（默认每小时），从存储累计指标的内存表中采样数据。快照由指定时间间隔内的某个 TiDB 节点发起，过程如下：

1. 从发起节点向 `WORKLOAD_SCHEMA.HIST_SNAPSHOTS` 表插入一行，记录快照 ID、开始和结束时间戳以及服务器版本信息。
2. 在每个 TiDB 节点上，将源表中的所有行复制到带有 `HIST_` 前缀的对应目标表中。复制的数据包括源表中的原始列以及用于记录时间戳、实例 ID 和快照 ID 的附加列。

注意，采样表返回的数据内容与查询这些数据的 TiDB 节点相关。

从以下表中采样数据：

| 源表 | 目标表 | 描述 |
| --- | --- | --- |
| [`TIDB_INDEX_USAGE`](/information-schema/information-schema-tidb-index-usage.md) | `HIST_TIDB_INDEX_USAGE` | 索引使用统计信息 |
| [`TIDB_STATEMENTS_STATS`](/statement-summary-tables.md) | `HIST_TIDB_STATEMENTS_STATS` | 语句统计信息 |
| [`CLIENT_ERRORS_SUMMARY_BY_HOST`](/information-schema/client-errors-summary-by-host.md) | `HIST_CLIENT_ERRORS_SUMMARY_BY_HOST` | 基于主机客户端的错误摘要 |
| [`CLIENT_ERRORS_SUMMARY_BY_USER`](/information-schema/client-errors-summary-by-user.md) | `HIST_CLIENT_ERRORS_SUMMARY_BY_USER` | 基于用户客户端的错误摘要 |
| [`CLIENT_ERRORS_SUMMARY_GLOBAL`](/information-schema/client-errors-summary-global.md) | `HIST_CLIENT_ERRORS_SUMMARY_GLOBAL` | 基于全局客户端的错误摘要 |

可以通过 [`tidb_workload_repository_snapshot_interval`](/system-variables.md#tidb_workload_repository_snapshot_interval-从-v900-版本开始引入) 控制快照采样间隔：

```sql
SET GLOBAL tidb_workload_repository_snapshot_interval = 900; -- 将间隔设置为 15 分钟
```

## 手动快照

请注意，虽然快照采样过程会根据配置的时间间隔自动运行，但你也可以使用以下 SQL 语句触发手动快照：

```sql
ADMIN CREATE WORKLOAD SNAPSHOT;
```

手动快照并不会改变下一次自动快照的发生时间。

## 基于时间的采样过程（默认每 5 秒）

基于时间的采样间隔可设置为 1 秒到 600 秒之间的任意时间，从各个记录瞬时状态的系统表中采样数据。

当基于时间的采样过程运行时，源表中的所有行都会被复制到带有 `HIST_` 前缀的对应目标表中。复制的数据包括源表中的原始列以及用于记录时间戳和实例 ID 的附加列。

与快照采样过程不同，不会向 `HIST_SNAPSHOTS` 表添加行。

注意，采样表返回的数据内容与查询这些数据的 TiDB 节点相关。

从以下表中采样数据：

| 源表 | 目标表 | 描述 |
| --- | --- | --- |
| [`PROCESSLIST`](/information-schema/information-schema-processlist.md) | `HIST_PROCESSLIST` | 活跃会话 |
| [`DATA_LOCK_WAITS`](/information-schema/information-schema-data-lock-waits.md) | `HIST_DATA_LOCK_WAITS` | 数据锁等待 |
| [`TIDB_TRX`](/information-schema/information-schema-tidb-trx.md) | `HIST_TIDB_TRX` | 活跃事务 |
| [`MEMORY_USAGE`](/information-schema/information-schema-memory-usage.md) | `HIST_MEMORY_USAGE` | 内存使用情况 |
| [`DEADLOCKS`](/information-schema/information-schema-deadlocks.md) | `HIST_DEADLOCKS` | 死锁信息 |

可以通过 [`tidb_workload_repository_active_sampling_interval`](/system-variables.md#tidb_workload_repository_active_sampling_interval-从-v900-版本开始引入) 控制基于时间的采样间隔：

```sql
SET GLOBAL tidb_workload_repository_active_sampling_interval = 20; -- 将间隔设置为 20 秒
```

把间隔设置为 `0` 将会禁用基于时间的采样。

## 数据保留

系统会根据保留期设置自动清除数据，并使用分区进行高效的数据管理。

默认情况下，Workload Repository 会保留 7 天的历史数据，但你可以通过 [`tidb_workload_repository_retention_days`](/system-variables.md#tidb_workload_repository_retention_days-从-v900-版本开始引入) 变量来控制保留期的长度。例如，要保留 30 天的数据，可以运行以下语句：

```sql
SET GLOBAL tidb_workload_repository_retention_days = 30;
```

此变量的值越高，数据保留时间越长，这可能有助于工作负载分析，但会增加存储需求。

## 注意事项

- 启用 Workload Repository 可能会对系统性能产生轻微影响。
- 采样间隔设置得过短可能会增加系统开销。
- 将保留天数设置为 `0` 会禁用旧数据的自动清除。

## 最佳实践

- 从默认设置开始，根据你的监控需求进行调整。
- 根据存储容量设置合理的保留期。
- 监控 `WORKLOAD_SCHEMA` 数据库的大小。
- 在生产环境中使用较长的采样间隔以最小化开销。
