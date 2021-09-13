---
title: TiCDC Craft
aliases: ['/docs/dev/ticdc/ticdc-craft/','/docs/dev/reference/tools/ticdc/craft/']
---

# TiCDC Craft

TiCDC Craft is a row-level data change notification protocol that provides data sources for monitoring, caching, full-text indexing, analysis engines, and primary-secondary replication between different databases. TiCDC complies with TiCDC Craft and replicates data changes of TiDB to third-party data medium such as MQ (Message Queue). Compared to JSON based Open Protocol, craft is a binary protocol therefore is more compact and use less resources to encode and decode. For large TiDB clusters which have high write throughput, performance is more important than human readability to support such high change events traffic.

TiCDC Craft uses Event as the basic unit to replicate data change events to the downstream. The Event is divided into three categories:

* [Row Changed Event](#row-changed-event): Represents the data change in a row. When a row is changed, this Event is sent and contains information about the changed row.
* [DDL Event](#ddl-event): Represents the DDL change. This Event is sent after a DDL statement is successfully executed in the upstream. The DDL Event is broadcasted to every MQ Partition.
* [Resolved Event](#resolved-event): Represents a special time point before which the Event received is complete.

## Restrictions

* In most cases, the Row Changed Event of a version is sent only once, but in special situations such as node failure and network partition, the Row Changed Event of the same version might be sent multiple times.
* On the same table, the Row Changed Events of each version which is first sent are incremented in the order of timestamps (TS) in the Event stream.
* Resolved Events are periodically broadcasted to each MQ Partition. The Resolved Event means that any Event with a TS earlier than Resolved Event TS has been sent to the downstream.
* DDL Events are broadcasted to each MQ Partition.
* Multiple Row Changed Events of a row are sent to the same MQ Partition.

## Benchmark

* Binary protocol encodes the same events with far less amount of bytes.
* Protobuf is a popular binary format that can be used instead of craft format. Since craft format can apply sophisticated optimizations, it can be more compact and faster than protobuf.

Serialized size:

| case | craft size | json size | protobuf 1 size | protobuf 2 size | craft compressed | json compressed | protobuf 1 compressed | protobuf 2 compressed |
| :---- | :--------- | :-------- | :-------------- | :-------------- | :--------------- | :-------------- | :-------------------- | :-------------------- |
| case 0 | 300 | 708 (136%)+ | 382 (27%)+ | 375 (25%)+ | 168 | 223 (32%)+ | 198 (17%)+ | 181 (7%)+ |
| case 1 | 993 | 2816 (183%)+ | 1528 (53%)+ | 1482 (49%)+ | 209 | 286 (36%)+ | 235 (12%)+ | 221 (5%)+ |

Encoding speed:

| craft | json | protobuf 1 | protobuf 2 |
| :---- | :--- | :--------- | :--------- |
| 4809 ns/op | 28388 ns/op (490%)+ | 3921 ns/op (19%)- | 3645 ns/op (25%)- |

Decoding speed:

| craft | json | protobuf 1 | protobuf 2 |
| :---- | :--- | :--------- | :--------- |
| 7944 ns/op | 75822 ns/op (854%)+ | 8020 ns/op (1%)+ | 8462 ns/op (6%) |

## Message format

A Message contains one or more Events, arranged in the following format:

Message:

| uvarint | header | body | term dictionary | size tables |
| :------ | :------ | :------ | :------ |
| version | events header | events body | term dictionary | size tables |

Header:

| delta uvarint chunk | uvarint chunk | delta varint chunk | delta varint chunk | delta varint chunk |
| :------ | :------ | :------ | :------ | :------ | :------ |
| commit ts | event type | partition id (-1 for no partition) | schema | table |

Body for [Row Changed Event](#row-changed-event):

| Column group | Column group |
| :------ | :------ |
| column group 1 | column group 2 (optional) |

Column group:
| 1 byte | uvarint | delta varint chunk | uvarint chunk | uvarint chunk | nullable bytes chunk |
| :------ | :------ | :------ | :------ | :------ | :------ |
| type: 1 New, 2 Old | number of columns | name | type | flag | value |

Body for [DDL Event](#ddl-event):

| uvarint | string |
| :------ | :------ |
| type | query |

Body for [Resolved Event](#resolved-event):

| empty |
| :---- |
| empty |

Term dictionary:

| uvarint | string chunk |
| :------ | :----------- |
| size | terms sorted by id |

Size tables:

| size table | size table | size table | ...... | size table | bytes of size tables |
| :--------- | :--------- | :--------- | :----- | :--------- | :------------------- |
| meta data size, including header size and term dictionary size | size of serialized events | size of serialized column groups 1 | ...... | size of serialized column groups N | uvarint in little byte order |

Size table:

| uvarint | delta varint chunk |
| :------ | :------------ |
| number of elements | Consecutive elements encoded in delta varint format |

Meta data size table:

| varint | varint |
| :------ | :------ |
| header size | term dictionary size |

Primitive types:

| type | encoding |
| :--- | :------- |
| uvarint | Each byte in a uvarint, except the last byte, has the most significant bit (msb) set – this indicates that there are further bytes to come. The lower 7 bits of each byte are used to store the two's complement representation of the number in groups of 7 bits, least significant group first |
| little endian uvarint | Each byte in a uvarint, except the last byte, has the most significant bit (msb) set – this indicates that there are further bytes to come. The lower 7 bits of each byte are used to store the two's complement representation of the number in groups of 7 bits, most significant group first |
| varint | Use ZigZag encoding to map signed integers to unsigned integers so that the numbers with a small absolute encoded value too. |
| float64 | Fixed 64 bits lump of data stored in little-endian byte order |
| string/bytes | Uvarint encoded length followed by a specific number of bytes of data |
| nullable string/bytes | Varint encoded length followed by a specific number of bytes of data. Length of -1 is used to indicate null string/bytes |

Chunk of primitive types:

| chunk type | encoding |
| :--------- | :------- |
| uvarint chunk | Consecutive elements encoded in uvarint format |
| varint chunk | Consecutive elements encoded in varint format |
| delta uvarint chunk | Base number encoded in uvarint format followed by delta of each element to last element encoded in uvarint format |
| delta varint chunk | Base number encoded in varint format followed by delta of each element to last element encoded in varint format |
| float64 chunk | Consecutive elements encoded in float64 format |
| string/bytes chunk | Consecutive length of all string/bytes encoded in uvarint format followed by bytes of each elements |
| nullable string/bytes chunk | Consecutive length of all string/bytes encoded in uvarint format followed by bytes of each elements. Length of -1 is used to indicate null string/bytes |

* The version of the current protocol is `1`.

## Event format

This section introduces the formats of Row Changed Event, DDL Event, and Resolved Event.

### Row Changed Event

+ **Header:**

    | Data | Type | Description |
    | :-------- | :--- | :---------- |
    | Commit TS | uint64 | The timestamp of transaction that causes the row change.  |
    | Type | uint64 | Type of the event. 0x1: Row Changed, 0x2: DDL, 0x3: Resolved |
    | Partition ID | uint64 | Partition ID (It is -1 when the physical table is not part of partitioned table)|
    | Schema | string |  The name of the schema where the row is in. |
    | Table | String |  The name of the table where the row is in. |

+ **Event:**

    `Insert` event. The newly added row data is output.

    | Column group(s) |
    | :-------------- |
    | New values |

    `Update` event. The newly added row data and the row data before the update are output. Old values are only available when the old value feature is enabled.

    | Column group(s) |
    | :-------------- |
    | New values |
    | Old values |

    `Delete` event. The deleted row data is output. When the old value feature is enabled, the `Delete` event includes all the columns of the deleted row data; when this feature is disabled, the `Delete` event only includes the [HandleKey](#bit-flags-of-columns) column.
    | Column group(s) |
    | :-------------- |
    | Deleted values |

    Column :

    | Data | Type | Description |
    | :--- | :--- | :---------- |
    | Name | string | The column name. |
    | Type | uint64 | The column type. For details, see [Column Type Code](#column-type-code). |
    | Flag (**experimental**) | numeric | The bit flags of columns. For details, see [Bit flags of columns](#bit-flags-of-columns). |
    | Value | any | The Column value. For details, see [Binary encoding for different column types](#column-type-code). |

### DDL Event

+ **Header:**

    | Data | Type   | Description                         |
    | :--- | :----- | :---------------------------------- |
    | Commit TS | uint64 | The timestamp of the transaction that performs the DDL change. |
    | Schema | string | The schema name of the DDL change, which might be an empty string. |
    | Table | string | The table name of the DDL change, which might be am empty string. |

+ **Event:**

    | Data | Type   | Description   |
    | :--- | :----- | :------------ |
    | Type | uint64 | The DDL type. For details, see [DDL Type Code](#ddl-type-code).    |
    | Query | string | DDL Query SQL |

### Resolved Event

+ **Header:**

    | Data | Type | Description |
    | :--- | :--- | :---------- |
    | TS | uint64 | The Resolved timestamp. Any TS earlier than this Event has been sent. |

+ **Event:** None

## Examples of the Event stream output

This section shows and displays the output logs of the Event stream. Since craft protocol is binary hence not human readable, we are going to use Open Protocol to demonstrate what will happen and the corresponding craft event stream is equivalent to the human readable json counterpart.

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

Currently, TiCDC does not provide the standard parsing library for TiCDC Craft, but the Golang version and Java version of parsers are provided. You can refer to the data format provided in this document and the following decoders to implement the protocol parsers for other languages.

- [Golang demo](https://github.com/pingcap/ticdc/tree/master/kafka_consumer)
- [Java demo](https://github.com/pingcap/ticdc/tree/master/demo/java)

## Column type code

`Column Type Code` represents the column data type of the Row Changed Event.

| Type                  | Code  | Encoding Format | Note |
| :-------------------- | :---- | :-------------- | :--- |
| TINYINT/BOOLEAN       | 1     | uvarint for unsigned / varint for signed | |
| SMALLINT              | 2     | uvarint for unsigned / varint for signed | |
| INT                   | 3     | uvarint for unsigned / varint for signed | |
| FLOAT                 | 4     | float64 | |
| DOUBLE                | 5     | float64 | |
| NULL                  | 6     | null bytes | |
| TIMESTAMP             | 7     | string | Example: 1973-12-30 15:30:00 |
| BIGINT                | 8     | uvarint for unsigned / varint for signed | |
| MEDIUMINT             | 9     | uvarint for unsigned / varint for signed | |
| DATE                  | 10/14 | string | Example: 2000-01-01 |
| TIME                  | 11    | string | Example: 23:59:59 |
| DATETIME              | 12    | string | 2015-12-20 23:58:58 |
| YEAR                  | 13    | uvarint for unsigned / varint for signed | |
| VARCHAR/VARBINARY     | 15/253| string | The value is encoded in UTF-8. |
| BIT                   | 16    | uvarint | |
| JSON                  | 245   | string | Example: {"key1": "value1"} |
| DECIMAL               | 246   | string | Example: 129012.1230000 |
| ENUM                  | 247   | uvarint | |
| SET                   | 248   | uvarint | |
| TINYTEXT/TINYBLOB     | 249   | bytes | |
| MEDIUMTEXT/MEDIUMBLOB | 250   | bytes | |
| LONGTEXT/LONGBLOB     | 251   | bytes | |
| TEXT/BLOB             | 252   | bytes | |
| CHAR/BINARY           | 254   | string | The value is encoded in UTF-8. |
| GEOMETRY              | 255   | null bytes | Unsupported |

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
| :-- | :---- | :--- | :---------- |
| 1   | 0x01 | BinaryFlag          | Whether the column is a binary-encoded column. |
| 2   | 0x02 | HandleKeyFlag       | Whether the column is a Handle index column. |
| 3   | 0x04 | GeneratedColumnFlag | Whether the column is a generated column. |
| 4   | 0x08 | PrimaryKeyFlag      | Whether the column is a primary key column. |
| 5   | 0x10 | UniqueKeyFlag       | Whether the column is a unique index column. |
| 6   | 0x20 | MultipleKeyFlag     | Whether the column is a composite index column. |
| 7   | 0x40 | NullableFlag        | Whether the column is a nullable column. |
| 8   | 0x80 | UnsignedFlag        | Whether the column is an unsigned column. |

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
> + This feature is still experimental. Do **NOT** use it in the production environment.
> + `BinaryFlag` is meaningful only when the column type is BLOB/TEXT (including TINYBLOB/TINYTEXT and BINARY/CHAR). When the upstream column is the BLOB type, the `BinaryFlag` value is set to `1`. When the upstream column is the TEXT type, the `BinaryFlag` value is set to `0`.
> + To replicate a table from the upstream, TiCDC selects a [valid index](/ticdc/ticdc-overview.md#restrictions) as the Handle index. The `HandleKeyFlag` value of the Handle index column is set to `1`.
> + [Protobuf definition for benchmark](https://github.com/sunxiaoguang/ticdc/blob/craft/proto/CraftBenchmark.proto)
