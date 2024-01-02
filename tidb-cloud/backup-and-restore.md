---
title: Back Up and Restore TiDB Dedicated Data
summary: Learn how to back up and restore your TiDB Dedicated cluster.
aliases: ['/tidbcloud/restore-deleted-tidb-cluster']
---

# Back Up and Restore TiDB Dedicated Data

This document describes how to back up and restore your TiDB Dedicated cluster data on TiDB Cloud. TiDB Dedicated supports automatic backup and manual backup. You can also restore backup data to a new cluster or restore a deleted cluster from the recycle bin.

> **Tip**
>
> To learn how to back up and restore TiDB Serverless cluster data, see [Back Up and Restore TiDB Serverless Data](/tidb-cloud/backup-and-restore-serverless.md).

## Limitations

- For clusters of v6.2.0 or later versions, TiDB Dedicated supports restoring user accounts and SQL bindings from backups by default.
- TiDB Dedicated does not support restoring system variables stored in the `mysql` schema. 
- It is recommended that you import data first, then perform a **manual** snapshot backup, and finally enable Point-in-time Restore. Because the data imported through the TiDB Cloud console **does not** generate change logs, it cannot be automatically detected and backed up. For more information, see [Import CSV Files from Amazon S3 or GCS into TiDB Cloud](/tidb-cloud/import-csv-files.md). 
- If you turn on and off Point-in-time Restore multiple times, you can only choose a time point within the recoverable range after the most recent Point-in-time Restore is enabled. The earlier recoverable range is not accessible.
- DO NOT modify the switches of **Point-in-time Restore** and **Dual Region Backup** at the same time.

## Backup

### Turn on auto backup

