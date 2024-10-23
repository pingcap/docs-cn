---
title: TiDB 备份与恢复概述
summary: 了解不同场景下如何使用 TiDB 的备份与恢复功能，以及不同功能、版本间的兼容性。
aliases: ['/docs-cn/dev/br/backup-and-restore-tool/','/docs-cn/dev/reference/tools/br/br/','/docs-cn/dev/how-to/maintain/backup-and-restore/br/','/zh/tidb/dev/backup-and-restore-tool/','/zh/tidb/dev/point-in-time-recovery/']
---

# TiDB 备份与恢复概述

基于 Raft 协议和合理的部署拓扑规划，TiDB 实现了集群的高可用，当集群中少数节点挂掉时，集群依然能对外提供服务。在此基础上，为了更进一步保证用户数据的安全，TiDB 还提供了集群的备份与恢复 (Backup & Restore, BR) 功能，作为数据安全的最后一道防线，使得集群能够免于严重的自然灾害，提供业务误操作“复原”的能力。

TiDB 备份恢复功能可以用于满足以下业务的需求：

- 备份集群数据到灾备系统，并保证 Recovery Point Objective (RPO) 低至 5 分钟，减少灾难场景下数据的丢失。
- 处理业务数据写错的案例，提供业务操作的“复原”能力。
- 审计业务的历史数据，满足司法审查的需求。
- 复制 (Clone) 生产环境，方便问题诊断、性能调优验证、仿真测试等。

## 使用须知

本部分介绍使用 TiDB 备份恢复功能前的注意事项，包括使用限制和使用建议。

### 使用限制

- PITR 仅支持恢复到**全新的空集群**。
- PITR 仅支持集群粒度的恢复，不支持对单个 database 或 table 的恢复。
- PITR 不支持恢复系统表中用户表和权限表的数据。
- 不支持在一个集群上**同时**运行多个数据备份任务。
- 不支持在一个集群上**同时**运行快照备份任务和数据恢复任务。
- PITR 数据恢复任务运行期间，不支持同时运行日志备份任务，也不支持通过 TiCDC 同步数据到下游集群。

### 使用建议

进行快照备份

- 推荐在业务低峰时执行集群快照数据备份，这样能最大程度地减少对业务的影响。
- 不推荐同时运行多个集群快照数据备份任务。不同的任务并行，不仅会导致备份的性能降低，影响在线业务，还会因为任务之间缺少协调机制造成任务失败，甚至对集群的状态产生影响。

进行快照恢复

- BR 恢复数据时会尽可能多地占用恢复集群的资源，因此推荐恢复数据到新集群或离线集群。应避免恢复数据到正在提供服务的生产集群，否则，恢复期间会对业务产生不可避免的影响。

备份存储和网络配置

- 推荐使用支持 Amazon S3、GCS 或 Azure Blob Storage 协议的存储系统保存备份数据；
- 应确保 BR、TiKV 节点和备份存储系统有足够的网络带宽，备份存储系统能提供足够的写入和读取性能，否则，它们有可能成为备份恢复时的性能瓶颈。

## 功能使用

根据 TiDB 部署方式的不同，使用备份恢复功能的方式也不同。本文主要介绍在本地部署方式下，如何使用 br 命令行工具进行 TiDB 的备份和恢复。

其它 TiDB 的部署方式的备份恢复功能使用，可以参考：

