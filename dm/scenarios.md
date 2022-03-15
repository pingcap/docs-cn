---
title: 应用场景
summary: 了解 TiDB Data Migration 支持的主要应用场景。
aliases: ['/docs-cn/tidb-data-migration/dev/scenarios/']
---

# 应用场景

本文档介绍 TiDB Data Migration (DM) 支持的主要应用场景及相关的使用建议。

## 将 TiDB 作为 MySQL/MariaDB 的从库

将 TiDB 作为上游 MySQL、Aurora、MariaDB 的从库，即将上游实例中的所有数据先以全量形式导入到 TiDB，然后以增量形式实时复制后续变更到 TiDB，则简单按如下规则配置数据迁移任务即可：

- 指定 `task-mode` 为 `all`。
- 配置 `target-database` 为下游 TiDB 相关连接信息。
- 在 `mysql-instances` 中为上游 MySQL/MariaDB 配置对应的 `source-id`。
- 使用默认的并发控制参数或按需配置 `mydumper-thread`、`loader-thread` 与 `syncer-thread`。
- 无需配置 `route-rules`、`filter-rules` 及 `block-allow-list` 等。

### 迁移 MySQL/MariaDB 中部分业务数据

如果原 MySQL/MariaDB 中有多个业务的数据，但暂时只需要迁移其中的部分业务数据到 TiDB，则按照[将 TiDB 作为 MySQL/MariaDB 的从库](#将-tidb-作为-mysqlmariadb-的从库)对迁移任务进行配置后，再按需配置 `block-allow-list` 即可。

如期望上游数据迁移到下游不同名的库或表中，则可额外配置 `route-rules`。

对于一些归档类场景，可能在上游会定期通过 `TRUNCATE TABLE`/`DROP TABLE` 或其他方式清理部分数据，但又期望下游 TiDB 中保留全部的数据，则可额外配置 `filter-rules` 过滤掉相关数据清理操作。

对于此类场景，可参考[从小数据量分库分表 MySQL 合并迁移数据到 TiDB](/migrate-small-mysql-shards-to-tidb.md)。

## 合库合表场景

如果上游 MySQL/MariaDB 中的数据是以分库分表等形式存在的，在迁移到 TiDB 时通常会期望将其进行合并，这时可通过配置 `route-rules` 来将上游数据中的库名、表名等重命名后合并到下游同一个库或表中，具体可参考[从小数据量分库分表 MySQL 合并迁移数据到 TiDB](/migrate-small-mysql-shards-to-tidb.md)以及[分表合并数据迁移最佳实践](/dm/shard-merge-best-practices.md)。

对于 DDL 的迁移，DM 提供了特殊的支持，具体可参考[分库分表合并迁移](/dm/feature-shard-merge.md)。

如只需迁移部分业务数据或过滤部分特定操作，可直接参考前述非合库合表场景中的[迁移 MySQL/MariaDB 中部分业务数据](#迁移-mysqlmariadb-中部分业务数据)。

## online DDL 场景

在 MySQL 生态中，经常会使用 pt-osc 或 gh-ost 等工具执行 online DDL 操作，DM 对此类场景提供了特殊的支持，通过配置 `online-ddl` 参数即可开启。具体可参考 [DM online-ddl](/dm/feature-online-ddl.md)。

## 变更 DM 连接的上游 MySQL 实例

使用 MySQL/MariaDB 时，经常会构建主从集群以提升读取性能，确保数据安全。如果在使用 DM 进行数据迁移过程中，DM-worker 原来连接的上游 MySQL/MariaDB 实例由于某些原因不可用，则需要将 DM-worker 连接到上游主从集群间的另一实例。对于此类场景，DM 提供了较好的支持，但仍有一些限制，具体可以参考 [切换 DM-worker 与上游 MySQL 实例的连接](/dm/usage-scenario-master-slave-switch.md)。
