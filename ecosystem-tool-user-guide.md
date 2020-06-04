---
title: TiDB 生态工具使用指南
category: reference
aliases: ['/docs-cn/dev/reference/tools/user-guide/','/docs-cn/dev/how-to/migrate/from-mysql/', '/docs-cn/dev/how-to/migrate/incrementally-from-mysql/', '/docs-cn/dev/how-to/migrate/overview/', '/docs-cn/dev/reference/tools/use-guide/']
---

# TiDB 生态工具使用指南

本文档从生态工具的功能与适用场景这两个维度出发，介绍 TiDB 相关生态工具的功能及部分常见场景下的工具选择，同时也简单介绍部分工具之间的替代关系。

## 生态工具功能

### 全量导出

[Mydumper](/mydumper-overview.md) 是一个用于从 MySQL/TiDB 进行全量逻辑导出的工具。

基本信息：

- Mydumper 的输入：MySQL/TiDB 集群
- Mydumper 的输出：SQL 文件
- 适用 TiDB 版本：所有版本
- Kubernetes 支持：[备份与恢复](https://pingcap.com/docs-cn/tidb-in-kubernetes/stable/backup-and-restore-using-helm-charts/)

### 全量导入

[TiDB Lightning](/tidb-lightning/tidb-lightning-overview.md) 是一个用于将全量数据导入到 TiDB 集群的工具。

使用 TiDB Lightning 导入数据到 TiDB 时，有两种模式：

- `importer` 模式：以 TiKV-importer 作为后端，这种模式一般用于导入大量的数据（TB 级别）到新集群，但在数据导入过程中集群无法提供正常的服务。
- `tidb` 模式：以 TiDB/MySQL 作为后端，这种模式相比 `importer` 模式的导入速度较慢，但是可以在线导入，同时也支持将数据导入到 MySQL。

基本信息：

- Lightning 的输入：
    - Mydumper 或 Dumpling 输出文件
    - CSV 格式文件
- 适用 TiDB 版本：v2.1 及以上
- Kubernetes 支持：[使用 TiDB Lightning 快速恢复 Kubernetes 上的 TiDB 集群数据](https://pingcap.com/docs-cn/tidb-in-kubernetes/stable/restore-data-using-tidb-lightning/)

> **注意：**
>
> 原 Loader 工具已停止维护，不再推荐使用。相关场景请使用 TiDB Lightning 的 `tidb` 模式进行替代，详细信息请参考 [TiDB Lightning TiDB-backend 文档](/tidb-lightning/tidb-lightning-tidb-backend.md#从-loader-迁移到-tidb-lightning-tidb-backend)。

### 备份和恢复

[BR](/br/backup-and-restore-tool.md) 是一个对 TiDB 进行分布式备份和恢复的工具，可以高效地对大数据量的 TiDB 集群进行数据备份和恢复。

基本信息：

- [备份输出和恢复输入的文件类型](/br/backup-and-restore-tool.md#备份文件类型)：SST + `backupmeta` 文件
- 适用 TiDB 版本：v3.1 及 v4.0
- Kubernetes 支持：已支持，文档撰写中

### TiDB Binlog

[TiDB Binlog](/tidb-binlog/tidb-binlog-overview.md) 是收集 TiDB 的增量 binlog 数据，并提供准实时同步和备份的工具。该工具可用于 TiDB 集群间的增量数据同步，如将其中一个 TiDB 集群作为另一个 TiDB 集群的从集群。

基本信息：

- TiDB Binlog 的输入：TiDB 集群
- TiDB Binlog 的输出：TiDB 集群、MySQL、Kafka 或者增量备份文件
- 适用 TiDB 版本：v2.1 及以上
- Kubernetes 支持：[TiDB Binlog 运维文档](https://pingcap.com/docs-cn/tidb-in-kubernetes/stable/deploy-tidb-binlog/)，[Kubernetes 上的 TiDB Binlog Drainer 配置](https://pingcap.com/docs-cn/tidb-in-kubernetes/stable/configure-tidb-binlog-drainer/)

### 数据迁入

[TiDB Data Migration (DM)](https://pingcap.com/docs-cn/tidb-data-migration/stable/overview/) 是将 MySQL/MariaDB 数据迁移到 TiDB 的工具，支持全量数据和增量数据的迁移。

基本信息：

- DM 的输入：MySQL/MariaDB
- DM 的输出：TiDB 集群
- 适用 TiDB 版本：所有版本
- Kubernetes 支持：开发中

如果数据量在 TB 级别以下，推荐直接使用 DM 迁移 MySQL/MariaDB 数据到 TiDB（迁移的过程包括全量数据的导出导入和增量数据的同步）。

如果数据量在 TB 级别，推荐的迁移步骤如下：

1. 使用 [Mydumper](/mydumper-overview.md) 导出 MySQL/MariaDB 全量数据。
2. 使用 [TiDB Lightning](/tidb-lightning/tidb-lightning-overview.md) 将全量导出数据导入 TiDB 集群。
3. 使用 DM 迁移 MySQL/MariaDB 增量数据到 TiDB。

> **注意：**
>
> - 原 Syncer 工具已停止维护，不再推荐使用，相关场景请使用 DM 的增量迁移模式进行替代。

## 常见适用场景

### 从 MySQL/Aurora 导入全量数据

当需要从 MySQL/Aurora 导入全量数据时，可先使用 [Mydumper](/mydumper-overview.md) 将数据导出为 SQL dump files，然后再使用 [TiDB Lightning](/tidb-lightning/tidb-lightning-overview.md) 将数据导入到 TiDB 集群。

如果已有其他工具导出的格式兼容的 CSV 或 SQL dump files，则可直接使用 TiDB Lightning 进行导入。

### 从 MySQL/Aurora 迁移数据

当既需要从 MySQL/Aurora 导入全量数据，又需要迁移增量数据时，可使用 [TiDB Data Migration (DM)](https://pingcap.com/docs-cn/tidb-data-migration/stable/overview/) 完成全量数据和增量数据的迁移。

如果全量数据量较大（TB 级别），则可先使用 [Mydumper](/mydumper-overview.md) 与 [TiDB Lightning](/tidb-lightning/tidb-lightning-overview.md) 完成全量数据的迁移，再使用 DM 完成增量数据的迁移。

### TiDB 集群备份与恢复

当需要对 TiDB 集群进行备份或在之后对 TiDB 集群进行恢复时，可使用 [BR](/br/backup-and-restore-tool.md)。

另外，BR 也可以对 TiDB 的数据进行[增加备份](/br/backup-and-restore-tool.md#增量备份)和[增量恢复](/br/backup-and-restore-tool.md#增量恢复)。

### 迁出数据到 MySQL/TiDB

当需要将 TiDB 集群的数据迁出到 MySQL 或其他 TiDB 集群时，可使用 [Mydumper](/mydumper-overview.md) 从 TiDB 将全量数据导出为 SQL dump files，然后再使用 [TiDB Lightning](/tidb-lightning/tidb-lightning-overview.md) 将数据导入到 MySQL/TiDB。

如果还需要执行增量数据的迁移，则可使用 [TiDB Binlog](/tidb-binlog/tidb-binlog-overview.md)。

### TiDB 增量数据订阅

当需要订阅 TiDB 增量数据的变更时，可使用 [TiDB Binlog](/tidb-binlog/binlog-slave-client.md)。
