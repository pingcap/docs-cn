---
title: TiCDC 简介
category: reference
aliases: ['/docs-cn/dev/reference/tools/ticdc/overview/']
---

# TiCDC 简介

> **注意：**
>
> TiCDC 目前为实验特性，不建议在生产环境中使用。

[TiCDC](https://github.com/pingcap/ticdc) 是一款通过拉取 TiKV 变更日志实现的 TiDB 增量数据同步工具，具有将数据还原到与上游任意 TSO 一致状态的能力，同时提供[开放数据协议](/ticdc/ticdc-open-protocol.md) (TiCDC Open Protocol)，支持其他系统订阅数据变更。

## TiCDC 架构

TiCDC 运行时是一种无状态节点，通过 PD 内部的 etcd 实现高可用。TiCDC 集群支持创建多个同步任务，向多个不同的下游进行数据同步。

TiCDC 的系统架构如下图所示：

![TiCDC architecture](/media/cdc-architecture.png)

### 系统角色

- TiKV CDC 组件：只输出 key-value (KV) change log。
    - 内部逻辑拼装 KV change log。
    - 提供输出 KV change log 的接口，发送数据包括实时 change log 和增量扫的 change log。

- `capture`：TiCDC 运行进程，多个 `capture` 组成一个 TiCDC 集群，负责 KV change log 的同步。
    - 每个 `capture` 负责拉取一部分 KV change log。
    - 对拉取的一个或多个 KV change log 进行排序。
    - 向下游还原事务或按照 TiCDC Open Protocol 进行输出。

## 同步功能介绍

本部分介绍 TiCDC 的同步功能。

### sink 支持

目前 TiCDC sink 模块支持同步数据到以下下游：

- MySQL 协议兼容的数据库，提供最终一致性支持。
- 以 TiCDC Open Protocol 输出到 Kafka，可实现行级别有序、最终一致性或严格事务一致性三种一致性保证。

### 同步顺序保证和一致性保证

#### 数据同步顺序

- TiCDC 对于所有的 DDL/DML 都能对外输出**至少一次**。
- TiCDC 在 TiKV/TiCDC 集群故障期间可能会重复发相同的 DDL/DML。对于重复的 DDL/DML：
    - MySQL sink 可以重复执行 DDL，对于在下游可重入的 DDL （譬如 truncate table）直接执行成功；对于在下游不可重入的 DDL（譬如 create table），执行失败，TiCDC 会忽略错误继续同步。
    - Kafka sink 会发送重复的消息，但重复消息不会破坏 Resolved Ts 的约束，用户可以在 Kafka 消费端进行过滤。

#### 数据同步一致性

- MySQL sink

    - TiCDC 不拆分表内事务，**保证**单表事务一致性，但**不保证**上游表内事务的顺序一致。
    - TiCDC 以表为单位拆分跨表事务，**不保证**跨表的事务始终一致。
    - TiCDC **保证**单行的更新与上游更新顺序一致。

- Kafka sink

    - TiCDC 提供不同的数据分发策略，可以按照表、主键或 ts 等策略分发数据到不同 Kafka partition。
    - 不同分发策略下 consumer 的不同实现方式，可以实现不同级别的一致性，包括行级别有序、最终一致性或跨表事务一致性。
    - TiCDC 没有提供 Kafka 消费端实现，只提供了 [TiCDC 开放数据协议](/ticdc/ticdc-open-protocol.md)，用户可以依据该协议实现 Kafka 数据的消费端。

## 同步限制

将数据同步到 TiDB 或 MySQL，需要满足以下条件才能保证正确性：

- 表必须要有主键或者唯一索引。
- 如果表只存在唯一索引，至少有一个唯一索引的每一列在表结构中明确定义 `NOT NULL`。

### 暂不支持的场景

目前 TiCDC（4.0 发布版本）暂不支持的场景如下：

- 暂不支持单独使用 RawKV 的 TiKV 集群。
- 暂不支持 TiDB 4.0 [新的 Collation 框架](/character-set-and-collation.md#新框架下的-collation-支持)。如果开启该功能，需保证下游集群为 TiDB 并使用与上游相同的 collation，否则会出现 collation 导致的无法定位数据的问题。
- 暂不支持 TiDB 4.0 中[创建 SEQUENCE 的 DDL 操作](/sql-statements/sql-statement-create-sequence.md) 和 [SEQUENCE 函数](/sql-statements/sql-statement-create-sequence.md#sequence-函数)。在上游 TiDB 使用 SEQUENCE 时，TiCDC 将会忽略掉上游执行的 SEQUENCE DDL 操作/函数，但是使用 SEQUENCE 函数的 DML 操作可以正确地同步。
- 暂不支持 [TiKV Hibernate Region](https://github.com/tikv/tikv/blob/master/docs/reference/configuration/raftstore-config.md#hibernate-region)。TiCDC 会使 Region 无法进入静默状态。
- TiCDC 集群扩容后，不支持将已有的同步表调度到新的 TiCDC 节点中。
- 暂不支持库表同步黑白名单。

## TiCDC 部署和任务管理

TiCDC 的详细部署和任务管理说明请参考 [TiCDC 运维操作及任务管理](/ticdc/manage-ticdc.md)。

## TiCDC 常见问题

在使用 TiCDC 过程中经常遇到的问题以及相对应的解决方案请参考 [TiCDC 常见问题](/ticdc/troubleshoot-ticdc.md)。

## TiCDC 开放数据协议

TiCDC Open Protocol 是一种行级别的数据变更通知协议，为监控、缓存、全文索引、分析引擎、异构数据库的主从复制等提供数据源。TiCDC 遵循 TiCDC Open Protocol，向 MQ (Message Queue) 等第三方数据媒介复制 TiDB 的数据变更。详细信息参考 [TiCDC 开放数据协议](/ticdc/ticdc-open-protocol.md)。
