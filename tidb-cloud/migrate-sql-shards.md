---
title: Migrate and Merge MySQL Shards of Large Datasets to TiDB Cloud
summary: Learn how to migrate and merge MySQL shards of large datasets to TiDB Cloud.
---

# Migrate and Merge MySQL Shards of Large Datasets to TiDB Cloud

This document describes how to migrate and merge a large MySQL dataset (for example, more than 1 TiB) from different partitions into TiDB Cloud. After full data migration, you can use [TiDB Data Migration (DM)](https://docs.pingcap.com/tidb/stable/dm-overview) to perform incremental migration according to your business needs.

The example in this document uses a complex shard migration task across multiple MySQL instances, and involves handling conflicts in auto-increment primary keys. The scenario in this example is also applicable to merging data from different sharded tables within a single MySQL instance.

## Environment information in the example

This section describes the basic information of the upstream cluster, DM, and downstream cluster used in the example.

### Upstream cluster

The environment information of the upstream cluster is as follows:

- MySQL version: MySQL v5.7.18
- MySQL instance1:
    - schema `store_01` and table `[sale_01, sale_02]`
    - schema `store_02` and table `[sale_01, sale_02]`
- MySQL instance 2:
    - schema `store_01`and table `[sale_01, sale_02]`
    - schema `store_02`and table `[sale_01, sale_02]`
- Table structure:

  ```sql
  CREATE TABLE sale_01 (
  id bigint(20) NOT NULL auto_increment,
  uid varchar(40) NOT NULL,
  sale_num bigint DEFAULT NULL,
  PRIMARY KEY (id),
  UNIQUE KEY ind_uid (uid)
  );
  ```

### DM

The version of DM is v5.3.0. You need to deploy TiDB DM manually. For detailed steps, see [Deploy a DM Cluster Using TiUP](https://docs.pingcap.com/tidb/stable/deploy-a-dm-cluster-using-tiup).

### External storage

This document uses the Amazon S3 as an example.

### Downstream cluster

The sharded schemas and tables are merged into the table `store.sales`.

## Perform full data migration from MySQL to TiDB Cloud

The following is the procedure to migrate and merge full data of MySQL shards to TiDB Cloud.

In the following example, you only need to export the data in tables to **CSV** format.

### Step 1. Create directories in the Amazon S3 bucket

Create a first-level directory `store` (corresponding to the level of databases) and a second-level directory `sales` (corresponding to the level of tables) in the Amazon S3 bucket. In `sales`, create a third-level directory for each MySQL instance (corresponding to the level of MySQL instances). For example:

- Migrate the data in MySQL instance1 to `s3://dumpling-s3/store/sales/instance01/`
- Migrate the data in MySQL instance2 to `s3://dumpling-s3/store/sales/instance02/`

If there are shards across multiple instances, you can create one first-level directory for each database and create one second-level directory for each sharded table. Then create a third-level directory for each MySQL instance for easy management. For example, if you want to migrate and merge tables `stock_N.product_N` from MySQL instance1 and MySQL instance2 into the table `stock.products` in TiDB Cloud, you can create the following directories:

- `s3://dumpling-s3/stock/products/instance01/`
- `s3://dumpling-s3/stock/products/instance02/`

### Step 2. Use Dumpling to export data to Amazon S3

For information about how to install Dumpling, see [Dumpling Introduction](https://docs.pingcap.com/tidb/stable/dumpling-overview).

When you use Dumpling to export data to Amazon S3, note the following:

- Enable binlog for upstream clusters.
- Choose the correct Amazon S3 directory and region.
- Choose the appropriate concurrency by configuring the `-t` option to minimize the impact on the upstream cluster, or export directly from the backup database. For more information about how to use this parameter, see [Option list of Dumpling](https://docs.pingcap.com/tidb/stable/dumpling-overview#option-list-of-dumpling).
- Set appropriate values for `--filetype csv` and `--no-schemas`. For more information about how to use these parameters, see [Option list of Dumpling](https://docs.pingcap.com/tidb/stable/dumpling-overview#option-list-of-dumpling).

Name the CSV files as follows:

- If the data of one table is separated into multiple CSV files, append a numeric suffix to these CSV files. For example, `${db_name}.${table_name}.000001.csv` and `${db_name}.${table_name}.000002.csv`. The numeric suffixes can be inconsecutive but must be in ascending order. You also need to add extra zeros before the number to ensure all the suffixes are in the same length.

> **Note:**
>
> If you cannot update the CSV filenames according to the preceding rules in some cases (for example, the CSV file links are also used by your other programs), you can keep the filenames unchanged and use the **File Patterns** in [Step 5](#step-5-perform-the-data-import-task) to import your source data to a single target table.

To export data to Amazon S3, do the following:

1. Get the `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY` of the Amazon S3 bucket.

    ```shell
    [root@localhost ~]# export AWS_ACCESS_KEY_ID={your_aws_access_key_id}
    [root@localhost ~]# export AWS_SECRET_ACCESS_KEY= {your_aws_secret_access_key}
    ```

2. Export data from MySQL instance1 to the `s3://dumpling-s3/store/sales/instance01/` directory in the Amazon S3 bucket.

    ```shell
    [root@localhost ~]# tiup dumpling -u {username} -p {password} -P {port} -h {mysql01-ip} -B store_01,store_02 -r 20000 --filetype csv --no-schemas -o "s3://dumpling-s3/store/sales/instance01/" --s3.region "ap-northeast-1"
    ```

    For more information about the parameters, see [Option list of Dumpling](https://docs.pingcap.com/tidb/stable/dumpling-overview#option-list-of-dumpling).

3. Export data from MySQL instance2 to the `s3://dumpling-s3/store/sales/instance02/` directory in the Amazon S3 bucket.

    ```shell
    [root@localhost ~]# tiup dumpling -u {username} -p {password} -P {port} -h {mysql02-ip} -B store_01,store_02 -r 20000 --filetype csv --no-schemas -o "s3://dumpling-s3/store/sales/instance02/" --s3.region "ap-northeast-1"
    ```

For detailed steps, see [Export data to Amazon S3 cloud storage](https://docs.pingcap.com/tidb/stable/dumpling-overview#export-data-to-amazon-s3-cloud-storage).

### Step 3. Create schemas in TiDB Cloud cluster

Create schemas in the TiDB Cloud cluster as follows:

```sql
mysql> CREATE DATABASE store;
Query OK, 0 rows affected (0.16 sec)
mysql> use store;
Database changed
```

In this example, the column IDs of the upstream tables `sale_01` and `sale_02` are auto-increment primary keys. Conflicts might occur when you merge sharded tables in the downstream database. Execute the following SQL statement to set the ID column as a normal index instead of a primary key:

```sql
mysql> CREATE TABLE `sales` (
         `id` bigint(20) NOT NULL ,
         `uid` varchar(40) NOT NULL,
         `sale_num` bigint DEFAULT NULL,
         INDEX (`id`),
         UNIQUE KEY `ind_uid` (`uid`)
        );
Query OK, 0 rows affected (0.17 sec)
```

For more information about the solutions to solve such conflicts, see [Remove the PRIMARY KEY attribute from the column](https://docs.pingcap.com/tidb/stable/shard-merge-best-practices#remove-the-primary-key-attribute-from-the-column).

### Step 4. Configure Amazon S3 access

Follow the instructions in [Configure Amazon S3 access](/tidb-cloud/config-s3-and-gcs-access.md#configure-amazon-s3-access) to get the role ARN to access the source data.

The following example only lists key policy configurations. Replace the Amazon S3 path with your own values.

```yaml
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
           "Resource": [
               "arn:aws:s3:::dumpling-s3/*"
           ]
       },
       {
           "Sid": "VisualEditor1",
           "Effect": "Allow",
           "Action": [
               "s3:ListBucket",
               "s3:GetBucketLocation"
           ],

           "Resource": "arn:aws:s3:::dumpling-s3"
       }
   ]
}
```

### Step 5. Perform the data import task

After configuring the Amazon S3 access, you can perform the data import task in the TiDB Cloud console as follows:

1. Open the **Import** page for your target cluster.

    1. Log in to the [TiDB Cloud console](https://tidbcloud.com/) and navigate to the [**Clusters**](https://tidbcloud.com/console/clusters) page of your project.

        > **Tip:**
        >
        > If you have multiple projects, you can click <MDSvgIcon name="icon-left-projects" /> in the lower-left corner and switch to another project.

    2. Click the name of your target cluster to go to its overview page, and then click **Import** in the left navigation pane.

2. On the **Import** page, click **Import Data** in the upper-right corner, and then select **From S3**.

3. On the **Import from S3** page, fill in the following information:

    - **Data format**: select **CSV**.
    - **Bucket URI**: fill in the bucket URI of your source data. You can use the second-level directory corresponding to tables, `s3://dumpling-s3/store/sales` in this example, so that TiDB Cloud can import and merge the data in all MySQL instances into `store.sales` in one go.
    - **Role ARN**: enter the Role-ARN you obtained.

    If the location of the bucket is different from your cluster, confirm the compliance of cross region. Click **Next**.

    TiDB Cloud starts validating whether it can access your data in the specified bucket URI. After validation, TiDB Cloud tries to scan all the files in the data source using the default file naming pattern, and returns a scan summary result on the left side of the next page. If you get the `AccessDenied` error, see [Troubleshoot Access Denied Errors during Data Import from S3](/tidb-cloud/troubleshoot-import-access-denied-error.md).

4. Modify the file patterns and add the table filter rules if needed.

    - **File Pattern**: modify the file pattern if you want to import CSV files whose filenames match a certain pattern to a single target table.

        > **Note:**
        >
        > When you use this feature, one import task can only import data to a single table at a time. If you want to use this feature to import data into different tables, you need to import several times, each time specifying a different target table.

        To modify the file pattern, click **Modify**, specify a custom mapping rule between CSV files and a single target table in the following fields, and then click **Scan**.

        - **Source file name**: enter a pattern that matches the names of the CSV files to be imported. If you have one CSV file only, enter the file name here directly. Note that the names of the CSV files must include the suffix ".csv".

            For example:

            - `my-data?.csv`: all CSV files starting with `my-data` and one character (such as `my-data1.csv` and `my-data2.csv`) will be imported into the same target table.
            - `my-data*.csv`: all CSV files starting with `my-data` will be imported into the same target table.

        - **Target table name**: enter the name of the target table in TiDB Cloud, which must be in the `${db_name}.${table_name}` format. For example, `mydb.mytable`. Note that this field only accepts one specific table name, so wildcards are not supported.

    - **Table Filter**: If you want to filter which tables to be imported, you can specify one or more [table filter](/table-filter.md#syntax) rules in this area.

5. Click **Next**.

6. On the **Preview** page, you can have a preview of the data. If the previewed data is not what you expect, click the **Click here to edit csv configuration** link to update the CSV-specific configurations, including separator, delimiter, header, `backslash escape`, and `trim last separator`.

    > **Note:**
    >
    > For the configurations of separator, delimiter, and null, you can use both alphanumeric characters and certain special characters. The supported special characters include `\t`, `\b`, `\n`, `\r`, `\f`, and `\u0001`.

7. Click **Start Import**.

8. When the import progress shows **Finished**, check the imported tables.

After the data is imported, if you want to remove the Amazon S3 access of TiDB Cloud, simply delete the policy that you added.

## Perform incremental data replication from MySQL to TiDB Cloud

To replicate the data changes based on binlog from a specified position in the upstream cluster to TiDB Cloud, you can use TiDB Data Migration (DM) to perform incremental replication.

### Before you begin

If you want to migrate incremental data and merge MySQL shards to TiDB Cloud, you need to manually deploy TiDB DM, because TiDB Cloud does not support migrating and merging MySQL shards yet. For detailed steps, see [Deploy a DM Cluster Using TiUP](https://docs.pingcap.com/tidb/stable/deploy-a-dm-cluster-using-tiup).

### Step 1. Add the data source

1. Create a new data source file `dm-source1.yaml` to configure an upstream data source into DM. Add the following content:

    ```yaml
    # MySQL Configuration.
    source-id: "mysql-replica-01"
    # Specifies whether DM-worker pulls binlogs with GTID (Global Transaction Identifier).
    # The prerequisite is that you have already enabled GTID in the upstream MySQL.
    # If you have configured the upstream database service to switch master between different nodes automatically, you must enable GTID.
    enable-gtid: true
    from:
     host: "${host}"           # For example: 192.168.10.101
     user: "user01"
     password: "${password}"   # Plaintext passwords are supported but not recommended. It is recommended that you use dmctl encrypt to encrypt plaintext passwords.
     port: ${port}             # For example: 3307
    ```

2. Create another new data source file `dm-source2.yaml`, and add the following content:

    ```yaml
    # MySQL Configuration.
    source-id: "mysql-replica-02"
    # Specifies whether DM-worker pulls binlogs with GTID (Global Transaction Identifier).
    # The prerequisite is that you have already enabled GTID in the upstream MySQL.
    # If you have configured the upstream database service to switch master between different nodes automatically, you must enable GTID.
    enable-gtid: true
    from:
     host: "192.168.10.102"
     user: "user02"
     password: "${password}"
     port: 3308
    ```

3. Run the following command in a terminal. Use `tiup dmctl` to load the first data source configuration into the DM cluster:

    ```shell
    [root@localhost ~]# tiup dmctl --master-addr ${advertise-addr} operate-source create dm-source1.yaml
    ```

    The parameters used in the command above are described as follows:

    |Parameter              |Description    |
    |-                      |-              |
    |`--master-addr`        |The `{advertise-addr}` of any DM-master node in the cluster where `dmctl` is to be connected. For example: 192.168.11.110:9261|
    |`operate-source create`|Loads the data source to the DM cluster.|

    The following is an example output:

    ```shell
    tiup is checking updates for component dmctl ...

    Starting component `dmctl`: /root/.tiup/components/dmctl/${tidb_version}/dmctl/dmctl /root/.tiup/components/dmctl/${tidb_version}/dmctl/dmctl --master-addr 192.168.11.110:9261 operate-source create dm-source1.yaml

    {
       "result": true,
       "msg": "",
       "sources": [
           {
               "result": true,
               "msg": "",
               "source": "mysql-replica-01",
               "worker": "dm-192.168.11.111-9262"
           }
       ]
    }

    ```

4. Run the following command in a terminal. Use `tiup dmctl` to load the second data source configuration into the DM cluster:

    ```shell
    [root@localhost ~]# tiup dmctl --master-addr 192.168.11.110:9261 operate-source create dm-source2.yaml
    ```

    The following is an example output:

    ```shell
    tiup is checking updates for component dmctl ...

    Starting component `dmctl`: /root/.tiup/components/dmctl/${tidb_version}/dmctl/dmctl /root/.tiup/components/dmctl/${tidb_version}/dmctl/dmctl --master-addr 192.168.11.110:9261 operate-source create dm-source2.yaml

    {
       "result": true,
       "msg": "",
       "sources": [
           {
               "result": true,
               "msg": "",
               "source": "mysql-replica-02",
               "worker": "dm-192.168.11.112-9262"
           }
       ]
    }
    ```

### Step 2. Create a replication task

1. Create a `test-task1.yaml` file for the replication task.

2. Find the starting point in the metadata file of MySQL instance1 exported by Dumpling. For example:

    ```toml
    Started dump at: 2022-05-25 10:16:26
    SHOW MASTER STATUS:
           Log: mysql-bin.000002
           Pos: 246546174
           GTID:b631bcad-bb10-11ec-9eee-fec83cf2b903:1-194801
    Finished dump at: 2022-05-25 10:16:27
    ```

3. Find the starting point in the metadata file of MySQL instance2 exported by Dumpling. For example:

    ```toml
    Started dump at: 2022-05-25 10:20:32
    SHOW MASTER STATUS:
           Log: mysql-bin.000001
           Pos: 1312659
           GTID:cd21245e-bb10-11ec-ae16-fec83cf2b903:1-4036
    Finished dump at: 2022-05-25 10:20:32
    ```

4. Edit the task configuration file `test-task1`, to configure the incremental replication mode and replication starting point for each data source.

    ```yaml
    ## ********* Task Configuration *********
    name: test-task1
    shard-mode: "pessimistic"
    # Task mode. The "incremental" mode only performs incremental data migration.
    task-mode: incremental
    # timezone: "UTC"

    ## ******** Data Source Configuration **********
    ## (Optional) If you need to incrementally replicate data that has already been migrated in the full data migration, you need to enable the safe mode to avoid the incremental data migration error.
    ##  This scenario is common in the following case: the full migration data does not belong to the data source's consistency snapshot, and after that, DM starts to replicate incremental data from a position earlier than the full migration.
    syncers:           # The running configurations of the sync processing unit.
     global:           # Configuration name.
       safe-mode: false # # If this field is set to true, DM changes INSERT of the data source to REPLACE for the target database,
                        # # and changes UPDATE of the data source to DELETE and REPLACE for the target database.
                        # # This is to ensure that when the table schema contains a primary key or unique index, DML statements can be imported repeatedly.
                        # # In the first minute of starting or resuming an incremental migration task, DM automatically enables the safe mode.
    mysql-instances:
    - source-id: "mysql-replica-01"
       block-allow-list:  "bw-rule-1"
       route-rules: ["store-route-rule", "sale-route-rule"]
       filter-rules: ["store-filter-rule", "sale-filter-rule"]
       syncer-config-name: "global"
       meta:
         binlog-name: "mysql-bin.000002"
         binlog-pos: 246546174
         binlog-gtid: "b631bcad-bb10-11ec-9eee-fec83cf2b903:1-194801"
    - source-id: "mysql-replica-02"
       block-allow-list:  "bw-rule-1"
       route-rules: ["store-route-rule", "sale-route-rule"]
       filter-rules: ["store-filter-rule", "sale-filter-rule"]
       syncer-config-name: "global"
       meta:
         binlog-name: "mysql-bin.000001"
         binlog-pos: 1312659
         binlog-gtid: "cd21245e-bb10-11ec-ae16-fec83cf2b903:1-4036"

    ## ******** Configuration of the target TiDB cluster on TiDB Cloud **********
    target-database:       # The target TiDB cluster on TiDB Cloud
     host: "tidb.xxxxxxx.xxxxxxxxx.ap-northeast-1.prod.aws.tidbcloud.com"
     port: 4000
     user: "root"
     password: "${password}"  # If the password is not empty, it is recommended to use a dmctl-encrypted cipher.

    ## ******** Function Configuration **********
    routes:
     store-route-rule:
       schema-pattern: "store_*"
       target-schema: "store"
     sale-route-rule:
       schema-pattern: "store_*"
       table-pattern: "sale_*"
       target-schema: "store"
       target-table:  "sales"
    filters:
     sale-filter-rule:
       schema-pattern: "store_*"
       table-pattern: "sale_*"
       events: ["truncate table", "drop table", "delete"]
       action: Ignore
     store-filter-rule:
       schema-pattern: "store_*"
       events: ["drop database"]
       action: Ignore
    block-allow-list:
     bw-rule-1:
       do-dbs: ["store_*"]

    ## ******** Ignore check items **********
    ignore-checking-items: ["table_schema","auto_increment_ID"]
    ```

For detailed task configurations, see [DM Task Configurations](https://docs.pingcap.com/tidb/stable/task-configuration-file-full).

To run a data replication task smoothly, DM triggers a precheck automatically at the start of the task and returns the check results. DM starts the replication only after the precheck is passed. To trigger a precheck manually, run the check-task command:

```shell
[root@localhost ~]# tiup dmctl --master-addr 192.168.11.110:9261 check-task dm-task.yaml
```

The following is an example output:

```shell
tiup is checking updates for component dmctl ...

Starting component `dmctl`: /root/.tiup/components/dmctl/${tidb_version}/dmctl/dmctl /root/.tiup/components/dmctl/${tidb_version}/dmctl/dmctl --master-addr 192.168.11.110:9261 check-task dm-task.yaml

{
   "result": true,
   "msg": "check pass!!!"
}
```

### Step 3. Start the replication task

Use `tiup dmctl` to run the following command to start the data replication task:

```shell
[root@localhost ~]# tiup dmctl --master-addr ${advertise-addr}  start-task dm-task.yaml
```

The parameters used in the command above are described as follows:

|Parameter              |Description    |
|-                      |-              |
|`--master-addr`        |The `{advertise-addr}` of any DM-master node in the cluster where `dmctl` is to be connected. For example: 192.168.11.110:9261|
|`start-task`           |Starts the migration task.|

The following is an example output:

```shell
tiup is checking updates for component dmctl ...

Starting component `dmctl`: /root/.tiup/components/dmctl/${tidb_version}/dmctl/dmctl /root/.tiup/components/dmctl/${tidb_version}/dmctl/dmctl --master-addr 192.168.11.110:9261 start-task dm-task.yaml

{
   "result": true,
   "msg": "",
   "sources": [
       {
           "result": true,
           "msg": "",
           "source": "mysql-replica-01",
           "worker": "dm-192.168.11.111-9262"
       },

       {
           "result": true,
           "msg": "",
           "source": "mysql-replica-02",
           "worker": "dm-192.168.11.112-9262"
       }
   ],
   "checkResult": ""
}
```

If the task fails to start, check the prompt message and fix the configuration. After that, you can re-run the command above to start the task.

If you encounter any problem, refer to [DM error handling](https://docs.pingcap.com/tidb/stable/dm-error-handling) and [DM FAQ](https://docs.pingcap.com/tidb/stable/dm-faq).

### Step 4. Check the replication task status

To learn whether the DM cluster has an ongoing replication task and view the task status, run the `query-status` command using `tiup dmctl`:

```shell
[root@localhost ~]# tiup dmctl --master-addr 192.168.11.110:9261 query-status test-task1
```

The following is an example output:

```shell
{
   "result": true,
   "msg": "",
   "sources": [
       {
           "result": true,
           "msg": "",
           "sourceStatus": {
               "source": "mysql-replica-01",
               "worker": "dm-192.168.11.111-9262",
               "result": null,
               "relayStatus": null
           },

           "subTaskStatus": [
               {
                   "name": "test-task1",
                   "stage": "Running",
                   "unit": "Sync",
                   "result": null,
                   "unresolvedDDLLockID": "",
                   "sync": {
                       "totalEvents": "4048",
                       "totalTps": "3",
                       "recentTps": "3",
                       "masterBinlog": "(mysql-bin.000002, 246550002)",
                       "masterBinlogGtid": "b631bcad-bb10-11ec-9eee-fec83cf2b903:1-194813",
                       "syncerBinlog": "(mysql-bin.000002, 246550002)",
                       "syncerBinlogGtid": "b631bcad-bb10-11ec-9eee-fec83cf2b903:1-194813",
                       "blockingDDLs": [
                       ],
                       "unresolvedGroups": [
                       ],
                       "synced": true,
                       "binlogType": "remote",
                       "secondsBehindMaster": "0",
                       "blockDDLOwner": "",
                       "conflictMsg": ""
                   }
               }
           ]
       },
       {
           "result": true,
           "msg": "",
           "sourceStatus": {
               "source": "mysql-replica-02",
               "worker": "dm-192.168.11.112-9262",
               "result": null,
               "relayStatus": null
           },
           "subTaskStatus": [
               {
                   "name": "test-task1",
                   "stage": "Running",
                   "unit": "Sync",
                   "result": null,
                   "unresolvedDDLLockID": "",
                   "sync": {
                       "totalEvents": "33",
                       "totalTps": "0",
                       "recentTps": "0",
                       "masterBinlog": "(mysql-bin.000001, 1316487)",
                       "masterBinlogGtid": "cd21245e-bb10-11ec-ae16-fec83cf2b903:1-4048",
                       "syncerBinlog": "(mysql-bin.000001, 1316487)",
                       "syncerBinlogGtid": "cd21245e-bb10-11ec-ae16-fec83cf2b903:1-4048",
                       "blockingDDLs": [
                       ],
                       "unresolvedGroups": [
                       ],
                       "synced": true,
                       "binlogType": "remote",
                       "secondsBehindMaster": "0",
                       "blockDDLOwner": "",
                       "conflictMsg": ""
                   }
               }
           ]
       }
   ]
}
```

For a detailed interpretation of the results, see [Query Status](https://docs.pingcap.com/tidb/stable/dm-query-status).
