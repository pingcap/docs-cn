---
title: Point-in-Time Recovery
summary: Learn the design, capabilities, and architecture of Point-in-Time Recovery (PITR).
---

# Point-in-Time Recovery

Point-in-Time Recovery (PITR) allows you to restore a snapshot of a TiDB cluster to a new cluster from any given time point in the past. In v6.2.0, TiDB introduces PITR in [Backup & Restore](/br/backup-and-restore-overview.md) (BR).

You can use PITR to meet the following business requirements:

- Reduce the Recovery Point Objective (RPO) of disaster recovery to less than 20 minutes.
- Handle the cases of incorrect writes from applications by rolling back data to a time point before the error event.
- Perform history data auditing to meet the requirements of laws and regulations.

This document introduces the design, capabilities, and architecture of PITR. If you need to learn how to use PITR, refer to [PITR Usage Scenarios](/br/pitr-usage.md).

## Use PITR in your business

[BR](/br/backup-and-restore-overview.md) provides the PITR feature. With BR, you can perform all operations of PITR, including data backup (snapshot backup and log backup), one-click restoration to a specified time point, and backup data management.

The following are the procedures of using PITR in your business:

![Point-in-Time Recovery](/media/br/pitr-usage.png)

### Back up data

To achieve PITR, you need to perform the following backup tasks:

- Start a log backup task. You can run the `br log start` command to start a log backup task. This task runs in the background of your TiDB cluster and automatically backs up the change log of KV storage to the backup storage.
- Perform [snapshot (full) backup](/br/br-usage-backup.md#back-up-tidb-cluster-snapshots) regularly. You can run the `br backup full` command to back up the cluster snapshot to the backup storage at a specified time point, for example, 00:00 every day.

### Restore data with one click

To restore data using PITR, you need to run the `br restore point` command to execute the restoration program. The program reads data from snapshot backup and log backup and restores the data of the specified time point to a new cluster.

When you run the `br restore point` command, you need to specify the latest snapshot backup data before the time point you want to restore and specify the log backup data. BR first restores the snapshot data, and then reads the log backup data between the snapshot time point and the specified restoration time point.

### Manage backup data

To manage backup data for PITR, you need to design a backup directory structure to store your backup data and regularly delete outdated or no longer needed backup data.

- Organize the backup data in the following structure:

    - Store the snapshot backup and log backup in the same directory for unified management. For example, `backup-${cluster-id}`.
    - Store each snapshot backup in a directory whose name includes the backup date. For example, `backup-${cluster-id}/snapshot-20220512000130`.
    - Store the log backup in a fixed directory. For example, `backup-${cluster-id}/log-backup`.

- Delete the outdated or no longer needed backup data:

    - When you delete the snapshot backup, you can delete the directory of the snapshot backup.
    - To delete the log backup before a specified time point, run the `br log truncate` command.

## Capabilities

- PITR log backup has a 5% impact on the cluster.
- When you back up logs and snapshots at the same time, it has a less than 20% impact on the cluster.
- On each TiKV node, PITR can restore snapshot data at 280 GB/h and log data at 30 GB/h.
- With PITR, the RPO of disaster recovery is less than 20 minutes. Depending on the data size to be restored, the Recovery Time Objective (RTO) varies from several minutes to several hours.
- BR deletes outdated log backup data at a speed of 600 GB/h.

> **Note:**
>
> - The preceding functional specification is based on test results from the following two testing scenarios. The actual data may be different.
> - Snapshot data restoration speed = Snapshot data size / (duration * the number of TiKV nodes)
> - Log data restoration speed = Restored log data size / (duration * the number of TiKV nodes)

Testing scenario 1 (on [TiDB Cloud](https://tidbcloud.com)):

- The number of TiKV nodes (8 core, 16 GB memory): 21
- The number of Regions: 183,000
- New log created in the cluster: 10 GB/h
- Write (insert/update/delete) QPS: 10,000

Testing scenario 2 (on-premises):

- The number of TiKV nodes (8 core, 64 GB memory): 6
- The number of Regions: 50,000
- New log created in the cluster: 10 GB/h
- Write (insert/update/delete) QPS: 10,000

## Limitations

- A single cluster can only run one log backup task.
- You can only restore data to an empty cluster. To avoid impact on the services and data of the cluster, do not perform PITR in-place or on a non-empty cluster.
- You can use Amazon S3 or a shared filesystem (such as NFS) to store the backup data. Currently, GCS and Azure Blob Storage are not supported.
- You can only perform cluster-level PITR. Database-level and table-level PITR are not supported.
- You cannot restore data in the user tables or the privilege tables.
- If the backup cluster has a TiFlash replica, after you perform PITR, the restoration cluster does not contain the data in the TiFlash replica. To restore data from the TiFlash replica, you need to [manually configure the TiFlash replica in the schema or the table](/br/pitr-troubleshoot.md#after-restoring-a-downstream-cluster-using-the-br-restore-point-command-data-cannot-be-accessed-from-tiflash-what-should-i-do).
- If the upstream database uses TiDB Lightning's physical import mode to import data, the data cannot be backed up in log backup. It is recommended to perform a full backup after the data import. For details, refer to [The upstream database uses TiDB Lightning Physical Mode to import data](/br/pitr-known-issues.md#the-upstream-database-imports-data-using-tidb-lightning-in-the-physical-import-mode-which-makes-it-impossible-to-use-the-log-backup-feature).
- During the backup process, do not exchange partition. For details, refer to [Executing the Exchange Partition DDL during PITR recovery](/br/pitr-troubleshoot.md#what-should-i-do-if-an-error-occurs-when-executing-the-exchange-partition-ddl-during-pitr-log-restoration).
- Do not restore the log backup data of a certain time period repeatedly. If you restore the log backup data of a range `[t1=10, t2=20)` repeatedly, the restored data might be inconsistent.
- For other known limitations, refer to [PITR Known Issues](/br/pitr-known-issues.md).
