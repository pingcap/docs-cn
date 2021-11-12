---
title: TiDB Lightning Error Resolution
summary: Learn how to get and resolve type conversion and duplication errors
---

# TiDB Lightning Error Resolution

> **Warning:**
>
> TiDB Lightning error report and resolution are still experimental features. It is **NOT** recommended to only rely on them in the production environment.

Starting from v5.3.0, TiDB Lightning can be configured to skip errors like invalid type conversion and unique key conflicts, and continue processing as if those bad rows do not exist. A report will be generated for you to read and manually fix them afterward. This is ideal for importing from slightly dirty data source, where locating the errors manually are difficult and restarting TiDB Lightning on every encounter are costly.

## Type error

{{< copyable "" >}}

```toml
[lightning]
max-error = 0
```

You can use the configuration `lightning.max-error` to increase the tolerance of errors related to data types. If this is set to *N*, TiDB Lightning will allow and skip up to *N* errors from the data source before aborting. The default value 0 means any single error is fatal.

The following errors are governed by this configuration:

* Invalid value (example: set `'Text'` to an INT column).
* Numeric overflow (example: set 500 to a TINYINT column)
* String overflow (example: set `'Very Long Text'` to a VARCHAR(5) column).
* Zero date time (namely `'0000-00-00'` and `'2021-12-00'`).
* Set NULL to a NOT NULL column.
* Failed to evaluate a generated column expression.
* Column count mismatch. Number of values in the row does not match number of columns of the table.
* Unique/Primary key conflict in TiDB backend, when `on-duplicate = "error"`.
* Any other SQL errors.

The following errors are always fatal, and cannot be skipped by changing `max-error`:

* Syntax error (such as unclosed quotation marks) in the original CSV, SQL or Parquet file.
* I/O, network or system permission errors.

Unique/Primary key conflict in Local backend is handled separately, explained in the next section.

## Duplicate resolution

{{< copyable "" >}}

```toml
[tikv-importer]
duplicate-resolution = 'record'
```

Local backend imports data by first converting them to KV pairs, and ingest them into TiKV in batches. Unlike the TiDB backend, duplicate rows are not detected until the end of task. Therefore, duplicate errors in local backend is not controlled by `max-error`, but rather a separate configuration `duplicate-resolution`.

There are three possible values of `duplicate-resolution`:

* **'none'** — Do not detect duplicates. If a unique/primary key conflict does exist, the imported table will have inconsistent data and index, and will fail checksum check.
* **'record'** — Detect duplicates, but do not attempt to fix it. If a unique/primary key conflict does exist, the imported table will have inconsistent data and index, and will fail checksum check.
* **'remove'** — Detect duplicates, and remove *all* duplicated rows. The imported table will be consistent, but the involved rows are ignored and have to be added back manually.

TiDB Lightning duplicate resolution can only detect duplicates within the data source. It cannot handle conflict with existing data before running TiDB Lightning.

## Error report

{{< copyable "" >}}

```toml
[lightning]
task-info-schema-name = 'lightning_task_info'
```

All errors are written to tables in the `lightning_task_info` database, in the downstream TiDB cluster. The database name can be changed with the configuration `lightning.task-info-schema-name`.

TiDB Lightning creates 3 tables inside this database:

```sql
CREATE TABLE syntax_error_v1 (
    task_id     bigint NOT NULL,
    create_time datetime(6) NOT NULL DEFAULT now(6),
    table_name  varchar(261) NOT NULL,
    path        varchar(2048) NOT NULL,
    offset      bigint NOT NULL,
    error       text NOT NULL,
    context     text
);

CREATE TABLE type_error_v1 (
    task_id     bigint NOT NULL,
    create_time datetime(6) NOT NULL DEFAULT now(6),
    table_name  varchar(261) NOT NULL,
    path        varchar(2048) NOT NULL,
    offset      bigint NOT NULL,
    error       text NOT NULL,
    row_data    text NOT NULL
);

CREATE TABLE conflict_error_v1 (
    task_id     bigint NOT NULL,
    create_time datetime(6) NOT NULL DEFAULT now(6),
    table_name  varchar(261) NOT NULL,
    index_name  varchar(128) NOT NULL,
    key_data    text NOT NULL,
    row_data    text NOT NULL,
    raw_key     mediumblob NOT NULL,
    raw_value   mediumblob NOT NULL,
    raw_handle  mediumblob NOT NULL,
    raw_row     mediumblob NOT NULL,
    KEY (task_id, table_name)
);
```

