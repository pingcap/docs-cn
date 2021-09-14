---
title: TiCDC Craft
aliases: ['/docs/dev/ticdc/ticdc-craft/','/docs/dev/reference/tools/ticdc/craft/']
---

# TiCDC Craft

TiCDC Craft 是一个行级的数据变更通知协议，为数据源提供了监控、缓存、全文索引、分析引擎和不同数据库之间的主次复制的能力。TiCDC 使用 TiCDC Craft，将 TiDB 的数据变化复制到第三方数据媒介，如MQ（消息队列）。与基于 JSON 的开放协议相比，craft 是一个二进制协议，因此更加紧凑，编码和解码时使用的资源更少。具有高写入量的大型 TiDB 集群事件变更日志也是海量的，此时协议的高性能远比可读性重要。

TiCDC Craft使用Event作为基本单元，将数据变更事件复制到下游。事件被分为以下三类：

* [Row Changed Event](#row-changed-event): 代表行数据变更。当某一行被改变时，包含行变更信息的事件将会被发送出去.
* [DDL Event](#ddl-event): 代表DDL变更。在上游成功执行 DDL 语句后此事件会被发送。DDL 事件会被广播到消息队列的每个分区。
* [Resolved Event](#resolved-event): 代表一个特殊的时间点，标志在这个时间点之前收到的事件都已被完成。

## Restrictions

* 在大多数情况下，同一版本的 Row Changed Event 只会发送一次，但在特殊情况下，如节点故障和网络分区，某一版本的 Row Chanhed Even 可能被多次发送。
* 在同一个表中，Row Changed Event 在事件流中的版本将在第一次发送后按时间戳（TS）依次递增。
* Resolved Events 会被定期广播的消息队列的每个分区中.  Resolved Event 表示任何 TS 早于 Resolved Event 的事件已被发送到下游。
* DDL 事件会被广播到消息队列的每个分区。
* 同一行的多个 Row Changed Events 会被发送到消息队列的同一个分区。

## Benchmark

* 对同一事件，二进制协议编码所占用的字节数更少。
* Protobuf 作为一种被广泛使用的二进制格式，可以用来代替 craft. 因为craft格式可以应用复杂的优化，所以它可以比 protobuf 更紧凑、更快。

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
| 7944 ns/op | 75822 ns/op (854%)+ | 8020 ns/op (1%)+ | 8462 ns/op (6%) |

## Message format

一条 message 包含一个或多个 event，按以下格式排列：

Message:

| uvarint | header | body | term dictionary | size tables |
| :------ | :------ | :------ | :------ | ------- |
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
| delta uvarint chunk | 以 uvarint 格式编码的基数，后面是以 uvarint 格式编码的每个元素与最后一个元素的差值。 |
| delta varint chunk | 以 varint 格式编码的基数，后面是以 uvarint 格式编码的每个元素与最后一个元素的差值。 |
| float64 chunk | 以 float64 格式编码的连续元素。 |
| string/bytes chunk | 以 uvarint 格式编码的所有字符串/字节的连续长度，后面是每个元素的字节数。 |
| nullable string/bytes chunk | 以 uvarint 格式编码的所有字符串/字节的连续长度，后面是每个元素的字节。长度为 -1 时表示空字符串或字节数组。 |

* 当前协议的版本号为  `1`.

## Event format

本节介绍 Row Changed Event, DDL Event 和 Resolved Event 这三种事件的格式。

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

### Resolved Event

+ **Header:**

    | Data | Type | Description |
    | :--- | :--- | :---------- |
    | TS | uint64 | Resolved Event 的时间戳。任何 TS 比此 TS 早的事件都已发送。 |

+ **Event:** None

## Examples of the Event stream output

本节展示事件流的输出日志。由于 craft 协议是二进制的，因此不具备可读性，我们将使用开放协议来演示发生的事情，相应的 craft 事件流被转化为具备可读性的 json.

假设你在上游执行以下 SQL 语句，消息队列分区编号为2.

{{< copyable "sql" >}}

```sql
CREATE TABLE test.t1(id int primary key, val varchar(16));
```

从下面的日志 1 和日志 3 可以看出，DDL Event 被广播到所有的 MQ 分区，而 Resolved Event 被定期广播到每个 MQ 分区。

```
1. [partition=0] [key="{\"ts\":415508856908021766,\"scm\":\"test\",\"tbl\":\"t1\",\"t\":2}"] [value="{\"q\":\"CREATE TABLE test.t1(id int primary key, val varchar(16))\",\"t\":3}"]
2. [partition=0] [key="{\"ts\":415508856908021766,\"t\":3}"] [value=]
3. [partition=1] [key="{\"ts\":415508856908021766,\"scm\":\"test\",\"tbl\":\"t1\",\"t\":2}"] [value="{\"q\":\"CREATE TABLE test.t1(id int primary key, val varchar(16))\",\"t\":3}"]
4. [partition=1] [key="{\"ts\":415508856908021766,\"t\":3}"] [value=]
```

在上游执行以下SQL语句：

{{< copyable "sql" >}}

```sql
BEGIN;
INSERT INTO test.t1(id, val) VALUES (1, 'aa');
INSERT INTO test.t1(id, val) VALUES (2, 'aa');
UPDATE test.t1 SET val = 'bb' WHERE id = 2;
INSERT INTO test.t1(id, val) VALUES (3, 'cc');
COMMIT;
```

+ 从下面的日志 5 和日志 6 中，你可以看到，同一表中的多个 Row Changed Event 可能会根据主键被发送到不同的分区，但同一行的改变会被发送到同一分区，这样下游就可以很容易地并发处理该事件。
+ 从日志 6 开始，在一个事务中对同一行的多个更改只在一个 Row Changed Event 中发送。
+ 日志 8 是日志 7 的一个重复事件。行改变的事件可能会被重复，但每个版本的第一个事件是有序发送的。

```
5. [partition=0] [key="{\"ts\":415508878783938562,\"scm\":\"test\",\"tbl\":\"t1\",\"t\":1}"] [value="{\"u\":{\"id\":{\"t\":3,\"h\":true,\"v\":1},\"val\":{\"t\":15,\"v\":\"YWE=\"}}}"]
6. [partition=1] [key="{\"ts\":415508878783938562,\"scm\":\"test\",\"tbl\":\"t1\",\"t\":1}"] [value="{\"u\":{\"id\":{\"t\":3,\"h\":true,\"v\":2},\"val\":{\"t\":15,\"v\":\"YmI=\"}}}"]
7. [partition=0] [key="{\"ts\":415508878783938562,\"scm\":\"test\",\"tbl\":\"t1\",\"t\":1}"] [value="{\"u\":{\"id\":{\"t\":3,\"h\":true,\"v\":3},\"val\":{\"t\":15,\"v\":\"Y2M=\"}}}"]
8. [partition=0] [key="{\"ts\":415508878783938562,\"scm\":\"test\",\"tbl\":\"t1\",\"t\":1}"] [value="{\"u\":{\"id\":{\"t\":3,\"h\":true,\"v\":3},\"val\":{\"t\":15,\"v\":\"Y2M=\"}}}"]
```

在上游执行以下SQL语句：

{{< copyable "sql" >}}

```sql
BEGIN;
DELETE FROM test.t1 WHERE id = 1;
UPDATE test.t1 SET val = 'dd' WHERE id = 3;
UPDATE test.t1 SET id = 4, val = 'ee' WHERE id = 2;
COMMIT;
```

+ 日志 9 是 `Delete`类型的  Row Changed Event, 这种类型的事件只包含主键列或唯一索引列。
+ 日志 13 和日志 14 是 Resolved Event. Resolved Event 表示在这个分区中，任何小于 Resolved Event 的 TS 的事件（包括 Row Changed Event 和DDL Event）都已经被发送。

```
9. [partition=0] [key="{\"ts\":415508881418485761,\"scm\":\"test\",\"tbl\":\"t1\",\"t\":1}"] [value="{\"d\":{\"id\":{\"t\":3,\"h\":true,\"v\":1}}}"]
10. [partition=1] [key="{\"ts\":415508881418485761,\"scm\":\"test\",\"tbl\":\"t1\",\"t\":1}"] [value="{\"d\":{\"id\":{\"t\":3,\"h\":true,\"v\":2}}}"]
11. [partition=0] [key="{\"ts\":415508881418485761,\"scm\":\"test\",\"tbl\":\"t1\",\"t\":1}"] [value="{\"u\":{\"id\":{\"t\":3,\"h\":true,\"v\":3},\"val\":{\"t\":15,\"v\":\"ZGQ=\"}}}"]
12. [partition=0] [key="{\"ts\":415508881418485761,\"scm\":\"test\",\"tbl\":\"t1\",\"t\":1}"] [value="{\"u\":{\"id\":{\"t\":3,\"h\":true,\"v\":4},\"val\":{\"t\":15,\"v\":\"ZWU=\"}}}"]
13. [partition=0] [key="{\"ts\":415508881038376963,\"t\":3}"] [value=]
14. [partition=1] [key="{\"ts\":415508881038376963,\"t\":3}"] [value=]
```

## Protocol parsing for consumers

目前，TiCDC 没有提供 TiCDC Craft 的标准解析库，但提供了 Golang 版本和 Java 版本的解析器。你可以参考本文件提供的数据格式和以下解码器来实现其他语言的协议解析器。

- [Golang demo](https://github.com/pingcap/ticdc/tree/master/kafka_consumer)
- [Java demo](https://github.com/pingcap/ticdc/tree/master/demo/java)

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

> **Note:**
>
> + 这一特性仍处于试验阶段。请**不要**在生产环境中使用它。
> + `BinaryFlag` 只有在列类型为 BLOB/TEXT (包括 TINYBLOB/TINYTEXT 和 BINARY/CHAR) 才有意义。 当上游列是 BLOB 类型时，`BinaryFlag`值被设置为`1`。当上游列是 TEXT 类型时，`BinaryFlag` 值被设置为 `0`.
> + 从上游复制一个表时，TiCDC选择一个[有效索引](/ticdc/ticdc-overview.md#restrictions)作为 Handle 索引。Handle 索引列的 `HandleKeyFlag` 值被设置为`1`。
> + [Protobuf definition for benchmark](https://github.com/sunxiaoguang/ticdc/blob/craft/proto/CraftBenchmark.proto)
