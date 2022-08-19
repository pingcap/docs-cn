---
title: Configure Amazon S3 Access and GCS Access
summary: Learn how to configure Amazon Simple Storage Service (Amazon S3) access and Google Cloud Storage (GCS) access.
---

# Configure Amazon S3 Access and GCS Access

If your source data is stored in Amazon S3 or GCS buckets, before importing or migrating the data to TiDB Cloud, you need to configure cross-account access to the buckets. This document describes how to do this.

- [Configure Amazon S3 access](#configure-amazon-s3-access)
- [Configure GCS access](#configure-gcs-access)

## Configure Amazon S3 access

To allow TiDB Cloud to access the source data in your Amazon S3 bucket, take the following steps to configure the bucket access for TiDB Cloud and get the Role-ARN. Once the configuration is done for one TiDB cluster in a project, all TiDB clusters in that project can use the same Role-ARN to access your Amazon S3 bucket.

1. In the TiDB Cloud Console, get the TiDB Cloud account ID and external ID of the target TiDB cluster.

    1. In the TiDB Cloud Console, choose your target project, and navigate to the **Active Clusters** page.
    2. Find the area of your target cluster and click **Import Data** in the upper-right corner of the area. The **Data Import Task** page is displayed.

        > **Tip:**
        >
        > Alternatively, you can also click the name of your cluster on the **Active Clusters** page and click **Import Data** in the upper-right corner.

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

## Configure GCS access

To allow TiDB cloud to access the source data in your GCS bucket, you need to configure the GCS access for each TiDB Cloud as a service on the GCP project and GCS bucket pair. Once the configuration is done for one cluster in a project, all database clusters in that project can access the GCS bucket.

1. Get the Google Cloud Service Account ID of the target TiDB cluster.

    1. In the TiDB Cloud Admin console, choose a target project and a target cluster deployed on the Google Cloud Platform, and then click **Import Data** in the upper-right corner.
    2. Click **Show Google Cloud Service Account ID**, and then copy the Service Account ID.

2. In the Google Cloud Platform (GCP) Management Console, go to **IAM & Admin** > **Roles**, and then check whether a role with the following read-only permissions of the storage container exists.

    - storage.buckets.get
    - storage.objects.get
    - storage.objects.list

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