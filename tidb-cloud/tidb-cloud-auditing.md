---
title: Database Audit Logging
summary: Learn about how to audit a cluster in TiDB Cloud.
---

# Database Audit Logging

TiDB Cloud provides you with a database audit logging feature to record a history of user access details (such as any SQL statements executed) in logs.

> **Note:**
>
> Currently, the database audit logging feature is only available upon request. To request this feature, click **?** in the lower-right corner of the [TiDB Cloud console](https://tidbcloud.com) and click **Request Support**. Then, fill in "Apply for database audit logging" in the **Description** field and click **Send**.

To assess the effectiveness of user access policies and other information security measures of your organization, it is a security best practice to conduct a periodic analysis of the database audit logs.

The audit logging feature is disabled by default. To audit a cluster, you need to enable the audit logging first, and then specify the auditing filter rules.

> **Note:**
>
> Because audit logging consumes cluster resources, be prudent about whether to audit a cluster.

## Prerequisites

- You are using a TiDB Dedicated cluster. Audit logging is not available for TiDB Serverless clusters.
- You are in the `Organization Owner` or `Project Owner` role of your organization. Otherwise, you cannot see the database audit-related options in the TiDB Cloud console. For more information, see [User roles](/tidb-cloud/manage-user-access.md#user-roles).

## Enable audit logging for AWS or Google Cloud

To allow TiDB Cloud to write audit logs to your cloud bucket, you need to enable audit logging first.

### Enable audit logging for AWS

To enable audit logging for AWS, take the following steps:

#### Step 1. Create an Amazon S3 bucket

Specify an Amazon S3 bucket in your corporate-owned AWS account as a destination to which TiDB Cloud writes the audit logs.

For more information, see [Creating a bucket](https://docs.aws.amazon.com/AmazonS3/latest/userguide/create-bucket-overview.html) in the AWS User Guide.

#### Step 2. Configure Amazon S3 access

> **Note:**
>
> Once the Amazon S3 access configuration is performed for one cluster in a project, you can use the same bucket as a destination for audit logs from all clusters in the same project.

1. Get the TiDB Cloud account ID and the External ID of the TiDB cluster that you want to enable audit logging.

    1. In the TiDB Cloud console, choose a project and a cluster deployed on AWS.
    2. Select **Settings** > **Audit Settings**. The **Audit Logging** dialog is displayed.
    3. In the **Audit Logging** dialog, click **Show AWS IAM policy settings**. The corresponding TiDB Cloud Account ID and TiDB Cloud External ID of the TiDB cluster are displayed.
    4. Record the TiDB Cloud Account ID and the External ID for later use.

2. In the AWS Management Console, go to **IAM** > **Access Management** > **Policies**, and then check whether there is a storage bucket policy with the `s3:PutObject` write-only permission.

    - If yes, record the matched storage bucket policy for later use.
    - If not, go to **IAM** > **Access Management** > **Policies** > **Create Policy**, and define a bucket policy according to the following policy template.

        ```json
        {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Effect": "Allow",
                    "Action": "s3:PutObject",
                    "Resource": "<Your S3 bucket ARN>/*"
                }
            ]
        }
        ```

        In the template, `<Your S3 bucket ARN>` is the Amazon Resource Name (ARN) of your S3 bucket where the audit log files are to be written. You can go to the **Properties** tab in your S3 bucket and get the ARN value in the **Bucket Overview** area. In the `"Resource"` field, you need to add `/*` after the ARN. For example, if the ARN is `arn:aws:s3:::tidb-cloud-test`, you need to configure the value of the `"Resource"` field as `"arn:aws:s3:::tidb-cloud-test/*"`.

3. Go to **IAM** > **Access Management** > **Roles**, and then check whether a role whose trust entity corresponds to the TiDB Cloud Account ID and the External ID that you recorded earlier already exists.

    - If yes, record the matched role for later use.
    - If not, click **Create role**, select **Another AWS account** as the trust entity type, and then enter the TiDB Cloud Account ID value into the **Account ID** field. Then, choose the **Require External ID** option and enter the TiDB Cloud External ID value into the **External ID** field.

4. In **IAM** > **Access Management** > **Roles**, click the role name from the previous step to go to the **Summary** page, and then take the following steps:

    1. Under the **Permissions** tab, check whether the recorded policy with the `s3:PutObject` write-only permission is attached to the role. If not, choose **Attach Policies**, search for the needed policy, and then click **Attach Policy**.
    2. Return to the **Summary** page and copy the **Role ARN** value to your clipboard.

#### Step 3. Enable audit logging

In the TiDB Cloud console, go back to the **Audit Logging** dialog box where you got the TiDB Cloud account ID and the External ID values, and then take the following steps:

1. In the **Bucket URI** field, enter the URI of your S3 bucket where the audit log files are to be written.
2. In the **Bucket Region** drop-down list, select the AWS region where the bucket locates.
3. In the **Role ARN** field, fill in the Role ARN value that you copied in [Step 2. Configure Amazon S3 access](#step-2-configure-amazon-s3-access).
4. Click **Test Connectivity** to verify whether TiDB Cloud can access and write to the bucket.

    If it is successful, **Pass** is displayed. Otherwise, check your access configuration.

5. In the upper-right corner, toggle the audit setting to **On**.

    TiDB Cloud is ready to write audit logs for the specified cluster to your Amazon S3 bucket.

> **Note:**
>
> - After enabling audit logging, if you make any new changes to the bucket URI, location, or ARN, you must click **Restart** to load the changes and rerun the **Test Connectivity** check to make the changes effective.
> - To remove Amazon S3 access from TiDB Cloud, simply delete the trust policy that you added.

### Enable audit logging for Google Cloud

To enable audit logging for Google Cloud, take the following steps:

#### Step 1. Create a GCS bucket

Specify a Google Cloud Storage (GCS) bucket in your corporate-owned Google Cloud account as a destination to which TiDB Cloud writes audit logs.

For more information, see [Creating storage buckets](https://cloud.google.com/storage/docs/creating-buckets) in the Google Cloud Storage documentation.

#### Step 2. Configure GCS access

> **Note:**
>
> Once the GCS access configuration is performed for one cluster in a project, you can use the same bucket as a destination for audit logs from all clusters in the same project.

1. Get the Google Cloud Service Account ID of the TiDB cluster that you want to enable audit logging.

    1. In the TiDB Cloud console, choose a project and a cluster deployed on Google Cloud Platform.
    2. Select **Settings** > **Audit Settings**. The **Audit Logging** dialog box is displayed.
    3. Click **Show Google Cloud Service Account ID**, and then copy the Service Account ID for later use.

2. In the Google Cloud console, go to **IAM & Admin** > **Roles**, and then check whether a role with the following write-only permissions of the storage container exists.

    - storage.objects.create
    - storage.objects.delete

    If yes, record the matched role for the TiDB cluster for later use. If not, go to **IAM & Admin** > **Roles** > **CREATE ROLE** to define a role for the TiDB cluster.

3. Go to **Cloud Storage** > **Browser**, select the GCS bucket you want TiDB Cloud to access, and then click **SHOW INFO PANEL**.

    The panel is displayed.

4. In the panel, click **ADD PRINCIPAL**.

    The dialog box for adding principals is displayed.

5. In the dialog box, take the following steps:

    1. In the **New Principals** field, paste the Google Cloud Service Account ID of the TiDB cluster.
    2. In the **Role** drop-down list, choose the role of the target TiDB cluster.
    3. Click **SAVE**.

#### Step 3. Enable audit logging

In the TiDB Cloud console, go back to the **Audit Logging** dialog box where you got the TiDB Cloud account ID, and then take the following steps:

1. In the **Bucket URI** field, enter your full GCS bucket name.
2. In the **Bucket Region** field, select the GCS region where the bucket locates.
3. Click **Test Connectivity** to verify whether TiDB Cloud can access and write to the bucket.

    If it is successful, **Pass** is displayed. Otherwise, check your access configuration.

4. In the upper-right corner, toggle the audit setting to **On**.

    TiDB Cloud is ready to write audit logs for the specified cluster to your Amazon S3 bucket.

> **Note:**
>
> - After enabling audit logging, if you make any new changes to bucket URI or location, you must click **Restart** to load the changes and rerun the **Test Connectivity** check to make the changes effective.
> - To remove GCS access from TiDB Cloud, simply delete the principal that you added.

## Specify auditing filter rules

After enabling audit logging, you must specify auditing filter rules to control which user access events to capture and write to audit logs versus which events to ignore. If no filter rules are specified, TiDB Cloud does not log anything.

To specify auditing filter rules for a cluster, take the following steps:

1. In the **Audit Logging** dialog box where you enable audit logging, scroll down and locate the **Filter Rules** section.
2. Add one or more filter rules, one rule per row, with each rule specifying a user expression, database expression, table expression, and access type.

> **Note:**
>
> - The filter rules are regular expressions and case-sensitive. If you use the wildcard rule `.*`, all users, databases, or table events in the cluster are logged.
> - Because audit logging consumes cluster resources, be prudent when specifying filter rules. To minimize the consumption, it is recommended that you specify filter rules to limit the scope of audit logging to specific database objects, users, and actions, where possible.

## View audit logs

TiDB Cloud audit logs are readable text files with the cluster ID, Pod ID, and log creation date incorporated into the fully qualified filenames.

For example, `13796619446086334065/tidb-0/tidb-audit-2022-04-21T18-16-29.529.log`. In this example, `13796619446086334065` indicates the cluster ID and `tidb-0` indicates the Pod ID.

## Disable audit logging

If you no longer want to audit a cluster, go to the page of the cluster, click **Settings** > **Audit Settings**, and then toggle the audit setting in the upper-right corner to **Off**.

> **Note:**
>
> Each time the size of the log file reaches 10 MiB, the log file will be pushed to the cloud storage bucket. Therefore, after the audit log is disabled, the log file whose size is smaller than 10 MiB will not be automatically pushed to the cloud storage bucket. To get the log file in this situation, contact [PingCAP support](/tidb-cloud/tidb-cloud-support.md).

## Audit log fields

For each database event record in audit logs, TiDB provides the following fields:

> **Note:**
>
> In the following tables, the empty maximum length of a field means that the data type of this field has a well-defined constant length (for example, 4 bytes for INTEGER).

| Col # | Field name | TiDB data type | Maximum length | Description |
|---|---|---|---|---|
| 1 | N/A | N/A | N/A | Reserved for internal use |
| 2 | N/A | N/A | N/A | Reserved for internal use |
| 3 | N/A | N/A | N/A | Reserved for internal use |
| 4 | ID       | INTEGER |  | Unique event ID  |
| 5 | TIMESTAMP | TIMESTAMP |  | Time of event   |
| 6 | EVENT_CLASS | VARCHAR | 15 | Event type     |
| 7 | EVENT_SUBCLASS     | VARCHAR | 15 | Event subtype |
| 8 | STATUS_CODE | INTEGER |  | Response status of the statement   |
| 9 | COST_TIME | FLOAT |  | Time consumed by the statement    |
| 10 | HOST | VARCHAR | 16 | Server IP    |
| 11 | CLIENT_IP         | VARCHAR | 16 | Client IP   |
| 12 | USER | VARCHAR | 17 | Login username    |
| 13 | DATABASE | VARCHAR | 64 | Event-related database      |
| 14 | TABLES | VARCHAR | 64 | Event-related table name          |
| 15 | SQL_TEXT | VARCHAR | 64 KB | Masked SQL statement   |
| 16 | ROWS | INTEGER |  | Number of affected rows (`0` indicates that no rows are affected)      |

Depending on the EVENT_CLASS field value set by TiDB, database event records in audit logs also contain additional fields as follows:

- If the EVENT_CLASS value is `CONNECTION`, database event records also contain the following fields:

    | Col # | Field name | TiDB data type | Maximum length | Description |
    |---|---|---|---|---|
    | 17 | CLIENT_PORT | INTEGER |  | Client port number |
    | 18 | CONNECTION_ID | INTEGER |  | Connection ID |
    | 19 | CONNECTION_TYPE  | VARCHAR | 12 | Connection via `socket` or `unix-socket` |
    | 20 | SERVER_ID | INTEGER |  | TiDB server ID |
    | 21 | SERVER_PORT | INTEGER |  | The port that the TiDB server uses to listen to client communicating via the MySQL protocol |
    | 22 | SERVER_OS_LOGIN_USER | VARCHAR | 17 | The username of the TiDB process startup system  |
    | 23 | OS_VERSION | VARCHAR | N/A | The version of the operating system where the TiDB server is located  |
    | 24 | SSL_VERSION | VARCHAR | 6 | The current SSL version of TiDB |
    | 25 | PID | INTEGER |  | The PID of the TiDB process |

- If the EVENT_CLASS value is `TABLE_ACCESS` or `GENERAL`, database event records also contain the following fields:

    | Col # | Field name | TiDB data type | Maximum length | Description |
    |---|---|---|---|---|
    | 17 | CONNECTION_ID | INTEGER |  | Connection ID   |
    | 18 | COMMAND | VARCHAR | 14 | The command type of the MySQL protocol |
    | 19 | SQL_STATEMENT  | VARCHAR | 17 | The SQL statement type |
    | 20 | PID | INTEGER |  | The PID of the TiDB process  |
