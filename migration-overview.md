---
title: 数据迁移概述
summary: 了解各种数据迁移场景和对应的数据迁移方案。
---

# 数据迁移概述

本文档总体介绍可用于 TiDB 的数据迁移方案。数据迁移方案如下：

- 全量数据迁移。
    - 数据导入：使用 TiDB Lightning 将 Aurora Snapshot，CSV 文件或 SQL dump 文件的数据全量导入到 TiDB 集群。
    - 数据导出：使用 Dumpling 将 TiDB 集群的数据全量导出为 CSV 文件或 SQL dump 文件，从而更好地配合从 MySQL 数据库或 MariaDB 数据库进行数据迁移。
    - TiDB DM (Data migration) 也提供了适合小规模数据量数据库（例如小于 1 TiB）的全量数据迁移功能。

- 快速初始化 TiDB 集群：TiDB Lightning 提供的快速导入功能可以实现快速初始化 TiDB 集群的指定表的效果。请注意，使用快速初始化 TiDB 集群的功能对 TiDB 集群的影响极大，在进行初始化的过程中，TiDB 集群不支持对外访问。

- 增量数据迁移：使用 TiDB DM 从 MySQL，MariaDB 或 Aurora 同步 Binlog 到 TiDB，该功能可以极大降低业务迁移过程中停机窗口时间。

- TiDB 集群复制：TiDB 支持备份恢复功能，该功能可以实现将 TiDB 的某个快照初始化到另一个全新的 TiDB 集群。

- TiDB 集群增量数据同步：TiCDC 支持同构数据库之间的灾备场景，能够在灾难发生时保证主备集群数据的最终一致性。目前该场景仅支持 TiDB 作为主备集群。

根据迁移数据所在数据库类型、部署位置、业务数据规模大小、业务需求等因素，会有不同数据迁移选择。下面展示一些常用的数据迁移场景，方便用户依据这些线索选择到最适合自己的数据迁移方案。

## 迁移 Aurora MySQL 到 TiDB

从 Aurora 迁移数据到部署在 AWS 的 TiDB 集群，数据迁移可以分为全量迁移和增量迁移两个步骤进行。请根据你的业务需求选择相应的步骤。

- [从 Aurora 迁移数据到 TiDB](/migrate-aurora-to-tidb.md)

## 迁移 MySQL 到 TiDB

如果你没有使用 Cloud storage (S3) 服务，而且网络联通和延迟情况良好，那么从 MySQL 迁移数据到 TiDB 时可以参照下面的方案。

- [从小数据量 MySQL 迁移数据到 TiDB](/migrate-small-mysql-to-tidb.md)

如果你对数据迁移速度有要求，或者数据规模特别大（例如大于 1 TiB），并且禁止 TiDB 集群在迁移期间有其他业务写入，那么你可以先使用 Lightning 进行快速导入，然后根据业务需要选择是否使用 DM 进行增量数据 (Binlog) 同步。

- [从大数据量 MySQL 迁移数据到 TiDB](/migrate-large-mysql-to-tidb.md)

## 分库分表 MySQL 合并迁移到 TiDB

如果你的业务使用了基于 MySQL 分库的方案来存储数据，业务数据从 MySQL 迁移到 TiDB 后，合并这些分表数据到一张合并，那么你可以使用 DM 进行分表合并迁移。

- [从小数据量分库分表 MySQL 合并迁移数据到 TiDB](/migrate-small-mysql-shards-to-tidb.md)

如果分表数据总规模特别大（例如大于 1 TiB），并且禁止 TiDB 集群在迁移期间有其他业务写入，那么你可以使用 Lightning 对分表数据进行快速合并导入，然后根据业务需要选择是否使用 DM 进行增量数据 (Binlog) 的分表同步。

- [从大数据量分库分表 MySQL 合并迁移数据到 TiDB](/migrate-large-mysql-shards-to-tidb.md)

### 将数据从 Vitess 迁移到 TiDB

将数据从 Vitess 迁移到 TiDB，可参考以下文档：

- [从 Vitess 迁移数据到 TiDB](/migrate-from-vitess.md)

## 从文件迁移数据到 TiDB

- [从 CSV 文件迁移数据到 TiDB](/migrate-from-csv-files-to-tidb.md)
- [从 SQL 文件迁移数据到 TiDB](/migrate-from-sql-files-to-tidb.md)
- [从 Parquet 文件迁移数据到 TiDB](/migrate-from-parquet-files-to-tidb.md)

## TiDB 集群增量数据同步

可以使用 TiCDC 进行 TiDB 集群间的增量数据同步。详情请参考 [TiCDC 简介](/ticdc/ticdc-overview.md)。

## 复杂迁移场景

DM 在实时同步过程中，多个已有特性可以使得同步过程更加灵活，适应各类业务需求：

- [上游使用 pt/gh-ost 工具的持续同步场景](/migrate-with-pt-ghost.md)
- [下游存在更多列的迁移场景](/migrate-with-more-columns-downstream.md)
- [如何过滤 binlog 事件](/filter-binlog-event.md)
- [如何通过 SQL 表达式过滤 binlog](/filter-dml-event.md)