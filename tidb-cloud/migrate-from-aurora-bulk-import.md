---
title: Migrate from Amazon Aurora MySQL to TiDB Cloud in Bulk
summary: Learn how to migrate data from Amazon Aurora MySQL to TiDB Cloud in bulk.
---

# Migrate from Amazon Aurora MySQL to TiDB Cloud in Bulk

This document describes how to migrate data from Amazon Aurora MySQL to TiDB Cloud in bulk using the import tools on TiDB Cloud console. 

## Learn how to create an import task on the TiDB Cloud console

To import data, perform the following steps:

1. Navigate to the TiDB Clusters page and click the name of your target cluster. The overview page of your target cluster is displayed.
2. In the cluster information pane on the left, click **Import**. The **Data Import Task** page is displayed.
3. Prepare source data according to [Learn how to create an Amazon S3 Bucket and prepare source data files](#learn-how-to-create-an-amazon-s3-bucket-and-prepare-source-data-files). You can see the advantages and disadvantages of different **Data Format** in the preparing data part.
4. Fill in the **Data Source Type**, **Bucket URL**, and **Data Format** fields according to the specification of your source data.
5. Fill in the **Username** and **Password** fields of the **Target Database** according to the connection settings of your cluster.
6. Create the bucket policy and role for cross-account access according to [Learn how to configure cross-account access](#learn-how-to-configure-cross-account-access).
7. Click **Import** to create the task.

> **Note:**
>
> If your task fails, refer to [Learn how to clean up incomplete data](#learn-how-to-clean-up-incomplete-data).

## Learn how to create an Amazon S3 Bucket and prepare source data files

To prepare data, you can select one from the following two options:

- [Option 1: Prepare source data files using Dumpling](#option-1-prepare-source-data-files-using-dumpling)

    You need to launch [Dumpling](https://docs.pingcap.com/tidb/stable/dumpling-overview) on your EC2, and export the data to Amazon S3. The data you export is the current latest data of your source database. This might affect the online service. Dumpling will lock the table when you export data.

- [Option 2: Prepare source data files using Amazon Aurora snapshots](#option-2-prepare-source-data-files-using-amazon-aurora-snapshots)

    This affects your online service. It might take a while when you export data, because the export task on Amazon Aurora first restores and scales the database before exporting data to Amazon S3. For more details, see [Exporting DB snapshot data to Amazon S3](https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/USER_ExportSnapshot.html).

### Prechecks and preparations

> **Note:**
>
> Currently, it is not recommended to import more than 2 TB of data.
>
> Before starting the migration, you need to do the following prechecks and preparations.

#### Ensure enough free space

Ensure that the free space of your TiDB cluster is larger than the size of your data. It is recommended that you should reserve 600 GB free space on each TiKV node. You can add more TiKV nodes to fulfill your demand.

#### Check the database’s collation set settings

Currently, TiDB only supports the `utf8_general_ci` and `utf8mb4_general_ci` collation. To verify the collation settings of your database, execute the following command in the MySQL terminal connected to Aurora:

{{< copyable "sql" >}}

```sql
select * from ((select table_schema, table_name, column_name, collation_name from information_schema.columns where character_set_name is not null) union all (select table_schema, table_name, null, table_collation from information_schema.tables)) x where table_schema not in ('performance_schema', 'mysql', 'information_schema') and collation_name not in ('utf8_bin', 'utf8mb4_bin', 'ascii_bin', 'latin1_bin', 'binary', 'utf8_general_ci', 'utf8mb4_general_ci');
```

The result is as follows:

```output
Empty set (0.04 sec)
```

If TiDB does not support your character set or collation, consider converting them to supported types. For more details, see [Character Set and Collation](https://docs.pingcap.com/tidb/stable/character-set-and-collation).

### Option 1: Prepare source data files using Dumpling

You need to prepare an EC2 to run the following data export task. It's better to run on the same network with Aurora and S3 to avoid extra fees.

1. Install Dumpling on EC2.

    {{< copyable "shell-regular" >}}

    ```bash
    curl --proto '=https' --tlsv1.2 -sSf https://tiup-mirrors.pingcap.com/install.sh | sh
    source ~/.bash_profile
    tiup install dumpling 
    ```

    In the above commands, you need to modify `~/.bash_profile` to the path of your profile file.

2. Grant the write privilege to Dumpling for writing S3.

    > **Note:**
    >
    > If you have assigned the IAM role to the EC2, you can skip configuring the access key and security key, and directly run Dumpling on this EC2.
    
    You can grant the write privilege using the access key and security key of your AWS account in the environment. Create a specific key pair for preparing data, and revoke the access key immediately after you finish the preparation.

    {{< copyable "shell-regular" >}}

    ```bash
    export AWS_ACCESS_KEY_ID=AccessKeyID
    export AWS_SECRET_ACCESS_KEY=SecretKey
    ```

3. Back up the source database to S3.

    Use Dumpling to export the data from Amazon Aurora. Based on your environment, replace the content in angle brackets (>), and then execute the following commands. If you want to use filter rules when exporting the data, refer to [Table Filter](https://docs.pingcap.com/tidb/stable/table-filter#cli).

    {{< copyable "shell-regular" >}}

    ```bash
    export_username="<Aurora username>"
    export_password="<Aurora password>"
    export_endpoint="<the endpoint for Amazon Aurora MySQL>"
    # You will use the s3 url when you create importing task
    backup_dir="s3://<bucket name>/<backup dir>"
    s3_bucket_region="<bueckt_region>"

    # Use `tiup -- dumpling` instead if "flag needs an argument: 'h' in -h" is prompted for TiUP versions earlier than v1.8
    tiup dumpling \
    -u "$export_username" \
    -p "$export_password" \
    -P 3306 \
    -h "$export_endpoint" \
    --filetype sql \
    --threads 8 \
    -o "$backup_dir" \
    --consistency="none" \
    --s3.region="$s3_bucket_region" \
    -r 200000 \
    -F 256MiB
    ```

4. On the data import task panel of TiDB Cloud, choose **TiDB Dumpling** as the **Data Format**.

### Option 2: Prepare source data files using Amazon Aurora snapshots

#### Back up the schema of the database and restore on TiDB Cloud

To migrate data from Aurora, you need to back up the schema of the database.

1. Install the MySQL client.

    {{< copyable "sql" >}}

    ```bash
    yum install mysql -y
    ```

2. Back up the schema of the database.

    {{< copyable "sql" >}}

    ```bash
    export_username="<Aurora username>"
    export_endpoint="<Aurora endpoint>"
    export_database="<Database to export>"

    mysqldump -h ${export_endpoint} -u ${export_username} -p --ssl-mode=DISABLED -d${export_database} >db.sql
    ```

3. Import the schema of the database into TiDB Cloud. 

    {{< copyable "sql" >}}

    ```bash
    dest_endpoint="<TiDB Cloud connect endpoint>"
    dest_username="<TiDB Cloud username>"
    dest_database="<Database to restore>"

    mysql -u ${dest_username} -h ${dest_endpoint} -P ${dest_port_number} -p -D${dest_database}<db.sql
    ```

4. On the data import task panel of TiDB Cloud, choose **Aurora Backup Snapshot** as the **Data Format**.

#### Take a snapshot and export it to S3

 1. From the Amazon RDS console, choose **Snapshots**, and click **Take snapshots** to create a manual snapshot.

 2. Fill in the blank under **Snapshot Name**. Click **Take snapshot**. When you finish creating the snapshot, the snapshot shows under the snapshot table.

 3. Choose the snapshot you have taken, click **Actions**. In the drop-down box, click **Export to Amazon S3**.

 4. Fill the blank under **Export identifier**.

 5. Choose the amount of data to be exported. In this guide, **All** is selected. You can also choose partial to use identifiers to decide which part of the database needs to be exported.

 6. Choose the S3 bucket to store the snapshot. You can create a new bucket to store the data for security concerns. It is recommended to use the bucket in the same region as your TiDB cluster. Downloading data across regions can cause additional network costs.

 7. Choose the proper IAM role to grant write access to the S3 bucket. Make a note of this role as it will be used later when you import the snapshot to TiDB Cloud.

 8. Choose a proper AWS KMS Key and make sure the IAM role has already been added to the KMS Key Users. To add a role, you can select a KSM service, select the key, and then click **Add**. 

 9. Click **Export Amazon S3**. You can see the progress in the task table.

 10. From the task table, record the destination bucket (for example, `s3://snapshot-bucket/snapshot-samples-1`).

## Learn how to configure cross-account access

The TiDB Cloud cluster and the S3 bucket are in different AWS accounts. To allow the TiDB Cloud cluster to access the source data files in the S3 bucket, you need to configure the cross-account access to Amazon S3. For more information, see [Configure the Amazon S3 access](/tidb-cloud/migrate-from-amazon-s3-or-gcs.md#step-2-configure-amazon-s3-access).

Once finished, you will have created a policy and role for cross-account. You can then continue with the configuration on the data import task panel of TiDB Cloud.

## Learn how to set up filter rules

Refer to the [Table Filter](https://docs.pingcap.com/tidb/stable/table-filter#cli) document. Currently, TiDB Cloud only supports one table filter rule.

## Learn how to clean up incomplete data

You can check the requirements again. When all the problems are solved, you can drop the incomplete database and restart the importing process.
