---
title: 部署和使用 BR
summary: 了解如何部署和使用 BR。
---
# 部署和使用 BR

本文档介绍 BR 的推荐部署方式，以及如何使用 BR 来备份和恢复数据。
## 部署 BR

- 生产环境中，推荐 BR 运行在（8 核+/16 GB+）的节点上。 操作系统版本要求可参考 [Linux 操作系统版本要求](/hardware-and-software-requirements.md#linux-操作系统版本要求)。
- 推荐使用支持 Amazon S3、GCS 或 Azure Blob Storage 来保存备份数据。
- 建议为备份和恢复配置足够的资源：

    - BR、TiKV 节点和备份存储系统需要提供大于备份速度的的网络带宽。当集群特别大的时候，备份和恢复速度上限受限于备份网络的带宽。
    - 备份存储系统还需要提供足够的写入/读取性能（IOPS），否则它有可能成为备份恢复时的性能瓶颈。
    - TiKV 节点需要为备份准备至少额外的两个 CPU core 和高性能的磁盘，否则备份将对集群上运行的业务产生影响。

> **注意：**
>
> - 如果没有挂载 NFS 到 BR 或 TiKV 节点，或者使用了支持 S3、GCS 或 Azure Blob Storage 协议的远端存储，那么 BR 备份的数据会在各个 TiKV 节点生成。由于 BR 只备份 leader 副本，所以各个节点预留的空间需要根据 leader size 来预估。这种部署情况下，由于 TiDB 默认使用 leader count 进行平衡，所以会出现 leader size 差别大的问题，导致各个节点备份数据不均衡。
> - *注意这不是推荐的 BR 使用方式* ，因为备份数据会分散在各个节点的本地文件系统中，聚集这些备份数据可能会造成数据冗余和运维上的麻烦，而且在不聚集这些数据便直接恢复的时候会遇到 `SST file not found` 报错。

## 使用方式

目前支持以下几种方式来使用 BR。

### 通过 SQL 语句

TiDB 支持使用 SQL 语句 [`BACKUP`](/sql-statements/sql-statement-backup.md) 和 [`RESTORE`](/sql-statements/sql-statement-restore.md) 进行备份恢复。如果要查看备份恢复的进度，你可以使用 [`SHOW BACKUPS| RESTORE`](/sql-statements/sql-statement-show-backups.md) 语句。

### 通过命令行工具

TiDB 支持使用 BR 命令行工具进行备份恢复（需[手动下载](/download-ecosystem-tools.md#备份和恢复-br-工具)）。 使用文档请参阅 [使用 br 命令行工具进行备份恢复](/br/use-br-command-line-tool.md)。

### 在 Kubernetes 环境下

在 Kubernetes 环境下，支持通过 TiDB Operator 备份 TiDB 集群数据到 S3、Google Cloud Storage 以及持久卷，并可以从中读取备份进行集群恢复。 使用文档请参阅 [使用 TiDB Operator 进行备份恢复](https://docs.pingcap.com/tidb-in-kubernetes/stable/backup-restore-overview)。
