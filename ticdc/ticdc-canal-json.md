---
title: TiCDC Canal-JSON Protocol
aliases: ['/docs-cn/dev/ticdc/ticdc-canal-json/','/docs-cn/dev/reference/tools/ticdc/canal-json/']
---

# TiCDC Canal-JSON Protocol

## 概述

Canal-JSON 是由 [Alibaba Canal](https://github.com/alibaba/canal) 提供的一种数据交换格式协议。TiCDC 提供了对 Canal-JSON 数据格式的近似复刻实现。当使用 MQ(Message Queue) 作为下游 sink 时，用户可以在 sink-uri 中指定使用 Canal-JSON，TiCDC 将以 Event 为基本单位封装构造 Canal-JSON Message，向下游发送 TiDB 的数据变更事件。Event 分为三类：

* Row Changed Event：代表一行数据变更记录，在行变更发生时该类 Event 被发出，包含变更后该行的相关信息。
* DDL Event：代表 DDL 变更记录，在上游成功执行 DDL 后发出，DDL Event 会被发送到索引偏移量为 0 的 MQ Partition。
* Resolved Event：代表一个特殊的时间点，表示在这个时间点前的收到的 Event 是完整的。仅当用户在 sink-uri 中设置 `enable-tidb-extension=true` 时生效。

### TiDB 自定义字段

TiCDC 支持在 sink-uri 中设置 `enable-tidb-extension=true`。开启该功能之后，Canal-JSON 将携带 TiCDC 自定义字段，内容如下：

* TiCDC 将会发送 ResolvedEvent 事件。
* TiCDC 发送的 Row Changed Event 和 DDL Event 类型事件中，将会含有一个名为 `_tidb` 的字段。

配置样例如下所示：

{{< copyable "shell-regular" >}}

```shell
--sink-uri="kafka://127.0.0.1:9092/topic-name?kafka-version=2.4.0&protocol=canal-json&enable-tidb-extension=true"
```

`enable-tidb-extension` 默认为 `false`，仅当使用 Canal-JSON 时生效。

## Message 格式定义
### DDL Event

TiCDC 会把一个 DDL Event 编码成如下 Canal-JSON 格式：

```
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
    "_tidb": {                             // 仅当 enable-tidb-extension=true 时存在该字段
        "commitTs": 163963309467037594
    }
}
```

| 字段         | 类型   | 说明                    |
| :---------- | :----- | :--------------------- |
| id          | Number | TiCDC 默认该值为 0       |
| database    | String | Row 所在的 Database 的名字 |
| table       | String | Row 所在的 Table 的名字  |
| pkNames     | Array  | 组成 primary key 的所有列的名字 |
| isDdl       | Bool   | 该条消息是否为 DDL 事件|
| type        | String | Canal-JSON 定义的事件类型|
| es          | Number | 产生该条消息的事件发生的时间 |
| ts          | Number | 消息被生成时候的 13 位时间戳 |
| sql         | String | 当 isDdl 为 true 时，记录对应的 DDL 语句 |
| sqlType     | Object | 当 isDdl 为 false 时，记录每一列数据类型在 Java 中的类型表示 |
| mysqlType   | object | 当 isDdl 为 false 时，记录每一列数据类型 在 MySQL 中的类型表示 |
| data        | Object | 当 isDdl 为 false 时，记录每一列的名字和其数据值 |
| old         | Object | 仅当该条消息由 Update 类型事件产生时，记录每一列的名字，和 Update 之前的数据值|
| _tidb       | Object | 仅当 enable-tidb-extension 为 true 时，该字段存在。当前阶段，只含有 commitTs，其为造成 Row 变更的事务的 tso ｜

### Row Changed Event

对于一行数据变更事件，TiCDC 会将其编码成如下形式:

```
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
    "_tidb": {                             // 仅当 enable-tidb-extension=true 时存在该字段
        "commitTs": 163963314122145239
    }
}
```

### Resolved Event

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
    "_tidb": {
        "watermarkTs": 429918007904436226
    }
}

