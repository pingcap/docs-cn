---
title: TiCDC CSV Protocol
summary: Learn the concept of TiCDC CSV Protocol and how to use it.
---

# TiCDC CSV Protocol

When using a cloud storage service as the downstream sink, you can send DML events to the cloud storage service in CSV format.

## Use CSV

The following is an example of the configuration when using the CSV protocol:

```shell
cdc cli changefeed create --server=http://127.0.0.1:8300 --changefeed-id="csv-test" --sink-uri="s3://bucket/prefix" --config changefeed.toml
```

The configuration in the `changefeed.toml` file is as follows:

```toml
[sink]
protocol = "csv"
terminator = "\n"

[sink.csv]
delimiter = ','
quote = '"'
null = '\N'
include-commit-ts = true
```

## Transactional constraints

- In a single CSV file, the `commit-ts` of a row is equal to or smaller than that of the subsequent row.
- The same transactions of a single table are stored in the same CSV file.
- Multiple tables of the same transaction can be stored in different CSV files.

## Data storage path structure

For more information about the storage path structure of the data, see [Storage path structure](/ticdc/ticdc-sink-to-cloud-storage.md#storage-path-structure).

## Definition of the data format

In the CSV file, each column is defined as follows:

- Column 1: The operation-type indicator, including `I`, `U`, and `D`. `I` means `INSERT`, `U` means `UPDATE`, and `D` means `DELETE`.
- Column 2: Table name.
- Column 3: Schema name.
- Column 4: The `commit-ts` of the source transaction. This column is optional.
- Column 5 to the last column: One or more columns that represent data to be changed.

Assume that table `hr.employee` is defined as follows:

```sql
CREATE TABLE `employee` (
  `Id` int NOT NULL,
  `LastName` varchar(20) DEFAULT NULL,
  `FirstName` varchar(30) DEFAULT NULL,
  `HireDate` date DEFAULT NULL,
  `OfficeLocation` varchar(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

The DML events of this table are stored in the CSV format as follows:

```shell
"I","employee","hr",433305438660591626,101,"Smith","Bob","2014-06-04","New York"
"U","employee","hr",433305438660591627,101,"Smith","Bob","2015-10-08","Los Angeles"
"D","employee","hr",433305438660591629,101,"Smith","Bob","2017-03-13","Dallas"
"I","employee","hr",433305438660591630,102,"Alex","Alice","2017-03-14","Shanghai"
"U","employee","hr",433305438660591630,102,"Alex","Alice","2018-06-15","Beijing"
```

## Data type mapping

| MySQL type                                          | CSV type | Example                          | Description                                   |
|-----------------------------------------------------|----------|------------------------------|---------------------------------------|
| `BOOLEAN`/`TINYINT`/`SMALLINT`/`INT`/`MEDIUMINT`/`BIGINT` | Integer | `123` | - |
| `FLOAT`/`DOUBLE`                                        | Float    | `153.123`                      |  -                                     |
| `NULL`                                                | Null     | `\N`                          | -                                      |
| `TIMESTAMP`/`DATETIME`                                  | String   | `"1973-12-30 15:30:00.123456"` | Format: `yyyy-MM-dd HH:mm:ss.%06d`         |
| `DATE`                                                | String   | `"2000-01-01"`                 | Format: `yyyy-MM-dd`                       |
| `TIME`                                                | String   | `"23:59:59"`                   | Format: `yyyy-MM-dd`                         |
| `YEAR`                                                | Integer  | `1970`                         |  -                                     |
| `VARCHAR`/`JSON`/`TINYTEXT`/`MEDIUMTEXT`/`LONGTEXT`/`TEXT`/`CHAR` | String   | `"test"`                       | UTF-8 encoded                       |
| `VARBINARY`/`TINYBLOB`/`MEDIUMBLOB`/`LONGBLOB`/`BLOB`/`BINARY`  | String   | `"6Zi/5pav"` or `"e998bfe696af"`                  | Base64 or hex encoded                      |
| `BIT`                                                 | Integer  | `81`                           | -                                      |
| `DECIMAL`                                             | String   | `"129012.1230000"`             | -                                      |
| `ENUM`                                                | String   | `"a"`                          | -                                     |
| `SET`                                                 | String   | `"a,b"`                        | -                                     |
