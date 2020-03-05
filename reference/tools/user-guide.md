---
title: TiDB 生态工具使用指南
category: reference
aliases: ['/docs-cn/v3.0/how-to/migrate/from-mysql/', '/docs-cn/v3.0/how-to/migrate/incrementally-from-mysql/', '/docs-cn/v3.0/how-to/migrate/overview/', '/docs-cn/v3.0/reference/tools/use-guide/']
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

[Loader](/reference/tools/loader.md) 是一款轻量级的全量数据导入工具，数据以 SQL 的形式导入到 TiDB 中。目前这个工具正在逐步被 [TiDB Lightning](#全量导入工具-tidb-lightning) 替换掉，参见 [TiDB Lightning TiDB-backend 文档](/reference/tools/tidb-lightning/tidb-backend.md#从-loader-迁移到-tidb-lightning-tidb-backend)。

以下是 Loader 的一些基本信息：

- Loader 的输入：Mydumper 输出的文件
- Loader 的输出：以 SQL 形式写入 TiDB
- 适用 TiDB 版本：所有版本
- Kubernetes 支持：[备份与恢复](/tidb-in-kubernetes/maintain/backup-and-restore/charts.md)

#### 全量导入工具 TiDB Lightning

[TiDB Lightning](/reference/tools/tidb-lightning/overview.md) 是将全量数据快速导入到一个新的 TiDB 集群的工具。

注意用 TiDB Lightning 导入数据到 TiDB 的时候，有两种模式：

- 默认模式：`tikv-importer` 为后端，这种模式下导入数据过程中集群无法提供正常的服务，用于导入大量的数据（TB 级别）。
- 第二种模式：`TiDB` 为后端（相当于 Loader 的功能），相对默认模式导入速度较慢，但是可以在线导入。

以下是 TiDB Lightning 的一些基本信息：

- Lightning 的输入
    - Mydumper 输出文件
    - CSV 格式文件
- 适用 TiDB 版本：v2.1 及以上
- Kubernetes 支持：[使用 TiDB Lightning 快速恢复 Kubernetes 上的 TiDB 集群数据](/tidb-in-kubernetes/maintain/lightning.md)

#### 增量导入工具 Syncer（已停止维护，不推荐使用）

[Syncer](/reference/tools/syncer.md) 是将 MySQL/MariaDB 增量 binlog 数据实时复制导入到 TiDB 的工具。目前推荐使用 [TiDB Data Migration](#增量导入工具-tidb-data-migration) 替换该工具。

以下是 Syncer 的一些基本信息：

- Syncer 的输入：MySQL/MariaDB 的 binlog
- Syncer 的输出：以 SQL 形式写入 TiDB
- 适用 TiDB 版本：所有版本
- Kubernetes 支持：不支持

#### 增量导入工具 TiDB Data Migration

[TiDB Data Migration (DM)](/reference/tools/data-migration/overview.md) 是将 MySQL/MariaDB 数据迁移到 TiDB 的工具，支持全量数据和增量数据的同步。

以下是 DM 的一些基本信息：

- DM 的输入：MySQL/MariaDB 的全量数据以及 binlog
- DM 的输出：以 SQL 形式写入 TiDB
- 适用 TiDB 版本：所有版本
- Kubernetes 支持：开发中

### 数据导出类

#### 全量导出工具 Mydumper

[Mydumper](/reference/tools/mydumper.md) 用于对 MySQL/TiDB 进行全量逻辑备份。

以下是 Mydumper 的一些基本信息：

- Mydumper 的输入：MySQL/TiDB 集群
- Mydumper 的输出：SQL 文件
- 适用 TiDB 版本：所有版本
- Kubernetes 支持：[备份与恢复](/tidb-in-kubernetes/maintain/backup-and-restore/charts.md)

#### 增量导出工具 TiDB Binlog

[TiDB Binlog](/reference/tidb-binlog/overview.md) 是收集 TiDB 的 binlog，并提供准实时同步和备份的工具。

以下是 TiDB Binlog 的一些基本信息：

- TiDB Binlog 的输入：TiDB 集群
- TiDB Binlog 的输出：MySQL、TiDB、Kafka 或者增量备份文件
- 适用 TiDB 版本：v2.1 及以上
- Kubernetes 支持：[TiDB Binlog 运维文档](/tidb-in-kubernetes/maintain/tidb-binlog.md)，[Kubernetes 上的 TiDB Binlog Drainer 配置](/tidb-in-kubernetes/reference/configuration/tidb-drainer.md)

## 工具演进路线

下面简单的介绍一下 TiDB 生态工具集的演进，方便大家了解工具之间的关系。

### MySQL 数据迁移

- Mydumper、Loader、Syncer -> DM：

    使用 Mydumper、Loader、Syncer 将 MySQL 数据迁移到 TiDB，迁移过程比较繁琐。DM 提供了一体化的数据迁移方案，提高了易用性，而且 DM 还支持分库分表的合并。

- Loader -> TiDB Lightning：

    TiDB Lightning 集成了 Loader 的逻辑导入数据功能，参见 [TiDB Lightning TiDB-backend 文档](/reference/tools/tidb-lightning/tidb-backend.md#从-loader-迁移到-tidb-lightning-tidb-backend)，由 TiDB Lightning 统一提供全量数据恢复功能。

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
