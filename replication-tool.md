---
title: 数据集成工具
summary: 了解数据集成工具 TiCDC 的原理、架构和功能。
---

# 数据集成工具

[TiCDC](https://github.com/pingcap/tiflow/tree/master/cdc) 是一款 TiDB 增量数据复制工具，通过拉取上游 TiKV 的数据变更日志，TiCDC 可以将数据解析为有序的行级变更数据输出到下游。

## TiCDC 适用场景

- 数据库灾备：TiCDC 可以用于同构数据库之间的灾备场景，能够在灾难发生时保证主备集群数据的最终一致性，目前该场景仅支持 TiDB 作为主备集群。
- 数据集成：TiCDC 提供 [TiCDC Canal-JSON Protocol](/ticdc/ticdc-canal-json.md)、[AVRO](/ticdc/ticdc-avro-protocol.md)，支持其他系统订阅数据变更，能够为监控、缓存、全文索引、数据分析、异构数据库的主从复制等场景提供数据源。

## TiCDC 架构

TiCDC 运行时是一种无状态节点，通过 PD 内部的 etcd 实现高可用。TiCDC 集群支持创建多个同步任务，向多个不同的下游进行数据同步。

TiCDC 的系统架构如下图所示：

![TiCDC architecture](/media/ticdc/cdc-architecture.png)

## 同步功能介绍

本部分介绍 TiCDC 的同步功能。

### sink 支持

目前 TiCDC sink 模块支持同步数据到以下下游：

- MySQL 协议兼容的数据库，提供最终一致性支持。
- 以 [TiCDC Canal-JSON Protocol](/ticdc/ticdc-canal-json.md)、[AVRO](/ticdc/ticdc-avro-protocol.md) 格式输出到 Apache Kafka 或 Confluent。

### 同步顺序保证和一致性保证

#### 数据同步顺序

- TiCDC 对于所有的 DDL/DML 都能对外输出**至少一次**。
- TiCDC 在 TiKV/TiCDC 集群故障期间可能会重复发相同的 DDL/DML。对于重复的 DDL/DML：
    - MySQL sink 可以重复执行 DDL，对于在下游可重入的 DDL （譬如 truncate table）直接执行成功；对于在下游不可重入的 DDL（譬如 create table），执行失败，TiCDC 会忽略错误继续同步。
    - Kafka sink 可能会发送重复的消息，对于大多数场景，这不会引发正确性问题。对重复消息敏感的业务，用户可以在 Kafka 消费端进行过滤。

#### 数据同步一致性

- MySQL sink

    - TiCDC 不拆分单表事务，**保证**单表事务的原子性。
    - TiCDC **不保证**下游事务的执行顺序和上游完全一致。
    - TiCDC 以表为单位拆分跨表事务，**不保证**跨表事务的原子性。
    - TiCDC **保证**单行的更新与上游更新顺序一致。

- Kafka sink

    - TiCDC 提供不同的数据分发策略，可以按照表、主键或 ts 等策略分发数据到不同 Kafka partition。
    - 不同分发策略下 consumer 的不同实现方式，可以实现不同级别的一致性，包括行级别有序、最终一致性或跨表事务一致性。

## TiCDC 使用限制

参考 [TiCDC 使用限制](/ticdc/ticdc-overview.md#同步限制)和 [TiCDC 兼容性问题](/ticdc/ticdc-overview.md#兼容性问题)。

## 探索更多

- [TiCDC 常见问题](/ticdc/troubleshoot-ticdc.md)
- [TiCDC 故障处理](/ticdc/troubleshoot-ticdc.md)