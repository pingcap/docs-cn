---
title: TiDB 生态工具功能概览
aliases: ['/docs-cn/v3.0/ecosystem-tool-user-guide/','/docs-cn/v3.0/reference/tools/user-guide/','/docs-cn/v3.0/how-to/migrate/from-mysql/', '/docs-cn/v3.0/how-to/migrate/incrementally-from-mysql/', '/docs-cn/v3.0/how-to/migrate/overview/', '/docs-cn/v3.0/reference/tools/use-guide/']
---

# TiDB 工具功能概览

本文档从工具的功能出发，介绍部分工具的功能以及它们之间的替代关系。

## 在 Kubernetes 上部署运维 TiDB

[TiDB Operator](https://docs.pingcap.com/zh/tidb-in-kubernetes/stable) 是 Kubernetes 上的 TiDB 集群自动运维系统，提供包括部署、升级、扩缩容、备份恢复、配置变更的 TiDB 全生命周期管理。借助 TiDB Operator，TiDB 可以无缝运行在公有云或私有部署的 Kubernetes 集群上。

基本信息：

- [TiDB Operator 架构](https://docs.pingcap.com/zh/tidb-in-kubernetes/stable/architecture)
- [在 Kubernetes 上部署运维 TiDB 快速上手](https://docs.pingcap.com/zh/tidb-in-kubernetes/stable/get-started/)
- 适用 TiDB 版本：v2.1 及以上

## 全量导出

[Dumpling](/export-or-backup-using-dumpling.md) 是一个用于从 MySQL/TiDB 进行全量逻辑导出的工具。

基本信息：

- Dumpling 的输入：MySQL/TiDB 集群
- Dumpling 的输出：SQL/CSV 文件
- 适用 TiDB 版本：所有版本
- Kubernetes 支持：尚未支持

## 全量导入

[TiDB Lightning](/tidb-lightning/tidb-lightning-overview.md) 是一个用于将全量数据导入到 TiDB 集群的工具。

使用 TiDB Lightning 导入数据到 TiDB 时，有两种模式：

- `importer` 模式：以 TiKV-importer 作为后端，这种模式一般用于导入大量的数据（TB 级别）到新集群，但在数据导入过程中集群无法提供正常的服务。
- `tidb` 模式：以 TiDB/MySQL 作为后端，这种模式相比 `importer` 模式的导入速度较慢，但是可以在线导入，同时也支持将数据导入到 MySQL。

基本信息：

- Lightning 的输入：
    - Dumpling 输出文件
    - 其他格式兼容的 CSV 文件
- 适用 TiDB 版本：v2.1 及以上
- Kubernetes 支持：[使用 TiDB Lightning 快速恢复 Kubernetes 上的 TiDB 集群数据](https://pingcap.com/docs-cn/tidb-in-kubernetes/v1.0/restore-data-using-tidb-lightning/)

> **注意：**
>
> 原 Loader 工具已停止维护，不再推荐使用。相关场景请使用 TiDB Lightning 的 `tidb` 模式进行替代，详细信息请参考 [TiDB Lightning TiDB-backend 文档](/tidb-lightning/tidb-lightning-tidb-backend.md#从-loader-迁移到-tidb-lightning-tidb-backend)。

## 备份和恢复

[Dumpling](/export-or-backup-using-dumpling.md) 可用于将 TiDB 集群备份到 SQL 或 CSV 格式的文件，可参考[全量导出](#全量导出)。

[TiDB Lightning](/tidb-lightning/tidb-lightning-overview.md) 可用于将 Dumpling 导出的 SQL 或 CSV 格式的文件恢复到 TiDB 集群，可参考 [全量导入](#全量导入)。

## TiDB 增量日志同步

[TiDB Binlog](/tidb-binlog/tidb-binlog-overview.md) 是收集 TiDB 的增量 binlog 数据，并提供准实时同步和备份的工具。该工具可用于 TiDB 集群间的增量数据同步，如将其中一个 TiDB 集群作为另一个 TiDB 集群的从集群。

基本信息：

- TiDB Binlog 的输入：TiDB 集群
- TiDB Binlog 的输出：TiDB 集群、MySQL、Kafka 或者增量备份文件
- 适用 TiDB 版本：v2.1 及以上
- Kubernetes 支持：[TiDB Binlog 运维文档](https://pingcap.com/docs-cn/tidb-in-kubernetes/v1.0/deploy-tidb-binlog/)，[Kubernetes 上的 TiDB Binlog Drainer 配置](https://pingcap.com/docs-cn/tidb-in-kubernetes/v1.0/configure-tidb-binlog-drainer/)

## 数据迁入

[TiDB Data Migration (DM)](https://docs.pingcap.com/zh/tidb-data-migration/v2.0/overview) 是将 MySQL/MariaDB 数据迁移到 TiDB 的工具，支持全量数据和增量数据的迁移。

基本信息：

- DM 的输入：MySQL/MariaDB
- DM 的输出：TiDB 集群
- 适用 TiDB 版本：所有版本
- Kubernetes 支持：开发中

如果数据量在 TB 级别以下，推荐直接使用 DM 迁移 MySQL/MariaDB 数据到 TiDB（迁移的过程包括全量数据的导出导入和增量数据的同步）。

如果数据量在 TB 级别，推荐的迁移步骤如下：

1. 使用 [Dumpling](/export-or-backup-using-dumpling.md) 导出 MySQL/MariaDB 全量数据。
2. 使用 [TiDB Lightning](/tidb-lightning/tidb-lightning-overview.md) 将全量导出数据导入 TiDB 集群。
3. 使用 DM 迁移 MySQL/MariaDB 增量数据到 TiDB。

> **注意：**
>
> - 原 Syncer 工具已停止维护，不再推荐使用，相关场景请使用 DM 的增量迁移模式进行替代。
