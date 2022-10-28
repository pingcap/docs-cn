---
title: Pause or Resume a TiDB Cluster
summary: Learn how to pause or resume a TiDB cluster.
---

# Pause or Resume a TiDB Cluster

You can easily pause and resume a cluster that is not in operation at all times in TiDB Cloud.

The pause does not affect your data stored in the cluster but only stops the collection of monitoring information and the consumption of computing resources. After the pause, you can resume your cluster at any time.

Comparing with backup and restore, pausing and resuming a cluster takes less time and keeps your cluster state information (including cluster version, cluster configurations, and TiDB user accounts).

> **Note:**
>
> You cannot pause a [Serverless Tier cluster](/tidb-cloud/select-cluster-tier.md#serverless-tier).

## Limitations

- You can pause your cluster only when it is in the **AVAILABLE** state. If your cluster is in other states such as **MODIFYING**, you must wait for the current operation to be completed before pausing the cluster.
- You cannot pause your cluster when a data import task is going on. You can either wait for the import task to be completed or cancel the import task.
- You cannot pause your cluster when a backup job is going on. You can either wait for the current backup job to be completed or [delete the running backup job](/tidb-cloud/backup-and-restore.md#delete-a-running-backup-job).

<!--- - You cannot pause your cluster if it has any [Changefeeds](/tidb-cloud/changefeed-overview.md). You need to delete the existing Changefeeds ([Delete Sink to Apache Kafka](/tidb-cloud/changefeed-sink-to-apache-kafka.md#delete-a-sink) or [Delete Sink to MySQL](/tidb-cloud/changefeed-sink-to-mysql.md#delete-a-sink)) before pausing the cluster. --->

## Pause a TiDB cluster

When a cluster is paused, note the following:

- TiDB Cloud stops collecting monitoring information of the cluster.
- You cannot read data from or write data to the cluster.
- You cannot import or back up data.
- Only the following costs will be charged:

    - Node Storage Cost
    - Data Backup Cost

- TiDB Cloud stops [automatic backup](/tidb-cloud/backup-and-restore.md#automatic-backup) of the cluster.

To pause a cluster, take the following steps:

1. In the TiDB Cloud console, navigate to the **Clusters** page of your project.
2. For the cluster that you want to pause, click **...** in the upper-right corner of the cluster area.

    > **Tip:**
    >
    > Alternatively, you can click the name of the cluster that you want to pause on the **Clusters** page, and then click **...** in the upper-right corner.

3. Click **Pause** in the drop-down menu.

    The **Pause your cluster** dialog is displayed.

4. In the dialog, click **Pause** to confirm your choice.

You can also pause a cluster using TiDB Cloud API. Currently, TiDB Cloud API is still in beta. For more information, see [TiDB Cloud API Documentation](https://docs.pingcap.com/tidbcloud/api/v1beta).

## Resume a TiDB cluster

After a paused cluster is resumed, note the following:

- TiDB Cloud resumes collecting the monitoring information of the cluster, and you can read data from or write data to the cluster.
- TiDB Cloud resumes charging both compute and storage costs.
- TiDB Cloud resumes [automatic backup](/tidb-cloud/backup-and-restore.md#automatic-backup) of the cluster.

To resume a paused cluster, take the following steps:

1. In the TiDB Cloud console, navigate to the **Clusters** page of your project.
2. For the cluster that you want to resume, click **Resume**.

    The **Resume your cluster** dialog is displayed.

3. In the dialog, click **Resume** to confirm your choice. The cluster status becomes **RESUMING**.

Depending on your cluster size, it can take several minutes to resume the cluster. After the cluster is resumed, the cluster state changes from **RESUMING**to **AVAILABLE**.

You can also resume a cluster using TiDB Cloud API. Currently, TiDB Cloud API is still in beta. For more information, see [TiDB Cloud API Documentation](https://docs.pingcap.com/tidbcloud/api/v1beta).
