---
title: Dumpling Overview
summary: Use the Dumpling tool to export data from TiDB.
---

# Dumpling Overview

This document introduces the data export tool - [Dumpling](https://github.com/pingcap/dumpling). Dumpling exports data stored in TiDB/MySQL as SQL or CSV data files and can be used to make a logical full backup or export.

For backups of SST files (key-value pairs) or backups of incremental data that are not sensitive to latency, refer to [BR](/br/backup-and-restore-tool.md). For real-time backups of incremental data, refer to [TiCDC](/ticdc/ticdc-overview.md).

## Improvements of Dumpling compared with Mydumper

1. Support exporting data in multiple formats, including SQL and CSV
2. Support the [table-filter](https://github.com/pingcap/tidb-tools/blob/master/pkg/table-filter/README.md) feature, which makes it easier to filter data
3. Support exporting data to Amazon S3 cloud storage.
4. More optimizations are made for TiDB:
    - Support configuring the memory limit of a single TiDB SQL statement
    - Support automatic adjustment of TiDB GC time for TiDB v4.0.0 and above
    - Use TiDB's hidden column `_tidb_rowid` to optimize the performance of concurrent data export from a single table
    - For TiDB, you can set the value of [`tidb_snapshot`](/read-historical-data.md#how-tidb-reads-data-from-history-versions) to specify the time point of the data backup. This ensures the consistency of the backup, instead of using `FLUSH TABLES WITH READ LOCK` to ensure the consistency.

## Dumpling introduction

Dumpling is written in Go. The Github project is [pingcap/dumpling](https://github.com/pingcap/dumpling).

For detailed usage of Dumpling, use the `--help` option or refer to [Option list of Dumpling](#option-list-of-dumpling).

When using Dumpling, you need to execute the export command on a running cluster. This document assumes that there is a TiDB instance on the `127.0.0.1:4000` host and that this TiDB instance has a root user without a password.

Dumpling is included in the tidb-toolkit installation package and can be [download here](/download-ecosystem-tools.md#dumpling).

## Export data from TiDB/MySQL

### Required privileges

- SELECT
- RELOAD
- LOCK TABLES
- REPLICATION CLIENT

### Export to SQL files

Dumpling exports data to SQL files by default. You can also export data to SQL files by adding the `--filetype sql` flag:

{{< copyable "shell-regular" >}}

```shell
dumpling \
  -u root \
  -P 4000 \
  -h 127.0.0.1 \
  --filetype sql \
  --threads 32 \
  -o /tmp/test \
  -F 256MiB
```

In the above command, `-h`, `-P` and `-u` mean address, port and user, respectively. If password authentication is required, you can pass it to Dumpling with `-p $YOUR_SECRET_PASSWORD`.

### Export to CSV files

If Dumpling exports data to CSV files (use `--filetype csv` to export to CSV files), you can also use `--sql <SQL>` to export the records selected by the specified SQL statement.

For example, you can export all records that match `id < 100` in `test.sbtest1` using the following command:

{{< copyable "shell-regular" >}}

```shell
./dumpling \
  -u root \
  -P 4000 \
  -h 127.0.0.1 \
  -o /tmp/test \
  --filetype csv \
  --sql 'select * from `test`.`sbtest1` where id < 100'
```

> **Note:**
>
> - Currently, the `--sql` option can be used only for exporting to CSV files.
>
> - Here you need to execute the `select * from <table-name> where id <100` statement on all tables to be exported. If some tables do not have specified fields, the export fails.

### Export data to Amazon S3 cloud storage

Since v4.0.8, Dumpling supports exporting data to cloud storages. If you need to back up data to Amazon's S3 backend storage, you need to specify the S3 storage path in the `-o` parameter.

You need to create an S3 bucket in the specified region (see the [Amazon documentation - How do I create an S3 Bucket](https://docs.aws.amazon.com/AmazonS3/latest/user-guide/create-bucket.html)). If you also need to create a folder in the bucket, see the [Amazon documentation - Creating a folder](https://docs.aws.amazon.com/AmazonS3/latest/user-guide/create-folder.html).

Pass `SecretKey` and `AccessKey` of the account with the permission to access the S3 backend storage to the Dumpling node as environment variables.

{{< copyable "shell-regular" >}}

```shell
export AWS_ACCESS_KEY_ID=${AccessKey}
export AWS_SECRET_ACCESS_KEY=${SecretKey}
```

Dumpling also supports reading credential files from `~/.aws/credentials`. For more Dumpling configuration, see the configuration of [BR storages](/br/backup-and-restore-storages.md), which is consistent with the Dumpling configuration.

When you back up data using Dumpling, explicitly specify the `--s3.region` parameter, which means the region of the S3 storage:

{{< copyable "shell-regular" >}}

```shell
./dumpling \
  -u root \
  -P 4000 \
  -h 127.0.0.1 \
  -o "s3://${Bucket}/${Folder}" \
  --s3.region "${region}"
```

### Filter the exported data

#### Use the `--where` option to filter data

By default, Dumpling exports the tables of the entire database except the tables in the system databases. You can use `--where <SQL where expression>` to select the records to be exported.

{{< copyable "shell-regular" >}}

```shell
./dumpling \
  -u root \
  -P 4000 \
  -h 127.0.0.1 \
  -o /tmp/test \
  --where "id < 100"
```

The above command exports the data that matches `id < 100` from each table.

#### Use the `--filter` option to filter data

Dumpling can filter specific databases or tables by specifying the table filter with the `--filter` option. The syntax of table filters is similar to that of `.gitignore`. For details, see [Table Filter](/table-filter.md).

{{< copyable "shell-regular" >}}

```shell
./dumpling \
  -u root \
  -P 4000 \
  -h 127.0.0.1 \
  -o /tmp/test \
  --filter "employees.*" \
  --filter "*.WorkOrder"
```

The above command exports all the tables in the `employees` database and the `WorkOrder` tables in all databases.

#### Use the `-B` or `-T` option to filter data

Dumpling can also export specific databases with the `-B` option or specific tables with the `-T` option.

> **Note:**
>
> - The `--filter` option and the `-T` option cannot be used at the same time.
> - The `-T` option can only accept a complete form of inputs like `database-name.table-name`, and inputs with only the table name are not accepted. Example: Dumpling cannot recognize `-T WorkOrder`.

Examples:

- `-B employees` exports the `employees` database.
- `-T employees.WorkOrder` exports the `employees.WorkOrder` table.

### Improve export efficiency through concurrency

The exported file is stored in the `./export-<current local time>` directory by default. Commonly used options are as follows:

- `-o` is used to select the directory where the exported files are stored.
- `-F` option is used to specify the maximum size of a single file (the unit here is `MiB`; inputs like `5GiB` or `8KB` are also acceptable).
- `-r` option is used to specify the maximum number of records (or the number of rows in the database) for a single file. When it is enabled, Dumpling enables concurrency in the table to improve the speed of exporting large tables.

With the above options specified, Dumpling can have a higher degree of parallelism.

### Adjust Dumpling's data consistency options

> **Note:**
>
> In most scenarios, you do not need to adjust the default data consistency options of Dumpling.

Dumpling uses the `--consistency <consistency level>` option to control the way in which data is exported for "consistency assurance". For TiDB, data consistency is guaranteed by getting a snapshot of a certain timestamp by default (i.e. `--consistency snapshot`). When using snapshot for consistency, you can use the `--snapshot` option to specify the timestamp to be backed up. You can also use the following levels of consistency:

- `flush`: Use [`FLUSH TABLES WITH READ LOCK`](https://dev.mysql.com/doc/refman/8.0/en/flush.html#flush-tables-with-read-lock) to ensure consistency.
- `snapshot`: Get a consistent snapshot of the specified timestamp and export it.
- `lock`: Add read locks on all tables to be exported.
- `none`: No guarantee for consistency.
- `auto`: Use `flush` for MySQL and `snapshot` for TiDB.

After everything is done, you can see the exported file in `/tmp/test`:

{{< copyable "shell-regular" >}}

```shell
ls -lh /tmp/test | awk '{print $5 "\t" $9}'
```

```
140B  metadata
66B   test-schema-create.sql
300B  test.sbtest1-schema.sql
190K  test.sbtest1.0.sql
300B  test.sbtest2-schema.sql
190K  test.sbtest2.0.sql
300B  test.sbtest3-schema.sql
190K  test.sbtest3.0.sql
```

### Export historical data snapshot of TiDB

Dumpling can export the data of a certain [tidb_snapshot](/read-historical-data.md#how-tidb-reads-data-from-history-versions) with the `--snapshot` option specified.

The `--snapshot` option can be set to a TSO (the `Position` field output by the `SHOW MASTER STATUS` command) or a valid time of the `datetime` data type, for example:

{{< copyable "shell-regular" >}}

```shell
./dumpling --snapshot 417773951312461825
./dumpling --snapshot "2020-07-02 17:12:45"
```

The TiDB historical data snapshots when the TSO is `417773951312461825` and the time is `2020-07-02 17:12:45` are exported.

### Control the memory usage of exporting large tables

When Dumpling is exporting a large single table from TiDB, Out of Memory (OOM) might occur because the exported data size is too large, which causes connection abort and export failure. You can use the following parameters to reduce the memory usage of TiDB:

+ Setting `--rows` to split the data to be exported into chunks. This reduces the memory overhead of TiDB's data scan and enables concurrent table data dump to improve export efficiency.
+ Reduce the value of `--tidb-mem-quota-query` to `8589934592` (8 GB) or lower. `--tidb-mem-quota-query` controls the memory usage of a TiDB query and its default value is 32 GB.
+ Adjust the `--params "tidb_distsql_scan_concurrency=5"` parameter. [`tidb_distsql_scan_concurrency`](/system-variables.md#tidb_distsql_scan_concurrency) is a session variable which controls the concurrency of the scan operations in TiDB.

### TiDB GC settings when exporting a large volume of data

When exporting data from TiDB, if the TiDB version is greater than v4.0.0 and Dumpling can access the PD address of the TiDB cluster, Dumpling automatically extends the GC time without affecting the original cluster. But for TiDB earlier than v4.0.0, you need to manually modify the GC time.

In other scenarios, if the data size is very large, to avoid export failure due to GC during the export process, you can extend the GC time in advance:

{{< copyable "sql" >}}

```sql
update mysql.tidb set VARIABLE_VALUE = '720h' where VARIABLE_NAME = 'tikv_gc_life_time';
```

After your operation is completed, set the GC time back (the default value is `10m`):

{{< copyable "sql" >}}

```sql
update mysql.tidb set VARIABLE_VALUE = '10m' where VARIABLE_NAME = 'tikv_gc_life_time';
```

Finally, all the exported data can be imported back to TiDB using [Lightning](/tidb-lightning/tidb-lightning-backends.md).

## Option list of Dumpling

| Options | Usage | Default value |
| --------| --- | --- |
| `-V` or `--version` | Output the Dumpling version and exit directly |
| `-B` or `--database` | Export specified databases |
| `-T` or `--tables-list` | Export specified tables |
| `-f` or `--filter` | Export tables that match the filter pattern. For the filter syntax, see [table-filter](/table-filter.md). | `"\*.\*"` (export all databases or tables) |
| `--case-sensitive` | whether table-filter is case-sensitive | false (case-insensitive) |
| `-h` or `--host` | The IP address of the connected database host | "127.0.0.1" |
| `-t` or `--threads` | The number of concurrent backup threads | 4 |
| `-r` or `--rows` | Divide the table into specified rows of data (generally applicable for concurrent operations of splitting a large table into multiple files. |
| `-L` or `--logfile` | Log output address. If it is empty, the log will be output to the console | "" |
| `--loglevel` | Log level {debug,info,warn,error,dpanic,panic,fatal} | "info" |
| `--logfmt` | Log output format {text,json} | "text" |
| `-d` or `--no-data` | Do not export data (suitable for scenarios where only the schema is exported) |
| `--no-header` | Export CSV files of the tables without generating header |
| `-W` or `--no-views` | Do not export the views | true |
| `-m` or `--no-schemas` | Do not export the schema with only the data exported |
| `-s` or `--statement-size` | Control the size of the `INSERT` statements; the unit is bytes |
| `-F` or `--filesize` | The file size of the divided tables. The unit must be specified such as `128B`, `64KiB`, `32MiB`, and `1.5GiB`. |
| `--filetype` | Exported file type (csv/sql) | "sql" |
| `-o` or `--output` | Exported file path | "./export-${time}" |
| `-S` or `--sql` | Export data according to the specified SQL statement. This command does not support concurrent export. |
| `--consistency` | flush: use FTWRL before the dump <br/> snapshot: dump the TiDB data of a specific snapshot of a TSO <br/> lock: execute `lock tables read` on all tables to be dumped <br/> none: dump without adding locks, which cannot guarantee consistency <br/> auto: MySQL defaults to using flush, TiDB defaults to using snapshot | "auto" |
| `--snapshot` | Snapshot TSO; valid only when `consistency=snapshot` |
| `--where` | Specify the scope of the table backup through the `where` condition |
| `-p` or `--password` | The password of the connected database host |
| `-P` or `--port` | The port of the connected database host | 4000 |
| `-u` or `--user` | The username of the connected database host | "root" |
| `--dump-empty-database` | Export the `CREATE DATABASE` statements of the empty databases | true |
| `--ca` | The address of the certificate authority file for TLS connection |
| `--cert` | The address of the client certificate file for TLS connection |
| `--key` | The address of the client private key file for TLS connection |
| `--csv-delimiter` | Delimiter of character type variables in CSV files | '"' |
| `--csv-separator` | Separator of each value in CSV files | ',' |
| `--csv-null-value` | Representation of null values in CSV files | "\\N" |
| `--escape-backslash` | Use backslash (`\`) to escape special characters in the export file | true |
| `--output-filename-template` | The filename templates represented in the format of [golang template](https://golang.org/pkg/text/template/#hdr-Arguments) <br/> Support the `{{.DB}}`, `{{.Table}}`, and `{{.Index}}` arguments <br/> The three arguments represent the database name, table name, and chunk ID of the data file | '{{.DB}}.{{.Table}}.{{.Index}}' |
| `--status-addr` | Dumpling's service address, including the address for Prometheus to pull metrics and pprof debugging | ":8281" |
| `--tidb-mem-quota-query` | The memory limit of exporting SQL statements by a single line of Dumpling command, the unit is byte, and the default value is 32 GB | 34359738368 |
| `--params` | Specifies the session variable for the connection of the database to be exported. The required format is `"character_set_client=latin1,character_set_connection=latin1"` |
