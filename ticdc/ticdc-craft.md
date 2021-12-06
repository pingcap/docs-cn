---
title: TiCDC Craft
aliases: ['/docs/dev/ticdc/ticdc-craft/','/docs/dev/reference/tools/ticdc/craft/']
---

# TiCDC Craft

## 概述

TiCDC Craft 是一种行级别的数据变更通知协议，为监控、缓存、全文索引、分析引擎、异构数据库的主从复制等提供数据源。TiCDC 使用 TiCDC Craft，将 TiDB 的数据变化复制到第三方数据媒介，如 MQ（消息队列）。与基于 JSON 的开放协议相比，craft 是一个二进制协议，因此更加紧凑，编码和解码时使用的资源更少。具有高写入量的大型 TiDB 集群事件变更日志也是海量的，此时协议的高性能远比可读性重要。

TiCDC Craft 以 Event 为基本单位向下游复制数据变更事件，Event 分为三类：

* [Row Changed Event](#row-changed-event): 代表一行的数据变化，在行发生变更时该 Event 被发出，包含变更后该行的相关信息。

* [DDL Event](#ddl-event): 代表代表 DDL 变更，在上游成功执行 DDL 后发出，DDL Event 会广播到每一个 MQ Partition 中。
* [Resolved Event](#resolved-event): 代表一个特殊的时间点，表示在这个时间点前的收到的 Event 是完整的。

> **警告：**
>
> + 当前该功能为实验特性，请勿在生产环境中使用。

## 协议约束

* 在绝大多数情况下，一个版本的 Row Changed Event 只会发出一次，但是特殊情况（节点故障、网络分区等）下，同一版本的 Row Changed Event 可能会多次发送。
* 同一张表中的每一个版本第一次发出的 Row Changed Event 在 Event 流中一定是按 TS (timestamp) 顺序递增的。
* Resolved Event 会被周期性的广播到各个 MQ Partition，Resolved Event 意味着任何 TS 小于 Resolved Event TS 的 Event 已经发送给下游。
* DDL Event 将被广播到各个 MQ Partition。
* 一行数据的多个 Row Changed Event 一定会被发送到同一个 MQ Partition 中。

## Benchmark

* 对同一事件，二进制协议编码所占用的字节数更少。
* Protobuf 作为一种被广泛使用的二进制格式，可以用来代替 craft。 因为 craft 格式可以应用复杂的优化，所以它可以比 protobuf 更紧凑。

压缩率对比:

| case | craft size | json size | protobuf 1 size | protobuf 2 size | craft compressed | json compressed | protobuf 1 compressed | protobuf 2 compressed |
| :---- | :--------- | :-------- | :-------------- | :-------------- | :--------------- | :-------------- | :-------------------- | :-------------------- |
| case 0 | 300 | 708 (136%)+ | 382 (27%)+ | 375 (25%)+ | 168 | 223 (32%)+ | 198 (17%)+ | 181 (7%)+ |
| case 1 | 993 | 2816 (183%)+ | 1528 (53%)+ | 1482 (49%)+ | 209 | 286 (36%)+ | 235 (12%)+ | 221 (5%)+ |

编码速度对比:

| craft | json | protobuf 1 | protobuf 2 |
| :---- | :--- | :--------- | :--------- |
| 4809 ns/op | 28388 ns/op (490%)+ | 3921 ns/op (19%)- | 3645 ns/op (25%)- |

解码速度对比:

| craft | json | protobuf 1 | protobuf 2 |
| :---- | :--- | :--------- | :--------- |
| 7944 ns/op | 75822 ns/op (854%)+ | 8020 ns/op (1%)+ | 8462 ns/op (6%)+ |

## Message 格式定义

Primitive types:

| type | encoding |
| :--- | :------- |
| uvarint | uvarint 中除了最后一个字节外，每个字节都设置了最高有效位（msb）— 表示是否还有更多的字节。每个字节的低 7 位用于存储以 7 位为一组数字的二进制补码表示，最低有效组优先。 |
| little endian uvarint | uvarint 中除了最后一个字节外，每个字节都设置了最高有效位（msb）— 表示是否还有更多的字节。每个字节的低 7 位用于存储以 7 位为一组数字的二进制补码表示，最高有效组优先。 |
| varint | 使用ZigZag编码将有符号整数映射到无符号整数，这样数字的绝对编码值也会变小。 |
| float64 | 固定64位的数据块以小端字节序存储。 |
| string/bytes | uvarint 编码的长度，后面是特定字节数的数据。 |
| nullable string/bytes | varint 编码的长度，后面是具体的数据字节数。长度为-1时，表示空字符串或字节数组。 |

Chunk of primitive types:

| chunk type | encoding |
| :--------- | :------- |
| uvarint chunk | 以 uvarint 格式编码的连续元素。 |
| varint chunk | 以 varint 格式编码的连续元素。 |
| delta uvarint chunk | 以 uvarint 格式编码的基数，后面是以 uvarint 格式编码的每个元素与前一个元素的差值。 |
| delta varint chunk | 以 varint 格式编码的基数，后面是以 uvarint 格式编码的每个元素与前一个元素的差值。 |
| float64 chunk | 以 float64 格式编码的连续元素。 |
| string/bytes chunk | 以 uvarint 格式编码的所有字符串/字节的连续长度，后面是每个元素的字节数。 |
| nullable string/bytes chunk | 以 uvarint 格式编码的所有字符串/字节的连续长度，后面是每个元素的字节。长度为 -1 时表示空字符串或字节数组。 |

一个 Message 中包含一个或多个 Event，按照以下格式排列：

Message:

| uvarint | header | body | term dictionary | size tables |
| :------ | :------ | :------ | :------ | ------- |
| version | events header | events body | term dictionary | size tables |

Header:

| delta uvarint chunk | uvarint chunk | delta varint chunk | delta varint chunk | delta varint chunk |
| :------ | :------ | :------ | :------ | :------ |
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

* 当前协议的版本号为 `1`。

## Event 格式定义

本部分介绍 Row Changed Event、DDL Event 和 Resolved Event 的格式定义。

### Row Changed Event

+ **Header:**

    | Data | Type | Description |
    | :-------- | :--- | :---------- |
    | Commit TS | uint64 | 导致行变化的事务的时间戳。 |
    | Type | uint64 | 事件类型. 0x1: Row Changed, 0x2: DDL, 0x3: Resolved. |
    | Partition ID | uint64 | 分区 ID（当物理表不是分区表的一部分时，ID 为 -1）。 |
    | Schema | string | 该行所在的库名。 |
    | Table | String | 该行所在的表名。 |

+ **Event:**

    `Insert` event. 新添加的数据将会被输出。

    | Column group(s) |
    | :-------------- |
    | New values |

    `Update` event. 新添加的行和更新前的行会被输出。旧值只有在启用旧值功能时才可用。

    | Column group(s) |
    | :-------------- |
    | New values |
    | Old values |

    `Delete` event. 被删除的行会被输出. 当旧值功能被启用时,  `Delete` event 包含被删除的所有列; 当旧值功能被禁用时, `Delete` event 仅仅包含 [HandleKey](#bit-flags-of-columns) .
    
    | Column group(s) |
    | :-------------- |
    | Deleted values |
    
    Column :
    
    | Data | Type | Description |
    | :--- | :--- | :---------- |
    | Name | string | 列名。 |
    | Type | uint64 | 列类型，详见 [Column Type Code](#column-type-code). |
    | Flag (**experimental**) | numeric | 列标签，详见 [Bit flags of columns](#bit-flags-of-columns). |
    | Value | any | 列值，详见 [Binary encoding for different column types](#column-type-code). |

+ **Example:**

```
    01 81 80 f0 81 81 b5 de  f1 05 01 01 00 02 01 08  |................|
    04 02 02 02 02 02 02 02  0f fe 01 0a 07 0c 04 03  |................|
    06 00 00 00 00 00 00 00  00 10 0e 14 26 26 10 04  |............&&..|
    01 76 61 72 63 68 61 72  31 73 74 72 69 6e 67 31  |.varchar1string1|
    32 30 32 31 2f 30 31 2f  30 32 32 30 32 31 2f 30  |2021/01/022021/0|
    31 2f 30 32 20 30 30 3a  30 30 3a 30 30 32 30 32  |1/02 00:00:00202|
    31 2f 30 31 2f 30 32 20  30 30 3a 30 30 3a 30 30  |1/01/02 00:00:00|
    00 00 00 00 00 00 00 40  a0 1f 02 08 04 02 02 02  |.......@........|
    02 02 02 02 0f fe 01 0a  07 0c 04 03 06 00 00 00  |................|
    00 00 00 00 00 10 0e 14  26 26 10 04 01 76 61 72  |........&&...var|
    63 68 61 72 30 73 74 72  69 6e 67 30 32 30 32 31  |char0string02021|
    2f 30 31 2f 30 31 32 30  32 31 2f 30 31 2f 30 31  |/01/012021/01/01|
    20 30 30 3a 30 30 3a 30  30 32 30 32 31 2f 30 31  | 00:00:002021/01|
    2f 30 31 20 30 30 3a 30  30 3a 30 30 00 00 00 00  |/01 00:00:00....|
    00 00 f0 3f d0 0f 0a 01  01 07 06 04 09 08 05 04  |...?............|
    04 61 62 76 61 72 63 68  61 72 73 74 72 69 6e 67  |.abvarcharstring|
    64 61 74 65 74 69 6d 65  73 74 61 6d 70 64 61 74  |datetimestampdat|
    65 74 69 6d 65 66 6c 6f  61 74 6c 6f 6e 67 6e 75  |etimefloatlongnu|
    6c 6c 02 1a 5e 01 b0 03  02 d8 01 00 0a           |ll..^........|
```

### DDL Event

+ **Header:**

    | Data | Type   | Description                         |
    | :--- | :----- | :---------------------------------- |
    | Commit TS | uint64 | 执行DDL变更的事务的时间戳。 |
    | Schema | string | DDL 变更影响的库名，可能为空字符串。 |
    | Table | string | DDL 变更影响的表名，可能为空字符串。 |

+ **Event:**

    | Data | Type   | Description   |
    | :--- | :----- | :------------ |
    | Type | uint64 | DDL 类型，详见 [DDL Type Code](#ddl-type-code). |
    | Query | string | DDL Query SQL |

+ **Example:**

```
    01 81 80 c0 dc f5 b5 de  f1 05 02 01 00 02 01 0e  |................|
    63 72 65 61 74 65 20 74  61 62 6c 65 20 61 02 01  |create table a..|
    01 61 62 02 1a 0f 01 20  05                       |.ab.... .|
```

### Resolved Event

+ **Header:**

    | Data | Type | Description |
    | :--- | :--- | :---------- |
    | TS | uint64 | Resolved Event 的时间戳。任何 TS 比此 TS 早的事件都已发送。 |

+ **Event:** None

+ **Example:**

```
    01 81 80 e0 bb 9b b6 de  f1 05 03 01 01 01 02 1a  |................|
    19 01 00 05                                       |....|
```

## 事件流输出日志示例

本节展示事件流的输出日志。由于 craft 协议是二进制的，因此不具备可读性，我们将使用开放协议来演示发生的事情，相应的 craft 事件流被转化为具备可读性的 json.

假设在上游执行以下 SQL 语句，MQ Partition 数量为 2：

{{< copyable "sql" >}}

```sql
CREATE TABLE test.t1(id int primary key, val varchar(16));
```

如以下执行日志中的 Log 1、Log 3 所示，DDL Event 将被广播到所有 MQ Partition，Resolved Event 会被周期性地广播到各个 MQ Partition：

```
1. [partition=0] [key="{\"ts\":415508856908021766,\"scm\":\"test\",\"tbl\":\"t1\",\"t\":2}"] [value="{\"q\":\"CREATE TABLE test.t1(id int primary key, val varchar(16))\",\"t\":3}"]
2. [partition=0] [key="{\"ts\":415508856908021766,\"t\":3}"] [value=]
3. [partition=1] [key="{\"ts\":415508856908021766,\"scm\":\"test\",\"tbl\":\"t1\",\"t\":2}"] [value="{\"q\":\"CREATE TABLE test.t1(id int primary key, val varchar(16))\",\"t\":3}"]
4. [partition=1] [key="{\"ts\":415508856908021766,\"t\":3}"] [value=]
```

在上游执行以下 SQL 语句：

{{< copyable "sql" >}}

```sql
BEGIN;
INSERT INTO test.t1(id, val) VALUES (1, 'aa');
INSERT INTO test.t1(id, val) VALUES (2, 'aa');
UPDATE test.t1 SET val = 'bb' WHERE id = 2;
INSERT INTO test.t1(id, val) VALUES (3, 'cc');
COMMIT;
```

+ 如以下执行日志中的 Log 5 和 Log 6 所示，同一张表内的 Row Changed Event 可能会根据主键被分派到不同的 Partition，但同一行的变更一定会分派到同一个 Partition，方便下游并发处理。
+ 如 Log 6 所示，在一个事务内对同一行进行多次修改，只会发出一个 Row Changed Event。
+ Log 8 是 Log 7 的重复 Event。Row Changed Event 可能重复，但每个版本的 Event 第一次发出的次序一定是有序的。

```
5. [partition=0] [key="{\"ts\":415508878783938562,\"scm\":\"test\",\"tbl\":\"t1\",\"t\":1}"] [value="{\"u\":{\"id\":{\"t\":3,\"h\":true,\"v\":1},\"val\":{\"t\":15,\"v\":\"YWE=\"}}}"]
6. [partition=1] [key="{\"ts\":415508878783938562,\"scm\":\"test\",\"tbl\":\"t1\",\"t\":1}"] [value="{\"u\":{\"id\":{\"t\":3,\"h\":true,\"v\":2},\"val\":{\"t\":15,\"v\":\"YmI=\"}}}"]
7. [partition=0] [key="{\"ts\":415508878783938562,\"scm\":\"test\",\"tbl\":\"t1\",\"t\":1}"] [value="{\"u\":{\"id\":{\"t\":3,\"h\":true,\"v\":3},\"val\":{\"t\":15,\"v\":\"Y2M=\"}}}"]
8. [partition=0] [key="{\"ts\":415508878783938562,\"scm\":\"test\",\"tbl\":\"t1\",\"t\":1}"] [value="{\"u\":{\"id\":{\"t\":3,\"h\":true,\"v\":3},\"val\":{\"t\":15,\"v\":\"Y2M=\"}}}"]
```

在上游执行以下 SQL 语句：

{{< copyable "sql" >}}

```sql
BEGIN;
DELETE FROM test.t1 WHERE id = 1;
UPDATE test.t1 SET val = 'dd' WHERE id = 3;
UPDATE test.t1 SET id = 4, val = 'ee' WHERE id = 2;
COMMIT;
```

+ Log 9 是 `Delete` 类型的 Row Changed Event，这种类型的 Event 只包含主键列或唯一索引列。
+ Log 13 和 Log 14 是 Resolved Event。Resolved Event 意味着在这个 Partition 中，任意小于 Resolved TS 的 Event（包括 Row Changed Event 和 DDL Event）已经发送完毕。

```
9. [partition=0] [key="{\"ts\":415508881418485761,\"scm\":\"test\",\"tbl\":\"t1\",\"t\":1}"] [value="{\"d\":{\"id\":{\"t\":3,\"h\":true,\"v\":1}}}"]
10. [partition=1] [key="{\"ts\":415508881418485761,\"scm\":\"test\",\"tbl\":\"t1\",\"t\":1}"] [value="{\"d\":{\"id\":{\"t\":3,\"h\":true,\"v\":2}}}"]
11. [partition=0] [key="{\"ts\":415508881418485761,\"scm\":\"test\",\"tbl\":\"t1\",\"t\":1}"] [value="{\"u\":{\"id\":{\"t\":3,\"h\":true,\"v\":3},\"val\":{\"t\":15,\"v\":\"ZGQ=\"}}}"]
12. [partition=0] [key="{\"ts\":415508881418485761,\"scm\":\"test\",\"tbl\":\"t1\",\"t\":1}"] [value="{\"u\":{\"id\":{\"t\":3,\"h\":true,\"v\":4},\"val\":{\"t\":15,\"v\":\"ZWU=\"}}}"]
13. [partition=0] [key="{\"ts\":415508881038376963,\"t\":3}"] [value=]
14. [partition=1] [key="{\"ts\":415508881038376963,\"t\":3}"] [value=]
```

## 消费端协议解析

目前，TiCDC 提供了 Golang 和 Java 版本的 Craft 标准解析库，你可以参考本文件提供的数据格式和以下解码器来实现其他语言的协议解析器。

- [Golang](https://github.com/pingcap/ticdc/blob/master/cdc/sink/codec/craft.go)
- [Java](https://github.com/tidb-incubator/TiBigData/tree/master/ticdc)

## Column type code

`Column Type Code` 表示 Row Changed Event 中列的数据类型。

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

`DDL Type Code` 表示 DDL Event 中 DDL 的类型。

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

The bit flags 表示列的特殊属性。

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

例:

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

> **说明：**
>
> + BinaryFlag 仅在列为 BLOB/TEXT（包括 TINYBLOB/TINYTEXT、BINARY/CHAR 等）类型时才有意义。当上游列为 BLOB 类型时，BinaryFlag 置 `1`；当上游列为 TEXT 类型时，BinaryFlag 置 `0`。
> + 若要同步上游的一张表，TiCDC 会选择一个[有效索引](/ticdc/ticdc-overview.md#同步限制)作为 Handle Index。Handle Index 包含的列的 HandleKeyFlag 置 `1`。
> + [Protobuf definition for benchmark](https://github.com/pingcap/ticdc/blob/master/proto/CraftBenchmark.proto)
