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

1. If a CSV file is larger than 256 MB, consider splitting the file into smaller files, each with a size around 256 MB.

    TiDB Cloud supports importing very large CSV files but performs best with multiple input files around 256 MB in size. This is because TiDB Cloud can process multiple files in parallel which can greatly improve the import speed.

2. According to the naming convention of existing objects in your bucket, identify a text pattern that matches the names of the CSV files to be imported.

    For example, to import all data files in a bucket, you can use the wildcard symbol `*` or `*.csv` as a pattern. Similarly, to import the subset of data files in partition `station=402260`, you can use `*station=402260*` as a pattern. Make a note of this pattern as you will need to provide it to TiDB Cloud in [Step 4](#step-4-import-csv-files-to-tidb-cloud).

## Step 2. Create the target table schema

Before importing CSV files into TiDB Cloud, you need to create the target database and table. Alternatively, TiDB Cloud can create these objects for you as part of the import process if you provide the target database and table schema as follows:

1. In the Amazon S3 or GCS directory where the CSV files are located, create a `${db_name}-schema-create.sql` file that contains the `CREATE DATABASE` DDL statement.

    For example, you can create a `mydb-scehma-create.sql` file that contains the following statement:

    {{< copyable "sql" >}}

    ```sql
    CREATE DATABASE mydb;
    ```

2. In the Amazon S3 or GCS directory where the CSV files are located, create a `${db_name}.${table_name}-schema.sql` file that contains the `CREATE TABLE` DDL statement.

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

To allow TiDB Cloud to access the CSV files in the Amazon S3 or GCS bucket, do one of the following:

- If your CSV files are located in Amazon S3, [configure cross-account access to Amazon S3](/tidb-cloud/migrate-from-amazon-s3-or-gcs.md#step-2-configure-amazon-s3-access).

    Once finished, make a note of the Role ARN value as you will need it in [Step 4](#step-4-import-csv-files-to-tidb-cloud).

- If your CSV files are located in GCS, [configure cross-account access to GCS](/tidb-cloud/migrate-from-amazon-s3-or-gcs.md#step-2-configure-gcs-access).

## Step 4. Import CSV files to TiDB Cloud

To import the CSV files to TiDB Cloud, take the following steps:

1. Navigate to the TiDB Clusters page and click the name of your target cluster. The overview page of your target cluster is displayed.
2. In the cluster information pane on the left, click **Import**. The **Data Import Task** page is displayed.
3. On the **Data Import Task** page, provide the following information.

    - **Data Source Type**: select the type of the data source.
    - **Bucket URL**: select the bucket URL where your CSV files are located.
    - **Data Format**: select **CSV**.
    - **Setup Credentials** (This field is visible only for AWS S3): enter the Role ARN value for **Role-ARN**.
    - **CSV Configuration**: check and update the CSV specific configurations, including separator, delimiter, header, not-null, null, backslash-escape, and trim-last-separator. You can find the explanation of each CSV configuration right beside these fields.

        > **Note:**
        >
        > For the configurations of separator, delimiter, and null, you can use both alphanumeric characters and certain special characters. The supported special characters include `\t`, `\b`, `\n`, `\r`, `\f`, and `\u0001`.

    - **Target Database**: fill in the **Username** and **Password** fields.
    - **DB/Tables Filter**: if necessary, you can specify a [table filter](/table-filter.md#syntax). If you want to configure multiple filter rules, use `,` to separate the rules.
    - **Object Name Pattern**: enter a pattern that matches the names of the CSV files to be imported. For example,`my-data.csv`.
    - **Target Table Name**: enter the name of the target table. For example, `mydb.mytable`.

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