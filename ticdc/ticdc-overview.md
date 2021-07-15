---
title: TiCDC 简介
---

# TiCDC 简介

> **注意：**
>
> TiCDC 从 v4.0.6 起成为正式功能，可用于生产环境。

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

    - TiCDC 不拆分单表事务，**保证**单表事务的原子性。 
    - TiCDC **不保证**下游事务的执行顺序和上游完全一致。
    - TiCDC 以表为单位拆分跨表事务，**不保证**跨表事务的原子性。
    - TiCDC **保证**单行的更新与上游更新顺序一致。

- Kafka sink

    - TiCDC 提供不同的数据分发策略，可以按照表、主键或 ts 等策略分发数据到不同 Kafka partition。
    - 不同分发策略下 consumer 的不同实现方式，可以实现不同级别的一致性，包括行级别有序、最终一致性或跨表事务一致性。
    - TiCDC 没有提供 Kafka 消费端实现，只提供了 [TiCDC 开放数据协议](/ticdc/ticdc-open-protocol.md)，用户可以依据该协议实现 Kafka 数据的消费端。

## 同步限制

TiCDC 只能同步至少存在一个**有效索引**的表，**有效索引**的定义如下：

- 主键 (`PRIMARY KEY`) 为有效索引。
- 同时满足下列条件的唯一索引 (`UNIQUE INDEX`) 为有效索引：
    - 索引中每一列在表结构中明确定义非空 (`NOT NULL`)。
    - 索引中不存在虚拟生成列 (`VIRTUAL GENERATED COLUMNS`)。

