---
title: TiCDC Avro Protocol
summary: 了解 TiCDC Avro Protocol 的概念和使用方法。
---

# TiCDC Avro Protocol

Avro 是由 [Apache Avro™](https://avro.apache.org/) 定义的一种数据交换格式协议，[Confluent Platform](https://docs.confluent.io/platform/current/platform.html) 选择它作为默认的数据交换格式。通过本文，你可以了解 TiCDC 对 Avro 数据格式的实现，包括 TiDB 扩展字段、Avro 数据格式定义，以及和 [Confluent Schema Registry](https://docs.confluent.io/platform/current/schema-registry/index.html) 的交互。

## 使用 Avro

当使用 Message Queue (MQ) 作为下游 Sink 时，你可以在 `sink-uri` 中指定使用 Avro。TiCDC 获取 TiDB 的 DML 事件，并将这些事件封装到 Avro Message，然后发送到下游。当 Avro 检测到 schema 变化时，会向 Schema Registry 注册最新的 schema。

使用 Avro 时的配置样例如下所示：

{{< copyable "shell-regular" >}}

```shell
cdc cli changefeed create --pd=http://127.0.0.1:2379 --changefeed-id="kafka-avro" --sink-uri="kafka://127.0.0.1:9092/topic-name?protocol=avro" --schema-registry=http://127.0.0.1:8081 --config changefeed_config.toml
```

```shell
[sink]
dispatchers = [
 {matcher = ['*.*'], topic = "tidb_{schema}_{table}"},
]
```

`--schema-registry` 的值支持 https 协议和 username:password 认证，比如`--schema-registry=https://username:password@schema-registry-uri.com`，username 和 password 必须经过 URL 编码。

## TiDB 扩展字段

默认情况下，Avro 只收集在 DML 事件中发生数据变更的行的所有数据信息，不收集数据变更的类型和 TiDB 专有的 CommitTS 事务唯一标识信息。为了解决这个问题，TiCDC 在 Avro 协议格式中附加了 TiDB 扩展字段。当 `sink-uri` 中设置 `enable-tidb-extension` 为 `true` （默认为 `false`）后，TiCDC 生成 Avro 消息时会新增三个字段：

- `_tidb_op`：DML 的类型，"c" 表示插入，"u" 表示更新。
- `_tidb_commit_ts`：事务唯一标识信息。
- `_tidb_commit_physical_time`：事务标识信息中现实时间的时间戳。

配置样例如下所示：

{{< copyable "shell-regular" >}}

```shell
cdc cli changefeed create --pd=http://127.0.0.1:2379 --changefeed-id="kafka-avro-enable-extension" --sink-uri="kafka://127.0.0.1:9092/topic-name?protocol=avro&enable-tidb-extension=true" --schema-registry=http://127.0.0.1:8081 --config changefeed_config.toml
```

 ```shell
 [sink]
 dispatchers = [
  {matcher = ['*.*'], topic = "tidb_{schema}_{table}"},
 ]
 ```

## 数据格式定义

TiCDC 会将一个 DML 事件转换为一个 kafka 事件，其中事件的 key 和 value 都按照 Avro 协议进行编码。

### Key 数据格式

```
{
    "name":"{{TableName}}",
    "namespace":"{{Namespace}}",
    "type":"record",
    "fields":[
        {{ColumnValueBlock}},
        {{ColumnValueBlock}},
    ]
}
```

- `{{TableName}}` 是事件来源表的名称。
- `{{Namespace}}` 是 Avro 的命名空间。
- `{{ColumnValueBlock}}` 是每列数据的格式定义。

Key 中的 `fields` 只包含主键或唯一索引列。

### Value 数据格式

```
{
    "name":"{{TableName}}",
    "namespace":"{{Namespace}}",
    "type":"record",
    "fields":[
        {{ColumnValueBlock}},
        {{ColumnValueBlock}},
    ]
}
```

Value 数据格式默认与 Key 数据格式相同，但是 Value 的 `fields` 中包含了所有的列，而不仅仅是主键列。

如果开启了 [TiDB 扩展字段](#tidb-扩展字段)，那么 Value 数据格式将会变成：

```
{
    "name":"{{TableName}}",
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

- `{{ColumnName}}` 表示列名。
- `{{TIDB_TYPE}}` 表示对应到 TiDB 中的类型，与原始的 SQL Type 不是一一对应关系。
- `{{AVRO_TYPE}}` 表示 [avro spec](https://avro.apache.org/docs/current/spec.html) 中的类型。

| SQL TYPE   | TIDB_TYPE | AVRO_TYPE | 说明                                                                                                               |
|------------|-----------|-----------|---------------------------------------------------------------------------------------------------------------------------|
| BOOL       | INT       | int       |                                                                                                                           |
| TINYINT    | INT       | int       | 当 TINYINT 为无符号值时，TIDB_TYPE 为 INT UNSIGNED。                                                                            |
| SMALLINT   | INT       | int       | 当 SMALLINT 为无符号值时，TIDB_TYPE 为 INT UNSIGNED.                                                                            |
| MEDIUMINT  | INT       | int       | 当 MEDIUMINT 为无符号值时，TIDB_TYPE 为 INT UNSIGNED。                                                                            |
| INT        | INT       | int       | 当 INT 为无符号值时，TIDB_TYPE 为 INT UNSIGNED，AVRO_TYPE 为 long。                                                      |
| BIGINT     | BIGINT    | long      | 当 BIGINT 为无符号值时，TIDB_TYPE 为 BIGINT UNSIGNED。当 `avro-bigint-unsigned-handling-mode` 为 string 时，AVRO_TYPE 也为 string。 |
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
| DECIMAL    | DECIMAL   | bytes     | 当 `avro-decimal-handling-mode` 为 string 时，AVRO_TYPE 也为 string。                                                         |

对于 Avro 协议，另外两个 `sink-uri` 参数 `avro-decimal-handling-mode` 和 `avro-bigint-unsigned-handling-mode` 也会影响 Column 数据格式:

- `avro-decimal-handling-mode` 决定了如何处理 DECIMAL 字段，它有两个选项：

    - string：Avro 将 DECIMAL 字段以 string 的方式处理。
    - precise：Avro 将 DECIMAL 字段以字节的方式处理。

- `avro-bigint-unsigned-handling-mode` 决定了如何处理 BIGINT UNSIGNED 字段，它有两个选项：

    - string：Avro 将 BIGINT UNSIGNED 字段以 string 的方式处理。
    - long：Avro 将 BIGINT UNSIGNED 字段以 64 位有符号整数处理，大于 9223372036854775807 的值会发生溢出。

配置样例如下所示：

{{< copyable "shell-regular" >}}

```shell
cdc cli changefeed create --pd=http://127.0.0.1:2379 --changefeed-id="kafka-avro-string-option" --sink-uri="kafka://127.0.0.1:9092/topic-name?protocol=avro&avro-decimal-handling-mode=string&avro-bigint-unsigned-handling-mode=string" --schema-registry=http://127.0.0.1:8081 --config changefeed_config.toml
```

```shell
[sink]
dispatchers = [
 {matcher = ['*.*'], topic = "tidb_{schema}_{table}"},
]
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

## DDL 事件与 Schema 变更

Avro 并不会向下游生成 DDL 事件。Avro 会在每次 DML 事件发生时检测是否发生 schema 变更，如果发生了 schema 变更，Avro 会生成新的 schema，并尝试向 Schema Registry 注册。注册时，Schema Registry 会做兼容性检测，如果此次 schema 变更没有通过兼容性检测，注册将会失败，Avro 并不会尝试解决 schema 的兼容性问题。

同时，即使 schema 变更通过兼容性检测并成功注册新版本，数据的生产者和消费者可能仍然需要升级才能正确工作。

比如，Confluent Schema Registry 默认的兼容性策略是 BACKWARD，在这种策略下，如果你在源表增加一个非空列，Avro 在生成新 schema 向 Schema Registry 注册时将会因为兼容性问题失败，这个时候 changefeed 将会进入 error 状态。

如需了解更多 schema 相关信息，请参阅 [Schema Registry 的相关文档](https://docs.confluent.io/platform/current/schema-registry/avro.html)。

## Topic 分发

Schema Registry 支持三种 [Subject Name Strategy](https://docs.confluent.io/platform/current/schema-registry/serdes-develop/index.html#subject-name-strategy)：TopicNameStrategy、RecordNameStrategy 和 TopicRecordNameStrategy。目前 TiCDC Avro 只支持 TopicNameStrategy 一种，这意味着一个 kafka topic 只能接收一种数据格式的数据，所以 TiCDC Avro 禁止将多张表映射到同一个 topic。在创建 changefeed 时，如果配置的分发规则中，topic 规则不包含 `{schema}` 和 `{table}` 占位符，将会报错。
