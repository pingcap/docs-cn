---
title: TiCDC Debezium Protocol
summary: 了解 TiCDC Debezium Protocol 的概念和使用方法。
---

# TiCDC Debezium Protocol

[Debezium](https://debezium.io/) 是一个用于捕获数据库变更的工具。它会将捕获的数据库变更的每一条记录转化为一个被称为“事件” (event) 的消息 (message)，并将这些事件发送到 Kafka 中。从 v8.0.0 起，TiCDC 支持将 TiDB 的变更以 Debezium 的格式直接传输到 Kafka，为之前使用 Debezium 的 MySQL 集成的用户简化了从 MySQL 数据库迁移的过程。从 v9.0.0 起，TiCDC 支持 DDL 事件和 WATERMARK 事件。

## 使用 Debezium 消息格式

当使用 Kafka 作为下游 Sink 时，你可以将 `sink-uri` 的 `protocol` 字段指定为 `debezium`，TiCDC 将以 event 为基本单位封装构造 Debezium 消息，向下游发送 TiDB 的数据变更事件。

Debezium 协议支持以下类型的事件：

- DDL 事件：表示 DDL 变更记录。在上游 DDL 语句成功执行后，DDL 事件被发送到索引为 0 的 MQ 分区。
- DML 事件：表示一行数据变更记录。在行变更发生时，DML 事件被发出，包含变更后该行的相关信息。
- WATERMARK 事件：表示一个特殊的时间点。在这个时间点之前收到的事件是完整的。仅适用于 TiDB 扩展字段，当你在 `sink-uri` 中设置 `enable-tidb-extension` 为 `true` 时生效。

使用 Debezium 消息格式时的配置样例如下所示：

```shell
cdc cli changefeed create --server=http://127.0.0.1:8300 --changefeed-id="kafka-debezium" --sink-uri="kafka://127.0.0.1:9092/topic-name?kafka-version=2.4.0&protocol=debezium"
```

Debezium 输出格式中包含当前行的 Schema 信息，以便下游消费者更好地理解当前行的数据结构。对于不需要输出 Schema 信息的场景，也可以通过在 changefeed 的配置文件或者 `sink-uri` 中将 `debezium-disable-schema` 参数设置为 `true` 来关闭 Schema 信息的输出。

此外，Debezium 原有格式中并不包含 TiDB 专有的 `CommitTS` 事务唯一标识等重要字段。为了保证数据的完整性，TiCDC 在 Debezium 格式中增加了 `CommitTs` 和 `ClusterID` 两个字段，用于标识 TiDB 数据变更的相关信息。

## 消息格式定义

本节介绍 DDL 事件、DML 事件和 WATERMARK 事件的消息格式。

### DDL 事件

TiCDC 会将一个 DDL 事件转换为一条 Kafka 消息，其中消息的 key 和 value 都按照 Debezium 协议进行编码。

#### Key 数据格式

```json
{
    "payload": {
        "databaseName": "test"
    },
    "schema": {
        "type": "struct",
        "name": "io.debezium.connector.mysql.SchemaChangeKey",
        "optional": false,
        "version": 1,
        "fields": [
            {
                "field": "databaseName",
                "optional": false,
                "type": "string"
            }
        ]
    }
}
```

Key 中的字段仅包含数据库名称。字段解释如下：

| 字段           | 类型       | 说明                                           |
|:--------------|:-----------|:---------------------------------------------|
| `payload`        | JSON    | 数据库名称。 |
| `schema.fields`  | JSON    | `payload` 中各个字段的类型信息。 |
| `schema.type`    | 字符串  | 字段类型。                      |
| `schema.optional` | 布尔值 | 该字段是否为选填项。值为 `true` 表示该字段为选填项。  |
| `schema.version`   | 字符串  | schema 的版本。                             |

#### Value 数据格式

```json
{
    "payload": {
        "source": {
            "version": "2.4.0.Final",
            "connector": "TiCDC",
            "name": "test_cluster",
            "ts_ms": 0,
            "snapshot": "false",
            "db": "test",
            "table": "table1",
            "server_id": 0,
            "gtid": null,
            "file": "",
            "pos": 0,
            "row": 0,
            "thread": 0,
            "query": null,
            "commit_ts": 1,
            "cluster_id": "test_cluster"
        },
        "ts_ms": 1701326309000,
        "databaseName": "test",
        "schemaName": null,
        "ddl": "RENAME TABLE test.table1 to test.table2",
        "tableChanges": [
            {
                "type": "ALTER",
                "id": "\"test\".\"table2\",\"test\".\"table1\"",
                "table": {
                    "defaultCharsetName": "",
                    "primaryKeyColumnNames": [
                        "id"
                    ],
                    "columns": [
                        {
                            "name": "id",
                            "jdbcType": 4,
                            "nativeType": null,
                            "comment": null,
                            "defaultValueExpression": null,
                            "enumValues": null,
                            "typeName": "INT",
                            "typeExpression": "INT",
                            "charsetName": null,
                            "length": 0,
                            "scale": null,
                            "position": 1,
                            "optional": false,
                            "autoIncremented": false,
                            "generated": false
                        }
                    ],
                    "comment": null
                }
            }
        ]
    },
    "schema": {
        "optional": false,
        "type": "struct",
        "version": 1,
        "name": "io.debezium.connector.mysql.SchemaChangeValue",
        "fields": [
            {
                "field": "source",
                "name": "io.debezium.connector.mysql.Source",
                "optional": false,
                "type": "struct",
                "fields": [
                    {
                        "field": "version",
                        "optional": false,
                        "type": "string"
                    },
                    {
                        "field": "connector",
                        "optional": false,
                        "type": "string"
                    },
                    {
                        "field": "name",
                        "optional": false,
                        "type": "string"
                    },
                    {
                        "field": "ts_ms",
                        "optional": false,
                        "type": "int64"
                    },
                    {
                        "field": "snapshot",
                        "optional": true,
                        "type": "string",
                        "parameters": {
                            "allowed": "true,last,false,incremental"
                        },
                        "default": "false",
                        "name": "io.debezium.data.Enum",
                        "version": 1
                    },
                    {
                        "field": "db",
                        "optional": false,
                        "type": "string"
                    },
                    {
                        "field": "sequence",
                        "optional": true,
                        "type": "string"
                    },
                    {
                        "field": "table",
                        "optional": true,
                        "type": "string"
                    },
                    {
                        "field": "server_id",
                        "optional": false,
                        "type": "int64"
                    },
                    {
                        "field": "gtid",
                        "optional": true,
                        "type": "string"
                    },
                    {
                        "field": "file",
                        "optional": false,
                        "type": "string"
                    },
                    {
                        "field": "pos",
                        "optional": false,
                        "type": "int64"
                    },
                    {
                        "field": "row",
                        "optional": false,
                        "type": "int32"
                    },
                    {
                        "field": "thread",
                        "optional": true,
                        "type": "int64"
                    },
                    {
                        "field": "query",
                        "optional": true,
                        "type": "string"
                    }
                ]
            },
            {
                "field": "ts_ms",
                "optional": false,
                "type": "int64"
            },
            {
                "field": "databaseName",
                "optional": true,
                "type": "string"
            },
            {
                "field": "schemaName",
                "optional": true,
                "type": "string"
            },
            {
                "field": "ddl",
                "optional": true,
                "type": "string"
            },
            {
                "field": "tableChanges",
                "optional": false,
                "type": "array",
                "items": {
                    "name": "io.debezium.connector.schema.Change",
                    "optional": false,
                    "type": "struct",
                    "version": 1,
                    "fields": [
                        {
                            "field": "type",
                            "optional": false,
                            "type": "string"
                        },
                        {
                            "field": "id",
                            "optional": false,
                            "type": "string"
                        },
                        {
                            "field": "table",
                            "optional": true,
                            "type": "struct",
                            "name": "io.debezium.connector.schema.Table",
                            "version": 1,
                            "fields": [
                                {
                                    "field": "defaultCharsetName",
                                    "optional": true,
                                    "type": "string"
                                },
                                {
                                    "field": "primaryKeyColumnNames",
                                    "optional": true,
                                    "type": "array",
                                    "items": {
                                        "type": "string",
                                        "optional": false
                                    }
                                },
                                {
                                    "field": "columns",
                                    "optional": false,
                                    "type": "array",
                                    "items": {
                                        "name": "io.debezium.connector.schema.Column",
                                        "optional": false,
                                        "type": "struct",
                                        "version": 1,
                                        "fields": [
                                            {
                                                "field": "name",
                                                "optional": false,
                                                "type": "string"
                                            },
                                            {
                                                "field": "jdbcType",
                                                "optional": false,
                                                "type": "int32"
                                            },
                                            {
                                                "field": "nativeType",
                                                "optional": true,
                                                "type": "int32"
                                            },
                                            {
                                                "field": "typeName",
                                                "optional": false,
                                                "type": "string"
                                            },
                                            {
                                                "field": "typeExpression",
                                                "optional": true,
                                                "type": "string"
                                            },
                                            {
                                                "field": "charsetName",
                                                "optional": true,
                                                "type": "string"
                                            },
                                            {
                                                "field": "length",
                                                "optional": true,
                                                "type": "int32"
                                            },
                                            {
                                                "field": "scale",
                                                "optional": true,
                                                "type": "int32"
                                            },
                                            {
                                                "field": "position",
                                                "optional": false,
                                                "type": "int32"
                                            },
                                            {
                                                "field": "optional",
                                                "optional": true,
                                                "type": "boolean"
                                            },
                                            {
                                                "field": "autoIncremented",
                                                "optional": true,
                                                "type": "boolean"
                                            },
                                            {
                                                "field": "generated",
                                                "optional": true,
                                                "type": "boolean"
                                            },
                                            {
                                                "field": "comment",
                                                "optional": true,
                                                "type": "string"
                                            },
                                            {
                                                "field": "defaultValueExpression",
                                                "optional": true,
                                                "type": "string"
                                            },
                                            {
                                                "field": "enumValues",
                                                "optional": true,
                                                "type": "array",
                                                "items": {
                                                    "type": "string",
                                                    "optional": false
                                                }
                                            }
                                        ]
                                    }
                                },
                                {
                                    "field": "comment",
                                    "optional": true,
                                    "type": "string"
                                }
                            ]
                        }
                    ]
                }
            }
        ]
    }
}
```

以上 JSON 数据的重点字段解释如下：

| 字段      | 类型   | 说明                                            |
|:----------|:-------|:-------------------------------------------------------|
| `payload.ts_ms`     | 数值 | TiCDC 生成这条信息的时间戳（毫秒级别）。 |
| `payload.ddl`    | 字符串   | DDL 事件的 SQL 语句。               |
| `payload.databaseName`     | 字符串   | 事件发生的数据库的名称。    |
| `payload.source.commit_ts`     | 数值  | TiCDC 生成此消息时的 `CommitTs` 标识符。   |
| `payload.source.db`     | 字符串   | 事件发生的数据库的名称。    |
| `payload.source.table`     | 字符串  |  事件发生的数据表的名称。   |
| `payload.tableChanges` | 数组 | 在 schema 变更后的整个表 schema 的结构化表示。`tableChanges` 字段包含一个数组，其中包括表中每一列的条目。由于结构化表示以 JSON 或 Avro 格式呈现数据，因此消费者可以在不通过 DDL 解析器处理的情况下轻松读取消息。 |
| `payload.tableChanges.type`     | 字符串   | 描述变更的类型。值为以下之一：`CREATE`，表示表已创建；`ALTER`，表示表已修改；`DROP`，表示表已删除。 |
| `payload.tableChanges.id`     | 字符串   | 被创建、修改或删除的表的完整标识符。如果是表重命名，则该标识符是 <code>&lt;old&gt;</code> 和 <code>&lt;new&gt;</code> 表名的拼接。 |
| `payload.tableChanges.table.defaultCharsetName` | 字符串   | 事件发生的表的字符集。 |
| `payload.tableChanges.table.primaryKeyColumnNames` | 字符串   | 组成表主键的列的名称列表。 |
| `payload.tableChanges.table.columns` | 数组   | 变更的表中每一列的元数据。 |
| `payload.tableChanges.table.columns.name` | 字符串   | 列的名称。 |
| `payload.tableChanges.table.columns.jdbcType` | 数值 | 列的 JDBC 类型。 |
| `payload.tableChanges.table.columns.comment` | 字符串 | 列的注释。 |
| `payload.tableChanges.table.columns.defaultValueExpression` | 字符串 | 列的默认值。 |
| `payload.tableChanges.table.columns.enumValues` | 字符串 | 列的枚举值。格式为 `ENUM ('e1', 'e2')` 或 `SET ('e1', 'e2')`。 |
| `payload.tableChanges.table.columns.charsetName` | 字符串 | 列的字符集。 |
| `payload.tableChanges.table.columns.length` | 数值 | 列的长度。 |
| `payload.tableChanges.table.columns.scale` | 数值 | 列的精度。 |
| `payload.tableChanges.table.columns.position` | 数值 | 列的位置。 |
| `payload.tableChanges.table.columns.optional` | 布尔值 | 是否为可选列。值为 `true` 表示为可选列。 |
| `schema.fields`     | JSON   | `payload` 每个字段的类型信息，包括变更表的列 schema 信息。   |
| `schema.name`     | 字符串  | schema 的名称，格式为 `"{cluster-name}.{schema-name}.{table-name}.SchemaChangeValue"`。 |
| `schema.optional` | 布尔值 | 该字段是否为选填项。值为 `true` 表示该字段为选填项。  |
| `schema.type`     | 字符串  | 字段的数据类型。 |

### DML 事件

TiCDC 会将一个 DML 事件转换为一条 Kafka 消息，其中消息的 key 和 value 都按照 Debezium 协议进行编码。

#### Key 数据格式

```json
{
    "payload": {
        "tiny": 1
    },
    "schema": {
        "fields": [
        {
            "field":"tiny",
            "optional":true,
            "type":"int16"
        }
        ],
        "name": "test_cluster.test.table1.Key",
        "optional": false,
        "type":"struct"
    }
}
```

Key 中的字段只包含主键或唯一索引列。字段解释如下：

| 字段      | 类型   | 说明                                                                      |
|:----------|:-------|:-------------------------------------------------------------------------|
| `payload``   | JSON | 主键或唯一索引列的信息。每个字段的 key 和 value 分别为列名和当前值。  |
| `schema.fields`   | JSON   |  `payload` 中各个字段的类型信息，包括对应行数据变更前后 schema 的信息。  |
| `schema.name`     | 字符串  |  schema 的名称，格式为 `"{cluster-name}.{schema-name}.{table-name}.Key"`。 |
| `schema.optional` | 布尔值  | 该字段是否为选填项。值为 `true` 表示该字段为选填项。  |
| `schema.type`     | 字符串  |  字段的数据类型。   |

#### Value 数据格式

```json
{
    "payload": {
        "source": {
            "version": "2.4.0.Final",
            "connector": "TiCDC",
            "name": "test_cluster",
            "ts_ms": 0,
            "snapshot": "false",
            "db": "test",
            "table": "table1",
            "server_id": 0,
            "gtid": null,
            "file": "",
            "pos": 0,
            "row": 0,
            "thread": 0,
            "query": null,
            "commit_ts": 1,
            "cluster_id": "test_cluster"
        },
        "ts_ms": 1701326309000,
        "transaction": null,
        "op": "u",
        "before": { "tiny": 2 },
        "after": { "tiny": 1 }
    },
    "schema": {
        "type": "struct",
        "optional": false,
        "name": "test_cluster.test.table1.Envelope",
        "version": 1,
        "fields": [
            {
                "type": "struct",
                "optional": true,
                "name": "test_cluster.test.table1.Value",
                "field": "before",
                "fields": [{ "type": "int16", "optional": true, "field": "tiny" }]
            },
            {
                "type": "struct",
                "optional": true,
                "name": "test_cluster.test.table1.Value",
                "field": "after",
                "fields": [{ "type": "int16", "optional": true, "field": "tiny" }]
            },
            {
                "type": "struct",
                "fields": [
                    { "type": "string", "optional": false, "field": "version" },
                    { "type": "string", "optional": false, "field": "connector" },
                    { "type": "string", "optional": false, "field": "name" },
                    { "type": "int64", "optional": false, "field": "ts_ms" },
                    {
                        "type": "string",
                        "optional": true,
                        "name": "io.debezium.data.Enum",
                        "version": 1,
                        "parameters": { "allowed": "true,last,false,incremental" },
                        "default": "false",
                        "field": "snapshot"
                    },
                    { "type": "string", "optional": false, "field": "db" },
                    { "type": "string", "optional": true, "field": "sequence" },
                    { "type": "string", "optional": true, "field": "table" },
                    { "type": "int64", "optional": false, "field": "server_id" },
                    { "type": "string", "optional": true, "field": "gtid" },
                    { "type": "string", "optional": false, "field": "file" },
                    { "type": "int64", "optional": false, "field": "pos" },
                    { "type": "int32", "optional": false, "field": "row" },
                    { "type": "int64", "optional": true, "field": "thread" },
                    { "type": "string", "optional": true, "field": "query" }
                ],
                "optional": false,
                "name": "io.debezium.connector.mysql.Source",
                "field": "source"
            },
            { "type": "string", "optional": false, "field": "op" },
            { "type": "int64", "optional": true, "field": "ts_ms" },
            {
                "type": "struct",
                "fields": [
                    { "type": "string", "optional": false, "field": "id" },
                    { "type": "int64", "optional": false, "field": "total_order" },
                    {
                        "type": "int64",
                        "optional": false,
                        "field": "data_collection_order"
                    }
                ],
                "optional": true,
                "name": "event.block",
                "version": 1,
                "field": "transaction"
            }
        ]
    }
}
```

以上 JSON 数据的重点字段解释如下：

| 字段      | 类型   | 说明                                                                      |
|:----------|:-------|:-------------------------------------------------------------------------|
| `payload.op`   | 字符串 | 变更事件类型。`"c"` 表示 `INSERT` 事件，`"u"` 表示 `UPDATE` 事件，`"d"` 表示 `DELETE` 事件。 |
| `payload.ts_ms`     | 数值 | TiCDC 生成这条信息的时间戳（毫秒级别）。                                |
| `payload.before`    | JSON   | 这条事件语句变更前的数据值。对于 `"c"` 事件，`before` 字段的值为 `null`。  |
| `payload.after`     | JSON   | 这条事件语句变更后的数据值。对于 `"d"` 事件，`after` 字段的值为 `null`。   |
| `payload.source.commit_ts`     | 数值  | TiCDC 生成此消息时的 `CommitTs` 标识符。                    |
| `payload.source.db`     | 字符串   | 事件发生的数据库的名称。                    |
| `payload.source.table`     | 字符串  |  事件发生的数据表的名称。                   |
| `schema.fields`     | JSON   |  `payload` 中各个字段的类型信息，包括对应行数据变更前后 schema 的信息。      |
| `schema.name`     | 字符串   |  schema 的名称，格式为 `"{cluster-name}.{schema-name}.{table-name}.Envelope"`。     |
| `schema.optional`     | 布尔值   |  该字段是否为选填项。值为 `true` 表示该字段为选填项。   |
| `schema.type`     | 字符串   |  字段的类型。   |

### WATERMARK 事件

TiCDC 会将一个 WATERMARK 事件转换为一条 Kafka 消息，其中消息的 key 和 value 都按照 Debezium 协议进行编码。

#### Key 数据格式

```json
{
    "payload": {},
    "schema": {
        "fields": [],
        "optional": false,
        "name": "test_cluster.watermark.Key",
        "type": "struct"
    }
}
```

Key 中的字段解释如下：

| 字段      | 类型   | 说明                                                               |
|:-----------|:--------|:---------------------------------------------------------------|
| `schema.name`   | 字符串  | schema 的名称，格式为 `"{cluster-name}.watermark.Key"`。 |

#### Value 数据格式

```json
{
    "payload": {
        "source": {
            "version": "2.4.0.Final",
            "connector": "TiCDC",
            "name": "test_cluster",
            "ts_ms": 0,
            "snapshot": "false",
            "db": "",
            "table": "",
            "server_id": 0,
            "gtid": null,
            "file": "",
            "pos": 0,
            "row": 0,
            "thread": 0,
            "query": null,
            "commit_ts": 3,
            "cluster_id": "test_cluster"
        },
        "op": "m",
        "ts_ms": 1701326309000,
        "transaction": null
    },
    "schema": {
        "type": "struct",
        "optional": false,
        "name": "test_cluster.watermark.Envelope",
        "version": 1,
        "fields": [
            {
                "type": "struct",
                "fields": [
                    {
                        "type": "string",
                        "optional": false,
                        "field": "version"
                    },
                    {
                        "type": "string",
                        "optional": false,
                        "field": "connector"
                    },
                    {
                        "type": "string",
                        "optional": false,
                        "field": "name"
                    },
                    {
                        "type": "int64",
                        "optional": false,
                        "field": "ts_ms"
                    },
                    {
                        "type": "string",
                        "optional": true,
                        "name": "io.debezium.data.Enum",
                        "version": 1,
                        "parameters": {
                            "allowed": "true,last,false,incremental"
                        },
                        "default": "false",
                        "field": "snapshot"
                    },
                    {
                        "type": "string",
                        "optional": false,
                        "field": "db"
                    },
                    {
                        "type": "string",
                        "optional": true,
                        "field": "sequence"
                    },
                    {
                        "type": "string",
                        "optional": true,
                        "field": "table"
                    },
                    {
                        "type": "int64",
                        "optional": false,
                        "field": "server_id"
                    },
                    {
                        "type": "string",
                        "optional": true,
                        "field": "gtid"
                    },
                    {
                        "type": "string",
                        "optional": false,
                        "field": "file"
                    },
                    {
                        "type": "int64",
                        "optional": false,
                        "field": "pos"
                    },
                    {
                        "type": "int32",
                        "optional": false,
                        "field": "row"
                    },
                    {
                        "type": "int64",
                        "optional": true,
                        "field": "thread"
                    },
                    {
                        "type": "string",
                        "optional": true,
                        "field": "query"
                    }
                ],
                "optional": false,
                "name": "io.debezium.connector.mysql.Source",
                "field": "source"
            },
            {
                "type": "string",
                "optional": false,
                "field": "op"
            },
            {
                "type": "int64",
                "optional": true,
                "field": "ts_ms"
            },
            {
                "type": "struct",
                "fields": [
                    {
                        "type": "string",
                        "optional": false,
                        "field": "id"
                    },
                    {
                        "type": "int64",
                        "optional": false,
                        "field": "total_order"
                    },
                    {
                        "type": "int64",
                        "optional": false,
                        "field": "data_collection_order"
                    }
                ],
                "optional": true,
                "name": "event.block",
                "version": 1,
                "field": "transaction"
            }
        ]
    }
}
```

以上 JSON 数据的重点字段解释如下：

| 字段      | 类型   | 说明                                                                      |
|:----------|:-------|:-------------------------------------------------------------------------|
| `payload.op`   | 字符串 | 变更事件类型。`"m"` 表示 WATERMARK 事件。                                |
| `payload.ts_ms`     | 数值 | TiCDC 生成这条信息的时间戳（毫秒级别）。                                |
| `payload.source.commit_ts`     | 数值  | TiCDC 生成此消息时的 `CommitTs` 标识符。     |
| `payload.source.db`     | 字符串   | 事件发生的数据库的名称。                    |
| `payload.source.table`     | 字符串  |  事件发生的数据表的名称。                   |
| `schema.fields`     | JSON   |  `payload` 中各个字段的类型信息，包括对应行数据变更前后 schema 的信息。      |
| `schema.name`     | 字符串   |  schema 的名称，格式为 `"{cluster-name}.watermark.Envelope"`。     |
| `schema.optional`     | 布尔值   |  该字段是否为选填项。值为 `true` 表示该字段为选填项。   |
| `schema.type`     | 字符串   |  字段的类型。   |

### 数据类型映射

TiCDC Debezium 消息中的数据格式映射基本遵循 [Debezium 的数据类型映射规则](https://debezium.io/documentation/reference/2.4/connectors/mysql.html#mysql-data-types)，与 Debezium Connector for MySQL 原生消息大体一致。但是对于部分数据类型，TiCDC Debezium 的处理方式与 Debezium Connector Message 存在一定差异，具体如下：

- 目前 TiDB 不支持空间数据类型，包括 GEOMETRY、LINESTRING、POLYGON、MULTIPOINT、MULTILINESTRING、MULTIPOLYGON、GEOMETRYCOLLECTION。

- 对于 String-likes 的数据类型，包括 Varchar、String、VarString、TinyBlob、MediumBlob、BLOB、LongBlob 等，当该列具有 BINARY 标志时，TiCDC 会将其按照 Base64 编码后以 String 类型表示；当该列没有 BINARY 标志时，TiCDC 则直接将其编码为 String 类型。而原生的 Debezium Connector 会根据 `binary.handling.mode` 以不同的编码方式进行编码。

- 对于 Decimal 数据类型，包括 DECIMAL 和 NUMERIC，TiCDC 均会使用 float64 类型来表示。而原生的 Debezium Connector 会根据数据类型的不同精度采用 float32 或者 float64 的方式进行编码。

- TiCDC 将 REAL 转换为 DOUBLE；当长度为 1 时，将 BOOLEAN 转换为 TINYINT(1)。

- 在 TiCDC 中，BLOB、TEXT、GEOMETRY、JSON 列没有默认值。

- Debezium 将 FLOAT 类型的 "5.61" 转换为 "5.610000133514404"，但 TiCDC 不会。

- TiCDC 在处理 FLOAT 时打印了错误的 `flen` [tidb#57060](https://github.com/pingcap/tidb/issues/57060)。

- 当列的排序规则为 `utf8_unicode_ci` 且字符集为 null 时，Debezium 将 `charsetName` 转换为 `"utf8mb4"`，但 TiCDC 不会。

- Debezium 会对 ENUM 元素进行转义，但 TiCDC 不会。例如，Debezium 将 ENUM 元素 ('c', 'd', 'g,''h') 编码为 ('c','d','g,\'\'h')。

- TiCDC 将 TIME 类型的默认值如 '1000-00-00 01:00:00.000' 转换为 "1000-00-00"，但 Debezium 不会。
