---
title:  Import Apache Parquet Files from Amazon S3 or GCS into TiDB Cloud
summary: Learn how to import Apache Parquet files from Amazon S3 or GCS into TiDB Cloud.
---

# Import Apache Parquet Files from Amazon S3 or GCS into TiDB Cloud

You can import both uncompressed and Snappy compressed [Apache Parquet](https://parquet.apache.org/) format data files to TiDB Cloud. This document describes how to import Parquet files from Amazon Simple Storage Service (Amazon S3) or Google Cloud Storage (GCS) into TiDB Cloud.

> **Note:**
>
> TiDB Cloud only supports importing Parquet files into empty tables. To import data into an existing table that already contains data, you can use TiDB Cloud to import the data into a temporary empty table by following this document, and then use the `INSERT SELECT` statement to copy the data to the target existing table.

## Step 1. Prepare the Parquet files

> **Note:**
>
> Currently, TiDB Cloud does not support importing Parquet files that contain any of the following data types. If Parquet files to be imported contain such data types, you need to first regenerate the Parquet files using the [supported data types](#supported-data-types) (for example, `STRING`). Alternatively, you could use a service such as AWS Glue to transform data types easily.
>
> - `LIST`
> - `NEST STRUCT`
> - `BOOL`
> - `ARRAY`
> - `MAP`

1. If a Parquet file is larger than 256 MB, consider splitting the file into smaller files, each with a size around 256 MB.

    TiDB Cloud supports importing very large Parquet files but performs best with multiple input files around 256 MB in size. This is because TiDB Cloud can process multiple files in parallel which can greatly improve the import speed.

2. According to the naming convention of existing objects in your bucket, identify a text pattern that matches the names of the parquet files to be imported.

    For example, to import all data files in a bucket, you can use the wildcard symbol `*` or `*.parquet` as a pattern. Similarly, to import the subset of data files in partition `station=402260`, you can use `*station=402260*` as a pattern. Make a note of this pattern as you will need to provide it to TiDB Cloud in [Step 4](#step-4-import-parquet-files-to-tidb-cloud).

## Step 2. Create the target database and table schema

Before importing Parquet files into TiDB Cloud, you need to create the target database and table. Alternatively, TiDB Cloud can create these objects for you as part of the import process if you provide the target database and table schema as follows:

1. In the Amazon S3 or GCS directory where the parquet files are located, create a `${db_name}-schema-create.sql` file that contains the `CREATE DATABASE` DDL statement.

    For example, you can create a `mydb-scehma-create.sql` file that contains the following statement:

    {{< copyable "sql" >}}

    ```sql
    CREATE DATABASE mydb;
    ```

2. In the Amazon S3 or GCS directory where the parquet files are located, create a `${db_name}.${table_name}-schema.sql` file that contains the `CREATE TABLE` DDL statement.

    For example, you can create a `mydb.mytable-schema.sql` file that contains the following statement:

    {{< copyable "sql" >}}

    ```sql
    CREATE TABLE mytable (
    ID INT,
    REGION VARCHAR(20),
    COUNT INT );
    ```

    > **Note:**
    >
    > The `${db_name}.${table_name}-schema.sql` file should only contain a single DDL statement. If the file contains multiple DDL statements, only the first statement takes effect.

## Step 3. Configure cross-account access

To allow TiDB Cloud to access the Parquet files in the Amazon S3 or GCS bucket, do one of the following:

- If your organization is using TiDB Cloud as a service on AWS, [configure cross-account access to Amazon S3](/tidb-cloud/migrate-from-amazon-s3-or-gcs.md#step-2-configure-amazon-s3-access).

    Once finished, make a note of the Role ARN value as you will need it in [Step 4](#step-4-import-parquet-files-to-tidb-cloud).

- If your organization is using TiDB Cloud as a service on Google Cloud Platform (GCP), [configure cross-account access to GCS](/tidb-cloud/migrate-from-amazon-s3-or-gcs.md#step-2-configure-gcs-access).

## Step 4. Import Parquet files to TiDB Cloud

To import the Parquet files to TiDB Cloud, take the following steps:

1. Navigate to the TiDB Clusters page and click the name of your target cluster. The overview page of your target cluster is displayed.
2. In the cluster information pane on the left, click **Import**. The **Data Import Task** page is displayed.
3. On the **Data Import Task** page, provide the following information.

    - **Data Source Type**: select the type of the data source.
    - **Bucket URL**: select the bucket URL where your Parquet files are located.
    - **Data Format**: select **Parquet**.
    - **Setup Credentials** (This field is visible only for AWS S3): enter the Role ARN value for **Role-ARN**.
    - **Target Database**: fill in the **Username** and **Password** fields.
    - **DB/Tables Filter**: if necessary, you can specify a [table filter](https://docs.pingcap.com/tidb/stable/table-filter#cli). Currently, TiDB Cloud only supports one table filter rule.
    - **Object Name Pattern**: enter a pattern that matches the names of the Parquet files to be imported. For example,`my-data.parquet`.
    - **Target Table Name**: enter the name of the target table. For example, `mydb.mytable`.

4. Click **Import** to start the import task.

5. When the import progress shows success, check the number after **Total Files:**.

    If the number is zero, it means no data files matched the value you entered in the **Object Name Pattern** field. In this case, check whether there are any typos in the **Object Name Pattern** field and try again.

When running an import task, if any unsupported or invalid conversions are detected, TiDB Cloud terminates the import job automatically and reports an importing error.

If you get an importing error, do the following:

1. Drop the partially imported table.
2. Check the table schema file. If there are any errors, correct the table schema file.
3. Check the data types in the Parquet files.

    If the Parquet files contain any unsupported data types (for example, `NEST STRUCT`, `ARRAY`, or `MAP`), you need to regenerate the Parquet files using [supported data types](#supported-data-types) (for example, `STRING`).

4. Try the import task again.

## Supported data types

The following table lists the supported Parquet data types that can be imported to TiDB Cloud.

| Parquet Primitive Type | Parquet Logical Type | Types in TiDB or MySQL |
|---|---|---|
| DOUBLE | DOUBLE | DOUBLE<br />FLOAT |
| FIXED_LEN_BYTE_ARRAY(9) | DECIMAL(20,0) | BIGINT UNSIGNED |
| FIXED_LEN_BYTE_ARRAY(N) | DECIMAL(p,s) | DECIMAL<br />NUMERIC |
| INT32 | DECIMAL(p,s) | DECIMAL<br />NUMERIC |
| INT32 | N/A | INT<br />MEDIUMINT<br />YEAR |
| INT64 | DECIMAL(p,s) | DECIMAL<br />NUMERIC |
| INT64 | N/A | BIGINT<br />INT UNSIGNED<br />MEDIUMINT UNSIGNED |
| INT64 | TIMESTAMP_MICROS | DATETIME<br />TIMESTAMP |
| BYTE_ARRAY | N/A | BINARY<br />BIT<br />BLOB<br />CHAR<br />LINESTRING<br />LONGBLOB<br />MEDIUMBLOB<br />MULTILINESTRING<br />TINYBLOB<br />VARBINARY |
| BYTE_ARRAY | STRING | ENUM<br />DATE<br />DECIMAL<br />GEOMETRY<br />GEOMETRYCOLLECTION<br />JSON<br />LONGTEXT<br />MEDIUMTEXT<br />MULTIPOINT<br />MULTIPOLYGON<br />NUMERIC<br />POINT<br />POLYGON<br />SET<br />TEXT<br />TIME<br />TINYTEXT<br />VARCHAR |
| SMALLINT | N/A | INT32 |
| SMALLINT UNSIGNED | N/A | INT32 |
| TINYINT | N/A | INT32 |
| TINYINT UNSIGNED | N/A | INT32 |