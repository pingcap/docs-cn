---
title: TiDB 工具适用场景
summary: 本文档介绍 TiDB 工具的常见适用场景与工具选择。
aliases: ['/docs-cn/v3.0/ecosystem-tool-user-case/']
---

# TiDB 工具适用场景

本文档从工具的适用场景出发，介绍部分常见场景下的工具选择。

## 在 Kubernetes 上部署运维 TiDB

当需要在 Kubernetes 上部署运维 TiDB 时，你可以先创建 Kubernetes 集群，部署 [TiDB Operator](https://docs.pingcap.com/zh/tidb-in-kubernetes/stable)，然后使用 TiDB Operator 部署运维 TiDB 集群。

## 从 CSV 导入数据到 TiDB

当需要将其他工具导出的格式兼容的 CSV files 导入到 TiDB 时，可使用 [TiDB Lightning](/tidb-lightning/migrate-from-csv-using-tidb-lightning.md)。

## 从 MySQL/Aurora 导入全量数据

当需要从 MySQL/Aurora 导入全量数据时，可先使用 [Dumpling](/export-or-backup-using-dumpling.md) 将数据导出为 SQL dump files，然后再使用 [TiDB Lightning](/tidb-lightning/tidb-lightning-overview.md) 将数据导入到 TiDB 集群。

## 从 MySQL/Aurora 迁移数据

当既需要从 MySQL/Aurora 导入全量数据，又需要迁移增量数据时，可使用 [TiDB Data Migration (DM)](https://docs.pingcap.com/zh/tidb-data-migration/v2.0/overview) 完成[全量数据和增量数据的迁移](https://docs.pingcap.com/zh/tidb-data-migration/v2.0/migrate-from-mysql-aurora)。

如果全量数据量较大（TB 级别），则可先使用 [Dumpling](/export-or-backup-using-dumpling.md) 与 [TiDB Lightning](/tidb-lightning/tidb-lightning-overview.md) 完成全量数据的迁移，再使用 DM 完成增量数据的迁移。

## TiDB 集群备份与恢复

当需要对 TiDB 集群进行备份时，可使用 [Dumpling](/export-or-backup-using-dumpling.md)。

当需要将备份文件恢复到 TiDB 集群时，可使用 [TiDB Lightning](/tidb-lightning/tidb-lightning-overview.md)。

## 迁出数据到 TiDB

当需要将 TiDB 集群的数据迁出到其他 TiDB 集群时，可使用 [Dumpling](/export-or-backup-using-dumpling.md) 从 TiDB 将全量数据导出为 SQL dump files，然后再使用 [TiDB Lightning](/tidb-lightning/tidb-lightning-overview.md) 将数据导入到 TiDB。

如果还需要执行增量数据的迁移，则可使用 [TiDB Binlog](/tidb-binlog/tidb-binlog-overview.md)。

## TiDB 增量数据订阅

当需要订阅 TiDB 增量数据的变更时，可使用 [TiDB Binlog](/tidb-binlog/binlog-consumer-client.md)。
