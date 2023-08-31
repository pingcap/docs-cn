---
title: Back Up and Restore TiDB Dedicated Data
summary: Learn how to back up and restore your TiDB Dedicated cluster.
aliases: ['/tidbcloud/restore-deleted-tidb-cluster']
---

# Back Up and Restore TiDB Dedicated Data

This document describes how to back up and restore your TiDB Dedicated cluster data on TiDB Cloud.

> **Tip:**
>
> To learn how to back up and restore TiDB Serverless cluster data, see [Back Up and Restore TiDB Serverless Data](/tidb-cloud/backup-and-restore-serverless.md).

## Limitations

- TiDB Cloud does not support restoring tables in the `mysql` schema, including user permissions and system variables.
- If you turn on and off PITR (Point-in-time Recovery) multiple times, you can only choose a time point within the recoverable range after the most recent PITR is enabled. The earlier recoverable range is not accessible.

## Backup

TiDB Dedicated supports automatic backup and manual backup.

Automatic backups are scheduled for your TiDB Dedicated clusters according to the backup setting, which can reduce your loss in extreme disaster situations. You can also pick a backup snapshot and restore it into a new TiDB Dedicated cluster at any time.

### Automatic backup

By the automatic backup, you can back up the TiDB Dedicated cluster data every day at the backup time you have set. To set the backup time, perform the following steps:

1. Navigate to the **Backup** page of a TiDB Dedicated cluster.

2. Click **Backup Settings**. The setting window displays.

3. In the setting window, configure the automatic backup:

    - Toggle the **Auto Backup** switch to **On**.

    - In **Backup Cycle**, select either the **Daily** or **Weekly** checkbox. If you select **Weekly**, you need to specify the days of the week for the backup.

    - In **Backup Time**, schedule a start time for the daily or weekly cluster backup.

        It is recommended to schedule automatic backup at a low workload period. If you do not specify a preferred backup time, TiDB Cloud assigns a default backup time, which is 2:00 AM in the time zone of the region where the cluster is located.

    - In **Backup Retention**, configure the minimum backup data retention period.

    - Turn on or off the PITR (**Point-in-time Recovery**) feature.

        > **Note:**
        >
        > - The PITR feature is enabled by default and cannot be disabled when you enable weekly backup.
        > - If you change the backup cycle from weekly to daily, the PITR feature remains enabled. You can manually disable it if needed.

        PITR supports restoring data of any point in time to a new cluster. You can use it to:

        - Reduce RPO in disaster recovery.
        - Resolve cases of data write errors by restoring point-in-time that is before the error event.
        - Audit the historical data of the business.

        If you have one of the preceding needs and want to use the PITR feature, make sure that your TiDB Dedicated cluster version is at least v6.4.0 and the TiKV node is at least 8 vCPU and 16 GiB.

    - In **Backup Storage Region**, select the regions where you want to store your backup data.

        TiDB Cloud stores your backup data in the current region of your cluster by default. This behavior cannot be changed. In addition, you can add another remote region, and TiDB Cloud will copy all new backup data to the remote region, which facilitates data safety and faster recovery. After adding a remote region as a backup data storage, you cannot remove the region.

4. Click **Confirm** to preview the configuration change.

    If you turn on PITR, you can select the **Perform a backup immediately and use it as recovery starting point in PITR.** checkbox. Otherwise, PITR will not be available until the next backup is completed.

5. Click **Confirm**.

### Backup storage region support

Currently, you cannot select an arbitrary remote region for backup data storage. The regions already supported are as follows:

| Cloud provider | Cluster region                      | Remote region support   |
|----------------|-----------------------------|--------------------------|
| Google Cloud            | Tokyo (asia-northeast1)     | Osaka (asia-northeast2)  |

> **Note:**
>
> If you select multiple backup storage regions, you will be charged for multiple backup storage and inter-region backup data replication out from the cluster region to each destination region. The cost is on a per-region basis and varies with the backup regions selected. For more information, see [Data Backup Cost](https://www.pingcap.com/tidb-cloud-pricing-details/#backup-storage-cost).

### Manual backup

Manual backups are user-initiated backups that enable you to back up your data to a known state as needed, and then restore to that state at any time.

To apply a manual backup to your TiDB Dedicated cluster, perform the following steps:

1. Navigate to the **Backup** tab of a cluster.

2. Click **Manual Backup**. The setting window displays.

3. Enter a **Name**.

4. Click **Confirm**. Then your cluster data is backed up.

### Delete backup files

To delete an existing backup file, perform the following steps:

1. Navigate to the **Backup** tab of a cluster.

2. Click **Delete** for the backup file that you want to delete.

### Delete a running backup job

To delete a running backup job, it is similar as [**Delete backup files**](#delete-backup-files).

1. Navigate to the **Backup** tab of a cluster.

2. Click **Delete** for the backup file that is in the **Pending** or **Running** state.

### Best practices for backup

- It is recommended that you perform backup operations at cluster idle time to minimize the impact on business.
- Do not run the manual backup while importing data, or during cluster scaling.
- After you delete a cluster, the existing manual backup files will be retained until you manually delete them, or your account is closed. Automatic backup files will be retained for 31 days from the date of cluster deletion. You need to delete the backup files accordingly.

## Restore

TiDB Dedicated provides two types of data restoration:

- Restore backup data to a new cluster
- Restore a deleted cluster from the recycle bin

### Restore data to a new cluster

To restore your TiDB Dedicated cluster data from a backup to a new cluster, take the following steps:

1. Navigate to the **Backup** tab of a cluster.

2. Click **Restore**. The setting window displays.

3. In **Restore Mode**, you can choose to restore data of any point in time or a selected backup to a new cluster.

    <SimpleTab>
    <div label="Select Time Point">

    To restore data of any point in time within the backup retention to a new cluster, make sure that **PITR** in **Backup Settings** is on and then take the following steps:

    1. Click **Select Time Point**.
    2. Select **Date** and **Time** you want to restore to.

    </div>

    <div label="Select Backup Name">

    To restore a selected backup to the new cluster, take the following steps:

    1. Click **Select Backup Name**.
    2. Select a backup you want to restore to.

    </div>
    </SimpleTab>

4. In **Restore to Region**, select the same region as the **Backup Storage Region** configured in the **Backup Settings**.

5. In the **Restore** window, you can also make the following changes if necessary:

    - Set the cluster name.
    - Update the port number of the cluster.
    - Increase node number, vCPU and RAM, and storage for the cluster.

6. Click **Restore**.

   The cluster restore process starts and the **Security Settings** dialog box is displayed.

7. In the **Security Settings** dialog box, set the root password and allowed IP addresses to connect to your cluster, and then click **Apply**.

### Restore a deleted cluster

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

> **Note:**
>
> You cannot restore a deleted cluster to any point in time. You can only select an automatic or manual backup to restore.
