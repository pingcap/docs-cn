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
    > If you cannot update the CSV filenames according to the preceding rules in some cases (for example, the CSV file links are also used by your other programs), you can keep the filenames unchanged and use the **File Pattern** in [Step 4](#step-4-import-csv-files-to-tidb-cloud) to import your source data to a single target table.

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

- If your CSV files are located in Amazon S3, [configure Amazon S3 access](/tidb-cloud/config-s3-and-gcs-access.md#configure-amazon-s3-access).

    Once finished, make a note of the Role ARN value as you will need it in [Step 4](#step-4-import-csv-files-to-tidb-cloud).

- If your CSV files are located in GCS, [configure GCS access](/tidb-cloud/config-s3-and-gcs-access.md#configure-gcs-access).

## Step 4. Import CSV files to TiDB Cloud

To import the CSV files to TiDB Cloud, take the following steps:

1. Log in to the [TiDB Cloud console](https://tidbcloud.com/), and navigate to the **Clusters** page.

2. Locate your target cluster, click **...** in the upper-right corner of the cluster area, and select **Import Data**. The **Data Import** page is displayed.

    > **Tip:**
    >
    > Alternatively, you can also click the name of your target cluster on the **Clusters** page and click **Import Data** in the **Import** area.

3. On the **Data Import** page, provide the following information.

    - **Data Format**: select **CSV**.
    - **Location**: select the location where your CSV files are located.
    - **Bucket URI**: select the bucket URI where your CSV files are located.
    - **Role ARN**: (This field is visible only for AWS S3): enter the Role ARN value for **Role ARN**.
    - **Target Cluster**: shows the cluster name and the region name.

    If the region of the bucket is different from your cluster, confirm the compliance of cross region. Click **Next**.

    TiDB Cloud starts validating whether it can access your data in the specified bucket URI. After validation, TiDB Cloud tries to scan all the files in the data source using the default file naming pattern, and returns a scan summary result on the left side of the next page. If you get the `AccessDenied` error, see [Troubleshoot Access Denied Errors during Data Import from S3](/tidb-cloud/troubleshoot-import-access-denied-error.md).

4. Modify the file patterns and add the table filter rules if needed.

    - **File Pattern**: modify the file pattern if you want to import CSV files whose filenames match a certain pattern to a single target table.

        > **Note:**
        >
        > When you use this feature, one import task can only import data to a single table at a time. If you want to use this feature to import data into different tables, you need to import several times, each time specifying a different target table.

        To modify the file pattern, click **Modify**, specify a custom mapping rule between CSV files and a single target table in the following fields, and then click **Scan**. After that, the data source files will be re-scanned using the provided custom mapping rule.

        - **Source file name**: enter a pattern that matches the names of the CSV files to be imported. If you have one CSV file only, enter the file name here directly. Note that the names of the CSV files must include the suffix `.csv`.

            For example:

            - `my-data?.csv`: all CSV files starting with `my-data` and one character (such as `my-data1.csv` and `my-data2.csv`) will be imported into the same target table.
            - `my-data*.csv`: all CSV files starting with `my-data` will be imported into the same target table.

        - **Target table name**: enter the name of the target table in TiDB Cloud, which must be in the `${db_name}.${table_name}` format. For example, `mydb.mytable`. Note that this field only accepts one specific table name, so wildcards are not supported.

    - **Table Filter**: If you want to filter which tables to be imported, you can specify table filter rules in this area.

        For example:

        - `db01.*`: all tables in the `db01` database will be imported.
        - `!db02.*`: except the tables in the `db02` database, all other tables will be imported. `!` is used to exclude tables that do not need to be imported.
        - `*.*` : all tables will be imported.

        For more information, see [table filter syntax](/table-filter.md#syntax).

5. Click **Next**.

6. On the **Preview** page, you can have a preview of the data. If the previewed data is not what you expect, click the **Click here to edit csv configuration** link to update the CSV-specific configurations, including separator, delimiter, header, not-null, null, backslash-escape, and trim-last-separator.

    > **Note:**
    >
    > For the configurations of separator, delimiter, and null, you can use both alphanumeric characters and certain special characters. The supported special characters include `\t`, `\b`, `\n`, `\r`, `\f`, and `\u0001`.

7. Click **Start Import**.

8. When the import progress shows **Finished**, check the imported tables.

    If the number is zero, it means no data files matched the value you entered in the **Source file name** field. In this case, ensure that there are no typos in the **Source file name** field and try again.

When you run an import task, if any unsupported or invalid conversions are detected, TiDB Cloud terminates the import job automatically and reports an importing error.

If you get an importing error, do the following:

1. Drop the partially imported table.
2. Check the table schema file. If there are any errors, correct the table schema file.
3. Check the data types in the CSV files.
4. Try the import task again.