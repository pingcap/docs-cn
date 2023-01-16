---
title: Delete a TiDB Cluster
summary: Learn how to delete a TiDB cluster.
---

# Delete a TiDB Cluster

This document describes how to delete a TiDB cluster on TiDB Cloud.

You can delete a cluster at any time by performing the following steps:

1. Navigate to the [**Clusters**](https://tidbcloud.com/console/clusters) page of your project.
2. In the row of your target cluster to be deleted, click **...**.

    > **Tip:**
    >
    > Alternatively, you can also click the name of the target cluster to go to its overview page, and then click **...** in the upper-right corner.

3. Click **Delete** in the drop-down menu.
4. In the cluster deleting window, enter the cluster name.

    If you want to restore the cluster sometime in the future, make sure that you have a backup of the cluster. Otherwise, you cannot restore it anymore. For more information about how to back up Dedicated Tier clusters, see [Back up and Restore TiDB Cluster Data](/tidb-cloud/backup-and-restore.md).

    > **Note:**
    >
    > For [Serverless Tier clusters](/tidb-cloud/select-cluster-tier.md#serverless-tier-beta), the backup and restore feature is unavailable. You can use [Dumpling](https://docs.pingcap.com/tidb/stable/dumpling-overview) to export your data as a backup.

5. Click **I understand the consequences. Delete this cluster**.

 Once a backed up Dedicated Tier cluster is deleted, the existing backup files of the cluster are moved to the recycle bin.

- For backup files from an automatic backup, the recycle bin can retain them for 7 days.
- For backup files from a manual backup, there is no expiration date.

 If you want to restore a cluster from recycle bin, see [Restore a deleted cluster](/tidb-cloud/backup-and-restore.md#restore-a-deleted-cluster).
