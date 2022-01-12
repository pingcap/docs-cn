---
title: 使用场景
summary: 了解在不同业务需求场景下如何配置数据迁移任务。
---

# DM 使用场景概述

> **注意：**
>
> 在创建数据迁移任务之前，需要先完成以下操作：
>
> 1. [使用 TiUP 部署 DM 集群](/dm/deploy-a-dm-cluster-using-tiup.md)。
> 2. [创建数据源](/dm/quick-start-create-source.md)。

本文介绍多个业务需求场景下如何完成数据迁移任务。

除了业务需求场景导向的创建数据迁移任务教程之外：

- 完整的数据迁移任务配置示例，请参考 [DM 任务完整配置文件介绍](/dm/task-configuration-file-full.md)
- 数据迁移任务的配置向导，请参考 [数据迁移任务配置向导](/dm/dm-task-configuration-guide.md)

## 从 Amazon Aurora 迁移数据到 TiDB

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

## 从文件迁移数据到 TiDB

- [从 CSV 文件迁移数据到 TiDB](/migrate-from-csv-files-to-tidb.md)
- [从 SQL 文件迁移数据到 TiDB](/migrate-from-sql-files-to-tidb.md)

## 复杂迁移场景

DM 在实时同步过程中，多个已有特性可以使得同步过程更加灵活，适应各类业务需求：

- [上游使用 pt/gh-ost 工具的持续同步场景](/migrate-with-pt-ghost.md)
- [下游存在更多列的迁移场景](/migrate-with-more-columns-downstream.md)
- [如何过滤 binlog 事件](/filter-binlog-event.md)
- [如何通过 SQL 表达式过滤 binlog](/filter-dml-event.md)