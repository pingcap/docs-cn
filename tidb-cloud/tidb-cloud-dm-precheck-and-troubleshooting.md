---
title: Precheck Errors, Migration Errors, and Alerts for Data Migration
summary: Learn how to resolve precheck errors, migration errors, and alerts when using Data Migration.
---

# Precheck Errors, Migration Errors, and Alerts for Data Migration

This document describes how to resolve precheck errors, troubleshoot migration errors, and subscribe to alerts when you [use Data Migration to migrate data](/tidb-cloud/migrate-from-mysql-using-data-migration.md). 

## Precheck errors and solutions

This section describes the precheck errors and corresponding solutions during data migration. These errors are shown on the **Precheck** page when you [migrate data using Data Migration](/tidb-cloud/migrate-from-mysql-using-data-migration.md).

The solutions vary depending on your upstream database.

### Error message: Check whether mysql server_id has been greater than 0

- Amazon Aurora MySQL or Amazon RDS: `server_id` is configured by default. You do not need to configure it. Make sure you are using Amazon Aurora MySQL writer instances to support both full and incremental data migration.
- MySQL: to configure `server_id` for MySQL, see [Setting the Replication Source Configuration](https://dev.mysql.com/doc/refman/8.0/en/replication-howto-masterbaseconfig.html).

### Error message: Check whether mysql binlog is enabled

- Amazon Aurora MySQL: see [How do I turn on binary logging for my Amazon Aurora MySQL-Compatible cluster](https://aws.amazon.com/premiumsupport/knowledge-center/enable-binary-logging-aurora/?nc1=h_ls). Make sure you are using Amazon Aurora MySQL writer instances to support both full and incremental data migration.
- Amazon RDS: see [Configuring MySQL binary logging](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_LogAccess.MySQL.BinaryFormat.html).
- Google Cloud SQL for MySQL: Google enables binary logging through point-in-time recovery for MySQL master databases. See [Enable point-in-time recovery](https://cloud.google.com/sql/docs/mysql/backup-recovery/pitr#enablingpitr).
- MySQL: see [Setting the Replication Source Configuration](https://dev.mysql.com/doc/refman/8.0/en/replication-howto-masterbaseconfig.html).

### Error message: Check whether mysql binlog_format is ROW

- Amazon Aurora MySQL: see [How do I turn on binary logging for my Amazon Aurora MySQL-Compatible cluster](https://aws.amazon.com/premiumsupport/knowledge-center/enable-binary-logging-aurora/?nc1=h_ls). Make sure you are using Amazon Aurora MySQL writer instances to support both full and incremental data migration.
- Amazon RDS: see [Configuring MySQL binary logging](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_LogAccess.MySQL.BinaryFormat.html).
- MySQL: execute `set global binlog_format=ROW;`. See [Setting The Binary Log Format](https://dev.mysql.com/doc/refman/8.0/en/binary-log-setting.html).

### Error message: Check whether mysql binlog_row_image is FULL

- Amazon Aurora MySQL: `binlog_row_image` is not configurable. This precheck item does not fail for it. Make sure you are using Amazon Aurora MySQL writer instances to support both full and incremental data migration.
- Amazon RDS: the process is similar to setting the `binlog_format` parameter. The only difference is that the parameter you need to change is `binlog_row_image` instead of `binlog_format`. See [Configuring MySQL binary logging](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_LogAccess.MySQL.BinaryFormat.html).
- MySQL: `set global binlog_row_image = FULL;`. See [Binary Logging Options and Variables](https://dev.mysql.com/doc/refman/8.0/en/replication-options-binary-log.html#sysvar_binlog_row_image).

### Error message: Check whether migrated dbs are in binlog_do_db/binlog_ignore_db

Make sure that binlog has been enabled in the upstream database. See [Check whether mysql binlog is enabled](#error-message-check-whether-mysql-binlog-is-enabled). After that, resolve the issue according to the message you get:

- If the message is similar to `These dbs xxx are not in binlog_do_db xxx`, make sure all the databases that you want to migrate are in the list. See [--binlog-do-db=db_name](https://dev.mysql.com/doc/refman/8.0/en/replication-options-binary-log.html#option_mysqld_binlog-do-db).
- If the message is similar to `These dbs xxx are in binlog_ignore_db xxx`, make sure all the databases that you want to migrate are not in the ignore list. See [--binlog-ignore-db=db_name](https://dev.mysql.com/doc/refman/8.0/en/replication-options-binary-log.html#option_mysqld_binlog-ignore-db).

For Amazon Aurora MySQL, this precheck item does not fail for it. Make sure you are using Amazon Aurora MySQL writer instances to support both full and incremental data migration.

For Amazon RDS, you need to change the following parameters: `replicate-do-db`, `replicate-do-table`, `replicate-ignore-db`, and `replicate-ignore-table`. See [Configuring MySQL binary logging](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_LogAccess.MySQL.BinaryFormat.html).

### Error message: Check if connection concurrency exceeds database's maximum connection limit

If the error occurs in the upstream database, set `max_connections` as follows:

- Amazon Aurora MySQL: the process is similar to setting the `binlog_format`. The only difference is that the parameter you change is `max_connections` instead of `binlog_format`. See [How do I turn on binary logging for my Amazon Aurora MySQL-Compatible cluster](https://aws.amazon.com/premiumsupport/knowledge-center/enable-binary-logging-aurora/?nc1=h_ls).
- Amazon RDS: the process is similar to setting the `binlog_format`. The only difference is that the parameter you change is `max_connections` instead of `binlog_format`.  See [Configuring MySQL binary logging](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_LogAccess.MySQL.BinaryFormat.html).
- MySQL: configure `max_connections` following the document [max_connections](https://dev.mysql.com/doc/refman/8.0/en/server-system-variables.html#sysvar_max_connections).

If the error occurs in the TiDB Cloud cluster, configure `max_connections` following the document [max_connections](https://docs.pingcap.com/tidb/stable/system-variables#max_connections).

## Migration errors and solutions

This section describes the problems and solutions you might encounter during the migration. These error messages are shown on the **Migration Job Details** page.

### Error message: "The required binary log for migration no longer exists on the source database. Please make sure binary log files are kept for long enough time for migration to succeed."

This error means that the binlogs to be migrated have been cleaned up and can only be restored by creating a new task.

Ensure that the binlogs required for incremental migration exist. It is recommended to configure `expire_logs_days` to extend the duration of binlogs. Do not use `purge binary log` to clean up binlogs if it's needed by some migration job.

### Error message: "Failed to connect to the source database using given parameters. Please make sure the source database is up and can be connected using the given parameters."

This error means that the connection to the source database failed. Check whether the source database is started and can be connected to using the specified parameters. After confirming that the source database is available, you can try to recover the task by clicking **Restart**.

### The migration task is interrupted and contains the error "driver: bad connection" or "invalid connection"

This error means that the connection to the downstream TiDB cluster failed. Check whether the downstream TiDB cluster is in a normal state (including `Available` and `Modifying`) and can be connected with the username and password specified by the job. After confirming that the downstream TiDB cluster is available, you can try to resume the task by clicking **Restart**.

### Error message: "Failed to connect to the TiDB cluster using the given user and password. Please make sure TiDB Cluster is up and can be connected to using the given user and password."

Failed to connect to the TiDB cluster. It is recommended to check whether the TiDB cluster is in a normal state (including `Available` and `Modifying`). You can connect with the username and password specified by the job. After confirming that the TiDB cluster is available, you can try to resume the task by clicking **Restart**.

### Error message: "TiDB cluster storage is not enough. Please increase the node storage of TiKV."

The TiDB cluster storage is running low. It is recommended to [increase the TiKV node storage](/tidb-cloud/scale-tidb-cluster.md#change-storage) and then resume the task by clicking **Restart**.

### Error message: "Failed to connect to the source database. Please check whether the database is available or the maximum connections have been reached."

Failed to connect to the source database. It is recommended to check whether the source database is started, the number of database connections has not reached the upper limit, and you can connect using the parameters specified by the job. After confirming that the source database is available, you can try to resume the job by clicking **Restart**.

## Alerts

You can subscribe to TiDB Cloud alert emails to be informed in time when an alert occurs.

The following are alerts about Data Migration: 

- "Data migration job met error during data export"

    Recommended action: check the error message on the data migration page, and see [Migration errors and solutions](#migration-errors-and-solutions) for help.

- "Data migration job met error during data import"

    Recommended action: check the error message on the data migration page, and see [Migration errors and solutions](#migration-errors-and-solutions) for help.

- "Data migration job met error during incremental data migration"

    Recommended action: check the error message on the data migration page, and see [Migration errors and solutions](#migration-errors-and-solutions) for help.

- "Data migration job has been paused for more than 6 hours during incremental migration" 

    Recommended action: resume the data migration job or ignore this alert.     

- "Replication lag is larger than 10 minutes and stilling increasing for more than 20 minutes"

    - Recommended action: contact [TiDB Cloud Support](/tidb-cloud/tidb-cloud-support.md) for help.

If you need help to address these alerts, contact [TiDB Cloud Support](/tidb-cloud/tidb-cloud-support.md) for consultation.

For more information about how to subscribe to alert emails, see [TiDB Cloud Built-in Alerting](/tidb-cloud/monitor-built-in-alerting.md).

## See also

- [Migrate MySQL-Compatible Databases to TiDB Cloud Using Data Migration](/tidb-cloud/migrate-from-mysql-using-data-migration.md)
