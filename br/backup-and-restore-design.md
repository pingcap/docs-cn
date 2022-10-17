---
title: TiDB 备份和恢复功能架构
summary: 了解 TiDB 的备份和恢复功能的架构设计
---

# TiDB 备份和恢复功能架构

正如 [TiDB 备份恢复功能介绍](/br/backup-and-restore-overview.md)，TiDB 备份恢复功能包含了多种不同类型的集群数据对象的备份和恢复实现。它们都以 br、tidb-operator 为使用入口，创建相应的任务从 TiKV 节点上备份数据，或者恢复数据到 TiKV 节点。

下面是各种备份恢复功能的实现架构介绍。

全量数据备份和恢复

- [备份集群快照数据](/br/br-snapshot-architecture.md#备份集群快照数据)
- [恢复快照备份数据](/br/br-snapshot-architecture.md#恢复快照备份数据)

数据变更日志备份

- [日志备份 - 备份 kv 数据变更](/br/br-log-architecture.md#进行日志备份)

PITR（Point in time recovery）

- [恢复到指定时间点](/br/br-log-architecture.md#进行-pitr)
