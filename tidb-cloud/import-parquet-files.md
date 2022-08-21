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

1. If a Parquet file is larger than 256 MB, consider splitting it into smaller files, each with a size around 256 MB.

    TiDB Cloud supports importing very large Parquet files but performs best with multiple input files around 256 MB in size. This is because TiDB Cloud can process multiple files in parallel, which can greatly improve the import speed.

2. Name the Parquet files as follows:

    - If a Parquet file contains all data of an entire table, name the file in the `${db_name}.${table_name}.parquet` format, which maps to the `${db_name}.${table_name}` table when you import the data.
    - If the data of one table is separated into multiple Parquet files, append a numeric suffix to these Parquet files. For example, `${db_name}.${table_name}.000001.parquet` and `${db_name}.${table_name}.000002.parquet`. The numeric suffixes can be inconsecutive but must be in ascending order. You also need to add extra zeros before the number to ensure all the suffixes are in the same length.

    > **Note:**
    >
    > If you cannot update the Parquet filenames according to the preceding rules in some cases (for example, the Parquet file links are also used by your other programs), you can keep the filenames unchanged and use the **Custom Pattern** in [Step 4](#step-4-import-parquet-files-to-tidb-cloud) to import your source data to a single target table.

## Step 2. Create the target table schemas

Because Parquet files do not contain schema information, before importing data from Parquet files into TiDB Cloud, you need to create the table schemas using either of the following methods:

- Method 1: In TiDB Cloud, create the target databases and tables for your source data.

- Method 2: In the Amazon S3 or GCS directory where the Parquet files are located, create the target table schema files for your source data as follows:

    1. Create database schema files for your source data.

        If your Parquet files follow the naming rules in [Step 1](#step-1-prepare-the-parquet-files), the database schema files are optional for the data import. Otherwise, the database schema files are mandatory.

        Each database schema file must be in the `${db_name}-schema-create.sql` format and contain a `CREATE DATABASE` DDL statement. With this file, TiDB Cloud will create the `${db_name}` database to store your data when you import the data.

        For example, if you create a `mydb-scehma-create.sql` file that contains the following statement, TiDB Cloud will create the `mydb` database when you import the data.

        {{< copyable "sql" >}}

        ```sql
        CREATE DATABASE mydb;
        ```

    2. Create table schema files for your source data.

        If you do not include the table schema files in the Amazon S3 or GCS directory where the Parquet files are located, TiDB Cloud will not create the corresponding tables for you when you import the data.

        Each table schema file must be in the `${db_name}.${table_name}-schema.sql` format and contain a `CREATE TABLE` DDL statement. With this file, TiDB Cloud will create the `${db_table}` table in the `${db_name}` database when you import the data.

        For example, if you create a `mydb.mytable-schema.sql` file that contains the following statement, TiDB Cloud will create the `mytable` table in the `mydb` database when you import the data.

        {{< copyable "sql" >}}

        ```sql
        CREATE TABLE mytable (
        ID INT,
        REGION VARCHAR(20),
        COUNT INT );
        ```

        > **Note:**
        >
        > Each `${db_name}.${table_name}-schema.sql` file should only contain a single DDL statement. If the file contains multiple DDL statements, only the first one takes effect.

## Step 3. Configure cross-account access

To allow TiDB Cloud to access the Parquet files in the Amazon S3 or GCS bucket, do one of the following:

- If your Parquet files are located in Amazon S3, [configure cross-account access to Amazon S3](/tidb-cloud/config-s3-and-gcs-access.md#configure-amazon-s3-access).

    Once finished, make a note of the Role ARN value as you will need it in [Step 4](#step-4-import-parquet-files-to-tidb-cloud).

- If your Parquet files are located in GCS, [configure cross-account access to GCS](/tidb-cloud/config-s3-and-gcs-access.md#configure-gcs-access).

## Step 4. Import Parquet files to TiDB Cloud

To import the Parquet files to TiDB Cloud, take the following steps:

1. Navigate to the **Active Clusters** page.
2. Find the area of your target cluster and click **Import Data** in the upper-right corner of the area. The **Data Import Task** page is displayed.

    > **Tip:**
    >
    > Alternatively, you can also click the name of your target cluster on the **Active Clusters** page and click **Import Data** in the upper-right corner.

3. On the **Data Import Task** page, provide the following information.

    - **Data Source Type**: select the type of the data source.
    - **Bucket URL**: select the bucket URL where your Parquet files are located.
    - **Data Format**: select **Parquet**.
    - **Setup Credentials** (This field is visible only for AWS S3): enter the Role ARN value for **Role-ARN**.
    - **Target Cluster**: fill in the **Username** and **Password** fields.
    - **DB/Tables Filter**: if you want to filter which tables to be imported, you can specify one or more table filters in this field, separated by `,`.

        For example:

        - `db01.*`: all tables in the `db01` database will be imported.
        - `db01.table01*,db01.table02*`: all tables starting with `table01` and `table02` in the `db01` database will be imported.
        - `!db02.*`: except the tables in the `db02` database, all other tables will be imported. `!` is used to exclude tables that do not need to be imported.
        - `*.*` : all tables will be imported.

        For more information, see [table filter snytax](/table-filter.md#syntax).

    - **Custom Pattern**: enable the **Custom Pattern** feature if you want to import Parquet files whose filenames match a certain pattern to a single target table.

        > **Note:**
        >
        > After enabling this feature, one import task can only import data to a single table at a time. If you want to use this feature to import data into different tables, you need to import several times, each time specifying a different target table.

        When **Custom Pattern** is enabled, you are required to specify a custom mapping rule between Parquet files and a single target table in the following fields:

        - **Object Name Pattern**: enter a pattern that matches the names of the Parquet files to be imported. If you have one Parquet file only, you can enter the filename here directly.

            For example:

            - `my-data?.parquet`: all Parquet files starting with `my-data` and one character (such as `my-data1.parquet` and `my-data2.parquet`) will be imported into the same target table.
            - `my-data*.parquet`: all Parquet files starting with `my-data` will be imported into the same target table.

        - **Target Table Name**: enter the name of the target table in TiDB Cloud, which must be in the `${db_name}.${table_name}` format. For example, `mydb.mytable`. Note that this field only accepts one specific table name, so wildcards are not supported.

4. Click **Import**.

    A warning message about the database resource consumption is displayed.

5. Click **Confirm**.

    TiDB Cloud starts validating whether it can access your data in the specified bucket URL. After the validation is completed and successful, the import task starts automatically. If you get the `AccessDenied` error, see [Troubleshoot Access Denied Errors during Data Import from S3](/tidb-cloud/troubleshoot-import-access-denied-error.md).

6. When the import progress shows success, check the number after **Total Files:**.

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