---
title: 备份与恢复工具 BR 简介
summary: 了解 BR 工具是什么、有什么用。
aliases: ['/docs-cn/dev/br/backup-and-restore-tool/','/docs-cn/dev/reference/tools/br/br/','/docs-cn/dev/how-to/maintain/backup-and-restore/br/', '/docs-cn/br/backup-and-restore-tool/']
---

# 备份与恢复工具 BR 简介

[BR](https://github.com/pingcap/br) 全称为 Backup & Restore，是 TiDB **分布式备份恢复**的命令行工具，用于对 TiDB 集群进行数据备份和恢复。BR 除了可以用来进行常规的备份恢复外，也可以在保证兼容性前提下用来做大规模的数据迁移。

本文介绍了 BR 的架构、功能、部署和使用。

## BR 架构

BR 将备份或恢复操作命令下发到各个 TiKV 节点。TiKV 收到命令后执行相应的备份或恢复操作。在一次备份或恢复中，各个 TiKV 节点都会有一个对应的备份路径，TiKV 备份时产生的备份文件将会保存在该路径下，恢复时也会从该路径读取相应的备份文件。

![br-arch](/media/br-arch.png)

备份恢复的详细设计可以参考[TiDB 备份与恢复功能 BR 的设计](/br/backup-and-restore-design.md)。

## BR 功能

下面介绍了 BR 的主要功能特性，及其性能指标。

### 对 TiDB 集群进行备份

- *集群快照备份*：TiDB 集群快照数据只包含某个物理时间点上集群的最新的，满足事务一致性的所有数据。BR 支持备份集群快照数据，使用请参考[备份 TiDB 集群快照](/br/br-usage-backup.md#备份-tidb-集群快照)；
- *集群增量备份*：TiDB 集群增量数据包含在某个时间段的起始和结束两个快照的变化差异的数据。 增量数据相对比全量数据而言数据量更小，适合配合快照备份一起使用，减少备份的数据量。使用请参考[备份 TiDB 集群增量数据](/br/br-usage-backup.md#备份-tidb-集群增量数据)；
- *只备份指定库表*：BR 支持在快照备份和增量数据备份的基础上，过滤掉不需要的备份数据，帮助用户实现只备份关键业务的数据。使用请参考[备份 TiDB 集群的指定库表的数据](/br/br-usage-backup.md#备份-tidb-集群的指定库表的数据)；
- *备份数据加密*： BR 支持在备份端，或备份到 Amazon S3 的时候在存储服务端，进行备份数据加密，用户可以根据自己情况选择其中一种使用。使用请参考[备份数据加密](/br/br-usage-backup.md#备份数据加密)；
- *备份性能和影响*： BR 备份期间对 TiDB 集群的影响可以保持在 20% 以下，通过合理的配置 TiDB 集群用于备份资源，影响可以降低到 10% 及更低；单 TiKV 存储节点的备份速度可以达到 50 MB/s ～ 100 MB/s，备份速度具有可扩展性；更详细说明请参考[备份性能和影响](/br/br-usage-backup.md#备份性能和影响)
- *支持的备份存储类型*：BR 支持将数据备份到 Amazon S3/Google Cloud Storage/Azure Blob Storage/NFS，或者实现 s3 协议的其他文件存储服务。使用请参考 [备份数据到远端存储](/br/br-usage-backup.md#备份数据到远端存储)。

### 从备份数据恢复 TiDB 集群

- *恢复集群快照备份*：BR 支持在一个空集群上执行快照备份恢复，将该集群恢复到快照备份时刻点的集群最新状态。使用请参考[恢复集群快照备份](/br/br-usage-restore.md#恢复快照备份数据)；
- *恢复集群增量备份*：BR 功能支持恢复某个时间段的增量备份数据。使用请参考[备份 TiDB 集群增量数据](/br/br-usage-restore.md#恢复增量备份数据)；
- *恢复备份中的指定库表*：BR 支持只恢复备份数据中指定库/表的局部数据。该功能在恢复过程中过滤掉不需要的数据，可以用于往 TiDB 集群上恢复指定库/表的数据。使用请参考[恢复备份数据中指定库表的数据](/br/br-usage-restore.md#恢复备份数据中指定库表的数据)；
- *恢复性能和影响*： 恢复速度约为 单 TiKV 存储节点 100 MB/s，恢复速度具有可扩展性；BR 只支持恢复数据到新集群，会尽可能多的使用恢复集群的资源。更详细说明请参考[恢复性能和影响](/br/br-usage-restore.md#恢复性能和影响)。

## 部署和使用备份恢复（BR）

### 推荐部署配置

- 生产环境中，推荐 BR 运行在（8 核+/16 GB+）的节点上。 操作系统版本要求可参考 [Linux 操作系统版本要求](/hardware-and-software-requirements.md#linux-操作系统版本要求);
- 推荐使用支持 Amazon S3/GCS/Azure Blob Storage 来保存备份数据；
- 推荐为备份和恢复配置足够的资源

    - BR，TiKV 节点和备份存储系统需要提供足够的网络带宽。当集群特别大的时候，备份和恢复速度上限去觉得备份网络的带宽；
    - 备份存储系统还需要提供足够的写入/读取性能（IOPS），否则它有可能成为备份恢复时的性能瓶颈；
    - TiKV 节点需要为备份准备至少额外的两个 CPU core 和高性能的磁盘，否则备份将对集群上运行的业务产生影响。

> **注意：**
>
> - 如果没有挂载 NFS 到 BR/TiKV 节点，或者使用支持 S3/GCS/Azure Blob Storage 协议的远端存储存储，那么 BR 备份的数据会生成在各个 TiKV 节点上。 由于 BR 只备份 leader 副本，所以各个节点预留的空间需要根据 leader size 来预估；
> - 同时这种部署情况下，由于 TiDB 默认使用 leader count 进行平衡，所以会出现 leader size 差别大的问题，导致各个节点备份数据不均衡；
> - 注意这不是推荐的 BR 使用方式，因为备份数据会分散在各个节点的本地文件系统中，聚集这些备份数据可能会造成数据冗余和运维上的麻烦，而且在不聚集这些数据便直接恢复的时候会遇到颇为迷惑的 `SST file not found` 报错。

### 使用限制

在使用 BR 之前需要先了解 BR 存在的使用上的限制。

#### 不支持的场景

以下是 BR 不支持的场景：

- BR 恢复数据到运行 TiCDC / TiDB Binlog 的上游集群时，恢复数据无法由 TiCDC / TiDB Binlog 同步到下游集群。

#### 功能的兼容性

BR 和 TiDB 集群的兼容性问题氛围两方面：

+ BR 部分版本和 TiDB 集群的接口不兼容

  BR 在 v5.4.0 之前不支持恢复 `charset=GBK` 的表。并且，任何版本的 BR 都不支持恢复 `charset=GBK` 的表到 5.4.0 之前的 TiDB 集群。
  
+ 某些功能在开启或关闭状态下，会导致 KV 格式发生变化，因此备份和恢复期间如果没有统一开启或关闭，就会带来不兼容的问题

下表整理了会导致 KV 格式发生变化的功能。

| 功能 | 相关 issue | 解决方式 |
|  ----  | ----  | ----- |
| 聚簇索引 | [#565](https://github.com/pingcap/br/issues/565)       | 确保备份时 `tidb_enable_clustered_index` 全局变量和恢复时一致，否则会导致数据不一致的问题，例如 `default not found` 和数据索引不一致。 |
| New collation  | [#352](https://github.com/pingcap/br/issues/352)       | 确保恢复时集群的 `new_collations_enabled_on_first_bootstrap` 变量值和备份时的一致，否则会导致数据索引不一致和 checksum 通不过。 |
| 全局临时表 | | 确保使用 BR v5.3.0 及以上版本进行备份和恢复，否则会导致全局临时表的表定义错误。 |

在上述功能确保备份恢复一致的**前提**下，BR 和 TiKV/TiDB/PD 还可能因为版本内部协议不一致/接口不一致出现不兼容的问题，因此 BR 内置了版本检查。

#### 版本兼容检查

BR 内置版本会在执行备份和恢复操作前，对 TiDB 集群版本和自身版本进行对比检查。如果大版本不匹配（比如 BR v4.x 和 TiDB v5.x 上），BR 会提示退出。如要跳过版本检查，可以通过设置 `--check-requirements=false` 强行跳过版本检查。

需要注意的是，跳过检查可能会遇到版本不兼容的问题。BR 和 TiDB 各版本兼容情况如下表所示：

| 恢复版本（横向）\ 备份版本（纵向）   | 用 BR nightly 恢复 TiDB nightly | 用 BR v5.0 恢复 TiDB v5.0| 用 BR v4.0 恢复 TiDB v4.0 |
|  ----  |  ----  | ---- | ---- |
| 用 BR nightly 备份 TiDB nightly | ✅ | ✅ | ❌（如果恢复了使用非整数类型聚簇主键的表到 v4.0 的 TiDB 集群，BR 会无任何警告地导致数据错误） |
| 用 BR v5.0 备份 TiDB v5.0 | ✅ | ✅ | ❌（如果恢复了使用非整数类型聚簇主键的表到 v4.0 的 TiDB 集群，BR 会无任何警告地导致数据错误）
| 用 BR v4.0 备份 TiDB v4.0 | ✅ | ✅  | ✅（如果 TiKV >= v4.0.0-rc.1，BR 包含 [#233](https://github.com/pingcap/br/pull/233) Bug 修复，且 TiKV 不包含 [#7241](https://github.com/tikv/tikv/pull/7241) Bug 修复，那么 BR 会导致 TiKV 节点重启) |
| 用 BR nightly 或 v5.0 备份 TiDB v4.0 | ❌（当 TiDB 版本小于 v4.0.9 时会出现 [#609](https://github.com/pingcap/br/issues/609) 问题) | ❌（当 TiDB 版本小于 v4.0.9 会出现 [#609](https://github.com/pingcap/br/issues/609) 问题) | ❌（当 TiDB 版本小于 v4.0.9 会出现 [#609](https://github.com/pingcap/br/issues/609) 问题) |

### 最佳实践

下面是使用 BR 进行备份恢复的推荐操作：

- 推荐在业务低峰时执行备份操作，这样能最大程度地减少对业务的影响；
- BR 只支持恢复数据到新集群，会尽可能多的使用恢复集群的资源。不推荐向正在提供服务的在线集群执行恢复，恢复期间对在线业务影响很大；
- 不推荐多个 BR 备份和恢复任务并行运行。不同的任务并行，不仅会导致备份或恢复的性能降低，影响在线业务；还会因为任务之间缺少协调机制造成任务失败，甚至对集群的状态产生影响；
- 推荐使用支持 S3/GCS/Azure Blob Storage 协议的存储系统保存备份数据；
- BR，TiKV 节点和备份存储系统需要提供足够的网络带宽，备份存储系统还需要提供足够的写入/读取性能，否则它们有可能成为备份恢复时的性能瓶颈；
- BR 默认会分别在备份、恢复完成后，进行一轮数据校验，将备份数据的 checksum 同集群 [admin checksum table](/sql-statements/sql-statement-admin-checksum-table.md) 的结果比较，来保证正确性。但是 `admin checksum table` 执行耗时久，并且对集群性能影响比较大，可以根据你的情况，选择备份时关闭校验(`--checksum=false`)，只在恢复时开启校验。

#### 使用方式

目前支持以下几种方式来备份恢复的使用方式。

#### 通过命令行工具

TiDB 支持使用 BR 命令行工具进行备份恢复（需[手动下载](/download-ecosystem-tools.md#备份和恢复-br-工具)）。 关于 BR 命令行工具的具体使用方法，请参阅[使用备份与恢复工具 BR](/br/use-br-command-line-tool.md)。

#### 在 Kubernetes 环境下

在 Kubernetes 环境下，支持通过 TiDB Operator 备份 TiDB 集群数据到 S3、Google Cloud Storage 以及持久卷，并作可以从中读取备份进行集群恢复：

> **注意：**
>
> Amazon S3 和 Google Cloud Storage (GCS) 参数描述见[外部存储](/br/backup-and-restore-storages.md#url-参数)文档。

- [备份 TiDB 集群数据到兼容 S3 的存储](https://docs.pingcap.com/zh/tidb-in-kubernetes/stable/backup-to-aws-s3-using-br)
- [恢复 S3 兼容存储上的备份数据](https://docs.pingcap.com/zh/tidb-in-kubernetes/stable/restore-from-aws-s3-using-br)
- [备份 TiDB 集群到 Google Cloud Storage](https://docs.pingcap.com/zh/tidb-in-kubernetes/stable/backup-to-gcs-using-br)
- [恢复 Google Cloud Storage 上的备份数据](https://docs.pingcap.com/zh/tidb-in-kubernetes/stable/restore-from-gcs-using-br)
- [备份 TiDB 集群到持久卷](https://docs.pingcap.com/zh/tidb-in-kubernetes/stable/backup-to-pv-using-br)
- [恢复持久卷上的备份数据](https://docs.pingcap.com/zh/tidb-in-kubernetes/stable/restore-from-pv-using-br)

## BR 相关文档

+ [使用 BR 命令行备份恢复](/br/use-br-command-line-tool.md)
+ [BR 备份与恢复场景示例](/br/backup-and-restore-use-cases.md)
+ [BR 常见问题](/br/backup-and-restore-faq.md)
+ [外部存储](/br/backup-and-restore-storages.md)
