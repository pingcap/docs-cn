---
title: Migrate Only Incremental Data from MySQL-Compatible Databases to TiDB Cloud Using Data Migration
summary: Learn how to migrate incremental data from MySQL-compatible databases hosted in Amazon Aurora MySQL, Amazon Relational Database Service (RDS), Google Cloud SQL for MySQL, or a local MySQL instance to TiDB Cloud using Data Migration.
---

# Migrate Only Incremental Data from MySQL-Compatible Databases to TiDB Cloud Using Data Migration

This document describes how to migrate incremental data from a MySQL-compatible database on a cloud provider (Amazon Aurora MySQL, Amazon Relational Database Service (RDS), or Google Cloud SQL for MySQL) or self-hosted source database to TiDB Cloud using the Data Migration feature of the TiDB Cloud console.

For instructions about how to migrate existing data or both existing data and incremental data, see [Migrate MySQL-Compatible Databases to TiDB Cloud Using Data Migration](/tidb-cloud/migrate-from-mysql-using-data-migration.md).

## Limitations

> **Note**:
>
> This section only includes limitations about incremental data migration. It is recommended that you also read the general limitations. See [Limitations](/tidb-cloud/migrate-from-mysql-using-data-migration.md#limitations).

- If the target table is not yet created in the target database, the migration job will report an error as follows and fail. In this case, you need to manually create the target table and then retry the migration job.

    ```sql
    startLocation: [position: (mysql_bin.000016, 5122), gtid-set:
    00000000-0000-0000-0000-00000000000000000], endLocation:
    [position: (mysql_bin.000016, 5162), gtid-set: 0000000-0000-0000
    0000-0000000000000:0]: cannot fetch downstream table schema of
    zm`.'table1' to initialize upstream schema 'zm'.'table1' in sschema
    tracker Raw Cause: Error 1146: Table 'zm.table1' doesn't exist
    ```

- If some rows are deleted or updated in the upstream and there are no corresponding rows in the downstream, the migration job will detect that there are no rows available for deletion or update when replicating the `DELETE` and `UPDATE` DML operations from the upstream.

If you specify GTID as the start position to migrate incremental data, note the following limitations:

- Make sure that the GTID mode is enabled in the source database.
- If the source database is MySQL, the MySQL version must be 5.6 or later, and the storage engine must be InnoDB.
- If the migration job connects to a secondary database in the upstream, the `REPLICATE CREATE TABLE ... SELECT` events cannot be migrated. This is because the statement will be split into two transactions (`CREATE TABLE` and `INSERT`) that are assigned the same GTID. As a result, the `INSERT` statement will be ignored by the secondary database.

## Prerequisites

> **Note**:
>
> This section only includes prerequisites about incremental data migration. It is recommended that you also read the [general prerequisites](/tidb-cloud/migrate-from-mysql-using-data-migration.md#prerequisites).

If you want to use GTID to specify the start position, make sure that the GTID is enabled in the source database. The operations vary depending on the database type.

### For Amazon RDS and Amazon Aurora MySQL

For Amazon RDS and Amazon Aurora MySQL, you need to create a new modifiable parameter group (that is, not the default parameter group) and then modify the following parameters in the parameter group and restart the instance application.

- `gtid_mode`
- `enforce_gtid_consistency`

You can check if the GTID mode has been successfully enabled by executing the following SQL statement:

```sql
SHOW VARIABLES LIKE 'gtid_mode';
```

If the result is `ON` or `ON_PERMISSIVE`, the GTID mode is successfully enabled.

For more information, see [Parameters for GTID-based replication](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/mysql-replication-gtid.html#mysql-replication-gtid.parameters).

### For Google Cloud SQL for MySQL

The GTID mode is enabled for Google Cloud SQL for MySQL by default. You can check if the GTID mode has been successfully enabled by executing the following SQL statement:

```sql
SHOW VARIABLES LIKE 'gtid_mode';
```

If the result is `ON` or `ON_PERMISSIVE`, the GTID mode is successfully enabled.

### For a self-hosted MySQL instance

> **Note**:
>
> The exact steps and commands might vary depending on the MySQL version and configuration. Make sure that you understand the impact of enabling GTID and that you have properly tested and verified it in a non-production environment before performing this action.

To enable the GTID mode for a self-hosted MySQL instance, follow these steps:

1. Connect to the MySQL server using a MySQL client with the appropriate privileges.

2. Execute the following SQL statements to enable the GTID mode:

    ```sql
    -- Enable the GTID mode
    SET GLOBAL gtid_mode = ON;

    -- Enable `enforce_gtid_consistency`
    SET GLOBAL enforce_gtid_consistency = ON;

    -- Reload the GTID configuration
    RESET MASTER;
    ```

3. Restart the MySQL server to ensure that the configuration changes take effect.

4. Check if the GTID mode has been successfully enabled by executing the following SQL statement:

    ```sql
    SHOW VARIABLES LIKE 'gtid_mode';
    ```

    If the result is `ON` or `ON_PERMISSIVE`, the GTID mode is successfully enabled.

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

To migrate only the incremental data of the source database to TiDB Cloud, select **Incremental data migration** and do not select **Existing data migration**. In this way, the migration job only migrates ongoing changes of the source database to TiDB Cloud.

In the **Start Position** area, you can specify one of the following types of start positions for incremental data migration:

- The time when the incremental migration job starts
- GTID
- Binlog file name and position

Once a migration job starts, you cannot change the start position.

### The time when the incremental migration job starts

If you select this option, the migration job will only migrate the incremental data that is generated in the source database after the migration job starts.

### Specify GTID

Select this option to specify the GTID of the source database, for example, `3E11FA47-71CA-11E1-9E33-C80AA9429562:1-23`. The migration job will replicate the transactions excluding the specified GTID set to migrate ongoing changes of the source database to TiDB Cloud.

You can run the following command to check the GTID of the source database:

```sql
SHOW MASTER STATUS;
```

For information about how to enable GTID, see [Prerequisites](#prerequisites).

### Specify binlog file name and position

Select this option to specify the binlog file name (for example, `binlog.000001`) and binlog position (for example, `1307`) of the source database. The migration job will start from the specified binlog file name and position to migrate ongoing changes of the source database to TiDB Cloud.

You can run the following command to check the binlog file name and position of the source database:

```sql
SHOW MASTER STATUS;
```

If there is data in the target database, make sure the binlog position is correct. Otherwise, there might be conflicts between the existing data and the incremental data. If conflicts occur, the migration job will fail. If you want to replace the conflicted records with data from the source database, you can resume the migration job.

## Step 4: Choose the objects to be migrated

1. On the **Choose Objects to Migrate** page, select the objects to be migrated. You can click **All** to select all objects, or click **Customize** and then click the checkbox next to the object name to select the object.

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
