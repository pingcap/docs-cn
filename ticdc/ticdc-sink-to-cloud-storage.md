---
title: Replicate Data to Storage Services
summary: Learn how to replicate data to storage services using TiCDC, and learn about the storage path of the replicated data.
---

# Replicate Data to Storage Services

> **Warning:**
>
> This feature is experimental. It is not recommended to use it in the production environment.

Since v6.5.0, TiCDC supports saving row change events to storage services, including Amazon S3, Azure Blob Storage, and NFS. This document describes how to create a changefeed that replicates incremental data to such storage services using TiCDC, and how data is stored. The organization of this document is as follows:

- [How to replicate data to storage services](#replicate-change-data-to-storage-services).
- [How data is stored in storage services](#storage-path-structure).

## Replicate change data to storage services

Run the following command to create a changefeed task:

```shell
cdc cli changefeed create \
    --server=http://10.0.10.25:8300 \
    --sink-uri="s3://logbucket/storage_test?protocol=canal-json" \
    --changefeed-id="simple-replication-task"
```

The output is as follows:

```shell
Info: {"upstream_id":7171388873935111376,"namespace":"default","id":"simple-replication-task","sink_uri":"s3://logbucket/storage_test?protocol=canal-json","create_time":"2022-11-29T18:52:05.566016967+08:00","start_ts":437706850431664129,"engine":"unified","config":{"case_sensitive":true,"enable_old_value":true,"force_replicate":false,"ignore_ineligible_table":false,"check_gc_safe_point":true,"enable_sync_point":false,"sync_point_interval":600000000000,"sync_point_retention":86400000000000,"filter":{"rules":["*.*"],"event_filters":null},"mounter":{"worker_num":16},"sink":{"protocol":"canal-json","schema_registry":"","csv":{"delimiter":",","quote":"\"","null":"\\N","include_commit_ts":false},"column_selectors":null,"transaction_atomicity":"none","encoder_concurrency":16,"terminator":"\r\n","date_separator":"none","enable_partition_separator":false},"consistent":{"level":"none","max_log_size":64,"flush_interval":2000,"storage":""}},"state":"normal","creator_version":"v6.5.0-master-dirty"}
```

- `--changefeed-id`: The ID of the changefeed. The format must match the `^[a-zA-Z0-9]+(\-[a-zA-Z0-9]+)*$` regular expression. If this ID is not specified, TiCDC automatically generates a UUID (the version 4 format) as the ID.
- `--sink-uri`: The downstream address of the changefeed. For details, see [Configure sink URI](#configure-sink-uri).
- `--start-ts`: The starting TSO of the changefeed. TiCDC starts pulling data from this TSO. The default value is the current time.
- `--target-ts`: The ending TSO of the changefeed. TiCDC stops pulling data until this TSO. The default value is empty, which means that TiCDC does not automatically stop pulling data.
- `--config`: The configuration file of the changefeed. For details, see [TiCDC changefeed configuration parameters](/ticdc/ticdc-changefeed-config.md).

## Configure sink URI

This section describes how to configure storage services in the changefeed URI, including Amazon S3, Azure Blob Storage, and NFS.

### Configure Amazon S3 or Azure Blob Storage

The URI parameters of Amazon S3 and Azure Blob Storage in TiCDC are the same as their URL parameters in BR. For details, see [Backup storage URI format](/br/backup-and-restore-storages.md#uri-format-description).

### Configure NFS

The following configuration saves row change events to NFS:

```shell
--sink-uri="file:///my-directory/prefix"
```

### Optional parameters

Other optional parameters in the URI are as follows:

| Parameter | Description | Default value | Value range |
| :---------| :---------- | :------------ | :---------- |
| `worker-count` | Concurrency for saving data changes to cloud storage in the downstream.  | `16` | `[1, 512]` |
| `flush-interval` | Interval for saving data changes to cloud storage in the downstream.   | `5s` | `[2s, 10m]` |
| `file-size` | A data change file is stored to cloud storage if the number of bytes exceeds the value of this parameter. | `67108864` | `[1048576, 536870912]` |
| `protocol` | The protocol format of the messages sent to the downstream.  | N/A |  `canal-json` and `csv` |

> **Note:**
>
> Data change files are saved to the downstream when either `flush-interval` or `file-size` meets the requirements.

## Storage path structure

This section describes the storage path structure of data change records, metadata, and DDL events.

### Data change records

Data change records are saved to the following path:

```shell
{scheme}://{prefix}/{schema}/{table}/{table-version-separator}/{partition-separator}/{date-separator}/CDC{num}.{extension}
```

- `scheme`: specifies the data transmission protocol, or the storage type, for example, <code>**s3**://xxxxx</code>.
- `prefix`: specifies the user-defined parent directory, for example, <code>s3://**bucket/bbb/ccc**</code>.
- `schema`: specifies the schema name, for example, <code>s3://bucket/bbb/ccc/**test**</code>.
- `table`: specifies the table name, for example, <code>s3://bucket/bbb/ccc/test/**table1**</code>.
- `table-version-separator`: specifies the separator that separates the path by the table version, for example, <code>s3://bucket/bbb/ccc/test/table1/**9999**</code>.
- `partition-separator`: specifies the separator that separates the path by the table partition, for example, <code>s3://bucket/bbb/ccc/test/table1/9999/**20**</code>.
- `date-separator`: classifies the files by the transaction commit date. Value options are:
    - `none`: no `date-separator`. For example, all files with `test.table1` version being `9999` are saved to `s3://bucket/bbb/ccc/test/table1/9999`.
    - `year`: the separator is the year of the transaction commit date, for example, <code>s3://bucket/bbb/ccc/test/table1/9999/**2022**</code>.
    - `month`: the separator is the year and month of the transaction commit date, for example, <code>s3://bucket/bbb/ccc/test/table1/9999/**2022-01**</code>.
    - `day`: the separator is the year, month, and day of the transaction commit date, for example, <code>s3://bucket/bbb/ccc/test/table1/9999/**2022-01-02**</code>.
- `num`: saves the serial number of the file that records the data change, for example, <code>s3://bucket/bbb/ccc/test/table1/9999/2022-01-02/CDC**000005**.csv</code>.
- `extension`: specifies the extension of the file. TiDB v6.5.0 supports the CSV and Canal-JSON formats.

> **Note:**
>
> The table version changes in the following two cases:
>
> - After a DDL operation is performed, the table version is the TSO when the DDL is executed in the upstream TiDB. However, the change of the table version does not mean the change of the table schema. For example, adding a comment to a column does not cause the `schema.json` file content to change.
> - The changefeed process restarts. The table version is the checkpoint TSO when the process restarts. When there are many tables and the process restarts, it takes a long time to traverse all directories and find the position where each table was written last time. Therefore, data is written to a new directory with the version being the checkpoint TSO, instead of to the earlier directory.

### Metadata

Metadata is saved in the following path:

```shell
{protocol}://{prefix}/metadata
```

Metadata is a JSON-formatted file, for example:

```json
{
    "checkpoint-ts":433305438660591626
}
```

- `checkpoint-ts`: Transactions with `commit-ts` smaller than `checkpoint-ts` are written to the target storage in the downstream.

### DDL events

When DDL events cause the table version to change, TiCDC switches to a new path to write data change records. For example, when the version of `test.table1` changes from `9999` to `10000`, data will be written to the path `s3://bucket/bbb/ccc/test/table1/10000/2022-01-02/CDC000001.csv`. In addition, when DDL events occur, TiCDC generates a `schema.json` file to save the table schema information.

Table schema information is saved in the following path:

```shell
{scheme}://{prefix}/{schema}/{table}/{table-version-separator}/schema.json
```

The following is a `schema.json` file:

```json
{
    "Table":"table1",
    "Schema":"test",
    "Version":1,
    "TableVersion":10000,
    "Query": "ALTER TABLE test.table1 ADD OfficeLocation blob(20)",
    "TableColumns":[
        {
            "ColumnName":"Id",
            "ColumnType":"INT",
            "ColumnNullable":"false",
            "ColumnIsPk":"true"
        },
        {
            "ColumnName":"LastName",
            "ColumnType":"CHAR",
            "ColumnLength":"20"
        },
        {
            "ColumnName":"FirstName",
            "ColumnType":"VARCHAR",
            "ColumnLength":"30"
        },
        {
            "ColumnName":"HireDate",
            "ColumnType":"DATETIME"
        },
        {
            "ColumnName":"OfficeLocation",
            "ColumnType":"BLOB",
            "ColumnLength":"20"
        }
    ],
    "TableColumnsTotal":"5"
}
```

- `Table`: Table name.
- `Schema`: Schema name.
- `Version`: Protocol version of the storage sink.
- `TableVersion`: Table version.
- `Query`：DDL statement.
- `TableColumns`: An array of one or more maps, each of which describes a column in the source table.
    - `ColumnName`: Column name.
    - `ColumnType`: Column type. For details, see [Data type](#data-type).
    - `ColumnLength`: Column length. For details, see [Data type](#data-type).
    - `ColumnPrecision`: Column precision. For details, see [Data type](#data-type).
    - `ColumnScale`: The number of digits following the decimal point (the scale). For details, see [Data type](#data-type).
    - `ColumnNullable`: The column can be NULL when the value of this option is `true`.
    - `ColumnIsPk`: The column is part of the primary key when the value of this option is `true`.
- `TableColumnsTotal`: The size of the `TableColumns` array.

### Data type

This section describes the data types used in the `schema.json` file. The data types are defined as `T(M[, D])`. For details, see [Data Types](/data-type-overview.md).

#### Integer types

Integer types in TiDB are defined as `IT[(M)] [UNSIGNED]`, where

- `IT` is the integer type, which can be `TINYINT`, `SMALLINT`, `MEDIUMINT`, `INT`, `BIGINT`, or `BIT`.
- `M` is the display width of the type.

Integer types are defined as follows in `schema.json`:

```json
{
    "ColumnName":"COL1",
    "ColumnType":"{IT} [UNSIGNED]",
    "ColumnPrecision":"{M}"
}
```

#### Decimal types

Decimal types in TiDB are defined as `DT[(M,D)][UNSIGNED]`, where

- `DT` is the floating-point type, which can be `FLOAT`, `DOUBLE`, `DECIMAL`, or `NUMERIC`.
- `M` is the precision of the data type, or the total number of digits.
- `D` is the number of digits following the decimal point.

Decimal types are defined as follows in `schema.json`:

```json
{
    "ColumnName":"COL1",
    "ColumnType":"{DT} [UNSIGNED]",
    "ColumnPrecision":"{M}",
    "ColumnScale":"{D}"
}
```

#### Date and time types

Date types in TiDB are defined as `DT`, where

- `DT` is the date type, which can be `DATE` or `YEAR`.

The date types are defined as follows in `schema.json`:

```json
{
    "ColumnName":"COL1",
    "ColumnType":"{DT}"
}
```

The time types in TiDB are defined as `TT[(M)]`, where

- `TT` is the time type, which can be `TIME`, `DATETIME`, or `TIMESTAMP`.
- `M` is the precision of seconds in the range from 0 to 6.

The time types are defined as follows in `schema.json`:

```json
{
    "ColumnName":"COL1",
    "ColumnType":"{TT}",
    "ColumnScale":"{M}"
}
```

#### String types

The string types in TiDB are defined as `ST[(M)]`, where

- `ST` is the string type, which can be `CHAR`, `VARCHAR`, `TEXT`, `BINARY`, `BLOB`, or `JSON`.
- `M` is the maximum length of the string.

The string types are defined as follows in `schema.json`:

```json
{
    "ColumnName":"COL1",
    "ColumnType":"{ST}",
    "ColumnLength":"{M}"
}
```

#### Enum and Set types

The Enum and Set types are defined as follows in `schema.json`:

```json
{
    "ColumnName":"COL1",
    "ColumnType":"{ENUM/SET}",
}
```
