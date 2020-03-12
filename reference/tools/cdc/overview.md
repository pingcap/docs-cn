---
title: TiCDC 简介
category: reference
---

# TiCDC 简介

[TiCDC](https://github.com/pingcap/ticdc) CDC 是一款通过拉取 TiKV 变更日志实现的 TiDB 增量数据同步工具。具有还原数据到与上游任意 TSO 一致状态的能力，同时提供开放数据协议，支持其他系统订阅数据变更。

## TiCDC 架构

CDC 运行时是一种无状态节点，通过 PD 内部的 etcd 实现高可用。CDC 集群支持创建多个同步任务，向多个不同的下游进行数据同步。CDC 的系统架构如下图所示：

![TiCDC architecture](/media/cdc-architecture.png)


### 系统角色

- TiKV CDC component: 只输出 kv change log

    - 内部逻辑拼装 kv change log
    - 提供输出 kv change log 的接口，发送数据包括实时 change log 和增量扫的 change log

- Capture: CDC 运行进程，多个 capture 组成一个 CDC 集群，负责 kv change log 的同步

    - 每个 capture 负责一部分的 kv change log 拉取
    - 对拉取的一个或多个 kv change log 进行排序
    - 向下游还原事务或按照 TiCDC open protocol 进行输出


## 同步功能介绍


### sink 支持

目前 TiCDC sink 模块支持同步数据到以下下游

- MySQL 协议兼容的数据库，提供最终一致性支持
- 以 TiCDC open protocol 输出到 Kafka，可实现行级别有序、最终一致性或严格事务一致性三种一致性保证

### 库表同步黑白名单

用户可以通过编写黑白名单过滤规则，来过滤或只同步某些数据库或某些表的所有变更数据。过滤规则类似于 MySQL replication-rules-db/replication-rules-table。

## 使用限制

同步到 TiDB/MySQL，需要满足以下条件才可以保证正确性

- 表必须要有主键或者唯一索引
- 如果只存在唯一索引，至少有一个唯一索引的每一列在表结构中明确定义 NOT NULL
