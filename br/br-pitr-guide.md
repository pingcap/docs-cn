---
title: TiDB 日志备份和 PITR 使用指南
summary: 了解 TiDB 的日志备份和 PITR 功能使用。
---

# TiDB 日志备份和 PITR 使用指南

全量备份包含集群某个时间点的全量数据，但是不包含其他时间点的更新数据，而 TiDB 日志备份能够将业务写入 TiDB 的数据记录及时地备份到指定存储中。如果你需要灵活的选择恢复的时间点，可以按照以下方式配合地使用两种备份方式。它是实现 PITR(Point in time recovery) 的基础。

- **启动日志备份任务**：运行 br log start 命令来启动日志备份任务，任务会在每个 TiKV 节点上持续运行，以小批量的形式定期钟将 TiDB 变更数据备份到指定存储中。
- **定期地执行快照（全量）备份**：运行 br backup full 命令来备份集群快照到备份存储，例如在每天零点进行集群快照备份。

## 对集群进行备份

### 启动日志备份

使用 `br log start` 启动日志备份任务，一个集群只能启动一个日志备份任务。日志备份任务启动后，该命令就会立即返回：

```shell
tiup br log start --task-name=pitr --pd "${PD_IP}:2379" --storage 's3://backup-101/logbackup?access_key=${access_key}&secret_access_key=${secret_access_key}"'
```

日志备份任务在 TiDB 集群后台持续地运行，直到你手动暂停它。 如果你需要查询日志备份任务当前状态，运行下面的命令：

```shell
tiup br log status --task-name=pitr --pd "${PD_IP}:2379"
```

日志备份任务状态输出如下

```
● Total 1 Tasks.
> #1 <
    name: pitr
    status: ● NORMAL
    start: 2022-05-13 11:09:40.7 +0800
      end: 2035-01-01 00:00:00 +0800
    storage: s3://backup-101/log-backup
    speed(est.): 0.00 ops/s
checkpoint[global]: 2022-05-13 11:31:47.2 +0800; gap=4m53s
```

### 定期执行全量备份

使用快照备份功能作为全量备份的方法，以固定的周期（比如 2 天）进行全量备份

```shell
tiup br backup full --pd "${PD_IP}:2379" --storage 's3://backup-101/snapshot-${date}?access_key=${access_key}&secret_access_key=${secret_access_key}"'
```

## 进行 PITR

如果你想恢复到备份保留期内的任意时间点，可以使用 `br restore point` 进行一键恢复。使用这个命令，你只需要指定**要恢复的时间点**、**恢复时间点之前最近的快照备份**以及**日志备份数据**。 br 会自动判断和读取恢复需要的数据，然后将这些数据依次恢复到指定的集群。

```shell
br restore point --pd "${PD_IP}:2379" \
--storage='s3://backup-101/logbackup?access_key=${access_key}&secret_access_key=${secret_access_key}"' \
--full-backup-storage='s3://backup-101/snapshot-${date}?access_key=${access_key}&secret_access_key=${secret_access_key}"' \
--restored-ts '2022-05-15 18:00:00+0800'
```

恢复期间有进度条会在终端中显示，进度条效果如下。 恢复分为两个阶段：全量恢复（Full Restore）和日志恢复（Restore Meta Files 和 Restore KV files。 每个阶段完成恢复后, br 都会输出恢复耗时、恢复数据大小等信息。

```shell
Full Restore <--------------------------------------------------------------------------------------------------------------------------------------------------------> 100.00%
*** ["Full Restore success summary"] ****** [total-take=xxx.xxxs] [restore-data-size(after-compressed)=xxx.xxx] [Size=xxxx] [BackupTS={TS}] [total-kv=xxx] [total-kv-size=xxx] [average-speed=xxx]
Restore Meta Files <--------------------------------------------------------------------------------------------------------------------------------------------------> 100.00%
Restore KV Files <----------------------------------------------------------------------------------------------------------------------------------------------------> 100.00%
*** ["restore log success summary"] [total-take=xxx.xx] [restore-from={TS}] [restore-to={TS}] [total-kv-count=xxx] [total-size=xxx]
```

## 清理过期的日志备份数据

如[使用指南概览](/br/br-use-overview.md)所述：

* 对于超过备份保留期的日志备份。使用 `br log truncate` 删除指定时间点之前的日志备份数据。因为进行 PITR 需要 1、恢复时间点之前最近的全量备份；2、全量备份和恢复时间点之间的日志备份。**建议只清理全量快照之前的日志备份**

我们可以按照下面的步骤清理超过**备份保留期**的日志备份数据：

* 查找备份保留期之外的**最近的一个全量备份**，使用 `validate` 指令获取它对应的时间点。例如，你要清理 2022/09/01 之前的备份数据，那么应该查找该日期之前的最近一个全量备份，且必须保证它不会被清理。执行下面的命令获取这个全量备份对应的时间点

  ```shell
  FULL_BACKUP_TS=`tiup br validate decode --field="end-version" -s "s3://backup-101/snapshot-${date}?access_key=${access_key}&secret_access_key=${secret_access_key}"| tail -n1`
  ```

* 清理该快照备份(< FULL_BACKUP_TS)之前的日志备份数据

  ```shell
  tiup br log truncate --until=${FULL_BACKUP_TS} --storage='s3://backup-101/logbackup?access_key=${access_key}&secret_access_key=${secret_access_key}"'
  ```

* 清理该快照备份(< FULL_BACKUP_TS)之前的快照备份

## 性能与影响

### 快照备份的性能与影响

### 能力指标

- PITR 恢复速度，平均到单台 TiKV 节点：全量恢复为 280 GB/h ，日志恢复为 30 GB/h
- 使用 BR 清理过期的日志备份数据速度为 600 GB/h

> **注意：**
>
> - 以上功能指标是根据下述两个场景测试得出的结论，如有出入，建议以实际测试结果为准
> - 全量恢复速度 = 全量恢复集群数据量 / (时间 * TiKV 数量)
> - 日志恢复速度 = 日志恢复总量 / (时间 * TiKV 数量)

测试场景 1（[TiDB Cloud](https://tidbcloud.com) 上部署）

- TiKV 节点（8 core，16 GB 内存）数量：21
- Region 数量：183,000
- 集群新增日志数据：10 GB/h
- 写入 (insert/update/delete) QPS：10,000

测试场景 2 (本地部署）

- TiKV 节点（8 core，64 GB 内存）数量：6
- Region 数量：50,000
- 集群新增日志数据：10 GB/h
- 写入 (insert/update/delete) QPS：10,000

## 进一步阅读

* [TiDB 集群备份和恢复实践示例](/br/backup-and-restore-use-cases.md)
* [br 命令行手册](/br/use-br-command-line-tool.md)
* [日志备份和 PITR 架构设计](/br/br-log-architecture.md)
