---
title: TiCDC Debezium Protocol
summary: 了解 TiCDC Debezium Protocol 的概念和使用方法。
---

# TiCDC Debezium Protocol

[Debezium](https://debezium.io/) 一种数据库变更数据捕获的工具，它会将捕获的数据库变更的每一条记录转化为一个被称为"事件"的消息，并将这些事件发送到 Kafka 中。 为了便利在数据链路中已经使用 Debezium 的用户，TiCDC 支持将 TiDB 的变更以 Debezium 的格式直接传输到 Kafka，来简化用户下游消费的数据链路。

## 使用 Debezium 消息格式

当使用 Kafka 作为下游 Sink 的时候，你可以在 `sink-uri` 中指定使用 Debezium，TiCDC 将以 Event 为基本单位封装构造 Debezium Message，向下游发送 TiDB 的数据变更事件。

TiCDC Debezium Protocol 以 Event 为基本单位向下游复制数据变更事件，目前 Debezium 协议只支持 Row Changed Event。Row Changed Event：代表一行的数据变化，在行发生变更时该 Event 被发出，包含该行在变更前后的相关信息。对于 DDL Event 和 WATERMARK Event 目前 Debezium 协议会直接忽略。

使用 `Debezium` 时的配置样例如下所示：

```shell
cdc cli changefeed create --server=http://127.0.0.1:8300 --changefeed-id="kafka-debezium" --sink-uri="kafka://127.0.0.1:9092/topic-name?kafka-version=2.4.0&protocol=debezium"
```

同时在 Debezium 输出格式中我们包含当前行的 Schema 信息，以便于下游消费者能够更好的理解当前行的数据结构。对于不需要输出 Schema 信息的场景，我们也可以通过在 changefeed 的配置文件或者 `sink-uri` 中将 `debezium-disable-schema` 参数设置为 true 来关闭 Schema 信息的输出。

另外，Debezium 原有格式其中并不包含 TiDB 专有的 CommitTS 事务唯一标识等重要字段。为了保证数据的完整性，TiCDC 在 Debezium 格式中增加了 CommitTs 和 ClusterID 两个字段，用于标识 TiDB 数据变更的相关信息。

## Message 格式定义

下面将介绍 Debezium 格式输出的 DML Event 的格式定义。

### DML Event

TiCDC 会把一个 DML Event 编码成如下格式:

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
| payload.op        | String | "c"表示这是一个 insert ，"u"表示这是一个 update，"d”表示这是一个 delete          |
| payload.ts_ms     | Number | 记录的是 TiCDC 生成这条信息的时间戳（ms 级别）                                |
| payload.before    | JSON   | 记录的是这条事件语句变更前该语句的值的情况，对于 "c" 事件，before 字段为 null     |
| payload.after     | JSON   | 记录的是这条事件语句变更后该语句的值的情况，对于 "d" 事件，after 字段为 null     |
| payload.source.commit_ts     | Number   | 记录的是 TiCDC 生成这条信息的 CommitTs 标识                    |
| payload.source.db     | String   | 记录的是对应事件发生的数据库的名称                    |
| payload.source.table     | String   |  记录的是对应事件发生的数据表的名称                    |
| schema.fields     | JSON   |  记录了 payload 中各个字段的类型信息，包括对应行数据变更前后 schema 的信息等      |

### 数据类型映射

消息中的数据格式映射基本遵循 https://debezium.io/documentation/reference/2.4/connectors/mysql.html#mysql-data-types 的数据类型映射规则，大体与 Debezium Connector 原生的 Message 保持一致。但是对于部分数据类型，TiCDC Debezium 的处理方式与 Debezium Connector Message 存在一定差异，具体如下：

1. 目前 TiDB 不支持空间数据类型，包括 GEOMETRY, LINESTRING, POLYGON, MULTIPOINT, MULTILINESTRING, MULTIPOLYGON, GEOMETRYCOLLECTION。

2. 对于 String-likes 的数据类型，包括 Varchar, String, VarString, TinyBlob, MediumBlob, BLOB, LongBlob 等, 当该列具有 BINARY 标志是，TiCDC 会将其按照 Base64 编码后以 String 类型表示。如果没有则直接编码为 String 类型。 而原生的 Debezium Connector 会根据 binary.handling.mode 以不同的编码方式进行编码。

3. 对于 Decimal 数据类型，TiCDC 均会使用 float64 类型来表示，包括 DECIMAL, NUMERIC。对于原生的 Debezium Connector，根据数据类型的不同精度会采用 float32 或者 float 64 的方式进行编码。