---
title:  Import CSV Files from Amazon S3 or GCS into TiDB Cloud
summary: Learn how to import CSV files from Amazon S3 or GCS into TiDB Cloud.
---

# Import CSV Files from Amazon S3 or GCS into TiDB Cloud

This document describes how to import uncompressed CSV files from Amazon Simple Storage Service (Amazon S3) or Google Cloud Storage (GCS) into TiDB Cloud.

> **Note:**
>
> - If your CSV source files are compressed, you must uncompress the files first before the import.
> - To ensure data consistency, TiDB Cloud allows to import CSV files into empty tables only. To import data into an existing table that already contains data, you can use TiDB Cloud to import the data into a temporary empty table by following this document, and then use the `INSERT SELECT` statement to copy the data to the target existing table.

## Step 1. Prepare the CSV files

1. If a CSV file is larger than 256 MB, consider splitting it into smaller files, each with a size around 256 MB.

    TiDB Cloud supports importing very large CSV files but performs best with multiple input files around 256 MB in size. This is because TiDB Cloud can process multiple files in parallel, which can greatly improve the import speed.

2. Name the CSV files as follows:

    - If a CSV file contains all data of an entire table, name the file in the `${db_name}.${table_name}.csv` format, which maps to the `${db_name}.${table_name}` table when you import the data.
    - If the data of one table is separated into multiple CSV files, append a numeric suffix to these CSV files. For example, `${db_name}.${table_name}.000001.csv` and `${db_name}.${table_name}.000002.csv`. The numeric suffixes can be inconsecutive but must be in ascending order. You also need to add extra zeros before the number to ensure all the suffixes are in the same length.

    > **Note:**
    >
    > If you cannot update the CSV filenames according to the preceding rules in some cases (for example, the CSV file links are also used by your other programs), you can keep the filenames unchanged and use the **Custom Pattern** in [Step 4](#step-4-import-csv-files-to-tidb-cloud) to import your source data to a single target table.

## Step 2. Create the target table schemas

Because CSV files do not contain schema information, before importing data from CSV files into TiDB Cloud, you need to create the table schemas using either of the following methods:

- Method 1: In TiDB Cloud, create the target databases and tables for your source data.

- Method 2: In the Amazon S3 or GCS directory where the CSV files are located, create the target table schema files for your source data as follows:

    1. Create database schema files for your source data.

        If your CSV files follow the naming rules in [Step 1](#step-1-prepare-the-csv-files), the database schema files are optional for the data import. Otherwise, the database schema files are mandatory.

        Each database schema file must be in the `${db_name}-schema-create.sql` format and contain a `CREATE DATABASE` DDL statement. With this file, TiDB Cloud will create the `${db_name}` database to store your data when you import the data.

        For example, if you create a `mydb-scehma-create.sql` file that contains the following statement, TiDB Cloud will create the `mydb` database when you import the data.

        {{< copyable "sql" >}}

        ```sql
        CREATE DATABASE mydb;
        ```

    2. Create table schema files for your source data.

        If you do not include the table schema files in the Amazon S3 or GCS directory where the CSV files are located, TiDB Cloud will not create the corresponding tables for you when you import the data.

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

To allow TiDB Cloud to access the CSV files in the Amazon S3 or GCS bucket, do one of the following:

- If your CSV files are located in Amazon S3, [configure cross-account access to Amazon S3](/tidb-cloud/config-s3-and-gcs-access.md#configure-amazon-s3-access).

    Once finished, make a note of the Role ARN value as you will need it in [Step 4](#step-4-import-csv-files-to-tidb-cloud).

- If your CSV files are located in GCS, [configure cross-account access to GCS](/tidb-cloud/config-s3-and-gcs-access.md#configure-gcs-access).

## Step 4. Import CSV files to TiDB Cloud

To import the CSV files to TiDB Cloud, take the following steps:

1. Navigate to the **Active Clusters** page.
2. Find the area of your target cluster and click **Import Data** in the upper-right corner of the area. The **Data Import Task** page is displayed.

    > **Tip:**
    >
    > Alternatively, you can also click the name of your target cluster on the **Active Clusters** page and click **Import Data** in the upper-right corner.

3. On the **Data Import Task** page, provide the following information.

    - **Data Source Type**: select the type of the data source.
    - **Bucket URL**: select the bucket URL where your CSV files are located.
    - **Data Format**: select **CSV**.
    - **Setup Credentials** (This field is visible only for AWS S3): enter the Role ARN value for **Role-ARN**.
    - **CSV Configuration**: check and update the CSV specific configurations, including separator, delimiter, header, not-null, null, backslash-escape, and trim-last-separator. You can find the explanation of each CSV configuration right beside these fields.

        > **Note:**
        >
        > For the configurations of separator, delimiter, and null, you can use both alphanumeric characters and certain special characters. The supported special characters include `\t`, `\b`, `\n`, `\r`, `\f`, and `\u0001`.

    - **Target Cluster**: fill in the **Username** and **Password** fields.
    - **DB/Tables Filter**: if you want to filter which tables to be imported, you can specify one or more table filters in this field, separated by `,`.

        For example:

        - `db01.*`: all tables in the `db01` database will be imported.
        - `db01.table01*,db01.table02*`: all tables starting with `table01` and `table02` in the `db01` database will be imported.
        - `!db02.*`: except the tables in the `db02` database, all other tables will be imported. `!` is used to exclude tables that do not need to be imported.
        - `*.*` : all tables will be imported.

        For more information, see [table filter snytax](/table-filter.md#syntax).

    - **Custom Pattern**: enable the **Custom Pattern** feature if you want to import CSV files whose filenames match a certain pattern to a single target table.

        > **Note:**
        >
        > After enabling this feature, one import task can only import data to a single table at a time. If you want to use this feature to import data into different tables, you need to import several times, each time specifying a different target table.

        When **Custom Pattern** is enabled, you are required to specify a custom mapping rule between CSV files and a single target table in the following fields:

        - **Object Name Pattern**: enter a pattern that matches the names of the CSV files to be imported. If you have one CSV file only, you can enter the filename here directly.

            For example:

            - `my-data?.csv`: all CSV files starting with `my-data` and one character (such as `my-data1.csv` and `my-data2.csv`) will be imported into the same target table.
            - `my-data*.csv`: all CSV files starting with `my-data` will be imported into the same target table.

        - **Target Table Name**: enter the name of the target table in TiDB Cloud, which must be in the `${db_name}.${table_name}` format. For example, `mydb.mytable`. Note that this field only accepts one specific table name, so wildcards are not supported.

4. Click **Import**.

    A warning message about the database resource consumption is displayed.

5. Click **Confirm**.

    TiDB Cloud starts validating whether it can access your data in the specified bucket URL. After the validation is completed and successful, the import task starts automatically. If you get the `AccessDenied` error, see [Troubleshoot Access Denied Errors during Data Import from S3](/tidb-cloud/troubleshoot-import-access-denied-error.md).

6. When the import progress shows success, check the number after **Total Files:**.

    If the number is zero, it means no data files matched the value you entered in the **Object Name Pattern** field. In this case, ensure that there are no typos in the **Object Name Pattern** field and try again.

When running an import task, if any unsupported or invalid conversions are detected, TiDB Cloud terminates the import job automatically and reports an importing error.

If you get an importing error, do the following:

1. Drop the partially imported table.
2. Check the table schema file. If there are any errors, correct the table schema file.
3. Check the data types in the CSV files.
4. Try the import task again.