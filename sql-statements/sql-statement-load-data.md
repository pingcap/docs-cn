---
title: LOAD DATA | TiDB SQL Statement Reference
summary: An overview of the usage of LOAD DATA for the TiDB database.
aliases: ['/docs/dev/sql-statements/sql-statement-load-data/','/docs/dev/reference/sql/statements/load-data/']
---

# LOAD DATA

The `LOAD DATA` statement batch loads data into a TiDB table.

In TiDB v7.0.0, the `LOAD DATA` SQL statement becomes more powerful by integrating TiDB Lightning's logical import mode, including the following:

- Support importing data from S3 and GCS
- Support importing Parquet format data
- Add new parameters `FORMAT`, `FIELDS DEFINED NULL BY`, and `With batch_size=<number>,detached`

> **Warning:**
>
> The new capabilities and parameters are experimental. It is not recommended to use it in a production environment.

<CustomContent platform="tidb-cloud">

> **Note:**
>
> This feature is only available on [Serverless Tier clusters](/tidb-cloud/select-cluster-tier.md#serverless-tier-beta).

</CustomContent>

## Synopsis

```ebnf+diagram
LoadDataStmt ::=
    'LOAD' 'DATA' LocalOpt 'INFILE' stringLit FormatOpt DuplicateOpt 'INTO' 'TABLE' TableName CharsetOpt Fields Lines IgnoreLines ColumnNameOrUserVarListOptWithBrackets LoadDataSetSpecOpt LoadDataOptionListOpt

LocalOpt ::= ('LOCAL')?

FormatOpt ::=
    ('FORMAT' ('DELIMITED DATA' | 'SQL FILE' | 'PARQUET'))?

Fields ::=
    ('TERMINATED' 'BY' stringLit
    | ('OPTIONALLY')? 'ENCLOSED' 'BY' stringLit
    | 'ESCAPED' 'BY' stringLit
    | 'DEFINED' 'NULL' 'BY' stringLit ('OPTIONALLY' 'ENCLOSED')?)?

LoadDataOptionListOpt ::=
    ('WITH' (LoadDataOption (',' LoadDataOption)*))?

LoadDataOption ::=
    detached | batch_size '=' numberLiteral
```

## Parameters

### `LOCAL`

You can use `LOCAL` to specify data files on the client to be imported, where the file parameter must be the file system path on the client.

### S3 and GCS storage

<CustomContent platform="tidb">

If you do not specify `LOCAL`, the file parameter must be a valid S3 or GCS path, as detailed in [external storage](/br/backup-and-restore-storages.md).

</CustomContent>

<CustomContent platform="tidb-cloud">

If you do not specify `LOCAL`, the file parameter must be a valid S3 or GCS path, as detailed in [external storage](https://docs.pingcap.com/tidb/stable/backup-and-restore-storages).

</CustomContent>

When the data files are stored on S3 or GCS, you can import individual files or use the wildcard character `*` to match multiple files to be imported. Note that wildcards do not recursively process files in subdirectories. The following are some examples:

- Import a single file: `s3://<bucket-name>/path/to/data/foo.csv`
- Import all files in the specified path: `s3://<bucket-name>/path/to/data/*`
- Import all files ending with `.csv` under the specified path: `s3://<bucket-name>/path/to/data/*.csv`
- Import all files prefixed with `foo` under the specified path: `s3://<bucket-name>/path/to/data/foo*`
- Import all files prefixed with `foo` and ending with `.csv` under the specified path: `s3://<bucket-name>/path/to/data/foo*.csv`

### `FORMAT`

You can use the `FORMAT` parameter to specify the format of the data file. If you do not specify this parameter, you are using the format defined by `DELIMITED DATA`, which is the default data format of MySQL `LOAD DATA`.

### `Fields`, `Lines`, and `Ignore Lines`

You can specify the `Fields`, `Lines`, and `Ignore Lines` parameters only when the data format is `DELIMITED DATA`.

You can use the `Fields` and `Lines` parameters to specify how to handle the data format.

- `FIELDS TERMINATED BY`: specifies the data delimiter.
- `FIELDS ENCLOSED BY`: specifies the enclosing character of the data.
- `LINES TERMINATED BY`: specifies the line terminator, if you want to end a line with a certain character.

You can use `DEFINED NULL BY` to specify how NULL values are represented in the data file.

- Consistent with MySQL behavior, if `ESCAPED BY` is not null, for example, if the default value `\` is used, then `\N` will be considered a NULL value.
- If you use `DEFINED NULL BY`, such as `DEFINED NULL BY 'my-null'`, `my-null` is considered a NULL value.
- If you use `DEFINED NULL BY ... OPTIONALLY ENCLOSED`, such as `DEFINED NULL BY 'my-null' OPTIONALLY ENCLOSED`, `my-null` and `"my-null"` (assuming `ENCLOSED BY '"`) are considered NULL values.
- If you do not use `DEFINED NULL BY` or `DEFINED NULL BY ... OPTIONALLY ENCLOSED`, but use `ENCLOSED BY`, such as `ENCLOSED BY '"'`, then `NULL` is considered a NULL value. This behavior is consistent with MySQL.
- In other cases, it is not considered a NULL value.

Take the following data format as an example:

```
"bob","20","street 1"\r\n
"alice","33","street 1"\r\n
```

If you want to extract `bob`, `20`, and `street 1`, specify the field delimiter as `','`, and the enclosing character as `'\"'`:

```sql
FIELDS TERMINATED BY ',' ENCLOSED BY '\"' LINES TERMINATED BY '\r\n'
```

If the data format is `DELIMITED DATA` and you do not specify the parameters above, the imported data is processed in the following way by default:

```sql
FIELDS TERMINATED BY '\t' ENCLOSED BY '' ESCAPED BY '\\'
LINES TERMINATED BY '\n' STARTING BY ''
```

You can ignore the first `number` lines of a file by configuring the `IGNORE <number> LINES` parameter. For example, if you configure `IGNORE 1 LINES`, the first line of a file is ignored.

### `WITH detached`

If you do not specify the `LOCAL` parameter, you can use `WITH detached` to make `LOAD DATA` run in the background.

You can view the created jobs via [`SHOW LOAD DATA`](/sql-statements/sql-statement-show-load-data.md) or you can use [`CANCEL LOAD DATA` and `DROP LOAD DATA`](/sql-statements/sql-statement-operate-load-data-job.md) to cancel or delete the created jobs.

### `WITH batch_size=<number>`

You can specify the number of rows to be written to TiDB in a batch with `WITH batch_size=<number>`. The default value is `1000`. `0` means no splitting.

## Examples

For a background job, the corresponding job id is output after the job execution.

```sql
LOAD DATA INFILE 's3://bucket-name/test.csv?access_key=XXX&secret_access_key=XXX' INTO TABLE my_db.my_table FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '' LINES TERMINATED BY '\n' WITH detached;
```

```sql
+--------+
| Job_ID |
+--------+
|      1 |
+--------+
1 row in set (3.14 sec)
```

```sql
SHOW LOAD DATA JOB 1;
```

```sql
+--------+----------------------------+----------------------------+---------------------+---------------------------+--------------------+-------------+------------+-----------+------------+------------------+------------------+-------------+----------------+
| Job_ID | Create_Time                | Start_Time                 | End_Time            | Data_Source               | Target_Table       | Import_Mode | Created_By | Job_State | Job_Status | Source_File_Size | Loaded_File_Size | Result_Code | Result_Message |
+--------+----------------------------+----------------------------+---------------------+---------------------------+-------------------+-------------+------------+-----------+------------+------------------+------------------+-------------+----------------+
|      1 | 2023-03-16 22:29:12.990576 | 2023-03-16 22:29:12.991951 | 0000-00-00 00:00:00 | s3://bucket-name/test.csv | `my_db`.`my_table` | logical     | root@%     | loading   | running    | 52.43MB          | 43.58MB          |           0 |                |
+--------+----------------------------+----------------------------+---------------------+---------------------------+--------------------+-------------+------------+-----------+------------+------------------+------------------+-------------+----------------+
1 row in set (0.01 sec)
```

The following example imports data using `LOAD DATA`. Comma is specified as the field delimiter. The double quotation marks that enclose the data are ignored. The first line of the file is ignored.

<CustomContent platform="tidb">

If you see `ERROR 1148 (42000): the used command is not allowed with this TiDB version`, refer to [ERROR 1148 (42000): the used command is not allowed with this TiDB version](/error-codes.md#mysql-native-error-messages) for troubleshooting.

</CustomContent>

<CustomContent platform="tidb-cloud">

If you see `ERROR 1148 (42000): the used command is not allowed with this TiDB version`, refer to [ERROR 1148 (42000): the used command is not allowed with this TiDB version](https://docs.pingcap.com/tidb/stable/error-codes#mysql-native-error-messages) for troubleshooting.

</CustomContent>

```sql
LOAD DATA LOCAL INFILE '/mnt/evo970/data-sets/bikeshare-data/2017Q4-capitalbikeshare-tripdata.csv' INTO TABLE trips FIELDS TERMINATED BY ',' ENCLOSED BY '\"' LINES TERMINATED BY '\r\n' IGNORE 1 LINES (duration, start_date, end_date, start_station_number, start_station, end_station_number, end_station, bike_number, member_type);
```

```sql
Query OK, 815264 rows affected (39.63 sec)
Records: 815264  Deleted: 0  Skipped: 0  Warnings: 0
```

`LOAD DATA` also supports using hexadecimal ASCII character expressions or binary ASCII character expressions as the parameters for `FIELDS ENCLOSED BY` and `FIELDS TERMINATED BY`. See the following example:

```sql
LOAD DATA LOCAL INFILE '/mnt/evo970/data-sets/bikeshare-data/2017Q4-capitalbikeshare-tripdata.csv' INTO TABLE trips FIELDS TERMINATED BY x'2c' ENCLOSED BY b'100010' LINES TERMINATED BY '\r\n' IGNORE 1 LINES (duration, start_date, end_date, start_station_number, start_station, end_station_number, end_station, bike_number, member_type);
```

In the above example, `x'2c'` is the hexadecimal representation of the `,` character, and `b'100010'` is the binary representation of the `"` character.

## MySQL compatibility

This statement is understood to be fully compatible with MySQL, except for character set options which are parsed but ignored. If you find any compatibility difference, you can [report it via an issue](https://github.com/pingcap/tidb/issues/new/choose) on GitHub.

<CustomContent platform="tidb">

> **Note:**
>
> - For versions earlier than TiDB v4.0.0, `LOAD DATA` commits every 20000 rows.
> - For versions from TiDB v4.0.0 to v6.6.0, TiDB commits all rows in one transaction by default.
> - Starting from TiDB v7.0.0, the number of rows to be committed in a batch is controlled by the `WITH batch_size=<number>` parameter of the `LOAD DATA` statement, which defaults to 1000 rows per commit.
> - After upgrading from TiDB v4.0.0 or earlier versions, `ERROR 8004 (HY000) at line 1: Transaction is too large, size: 100000058` might occur. The recommended way to resolve this error is to increase the [`txn-total-size-limit`](/tidb-configuration-file.md#txn-total-size-limit) value in your `tidb.toml` file. If you are unable to increase this limit, you can also restore the behavior before the upgrade by setting [`tidb_dml_batch_size`](/system-variables.md#tidb_dml_batch_size) to `20000`.

</CustomContent>

<CustomContent platform="tidb-cloud">

> **Note:**
>
> - For versions earlier than TiDB v4.0.0, `LOAD DATA` commits every 20000 rows.
> - For versions from TiDB v4.0.0 to v6.6.0, TiDB commits all rows in one transaction by default.
> - Starting from TiDB v7.0.0, the number of rows to be committed in a batch is controlled by the `WITH batch_size=<number>` parameter of the `LOAD DATA` statement, which defaults to 1000 rows per commit.
> - After upgrading from TiDB v4.0.0 or earlier versions, `ERROR 8004 (HY000) at line 1: Transaction is too large, size: 100000058` might occur. To resolve this error, you can restore the behavior before the upgrade by setting [`tidb_dml_batch_size`](/system-variables.md#tidb_dml_batch_size) to `20000`.

</CustomContent>

## See also

<CustomContent platform="tidb">

* [INSERT](/sql-statements/sql-statement-insert.md)
* [TiDB Optimistic Transaction Model](/optimistic-transaction.md)
* [TiDB Lightning](/tidb-lightning/tidb-lightning-overview.md)
* [`SHOW LOAD DATA`](/sql-statements/sql-statement-show-load-data.md)
* [`CANCEL LOAD DATA` and `DROP LOAD DATA`](/sql-statements/sql-statement-operate-load-data-job.md)

</CustomContent>

<CustomContent platform="tidb-cloud">

* [INSERT](/sql-statements/sql-statement-insert.md)
* [TiDB Optimistic Transaction Model](/optimistic-transaction.md)
* [TiDB Lightning](https://docs.pingcap.com/tidb/stable/tidb-lightning-overview)
* [`SHOW LOAD DATA`](/sql-statements/sql-statement-show-load-data.md)
* [`CANCEL LOAD DATA` and `DROP LOAD DATA`](/sql-statements/sql-statement-operate-load-data-job.md)

</CustomContent>