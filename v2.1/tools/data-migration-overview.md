---
title: Data Migration Overview
summary: Learn about the Data Migration tool, the architecture, the key components and features.
category: tools
---

# Data Migration Overview

Data Migration (DM) is an integrated data replication task management platform that supports the full data migration and the incremental data migration from MySQL/MariaDB into TiDB. It can help to reduce the operations cost and simplify the troubleshooting process.

## Architecture

The Data Migration tool includes three components: DM-master, DM-worker, and dmctl.

![Data Migration architecture](../media/dm-architecture.png)

### DM-master

DM-master manages and schedules the operation of data replication tasks.

- Storing the topology information of the DM cluster
- Monitoring the running state of DM-worker processes
- Monitoring the running state of data replication tasks
- Providing a unified portal for the management of data replication tasks
- Coordinating the DDL replication of sharded tables in each instance under the sharding scenario

### DM-worker

DM-worker executes specific data replication tasks.

- Persisting the binlog data to the local storage
- Storing the configuration information of the data replication subtasks
- Orchestrating the operation of the data replication subtasks
- Monitoring the running state of the data replication subtasks

For details about DM-worker, see [DM-worker Introduction](../tools/dm-worker-intro.md).

### dmctl 

dmctl is the command line tool used to control the DM cluster.

- Creating/Updating/Dropping data replication tasks
- Checking the state of data replication tasks
- Handling the errors during data replication tasks
- Verifying the configuration correctness of data replication tasks

## Data replication introduction

This section describes the data replication feature provided by Data Migration in detail.

### Black and white lists replication at the schema and table levels

The black and white lists filtering rule of the upstream database instances is similar to MySQL replication-rules-db/tables, which can be used to filter or only replicate all operations of some databases or some tables.

### Binlog event filtering

Binlog event filtering is a more fine-grained filtering rule than the black and white lists filtering rule at the schema and table levels. You can use statements like `INSERT` and `TRUNCATE TABLE` to specify the Binlog events of the database(s) or table(s) that you need to replicate or filter out.

### Column mapping

Column mapping is used to resolve the conflicts occurred when the sharding auto-increment primary key IDs are merged for sharded tables. The value of the auto-increment primary key ID can be modified according to the instance-id, which is configured by the user, and the schema/table ID.

### Sharding support

DM supports merging the original sharded instances and tables into TiDB, with some restrictions.

### Incompatible DDL handling

Currently, TiDB is not compatible with all the DDL statements that MySQL supports. See [the DDL statements supported by TiDB](../sql/ddl.md).

DM reports an error when it encounters an incompatible DDL statement. To solve this error, you need to manually handle it using dmctl, either skipping this DDL statement or replacing it with a specified DDL statement(s). For details, see [Skip or replace abnormal SQL statements](../tools/data-migration-troubleshooting.md#skip-or-replace-abnormal-sql-statements).
