---
title: Use BR to Restore Cluster Data
summary: Learn how to restore data using BR commands
---

# Use BR to Restore Cluster Data

This document describes how to restore cluster data using BR in the following scenarios:

- [Restore TiDB cluster snapshots](#restore-tidb-cluster-snapshots)
- [Restore a database](#restore-a-database)
- [Restore a table](#restore-a-table)
- [Restore multiple tables with table filter](#restore-multiple-tables-with-table-filter)
- [Restore backup data from external storage](#restore-backup-data-from-external-storage)
- [Restore incremental data](#restore-incremental-data)
- [Restore encrypted backup data](#restore-encrypted-backup-data)
- [Restore tables created in the `mysql` schema](#restore-tables-created-in-the-mysql-schema)

If you are not familiar with Backup & Restore (BR), it is recommended that you read the following documents to fully understand BR usage principles and methods:

- [BR Overview](/br/backup-and-restore-overview.md)
- [Use BR Command-line for Backup and Restoration](/br/use-br-command-line-tool.md)

## Restore TiDB cluster snapshots

BR supports restoring snapshot backup on an empty cluster to restore the target cluster to the latest state when the snapshot is backed up.

Example: Restore the snapshot generated at `2022-01-30 07:42:23` from the `2022-01-30/` directory in the `backup-data` bucket of Amazon S3 to the target cluster.

{{< copyable "shell-regular" >}}

```shell
br restore full \
    --pd "${PDIP}:2379" \
    --storage "s3://backup-data/2022-01-30/" \
    --ratelimit 128 \
    --log-file restorefull.log
```

In the preceding command,

- `--ratelimit`: The maximum speed for **each TiKV** to perform a restoration task (unit: MiB/s)
- `--log-file` The target file for BR logging

During restoration, a progress bar is displayed in the terminal, as shown below. When the progress bar advances to 100%, the restoration is complete. To ensure data security, BR performs a check on the restored data.

```shell
br restore full \
    --pd "${PDIP}:2379" \
    --storage "s3://backup-data/2022-01-30/" \
    --ratelimit 128 \
    --log-file restorefull.log
Full Restore <---------/...............................................> 17.12%.
```

## Restore a database or a table

BR supports restoring partial data of a specified database or table from backup data. This feature allows you to filter out unwanted data and back up only a specific database or table.

### Restore a database

To restore a database to the cluster, run the `br restore db` command. To get help on this command, run the `br restore db --help` command.

Example: Restore the `test` database from the `db-test/2022-01-30/` directory in the `backup-data` bucket of Amazon S3 to the target cluster.

{{< copyable "shell-regular" >}}

```shell
br restore db \
    --pd "${PDIP}:2379" \
    --db "test" \
    --ratelimit 128 \
    --storage "s3://backup-data/db-test/2022-01-30/" \
    --log-file restore_db.log
```

In the preceding command, `--db` specifies the name of the database to be restored, and other parameters are the same as those in [Restore TiDB cluster snapshots](#restore-tidb-cluster-snapshots).

> **Note:**
>
> When you restore the backup data, the database name specified by `--db` must be the same as the one specified by `-- db` in the backup command. Otherwise, the restoration fails. This is because the metafile of the backup data ( `backupmeta` file) records the database name, and you can only restore data to the database with the same name. The recommended method is to restore the backup data to the database with the same name in another cluster.

### Restore a table

To restore a single table to the cluster, run the `br restore table` command. To get help on this command, run the `br restore table --help` command.

Example: Restore `test`.`usertable` from the `table-db-usertable/2022-01-30/`directory in the `backup-data` bucket of Amazon S3 to the target cluster.

{{< copyable "shell-regular" >}}

```shell
br restore table \
    --pd "${PDIP}:2379" \
    --db "test" \
    --table "usertable" \
    --ratelimit 128 \
    --storage "s3://backup-data/table-db-usertable/2022-01-30/" \
    --log-file restore_table.log
```

In the preceding command, `--table` specifies the name of the table to be restored, and other parameters are the same as those in [Restore TiDB cluster snapshots](#restore-tidb-cluster-snapshots).

### Restore multiple tables with table filter

To restore multiple tables with more criteria, run the `br restore full` command and specify the [table filters](/table-filter.md) with `--filter` or `-f`.

Example: Restore data matching the `db*.tbl*` table from the `table-filter/2022-01-30/` directory in the `backup-data` bucket of Amazon S3 to the target cluster.

{{< copyable "shell-regular" >}}

```shell
br restore full \
    --pd "${PDIP}:2379" \
    --filter 'db*.tbl*' \
    --storage "s3://backup-data/table-filter/2022-01-30/"  \
    --log-file restorefull.log
```

## Restore backup data from external storage

BR supports restoring data to Amazon S3, Google Cloud Storage (GCS), Azure Blob Storage, NFS, or other S3-compatible file storage services. For details, see the following documents:

- [Restore data on Amazon S3 using BR](/br/backup-storage-S3.md)
- [Restore data on Google Cloud Storage using BR](/br/backup-storage-gcs.md)
- [Restore data on Azure Blob Storage using BR](/br/backup-storage-azblob.md)

## Restore incremental data

> **Warning:**
>
> This is still an experimental feature. It is **NOT** recommended that you use it in the production environment.

Restoring incremental data is similar to restoring full data using BR. When restoring incremental data, make sure that all the data backed up before `last backup ts` has been restored to the target cluster. Also, because incremental restoration updates ts data, you need to ensure that there are no other writes during the restoration. Otherwise, conflicts might occur.

```shell
br restore full \
    --pd "${PDIP}:2379" \
    --storage "s3://backup-data/2022-01-30/incr"  \
    --ratelimit 128 \
    --log-file restorefull.log
```

## Restore encrypted backup data

> **Warning:**
>
> This is still an experimental feature. It is **NOT** recommended that you use it in the production environment.

After encrypting the backup data, you need to pass in the corresponding decryption parameters to restore the data. Ensure that the decryption algorithm and key are correct. If the decryption algorithm or key is incorrect, the data cannot be restored.

{{< copyable "shell-regular" >}}

```shell
br restore full\
    --pd ${PDIP}:2379 \
    --storage "s3://backup-data/2022-01-30/" \
    --crypter.method aes128-ctr \
    --crypter.key 0123456789abcdef0123456789abcdef
```

## Restore tables created in the `mysql` schema

> **Warning:**
>
> This is still an experimental feature. It is **NOT** recommended that you use it in the production environment.

BR backs up tables created in the `mysql` schema by default. When you restore data using BR, the tables created in the `mysql` schema are not restored by default. To restore these tables, you can explicitly include them using the [table filter](/table-filter.md#syntax). The following example restores `mysql.usertable` created in the `mysql` schema. The command restores `mysql.usertable` along with other data.

{{< copyable "shell-regular" >}}

```shell
br restore full -f '*.*' -f '!mysql.*' -f 'mysql.usertable' -s $external_storage_url --ratelimit 128
```

In the preceding command,

- `-f '*.*'` is used to override the default rules
- `-f '!mysql.*'` instructs BR not to restore tables in `mysql` unless otherwise stated.
- `-f 'mysql.usertable'` indicates that `mysql.usertable` should be restored.

If you only need to restore `mysql.usertable`, run the following command:

{{< copyable "shell-regular" >}}

```shell
br restore full -f 'mysql.usertable' -s $external_storage_url --ratelimit 128
```

> **Warning:**
>
> Although you can back up system tables (such as `mysql.tidb`) using BR, BR ignores the following system tables even if you use the --filter setting to perform the restoration:
>
> - Statistical information tables (`mysql.stat_*`)
> - System variable tables (`mysql.tidb`, `mysql.global_variables`)
> - User information tables (such as `mysql.user` and `mysql.columns_priv`)
> - [Other system tables](https://github.com/pingcap/tidb/blob/master/br/pkg/restore/systable_restore.go#L31)
>
> Compatibility issues might occur when restoring system tables. Therefore, avoid restoring system tables in production environments.

## Restoration performance and impact

- TiDB fully uses TiKV CPU, disk IO, network bandwidth, and other resources when restoring data. Therefore, it is recommended that you restore backup data on an empty cluster to avoid affecting running services.
- The restoration speed depends much on cluser configuration, deployment, and running services. Generally, the restoration speed can reach 100 MB/s (per TiKV node).

> **Note:**
>
> The preceding test conclusions, based on simulation tests in many scenarios and verified in some customer sites, are worthy of reference. However, the restoration speed may vary depending on the scenarios. Therefore, you should always run the test and verify the test results.
