---
title: 数据迁移场景综述
summary: This document describes how to migrate data from databases or data formats (CSV/SQL).
aliases: ['/docs/dev/migration-overview/']
---

# 数据迁移场景综述

这篇文章描述如何迁移数据到 TiDB。TiDB 提供了下面几种数据迁移功能

- 全量数据迁移：使用 TiDB Lightning 将 平面文件/Aurora Snapshot/mydumper sql file 数据导入到 TiDB 集群；为了更好的配合从 MySQL/MariaDB 数据库进行全量迁移，TiDB 也提供了数据导出工具 Dumpling，支持将全量数据导出成 平面文件/mydumper sql 文件。

- 快速初始化 TiDB 集群：TiDB Lightning 还提供的快速导入功能，可以实现快速初始化 TiDB 集群的指定表的效果，使用该功能前需要了解，快速导入期间对 TiDB 集群影响极大，集群不适合对外提供访问；

- 增量数据迁移：使用 TiDB DM 从 MySQL/MariaDB/Aurora 同步 Binlog 到 TiDB，该功能可以极大降低业务迁移过程中停机窗口时间；此外 DM 提供了适合小规模数据量数据库（< 1T）的全量数据迁移功能；

- TiDB 集群复制：TiDB 支持备份恢复功能，该功能可以实现将 TiDB 的某个快照初始化到另一个全新的 TiDB 集群。

根据迁移数据所在数据库类型、部署位置、业务数据规模大小、业务需求等因素，会有不同数据迁移选择。下面展示一些常用的数据迁移场景，方便用户依据这些线索选择到最适合自己的数据迁移方案。

## 迁移 Aurora MySQL 到 TiDB

从 Aurora 迁移数据到部署在 AWS 的 TiDB 集群，数据迁移可以分为全量迁移和增量迁移两个步骤进行。请根据你的业务需求选择相应的步骤。

- [从 Aurora 迁移数据到 TiDB](/data-migration/migrate-aurora-tidb-from-snapshot.md)

## 迁移 MySQL 到 TiDB

没有 Cloud storage（S3）服务，网络联通和延迟情况良好，从 MySQL 迁移数据到 TiDB 可以考虑参照下面的便捷方案。

- [从 TiB 级以下 MySQL 迁移数据到 TiDB](/data-migration/migrate-mysql-tidb-less-tb.md)

如果你对数据迁移速度有要求，或者数据规模特别大（例如 TiB 级以上），并且允许 TiDB 集群在迁移期间禁止其他业务写入，那么你可以先使用 Lightning 进行快速导入，然后根据业务需要选择是否使用 DM 进行增量数据（Binlog）同步

- [从 TiB 级以上 MySQL 迁移数据到 TiDB](/data-migration/migrate-mysql-tidb-above-tb.md)

## 分库分表 MySQL 合并迁移到 TiDB

如果你的业务使用了基于 MySQL 分库的方案来存储数据，业务数据从 MySQL 迁移到 TiDB 后合并这些分表数据到一张合并，你可以使用 DM 进行分表合并迁移

- [TiB 级以下分库分表 MySQL 合并迁移数据到 TiDB](/data-migration/migrate-shared-mysql-tidb-less-tb.md)

如果分表数据总规模特别大（例如 TiB 级以上），并且允许 TiDB 集群在迁移期间禁止其他业务写入，那么你可以使用 Lightning 对分表数据进行快速合并导入，然后根据业务需要选择是否使用 DM 进行增量数据（Binlog）的分表同步

- [TiB 级以上分库分表 MySQL 合并迁移数据到 TiDB](/data-migration/migrate-shared-mysql-tidb-above-tb.md)

## 从文件迁移数据到 TiDB

- [从平面文件迁移数据到 TiDB](/data-migration/migrate-flat-file-tidb.md)
- [从 SQL 文件迁移数据到 TiDB](//data-migration/migrate-sql-file-tidb.md)

## 更加复杂的迁移方式

DM 在实时同步过程中，多个已有特性可以使得同步过程更加灵活，适应各类业务需求：

- [上游使用 pt/gh-ost 工具的持续同步场景](/data-migration/migrate-with-pt-ghost.md)
- [如何过滤 binlog 事件](/data-migration/migrate-with-binlog-event-filter.md)
- [如何通过 SQL 表达式过滤 binlog](/data-migration/migrate-with-binlog-sql-expression-filter.md)
- [下游存在更多列的迁移场景](//data-migration/migrate-with-more-columns-downstream.md)
