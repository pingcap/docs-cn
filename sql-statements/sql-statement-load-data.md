---
title: LOAD DATA | TiDB SQL Statement Reference
summary: An overview of the usage of LOAD DATA for the TiDB database.
aliases: ['/docs/dev/sql-statements/sql-statement-load-data/','/docs/dev/reference/sql/statements/load-data/']
---

# LOAD DATA

The `LOAD DATA` statement batch loads data into a TiDB table.

## Synopsis

**LoadDataStmt:**

![LoadDataStmt](/media/sqlgram/LoadDataStmt.png)

## Parameters

### `LocalOpt`

You can specify that the imported data file is located on the client or on the server by configuring the `LocalOpt` parameter. Currently, TiDB only supports data import from the client. Therefore, when importing data, set the value of `LocalOpt` to `Local`.

### `Fields` and `Lines`

You can specify how to process the data format by configuring the `Fields` and `Lines` parameters.

- `FIELDS TERMINATED BY`: Specifies the separating character of each data.
- `FIELDS ENCLOSED BY`: Specifies the enclosing character of each data.
- `LINES TERMINATED BY`: Specifies the line terminator, if you want to end a line with a certain character.

Take the following data format as an example:

```
"bob","20","street 1"\r\n
"alice","33","street 1"\r\n
```

If you want to extract `bob`, `20`, and `street 1`, specify the separating character as `','`, and the enclosing character as `'\"'`:

```sql
FIELDS TERMINATED BY ',' ENCLOSED BY '\"' LINES TERMINATED BY '\r\n'
```

If you do not specify the parameters above, the imported data is processed in the following way by default:

```sql
FIELDS TERMINATED BY '\t' ENCLOSED BY ''
LINES TERMINATED BY '\n'
```

### `IGNORE number LINES`

You can ignore the first `number` lines of a file by configuring the `IGNORE number LINES` parameter. For example, if you configure `IGNORE 1 LINES`, the first line of a file is ignored.

In addition, TiDB currently only supports parsing the syntax of the `DuplicateOpt`, `CharsetOpt`, and `LoadDataSetSpecOpt` parameters.

## Examples

{{< copyable "sql" >}}

```sql
CREATE TABLE trips (
    ->  trip_id bigint NOT NULL PRIMARY KEY AUTO_INCREMENT,
    ->  duration integer not null,
    ->  start_date datetime,
    ->  end_date datetime,
    ->  start_station_number integer,
    ->  start_station varchar(255),
    ->  end_station_number integer,
    ->  end_station varchar(255),
    ->  bike_number varchar(255),
    ->  member_type varchar(255)
    -> );
```

```
Query OK, 0 rows affected (0.14 sec)
```

The following example imports data using `LOAD DATA`. Comma is specified as the separating character. The double quotation marks that enclose the data is ignored. The first line of the file is ignored.

If you see the error message `ERROR 1148 (42000): the used command is not allowed with this TiDB version`, refer to [ERROR 1148 (42000): the used command is not allowed with this TiDB version](/faq/tidb-faq.md#error-1148-42000-the-used-command-is-not-allowed-with-this-tidb-version).

{{< copyable "sql" >}}

```
LOAD DATA LOCAL INFILE '/mnt/evo970/data-sets/bikeshare-data/2017Q4-capitalbikeshare-tripdata.csv' INTO TABLE trips FIELDS TERMINATED BY ',' ENCLOSED BY '\"' LINES TERMINATED BY '\r\n' IGNORE 1 LINES (duration, start_date, end_date, start_station_number, start_station, end_station_number, end_station, bike_number, member_type);
```

```
Query OK, 815264 rows affected (39.63 sec)
Records: 815264  Deleted: 0  Skipped: 0  Warnings: 0
```

`LOAD DATA` also supports using hexadecimal ASCII character expressions or binary ASCII character expressions as the parameters for `FIELDS ENCLOSED BY` and `FIELDS TERMINATED BY`. See the following example:

{{< copyable "sql" >}}

```sql
LOAD DATA LOCAL INFILE '/mnt/evo970/data-sets/bikeshare-data/2017Q4-capitalbikeshare-tripdata.csv' INTO TABLE trips FIELDS TERMINATED BY x'2c' ENCLOSED BY b'100010' LINES TERMINATED BY '\r\n' IGNORE 1 LINES (duration, start_date, end_date, start_station_number, start_station, end_station_number, end_station, bike_number, member_type);
```

In the above example, `x'2c'` is the hexadecimal representation of the `,` character and `b'100010'` is the binary representation of the `"` character.

## MySQL compatibility

* TiDB will by default commit every 20 000 rows. This behavior is similar to MySQL NDB Cluster, but not the default configuration with the InnoDB storage engine.

> **Note:**
>
> Committing through splitting a transaction is at the expense of breaking the atomicity and isolation of the transaction. When performing this operation, you must ensure that there are **no other** ongoing operations on the table. When an error occurs, **manual intervention is required to check the consistency and integrity of the data**. Therefore, it is not recommended to set this variable in a production environment.

## See also

* [INSERT](/sql-statements/sql-statement-insert.md)
* [Optimistic Transaction Model](/optimistic-transaction.md)
* [Import Example Database](/import-example-data.md)
