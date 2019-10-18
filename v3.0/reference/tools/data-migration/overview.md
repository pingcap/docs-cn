---
title: Data Migration 简介
category: reference
aliases: ['/docs-cn/tools/dm/overview/','/docs-cn/tools/data-migration-overview/']
---

# Data Migration 简介

[DM](https://github.com/pingcap/dm) (Data Migration) 是一体化的数据同步任务管理平台，支持从 MySQL 或 MariaDB 到 TiDB 的全量数据迁移和增量数据同步。使用 DM 工具有利于简化错误处理流程，降低运维成本。

## DM 架构

DM 主要包括三个组件：DM-master，DM-worker 和 dmctl。

![Data Migration architecture](/media/dm-architecture.png)

### DM-master

DM-master 负责管理和调度数据同步任务的各项操作。

- 保存 DM 集群的拓扑信息
- 监控 DM-worker 进程的运行状态
- 监控数据同步任务的运行状态
- 提供数据同步任务管理的统一入口
- 协调分库分表场景下各个实例分表的 DDL 同步

### DM-worker

DM-worker 负责执行具体的数据同步任务。

- 将 binlog 数据持久化保存在本地
- 保存数据同步子任务的配置信息
- 编排数据同步子任务的运行
- 监控数据同步子任务的运行状态

DM-worker 启动后，会自动同步上游 binlog 至本地配置目录（如果使用 DM-Ansible 部署 DM 集群，默认的同步目录为 `<deploy_dir>/relay_log`）。关于 DM-worker，详见 [DM-worker 简介](/v3.0/reference/tools/data-migration/dm-worker-intro.md)。关于 relay log，详见 [DM Relay Log](/v3.0/reference/tools/data-migration/relay-log.md)。

### dmctl

dmctl 是用来控制 DM 集群的命令行工具。

- 创建、更新或删除数据同步任务
- 查看数据同步任务状态
- 处理数据同步任务错误
- 校验数据同步任务配置的正确性

## 同步功能介绍

下面简单介绍 DM 数据同步功能的核心特性。

### Table routing

[Table routing](/v3.0/reference/tools/data-migration/features/overview.md#table-routing) 是指将上游 MySQL 或 MariaDB 实例的某些表同步到下游指定表的路由功能，可以用于分库分表的合并同步。

### Black & white table lists

[Black & white table lists](/v3.0/reference/tools/data-migration/features/overview.md#black--white-table-lists) 是指上游数据库实例表的黑白名单过滤规则。其过滤规则类似于 MySQL `replication-rules-db`/`replication-rules-table`，可以用来过滤或只同步某些数据库或某些表的所有操作。

### Binlog event filter

[Binlog event filter](/v3.0/reference/tools/data-migration/features/overview.md#binlog-event-filter) 是比库表同步黑白名单更加细粒度的过滤规则，可以指定只同步或者过滤掉某些 `schema`/`table` 的指定类型的 binlog events，比如 `INSERT`，`TRUNCATE TABLE`。

### Shard support

DM 支持对原分库分表进行合库合表操作，但需要满足一些[使用限制](/v3.0/reference/tools/data-migration/features/shard-merge.md#使用限制)。

## 使用限制

在使用 DM 工具之前，需了解以下限制：

+ 数据库版本

    - 5.5 < MySQL 版本 < 8.0
    - MariaDB 版本 >= 10.1.2

    > **注意：**
    >
    > 如果上游 MySQL/MariaDB server 间构成主从复制结构，则
    >
    > - 5.7.1 < MySQL 版本 < 8.0
    > - MariaDB 版本 >= 10.1.3

    在使用 dmctl 启动任务时，DM 会自动对任务上下游数据库的配置、权限等进行[前置检查](/v3.0/reference/tools/data-migration/precheck.md)。

+ DDL 语法

    - 目前，TiDB 部分兼容 MySQL 支持的 DDL 语句。因为 DM 使用 TiDB parser 来解析处理 DDL 语句，所以目前仅支持 TiDB parser 支持的 DDL 语法。
    - DM 遇到不兼容的 DDL 语句时会报错。要解决此报错，需要使用 dmctl 手动处理，要么跳过该 DDL 语句，要么用指定的 DDL 语句来替换它。

+ 分库分表

    - 如果业务分库分表之间存在数据冲突，可以参考[自增主键冲突处理](/v3.0/reference/tools/data-migration/usage-scenarios/best-practice-dm-shard.md#自增主键冲突处理)来解决；否则不推荐使用 DM 进行同步，如果进行同步则有冲突的数据会相互覆盖造成数据丢失。
    - 关于分库分表合并场景的其它限制，参见[使用限制](/v3.0/reference/tools/data-migration/features/shard-merge.md#使用限制)。

+ 操作限制

    - DM-worker 重启后不能自动恢复数据同步任务，需要使用 dmctl 手动执行 `start-task`。详见[管理数据同步任务](/v3.0/reference/tools/data-migration/manage-tasks.md)。
    - 在一些情况下，DM-worker 重启后不能自动恢复 DDL lock 同步，需要手动处理。详见[手动处理 Sharding DDL Lock](/v3.0/reference/tools/data-migration/features/manually-handling-sharding-ddl-locks.md)。

+ DM-worker 切换 MySQL

    - 当 DM-worker 通过虚拟 IP（VIP）连接到 MySQL 且 VIP 实际指向的 MySQL 发生切换时，可能出现在同一时刻 DM 内部不同的 connection 分别连接到 VIP 切换前后不同的 MySQL 实例的情况，并造成 DM 拉取的 binlog 与获取到的其他状态不一致而导致难以预期的异常行为甚至数据损坏。如需切换 VIP 连接的 MySQL，请参考 [虚拟 IP 环境下的上游主从切换](/v3.0/reference/tools/data-migration/usage-scenarios/master-slave-switch.md#虚拟-IP-环境下的上游主从切换) 对 DM 手动执行变更。
