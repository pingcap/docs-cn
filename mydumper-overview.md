---
title: Mydumper Instructions
summary: Use Mydumper to export data from TiDB.
aliases: ['/docs/dev/mydumper-overview/','/docs/dev/reference/tools/mydumper/']
---

# Mydumper Instructions

## What is Mydumper?

[Mydumper](https://github.com/pingcap/mydumper) is a fork project optimized for TiDB. You can use this tool for logical backups of **MySQL** or **TiDB**.

It can be [downloaded](/download-ecosystem-tools.md) as part of the Enterprise Tools package.

### What enhancements does it contain over regular Mydumper?

+ To ensure backup consistency for TiDB, this optimized Mydumper tool sets the value of [tidb_snapshot](/read-historical-data.md#how-tidb-reads-data-from-history-versions) to specify the point in time when the data is backed up instead of using `FLUSH TABLES WITH READ LOCK`.

+ This tool uses the hidden `_tidb_rowid` column of TiDB to optimize the performance of concurrently exporting data from a single table.

## Usage

### New parameter description

`-z` or `--tidb-snapshot`: sets the `tidb_snapshot` to be used for the backup. The default value is the current TSO (the `Position` field output from `SHOW MASTER STATUS`). Set this parameter to the TSO or a valid `datetime` such as `-z "2016-10-08 16:45:26"`.

### Required privileges

- SELECT
- RELOAD
- LOCK TABLES
- REPLICATION CLIENT

### Usage example

Execute the following command to back up data from TiDB. You can add command line parameters to the command as needed:

{{< copyable "shell-regular" >}}

```bash
./bin/mydumper -h 127.0.0.1 -u root -P 4000
```

## Dump table data concurrently

This section introduces the working principle and parameters of Mydumper. This section also gives an example of Mydumper command, and explains the performance evaluation and the TiDB versions that support the `_tidb_rowid` index.

### Working principle

Mydumper first calculates `min(_tidb_rowid)` and `max(_tidb_rowid)`, and segments the table into chunks according to the value specified by `-r`. Then, Mydumper assigns these chunks to different threads and dumps these chunks concurrently.

### Parameters

- `-t` or `--threads`: specifies the number of concurrent threads (`4` by default).
- `-r` or `--rows`: specifies the maximum number of rows in a chunk. If this parameter is specified, Mydumper ignores the value of `--chunk-filesize`.

### Example

The following is a complete Mydumper command:

{{< copyable "shell-regular" >}}

```shell
./bin/mydumper -h 127.0.0.1 -u root -P 4000 -r 10000 -t 4
```

### Performance evaluation

Do a performance evaluation before you perform the dump operation. Because the concurrent scanning brings pressure on the TiDB and TiKV clusters, you need to evaluate and test the impact that the dump operation might have on the database clusters and applications.

### TiDB versions that support the `_tidb_rowid` index

Because concurrent table data dump uses the implicit `_tidb_rowid` row of TiDB, TiDB versions that support the `_tidb_rowid` index can fully take advantage of the concurrent dump.

The following TiDB versions supports the `_tidb_rowid` index:

- v2.1.3 and later v2.1 versions
- v3.0 and v3.1
- the latest unpublished version (by default)

## FAQ

### How to determine if the Mydumper I am using is the PingCAP optimized version?

Execute the following command：

{{< copyable "shell-regular" >}}

```bash
./bin/mydumper -V
```

If the output contains `git_hash` (`d3e6fec8b069daee772d0dbaa47579f67a5947e7` in the following example), you are using the PingCAP optimized version of Mydumper:

```
mydumper 0.9.5 (d3e6fec8b069daee772d0dbaa47579f67a5947e7), built against MySQL 5.7.24
```

### How to resolve the "invalid mydumper files for there are no `-schema-create.sql` files found" error when using Loader to restore the data backed up by Mydumper?

Check whether the `-T` or `--tables-list` option is used when using Mydumper to back up data. If these options are used, Mydumper does not generate a file that includes a `CREATE DATABASE` SQL statement.

**Solution**: Create the `{schema-name}-schema-create.sql` file in the directory for data backup of Mydumper. Write "CREATE DATABASE `{schema-name}`" to the file, and then run Loader.

### Why is the TIMESTAMP type of data exported using Mydumper inconsistent with that in the database?

Check whether the time zone of the server that is running Mydumper is consistent with that of the database. Mydumper converts the TIMESTAMP type of data according to the time zone of its server. You can add the `--skip-tz-utc` option to disable the conversion of dates and times.

### How to configure the `-F,--chunk-filesize` option of Mydumper?

Mydumper splits the data of each table into multiple chunks according to the value of this option during backup. Each chunk is saved in a file with a size of about `chunk-filesize`. In this way, data is split into multiple files and you can use the parallel processing of Loader/TiDB lightning to improve the import speed. If you later use **Loader** to restore the backup files, it is recommended to set the value of this option to `64` (in MB); If you use **TiDB Lightning** to restore files, `256` (in MB) is recommended.

### How to configure the `-s --statement-size` option of Mydumper?

Mydumper uses this option to control the size of `Insert Statement` which defaults to `10000000` (about 1 MB). Use this option to avoid the following errors when restoring data:

```log
packet for query is too large. Try adjusting the 'max_allowed_packet' variable
```

The default value meets the requirements in most cases, but **if it is a wide table, the size of a single row of data might exceed the limit of `statement-size`, and Mydumper reports the following warning**:

```log
Row bigger than statement_size for xxx
```

If you restore the data in this situation, Mydumper still reports the `packet for query is too large` error. To solve this problem, modify the following two configurations (take `128 MB` as an example):

* Execute `set @@global.max_allowed_packet=134217728` (`134217728` = `128 MB`) in TiDB server.
* Add the `max-allowed-packet=128M` line to the DB configuration of Loader or DM task's configuration file according to your situation. Then, restart the process or task.

### How to set the `-l, --long-query-guard` option of Mydumper?

Set the value of this option to the estimated time required for a backup. If Mydumper runs longer than this value, it reports an error and exits. It is recommended to set the value to `7200` (in seconds) for the first time of your backup and then modify it according to your actual backup time.

### How to set the `--tidb-force-priority` option of Mydumper?

This option can only be set when backing up TiDB’s data. It can be set to `LOW_PRIORITY`, `DELAYED`, or `HIGH_PRIORITY`. If you do not want data backup to affect online services, it is recommended to set this option to `LOW_PRIORITY`; if the backup has a higher priority, `HIGH_PRIORITY` is recommended.

### How to resolve the "GC life time is short than transaction duration" error when using Mydumper to back up TiDB's data?

Mydumper uses the `tidb_snapshot` system variable to ensure data consistency when backing up TiDB's data. This error is reported if the historical data of a snapshot is cleared by TiDB's Garbage Collection (GC) during backup. To solve this problem, perform the following steps:

1. Before using Mydumper to back up data, use MySQL client to check the value of `tikv_gc_life_time` in the TiDB cluster and set it to an appropriate value:

    {{< copyable "sql" >}}

    ```sql
    SELECT * FROM mysql.tidb WHERE VARIABLE_NAME = 'tikv_gc_life_time';
    ```

    ```
    +-----------------------+------------------------------------------------------------------------------------------------+
    | VARIABLE_NAME         | VARIABLE_VALUE                                                                                 |
    +-----------------------+------------------------------------------------------------------------------------------------+
    | tikv_gc_life_time     | 10m0s                                                                                          |
    +-----------------------+------------------------------------------------------------------------------------------------+
    1 rows in set (0.02 sec)
    ```

    {{< copyable "sql" >}}

    ```sql
    update mysql.tidb set VARIABLE_VALUE = '720h' where VARIABLE_NAME = 'tikv_gc_life_time';
    ```

2. Set the value of `tikv_gc_life_time` to the initial one after the backup is complete:

    {{< copyable "sql" >}}

    ```sql
    update mysql.tidb set VARIABLE_VALUE = '10m0s' where VARIABLE_NAME = 'tikv_gc_life_time';
    ```

### Do I need to configure the `--tidb-rowid` option of Mydumper?

If this option is set to true, the exported data contains the data of TiDB's hidden columns. Using hidden columns when restoring data to TiDB might cause data inconsistency. Currently, it is not recommended to use this option.

### How to resolve the "Segmentation Fault" error?

This bug has been fixed. If the error persists, you can upgrade to the latest version of Mydumper.

### How to resolve the "Error dumping table ({schema}.{table}) data: line ...... (total length ...)" error?

This error occurs when Mydumper parses SQL statements. In this situation, use the latest version of Mydumper. If this error persists, you can file an issue to [mydumper/issues](https://github.com/pingcap/mydumper/issues).

### How to resolve the "Failed to set tidb_snapshot: parsing time \"20190901-10:15:00 +0800\" as \"20190901-10:15:00 +0700 MST\": cannot parse \"\" as \"MST\"" error?

Check whether the version of TiDB is lower than 2.1.11. If so, upgrade to TiDB 2.1.11 or later versions.

### Do you plan to make these changes available to upstream Mydumper?

Yes, we intend to make our changes available to upstream Mydumper. See [PR #155](https://github.com/maxbube/mydumper/pull/155).
