---
title: TiDB Data Migration Glossary
summary: Learn the terms used in TiDB Data Migration.
aliases: ['/docs/tidb-data-migration/dev/glossary/']
---

# TiDB Data Migration Glossary

This document lists the terms used in the logs, monitoring, configurations, and documentation of TiDB Data Migration (DM).

## B

### Binlog

In TiDB DM, binlogs refer to the binary log files generated in the TiDB database. It has the same indications as that in MySQL or MariaDB. Refer to [MySQL Binary Log](https://dev.mysql.com/doc/dev/mysql-server/latest/page_protocol_replication.html) and [MariaDB Binary Log](https://mariadb.com/kb/en/library/binary-log/) for details.

### Binlog event

Binlog events are information about data modification made to a MySQL or MariaDB server instance. These binlog events are stored in the binlog files. Refer to [MySQL Binlog Event](https://dev.mysql.com/doc/dev/mysql-server/latest/page_protocol_replication_binlog_event.html) and [MariaDB Binlog Event](https://mariadb.com/kb/en/library/1-binlog-events/) for details.

### Binlog event filter

[Binlog event filter](/dm/dm-binlog-event-filter.md) is a more fine-grained filtering feature than the block and allow lists filtering rule. Refer to [binlog event filter](/dm/dm-binlog-event-filter.md) for details.

### Binlog position

The binlog position is the offset information of a binlog event in a binlog file. Refer to [MySQL `SHOW BINLOG EVENTS`](https://dev.mysql.com/doc/refman/8.0/en/show-binlog-events.html) and [MariaDB `SHOW BINLOG EVENTS`](https://mariadb.com/kb/en/library/show-binlog-events/) for details.

### Binlog replication processing unit/sync unit

Binlog replication processing unit is the processing unit used in DM-worker to read upstream binlogs or local relay logs, and to migrate these logs to the downstream. Each subtask corresponds to a binlog replication processing unit. In the current documentation, the binlog replication processing unit is also referred to as the sync processing unit.

### Block & allow table list

Block & allow table list is the feature that filters or only migrates all operations of some databases or some tables. Refer to [block & allow table lists](/dm/dm-block-allow-table-lists.md) for details. This feature is similar to [MySQL Replication Filtering](https://dev.mysql.com/doc/refman/5.6/en/replication-rules.html) and [MariaDB Replication Filters](https://mariadb.com/kb/en/replication-filters/).

## C

### Checkpoint

A checkpoint indicates the position from which a full data import or an incremental replication task is paused and resumed, or is stopped and restarted.

- In a full import task, a checkpoint corresponds to the offset and other information of the successfully imported data in a file that is being imported. A checkpoint is updated synchronously with the data import task.
- In an incremental replication, a checkpoint corresponds to the [binlog position](#binlog-position) and other information of a [binlog event](#binlog-event) that is successfully parsed and migrated to the downstream. A checkpoint is updated after the DDL operation is successfully migrated or 30 seconds after the last update.

In addition, the `relay.meta` information corresponding to a [relay processing unit](#relay-processing-unit) works similarly to a checkpoint. A relay processing unit pulls the [binlog event](#binlog-event) from the upstream and writes this event to the [relay log](#relay-log), and writes the [binlog position](#binlog-position) or the GTID information corresponding to this event to `relay.meta`.

## D

### Dump processing unit/dump unit

The dump processing unit is the processing unit used in DM-worker to export all data from the upstream. Each subtask corresponds to a dump processing unit.

## G

### GTID

The GTID is the global transaction ID of MySQL or MariaDB. With this feature enabled, the GTID information is recorded in the binlog files. Multiple GTIDs form a GTID set. Refer to [MySQL GTID Format and Storage](https://dev.mysql.com/doc/refman/5.7/en/replication-gtids-concepts.html) and [MariaDB Global Transaction ID](https://mariadb.com/kb/en/library/gtid/) for details.

## L

### Load processing unit/load unit

The load processing unit is the processing unit used in DM-worker to import the fully exported data to the downstream. Each subtask corresponds to a load processing unit. In the current documentation, the load processing unit is also referred to as the import processing unit.

## M

### Migrate/migration

The process of using the TiDB Data Migration tool to copy the **full data** of the upstream database to the downstream database.

In the case of clearly mentioning "full", not explicitly mentioning "full or incremental", and clearly mentioning "full + incremental", use migrate/migration instead of replicate/replication.

## R

### Relay log

The relay log refers to the binlog files that DM-worker pulls from the upstream MySQL or MariaDB, and stores in the local disk. The format of the relay log is the standard binlog file, which can be parsed by tools such as [mysqlbinlog](https://dev.mysql.com/doc/refman/8.0/en/mysqlbinlog.html) of a compatible version. Its role is similar to [MySQL Relay Log](https://dev.mysql.com/doc/refman/5.7/en/replica-logs-relaylog.html) and [MariaDB Relay Log](https://mariadb.com/kb/en/library/relay-log/).

For more details such as the relay log's directory structure, initial migration rules, and data purge in TiDB DM, see [TiDB DM relay log](/dm/relay-log.md).

### Relay processing unit

The relay processing unit is the processing unit used in DM-worker to pull binlog files from the upstream and write data into relay logs. Each DM-worker instance has only one relay processing unit.

### Replicate/replication

The process of using the TiDB Data Migration tool to copy the **incremental data** of the upstream database to the downstream database.

In the case of clearly mentioning "incremental", use replicate/replication instead of migrate/migration.

## S

### Safe mode

Safe mode is the mode in which DML statements can be imported more than once when the primary key or unique index exists in the table schema. In this mode, some statements from the upstream are migrated to the downstream only after they are re-written. The `INSERT` statement is re-written as `REPLACE`; the `UPDATE` statement is re-written as `DELETE` and `REPLACE`.

This mode is enabled in any of the following situations:

- The safe mode remains enabled when the `safe-mode` parameter in the task configuration file is set to `true`.
- In shard merge scenarios, the safe mode remains enabled before DDL statements are replicated in all sharded tables.
- If the argument `--consistency none` is configured for the dump processing unit of a full migration task, it cannot be determined whether the binlog changes at the beginning of the export affect the exported data or not. Therefore, the safe mode remains enabled for the incremental replication of these binlog changes.
- If the task is paused by error and then resumed, the operations on some data might be executed twice.

### Shard DDL

The shard DDL is the DDL statement that is executed on the upstream sharded tables. It needs to be coordinated and migrated by TiDB DM in the process of merging the sharded tables. In the current documentation, the shard DDL is also referred to as the sharding DDL.

### Shard DDL lock

The shard DDL lock is the lock mechanism that coordinates the migration of shard DDL. Refer to [the implementation principles of merging and migrating data from sharded tables in the pessimistic mode](/dm/feature-shard-merge-pessimistic.md#principles) for details. In the current documentation, the shard DDL lock is also referred to as the sharding DDL lock.

### Shard group

A shard group is all the upstream sharded tables to be merged and migrated to the same table in the downstream. Two-level shard groups are used for implementation of TiDB DM. Refer to [the implementation principles of merging and migrating data from sharded tables in the pessimistic mode](/dm/feature-shard-merge-pessimistic.md#principles) for details. In the current documentation, the shard group is also referred to as the sharding group.

### Subtask

The subtask is a part of a data migration task that is running on each DM-worker instance. In different task configurations, a single data migration task might have one subtask or multiple subtasks.

### Subtask status

The subtask status is the status of a data migration subtask. The current status options include `New`, `Running`, `Paused`, `Stopped`, and `Finished`. Refer to [subtask status](/dm/dm-query-status.md#subtask-status) for more details about the status of a data migration task or subtask.

## T

### Table routing

The table routing feature enables DM to migrate a certain table of the upstream MySQL or MariaDB instance to the specified table in the downstream, which can be used to merge and migrate sharded tables. Refer to [table routing](/dm/dm-table-routing.md) for details.

### Task

The data migration task, which is started after you successfully execute a `start-task` command. In different task configurations, a single migration task can run on a single DM-worker instance or on multiple DM-worker instances at the same time.

### Task status

The task status refers to the status of a data migration task. The task status depends on the statuses of all its subtasks. Refer to [subtask status](/dm/dm-query-status.md#subtask-status) for details.
