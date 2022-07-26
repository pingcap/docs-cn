---
title: PiTR 功能介绍 
summary: 了解 PiTR 功能设计和使用。
---

# PiTR 功能介绍

使用 PiTR (Point-in-time recovery) 功能，你可以在新集群上恢复备份集群的历史任意时刻点的快照。TiDB 自 v6.2.0 开始支持 PiTR 功能，满足以下需求：

- 降低灾备场景下的 RPO，实现 RPO 15min。
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

## 功能指标

以下是 PiTR 能力的数字指标

- PiTR 的日志备份对集群的影响在 5% 左右
- PiTR 的日志备份和全量备份一起运行时，对集群的影响在 20% 以内
- PiTR 恢复速度，全量恢复 ？，日志恢复 ?

### 功能验证边界

目前 PiTR 功能经过再以下集群和数据规模场景上做过充分的验证, 请放心使用

- 20+ （8c，16G 内存） TiKV 节点数
- 100k 数量的 Region 个数
- 每小时 TiKV 增量写入数据 10 GB， 写入 (insert/update/delete) QPS 10k 

## 使用限制

- 单个集群只支持启动一个日志备份任务
- 仅支持恢复到空集群。为了避免对集群的业务请求和数据产生影响，不要在原集群（in-place）和其他已有数据集群执行 PiTR
- 存储支持 AWS S3 和 Posix file system(如 nfs 等)，暂不支持 GCS/Azure Blob Storage 做为备份存储
- 仅支持集群粒度的 PiTR，不支持对单个 database/table 执行 PiTR
- 不支持恢复用户表和权限表的数据
- 不支持恢复数据到 TiFlash storage engine。如果备份集群包含 TiFlash，执行 PiTR 后，恢复集群的数据不包含 TiFlash 副本
- 备份过程中不支持分区交换 EXCHANGE PARTITION
- 不支持在恢复中重复恢复某段时间区间的日志, 如多次重复恢复 [t1=10, ts2=20) 区间的日志备份数据可能会造成恢复后的数据不一致

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
