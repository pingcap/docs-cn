---
title: PITR 功能介绍
summary: 了解 PITR 功能设计和使用。
---

# PITR 功能介绍

使用 PITR (Point-in-time recovery) 功能，你可以在新集群上恢复备份集群的历史任意时刻点的快照。TiDB 自 v6.2.0 开始在 [BR](/br/backup-and-restore-overview.md) 工具引入 PITR 功能。

PITR 可用于满足以下业务需求：

- 降低灾备场景下的 RPO，如 RPO 不超过十几分钟。
- 处理业务数据写错的案例，如回滚业务数据到出错事件前。
- 审计业务的历史数据，满足司法审查的需求。

本文档介绍 PITR 的功能设计、能力边界与架构。如需了解如何使用 PITR，请查阅[使用 PITR](/br/pitr-usage.md)。

## 在业务中使用 PITR

[BR](/br/backup-and-restore-overview.md) 是 PITR 功能的使用入口，通过 BR 工具，你可以完成 PITR 的所有操作，包含数据备份（快照备份、日志备份）、一键恢复到指定时间点、备份数据管理。

下图为 PITR 功能使用示意：

![Point-in-Time Recovery](/media/br/pitr-usage.png)

### 备份数据

为了实现 PITR，你需要执行以下备份任务：

- 启动一个日志备份。运行 `br log start` 命令来启动数据库日志备份任务。该任务在 TiDB 集群后台持续地运行，及时地将 KV storage 的变更日志保存到备份存储中。
- 定期地执行[快照（全量）备份](/br/br-usage-backup.md#备份-tidb-集群快照)。运行 `br backup full` 命令来备份集群快照到备份存储，例如在每天零点进行集群快照备份。

### 一键恢复数据

当你执行 PITR 一键恢复数据时，你需要运行 `br restore point` 命令来调用恢复程序读取快照备份和日志备份的数据，将新集群恢复到指定时间点。

使用 `br restore point` 执行 PITR 时，需要指定恢复时间点之前的最近的快照备份数据以及日志备份数据。BR 程序会先恢复快照备份数据，然后读取并应用快照备份时间点到恢复时间点之间的日志备份数据。

### 管理备份数据

在管理备份数据时，你需要设计备份数据的存放目录结构，定期删除过期的或不再需要的备份数据。

- 组织备份数据目录：

    - 快照备份和日志备份保存在相同的目录下，方便统一管理，例如 `backup-${cluster-id}`。
    - 每个快照备份保存到命名带有备份日期的目录下，例如 `backup-${cluster-id}/snapshot-20220512000130`。
    - 日志备份数据保存在一个固定目录下，例如 `backup-${cluster-id}/log-backup`。

- 清理过期的或不再需要的备份数据：

    - 删除快照备份时，可以直接删除快照备份数据的目录。
    - 使用 BR 命令 `br log truncate` 删除备份存储指定点之前的日志备份数据。

## 功能指标

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

## 使用限制

- 单个集群只支持启动一个日志备份任务。
- 仅支持恢复到空集群。为了避免对集群的业务请求和数据产生影响，不能在原集群（in-place）和其他已有数据集群执行 PITR。
- 存储支持共享的文件系统（如 NFS 等）、 AWS S3、GCS 和 Azure Blob Storage 作为备份存储，详细介绍请参考 [AWS S3 storage](/br/backup-storage-S3.md)、[GCS storage](/br/backup-storage-gcs.md) 和 [Azure blob storage](/br/backup-storage-azblob.md)。
- 仅支持集群粒度的 PITR，不支持对单个 database 或 table 执行 PITR。
- 不支持恢复用户表和权限表的数据。
- 如果备份集群包含 TiFlash，执行 PITR 后恢复集群的数据不包含 TiFlash 副本，而是需要在恢复完成之后从 TiKV 同步数据，这会消耗一定时间。因此，恢复完成之后，TiFlash 不会立即可用。
- 上游数据库使用 TiDB Lightning Physical 方式导入的数据，无法作为数据日志备份下来。推荐在数据导入后执行一次全量备份，细节参考[上游数据库使用 TiDB Lightning Physical 方式导入数据的恢复](/br/pitr-known-issues.md#上游数据库使用-tidb-lightning-physical-方式导入数据导致无法使用日志备份功能)。
- 不支持在恢复中重复恢复某段时间区间的日志，如果多次重复恢复 [t1=10, t2=20) 区间的日志备份数据，可能会造成恢复后的数据不一致。
- 其他已知问题，请参考 [PITR 已知问题](/br/pitr-known-issues.md)。

### 版本兼容检查

在 v6.3.0 中，PITR 产生的备份文件采用新的压缩方法，同时还会合并小文件（为解决之前小文件过多带来的问题），但是这也导致旧版本 TiDB 集群与新版本产生的备份数据不兼容，详情如下表所示：

| 恢复版本（横向）\ 备份版本（纵向）   | 用 PITR v6.2.0 恢复 TiDB v6.2.0 | 用 PITR v6.3.0 恢复 TiDB v6.3.0 |
|  ----  |  ----  | ---- |
|用 PITR v6.2.0 备份 TiDB v6.2.0 | 兼容 | 兼容 |
|用 PITR v6.3.0 备份 TiDB v6.3.0 | 不兼容 |兼容 |

## PITR 架构

PITR 主要用于快照备份恢复和日志备份恢复。关于快照备份恢复，请参考 [BR 设计原理](/br/backup-and-restore-design.md)。本节介绍日志备份和恢复的实现。

日志备份恢复的架构实现如下：

![BR log backup and restore architecture](/media/br/br-log-arch.png)

进行日志备份时：

1. BR 收到 `br log start` 命令。
2. BR 在 PD 注册日志备份任务，并在 PD 保存 log backup metadata。
3. TiKV backup executor 模块监听 PD 中日志备份任务的创建，发现任务创建后开始运行任务。
4. TiKV backup executor 模块读取 KV 数据变更，并且写入到本地 SST 文件。
5. TiKV backup executor 定期将本地 SST 文件发送到备份存储中，并且更新备份存储中的 metadata。

进行日志恢复时：

1. BR 收到 `br restore point` 命令。
2. BR 读取备份存储中的日志备份数据，并计算筛选出来需要恢复的日志备份数据。
3. BR 请求 PD 创建用于恢复日志备份数据的 region (split regions)，将 region 调度到对应的 TiKV (scatter regions)。
4. PD 调度 region 成功后，BR 将恢复数据请求发送到各个 TiKV restore executor 模块。
5. TiKV restore executor 从备份存储下载日志备份数据，并将其写入对应的 region。

## 探索更多

- [日志备份和恢复功能命令使用介绍](/br/br-log-command-line.md)
- [PITR 使用教程](/br/pitr-usage.md)
- [PITR 监控告警](/br/pitr-monitoring-and-alert.md)
