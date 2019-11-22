---
title: 术语表
summary: 学习 Data Migration 相关术语
category: glossary
---

# 术语表

## B

### Binlog

在 DM 中，Binlog 通常指 MySQL/MariaDB 生成的 binary log 文件，具体请参考 [MySQL Binary Log](https://dev.mysql.com/doc/internals/en/binary-log.html) 与 [MariaDB Binary Log](https://mariadb.com/kb/en/library/binary-log/)。

### Binlog Event

MySQL/MariaDB 生成的 Binlog 文件中的数据变更信息，具体请参考 [MySQL Binlog Event](https://dev.mysql.com/doc/internals/en/binlog-event.html) 与 [MariaDB Binlog Event](https://mariadb.com/kb/en/library/1-binlog-events/)。

### Binlog event filter

比 Black & white table lists 更加细粒度的过滤功能，具体可参考 [Binlog event filter](/dev/reference/tools/data-migration/overview.md#binlog-event-filter)。

### Binlog Position

特定 Binlog Event 在 Binlog 文件中的位置偏移信息，具体请参考 [MySQL SHOW BINLOG EVENTS](https://dev.mysql.com/doc/refman/8.0/en/show-binlog-events.html) 与 [MariaDB SHOW BINLOG EVENTS](https://mariadb.com/kb/en/library/show-binlog-events/)。

### Binlog Replication 处理单元

DM-worker 内部用于读取上游 Binlog 或本地 Relay Log 并迁移到下游的处理单元，每个 Subtask 对应一个 Binlog Replication 处理单元。在当前文档中，有时也称作 Sync 处理单元。

### Black & white table lists

针对上游数据库实例表的黑白名单过滤功能，具体可参考 [Black & white table lists](/dev/reference/tools/data-migration/overview.md#black--white-table-lists)。该功能与 [MySQL Replication Filtering](https://dev.mysql.com/doc/refman/5.6/en/replication-rules.html)/[MariaDB Replication Filters](https://mariadb.com/kb/en/library/replication-filters/) 类似。

## D

### Dump 处理单元

DM-worker 内部用于从上游导出全量数据的处理单元，每个 Subtask 对应一个 Dump 处理单元。

## G

### GTID

MySQL/MariaDB 的全局事务 ID，当启用该功能后会在 Binlog 文件中记录 GTID 相关信息，多个 GTID 即组成为 GTID Sets，具体请参考 [MySQL GTID Format and Storage](https://dev.mysql.com/doc/refman/5.7/en/replication-gtids-concepts.html) 与 [MariaDB Global Transaction ID](https://mariadb.com/kb/en/library/gtid/)。

## H

### Heartbeat

在增量数据迁移过程中，用于估算数据从在上游写入后到达 Binlog Replication 处理单元延迟时间的机制，具体可参考 [同步延迟监控](/dev/reference/tools/data-migration/features#同步延迟监控)。

## L

### Load 处理单元

DM-worker 内部用于将全量导出数据导入到下游的处理单元，每个 Subtask 对应一个 Load 处理单元。在当前文档中，有时也称作 Import 处理单元。

## R

### Relay Log

DM-worker 从上游 MySQL/MariaDB 拉取 Binlog 后存储在本地的文件，当前其格式为标准的 Binlog 格式，可使用版本兼容的 [mysqlbinlog](https://dev.mysql.com/doc/refman/8.0/en/mysqlbinlog.html) 等工具进行解析。其作用与 [MySQL Relay Log](https://dev.mysql.com/doc/refman/5.7/en/slave-logs-relaylog.html)/[MariaDB Relay Log](https://mariadb.com/kb/en/library/relay-log/) 相近。

有关 DM 内 Relay log 的目录结构、初始同步规则、数据清理等内容，可参考 [DM Relay Log](https://pingcap.com/docs-cn/stable/reference/tools/data-migration/relay-log/)。

### Relay 处理单元

DM-worker 内部用于从上游拉取 Binlog 并写入数据到 Relay log 的处理单元，每个 DM-worker 实例内部仅存在一个该处理单元。

## S

### Shard DDL

指合库合表迁移过程中，在上游各分表（shards）上执行的需要 DM 进行协调迁移的 DDL。在当前文档中，有时也称作 Sharding DDL。

### Shard DDL Lock

用于协调 Shard DDL 迁移的锁机制，具体原理可查看[分库分表合并同步实现原理](/dev/reference/tools/data-migration/features/shard-merge.md#实现原理)。在当前文档中，有时也称作 Sharding DDL Lock。

### Shard Group

指合库合表迁移过程中，需要合并迁移到下游同一张表的所有上游分表（shards），DM 内部具体实现时使用了两级抽象的 Shard Group，具体可查看[分库分表合并同步实现原理](/dev/reference/tools/data-migration/features/shard-merge.md#实现原理)。在当前文档中，有时也称作 Sharding Group。

### Subtask

数据迁移子任务，即数据迁移任务运行在单个 DM-worker 实例上的部分。根据任务配置的不同，单个数据迁移任务可能只有一个子任务，也可能有多个子任务。

### Subtask Status

数据迁移子任务所处的状态，目前包括 `New`、`Running`、`Paused`、`Stopped` 及 `Finished` 5 种状态。有关数据迁移任务、子任务状态的更多信息可参考[任务状态](/dev/reference/tools/data-migration/query-status.md#任务状态)。 

## T

### Table routing

用于支持将上游 MySQL/MariaDB 实例的某些表同步到下游指定表的路由功能，可以用于分库分表的合并同步，具体可参考 [Table routing](/dev/reference/tools/data-migration/features/overview.md#table-routing)。

### Task

数据迁移任务，执行 `start-task` 命令成功后即启动一个数据迁移任务。根据任务配置的不同，单个数据迁移任务既可能只在单个 DM-worker 实例上运行，也可能同时在多个 DM-worker 实例上运行。

### Task Status

数据迁移子任务所处的状态，由 [Subtask Status](#subtask-status) 整合而来，具体信息可查看[任务状态](/dev/reference/tools/data-migration/query-status.md#任务状态)。