TiCDC 仅当 `enable-tidb-extension` 为 `true` 时才会发送 Resolved Event，其 `type` 字段值为 `TIDB_WATERMARK`。该类型事件具有 `_tidb` 字段，当前只含有 `watermarkTs`，其含义为当前 tso。当用户收到该类型事件时，可以得知，所有 tso 小于 `watermarkTs` 的事件，已经发送完毕。

### 消费端数据解析

从上面的示例中可知，Canal-JSON 具有统一的数据格式，针对不同的事件类型，有不同的字段填充规则。消费者可以使用统一的方法对该 JSON 格式的数据进行解析，然后通过判断字段值的方式，来确定具体事件类型：

* 当 `isDdl` 为 true 时，该消息含有一条 DDL Event。
* 当 `isDdl` 为 false 时，需要对 `type` 字段加以判断。如果 `type ` 为 `TIDB_WATERMARK`，可得知其为 Resolved Event，反之则为 Row Changed Event。

## MySQL Type 字段说明

Canal-JSON 格式会在 `mysqlType` 字段中记录每一列的 MySQL Type 的字符串表示。相关详情可以参考 [TiDB Data Types](/data-type-overview.md)。

## SQL Type 字段说明

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

### 整数类型

[整数类型](/data-type-numeric.md#整数类型)，需要考虑是否有 `Unsigned` 限定，并且需要考虑当前取值大小，分别对应有不同的 Java SQL Type (Code)。

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

TiCDC 涉及的 Java SQL Type 及其 Code 映射关系如下所示:

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

对 Java SQL Type 的更多解释，可以参考 [Java SQL Class Types](https://docs.oracle.com/javase/8/docs/api/java/sql/Types.html)

## TiCDC Canal-JSON 和 Canal 官方实现对比

TiCDC 对 Canal-JSON 数据格式的实现，和官方有些许不同。具体如下：

* 对于 `Update` 类型事件，Canal 官方实现中，`Old` 字段仅包含被修改的列数据，而 TiCDC 的实现则包含所有列数据。

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

对于 `update` 语句，TiCDC 将会输出一条 `type` 为 `UPDATE` 的事件消息，如下所示。该 `update` 语句，仅对 `c_int`, `c_tinyint` 两列进行了修改, 输出事件消息的 `Old` 字段，则含有所有列数据。

```
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
    "old": [
        {
            "c_bigint": "9223372036854775807",
            "c_int": "2147483647",
            "c_mediumint": "8388607",
            "c_smallint": "32767",
            "c_tinyint": "127",
            "id": "2"
        }
    ]
}
```

* 对于 `mysqlType` 字段，Canal 官方实现中，对于含有参数的类型，会含有完整的参数信息, TiCDC 实现则没有类型参数信息。

假设在上游 TiDB 按顺序执行如下 SQL 语句:

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

在上面的表定义 SQL 语句中，如 decimal / char / varchar / enum 等类型，都还有参数。在下所示的输出 Canal-JSON 格式中，`mysqlType` 字段中的数据，只含有基本 MySQL Type 字符串表示。如果业务需要这部分类型参数信息，需要用户自行通过其他方式确定。

```
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

### TiCDC Canal-JSON 特殊说明

TiCDC 自 vxx 引入了 Canal-JSON，并在 v5.4.0 对该功能进行 GA。 GA 前后两版 Canal-JSON 实现有些许不同，具体如下:

* `Delete` 类型的事件，GA 后版本的 `Old` 字段的内容发生了变化。

如下是一个 `DELETE` 事件的数据内容，在 GA 前的实现中，"old" 的内容和 "data" 相同，在 GA 后的实现中，"old" 将被设为 null。用户可以通过 "data" 字段获取到被删除数据，在删除之前的数据。

```
{
    "id": 0,
    "database": "test",
    ...
    "type": "DELETE",
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
    "old": [
        {
            "c_bigint": "9223372036854775807",
            "c_int": "0",
            "c_mediumint": "8388607",
            "c_smallint": "32767",
            "c_tinyint": "0",
            "id": "2"
        }
    ]

    // GA 后实现，`old` 设为 null
    "old": null
}
```

* `mysqlType` 字段，对于含有 `Unsigned` 约束的数值类型，GA 后的实现添加了 `unsigned` 关键字。

假设执行如下 SQL 语句：

```sql
create table tp_unsigned_int (
     id          int auto_increment,
     c_unsigned_tinyint   tinyint   unsigned null,
     c_unsigned_smallint  smallint  unsigned null,
     c_unsigned_mediumint mediumint unsigned null,
     c_unsigned_int       int       unsigned null,
     c_unsigned_bigint    bigint    unsigned null,
     constraint pk
         primary key (id)
);

insert into tp_unsigned_int (...) values (...);
```

如下所示为一个 GA 之前的实现示例。对于 `insert` 语句，在 `mysqlType` 中, 不含有 `unsigned` 关键字。

```
{
    "id": 0,
    ...
    "type": "INSERT",
    ...
    "sqlType": {
        ...
    },
    "mysqlType": { // 注意：列类型没有被标记为 unsigned
        "c_unsigned_bigint": "bigint",
        "c_unsigned_int": "int",
        "c_unsigned_mediumint": "mediumint",
        "c_unsigned_smallint": "smallint",
        "c_unsigned_tinyint": "tinyint",
        "id": "int"
    },
    "data": [
        ...
    ],
    "old": [
        null
    ]
}
```

在 GA 后的实现输出内容如下:
```
{
    "id": 0,
    ...
    "type": "INSERT",
    ...
    "sqlType": {
        ...
    },
    "mysqlType": {
        "c_unsigned_bigint": "bigint unsigned",
        "c_unsigned_int": "int unsigned",
        "c_unsigned_mediumint": "mediumint unsigned",
        "c_unsigned_smallint": "smallint unsigned",
        "c_unsigned_tinyint": "tinyint unsigned",
        "id": "int"
    },
    "data": [
        ...
    ],
    "old": [
        null
    ]
}
```

* `sqlType` 字段，GA 前后实现, 相同 MySQL Type 对其取值有所不同。具体如下所示:

| MySQL Type | Java SQL Type (Old) | Java SQL Type (New) |
| :----------| :-------------------| :-------------------|
| Boolean    | 5                   | -6                  | 
| Tinyint    | 5                   | -6 / 5              |
| Smallint   | 4                   | 5 / 4               |
| Int        | -5                  | 4 / -5              |
| Bigint     | 3                   | -5 / 3              |
| Binary     | 1                   | 2004                |
| Varbinary  | 12                  | 2004                |
| Year       | 91                  | 12                  |
| Enum       | 1                   | 4                   |
| Set        | 1                   | -7                  |
| Json       | -1                  | 12                  |

在 GA 前的实现对 Java SQL Type 计算过程中，针对有 `unsigned` 约束的整数类型，未考虑取值因素，一律进行了类型提升。GA 后实现，考虑了取值因素，详细可以参考 [整数类型](#整数类型)。

* `Old` 字段的表现形式发生改变。

在 GA 前的实现中，如果 `Old` 字段为 null，其会被存放在一个数组中。
```
{
    "id": 0,
    ...
    "type": "INSERT",
    ...
    "sqlType": {
        ...
    },
    "mysqlType": {
        ...
    },
    "data": [
        ...
    ],
    "old": [
        null
    ]
}
```

在 GA 后的实现中，如果 `Old` 字段为 null，则直接对其进行设置。

```
{
    "id": 0,
    ...
    "type": "INSERT",
    ...
    "sqlType": {
        ...
    },
    "mysqlType": {
        ...
    },
    "data": [
        ...
    ],
    "old": null
}
```