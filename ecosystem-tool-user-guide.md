---
title: TiDB 工具功能概览
aliases: ['/docs-cn/dev/ecosystem-tool-user-guide/','/docs-cn/dev/reference/tools/user-guide/','/docs-cn/dev/how-to/migrate/from-mysql/', '/docs-cn/dev/how-to/migrate/incrementally-from-mysql/', '/docs-cn/dev/how-to/migrate/overview/', '/docs-cn/dev/reference/tools/use-guide/']
summary: TiDB 提供了丰富的工具，包括部署运维工具 TiUP 和 TiDB Operator，数据管理工具如 TiDB Data Migration（DM）、Dumpling、TiDB Lightning、Backup & Restore（BR）、TiCDC、sync-diff-inspector，以及 OLAP 分析工具 TiSpark。这些工具可用于部署、数据迁移、备份恢复、数据校验等多种操作，满足不同需求。
---

# TiDB 工具功能概览

TiDB 提供了丰富的工具，可以帮助你进行部署运维、数据管理（例如，数据迁移、备份恢复、数据校验）、在 TiKV 上运行 Spark SQL。请根据需要选择适用的工具。

## 部署运维工具

TiDB 提供了 TiUP 和 TiDB Operator 部署运维工具，满足你在不同系统环境下的部署运维需求。

### 在物理机或虚拟机上部署运维 TiDB

#### TiUP

[TiUP](/tiup/tiup-overview.md) 是在物理机或虚拟机上的 TiDB 包管理器，管理着 TiDB 的众多的组件，如 TiDB、PD、TiKV 等。当你想要运行 TiDB 生态中任何组件时，只需要执行一行 TiUP 命令即可。

