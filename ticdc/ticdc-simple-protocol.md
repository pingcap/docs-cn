---
title: TiCDC Simple Protocol
summary: 本文介绍了 TiCDC Simple Protocol 的使用方法和数据格式实现。
---

# TiCDC Simple Protocol

TiCDC Simple Protocol 是一种行级别的数据变更通知协议，为监控、缓存、全文索引、分析引擎、异构数据库的主从复制等提供数据源。本文将介绍 TiCDC Simple Protocol 的使用方法和数据格式实现。

## 使用方式

当使用 Kafka 作为下游时，你可以在 changefeed 配置中指定 `protocol` 为 `"simple"`，TiCDC 会将每个行变更或者 DDL 事件 (event) 编码为一个 Message，向下游发送数据变更事件。

使用 Simple Protocol 时的配置样例如下所示：

`sink-uri` 配置：

```shell
--sink-uri = "kafka://127.0.0.1:9092/topic-name?kafka-version=2.4.0"
```

changefeed 配置：

```toml
[sink]
protocol = "simple"

# 以下为 Simple Protocol 参数，用来控制 bootstrap 消息的发送行为。
# send-bootstrap-interval-in-sec 用来控制发送 bootstrap 消息的时间间隔，单位为秒。
# 默认值为 120 秒，即每张表每隔 120 秒发送一次 bootstrap 消息。
send-bootstrap-interval-in-sec = 120

# send-bootstrap-in-msg-count 用来控制发送 bootstrap 的消息间隔，单位为消息数。
# 默认值为 10000，即每张表每发送 10000 条行变更消息就发送一次 bootstrap 消息。
send-bootstrap-in-msg-count = 10000
# 注意：如果要关闭 bootstrap 消息的发送，则将 send-bootstrap-interval-in-sec 和 send-bootstrap-in-msg-count 均设置为 0。

# send-bootstrap-to-all-partition 用来控制是否发送 bootstrap 消息到所有的 partition。
# 默认值为 true，即发送 bootstrap 消息到对应表 topic 的所有的 partition。
# 如果设置为 false，则只发送 bootstrap 消息到对应表 topic 的第一个 partition。
send-bootstrap-to-all-partition = true

[sink.kafka-config.codec-config]
# encoding-format 用来控制消息的编码格式，目前支持 "json" 和 "avro" 两种格式。
# 默认值为 "json"。
encoding-format = "json"
```

## Message 类型

TiCDC Simple Protocol 支持如下 Message 类型：

DDL：

- `CREATE`：创建表。
- `RENAME`：重命名表。
- `CINDEX`：创建索引。
- `DINDEX`：删除索引。
- `ERASE`：删除表。
- `TRUNCATE`：清空表。
- `ALTER`：修改表结构，包括增加列、删除列、修改列类型和其他 TiCDC 支持的 `ALTER TABLE` 语句。
- `QUERY`：其他 DDL 语句。

DML：

- `INSERT`：插入事件。
- `UPDATE`：更新事件。
- `DELETE`：删除事件。

其他：

- `WATERMARK`：与上游 TiDB 集群的 TSO 含义相同，包含一个 64 位的 timestamp，用于标记一个表的同步进度，所有早于 watermark 的事件都已经发送给下游。
- `BOOTSTRAP`：包含了一张表的 schema 信息，用于给下游构建表的结构。

## Message 格式

