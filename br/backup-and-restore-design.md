---
title: TiDB 备份与恢复功能架构概述
summary: 了解 TiDB 的备份与恢复功能的架构设计。
---

# TiDB 备份与恢复功能架构概述

正如 [TiDB 备份与恢复概述](/br/backup-and-restore-overview.md)所介绍，TiDB 备份恢复功能包含了多种不同类型的集群数据对象的备份与恢复实现。这些功能都以 Backup & Restore (BR) 和 TiDB Operator 为使用入口，创建相应的任务从 TiKV 节点上备份数据，或者恢复数据到 TiKV 节点。

关于各种备份恢复功能的实现架构，请参考以下链接：

- 全量数据备份与恢复

    - [备份集群快照数据](/br/br-snapshot-architecture.md#备份流程)
    - [恢复快照备份数据](/br/br-snapshot-architecture.md#恢复流程)

- 数据变更日志备份

    - [日志备份 - 备份 kv 数据变更](/br/br-log-architecture.md#日志备份)

- Point-in-time recovery (PITR)

    - [恢复到指定时间点](/br/br-log-architecture.md#pitr)
