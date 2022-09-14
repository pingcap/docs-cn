---
title: TiDB 备份和恢复功能
summary: 了解 TiDB 的备份和恢复功能。
---

# TiDB 备份和恢复功能

本文介绍 TiDB 备份恢复功能及使用须知。

## 功能使用

根据 TiDB 部署方式的不同，备份恢复的方式也不同。本文主要介绍在 On-Premise 物理部署方式下，如何使用 br 命令行工具进行 TiDB 的备份和恢复。

其它 TiDB 的部署方式的备份恢复功能使用，可以参考

- [TiDB on TiDB Cloud 的备份恢复](https://docs.pingcap.com/tidbcloud/backup-and-restore)。推荐在 [TiDB Cloud](https://en.pingcap.com/tidb-cloud/) 上创建 TiDB 集群，集群的运维管将由 TiDB Cloud 团队托管完成，你可以聚焦于业务。
- [TiDB on K8S 的备份恢复](https://docs.pingcap.com/zh/tidb-in-kubernetes/stable/backup-restore-overview)。如果你使用 TiDB Operator 在 k8s 中部署了 TiDB 集群，建议通过 k8s CRD 来提交备份和恢复任务。

## 功能介绍

使用备份恢复功能，你可以进行以下两类的操作

- 对集群进行备份：你可以对集群某个时间点的全量数据进行备份（**全量备份**），也支持对业务写入在 TiDB 产生的数据变更记录进行备份（**日志备份**，日志指的是 TiKV 中的 kv 变更数据的记录）。

- 恢复备份数据：

    - 你可以**恢复某个全量备份**，或者全量备份中的**部分库/表**，将目标集群恢复到该全量备份对应的数据状态。
    - 基于备份（全量和日志）数据，你可以使用 br 指定任意时间点，将目标集群恢复到该时间所对应的备份集群数据状态。

### 对 TiDB 集群进行备份

如上所述，TiDB 支持两种类型的备份：全量备份和日志备份。

全量备份是对集群某个时间点的全量数据进行备份。 TiDB 支持以下方式的全量备份：

- 快照数据备份：TiDB 集群快照数据包含某个物理时间点上集群满足事务一致性的所有数据。BR 支持备份集群快照数据，使用请参考[快照备份](/br/br-usage-backup.md#备份-tidb-集群快照)。

全量备份一般会占用不小的存储空间，且只包含某个时间点的集群数据。如果你需要灵活的选择恢复的时间点，可以按照以下方式进行备份。它也是产品上的备份最佳实践。 实现 PITR(Point in time recovery) 的基础。

- 启动日志备份任务：运行 `br log start` 命令来启动日志备份任务，任务会在每个 TiKV 节点上持续运行，以小批量的形式定期钟将 TiDB 变更数据备份到指定存储中。
- 定期执行[快照备份](/br/br-usage-backup.md#备份-tidb-集群快照)：运行 `br backup full` 命令来备份集群快照到备份存储，例如在每天零点进行集群快照备份。

### 恢复备份数据

与备份功能相对应，你可以进行两种类型的恢复：全量恢复和 PITR (Point-in-time recovery)。

- 恢复某个全量备份

    - 恢复集群快照数据备份：你可以在一个空集群上执行快照数据备份的恢复，将该集群恢复到快照备份对应数据状态。使用请参考恢复集群快照备份。 此外你可以只恢复备份数据中指定库/表的局部数据。该功能在恢复过程中过滤掉不需要的数据。使用请参考恢复备份数据中指定库表的数据。

- 恢复到集群的历史任意时间点/PITR

    - br 提供了个一键恢复的命令，`br restore point`。 你可以指定要恢复的时间点，恢复时间点之前最近的快照数据备份，以及日志备份数据。 br 会自动判断和读取恢复需要的数据，然后将这些数据依次恢复到指定的集群。

## 备份存储

TiDB 支持将数据备份到 Amazon S3、Google Cloud Storage (GCS)、Azure Blob Storage、NFS，或者实现 S3 协议的其他文件存储服务。更多备份存储的详细信息，请参考如下内容：

- [使用 URL 格式指定备份存储](/backup-and-restore-storages.md/#url-格式)
- [使用命令行格式指定备份存储](/backup-and-restore-storages.md/#命令行格式)
- [使用外部存储时的鉴权](/backup-and-restore-storages.md#鉴权)

## 备份数据安全

TiDB 备份功能支持在存储服务端对备份数据进行加密，使用请参考[备份数据加密](/br/br-usage-backup.md#备份数据加密)。

## 使用须知

本部分介绍使用 TiDB 备份恢复功能前的注意事项，包括使用建议和兼容性。

### 使用建议

- 推荐在业务低峰时执行集群快照数据备份，这样能最大程度地减少对业务的影响；
- BR 恢复数据时会尽可能多地占用恢复集群的资源，因此推荐恢复数据到新集群或离线集群。应避免向正在提供服务的生产集群执行恢复，否则，恢复期间会对业务产生不可避免的影响；
- 不推荐同时运行多个集群快照数据备份或者恢复任务。不同的任务并行，不仅会导致备份或恢复的性能降低，影响在线业务；还会因为任务之间缺少协调机制造成任务失败，甚至对集群的状态产生影响；
- 推荐使用支持 S3、GCS 或 Azure Blob Storage 协议的存储系统保存备份数据；
- 应确保 BR、TiKV 节点和备份存储系统有足够的网络带宽，备份存储系统能提供足够的写入和读取性能，否则，它们有可能成为备份恢复时的性能瓶颈。

### 兼容性

在使用 BR 之前需要先了解 BR 存在的使用上的建议和限制。

#### 与其他功能的兼容性

+ `charset=GBK` 不兼容

 BR 在 v5.4.0 之前不支持恢复 `charset=GBK` 的表。并且，任何版本的 BR 都不支持恢复 `charset=GBK` 的表到 v5.4.0 之前的 TiDB 集群。

+ 某些功能在开启或关闭状态下，会导致 KV 格式发生变化，因此需要保证恢复集群的这些配置，与备份集群备份时的配置相同

下表整理了会导致 KV 格式发生变化的功能。

| 功能 | 相关 issue | 解决方式 |
|  ----  | ----  | ----- |
| 聚簇索引 | [#565](https://github.com/pingcap/br/issues/565)       | 确保恢复时集群的 `tidb_enable_clustered_index` 全局变量和备份时一致，否则会导致数据不一致的问题，例如 `default not found` 和数据索引不一致。 |
| New collation  | [#352](https://github.com/pingcap/br/issues/352)       | 确保恢复时集群的 `new_collations_enabled_on_first_bootstrap` 变量值和备份时的一致，否则会导致数据索引不一致和 checksum 通不过。更多信息，请参考 [FAQ - BR 为什么会报 `new_collations_enabled_on_first_bootstrap` 不匹配？](/br/backup-and-restore-faq.md#br-为什么会报-new_collations_enabled_on_first_bootstrap-不匹配)。 |
| 全局临时表 | | 确保使用 BR v5.3.0 及以上版本进行备份和恢复，否则会导致全局临时表的表定义错误。 |

在上述功能确保备份恢复一致的**前提**下，BR 和 TiKV、TiDB 及 PD 还可能因为版本之间实现不一致的问题导致功能运行失败，因此 BR 内置了版本检查。

#### 版本兼容检查

BR 内置版本会在执行备份和恢复操作前，对 TiDB 集群版本和自身版本进行对比检查。如果大版本不匹配（比如 BR v4.x 和 TiDB v5.x 上），BR 会提示退出。如要跳过版本检查，可以通过设置 `--check-requirements=false` 强行跳过版本检查。需要注意的是，跳过检查可能会遇到版本不兼容的问题。

BR 和 TiDB 各版本兼容情况如下表所示：

| 恢复版本（横向）\ 备份版本（纵向）   | 用 BR v5.4 恢复 TiDB v5.4 | 用 BR v6.0 恢复 TiDB v6.0 | 用 BR v6.1 恢复 TiDB v6.1| 用 BR v6.2 恢复 TiDB v6.2 |
|  ----  |  ----  | ---- | ---- | ---- |
|用 BR v5.4 备份 TiDB v5.4| 兼容 | 不兼容（调整恢复集群的 [新 collation](/tidb-configuration-file.md#new_collations_enabled_on_first_bootstrap) 配置跟备份集群相同后，可以恢复）| 不兼容（调整恢复集群的 [新 collation](/tidb-configuration-file.md#new_collations_enabled_on_first_bootstrap) 配置跟备份集群相同后，可以恢复） | 不兼容（调整恢复集群的 [新 collation](/tidb-configuration-file.md#new_collations_enabled_on_first_bootstrap) 配置跟备份集群相同后，可以恢复）|
|用 BR v6.0 备份 TiDB v6.0| 不兼容 |兼容 | 兼容 | 兼容 |
|用 BR v6.1 备份 TiDB v6.1| 不兼容 | 兼容（已知问题，如果备份数据中包含空库可能导致报错，参考 [#36379](https://github.com/pingcap/tidb/issues/36379)） | 兼容 | 兼容 |
|用 BR v6.2 备份 TiDB v6.2| 不兼容 | 兼容（已知问题，如果备份数据中包含空库可能导致报错，参考 [#36379](https://github.com/pingcap/tidb/issues/36379)） | 兼容 | 兼容 |
