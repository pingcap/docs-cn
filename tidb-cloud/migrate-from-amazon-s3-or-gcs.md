---
title: Import or Migrate from Amazon S3 or GCS to TiDB Cloud
summary: Learn how to import or migrate data from Amazon Simple Storage Service (Amazon S3) or Google Cloud Storage (GCS) to TiDB Cloud.
---

# Import or Migrate from Amazon S3 or GCS to TiDB Cloud

This document describes how to use Amazon Simple Storage Service (Amazon S3) or Google Cloud Storage (GCS) as a staging area for importing or migrating data into TiDB Cloud.

> **Note:**
>
> If your upstream database is Amazon Aurora MySQL, instead of referring to this document, follow instructions in [Migrate from Amazon Aurora MySQL to TiDB Cloud in Bulk](/tidb-cloud/migrate-from-aurora-bulk-import.md).

## Import or migrate from Amazon S3 to TiDB Cloud

If your organization is using TiDB Cloud as a service on AWS, you can use Amazon S3 as a staging area for importing or migrating data into TiDB Cloud.

### Prerequisites

Before migrating data from Amazon S3 to TiDB Cloud, ensure you have administrator access to your corporate-owned AWS account.

### Step 1. Create an Amazon S3 bucket and prepare source data files

1. Create an Amazon S3 bucket in your corporate-owned AWS account.

    For more information, see [Creating a bucket](https://docs.aws.amazon.com/AmazonS3/latest/userguide/create-bucket-overview.html) in the AWS User Guide.

    > **Note:**
    >
    > To minimize egress charges and latency, create your Amazon S3 bucket and TiDB Cloud database cluster in the same region.

2. If you are migrating data from an upstream database, you need to export the source data first.

    For more information, see [Migrate Data from MySQL-Compatible Databases](/tidb-cloud/migrate-data-into-tidb.md).

3. If your source data is in local files, you can upload the files to the Amazon S3 bucket using either the Amazon S3 Console or the AWS CLI.

    - To upload files using the Amazon S3 Console, see [Uploading objects](https://docs.aws.amazon.com/AmazonS3/latest/userguide/upload-objects.html) in the AWS User Guide.
    - To upload files using the AWS CLI, use the following command:

        ```shell
        aws s3 sync <Local path> <Amazon S3 bucket URL>
        ```

        For example:

        ```shell
        aws s3 sync ./tidbcloud-samples-us-west-2/ s3://tidb-cloud-source-data
        ```

> **Note:**
>
> - Ensure that your source data can be copied to a file format supported by TiDB Cloud. The supported formats include CSV, Dumpling, and Aurora Backup Snapshot. If your source files are in the CSV format, you need to follow [the naming convention supported by TiDB](https://docs.pingcap.com/tidb/stable/migrate-from-csv-using-tidb-lightning#file-name).
> - Where possible and applicable, it is recommended that you split a large source file into smaller files of maximum size 256 MB. It allows TiDB Cloud to read files in parallel across threads, thereby resulting in potentially enhanced import performance.

### Step 2. Configure Amazon S3 access

To allow TiDB Cloud to access the source data in your Amazon S3 bucket, you need to configure the bucket access for TiDB Cloud and get the Role-ARN. Once the configuration is done for one TiDB cluster in a project, all TiDB clusters in that project can use the same Role-ARN to access your Amazon S3 bucket.

For detailed steps, see [Configure Amazon S3 access](/tidb-cloud/config-s3-and-gcs-access.md#configure-amazon-s3-access).

### Step 3. Import data into TiDB Cloud

1. On the **Data Import Task** page, besides the **Role ARN** field, you also need to fill in the following information:

    - **Data Source Type**: `AWS S3`.
    - **Bucket URL**: fill in the bucket URL of your source data.
    - **Data Format**: choose the format of your data.
    - **Target Cluster**: fill in the **Username** and **Password** fields.
    - **DB/Tables Filter**: if necessary, you can specify a [table filter](/table-filter.md#syntax). If you want to configure multiple filter rules, use `,` to separate the rules.

2. Click **Import**.

    A warning message about the database resource consumption is displayed.

3. Click **Confirm**.

    TiDB Cloud starts validating whether it can access your data in the specified bucket URL. After the validation is completed and successful, the import task starts automatically. If you get the `AccessDenied` error, see [Troubleshoot Access Denied Errors during Data Import from S3](/tidb-cloud/troubleshoot-import-access-denied-error.md).

After the data is imported, if you want to remove the Amazon S3 access of TiDB Cloud, simply delete the policy that you added in [Step 2. Configure Amazon S3 access](#step-2-configure-amazon-s3-access).

## Import or migrate from GCS to TiDB Cloud

If your organization is using TiDB Cloud as a service on Google Cloud Platform (GCP), you can use Google Cloud Storage (GCS) as a staging area for importing or migrating data into TiDB Cloud.

### Prerequisites

Before migrating data from GCS to TiDB Cloud, ensure the following:

- You have administrator access to your corporate-owned GCP account.
- You have administrator access to the TiDB Cloud Management Portal.

### Step 1. Create a GCS bucket and prepare source data files

1. Create a GCS bucket in your corporate-owned GCP account. 

    For more information, see [Creating storage buckets](https://cloud.google.com/storage/docs/creating-buckets) in the Google Cloud Storage documentation.

2. If you are migrating data from an upstream database, you need to export the source data first.

    For more information, see [Install TiUP](/tidb-cloud/migrate-data-into-tidb.md#step-1-install-tiup) and [Export data from MySQL compatible databases](/tidb-cloud/migrate-data-into-tidb.md#step-2-export-data-from-mysql-compatible-databases).

> **Note:**
> 
> - Ensure that your source data can be copied to a file format supported by TiDB Cloud. The supported formats include CSV, Dumpling, and Aurora Backup Snapshot. If your source files are in the CSV format, you need to follow [the naming convention supported by TiDB](https://docs.pingcap.com/tidb/stable/migrate-from-csv-using-tidb-lightning#file-name). 
> - Where possible and applicable, it is recommended that you split a large source file into smaller files of maximum size 256 MB because it can allow TiDB Cloud to read files in parallel across threads, which provides you faster importing performance.

### Step 2. Configure GCS access 

To allow TiDB cloud to access the source data in your GCS bucket, you need to configure the GCS access for each TiDB Cloud as a service on the GCP project and GCS bucket pair. Once the configuration is done for one cluster in a project, all database clusters in that project can access the GCS bucket.

For detailed steps, see [Configure GCS access](/tidb-cloud/config-s3-and-gcs-access.md#configure-gcs-access).

### Step 3. Copy source data files to GCS and import data into TiDB Cloud

1. To copy your source data files to your GCS bucket, you can upload the data to the GCS bucket using either Google Cloud Console or gsutil.

    - To upload data using Google Cloud Console, see [Creating storage buckets](https://cloud.google.com/storage/docs/creating-buckets) in Google Cloud Storage documentation.
    - To upload data using gsutil, use the following command:

        ```shell
        gsutil rsync -r <Local path> <GCS URL>
        ```

        For example:

        ```shell
        gsutil rsync -r ./tidbcloud-samples-us-west-2/ gs://target-url-in-gcs
        ```

2. From the TiDB Cloud console, navigate to the TiDB Clusters page, and then click the name of your target cluster to go to its own overview page. In the upper-right corner, click **Import Data**, and then fill in the importing related information on the **Data Import Task** page.

> **Note:**
>
> To minimize egress charges and latency, locate your GCS bucket and TiDB Cloud database cluster in the same region.
