---
title: TiDB Data Migration Glossary
summary: Learn the terms used in TiDB Data Migration.
category: glossary
---

# TiDB Data Migration Glossary

This document lists the terms used in the logs, monitoring, configurations, and documentation of TiDB Data Migration (DM).

## B

### Binlog

In TiDB DM, binlogs refer to the binary log files generated in the TiDB database. It has the same indications as that in MySQL or MariaDB. Refer to [MySQL Binary Log](https://dev.mysql.com/doc/internals/en/binary-log.html) and [MariaDB Binary Log](https://mariadb.com/kb/en/library/binary-log/) for details.

### Binlog event

Binlog events are information about data modification made to a MySQL or MariaDB server instance. These binlog events are stored in the binlog files. Refer to [MySQL Binlog Event](https://dev.mysql.com/doc/internals/en/binlog-event.html) and [MariaDB Binlog Event](https://mariadb.com/kb/en/library/1-binlog-events/) for details.

### Binlog event filter

[Binlog event filter](/reference/tools/data-migration/features/overview.md#binlog-event-filter) is a more fine-grained filtering feature than the black and white lists filtering rule. Refer to [binlog event filter](/reference/tools/data-migration/overview.md#binlog-event-filtering) for details.

### Binlog position

The binlog position is the offset information of a binlog event in a binlog file. Refer to [MySQL `SHOW BINLOG EVENTS`](https://dev.mysql.com/doc/refman/8.0/en/show-binlog-events.html) and [MariaDB `SHOW BINLOG EVENTS`](https://mariadb.com/kb/en/library/show-binlog-events/) for details.

### Binlog replication processing unit

Binlog replication processing unit is the processing unit used in DM-worker to read upstream binlogs or local relay logs, and to replicate these logs to the downstream. Each subtask corresponds to a binlog replication processing unit. In the current documentation, the binlog replication processing unit is also referred to as the sync processing unit.

### Black & white table list

Black & white table list is the feature that filters or only replicates all operations of some databases or some tables. Refer to [black & white table lists](/reference/tools/data-migration/overview.md#black-and-white-lists-replication-at-the-schema-and-table-levels) for details. This feature is similar to [MySQL Replication Filtering](https://dev.mysql.com/doc/refman/5.6/en/replication-rules.html) and [MariaDB Replication Filters](https://mariadb.com/kb/en/library/replication-filters/).

## C

### Checkpoint

A checkpoint indicates the position from which a full data import or an incremental replication task is paused and resumed, or is stopped and restarted.

- In a full import task, a checkpoint corresponds to the offset and other information of the successfully imported data in a file that is being imported. A checkpoint is updated synchronously with the data import task.
- In an incremental replication, a checkpoint corresponds to the [binlog position](#binlog-position) and other information of a [binlog event](#binlog-event) that is successfully parsed and replicated to the downstream. A checkpoint is updated after the DDL operation is successfully replicated or 30 seconds after the last update.

In addition, the `relay.meta` information corresponding to a [relay processing unit](#relay-processing-unit) works similarly to a checkpoint. A relay processing unit pulls the [binlog event](#binlog-event) from the upstream and writes this event to the [relay log](#relay-log), and writes the [binlog position](#binlog-position) or the GTID information corresponding to this event to `relay.meta`.

## D

### Dump processing unit

The dump processing unit is the processing unit used in DM-worker to export all data from the upstream. Each subtask corresponds to a dump processing unit.

## G

### GTID

The GTID is the global transaction ID of MySQL or MariaDB. With this feature enabled, the GTID information is recorded in the binlog files. Multiple GTIDs form a GTID set. Refer to [MySQL GTID Format and Storage](https://dev.mysql.com/doc/refman/5.7/en/replication-gtids-concepts.html) and [MariaDB Global Transaction ID](https://mariadb.com/kb/en/library/gtid/) for details.

## H

### Heartbeat

The heartbeat is a mechanism that calculates the delay from the time data is written in the upstream to the time data is processed by the binlog replication processing unit. Refer to [replication delay monitoring](/reference/tools/data-migration/features/overview.md#replication-delay-monitoring) for details.

## L

### Load processing unit

The load processing unit is the processing unit used in DM-worker to import the fully exported data to the downstream. Each subtask corresponds to a load processing unit. In the current documentation, the load processing unit is also referred to as the import processing unit.

## R

### Relay log

The relay log refers to the binlog files that DM-worker pulls from the upstream MySQL or MariaDB, and stores in the local disk. The format of the relay log is the standard binlog file, which can be parsed by tools such as [mysqlbinlog](https://dev.mysql.com/doc/refman/8.0/en/mysqlbinlog.html) of a compatible version.

For more details such as the relay log's directory structure, initial replication rules, and data purge in TiDB DM, see [TiDB DM relay log](/reference/tools/data-migration/relay-log.md).

### Relay processing unit

The relay processing unit is the processing unit used in DM-worker to pull binlog files from the upstream and write data into relay logs. Each DM-worker instance has only one relay processing unit.

## S

### Safe mode

Safe mode is the mode in which DML statements can be imported more than once when the primary key or unique index exists in the table schema.

In this mode, some statements from the upstream are replicated to the downstream only after they are re-written. The `INSERT` statement is re-written as `REPLACE`; the `UPDATE` statement is re-written as `DELETE` and `REPLACE`. TiDB DM automatically enables the safe mode within 5 minutes after the replication task is started or resumed. You can manually enable the mode by modifying the `safe-mode` parameter in the task configuration file.

### Shard DDL

The shard DDL is the DDL statement that is executed on the upstream sharded tables. It needs to be coordinated and migrated by TiDB DM in the process of merging the sharded tables. In the current documentation, the shard DDL is also referred to as the sharding DDL.

### Shard DDL lock

The shard DDL lock is the lock mechanism that coordinates the replication of shard DDL. Refer to [the implementation principles of merging and replicating data from sharded tables](/reference/tools/data-migration/features/shard-merge.md#principles) for details. In the current documentation, the shard DDL lock is also referred to as the sharding DDL lock.

### Shard group

A shard group is all the upstream sharded tables to be merged and replicated to the same table in the downstream. Two-level shard groups are used for implementation of TiDB DM. Refer to [the implementation principles of merging and replicating sharded tables](/reference/tools/data-migration/features/shard-merge.md#principles) for details. In the current documentation, the shard group is also referred to as the sharding group.

### Subtask

The subtask is a part of a data replication task that is running on each DM-worker instance. In different task configurations, a single data replication task might have one subtask or multiple subtasks.

### Subtask status

The subtask status is the status of a data replication subtask. The current status options include `New`, `Running`, `Paused`, `Stopped`, and `Finished`. Refer to [subtask status](/reference/tools/data-migration/query-status.md#subtask-status) for more details about the status of a data replication task or subtask.

## T

### Table routing

The table routing feature enables DM to replicate a certain table of the upstream MySQL or MariaDB instance to the specified table in the downstream, which can be used to merge and replicate sharded tables. Refer to [table routing](/reference/tools/data-migration/features/overview.md#table-routing) for details.

### Task

The data replication task, which is started after you successfully execute a `start-task` command. In different task configurations, a single replication task can run on a single DM-worker instance or on multiple DM-worker instances at the same time.

### Task status

The task status refers to the status of a data replication task. The task status depends on the statuses of all its subtasks. Refer to [subtask status](/reference/tools/data-migration/query-status.md#subtask-status) for details.
