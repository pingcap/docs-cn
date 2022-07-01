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

## Scale out a cluster

To scale out a cluster, take the following steps:

1. Navigate to the TiDB Clusters page and click the name of a cluster that you want to scale. The overview page of the cluster is displayed.
2. In the cluster information pane on the left, click **Setting**.
3. Click **Scale** in the drop-down menu. The **Scale** window is displayed.
4. In the **Scale** window, increase the node quantity of your TiDB, TiKV, and TiFlash<sup>beta</sup> respectively.
5. Click **Confirm**.

## Scale the vCPU or storage size

When a cluster is running, you cannot change its vCPU or storage size. To make such changes, take either of the following methods:

> **Warning:**
>
> Scaling down the vCPU or storage size of TiKV or TiFlash<sup>beta</sup> nodes can be risky, which might lead to insufficient storage space, excessive CPU usage, or excessive memory usage on remaining nodes. If you need to do that, choose Method 2: Scale vCPU or storage size through a support ticket.

- Method 1: Scale vCPU or storage size through backup and restore

    Scaling vCPU or storage size through backup and restore means that you need to [create a latest backup of the cluster](/tidb-cloud/backup-and-restore.md#manual-backup), [delete the cluster](/tidb-cloud/delete-tidb-cluster.md), and then change the vCPU or storage size when you [restore the deleted cluster](/tidb-cloud/backup-and-restore.md#restore-a-deleted-cluster). Before taking this method, make sure the following impacts are acceptable:

    - To avoid any data loss during or after the backup, you need to stop the connection to the cluster through your SQL client before creating the backup.
    - After you stop the connection to the cluster, your applications running on this cluster cannot provide service normally until the restoring process is completed.

- Method 2: Scale vCPU or storage size through a support ticket

    Perform the steps in [TiDB Cloud Support](/tidb-cloud/tidb-cloud-support.md) to create a support ticket. For each node to be scaled, provide the following information in the **Description** box of the ticket:

    - Node type: TiDB, TiKV, or TiFlash
    - Current vCPU size: xxx
    - Expected vCPU size: xxx
    - Current storage size: xxx
    - Expected storage size: xxx
    - Cloud Provider: GCP or AWS
    - Cluster Name: xxx

## Scale in TiDB nodes

To scale in TiDB nodes, take the following steps:

1. Navigate to the TiDB Clusters page and click the name of a cluster that you want to scale. The overview page of the cluster is displayed.
2. In the cluster information pane on the left, click **Setting**.
3. Click **Scale** in the drop-down menu. The **Scale** window is displayed.
4. In the **Scale** window, decrease the node quantity of your TiDB.
5. Click **Confirm**.

## Scale in TiKV or TiFlash<sup>beta</sup> nodes

To scale in TiKV nodes or TiFlash<sup>beta</sup> nodes, you need to submit a scale-in support ticket. We will contact you and complete the scale-in within the agreed time.

> **Warning:**
>
> Scaling in your TiKV nodes and TiFlash<sup>beta</sup> nodes can be risky, which might lead to insufficient storage space, excessive CPU usage, or excessive memory usage on remaining nodes.

To submit a scale-in request, perform the steps in [TiDB Cloud Support](/tidb-cloud/tidb-cloud-support.md) to contact our support team. For each node to be scaled, provide the following information in the **Description** box:

- Node type: TiKV or TiFlash
- Current node number: xxx
- Expected node number: xxx
- Cloud Provider: GCP or AWS
- Cluster Name: xxx
