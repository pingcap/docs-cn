---
title: TiCDC Debezium Protocol
summary: 了解 TiCDC Debezium Protocol 的概念和使用方法。
---

# TiCDC Debezium Protocol

[Debezium](https://debezium.io/) 是一个用于捕获数据库变更的工具。它会将捕获的数据库变更的每一条记录转化为一个被称为“事件” (event) 的消息，并将这些事件发送到 Kafka 中。从 v8.0.0 起，TiCDC 支持将 TiDB 的变更以 Debezium 的格式直接传输到 Kafka，为之前使用 Debezium 的 MySQL 集成的用户简化了从 MySQL 数据库迁移的过程。

## 使用 Debezium 消息格式

当使用 Kafka 作为下游 Sink 时，你可以将 `sink-uri` 的 `protocol` 字段指定为 `debezium`，TiCDC 将以 Event 为基本单位封装构造 Debezium 消息，向下游发送 TiDB 的数据变更事件。

目前，Debezium 协议只支持 Row Changed Event，会直接忽略 DDL Event 和 WATERMARK Event。Row Changed Event 代表一行的数据变化，在行发生变更时该 Event 被发出，包含该行在变更前后的相关信息。WATERMARK Event 用于标记一个表的同步进度，所有早于 watermark 的事件都已经发送给下游。

使用 Debezium 消息格式时的配置样例如下所示：

```shell
cdc cli changefeed create --server=http://127.0.0.1:8300 --changefeed-id="kafka-debezium" --sink-uri="kafka://127.0.0.1:9092/topic-name?kafka-version=2.4.0&protocol=debezium"
```

Debezium 输出格式中包含当前行的 Schema 信息，以便下游消费者更好地理解当前行的数据结构。对于不需要输出 Schema 信息的场景，也可以通过在 changefeed 的配置文件或者 `sink-uri` 中将 `debezium-disable-schema` 参数设置为 `true` 来关闭 Schema 信息的输出。

此外，Debezium 原有格式中并不包含 TiDB 专有的 `CommitTS` 事务唯一标识等重要字段。为了保证数据的完整性，TiCDC 在 Debezium 格式中增加了 `CommitTs` 和 `ClusterID` 两个字段，用于标识 TiDB 数据变更的相关信息。

## Message 格式定义

下面将介绍 Debezium 格式输出的 DML Event 的格式定义。

### DML Event

TiCDC 会将一个 DML 事件转换为一个 Kafka 事件，其中事件的 key 和 value 都按照 Debezium 协议进行编码。

#### Key 数据格式

```json
{
    "payload": {
        "a": 4
    },
    "schema": {
        "fields": [
            {
                "field": "a",
                "optional": true,
                "type": "int32"
            }
        ],
        "name": "default.test.t2.Key",
        "optional": false,
        "type": "struct"
    }
}
```

Key 中的字段只包含主键或唯一索引列。字段解释如下：

| 字段      | 类型   | 说明                                                                      |
|:----------|:-------|:-------------------------------------------------------------------------|
| payload   | JSON | 主键或唯一索引列的信息。每个字段的 key 和 value 分别为列名和当前值  |
| schema.fields     | JSON   |  payload 中各个字段的类型信息，包括对应行数据变更前后 schema 的信息等      |
| schema.name     | 字符串   |  schema 的名称，格式为 `"{cluster-name}.{schema-name}.{table-name}.Key"`     |
| schema.optional     | 布尔值   |  optional 为 `true` 时表示该字段为选填项   |
| schema.type     | 字符串   |  表示该字段的数据类型   |

#### Value 数据格式

```json
{
    "payload":{
        "ts_ms":1707103832957,
        "transaction":null,
        "op":"c",
        "before":null,
        "after":{
            "a":4,
            "b":2
        },
        "source":{
            "version":"2.4.0.Final",
            "connector":"TiCDC",
            "name":"default",
            "ts_ms":1707103832263,
            "snapshot":"false",
            "db":"test",
            "table":"t2",
            "server_id":0,
            "gtid":null,
            "file":"",
            "pos":0,
            "row":0,
            "thread":0,
            "query":null,
            "commit_ts":447507027004751877,
            "cluster_id":"default"
        }
    },
    "schema":{
        "type":"struct",
        "optional":false,
        "name":"default.test.t2.Envelope",
        "version":1,
        "fields":{
            {
                "type":"struct",
                "optional":true,
                "name":"default.test.t2.Value",
                "field":"before",
                "fields":[
                    {
                        "type":"int32",
                        "optional":false,
                        "field":"a"
                    },
                    {
                        "type":"int32",
                        "optional":true,
                        "field":"b"
                    }
                ]
            },
            {
                "type":"struct",
                "optional":true,
                "name":"default.test.t2.Value",
                "field":"after",
                "fields":[
                    {
                        "type":"int32",
                        "optional":false,
                        "field":"a"
                    },
                    {
                        "type":"int32",
                        "optional":true,
                        "field":"b"
                    }
                ]
            },
            {
                "type":"string",
                "optional":false,
                "field":"op"
            },
            ...
        }
    }
}
```

以上 JSON 数据的重点字段解释如下：

| 字段      | 类型   | 说明                                                                      |
|:----------|:-------|:-------------------------------------------------------------------------|
| payload.op        | 字符串 | 变更事件类型。`"c"` 表示这是一个 `INSERT` 事件，`"u"` 表示这是一个 `UPDATE` 事件，`"d"` 表示这是一个 `DELETE` 事件  |
| payload.ts_ms     | 数值 | TiCDC 生成这条信息的时间戳（毫秒级别）                                |
| payload.before    | JSON   | 这条事件语句变更前的数据值，对于 `"c"` 事件，`before` 字段的值为 `null`     |
| payload.after     | JSON   | 这条事件语句变更后的数据值，对于 `"d"` 事件，`after` 字段的值为 `null`     |
| payload.source.commit_ts     | 数值  | TiCDC 生成这条信息时的 `CommitTs` 标识                    |
| payload.source.db     | 字符串   | 事件发生的数据库的名称                    |
| payload.source.table     | 字符串  |  事件发生的数据表的名称                    |
| schema.fields     | JSON   |  payload 中各个字段的类型信息，包括对应行数据变更前后 schema 的信息等      |
| schema.name     | 字符串   |  schema 的名称，格式为 `"{cluster}.{schema}.{table}.Envelope"`     |
| schema.optional     | 布尔值   |  optional 为 `true` 时表示该字段为选填项   |
| schema.type     | 字符串   |  表示该字段的类型   |

### 数据类型映射

TiCDC Debezium 消息中的数据格式映射基本遵循 [Debezium 的数据类型映射规则](https://debezium.io/documentation/reference/2.4/connectors/mysql.html#mysql-data-types)，与 Debezium Connector for MySQL 原生消息大体一致。但是对于部分数据类型，TiCDC Debezium 的处理方式与 Debezium Connector Message 存在一定差异，具体如下：

- 目前 TiDB 不支持空间数据类型，包括 GEOMETRY、LINESTRING、POLYGON、MULTIPOINT、MULTILINESTRING、MULTIPOLYGON、GEOMETRYCOLLECTION。

- 对于 String-likes 的数据类型，包括 Varchar、String、VarString、TinyBlob、MediumBlob、BLOB、LongBlob 等，当该列具有 BINARY 标志时，TiCDC 会将其按照 Base64 编码后以 String 类型表示；当该列没有 BINARY 标志时，TiCDC 则直接将其编码为 String 类型。而原生的 Debezium Connector 会根据 `binary.handling.mode` 以不同的编码方式进行编码。

- 对于 Decimal 数据类型，包括 `DECIMAL` 和 `NUMERIC`，TiCDC 均会使用 float64 类型来表示。而原生的 Debezium Connector 会根据数据类型的不同精度采用 float32 或者 float64 的方式进行编码。
