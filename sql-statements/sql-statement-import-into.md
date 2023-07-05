---
title: IMPORT INTO
summary: An overview of the usage of IMPORT INTO in TiDB.
---

# IMPORT INTO

The `IMPORT INTO` statement is used to import data in formats such as `CSV`, `SQL`, and `PARQUET` into an empty table in TiDB via the [Physical Import Mode](/tidb-lightning/tidb-lightning-physical-import-mode.md) of TiDB Lightning.

<!-- Support note for TiDB Cloud:

This TiDB statement is not applicable to TiDB Cloud.

-->

> **Warning:**
>
> Currently, this statement is experimental. It is not recommended to use it in production environments.

`IMPORT INTO` supports importing data from files stored in Amazon S3, GCS, and the TiDB local storage.

- For data files stored in Amazon S3 or GCS, `IMPORT INTO` supports running in the [TiDB backend task distributed execution framework](/tidb-distributed-execution-framework.md).

    - When this framework is enabled ([tidb_enable_dist_task](/system-variables.md#tidb_enable_dist_task-new-in-v710) is `ON`), `IMPORT INTO` splits a data import job into multiple sub-jobs and distributes these sub-jobs to different TiDB nodes for execution to improve the import efficiency.
    - When this framework is disabled, `IMPORT INTO` only supports running on the TiDB node where the current user is connected.

- For data files stored locally in TiDB, `IMPORT INTO` only supports running on the TiDB node where the current user is connected. Therefore, the data files need to be placed on the TiDB node where the current user is connected. If you access TiDB through a proxy or load balancer, you cannot import data files stored locally in TiDB.

## Known issue

After starting a data import job, TiDB sorts the data to be imported locally. During the sorting, in the case that the disk space used by TiDB exceeds the specified value of [`DISK_QUOTA`](#withoptions) or reaches 80% of the local disk space and TiDB has already started writing data to TiKV, if you cancel the import job or the import job fails, the background import thread will continue running for a while before exiting completely. For more information, see [#45048](https://github.com/pingcap/tidb/issues/45048).

## Restrictions

- Currently, `IMPORT INTO` only supports importing data within 1 TiB.
- `IMPORT INTO` only supports importing data into existing empty tables in the database.
- `IMPORT INTO` does not support transactions or rollback. Executing `IMPORT INTO` within an explicit transaction (`BEGIN`/`END`) will return an error.
- The execution of `IMPORT INTO` blocks the current connection until the import is completed. To execute the statement asynchronously, you can add the `DETACHED` option.
- `IMPORT INTO` does not support working simultaneously with features such as [Backup & Restore](/br/backup-and-restore-overview.md), [`FLASHBACK CLUSTER TO TIMESTAMP`](/sql-statements/sql-statement-flashback-to-timestamp.md), [acceleration of adding indexes](/system-variables.md#tidb_ddl_enable_fast_reorg-new-in-v630), data import using TiDB Lightning, data replication using TiCDC, or [Point-in-Time Recovery (PITR)](/br/br-log-architecture.md).
- Only one `IMPORT INTO` job can run on a cluster at a time. Although `IMPORT INTO` performs a precheck for running jobs, it is not a hard limit. Starting multiple import jobs might work when multiple clients execute `IMPORT INTO` simultaneously, but you need to avoid that because it might result in data inconsistency or import failures.
- During the data import process, do not perform DDL or DML operations on the target table, and do not execute [`FLASHBACK DATABASE`](/sql-statements/sql-statement-flashback-database.md) for the target database. These operations can lead to import failures or data inconsistencies. In addition, it is **NOT** recommended to perform read operations during the import process, as the data being read might be inconsistent. Perform read and write operations only after the import is completed.
- The import process consumes system resources significantly. To get better performance, it is recommended to use TiDB nodes with at least 32 cores and 64 GiB of memory. TiDB writes sorted data to the TiDB [temporary directory](/tidb-configuration-file.md#temp-dir-new-in-v630) during import, so it is recommended to configure high-performance storage media such as flash memory. For more information, see [Physical Import Mode limitations](/tidb-lightning/tidb-lightning-physical-import-mode.md#requirements-and-restrictions).
- The TiDB [temporary directory](/tidb-configuration-file.md#temp-dir-new-in-v630) is expected to have at least 90 GiB of available space. It is recommended to allocate storage space that is equal to or greater than the volume of data to be imported.
- One import job supports importing data into one target table only. To import data into multiple target tables, after the import for a target table is completed, you need to create a new job for the next target table.

## Prerequisites for import

Before using `IMPORT INTO` to import data, make sure the following requirements are met:

- The target table to be imported is already created in TiDB and it is empty.
- The target cluster has sufficient space to store the data to be imported.
- The [temporary directory](/tidb-configuration-file.md#temp-dir-new-in-v630) of the TiDB node connected to the current session has at least 90 GiB of available space. If [`tidb_enable_dist_task`](/system-variables.md#tidb_enable_dist_task-new-in-v710) is enabled, also make sure that the temporary directory of each TiDB node in the cluster has sufficient disk space.

## Required privileges

Executing `IMPORT INTO` requires the `SELECT`, `UPDATE`, `INSERT`, `DELETE`, and `ALTER` privileges on the target table. To import files in TiDB local storage, the `FILE` privilege is also required.

## Synopsis

```ebnf+diagram
ImportIntoStmt ::=
    'IMPORT' 'INTO' TableName ColumnNameOrUserVarList? SetClause? FROM fileLocation Format? WithOptions?

ColumnNameOrUserVarList ::=
    '(' ColumnNameOrUserVar (',' ColumnNameOrUserVar)* ')'

SetClause ::=
    'SET' SetItem (',' SetItem)*

SetItem ::=
    ColumnName '=' Expr

Format ::=
    'CSV' | 'SQL' | 'PARQUET'

WithOptions ::=
    'WITH' OptionItem (',' OptionItem)*

OptionItem ::=
    optionName '=' optionVal | optionName
```

## Parameter description

### ColumnNameOrUserVarList

It specifies how each field in the data file corresponds to the columns in the target table. You can also use it to map fields to variables to skip certain fields for the import, or use it in `SetClause`.

- If this parameter is not specified, the number of fields in each row of the data file must match the number of columns in the target table, and the fields will be imported to the corresponding columns in order.
- If this parameter is specified, the number of specified columns or variables must match the number of fields in each row of the data file.

### SetClause

It specifies how the values of target columns are calculated. In the right side of the `SET` expression, you can reference the variables specified in `ColumnNameOrUserVarList`.

In the left side of the `SET` expression, you can only reference a column name that is not included in `ColumnNameOrUserVarList`. If the target column name already exists in `ColumnNameOrUserVarList`, the `SET` expression is invalid.

### fileLocation

It specifies the storage location of the data file, which can be an Amazon S3 or GCS URI path, or a TiDB local file path.

- Amazon S3 or GCS URI path: for URI configuration details, see [External storage](/br/backup-and-restore-storages.md#uri-format).
- TiDB local file path: it must be an absolute path, and the file extension must be `.csv`, `.sql`, or `.parquet`. Make sure that the files corresponding to this path are stored on the TiDB node connected by the current user, and the user has the `FILE` privilege.

> **Note:**
>
> If [SEM](/system-variables.md#tidb_enable_enhanced_security) is enabled in the target cluster, the `fileLocation` cannot be specified as a local file path.

In the `fileLocation` parameter, you can specify a single file or use the `*` wildcard to match multiple files for import. Note that the wildcard can only be used in the file name, because it does not match directories or recursively match files in subdirectories. Taking files stored on Amazon S3 as examples, you can configure the parameter as follows:

- Import a single file: `s3://<bucket-name>/path/to/data/foo.csv`
- Import all files in a specified path: `s3://<bucket-name>/path/to/data/*`
- Import all files with the `.csv` suffix in a specified path: `s3://<bucket-name>/path/to/data/*.csv`
- Import all files with the `foo` prefix in a specified path: `s3://<bucket-name>/path/to/data/foo*`
- Import all files with the `foo` prefix and the `.csv` suffix in a specified path: `s3://<bucket-name>/path/to/data/foo*.csv`

### Format

The `IMPORT INTO` statement supports three data file formats: `CSV`, `SQL`, and `PARQUET`. If not specified, the default format is `CSV`.

### WithOptions

You can use `WithOptions` to specify import options and control the data import process. For example, to execute the import asynchronously in the backend, you can enable the `DETACHED` mode for the import by adding the `WITH DETACHED` option to the `IMPORT INTO` statement.

The supported options are described as follows:

| Option name | Supported data formats | Description |
|:---|:---|:---|
| `CHARACTER_SET='<string>'` | CSV | Specifies the character set of the data file. The default character set is `utf8mb4`. The supported character sets include `binary`, `utf8`, `utf8mb4`, `gb18030`, `gbk`, `latin1`, and `ascii`. |
| `FIELDS_TERMINATED_BY='<string>'` | CSV | Specifies the field separator. The default separator is `,`. |
| `FIELDS_ENCLOSED_BY='<char>'` | CSV | Specifies the field delimiter. The default delimiter is `"`. |
| `FIELDS_ESCAPED_BY='<char>'` | CSV | Specifies the escape character for fields. The default escape character is `\`. |
| `FIELDS_DEFINED_NULL_BY='<string>'` | CSV | Specifies the value that represents `NULL` in the fields. The default value is `\N`. |
| `LINES_TERMINATED_BY='<string>'` | CSV | Specifies the line terminator. By default, `IMPORT INTO` automatically identifies `\n`, `\r`, or `\r\n` as line terminators. If the line terminator is one of these three, you do not need to explicitly specify this option. |
| `SKIP_ROWS=<number>` | CSV | Specifies the number of rows to skip. The default value is `0`. You can use this option to skip the header in a CSV file. If you use a wildcard to specify the source files for import, this option applies to all source files that are matched by the wildcard in `fileLocation`. |
| `DISK_QUOTA='<string>'` | All formats | Specifies the disk space threshold that can be used during data sorting. The default value is 80% of the disk space in the TiDB [temporary directory](/tidb-configuration-file.md#temp-dir-new-in-v630). If the total disk size cannot be obtained, the default value is 50 GiB. When specifying `DISK_QUOTA` explicitly, make sure that the value does not exceed 80% of the disk space in the TiDB temporary directory. |
| `DISABLE_TIKV_IMPORT_MODE` | All formats | Specifies whether to disable switching TiKV to import mode during the import process. By default, switching TiKV to import mode is not disabled. If there are ongoing read-write operations in the cluster, you can enable this option to avoid impact from the import process. |
| `THREAD=<number>` | All formats | Specifies the concurrency for import. The default value is 50% of the CPU cores, with a minimum value of 1. You can explicitly specify this option to control the resource usage, but make sure that the value does not exceed the number of CPU cores. To import data into a new cluster without any data, it is recommended to increase this concurrency appropriately to improve import performance. If the target cluster is already used in a production environment, it is recommended to adjust this concurrency according to your application requirements. |
| `MAX_WRITE_SPEED='<string>'` | All formats | Controls the write speed to a TiKV node. By default, there is no speed limit. For example, you can specify this option as `1MiB` to limit the write speed to 1 MiB/s. |
| `CHECKSUM_TABLE='<string>'` | All formats | Configures whether to perform a checksum check on the target table after the import to validate the import integrity. The supported values include `"required"` (default), `"optional"`, and `"off"`. `"required"` means performing a checksum check after the import. If the checksum check fails, TiDB will return an error and the import will exit. `"optional"` means performing a checksum check after the import. If an error occurs, TiDB will return a warning and ignore the error. `"off"` means not performing a checksum check after the import. |
| `DETACHED` | All Formats | Controls whether to execute `IMPORT INTO` asynchronously. When this option is enabled, executing `IMPORT INTO` immediately returns the information of the import job (such as the `Job_ID`), and the job is executed asynchronously in the backend. |

## Output

When `IMPORT INTO` completes the import or when the `DETACHED` mode is enabled, `IMPORT INTO` will return the current job information in the output, as shown in the following examples. For the description of each field, see [`SHOW IMPORT JOB(s)`](/sql-statements/sql-statement-show-import-job.md).

When `IMPORT INTO` completes the import, the example output is as follows:

```sql
IMPORT INTO t FROM '/path/to/small.csv';
+--------+--------------------+--------------+----------+-------+----------+------------------+---------------+----------------+----------------------------+----------------------------+----------------------------+------------+
| Job_ID | Data_Source        | Target_Table | Table_ID | Phase | Status   | Source_File_Size | Imported_Rows | Result_Message | Create_Time                | Start_Time                 | End_Time                   | Created_By |
+--------+--------------------+--------------+----------+-------+----------+------------------+---------------+----------------+----------------------------+----------------------------+----------------------------+------------+
|  60002 | /path/to/small.csv | `test`.`t`   |      363 |       | finished | 16B              |             2 |                | 2023-06-08 16:01:22.095698 | 2023-06-08 16:01:22.394418 | 2023-06-08 16:01:26.531821 | root@%     |
+--------+--------------------+--------------+----------+-------+----------+------------------+---------------+----------------+----------------------------+----------------------------+----------------------------+------------+
```

When the `DETACHED` mode is enabled, executing the `IMPORT INTO` statement will immediately return the job information in the output. From the output, you can see that the status of the job is `pending`, which means waiting for execution.

```sql
IMPORT INTO t FROM '/path/to/small.csv' WITH DETACHED;
+--------+--------------------+--------------+----------+-------+---------+------------------+---------------+----------------+----------------------------+------------+----------+------------+
| Job_ID | Data_Source        | Target_Table | Table_ID | Phase | Status  | Source_File_Size | Imported_Rows | Result_Message | Create_Time                | Start_Time | End_Time | Created_By |
+--------+--------------------+--------------+----------+-------+---------+------------------+---------------+----------------+----------------------------+------------+----------+------------+
|  60001 | /path/to/small.csv | `test`.`t`   |      361 |       | pending | 16B              |          NULL |                | 2023-06-08 15:59:37.047703 | NULL       | NULL     | root@%     |
+--------+--------------------+--------------+----------+-------+---------+------------------+---------------+----------------+----------------------------+------------+----------+------------+
```

## View and manage import jobs

For an import job with the `DETACHED` mode enabled, you can use [`SHOW IMPORT`](/sql-statements/sql-statement-show-import-job.md) to view its current job progress.

After an import job is started, you can cancel it using [`CANCEL IMPORT JOB <job-id>`](/sql-statements/sql-statement-cancel-import-job.md).

## Examples

### Import a CSV file with headers

```sql
IMPORT INTO t FROM '/path/to/file.csv' WITH skip_rows=1;
```

### Import a file asynchronously in the `DETACHED` mode

```sql
IMPORT INTO t FROM '/path/to/file.csv' WITH DETACHED;
```

### Skip importing a specific field in your data file

Assume that your data file is in the CSV format and its content is as follows:

```
id,name,age
1,Tom,23
2,Jack,44
```

And assume that the target table schema for the import is `CREATE TABLE t(id int primary key, name varchar(100))`. To skip importing the `age` field in the data file to the table `t`, you can execute the following SQL statement:

```sql
IMPORT INTO t(id, name, @1) FROM '/path/to/file.csv' WITH skip_rows=1;
```

### Import multiple data files using the wildcard `*`

Assume that there are three files named `file-01.csv`, `file-02.csv`, and `file-03.csv` in the `/path/to/` directory. To import these three files into a target table `t` using `IMPORT INTO`, you can execute the following SQL statement:

```sql
IMPORT INTO t FROM '/path/to/file-*.csv'
```

### Import data files from Amazon S3 or GCS

- Import data files from Amazon S3:

    ```sql
    IMPORT INTO t FROM 's3://bucket-name/test.csv?access-key=XXX&secret-access-key=XXX';
    ```

- Import data files from GCS:

    ```sql
    IMPORT INTO t FROM 'gs://bucket-name/test.csv';
    ```

For details about the URI path configuration for Amazon S3 or GCS, see [External storage](/br/backup-and-restore-storages.md#uri-format).

### Calculate column values using SetClause

Assume that your data file is in the CSV format and its content is as follows:

```
id,name,val
1,phone,230
2,book,440
```

And assume that the target table schema for the import is `CREATE TABLE t(id int primary key, name varchar(100), val int)`. If you want to multiply the `val` column values by 100 during the import, you can execute the following SQL statement:

```sql
IMPORT INTO t(id, name, @1) SET val=@1*100 FROM '/path/to/file.csv' WITH skip_rows=1;
```

### Import a data file in the SQL format

```sql
IMPORT INTO t FROM '/path/to/file.sql' FORMAT 'sql';
```

### Limit the write speed to TiKV

To limit the write speed to a TiKV node to 10 MiB/s, execute the following SQL statement:

```sql
IMPORT INTO t FROM 's3://bucket/path/to/file.parquet?access-key=XXX&secret-access-key=XXX' FORMAT 'parquet' WITH MAX_WRITE_SPEED='10MiB';
```

## MySQL compatibility

This statement is a TiDB extension to MySQL syntax.

## See also

* [`SHOW IMPORT JOB(s)`](/sql-statements/sql-statement-show-import-job.md)
* [`CANCEL IMPORT JOB`](/sql-statements/sql-statement-cancel-import-job.md)
