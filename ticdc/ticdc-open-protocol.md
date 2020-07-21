---
title: TiCDC Open Protocol
aliases: ['/docs/dev/ticdc/ticdc-open-protocol/','/docs/dev/reference/tools/ticdc/open-protocol/']
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

    ```
    {
        <UpdateOrDelete>:{
            <Column Name>:{
                "t":<Column Type>,
                "h":<Where Handle>,
                "v":<Column Value>
            },
            <Column Name>:{
                "t":<Column Type>,
                "h":<Where Handle>,
                "v":<Column Value>
            }
        }
    }
    ```

    | Parameter         | Type   | Description                    |
    | :---------- | :----- | :--------------------- |
    | UpdateOrDelete | String |  Identifies whether the row is updated or deleted in the Event. The optional values are `u` or `d`. |
    | Column Name    | String |  The column name.  |
    | Column Type    | Number |  The column type. For details, see [Column Type Code](#column-type-code).  |
    | Where Handle   | Bool   |  Determines whether this column can be the filter condition of the `Where` clause. When this column is unique on the table, `Where Handle` is `true`. |
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

## Column and DDL type codes

The column and DDL type codes are encodings defined by TiCDC Open Protocol. `Column Type Code` represents the column data type of the Row Changed Event, and `DDL Type Code` represents the DDL statement type of the DDL Event.

### Column Type Code

| Type        | Code | Output Example | Note |
| :---------- | :--- | :------ | :-- |
| Decimal     | 0    | {"t":0,"v":"129012.1230000"} | |
| Tiny/Bool   | 1    | {"t":1,"v":1} | |
| Short       | 2    | {"t":2,"v":1} | |
| Long        | 3    | {"t":3,"v":123} | |
| Float       | 4    | {"t":4,"v":153.123} | |
| Double      | 5    | {"t":5,"v":153.123} | |
| Null        | 6    | {"t":6,"v":null} | |
| Timestamp   | 7    | {"t":7,"v":"1973-12-30 15:30:00"} | |
| Longlong    | 8    | {"t":8,"v":123} | |
| Int24       | 9    | {"t":9,"v":123} | |
| Date        | 10   | {"t":10,"v":"2000-01-01"} | |
| Duration    | 11   | {"t":11,"v":"23:59:59"} | |
| Datetime    | 12   | {"t":12,"v":"2015-12-20 23:58:58"} | |
| Year        | 13   | {"t":13,"v":1970} | |
| New Date    | 14   | {"t":14,"v":"2000-01-01"} | |
| Varchar     | 15   | {"t":15,"v":"test"} | The value is encoded in UTF-8. |
| Bit         | 16   | {"t":16,"v":81} | |
| JSON        | 245  | {"t":245,"v":"{\\"key1\\": \\"value1\\"}"} | |
| New Decimal | 246  | {"t":246,"v":"129012.1230000"} | |
| Enum        | 247  | {"t":247,"v":1} | |
| Set         | 248  | {"t":248,"v":3} | |
| Tiny Blob   | 249  | {"t":249,"v":"5rWL6K+VdGV4dA=="} | The value is encoded in Base64. |
| Medium Blob | 250  | {"t":250,"v":"5rWL6K+VdGV4dA=="} | The value is encoded in Base64. |
| Long Blob   | 251  | {"t":251,"v":"5rWL6K+VdGV4dA=="} | The value is encoded in Base64. |
| Blob        | 252  | {"t":252,"v":"5rWL6K+VdGV4dA=="} | The value is encoded in Base64. |
| Var String  | 253  | {"t":253,"v":"test"} | The value is encoded in UTF-8. |
| String      | 254  | {"t":254,"v":"test"} | The value is encoded in UTF-8. |
| Geometry    | 255  |  | Unsupported type. |

### DDL Type Code

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
