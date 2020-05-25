---
title: 支持的迁移路径
summary: 本文档介绍支持哪些路径将数据迁移到 TiDB
category: reference
---

# 支持的迁移路径

本文档介绍支持哪些路径将数据迁移到 TiDB。

## 从 MySQL 迁移到 TiDB

目前推荐使用以下两种方式将 MySQL 数据迁移到 TiDB。

### 使用 Mydumper 和 TiDB Lightning 迁移全量数据

#### 适合场景

适合 MySQL 全量数据的大小大于 1TB 的场景。该方案只能迁移全量数据，如果需要继续同步增量数据，需要再使用 DM 创建增量同步任务。

#### 迁移方法

使用 Mydumper 导出 MySQL 的全量数据，再使用 TiDB Lightning 将全量数据导入到 TiDB，详细信息请参考：[从 Mydumper 文件迁移](/migrate-from-mysql-mydumper-files.md)

### 使用 TiDB DM（Data Migration）迁移数据

#### 适合场景

适合迁移 MySQL 全量数据并同步增量数据的场景，且全量数据的大小小于 1TB。如果全量数据的大小大于 1TB，建议使用 Mydumper 和 TiDB Lightning 导入全量数据后，再使用 DM 同步增量数据。

#### 迁移方法

TiDB DM 支持将 MySQL 全量数据迁移到 TiDB，并同步 MySQL 的增量数据到 TiDB，详细信息请参考：[使用 DM 工具从 Amazon Aurora MySQL 迁移](/migrate-from-aurora-mysql-database.md)

## 从 CSV 文件迁移到 TiDB

### 适合场景

适合将不兼容 MySQL 协议的异构数据库的数据迁移到 TiDB。

### 迁移方法

将全量数据导出到 CSV 格式的文件中，再使用 TiDB Lightning 将 CSV 格式的数据迁移到 TiDB，详细信息请参考：[从 CSV 文件迁移至 TiDB](/tidb-lightning/migrate-from-csv-using-tidb-lightning.md)