**syntax_error_v1** is intended to record syntax error from files. It is not implemented yet.

**type_error_v1** records all [type errors](#type-error) managed by the `max-error` configuration. There is one row per error.

**conflict_error_v1** records all [unique/primary key conflict in local backend](#duplicate-resolution). There are 2 rows per pair of conflict.

| Column       | syntax | type | conflict | Explanation                                                                                                                         |
| ------------ | ------ | ---- | -------- | ----------------------------------------------------------------------------------------------------------------------------------- |
| task_id      | ✓      | ✓    | ✓        | The TiDB Lightning task ID generating this error                                                                                    |
| create_table | ✓      | ✓    | ✓        | When the error was recorded                                                                                                         |
| table_name   | ✓      | ✓    | ✓        | Name of the table containing the error, in the form ``'`db`.`tbl`'``                                                                |
| path         | ✓      | ✓    |          | Path of the file containing the error                                                                                               |
| offset       | ✓      | ✓    |          | Byte position in the file where the error is found                                                                                  |
| error        | ✓      | ✓    |          | Error message                                                                                                                       |
| context      | ✓      |      |          | Text surrounding the error                                                                                                          |
| index_name   |        |      | ✓        | Name of unique key in conflict. It is `'PRIMARY'` for primary key conflict                                                          |
| key_data     |        |      | ✓        | Formatted key handle of the row causing the error. The content is for human reference only, and not intended to be machine readable |
| row_data     |        | ✓    | ✓        | Formatted row data causing the error. The content is for human reference only, and not intended to be machine readable              |
| raw_key      |        |      | ✓        | Key of the conflicted KV pair                                                                                                       |
| raw_value    |        |      | ✓        | Value of the conflicted KV pair                                                                                                     |
| raw_handle   |        |      | ✓        | Row handle of the conflicted row                                                                                                    |
| raw_row      |        |      | ✓        | Encoded value of the conflicted row                                                                                                 |

> **Note:**
>
> The error report records the file offset, not line/column number which is inefficient to obtain. You can quickly jump near a byte position (using 183 as example) with
>
> * shell, printing several lines before —
>
>     ```sh
>     head -c 183 file.csv | tail
>     ```
>
> * shell, printing several lines after —
>
>     ```sh
>     tail -c +183 file.csv | head
>     ```
>
> * vim — `:goto 183` or `183go`

## Example

In this example we prepare a data source with some known errors.

1. Prepare the database and table schemas.

    {{< copyable "shell-regular" >}}

    ```sh
    mkdir example && cd example

    echo 'CREATE SCHEMA example;' > example-schema-create.sql
    echo 'CREATE TABLE t(a TINYINT PRIMARY KEY, b VARCHAR(12) NOT NULL UNIQUE);' > example.t-schema.sql
    ```

2. Prepare the data.

    {{< copyable "shell-regular" >}}

    ```sh
    cat <<EOF > example.t.1.sql

        INSERT INTO t (a, b) VALUES
        (0, NULL),              -- column is NOT NULL
        (1, 'one'),
        (2, 'two'),
        (40, 'forty'),          -- conflicts with the other 40 below
        (54, 'fifty-four'),     -- conflicts with the other 'fifty-four' below
        (77, 'seventy-seven'),  -- the string is longer than 12 characters
        (600, 'six hundred'),   -- the number overflows TINYINT
        (40, 'fourty'),         -- conflicts with the other 40 above
        (42, 'fifty-four');     -- conflicts with the other 'fifty-four' above

    EOF
    ```

3. Configure TiDB Lightning enable strict SQL mode, use the local backend to import, resolve duplicates by deleting, and skip up to 10 errors.

    {{< copyable "shell-regular" >}}

    ```sh
    cat <<EOF > config.toml

        [lightning]
        max-error = 10

        [tikv-importer]
        backend = 'local'
        sorted-kv-dir = '/tmp/lightning-tmp/'
        duplicate-resolution = 'remove'

        [mydumper]
        data-source-dir = '.'

        [tidb]
        host = '127.0.0.1'
        port = 4000
        user = 'root'
        password = ''
        sql-mode = 'STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE'

    EOF
    ```

4. Run TiDB Lightning. This command will exit successfully because all errors are skipped.

    {{< copyable "shell-regular" >}}

    ```sh
    tiup tidb-lightning -c config.toml
    ```

5. Verify that the imported table contains just the two normal rows:

    ```console
    $ mysql -u root -h 127.0.0.1 -P 4000 -e 'select * from example.t'

    +---+-----+
    | a | b   |
    +---+-----+
    | 1 | one |
    | 2 | two |
    +---+-----+
    ```

6. Check that `type_error_v1` table caught the three rows involving type conversion:

    ```console
    $ mysql -u root -h 127.0.0.1 -P 4000 -e 'select * from lightning_task_info.type_error_v1;' -E

    *************************** 1. row ***************************
        task_id: 1635888701843303564
    create_time: 2021-11-02 21:31:42.620090
     table_name: `example`.`t`
           path: example.t.1.sql
         offset: 46
          error: failed to cast value as varchar(12) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin for column `b` (#2): [table:1048]Column 'b' cannot be null
       row_data: (0,NULL)
    *************************** 2. row ***************************
        task_id: 1635888701843303564
    create_time: 2021-11-02 21:31:42.627496
     table_name: `example`.`t`
           path: example.t.1.sql
         offset: 183
          error: failed to cast value as varchar(12) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin for column `b` (#2): [types:1406]Data Too Long, field len 12, data len 13
       row_data: (77,'seventy-seven')
    *************************** 3. row ***************************
        task_id: 1635888701843303564
    create_time: 2021-11-02 21:31:42.629929
     table_name: `example`.`t`
           path: example.t.1.sql
         offset: 253
          error: failed to cast value as tinyint(4) for column `a` (#1): [types:1690]constant 600 overflows tinyint
       row_data: (600,'six hundred')
    ```

7. Check that `conflict_error_v1` table caught the four rows having unique/primary key conflicts:

    ```console
    $ mysql -u root -h 127.0.0.1 -P 4000 -e 'select * from lightning_task_info.conflict_error_v1;' --binary-as-hex -E

    *************************** 1. row ***************************
        task_id: 1635888701843303564
    create_time: 2021-11-02 21:31:42.669601
     table_name: `example`.`t`
     index_name: PRIMARY
       key_data: 40
       row_data: (40, "forty")
        raw_key: 0x7480000000000000C15F728000000000000028
      raw_value: 0x800001000000020500666F727479
     raw_handle: 0x7480000000000000C15F728000000000000028
        raw_row: 0x800001000000020500666F727479
    *************************** 2. row ***************************
        task_id: 1635888701843303564
    create_time: 2021-11-02 21:31:42.674798
     table_name: `example`.`t`
     index_name: PRIMARY
       key_data: 40
       row_data: (40, "fourty")
        raw_key: 0x7480000000000000C15F728000000000000028
      raw_value: 0x800001000000020600666F75727479
     raw_handle: 0x7480000000000000C15F728000000000000028
        raw_row: 0x800001000000020600666F75727479
    *************************** 3. row ***************************
        task_id: 1635888701843303564
    create_time: 2021-11-02 21:31:42.680332
     table_name: `example`.`t`
     index_name: b
       key_data: 54
       row_data: (54, "fifty-four")
        raw_key: 0x7480000000000000C15F6980000000000000010166696674792D666FFF7572000000000000F9
      raw_value: 0x0000000000000036
     raw_handle: 0x7480000000000000C15F728000000000000036
        raw_row: 0x800001000000020A0066696674792D666F7572
    *************************** 4. row ***************************
        task_id: 1635888701843303564
    create_time: 2021-11-02 21:31:42.681073
     table_name: `example`.`t`
     index_name: b
       key_data: 42
       row_data: (42, "fifty-four")
        raw_key: 0x7480000000000000C15F6980000000000000010166696674792D666FFF7572000000000000F9
      raw_value: 0x000000000000002A
     raw_handle: 0x7480000000000000C15F72800000000000002A
        raw_row: 0x800001000000020A0066696674792D666F7572
    ```