---
title: Migrate MySQL-Compatible Databases to TiDB Cloud Using Data Migration
summary: Learn how to migrate data from MySQL-compatible databases hosted in Amazon Aurora MySQL, Amazon Relational Database Service (RDS), Google Cloud SQL for MySQL, or a local MySQL instance to TiDB Cloud using Data Migration.
aliases: ['/tidbcloud/migrate-data-into-tidb','/tidbcloud/migrate-incremental-data-from-mysql']
---

# Migrate MySQL-Compatible Databases to TiDB Cloud Using Data Migration

This document describes how to migrate data from a MySQL-compatible database on a cloud provider (Amazon Aurora MySQL, Amazon Relational Database Service (RDS), or Google Cloud SQL for MySQL) or self-hosted source database to TiDB Cloud using the Data Migration feature of the TiDB Cloud console.

This feature helps you migrate your source databases' existing data and ongoing changes to TiDB Cloud (either in the same region or cross regions) directly in one go.

If you want to migrate incremental data only, see [Migrate Incremental Data from MySQL-Compatible Databases to TiDB Cloud Using Data Migration](/tidb-cloud/migrate-incremental-data-from-mysql-using-data-migration.md).

## Limitations

### Availability

- The Data Migration feature is available only for **TiDB Dedicated** clusters.

