---
title: Scale Your TiDB Cluster
summary: Learn how to scale your TiDB Cloud cluster.
---

# Scale Your TiDB Cluster

> **Note:**
>
> - You cannot scale a [TiDB Serverless cluster](/tidb-cloud/select-cluster-tier.md#tidb-serverless).
> - When a cluster is in the **MODIFYING** status, you cannot perform any new scaling operations on it.

You can scale a TiDB cluster in the following dimensions:

- Node number of TiDB, TiKV, and TiFlash
- vCPU and RAM of TiDB, TiKV, and TiFlash
- Storage of TiKV and TiFlash

For information about how to determine the size of your TiDB cluster, see [Determine Your TiDB Size](/tidb-cloud/size-your-cluster.md).

> **Note:**
>
> If the vCPU and RAM size of TiDB or TiKV is set as **2 vCPU, 8 GiB (Beta)** or **4 vCPU, 16 GiB**, note the following restrictions. To bypass these restrictions, you can [increase the vCPU and RAM](#change-vcpu-and-ram) first.
>
> - The node number of TiDB can only be set to 1 or 2, and the node number of TiKV is fixed to 3.
> - 2 vCPU TiDB can only be used with 2 vCPU TiKV, and 2 vCPU TiKV can only be used with 2 vCPU TiDB.
> - 4 vCPU TiDB can only be used with 4 vCPU TiKV, and 4 vCPU TiKV can only be used with 4 vCPU TiDB.
> - TiFlash is unavailable.

## Change node number

You can increase or decrease the number of TiDB, TiKV, or TiFlash nodes.

> **Warning:**
>
> Decreasing TiKV or TiFlash node number can be risky, which might lead to insufficient storage space, excessive CPU usage, or excessive memory usage on remaining nodes.

To change the number of TiDB, TiKV, or TiFlash nodes, take the following steps:

1. In the TiDB Cloud console, navigate to the [**Clusters**](https://tidbcloud.com/console/clusters) page of your project.
2. In the row of the cluster that you want to scale, click **...**.

    > **Tip:**
    >
    > Alternatively, you can also click the name of the cluster that you want to scale on the **Clusters** page and click **...** in the upper-right corner.

3. Click **Modify** in the drop-down menu. The **Modify Cluster** page is displayed.
4. On the **Modify Cluster** page, change the number of TiDB, TiKV, or TiFlash nodes.
5. Review the cluster size in the right pane, and then click **Confirm**.

You can also change the number of TiDB, TiKV, or TiFlash nodes using TiDB Cloud API through the [Modify a TiDB Dedicated cluster](https://docs.pingcap.com/tidbcloud/api/v1beta#tag/Cluster/operation/UpdateCluster) endpoint. Currently, TiDB Cloud API is still in beta. For more information, see [TiDB Cloud API Documentation](https://docs.pingcap.com/tidbcloud/api/v1beta).

## Change vCPU and RAM

You can increase or decrease vCPU and RAM of TiDB, TiKV, or TiFlash nodes.

> **Note:**
>
> - Changing vCPU and RAM is only available to the following clusters:
>     - Hosted on AWS and created after 2022/12/31.
>     - Hosted on Google Cloud and created after 2023/04/26.
> - AWS has a cooldown period of vCPU and RAM changes. If your TiDB cluster is hosted on AWS, after changing the storage or vCPU and RAM of TiKV or TiFlash, you must wait at least six hours before you can change it again.

To change the vCPU and RAM of TiDB, TiKV, or TiFlash nodes, take the following steps:

1. In the TiDB Cloud console, navigate to the [**Clusters**](https://tidbcloud.com/console/clusters) page of your project.
2. In the row of the cluster that you want to scale, click **...**.

    > **Tip:**
    >
    > Alternatively, you can also click the name of the cluster that you want to scale on the **Clusters** page and click **...** in the upper-right corner.

3. Click **Modify** in the drop-down menu. The **Modify Cluster** page is displayed.
4. On the **Modify Cluster** page, change the vCPU and RAM of TiDB, TiKV, or TiFlash nodes.
5. Review the cluster size in the right pane, and then click **Confirm**.

You can also change the vCPU and RAM of a TiDB, TiKV, or TiFlash node using TiDB Cloud API through the [Modify a TiDB Dedicated cluster](https://docs.pingcap.com/tidbcloud/api/v1beta#tag/Cluster/operation/UpdateCluster) endpoint. Currently, TiDB Cloud API is still in beta. For more information, see [TiDB Cloud API Documentation](https://docs.pingcap.com/tidbcloud/api/v1beta).

## Change storage

You can increase the storage of TiKV or TiFlash.

> **Warning:**
>
> - For a running cluster, AWS and Google Cloud do not allow in-place storage capacity downgrade.
> - AWS has a cooldown period of storage changes. If your TiDB cluster is hosted on AWS, after changing the storage or vCPU and RAM of TiKV or TiFlash, you must wait at least six hours before you can change it again.

To change the storage of TiKV or TiFlash, take the following steps:

1. In the TiDB Cloud console, navigate to the [**Clusters**](https://tidbcloud.com/console/clusters) page of your project.
2. In the row of the cluster that you want to scale, click **...**.

    > **Tip:**
    >
    > Alternatively, you can also click the name of the cluster that you want to scale on the **Clusters** page and click **...** in the upper-right corner.

3. Click **Modify** in the drop-down menu. The **Modify Cluster** page is displayed.
4. On the **Modify Cluster** page, change the storage of each TiKV or TiFlash node.
5. Review the cluster size in the right pane, and then click **Confirm**.

You can also change the storage of a TiKV or TiFlash node using TiDB Cloud API through the [Modify a TiDB Dedicated cluster](https://docs.pingcap.com/tidbcloud/api/v1beta#tag/Cluster/operation/UpdateCluster) endpoint. Currently, TiDB Cloud API is still in beta. For more information, see [TiDB Cloud API Documentation](https://docs.pingcap.com/tidbcloud/api/v1beta).