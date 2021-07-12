---
title: TiCDC Open Protocol
aliases: ['/docs/dev/ticdc/ticdc-open-protocol/','/docs/dev/reference/tools/ticdc/open-protocol/','/docs/dev/ticdc/column-ddl-type-codes/']
---

# TiCDC Open Protocol

TiCDC Open Protocol is a row-level data change notification protocol that provides data sources for monitoring, caching, full-text indexing, analysis engines, and primary-secondary replication between different databases. TiCDC complies with TiCDC Open Protocol and replicates data changes of TiDB to third-party data medium such as MQ (Message Queue).

TiCDC Open Protocol uses Event as the basic unit to replicate data change events to the downstream. The Event is divided into three categories:

* Row Changed Event: Represents the data change in a row. When a row is changed, this Event is sent and contains information about the changed row.
* DDL Event: Represents the DDL change. This Event is sent after a DDL statement is successfully executed in the upstream. The DDL Event is broadcasted to every MQ Partition.
* Resolved Event: Represents a special time point before which the Event received is complete.

## Restrictions

* In most cases, the Row Changed Event of a version is sent only once, but in special situations such as node failure and network partition, the Row Changed Event of the same version might be sent multiple times.
* On the same table, the Row Changed Events of each version which is first sent are incremented in the order of timestamps (TS) in the Event stream.
* Resolved Events are periodically broadcasted to each MQ Partition. The Resolved Event means that any Event with a TS earlier than Resolved Event TS has been sent to the downstream.
* DDL Events are broadcasted to each MQ Partition.
* Multiple Row Changed Events of a row are sent to the same MQ Partition.

## Message format

A Message contains one or more Events, arranged in the following format:

Key:

| Offset(Byte) | 0~7     | 8~15 | 16~(15+length1) | ... | ... |
| :----------- | :------ | :--- | :----------- | :--- | :----------- |
| Parameter         | Protocol version | Length1 | Event Key1         | LengthN | Event KeyN         |

Value:

| Offset(Byte) | 0~7 | 8~(7+length1) | ... | ... |
| :----------- | :--- | :-------- | :--- | :------ |
| Parameter         | Length1 | Event Value1     | LengthN | Event ValueN |

* `LengthN` represents the length of the `N`th key/value.
* The length and protocol version are the big-endian `int64` type.
* The version of the current protocol is `1`.

## Event format

This section introduces the formats of Row Changed Event, DDL Event, and Resolved Event.

### Row Changed Event

+ **Key:**

    ```
    {
        "ts":<TS>,
        "scm":<Schema Name>,
        "tbl":<Table Name>,
        "t":1
    }
    ```

    | Parameter         | Type   | Description                    |
    | :---------- | :----- | :--------------------- |
    | TS          | Number |  The timestamp of the transaction that causes the row change.  |
    | Schema Name | String |  The name of the schema where the row is in. |
    | Table Name  | String |  The name of the table where the row is in. |

