---
title: TiDB 工具的使用场景
summary: 本文档介绍 TiDB 工具的常见使用场景与工具选择。
aliases: ['/docs-cn/dev/ecosystem-tool-user-case/']
---

# TiDB 工具的使用场景

本文档从数据迁移工具的使用场景出发，介绍部分常见场景下的迁移工具的选择。

## 在物理机或虚拟机上部署运维 TiDB

当需要在物理机或虚拟机上部署运维 TiDB 时，你可以先安装 [TiUP](/tiup/tiup-overview.md)，再通过 TiUP 管理 TiDB 的众多组件，如 TiDB、PD、TiKV 等。

## 在 Kubernetes 上部署运维 TiDB

当需要在 Kubernetes 上部署运维 TiDB 时，你可以先创建 Kubernetes 集群，部署[TiDB Operator](https://docs.pingcap.com/zh/tidb-in-kubernetes/stable)，然后使用 TiDB Operator 部署运维 TiDB 集群。

## 从 CSV 导入数据到 TiDB

当需要将其他工具导出的格式兼容的 CSV files 导入到 TiDB 时，可使用 [TiDB Lightning](/tidb-lightning/tidb-lightning-overview.md)。

## 从 MySQL/Aurora 导入全量数据

当需要从 MySQL/Aurora 导入全量数据时，可先使用 [Dumpling](/dumpling-overview.md) 将数据导出为 SQL dump files，然后再使用 [TiDB Lightning](/tidb-lightning/tidb-lightning-overview.md) 将数据导入到 TiDB 集群。

## 从 MySQL/Aurora 迁移数据

当既需要从 MySQL/Aurora 导入全量数据，又需要迁移增量数据时，可使用 [TiDB Data Migration (DM)](/dm/dm-overview.md) 完成[从 Amazon Aurora 迁移数据到 TiDB](/migrate-aurora-to-tidb.md)。

如果全量数据量较大（TB 级别），则可先使用 [Dumpling](/dumpling-overview.md) 与 [TiDB Lightning](/tidb-lightning/tidb-lightning-overview.md) 完成全量数据的迁移，再使用 DM 完成增量数据的迁移。

## TiDB 集群备份与恢复

当需要对 TiDB 集群进行备份或在之后对 TiDB 集群进行恢复时，可使用 [BR](/br/backup-and-restore-overview.md)。

## 迁出数据到 TiDB

当需要将 TiDB 集群的数据迁出到其他 TiDB 集群时，可使用 [Dumpling](/dumpling-overview.md) 从 TiDB 将全量数据导出为 SQL dump files，然后再使用 [TiDB Lightning](/tidb-lightning/tidb-lightning-overview.md) 将数据导入到 TiDB。

如果还需要执行增量数据的迁移，则可使用 [TiCDC](/ticdc/ticdc-overview.md)。

## TiDB 增量数据订阅

当需要订阅 TiDB 增量数据的变更时，可使用 [TiCDC](/ticdc/ticdc-overview.md)。
