---
title: TiDB 生态工具使用指南
category: reference
aliases: ['/docs-cn/dev/reference/tools/user-guide/','/docs-cn/dev/how-to/migrate/from-mysql/', '/docs-cn/dev/how-to/migrate/incrementally-from-mysql/', '/docs-cn/dev/how-to/migrate/overview/', '/docs-cn/dev/reference/tools/use-guide/']
---

# TiDB 生态工具使用指南

目前 TiDB 生态工具较多，有些工具之间有功能重叠，也有些属于版本迭代关系。本文档将对各个工具进行介绍，说明各个工具之间的关系，并且说明各个版本、场景下应该使用哪些工具。

## TiDB 生态工具概览

TiDB 生态工具可以分为几种：

- 数据导入类，包括全量导入工具、备份和恢复工具、增量导入工具等
- 数据导出类，包括全量导出工具、增量导出工具等

下面将分别介绍这两类工具。

### 数据导入类

#### 全量导入工具 Loader（停止维护，不推荐使用）

[Loader](/loader-overview.md) 是一款轻量级的全量数据导入工具，数据以 SQL 的形式导入到 TiDB 中。目前这个工具正在逐步被 [TiDB Lightning](#全量导入工具-tidb-lightning) 替换掉，参见 [TiDB Lightning TiDB-backend 文档](/tidb-lightning/tidb-lightning-tidb-backend.md#从-loader-迁移到-tidb-lightning-tidb-backend)。

以下是 Loader 的一些基本信息：

- Loader 的输入：Mydumper 输出的文件
- Loader 的输出：以 SQL 形式写入 TiDB
- 适用 TiDB 版本：所有版本
- Kubernetes 支持：[备份与恢复](https://pingcap.com/docs-cn/tidb-in-kubernetes/stable/backup-and-restore-using-helm-charts/)

#### 全量导入工具 TiDB Lightning

[TiDB Lightning](/tidb-lightning/tidb-lightning-overview.md) 是将全量数据快速导入到一个新的 TiDB 集群的工具。

注意用 TiDB Lightning 导入数据到 TiDB 的时候，有两种模式：

- 默认模式：`tikv-importer` 为后端，这种模式下导入数据过程中集群无法提供正常的服务，用于导入大量的数据（TB 级别）。
- 第二种模式：`TiDB` 为后端（相当于 Loader 的功能），相对默认模式导入速度较慢，但是可以在线导入。

以下是 TiDB Lightning 的一些基本信息：

- Lightning 的输入
    - Mydumper 输出文件
    - CSV 格式文件
- 适用 TiDB 版本：v2.1 及以上
- Kubernetes 支持：[使用 TiDB Lightning 快速恢复 Kubernetes 上的 TiDB 集群数据](https://pingcap.com/docs-cn/tidb-in-kubernetes/stable/restore-data-using-tidb-lightning/)

#### 备份和恢复工具 BR

[BR](/br/backup-and-restore-tool.md) 是 TiDB 进行分布式备份恢复的命令行工具，用于对 TiDB 集群进行数据备份和恢复。相比 Mydumper 和 Loader，BR 更适合大数据量的场景，有更高效的备份和恢复效率。

以下是 BR 的一些基本信息：

- [备份输出和恢复输入的文件类型](/br/backup-and-restore-tool.md#备份文件类型)：SST + `backupmeta` 文件
- 适用 TiDB 版本：v3.1 及 v4.0
- Kubernetes 支持：已支持，文档撰写中

#### 增量导入工具 Syncer（已停止维护，不推荐使用）

[Syncer](/syncer-overview.md) 是将 MySQL/MariaDB 增量 binlog 数据实时复制导入到 TiDB 的工具。目前推荐使用 [TiDB Data Migration](#增量导入工具-tidb-data-migration) 替换该工具。

以下是 Syncer 的一些基本信息：

- Syncer 的输入：MySQL/MariaDB 的 binlog
- Syncer 的输出：以 SQL 形式写入 TiDB
- 适用 TiDB 版本：所有版本
- Kubernetes 支持：不支持

#### 增量导入工具 TiDB Data Migration

[TiDB Data Migration (DM)](https://pingcap.com/docs-cn/tidb-data-migration/stable/overview/) 是将 MySQL/MariaDB 数据迁移到 TiDB 的工具，支持全量数据和增量数据的同步。

以下是 DM 的一些基本信息：

- DM 的输入：MySQL/MariaDB 的全量数据以及 binlog
- DM 的输出：以 SQL 形式写入 TiDB
- 适用 TiDB 版本：所有版本
- Kubernetes 支持：开发中

### 数据导出类

#### 全量导出工具 Mydumper

[Mydumper](/mydumper-overview.md) 用于对 MySQL/TiDB 进行全量逻辑备份。

以下是 Mydumper 的一些基本信息：

- Mydumper 的输入：MySQL/TiDB 集群
- Mydumper 的输出：SQL 文件
- 适用 TiDB 版本：所有版本
- Kubernetes 支持：[备份与恢复](https://pingcap.com/docs-cn/tidb-in-kubernetes/stable/backup-and-restore-using-helm-charts/)

#### 增量导出工具 TiDB Binlog

[TiDB Binlog](/tidb-binlog/tidb-binlog-overview.md) 是收集 TiDB 的 binlog，并提供准实时同步和备份的工具。

以下是 TiDB Binlog 的一些基本信息：

- TiDB Binlog 的输入：TiDB 集群
- TiDB Binlog 的输出：MySQL、TiDB、Kafka 或者增量备份文件
- 适用 TiDB 版本：v2.1 及以上
- Kubernetes 支持：[TiDB Binlog 运维文档](https://pingcap.com/docs-cn/tidb-in-kubernetes/stable/deploy-tidb-binlog/)，[Kubernetes 上的 TiDB Binlog Drainer 配置](https://pingcap.com/docs-cn/tidb-in-kubernetes/stable/configure-tidb-binlog-drainer/)

## 工具演进路线

下面简单的介绍一下 TiDB 生态工具集的演进，方便大家了解工具之间的关系。

### TiDB 备份与恢复

Mydumper、Loader -> BR：

Mydumper 和 Loader 都是在逻辑层面进行备份和恢复，效率较低；BR 使用 TiDB 的特性进行备份和恢复，适合数据量比较大的场景，备份效率大大提升。

### TiDB 全量恢复

Loader -> TiDB Lightning：

Loader 使用 SQL 的方式进行全量数据恢复，效率较低。TiDB Lightning 将数据直接导入 TiKV，大大提升了全量数据恢复的效率，适合将大量数据（TB 级别以上数据）快速导入到一个全新的 TiDB 集群中；且 TiDB Lightning 集成了 Loader 的逻辑导入数据功能，参见 [TiDB Lightning TiDB-backend 文档](/tidb-lightning/tidb-lightning-tidb-backend.md#从-loader-迁移到-tidb-lightning-tidb-backend)，支持在线导入数据。

### MySQL 数据迁移

- Mydumper、Loader、Syncer -> DM：

    使用 Mydumper、Loader、Syncer 将 MySQL 数据迁移到 TiDB，迁移过程比较繁琐。DM 提供了一体化的数据迁移方案，提高了易用性，而且 DM 还支持分库分表的合并。

- Loader -> TiDB Lightning：

    TiDB Lightning 集成了 Loader 的逻辑导入数据功能，参见 [TiDB Lightning TiDB-backend 文档](/tidb-lightning/tidb-lightning-tidb-backend.md#从-loader-迁移到-tidb-lightning-tidb-backend)，由 TiDB Lightning 统一提供全量数据恢复功能。

## 数据迁移解决方案

针对 TiDB 的 2.1，3.0 以及 3.1 版本，下面给出典型业务场景下的数据迁移方案。

### TiDB 3.0 全链路数据迁移方案

#### MySQL 数据迁移到 TiDB

如果 MySQL 数据量在 TB 级别以上，推荐迁移步骤如下：

1. 使用 Mydumper 导出 MySQL 全量数据
2. 使用 TiDB Lightning 将 MySQL 全量备份数据导入 TiDB 集群
3. 使用 DM 同步 MySQL 增量数据到 TiDB

如果 MySQL 数据量在 TB 级别以下，推荐直接使用 DM 迁移 MySQL 数据到 TiDB（迁移的过程包括全量导入和增量的同步）。

#### TiDB 集群数据的同步

使用 TiDB Binlog 将 TiDB 数据同步到下游 TiDB/MySQL。

#### TiDB 集群数据的全量备份及恢复

推荐步骤：

1. 使用 Mydumper 进行全量数据的备份
2. 使用 TiDB Lightning 将全量数据恢复到 TiDB/MySQL

### TiDB 3.1 全链路数据迁移方案

#### MySQL 数据迁移到 TiDB

如果 MySQL 数据量在 TB 级别以上，推荐迁移步骤如下：

1. 使用 Mydumper 导出 MySQL 全量数据
2. 使用 TiDB Lightning 将 MySQL 全量备份数据导入 TiDB 集群
3. 使用 DM 同步 MySQL 增量数据到 TiDB

如果 MySQL 数据量在 TB 级别以下，推荐直接使用 DM 迁移 MySQL 数据到 TiDB（迁移的过程包括全量导入和增量的同步）。

#### TiDB 集群数据的同步

使用 TiDB-Binlog 将 TiDB 数据同步到下游 TiDB/MySQL。

#### TiDB 集群数据的全量备份及恢复

- 恢复到 TiDB

    - 使用 BR 进行全量数据的备份
    - 使用 BR 进行全量数据的恢复

- 恢复到 MySQL

    - 使用 Mydumper 进行全量数据的备份
    - 使用 TiDB Lightning 进行全量数据的恢复