[TiUP cluster](https://github.com/pingcap/tiup/tree/master/components/cluster) 是 TiUP 提供的使用 Golang 编写的集群管理组件，通过 TiUP cluster 组件就可以进行日常的运维工作，包括部署、启动、关闭、销毁、弹性扩缩容、升级 TiDB 集群，以及管理 TiDB 集群参数。

基本信息：

- [术语及核心概念](/tiup/tiup-terminology-and-concepts.md)
- [使用 TiUP 部署 TiDB 集群](/production-deployment-using-tiup.md)
- [TiUP 组件管理](/tiup/tiup-component-management.md)
- 适用 TiDB 版本：v4.0 及以上

### 在 Kubernetes 上部署运维 TiDB - TiDB Operator

[TiDB Operator](https://docs.pingcap.com/zh/tidb-in-kubernetes/stable) 是 Kubernetes 上的 TiDB 集群自动运维系统，提供包括部署、升级、扩缩容、备份恢复、配置变更的 TiDB 全生命周期管理。借助 TiDB Operator，TiDB 可以无缝运行在公有云或自托管的 Kubernetes 集群上。

基本信息：

- [TiDB Operator 架构](https://docs.pingcap.com/zh/tidb-in-kubernetes/stable/architecture)
- [在 Kubernetes 上部署运维 TiDB 快速上手](https://docs.pingcap.com/zh/tidb-in-kubernetes/stable/get-started/)
- 适用 TiDB 版本：v2.1 及以上

## 数据管理工具

 TiDB 提供了丰富的数据管理工具，例如数据迁移、导入导出、备份恢复、增量同步、数据校验等。

### 数据迁入 - TiDB Data Migration (DM)

[TiDB Data Migration (DM)](/dm/dm-overview.md) 是将 MySQL/MariaDB 数据迁移到 TiDB 的工具，支持全量数据的迁移和增量数据的复制。

基本信息：

- TiDB DM 的输入：MySQL/MariaDB
- TiDB DM 的输出：TiDB 集群
- 适用 TiDB 版本：所有版本
- Kubernetes 支持：使用 [TiDB Operator](https://docs.pingcap.com/zh/tidb-in-kubernetes/dev/deploy-tidb-dm) 在 Kubernetes 上部署 TiDB DM。

如果数据量在 TB 级别以下，推荐直接使用 TiDB DM 迁移 MySQL/MariaDB 数据到 TiDB（迁移的过程包括全量数据的导出导入和增量数据的复制）。

如果数据量在 TB 级别，推荐的迁移步骤如下：

1. 使用 [Dumpling](/dumpling-overview.md) 导出 MySQL/MariaDB 全量数据。
2. 使用 [TiDB Lightning](/tidb-lightning/tidb-lightning-overview.md) 将全量导出数据导入 TiDB 集群。
3. 使用 TiDB DM 复制 MySQL/MariaDB 增量数据到 TiDB。

> **注意：**
>
> - 原 Syncer 工具已停止维护，不再推荐使用，相关场景请使用 TiDB DM 的增量复制模式进行替代。

### 全量导出 - Dumpling

[Dumpling](/dumpling-overview.md) 是一个用于从 MySQL/TiDB 进行全量逻辑导出的工具。

基本信息：

- Dumpling 的输入：MySQL/TiDB 集群
- Dumpling 的输出：SQL/CSV 文件
- 适用 TiDB 版本：所有版本
- Kubernetes 支持：尚未支持

> **注意：**
>
> PingCAP 之前维护的 Mydumper 工具 fork 自 [mydumper project](https://github.com/maxbube/mydumper)，针对 TiDB 的特性进行了优化。从 v7.5.0 开始，[Mydumper](https://docs.pingcap.com/tidb/v4.0/mydumper-overview) 废弃，其绝大部分功能已经被 [Dumpling](/dumpling-overview.md) 取代，强烈建议切换到 Dumpling。

### 全量导入 - TiDB Lightning

[TiDB Lightning](/tidb-lightning/tidb-lightning-overview.md) 是一个用于将全量数据导入到 TiDB 集群的工具。

使用 TiDB Lightning 导入数据到 TiDB 时，有以下模式：

- [物理导入模式](/tidb-lightning/tidb-lightning-physical-import-mode.md)：TiDB Lightning 将数据解析为有序的键值对，并直接将其导入 TiKV。这种模式一般用于导入大量的数据（TB 级别）到新集群，但在数据导入过程中集群无法提供正常的服务。
- [逻辑导入模式](/tidb-lightning/tidb-lightning-logical-import-mode.md)：以 TiDB/MySQL 作为后端，这种模式相比物理导入模式，导入速度较慢，但是可以在线导入，同时也支持将数据导入到 MySQL。

基本信息：

- TiDB Lightning 的输入：
    - Dumpling 输出文件
    - 其他格式兼容的 CSV 文件
    - 从 Aurora、Hive 或 Snowflake 导出的 Parquet 文件
- 适用 TiDB 版本：v2.1 及以上
- Kubernetes 支持：[使用 TiDB Lightning 快速恢复 Kubernetes 上的 TiDB 集群数据](https://docs.pingcap.com/zh/tidb-in-kubernetes/stable/restore-data-using-tidb-lightning)

> **注意：**
>
> 原 Loader 工具已停止维护，不再推荐使用。相关场景请使用 TiDB Lightning 的 `tidb` 模式进行替代。

### 备份和恢复 - Backup & Restore

[Backup & Restore (BR)](/br/backup-and-restore-overview.md) 是一个对 TiDB 进行分布式备份和恢复的工具，可以高效地对大数据量的 TiDB 集群进行数据备份和恢复。

基本信息：

- [备份输出和恢复输入的文件类型](/br/backup-and-restore-design.md)
- 适用 TiDB 版本：v4.0 及以上
- Kubernetes 支持：[使用 BR 工具备份 TiDB 集群数据到兼容 S3 的存储](https://docs.pingcap.com/zh/tidb-in-kubernetes/stable/backup-to-aws-s3-using-br)，[使用 BR 工具恢复 S3 兼容存储上的备份数据](https://docs.pingcap.com/zh/tidb-in-kubernetes/stable/restore-from-aws-s3-using-br)

### TiDB 增量数据同步 - TiCDC

[TiCDC](/ticdc/ticdc-overview.md) 是一款通过拉取 TiKV 变更日志实现的 TiDB 增量数据同步工具，具有将数据还原到与上游任意 TSO 一致状态的能力，同时提供开放数据协议 (TiCDC Open Protocol)，支持其他系统订阅数据变更。

基本信息：

- TiCDC 的输入：TiDB 集群
- TiCDC 的输出：TiDB 集群、MySQL、Kafka、Confluent
- 适用 TiDB 版本：v4.0.6 及以上

### 数据校验 - sync-diff-inspector

[sync-diff-inspector](/sync-diff-inspector/sync-diff-inspector-overview.md) 是一个用于校验 MySQL/TiDB 中两份数据是否一致的工具。该工具还提供了修复数据的功能，可用于修复少量不一致的数据。

基本信息：

- sync-diff-inspector 的输入：TiDB、MySQL
- sync-diff-inspector 的输出：TiDB、MySQL
- 适用 TiDB 版本：所有版本

## OLAP 分析工具 - TiSpark

[TiSpark](/tispark-overview.md) 是 PingCAP 为解决用户复杂 OLAP 需求而推出的产品。它借助 Spark 平台，同时融合 TiKV 分布式集群的优势，和 TiDB 一起为用户一站式解决 HTAP (Hybrid Transactional/Analytical Processing) 的需求。
