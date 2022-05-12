---
title: TiCDC Avro Protocol
summary: 了解 TiCDC Avro Protocol 的概念和使用方法。
---

# TiCDC Avro Protocol

Avro 是由 [Apache Avro™](https://avro.apache.org/) 定义的一种数据交换格式协议，被 [Confluent Platform](https://docs.confluent.io/platform/current/platform.html) 选择作为默认的数据交换格式。通过本文，你可以了解 TiCDC 对 Avro 数据格式的实现，包括 TiDB 扩展字段、Avro 数据格式定义，以及和 [Confluent Schema Registry](https://docs.confluent.io/platform/current/schema-registry/index.html) 的交互。

## 使用 Avro

当使用 MQ (Message Queue) 作为下游 Sink 时，你可以在 `sink-uri` 中指定使用 Avro，TiCDC 将以 Event 为基本单位封装构造 Avro Message，向下游发送 TiDB 的数据变更事件。当 Avro 检测到 schema 变化时，会向 Schema Registry 注册最新的 schema。

使用 Avro 时的配置样例如下所示：

{{< copyable "shell-regular" >}}

```shell
cdc cli changefeed create --pd=http://127.0.0.1:2379 --changefeed-id="kafka-avro" --sink-uri="kafka://127.0.0.1:9092/topic-name?kafka-version=2.6.0&protocol=avro" --schema-registry=http://127.0.0.1:8081
```

`protocol` 除了可以是 `avro`，还可以是 `flat-avro`。`flat-avro` 是 `avro` 的别名。

## TiDB 扩展字段

默认情况下，Avro 只会在数据变更事件中囊括发生数据变更的行中的所有数据信息，不包括数据变更的类型和 TiDB 专有的 CommitTS 事务唯一标识信息。为了解决这个问题，TiCDC 在 Avro 协议格式中附加了 TiDB 扩展字段。在 `sink-uri` 中设置 `enable-tidb-extension` 为 `true` 后，TiCDC 生成 Avro 消息时会新增三个字段：

* `_tidb_op` 字段，表示数据变更的类型，"c" 表示插入，"u" 表示更新。
* `_tidb_commit_ts` 字段，事务唯一标识信息。
* `_tidb_commit_physical_time` 字段，事务标识信息中的现实时间时间戳。

配置样例如下所示：

{{< copyable "shell-regular" >}}

```shell
cdc cli changefeed create --pd=http://127.0.0.1:2379 --changefeed-id="kafka-avro-enable-extension" --sink-uri="kafka://127.0.0.1:9092/topic-name?kafka-version=2.6.0&protocol=avro&enable-tidb-extension=true" --schema-registry=http://127.0.0.1:8081
```

`enable-tidb-extension` 默认为 `false`。

## 数据格式定义

TiCDC 会将一个数据变更事件转换为一个 kafka 事件，其中事件的 key 和 value 都按照 Avro 协议进行编码。

### Key 数据格式

```
{
    "name":"{{RecordName}}",
    "namespace":"{{Namespace}}",
    "type":"record",
    "fields":[
        {{ColumnValueBlock}},
        {{ColumnValueBlock}},
    ]
}
```

* `{{RecordName}}` 是事件来源表的名称。
* `{{Namespace}}` 是 changefeed namespace。
* `{{ColumnValueBlock}}` 是每列数据的格式定义。

Key 中的由主键列组成。

### Value 数据格式

```
{
    "name":"{{RecordName}}",
    "namespace":"{{Namespace}}",
    "type":"record",
    "fields":[
        {{ColumnValueBlock}},
        {{ColumnValueBlock}},
    ]
}
```

Value 数据格式默认与 Key 数据格式相同，但是 Value 的 `fields` 中包含了所有的列，而不仅仅是主键列。

如果打开了 TiDB 扩展字段选项，那么 Value 数据格式将会变成

```
{
    "name":"{{RecordName}}",
    "namespace":"{{Namespace}}",
    "type":"record",
    "fields":[
        {{ColumnValueBlock}},
        {{ColumnValueBlock}},
        {
            "name":"_tidb_op",
            "type":"string"
        },
        {
            "name":"_tidb_commit_ts",
            "type":"long"
        },
        {
            "name":"_tidb_commit_physical_time",
            "type":"long"
        }
    ]
}
```

相比于不打开 TiDB 扩展字段选项，多出了 `_tidb_op`, `_tidb_commit_ts`, `_tidb_commit_physical_time` 三个字段的定义。

### Column 数据格式

Column 数据格式即 Key/Value 数据格式中的 `{{ColumnValueBlock}}` 部分，TiCDC 会根据 SQL Type 生成对应的 Column 数据格式。基础的 Column 数据格式是：

```
{
    "name":"{{ColumnName}}",
    "type":{
        "connect.parameters":{
            "tidb_type":"{{TIDB_TYPE}}"
        },
        "type":"{{AVRO_TYPE}}"
    }
}
```

如果一列可以为 NULL，那么 Column 数据格式是：

```
{
    "default":null,
    "name":"{{ColumnName}}",
    "type":[
        "null",
        {
            "connect.parameters":{
                "tidb_type":"{{TIDB_TYPE}}"
            },
            "type":"{{AVRO_TYPE}}"
        }
    ]
}
```

* `{{ColumnName}}` 表示列名。
* `{{TIDB_TYPE}}` 表示对应到 TiDB 中的类型，与原始的 SQL Type 不是一一对应关系。
* `{{AVRO_TYPE}}` 表示 [avro spec](https://avro.apache.org/docs/current/spec.html) 中的类型。

| SQL TYPE   | TIDB_TYPE | AVRO_TYPE | 说明                                                                                                               |
|------------|-----------|-----------|---------------------------------------------------------------------------------------------------------------------------|
| BOOL       | INT       | int       |                                                                                                                           |
| TINYINT    | INT       | int       | When it's unsigned, TIDB_TYPE is INT UNSIGNED.                                                                            |
| SMALLINT   | INT       | int       | When it's unsigned, TIDB_TYPE is INT UNSIGNED.                                                                            |
| MEDIUMINT  | INT       | int       | When it's unsigned, TIDB_TYPE is INT UNSIGNED.                                                                            |
| INT        | INT       | int       | When it's unsigned, TIDB_TYPE is INT UNSIGNED and AVRO_TYPE is long.                                                      |
| BIGINT     | BIGINT    | long      | When it's unsigned, TIDB_TYPE is BIGINT UNSIGNED. If `avro-bigint-unsigned-handling-mode` is string, AVRO_TYPE is string. |
| TINYBLOB   | BLOB      | bytes     |                                                                                                                           |
| BLOB       | BLOB      | bytes     |                                                                                                                           |
| MEDIUMBLOB | BLOB      | bytes     |                                                                                                                           |
| LONGBLOB   | BLOB      | bytes     |                                                                                                                           |
| BINARY     | BLOB      | bytes     |                                                                                                                           |
| VARBINARY  | BLOB      | bytes     |                                                                                                                           |
| TINYTEXT   | TEXT      | string    |                                                                                                                           |
| TEXT       | TEXT      | string    |                                                                                                                           |
| MEDIUMTEXT | TEXT      | string    |                                                                                                                           |
| LONGTEXT   | TEXT      | string    |                                                                                                                           |
| CHAR       | TEXT      | string    |                                                                                                                           |
| VARCHAR    | TEXT      | string    |                                                                                                                           |
| FLOAT      | FLOAT     | double    |                                                                                                                           |
| DOUBLE     | DOUBLE    | double    |                                                                                                                           |
| DATE       | DATE      | string    |                                                                                                                           |
| DATETIME   | DATETIME  | string    |                                                                                                                           |
| TIMESTAMP  | TIMESTAMP | string    |                                                                                                                           |
| TIME       | TIME      | string    |                                                                                                                           |
| YEAR       | YEAR      | int       |                                                                                                                           |
| BIT        | BIT       | bytes     |                                                                                                                           |
| JSON       | JSON      | string    |                                                                                                                           |
| ENUM       | ENUM      | string    |                                                                                                                           |
| SET        | SET       | string    |                                                                                                                           |
| DECIMAL    | DECIMAL   | bytes     | When `avro-decimal-handling-mode` is string, AVRO_TYPE is string.                                                         |

对于 Avro 协议，还有另外两个 `sink-uri` 参数: `avro-decimal-handling-mode` 和 `avro-bigint-unsigned-handling-mode`，影响着 Column 数据格式:

* `avro-decimal-handling-mode` 决定了如何处理 DECIMAL 字段，它有两个选项，string 和 precise。如果是 precise，Avro 会将它以字节的方式存储；如果是 string，则会以 string 的方式处理。
* `avro-bigint-unsigned-handling-mode` 决定了如何处理 BIGINT UNSIGNED 字段，它有两个选项，string 和 long。如果是 long，Avro 会将它以 64 位有符号整数处理，这意味着值可能会溢出；如果是 string，则会以 string 的方式处理。

配置样例如下所示：

{{< copyable "shell-regular" >}}

```shell
cdc cli changefeed create --pd=http://127.0.0.1:2379 --changefeed-id="kafka-avro-enable-extension" --sink-uri="kafka://127.0.0.1:9092/topic-name?kafka-version=2.6.0&protocol=avro&avro-decimal-handling-mode=string&avro-bigint-unsigned-handling-mode=string" --schema-registry=http://127.0.0.1:8081
```

大多数的 SQL Type 都会映射成基础的 Column 数据格式，但有一些类型会在基础数据格式上拓展，提供更多的信息。

BIT(64)
```
{
    "name":"{{ColumnName}}",
    "type":{
        "connect.parameters":{
            "tidb_type":"BIT",
            "length":"64"
        },
        "type":"bytes"
    }
}
```

ENUM/SET(a,b,c)
```
{
    "name":"{{ColumnName}}",
    "type":{
        "connect.parameters":{
            "tidb_type":"ENUM/SET",
            "allowed":"a,b,c"
        },
        "type":"string"
    }
}
```

DECIMAL(10, 4)
```
{
    "default":null,
    "name":"{{ColumnName}}",
    "type":{
        "connect.parameters":{
            "tidb_type":"DECIMAL",
        },
        "logicalType":"decimal",
        "precision":10,
        "scale":4,
        "type":"bytes"
    }
}
```

## 格式变更

Avro 并不会向下游生成格式变更事件。Avro 会在每次事件变更时检测是否发生格式变更，如果发生了格式变更，Avro 会生成新的格式，并尝试向 Schema Registry 注册。在注册时，Schema Registry 会做兼容性检测，如果此次格式变更没有通过兼容性检测，注册将会失败，Avro 并不会尝试解决格式的兼容性问题。同时，即使通过兼容性检测并成功注册新版本，Avro 生产者和消费者可能仍然需要进行升级才能正确工作。详情请查看 [Schema Registry 的相关资料](https://docs.confluent.io/platform/current/schema-registry/avro.html)。

## Topic 分发

Schema Registry 支持三种 [Subject Name Strategy](https://docs.confluent.io/platform/current/schema-registry/serdes-develop/index.html#subject-name-strategy)，目前 TiCDC Avro 只支持 TopicNameStrategy 一种，这意味着一个 kafka topic 只能接收一种数据格式的数据，所以 TiCDC Avro 禁止将多张表映射到同一个 topic。在创建 changefeed 时，如果配置中的分发规则配种中，topic 规则不包含 `{schema}` 和 `{table}` 占位符，将会报错。