TiDB Dedicated supports both [snapshot backup](https://docs.pingcap.com/tidb/stable/br-snapshot-guide) and [log backup](https://docs.pingcap.com/tidb/stable/br-pitr-guide). Snapshot backup enables you to restore data to the backup point. By default, snapshot backups are taken automatically and stored according to your backup retention policy. You can disable auto backup at any time.

#### Turn on Point-in-time Restore

> **Note**
>
> The Point-in-time Restore feature is supported for TiDB Dedicated clusters that are v6.4.0 or later.

This feature supports restoring data of any point in time to a new cluster. You can use it to:

- Reduce RPO in disaster recovery.
- Resolve cases of data write errors by restoring point-in-time that is before the error event.
- Audit the historical data of the business.

It is strongly recommended to turn on this feature. The cost is the same as snapshot backup. For more information, refer to [Data Backup Cost](https://www.pingcap.com/tidb-dedicated-pricing-details#backup-storage-cost).

To turn on this feature, perform the following steps:

1. Navigate to the **Backup** page of a TiDB Dedicated cluster.

2. Click **Backup Settings**.

3. Toggle the **Auto Backup** switch to **On**.

4. Toggle the **Point-in-time Restore** switch to **On**.

    > **Warning**
    >
    > Point-in-Time Restore only takes effect after the next backup task is completed. To make it take effect earlier, you can [manually perform a backup](#perform-a-manual-backup) after enabling it.

5. Click **Confirm** to preview the configuration changes.

6. Click **Confirm** again to save changes.

#### Configure backup schedule

TiDB Dedicated supports daily and weekly backup schedules. By default, the backup schedule is set to daily. You can choose a specific time of the day or week to start snapshot backup.

To configure the backup schedule, perform the following steps:

1. Navigate to the **Backup** page of a TiDB Dedicated cluster.

2. Click **Backup Settings**.

3. Toggle the **Auto Backup** switch to **On**.

4. Configure the backup schedule as follows:

    - In **Backup Scheduler**, select either the **Daily** or **Weekly** checkbox. If you select **Weekly**, you need to specify the days of the week for the backup.

        > **Warning**
        >
        > - When weekly backup is enabled, the Point-in-time Restore feature is enabled by default and cannot be disabled.
        > - If you change the backup scheduler from weekly to daily, the Point-in-time Restore feature remains its original setting. You can manually disable it if needed.

    - In **Backup Time**, schedule a start time for the daily or weekly cluster backup.

        If you do not specify a preferred backup time, TiDB Cloud assigns a default backup time, which is 2:00 AM in the time zone of the region where the cluster is located.

        > **Note**
        >
        > - Backup jobs are automatically delayed when data import jobs are in progress. **DO NOT** run manual backups during data import or cluster scaling.

    - In **Backup Retention**, configure the minimum backup data retention period. The default period is 7 days. To minimize the impact on business, it is recommended to schedule automatic backup during periods of low workloads.

        > **Note**
        >
        > - After you delete a cluster, the automatic backup files will be retained for a specified period, as set in backup retention. You need to delete the backup files accordingly.
        > - After you delete a cluster, the existing manual backup files will be retained until you manually delete them, or your account is closed.

### Turn on dual region backup (beta)

> **Note:**
>
> - The dual region backup feature is currently in beta.
> - TiDB Dedicated clusters hosted on Google Cloud work seamlessly with Google Cloud Storage. Similar to Google Cloud Storage, **TiDB Dedicated supports dual-region pairing only within the same multi-region code as Google dual-region storage**. For example, in Asia, currently you must pair Tokyo and Osaka together for dual-region storage. For more information, refer to [Dual-regions](https://cloud.google.com/storage/docs/locations#location-dr).

TiDB Dedicated supports dual region backup by replicating backups from your cluster region to another different region. After you enable this feature, all backups are automatically replicated to the specified region. This provides cross-region data protection and disaster recovery capabilities. It is estimated that approximately 99% of the data can be replicated to the secondary region within an hour.

Dual region backup costs include both backup storage usage and cross-region data transfer fees. For more information, refer to [Data Backup Cost](https://www.pingcap.com/tidb-dedicated-pricing-details#backup-storage-cost).

To turn on dual region backup, perform the following steps:

1. Navigate to the **Backup** page of a TiDB Dedicated cluster.

2. Click **Backup Settings**.

3. Toggle the **Dual Region Backup** switch to **On**.

4. From the **Dual Region** drop-down list, select a region to store the backup files.

5. Click **Confirm** to preview the configuration changes.

6. Click **Confirm** again to save changes.

### Turn off auto backup

> **Note**
>
> Turning off auto backup will also turn off point-in-time restore by default.

To turn off auto backup, perform the following steps:

1. Navigate to the **Backup** page of a TiDB Dedicated cluster.

2. Click **Backup Settings**.

3. Toggle the **Auto Backup** switch to **Off**.

4. Click **Confirm** to preview the configuration changes.

5. Click **Confirm** again to save changes.

### Turn off dual region backup (beta)

> **Tip**
>
> Disabling dual region backup does not immediately delete the backups in the secondary region. These backups will be cleaned up later according to the backup retention schedule. To remove them immediately, you can manually [delete the backups](#delete-backups).

To turn off dual region backup, perform the following steps:

1. Navigate to the **Backup** page of a TiDB Dedicated cluster.

2. Click **Backup Settings**.

3. Toggle the **Dual Region Backup** switch to **Off**.

4. Click **Confirm** to preview the configuration changes.

5. Click **Confirm** again to save changes.

### Perform a manual backup

Manual backups are user-initiated backups that enable you to back up your data to a known state as needed, and then restore to that state at any time.

To apply a manual backup to your TiDB Dedicated cluster, perform the following steps:

1. Navigate to the **Backup** tab of a cluster.

2. Click **Manual Backup**. The setting window displays.

3. Enter a **Name**.

4. Click **Confirm**. Then your cluster data is backed up.

### Delete backups

#### Delete backup files

To delete an existing backup file, perform the following steps:

1. Navigate to the **Backup** tab of a cluster.

2. Click **Delete** for the backup file that you want to delete.

#### Delete a running backup job

To delete a running backup job, it is similar as [**Delete backup files**](#delete-backup-files).

1. Navigate to the **Backup** tab of a cluster.

2. Click **Delete** for the backup file that is in the **Pending** or **Running** state.

## Restore

### Restore data to a new cluster

> **Note**
>
> When you restore a TiDB cluster from backups, the restore process retains the original time zone setting without overwriting it.

To restore your TiDB Dedicated cluster data from a backup to a new cluster, take the following steps:

1. Navigate to the **Backup** tab of a cluster.

2. Click **Restore**. The setting window displays.

3. In **Restore Mode**, choose **Restore From Region**, indicating the region of backup stores.

    > **Note**
    >
    > - The default value of the **Restore From Region** is the same as the backup cluster.

4. In **Restore Mode**, choose to restore data of any point in time or a selected backup to a new cluster.

    <SimpleTab>
    <div label="Select Time Point">

    To restore data of any point in time within the backup retention to a new cluster, make sure that **Point-in-time Restore** in **Backup Settings** is on and then take the following steps:

    - Click **Select Time Point**.
    - Select **Date** and **Time** you want to restore to.

    </div>

    <div label="Select Backup Name">

    To restore a selected backup to the new cluster, take the following steps:

    - Click **Select Backup Name**.
    - Select a backup you want to restore to.

    </div>
    </SimpleTab>

5. In **Restore to Region**, select the same region as the **Backup Storage Region** configured in the **Backup Settings**.

6. In the **Restore** window, you can also make the following changes if necessary:

    - Set the cluster name.
    - Update the port number of the cluster.
    - Increase node number, vCPU and RAM, and storage for the cluster.

7. Click **Restore**.

   The cluster restore process starts and the **Security Settings** dialog box is displayed.

8. In the **Security Settings** dialog box, set the root password and allowed IP addresses to connect to your cluster, and then click **Apply**.

### Restore a deleted cluster

> **Note:**
>
> You cannot restore a deleted cluster to any point in time. You can only select an automatic or manual backup to restore.

To restore a deleted cluster from recycle bin, take the following steps:

1. Log in to the [TiDB Cloud console](https://tidbcloud.com).
2. Click <MDSvgIcon name="icon-left-projects" /> in the lower-left corner, switch to the target project if you have multiple projects, and then click **Project Settings**.
3. On the **Project Settings** page of your project, click **Recycle Bin** in the left navigation pane, locate the cluster you want to restore, and then click **Backups** in the **Action** column.
4. Locate your desired backup time, and then click **Restore** in the **Action** column.
5. In the **Restore** window, make the following changes if necessary:

    - Update the port number of the cluster.
    - Increase the node number, vCPU and RAM, and storage for the cluster.

6. Click **Confirm**.

   The cluster restore process starts and the **Security Settings** dialog box is displayed.

7. In the **Security Settings** dialog box, set the root password and allowed IP addresses to connect to your cluster, and then click **Apply**.
