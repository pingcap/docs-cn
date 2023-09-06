---
title: LOAD DATA | TiDB SQL Statement Reference
summary: An overview of the usage of LOAD DATA for the TiDB database.
aliases: ['/docs/dev/sql-statements/sql-statement-load-data/','/docs/dev/reference/sql/statements/load-data/','/tidb/dev/sql-statement-operate-load-data-job','/tidb/dev/sql-statement-show-load-data']
---

# LOAD DATA

The `LOAD DATA` statement batch loads data into a TiDB table.

Starting from TiDB v7.0.0, the `LOAD DATA` SQL statement supports the following features:

- Support importing data from S3 and GCS
- Add a new parameter `FIELDS DEFINED NULL BY`

> **Warning:**
>
> The new parameter `FIELDS DEFINED NULL BY` and support for importing data from S3 and GCS are experimental. It is not recommended that you use it in the production environment. This feature might be changed or removed without prior notice. If you find a bug, you can report an [issue](https://github.com/pingcap/tidb/issues) on GitHub.

## Synopsis

```ebnf+diagram
LoadDataStmt ::=
    'LOAD' 'DATA' LocalOpt 'INFILE' stringLit DuplicateOpt 'INTO' 'TABLE' TableName CharsetOpt Fields Lines IgnoreLines ColumnNameOrUserVarListOptWithBrackets LoadDataSetSpecOpt

LocalOpt ::= ('LOCAL')?

Fields ::=
    ('TERMINATED' 'BY' stringLit
    | ('OPTIONALLY')? 'ENCLOSED' 'BY' stringLit
    | 'ESCAPED' 'BY' stringLit
    | 'DEFINED' 'NULL' 'BY' stringLit ('OPTIONALLY' 'ENCLOSED')?)?
```

## Parameters

### `LOCAL`

You can use `LOCAL` to specify data files on the client to be imported, where the file parameter must be the file system path on the client.

If you are using TiDB Cloud, to use the `LOAD DATA` statement to load local data files, you need to add the `--local-infile` option to the connection string when you connect to TiDB Cloud. 

- The following is an example connection string for TiDB Serverless:

    ```
    mysql --connect-timeout 15 -u '<user_name>' -h <host_name> -P 4000 -D test --ssl-mode=VERIFY_IDENTITY --ssl-ca=/etc/ssl/cert.pem -p<your_password> --local-infile
    ```

- The following is an example connection string for TiDB Dedicated:

    ```
    mysql --connect-timeout 15 --ssl-mode=VERIFY_IDENTITY --ssl-ca=<CA_path> --tls-version="TLSv1.2" -u root -h <host_name> -P 4000 -D test -p<your_password> --local-infile
    ```

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

### `Fields`, `Lines`, and `Ignore Lines`

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

If you do not specify the preceding parameters, the imported data is processed in the following way by default:

```sql
FIELDS TERMINATED BY '\t' ENCLOSED BY '' ESCAPED BY '\\'
LINES TERMINATED BY '\n' STARTING BY ''
```

You can ignore the first `number` lines of a file by configuring the `IGNORE <number> LINES` parameter. For example, if you configure `IGNORE 1 LINES`, the first line of a file is ignored.

## Examples

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

The syntax of the `LOAD DATA` statement is compatible with that of MySQL, except for character set options which are parsed but ignored. If you find any syntax compatibility difference, you can [report a bug](https://docs.pingcap.com/tidb/stable/support).

<CustomContent platform="tidb">

> **Note:**
>
> - For versions earlier than TiDB v4.0.0, `LOAD DATA` commits every 20000 rows.
> - For versions from TiDB v4.0.0 to v6.6.0, TiDB commits all rows in one transaction by default.
> - After upgrading from TiDB v4.0.0 or earlier versions, `ERROR 8004 (HY000) at line 1: Transaction is too large, size: 100000058` might occur. The recommended way to resolve this error is to increase the [`txn-total-size-limit`](/tidb-configuration-file.md#txn-total-size-limit) value in your `tidb.toml` file. If you are unable to increase this limit, you can also restore the behavior before the upgrade by setting [`tidb_dml_batch_size`](/system-variables.md#tidb_dml_batch_size) to `20000`. Note that starting from v7.0.0, `tidb_dml_batch_size` no longer takes effect on the `LOAD DATA` statement.
> - No matter how many rows are committed in a transaction, `LOAD DATA` is not rolled back by the [`ROLLBACK`](/sql-statements/sql-statement-rollback.md) statement in an explicit transaction.
> - The `LOAD DATA` statement is always executed in optimistic transaction mode, regardless of the TiDB transaction mode configuration.

</CustomContent>

<CustomContent platform="tidb-cloud">

> **Note:**
>
> - For versions earlier than TiDB v4.0.0, `LOAD DATA` commits every 20000 rows.
> - For versions from TiDB v4.0.0 to v6.6.0, TiDB commits all rows in one transaction by default.
> - Starting from TiDB v7.0.0, the number of rows to be committed in a batch is controlled by the `WITH batch_size=<number>` parameter of the `LOAD DATA` statement, which defaults to 1000 rows per commit.
> - After upgrading from TiDB v4.0.0 or earlier versions, `ERROR 8004 (HY000) at line 1: Transaction is too large, size: 100000058` might occur. To resolve this error, you can restore the behavior before the upgrade by setting [`tidb_dml_batch_size`](/system-variables.md#tidb_dml_batch_size) to `20000`.
> - No matter how many rows are committed in a transaction, `LOAD DATA` is not rolled back by the [`ROLLBACK`](/sql-statements/sql-statement-rollback.md) statement in an explicit transaction.
> - The `LOAD DATA` statement is always executed in optimistic transaction mode, regardless of the TiDB transaction mode configuration.

</CustomContent>

## See also

<CustomContent platform="tidb">

* [INSERT](/sql-statements/sql-statement-insert.md)
* [TiDB Optimistic Transaction Model](/optimistic-transaction.md)
* [TiDB Pessimistic Transaction Mode](/pessimistic-transaction.md)

</CustomContent>

<CustomContent platform="tidb-cloud">

* [INSERT](/sql-statements/sql-statement-insert.md)
* [TiDB Optimistic Transaction Model](/optimistic-transaction.md)
* [TiDB Pessimistic Transaction Mode](/pessimistic-transaction.md)

</CustomContent>
