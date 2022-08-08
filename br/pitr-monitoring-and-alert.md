---
title: PiTR 监控告警
summary: PiTR 监控告警介绍。
---

# PiTR 监控告警

PiTR 支持使用 [Prometheus](https://prometheus.io/) 采集监控指标，目前所有的监控指标都内置在 TiKV 中。

## 监控配置

- 通过 TiUP 部署的集群，[Prometheus](https://prometheus.io/) 会自动采集相关的监控指标。

- 手动部署的集群，需要参考 [TiDB 集群监控部署](/deploy-monitoring-services.md)，在 Prometheus 配置文件的 `scrape_configs` 中加入 TiKV 相关的 job。

## 监控指标

| 指标                                                | 类型    | 说明                                                                                                                                                 |
|-------------------------------------------------------|-----------|---------------------------------------------------------------------------------------------------------------------------------------------------------|
| **tikv_log_backup_interal_actor_acting_duration_sec** | Histogram | 处理内部各种消息事件的耗时。<br/>`message :: TaskType`                                                                                                            |
| **tikv_log_backup_initial_scan_reason**               | Counter   | 触发增量扫的原因统计。主要是 Leader 迁移或者 Region Version 变更。<br/> `reason :: {"leader-changed", "region-changed", "retry"}`                                           |
| **tikv_log_backup_event_handle_duration_sec**         | Histogram | 处理 KV Event 的耗时。和 `tikv_log_backup_on_event_duration_seconds` 相比，这个指标还包含了一些内部转化消耗的时间。  <br/>`stage :: {"to_stream_event", "save_to_temp_file"}` |
| **tikv_log_backup_handle_kv_batch**                   | Histogram | 由 RaftStore 发送的 KV 对的 Batch 大小统计，统计数据为 Region 级别。                                                                                                     |
| **tikv_log_backup_initial_scan_disk_read**            | Counter   | 增量扫期间，从硬盘读取的数据量的大小。在 Linux 系统下，这个信息来自于 procfs，是实际从 block device 读取的数据量的大小；配置项 `initial-scan-rate-limit` 也是施加于这个数值上。                                     |
| **tikv_log_backup_incremental_scan_bytes**            | Histogram | 增量扫期间，实际产生的 KV 对的大小。因为压缩和读放大的缘故，这个数值和 `tikv_log_backup_initial_scan_disk_read` 不一定相同。                                                                   |
| **tikv_log_backup_skip_kv_count**                     | Counter   | 日志备份期间，因为对备份没有帮助而被跳过的 Raft Event 数量。                                                                                                                    |
| **tikv_log_backup_errors**                            | Counter   | 日志备份期间，遇到的可以重试或可以忽略的错误。 <br/>`type :: ErrorType`                                                                                                       |
| **tikv_log_backup_fatal_errors**                      | Counter   | 日志备份期间，遇到的不可重试或不可忽略的错误。当该类错误出现的时候，日志备份任务会被暂停。 <br/>`type :: ErrorType`                                                                                   |
| **tikv_log_backup_heap_memory**                       | Gauge     | 日志备份期间，增量扫发现的、尚未被消费的事件占用的内存。                                                                                                                           |
| **tikv_log_backup_on_event_duration_seconds**         | Histogram | 将 KV Event 保存到临时文件各个阶段的耗时。 <br/>`stage :: {"write_to_tempfile", "syscall_write"}`                                                                        |
| **tikv_log_backup_store_checkpoint_ts**               | Gauge     | Store 级别的 Checkpoint TS，已经弃用。其含义更加接近于 Store 当前注册的 GC Safepoint. <br/>`task :: string`                                                                    |
| **tikv_log_backup_flush_duration_sec**                | Histogram | 将本地临时文件移动到外部存储的耗时。<br/>`stage :: {"generate_metadata", "save_files", "clear_temp_files"}`                                                                |
| **tikv_log_backup_flush_file_size**                   | Histogram | 备份产生的文件的大小统计。                                                                                                                                           |
| **tikv_log_backup_initial_scan_duration_sec**         | Histogram | 增量扫的整体耗时统计。                                                                                                                                             |
| **tikv_log_backup_skip_retry_observe**                | Counter   | 在日志备份过程中，遇到的可忽略错误的统计，即放弃 retry 的原因。 <br/>`reason :: {"region-absent", "not-leader", "stale-command"}`                                                   |
| **tikv_log_backup_initial_scan_operations**           | Counter   | 增量扫过程中， RocksDB 相关的操作统计。<br/>`cf :: {"default", "write", "lock"}, op :: RocksDBOP`                                                                       |
| **tikv_log_backup_enabled**                           | Counter   | 日志备份功能是否开启，若值大于 0，表示开启                                                                                                                                  |
| **tikv_log_backup_observed_region**                   | Gauge     | 被监听的 region 数量                                                                                                                                          |
| **tikv_log_backup_task_status**                       | Gauge     | 日志备份任务状态，0-Running 1-Paused 2-Error <br/>`task :: string`                                                                                                |
| **tikv_log_backup_pending_initial_scan**              | Gauge     | 尚未执行的增量扫的统计。<br/>`stage :: {"queuing", "executing"}`                                                                                                     |

## Grafana 配置

- 通过 TiUP 部署的集群，[Grafana](https://grafana.com/) 中内置了 PiTR 的面板。TiKV-Details dashboard 中的 Backup Log 面板即为 PiTR 面板。

- 手动部署的集群，需要参考[导入 Grafana 面板](/deploy-monitoring-services.md#第-2-步导入-grafana-面板)，将 [tikv_details](https://github.com/tikv/tikv/blob/master/metrics/grafana/tikv_details.json) JSON 文件上传到 Grafana 中。之后在 TiKV-Details dashboard 中找到 Backup Log 面板即可。

## 告警配置

目前 PiTR 还未内置告警项，以下告警项为推荐的配置。

### LogBackupRunningRPOMoreThan10m

- 表达式：max(time() - tikv_stream_store_checkpoint_ts / 262144000) by (task) / 60 > 10 and max(tikv_stream_store_checkpoint_ts) by (task) > 0 and max(tikv_log_backup_task_status) by (task) == 0
- 告警级别：warning
- 说明：日志数据超过 10 分钟未持久化到存储中，该配置项主要用于提醒，大部分情况下，不会影响日志备份

### LogBackupRunningRPOMoreThan30m

- 表达式：max(time() - tikv_stream_store_checkpoint_ts / 262144000) by (task) / 60 > 30 and max(tikv_stream_store_checkpoint_ts) by (task) > 0 and max(tikv_log_backup_task_status) by (task) == 0
- 告警级别：critical
- 说明：日志数据超过 30 分钟未持久化到存储中，出现该告警表示极有可能出现异常，可以查看 TiKV 日志定位原因

### LogBackupPausingMoreThan2h

- 表达式：max(time() - tikv_stream_store_checkpoint_ts / 262144000) by (task) / 3600 > 2 and max(tikv_stream_store_checkpoint_ts) by (task) > 0 and max(tikv_log_backup_task_status) by (task) == 1
- 告警级别：warning
- 说明：日志备份任务处于暂停状态超过 2 小时，该告警主要用于提醒，建议尽早执行 `br log resume` 恢复任务

### LogBackupPausingMoreThan12h

- 表达式：max(time() - tikv_stream_store_checkpoint_ts / 262144000) by (task) / 3600 > 12 and max(tikv_stream_store_checkpoint_ts) by (task) > 0 and max(tikv_log_backup_task_status) by (task) == 1
- 告警级别：critical
- 说明：日志备份任务处于暂停状态超过 12 小时，应尽快执行 `br log resume` 恢复任务。任务处于暂停状态时间过长会有数据丢失的风险

### LogBackupFailed

- 表达式：max(tikv_log_backup_task_status) by (task) == 2 and max(tikv_stream_store_checkpoint_ts) by (task) > 0
- 告警级别：critical
- 说明：日志备份任务进入失败状态，需要执行 `br log status` 查看失败原因，如有必要还需进一步查看 TiKV 日志

### LogBackupGCSafePointExceedsCheckpoint

- 表达式：min(tikv_stream_store_checkpoint_ts) by (instance) - max(tikv_gcworker_autogc_safe_point) by (instance) < 0
- 告警级别：critical
- 说明：部分数据在备份前被 GC，此时已有部分数据丢失，极有可能对业务产生影响
