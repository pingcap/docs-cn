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

To allow TiDB Cloud to access the source data in your Amazon S3 bucket, take the following steps to configure the bucket access for TiDB Cloud and get the Role-ARN. Once the configuration is done for one TiDB cluster in a project, all TiDB clusters in that project can use the same Role-ARN to access your Amazon S3 bucket.

1. In the TiDB Cloud Console, get the TiDB Cloud account ID and external ID of the target TiDB cluster.

    1. In the TiDB Cloud Console, choose your target project, and then click the name of your target cluster to go to its overview page.
    2. In the cluster overview pane on the left, click **Import**. The **Data Import Task** page is displayed.
    3. On the **Data Import Task** page, click **Show AWS IAM policy settings** to get the TiDB Cloud Account ID and TiDB Cloud External ID. Take a note of these IDs for later use.

2. In the AWS Management Console, create a managed policy for your Amazon S3 bucket.

    1. Sign in to the AWS Management Console and open the Amazon S3 console at <https://console.aws.amazon.com/s3/>.
    2. In the **Buckets** list, choose the name of your bucket with the source data, and then click **Copy ARN** to get your S3 bucket ARN (for example, `arn:aws:s3:::tidb-cloud-source-data`). Take a note of the bucket ARN for later use.

        ![Copy bucket ARN](/media/tidb-cloud/copy-bucket-arn.png)

    3. Open the IAM console at <https://console.aws.amazon.com/iam/>, click **Policies** in the navigation pane on the left, and then click **Create Policy**.

        ![Create a policy](/media/tidb-cloud/aws-create-policy.png)

    4. On the **Create policy** page, click the **JSON** tab.
    5. Copy the following access policy template and paste it to the policy text field.

        ```
        {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Sid": "VisualEditor0",
                    "Effect": "Allow",
                    "Action": [
                        "s3:GetObject",
                        "s3:GetObjectVersion"
                    ],
                    "Resource": "<Your S3 bucket ARN>/<Directory of your source data>/*"
                },
                {
                    "Sid": "VisualEditor1",
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

        In the policy text field, update the following configurations to your own values.

        - `"Resource": "<Your S3 bucket ARN>/<Directory of the source data>/*"`

            For example, if your source data is stored in the root directory of the `tidb-cloud-source-data` bucket, use `"Resource": "arn:aws:s3:::tidb-cloud-source-data/*"`. If your source data is stored in the `mydata` directory of the bucket, use `"Resource": "arn:aws:s3:::tidb-cloud-source-data/mydata/*"`. Make sure that `/*` is added to the end of the directory so TiDB Cloud can access all files in this directory.

        - `"Resource": "<Your S3 bucket ARN>"`

            For example, `"Resource": "arn:aws:s3:::tidb-cloud-source-data"`.

    6. Click **Next: Tags**, add a tag of the policy (optional), and then click **Next:Review**.

    7. Set a policy name, and then click **Create policy**.

3. In the AWS Management Console, create an access role for TiDB Cloud and get the role ARN.

    1. In the IAM console at <https://console.aws.amazon.com/iam/>, click **Roles** in the navigation pane on the left, and then click **Create role**.

        ![Create a role](/media/tidb-cloud/aws-create-role.png)

    2. To create a role, fill in the following information:

        - Under **Trusted entity type**, select **AWS account**.
        - Under **An AWS account**, select **Another AWS account**, and then paste the TiDB Cloud account ID to the **Account ID** field.
        - Under **Options**, click **Require external ID (Best practice when a third party will assume this role)**, and then paste the TiDB Cloud External ID to the **External ID** field.

    3. Click **Next** to open the policy list, choose the policy you just created, and then click **Next**.
    4. Under **Role details**, set a name for the role, and then click **Create role** in the lower-right corner. After the role is created, the list of roles is displayed.
    5. In the list of roles, click the name of the role that you just created to go to its summary page, and then copy the role ARN.

        ![Copy AWS role ARN](/media/tidb-cloud/aws-role-arn.png)

4. In the TiDB Cloud console, go to the **Data Import Task** page where you get the TiDB Cloud account ID and external ID, and then paste the role ARN to the **Role ARN** field.

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

        ```shell
        gsutil rsync -r <Local path> <GCS URL>
        ```

        For example:

        ```shell
        gsutil rsync -r ./tidbcloud-samples-us-west-2/ gs://target-url-in-gcs
        ```

2. From the TiDB Cloud console, navigate to the TiDB Clusters page, and then click the name of your target cluster to go to its own overview page. In the cluster information pane on the left, click **Import**, and then fill in the importing related information on the **Data Import Task** page.

> **Note:**
>
> To minimize egress charges and latency, locate your GCS bucket and TiDB Cloud database cluster in the same region.
