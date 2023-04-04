---
title: Import Local Files to TiDB Cloud
summary: Learn how to import local files to TiDB Cloud.
---

# Import Local Files to TiDB Cloud

You can import local files to TiDB Cloud directly. It only takes a few clicks to complete the task configuration, and then your local CSV data will be quickly imported to your TiDB cluster. Using this method, you do not need to provide the cloud storage bucket path and Role ARN. The whole importing process is quick and smooth.

Currently, this method supports importing one CSV file for one task into either an existing table or a new table.

## Limitations

- Currently, TiDB Cloud only supports importing a local file in CSV format within 50 MiB for one task.
- Importing local files is supported only for Serverless Tier clusters, not for Dedicated Tier clusters.
- You cannot run more than one import task at the same time.
- If you import a CSV file into an existing table in TiDB Cloud, make sure that the first line of the CSV file contains the column names, and the order of the columns in the CSV file must be the same as that in the target table.

## Import local files

1. Open the **Import** page for your target cluster.

    1. Log in to the [TiDB Cloud console](https://tidbcloud.com/) and navigate to the [**Clusters**](https://tidbcloud.com/console/clusters) page of your project.

        > **Tip:**
        >
        > If you have multiple projects, you can switch to the target project in the left navigation pane of the **Clusters** page.

    2. Click the name of your target cluster to go to its overview page, and then click **Import** in the left navigation pane.

2. On the **Import** page, you can directly drag and drop your local file to the upload area, or click the upload area to select and upload the target local file. Note that you can upload only one CSV file of less than 50 MiB for one task.

3. In the **Target** area, select the target database and the target table, or enter a name directly to create a new database or a new table. The name must start with letters (a-z and A-Z) or numbers (0-9), and can contain letters (a-z and A-Z), numbers (0-9), and the underscore (_) character. Click **Next**.

4. Check the table.

    You can see a list of configurable table columns. Each line shows the table column name inferred by TiDB Cloud, the table column type inferred, and the previewed data from the CSV file.

    - If you import data into an existing table in TiDB Cloud, the column list is extracted from the table definition, and the previewed data is mapped to the corresponding columns by column names.

    - If you want to create a new table, the column list is extracted from the CSV file, and the column type is inferred by TiDB Cloud. For example, if the previewed data is all integers, the inferred column type will be **int** (integer).

5. Configure the column names and data types.

    If the first row in the CSV file records the column names, make sure that **Use the first row as column name** is selected, which is selected by default.

    If the CSV file does not have a row for the column names, do not select **Use the first row as column name**. In this case:

    - If the target table already exists, the columns in the CSV file will be imported into the target table in order. Extra columns will be truncated and missing columns will be filled with default values. You can also select the **Ignore the first row** option to ignore the first row and start importing from the second row.

    - If you need TiDB Cloud to create the target table, input the name for each column. The column name must start with letters (a-z and A-Z) or numbers (0-9), and can contain letters (a-z and A-Z), numbers (0-9), and the underscore (_) character. You can also change the data type if needed.

6. For a new target table, you can set the primary key. You can select a column as the primary key, or select multiple columns to create a composite primary key. The composite primary key will be formed in the order in which you select the column names.

    > **Note:**
    >
    > - The primary key of the table is a clustered index and cannot be deleted after creation.
    > - Ensure that the data corresponding to the primary key field is unique and not empty. Otherwise, the import task will result in data inconsistency.

7. Edit the CSV configuration if needed.

   You can also click **Edit CSV configuration** to configure Backslash Escape, Separator, and Delimiter for more fine-grained control. For more information about the CSV configuration, see [CSV Configurations for Importing Data](/tidb-cloud/csv-config-for-import-data.md).

8. Click **Start Import**.

    You can view the import progress on the **Import Task Detail** page. If there are warnings or failed tasks, you can check to view the details and solve them.

9. After the import task is completed, you can click **Explore your data by Chat2Query** to query your imported data. For more information about how to use Chat2Qury, see [Explore Your Data with AI-Powered Chat2Query](/tidb-cloud/explore-data-with-chat2query.md).

10. On the **Import** page, you can click **View** in the **Action** column to check the import task detail.
