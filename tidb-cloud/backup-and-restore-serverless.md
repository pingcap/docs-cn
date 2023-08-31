---
title: Back Up and Restore TiDB Serverless Data
summary: Learn how to back up and restore your TiDB Serverless cluster.
aliases: ['/tidbcloud/restore-deleted-tidb-cluster']
---

# Back Up and Restore TiDB Serverless Data

This document describes how to back up and restore your TiDB Serverless cluster data on TiDB Cloud.

> **Tip:**
>
> To learn how to back up and restore TiDB Dedicated cluster data, see [Back Up and Restore TiDB Dedicated Data](/tidb-cloud/backup-and-restore.md).

## Limitations

- It is important to note that TiDB Serverless clusters only support in-place restoring from backups. When a restore is performed, tables in the `mysql` schema are also impacted. Hence, any changes made to user credentials and permissions or system variables will be rolled back to the state when the backup was taken.
- Manual backup is not yet supported.
- The cluster will be unavailable during the restore process, and existing connections will be terminated. You can establish new connections once the restore is complete.
- If any TiFlash replica is enabled, the replica will be unavailable for a while after the restore because data needs to be rebuilt in TiFlash.

## Backup

Automatic backups are scheduled for your TiDB Serverless clusters according to the backup setting, which can reduce your loss in extreme disaster situations.

### Automatic backup

By the automatic backup, you can back up the TiDB Serverless cluster data every day at the backup time you have set. To set the backup time, perform the following steps:

1. Navigate to the **Backup** page of a TiDB Serverless cluster.

2. Click **Backup Settings**. This will open the **Backup Settings** window, where you can configure the automatic backup settings according to your requirements.

    - In **Backup Time**, schedule a start time for the daily cluster backup.

        If you do not specify a preferred backup time, TiDB Cloud assigns a default backup time, which is 2:00 AM in the time zone of the region where the cluster is located.

    - In **Backup Retention**, configure the minimum backup data retention period.

        The backup retention period must be set within a range of 7 to 90 days.

3. Click **Confirm**.

### Delete backup files

To delete an existing backup file, perform the following steps:

1. Navigate to the **Backup** tab of a cluster.

2. Click **Delete** for the backup file that you want to delete.

## Restore

TiDB Serverless only supports in-place restoration. To restore your TiDB Serverless cluster from a backup, follow these steps:

1. Navigate to the **Backup** page of a cluster.

2. Click **Restore**. The setting window displays.

3. In **Restore Mode**, you can choose to restore from a specific backup or any point in time.

    <SimpleTab>
    <div label="Basic Snapshot Restore">

    To restore from a selected backup snapshot, take the following steps:

    1. Click **Basic Snapshot Restore**.
    2. Select the backup snapshot you want to restore to.

    </div>
    <div label="Point-in-Time Restore">

    This feature lets you restore a cluster to a specific state from any time within the last 90 days.

    > **Note:**
    >
    > The **Point-in-Time Restore** feature is currently in beta.

    To restore from a specific point in time, take the following steps:

    1. Click **Point-in-Time Restore**.
    2. Select the date and time you want to restore to.

    </div>
    </SimpleTab>

4. Click **Restore** to begin the restoration process.

   After initiating the restore process, the cluster status changes to **Restoring**. The cluster will be unavailable during the restore process and existing connections will be terminated. Once the restore process completes successfully, you can access the cluster as usual.