在 Simple Protocol 中，每一个 Message 都只会包含一个事件。当前 Simple Protocol 支持把消息编码为 JSON 格式和 Avro 格式。本文将以 JSON 格式为例进行说明。对于 Avro 格式的消息，其字段和含义与 JSON 格式的消息一致，只是编码格式不同，格式详见 [Simple Protocol Avro Schema](https://github.com/pingcap/tiflow/blob/master/pkg/sink/codec/simple/message.json)。

### DDL

TiCDC 会把一个 DDL 事件编码成如下的 JSON 格式：

```json
{
   "version":1,
   "type":"ALTER",
   "sql":"ALTER TABLE `user` ADD COLUMN `createTime` TIMESTAMP",
   "commitTs":447987408682614795,
   "buildTs":1708936343598,
   "tableSchema":{
      "schema":"simple",
      "table":"user",
      "tableID":148,
      "version":447987408682614791,
      "columns":[
         {
            "name":"id",
            "dataType":{
               "mysqlType":"int",
               "charset":"binary",
               "collate":"binary",
               "length":11
            },
            "nullable":false,
            "default":null
         },
         {
            "name":"name",
            "dataType":{
               "mysqlType":"varchar",
               "charset":"utf8mb4",
               "collate":"utf8mb4_bin",
               "length":255
            },
            "nullable":true,
            "default":null
         },
         {
            "name":"age",
            "dataType":{
               "mysqlType":"int",
               "charset":"binary",
               "collate":"binary",
               "length":11
            },
            "nullable":true,
            "default":null
         },
         {
            "name":"score",
            "dataType":{
               "mysqlType":"float",
               "charset":"binary",
               "collate":"binary",
               "length":12
            },
            "nullable":true,
            "default":null
         },
         {
            "name":"createTime",
            "dataType":{
               "mysqlType":"timestamp",
               "charset":"binary",
               "collate":"binary",
               "length":19
            },
            "nullable":true,
            "default":null
         }
      ],
      "indexes":[
         {
            "name":"primary",
            "unique":true,
            "primary":true,
            "nullable":false,
            "columns":[
               "id"
            ]
         }
      ]
   },
   "preTableSchema":{
      "schema":"simple",
      "table":"user",
      "tableID":148,
      "version":447984074911121426,
      "columns":[
         {
            "name":"id",
            "dataType":{
               "mysqlType":"int",
               "charset":"binary",
               "collate":"binary",
               "length":11
            },
            "nullable":false,
            "default":null
         },
         {
            "name":"name",
            "dataType":{
               "mysqlType":"varchar",
               "charset":"utf8mb4",
               "collate":"utf8mb4_bin",
               "length":255
            },
            "nullable":true,
            "default":null
         },
         {
            "name":"age",
            "dataType":{
               "mysqlType":"int",
               "charset":"binary",
               "collate":"binary",
               "length":11
            },
            "nullable":true,
            "default":null
         },
         {
            "name":"score",
            "dataType":{
               "mysqlType":"float",
               "charset":"binary",
               "collate":"binary",
               "length":12
            },
            "nullable":true,
            "default":null
         }
      ],
      "indexes":[
         {
            "name":"primary",
            "unique":true,
            "primary":true,
            "nullable":false,
            "columns":[
               "id"
            ]
         }
      ]
   }
}
```

以上 JSON 数据的字段解释如下：

| 字段      | 类型   | 说明                                                                      |
| --------- | ------ | ------------------------------------------------------------------------- |
| `version`   | Number    | 协议版本号，目前为 `1`。                                                     |
| `type`      | String | DDL 事件类型，包括 `CREATE`、`RENAME`、`CINDEX`、`DINDEX`、`ERASE`、`TRUNCATE`、`ALTER` 和 `QUERY`。 |
| `sql`       | String | DDL 语句。                                                            |
| `commitTs`  | Number    | 该 DDL 在上游执行结束时的 `commitTs`。                                |
| `buildTs`   | Number    | 该消息在 TiCDC 内部被编码成功时的 UNIX 时间戳。                                |
| `tableSchema` | Object | 表的当前 schema 信息，详见 [TableSchema 定义](#tableschema-定义)。                     |
| `preTableSchema` | Object | DDL 执行前的表的 schema 信息。除了 `CREATE` 类型的 DDL 事件外，其他类型的 DDL 事件都会包含该字段。     |

### DML

#### INSERT

TiCDC 会把一个 `INSERT` 事件编码成如下的 JSON 格式：

```json
{
   "version":1,
   "database":"simple",
   "table":"user",
   "tableID":148,
   "type":"INSERT",
   "commitTs":447984084414103554,
   "buildTs":1708923662983,
   "schemaVersion":447984074911121426,
   "data":{
      "age":"25",
      "id":"1",
      "name":"John Doe",
      "score":"90.5"
   }
}
```

以上 JSON 数据的字段解释如下：

| 字段          | 类型   | 说明                                                                      |
| ------------- | ------ | ------------------------------------------------------------------------- |
| `version`       | Number    | 协议版本号，目前为 `1`。                                                     |
| `database`      | String | 数据库名。                                                                 |
| `table`         | String | 表名。                                                                     |
| `tableID`       | Number    | 表的 ID。                                                                  |
| `type`          | String | DML 事件类型，包括 `INSERT`、`UPDATE` 和 `DELETE`。                              |
| `commitTs`      | Number    | 该 DML 在上游执行结束时的 `commitTs`。                              |
| `buildTs`       | Number    | 该消息在 TiCDC 内部被编码成功时的 UNIX 时间戳。                            |
| `schemaVersion` | Number    | 编码该 DML 消息时所使用表的 schema 版本号。                                |
| `data`          | Object | 插入的数据，字段名为列名，字段值为列值。                                   |

`INSERT` 类型的事件只包含 `data` 字段，不包含 `old` 字段。

#### UPDATE

TiCDC 会把一个 `UPDATE` 事件编码成如下的 JSON 格式：

```json
{
   "version":1,
   "database":"simple",
   "table":"user",
   "tableID":148,
   "type":"UPDATE",
   "commitTs":447984099186180098,
   "buildTs":1708923719184,
   "schemaVersion":447984074911121426,
   "data":{
      "age":"25",
      "id":"1",
      "name":"John Doe",
      "score":"95"
   },
   "old":{
      "age":"25",
      "id":"1",
      "name":"John Doe",
      "score":"90.5"
   }
}
```

以上 JSON 数据的字段解释如下：

| 字段          | 类型   | 说明                                                                      |
| ------------- | ------ | ------------------------------------------------------------------------- |
| `version`       | Number    | 协议版本号，目前为 `1`。                                                     |
| `database`      | String | 数据库名。                                                                 |
| `table`         | String | 表名。                                                                     |
| `tableID`       | Number    | 表的 ID。                                                                  |
| `type`          | String | DML 事件类型，包括 `INSERT`、`UPDATE` 和 `DELETE`。                              |
| `commitTs`      | Number    | 该 DML 在上游执行结束时的 `commitTs`。                         |
| `buildTs`       | Number    | 该消息在 TiCDC 内部被编码成功时的 UNIX 时间戳。                            |
| `schemaVersion` | Number    | 编码该 DML 消息时所使用表的 schema 版本号。                                |
| `data`          | Object | 更新后的数据，字段名为列名，字段值为列值。                                 |
| `old`           | Object | 更新前的数据，字段名为列名，字段值为列值。                                 |

`UPDATE` 类型的事件包含 `data` 和 `old` 两个字段，分别表示更新后的数据和更新前的数据。

#### DELETE

TiCDC 会把一个 `DELETE` 事件编码成如下的 JSON 格式：

```json
{
   "version":1,
   "database":"simple",
   "table":"user",
   "tableID":148,
   "type":"DELETE",
   "commitTs":447984114259722243,
   "buildTs":1708923776484,
   "schemaVersion":447984074911121426,
   "old":{
      "age":"25",
      "id":"1",
      "name":"John Doe",
      "score":"95"
   }
}
```

以上 JSON 数据的字段解释如下：

| 字段          | 类型   | 说明                                                                      |
| ------------- | ------ | ------------------------------------------------------------------------- |
| `version`       | Number    | 协议版本号，目前为 `1`。                                                     |
| `database`      | String | 数据库名。                                                                 |
| `table`         | String | 表名。                                                                     |
| `tableID`       | Number    | 表的 ID。                                                                  |
| `type`          | String | DML 事件类型，包括 `INSERT`、`UPDATE` 和 `DELETE`。                              |
| `commitTs`      | Number    | 该 DML 在上游执行结束的 `commitTs`。                                         |
| `buildTs`       | Number    | 该消息在 TiCDC 内部被编码成功时的 UNIX 时间戳。                            |
| `schemaVersion` | Number    | 编码该 DML 消息时所使用表的 schema 版本号。                                  |
| `old`           | Object | 删除的数据，字段名为列名，字段值为列值。                                   |

`DELETE` 类型的事件只包含 `old` 字段，不包含 `data` 字段。

### WATERMARK

TiCDC 会把一个 `WATERMARK` 事件编码成如下的 JSON 格式：

```json
{
   "version":1,
   "type":"WATERMARK",
   "commitTs":447984124732375041,
   "buildTs":1708923816911
}
```

以上 JSON 数据的字段解释如下：

| 字段      | 类型   | 说明                                                                      |
| --------- | ------ | ------------------------------------------------------------------------- |
| `version`   | Number    | 协议版本号，目前为 `1`。                                                     |
| `type`      | String | WATERMARK 事件类型。                                                       |
| `commitTs`  | Number    | 该 WATERMARK 的 `commitTs`。                                             |
| `buildTs`   | Number    | 该消息在 TiCDC 内部被编码成功时的 UNIX 时间戳。                            |

### BOOTSTRAP

TiCDC 会把一个 `BOOTSTRAP` 事件编码成如下的 JSON 格式：

```json
{
   "version":1,
   "type":"BOOTSTRAP",
   "commitTs":0,
   "buildTs":1708924603278,
   "tableSchema":{
      "schema":"simple",
      "table":"new_user",
      "tableID":148,
      "version":447984074911121426,
      "columns":[
         {
            "name":"id",
            "dataType":{
               "mysqlType":"int",
               "charset":"binary",
               "collate":"binary",
               "length":11
            },
            "nullable":false,
            "default":null
         },
         {
            "name":"name",
            "dataType":{
               "mysqlType":"varchar",
               "charset":"utf8mb4",
               "collate":"utf8mb4_bin",
               "length":255
            },
            "nullable":true,
            "default":null
         },
         {
            "name":"age",
            "dataType":{
               "mysqlType":"int",
               "charset":"binary",
               "collate":"binary",
               "length":11
            },
            "nullable":true,
            "default":null
         },
         {
            "name":"score",
            "dataType":{
               "mysqlType":"float",
               "charset":"binary",
               "collate":"binary",
               "length":12
            },
            "nullable":true,
            "default":null
         }
      ],
      "indexes":[
         {
            "name":"primary",
            "unique":true,
            "primary":true,
            "nullable":false,
            "columns":[
               "id"
            ]
         }
      ]
   }
}
```

以上 JSON 数据的字段解释如下：

| 字段      | 类型   | 说明                                                                      |
| --------- | ------ | ------------------------------------------------------------------------- |
| `version`  | Number    | 协议版本号，目前为 `1`。                                                     |
| `type`      | String | BOOTSTRAP 事件类型。                                                       |
| `commitTs`  | Number    | BOOTSTRAP 的 `commitTs` 为 `0`，因为它是 TiCDC 内部生成的，其 `commitTs` 没有意义。 |
| `buildTs`   | Number    | 该消息在 TiCDC 内部被编码成功时的 UNIX 时间戳。                            |
| `tableSchema` | Object | 表的 schema 信息，详见 [TableSchema 定义](#tableschema-定义)。               |

## Message 生成和发送规则

### DDL

- 生成时机：DDL 事件将会在该 DDL 发生之前的所有事务都被发送完毕后发送。
- 发送目的地：DDL 事件将会被发送到对应 Topic 的所有的 Partition。

### DML

- 生成时机：DML 事件会按照事务的 `commitTs` 顺序被发送。
- 发送目的地：DML 事件将会按照用户配置的 Dispatch 规则发送到对应 Topic 的对应 Partition。

### WATERMARK

- 生成时机：TiCDC 会周期性地发送 WATERMARK 事件，用于标记一个 changefeed 的同步进度，目前的周期为 1 秒。
- 发送目的地：WATERMARK 事件将会被发送到对应 Topic 的所有 Partition。

### BOOTSTRAP

- 生成时机：
    - 创建一个新的 changefeed 后，在一张表的第一条 DML 事件发送之前，TiCDC 会发送 BOOTSTRAP 事件给下游，用于给下游构建表的结构。
    - 此外，TiCDC 会周期性地发送 BOOTSTRAP 事件，以供下游新加入的 consumer 构建表的结构。目前默认每 120 秒或者每间隔 10000 个消息发送一次，可以通过 `sink` 配置项 `send-bootstrap-interval-in-sec` 和 `send-bootstrap-in-msg-count` 来调整发送周期。
    - 如果一张表在 30 分钟内没有收到任何新的 DML 消息，那么该表将被认为是不活跃的。TiCDC 将停止为该表发送 BOOTSTRAP 事件，直到该表收到新的 DML 事件。
- 发送目的地：BOOTSTRAP 事件默认发送到对应 Topic 的所有 Partition，可以通过 `sink` 配置项 `send-bootstrap-to-all-partition` 来调整该发送策略。

## Message 消费方法

由于 Simple Protocol 在发送 DML 消息时没有包含表的 schema 信息，因此在消费一条 DML 消息之前，下游需要先接收到 DDL 或者 BOOTSTRAP 消息，并且把表的 schema 信息缓存起来。在接收到 DML 消息时，通过 DML 消息中的 `table` 名和 `schemaVersion` 字段去缓存中查找对应的 tableSchema 信息，从而正确地消费 DML 消息。

下面介绍如何根据 DDL 或者 BOOTSTRAP 消息来消费 DML 消息。

根据上文描述，已知如下信息：

- 每个 DML 消息都会包含一个 `schemaVersion` 字段，用于标记该 DML 消息对应的表的 schema 版本号。
- 每个 DDL 消息都会包含一个 `tableSchema` 和 `preTableSchema` 字段，用于标记该 DDL 发生前后的表的 schema 信息。
- 每个 BOOTSTRAP 消息都会包含一个 `tableSchema` 字段，用于标记该 BOOTSTRAP 对应的表的 schema 信息。

接下来介绍两种场景下的消费方法。

### 场景一：消费者从头开始消费

在此场景下，消费者从创建表开始消费，因此消费者能够接收到该表的所有 DDL 和 BOOTSTRAP 消息。此时，消费者可以通过一个 DML 消息中的 `table` 名和 `schemaVersion` 字段来获取对应的 tableSchema 信息。具体过程如下图所示：

![TiCDC Simple Protocol consumer scene 1](/media/ticdc/ticdc-simple-consumer-1.png)

### 场景二：消费者从中间开始消费

在一个新的消费者加入到消费者组时，它可能会从中间开始消费，因此它可能会错过之前的 DDL 和 BOOTSTRAP 消息。在这种情况下，消费者可能会先接收到一些 DML 消息，但是此时它还没有该表的 schema 信息。因此，它需要先等待一段时间，直到它接收到该表 DDL 或 BOOTSTRAP 消息，从而获取到该表的 schema 信息。由于 TiCDC 会周期性地发送 BOOTSTRAP 消息，消费者总是能够在一段时间内获取到该表的 schema 信息。具体过程如下图所示：

![TiCDC Simple Protocol consumer scene 2](/media/ticdc/ticdc-simple-consumer-2.png)

## 参考

### TableSchema 定义

TableSchema 是一个 JSON 对象，包含了表的 schema 信息，包括表名、表 ID、表的版本号、列信息和索引信息。其 JSON 消息格式如下：

```json
{
    "schema":"simple",
    "table":"user",
    "tableID":148,
    "version":447984074911121426,
    "columns":[
        {
        "name":"id",
        "dataType":{
            "mysqlType":"int",
            "charset":"binary",
            "collate":"binary",
            "length":11
        },
        "nullable":false,
        "default":null
        },
        {
        "name":"name",
        "dataType":{
            "mysqlType":"varchar",
            "charset":"utf8mb4",
            "collate":"utf8mb4_bin",
            "length":255
        },
        "nullable":true,
        "default":null
        },
        {
        "name":"age",
        "dataType":{
            "mysqlType":"int",
            "charset":"binary",
            "collate":"binary",
            "length":11
        },
        "nullable":true,
        "default":null
        },
        {
        "name":"score",
        "dataType":{
            "mysqlType":"float",
            "charset":"binary",
            "collate":"binary",
            "length":12
        },
        "nullable":true,
        "default":null
        }
    ],
    "indexes":[
        {
        "name":"primary",
        "unique":true,
        "primary":true,
        "nullable":false,
        "columns":[
            "id"
        ]
        }
    ]
}
```

以上 JSON 数据的字段解释如下：

| 字段      | 类型   | 说明                                                                      |
| --------- | ------ | ------------------------------------------------------------------------- |
| `schema`    | String | 数据库名。                                                         |
| `table`     | String | 表名。                                                                     |
| `tableID`   | Number    | 表的 ID。                                                              |
| `version`   | Number    | 表的 schema 版本号。                                                       |
| `columns`   | Array  | 列信息，包括列名、数据类型、是否可为空、默认值等。                         |
| `indexes`   | Array  | 索引信息，包括索引名、是否唯一、是否为主键、索引列等。                       |

你可以通过表名和表的 schema 版本号来唯一标识一张表的 schema 信息。

> **注意：**
>
> 由于 TiDB 的实现限制，在执行 `RENAME TABLE` 的 DDL 操作时，表的 schema 版本号不会发生变化。

#### Column 定义

Column 是一个 JSON 对象，包含了列的 schema 信息，包括列名、数据类型、是否可为空、默认值等。

```json
{
        "name":"id",
        "dataType":{
            "mysqlType":"int",
            "charset":"binary",
            "collate":"binary",
            "length":11
        },
        "nullable":false,
        "default":null
}
```

以上 JSON 数据的字段解释如下：

| 字段      | 类型   | 说明                                                                      |
| --------- | ------ | ------------------------------------------------------------------------- |
| `name`      | String | 列名。                                                                     |
| `dataType`  | Object | 数据类型信息，包括 MySQL 数据类型、字符集、字符序、字段长度。                   |
| `nullable`  | Boolean | 是否可为空。                                                              |
| `default`   | String | 默认值。                                                                   |

#### Index 定义

Index 是一个 JSON 对象，包含了索引的 schema 信息，包括索引名、是否唯一、是否为主键、索引列等。

```json
{
        "name":"primary",
        "unique":true,
        "primary":true,
        "nullable":false,
        "columns":[
            "id"
        ]
}
```

以上 JSON 数据的字段解释如下：

| 字段      | 类型   | 说明                                                                      |
| --------- | ------ | ------------------------------------------------------------------------- |
| `name`      | String | 索引名。                                                                   |
| `unique`    | Boolean | 是否唯一。                                                                |
| `primary`   | Boolean | 是否为主键。                                                                |
| `nullable`  | Boolean | 是否可为空。                                                              |
| `columns`   | Array  | 索引包含的列名。                                                            |

### mysqlType 参考表格

以下表格描述了 TiCDC Simple Protocol 中所有的 `mysqlType` 字段的取值范围及其在 TiDB (Golang) 和 Avro (JAVA) 中的类型。当你需要对 DML 消息进行解析时，取决于你所使用的协议和语言，可以根据该表格和 DML 消息中的 mysqlType 字段来正确地解析数据。

其中，TiDB Type (Golang) 代表了对应 `mysqlType` 在 TiDB 和 TiCDC (Golang) 中处理时的类型，Avro Type (Java) 代表了对应 `mysqlType` 在编码为 Avro 格式消息时的类型。

| mysqlType | 取值范围 | TiDB Type (Golang) | Avro Type (Java) |
| --- | --- | --- | --- |
| tinyint | [-128, 127] | int64 | long |
| tinyint unsigned | [0, 255] | uint64 | long |
| smallint | [-32768, 32767] | int64 | long |
| smallint unsigned | [0, 65535] | uint64 | long |
| mediumint | [-8388608, 8388607] | int64 | long |
| mediumint unsigned | [0, 16777215] | uint64 | long |
| int | [-2147483648, 2147483647] | int64 | long |
| int unsigned | [0, 4294967295] | uint64 | long |
| bigint | [-9223372036854775808, 9223372036854775807] | int64 | long |
| bigint unsigned | [0, 9223372036854775807] | uint64 | long |
| bigint unsigned | [9223372036854775808, 18446744073709551615] | uint64 | string |
| float | / | float32 | float |
| double | / | float64 | double |
| decimal | / | string | string |
| varchar | / | []uint8 | string |
| char | / | []uint8 | string |
| varbinary | / | []uint8 | bytes |
| binary | / | []uint8 | bytes |
| tinytext | / | []uint8 | string |
| text | / | []uint8 | string |
| mediumtext | / | []uint8 | string |
| longtext | / | []uint8 | string |
| tinyblob | / | []uint8 | bytes |
| blob | / | []uint8 | bytes |
| mediumblob | / | []uint8 | bytes |
| longblob | / | []uint8 | bytes |
| date | / | string | string |
| datetime | / | string | string |
| timestamp | / | string | string |
| time | / | string | string |
| year | / | int64 | long |
| enum | / | uint64 | long |
| set | / | uint64 | long |
| bit | / | uint64 | long |
| json | / | string | string |
| bool | / | int64 | long |

### Avro Schema 定义

Simple Protocol 支持输出 Avro 格式的消息，Avro Schema 格式请参考 [Simple Protocol Avro Schema](https://github.com/pingcap/tiflow/blob/master/pkg/sink/codec/simple/message.json)。
