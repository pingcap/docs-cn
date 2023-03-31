---
title: TiDB Data Migration 处理告警
summary: 了解 DM 中各主要告警信息的处理方法。
aliases: ['/docs-cn/tidb-data-migration/dev/handle-alerts/']
---

# TiDB Data Migration 处理告警

本文档介绍如何处理 TiDB Data Migration (DM) 中的告警。

## 高可用告警

### `DM_master_all_down`

当全部 DM-master 离线时触发该告警。发生该错误时，需要检查集群环境，并通过各节点日志排查错误。

### `DM_worker_offline`

存在离线的 DM-worker 超过一小时会触发该告警。在高可用架构下，该告警可能不会直接中断任务，但是会提升任务中断的风险。处理告警可以查看对应 DM-worker 节点的工作状态，检查是否连通，并通过日志排查错误。

### `DM_DDL_error`

处理 shard DDL 时出现错误，此时需要参考 [DM 故障诊断](/dm/dm-error-handling.md#dm-故障诊断)进行处理。

### `DM_pending_DDL`

存在未完成的 shard DDL 并超过一小时会触发该告警。在某些应用场景下，存在未完成的 shard DDL 可能是用户所期望的。在用户预期以外的场景下，可以通过[手动处理 Sharding DDL Lock](/dm/manually-handling-sharding-ddl-locks.md)解决。

## 任务状态告警

### `DM_task_state`

当 DM-worker 内有子任务处于 `Paused` 状态超过 20 分钟时会触发该告警，此时需要参考 [DM 故障诊断](/dm/dm-error-handling.md#dm-故障诊断)进行处理。

## relay log 告警

### `DM_relay_process_exits_with_error`

当 relay log 处理单元遇到无法自动恢复的错误时（如找不到 binlog 文件），或者短时间内多次遇到（如 2 分钟内遇到 3 次以上）可自动恢复的错误时（如网络问题），会触发该告警，此时需要参考 [DM 故障诊断](/dm/dm-error-handling.md#dm-故障诊断)进行处理。

### `DM_remain_storage_of_relay_log`

当 relay log 所在磁盘的剩余可用容量小于 10G 时会触发该告警，对应的处理方法包括：

- 手动清理该磁盘上其他无用数据以增加可用容量。
- 尝试调整 relay log 的[自动清理策略](/dm/relay-log.md#自动数据清理)或执行[手动清理](/dm/relay-log.md#手动数据清理)。
- 使用 `pause-relay` 命令暂停 relay log 的拉取，并在磁盘空间合适之后使用 `resume-relay` 命令恢复。需要注意上游数据源不要清理尚未拉取的 binlog。

### `DM_relay_log_data_corruption`

当 relay log 处理单元在校验从上游读取到的 binlog event 且发现 checksum 信息异常时会转为 `Paused` 状态并立即触发告警，此时需要参考 [DM 故障诊断](/dm/dm-error-handling.md#dm-故障诊断)进行处理。

### `DM_fail_to_read_binlog_from_master`

当 relay log 处理单元在尝试从上游读取 binlog event 发生错误时，会转为 `Paused` 状态并立即触发该告警，此时需要参考 [DM 故障诊断](/dm/dm-error-handling.md#dm-故障诊断)进行处理。

### `DM_fail_to_write_relay_log`

当 relay log 处理单元在尝试将 binlog event 写入 relay log 文件发生错误时，会转为 `Paused` 状态并立即触发该告警，此时需要参考 [DM 故障诊断](/dm/dm-error-handling.md#dm-故障诊断)进行处理。

### `DM_binlog_file_gap_between_master_relay`

当 relay log 处理单元已拉取到的最新的 binlog 文件个数落后于当前上游 MySQL/MariaDB 超过 1 个（不含 1 个）且持续 10 分钟时会触发该告警，此时需要参考[性能问题及处理方法](/dm/dm-handle-performance-issues.md)对 relay log 处理单元相关的性能问题进行排查与处理。

## Dump/Load 告警

### `DM_dump_process_exists_with_error`

当 Dump 处理单元遇到无法自动恢复的错误时（如找不到 binlog 文件），或者短时间内多次遇到（如 2 分钟内遇到 3 次以上）可自动恢复的错误时（如网络问题），会触发该告警，此时需要参考 [DM 故障诊断](/dm/dm-error-handling.md#dm-故障诊断)进行处理。

### `DM_load_process_exists_with_error`

当 Load 处理单元遇到无法自动恢复的错误时（如找不到 binlog 文件），或者短时间内多次遇到（如 2 分钟内遇到 3 次以上）可自动恢复的错误时（如网络问题），会触发该告警，此时需要参考 [DM 故障诊断](/dm/dm-error-handling.md#dm-故障诊断)进行处理。

## Binlog replication 告警

### `DM_sync_process_exists_with_error`

当 Binlog replication 处理单元遇到无法自动恢复的错误时（如找不到 binlog 文件），或者短时间内多次遇到（如 2 分钟内遇到 3 次以上）可自动恢复的错误时（如网络问题），会触发该告警，此时需要参考 [DM 故障诊断](/dm/dm-error-handling.md#dm-故障诊断)进行处理。

### `DM_binlog_file_gap_between_master_syncer`

当 Binlog replication 处理单元已处理到的最新的 binlog 文件个数落后于当前上游 MySQL/MariaDB 超过 1 个（不含 1 个）且持续 10 分钟时 DM 会触发该告警，此时需要参考[性能问题及处理方法](/dm/dm-handle-performance-issues.md)对 Binlog replication 处理单元相关的性能问题进行排查与处理。

### `DM_binlog_file_gap_between_relay_syncer`

当 Binlog replication 处理单元已处理到的最新的 binlog 文件个数落后于当前 relay log 处理单元超过 1 个（不含 1 个）且持续 10 分钟时 DM 会触发该告警，此时需要参考[性能问题及处理方法](/dm/dm-handle-performance-issues.md)对 Binlog replication 处理单元相关的性能问题进行排查与处理。
