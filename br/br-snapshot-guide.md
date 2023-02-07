---
title: Snapshot Backup and Restore Guide
summary: Learn about how to back up and restore TiDB snapshots using the br command-line tool.
aliases: ['/tidb/dev/br-usage-backup/','/tidb/dev/br-usage-restore/','/tidb/dev/br-usage-restore-for-maintain/', '/tidb/dev/br-usage-backup-for-maintain/']
---

# Snapshot Backup and Restore Guide

This document describes how to back up and restore TiDB snapshots using the br command-line tool (hereinafter referred to as `br`). Before backing up and restoring data, you need to [install the br command-line tool](/br/br-use-overview.md#deploy-and-use-br) first.

Snapshot backup is an implementation to back up the entire cluster. It is based on [multi-version concurrency control (MVCC)](/tidb-storage.md#mvcc) and backs up all data in the specified snapshot to a target storage. The size of the backup data is approximately the size of the compressed single replica in the cluster. After the backup is completed, you can restore the backup data to an empty cluster or a cluster that does not contain conflict data (with the same schema or same tables), restore the cluster to the time point of the snapshot backup, and restore multiple replicas according to the cluster replica settings.

Besides basic backup and restore, snapshot backup and restore also provides the following features:

* [Backup data of a specified time point](#back-up-cluster-snapshots)
* [Restore data of a specified database or table](#restore-a-database-or-a-table)

## Back up cluster snapshots

> **Note:**
>
> - The following examples assume that Amazon S3 access keys and secret keys are used to authorize permissions. If IAM roles are used to authorize permissions, you need to set `--send-credentials-to-tikv` to `false`.
> - If other storage systems or authorization methods are used to authorize permissions, adjust the parameter settings according to [Backup Storages](/br/backup-and-restore-storages.md).

You can back up a TiDB cluster snapshot by running the `br backup full` command. Run `br backup full --help` to see the help information:

```shell
tiup br backup full --pd "${PD_IP}:2379" \
    --backupts '2022-09-08 13:30:00' \
    --storage "s3://backup-101/snapshot-202209081330?access-key=${access-key}&secret-access-key=${secret-access-key}" \
    --ratelimit 128 \
```

In the preceding command:

- `--backupts`: The time point of the snapshot. The format can be [TSO](/glossary.md#tso) or timestamp, such as `400036290571534337` or `2018-05-11 01:42:23`. If the data of this snapshot is garbage collected, the `br backup` command returns an error and `br` exits. If you leave this parameter unspecified, `br` picks the snapshot corresponding to the backup start time.
- `--storage`: The storage address of the backup data. Snapshot backup supports Amazon S3, Google Cloud Storage, and Azure Blob Storage as backup storage. The preceding command uses Amazon S3 as an example. For more details, see [URL format of backup storages](/br/backup-and-restore-storages.md#url-format).
- `--ratelimit`: The maximum speed **per TiKV** performing backup tasks. The unit is in MiB/s.

During backup, a progress bar is displayed in the terminal as shown below. When the progress bar advances to 100%, the backup task is completed and statistics such as total backup time, average backup speed, and backup data size are displayed.

```shell
Full Backup <-------------------------------------------------------------------------------> 100.00%
Checksum <----------------------------------------------------------------------------------> 100.00%
*** ["Full Backup success summary"] *** [backup-checksum=3.597416ms] [backup-fast-checksum=2.36975ms] *** [total-take=4.715509333s] [BackupTS=435844546560000000] [total-kv=1131] [total-kv-size=250kB] [average-speed=53.02kB/s] [backup-data-size(after-compressed)=71.33kB] [Size=71330]
```

## Get the backup time point of a snapshot backup

To manage a lot of backups, if you need to get the physical time of a snapshot backup, you can run the following command:

```shell
tiup br validate decode --field="end-version" \
--storage "s3://backup-101/snapshot-202209081330?access-key=${access-key}&secret-access-key=${secret-access-key}" | tail -n1
```

The output is as follows, corresponding to the physical time `2022-09-08 13:30:00 +0800 CST`:

```
435844546560000000
```

## Restore cluster snapshots

You can restore a snapshot backup by running the `br restore full` command. Run `br restore full --help` to see the help information:

The following example restores the [preceding backup snapshot](#back-up-cluster-snapshots) to a target cluster:

```shell
tiup br restore full --pd "${PD_IP}:2379" \
--storage "s3://backup-101/snapshot-202209081330?access-key=${access-key}&secret-access-key=${secret-access-key}"
```

During restore, a progress bar is displayed in the terminal as shown below. When the progress bar advances to 100%, the restore task is completed and statistics such as total restore time, average restore speed, and total data size are displayed.

```shell
Full Restore <------------------------------------------------------------------------------> 100.00%
*** ["Full Restore success summary"] *** [total-take=4.344617542s] [total-kv=5] [total-kv-size=327B] [average-speed=75.27B/s] [restore-data-size(after-compressed)=4.813kB] [Size=4813] [BackupTS=435844901803917314]
```

### Restore a database or a table

BR supports restoring partial data of a specified database or table from backup data. This feature allows you to filter out unwanted data and back up only a specific database or table.

**Restore a database**

To restore a database to a cluster, run the `br restore db` command. The following example restores the `test` database from the backup data to the target cluster:

```shell
tiup br restore db \
--pd "${PD_IP}:2379" \
--db "test" \
--storage "s3://backup-101/snapshot-202209081330?access-key=${access-key}&secret-access-key=${secret-access-key}"
```

In the preceding command, `--db` specifies the name of the database to be restored.

**Restore a table**

To restore a single table to a cluster, run the `br restore table` command. The following example restores the `test.usertable` table from the backup data to the target cluster:

```shell
tiup br restore table --pd "${PD_IP}:2379" \
--db "test" \
--table "usertable" \
--storage "s3://backup-101/snapshot-202209081330?access-key=${access-key}&secret-access-key=${secret-access-key}"
```

In the preceding command, `--db` specifies the name of the database to be restored, and `--table` specifies the name of the table to be restored.

**Restore multiple tables with table filter**

To restore multiple tables with more complex filter rules, run the `br restore full` command and specify the [table filters](/table-filter.md) with `--filter` or `-f`. The following example restores tables that match the `db*.tbl*` filter rule from the backup data to the target cluster:

```shell
tiup br restore full \
--pd "${PD_IP}:2379" \
--filter 'db*.tbl*' \
--storage "s3://backup-101/snapshot-202209081330?access-key=${access-key}&secret-access-key=${secret-access-key}"
```

### Restore tables in the `mysql` schema

Starting from BR v5.1.0, when you back up snapshots, BR backs up the **system tables** in the `mysql` schema and does not restore them by default. Starting from BR v6.2.0, BR restores **data in some system tables** if you configure `--with-sys-table`.

**BR can restore data in the following system tables:**

```
+----------------------------------+
| mysql.columns_priv               |
| mysql.db                         |
| mysql.default_roles              |
| mysql.global_grants              |
| mysql.global_priv                |
| mysql.role_edges                 |
| mysql.tables_priv                |
| mysql.user                       |
+----------------------------------+
```

**BR does not restore the following system tables:**

- Statistics tables (`mysql.stats_*`)
- System variable tables (`mysql.tidb` and `mysql.global_variables`)
- [Other system tables](https://github.com/pingcap/tidb/blob/master/br/pkg/restore/systable_restore.go#L31)

When you restore data related to system privilege, note the following:

- BR does not restore user data with `user` as `cloud_admin` and `host` as `'%'`. This user is reserved for TiDB Cloud. Do not create a user or role named `cloud_admin` in your cluster, because the user privileges related to `cloud_admin` cannot be restored correctly.
- Before restoring data, BR checks whether the system tables in the target cluster are compatible with those in the backup data. "Compatible" means that all the following conditions are met:

    - The target cluster has the same system tables as the backup data.
    - The **number of columns** in the system privilege table of the target cluster is the same as that in the backup data. The column order is not important.
    - The columns in the system privilege table of the target cluster are compatible with that in the backup data. If the data type of the column is a type with a length (such as integer and string), the length in the target cluster must be >= the length in the backup data. If the data type of the column is an `ENUM` type, the number of `ENUM` values in the target cluster must be a superset of that in the backup data.

## Performance and impact

### Performance and impact of snapshot backup

The backup feature has some impact on cluster performance (transaction latency and QPS). However, you can mitigate the impact by adjusting the number of backup threads [`backup.num-threads`](/tikv-configuration-file.md#num-threads-1) or by adding more clusters.

To illustrate the impact of backup, this document lists the test conclusions of several snapshot backup tests:

- (5.3.0 and earlier) When the backup threads of BR on a TiKV node take up 75% of the total CPU of the node, the QPS is reduced by 35% of the original QPS.
- (5.4.0 and later) When there are no more than `8` threads of BR on a TiKV node and the cluster's total CPU utilization does not exceed 80%, the impact of BR tasks on the cluster (write and read) is 20% at most.
- (5.4.0 and later) When there are no more than `8` threads of BR on a TiKV node and the cluster's total CPU utilization does not exceed 75%, the impact of BR tasks on the cluster (write and read) is 10% at most.
- (5.4.0 and later) When there are no more than `8` threads of BR on a TiKV node and the cluster's total CPU utilization does not exceed 60%, BR tasks have little impact on the cluster (write and read).

You can use the following methods to manually control the impact of backup tasks on cluster performance. However, these two methods also reduce the speed of backup tasks while reducing the impact of backup tasks on the cluster.

- Use the `--ratelimit` parameter to limit the speed of backup tasks. Note that this parameter limits the speed of **saving backup files to external storage**. When calculating the total size of backup files, use the `backup data size(after compressed)` as a benchmark.
- Adjust the TiKV configuration item [`backup.num-threads`](/tikv-configuration-file.md#num-threads-1) to limit the number of threads used by backup tasks. According to internal tests, when BR uses no more than `8` threads for backup tasks, and the total CPU utilization of the cluster does not exceed 60%, the backup tasks have little impact on the cluster, regardless of the read and write workload.

The impact of backup on cluster performance can be reduced by limiting the backup threads number, but this affects the backup performance. The preceding tests show that the backup speed is proportional to the number of backup threads. When the number of threads is small, the backup speed is about 20 MiB/thread. For example, 5 backup threads on a single TiKV node can reach a backup speed of 100 MiB/s.

### Performance and impact of snapshot restore

- During data restore, TiDB tries to fully utilize the TiKV CPU, disk IO, and network bandwidth resources. Therefore, it is recommended to restore the backup data on an empty cluster to avoid affecting the running applications.
- The speed of restoring backup data is much related with the cluster configuration, deployment, and running applications. In internal tests, the restore speed of a single TiKV node can reach 100 MiB/s. The performance and impact of snapshot restore are varied in different user scenarios and should be tested in actual environments.

## See also

* [TiDB Backup and Restore Use Cases](/br/backup-and-restore-use-cases.md)
* [br Command-line Manual](/br/use-br-command-line-tool.md)
* [TiDB Snapshot Backup and Restore Architecture](/br/br-snapshot-architecture.md)
