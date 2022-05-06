---
title: Migration Task Precheck
summary: Learn the precheck that DM performs before starting a migration task.
aliases: ['/docs/tidb-data-migration/dev/precheck/']
---

# Migration Task Precheck

Before using DM to migrate data from upstream to downstream, a precheck helps detect errors in the upstream database configurations and ensures that the migration goes smoothly. This document introduces the DM precheck feature, including its usage scenario, check items, and arguments.

## Usage scenario

To run a data migration task smoothly, DM triggers a precheck automatically at the start of the task and returns the check results. DM starts the migration only after the precheck is passed.

To trigger a precheck manually, run the `check-task` command.

For example:

{{< copyable "" >}}

```bash
tiup dmctl check-task ./task.yaml
```

## Descriptions of check items

After a precheck is triggered for a task, DM checks the corresponding items according to your migration mode configuration.

This section lists all the precheck items.

> **Note:**
>
> In this document, check items that must be passed are labeled "(Mandatory)".

> - If a mandatory check item does not pass, DM returns an error after the check and does not proceed with the migration task. In this case, modify the configurations according to the error message and retry the task after meeting the precheck requirements.
>
> - If a non-mandatory check item does not pass, DM returns a warning after the check. DM automatically starts a migration task if the check result contains only warnings but no errors.

### Common check items

Regardless of the migration mode you choose, the precheck always includes the following common check items:

- Database version

    - MySQL version > 5.5
    - MariaDB version >= 10.1.2

    > **Warning:**
    >
    > - Migrating data from MySQL 8.0 to TiDB using DM is an experimental feature (introduced since DM v2.0). It is NOT recommended that you use it in a production environment.
    > - Migrating data from MariaDB to TiDB using DM is an experimental feature. It is NOT recommended that you use it in a production environment.

- Compatibility of the upstream MySQL table schema

    - Check whether the upstream tables have foreign keys, which are not supported by TiDB. A warning is returned if a foreign key is found in the precheck.
    - (Mandatory) Check whether there are compatibility differences in character sets. For more information, see [TiDB Supported Character Sets](/character-set-and-collation.md).
    - (Mandatory) Check whether the upstream tables have primary key constraints or unique key constraints (introduced from v1.0.7)

### Check items for full data migration

For the full data migration mode (`task-mode: full`), in addition to the [common check items](#common-check-items), the precheck also includes the following check items:

* (Mandatory) dump permission of the upstream database

    - SELECT permission on INFORMATION_SCHEMA and dump tables
    - RELOAD permission if `consistency=flush`
    - LOCK TABLES permission on the dump tables if `consistency=flush/lock`

* (Mandatory) Consistency of upstream MySQL multi-instance sharding tables

    - In the pessimistic mode, check whether the table schemas of all sharded tables are consistent in the following items:

        - Number of columns
        - Column name
        - Column order
        - Column type
        - Primary key
        - Unique index

    - In the optimistic mode, check whether the schemas of all sharded tables meet the [optimistic compatibility](https://github.com/pingcap/tiflow/blob/master/dm/docs/RFCS/20191209_optimistic_ddl.md#modifying-column-types).

    - If a migration task was started successfully by the `start-task` command, the precheck of this task skips the consistency check.

* Auto-increment primary key in sharded tables

    - If sharded tables have auto-increment primary keys, the precheck returns a warning. If there are conflicts in auto-increment primary keys, see [Handle conflicts of auto-increment primary key](/dm/shard-merge-best-practices.md#handle-conflicts-of-auto-increment-primary-key) for solutions.

### Check items for incremental data migration

For the incremental data migration mode (`task-mode: incremental`), in addition to the [common check items](#common-check-items), the precheck also includes the following check items:

* (Mandatory) Upstream database REPLICATION permission

    - REPLICATION CLIENT permission
    - REPLICATION SLAVE permission

* (Mandatory) Database primary-secondary configuration

    - The database ID `server_id` of the upstream database must be specified (GTID is recommended for non-AWS Aurora environments).

* (Mandatory) MySQL binlog configuration

    - Check whether binlog is enabled (required by DM).
    - Check whether `binlog_format=ROW` is configured (DM only supports the migration of binlog in the ROW format).
    - Check whether `binlog_row_image=FULL` is configured (DM only supports `binlog_row_image=FULL`).
    - If `binlog_do_db` or `binlog_ignore_db` is configured, check whether the database tables to be migrated meet the conditions of `binlog_do_db` and `binlog_ignore_db`.

* (Mandatory) Check if the upstream database is in an [Online-DDL](/dm/feature-online-ddl.md) process (in which the `ghost` table is created but the `rename` phase is not executed yet). If the upstream is in the online-DDL process, the precheck returns an error. In this case, wait until the DDL to complete and retry.

### Check items for full and incremental data migration

For the full and incremental data migration mode (`task-mode: all`), in addition to the [common check items](#common-check-items), the precheck also includes the [full data migration check items](#check-items-for-full-data-migration) and the [incremental data migration check items](#check-items-for-incremental-data-migration).

### Ignorable check items

Prechecks can find potential risks in your environments. It is not recommended to ignore check items. If your data migration task has special needs, you can use the [`ignore-checking-items` configuration item](/dm/task-configuration-file-full.md#task-configuration-file-template-advanced) to skip some check items.

| Check item  | Description   |
| :---------- | :------------ |
| `dump_privilege`         | Checks the dump privilege of the user in the upstream MySQL instance. |
| `replication_privilege` | Checks the replication privilege of the user in the upstream MySQL instance. |
| `version`               | Checks the version of the upstream database. |
| `server_id`             | Checks whether server_id is configured in the upstream database. |
| `binlog_enable`         | Checks whether binlog is enabled in the upstream database. |
| `table_schema`          | Checks the compatibility of the table schemas in the upstream MySQL tables. |
| `schema_of_shard_tables`| Checks the consistency of the table schemas in the upstream MySQL multi-instance shards. |
| `auto_increment_ID`     | Checks whether the auto-increment primary key conflicts in the upstream MySQL multi-instance shards. |

> **Note:**
>
> More ignorable check items are supported in versions earlier than v6.0. Since v6.0, DM does not allow ignoring some check items related to data safety. For example, if you configure the `binlog_row_image` parameter incorrectly, data might be lost during the replication.

## Configure precheck arguments

The migration task precheck supports processing in parallel. Even if the number of rows in sharded tables reaches a million level, the precheck can be completed in minutes.

To specify the number of threads for the precheck, you can configure the `threads` argument of the `mydumpers` field in the migration task configuration file.

```yaml
mydumpers:                           # Configuration arguments of the dump processing unit
  global:                            # Configuration name
    threads: 4                       # The number of threads that access the upstream when the dump processing unit performs the precheck and exports data from the upstream database (4 by default)
    chunk-filesize: 64               # The size of the files generated by the dump processing unit (64 MB by default)
    extra-args: "--consistency none" # Other arguments of the dump processing unit. You do not need to manually configure table-list in `extra-args`, because it is automatically generated by DM.

```

> **Note:**
>
> The value of `threads` determines the number of physical connections between the upstream database and DM. An excessively large `threads` value might increase the load of the upstream. Therefore, you need to set `threads` to a proper value.
