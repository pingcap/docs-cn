---
title: DM 监控指标
summary: 介绍 DM 的监控指标
aliases: ['/docs-cn/tidb-data-migration/dev/monitor-a-dm-cluster/']
---

# DM 监控指标

使用 TiUP 部署 DM 集群的时候，会默认部署一套[监控系统](/dm/migrate-data-using-dm.md#第-8-步监控任务与查看日志)。

## Task

在 Grafana dashboard 中，DM 默认名称为 `DM-task`。

### Overview

overview 下包含运行当前选定 task 的所有 DM-worker/master instance/source 的部分监控指标。当前默认告警规则只针对于单个 DM-worker/master instance/source。

| metric 名称 | 说明 | 告警说明 | 告警级别 |
|:----|:------------|:----|:----|
| task state | 迁移子任务的状态 | N/A | N/A |
| storage capacity | relay log 占有的磁盘的总容量  | N/A | N/A |
| storage remain | relay log 占有的磁盘的剩余可用容量  | N/A | N/A |
| binlog file gap between master and relay | relay 与上游 master 相比落后的 binlog file 个数 | N/A | N/A |
| load progress | load unit 导入过程的进度百分比，值变化范围为：0% - 100%  | N/A | N/A |
| binlog file gap between master and syncer | 与上游 master 相比 binlog replication unit 落后的 binlog file 个数 | N/A | N/A |
| shard lock resolving | 当前子任务是否正在等待 shard DDL 迁移，大于 0 表示正在等待迁移 | N/A | N/A |

### Operate error

| metric 名称 | 说明 | 告警说明 | 告警级别 |
|:----|:------------|:----|:----|
| before any operate error | 在进行操作之前出错的次数 | N/A | N/A |
| source bound error | 数据源绑定操作出错次数 | N/A | N/A |
| start error | 子任务启动的出错次数 | N/A | N/A |
| pause error | 子任务暂停的出错次数 | N/A | N/A |
| resume error | 子任务恢复的出错次数 | N/A | N/A |
| auto-resume error | 子任务自动恢复的出错次数 | N/A | N/A |
| update error | 子任务更新的出错次数 | N/A | N/A |
| stop error | 子任务停止的出错次数 | N/A | N/A |

### HA 高可用

| metric 名称 | 说明 | 告警说明 | 告警级别 |
|:----|:------------|:----|:----|
| number of dm-masters start leader components per minute | 每分钟内 DM-master 尝试启用 leader 相关组件次数 | N/A | N/A |
| number of workers in different state | 不同状态下有多少个 DM-worker | 存在离线的 DM-worker 超过一小时 | critical |
| workers' state | DM-worker 的状态 | N/A | N/A |
| number of worker event error | 不同类型的 DM-worker 错误出现次数 | N/A | N/A |
| shard ddl error per minute | 每分钟内不同类型的 shard DDL 错误次数 | 发生 shard DDL 错误 | critical |
| number of pending shard ddl | 未完成的 shard DDL 数目 | 存在未完成的 shard DDL 数目超过一小时 | critical |

### Task 状态

| metric 名称 | 说明 | 告警说明 | 告警级别 |
|:----|:------------|:----|:----|
| task state | 迁移子任务的状态 | 当子任务状态处于 `Paused` 超过 20 分钟时| critical |

### Dump/Load unit

下面 metrics 仅在 `task-mode` 为 `full` 或者 `all` 模式下会有值。

| metric 名称 | 说明 | 告警说明 | 告警级别 |
|:----|:------------|:----|:----|
| dump progress | dump unit 导出过程的进度百分比，值变化范围为：0% - 100%  | N/A | N/A |
| load progress | load unit 导入过程的进度百分比，值变化范围为：0% - 100%  | N/A | N/A |
| checksum progress | load unit 导入完成后，数据校验过程的进度百分比，值变化范围为：0% - 100%  | N/A | N/A |
| total bytes for load unit | load unit 导入过程中源数据解析、生成数据 KV、生成索引 KV 阶段处理的字节数 | N/A | N/A |
| chunk process duration | load unit 处理数据源文件 chunk 的耗时，单位：秒 | N/A | N/A |
| dump process exits with error | dump unit 在 DM-worker 内部遇到错误并且退出了 | 立即告警 | critical |
| load process exits with error | load unit 在 DM-worker 内部遇到错误并且退出了  | 立即告警 | critical |

### Binlog replication

下面 metrics 仅在 `task-mode` 为 `incremental` 或者 `all` 模式下会有值。

| metric 名称 | 说明  | 告警说明 | 告警级别 |
|:----|:------------|:----|:----|
| remaining time to sync | 预计 Syncer 还需要多少分钟可以和上游 master 完全同步，单位：分钟 | N/A | N/A |
| replicate lag gauge | 上游 master 到下游的 binlog 复制延迟时间，单位：秒 | N/A | N/A |
| replicate lag histogram | 上游 master 到下游的 binlog 复制延迟分布，单位：秒。注意由于统计机制不同，数据会有误差 | N/A | N/A |
| process exist with error | binlog replication unit 在 DM-worker 内部遇到错误并且退出了 | 立即告警 | critical |
| binlog file gap between master and syncer | 与上游 master 相比落后的 binlog file 个数 | 落后 binlog file 个数超过 1 个（不含 1 个）且持续 10 分钟时 | critical |
| binlog file gap between relay and syncer | 与 relay 相比落后的 binlog file 个数 | 落后 binlog file 个数超过 1 个（不含 1 个）且持续 10 分钟时 | critical |
| binlog event QPS | 单位时间内接收到的 binlog event 数量 (不包含需要跳过的 event) | N/A | N/A |
| skipped binlog event QPS | 单位时间内接收到的需要跳过的 binlog event 数量  | N/A | N/A |
| read binlog event duration | binlog replication unit 从 relay log 或上游 MySQL 读取 binlog 的耗时，单位：秒 | N/A | N/A |
| transform binlog event duration | binlog replication unit 解析 binlog 并将 binlog 转换成 SQL 语句的耗时，单位：秒 | N/A | N/A |
| dispatch binlog event duration | binlog replication unit 调度一条 binlog event 的耗时，单位：秒 | N/A | N/A |
| transaction execution latency | binlog replication unit 执行事务到下游的耗时，单位：秒 | N/A | N/A |
| binlog event size | binlog replication unit 从 relay log 或上游 MySQL 读取的单条 binlog event 的大小 | N/A | N/A |
| DML queue remain length | 剩余 DML job 队列的长度 | N/A | N/A |
| total sqls jobs | 单位时间内新增的 job 数量 | N/A | N/A |
| finished sqls jobs | 单位时间内完成的 job 数量 | N/A | N/A |
| statement execution latency | binlog replication unit 执行语句到下游的耗时，单位：秒 | N/A | N/A |
| add job duration | binlog replication unit 增加一条 job 到队列的耗时，单位：秒 | N/A | N/A |
| DML conflict detect duration | binlog replication unit 检测 DML 间冲突的耗时，单位：秒 | N/A | N/A |
| skipped event duration | binlog replication unit 跳过 binlog event 的耗时，单位：秒 | N/A | N/A |
| unsynced tables | 当前子任务内还未收到 shard DDL 的分表数量 | N/A | N/A |
| shard lock resolving | 当前子任务是否正在等待 shard DDL 迁移，大于 0 表示正在等待迁移 | N/A | N/A |
| ideal QPS | 在 DM 运行耗时为 0 时可以达到的最高 QPS | N/A | N/A |
| binlog event row | 一个 binlog 事件中的行数 | N/A | N/A |
| finished transaction total | 执行完毕的事务数量 | N/A | N/A |
| replication transaction batch | 执行到下游的事务里中 sql 行数 | N/A | N/A |
| flush checkpoints time interval | 检查点刷新时间间隔，单位：秒  | N/A | N/A |

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
| read binlog event duration | relay log 从上游的 MySQL 读取 binlog 的时延，单位：秒 |  N/A | N/A |
| write relay log duration | relay log 每次写 binlog 到磁盘的时延，单位：秒| N/A | N/A |
| binlog event size | relay log 写到磁盘的单条 binlog 的大小 | N/A | N/A |

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
| task state | 迁移子任务的状态 | 当子任务状态处于 paused 超过 10 分钟时 | critical |
| load progress | load unit 导入过程的进度百分比，值变化范围为：0% - 100%  | N/A | N/A |
| binlog file gap between master and syncer | 与上游 master 相比 binlog replication unit 落后的 binlog file 个数 | N/A | N/A |
| shard lock resolving | 当前子任务是否正在等待 shard DDL 迁移，大于 0 表示正在等待迁移 | N/A | N/A |
