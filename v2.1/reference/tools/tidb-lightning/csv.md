---
title: TiDB-Lightning CSV Support
summary: Learn how to import CSV files via TiDB-Lightning.
category: reference
---

# TiDB-Lightning CSV Support

TiDB-Lightning supports reading CSV (comma-separated values) data source, as well as other
delimited format such as TSV (tab-separated values).

## File name

A CSV file representing a whole table must be named as `db_name.table_name.csv`. This will be
restored as a table `table_name` inside the database `db_name`.

If a table spans multiple CSV files, they should be named like `db_name.table_name.003.csv`.

The file extension must be `*.csv`, even if the content is not separated by commas.

## Schema

CSV files are schema-less. To import them into TiDB, a table schema must be provided. This could be
done either by:

* Providing a file named `db_name.table_name-schema.sql` containing the `CREATE TABLE` DDL
    statement
* Creating the empty tables directly in TiDB in the first place, and then setting
    `[mydumper] no-schema = true` in `tidb-lightning.toml`.

## Configuration

The CSV format can be configured in `tidb-lightning.toml` under the `[mydumper.csv]` section.
Most settings have a corresponding option in the MySQL [`LOAD DATA`] statement.

```toml
[mydumper.csv]
# Separator between fields, should be an ASCII character.
separator = ','
# Quoting delimiter, can either be an ASCII character or empty string.
delimiter = '"'
# Whether the CSV files contain a header.
# If `header` is true, the first line will be skipped.
header = true
# Whether the CSV contains any NULL value.
# If `not-null` is true, all columns from CSV cannot be NULL.
not-null = false
# When `not-null` is false (i.e. CSV can contain NULL),
# fields equal to this value will be treated as NULL.
null = '\N'
# Whether to interpret backslash escapes inside fields.
backslash-escape = true
# If a line ends with a separator, remove it.
trim-last-separator = false
```

[`LOAD DATA`]: https://dev.mysql.com/doc/refman/8.0/en/load-data.html

### `separator`

- Defines the field separator.
- Must be a single ASCII character.
- Common values:

    * `','` for CSV
    * `"\t"` for TSV

- Corresponds to the `FIELDS TERMINATED BY` option in the LOAD DATA statement.

### `delimiter`

- Defines the delimiter used for quoting.
- If `delimiter` is empty, all fields are unquoted.
- Common values:

    * `'"'` quote fields with double-quote, same as [RFC 4180]
    * `''` disable quoting

- Corresponds to the `FIELDS ENCLOSED BY` option in the `LOAD DATA` statement.

[RFC 4180]: https://tools.ietf.org/html/rfc4180

### `header`

- Whether *all* CSV files contain a header row.
- If `header` is true, the first row will be used as the
*column names*. If `header` is false, the first row is not special and treated as an ordinary data row.

### `not-null` and `null`

- The `not-null` setting controls whether all fields are non-nullable.
- If `not-null` is false, the
string specified by `null` will be transformed to the SQL NULL instead of a concrete value.
- Quoting will not affect whether a field is null.

    For example, with the CSV file:

    ```csv
    A,B,C
    \N,"\N",
    ```

    In the default settings (`not-null = false; null = '\N'`), the columns `A` and `B` are both
converted to NULL after importing to TiDB. The column `C` is simply the empty string `''` but not
NULL.

### `backslash-escape`

- Whether to interpret backslash escapes inside fields.
- If `backslash-escape` is true, the following sequences are
recognized and transformed:

    | Sequence | Converted to             |
    |----------|--------------------------|
    | `\0`     | Null character (U+0000)  |
    | `\b`     | Backspace (U+0008)       |
    | `\n`     | Line feed (U+000A)       |
    | `\r`     | Carriage return (U+000D) |
    | `\t`     | Tab (U+0009)             |
    | `\Z`     | Windows EOF (U+001A)     |

    In all other cases (e.g. `\"`) the backslash is simply stripped, leaving the next character (`"`)
in the field.

- Quoting will not affect whether backslash escapes are interpreted.

- Corresponds to the `FIELDS ESCAPED BY '\'` option in the `LOAD DATA` statement.

### `trim-last-separator`

- Treats the field `separator` as a terminator, and removes all trailing separators.

    For example, with the CSV file:

    ```csv
    A,,B,,
    ```

- When `trim-last-separator = false`, this is interpreted as a row of 5 fields `('A', '', 'B', '', '')`.
- When `trim-last-separator = true`, this is interpreted as a row of 3 fields `('A', '', 'B')`.

### Non-configurable options

Lightning does not support every option supported by the `LOAD DATA` statement. Some examples:

* The line terminator must only be CR (`\r`), LF (`\n`) or CRLF (`\r\n`), i.e. `LINES TERMINATED BY`
    is not customizable.
* There cannot be line prefixes (`LINES STARTING BY`).
* The header cannot be simply skipped (`IGNORE n LINES`), it must be valid column names if present.
* Delimiters and separators can only be a single ASCII character.

## Common configurations

### CSV

The default setting is already tuned for CSV following RFC 4180.

```toml
[mydumper.csv]
separator = ','
delimiter = '"'
header = true
not-null = false
null = '\N'
backslash-escape = true
trim-last-separator = false
```

Example content:

```
ID,Region,Count
1,"East",32
2,"South",\N
3,"West",10
4,"North",39
```

### TSV

```toml
[mydumper.csv]
separator = "\t"
delimiter = ''
header = true
not-null = false
null = 'NULL'
backslash-escape = false
trim-last-separator = false
```

Example content:

```
ID    Region    Count
1     East      32
2     South     NULL
3     West      10
4     North     39
```


### TPC-H DBGEN

```toml
[mydumper.csv]
separator = '|'
delimiter = ''
header = false
not-null = true
backslash-escape = false
trim-last-separator = true
```

Example content:

```
1|East|32|
2|South|0|
3|West|10|
4|North|39|
```
