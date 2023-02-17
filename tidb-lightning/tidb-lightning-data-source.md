---
title: TiDB Lightning Data Sources
summary: Learn all the data sources supported by TiDB Lightning.
aliases: ['/docs/dev/tidb-lightning/migrate-from-csv-using-tidb-lightning/','/docs/dev/reference/tools/tidb-lightning/csv/','/tidb/dev/migrate-from-csv-using-tidb-lightning/']
---

# TiDB Lightning Data Sources

TiDB Lightning supports importing data from multiple data sources to TiDB clusters, including CSV, SQL, and Parquet files.

To specify the data source for TiDB Lightning, use the following configuration:

```toml
[mydumper]
# Local source data directory or the URI of the external storage such as S3. For more information about the URI of the external storage, see https://docs.pingcap.com/tidb/v6.6/backup-and-restore-storages#uri-format.
data-source-dir = "/data/my_database"
```

When TiDB Lightning is running, it looks for all files that match the pattern of `data-source-dir`.

| File | Type | Pattern |
| --------- | -------- | ------- |
| Schema file | Contains the `CREATE TABLE` DDL statement | `${db_name}.${table_name}-schema.sql` |
| Schema file | Contains the `CREATE DATABASE` DDL statement| `${db_name}-schema-create.sql` |
| Data file | If the data file contains data for a whole table, the file is imported into a table named `${db_name}.${table_name}` | <code>\${db_name}.\${table_name}.\${csv\|sql\|parquet}</code> |
| Data file | If the data for a table is split into multiple data files, each data file must be suffixed with a number in its filename | <code>\${db_name}.\${table_name}.001.\${csv\|sql\|parquet}</code> |
| Compressed file | If the file contains a compression suffix, such as `gzip`, `snappy`, or `zstd`, TiDB Lightning will decompress the file before importing it. | <code>\${db_name}.\${table_name}.\${csv\|sql\|parquet}.{compress}</code> |

TiDB Lightning processes data in parallel as much as possible. Because files must be read in sequence, the data processing concurrency is at the file level (controlled by `region-concurrency`). Therefore, when the imported file is large, the import performance is poor. It is recommended to limit the size of the imported file to no greater than 256 MiB to achieve the best performance.

## CSV

### Schema

CSV files are schema-less. To import CSV files into TiDB, you must provide a table schema. You can provide schema by either of the following methods:

* Create files named `${db_name}.${table_name}-schema.sql` and `${db_name}-schema-create.sql` that contain DDL statements.
* Manually create the table schema in TiDB.

### Configuration

