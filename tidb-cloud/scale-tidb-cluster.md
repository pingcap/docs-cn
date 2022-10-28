---
title: Scale Your TiDB Cluster
summary: Learn how to scale your TiDB Cloud cluster.
aliases: ['/tidbcloud/beta/scale-tidb-cluter']
---

# Scale Your TiDB Cluster

> **Note:**
>
> - You cannot scale a [Serverless Tier cluster](/tidb-cloud/select-cluster-tier.md#serverless-tier).
> - When a cluster is in the **MODIFYING** status, you cannot perform any new scaling operations on it.

You can scale a TiDB cluster in the following dimensions:

- Node number of TiDB, TiKV, and TiFlash
- Node storage of TiKV and TiFlash
- Node size (including vCPUs and memory) of TiDB, TiKV, and TiFlash

For information about how to determine the size of your TiDB cluster, see [Determine Your TiDB Size](/tidb-cloud/size-your-cluster.md).

> **Note:**
>
> If the node size of TiDB or TiKV is set as **2 vCPU, 8 GiB (Beta)** or **4 vCPU, 16 GiB**, note the following restrictions. To bypass these restrictions, you can [increase your node size](#increase-node-size) first.
>
> - The node quantity of TiDB can only be set to 1 or 2, and the node quantity of TiKV is fixed to 3.
> - 2 vCPU TiDB can only be used with 2 vCPU TiKV, and 2 vCPU TiKV can only be used with 2 vCPU TiDB.
> - 4 vCPU TiDB can only be used with 4 vCPU TiKV, and 4 vCPU TiKV can only be used with 4 vCPU TiDB.
> - TiFlash is unavailable.

## Change node number

You can change the number of TiDB, TiKV, or TiFlash nodes.

### Increase node number

To increase the number of TiDB, TiKV, or TiFlash nodes, take the following steps:

1. In the TiDB Cloud console, navigate to the **Clusters** page for your project.
2. Locate the cluster that you want to scale, and click **...** in the upper-right corner of the cluster area.

    > **Tip:**
    >
    > Alternatively, you can also click the name of the cluster that you want to scale on the **Clusters** page and click **...** in the upper-right corner.

3. Click **Modify** in the drop-down menu. The **Modify Cluster** page is displayed.
4. On the **Modify Cluster** page, increase the number of TiDB, TiKV, or TiFlash nodes.
5. Click **Confirm**.

You can also increase the number of TiDB, TiKV, or TiFlash nodes using TiDB Cloud API through the [Modify a Dedicated Tier cluster](https://docs.pingcap.com/tidbcloud/api/v1beta#tag/Cluster/operation/UpdateCluster) endpoint. Currently, TiDB Cloud API is still in beta. For more information, see [TiDB Cloud API Documentation](https://docs.pingcap.com/tidbcloud/api/v1beta).

### Decrease node number

To decrease the number of TiDB nodes, take the following steps:

1. In the TiDB Cloud console, navigate to the **Clusters** page for your project.
2. Locate the cluster that you want to scale, and click **...** in the upper-right corner of the cluster area.

    > **Tip:**
    >
    > Alternatively, you can also click the name of the cluster that you want to scale on the **Clusters** page and click **...** in the upper-right corner.

3. Click **Modify** in the drop-down menu. The **Modify Cluster** page is displayed.
4. On the **Modify Cluster** page, decrease the number of TiDB nodes.
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

## Change node storage

You can change the node storage of TiKV or TiFlash.

### Increase node storage

To increase the node storage of TiKV or TiFlash, take the following steps:

1. In the TiDB Cloud console, navigate to the **Clusters** page for your project.
2. Locate the cluster that you want to scale, and click **...** in the upper-right corner of the cluster area.

    > **Tip:**
    >
    > Alternatively, you can also click the name of the cluster that you want to scale on the **Clusters** page and click **...** in the upper-right corner.

3. Click **Modify** in the drop-down menu. The **Modify Cluster** page is displayed.
4. On the **Modify Cluster** page, increase the node storage of TiKV or TiFlash.
5. Click **Confirm**.

You can also increase the storage of a TiKV or TiFlash node using TiDB Cloud API through the [Modify a Dedicated Tier cluster](https://docs.pingcap.com/tidbcloud/api/v1beta#tag/Cluster/operation/UpdateCluster) endpoint. Currently, TiDB Cloud API is still in beta. For more information, see [TiDB Cloud API Documentation](https://docs.pingcap.com/tidbcloud/api/v1beta).

> **Note:**
>
> AWS has a cooldown period of node storage changes. If your TiDB cluster is hosted by AWS, after changing the node storage of TiKV or TiFlash, you must wait at least six hours before you can change it again.

### Decrease node storage

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
