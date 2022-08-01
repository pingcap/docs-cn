---
title: PiTR 功能介绍
summary: 了解 PiTR 功能设计和使用。
---

# PiTR 功能介绍

使用 PiTR (Point-in-time recovery) 功能，你可以在新集群上恢复备份集群的历史任意时刻点的快照。TiDB 自 v6.2.0 开始在 [BR](/br/backup-and-restore-overview.md) 工具引入 PiTR 功能。通过 BR 工具，你可以完成 PiTR 的所有操作，包含数据备份（快照备份、日志备份）、一键恢复到指定时间点。

PiTR 可用于满足以下业务需求：

- 降低灾备场景下的 RPO，如 RPO 不超过十几分钟。
- 处理业务数据写错的案例，如回滚业务数据到出错事件前。
- 审计业务的历史数据，满足司法审查的需求。

本文档介绍 PiTR 的功能设计、能力边界与架构。如需了解如何使用 PiTR，请查阅 [使用 PiTR](/br/pitr-usage.md)。

## 在业务中使用 PiTR

[BR](/br/backup-and-restore-overview.md) 是 PiTR 功能的使用入口，通过 BR 工具，你可以完成 PiTR 的所有操作，包含数据备份（快照备份、日志备份）、一键恢复到指定时间点、备份数据管理。

下图为 PiTR 功能使用示意：

![Point-in-Time Recovery](/media/br/pitr-usage.png)

### 备份数据

为了实现 PiTR，你需要执行以下的数据备份：

- 启动一个日志备份。运行 `br log start` 命令来启动数据库日志备份任务。该任务在 TiDB 集群后台持续地运行，及时地将 KV storage 的变更日志保存到备份存储中。
- 定期地执行[快照（全量）备份](/br/br-usage-backup.md#备份-tidb-集群快照)。运行 `br backup full` 命令来备份集群快照到备份存储，例如在每天零点进行集群快照备份。

### 一键恢复数据

当你执行 PiTR 一键恢复数据时，你需要运行 `br restore point` 命令来调用恢复程序读取快照备份和日志备份的数据，将新集群恢复到指定时间点。

使用 `br restore point` 执行 PiTR 时，需要指定恢复时间点之前的最近的快照备份数据以及日志备份数据。BR 程序会先恢复快照备份数据，然后读取并应用快照备份时间点到恢复时间点之间的日志备份数据。

### 管理备份数据

在管理备份数据时，你需要设计备份数据的存放目录结构，和定期删除过期的（不再被需要的）备份数据。

- 组织备份数据目录：

  - 快照备份和日志备份保存在相同的目录下，方便统一管理，例如 `backup-${cluster-id}`。
  - 每个快照备份保存到命名带有备份日期的目录下，例如 `backup-${cluster-id}/snapshot-20220512000130`。
  - 日志备份数据保存在一个固定目录下, 例如 `backup-${cluster-id}/log-backup`。

- 清理过期的（不再被需要）的备份数据：

  - 删除快照备份时，可以直接删除快照备份数据的目录
  - 使用 BR 命令 `br log truncate` 删除备份存储指定点之前的日志备份数据

## 功能指标

以下是 PiTR 能力的数字指标：

- PiTR 的日志备份对集群的影响在 5% 左右
- PiTR 的日志备份和全量备份一起运行时，对集群的影响在 20% 以内
- PiTR 恢复速度，平均到单台 TiKV 节点：全量恢复为 290 GB/h ，日志恢复为 30 GB/h
- PiTR 功能提供的灾备 RPO 低至十几分钟，RTO 根据要恢复的数据规模几分钟到几个小时不等
- 使用 BR 清理过期的日志备份数据速度为 600GB/h

以上功能指标经过了以下场景验证：


测试场景 1 （on TiDB Cloud）

- 21 （8c，16G 内存） TiKV 节点
- 183k 数量的 Region
- 每小时 TiKV 增量写入数据 10 GB， 写入 (insert/update/delete) QPS 10k

测试场景 2 （On-premise）

- 6 （8c，16G 内存） TiKV 节点数
- 50k 数量的 Region 个数
- 每小时 TiKV 增量写入数据 10 GB， 写入 (insert/update/delete) QPS 10k

## 使用限制

- 单个集群只支持启动一个日志备份任务。
- 仅支持恢复到空集群。为了避免对集群的业务请求和数据产生影响，不要在原集群（in-place）和其他已有数据集群执行 PiTR。
- 存储支持 AWS S3 和 POSIX file system（如 NFS 等），暂不支持使用 GCS 和 Azure Blob Storage 作为备份存储。
- 仅支持集群粒度的 PiTR，不支持对单个 database 或 table 执行 PiTR。
- 不支持恢复用户表和权限表的数据。
- 不支持恢复数据到 TiFlash 存储引擎。如果备份集群包含 TiFlash，执行 PiTR 后，恢复集群的数据不包含 TiFlash 副本。如果恢复集群包含 TiFlash，用户需要进行设置。具体操作，参考[手动设置 schema 或 table 的 TiFlash 副本](/br/pitr-troubleshoot.md#在使用-br-restore-point-命令恢复下游集群后无法从-tiflash-引擎中查询到数据该如何处理)。
- 备份过程中不支持分区交换 (Exchange Partition)。
- 不支持在恢复中重复恢复某段时间区间的日志，如果多次重复恢复 [t1=10, ts2=20) 区间的日志备份数据，可能会造成恢复后的数据不一致。

## PiTR 架构

PiTR 功能主要包含了快照备份恢复、日志备份恢复功能。关于快照备份恢复，请参考 [BR 设计原理](/br/backup-and-restore-design.md)。本节介绍日志备份和恢复的实现。

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
5. TiKV restore executor从备份存储下载日志备份数据，并将其写入对应的 region。

## 部署和使用 PiTR

运行 PiTR 的相关功能，BR 需要运行在（8 核+/16 GB+）的节点上, 用于备份和恢复的 TiDB 集群配置需要满足 [TiDB 集群推荐配置](/hardware-and-software-requirements.md)。

## 探索更多

-  [日志备份和恢复功能命令使用介绍](/br/br-log-command-line.md)
-  [PiTR 使用教程](/br/pitr-usage.md)