You can configure the CSV format in the `[mydumper.csv]` section in the `tidb-lightning.toml` file. Most settings have a corresponding option in the [`LOAD DATA`](https://dev.mysql.com/doc/refman/8.0/en/load-data.html) statement of MySQL.

```toml
[mydumper.csv]
# The field separator. Can be one or multiple characters. The default is ','.
# If the data might contain commas, it is recommended to use '|+|' or other uncommon
# character combinations as a separator.
separator = ','
# Quoting delimiter. Empty value means no quoting.
delimiter = '"'
# Line terminator. Can be one or multiple characters. Empty value (default) means
# both "\n" (LF) and "\r\n" (CRLF) are line terminators.
terminator = ''
# Whether the CSV file contains a header.
# If `header` is true, the first line is skipped and mapped
# to the table columns.
header = true
# Whether the CSV file contains any NULL value.
# If `not-null` is true, all columns from CSV cannot be parsed as NULL.
not-null = false
# When `not-null` is false (that is, CSV can contain NULL),
# fields equal to this value will be treated as NULL.
null = '\N'
# Whether to parse backslash as escape character.
backslash-escape = true
# Whether to treat `separator` as the line terminator and trim all trailing separators.
trim-last-separator = false
```

If the input of a string field such as `separator`, `delimiter`, or `terminator` involves special characters, you can use a backslash to escape the special characters. The escape sequence must be a *double-quoted* string (`"…"`). For example, `separator = "\u001f"` means using the ASCII character `0X1F` as the separator.

You can use *single-quoted* strings (`'…'`) to suppress backslash escaping. For example, `terminator = '\n'` means using the two-character string, a backslash (`\`) followed by the letter `n`, as the terminator, rather than the LF `\n`.

For more details, see the [TOML v1.0.0 specification](https://toml.io/en/v1.0.0#string).

#### `separator`

- Defines the field separator.
- Can be one or multiple characters, but must not be empty.
- Common values:

    * `','` for CSV (comma-separated values).
    * `"\t"` for TSV (tab-separated values).
    * `"\u0001"` to use the ASCII character `0x01`.

- Corresponds to the `FIELDS TERMINATED BY` option in the LOAD DATA statement.

#### `delimiter`

- Defines the delimiter used for quoting.
- If `delimiter` is empty, all fields are unquoted.
- Common values:

    * `'"'` quotes fields with double-quote. The same as [RFC 4180](https://tools.ietf.org/html/rfc4180).
    * `''` disables quoting.

- Corresponds to the `FIELDS ENCLOSED BY` option in the `LOAD DATA` statement.

#### `terminator`

- Defines the line terminator.
- If `terminator` is empty, both `"\n"` (Line Feed) and `"\r\n"` (Carriage Return + Line Feed) are used as the line terminator.
- Corresponds to the `LINES TERMINATED BY` option in the `LOAD DATA` statement.

#### `header`

- Whether *all* CSV files contain a header row.
- If `header` is `true`, the first row is used as the *column names*. If `header` is `false`, the first row is treated as an ordinary data row.

#### `not-null` and `null`

- The `not-null` setting controls whether all fields are non-nullable.
- If `not-null` is `false`, the string specified by `null` is transformed to the SQL NULL instead of a specific value.
- Quoting does not affect whether a field is null.

    For example, in the following CSV file:

    ```csv
    A,B,C
    \N,"\N",
    ```

    In the default settings (`not-null = false; null = '\N'`), the columns `A` and `B` are both converted to NULL after being imported to TiDB. The column `C` is an empty string `''` but not NULL.

#### `backslash-escape`

- Whether to parse backslash inside fields as escape characters.
- If `backslash-escape` is true, the following sequences are recognized and converted:

    | Sequence | Converted to             |
    |----------|--------------------------|
    | `\0`     | Null character (`U+0000`)  |
    | `\b`     | Backspace (`U+0008`)       |
    | `\n`     | Line feed (`U+000A`)       |
    | `\r`     | Carriage return (`U+000D`) |
    | `\t`     | Tab (`U+0009`)             |
    | `\Z`     | Windows EOF (`U+001A`)     |

    In all other cases (for example, `\"`), the backslash is stripped, leaving the next character (`"`) in the field. The character left has no special roles (for example, delimiters) and is just an ordinary character.

- Quoting does not affect whether backslash is parsed as an escape character.

- Corresponds to the `FIELDS ESCAPED BY '\'` option in the `LOAD DATA` statement.

#### `trim-last-separator`

- Whether to treat `separator` as the line terminator and trim all trailing separators.

    For example, in the following CSV file:

    ```csv
    A,,B,,
    ```

    - When `trim-last-separator = false`, this is interpreted as a row of 5 fields `('A', '', 'B', '', '')`.
    - When `trim-last-separator = true`, this is interpreted as a row of 3 fields `('A', '', 'B')`.

- This option is deprecated. Use the `terminator` option instead.

    If your existing configuration is:

    ```toml
    separator = ','
    trim-last-separator = true
    ```

    It is recommended to change the configuration to:

    ```toml
    separator = ','
    terminator = ",\n" # Use ",\n" or ",'\r\n" according to your actual file.
    ```

#### Non-configurable options

TiDB Lightning does not support every option supported by the `LOAD DATA` statement. For example:

* There cannot be line prefixes (`LINES STARTING BY`).
* The header cannot be skipped (`IGNORE n LINES`) and must be valid column names.

### Strict format

TiDB Lightning works best when the input files have a uniform size of around 256 MiB. When the input is a single huge CSV file, TiDB Lightning can only process the file in one thread, which slows down the import speed.

This can be fixed by splitting the CSV into multiple files first. For the generic CSV format, there is no way to quickly identify where a row starts or ends without reading the whole file. Therefore, TiDB Lightning by default does *not* automatically split a CSV file. However, if you are certain that the CSV input adheres to certain restrictions, you can enable the `strict-format` setting to allow TiDB Lightning to split the file into multiple 256 MiB-sized chunks for parallel processing.

```toml
[mydumper]
strict-format = true
```

In a strict CSV file, every field occupies only a single line. In other words, one of the following must be true:

* Delimiter is empty.
* Every field does not contain the terminator itself. In the default configuration, this means every field does not contain CR (`\r`) or LF (`\n`).

If a CSV file is not strict, but `strict-format` is wrongly set to `true`, a field spanning multiple lines may be cut in half into two chunks, causing parse failure, or even quietly importing corrupted data.

### Common configuration examples

#### CSV

The default setting is already tuned for CSV following RFC 4180.

```toml
[mydumper.csv]
separator = ',' # If the data might contain a comma (','), it is recommended to use '|+|' or other uncommon character combinations as the separator.
delimiter = '"'
header = true
not-null = false
null = '\N'
backslash-escape = true
```

Example content:

```
ID,Region,Count
1,"East",32
2,"South",\N
3,"West",10
4,"North",39
```

#### TSV

```toml
[mydumper.csv]
separator = "\t"
delimiter = ''
header = true
not-null = false
null = 'NULL'
backslash-escape = false
```

Example content:

```
ID    Region    Count
1     East      32
2     South     NULL
3     West      10
4     North     39
```

#### TPC-H DBGEN

```toml
[mydumper.csv]
separator = '|'
delimiter = ''
terminator = "|\n"
header = false
not-null = true
backslash-escape = false
```

Example content:

```
1|East|32|
2|South|0|
3|West|10|
4|North|39|
```

## SQL

When TiDB Lightning processes a SQL file, because TiDB Lightning cannot quickly split a single SQL file, it cannot improve the import speed of a single file by increasing concurrency. Therefore, when you import data from SQL files, avoid a single huge SQL file. TiDB Lightning works best when the input files have a uniform size of around 256 MiB.

## Parquet

TiDB Lightning currently only supports Parquet files generated by Amazon Aurora or Apache Hive. To identify the file structure in S3, use the following configuration to match all data files:

```
[[mydumper.files]]
# The expression needed for parsing Amazon Aurora parquet files
pattern = '(?i)^(?:[^/]*/)*([a-z0-9_]+)\.([a-z0-9_]+)/(?:[^/]*/)*(?:[a-z0-9\-_.]+\.(parquet))$'
schema = '$1'
table = '$2'
type = '$3'
```

Note that this configuration only shows how to match the parquet files exported by Aurora snapshot. You need to export and process the schema file separately.

For more information on `mydumper.files`, refer to [Match customized file](#match-customized-files).

## Compressed files

TiDB Lightning currently supports compressed files exported by Dumpling or compressed files that follow the naming rules. Currently, TiDB Lightning supports the following compression algorithms: `gzip`, `snappy`, and `zstd`. When the file name follows the naming rules, TiDB Lightning automatically identifies the compression algorithm and imports the file after streaming decompression, without additional configuration.

> **Note:**
>
> - Because TiDB Lightning cannot concurrently decompress a single large compressed file, the size of the compressed file affects the import speed. It is recommended that a source file is no greater than 256 MiB after decompression.
> - TiDB Lightning only imports individually compressed data files and does not support importing a single compressed file with multiple data files included.
> - TiDB Lightning does not support `parquet` files compressed through another compression tool, such as `db.table.parquet.snappy`. If you want to compress `parquet` files, you can configure the compression format for the `parquet` file writer.
> - TiDB Lightning v6.4.0 and later versions only support `.bak` files and the following compressed data files: `gzip`, `snappy`, and `zstd`. Other types of files cause errors. For those unsupported files, you need to modify the file names in advance, or move those files out of the import data directory to avoid such errors.

## Match customized files

TiDB Lightning only recognizes data files that follow the naming pattern. In some cases, your data file might not follow the naming pattern, and thus data import is completed in a short time without importing any file.

To resolve this issue, you can use `[[mydumper.files]]` to match data files in your customized expression.

Take the Aurora snapshot exported to S3 as an example. The complete path of the Parquet file is `S3://some-bucket/some-subdir/some-database/some-database.some-table/part-00000-c5a881bb-58ff-4ee6-1111-b41ecff340a3-c000.gz.parquet`.

Usually, `data-source-dir` is set to `S3://some-bucket/some-subdir/some-database/` to import the `some-database` database.

Based on the preceding Parquet file path, you can write a regular expression like `(?i)^(?:[^/]*/)*([a-z0-9_]+)\.([a-z0-9_]+)/(?:[^/]*/)*(?:[a-z0-9\-_.]+\.(parquet))$` to match the files. In the match group, `index=1` is `some-database`, `index=2` is `some-table`, and `index=3` is `parquet`.

You can write the configuration file according to the regular expression and the corresponding index so that TiDB Lightning can recognize the data files that do not follow the default naming convention. For example:

```toml
[[mydumper.files]]
# The expression needed for parsing the Amazon Aurora parquet file
pattern = '(?i)^(?:[^/]*/)*([a-z0-9_]+)\.([a-z0-9_]+)/(?:[^/]*/)*(?:[a-z0-9\-_.]+\.(parquet))$'
schema = '$1'
table = '$2'
type = '$3'
```

- **schema**: The name of the target database. The value can be:
    - The group index obtained by using a regular expression, such as `$1`.
    - The name of the database that you want to import, such as `db1`. All matched files are imported into `db1`.
- **table**: The name of the target table. The value can be:
    - The group index obtained by using a regular expression, such as `$2`.
    - The name of the table that you want to import, such as `table1`. All matched files are imported into `table1`.
- **type**: The file type. Supports `sql`, `parquet`, and `csv`. The value can be:
    - The group index obtained by using a regular expression, such as `$3`.
- **key**: The file number, such as `001` in `${db_name}.${table_name}.001.csv`.
    - The group index obtained by using a regular expression, such as `$4`.

## Import data from Amazon S3

The following examples show how to import data from Amazon S3 using TiDB Lightning. For more parameter configurations, see [external storage URI](/br/backup-and-restore-storages.md#uri-format).

+ Use the locally configured permissions to access S3 data:

    ```bash
    ./tidb-lightning --tidb-port=4000 --pd-urls=127.0.0.1:2379 --backend=local --sorted-kv-dir=/tmp/sorted-kvs \
        -d 's3://my-bucket/sql-backup'
    ```

+ Use the path-style request to access S3 data:

    ```bash
    ./tidb-lightning --tidb-port=4000 --pd-urls=127.0.0.1:2379 --backend=local --sorted-kv-dir=/tmp/sorted-kvs \
        -d 's3://my-bucket/sql-backup?force-path-style=true&endpoint=http://10.154.10.132:8088'
    ```

+ Use a specific AWS IAM role ARN to access S3 data:

    ```bash
    ./tidb-lightning --tidb-port=4000 --pd-urls=127.0.0.1:2379 --backend=local --sorted-kv-dir=/tmp/sorted-kvs \
        -d 's3://my-bucket/test-data?role-arn=arn:aws:iam::888888888888:role/my-role'
    ```

* Use access keys of an AWS IAM user to access S3 data:

    ```bash
    ./tidb-lightning --tidb-port=4000 --pd-urls=127.0.0.1:2379 --backend=local --sorted-kv-dir=/tmp/sorted-kvs \
        -d 's3://my-bucket/test-data?access_key={my_access_key}&secret_access_key={my_secret_access_key}'
    ```

* Use the combination of AWS IAM role access keys and session tokens to access S3 data:

    ```bash
    ./tidb-lightning --tidb-port=4000 --pd-urls=127.0.0.1:2379 --backend=local --sorted-kv-dir=/tmp/sorted-kvs \
        -d 's3://my-bucket/test-data?access_key={my_access_key}&secret_access_key={my_secret_access_key}&session-token={my_session_token}'
    ```

## More resources

- [Export to CSV files Using Dumpling](/dumpling-overview.md#export-to-csv-files)
- [`LOAD DATA`](https://dev.mysql.com/doc/refman/8.0/en/load-data.html)
