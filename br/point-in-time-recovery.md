---
title: PiTR 功能介绍 
summary: 了解 PiTR 功能设计和使用。
---

# PiTR 功能介绍

> **警告：**
>
> 当前该功能为实验特性，不建议在生产环境中使用。打开该功能需要配置参数 `tikv: backup-stream.enable: true` 开启该功能。

使用 PiTR (Point-in-time recovery) 功能，你可以在新集群上恢复备份集群的历史任意时刻点的快照。TiDB 自 v6.2.0 开始支持 PiTR 功能，满足以下需求：

- 降低灾备场景下的 RPO，如实现 RPO <= 10min。
- 处理业务数据写错的案例，如回滚业务数据到出错事件前。
- 审计业务的历史数据，满足司法审查的需求。

## 在业务中使用 PiTR

[BR](/br/backup-and-restore-overview.md) 是 PiTR 功能的使用入口，通过 BR 工具，你可以完成 PiTR 的所有操作，包含数据备份（快照备份、日志备份）、一键恢复到指定时间点、备份数据管理。

下图为 PiTR 功能使用示意：

![br-arch](/media/br/pitr-usage.png)

### 备份数据

为了实现 PiTR，你需要进行以下的数据备份：

- 启动一个日志备份。运行 `br log start` 命令来启动数据库日志备份任务，该任务在 TiDB 集群后台持续地运行，及时地将 KV storage 的变更日志保存到备份存储中。
- 定期地执行[快照（全量）备份](/br/br-usage-backup.md#备份-tidb-集群快照)。运行 `br backup full` 命令来备份集群快照到备份存储，例如在每天零点进行集群快照备份。

### 一键恢复数据

当你执行 PiTR 一键恢复数据时，你需要运行 `br restore point` 命令来调用恢复程序读取快照备份和日志备份的数据，将新集群恢复到指定时间点。

### 管理备份数据

在管理备份数据时，你需要考虑如何设计备份数据的存放目录结构，和定期删除过期的（不再被需要的）备份数据。

- 推荐的备份数据目录组织方法

  - 快照备份和日志备份保存在相同的目录下，方便统一管理，例如 `backup-${cluster-id}`
  - 每个快照备份保存到命名带有备份日期的目录下，例如 `backup-${cluster-id}/snapshot-20220512000130`
  - 日志备份数据保存在一个固定目录下, 例如 `backup-${cluster-id}/log-backup`

- 清理过期的（不再被需要）的备份数据

  - 删除快照备份时，可以直接删除快照备份数据的目录
  - 使用 BR 命令 `br log truncate` 删除备份存储指定点之前的日志备份数据

## 使用限制

在使用 PiTR 功能前，需要了解下面的 PiTR 使用限制

### 功能限制

- 单个集群只支持启动一个日志备份任务
- 只支持恢复到新集群。为了避免对集群的业务请求和数据产生影响，不要在原集群（in-place）和其他已有数据集群执行 PiTR
- 不支持恢复用户表和权限表的数据
- 只支持保存数据到 S3 和分布文件系统等共享存储，暂不支持 GCS/Azure Blob Storage 做为备份存储
- 只支持集群粒度的 PiTR，不支持对单个 database/table 执行 PiTR
- 不支持恢复数据到 TiFlash storage engine。如果备份集群包含 TiFlash，执行 PiTR 后，恢复集群的数据不包含 TiFlash 副本

### 使用限制

- 不支持在（单次）恢复中重复地恢复相同时间段的日志备份

### 集群规模限制

- 目前此功能仅在 5TB 左右的数据规模上做过验证。

## 架构介绍

PiTR 功能主要包含了快照备份恢复、日志备份恢复功能。 [BR 快照备份](/br/backup-and-restore-design.md) 介绍了 BR 快照备份恢复功能。下面介绍日志备份和恢复的实现，其架构实现如下

![br-log-arch](/media/br/br-log-arch.png)

进行日志备份的时候

1. BR 收到 `br log start` 命令
2. BR 在 PD 注册日志备份任务，并在 PD 保存 log backup metadata
3. TiKV  backup executor 模块监听 PD 中日志备份任务的创建，发现任务创建后开始运行任务
4. TiKV  backup executor 模块读取 kv 数据变更，并且写入到本地 SST 文件
5. TiKV backup executor 定期将本地 SST 文件发送到备份存储中，并且更新备份存储中的 metadata

进行日志恢复的时候

1. BR 接收到 `br restore point` 命令
2. BR 读取备份存储中日志备份数据，并计算筛选出来需要恢复的日志备份数据
3. BR 请求 PD 创建用于恢复日志备份数据的 region (split regions)，将 region 调度到对应的 TiKV (scatter regions)
4. PD 调度 region 成功后，BR 将恢复数据请求发送到各个 TiKV restore executor 模块
5. TiKV restore executor从备份存储下载日志备份数据，并将其写入对应的 region

## 部署和使用 PiTR

运行 PiTR 的相关功能，BR 需要运行在（8 核+/16 GB+）的节点上, 备份和恢复 TiDB 集群配置需要能够满足 [TiDB 集群配置推荐](/hardware-and-software-requirements.md)。 

使用 BR 进行 PiTR 操作，请参考下面教程

-  [日志备份和恢复功能命令使用介绍](/br/br-log-command-line.md)
-  [PiTR 使用教程](/br/pitr-usage.md)

## 监控告警

PiTR 支持使用 [Prometheus](https://prometheus.io/) 采集监控指标（metrics），目前所有的监控指标都内置在 TiKV 中。

### 监控配置

如果是通过 TiUP 部署的集群，[Prometheus](https://prometheus.io/) 会自动采集相关的监控指标。

如果是手动部署集群，需要参考 [TiDB 集群监控部署](/deploy-monitoring-services.md)，在 Prometheus 配置文件的 scrape_configs 中加入 TiKV 相关的 job。

### 监控指标

| **指标**                                                | **类型**    | **说明**                              |
|-------------------------------------------------------|-----------|-------------------------------------|
| **tikv_log_backup_interal_actor_acting_duration_sec** | Histogram |                                     |
| **tikv_log_backup_initial_scan_reason**               | Counter   |                                     |
| **tikv_stream_event_handle_duration_sec**             | Histogram |                                     |
| **tikv_stream_handle_kv_batch**                       | Histogram |                                     |
| **tikv_log_backup_initial_scan_disk_read**            | Counter   |                                     |
| **tikv_stream_incremental_scan_bytes**                | Histogram |                                     |
| **tikv_stream_skip_kv_count**                         | Counter   |                                     |
| **tikv_stream_errors**                                | Counter   |                                     |
| **tikv_log_backup_fatal_errors**                      | Counter   |                                     |
| **tikv_stream_heap_memory**                           | Gauge     |                                     |
| **tikv_stream_on_event_duration_seconds**             | Histogram |                                     |
| **tikv_stream_store_checkpoint_ts**                   | Gauge     |                                     |
| **tikv_stream_flush_duration_sec**                    | Histogram |                                     |
| **tikv_stream_flush_file_size**                       | Histogram |                                     |
| **tikv_stream_initial_scan_duration_sec**             | Histogram |                                     |
| **tikv_stream_skip_retry_observe**                    | Counter   |                                     |
| **tikv_stream_initial_scan_operations**               | Counter   |                                     |
| **tikv_stream_enabled**                               | Counter   | 日志备份功能是否开启，若值大于 0，表示开启              |
| **tikv_stream_observed_region**                       | Gauge     | 被监听的 region 数量                      |
| **tikv_log_backup_task_status**                       | Gauge     | 日志备份任务状态，0-Running 1-Paused 2-Error |
| **tikv_pending_initial_scan**                         | Gauge     |                                     |

### Grafana 配置

如果是通过 TiUP 部署的集群，[Grafana](https://grafana.com/) 中已经内置了 PiTR 的面板。TiKV-Details dashboard 中的 Backup Log 面板即为 PiTR 的面板。

如果是手动部署集群，需要参考[导入 Grafana 面板](/deploy-monitoring-services.md#第-2-步导入-grafana-面板)，将 [tikv_details](https://github.com/tikv/tikv/blob/master/metrics/grafana/tikv_details.json) JSON 文件上传到 Grafana 中。之后在 TiKV-Details dashboard 中找到 Backup Log 面板即可。

### 告警配置

目前 PiTR 还未内置告警项，以下告警项为推荐的配置。

#### LogBackupRunningRPOMoreThan10m

- **表达式：** max(time() - tikv_stream_store_checkpoint_ts / 262144000) by (task) / 60 > 10
and max(tikv_stream_store_checkpoint_ts) by (task) > 0
and max(tikv_log_backup_task_status) by (task) == 0
- **告警级别：** warning
- **说明：** 日志数据超过 10 分钟未持久化到存储中，这里主要是提醒，大部分情况下日志备份还会正常推进

#### LogBackupRunningRPOMoreThan30m

- **表达式：** max(time() - tikv_stream_store_checkpoint_ts / 262144000) by (task) / 60 > 30
  and max(tikv_stream_store_checkpoint_ts) by (task) > 0
  and max(tikv_log_backup_task_status) by (task) == 0
- **告警级别：** critical
- **说明：** 日志数据超过 30 分钟未持久化到存储中，此时极可能出现异常，可以查看 TiKV 日志定位原因

#### LogBackupPausingMoreThan2h

- **表达式：** max(time() - tikv_stream_store_checkpoint_ts / 262144000) by (task) / 3600 > 2
  and max(tikv_stream_store_checkpoint_ts) by (task) > 0
  and max(tikv_log_backup_task_status) by (task) == 1
- **告警级别：** warning
- **说明：** 日志备份任务处于暂停状态超过 2 小时，这里主要是提醒，建议尽早执行 `br log resume` 恢复任务

#### LogBackupPausingMoreThan12h

- **表达式：** max(time() - tikv_stream_store_checkpoint_ts / 262144000) by (task) / 3600 > 12
  and max(tikv_stream_store_checkpoint_ts) by (task) > 0
  and max(tikv_log_backup_task_status) by (task) == 1
- **告警级别：** critical
- **说明：** 日志备份任务处于暂停状态超过 12 小时，应尽快执行 `br log resume` 恢复任务。任务处于暂停状态时间过长会有数据丢失的风险

#### LogBackupFailed

- **表达式：** max(tikv_log_backup_task_status) by (task) == 2
  and max(tikv_stream_store_checkpoint_ts) by (task) > 0
- **告警级别：** critical
- **说明：** 日志备份任务进入失败状态，需要执行 `br log status` 查看失败原因，如有必要还需进一步查看 TiKV 日志

#### LogBackupGCSafePointExceedsCheckpoint

- **表达式：** min(tikv_stream_store_checkpoint_ts) by (instance) - max(tikv_gcworker_autogc_safe_point) by (instance) < 0
- **告警级别：** critical
- **说明：** 部分数据未被备份就已经被 GC，此时已有部分数据丢失，极有可能对业务产生影响
