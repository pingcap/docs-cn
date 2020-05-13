---
title: TiCDC 简介
category: reference
aliases: ['/docs-cn/dev/reference/tools/ticdc/overview/']
---

# TiCDC 简介

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

### 库表同步黑白名单

用户可以通过编写黑白名单过滤规则，来过滤或只同步某些数据库或某些表的所有变更数据。过滤规则类似于 MySQL `replication-rules-db` 或 `replication-rules-table`。

## 同步限制

将数据同步到 TiDB 或 MySQL，需要满足以下条件才能保证正确性：

- 表必须要有主键或者唯一索引。
- 如果表只存在唯一索引，至少有一个唯一索引的每一列在表结构中明确定义 `NOT NULL`。

### 暂不支持的场景

目前 TiCDC（4.0 发布版本）与部分 TiDB 特性存在冲突，在后续的 TiCDC 版本上会逐渐修复。当前版本需要做相应的兼容性处理。暂不支持的场景如下：

- 暂不支持同步分区表。
- 暂不支持 TiDB 4.0 [新的 Collation 框架](/character-set-and-collation.md#新框架下的-collation-支持)。如果开启该功能，需保证下游集群为 TiDB 并使用与上游相同的 collation，否则会出现 collation 导致的无法定位数据的问题。
- 暂不支持 [TiKV Hibernate Region](https://github.com/tikv/tikv/blob/master/docs/reference/configuration/raftstore-config.md#hibernate-region)。TiCDC 会使 Region 无法进入静默状态。
