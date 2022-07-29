---
title: Scale Your TiDB Cluster
summary: Learn how to scale your TiDB Cloud cluster.
aliases: ['/tidbcloud/beta/scale-tidb-cluter']
---

# Scale Your TiDB Cluster

> **Note:**
>
> - Currently, you cannot scale a [Developer Tier cluster](/tidb-cloud/select-cluster-tier.md#developer-tier).
> - When a cluster is in the scaling status, you cannot perform any new scaling operations on it.

You can scale a TiDB cluster in the following dimensions:

- Node number of TiDB, TiKV, and TiFlash
- Storage size of TiKV and TiFlash
- Node size (including vCPUs and memory) of TiDB, TiKV, and TiFlash

For information about how to determine the size of your TiDB cluster, see [Determine Your TiDB Size](/tidb-cloud/size-your-cluster.md).

## Change node number

You can change the number of TiDB, TiKV, or TiFlash nodes.

### Increase node number

To increase the number of TiDB, TiKV, or TiFlash nodes, take the following steps:

1. In the TiDB Cloud console, navigate to the **Active Clusters** page for your project, and then click the name of a cluster that you want to scale. The overview page of the cluster is displayed.
2. In the cluster information pane on the left, click **Setting**.
3. Click **Scale** in the drop-down menu. The **Scale** window is displayed.
4. In the **Scale** window, increase the number of TiDB, TiKV, or TiFlash nodes.
5. Click **Confirm**.

### Decrease node number

To decrease the number of TiDB nodes, take the following steps:

1. In the TiDB Cloud console, navigate to the **Active Clusters** page for your project, and then click the name of a cluster that you want to scale. The overview page of the cluster is displayed.
2. In the cluster information pane on the left, click **Setting**.
3. Click **Scale** in the drop-down menu. The **Scale** window is displayed.
4. In the **Scale** window, decrease the number of TiDB nodes.
5. Click **Confirm**.

To decrease the number of TiKV or TiFlash nodes, you need to submit a support ticket. The PingCAP support team will contact you and complete the scaling within the agreed time.

> **Warning:**
>
> Decreasing TiKV or TiFlash node number can be risky, which might lead to insufficient storage space, excessive CPU usage, or excessive memory usage on remaining nodes.

To submit a support ticket, perform the steps in [TiDB Cloud Support](/tidb-cloud/tidb-cloud-support.md). For each node to be scaled, provide the following information in the **Description** box:

- Cluster name: xxx
- Cloud provider: GCP or AWS
- Node type: TiKV or TiFlash
- Current node number: xxx
- Expected node number: xxx

## Change storage size

You can change the storage size of TiKV or TiFlash.

### Increase storage size

To increase the storage size of TiKV or TiFlash, take the following steps:

1. In the TiDB Cloud console, navigate to the **Active Clusters** page for your project, and then click the name of a cluster that you want to scale. The overview page of the cluster is displayed.
2. In the cluster information pane on the left, click **Setting**.
3. Click **Scale** in the drop-down menu. The **Scale** window is displayed.
4. In the **Scale** window, increase the storage size of TiKV or TiFlash.
5. Click **Confirm**.

> **Note:**
>
> AWS has a cooldown period of storage size changes. If your TiDB cluster is hosted by AWS, after changing the storage size of TiKV or TiFlash, you must wait at least six hours before you can change it again.

### Decrease storage size

For a running cluster, AWS and Google Cloud do not allow in-place storage capacity downgrade.

## Increase node size

When a cluster is running, you cannot increase its node size. To make such changes, take either of the following methods:

- Method 1: Increase the node size through backup and restore

    You need to [create a latest backup of the cluster](/tidb-cloud/backup-and-restore.md#manual-backup), [delete the cluster](/tidb-cloud/delete-tidb-cluster.md), and then increase the node size when you [restore the deleted cluster](/tidb-cloud/backup-and-restore.md#restore-a-deleted-cluster). Before taking this method, make sure the following impacts are acceptable:

    - To avoid any data loss during or after the backup, you need to stop the connection to the cluster through your SQL client before creating the backup.
    - After you stop the connection to the cluster, your applications running on this cluster cannot provide service normally until the restoring process is completed.

- Method 2: Increase the node size through a support ticket

    To submit a support ticket, perform the steps in [TiDB Cloud Support](/tidb-cloud/tidb-cloud-support.md). The PingCAP support team will contact you and complete the scaling within the agreed time.

    For each node to be scaled, provide the following information in the **Description** box of the ticket:

    - Cluster name: xxx
    - Cloud provider: GCP or AWS
    - Node type: TiDB, TiKV, or TiFlash
    - Current node size: xxx
    - Expected node size: xxx