---
title: 数据迁移概述
summary: 本文档介绍支持哪些路径将数据迁移到 TiDB。
aliases: ['/docs-cn/dev/migration-overview/','/docs-cn/dev/data-migration-route','/zh/tidb/dev/data-migration-route']
---

# 数据迁移概述

本文档介绍支持从哪些路径将数据迁移到 TiDB，包括从 MySQL 迁移到 TiDB 和从 CSV/SQL 文件迁移到 TiDB。

## 从 Aurora 迁移到 TiDB

在云环境下，可以直接通过 Aurora Snapshot 导出的方式，将全量数据迁移至 TiDB。详细可参考[使用 TiDB Lightning 从 Amazon Aurora MySQL 迁移全量数据](/migrate-from-aurora-using-lightning.md)。

## 从 MySQL 全量迁移到 TiDB

目前可以使用以下两种方式将 MySQL 数据全量迁移到 TiDB。

- [1 TiB 以内的全量数据迁移](#使用-dm-迁移数据)
- [大于 1 TiB 的全量数据迁移](#使用-dumpling-和-tidb-lightning-迁移全量数据)

### 1 TiB 以内的全量数据迁移

#### 适合场景

使用 DM 迁移数据适合迁移 MySQL 全量数据并同步增量数据的场景，且全量数据的大小小于 1 TiB。如果全量数据的大小大于 1 TiB，建议使用 Dumpling 和 TiDB Lightning 导入全量数据后，再使用 DM 同步增量数据。

#### 迁移方法

DM 支持将 MySQL 全量数据迁移到 TiDB，并同步 MySQL 的增量数据到 TiDB，详细信息可参考[使用 DM 工具从 Amazon Aurora MySQL 迁移](https://docs.pingcap.com/zh/tidb-data-migration/v2.0/migrate-from-mysql-aurora)

### 大于 1 TiB 的全量数据迁移

#### 适合场景

使用 Dumpling 和 TiDB Lightning 迁移全量数据，适合 MySQL 全量数据的大小大于 1 TiB 的场景。该方案只能迁移全量数据，如果需要继续同步增量数据，需要再使用 TiDB Data Migration (DM) 创建增量同步任务。

#### 迁移方法

使用 Dumpling 导出 MySQL 的全量数据，再使用 TiDB Lightning 将全量数据导入到 TiDB，详细信息可参考[使用 Dumpling 与 TiDB Lightning 进行全量迁移](/migrate-from-mysql-dumpling-files.md)。

## 从 MySQL 分库分表合并迁移到 TiDB

目前可以使用以下两种方式将 MySQL 数据全量迁移到 TiDB。

- [使用 DM 将 MySQL 分库分表（1 TiB以内）合并迁移到 TiDB](/migrate-shard-tables-within-1tb.md)
- [使用 Dumpling 和 TiDB Lightning 将分库分表合并导入到 TiDB（大于 1 TiB）](/migrate-from-mysql-shard-merge-using-lightning.md)

### 将 1 TiB 以内的 MySQL 分库分表合并导入到 TiDB 

#### 适合场景

适合 MySQL 全量数据小于 1 TiB、分表合并迁移的场景。该方案只能迁移全量数据，如果需要继续同步增量数据，需要再使用 TiDB Data Migration (DM) 创建增量同步任务。

#### 迁移方法

直接使用 DM 将各 MySQL 分库分表数据合并导入到 TiDB，详细信息可参考[将 MySQL 分库分表(1 TiB以内)合并迁移到 TiDB](/migrate-shard-tables-within-1tb.md)  。

### 将大量数据（大于 1 TiB）分库分表合并导入到 TiDB 

#### 适合场景

适合 MySQL 全量数据大于 1 TiB、分表合并迁移的场景。该方案只能迁移全量数据，如果需要继续同步增量数据，需要再使用 TiDB Data Migration (DM) 创建增量同步任务。

#### 迁移方法

使用 Dumpling 从多个 MySQL 数据库中导出数据，再使用 TiDB Lightning 将各分库分表数据合并导入到 TiDB，详细信息可参考[分库分表合并导入到 TiDB （大于 1 TiB）](/migrate-from-mysql-shard-merge-using-lightning.md)。

## 从文件迁移到 TiDB

支持通过 CSV 和 SQL 两种格式文件将数据迁移到 TiDB。

### 从 CSV 文件迁移到 TiDB

#### 适合场景

适合将不兼容 MySQL 协议的异构数据库的数据迁移到 TiDB。

#### 迁移方法

将全量数据导出到 CSV 格式的文件中，将 CSV 文件导入到 TiDB 有以下两种方法：

- 使用 TiDB Lightning 将 CSV 格式的数据导入到 TiDB
  
    TiDB Lightning 导入速度快，适合 CSV 文件数据量较大的场景。详细信息可参考[从 CSV 文件迁移至 TiDB](/tidb-lightning/migrate-from-csv-using-tidb-lightning.md)。

- 使用 `LOAD DATA` 语句将 CSV 格式的数据导入到 TiDB

    在 TiDB 中执行 `LOAD DATA` SQL 语句导入 CSV 格式的数据，这种导入方法使用比较方便，但是如果在导入过程中出现错误或者中断，需要人工介入，检查数据的一致性和完整性，因此不建议在生产环境中使用。详细信息可参考 [LOAD DATA](/sql-statements/sql-statement-load-data.md)。

### 从 SQL 文件迁移到 TiDB

该部分内容与[使用 Dumpling 和 TiDB Lightning 迁移全量数据](#使用-dumpling-和-tidb-lightning-迁移全量数据)相同。
