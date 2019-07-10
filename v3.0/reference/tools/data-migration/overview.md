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

DM-worker 启动后，会自动同步上游 binlog 至本地配置目录（如果使用 DM-Ansible 部署 DM 集群，默认的同步目录为 `<deploy_dir>/relay_log`）。关于 DM-worker，详见 [DM-worker 简介](/reference/tools/data-migration/dm-worker-intro.md)。关于 relay log，详见 [DM Relay Log](/reference/tools/data-migration/relay-log.md)。

### dmctl

dmctl 是用来控制 DM 集群的命令行工具。

- 创建、更新或删除数据同步任务
- 查看数据同步任务状态
- 处理数据同步任务错误
- 校验数据同步任务配置的正确性

## 同步功能介绍

下面简单介绍 DM 数据同步功能的核心特性。

### Table routing

[Table routing](/reference/tools/data-migration/features/overview.md#table-routing) 是指将上游 MySQL 或 MariaDB 实例的某些表同步到下游指定表的路由功能，可以用于分库分表的合并同步。

### Black & white table lists

[Black & white table lists](/reference/tools/data-migration/features/overview.md#black-white-table-lists) 是指上游数据库实例表的黑白名单过滤规则。其过滤规则类似于 MySQL `replication-rules-db`/`replication-rules-table`，可以用来过滤或只同步某些数据库或某些表的所有操作。

### Binlog event filter

[Binlog event filter](/reference/tools/data-migration/features/overview.md#binlog-event-filter) 是比库表同步黑白名单更加细粒度的过滤规则，可以指定只同步或者过滤掉某些 `schema`/`table` 的指定类型的 binlog events，比如 `INSERT`，`TRUNCATE TABLE`。

### Column mapping

[Column mapping](/reference/tools/data-migration/features/overview.md#column-mapping) 是指根据用户指定的内置表达式对表的列进行转换，可以用来解决分库分表合并时自增主键 ID 的冲突。

### Shard support

DM 支持对原分库分表进行合库合表操作，但需要满足一些[使用限制](/reference/tools/data-migration/features/shard-merge.md#使用限制)。

## 使用限制

在使用 DM 工具之前，需了解以下限制：

+ 数据库版本

    - 5.5 < MySQL 版本 < 5.8
    - MariaDB 版本 >= 10.1.2

    > **注意：**
    >
    > 如果上游 MySQL/MariaDB server 间构成主从复制结构，则
    >
    > - 5.7.1 < MySQL 版本 < 5.8
    > - MariaDB 版本 >= 10.1.3

    在使用 dmctl 启动任务时，DM 会自动对任务上下游数据库的配置、权限等进行[前置检查](/reference/tools/data-migration/precheck.md)。

+ DDL 语法

    - 目前，TiDB 部分兼容 MySQL 支持的 DDL 语句。因为 DM 使用 TiDB parser 来解析处理 DDL 语句，所以目前仅支持 TiDB parser 支持的 DDL 语法。详见 [TiDB DDL 语法支持](/reference/mysql-compatibility.md#ddl)。

    - DM 遇到不兼容的 DDL 语句时会报错。要解决此报错，需要使用 dmctl 手动处理，要么跳过该 DDL 语句，要么用指定的 DDL 语句来替换它。

+ 分库分表

    - 如果业务分库分表之间存在数据冲突，冲突的列**只有自增主键列**，并且**列的类型是 bigint**，可以尝试使用 [Column mapping](/reference/tools/data-migration/features/overview.md#column-mapping) 来解决；否则不推荐使用 DM 进行同步，如果进行同步则有冲突的数据会相互覆盖造成数据丢失。
    - 关于分库分表合并场景的其它限制，参见[使用限制](/reference/tools/data-migration/features/shard-merge.md#使用限制)。

+ 操作限制

    - DM-worker 重启后不能自动恢复数据同步任务，需要使用 dmctl 手动执行 `start-task`。详见[管理数据同步任务](/reference/tools/data-migration/manage-tasks.md)。
    - 在一些情况下，DM-worker 重启后不能自动恢复 DDL lock 同步，需要手动处理。详见[手动处理 Sharding DDL Lock](/reference/tools/data-migration/features/manually-handling-sharding-ddl-locks.md)。
