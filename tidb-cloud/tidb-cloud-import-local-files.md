---
title: Import Local Files to TiDB Cloud
summary: Learn how to import local files to TiDB Cloud.
---

# Import Local Files to TiDB Cloud

You can import local files to TiDB Cloud directly. It only takes a few clicks to complete the task configuration, and then your local CSV data will be quickly imported to your TiDB cluster. Using this method, you do not need to provide the cloud storage bucket path and Role ARN. The whole importing process is quick and smooth.

Currently, this method supports importing one CSV file for one task into either an existing table or a new table.

## Limitations

- Currently, TiDB Cloud only supports importing a local file in CSV format within 50 MiB for one task.
- Importing local files is supported only for TiDB Serverless clusters, not for TiDB Dedicated clusters.
- You cannot run more than one import task at the same time.
- When you import a CSV file into an existing table in TiDB Cloud and the target table has more columns than the source file, the extra columns are handled differently depending on the situation:
    - If the extra columns are not the primary keys or the unique keys, no error will be reported. Instead, these extra columns will be populated with their [default values](/data-type-default-values.md).
    - If the extra columns are the primary keys or the unique keys and do not have the `auto_increment` or `auto_random` attribute, an error will be reported. In that case, it is recommended that you choose one of the following strategies:
        - Provide a source file that includes these the primary keys or the unique keys columns.
        - Set the attributes of the the primary key or the unique key columns to `auto_increment` or `auto_random`.
- If a column name is a reserved [keyword](/keywords.md) in TiDB, TiDB Cloud automatically adds backticks `` ` `` to enclose the column name. For example, if the column name is `order`, TiDB Cloud automatically adds backticks `` ` `` to change it to `` `order` `` and imports the data into the target table.

## Import local files

1. Open the **Import** page for your target cluster.

    1. Log in to the [TiDB Cloud console](https://tidbcloud.com/) and navigate to the [**Clusters**](https://tidbcloud.com/console/clusters) page of your project.

        > **Tip:**
        >
        > If you have multiple projects, you can click <MDSvgIcon name="icon-left-projects" /> in the lower-left corner and switch to another project.

    2. Click the name of your target cluster to go to its overview page, and then click **Import** in the left navigation pane.

2. On the **Import** page, you can directly drag and drop your local file to the upload area, or click the upload area to select and upload the target local file. Note that you can upload only one CSV file of less than 50 MiB for one task. If your local file is larger than 50 MiB, see [How to import a local file larger than 50 MiB?](#how-to-import-a-local-file-larger-than-50-mib).

3. In the **Target** area, select the target database and the target table, or enter a name directly to create a new database or a new table. The name must start with letters (a-z and A-Z) or numbers (0-9), and can contain letters (a-z and A-Z), numbers (0-9), and the underscore (_) character. Click **Preview**.

4. Check the table.

    You can see a list of configurable table columns. Each line shows the table column name inferred by TiDB Cloud, the table column type inferred, and the previewed data from the CSV file.

    - If you import data into an existing table in TiDB Cloud, the column list is extracted from the table definition, and the previewed data is mapped to the corresponding columns by column names.

    - If you want to create a new table, the column list is extracted from the CSV file, and the column type is inferred by TiDB Cloud. For example, if the previewed data is all integers, the inferred column type will be **int** (integer).

5. Configure the column names and data types.

    If the first row in the CSV file records the column names, make sure that **Use first row as column name** is selected, which is selected by default.

    If the CSV file does not have a row for the column names, do not select **Use first row as column name**. In this case:

    - If the target table already exists, the columns in the CSV file will be imported into the target table in order. Extra columns will be truncated and missing columns will be filled with default values.

    - If you need TiDB Cloud to create the target table, input the name for each column. The column name must meet the following requirements:

        * The name must be composed of only letters (a-z and A-Z), numbers (0-9), characters (such as Chinese and Japanese), and the underscore (`_`) character.
        * Other special characters are not supported.
        * The length of the name must be less than 65 characters.

        You can also change the data type if needed.

6. For a new target table, you can set the primary key. You can select a column as the primary key, or select multiple columns to create a composite primary key. The composite primary key will be formed in the order in which you select the column names.

    > **Note:**
    >
    > - The primary key of the table is a clustered index and cannot be deleted after creation.
    > - Ensure that the data corresponding to the primary key field is unique and not empty. Otherwise, the import task will result in data inconsistency.

7. Edit the CSV configuration if needed.

   You can also click **Edit CSV configuration** to configure Backslash Escape, Separator, and Delimiter for more fine-grained control. For more information about the CSV configuration, see [CSV Configurations for Importing Data](/tidb-cloud/csv-config-for-import-data.md).

8. On the **Preview** page, you can have a preview of the data. Click **Start Import**.

    You can view the import progress on the **Import Task Detail** page. If there are warnings or failed tasks, you can check to view the details and solve them.

9. After the import task is completed, you can click **Explore your data by Chat2Query** to query your imported data. For more information about how to use Chat2Query, see [Explore Your Data with AI-Powered Chat2Query](/tidb-cloud/explore-data-with-chat2query.md).

10. On the **Import** page, you can click **View** in the **Action** column to check the import task detail.

## FAQ

### Can I only import some specified columns by the Import feature in TiDB Cloud?

No. Currently, you can only import all columns of a CSV file into an existing table when using the Import feature.

To import only some specified columns, you can use the MySQL client to connect your TiDB cluster, and then use [`LOAD DATA`](https://docs.pingcap.com/tidb/stable/sql-statement-load-data) to specify the columns to be imported. For example:

```sql
CREATE TABLE `import_test` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(64) NOT NULL,
  `address` varchar(64) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB;
LOAD DATA LOCAL INFILE 'load.txt' INTO TABLE import_test FIELDS TERMINATED BY ',' (name, address);
```

If you use `mysql` and encounter `ERROR 2068 (HY000): LOAD DATA LOCAL INFILE file request rejected due to restrictions on access.`, you can add `--local-infile=true` in the connection string.

### Why can't I query a column with a reserved keyword after importing data into TiDB Cloud?

If a column name is a reserved [keyword](/keywords.md) in TiDB, TiDB Cloud automatically adds backticks `` ` `` to enclose the column name and then imports the data into the target table. When you query the column, you need to add backticks `` ` `` to enclose the column name. For example, if the column name is `order`, you need to query the column with `` `order` ``.

### How to import a local file larger than 50 MiB?

If the file is larger than 50 MiB, you can use the `split [-l ${line_count}]` utility to split it into multiple smaller files (for Linux or macOS only). For example, run `split -l 100000 tidb-01.csv small_files` to split a file named `tidb-01.csv` by line length `100000`, and the split files are named `small_files${suffix}`. Then, you can import these smaller files to TiDB Cloud one by one.

Refer to the following script:

```bash
#!/bin/bash
n=$1
file_path=$2
file_extension="${file_path##*.}"
file_name="${file_path%.*}"
lines_per_file=$(( $(wc -l < $file_path) / $n ))
split -d -a 1 -l $lines_per_file $file_path $file_name.
for (( i=0; i<$n; i++ ))
do
    mv $file_name.$i $file_name.$i.$file_extension
done
```

You can input `n` and a file name, and then run the script. The script will divide the file into `n` equal parts while keeping the original file extension. For example:

```bash
> sh ./split.sh 3 mytest.customer.csv
> ls -h | grep mytest
mytest.customer.0.csv
mytest.customer.1.csv
mytest.customer.2.csv
mytest.customer.csv
```