- The Data Migration feature is only available to clusters that are created in [certain regions](https://www.pingcap.com/tidb-cloud-pricing-details/#dm-cost) after November 9, 2022. If your **project** was created before the date or if your cluster is in another region, this feature is not available to your cluster and the **Data Migration** tab will not be displayed on the cluster overview page in the TiDB Cloud console.

- Amazon Aurora MySQL writer instances support both existing data and incremental data migration. Amazon Aurora MySQL reader instances only support existing data migration and do not support incremental data migration.

### Maximum number of migration jobs

You can create up to 200 migration jobs for each organization. To create more migration jobs, you need to [file a support ticket](/tidb-cloud/tidb-cloud-support.md).

### Filtered out and deleted databases

- The system databases will be filtered out and not migrated to TiDB Cloud even if you select all of the databases to migrate. That is, `mysql`, `information_schema`, `information_schema`, and `sys` will not be migrated using this feature.

- When you delete a cluster in TiDB Cloud, all migration jobs in that cluster are automatically deleted and not recoverable.

### Limitations of existing data migration

- During existing data migration, if the table to be migrated already exists in the target database with duplicated keys, the duplicate keys will be replaced.

- If your dataset size is smaller than 1 TiB, it is recommended that you use logical mode (the default mode). If your dataset size is larger than 1 TiB, or you want to migrate existing data faster, you can use physical mode. For more information, see [Migrate existing data and incremental data](#migrate-existing-data-and-incremental-data).

### Limitations of incremental data migration

- During incremental data migration, if the table to be migrated already exists in the target database with duplicated keys, an error is reported and the migration is interrupted. In this situation, you need to make sure whether the upstream data is accurate. If yes, click the "Restart" button of the migration job and the migration job will replace the downstream conflicting records with the upstream records.

- During incremental replication (migrating ongoing changes to your cluster), if the migration job recovers from an abrupt error, it might open the safe mode for 60 seconds. During the safe mode, `INSERT` statements are migrated as `REPLACE`, `UPDATE` statements as `DELETE` and `REPLACE`, and then these transactions are migrated to the downstream cluster to make sure that all the data during the abrupt error has been migrated smoothly to the downstream cluster. In this scenario, for upstream tables without primary keys or not-null unique indexes, some data might be duplicated in the downstream cluster because the data might be inserted repeatedly to the downstream.

- In the following scenarios, if the migration job takes longer than 24 hours, do not purge binary logs in the source database to ensure that Data Migration can get consecutive binary logs for incremental replication:

    - During existing data migration.
    - After the existing data migration is completed and when incremental data migration is started for the first time, the latency is not 0ms.

## Prerequisites

Before performing the migration, you need to check the data sources, prepare privileges for upstream and downstream databases, and set up network connections.

### Make sure your data source and version are supported

Data Migration supports the following data sources and versions:

- MySQL 5.6, 5.7, and 8.0 local instances or on a public cloud provider. Note that MySQL 8.0 is still experimental on TiDB Cloud and might have incompatibility issues.
- Amazon Aurora (MySQL 5.6 and 5.7)
- Amazon RDS (MySQL 5.7)
- Google Cloud SQL for MySQL 5.6 and 5.7

### Grant required privileges to the upstream database

The username you use for the upstream database must have all the following privileges:

| Privilege | Scope |
|:----|:----|
| `SELECT` | Tables |
| `LOCK` | Tables |
| `REPLICATION SLAVE` | Global |
| `REPLICATION CLIENT` | Global |

For example, you can use the following `GRANT` statement to grant corresponding privileges:

```sql
GRANT SELECT,LOCK TABLES,REPLICATION SLAVE,REPLICATION CLIENT ON *.* TO 'your_user'@'your_IP_address_of_host'
```

### Grant required privileges to the downstream TiDB Cloud cluster

The username you use for the downstream TiDB Cloud cluster must have the following privileges:

| Privilege | Scope |
|:----|:----|
| `CREATE` | Databases, Tables |
| `SELECT` | Tables |
| `INSERT` | Tables |
| `UPDATE` | Tables |
| `DELETE` | Tables |
| `ALTER`  | Tables |
| `DROP`   | Databases, Tables |
| `INDEX`  | Tables |
| `TRUNCATE`  | Tables |

For example, you can execute the following `GRANT` statement to grant corresponding privileges:

```sql
GRANT CREATE,SELECT,INSERT,UPDATE,DELETE,ALTER,TRUNCATE,DROP,INDEX ON *.* TO 'your_user'@'your_IP_address_of_host'
```

To quickly test a migration job, you can use the `root` account of the TiDB Cloud cluster.

### Set up network connection

Before creating a migration job, set up the network connection according to your connection methods. See [Connect to Your TiDB Dedicated Cluster](/tidb-cloud/connect-to-tidb-cluster.md).

- If you use public IP (this is, standard connection) for network connection, make sure that the upstream database can be connected through the public network.

- If you use AWS VPC Peering or Google Cloud VPC Network Peering, see the following instructions to configure the network.

<details>
<summary> Set up AWS VPC Peering</summary>

If your MySQL service is in an AWS VPC, take the following steps:

1. [Set up a VPC peering connection](/tidb-cloud/set-up-vpc-peering-connections.md) between the VPC of the MySQL service and your TiDB cluster.

2. Modify the inbound rules of the security group that the MySQL service is associated with.

    You must add [the CIDR of the region where your TiDB Cloud cluster is located](/tidb-cloud/set-up-vpc-peering-connections.md#prerequisite-set-a-project-cidr) to the inbound rules. Doing so allows the traffic to flow from your TiDB cluster to the MySQL instance.

3. If the MySQL URL contains a DNS hostname, you need to allow TiDB Cloud to be able to resolve the hostname of the MySQL service.

    1. Follow the steps in [Enable DNS resolution for a VPC peering connection](https://docs.aws.amazon.com/vpc/latest/peering/modify-peering-connections.html#vpc-peering-dns).
    2. Enable the **Accepter DNS resolution** option.

</details>

<details>
<summary> Set up Google Cloud VPC Network Peering </summary>

If your MySQL service is in a Google Cloud VPC, take the following steps:

1. If it is a self-hosted MySQL, you can skip this step and proceed to the next step. If your MySQL service is Google Cloud SQL, you must expose a MySQL endpoint in the associated VPC of the Google Cloud SQL instance. You might need to use the [Cloud SQL Auth proxy](https://cloud.google.com/sql/docs/mysql/sql-proxy) developed by Google.

2. [Set up a VPC peering connection](/tidb-cloud/set-up-vpc-peering-connections.md) between the VPC of your MySQL service and your TiDB cluster.

3. Modify the ingress firewall rules of the VPC where MySQL is located.

    You must add [the CIDR of the region where your TiDB Cloud cluster is located](/tidb-cloud/set-up-vpc-peering-connections.md#prerequisite-set-a-project-cidr) to the ingress firewall rules. This allows the traffic to flow from your TiDB cluster to the MySQL endpoint.

</details>

### Enable binary logs

To perform incremental data migration, make sure you have enabled binary logs of the upstream database, and the binary logs have been kept for more than 24 hours.

## Step 1: Go to the **Data Migration** page

1. Log in to the [TiDB Cloud console](https://tidbcloud.com/) and navigate to the [**Clusters**](https://tidbcloud.com/console/clusters) page of your project.

    > **Tip:**
    >
    > If you have multiple projects, you can click <MDSvgIcon name="icon-left-projects" /> in the lower-left corner and switch to another project.

2. Click the name of your target cluster to go to its overview page, and then click **Data Migration** in the left navigation pane.

3. On the **Data Migration** page, click **Create Migration Job** in the upper-right corner. The **Create Migration Job** page is displayed.

## Step 2: Configure the source and target connection

On the **Create Migration Job** page, configure the source and target connection.

1. Enter a job name, which must start with a letter and must be less than 60 characters. Letters (A-Z, a-z), numbers (0-9), underscores (_), and hyphens (-) are acceptable.

2. Fill in the source connection profile.

   - **Data source**: the data source type.
   - **Region**: the region of the data source, which is required for cloud databases only.
   - **Connectivity method**: the connection method for the data source. Currently, you can choose public IP, VPC Peering, or Private Link according to your connection method.
   - **Hostname or IP address** (for public IP and VPC Peering): the hostname or IP address of the data source.
   - **Service Name** (for Private Link): the endpoint service name.
   - **Port**: the port of the data source.
   - **Username**: the username of the data source.
   - **Password**: the password of the username.
   - **SSL/TLS**: if you enable SSL/TLS, you need to upload the certificates of the data source, including any of the following:
        - only the CA certificate
        - the client certificate and client key
        - the CA certificate, client certificate and client key

3. Fill in the target connection profile.

   - **Username**: enter the username of the target cluster in TiDB Cloud.
   - **Password**: enter the password of the TiDB Cloud username.

4. Click **Validate Connection and Next** to validate the information you have entered.

5. Take action according to the message you see:

    - If you use Public IP or VPC Peering, you need to add the Data Migration service's IP addresses to the IP Access List of your source database and firewall (if any).
    - If you use AWS Private Link, you are prompted to accept the endpoint request. Go to the [AWS VPC console](https://us-west-2.console.aws.amazon.com/vpc/home), and click **Endpoint services** to accept the endpoint request.

## Step 3: Choose migration job type

In the **Choose the objects to be migrated** step, you can choose existing data migration, incremental data migration, or both.

### Migrate existing data and incremental data

To migrate data to TiDB Cloud once and for all, choose both **Existing data migration** and **Incremental data migration**, which ensures data consistency between the source and target databases.

You can use **physical mode** or **logical mode** to migrate **existing data**.

- The default mode is **logical mode**. This mode exports data from upstream databases as SQL statements, and then executes them on TiDB. In this mode, the target tables before migration can be either empty or non-empty. But the performance is slower than physical mode.

- For large datasets, it is recommended to use **physical mode**. This mode exports data from upstream databases and encodes it as KV pairs, writing directly to TiKV to achieve faster performance. This mode requires the target tables to be empty before migration. For the specification of 16 RCUs (Replication Capacity Units), the performance is about 2.5 times faster than logical mode. The performance of other specifications can increase by 20% to 50% compared with logical mode. Note that the performance data is for reference only and might vary in different scenarios.

Physical mode is available for TiDB clusters deployed on AWS and Google Cloud.

> **Note:**
>
> - When you use physical mode, you cannot create a second migration job or import task for the TiDB cluster before the existing data migration is completed.
> - When you use physical mode and the migration job has started, do **NOT** enable PITR (Point-in-time Recovery) or have any changefeed on the cluster. Otherwise, the migration job will be stuck. If you need to enable PITR or have any changefeed, use logical mode instead to migrate data.

Physical mode exports the upstream data as fast as possible, so [different specifications](/tidb-cloud/tidb-cloud-billing-dm.md#specifications-for-data-migration) have different performance impacts on QPS and TPS of the upstream database during data export. The following table shows the performance regression of each specification.

| Migration specification |  Maximum export speed | Performance regression of the upstream database |
|---------|-------------|--------|
| 2 RCUs   | 80.84 MiB/s  | 15.6% |
| 4 RCUs   | 214.2 MiB/s  | 20.0% |
| 8 RCUs   | 365.5 MiB/s  | 28.9% |
| 16 RCUs | 424.6 MiB/s  | 46.7% |

### Migrate only existing data

To migrate only existing data of the source database to TiDB Cloud, choose **Existing data migration**.

You can choose to use physical mode or logical mode to migrate existing data. For more information, see [Migrate existing data and incremental data](#migrate-existing-data-and-incremental-data).

### Migrate only incremental data

To migrate only the incremental data of the source database to TiDB Cloud, choose **Incremental data migration**. In this case, the migration job does not migrate the existing data of the source database to TiDB Cloud, but only migrates the ongoing changes of the source database that are explicitly specified by the migration job.

For detailed instructions about incremental data migration, see [Migrate Only Incremental Data from MySQL-Compatible Databases to TiDB Cloud Using Data Migration](/tidb-cloud/migrate-incremental-data-from-mysql-using-data-migration.md).

## Step 4: Choose the objects to be migrated

1. On the **Choose Objects to Migrate** page, select the objects to be migrated. You can click **All** to select all objects, or click **Customize** and then click the checkbox next to the object name to select the object.

    - If you click **All**, the migration job will migrate the existing data from the whole source database instance to TiDB Cloud and migrate ongoing changes after the full migration. Note that it happens only if you have selected the **Existing data migration** and **Incremental data migration** checkboxes in the previous step.

        <img src="https://download.pingcap.com/images/docs/tidb-cloud/migration-job-select-all.png" width="60%" />

    - If you click **Customize** and select some databases, the migration job will migrate the existing data and migrate ongoing changes of the selected databases to TiDB Cloud. Note that it happens only if you have selected the **Existing data migration** and **Incremental data migration** checkboxes in the previous step.

        <img src="https://download.pingcap.com/images/docs/tidb-cloud/migration-job-select-db.png" width="60%" />

    - If you click **Customize** and select some tables under a dataset name, the migration job only will migrate the existing data and migrate ongoing changes of the selected tables. Tables created afterwards in the same database will not be migrated.

        <img src="https://download.pingcap.com/images/docs/tidb-cloud/migration-job-select-tables.png" width="60%" />

    <!--
    - If you click **Customize** and select some databases, and then select some tables in the **Selected Objects** area to move them back to the **Source Database** area, (for example the `username` table in the following screenshots), then the tables will be treated as in a blocklist. The migration job will migrate the existing data but filter out the excluded tables (such as the `username` table in the screenshots), and will migrate ongoing changes of the selected databases to TiDB Cloud except the filtered-out tables.
        ![Select Databases and Deselect Some Tables](/media/tidb-cloud/migration-job-select-db-blacklist1.png)
        ![Select Databases and Deselect Some Tables](/media/tidb-cloud/migration-job-select-db-blacklist2.png)
    -->

2. Click **Next**.

## Step 5: Precheck

On the **Precheck** page, you can view the precheck results. If the precheck fails, you need to operate according to **Failed** or **Warning** details, and then click **Check again** to recheck.

If there are only warnings on some check items, you can evaluate the risk and consider whether to ignore the warnings. If all warnings are ignored, the migration job will automatically go on to the next step.

For more information about errors and solutions, see [Precheck errors and solutions](/tidb-cloud/tidb-cloud-dm-precheck-and-troubleshooting.md#precheck-errors-and-solutions).

For more information about precheck items, see [Migration Task Precheck](https://docs.pingcap.com/tidb/stable/dm-precheck).

If all check items show **Pass**, click **Next**.

## Step 6: Choose a spec and start migration

On the **Choose a Spec and Start Migration** page, select an appropriate migration specification according to your performance requirements. For more information about the specifications, see [Specifications for Data Migration](/tidb-cloud/tidb-cloud-billing-dm.md#specifications-for-data-migration).

After selecting the spec, click **Create Job and Start** to start the migration.

## Step 7: View the migration progress

After the migration job is created, you can view the migration progress on the **Migration Job Details** page. The migration progress is displayed in the **Stage and Status** area.

You can pause or delete a migration job when it is running.

If a migration job has failed, you can resume it after solving the problem.

You can delete a migration job in any status.

If you encounter any problems during the migration, see [Migration errors and solutions](/tidb-cloud/tidb-cloud-dm-precheck-and-troubleshooting.md#migration-errors-and-solutions).

## Scale a migration job specification

TiDB Cloud supports scaling up or down a migration job specification to meet your performance and cost requirements in different scenarios.

Different migration specifications have different performances. Your performance requirements might vary at different stages as well. For example, during the existing data migration, you want the performance to be as fast as possible, so you choose a migration job with a large specification, such as 8 RCU. Once the existing data migration is completed, the incremental migration does not require such a high performance, so you can scale down the job specification, for example, from 8 RCU to 2 RUC, to save cost.

When scaling a migration job specification, note the following:

- It takes about 5 to 10 minutes to scale a migration job specification.
- If the scaling fails, the job specification remains the same as it was before the scaling.

### Limitations

- You can only scale a migration job specification when the job is in the **Running** or **Paused** status.
- TiDB Cloud does not support scaling a migration job specification during the existing data export stage.
- Scaling a migration job specification will restart the job. If a source table of the job does not have a primary key, duplicate data might be inserted.
- During scaling, do not purge the binary log of the source database or increase `expire_logs_days` of the upstream database temporarily. Otherwise, the job might fail because it cannot get the continuous binary log position.

### Scaling procedure

1. Log in to the [TiDB Cloud console](https://tidbcloud.com/) and navigate to the [**Clusters**](https://tidbcloud.com/console/clusters) page of your project.

2. Click the name of your target cluster to go to its overview page, and then click **Data Migration** in the left navigation pane.

3. On the **Data Migration** page, locate the migration job you want to scale. In the **Action** column, click **...** > **Scale Up/Down**.

4. In the **Scale Up/Down** window, select the new specification you want to use, and then click **Submit**. You can view the new price of the specification at the bottom of the window.
