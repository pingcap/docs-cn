---
title: Back up and Restore TiDB Cluster Data
summary: Learn how to back up and restore your TiDB Cloud cluster.
aliases: ['/tidbcloud/restore-deleted-tidb-cluster']
---

# Back up and Restore TiDB Cluster Data

This document describes how to back up and restore your TiDB cluster data on TiDB Cloud.

## Backup

TiDB Cloud provides two types of data backup: automatic backup and manual backup.

For [Developer Tier clusters](/tidb-cloud/select-cluster-tier.md#developer-tier), each cluster allows one automatic backup and two manual backups:

- For the automatic backup, the existing backup will be replaced by the newer backup.
- For the manual backup, if you already have two backups, you need to delete at least one backup before you are able to make another backup.

### Automatic backup

By the automatic backup, you can back up the cluster data every day at the backup time you have set. To set the backup time, perform the following steps:

1. Navigate to the **Backup** tab of a cluster.

2. Click **Auto Setting**. The setting window displays.

3. In the setting window, select **Backup Time** and maximum backup files in **Limit (backup files)**.

4. Click **Confirm**.

If you do not specify a preferred backup time, TiDB Cloud assigns a default backup time based on each region. The following table lists the default backup time for each region:

| Cloud provider | Region name              | Region          | Default backup time |
|----------------|--------------------------|-----------------|---------------------|
| AWS            | US East (N. Virginia)    | us-east-1       | 07:00 UTC           |
| AWS            | US West (Oregon)         | us-west-2       | 10:00 UTC           |
| AWS            | Asia Pacific (Tokyo)     | ap-northeast-1  | 17:00 UTC           |
| AWS            | Asia Pacific (Seoul)     | ap-northeast-2  | 17:00 UTC           |
| AWS            | Asia Pacific (Singapore) | ap-southeast-1  | 18:00 UTC           |
| AWS            | Asia Pacific (Mumbai)    | ap-south-1      | 20:30 UTC           |
| AWS            | Europe (Frankfurt)       | eu-central-1    | 03:00 UTC           |
| GCP            | Iowa                     | us-central1     | 08:00 UTC           |
| GCP            | Oregon                   | us-west1        | 10:00 UTC           |
| GCP            | Tokyo                    | asia-northeast1 | 17:00 UTC           |
| GCP            | Singapore                | asia-southeast1 | 18:00 UTC           |
| GCP            | Taiwan                   | asia-east1      | 18:00 UTC           |

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
    - Increase the vCPUs size, node quantity, and storage size for the cluster.

4. Click **Confirm**.

   The cluster restore process starts and the **Security Quick Start** dialog box is displayed.

5. In the **Security Quick Start** dialog box, set the root password and allowed IP addresses to connect to your cluster, and then click **Apply**.

### Restore a deleted cluster

To restore a deleted cluster from recycle bin, take the following steps:

1. In the TiDB Cloud console, go to the target project and click the **Recycle Bin** tab.
2. Locate the cluster you want to restore, and then click **Backups** in the **Action** column.
3. Locate your desired backup time, and then click **Restore**.
4. In the **Restore** window, make the following changes if necessary:

    - Update the port number of the cluster.
    - Increase the vCPUs size, node quantity, and storage size for the cluster.

5. Click **Confirm**.

   The cluster restore process starts and the **Security Quick Start** dialog box is displayed.

6. In the **Security Quick Start** dialog box, set the root password and allowed IP addresses to connect to your cluster, and then click **Apply**.