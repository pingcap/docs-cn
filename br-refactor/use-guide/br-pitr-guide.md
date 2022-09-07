---
title: TiDB 日志备份和 PITR 功能使用
summary: 了解 TiDB 的日志备份和 PITR 功能使用。
---

# 使用日志备份和 PITR

TiDB 日志备份能够及时的将 TiDB 变更数据备份到指定存储中。如果你需要灵活的选择恢复的时间点，可以按照以下方式进行备份。它是实现 PITR(Point in time recovery) 的基础。

- **启动日志备份任务**：运行 br log start 命令来启动日志备份任务，任务会在每个 TiKV 节点上持续运行，以小批量的形式定期钟将 TiDB 变更数据备份到指定存储中。
- **定期地执行快照（全量）备份**：运行 br backup full 命令来备份集群快照到备份存储，例如在每天零点进行集群快照备份。

## 对集群进行备份

### 启动日志备份

使用 `br log start` 启动日志备份任务，一个集群只能启动一个日志备份任务：

```shell
br log start --task-name=pitr --pd "${PDIP}:2379" --storage='s3://{tidb_cluster_id}/backup-data/log-backup'
```

启动日志备份任务后，可以查询日志备份任务状态：

```shell
br log status --task-name=pitr --pd "${PDIP}:2379"
```

输出结果如下

```
● Total 1 Tasks.
> #1 <
    name: pitr
    status: ● NORMAL
    start: 2022-05-13 11:09:40.7 +0800
      end: 2035-01-01 00:00:00 +0800
    storage: s3://tidb_cluster_ud/backup-data/log-backup
    speed(est.): 0.00 ops/s
checkpoint[global]: 2022-05-13 11:31:47.2 +0800; gap=4m53s
```

### 定期执行全量备份

使用快照备份功能作为全量备份的方法，以固定的周期（比如 2 天）进行全量备份

```shell
br backup full --pd "${PDIP}:2379" --storage 's3://{tidb_cluster_id}/backup-data/full-backup-{date}'
```

## 进行 PITR

如果你想恢复到备份保留期内的任意时间点，可以使用 `br restore point` 进行一键恢复，你只需要指定要恢复的时间点、恢复时间点之前最近的快照数据备份以及日志备份数据。 br 会自动判断和读取恢复需要的数据，然后将这些数据依次恢复到指定的集群。

```shell
br restore point --pd "${PDIP}:2379" \
--storage='s3://{tidb_cluster_id}/backup-data/log-backup' \
--full-backup-storage='s3://{tidb_cluster_id}/backup-data/full-backup-{date}' \
--restored-ts '2022-05-15 18:00:00+0800'
```

## PITR 功能指标

### 能力指标

- PITR 的日志备份对集群的影响在 5% 左右
- PITR 的日志备份和全量备份一起运行时，对集群的影响在 20% 以内
- PITR 恢复速度，平均到单台 TiKV 节点：全量恢复为 280 GB/h ，日志恢复为 30 GB/h
- PITR 功能提供的灾备 RPO 低至十几分钟，RTO 根据要恢复的数据规模几分钟到几个小时不等
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

### 使用限制

- 单个集群只支持启动一个日志备份任务。
- 仅支持恢复到空集群。为了避免对集群的业务请求和数据产生影响，不能在原集群（in-place）和其他已有数据集群执行 PITR。
- 存储支持 AWS S3 和共享的文件系统（如 NFS 等），暂不支持使用 GCS 和 Azure Blob Storage 作为备份存储。
- 仅支持集群粒度的 PITR，不支持对单个 database 或 table 执行 PITR。
- 不支持恢复用户表和权限表的数据。
- 如果备份集群包含 TiFlash，执行 PITR 后恢复集群的数据不包含 TiFlash 副本，需要手动恢复 TiFlash 副本。具体操作参考[手动设置 schema 或 table 的 TiFlash 副本](/br/pitr-troubleshoot.md#在使用-br-restore-point-命令恢复下游集群后无法从-tiflash-引擎中查询到数据该如何处理)。
- 上游数据库使用 TiDB Lightning Physical 方式导入的数据，无法作为数据日志备份下来。推荐在数据导入后执行一次全量备份，细节参考[上游数据库使用 TiDB Lightning Physical 方式导入数据的恢复](/br/pitr-known-issues.md#上游数据库使用-tidb-lightning-physical-方式导入数据导致无法使用日志备份功能)。
- 备份过程中不支持分区交换 (Exchange Partition)，参考[日志备份过程中执行分区交换](/br/pitr-troubleshoot.md#日志备份过程中执行分区交换-exchange-partition-ddl在-pitr-恢复时会报错该如何处理)。
- 不支持在恢复中重复恢复某段时间区间的日志，如果多次重复恢复 [t1=10, ts2=20) 区间的日志备份数据，可能会造成恢复后的数据不一致。
- 其他已知问题，请参考 [PITR 已知问题](/br/pitr-known-issues.md)。

## 进一步阅读

* [TiDB 集群备份和恢复实践示例](/br-refactor/use-guide/br-usage.md)