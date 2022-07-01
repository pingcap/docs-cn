---
title: Delete a TiDB Cluster
summary: Learn how to delete a TiDB cluster.
---

# Delete a TiDB Cluster

This document describes how to delete a TiDB cluster on TiDB Cloud.

You can delete a cluster at any time by performing the following steps:

1. Navigate to the TiDB Clusters page and click the name of a cluster that you want to delete. The overview page of the cluster is displayed.
2. In the cluster information pane on the left, click **Setting**.
3. Click **Delete** in the drop-down menu.
4. In the cluster deleting window, enter the cluster name.

    If you want to restore the cluster sometime in the future, make sure you have a backup of the cluster. Otherwise, you cannot restore it anymore. For more information about how to back up clusters, see [Back up and Restore TiDB Cluster Data](/tidb-cloud/backup-and-restore.md).

5. Click **I understand the consequences, delete this cluster**.

 Once a backed up cluster is deleted, the existing backup files of the cluster are moved to the recycle bin.

- For backup files from an automatic backup, the recycle bin can retain them for 7 days.
- For backup files from a manual backup, there is no expiration date.

 If you want to restore a cluster from recycle bin, see [Restore a deleted cluster](/tidb-cloud/backup-and-restore.md#restore-a-deleted-cluster).