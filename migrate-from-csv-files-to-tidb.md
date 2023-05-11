---
title: Migrate Data from CSV Files to TiDB
summary: Learn how to migrate data from CSV files to TiDB.
aliases: ['/docs/dev/tidb-lightning/migrate-from-csv-using-tidb-lightning/','/docs/dev/reference/tools/tidb-lightning/csv/','/tidb/dev/migrate-from-csv-using-tidb-lightning']
---

# Migrate Data from CSV Files to TiDB

This document describes how to migrate data from CSV files to TiDB.

TiDB Lightning can read data from CSV files and other delimiter formats, such as tab-separated values (TSV). For other flat file data sources, you can also refer to this document and migrate data to TiDB.

## Prerequisites

- [Install TiDB Lightning](/migration-tools.md).
- [Get the target database privileges required for TiDB Lightning](/tidb-lightning/tidb-lightning-requirements.md#privileges-of-the-target-database).

## Step 1. Prepare the CSV files

Put all the CSV files in the same directory. If you need TiDB Lightning to recognize all CSV files, the file names should meet the following requirements:

- If a CSV file contains the data for an entire table, name the file `${db_name}.${table_name}.csv`.
- If the data of one table is separated into multiple CSV files, append a numeric suffix to these CSV files. For example, `${db_name}.${table_name}.003.csv`. The numeric suffixes can be inconsecutive but must be in ascending order. You also need to add extra zeros before the number to ensure all the suffixes are in the same length.

## Step 2. Create the target table schema

Because CSV files do not contain schema information, before importing data from CSV files into TiDB, you need to create the target table schema. You can create the target table schema by either of the following two methods:

* **Method 1**: create the target table schema using TiDB Lightning.

    Create SQL files that contain the required DDL statements:

    - Add `CREATE DATABASE` statements in the `${db_name}-schema-create.sql` files.
    - Add `CREATE TABLE` statements in the `${db_name}.${table_name}-schema.sql` files.

* **Method 2**: create the target table schema manually.

## Step 3. Create the configuration file

Create a `tidb-lightning.toml` file with the following content:

```toml
[lightning]
# Log
level = "info"
file = "tidb-lightning.log"

[tikv-importer]
# "local": Default backend. The local backend is recommended to import large volumes of data (1 TiB or more). During the import, the target TiDB cluster cannot provide any service.
# "tidb": The "tidb" backend is recommended to import data less than 1 TiB. During the import, the target TiDB cluster can provide service normally.
# For more information on import mode, refer to <https://docs.pingcap.com/tidb/stable/tidb-lightning-overview#tidb-lightning-architecture>
backend = "local"
# Set the temporary storage directory for the sorted Key-Value files. The directory must be empty, and the storage space must be greater than the size of the dataset to be imported. For better import performance, it is recommended to use a directory different from `data-source-dir` and use flash storage, which can use I/O exclusively.
sorted-kv-dir = "/mnt/ssd/sorted-kv-dir"

[mydumper]
# Directory of the data source.
data-source-dir = "${data-path}" # A local path or S3 path. For example, 's3://my-bucket/sql-backup'.

# Defines CSV format.
[mydumper.csv]
# Field separator of the CSV file. Must not be empty. If the source file contains fields that are not string or numeric, such as binary, blob, or bit, it is recommended not to usesimple delimiters such as ",", and use an uncommon character combination like "|+|" instead.
separator = ','
# Delimiter. Can be zero or multiple characters.
delimiter = '"'
# Configures whether the CSV file has a table header.
# If this item is set to true, TiDB Lightning uses the first line of the CSV file to parse the corresponding relationship of fields.
header = true
# Configures whether the CSV file contains NULL.
# If this item is set to true, any column of the CSV file cannot be parsed as NULL.
not-null = false
# If `not-null` is set to false (CSV contains NULL),
# The following value is parsed as NULL.
null = '\N'
# Whether to treat the backslash ('\') in the string as an escape character.
backslash-escape = true
# Whether to trim the last separator at the end of each line.
trim-last-separator = false

[tidb]
# The target cluster.
host = ${host}            # e.g.: 172.16.32.1
port = ${port}            # e.g.: 4000
user = "${user_name}"     # e.g.: "root"
password = "${password}"  # e.g.: "rootroot"
status-port = ${status-port} # During the import, TiDB Lightning needs to obtain the table schema information from the TiDB status port. e.g.: 10080
pd-addr = "${ip}:${port}" # The address of the PD cluster, e.g.: 172.16.31.3:2379. TiDB Lightning obtains some information from PD. When backend = "local", you must specify status-port and pd-addr correctly. Otherwise, the import will be abnormal.
```

For more information on the configuration file, refer to [TiDB Lightning Configuration](/tidb-lightning/tidb-lightning-configuration.md).

## Step 4. Tune the import performance (optional)

When you import data from CSV files with a uniform size of about 256 MiB, TiDB Lightning works in the best performance. However, if you import data from a single large CSV file, TiDB Lightning can only use one thread to process the import by default, which might slow down the import speed.

To speed up the import, you can split a large CSV file into smaller ones. For a CSV file in a common format, before TiDB Lightning reads the entire file, it is hard to quickly locate the beginning and ending positions of each line. Therefore, TiDB Lightning does not automatically split CSV files by default. But if your CSV files to be imported meet certain format requirements, you can enable the `strict-format` mode. In this mode, TiDB Lightning automatically splits a single large CSV file into multiple files, each in about 256 MiB, and processes them in parallel.

> **Note:**
>
> If a CSV file is not in a strict format but the `strict-format` mode is set to `true` by mistake, a field that spans multiple lines will be split into two fields. This causes the parsing to fail, and TiDB Lightning might import the corrupted data without reporting any error.

In a strict-format CSV file, each field only takes up one line. It must meet the following requirements:

- The delimiter is empty.
- Each field does not contain CR (`\r`) or LF (`\n`).

If your CSV file meets the above requirements, you can speed up the import by enabling the `strict-format` mode as follows:

```toml
[mydumper]
strict-format = true
```

## Step 5. Import the data

To start the import, run `tidb-lightning`. If you launch the program in the command line, the process might exit unexpectedly after receiving a SIGHUP signal. In this case, it is recommended to run the program using a `nohup` or `screen` tool. For example:

{{< copyable "shell-regular" >}}

```shell
nohup tiup tidb-lightning -config tidb-lightning.toml > nohup.out 2>&1 &
```

After the import starts, you can check the progress of the import by either of the following methods:

- `grep` the keyword `progress` in the log. The progress is updated every 5 minutes by default.
- Check progress in [the monitoring dashboard](/tidb-lightning/monitor-tidb-lightning.md).
- Check progress in [the TiDB Lightning web interface](/tidb-lightning/tidb-lightning-web-interface.md).

After TiDB Lightning completes the import, it exits automatically. Check whether `tidb-lightning.log` contains `the whole procedure completed` in the last lines. If yes, the import is successful. If no, the import encounters an error. Address the error as instructed in the error message.

> **Note:**
>
> Whether the import is successful or not, the last line of the log shows `tidb lightning exit`. It means that TiDB Lightning exits normally, but does not necessarily mean that the import is successful.

If the import fails, refer to [TiDB Lightning FAQ](/tidb-lightning/tidb-lightning-faq.md) for troubleshooting.

## Other file formats

If your data source is in other formats, to migrate data from your data source, you must end the file name with `.csv` and make corresponding changes in the `[mydumper.csv]` section of the `tidb-lightning.toml` configuration file. Here are example changes for common formats:

**TSV:**

```toml
# Format example
# ID    Region    Count
# 1     East      32
# 2     South     NULL
# 3     West      10
# 4     North     39

# Format configuration
[mydumper.csv]
separator = "\t"
delimiter = ''
header = true
not-null = false
null = 'NULL'
backslash-escape = false
trim-last-separator = false
```

**TPC-H DBGEN:**

```toml
# Format example
# 1|East|32|
# 2|South|0|
# 3|West|10|
# 4|North|39|

# Format configuration
[mydumper.csv]
separator = '|'
delimiter = ''
header = false
not-null = true
backslash-escape = false
trim-last-separator = true
```

## What's next

- [CSV Support and Restrictions](/tidb-lightning/tidb-lightning-data-source.md#csv).
