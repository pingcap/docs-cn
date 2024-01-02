---
title: Changefeed
summary: TiDB Cloud changefeed helps you stream data from TiDB Cloud to other data services.
---

# Changefeed

TiDB Cloud changefeed helps you stream data from TiDB Cloud to other data services. Currently, TiDB Cloud supports streaming data to Apache Kafka, MySQL, TiDB Cloud and cloud storage.

> **Note:**
>
> - Currently, TiDB Cloud only allows up to 100 changefeeds per cluster.
> - Currently, TiDB Cloud only allows up to 100 table filter rules per changefeed.
> - For [TiDB Serverless clusters](/tidb-cloud/select-cluster-tier.md#tidb-serverless), the changefeed feature is unavailable.

To access the changefeed feature, navigate to the cluster overview page of your TiDB cluster, and then click **Changefeed** in the left navigation pane. The changefeed page is displayed.

On the changefeed page, you can create a changefeed, view a list of existing changefeeds, and operate the existing changefeeds (such as scaling, pausing, resuming, editing, and deleting a changefeed).

## Create a changefeed

To create a changefeed, refer to the tutorials:

- [Sink to Apache Kafka](/tidb-cloud/changefeed-sink-to-apache-kafka.md)
- [Sink to MySQL](/tidb-cloud/changefeed-sink-to-mysql.md)
- [Sink to TiDB Cloud](/tidb-cloud/changefeed-sink-to-tidb-cloud.md)
- [Sink to cloud storage](/tidb-cloud/changefeed-sink-to-cloud-storage.md)

## Query Changefeed RCUs

1. Navigate to the cluster overview page of the target TiDB cluster, and then click **Changefeed** in the left navigation pane.
2. Locate the corresponding changefeed you want to query, and click **...** > **View** in the **Action** column.
3. You can see the current TiCDC Replication Capacity Units (RCUs) in the **Specification** area of the page.

## Scale a changefeed

You can change the TiCDC Replication Capacity Units (RCUs) of a changefeed by scaling up or down the changfeed.

> **Note:**
>
> - To scale a changefeed for a cluster, make sure that all changefeeds for this cluster are created after March 28, 2023.
> - If a cluster has changefeeds created before March 28, 2023, neither the existing changefeeds nor newly created changefeeds for this cluster support scaling up or down.

1. Navigate to the cluster overview page of the target TiDB cluster, and then click **Changefeed** in the left navigation pane.
2. Locate the corresponding changefeed you want to scale, and click **...** > **Scale Up/Down** in the **Action** column.
3. Select a new specification.
4. Click **Submit**.

It takes about 10 minutes to complete the scaling process (during which the changfeed works normally) and a few seconds to switch to the new specification (during which the changefeed will be paused and resumed automatically).

## Pause or resume a changefeed

1. Navigate to the cluster overview page of the target TiDB cluster, and then click **Changefeed** in the left navigation pane.
2. Locate the corresponding changefeed you want to pause or resume, and click **...** > **Pause/Resume** in the **Action** column.

## Edit a changefeed

> **Note:**
>
> TiDB Cloud currently only allows editing changefeeds in the paused status.

1. Navigate to the cluster overview page of the target TiDB cluster, and then click **Changefeed** in the left navigation pane.
2. Locate the changefeed you want to pause, and click **...** > **Pause** in the **Action** column.
3. When the changefeed status changes to `Paused`, click **...** > **Edit** to edit the corresponding changefeed.

    TiDB Cloud populates the changefeed configuration by default. You can modify the following configurations:

    - Apache Kafka sink: all configurations.
    - MySQL sink: **MySQL Connection**, **Table Filter**, and **Event Filter**.
    - TiDB Cloud sink: **TiDB Cloud Connection**, **Table Filter**, and **Event Filter**.
    - Cloud storage sink: **Storage Endpoint**, **Table Filter**, and **Event Filter**.

4. After editing the configuration, click **...** > **Resume** to resume the corresponding changefeed.

## Delete a changefeed

1. Navigate to the cluster overview page of the target TiDB cluster, and then click **Changefeed** in the left navigation pane.
2. Locate the corresponding changefeed you want to delete, and click **...** > **Delete** in the **Action** column.

## Changefeed billing

To learn the billing for changefeeds in TiDB Cloud, see [Changefeed billing](/tidb-cloud/tidb-cloud-billing-ticdc-rcu.md).

## Changefeed states

The state of a replication task represents the running state of the replication task. During the running process, replication tasks might fail with errors, be manually paused, resumed, or reach the specified `TargetTs`. These behaviors can lead to changes of the replication task state.

The states are described as follows:

- `CREATING`: the replication task is being created.
- `RUNNING`: the replication task runs normally and the checkpoint-ts proceeds normally.
- `EDITING`: the replication task is being edited.
- `PAUSING`: the replication task is being paused.
- `PAUSED`: the replication task is paused.
- `RESUMING`: the replication task is being resumed.
- `DELETING`: the replication task is being deleted.
- `DELETED`: the replication task is deleted.
- `WARNING`: the replication task returns a warning. The replication cannot continue due to some recoverable errors. The changefeed in this state keeps trying to resume until the state transfers to `RUNNING`. The changefeed in this state blocks [GC operations](https://docs.pingcap.com/tidb/stable/garbage-collection-overview).
- `FAILED`: the replication task fails. Due to some errors, the replication task cannot resume and cannot be recovered automatically. If the issues are resolved before the garbage collection (GC) of the incremental data, you can manually resume the failed changefeed. The default Time-To-Live (TTL) duration for incremental data is 24 hours, which means that the GC mechanism does not delete any data within 24 hours after the changefeed is interrupted.
