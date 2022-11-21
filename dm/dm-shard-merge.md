---
title: TiDB Data Migration 分库分表合并
summary: 了解 DM 的分库分表合并功能。
---

# TiDB Data Migration 分库分表合并

TiDB Data Migration (DM) 支持将上游 MySQL/MariaDB 各分库分表中的 DML、DDL 数据合并后迁移到下游 TiDB 的库表中。

如果你需要从小数据量分库分表 MySQL 合并迁移数据到 TiDB，请参考[这篇文档](/migrate-small-mysql-shards-to-tidb.md)

## 使用限制

目前分库分表合并功能仅支持有限的场景，使用该功能前，请仔细阅读[悲观模式分库分表合并迁移使用限制](/dm/feature-shard-merge-pessimistic.md#使用限制)和[乐观模式分库分表合并迁移使用限制](/dm/feature-shard-merge-optimistic.md#使用限制)。

## 参数配置

在任务配置文件中设置：

```yaml
shard-mode: "pessimistic" # 默认值为 "" 即无需协调。如果为分库分表合并任务，请设置为悲观协调模式 "pessimistic"。在深入了解乐观协调模式的原理和使用限制后，也可以设置为乐观协调模式 "optimistic"
```

## 手动处理 Sharding DDL Lock

如果分库分表合并迁移过程中发生了异常，对于部分场景，可尝试参考[手动处理 Sharding DDL Lock](/dm/manually-handling-sharding-ddl-locks.md) 进行处理。