TiCDC 从 4.0.8 版本开始，可通过修改任务配置来同步**没有有效索引**的表，但在数据一致性的保证上有所减弱。具体使用方法和注意事项参考[同步没有有效索引的表](/ticdc/manage-ticdc.md#同步没有有效索引的表)。

### 暂不支持的场景

目前 TiCDC 暂不支持的场景如下：

- 暂不支持单独使用 RawKV 的 TiKV 集群。
- 暂不支持在 TiDB 中[创建 SEQUENCE 的 DDL 操作](/sql-statements/sql-statement-create-sequence.md)和 [SEQUENCE 函数](/sql-statements/sql-statement-create-sequence.md#sequence-函数)。在上游 TiDB 使用 SEQUENCE 时，TiCDC 将会忽略掉上游执行的 SEQUENCE DDL 操作/函数，但是使用 SEQUENCE 函数的 DML 操作可以正确地同步。
- 对上游存在较大事务的场景提供部分支持，详见 [TiCDC 是否支持同步大事务？有什么风险吗？](/ticdc/troubleshoot-ticdc.md#ticdc-支持同步大事务吗有什么风险吗)

## 兼容性问题提示

### 使用 TiCDC v5.0.0-rc 版本的 `cdc cli` 工具操作 v4.0.x 集群导致不兼容问题

使用 TiCDC v5.0.0-rc 版本的 `cdc cli` 工具操作 v4.0.x 版本的 TiCDC 集群时，可能会遇到如下异常情况：

- 若 TiCDC 集群版本为 v4.0.8 或以下，使用 v5.0.0-rc 版本的 `cdc cli` 创建同步任务 changefeed 时，可能导致 TiCDC 集群陷入异常状态，导致同步卡住。
- 若 TiCDC 集群版本为 v4.0.9 或以上，使用 v5.0.0-rc 版本的 `cdc cli` 创建同步任务 changefeed，会导致 Old Value 和 Unified Sorter 特性被非预期地默认开启。

处理方案：

使用和 TiCDC 集群版本对应的 `cdc` 可执行文件进行如下操作：

1. 删除使用 v5.0.0-rc 版本创建的 changefeed，例如：`tiup cdc:v4.0.9 cli changefeed remove -c xxxx --pd=xxxxx --force`。
2. 如果 TiCDC 同步已经卡住，重启 TiCDC 集群，例如：`tiup cluster restart <cluster_name> -R cdc`。
3. 重新创建 changefeed，例如：`tiup cdc:v4.0.9 cli changefeed create --sink-uri=xxxx --pd=xxx`。

> **注意：**
>
> 上述问题仅在 `cdc cli` 的版本是 v5.0.0-rc 时存在。未来其他 v5.0.x 版本的 `cdc cli` 可以兼容 v4.0.x 版本的集群。

## TiCDC 安装和部署

要安装 TiCDC，可以选择随新集群一起部署，也可以对现有 TiDB 集群新增 TiCDC 组件。详请参阅 [TiCDC 安装部署](/ticdc/deploy-ticdc.md)。

## TiCDC 集群管理和同步任务管理

目前支持使用 `cdc cli` 工具或 HTTP 接口来管理 TiCDC 集群状态和数据同步任务。详细操作见：

- [使用 `cdc cli` 工具来管理集群状态和数据同步](/ticdc/manage-ticdc.md#使用-cdc-cli-工具来管理集群状态和数据同步)
- [使用 HTTP 接口管理集群状态和数据同步](/ticdc/manage-ticdc.md#使用-http-接口管理集群状态和数据同步)

## TiCDC 常见问题

在使用 TiCDC 过程中经常遇到的问题以及相对应的解决方案请参考 [TiCDC 常见问题](/ticdc/troubleshoot-ticdc.md)。

## TiCDC 开放数据协议

TiCDC Open Protocol 是一种行级别的数据变更通知协议，为监控、缓存、全文索引、分析引擎、异构数据库的主从复制等提供数据源。TiCDC 遵循 TiCDC Open Protocol，向 MQ (Message Queue) 等第三方数据媒介复制 TiDB 的数据变更。详细信息参考 [TiCDC 开放数据协议](/ticdc/ticdc-open-protocol.md)。

## `sort-dir` 及 `data-dir` 配置项的兼容性说明

`sort-dir` 配置项用于给 TiCDC 内部的排序器指定临时文件目录，其作用在各版本有过如下兼容性更改：

|  版本  |  `sort-engine` 的使用  |  说明   |
|  :---  |    :---               |  :--    |
| v4.0.11 及之前的 v4.0 版本，v5.0.0-rc | 作为 changefeed 配置项，给 `file` sorter 和 `unified` Sorter 指定临时文件目录 | 在这些版本中，`file` sorter 和 `unified` sorter **均不是**正式功能 (GA)，不推荐在生产环境中使用。<br/><br/>如果有多个 changefeed 被配置使用了 `unified` 作为 `sort-engine`，那么实际使用的临时文件目录可能是任何一个 changefeed 的 `sort-dir` 配置，且每个 TiCDC 节点上使用的目录可能不一致。 |
| v4.0.12，v4.0.13，v5.0.0 及 v5.0.1 | 作为 changefeed 配置项或 `cdc server` 配置项 | 在默认情况下 changefeed 的 `sort-dir` 配置不会生效，而 `cdc server` 的 `sort-dir` 配置默认为 `/tmp/cdc_sort`。建议生产环境下仅配置 `cdc server` 的相关配置。<br /><br />如果你使用 TiUP 部署 TiCDC，建议升级到最新的 TiUP 版本并在 TiCDC server 配置中设置 `sorter.sort-dir` 一项。<br /><br />在 v4.0.13、v5.0.0 和 v5.0.1 中 unified sorter 是默认开启的，如果要将集群升级至这些版本，请确保 TiCDC server 配置中的 `sorter.sort-dir` 已经被正确配置。|
|  v5.0.2 及之后的 v5.0 版本，v5.1 | `sort-dir` 被弃用，建议配置 `data-dir` |  `data-dir` 可以通过最新版本的 TiUP 进行配置。这些版本中 unified sorter 是默认开启的，升级时请确保 `data-dir` 已经被正确配置，否则将默认使用 `/tmp/cdc_data`。<br /><br />如果该目录所在设备空间不足，有可能出现硬盘空间不足的问题。之前配置的 changefeed 的 `sort-dir` 配置将会失效。|