---
title: Precheck the Upstream MySQL Instance Configurations
summary: Learn how to use the precheck feature provided by DM to detect errors in the upstream MySQL instance configurations.
aliases: ['/docs/tidb-data-migration/dev/precheck/']
---

# Precheck the Upstream MySQL Instance Configurations

This document introduces the precheck feature provided by DM. This feature is used to detect possible errors in the upstream MySQL instance configuration when the data migration task is started.

## Command

`check-task` allows you to precheck whether the upstream MySQL instance configuration satisfies the DM requirements.

## Checking items

Upstream and downstream database users must have the corresponding read and write privileges. DM checks the following privileges and configuration automatically while the data migration task is started:

+ Database version

    - MySQL version > 5.5
    - MariaDB version >= 10.1.2

    > **Warning:**
    >
    > Support for MySQL 8.0 is an experimental feature of TiDB Data Migration v2.0 and later versions. It is **NOT** recommended that you use it in a production environment.

+ Database configuration

    - Whether `server_id` is configured

+ MySQL binlog configuration

    - Whether the binlog is enabled (DM requires that the binlog must be enabled)
    - Whether `binlog_format=ROW` (DM only supports migration of the binlog in the ROW format)
    - Whether `binlog_row_image=FULL` (DM only supports `binlog_row_image=FULL`)

+ The privileges of the upstream MySQL instance users

    MySQL users in DM configuration need to have the following privileges at least:

    - REPLICATION SLAVE
    - REPLICATION CLIENT
    - RELOAD
    - SELECT

+ The compatibility of the upstream MySQL table schema

    TiDB differs from MySQL in compatibility in the following aspects:

    - TiDB does not support the foreign key.
    - [Character set compatibility differs](/character-set-and-collation.md).

    DM will also check whether the primary key or unique key restriction exists in all upstream tables. This check is introduced in v1.0.7.

+ The consistency of the sharded tables in the multiple upstream MySQL instances

    + The schema consistency of all sharded tables

        - Column size
        - Column name
        - Column position
        - Column type
        - Primary key
        - Unique index

    + The conflict of the auto increment primary keys in the sharded tables

        - The check fails in the following two conditions:

            - The auto increment primary key exists in the sharded tables and its column type *is not* bigint.
            - The auto increment primary key exists in the sharded tables and its column type *is* bigint, but column mapping *is not* configured.

        - The check succeeds in other conditions except the two above.

### Disable checking items

DM checks items according to the task type, and you can use `ignore-checking-items` in the task configuration file to disable checking items. The list of element options for `ignore-checking-items` is as follows:

| Element  | Description   |
| :----  | :-----|
| all | Disables all checks |
| dump_privilege | Disables checking dump-related privileges of the upstream MySQL instance user |
| replication_privilege | Disables checking replication-related privileges of the upstream MySQL instance user |
| version | Disables checking the upstream database version |
| server_id | Disables checking the upstream database server_id |
| binlog_enable | Disables checking whether the upstream database has binlog enabled |
| binlog_format | Disables checking whether the binlog format of the upstream database is ROW |
| binlog_row_image |  Disables checking whether the binlog_row_image of the upstream database is FULL |
| table_schema | Disables checking the compatibility of the upstream MySQL table schema |
| schema_of_shard_tables | Disables checking whether the schemas of upstream MySQL sharded tables are consistent in the multi-instance sharding scenario |
| auto_increment_ID | Disables checking the conflicts of auto-increment primary keys of the upstream MySQL shared tables in the multi-instance sharding scenario |
