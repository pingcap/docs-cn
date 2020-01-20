---
title: TiDB Data Migration 术语表
summary: 学习 TiDB Data Migration 相关术语
category: glossary
---

# TiDB Data Migration 术语表

本文档介绍 TiDB Data Migration (TiDB DM) 相关术语。

## B

### Binlog

在 TiDB DM 中，Binlog 通常指 MySQL/MariaDB 生成的 binary log 文件，具体请参考 [MySQL Binary Log](https://dev.mysql.com/doc/internals/en/binary-log.html) 与 [MariaDB Binary Log](https://mariadb.com/kb/en/library/binary-log/)。

### Binlog event

MySQL/MariaDB 生成的 Binlog 文件中的数据变更信息，具体请参考 [MySQL Binlog Event](https://dev.mysql.com/doc/internals/en/binlog-event.html) 与 [MariaDB Binlog Event](https://mariadb.com/kb/en/library/1-binlog-events/)。

### Binlog event filter

比 Black & white table list 更加细粒度的过滤功能，具体可参考 [Binlog event filter](/v2.1/reference/tools/data-migration/overview.md#binlog-event-filter)。

### Binlog position

特定 Binlog event 在 Binlog 文件中的位置偏移信息，具体请参考 [MySQL `SHOW BINLOG EVENTS`](https://dev.mysql.com/doc/refman/8.0/en/show-binlog-events.html) 与 [MariaDB `SHOW BINLOG EVENTS`](https://mariadb.com/kb/en/library/show-binlog-events/)。

### Binlog replication 处理单元

DM-worker 内部用于读取上游 Binlog 或本地 Relay log 并迁移到下游的处理单元，每个 Subtask 对应一个 Binlog replication 处理单元。在当前文档中，有时也称作 Sync 处理单元。

### Black & white table list

针对上游数据库实例表的黑白名单过滤功能，具体可参考 [Black & white table lists](/v2.1/reference/tools/data-migration/overview.md#black--white-table-lists)。该功能与 [MySQL Replication Filtering](https://dev.mysql.com/doc/refman/5.6/en/replication-rules.html) 及 [MariaDB Replication Filters](https://mariadb.com/kb/en/library/replication-filters/) 类似。

## C

### Checkpoint

TiDB DM 在全量导入与增量复制过程中的断点信息，用于在重新启动或恢复任务时从之前已经处理过的位置继续执行。

- 对于全量导入，Checkpoint 信息对应于每个数据文件已经被成功导入的数据对应的文件内偏移量等信息，其在每个导入数据的事务中同步更新；
- 对于增量复制，Checkpoint 信息对应于已经成功解析并导入到下游的 [Binlog event](#binlog-event) 对应的 [Binlog position](#binlog-position) 等信息，其在 DDL 导入成功后或距上次更新时间超过 30 秒等条件下更新。

另外，[Relay 处理单元](#relay-处理单元) 对应的 `relay.meta` 内记录的信息也相当于 Checkpoint，其对应于 Relay 处理单元已经成功从上游拉取并写入到 [Relay log](#relay-log) 的 [Binlog event](#binlog-event) 对应的 [Binlog position](#binlog-position) 或 [GTID](#GTID) 信息。

## D

### Dump 处理单元

DM-worker 内部用于从上游导出全量数据的处理单元，每个 Subtask 对应一个 Dump 处理单元。

## G

### GTID

MySQL/MariaDB 的全局事务 ID，当启用该功能后会在 Binlog 文件中记录 GTID 相关信息，多个 GTID 即组成为 GTID Set，具体请参考 [MySQL GTID Format and Storage](https://dev.mysql.com/doc/refman/5.7/en/replication-gtids-concepts.html) 与 [MariaDB Global Transaction ID](https://mariadb.com/kb/en/library/gtid/)。

## H

### Heartbeat

在增量数据迁移过程中，用于估算数据从在上游写入后到达 Binlog replication 处理单元延迟时间的机制，具体可参考[同步延迟监控](/v2.1/reference/tools/data-migration/features/overview.md#同步延迟监控)。

## L

### Load 处理单元

DM-worker 内部用于将全量导出数据导入到下游的处理单元，每个 Subtask 对应一个 Load 处理单元。在当前文档中，有时也称作 Import 处理单元。

## R

### Relay log

DM-worker 从上游 MySQL/MariaDB 拉取 Binlog 后存储在本地的文件，当前其格式为标准的 Binlog 格式，可使用版本兼容的 [mysqlbinlog](https://dev.mysql.com/doc/refman/8.0/en/mysqlbinlog.html) 等工具进行解析。其作用与 [MySQL Relay Log](https://dev.mysql.com/doc/refman/5.7/en/slave-logs-relaylog.html) 及 [MariaDB Relay Log](https://mariadb.com/kb/en/library/relay-log/) 相近。

有关 TiDB DM 内 Relay log 的目录结构、初始同步规则、数据清理等内容，可参考 [TiDB DM Relay Log](https://pingcap.com/docs-cn/stable/reference/tools/data-migration/relay-log/)。

### Relay 处理单元

DM-worker 内部用于从上游拉取 Binlog 并写入数据到 Relay log 的处理单元，每个 DM-worker 实例内部仅存在一个该处理单元。

## S

### Safe mode

指增量复制过程中，用于支持在表结构中存在主键或唯一索引的条件下可重复导入 DML 的模式。

该模式的主要特点为将来自上游的 `INSERT` 改写为 `REPLACE`，将 `UPDATE` 改写为 `DELETE` 与 `REPLACE` 后再向下游执行。在启动或恢复增量迁移任务的前 5 分钟 TiDB DM 会自动启动 Safe mode，另外也可以在任务配置文件中通过 `safe-mode` 参数手动开启。

### Shard DDL

指合库合表迁移过程中，在上游各分表 (shard) 上执行的需要 TiDB DM 进行协调迁移的 DDL。在当前文档中，有时也称作 Sharding DDL。

### Shard DDL lock

用于协调 Shard DDL 迁移的锁机制，具体原理可查看[分库分表合并同步实现原理](/v2.1/reference/tools/data-migration/features/shard-merge.md#实现原理)。在当前文档中，有时也称作 Sharding DDL lock。

### Shard group

指合库合表迁移过程中，需要合并迁移到下游同一张表的所有上游分表 (shard)，TiDB DM 内部具体实现时使用了两级抽象的 Shard group，具体可查看[分库分表合并同步实现原理](/v2.1/reference/tools/data-migration/features/shard-merge.md#实现原理)。在当前文档中，有时也称作 Sharding group。

### Subtask

数据迁移子任务，即数据迁移任务运行在单个 DM-worker 实例上的部分。根据任务配置的不同，单个数据迁移任务可能只有一个子任务，也可能有多个子任务。

### Subtask status

数据迁移子任务所处的状态，目前包括 `New`、`Running`、`Paused`、`Stopped` 及 `Finished` 5 种状态。有关数据迁移任务、子任务状态的更多信息可参考[任务状态](/v2.1/reference/tools/data-migration/query-status.md#任务状态)。

## T

### Table routing

用于支持将上游 MySQL/MariaDB 实例的某些表同步到下游指定表的路由功能，可以用于分库分表的合并同步，具体可参考 [Table routing](/v2.1/reference/tools/data-migration/features/overview.md#table-routing)。

### Task

数据迁移任务，执行 `start-task` 命令成功后即启动一个数据迁移任务。根据任务配置的不同，单个数据迁移任务既可能只在单个 DM-worker 实例上运行，也可能同时在多个 DM-worker 实例上运行。

### Task status

数据迁移子任务所处的状态，由 [Subtask status](#subtask-status) 整合而来，具体信息可查看[任务状态](/v2.1/reference/tools/data-migration/query-status.md#任务状态)。
