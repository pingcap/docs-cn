---
title: TiCDC Canal-JSON Protocol
summary: 了解 TiCDC Canal-JSON Protocol 的概念和使用方法。
---

# TiCDC Canal-JSON Protocol

Canal-JSON 是由 [Alibaba Canal](https://github.com/alibaba/canal) 定义的一种数据交换格式协议。通过本文，你可以了解 TiCDC 对 Canal-JSON 数据格式的实现，包括 TiDB 扩展字段、Canal-JSON 数据格式定义，以及和官方实现进行对比等相关内容。

## 使用 Canal-JSON

当使用 MQ (Message Queue) 作为下游 Sink 时，你可以在 `sink-uri` 中指定使用 Canal-JSON，TiCDC 将以 Event 为基本单位封装构造 Canal-JSON Message，向下游发送 TiDB 的数据变更事件。

Event 分为三类：

* DDL Event：代表 DDL 变更记录，在上游成功执行 DDL 语句后发出，DDL Event 会被发送到索引为 0 的 MQ Partition。
* DML Event：代表一行数据变更记录，在行变更发生时该类 Event 被发出，包含变更后该行的相关信息。
* WATERMARK Event：代表一个特殊的时间点，表示在这个时间点前收到的 Event 是完整的。仅适用于 TiDB 扩展字段，当你在 `sink-uri` 中设置 `enable-tidb-extension=true` 时生效。

使用 `Canal-JSON` 时的配置样例如下所示：

{{< copyable "shell-regular" >}}

```shell
cdc cli changefeed create --pd=http://127.0.0.1:2379 --changefeed-id="kafka-canal-json" --sink-uri="kafka://127.0.0.1:9092/topic-name?kafka-version=2.6.0&protocol=canal-json"
```

## TiDB 扩展字段

Canal-JSON 协议本是为 MySQL 设计的，其中并不包含 TiDB 专有的 CommitTS 事务唯一标识等重要字段。为了解决这个问题，TiCDC 在 Canal-JSON 协议格式中附加了 TiDB 扩展字段。在 `sink-uri` 中设置 `enable-tidb-extension` 为 `true` 后，TiCDC 生成 Canal-JSON 消息时的行为如下：

* TiCDC 发送的 DML Event 和 DDL Event 类型消息中，将会含有一个名为 `_tidb` 的字段。
* TiCDC 将会发送 WATERMARK Event 消息。·

配置样例如下所示：

{{< copyable "shell-regular" >}}

```shell
cdc cli changefeed create --pd=http://127.0.0.1:2379 --changefeed-id="kafka-canal-json-enable-tidb-extension" --sink-uri="kafka://127.0.0.1:9092/topic-name?kafka-version=2.6.0&protocol=canal-json&enable-tidb-extension=true"
```

`enable-tidb-extension` 默认为 `false`，仅当使用 Canal-JSON 时生效。

## Message 格式定义

下面介绍 DDL Event、DML Event 和 WATERMARK Event 的格式定义，以及消费端的数据解析。

### DDL Event

TiCDC 会把一个 DDL Event 编码成如下 Canal-JSON 格式：

```json
{
    "id": 0,
    "database": "test",
    "table": "",
    "pkNames": null,
    "isDdl": true,
    "type": "QUERY",
    "es": 1639633094670,
    "ts": 1639633095489,
    "sql": "drop database if exists test",
    "sqlType": null,
    "mysqlType": null,
    "data": null,
    "old": null,
    "_tidb": {     // TiDB 的扩展字段
        "commitTs": 163963309467037594
    }
}
```

以上 JSON 数据的字段解释如下：

| 字段      | 类型   | 说明                                                                      |
|:----------|:-------|:-------------------------------------------------------------------------|
| id        | Number | TiCDC 默认值为 0                                                        |
| database  | String | Row 所在的 Database 的名字                                                |
| table     | String | Row 所在的 Table 的名字                                                   |
| pkNames   | Array  | 组成 primary key 的所有列的名字                                            |
| isDdl     | Bool   | 该条消息是否为 DDL 事件                                                    |
| type      | String | Canal-JSON 定义的事件类型                                                  |
| es        | Number | 产生该条消息的事件发生时的 13 位（毫秒级）时间戳                               |
| ts        | Number | TiCDC 生成该条消息时的 13 位（毫秒级）时间戳                                  |
| sql       | String | 当 isDdl 为 true 时，记录对应的 DDL 语句                                    |
| sqlType   | Object | 当 isDdl 为 false 时，记录每一列数据类型在 Java 中的类型表示                  |
| mysqlType | object | 当 isDdl 为 false 时，记录每一列数据类型在 MySQL 中的类型表示                |
| data      | Object | 当 isDdl 为 false 时，记录每一列的名字及其数据值                             |
| old       | Object | 仅当该条消息由 Update 类型事件产生时，记录每一列的名字，和 Update 之前的数据值  |
| _tidb     | Object | TiDB 扩展字段，仅当 `enable-tidb-extension` 为 true 时才会存在。其中的 `commitTs` 值为造成 Row 变更的事务的 TSO  |

### DML Event

对于一行 DML 数据变更事件，TiCDC 会将其编码成如下形式:

```json
{
    "id": 0,
    "database": "test",
    "table": "tp_int",
    "pkNames": [
        "id"
    ],
    "isDdl": false,
    "type": "INSERT",
    "es": 1639633141221,
    "ts": 1639633142960,
    "sql": "",
    "sqlType": {
        "c_bigint": -5,
        "c_int": 4,
        "c_mediumint": 4,
        "c_smallint": 5,
        "c_tinyint": -6,
        "id": 4
    },
    "mysqlType": {
        "c_bigint": "bigint",
        "c_int": "int",
        "c_mediumint": "mediumint",
        "c_smallint": "smallint",
        "c_tinyint": "tinyint",
        "id": "int"
    },
    "data": [
        {
            "c_bigint": "9223372036854775807",
            "c_int": "2147483647",
            "c_mediumint": "8388607",
            "c_smallint": "32767",
            "c_tinyint": "127",
            "id": "2"
        }
    ],
    "old": null,
    "_tidb": {     // TiDB 的扩展字段
        "commitTs": 163963314122145239
    }
}
```

### WATERMARK Event

仅当 `enable-tidb-extension` 为 `true` 时，TiCDC 才会发送 WATERMARK Event，其 `type` 字段值为 `TIDB_WATERMARK`。该类型事件具有 `_tidb` 字段，当前只含有 `watermarkTs`，其值为该 Event 发送时的 TSO。

当你收到一个该类型的事件，所有 `commitTs` 小于 `watermarkTs` 的事件均已发送完毕。因为 TiCDC 提供 At Least Once 语义，可能出现重复发送数据的情况。如果后续收到有 `commitTs` 小于 `watermarkTs` 的事件，可以忽略。

WATERMARK Event 的示例如下：

```json
{
    "id": 0,
    "database": "",
    "table": "",
    "pkNames": null,
    "isDdl": false,
    "type": "TIDB_WATERMARK",
    "es": 1640007049196,
    "ts": 1640007050284,
    "sql": "",
    "sqlType": null,
    "mysqlType": null,
    "data": null,
    "old": null,
    "_tidb": {     // TiDB 的扩展字段
        "watermarkTs": 429918007904436226
    }
}
```

### 消费端数据解析

从上面的示例中可知，Canal-JSON 具有统一的数据格式，针对不同的事件类型，有不同的字段填充规则。消费者可以使用统一的方法对该 JSON 格式的数据进行解析，然后通过判断字段值的方式，来确定具体事件类型：

* 当 `isDdl` 为 true 时，该消息含有一条 DDL Event。
* 当 `isDdl` 为 false 时，需要对 `type` 字段加以判断。如果 `type` 为 `TIDB_WATERMARK`，可得知其为 WATERMARK Event，否则就是 DML Event。

## 字段说明

Canal-JSON 格式会在 `mysqlType` 字段和 `sqlType` 字段中记录对应的数据类型。

### MySQL Type 字段

Canal-JSON 格式会在 `mysqlType` 字段中记录每一列的 MySQL Type 的字符串表示。相关详情可以参考 [TiDB Data Types](/data-type-overview.md)。

### SQL Type 字段

Canal-JSON 格式会在 `sqlType` 字段中记录每一列的 Java SQL Type，即每条数据在 JDBC 中对应的数据类型，其值可以通过 MySQL Type 和具体数据值计算得到。具体对应关系如下:

| MySQL Type | Java SQL Type Code |
| :----------| :----------------- |
| Boolean    | -6                 |
| Float      | 7                  |
| Double     | 8                  |
| Decimal    | 3                  |
| Char       | 1                  |
| Varchar    | 12                 |
| Binary     | 2004               |
| Varbinary  | 2004               |
| Tinytext   | 2005               |
| Text       | 2005               |
| Mediumtext | 2005               |
| Longtext   | 2005               |
| Tinyblob   | 2004               |
| Blob       | 2004               |
| Mediumblob | 2004               |
| Longblob   | 2004               |
| Date       | 91                 |
| Datetime   | 93                 |
| Timestamp  | 93                 |
| Time       | 92                 |
| Year       | 12                 |
| Enum       | 4                  |
| Set        | -7                 |
| Bit        | -7                 |
| JSON       | 12                 |

## 整数类型

你需要考虑[整数类型](/data-type-numeric.md#整数类型)是否有 `Unsigned` 约束，以及当前取值大小，分别对应不同的 Java SQL Type Code。如下表所示。

| MySQL Type String  | Value Range                                 | Java SQL Type Code |
| :------------------| :------------------------------------------ | :----------------- |
| tinyint            | [-128, 127]                                 | -6                 |
| tinyint unsigned   | [0, 127]                                    | -6                 |
| tinyint unsigned   | [128, 255]                                  | 5                  |
| smallint           | [-32768, 32767]                             | 5                  |
| smallint unsigned  | [0, 32767]                                  | 5                  |
| smallint unsigned  | [32768, 65535]                              | 4                  |
| mediumint          | [-8388608, 8388607]                         | 4                  |
| mediumint unsigned | [0, 8388607]                                | 4                  |
| mediumint unsigned | [8388608, 16777215]                         | 4                  |
| int                | [-2147483648, 2147483647]                   | 4                  |
| int unsigned       | [0, 2147483647]                             | 4                  |
| int unsigned       | [2147483648, 4294967295]                    | -5                 |
| bigint             | [-9223372036854775808, 9223372036854775807] | -5                 |
| bigint unsigned    | [0, 9223372036854775807]                    | -5                 |
| bigint unsigned    | [9223372036854775808, 18446744073709551615] | 3                  |

TiCDC 涉及的 Java SQL Type 及其 Code 映射关系如下表所示。

| Java SQL Type | Java SQL Type Code |
| :-------------| :------------------|
| CHAR          | 1                  |
| DECIMAL       | 3                  |
| INTEGER       | 4                  |
| SMALLINT      | 5                  |
| REAL          | 7                  |
| DOUBLE        | 8                  |
| VARCHAR       | 12                 |
| DATE          | 91                 |
| TIME          | 92                 |
| TIMESTAMP     | 93                 |
| BLOB          | 2004               |
| CLOB          | 2005               |
| BIGINT        | -5                 |
| TINYINT       | -6                 |
| Bit           | -7                 |

想要了解 Java SQL Type 的更多信息，请参考 [Java SQL Class Types](https://docs.oracle.com/javase/8/docs/api/java/sql/Types.html)。

## TiCDC Canal-JSON 和 Canal 官方实现对比

TiCDC 对 Canal-JSON 数据格式的实现，包括 `Update` 类型事件和 `mysqlType` 字段，和官方有些许不同。主要差异见下表。

| 差异点            | TiCDC                  | Canal                                |
|:----------------|:-------------------------|:-------------------------------------|
| `Update` 类型事件 | `old` 字段包含所有列数据 | `old` 字段仅包含被修改的列数据          |
| `mysqlType` 字段  | 对于含有参数的类型，没有类型参数信息         | 对于含有参数的类型，会包含完整的参数信息 |

### `Update` 类型事件

对于 `Update` 类型事件，Canal 官方实现中，`old` 字段仅包含被修改的列数据，而 TiCDC 的实现则包含所有列数据。

假设在上游 TiDB 按顺序执行如下 SQL 语句:

```sql
create table tp_int
(
    id          int auto_increment,
    c_tinyint   tinyint   null,
    c_smallint  smallint  null,
    c_mediumint mediumint null,
    c_int       int       null,
    c_bigint    bigint    null,
    constraint pk
        primary key (id)
);

insert into tp_int(c_tinyint, c_smallint, c_mediumint, c_int, c_bigint)
values (127, 32767, 8388607, 2147483647, 9223372036854775807);

update tp_int set c_int = 0, c_tinyint = 0 where c_smallint = 32767;
```

对于 `update` 语句，TiCDC 将会输出一条 `type` 为 `UPDATE` 的事件消息，如下所示。该 `update` 语句仅对 `c_int` 和 `c_tinyint` 两列进行了修改。输出事件消息的 `old` 字段，则包含所有列数据。

```json
{
    "id": 0,
    ...
    "type": "UPDATE",
    ...
    "sqlType": {
        ...
    },
    "mysqlType": {
        ...
    },
    "data": [
        {
            "c_bigint": "9223372036854775807",
            "c_int": "0",
            "c_mediumint": "8388607",
            "c_smallint": "32767",
            "c_tinyint": "0",
            "id": "2"
        }
    ],
    "old": [                                 // TiCDC 输出事件消息的 `old` 字段，则包含所有列数据。
        {
            "c_bigint": "9223372036854775807",
            "c_int": "2147483647",           // 修改的列
            "c_mediumint": "8388607",
            "c_smallint": "32767",
            "c_tinyint": "127",              // 修改的列
            "id": "2"
        }
    ]
}
```

官方 Canal 输出事件消息的 `old` 字段仅包含被修改的列数据。示例如下。

```json
{
    "id": 0,
    ...
    "type": "UPDATE",
    ...
    "sqlType": {
        ...
    },
    "mysqlType": {
        ...
    },
    "data": [
        {
            "c_bigint": "9223372036854775807",
            "c_int": "0",
            "c_mediumint": "8388607",
            "c_smallint": "32767",
            "c_tinyint": "0",
            "id": "2"
        }
    ],
    "old": [                                    // Canal 输出事件消息的 `old` 字段，仅包含被修改的列的数据。
        {
            "c_int": "2147483647",              // 修改的列
            "c_tinyint": "127",                 // 修改的列
        }
    ]
}
```

### `mysqlType` 字段

对于 `mysqlType` 字段，Canal 官方实现中，对于含有参数的类型，会包含完整的参数信息，TiCDC 实现则没有类型参数信息。

在下面示例的表定义 SQL 语句中，如 decimal / char / varchar / enum 等类型，都含有参数。对比 TiCDC 和 Canal 官方实现分别生成的 Canal-JSON 格式数据可知，在 `mysqlType` 字段中的数据，TiCDC 实现只包含基本 MySQL Type。如果业务需要类型参数信息，需要你自行通过其他方式实现。

假设在上游数据库按顺序执行如下 SQL 语句:

```sql
create table t (
    id     int auto_increment,
    c_decimal    decimal(10, 4) null,
    c_char       char(16)      null,
    c_varchar    varchar(16)   null,
    c_binary     binary(16)    null,
    c_varbinary  varbinary(16) null,

    c_enum enum('a','b','c') null,
    c_set  set('a','b','c')  null,
    c_bit  bit(64)            null,
    constraint pk
        primary key (id)
);

insert into t (c_decimal, c_char, c_varchar, c_binary, c_varbinary, c_enum, c_set, c_bit)
values (123.456, "abc", "abc", "abc", "abc", 'a', 'a,b', b'1000001');
```

TiCDC 输出内容如下：

```json
{
    "id": 0,
    ...
    "isDdl": false,
    "sqlType": {
        ...
    },
    "mysqlType": {
        "c_binary": "binary",
        "c_bit": "bit",
        "c_char": "char",
        "c_decimal": "decimal",
        "c_enum": "enum",
        "c_set": "set",
        "c_varbinary": "varbinary",
        "c_varchar": "varchar",
        "id": "int"
    },
    "data": [
        {
            ...
        }
    ],
    "old": null,
}
```

Canal 官方实现输出内容如下：

```json
{
    "id": 0,
    ...
    "isDdl": false,
    "sqlType": {
        ...
    },
    "mysqlType": {
        "c_binary": "binary(16)",
        "c_bit": "bit(64)",
        "c_char": "char(16)",
        "c_decimal": "decimal(10, 4)",
        "c_enum": "enum('a','b','c')",
        "c_set": "set('a','b','c')",
        "c_varbinary": "varbinary(16)",
        "c_varchar": "varchar(16)",
        "id": "int"
    },
    "data": [
        {
            ...
        }
    ],
    "old": null,
}
```