+ **Value:**

    `Insert` event. The newly added row data is output.

    ```
    {
        "u":{
            <Column Name>:{
                "t":<Column Type>,
                "h":<Where Handle>,
                "f":<Flag>,
                "v":<Column Value>
            },
            <Column Name>:{
                "t":<Column Type>,
                "h":<Where Handle>,
                "f":<Flag>,
                "v":<Column Value>
            }
        }
    }
    ```

    `Update` event. The newly added row data ("u") and the row data before the update ("p") are output. The latter ("p") is output only when the old value feature is enabled.

    ```
    {
        "u":{
            <Column Name>:{
                "t":<Column Type>,
                "h":<Where Handle>,
                "f":<Flag>,
                "v":<Column Value>
            },
            <Column Name>:{
                "t":<Column Type>,
                "h":<Where Handle>,
                "f":<Flag>,
                "v":<Column Value>
            }
        },
        "p":{
            <Column Name>:{
                "t":<Column Type>,
                "h":<Where Handle>,
                "f":<Flag>,
                "v":<Column Value>
            },
            <Column Name>:{
                "t":<Column Type>,
                "h":<Where Handle>,
                "f":<Flag>,
                "v":<Column Value>
            }
        }
    }
    ```

    `Delete` event. The deleted row data is output. When the old value feature is enabled, the `Delete` event includes all the columns of the deleted row data; when this feature is disabled, the `Delete` event only includes the [HandleKey](#bit-flags-of-columns) column.

    ```
    {
        "d":{
            <Column Name>:{
                "t":<Column Type>,
                "h":<Where Handle>,
                "f":<Flag>,
                "v":<Column Value>
            },
            <Column Name>:{
                "t":<Column Type>,
                "h":<Where Handle>,
                "f":<Flag>,
                "v":<Column Value>
            }
        }
    }
    ```

    | Parameter         | Type   | Description                    |
    | :---------- | :----- | :--------------------- |
    | Column Name    | String |  The column name.  |
    | Column Type    | Number |  The column type. For details, see [Column Type Code](#column-type-code).  |
    | Where Handle  | Boolean   |  Determines whether this column can be the filter condition of the `Where` clause. When this column is unique on the table, `Where Handle` is `true`. |
    | Flag       | Number   |  The bit flags of columns. For details, see [Bit flags of columns](#bit-flags-of-columns). |
    | Column Value   | Any    | The Column value.   |

### DDL Event

+ **Key:**

    ```
    {
        "ts":<TS>,
        "scm":<Schema Name>,
        "tbl":<Table Name>,
        "t":2
    }
    ```

    | Parameter         | Type   | Description                                 |
    | :---------- | :----- | :---------------------------------- |
    | TS          | Number |  The timestamp of the transaction that performs the DDL change.    |
    | Schema Name | String |  The schema name of the DDL change, which might be an empty string.  |
    | Table Name  | String |  The table name of the DDL change, which might be am empty string. |

+ **Value:**

    ```
    {
        "q":<DDL Query>,
        "t":<DDL Type>
    }
    ```

    | Parameter       | Type   | Description           |
    | :-------- | :----- | :------------ |
    | DDL Query | String | DDL Query SQL |
    | DDL Type  | String | The DDL type. For details, see [DDL Type Code](#ddl-type-code).    |

### Resolved Event

+ **Key:**

    ```
    {
        "ts":<TS>,
        "t":3
    }
    ```

    | Parameter         | Type   | Description                                         |
    | :---------- | :----- | :------------------------------------------ |
    | TS          | Number | The Resolved timestamp. Any TS earlier than this Event has been sent. |

+ **Value:** None

## Examples of the Event stream output

This section shows and displays the output logs of the Event stream.

Suppose that you execute the following SQL statement in the upstream and the MQ Partition number is 2:

{{< copyable "sql" >}}

```sql
CREATE TABLE test.t1(id int primary key, val varchar(16));
```

From the following Log 1 and Log 3, you can see that the DDL Event is broadcasted to all MQ Partitions, and that the Resolved Event is periodically broadcasted to each MQ Partition.

```
1. [partition=0] [key="{\"ts\":415508856908021766,\"scm\":\"test\",\"tbl\":\"t1\",\"t\":2}"] [value="{\"q\":\"CREATE TABLE test.t1(id int primary key, val varchar(16))\",\"t\":3}"]
2. [partition=0] [key="{\"ts\":415508856908021766,\"t\":3}"] [value=]
3. [partition=1] [key="{\"ts\":415508856908021766,\"scm\":\"test\",\"tbl\":\"t1\",\"t\":2}"] [value="{\"q\":\"CREATE TABLE test.t1(id int primary key, val varchar(16))\",\"t\":3}"]
4. [partition=1] [key="{\"ts\":415508856908021766,\"t\":3}"] [value=]
```

Execute the following SQL statements in the upstream:

{{< copyable "sql" >}}

```sql
BEGIN;
INSERT INTO test.t1(id, val) VALUES (1, 'aa');
INSERT INTO test.t1(id, val) VALUES (2, 'aa');
UPDATE test.t1 SET val = 'bb' WHERE id = 2;
INSERT INTO test.t1(id, val) VALUES (3, 'cc');
COMMIT;
```

+ From the following Log 5 and Log 6, you can see that Row Changed Events on the same table might be sent to different partitions based on the primary key, but changes to the same row are sent to the same partition so that the downstream can easily process the Event concurrently.
+ From Log 6, multiple changes to the same row in a transaction are only sent in one Row Changed Event.
+ Log 8 is a repeated event of Log 7. Row Changed Event might be repeated, but the first Event of each version is sent orderly.

```
5. [partition=0] [key="{\"ts\":415508878783938562,\"scm\":\"test\",\"tbl\":\"t1\",\"t\":1}"] [value="{\"u\":{\"id\":{\"t\":3,\"h\":true,\"v\":1},\"val\":{\"t\":15,\"v\":\"YWE=\"}}}"]
6. [partition=1] [key="{\"ts\":415508878783938562,\"scm\":\"test\",\"tbl\":\"t1\",\"t\":1}"] [value="{\"u\":{\"id\":{\"t\":3,\"h\":true,\"v\":2},\"val\":{\"t\":15,\"v\":\"YmI=\"}}}"]
7. [partition=0] [key="{\"ts\":415508878783938562,\"scm\":\"test\",\"tbl\":\"t1\",\"t\":1}"] [value="{\"u\":{\"id\":{\"t\":3,\"h\":true,\"v\":3},\"val\":{\"t\":15,\"v\":\"Y2M=\"}}}"]
8. [partition=0] [key="{\"ts\":415508878783938562,\"scm\":\"test\",\"tbl\":\"t1\",\"t\":1}"] [value="{\"u\":{\"id\":{\"t\":3,\"h\":true,\"v\":3},\"val\":{\"t\":15,\"v\":\"Y2M=\"}}}"]
```

Execute the following SQL statements in the upstream:

{{< copyable "sql" >}}

```sql
BEGIN;
DELETE FROM test.t1 WHERE id = 1;
UPDATE test.t1 SET val = 'dd' WHERE id = 3;
UPDATE test.t1 SET id = 4, val = 'ee' WHERE id = 2;
COMMIT;
```

+ Log 9 is the Row Changed Event of the `Delete` type. This type of Event only contains primary key columns or unique index columns.
+ Log 13 and Log 14 are Resolved Events. The Resolved Event means that in this Partition, any events smaller than the Resolved TS (including Row Changed Event and DDL Event) have been sent.

```
9. [partition=0] [key="{\"ts\":415508881418485761,\"scm\":\"test\",\"tbl\":\"t1\",\"t\":1}"] [value="{\"d\":{\"id\":{\"t\":3,\"h\":true,\"v\":1}}}"]
10. [partition=1] [key="{\"ts\":415508881418485761,\"scm\":\"test\",\"tbl\":\"t1\",\"t\":1}"] [value="{\"d\":{\"id\":{\"t\":3,\"h\":true,\"v\":2}}}"]
11. [partition=0] [key="{\"ts\":415508881418485761,\"scm\":\"test\",\"tbl\":\"t1\",\"t\":1}"] [value="{\"u\":{\"id\":{\"t\":3,\"h\":true,\"v\":3},\"val\":{\"t\":15,\"v\":\"ZGQ=\"}}}"]
12. [partition=0] [key="{\"ts\":415508881418485761,\"scm\":\"test\",\"tbl\":\"t1\",\"t\":1}"] [value="{\"u\":{\"id\":{\"t\":3,\"h\":true,\"v\":4},\"val\":{\"t\":15,\"v\":\"ZWU=\"}}}"]
13. [partition=0] [key="{\"ts\":415508881038376963,\"t\":3}"] [value=]
14. [partition=1] [key="{\"ts\":415508881038376963,\"t\":3}"] [value=]
```

## Protocol parsing for consumers

Currently, TiCDC does not provide the standard parsing library for TiCDC Open Protocol, but the Golang version and Java version of parsing demonstrations are provided. You can refer to the data format provided in this document and the following demonstrations to implement the protocol parsing for consumers.

- [Golang demo](https://github.com/pingcap/ticdc/tree/master/kafka_consumer)
- [Java demo](https://github.com/pingcap/ticdc/tree/master/demo/java)

## Column type code

`Column Type Code` represents the column data type of the Row Changed Event.

| Type                   | Code | Output Example | Description |
| :-------------------- | :--- | :------ | :-- |
| TINYINT/BOOLEAN          | 1    | {"t":1,"v":1} | |
| SMALLINT              | 2    | {"t":2,"v":1} | |
| INT                   | 3    | {"t":3,"v":123} | |
| FLOAT                 | 4    | {"t":4,"v":153.123} | |
| DOUBLE                | 5    | {"t":5,"v":153.123} | |
| NULL                  | 6    | {"t":6,"v":null} | |
| TIMESTAMP             | 7    | {"t":7,"v":"1973-12-30 15:30:00"} | |
| BIGINT                | 8    | {"t":8,"v":123} | |
| MEDIUMINT             | 9    | {"t":9,"v":123} | |
| DATE                  | 10/14   | {"t":10,"v":"2000-01-01"} | |
| TIME                  | 11   | {"t":11,"v":"23:59:59"} | |
| DATETIME              | 12   | {"t":12,"v":"2015-12-20 23:58:58"} | |
| YEAR                  | 13   | {"t":13,"v":1970} | |
| VARCHAR/VARBINARY     | 15/253   | {"t":15,"v":"test"} / {"t":15,"v":"\\\\x89PNG\\\\r\\\\n\\\\x1a\\\\n"} |  The value is encoded in UTF-8. When the upstream type is VARBINARY, invisible characters are escaped. |
| BIT                   | 16   | {"t":16,"v":81} | |
| JSON                  | 245  | {"t":245,"v":"{\\"key1\\": \\"value1\\"}"} | |
| DECIMAL               | 246  | {"t":246,"v":"129012.1230000"} | |
| ENUM                  | 247  | {"t":247,"v":1} | |
| SET                   | 248  | {"t":248,"v":3} | |
| TINYTEXT/TINYBLOB     | 249  | {"t":249,"v":"5rWL6K+VdGV4dA=="} | The value is encoded in Base64. |
| MEDIUMTEXT/MEDIUMBLOB | 250  | {"t":250,"v":"5rWL6K+VdGV4dA=="} | The value is encoded in Base64. |
| LONGTEXT/LONGBLOB     | 251  | {"t":251,"v":"5rWL6K+VdGV4dA=="} | The value is encoded in Base64. |
| TEXT/BLOB             | 252  | {"t":252,"v":"5rWL6K+VdGV4dA=="} | The value is encoded in Base64. |
| CHAR/BINARY           | 254  | {"t":254,"v":"test"} / {"t":254,"v":"\\\\x89PNG\\\\r\\\\n\\\\x1a\\\\n"} | The value is encoded in UTF-8. When the upstream type is BINARY, invisible characters are escaped. |
| GEOMETRY              | 255  |  | Unsupported |

## DDL Type Code

`DDL Type Code` represents the DDL statement type of the DDL Event.

| Type                              | Code |
| :-------------------------------- | :- |
| Create Schema                     | 1  |
| Drop Schema                       | 2  |
| Create Table                      | 3  |
| Drop Table                        | 4  |
| Add Column                        | 5  |
| Drop Column                       | 6  |
| Add Index                         | 7  |
| Drop Index                        | 8  |
| Add Foreign Key                   | 9  |
| Drop Foreign Key                  | 10 |
| Truncate Table                    | 11 |
| Modify Column                     | 12 |
| Rebase Auto ID                    | 13 |
| Rename Table                      | 14 |
| Set Default Value                 | 15 |
| Shard RowID                       | 16 |
| Modify Table Comment              | 17 |
| Rename Index                      | 18 |
| Add Table Partition               | 19 |
| Drop Table Partition              | 20 |
| Create View                       | 21 |
| Modify Table Charset And Collate  | 22 |
| Truncate Table Partition          | 23 |
| Drop View                         | 24 |
| Recover Table                     | 25 |
| Modify Schema Charset And Collate | 26 |
| Lock Table                        | 27 |
| Unlock Table                      | 28 |
| Repair Table                      | 29 |
| Set TiFlash Replica               | 30 |
| Update TiFlash Replica Status     | 31 |
| Add Primary Key                   | 32 |
| Drop Primary Key                  | 33 |
| Create Sequence                   | 34 |
| Alter Sequence                    | 35 |
| Drop Sequence                     | 36 |

## Bit flags of columns

The bit flags represent specific attributes of columns.

| Bit | Value | Name | Description |
| :-- | :- | :- | :- |
| 1   | 0x01 | BinaryFlag          | Whether the column is a binary-encoded column. |
| 2   | 0x02 | HandleKeyFlag       | Whether the column is a Handle index column. |
| 3   | 0x04 | GeneratedColumnFlag | Whether the column is a generated column.     |
| 4   | 0x08 | PrimaryKeyFlag      | Whether the column is a primary key column.      |
| 5   | 0x10 | UniqueKeyFlag       | Whether the column is a unique index column.  |
| 6   | 0x20 | MultipleKeyFlag     | Whether the column is a composite index column.   |
| 7   | 0x40 | NullableFlag        | Whether the column is a nullable column.       |
| 8   | 0x80 | UnsignedFlag        | Whether the column is an unsigned column.     |

Example:

If the value of a column flag is `85`, the column is a nullable column, a unique index column, a generated column, and a binary-encoded column.

```
85 == 0b_101_0101
   == NullableFlag | UniqueKeyFlag | GeneratedColumnFlag | BinaryFlag
```

If the value of a column is `46`, the column is a composite index column, a primary key column, a generated column, and a Handle key column.

```
46 == 0b_010_1110
   == MultipleKeyFlag | PrimaryKeyFlag | GeneratedColumnFlag | HandleKeyFlag
```

> **Note:**
>
> + `BinaryFlag` is meaningful only when the column type is BLOB/TEXT (including TINYBLOB/TINYTEXT and BINARY/CHAR). When the upstream column is the BLOB type, the `BinaryFlag` value is set to `1`. When the upstream column is the TEXT type, the `BinaryFlag` value is set to `0`.
> + To replicate a table from the upstream, TiCDC selects a [valid index](/ticdc/ticdc-overview.md#restrictions) as the Handle index. The `HandleKeyFlag` value of the Handle index column is set to `1`.
