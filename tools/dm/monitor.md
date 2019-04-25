---
title: DM 监控指标
summary: 介绍 DM 的监控指标
category: tools
---

# DM 监控指标

使用 DM-Ansible 部署 DM 集群的时候，会默认部署一套[监控系统](/tools/dm/practice.md#第-7-步监控任务与查看日志)。

> **注意：**
>
> 目前只有 DM-worker 提供了 metrics，DM-master 暂未提供。

## Task

在 Grafana dashboard 中，DM 默认名称为 `DM-task`。 

### overview

overview 下包含运行当前选定 task 的所有 DM-worker instance 的部分监控指标。当前默认告警规则只针对于单个 DM-worker instance。

| metric 名称 | 说明 | 告警说明 |
|:----|:------------|:----|
| task state | 同步子任务的状态 | N/A |
| storage capacity | relay log 占有的磁盘的总容量  | N/A |
| storage remain | relay log 占有的磁盘的剩余可用容量  | N/A |
| binlog file gap between master and relay | relay 与上游 master 相比落后的 binlog file 个数 | N/A |
| load progress | loader 导入过程的进度百分比，值变化范围为：0% - 100%  | N/A |
| binlog file gap between master and syncer | 与上游 master 相比 binlog replication 落后的 binlog file 个数 | N/A |
| shard lock resolving | 当前子任务是否正在等待 shard DDL 同步，大于 0 表示正在等待同步 | N/A |


### task 状态

| metric 名称 | 说明 | 告警说明 |
|:----|:------------|:----|
| task state | 同步子任务的状态 | 当子任务状态处于 paused 超过 10 分钟时|

### Relay log

| metric 名称 | 说明 | 告警说明 |
|:----|:------------|:----|
| storage capacity | relay log 占有的磁盘的总容量  | N/A |
| storage remain | relay log 占有的磁盘的剩余可用容量  | 小于 10G 的时候需要告警 |
| process exits with error | relay log 在 DM-worker 内部遇到错误并且退出了  | 立即告警 |
| relay log data corruption | relay log 文件损坏的个数 | 立即告警 |
| fail to read binlog from master | relay 从上游的 MySQL 读取 binlog 时遇到的错误数 | 立即告警 |
| fail to write relay log | relay 写 binlog 到磁盘时遇到的错误数 | 立即告警 |
| binlog file index | relay log 最大的文件序列号。如 value = 1 表示 relay-log.000001 | N/A |
| binlog file gap between master and relay | relay 与上游 master 相比落后的 binlog file 个数 | 落后 binlog file 个数超过 1 个（不含 1 个）且持续 10 分钟时 |
| binlog pos | relay log 最新文件的写入 offset  | N/A |
| read binlog duration | relay log 从上游的 MySQL 读取 binlog 的时延，单位：秒 |  N/A |
| write relay log duration | relay log 每次写 binlog 到磁盘的时延，单位：秒| N/A |
| binlog size | relay log 写到磁盘的单条 binlog 的大小 | N/A |

### Dumper

下面 metrics 仅在 `task-mode` 为 `full` 或者 `all` 模式下会有值。

| metric 名称 | 说明 | 告警说明 |
|:----|:------------|:----|
| dump process exits with error | dumper 在 DM-worker 内部遇到错误并且退出了 | 立即告警 |

### Loader

下面 metrics 仅在 `task-mode` 为 `full` 或者 `all` 模式下会有值。

| metric 名称 | 说明 | 告警说明 |
|:----|:------------|:----|
| load progress | loader 导入过程的进度百分比，值变化范围为：0% - 100%  | N/A |
| data file size | loader 导入的全量数据中数据文件（内含 `INSERT INTO` 语句）的总大小 | N/A |
| load process exits with error | loader 在 DM-worker 内部遇到错误并且退出了  | 立即告警 |
| table count | loader 导入的全量数据中 table 的数量总和  | N/A |
| data file count | loader 导入的全量数据中数据文件（内含 `INSERT INTO` 语句）的数量总和| N/A |
| latency of execute transaction | loader 在执行事务的时延，单位：秒 | N/A |
| latency of query | loader 执行 query 的耗时，单位：秒 | N/A |

### Binlog replication

下面 metrics 仅在 `task-mode` 为 `incremental` 或者 `all` 模式下会有值。

| metric 名称 | 说明  | 告警说明 |
|:----|:------------|:----|
| remaining time to sync | 预计 syncer 还需要多少分钟可以和 master 完全同步，单位：分钟 | N/A |
| replicate lag | master 到 syncer 的 binlog 复制延迟时间，单位：秒 | N/A |
| process exist with error | binlog replication 在 DM-worker 内部遇到错误并且退出了 | 立即告警 |
| binlog file gap between master and syncer | 与上游 master 相比落后的 binlog file 个数 | 落后 binlog file 个数超过 1 个（不含 1 个）且持续 10 分钟时 |
| binlog file gap between relay and syncer | 与 relay 相比落后的 binlog file 个数 | 落后 binlog file 个数超过 1 个（不含 1 个）且持续 10 分钟时 |
| binlog event qps | 单位时间内接收到的 binlog event 数量 (不包含需要跳过的 event) | N/A |
| skipped binlog event qps  | 单位时间内接收到的需要跳过的 binlog event 数量  | N/A |
| cost of binlog event transform | syncer 解析并且转换 binlog 成 SQLs 的耗时，单位：秒 | N/A |
| total sqls jobs | 单位时间内新增的 job 数量 | N/A |
| finished sqls jobs | 单位时间内完成的 job 数量 | N/A |
| execution latency | syncer 执行 transaction 到下游的耗时，单位：秒 | N/A |
| unsynced tables | 当前子任务内还未收到 shard DDL 的分表数量 | N/A |
| shard lock resolving | 当前子任务是否正在等待 shard DDL 同步，大于 0 表示正在等待同步 | N/A |


## Instance

在 Grafana dashboard 中，instance 的默认名称为 `DM-instance`。

### Relay log

| metric 名称 | 说明 | 告警说明 |
|:----|:------------|:----|
| storage capacity | relay log 占有的磁盘的总容量  | N/A |
| storage remain | relay log 占有的磁盘的剩余可用容量  | 小于 10G 的时候需要告警 |
| process exits with error | relay log 在 DM-worker 内部遇到错误并且退出了  | 立即告警 |
| relay log data corruption | relay log 文件损坏的个数 | 立即告警 |
| fail to read binlog from master | relay 从上游的 MySQL 读取 binlog 时遇到的错误数 | 立即告警 |
| fail to write relay log | relay 写 binlog 到磁盘时遇到的错误数 | 立即告警 |
| binlog file index | relay log 最大的文件序列号。如 value = 1 表示 relay-log.000001 | N/A |
| binlog file gap between master and relay | relay 与上游 master 相比落后的 binlog file 个数 | 落后 binlog file 个数超过 1 个（不含 1 个）且持续 10 分钟时 |
| binlog pos | relay log 最新文件的写入 offset  | N/A |
| read binlog duration | relay log 从上游的 MySQL 读取 binlog 的时延，单位：秒 |  N/A |
| write relay log duration | relay log 每次写 binlog 到磁盘的时延，单位：秒 | N/A |
| binlog size | relay log 写到磁盘的单条 binlog 的大小 | N/A |

### task

| metric 名称 | 说明 | 告警说明 |
|:----|:------------|:----|
| task state | 同步子任务的状态 | 当子任务状态处于 paused 超过 10 分钟时 |
| load progress | loader 导入过程的进度百分比，值变化范围为：0% - 100%  | N/A |
| binlog file gap between master and syncer | 与上游 master 相比 binlog replication 落后的 binlog file 个数 | N/A |
| shard lock resolving | 当前子任务是否正在等待 shard DDL 同步，大于 0 表示正在等待同步 | N/A |
