---
title: Changefeed
---

# Changefeed

TiDB Cloud changefeed helps you stream data from TiDB Cloud to other data services. Currently, TiDB Cloud supports streaming data to Apache Kafka and MySQL.

> **Note:**
>
> To use the changefeed feature, make sure that your TiDB cluster version is v6.4.0 or later and the TiKV node size is at least 8 vCPU and 16 GiB.
>
> Currently, TiDB Cloud only allows up to 10 changefeeds per cluster.
>
> For [Serverless Tier clusters](/tidb-cloud/select-cluster-tier.md#serverless-tier-beta), the changefeed feature is unavailable.

To access the changefeed feature, navigate to the cluster overview page of your TiDB cluster, and then click **Changefeed** in the left navigation pane. The changefeed list is displayed.

In the changefeed list, you can:

- View the information of the created changefeed, including changefeed's id, checkpoint, and status.
- Operate the changefeed, including creating, pausing, resuming, editing, and deleting the changefeed.

## Create a changefeed

To create a changefeed, refer to the tutorials:

- [Sink to Apache Kafka](/tidb-cloud/changefeed-sink-to-apache-kafka.md) (Beta)
- [Sink to MySQL](/tidb-cloud/changefeed-sink-to-mysql.md)

## Delete a changefeed

1. Navigate to the cluster overview page of the target TiDB cluster, and then click **Changefeed** in the left navigation pane.
2. Locate the corresponding changefeed you want to delete, and click **...** > **Delete** in the **Action** column.

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

    - MySQL sink: **MySQL Connection** and **Table Filter**.
    - Kafka sink: all configurations.

4. After editing the configuration, click **...** > **Resume** to resume the corresponding changefeed.

## Query TiCDC RCUs

1. Navigate to the cluster overview page of the target TiDB cluster, and then click **Changefeed** in the left navigation pane.
2. You can see the current TiCDC Replication Capacity Units (RCUs) in the upper-left corner of the page.

## Changefeed billing

To learn the billing for changefeeds in TiDB Cloud, see [Changefeed billing](/tidb-cloud/tidb-cloud-billing-ticdc-rcu.md).
