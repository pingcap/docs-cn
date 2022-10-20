---
title: TiDB 备份和恢复功能使用概述
summary: 了解 TiDB 的备份和恢复功能使用。
aliases: ['/zh/tidb/dev/br-deployment/']
---

# TiDB 备份和恢复功能使用概述

[TiDB 备份和恢复功能](/br/backup-and-restore-overview.md) 介绍了备份和恢复功能，在此基础上，本教程将会介绍备份和恢复功能的使用，并提供了使用示例。

## 业务使用概览

深入 TiDB 备份和恢复功能使用之前，先介绍一下推荐的对集群进行备份和恢复方案。

### 如何备份数据？

**TiDB 支持两种类型的备份，应该使用哪种备份？** 全量备份包含集群某个时间点的全量数据，日志备份包含业务写入在 TiDB 产生的数据变更记录。我们推荐这两种备份方式配合一起使用：

- **启动日志备份任务**：运行 `br log start` 命令来启动日志备份任务，任务会在每个 TiKV 节点上持续运行，以小批量的形式定期钟将 TiDB 变更数据备份到指定存储中。
- **定期地执行[快照（全量）备份](/br/br-snapshot-guide.md#对集群进行快照备份)**：运行 `br backup full` 命令来备份集群快照到备份存储，例如在每天零点进行集群快照备份。

### 如何管理备份数据？

BR 只提供备份和恢复功能的基础功能，尚不支持备份管理的功能，因此用户需要自己规划备份数据的管理事项，可能包含以下的问题：

* 选择什么备份存储系统？
* 数据备份的时候，备份数据应该放在什么目录下？
* 全量备份和日志备份的数据目录如何组织？
* 如何处理存储系统中历史备份数据？

下面是处理这些问题推荐的方式

**选择备份存储**

Amazon S3、Google Cloud Storage (GCS)、Azure Blob Storage 是 BR 推荐的存储系统选择，使用这些系统用户无需担心备份容量、备份带宽规划等。

如果 TiDB 集群部署在自建机房中， 那么推荐以下方式：

* 搭建 [minio](https://docs.min.io/docs/minio-quickstart-guide.html) 作为备份存储系统，使用 S3 协议将数据备份到 MinIO 中。
* 挂载 NFS (如 NAS) 盘到 BR 和所有的 TiKV 实例，使用 Posix file system 接口将备份数据写入对应的 NFS 目录中。

> **注意：**
>
> 如果没有挂载 NFS 到 BR 或 TiKV 节点，或者使用了支持 S3、GCS 或 Azure Blob Storage 协议的远端存储，那么 BR 备份的数据会在各个 TiKV 节点生成。**注意这不是推荐的 BR 使用方式** ，因为备份数据会分散在各个节点的本地文件系统中，聚集这些备份数据可能会造成数据冗余和运维上的麻烦，而且在不聚集这些数据便直接恢复的时候会遇到 `SST file not found` 报错。

**组织备份数据目录**

* 全量备份和日志备份保存在相同的目录下，方便统一管理，例如 `backup-${cluster-id}`。
* 每个全量备份保存到命名带有备份日期的目录下，例如 `backup-${cluster-id}/fullbackup-202209081330`。
* 日志备份数据保存在一个固定目录下, 例如 `backup-${cluster-id}/logbackup`。日志备份程序会在 logbackup 目录中每天切分出来一个新的子目录来区分每天的日志备份数据。

**处理历史备份数据**

假设你设置了**备份保留期**，即保存固定时间的备份数据，比如 7 天。 请注意**备份保留期**的概念，后面使用教程中也会多次遇到。

* 对于超过备份保留期的日志备份。使用 `br log truncate` 删除指定时间点之前的日志备份数据。因为进行 PITR 需要 1、恢复时间点之前最近的全量备份；2、全量备份和恢复时间点之间的日志备份。**建议只清理全量快照之前的日志备份**
* 对于超过备份保留期的全量备份。直接删除或者归档全量备份的目录

### 如何恢复数据？

- 如果你只有全量备份数据，或者想恢复某个确定的全量备份，那么可以使用 `br restore`  恢复指定的全量备份。
- 如果你按照以上推荐的的方式进行备份，那么你可以使用 `br restore point` 恢复到备份保留期内任意时间点。

## 部署和使用 BR

使用备份恢复功能的部署要求

- BR、TiKV 节点和备份存储系统需要提供大于备份速度的的网络带宽。当集群特别大的时候，备份和恢复速度上限受限于备份网络的带宽。
- 备份存储系统还需要提供足够的写入/读取性能（IOPS），否则它有可能成为备份恢复时的性能瓶颈。
- TiKV 节点需要为备份准备至少额外的两个 CPU core 和高性能的磁盘，否则备份将对集群上运行的业务产生影响。
- 推荐 br 运行在（8 核+/16 GB+）的节点上。

目前支持以下几种方式来使用 BR。

### 通过命令行工具（推荐）

TiDB 支持使用 br 工具进行备份恢复。

* 安装方法可以使用[使用 TiUP 在线安装](/migration-tools.md#使用-tiup-快速安装)：`tiup install br`。
* 了解如何使用 `br` 命令含工具进行备份和恢复，请参阅

    * [（全量）快照备份和恢复功能使用](/br/br-snapshot-guide.md)
    * [日志备份和 PITR 功能使用](/br/br-pitr-guide.md)
    * [TiDB 集群备份和恢复实践示例](/br/backup-and-restore-use-cases.md)

### 通过 SQL 语句

TiDB 支持使用 SQL 语句进行全量快照备份和恢复

- [`BACKUP`](/sql-statements/sql-statement-backup.md) 进行全量快照数据备份。
- [`RESTORE`](/sql-statements/sql-statement-restore.md) 进行快照备份恢复。
- [`SHOW BACKUPS|RESTORES`](/sql-statements/sql-statement-show-backups.md) 查看备份恢复的进度。

### 在 Kubernetes 环境下通过 TiDB Operator

在 Kubernetes 环境下，支持通过 TiDB Operator 支持以 S3、GCS、Azure blob storage 作为备份存储。 使用文档请参阅[使用 TiDB Operator 进行备份恢复](https://docs.pingcap.com/tidb-in-kubernetes/stable/backup-restore-overview)。