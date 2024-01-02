---
title: Pause or Resume a TiDB Dedicated Cluster
summary: Learn how to pause or resume a TiDB Dedicated cluster.
---

# Pause or Resume a TiDB Dedicated Cluster

You can easily pause and resume a TiDB Dedicated cluster that is not in operation at all times in TiDB Cloud.

The pause does not affect your data stored in the cluster but only stops the collection of monitoring information and the consumption of computing resources. After the pause, you can resume your cluster at any time.

Comparing with backup and restore, pausing and resuming a cluster takes less time and keeps your cluster information (including cluster version, cluster configurations, and TiDB user accounts).

> **Note:**
>
> You cannot pause a [TiDB Serverless cluster](/tidb-cloud/select-cluster-tier.md#tidb-serverless).

## Limitations

- You can pause your cluster only when it is in the **Available** status. If your cluster is in other status such as **Modifying**, you must wait for the current operation to be completed before pausing the cluster.
- You cannot pause your cluster when a data import task is going on. You can either wait for the import task to be completed or cancel the import task.
- You cannot pause your cluster when a backup job is going on. You can either wait for the current backup job to be completed or [delete the running backup job](/tidb-cloud/backup-and-restore.md#delete-a-running-backup-job).
- You cannot pause your cluster if it has any [changefeeds](/tidb-cloud/changefeed-overview.md). You need to [delete the existing changefeeds](/tidb-cloud/changefeed-overview.md#delete-a-changefeed) before pausing the cluster.

## Pause a TiDB cluster

When a cluster is paused, note the following:

- TiDB Cloud stops collecting monitoring information of the cluster.
- You cannot read data from or write data to the cluster.
- You cannot import or back up data.
- Only the following costs will be charged:

    - Node Storage Cost
    - Data Backup Cost

- TiDB Cloud stops [automatic backup](/tidb-cloud/backup-and-restore.md#turn-on-auto-backup) of the cluster.

To pause a cluster, take the following steps:

1. In the TiDB Cloud console, navigate to the [**Clusters**](https://tidbcloud.com/console/clusters) page of your project.
2. In the row of the cluster that you want to pause, click **...**.

    > **Tip:**
    >
    > Alternatively, you can click the name of the cluster that you want to pause on the **Clusters** page, and then click **...** in the upper-right corner.

3. Click **Pause** in the drop-down menu.

    The **Pause your cluster** dialog is displayed.

4. In the dialog, click **Pause** to confirm your choice.

    After you click **Pause**, the cluster will enter the **Pausing** status first. Once the pause operation is done, the cluster will transition to the **Paused** status.

You can also pause a cluster using TiDB Cloud API. Currently, TiDB Cloud API is still in beta. For more information, see [TiDB Cloud API Documentation](https://docs.pingcap.com/tidbcloud/api/v1beta).

## Resume a TiDB cluster

After a paused cluster is resumed, note the following:

- TiDB Cloud resumes collecting the monitoring information of the cluster, and you can read data from or write data to the cluster.
- TiDB Cloud resumes charging both compute and storage costs.
- TiDB Cloud resumes [automatic backup](/tidb-cloud/backup-and-restore.md#turn-on-auto-backup) of the cluster.

To resume a paused cluster, take the following steps:

1. In the TiDB Cloud console, navigate to the [**Clusters**](https://tidbcloud.com/console/clusters) page of your project.
2. For the cluster that you want to resume, click **Resume**. The **Resume your cluster** dialog is displayed.

    > **Note:**
    >
    > You cannot resume a cluster in the **Pausing** status.

3. In the dialog, click **Resume** to confirm your choice. The cluster status becomes **Resuming**.

Depending on your cluster size, it can take several minutes to resume the cluster. After the cluster is resumed, the cluster status changes from **Resuming** to **Available**.

You can also resume a cluster using TiDB Cloud API. Currently, TiDB Cloud API is still in beta. For more information, see [TiDB Cloud API Documentation](https://docs.pingcap.com/tidbcloud/api/v1beta).
