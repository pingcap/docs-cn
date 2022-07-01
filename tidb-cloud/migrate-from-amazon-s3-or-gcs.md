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

Before migrating data from Amazon S3 to TiDB Cloud, ensure the following:

- You have administrator access to your corporate-owned AWS account. 
- You have administrator access to the TiDB Cloud Management Portal.

### Step 1. Create an Amazon S3 bucket and prepare source data files

1. Create an Amazon S3 bucket in your corporate-owned AWS account. 

    For more information, see [Creating a bucket](https://docs.aws.amazon.com/AmazonS3/latest/userguide/create-bucket-overview.html) in the AWS User Guide.

2. If you are migrating data from an upstream database, you need to export the source data first.

    For more information, see [Install TiUP](/tidb-cloud/migrate-data-into-tidb.md#step-1-install-tiup) and [Export data from MySQL compatible databases](/tidb-cloud/migrate-data-into-tidb.md#step-2-export-data-from-mysql-compatible-databases).

> **Note:**
> 
> - Ensure that your source data can be copied to a file format supported by TiDB Cloud. The supported formats include CSV, Dumpling, and Aurora Backup Snapshot. If your source files are in the CSV format, you need to follow [the naming convention supported by TiDB](https://docs.pingcap.com/tidb/stable/migrate-from-csv-using-tidb-lightning#file-name). 
> - Where possible and applicable, it is recommended that you split a large source file into smaller files of maximum size 256 MB because it allows TiDB Cloud to read files in parallel across threads, thereby resulting in potentially enhanced import performance.

### Step 2. Configure Amazon S3 access 

To allow TiDB cloud to access the source data in your Amazon S3 bucket, you need to configure the Amazon S3 for each TiDB Cloud as a service on the AWS project and Amazon S3 bucket pair. Once the configuration is done for one cluster in a project, all database clusters in that project can access the Amazon S3 bucket.

1. Get the TiDB Cloud account ID and external ID of the target TiDB cluster. 

    1. In the TiDB Cloud Admin console, choose a target project and a target cluster deployed on the AWS, and then click **Import**. 
    2. Click **Show AWS IAM policy settings**. The corresponding TiDB Cloud Account ID and TiDB Cloud External ID of the target TiDB cluster are displayed.  
    3. Take a note of the TiDB Cloud Account ID and External ID because they will be used in the following steps. 

2. In the AWS Management Console, go to **IAM** > **Access Management** > **Policies**, and then check whether a storage bucket policy with the following read-only permissions exists.

    - s3:GetObject
    - s3:GetObjectVersion
    - s3:ListBucket
    - s3:GetBucketLocation

    Depending on whether a storage bucket policy with the above permissions exists, do one of the following:
    
    - If yes, you can use the matched storage bucket policy for the target TiDB cluster in the following steps. 
    - If not, go to **IAM** > **Access Management** > **Policies** > **Create Policy**, and define a bucket policy for the target TiDB cluster according to the following policy template.

    {{< copyable "" >}}

    ```
    {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Action": [
                    "s3:GetObject",
                    "s3:GetObjectVersion"
                ],
                "Resource": "arn:aws:s3:::<Your customized directory>"
            },
            {
                "Effect": "Allow",
                "Action": [
                    "s3:ListBucket",
                    "s3:GetBucketLocation"
                ],
                "Resource": "<Your S3 bucket ARN>"
            }
        ]
    }
    ``` 

    In the template, you need to update the following two fields to your own resource values:

    - `"Resource": "<Your S3 bucket ARN>"`: `<Your S3 bucket ARN>` is the ARN of your S3 bucket. You can go to the **Properties** tab in your S3 bucket, and get the Amazon Resource Name (ARN) value in the **Bucket Overview** area. For example, `"Resource": "arn:aws:s3:::tidb-cloud-test"`.
    - `"Resource": "arn:aws:s3:::<Your customized directory>"`: `<Your customized directory>` is a directory that you can customize in your S3 bucket root level for data storage. For example, `"Resource": "arn:aws:s3:::tidb-cloud-test/mydata/*"`. If you want to store your data in the S3 bucket root directory, just use `"Resource": "arn:aws:s3:::tidb-cloud-test/*"`.

3. Go to **IAM** > **Access Management** > **Roles**, and then check whether a role whose trust entity corresponds to the TiDB Cloud Account ID of the target TiDB cluster exists. 

    - If yes, you can use the matched role for the target TiDB cluster in the following steps. 
    - If not, click **Create role**, select **Another AWS account** as the trust entity type, and then enter the TiDB Cloud Account ID of the target TiDB cluster in the **Account ID** field.

4. In **IAM** > **Access Management** > **Roles**, click the role name from the previous step to go to the **Summary** page, and then do the following: 

    1. Under the **Permissions** tab, check whether the storage bucket policy for the target TiDB cluster is attached to the role. 

        If not, choose **Attach Policies**, search for the needed policy, and then click **Attach Policy**.

    2. Click the **Trust relationships** tab, click **Edit trust relationship**, and then check whether the value of the **Condition sts:ExternalId** attribute is the TiDB Cloud External ID of the target TiDB cluster. 

        If not, update the **Condition sts:ExternalId** attribute in the JSON text editor, and then click **Update Trust Policy**. 
        
        The following is a configuration example of the **Condition sts:ExternalId** attribute.

        {{< copyable "" >}}

        ```
        "Condition": {
            "StringEquals": {
            "sts:ExternalId": "696e6672612d61706993147c163238a8a7005caaf40e0338fc"
            }
        }
        ```         

    3. Return to the **Summary** page and copy the **Role ARN** value to your clipboard.

5. In the TiDB Cloud Admin console, go to the screen where you get the TiDB Cloud account ID and external ID of the target TiDB cluster, update the **Role ARN** field using the role value from the previous step. 

Your TiDB Cloud cluster can now access the Amazon S3 bucket.

> **Note:**
>
> To remove access to TiDB Cloud, simply delete the trust policy that you added.

### Step 3. Copy source data files to Amazon S3 and import data into TiDB Cloud 

1. To copy your source data files to your Amazon S3 bucket, you can upload the data to the Amazon S3 bucket using either AWS Web console or AWS CLI.

    - To upload data using the AWS Web console, see [Uploading objects](https://docs.aws.amazon.com/AmazonS3/latest/userguide/upload-objects.html) in the AWS User Guide.
    - To upload data using the AWS CLI, use the following command:

        {{< copyable "shell-regular" >}}

        ```shell
        aws s3 sync <Local path> <S3 URL> 
        ```

        For example:

        {{< copyable "shell-regular" >}}

        ```shell
        aws s3 sync ./tidbcloud-samples-us-west-2/ s3://target-url-in-s3
        ```        

2. From the TiDB Cloud console, navigate to the TiDB Clusters page, and then click the name of your target cluster to go to its own overview page. In the cluster information pane on the left, click **Import**, and then fill in the importing related information on the **Data Import Task** page.

> **Note:**
> 
> To minimize egress charges and latency, locate your Amazon S3 bucket and TiDB Cloud database cluster in the same region. 

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

1. Get the Google Cloud Service Account ID of the target TiDB cluster. 

    1. In the TiDB Cloud Admin console, choose a target project and a target cluster deployed on the Google Cloud Platform, and then click **Import**. 
    2. Click **Show Google Cloud Service Account ID**, and then copy the Service Account ID.

2. In the Google Cloud Platform (GCP) Management Console, go to **IAM & Admin** > **Roles**, and then check whether a role with the following read-only permissions of the storage container exists. 

    - storage.buckets.get
    - storage.objects.get
    - storage.objects. list

    If yes, you can use the matched role for the target TiDB cluster in the following steps. If not, go to **IAM & Admin** > **Roles** > **CREATE ROLE** to define a role for the target TiDB cluster.

3. Go to **Cloud Storage** > **Browser**, select the GCS bucket you want TiDB Cloud to access, and then click **SHOW INFO PANEL**. 

    The panel is displayed. 

4. In the panel, click **ADD PRINCIPAL**. 

    The dialog box for adding principals is displayed. 

5. In the dialog box, perform the following steps:

    1. In the **New Principals** field, paste the Google Cloud Service Account ID of the target TiDB cluster. 
    2. In the **Role** drop-down list, choose the role of the target TiDB cluster. 
    3. Click **SAVE**. 
    
Your TiDB Cloud cluster can now access the GCS bucket.

> **Note:**
>
> To remove the access to TiDB Cloud, you can simply delete the principal that you added.

### Step 3. Copy source data files to GCS and import data into TiDB Cloud 

1. To copy your source data files to your GCS bucket, you can upload the data to the GCS bucket using either Google Cloud Console or gsutil.

    - To upload data using Google Cloud Console, see [Creating storage buckets](https://cloud.google.com/storage/docs/creating-buckets) in Google Cloud Storage documentation.
    - To upload data using gsutil, use the following command:

        {{< copyable "shell-regular" >}}

        ```shell
        gsutil rsync -r <Local path> <GCS URL> 
        ```

        For example:

        {{< copyable "shell-regular" >}}

        ```shell
        gsutil rsync -r ./tidbcloud-samples-us-west-2/ gs://target-url-in-gcs
        ```       

2. From the TiDB Cloud console, navigate to the TiDB Clusters page, and then click the name of your target cluster to go to its own overview page. In the cluster information pane on the left, click **Import**, and then fill in the importing related information on the **Data Import Task** page.

> **Note:**
>
> To minimize egress charges and latency, locate your GCS bucket and TiDB Cloud database cluster in the same region. 
