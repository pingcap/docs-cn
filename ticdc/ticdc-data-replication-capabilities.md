---
title: TiCDC 数据同步能力详解
summary: 了解 TiCDC 的数据同步能力。
---

# TiCDC 数据同步能力详解

[TiCDC](/ticdc/ticdc-overview.md) (TiDB Change Data Capture) 是 TiDB 生态中用于​​实时数据同步​​的核心组件。本文详细解释 TiCDC 的数据同步能力。

## 工作原理​

- TiCDC 监听 TiKV 的变更日志 (Raft Log)，将行数据的增删改操作转换为下游兼容的 SQL 语句，并不基于上游的 SQL 获取数据变更。详情请参考 [TiCDC 处理数据变更的实现原理](/ticdc/ticdc-overview.md#ticdc-处理数据变更的实现原理)。

- TiCDC 生成与 SQL 语义等效的逻辑操作（如 `INSERT`、`UPDATE`、`DELETE`），而非逐条还原上游执行的原始 SQL 语句。详情请参考 [TiCDC 处理数据变更的实现原理](/ticdc/ticdc-overview.md#ticdc-处理数据变更的实现原理)。

- TiCDC 提供事务最终一致性的保证。开启 [redo log](/ticdc/ticdc-sink-to-mysql.md#灾难场景的最终一致性复制) 后，TiCDC 可以保证容灾场景下的最终一致性；开启 [Syncpoint](/ticdc/ticdc-upstream-downstream-check.md#启用-syncpoint) 后，TiCDC 提供一致性快照读和数据一致性校验。

## 支持的下游

TiCDC 支持同步数据到多类下游，包括：

- [TiDB 及兼容 MySQL 协议的数据库](/ticdc/ticdc-sink-to-mysql.md)
- [Apache Kafka](/ticdc/ticdc-sink-to-kafka.md)
- [Message Queue (MQ) 类的下游](/ticdc/ticdc-changefeed-config.md#sink)，如 [Pulsar](/ticdc/ticdc-sink-to-pulsar.md)
- [存储服务（Amazon S3、GCS、Azure Blob Storage 和 NFS）](/ticdc/ticdc-sink-to-cloud-storage.md)
- [通过 Confluent Cloud 同步至 Snowflake、ksqlDB、SQL Server](/ticdc/integrate-confluent-using-ticdc.md)
- [使用 Apache Flink 消费同步至 Kafka 的数据](/replicate-data-to-kafka.md)

## 数据同步范围

TiCDC 对上游数据变更的支持范围如下：

+ 支持：

    - DDL 和 DML 语句（非系统表）。
    - 索引操作 (`ADD INDEX`, `CREATE INDEX`)：为了减少对 Changefeed 同步延迟的影响，当下游为 TiDB 时，TiCDC 会[异步执行创建和添加索引的 DDL 操作](/ticdc/ticdc-ddl.md#创建和添加索引-ddl-的异步执行)。
    - 外键约束 DDL 语句 (`ADD FOREIGN KEY`)：TiCDC 不会同步上游系统变量的设置，需要在下游手动设置 [`foreign_key_checks`](/system-variables.md#foreign_key_checks) 来决定是否开启下游的外键约束检查。另外，TiCDC 在向下游写入数据时，自动启用会话级别的设置 `SET SESSION foreign_key_checks = OFF;`。因此，即使下游开启了全局外键检查，TiCDC 写入的数据也不会触发外键约束验证。

+ 不支持：

    - 系统表（如 `mysql.*` 和 `information_schema.*`）的 DDL 和 DML 语句。
    - 临时表的 DDL 和 DML 语句。
    - DQL (Data Query Language) 语句和 DCL (Data Control Language) 语句。

## 使用限制

- TiCDC 对一些场景暂不支持，详见[暂不支持的场景](/ticdc/ticdc-overview.md#暂不支持的场景)。
- TiCDC 只检查上游数据变更的完整性，不检查数据变更是否符合上游或下游的约束。如果遇到不满足下游约束的数据变更，TiCDC 会在写入下游时报错。

    例如：当通过 changefeed 配置了过滤所有 DDL 事件后，如果上游执行 `DROP COLUMN` 操作后继续写入涉及该列的 `INSERT` 语句，TiCDC 同步这些 DML 变更到下游时，会因下游表结构不同而导致数据写入失败。

- 对于 TiCDC [老架构](/ticdc/ticdc-classic-architecture.md)，当单个 TiCDC 集群同步的表数量超过以下建议值时，TiCDC 可能无法稳定工作：
  
    |  TiCDC 集群版本 | 同步表的数量建议值 |
    |---|:---:|
    | v5.4.0 - v6.4.x | 2000 |
    | v6.5.x - v7.4.x | 4000 |
    | v7.5.x - v8.5.x | 40000 |

    > **注意:**
    >
    > 如果同步的是分区表，TiCDC 会将每个分区视为一张独立的表，因此在计算同步表的数量时会将分区数量也计算在内。

    如果需要同步的表数量超过以上建议值，建议使用 [TiCDC 新架构](/ticdc/ticdc-architecture.md)。新架构单个 Changefeed 支持同步超过百万张表，适用于大规模同步场景。