- [备份恢复部署在 TiDB Cloud 上的 TiDB](https://docs.pingcap.com/tidbcloud/backup-and-restore)。推荐在 [TiDB Cloud](https://www.pingcap.com/tidb-cloud/?from=en) 上创建 TiDB 集群，集群的运维管理将由 TiDB Cloud 团队托管完成，你可以聚焦于业务。
- [备份恢复部署在 Kubernetes 上的 TiDB](https://docs.pingcap.com/zh/tidb-in-kubernetes/stable/backup-restore-overview)。如果你使用 TiDB Operator 在 Kubernetes 中部署了 TiDB 集群，建议通过 Kubernetes CustomResourceDefinition (CRD) 来提交备份和恢复任务。

## 功能介绍

使用备份恢复功能，你可以进行以下两类操作：

- 对集群进行备份：你可以对集群某个时间点的全量数据进行备份（**全量备份**），也可以对业务写入在 TiDB 产生的数据变更记录进行备份（**日志备份**，日志指的是 TiKV 中的 kv 变更数据的记录）。

- 恢复备份数据：

    - 你可以**恢复某个全量备份**，或者全量备份中的**部分库/表**，将目标集群恢复到该全量备份对应的数据状态。
    - 基于备份（全量和日志）数据，你可以指定任意时间点，将目标集群恢复到该时间点所对应的备份集群数据状态 (Point-in-time recovery, PITR)。

### 备份集群数据

全量备份是对集群某个时间点的全量数据进行备份。TiDB 支持以下方式的全量备份：

- 快照数据备份：TiDB 集群快照数据包含某个物理时间点上集群满足事务一致性的所有数据。BR 支持备份集群快照数据，使用请参考[快照备份](/br/br-snapshot-guide.md#对集群进行快照备份)。

全量备份一般会占用不小的存储空间，且只包含某个时间点的集群数据。如果你需要灵活的选择恢复的时间点，即实现 PITR，可以按以下说明同时使用两种备份方式：

- 开启[日志备份](/br/br-pitr-guide.md#开启日志备份)任务后，任务会在所有 TiKV 节点上持续运行，以小批量的形式定期将 TiDB 变更数据备份到指定存储中。
- 定期执行[快照备份](/br/br-snapshot-guide.md#对集群进行快照备份)，备份集群全量数据到备份存储，例如在每天零点进行集群快照备份。

#### 备份的性能，以及对集群的影响

- 在集群 CPU 和 I/O 资源充裕时，集群快照数据备份对 TiDB 集群的影响可以保持在 20% 以下，通过合理的配置 TiDB 集群用于备份资源，影响可以降低到 10% 及更低；在集群 CPU 和 I/O 资源紧张时，可以通过调整 TiKV 配置项 [`backup.num-threads`](/tikv-configuration-file.md#num-threads-1) 来调整备份任务使用的工作线程数量以降低备份任务对 TiDB 集群的影响；单 TiKV 存储节点的备份速度可以达到 50 MB/s ～ 100 MB/s，备份速度具有可扩展性；更详细说明请参考[备份性能和影响](/br/br-snapshot-guide.md#快照备份的性能与影响)。
- 单独运行日志备份时影响约在 5%。日志备份每隔 3～5 分钟将上次刷新后产生的变更数据记录刷新到备份存储中，可以**实现低至五分钟 RPO 的集群容灾目标**。

### 恢复备份数据

与备份功能相对应，你可以进行两种类型的恢复：全量恢复和 PITR。

- 恢复某个全量备份

    - 恢复集群快照数据备份：你可以在一个空集群或不存在数据冲突（相同 schema 或 table）的集群执行快照备份恢复，将该集群恢复到快照备份对应数据状态。使用请参考[恢复快照备份](/br/br-snapshot-guide.md#恢复快照备份数据)。此外你可以只恢复备份数据中指定库/表的局部数据。该功能在恢复过程中过滤掉不需要的数据。使用请参考[恢复备份数据中指定库表的数据](/br/br-snapshot-guide.md#恢复备份数据中指定库表的数据)。

- 恢复到集群的历史任意时间点 (PITR)

    - 通过 `br restore point` 功能。你可以指定要恢复的时间点，恢复时间点之前最近的快照数据备份，以及日志备份数据。BR 会自动判断和读取恢复需要的数据，然后将这些数据依次恢复到指定的集群。

#### 恢复的性能

- 恢复集群快照数据备份，速度可以达到单 TiKV 存储节点 100 MiB/s，恢复速度具有可扩展性。更详细说明请参考[恢复性能和影响](/br/br-snapshot-guide.md#快照恢复的性能与影响)。
- 恢复日志备份数据，速度可以达到 30 GiB/h。更详细说明请参考 [PITR 的性能指标](/br/br-pitr-guide.md#pitr-的性能指标)。

## 备份存储

TiDB 支持将数据备份到 Amazon S3、Google Cloud Storage (GCS)、Azure Blob Storage、NFS，或者实现 S3 协议的其他文件存储服务。更多备份存储的详细信息，请参考如下内容：

- [使用 URI 格式指定备份存储](/external-storage-uri.md)
- [配置备份存储的访问权限](/br/backup-and-restore-storages.md#鉴权)

## 兼容性

在使用备份恢复功能之前，需要先了解 BR 工具与其他功能的兼容性以及使用限制。

### 与其他功能的兼容性

某些功能在开启或关闭状态下，会导致备份恢复功能使用出错。因此需要保证恢复集群的这些配置，与备份集群备份时的配置相同。

| 功能 | 相关 issue | 解决方式 |
|  ----  | ----  | ----- |
|GBK charset|| BR 在 v5.4.0 之前不支持恢复 `charset=GBK` 的表。并且，任何版本的 BR 都不支持恢复 `charset=GBK` 的表到 v5.4.0 之前的 TiDB 集群。|
| 聚簇索引 | [#565](https://github.com/pingcap/br/issues/565)       | 确保恢复时集群的 `tidb_enable_clustered_index` 全局变量和备份时一致，否则会导致数据不一致的问题，例如 `default not found` 和数据索引不一致。 |
| New collation  | [#352](https://github.com/pingcap/br/issues/352)       | 确保恢复时集群的 `mysql.tidb` 表中 `new_collation_enabled` 变量值和备份时的一致，否则会导致数据索引不一致和 checksum 通不过。更多信息，请参考 [FAQ - BR 为什么会报 `new_collations_enabled_on_first_bootstrap` 不匹配？](/faq/backup-and-restore-faq.md#恢复时为什么会报-new_collation_enabled-不匹配)。 |
| 全局临时表 | | 确保使用 BR v5.3.0 及以上版本进行备份和恢复，否则会导致全局临时表的表定义错误。 |
| TiDB Lightning 物理导入模式| |上游数据库使用 TiDB Lightning 物理导入模式导入的数据，无法作为数据日志备份下来。推荐在数据导入后执行一次全量备份，细节参考[上游数据库使用 TiDB Lightning 物理导入模式导入数据的恢复](/faq/backup-and-restore-faq.md#上游数据库使用-tidb-lightning-物理导入模式导入数据时为什么无法使用日志备份功能)。|
| TiCDC | | BR v8.2.0 及以上版本：如果在恢复的目标集群有 [CheckpointTS](/ticdc/ticdc-architecture.md#checkpointts) 早于 BackupTS 的 Changefeed，BR 会拒绝执行恢复。BR v8.2.0 之前的版本：如果在恢复的目标集群有任何活跃的 TiCDC Changefeed，BR 会拒绝执行恢复。 |
| 向量搜索 | | 确保使用 BR v8.4.0 及以上版本进行备份与恢复。不支持将带有[向量数据类型](/vector-search-data-types.md)的表恢复至 v8.4.0 之前的 TiDB 集群。 |

### 版本间兼容性

> **注意：**
>
> 建议使用与 TiDB 集群相同大版本的 BR 工具进行集群的备份和恢复。

在执行备份和恢复操作之前，BR 工具会检查自己的版本与 TiDB 集群的版本是否兼容。如果它们不兼容，BR 工具将报错并停止执行。如果你想跳过版本检查，可以设置 `--check-requirements=false`。但是请注意，跳过检查可能会导致恢复的数据不兼容。

从 v7.0.0 开始，TiDB 逐步支持通过 SQL 语句来执行备份和恢复操作。因此，强烈建议在备份和恢复集群时使用与 TiDB 集群相同大版本的 BR 工具，并避免跨大版本进行数据备份和恢复操作。这有助于确保恢复操作的顺利执行和数据的一致性。特别是从 v7.6.0 起，BR 默认支持在恢复数据的同时恢复 `mysql` 库下的系统表，即恢复时默认配置为 `--with-sys-table=true`。在跨版本进行数据恢复时，如果遇到 `mysql` 库的系统表结构不同导致类似 `[BR:Restore:ErrRestoreIncompatibleSys]incompatible system table` 异常，你可以通过设置 `--with-sys-table=false` 跳过恢复系统表以规避该问题。

TiDB v6.6.0 版本之前的 BR 版本兼容性矩阵：

| 备份版本（纵向）\ 恢复版本（横向）  | 恢复到 TiDB v6.0 | 恢复到 TiDB v6.1| 恢复到 TiDB v6.2 | 恢复到 TiDB v6.3、v6.4 或 v6.5 | 恢复到 TiDB v6.6 |
|  ----  |  ----  | ---- | ---- | ---- | ---- |
| TiDB v6.0、v6.1、v6.2、v6.3、v6.4 或 v6.5 快照备份 | 兼容（已知问题，如果备份数据中包含空库可能导致报错，参考 [#36379](https://github.com/pingcap/tidb/issues/36379)） | 兼容 | 兼容 | 兼容 | 兼容（需使用 v6.6 的 BR） |
| TiDB v6.3、v6.4、v6.5 或 v6.6 日志备份| 不兼容 | 不兼容 | 不兼容 | 兼容 | 兼容 |

## 探索更多

- [TiDB 快照备份与恢复使用指南](/br/br-snapshot-guide.md)
- [TiDB 日志备份与 PITR 使用指南](/br/br-pitr-guide.md)
- [备份存储](/br/backup-and-restore-storages.md)
