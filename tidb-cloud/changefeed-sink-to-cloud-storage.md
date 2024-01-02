---
title: Sink to Cloud Storage
Summary: Learn how to create a changefeed to stream data from a TiDB Dedicated cluster to cloud storage, such as Amazon S3 and GCS.
---

# Sink to Cloud Storage

This document describes how to create a changefeed to stream data from TiDB Cloud to cloud storage. Currently, Amazon S3 and GCS are supported.

> **Note:**
>
> - To stream data to cloud storage, make sure that your TiDB cluster version is v7.1.1 or later. To upgrade your TiDB Dedicated cluster to v7.1.1 or later, [contact TiDB Cloud Support](/tidb-cloud/tidb-cloud-support.md).
> - For [TiDB Serverless](/tidb-cloud/select-cluster-tier.md#tidb-serverless) clusters, the changefeed feature is unavailable.

## Restrictions

- For each TiDB Cloud cluster, you can create up to 100 changefeeds.
- Because TiDB Cloud uses TiCDC to establish changefeeds, it has the same [restrictions as TiCDC](https://docs.pingcap.com/tidb/stable/ticdc-overview#unsupported-scenarios).
- If the table to be replicated does not have a primary key or a non-null unique index, the absence of a unique constraint during replication could result in duplicated data being inserted downstream in some retry scenarios.

## Step 1. Configure destination

Navigate to the cluster overview page of the target TiDB cluster. Click **Changefeed** in the left navigation pane, click **Create Changefeed**, and select **Amazon S3** or **GCS** as the destination. The configuration process varies depend on the destination you choose.

<SimpleTab>
<div label="Amazon S3">

For **Amazon S3**, fill the **S3 Endpoint** area: `S3 URI`, `Access Key ID`, and `Secret Access Key`. Make the S3 bucket in the same region with your TiDB cluster.

![s3_endpoint](/media/tidb-cloud/changefeed/sink-to-cloud-storage-s3-endpoint.jpg)

</div>
<div label="GCS">

For **GCS**, before filling **GCS Endpoint**, you need to first grant the GCS bucket access. Take the following steps:

1. In the TiDB Cloud console, record the **Service Account ID**, which will be used to grant TiDB Cloud access to your GCS bucket.

    ![gcs_endpoint](/media/tidb-cloud/changefeed/sink-to-cloud-storage-gcs-endpoint.png)

2. In the Google Cloud console, create an IAM role for your GCS bucket.

    1. Sign in to the [Google Cloud console](https://console.cloud.google.com/).
    2. Go to the [Roles](https://console.cloud.google.com/iam-admin/roles) page, and then click **Create role**.

        ![Create a role](/media/tidb-cloud/changefeed/sink-to-cloud-storage-gcs-create-role.png)

    3. Enter a name, description, ID, and role launch stage for the role. The role name cannot be changed after the role is created. 
    4. Click **Add permissions**. Add the following read-only permissions to the role, and then click **Add**.

        - storage.buckets.get
        - storage.objects.create
        - storage.objects.delete
        - storage.objects.get
        - storage.objects.list
        - storage.objects.update

    ![Add permissions](/media/tidb-cloud/changefeed/sink-to-cloud-storage-gcs-assign-permission.png)

3. Go to the [Bucket](https://console.cloud.google.com/storage/browser) page, and choose a GCS bucket you want TiDB Cloud to access. Note that the GCS bucket must be in the same region as your TiDB cluster.

4. On the **Bucket details** page, click the **Permissions** tab, and then click **Grant access**.

    ![Grant Access to the bucket ](/media/tidb-cloud/changefeed/sink-to-cloud-storage-gcs-grant-access-1.png)

5. Fill in the following information to grant access to your bucket, and then click **Save**.

    - In the **New Principals** field, paste the **Service Account ID** of the target TiDB cluster you recorded before.
    - In the **Select a role** drop-down list, type the name of the IAM role you just created, and then choose the name from the filter result.

    > **Note:**
    >
    > To remove the access to TiDB Cloud, simply remove the access that you have granted.

6. On the **Bucket details** page, click the **Objects** tab.

    - To get a bucket's gsutil URI, click the copy button and add `gs://` as a prefix. For example, if the bucket name is `test-sink-gcs`, the URI would be `gs://test-sink-gcs/`.

        ![Get bucket URI](/media/tidb-cloud/changefeed/sink-to-cloud-storage-gcs-uri01.png)

    - To get a folder's gsutil URI, open the folder, click the copy button, and add `gs://` as a prefix. For example, if the bucket name is `test-sink-gcs` and the folder name is `changefeed-xxx`, the URI would be `gs://test-sink-gcs/changefeed-xxx/`.

        ![Get bucket URI](/media/tidb-cloud/changefeed/sink-to-cloud-storage-gcs-uri02.png)

7. In the TiDB Cloud console, go to the Changefeed's **Configure Destination** page, and fill in the **bucket gsutil URI** field.

</div>
</SimpleTab>

Click **Next** to establish the connection from the TiDB Dedicated cluster to Amazon S3 or GCS. TiDB Cloud will automatically test and verify if the connection is successful.

- If yes, you are directed to the next step of configuration.
- If not, a connectivity error is displayed, and you need to handle the error. After the error is resolved, click **Next** to retry the connection.

## Step 2. Configure replication

1. Customize **Table Filter** to filter the tables that you want to replicate. For the rule syntax, refer to [table filter rules](https://docs.pingcap.com/tidb/stable/ticdc-filter#changefeed-log-filters).

    ![the table filter of changefeed](/media/tidb-cloud/changefeed/sink-to-s3-02-table-filter.jpg)

    - **Filter Rules**: you can set filter rules in this column. By default, there is a rule `*.*`, which stands for replicating all tables. When you add a new rule, TiDB Cloud queries all the tables in TiDB and displays only the tables that match the rules in the box on the right. You can add up to 100 filter rules.
    - **Tables with valid keys**: this column displays the tables that have valid keys, including primary keys or unique indexes.
    - **Tables without valid keys**: this column shows tables that lack primary keys or unique keys. These tables present a challenge during replication because the absence of a unique identifier can result in inconsistent data when handling duplicate events downstream. To ensure data consistency, it is recommended to add unique keys or primary keys to these tables before initiating the replication. Alternatively, you can employ filter rules to exclude these tables. For example, you can exclude the table `test.tbl1` by using the rule `"!test.tbl1"`.

2. Customize **Event Filter** to filter the events that you want to replicate.

    - **Tables matching**: you can set which tables the event filter will be applied to in this column. The rule syntax is the same as that used for the preceding **Table Filter** area. You can add up to 10 event filter rules per changefeed.
    - **Ignored events**: you can set which types of events the event filter will exclude from the changefeed.

3. In the **Start Replication Position** area, select one of the following replication positions:

    - Start replication from now on
    - Start replication from a specific [TSO](https://docs.pingcap.com/tidb/stable/glossary#tso)
    - Start replication from a specific time

4. In the **Data Format** area, select either the **CSV** or **Canal-JSON** format.

    <SimpleTab>
    <div label="Configure CSV format">

    To configure the **CSV** format, fill in the following fields:

    - **Binary Encode Method**: The encoding method for binary data. You can choose **base64** (default) or **hex**. If you want to integrate with AWS DMS, use **hex**.
    - **Date Separator**: To rotate data based on the year, month, and day, or choose not to rotate at all.
    - **Delimiter**: Specify the character used to separate values in the CSV file. The comma (`,`) is the most commonly used delimiter.
    - **Quote**: Specify the character used to enclose values that contain the delimiter character or special characters. Typically, double quotes (`"`) are used as the quote character.
    - **Null/Empty Values**: Specify how null or empty values are represented in the CSV file. This is important for proper handling and interpretation of the data.
    - **Include Commit Ts**: Control whether to include [`commit-ts`](https://docs.pingcap.com/tidb/stable/ticdc-sink-to-cloud-storage#replicate-change-data-to-storage-services) in the CSV row.

    </div>
    <div label="Configure Canal-JSON format">

    Canal-JSON is a plain JSON text format. To configure it, fill in the following fields:

    - **Date Separator**: To rotate data based on the year, month, and day, or choose not to rotate at all.
    - **Enable TiDB Extension**: When you enable this option, TiCDC sends [WATERMARK events](https://docs.pingcap.com/tidb/stable/ticdc-canal-json#watermark-event) and adds the [TiDB extension field](https://docs.pingcap.com/tidb/stable/ticdc-canal-json#tidb-extension-field) to Canal-JSON messages.

    </div>
    </SimpleTab>

5. In the **Flush Parameters** area, you can configure two items:

    - **Flush Interval**: set to 60 seconds by default, adjustable within a range of 2 seconds to 10 minutes;
    - **File Size**: set to 64 MB by default, adjustable within a range of 1 MB to 512 MB.

    ![Flush Parameters](/media/tidb-cloud/changefeed/sink-to-cloud-storage-flush-parameters.jpg)

    > **Note:**
    >
    > These two parameters will affect the quantity of objects generated in cloud storage for each individual database table. If there are a large number of tables, using the same configuration will increase the number of objects generated and subsequently raise the cost of invoking the cloud storage API. Therefore, it is recommended to configure these parameters appropriately based on your Recovery Point Objective (RPO) and cost requirements.

## Step 3. Configure specification

Click **Next** to configure your changefeed specification.

1. In the **Changefeed Specification** area, specify the number of Replication Capacity Units (RCUs) to be used by the changefeed.
2. In the **Changefeed Name** area, specify a name for the changefeed.

## Step 4. Review the configuration and start replication

Click **Next** to review the changefeed configuration.

- If you have verified that all configurations are correct, click **Create** to proceed with the creation of the changefeed.
- If you need to modify any configurations, click **Previous** to go back and make the necessary changes.

The sink will start shortly, and you will observe the status of the sink changing from **Creating** to **Running**.

Click the name of the changefeed to go to its details page. On this page, you can view more information about the changefeed, including the checkpoint status, replication latency, and other relevant metrics.
