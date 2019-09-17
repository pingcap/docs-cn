---
title: DM 监控指标
summary: 介绍 DM 的监控指标
category: reference
---

# DM 监控指标

使用 DM-Ansible 部署 DM 集群的时候，会默认部署一套[监控系统](./deploy.md#第-7-步监控任务与查看日志)。

> **注意：**
>
> 目前只有 DM-worker 提供了 metrics，DM-master 暂未提供。

## Task

在 Grafana dashboard 中，DM 默认名称为 `DM-task`。

### overview

overview 下包含运行当前选定 task 的所有 DM-worker instance 的部分监控指标。当前默认告警规则只针对于单个 DM-worker instance。

| metric 名称 | 说明 | 告警说明 | 告警级别 |
|:----|:------------|:----|:----|
| task state | 同步子任务的状态 | N/A | N/A |
| storage capacity | relay log 占有的磁盘的总容量  | N/A | N/A |
| storage remain | relay log 占有的磁盘的剩余可用容量  | N/A | N/A |
| binlog file gap between master and relay | relay 与上游 master 相比落后的 binlog file 个数 | N/A | N/A |
| load progress | load unit 导入过程的进度百分比，值变化范围为：0% - 100%  | N/A | N/A |
| binlog file gap between master and syncer | 与上游 master 相比 binlog replication 落后的 binlog file 个数 | N/A | N/A |
| shard lock resolving | 当前子任务是否正在等待 shard DDL 同步，大于 0 表示正在等待同步 | N/A | N/A |

### task 状态

| metric 名称 | 说明 | 告警说明 | 告警级别 |
|:----|:------------|:----|:----|
| task state | 同步子任务的状态 | 当子任务状态处于 paused 超过 10 分钟时| critical |

### Relay log

| metric 名称 | 说明 | 告警说明 | 告警级别 |
|:----|:------------|:----|:----|
| storage capacity | relay log 占有的磁盘的总容量  | N/A | N/A |
| storage remain | relay log 占有的磁盘的剩余可用容量  | 小于 10G 的时候需要告警 | critical |
| process exits with error | relay log 在 DM-worker 内部遇到错误并且退出了  | 立即告警 | critical |
| relay log data corruption | relay log 文件损坏的个数 | 立即告警 | emergency |
| fail to read binlog from master | relay 从上游的 MySQL 读取 binlog 时遇到的错误数 | 立即告警 | critical |
| fail to write relay log | relay 写 binlog 到磁盘时遇到的错误数 | 立即告警 | critical |
| binlog file index | relay log 最大的文件序列号。如 value = 1 表示 relay-log.000001 | N/A | N/A |
| binlog file gap between master and relay | relay 与上游 master 相比落后的 binlog file 个数 | 落后 binlog file 个数超过 1 个（不含 1 个）且持续 10 分钟时 | critical |
| binlog pos | relay log 最新文件的写入 offset  | N/A | N/A |
| read binlog duration | relay log 从上游的 MySQL 读取 binlog 的时延，单位：秒 |  N/A | N/A |
| write relay log duration | relay log 每次写 binlog 到磁盘的时延，单位：秒| N/A | N/A |
| binlog size | relay log 写到磁盘的单条 binlog 的大小 | N/A | N/A |

### Dump/Load unit

下面 metrics 仅在 `task-mode` 为 `full` 或者 `all` 模式下会有值。

| metric 名称 | 说明 | 告警说明 | 告警级别 |
|:----|:------------|:----|:----|
| load progress | load unit 导入过程的进度百分比，值变化范围为：0% - 100%  | N/A | N/A |
| data file size | load unit 导入的全量数据中数据文件（内含 `INSERT INTO` 语句）的总大小 | N/A | N/A |
| dump process exits with error | dump unit 在 DM-worker 内部遇到错误并且退出了 | 立即告警 | critical |
| load process exits with error | load unit 在 DM-worker 内部遇到错误并且退出了  | 立即告警 | critical |
| table count | load unit 导入的全量数据中 table 的数量总和  | N/A | N/A |
| data file count | load unit 导入的全量数据中数据文件（内含 `INSERT INTO` 语句）的数量总和| N/A | N/A |
| latency of execute transaction | load unit 在执行事务的时延，单位：秒 | N/A | N/A |
| latency of query | load unit 执行 query 的耗时，单位：秒 | N/A | N/A |

### Binlog replication

下面 metrics 仅在 `task-mode` 为 `incremental` 或者 `all` 模式下会有值。

| metric 名称 | 说明  | 告警说明 | 告警级别 |
|:----|:------------|:----|:----|
| remaining time to sync | 预计 Syncer 还需要多少分钟可以和 master 完全同步，单位：分钟 | N/A | N/A |
| replicate lag | master 到 Syncer 的 binlog 复制延迟时间，单位：秒 | N/A | N/A |
| process exist with error | binlog replication 在 DM-worker 内部遇到错误并且退出了 | 立即告警 | critical |
| binlog file gap between master and syncer | 与上游 master 相比落后的 binlog file 个数 | 落后 binlog file 个数超过 1 个（不含 1 个）且持续 10 分钟时 | critical |
| binlog file gap between relay and syncer | 与 relay 相比落后的 binlog file 个数 | 落后 binlog file 个数超过 1 个（不含 1 个）且持续 10 分钟时 | critical |
| binlog event qps | 单位时间内接收到的 binlog event 数量 (不包含需要跳过的 event) | N/A | N/A |
| skipped binlog event qps  | 单位时间内接收到的需要跳过的 binlog event 数量  | N/A | N/A |
| cost of binlog event transform | Syncer 解析并且转换 binlog 成 SQLs 的耗时，单位：秒 | N/A | N/A |
| total sqls jobs | 单位时间内新增的 job 数量 | N/A | N/A |
| finished sqls jobs | 单位时间内完成的 job 数量 | N/A | N/A |
| execution latency | Syncer 执行 transaction 到下游的耗时，单位：秒 | N/A | N/A |
| unsynced tables | 当前子任务内还未收到 shard DDL 的分表数量 | N/A | N/A |
| shard lock resolving | 当前子任务是否正在等待 shard DDL 同步，大于 0 表示正在等待同步 | N/A | N/A |

## Instance

在 Grafana dashboard 中，instance 的默认名称为 `DM-instance`。

### Relay log

| metric 名称 | 说明 | 告警说明 | 告警级别 |
|:----|:------------|:----|:----|
| storage capacity | relay log 占有的磁盘的总容量  | N/A | N/A |
| storage remain | relay log 占有的磁盘的剩余可用容量  | 小于 10G 的时候需要告警 | critical |
| process exits with error | relay log 在 DM-worker 内部遇到错误并且退出了  | 立即告警 | critical |
| relay log data corruption | relay log 文件损坏的个数 | 立即告警 | emergency |
| fail to read binlog from master | relay 从上游的 MySQL 读取 binlog 时遇到的错误数 | 立即告警 | critical |
| fail to write relay log | relay 写 binlog 到磁盘时遇到的错误数 | 立即告警 | critical |
| binlog file index | relay log 最大的文件序列号。如 value = 1 表示 relay-log.000001 | N/A | N/A |
| binlog file gap between master and relay | relay 与上游 master 相比落后的 binlog file 个数 | 落后 binlog file 个数超过 1 个（不含 1 个）且持续 10 分钟时 | critical |
| binlog pos | relay log 最新文件的写入 offset  | N/A | N/A |
| read binlog duration | relay log 从上游的 MySQL 读取 binlog 的时延，单位：秒 |  N/A | N/A |
| write relay log duration | relay log 每次写 binlog 到磁盘的时延，单位：秒 | N/A | N/A |
| binlog size | relay log 写到磁盘的单条 binlog 的大小 | N/A | N/A |

### task

| metric 名称 | 说明 | 告警说明 | 告警级别 |
|:----|:------------|:----|:----|
| task state | 同步子任务的状态 | 当子任务状态处于 paused 超过 10 分钟时 | critical |
| load progress | load unit 导入过程的进度百分比，值变化范围为：0% - 100%  | N/A | N/A |
| binlog file gap between master and syncer | 与上游 master 相比 binlog replication 落后的 binlog file 个数 | N/A | N/A |
| shard lock resolving | 当前子任务是否正在等待 shard DDL 同步，大于 0 表示正在等待同步 | N/A | N/A |
