---
title: TiDB 生态工具适用场景
summary: 本文档介绍 TiDB 生态工具的常见适用场景与工具选择。
aliases: ['/docs-cn/dev/ecosystem-tool-user-case/']
---

# TiDB 生态工具适用场景

本文档从生态工具的适用场景出发，介绍部分常见场景下的生态工具选择。

## 从 CSV 导入数据到 TiDB

当需要将其他工具导出的格式兼容的 CSV files 导入到 TiDB 时，可使用 [TiDB Lightning](/tidb-lightning/migrate-from-csv-using-tidb-lightning.md)。

## 从 MySQL/Aurora 导入全量数据

当需要从 MySQL/Aurora 导入全量数据时，可先使用 [Dumpling](/dumpling-overview.md) 将数据导出为 SQL dump files，然后再使用 [TiDB Lightning](/tidb-lightning/tidb-lightning-overview.md) 将数据导入到 TiDB 集群。

## 从 MySQL/Aurora 迁移数据

当既需要从 MySQL/Aurora 导入全量数据，又需要迁移增量数据时，可使用 [TiDB Data Migration (DM)](https://docs.pingcap.com/zh/tidb-data-migration/v2.0/overview) 完成[全量数据和增量数据的迁移](https://docs.pingcap.com/zh/tidb-data-migration/v2.0/migrate-from-mysql-aurora)。

如果全量数据量较大（TB 级别），则可先使用 [Dumpling](/dumpling-overview.md) 与 [TiDB Lightning](/tidb-lightning/tidb-lightning-overview.md) 完成全量数据的迁移，再使用 DM 完成增量数据的迁移。

## TiDB 集群备份与恢复

当需要对 TiDB 集群进行备份或在之后对 TiDB 集群进行恢复时，可使用 [BR](/br/backup-and-restore-tool.md)。

另外，BR 也可以对 TiDB 的数据进行[增量备份](/br/use-br-command-line-tool.md#增量备份)和[增量恢复](/br/use-br-command-line-tool.md#增量恢复)。

## 迁出数据到 TiDB

当需要将 TiDB 集群的数据迁出到其他 TiDB 集群时，可使用 [Dumpling](/dumpling-overview.md) 从 TiDB 将全量数据导出为 SQL dump files，然后再使用 [TiDB Lightning](/tidb-lightning/tidb-lightning-overview.md) 将数据导入到 TiDB。

如果还需要执行增量数据的迁移，则可使用 [TiDB Binlog](/tidb-binlog/tidb-binlog-overview.md)。

## TiDB 增量数据订阅

当需要订阅 TiDB 增量数据的变更时，可使用 [TiDB Binlog](/tidb-binlog/binlog-consumer-client.md)。
