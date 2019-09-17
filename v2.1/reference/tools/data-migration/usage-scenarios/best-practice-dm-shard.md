---
title: 分表合并数据迁移最佳实践
summary: 使用 DM 对分库分表进行合并迁移时的最佳实践。
category: reference
---
# 分表合并数据迁移最佳实践

本文目的是阐述在使用 DM 对分库分表进行合并迁移的场景中，DM 相关功能的支持限制，旨在给出一个业务的最佳实践。

## 独立的数据迁移任务

在[分库分表合并同步的实现原理部分](/v2.1/reference/tools/data-migration/features/shard-merge.md#实现原理)，我们介绍了 shard group 的概念，简单来说可以理解为所有需要合并到同一个下游表的所有上游表即组成一个 shard group。

当前的 shard DDL 算法为了能协调在不同分表执行 DDL 对 schema 变更的影响，加入了一些[使用限制](/v2.1/reference/tools/data-migration/features/shard-merge.md#使用限制)。而当这些使用限制由于某些异常原因被打破时，我们需要[手动处理 Sharding DDL Lock](/v2.1/reference/tools/data-migration/features/manually-handling-sharding-ddl-locks.md) 甚至是完整重做整个数据迁移任务。

因此，为了减小异常发生时对数据迁移的影响，我们推荐将每一个 shard group 拆分成一个独立的数据迁移任务。**这样当异常发生时，可能只有少部分迁移任务需要进行手动处理，其他数据迁移任务可以不受影响。**

## 手动处理 shard DDL lock

从[分库分表合并同步的实现原理部分](/v2.1/reference/tools/data-migration/features/shard-merge.md#实现原理)我们可以知道，DM 中的 shard DDL lock 是用于协调不同上游分表向下游执行 DDL 的一种机制，本身并不是异常。

因此，当通过 `show-ddl-locks` 查看到 DM-master 上存在 shard DDL lock 时，或通过 `query-status` 查看到某些 DM-worker 有 `unresolvedGroups` 或 `blockingDDLs` 时，并不要急于使用 `unlock-ddl-lock` 或 `break-ddl-lock` 尝试去手动解除 shard DDL lock。

只有在确认当前未能自动解除 shard DDL lock 是文档中所列的[支持场景](/v2.1/reference/tools/data-migration/features/manually-handling-sharding-ddl-locks.md#支持场景)之一时，才能参照对应支持场景中的手动处理示例进行处理。对于其他未被支持的场景，我们建议完整重做整个数据迁移任务，即清空下游数据库中的数据以及该数据迁移任务相关的 `dm_meta` 信息后，重新执行全量数据及增量数据的迁移。

## 自增主键冲突处理

在 DM 中，我们提供了 [Column mapping](/v2.1/reference/tools/data-migration/features/overview.md#column-mapping) 用于处理 bigint 类型的自增主键在合并时可能出现冲突的问题，但我们**强烈不推荐**使用该功能。如果业务上允许，我们推荐使用以下两种处理方式。

### 去掉自增主键的主键属性

假设上游分表的表结构如下：

```sql
CREATE TABLE `tbl_no_pk` (
  `auto_pk_c1` bigint(20) NOT NULL,
  `uk_c2` bigint(20) NOT NULL,
  `content_c3` text,
  PRIMARY KEY (`auto_pk_c1`),
  UNIQUE KEY `uk_c2` (`uk_c2`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1
```

如果满足下列条件：

- `auto_pk_c1` 列对业务无意义，且不依赖该列的 `PRIMARY KEY` 属性。
- `uk_c2` 列有 `UNIQUE KEY` 属性，且能保证在所有上游分表间全局唯一。

则可以用以下步骤处理合表时可能由 `auto_pk_c1` 导致的 `ERROR 1062 (23000): Duplicate entry '***' for key 'PRIMARY'` 问题：

1. 在开始执行全量数据迁移前，在下游数据库创建用于合表迁移的表，但不为 `auto_pk_c1` 指定 `PRIMARY KEY` 属性。

   ```sql
   CREATE TABLE `tbl_no_pk_2` (
     `auto_pk_c1` bigint(20) NOT NULL,
     `uk_c2` bigint(20) NOT NULL,
     `content_c3` text,
     UNIQUE KEY `uk_c2` (`uk_c2`)
   ) ENGINE=InnoDB DEFAULT CHARSET=latin1
   ```

2. 启动数据迁移任务，执行全量与增量数据迁移。
3. 通过 `query-status` 验证数据迁移任务是否正常，在下游数据库中验证合表中是否已经存在了来自上游的数据。

### 使用联合主键

假设上游分表的表结构如下：

```sql
CREATE TABLE `tbl_multi_pk` (
  `auto_pk_c1` bigint(20) NOT NULL,
  `uuid_c2` bigint(20) NOT NULL,
  `content_c3` text,
  PRIMARY KEY (`auto_pk_c1`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1
```

如果满足下列条件：

* 业务不依赖 `auto_pk_c1` 的 `PRIMARY KEY` 属性。
* `auto_pk_c1` 与 `uuid_c2` 的组合能确保全局唯一。
* 业务能接受将 `auto_pk_c1` 与 `uuid_c2` 组成联合 `PRIMARY KEY`。

则可以用以下步骤处理合表时可能由 `auto_pk_c1` 导致的 `ERROR 1062 (23000): Duplicate entry '***' for key 'PRIMARY'` 问题：

1. 在开始执行全量数据迁移前，在下游数据库创建用于合表迁移的表，但不为 `auto_pk_c1` 指定 `PRIMARY KEY` 属性，而是将 `auto_pk_c1` 与 `uuid_c2` 一起组成 `PRIMARY KEY`。

   ```sql
   CREATE TABLE `tbl_multi_pk_c2` (
     `auto_pk_c1` bigint(20) NOT NULL,
     `uuid_c2` bigint(20) NOT NULL,
     `content_c3` text,
     PRIMARY KEY (`auto_pk_c1`,`uuid_c2`)
   ) ENGINE=InnoDB DEFAULT CHARSET=latin1
   ```

2. 启动数据迁移任务，执行全量与增量数据迁移。

3. 通过 `query-status` 验证数据迁移任务是否正常，在下游数据库中验证合表中是否已经存在了来自上游的数据。

## 合表迁移过程中在上游增/删表

从[分库分表合并同步的实现原理部分](/v2.1/reference/tools/data-migration/features/shard-merge.md#实现原理)我们可以知道，shard DDL lock 的协调依赖于是否已收到上游已有各分表对应的 DDL，且当前 DM 在合表迁移过程中暂时**不支持**在上游动态增加或删除分表。如果需要在合表迁移过程中，对上游执行增、删分表操作，推荐按以下方式进行处理。

### 在上游增加分表

如果需要在上游增加新的分表，推荐按以下顺序执行操作：

1. 等待在上游分表上执行过的所有 shard DDL 协调同步完成。
2. 通过 `stop-task` 停止任务。
3. 在上游添加新的分表。
4. 确保 `task.yaml` 配置能使新添加的分表与其他已有的分表能合并到同一个下游表。
5. 通过 `start-task` 启动任务。
6. 通过 `query-status` 验证数据迁移任务是否正常，在下游数据库中验证合表中是否已经存在了来自上游的数据。

### 在上游删除分表

如果需要在上游删除原有的分表，推荐按以下顺序执行操作：

1. 在上游删除原有的分表，并通过 [`SHOW BINLOG EVENTS`](https://dev.mysql.com/doc/refman/5.7/en/show-binlog-events.html) 获取该 `DROP TABLE` 语句在 binlog 中对应的 `End_log_pos`，记为 _Pos-M_。
2. 通过 `query-status` 获取当前 DM 已经处理完成的 binlog event 对应的 position（`syncerBinlog`），记为 _Pos-S_。
3. 当 _Pos-S_ 比 _Pos-M_ 更大后，则说明 DM 已经处理完 `DROP TABLE` 语句，且该表在被删除前的数据都已经同步到下游，可以进行后续操作；否则，继续等待 DM 进行数据同步。
4. 通过 `stop-task` 停止任务。
5. 确保 `task.yaml` 配置能忽略上游已删除的分表。
6. 通过 `start-task` 启动任务。
7. 通过 `query-status` 验证数据迁移任务是否正常。

## 数据迁移限速/流控

当将多个上游 MySQL/MariaDB 实例的数据合并迁移到下游同一个 TiDB 集群时，由于每个与上游 MySQL/MariaDB 对应的 DM-worker 都会并发地进行全量与增量数据迁移，默认的并发度（全量阶段的 `pool-size` 与增量阶段的 `worker-count`）通过多个 DM-worker 累加后，可能会给下游造成过大的压力，此时应根据 TiDB 监控及 DM 监控进行初步的性能分析后，适当地调整各并发度参数的大小。后续 DM 也将考虑支持部分自动的流控策略。
