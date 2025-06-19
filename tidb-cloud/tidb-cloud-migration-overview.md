---
title: 数据迁移和导入概览
summary: 了解 TiDB Cloud 的数据迁移和导入场景概览。
aliases: ['/tidbcloud/export-data-from-tidb-cloud']
---

# 数据迁移和导入概览

你可以将数据从各种数据源迁移到 TiDB Cloud。本文档概述了数据迁移的场景。

## 从 MySQL 兼容的数据库迁移数据

当你从 MySQL 兼容的数据库迁移数据时，你可以执行全量数据迁移和增量数据迁移。迁移场景和方法如下：

- 使用数据迁移工具迁移 MySQL 兼容的数据库

    TiDB 与 MySQL 高度兼容。你可以使用 TiDB Cloud 控制台中的数据迁移工具从任何 MySQL 兼容的数据库顺利迁移数据到 TiDB Cloud。更多信息，请参见[使用数据迁移工具将 MySQL 兼容的数据库迁移到 TiDB Cloud](/tidb-cloud/migrate-from-mysql-using-data-migration.md)。

- 使用 AWS DMS 迁移

    如果你想迁移异构数据库（如 PostgreSQL、Oracle 和 SQL Server）到 TiDB Cloud，建议使用 AWS Database Migration Service (AWS DMS)。

    - [使用 AWS DMS 将 MySQL 兼容的数据库迁移到 TiDB Cloud](/tidb-cloud/migrate-from-mysql-using-aws-dms.md)
    - [使用 AWS DMS 从 Amazon RDS for Oracle 迁移](/tidb-cloud/migrate-from-oracle-using-aws-dms.md)

- 迁移和合并 MySQL 分片

    如果你的应用程序使用 MySQL 分片存储数据，你可以将这些分片作为一个表迁移到 TiDB Cloud。更多信息，请参见[将大数据集的 MySQL 分片迁移和合并到 TiDB Cloud](/tidb-cloud/migrate-sql-shards.md)。

- 从 TiDB 自托管迁移

    你可以通过 Dumpling 和 TiCDC 将数据从 TiDB 自托管集群迁移到 TiDB Cloud (AWS)。更多信息，请参见[从 TiDB 自托管迁移到 TiDB Cloud](/tidb-cloud/migrate-from-op-tidb.md)。

## 从文件导入数据到 TiDB Cloud

如果你有 SQL、CSV、Parquet 或 Aurora 快照格式的数据文件，你可以一次性将这些文件导入到 TiDB Cloud。导入场景和方法如下：

- 将本地 CSV 文件导入到 TiDB Cloud

    你可以将本地 CSV 文件导入到 TiDB Cloud。更多信息，请参见[将本地文件导入到 TiDB Cloud](/tidb-cloud/tidb-cloud-import-local-files.md)。

- 将示例数据（SQL 文件）导入到 TiDB Cloud

    你可以将示例数据（SQL 文件）导入到 TiDB Cloud，以快速熟悉 TiDB Cloud 界面和导入过程。更多信息，请参见[将示例数据导入到 TiDB Cloud Serverless](/tidb-cloud/import-sample-data-serverless.md) 和[将示例数据导入到 TiDB Cloud Dedicated](/tidb-cloud/import-sample-data.md)。

- 从 Amazon S3、Google Cloud Storage (GCS) 或 Azure Blob Storage 将 CSV 文件导入到 TiDB Cloud

    你可以从 Amazon S3、Google Cloud Storage (GCS) 或 Azure Blob Storage 将 CSV 文件导入到 TiDB Cloud。更多信息，请参见[从云存储将 CSV 文件导入到 TiDB Cloud Serverless](/tidb-cloud/import-csv-files-serverless.md) 和[从云存储将 CSV 文件导入到 TiDB Cloud Dedicated](/tidb-cloud/import-csv-files.md)。

- 从 Amazon S3、Google Cloud Storage (GCS) 或 Azure Blob Storage 将 Apache Parquet 文件导入到 TiDB Cloud

    你可以从 Amazon S3、Google Cloud Storage (GCS) 或 Azure Blob Storage 将 Parquet 文件导入到 TiDB Cloud。更多信息，请参见[从云存储将 Apache Parquet 文件导入到 TiDB Cloud Serverless](/tidb-cloud/import-parquet-files-serverless.md) 和[从云存储将 Apache Parquet 文件导入到 TiDB Cloud Dedicated](/tidb-cloud/import-parquet-files.md)。

## 参考

### 配置云存储访问

如果你的源数据存储在 Amazon S3、Google Cloud Storage (GCS) 存储桶或 Azure Blob Storage 容器中，在将数据导入或迁移到 TiDB Cloud 之前，你需要配置对存储的访问。更多信息，请参见[为 TiDB Cloud Serverless 配置外部存储访问](/tidb-cloud/serverless-external-storage.md) 和[为 TiDB Cloud Dedicated 配置外部存储访问](/tidb-cloud/dedicated-external-storage.md)。

### 数据导入的命名规范

为确保你的数据能够成功导入，你需要准备符合命名规范的架构文件和数据文件。更多信息，请参见[数据导入的命名规范](/tidb-cloud/naming-conventions-for-data-import.md)。

### 排查从 Amazon S3 导入数据时的访问被拒绝错误

你可以排查从 Amazon S3 导入数据到 TiDB Cloud 时可能出现的访问被拒绝错误。更多信息，请参见[排查从 Amazon S3 导入数据时的访问被拒绝错误](/tidb-cloud/troubleshoot-import-access-denied-error.md)。
