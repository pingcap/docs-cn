---
title: Use BR to Back Up Cluster Data
summary: Learn how to back up data using BR commands
---

# Use BR to Back Up Cluster Data

This document describes how to back up cluster data using BR in the following scenarios:

- [Back up TiDB cluster snapshots](#back-up-tidb-cluster-snapshots)
- [Back up a database](#back-up-a-database)
- [Back up a table](#back-up-a-table)
- [Back up multiple tables with table filter](#back-up-multiple-tables-with-table-filter)
- [Back up data to external storage](#back-up-data-to-external-storage)
- [Back up incremental data](#back-up-incremental-data)
- [Encrypt backup data](#encrypt-backup-data)

If you are not familiar with Backup & Restore (BR), it is recommended that you read the following documents to fully understand BR usage principles and methods:

- [BR Overview](/br/backup-and-restore-overview.md)
- [Use BR Command-line for Backup and Restoration](/br/use-br-command-line-tool.md)

## Back up TiDB cluster snapshots

A snapshot of a TiDB cluster contains only the latest and transactionally consistent data at a specific time. You can back up the latest or specified snapshot data of a TiDB cluster by running the `br backup full` command. To get help on this command, run the `br backup full --help` command.

Example: Back up the snapshot generated at `2022-01-30 07:42:23` to the `2022-01-30/` directory in the `backup-data` bucket of Amazon S3.

{{< copyable "shell-regular" >}}

```shell
br backup full \
    --pd "${PDIP}:2379" \
    --backupts '2022-01-30 07:42:23' \
    --storage "s3://backup-data/2022-01-30/" \
    --ratelimit 128 \
    --log-file backupfull.log
```

In the preceding command:

- `--backupts`: The physical time of the snapshot. If data of this snapshot is processed by Garbage Collection (GC), the `br backup` command will exit with an error. If you leave this parameter unspecified, BR picks the snapshot corresponding to the backup start time.
- `--ratelimit`: The maximum speed **per TiKV** performing backup tasks (in MiB/s).
- `--log-file`: The target file for BR logging.

During backup, a progress bar is displayed in the terminal, as shown below. When the progress bar advances to 100%, the backup is complete.

```shell
br backup full \
    --pd "${PDIP}:2379" \
    --storage "s3://backup-data/2022-01-30/" \
    --ratelimit 128 \
    --log-file backupfull.log
Full Backup <---------/................................................> 17.12%.
```

After the backup is completed, BR compares the checksum of the backup data with the [admin checksum table](/sql-statements/sql-statement-admin-checksum-table.md) of the cluster to ensure data correctness and security.

## Back up a database or a table

BR supports backing up partial data of a specified database or table from a cluster snapshot or incremental data backup. This feature allows you to filter out unwanted data from snapshot backup and incremental data backup, and back up only business-critical data.

### Back up a database

To back up a database in a cluster, run the `br backup db` command. To get help on this command, run the `br backup db --help` command.

Example: Back up the `test` database to the `db-test/2022-01-30/` directory in the `backup-data` bucket of Amazon S3.

{{< copyable "shell-regular" >}}

```shell
br backup db \
    --pd "${PDIP}:2379" \
    --db test \
    --storage "s3://backup-data/db-test/2022-01-30/" \
    --ratelimit 128 \
    --log-file backuptable.log
```

In the preceding command, `--db` specifies the database name, and other parameters are the same as those in [Back up TiDB cluster snapshots](#back-up-tidb-cluster-snapshots).

### Back up a table

To back up a table in a cluster, run the `br backup table` command. To get help on this command, run the `br backup table --help` command.

Example: Back up `test.usertable` to the `table-db-usertable/2022-01-30/` directory in the `backup-data` bucket of Amazon S3.

{{< copyable "shell-regular" >}}

```shell
br backup table \
    --pd "${PDIP}:2379" \
    --db test \
    --table usertable \
    --storage "s3://backup-data/table-db-usertable/2022-01-30/" \
    --ratelimit 128 \
    --log-file backuptable.log
```

In the preceding command, `--db` and `--table` specify the database name and table name respectively, and other parameters are the same as those in [Back up TiDB cluster snapshots](#back-up-tidb-cluster-snapshots).

### Back up multiple tables with table filter

To back up multiple tables with more criteria, run the `br backup full` command and specify the [table filters](/table-filter.md) with `--filter` or `-f`.

Example: Back up `db*.tbl*` data of a table to  the `table-filter/2022-01-30/` directory in the `backup-data` bucket of Amazon S3.

{{< copyable "shell-regular" >}}

```shell
br backup full \
    --pd "${PDIP}:2379" \
    --filter 'db*.tbl*' \
    --storage "s3://backup-data/table-filter/2022-01-30/" \
    --ratelimit 128 \
    --log-file backupfull.log
```

## Back up data to external storage

BR supports backing up data to Amazon S3, Google Cloud Storage (GCS), Azure Blob Storage, NFS, or other S3-compatible file storage services. For details, see the following documents:

- [Back up data on Amazon S3 using BR](/br/backup-storage-S3.md)
- [Back up data on Google Cloud Storage using BR](/br/backup-storage-gcs.md)
- [Back up data on Azure Blob Storage using BR](/br/backup-storage-azblob.md)

## Back up incremental data

> **Warning:**
>
> This is still an experimental feature. It is **NOT** recommended that you use it in the production environment.

Incremental data of a TiDB cluster is differentiated data between the snapshot of a starting point and that of an end point. Compared with snapshot data, incremental data is smaller and therefore it is a supplementary to snapshot backup, which reduces the volume of backup data.

To back up incremental data, run the `br backup` command with **the last backup timestamp** `--lastbackupts` specified. To get `--lastbackupts`, run the `validate` command. The following is an example:

{{< copyable "shell-regular" >}}

```shell
LAST_BACKUP_TS=`br validate decode --field="end-version" -s s3://backup-data/2022-01-30/ | tail -n1`
```

> **Note:**
>
> - You need to save the incremental backup data under a different path from the previous snapshot backup.
> - GC safepoint must be prior to `lastbackupts`. The defalt GC lifetime is 10 minutes in TiDB, which means that TiDB only backs up incremental data generated in the last 10 minutes. To back up earlier incremental data, you need to [adjust TiDB GC Lifetime setting](/system-variables.md#tidb_gc_life_time-new-in-v50).

{{< copyable "shell-regular" >}}

```shell
br backup full\
    --pd ${PDIP}:2379 \
    --ratelimit 128 \
    --storage "s3://backup-data/2022-01-30/incr" \
    --lastbackupts ${LAST_BACKUP_TS}
```

The preceding command backs up the incremental data between `(LAST_BACKUP_TS, current PD timestamp]` and the DDLs generated during this time period. When restoring incremental data, BR restores all DDLs first, and then restores data.

## Encrypt backup data

> **Warning:**
>
> This is still an experimental feature. It is **NOT** recommended that you use it in the production environment.

BR supports encrypting backup data at the backup end and at the storage end when backing up to Amazon S3. You can choose either encryption method as required.

### Encrypt backup data at the backup end

Since TiDB v5.3.0, you can encrypt backup data by configuring the following parameters:

- `--crypter.method`: Encryption algorithm, which can be `aes128-ctr`, `aes192-ctr`, or `aes256-ctr`. The default value is `plaintext`, indicating that data is not encrypted.
- `--crypter.key`: Encryption key in hexadecimal string format. It is a  128-bit (16 bytes) key for the algorithm `aes128-ctr`, 24-byte key for the algorithm `aes192-ctr`, and 32-byte key for the algorithm `aes256-ctr`.
- `--crypter.key-file`: The key file. You can directly pass in the file path where the key is stored as a parameter without passing in "crypter.key".

Example: Encrypt backup data at the backup end.

{{< copyable "shell-regular" >}}

```shell
br backup full\
    --pd ${PDIP}:2379 \
    --storage "s3://backup-data/2022-01-30/"  \
    --crypter.method aes128-ctr \
    --crypter.key 0123456789abcdef0123456789abcdef
```

> **Note:**
>
> - If the key is lost, the backup data cannot be restored to the cluster.
> - The encryption feature needs to be used on BR tools and TiDB clusters v5.3.0 or later versions. The encrypted backup data cannot be restored on clusters earlier than v5.3.0.

### Encrypt backup data when backing up to Amazon S3

BR supports server-side encryption (SSE) when backing up data to S3. In this scenario, you can use AWS KMS keys you have created to encrypt data. For details, see [BR S3 server-side encryption](/encryption-at-rest.md#br-s3-server-side-encryption).

## Backup performance and impact

The backup feature has some impact on cluster performance (transaction latency and QPS). However, you can mitigate the impact by adjusting the number of backup threads [`backup.num-threads`](/tikv-configuration-file.md#num-threads-1) or by adding more clusters.

To illustrate the impact of backup, this document lists the test conclusions of several snapshot backup tests:

- (5.3.0 and earlier) When the backup threads of BR on a TiKV node takes up 75% of the total CPU of the node, the QPS is reduced by 30% of the original QPS.
- (5.4.0 and later) When there are no more than `8` threads of BR on a TiKV node and the cluster's total CPU utilization does not exceed 80%, the impact of BR tasks on the cluster (write and read) is 20% at most.
- (5.4.0 and later) When there are no more than `8` threads of BR on a TiKV node and the cluster's total CPU utilization does not exceed 75%, the impact of BR tasks on the cluster (write and read) is 10% at most.
- (5.4.0 and later) When there are no more than `8` threads of BR on a TiKV node and the cluster's total CPU utilization does not exceed 60%, BR tasks has little impact on the cluster (write and read).

You can mitigate impact on cluster performance by reducing the number of backup threads. However, this might cause backup performance to deteriorate. Based on the preceding test results: (On a single TiKV node) the backup speed is proportional to the number of backup threads. When the number of threads is small, the backup speed is about 20 MB/thread. For example, a single node with 5 backup threads can deliver a backup speed of 100 MB/s.

> **Note:**
>
> The impact and speed of backup depends much on cluser configuration, deployment, and running services. The preceding test conclusions, based on simulation tests in many scenarios and verified in some customer sites, are worthy of reference. However, the exact impact and performance cap may vary depending on the scenarios. Therefore, you should always run the test and verify the test results.

 Since v5.3.0, BR introduces the auto tunning feature (enabled by default) to adjust the number of backup threads. It can maintain the CPU utilization of the cluster below 80% during backup tasks. For details, see [BR Auto-Tune](/br/br-auto-tune.md).
