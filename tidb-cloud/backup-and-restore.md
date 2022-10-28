---
title: Back up and Restore TiDB Cluster Data
summary: Learn how to back up and restore your TiDB Cloud cluster.
aliases: ['/tidbcloud/restore-deleted-tidb-cluster']
---

# Back up and Restore TiDB Cluster Data

This document describes how to back up and restore your TiDB cluster data on TiDB Cloud.

> **Note:**
>
> For [Serverless Tier clusters](/tidb-cloud/select-cluster-tier.md#serverless-tier), the backup and restore feature is unavailable. You can use [Dumpling](https://docs.pingcap.com/tidb/stable/dumpling-overview) to export your data as a backup.

## Backup

TiDB Cloud provides two types of data backup: automatic backup and manual backup.

Daily backups are automatically scheduled for your TiDB clusters in TiDB Cloud. You can pick a backup snapshot and restore it into a new TiDB cluster at any time. Automated backup can reduce your losses in extreme disaster situations.

### Automatic backup

By the automatic backup, you can back up the cluster data every day at the backup time you have set. To set the backup time, perform the following steps:

1. Navigate to the **Backup** tab of a cluster.

2. Click **Auto Setting**. The setting window displays.

3. In the setting window, select **Backup Time** and maximum backup files in **Limit (backup files)**.

4. Click **Confirm**.

If you do not specify a preferred backup time, TiDB Cloud assigns a default backup time, which is 2:00 AM in the time zone of the region where the cluster is located.

Note that you can not disable automatic backup.

### Manual backup

Manual backups are user-initiated backups that enable you to back up your data to a known state as needed, and then restore to that state at any time.

To apply a manual backup to your TiDB cluster, perform the following steps:

1. Navigate to the **Backup** tab of a cluster.

2. Click **Manual** on the upper right.

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
- After you delete a cluster, the existing manual backup files will be retained until you manually delete them, or your account is closed. Automatic backup files will be retained for 7 days from the date of cluster deletion. You need to delete the backup files accordingly.

## Restore

TiDB Cloud provides two types of data restoration:

- Restore backup data to a new cluster
- Restore a deleted cluster from the recycle bin

### Restore data to a new cluster

To restore your TiDB cluster data from a backup to a new cluster, take the following steps:

1. Navigate to the **Backup** tab of a cluster.

2. Select an existing backup in the list, and click **Restore**.

3. In the **Restore** window, make the following changes if necessary:

    - Update the port number of the cluster.
    - Increase the node size, node quantity, and node storage for the cluster.

4. Click **Confirm**.

   The cluster restore process starts and the **Security Settings** dialog box is displayed.

5. In the **Security Settings** dialog box, set the root password and allowed IP addresses to connect to your cluster, and then click **Apply**.

### Restore a deleted cluster

To restore a deleted cluster from recycle bin, take the following steps:

1. In the TiDB Cloud console, go to the target project and click the **Recycle Bin** tab.
2. Locate the cluster you want to restore, and then click **Backups** in the **Action** column.
3. Locate your desired backup time, and then click **Restore**.
4. In the **Restore** window, make the following changes if necessary:

    - Update the port number of the cluster.
    - Increase the node size, node quantity, and node storage for the cluster.

5. Click **Confirm**.

   The cluster restore process starts and the **Security Settings** dialog box is displayed.

6. In the **Security Settings** dialog box, set the root password and allowed IP addresses to connect to your cluster, and then click **Apply**.
