---
title: 支持的迁移路径
summary: 本文档介绍支持哪些路径将数据迁移到 TiDB
category: reference
---

# 支持的迁移路径

本文档介绍支持哪些路径将数据迁移到 TiDB。

## 从 MySQL 迁移到 TiDB

### 使用 Mydumper 和 TiDB Lightning 迁移全量数据

可以使用 Mydumper 导出 MySQL 的全量数据，再使用 TiDB Lightning 将全量数据导入到 TiDB，详细信息请参考：[从 Mydumper 文件迁移](/migrate-from-mysql-mydumper-files.md)

### 使用 TiDB DM（Data Migration）迁移数据

TiDB DM 支持将 MySQL 全量数据迁移到 TiDB，并同步 MySQL 的增量数据到 TiDB，详细信息请参考：[使用 DM 工具从 Amazon Aurora MySQL 迁移](/migrate-from-aurora-mysql-database.md)

## 从 CSV 文件迁移到 TiDB

可以使用 TiDB Lightning 将 CSV 格式的数据迁移到 TiDB，详细信息请参考：[从 CSV 文件迁移至 TiDB](/tidb-lightning/migrate-from-csv-using-tidb-lightning.md)