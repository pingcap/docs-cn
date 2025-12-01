---
title: 备份恢复监控告警
summary: 了解备份恢复的监控告警。
---

# 备份恢复监控告警

本文介绍备份恢复的监控和告警，包括如何部署监控、监控指标及常用告警项。

## 日志备份监控

日志备份支持功能使用 [Prometheus](https://prometheus.io/) 采集监控指标，目前所有的监控指标都内置在 TiKV 中。

### 部署监控

- 通过 TiUP 部署的集群，Prometheus 会自动采集相关的监控指标。

- 手动部署的集群，需要参考 [TiDB 集群监控部署](/deploy-monitoring-services.md)，在 Prometheus 配置文件的 `scrape_configs` 中加入 TiKV 相关的 job。

### 配置 Grafana

- 通过 TiUP 部署的集群，[Grafana](https://grafana.com/) 中内置了 Backup log 的面板。

- 手动部署的集群，需要参考[导入 Grafana 面板](/deploy-monitoring-services.md#第-2-步导入-grafana-面板)，将 [tikv_details.json](https://github.com/tikv/tikv/blob/release-8.5/metrics/grafana/tikv_details.json) 文件上传到 Grafana 中。之后在 TiKV-Details Dashboard 中找到 Backup Log 面板即可。

### 监控指标

| 指标                                                    | 类型        | 说明                                                                                                                                              |
|-------------------------------------------------------|-----------|-------------------------------------------------------------------------------------------------------------------------------------------------|
| **tikv_log_backup_internal_actor_acting_duration_sec** | Histogram | 处理内部各种消息事件的耗时。<br/>`message :: TaskType`                                                                                                        |
| **tikv_log_backup_initial_scan_reason**               | Counter   | 触发增量扫的原因统计。主要是 Leader 迁移或者 Region Version 变更。<br/> `reason :: {"leader-changed", "region-changed", "retry"}`                                    |
| **tikv_log_backup_event_handle_duration_sec**         | Histogram | 处理 KV Event 的耗时。和 `tikv_log_backup_on_event_duration_seconds` 相比，这个指标还包含了一些内部转化消耗的时间。  <br/>`stage :: {"to_stream_event", "save_to_temp_file"}` |
| **tikv_log_backup_handle_kv_batch**                   | Histogram | 由 RaftStore 发送的 KV 对的 Batch 大小统计，统计数据为 Region 级别。                                                                                               |
| **tikv_log_backup_initial_scan_disk_read**            | Counter   | 增量扫期间，从硬盘读取的数据量的大小。在 Linux 系统下，这个信息来自于 procfs，是实际从 block device 读取的数据量的大小；配置项 `initial-scan-rate-limit` 也是施加于这个数值上。                             |
| **tikv_log_backup_incremental_scan_bytes**            | Histogram | 增量扫期间，实际产生的 KV 对的大小。因为压缩和读放大的缘故，这个数值和 `tikv_log_backup_initial_scan_disk_read` 不一定相同。                                                           |
| **tikv_log_backup_skip_kv_count**                     | Counter   | 日志备份期间，因为对备份没有帮助而被跳过的 Raft Event 数量。                                                                                                            |
| **tikv_log_backup_errors**                            | Counter   | 日志备份期间，遇到的可以重试或可以忽略的错误。 <br/>`type :: ErrorType`                                                                                                |
| **tikv_log_backup_fatal_errors**                      | Counter   | 日志备份期间，遇到的不可重试或不可忽略的错误。当该类错误出现的时候，日志备份任务会被暂停。 <br/>`type :: ErrorType`                                                                          |
| **tikv_log_backup_heap_memory**                       | Gauge     | 日志备份期间，增量扫发现的、尚未被消费的事件占用的内存。                                                                                                                    |
| **tikv_log_backup_on_event_duration_seconds**         | Histogram | 将 KV Event 保存到临时文件各个阶段的耗时。 <br/>`stage :: {"write_to_tempfile", "syscall_write"}`                                                               |
| **tikv_log_backup_store_checkpoint_ts**               | Gauge     | Store 级别的 Checkpoint TS，已经弃用。其含义更加接近于 Store 当前注册的 GC Safepoint。 <br/>`task :: string`                                                           |
| **tidb_log_backup_last_checkpoint**                   | Gauge     | 全局 Checkpoint TS，表示日志备份功能中已经备份的时间点。 <br/>`task :: string`                                                                                    |
| **tikv_log_backup_flush_duration_sec**                | Histogram | 将本地临时文件移动到外部存储的耗时。<br/>`stage :: {"generate_metadata", "save_files", "clear_temp_files"}`                                                       |
| **tikv_log_backup_flush_file_size**                   | Histogram | 备份产生的文件的大小统计。                                                                                                                                   |
| **tikv_log_backup_initial_scan_duration_sec**         | Histogram | 增量扫的整体耗时统计。                                                                                                                                     |
| **tikv_log_backup_skip_retry_observe**                | Counter   | 在日志备份过程中，遇到的可忽略错误的统计，即放弃 retry 的原因。 <br/>`reason :: {"region-absent", "not-leader", "stale-command"}`                                           |
| **tikv_log_backup_initial_scan_operations**           | Counter   | 增量扫过程中，RocksDB 相关的操作统计。<br/>`cf :: {"default", "write", "lock"}, op :: RocksDBOP`                                                              |
| **tikv_log_backup_enabled**                           | Counter   | 日志备份功能是否开启，若值大于 0，表示开启                                                                                                                          |
| **tikv_log_backup_observed_region**                   | Gauge     | 被监听的 Region 数量                                                                                                                                  |
| **tikv_log_backup_task_status**                       | Gauge     | 日志备份任务状态，0-Running 1-Paused 2-Error <br/>`task :: string`                                                                                       |
| **tikv_log_backup_pending_initial_scan**              | Gauge     | 尚未执行的增量扫的统计。<br/>`stage :: {"queuing", "executing"}`                                                                                            |

### 日志备份告警

#### 配置告警

目前 Point-in-time recovery (PITR) 还未内置告警项，本节介绍如何在 PITR 中配置告警项，以及推荐的告警项规则。

告警规则配置可以参考下面的步骤：

1. 在 Prometheus 所在节点上创建告警规则的配置文件（例如 `pitr.rules.yml`），参考 [Prometheus 文档](https://prometheus.io/docs/prometheus/latest/configuration/alerting_rules/)和下列推荐的告警项及配置样例填写告警规则。
2. 在 Prometheus 配置文件中的 `rule_files` 字段填入告警规则文件的路径。
3. 通过向 Prometheus 进程发送 `SIGHUP` 信号（`kill -HUP pid`）或向 `http://prometheus-addr/-/reload` 发送 HTTP `POST` 请求（使用 HTTP 请求方式前需要在启动 Prometheus 时指定 `--web.enable-lifecycle` 参数）。

以下为推荐的告警项配置：

#### LogBackupRunningRPOMoreThan10m

- 表达式：`max(time() - tidb_log_backup_last_checkpoint / 262144000) by (task) / 60 > 10 and max(tidb_log_backup_last_checkpoint) by (task) > 0 and max(tikv_log_backup_task_status) by (task) == 0`
- 告警级别：warning
- 说明：日志数据超过 10 分钟未持久化到存储中，该配置项主要用于提醒，大部分情况下，不会影响日志备份。

Prometheus 中的配置样例如下：

```yaml
groups:
- name: PiTR
  rules:
  - alert: LogBackupRunningRPOMoreThan10m
    expr: max(time() - tidb_log_backup_last_checkpoint / 262144000) by (task) / 60 > 10 and max(tidb_log_backup_last_checkpoint) by (task) > 0 and max(tikv_log_backup_task_status) by (task) == 0
    labels:
      severity: warning
    annotations:
      summary: RPO of log backup is high
      message: RPO of the log backup task {{ $labels.task }} is more than 10m
```

#### LogBackupRunningRPOMoreThan30m

- 表达式：`max(time() - tidb_log_backup_last_checkpoint / 262144000) by (task) / 60 > 30 and max(tidb_log_backup_last_checkpoint) by (task) > 0 and max(tikv_log_backup_task_status) by (task) == 0`
- 告警级别：critical
- 说明：日志数据超过 30 分钟未持久化到存储中，出现该告警表示极有可能出现异常，可以查看 TiKV 日志定位原因。

#### LogBackupPausingMoreThan2h

- 表达式：`max(time() - tidb_log_backup_last_checkpoint / 262144000) by (task) / 3600 > 2 and max(tidb_log_backup_last_checkpoint) by (task) > 0 and max(tikv_log_backup_task_status) by (task) == 1`
- 告警级别：warning
- 说明：日志备份任务处于暂停状态超过 2 小时，该告警主要用于提醒，建议尽早执行 `br log resume` 恢复任务。

#### LogBackupPausingMoreThan12h

- 表达式：`max(time() - tidb_log_backup_last_checkpoint / 262144000) by (task) / 3600 > 12 and max(tidb_log_backup_last_checkpoint) by (task) > 0 and max(tikv_log_backup_task_status) by (task) == 1`
- 告警级别：critical
- 说明：日志备份任务处于暂停状态超过 12 小时，应尽快执行 `br log resume` 恢复任务。任务处于暂停状态时间过长会有数据丢失的风险。

#### LogBackupFailed

- 表达式：`max(tikv_log_backup_task_status) by (task) == 2 and max(tidb_log_backup_last_checkpoint) by (task) > 0`
- 告警级别：critical
- 说明：日志备份任务进入失败状态，需要执行 `br log status` 查看失败原因，如有必要还需进一步查看 TiKV 日志。

#### LogBackupGCSafePointExceedsCheckpoint

- 表达式：`min(tidb_log_backup_last_checkpoint) by (instance) - max(tikv_gcworker_autogc_safe_point) by (instance) < 0`
- 告警级别：critical
- 说明：部分数据在备份前被 GC，此时已有部分数据丢失，极有可能对业务产生影响。
