---
title: Migrate from MySQL-Compatible Databases to TiDB Cloud Using AWS DMS
summary: Learn how to migrate data from MySQL-compatible databases to TiDB Cloud using AWS Database Migration Service (AWS DMS).
---

# Migrate from MySQL-Compatible Databases to TiDB Cloud Using AWS DMS

If you want to migrate heterogeneous databases, such as PostgreSQL, Oracle, and SQL Server to TiDB Cloud, it is recommended to use AWS Database Migration Service (AWS DMS).

AWS DMS is a cloud service that makes it easy to migrate relational databases, data warehouses, NoSQL databases, and other types of data stores. You can use AWS DMS to migrate your data into TiDB Cloud.

This document uses Amazon RDS as an example to show how to migrate data to TiDB Cloud using AWS DMS. The procedure also applies to migrating data from self-hosted MySQL databases or Amazon Aurora to TiDB Cloud.

In this example, the data source is Amazon RDS, and the data destination is a TiDB Dedicated cluster in TiDB Cloud. Both upstream and downstream databases are in the same region.

## Prerequisites

Before you start the migration, make sure you have read the following:

- If the source database is Amazon RDS or Amazon Aurora, you need to set the `binlog_format` parameter to `ROW`. If the database uses the default parameter group, the `binlog_format` parameter is `MIXED` by default and cannot be modified. In this case, you need to [create a new parameter group](https://docs.aws.amazon.com/dms/latest/userguide/CHAP_GettingStarted.Prerequisites.html#CHAP_GettingStarted.Prerequisites.params), for example `newset`, and set its `binlog_format` to `ROW`. Then, [modify the default parameter group](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_WorkingWithDBInstanceParamGroups.html#USER_WorkingWithParamGroups.Modifying) to `newset`. Note that modifying the parameter group will restart the database.
- Check and ensure that the source database uses collations that are compatible with TiDB. The default collation for the utf8mb4 character set in TiDB is `utf8mb4_bin`. But in MySQL 8.0, the default collation is `utf8mb4_0900_ai_ci`. If the upstream MySQL uses the default collation, because TiDB is not compatible with `utf8mb4_0900_ai_ci`, AWS DMS cannot create the target tables in TiDB and cannot migrate the data. To resolve this problem, you need to modify the collation of the source database to `utf8mb4_bin` before the migration. For a complete list of TiDB supported character sets and collations, see [Character Set and Collation](https://docs.pingcap.com/tidb/stable/character-set-and-collation).
- TiDB contains the following system databases by default: `INFORMATION_SCHEMA`, `PERFORMANCE_SCHEMA`, `mysql`, `sys`, and `test`. When you create an AWS DMS migration task, you need to filter out these system databases instead of using the default `%` to select the migration object. Otherwise, AWS DMS will try to migrate these system databases from the source database to the target TiDB, which will cause the task to fail. To avoid this issue, it is recommended to fill in the specific database and table names.
- Add the public and private network IP addresses of AWS DMS to the IP access lists of both source and target databases. Otherwise, the network connection might fail in some scenarios.
- Use [VPC Peerings](/tidb-cloud/set-up-vpc-peering-connections.md#set-up-vpc-peering-on-aws) or [Private Endpoint connections](/tidb-cloud/set-up-private-endpoint-connections.md) to connect AWS DMS and the TiDB cluster.
- It is recommended to use the same region for AWS DMS and the TiDB cluster to get better data writing performance.
- It is recommended to use AWS DMS `dms.t3.large` (2 vCPUs and 8 GiB memory) or a higher instance class. Small instance classes will possibly cause out of memory (OOM) errors.
- AWS DMS will automatically create the `awsdms_control` database in the target database.

## Limitation

AWS DMS does not support replicating `DROP TABLE`.

## Step 1. Create an AWS DMS replication instance

1. Go to the [Replication instances](https://console.aws.amazon.com/dms/v2/home#replicationInstances) page in the AWS DMS console, and switch to the corresponding region. It is recommended to use the same region for AWS DMS as TiDB Cloud. In this document, the upstream and downstream databases and the DMS instance are all in the **us-west-2** region.

2. Click **Create replication instance**.

    ![Create replication instance](/media/tidb-cloud/aws-dms-tidb-cloud/aws-dms-to-tidb-cloud-create-instance.png)

3. Fill in an instance name, ARN, and description.

4. Fill in the instance configuration:
    - **Instance class**: select an appropriate instance class. It is recommended to use `dms.t3.large` or a higher instance class to get better performance.
    - **Engine version**: use the default configuration.
    - **Multi-AZ**: select **Single-AZ** or **Multi-AZ** based on your business needs.

5. Configure the storage in the **Allocated storage (GiB)** field. Use the default configuration.

6. Configure connectivity and security.
    - **Network type - new**: select **IPv4**.
    - **Virtual private cloud (VPC) for IPv4**: select the VPC that you need. It is recommended to use the same VPC as the upstream database to simplify the network configuration.
    - **Replication subnet group**: choose a subnet group for your replication instance.
    - **Public accessible**: use the default configuration.

7. Configure the **Advanced settings**, **Maintenance**, and **Tags** if needed. Click **Create replication instance** to finish the instance creation.

## Step 2. Create the source database endpoint

1. In the [AWS DMS console](https://console.aws.amazon.com/dms/v2/home), click the replication instance that you just created. Copy the public and private network IP addresses as shown in the following screenshot.

    ![Copy the public and private network IP addresses](/media/tidb-cloud/aws-dms-tidb-cloud/aws-dms-to-tidb-cloud-copy-ip.png)

2. Configure the security group rules for Amazon RDS. In this example, add the public and private IP addresses of the AWS DMS instance to the security group.

    ![Configure the security group rules](/media/tidb-cloud/aws-dms-tidb-cloud/aws-dms-to-tidb-cloud-rules.png)

3. Click **Create endpoint** to create the source database endpoint.

    ![Click Create endpoint](/media/tidb-cloud/aws-dms-tidb-cloud/aws-dms-to-tidb-cloud-endpoint.png)

4. In this example, click **Select RDS DB instance** and then select the source RDS instance. If the source database is a self-hosted MySQL, you can skip this step and fill in the information in the following steps.

    ![Select RDS DB instance](/media/tidb-cloud/aws-dms-tidb-cloud/aws-dms-to-tidb-cloud-select-rds.png)

5. Configure the following information:
   - **Endpoint identifier**: create a label for the source endpoint to help you identify it in the subsequent task configuration.
   - **Descriptive Amazon Resource Name (ARN) - optional**: create a friendly name for the default DMS ARN.
   - **Source engine**: select **MySQL**.
   - **Access to endpoint database**: select **Provide access information manually**.
   - **Server name**: fill in the name of the data server for the data provider. You can copy it from the database console. If the upstream is Amazon RDS or Amazon Aurora, the name will be automatically filled in. If it is a self-hosted MySQL without a domain name, you can fill in the IP address.
   - Fill in the source database **Port**, **Username**, and **Password**.
   - **Secure Socket Layer (SSL) mode**: you can enable SSL mode as needed.

    ![Fill in the endpoint configurations](/media/tidb-cloud/aws-dms-tidb-cloud/aws-dms-to-tidb-cloud-endpoint-config.png)

6. Use default values for **Endpoint settings**, **KMS key**, and **Tags**. In the **Test endpoint connection (optional)** section, it is recommended to select the same VPC as the source database to simplify the network configuration. Select the corresponding replication instance, and then click **Run test**. The status needs to be **successful**.

7. Click **Create endpoint**.

    ![Click Create endpoint](/media/tidb-cloud/aws-dms-tidb-cloud/aws-dms-to-tidb-cloud-connection.png)

## Step 3. Create the target database endpoint

1. In the [AWS DMS console](https://console.aws.amazon.com/dms/v2/home), click the replication instance that you just created. Copy the public and private network IP addresses as shown in the following screenshot.

    ![Copy the public and private network IP addresses](/media/tidb-cloud/aws-dms-tidb-cloud/aws-dms-to-tidb-cloud-copy-ip.png)

2. In the TiDB Cloud console, go to the [**Clusters**](https://tidbcloud.com/console/clusters) page, click the name of your target cluster, and then click **Connect** in the upper-right corner to get the TiDB Cloud database connection information.

3. Under **Step 1: Create traffic filter** in the dialog, click **Edit**, enter the public and private network IP addresses that you copied from the AWS DMS console, and then click **Update Filter**. It is recommended to add the public IP address and private IP address of the AWS DMS replication instance to the TiDB cluster traffic filter at the same time. Otherwise, AWS DMS might not be able to connect to the TiDB cluster in some scenarios.

4. Click **Download TiDB cluster CA** to download the CA certificate. Under **Step 3: Connect with a SQL client** in the dialog, take a note of the `-u`, `-h`, and `-P` information in the connection string for later use.

5. Click the **VPC Peering** tab in the dialog, and then click **Add** under **Step 1: Set up VPC** to create a VPC Peering connection for the TiDB cluster and AWS DMS.

6. Configure the corresponding information. See [Set Up VPC Peering Connections](/tidb-cloud/set-up-vpc-peering-connections.md).

7. Configure the target endpoint for the TiDB cluster.
    - **Endpoint type**: select **Target endpoint**.
    - **Endpoint identifier**: fill in a name for the endpoint.
    - **Descriptive Amazon Resource Name (ARN) - optional**: create a friendly name for the default DMS ARN.
    - **Target engine**: select **MySQL**.

    ![Configure the target endpoint](/media/tidb-cloud/aws-dms-tidb-cloud/aws-dms-to-tidb-cloud-target-endpoint.png)

8. In the [AWS DMS console](https://console.aws.amazon.com/dms/v2/home), click **Create endpoint** to create the target database endpoint, and then configure the following information:
    - **Server name**: fill in the hostname of your TiDB cluster, which is the `-h` information you have recorded.
    - **Port**: enter the port of your TiDB cluster, which is the `-P` information you have recorded. The default port of a TiDB cluster is 4000.
    - **User name**: enter the user name of your TiDB cluster, which is the `-u` information you have recorded.
    - **Password**: enter the password of your TiDB cluster.
    - **Secure Socket Layer (SSL) mode**: select **Verify-ca**.
    - Click **Add new CA certificate** to import the CA file downloaded from the TiDB Cloud console in the previous steps.

    ![Fill in the target endpoint information](/media/tidb-cloud/aws-dms-tidb-cloud/aws-dms-to-tidb-cloud-target-endpoint2.png)

9. Import the CA file.

    ![Upload CA](/media/tidb-cloud/aws-dms-tidb-cloud/aws-dms-to-tidb-cloud-upload-ca.png)

10. Use the default values for **Endpoint settings**, **KMS key**, and **Tags**. In the **Test endpoint connection (optional)** section, select the same VPC as the source database. Select the corresponding replication instance, and then click **Run test**. The status needs to be **successful**.

11. Click **Create endpoint**.

    ![Click Create endpoint](/media/tidb-cloud/aws-dms-tidb-cloud/aws-dms-to-tidb-cloud-target-endpoint3.png)

## Step 4. Create a database migration task

1. In the AWS DMS console, go to the [Data migration tasks](https://console.aws.amazon.com/dms/v2/home#tasks) page. Switch to your region. Then click **Create task** in the upper-right corner of the window.

    ![Create task](/media/tidb-cloud/aws-dms-tidb-cloud/aws-dms-to-tidb-cloud-create-task.png)

2. Configure the following information:
    - **Task identifier**: fill in a name for the task. It is recommended to use a name that is easy to remember.
    - **Descriptive Amazon Resource Name (ARN) - optional**: create a friendly name for the default DMS ARN.
    - **Replication instance**: select the AWS DMS instance that you just created.
    - **Source database endpoint**: select the source database endpoint that you just created.
    - **Target database endpoint**: select the target database endpoint that you just created.
    - **Migration type**: select a migration type as needed. In this example, select **Migrate existing data and replicate ongoing changes**.

    ![Task configurations](/media/tidb-cloud/aws-dms-tidb-cloud/aws-dms-to-tidb-cloud-task-config.png)

3. Configure the following information:
    - **Editing mode**: select **Wizard**.
    - **Custom CDC stop mode for source transactions**: use the default setting.
    - **Target table preparation mode**: select **Do nothing** or other options as needed. In this example, select **Do nothing**.
    - **Stop task after full load completes**: use the default setting.
    - **Include LOB columns in replication**: select **Limited LOB mode**.
    - **Maximum LOB size in (KB)**: use the default value **32**.
    - **Turn on validation**: select it according to your needs.
    - **Task logs**: select **Turn on CloudWatch logs** for troubleshooting in future. Use the default settings for the related configurations.

    ![Task settings](/media/tidb-cloud/aws-dms-tidb-cloud/aws-dms-to-tidb-cloud-task-settings.png)

4. In the **Table mappings** section, specify the database to be migrated.

    The schema name is the database name in the Amazon RDS instance. The default value of the **Source name** is "%", which means that all databases in the Amazon RDS will be migrated to TiDB. It will cause the system databases such as `mysql` and `sys` in Amazon RDS to be migrated to the TiDB cluster, and result in task failure. Therefore, it is recommended to fill in the specific database name, or filter out all system databases. For example, according to the settings in the following screenshot, only the database named `franktest` and all the tables in that database will be migrated.

    ![Table mappings](/media/tidb-cloud/aws-dms-tidb-cloud/aws-dms-to-tidb-cloud-table-mappings.png)

5. Click **Create task** in the lower-right corner.

6. Go back to the [Data migration tasks](https://console.aws.amazon.com/dms/v2/home#tasks) page. Switch to your region. You can see the status and progress of the task.

    ![Tasks status](/media/tidb-cloud/aws-dms-tidb-cloud/aws-dms-to-tidb-cloud-task-status.png)

If you encounter any issues or failures during the migration, you can check the log information in [CloudWatch](https://console.aws.amazon.com/cloudwatch/home) to troubleshoot the issues.

![Troubleshooting](/media/tidb-cloud/aws-dms-tidb-cloud/aws-dms-to-tidb-cloud-troubleshooting.png)

## See also

- If you want to migrate from MySQL-compatible databases, such as Aurora MySQL and Amazon Relational Database Service (RDS), to TiDB Cloud, it is recommended to use [Data Migration on TiDB Cloud](/tidb-cloud/migrate-from-mysql-using-data-migration.md).

- If you want to migrate from Amazon RDS for Oracle to TiDB Serverless Using AWS DMS, see [Migrate from Amazon RDS for Oracle to TiDB Serverless Using AWS DMS](/tidb-cloud/migrate-from-oracle-using-aws-dms.md).
