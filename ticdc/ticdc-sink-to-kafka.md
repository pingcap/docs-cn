---
title: 同步数据到 Kafka
summary: 了解如何使用 TiCDC 将数据同步到 Kafka。
---

# 同步数据到 Kafka

本文介绍如何使用 TiCDC 创建一个将增量数据复制到 Kafka 的 Changefeed。

## 创建同步任务，复制增量数据 Kafka

使用以下命令来创建同步任务：

```shell
cdc cli changefeed create \
    --server=http://10.0.10.25:8300 \
    --sink-uri="kafka://127.0.0.1:9092/topic-name?protocol=canal-json&kafka-version=2.4.0&partition-num=6&max-message-bytes=67108864&replication-factor=1" \
    --changefeed-id="simple-replication-task"
```

```shell
Create changefeed successfully!
ID: simple-replication-task
Info: {"sink-uri":"kafka://127.0.0.1:9092/topic-name?protocol=canal-json&kafka-version=2.4.0&partition-num=6&max-message-bytes=67108864&replication-factor=1","opts":{},"create-time":"2020-03-12T22:04:08.103600025+08:00","start-ts":415241823337054209,"target-ts":0,"admin-job-type":0,"sort-engine":"unified","sort-dir":".","config":{"case-sensitive":true,"filter":{"rules":["*.*"],"ignore-txn-start-ts":null,"ddl-allow-list":null},"mounter":{"worker-num":16},"sink":{"dispatchers":null},"scheduler":{"type":"table-number","polling-time":-1}},"state":"normal","history":null,"error":null}
```

- `--server`：TiCDC 集群中任意一个 TiCDC 服务器的地址。
- `--changefeed-id`：同步任务的 ID，格式需要符合正则表达式 `^[a-zA-Z0-9]+(\-[a-zA-Z0-9]+)*$`。如果不指定该 ID，TiCDC 会自动生成一个 UUID（version 4 格式）作为 ID。
- `--sink-uri`：同步任务下游的地址，详见：[Sink URI 配置 Kafka](/ticdc/ticdc-sink-to-kafka.md#sink-uri-配置-kafka)。
- `--start-ts`：指定 changefeed 的开始 TSO。TiCDC 集群将从这个 TSO 开始拉取数据。默认为当前时间。
- `--target-ts`：指定 changefeed 的目标 TSO。TiCDC 集群拉取数据直到这个 TSO 停止。默认为空，即 TiCDC 不会自动停止。
- `--config`：指定 changefeed 配置文件，详见：[TiCDC Changefeed 配置参数](/ticdc/ticdc-changefeed-config.md)。

## Sink URI 配置 `kafka`

Sink URI 用于指定 TiCDC 目标系统的连接信息，遵循以下格式：

```shell
[scheme]://[userinfo@][host]:[port][/path]?[query_parameters]
```

一个通用的配置样例如下所示：

```shell
--sink-uri="kafka://127.0.0.1:9092/topic-name?protocol=canal-json&kafka-version=2.4.0&partition-num=6&max-message-bytes=67108864&replication-factor=1"
```

URI 中可配置的的参数如下：

| 参数               | 描述                                                         |
| :------------------ | :------------------------------------------------------------ |
| `127.0.0.1`          | 下游 Kafka 对外提供服务的 IP。                                 |
| `9092`               | 下游 Kafka 的连接端口。                                          |
| `topic-name`           | 变量，使用的 Kafka topic 名字。                                      |
| `kafka-version`      | 下游 Kafka 版本号（可选，默认值 `2.4.0`，目前支持的最低版本为 `0.11.0.2`，最高版本为 `3.2.0`。该值需要与下游 Kafka 的实际版本保持一致）。 |
| `kafka-client-id`    | 指定同步任务的 Kafka 客户端的 ID（可选，默认值为 `TiCDC_sarama_producer_同步任务的 ID`）。 |
| `partition-num`      | 下游 Kafka partition 数量（可选，不能大于实际 partition 数量，否则创建同步任务会失败，默认值 `3`）。|
| `max-message-bytes`  | 每次向 Kafka broker 发送消息的最大数据量（可选，默认值 `10MB`）。从 v5.0.6 和 v4.0.6 开始，默认值分别从 64MB 和 256MB 调整至 10 MB。|
| `replication-factor` | Kafka 消息保存副本数（可选，默认值 `1`）。                       |
| `required-acks`      | 在 `Produce` 请求中使用的配置项，用于告知 broker 需要收到多少副本确认后才进行响应。可选值有：`0`（`NoResponse`：不发送任何响应，只有 TCP ACK），`1`（`WaitForLocal`：仅等待本地提交成功后再响应）和 `-1`（`WaitForAll`：等待所有同步副本提交后再响应。最小同步副本数量可通过 broker 的 [`min.insync.replicas`](https://kafka.apache.org/33/documentation.html#brokerconfigs_min.insync.replicas) 配置项进行配置）。（可选，默认值为 `-1`）。                      |
| `compression`        | 设置发送消息时使用的压缩算法（可选值为 `none`、`lz4`、`gzip`、`snappy` 和 `zstd`，默认值为 `none`）。|
| `protocol` | 输出到 Kafka 的消息协议，可选值有 `canal-json`、`open-protocol`、`canal`、`avro`、`maxwell`。 |
| `auto-create-topic` | 当传入的 `topic-name` 在 Kafka 集群不存在时，TiCDC 是否要自动创建该 topic（可选，默认值 `true`）。 |
| `enable-tidb-extension` | 可选，默认值是 `false`。当输出协议为 `canal-json` 时，如果该值为 `true`，TiCDC 会发送 [WATERMARK 事件](/ticdc/ticdc-canal-json.md#watermark-event)，并在 Kafka 消息中添加 TiDB 扩展字段。从 6.1.0 开始，该参数也可以和输出协议 `avro` 一起使用。如果该值为 `true`，TiCDC 会在 Kafka 消息中添加[三个 TiDB 扩展字段](/ticdc/ticdc-avro-protocol.md#tidb-扩展字段)。|
| `max-batch-size` |  从 v4.0.9 开始引入。当消息协议支持把多条变更记录输出至一条 Kafka 消息时，该参数用于指定这一条 Kafka 消息中变更记录的最多数量。目前，仅当 Kafka 消息的 `protocol` 为 `open-protocol` 时有效（可选，默认值 `16`）。|
| `enable-tls` | 连接下游 Kafka 实例是否使用 TLS（可选，默认值 `false`）。 |
| `ca`       | 连接下游 Kafka 实例所需的 CA 证书文件路径（可选）。 |
| `cert`     | 连接下游 Kafka 实例所需的证书文件路径（可选）。 |
| `key`      | 连接下游 Kafka 实例所需的证书密钥文件路径（可选）。 |
| `sasl-user` | 连接下游 Kafka 实例所需的 SASL/PLAIN 或 SASL/SCRAM 认证的用户名（authcid）（可选）。 |
| `sasl-password` | 连接下游 Kafka 实例所需的 SASL/PLAIN 或 SASL/SCRAM 认证的密码（可选）。如有特殊字符，需要用 URL encode 转义。 |
| `sasl-mechanism` | 连接下游 Kafka 实例所需的 SASL 认证方式的名称，可选值有 `plain`、`scram-sha-256`、`scram-sha-512` 和 `gssapi`。 |
| `sasl-gssapi-auth-type` | gssapi 认证类型，可选值有 `user` 和 `keytab`（可选）。 |
| `sasl-gssapi-keytab-path` | gssapi keytab 路径（可选）。|
| `sasl-gssapi-kerberos-config-path` | gssapi kerberos 配置路径（可选）。 |
| `sasl-gssapi-service-name` | gssapi 服务名称（可选）。 |
| `sasl-gssapi-user` | gssapi 认证使用的用户名（可选）。 |
| `sasl-gssapi-password` | gssapi 认证使用的密码（可选）。如有特殊字符，需要用 URL encode 转义。 |
| `sasl-gssapi-realm` | gssapi realm 名称（可选）。 |
| `sasl-gssapi-disable-pafxfast` | gssapi 是否禁用 PA-FX-FAST（可选）。 |
| `dial-timeout` | 和下游 Kafka 建立连接的超时时长，默认值为 `10s`。 |
| `read-timeout` | 读取下游 Kafka 返回的 response 的超时时长，默认值为 `10s`。 |
| `write-timeout` | 向下游 Kafka 发送 request 的超时时长，默认值为 `10s`。 |
| `avro-decimal-handling-mode` | 仅在输出协议是 `avro` 时有效。该参数决定了如何处理 DECIMAL 类型的字段，值可以是 `string` 或 `precise`，表明映射成字符串还是浮点数。 |
| `avro-bigint-unsigned-handling-mode` | 仅在输出协议是 `avro` 时有效。该参数决定了如何处理 BIGINT UNSIGNED 类型的字段，值可以是 `string` 或 `long`，表明映射成字符串还是 64 位整形。|

### 最佳实践

* TiCDC 推荐用户自行创建 Kafka Topic，你至少需要设置该 Topic 每次向 Kafka broker 发送消息的最大数据量和下游 Kafka partition 的数量。在创建 changefeed 的时候，这两项设置分别对应 `max-message-bytes` 和 `partition-num` 参数。
* 如果你在创建 changefeed 时，使用了尚未存在的 Topic，那么 TiCDC 会尝试使用 `partition-num` 和 `replication-factor` 参数自行创建 Topic。建议明确指定这两个参数。
* 在大多数情况下，建议使用 `canal-json` 协议。

> **注意：**
>
> 当 `protocol` 为 `open-protocol` 时，TiCDC 会尽量避免产生长度超过 `max-message-bytes` 的消息。但如果单条数据变更记录需要超过 `max-message-bytes` 个字节来表示，为了避免静默失败，TiCDC 会试图输出这条消息并在日志中输出 Warning。

### TiCDC 使用 Kafka 的认证与授权

使用 Kafka 的 SASL 认证时配置样例如下所示：

- SASL/PLAIN

  ```shell
  --sink-uri="kafka://127.0.0.1:9092/topic-name?kafka-version=2.4.0&sasl-user=alice-user&sasl-password=alice-secret&sasl-mechanism=plain"
  ```

- SASL/SCRAM

  SCRAM-SHA-256、SCRAM-SHA-512 与 PLAIN 方式类似，只需要将 `sasl-mechanism` 指定为对应的认证方式即可。

- SASL/GSSAPI

  SASL/GSSAPI `user` 类型认证：

  ```shell
  --sink-uri="kafka://127.0.0.1:9092/topic-name?kafka-version=2.4.0&sasl-mechanism=gssapi&sasl-gssapi-auth-type=user&sasl-gssapi-kerberos-config-path=/etc/krb5.conf&sasl-gssapi-service-name=kafka&sasl-gssapi-user=alice/for-kafka&sasl-gssapi-password=alice-secret&sasl-gssapi-realm=example.com"
  ```

  `sasl-gssapi-user` 和 `sasl-gssapi-realm` 的值与 kerberos 中指定的 [principle](https://web.mit.edu/kerberos/krb5-1.5/krb5-1.5.4/doc/krb5-user/What-is-a-Kerberos-Principal_003f.html) 有关。例如，principle 为 `alice/for-kafka@example.com`，则 `sasl-gssapi-user` 和 `sasl-gssapi-realm` 的值应该分别指定为 `alice/for-kafka` 和 `example.com`。

  SASL/GSSAPI `keytab` 类型认证：

  ```shell
  --sink-uri="kafka://127.0.0.1:9092/topic-name?kafka-version=2.4.0&sasl-mechanism=gssapi&sasl-gssapi-auth-type=keytab&sasl-gssapi-kerberos-config-path=/etc/krb5.conf&sasl-gssapi-service-name=kafka&sasl-gssapi-user=alice/for-kafka&sasl-gssapi-keytab-path=/var/lib/secret/alice.key&sasl-gssapi-realm=example.com"
  ```

  SASL/GSSAPI 认证方式详见 [Configuring GSSAPI](https://docs.confluent.io/platform/current/kafka/authentication_sasl/authentication_sasl_gssapi.html)。

- TLS/SSL 加密

  如果 Kafka broker 启用了 TLS/SSL 加密，则需要在 `--sink-uri` 中增加 `enable-tls=true` 参数值。如果需要使用自签名证书，则还需要在 `--sink-uri` 中指定 `ca`、`cert` 跟 `key` 几个参数。

- ACL 授权

  TiCDC 能够正常工作所需的最小权限集合如下：

    - 对 Topic [资源类型](https://docs.confluent.io/platform/current/kafka/authorization.html#resources)的 `Create` 和 `Write` 权限。
    - 对 Cluster 资源类型的 `DescribeConfigs` 权限。

### TiCDC 集成 Kafka Connect (Confluent Platform)

如要使用 Confluent 提供的 [data connectors](https://docs.confluent.io/current/connect/managing/connectors.html) 向关系型或非关系型数据库传输数据，请选择 `avro` 协议，并在 `schema-registry` 中提供 [Confluent Schema Registry](https://www.confluent.io/product/confluent-platform/data-compatibility/) 的 URL。

配置样例如下所示：

```shell
--sink-uri="kafka://127.0.0.1:9092/topic-name?&protocol=avro&replication-factor=3" --schema-registry="http://127.0.0.1:8081" --config changefeed_config.toml
```

```shell
[sink]
dispatchers = [
 {matcher = ['*.*'], topic = "tidb_{schema}_{table}"},
]
```

集成具体步骤详见[与 Confluent Cloud 进行数据集成](/ticdc/integrate-confluent-using-ticdc.md)。

## 自定义 Kafka Sink 的 Topic 和 Partition 的分发规则

### Matcher 匹配规则

以上一节示例配置文件中的 dispatchers 配置项为例：

- 对于匹配了 matcher 规则的表，按照对应的 topic 表达式指定的策略进行分发。例如表 test3.aa，按照 topic 表达式 2 分发；表 test5.aa，按照 topic 表达式 3 分发。
- 对于匹配了多个 matcher 规则的表，以靠前的 matcher 对应的 topic 表达式为准。例如表 test1.aa，按照 topic 表达式 1 分发。
- 对于没有匹配任何 matcher 的表，将对应的数据变更事件发送到 --sink-uri 中指定的默认 topic 中。例如表 test10.aa 发送到默认 topic。
- 对于匹配了 matcher 规则但是没有指定 topic 分发器的表，将对应的数据变更发送到 --sink-uri 中指定的默认 topic 中。例如表 test6.aa 发送到默认 topic。

### Topic 分发器

Topic 分发器用 topic = "xxx" 来指定，并使用 topic 表达式来实现灵活的 topic 分发策略。topic 的总数建议小于 1000。

Topic 表达式的基本规则为 `[prefix]{schema}[middle][{table}][suffix]`，详细解释如下：

- `prefix`：可选项，代表 Topic Name 的前缀。
- `{schema}`：必选项，用于匹配库名。
- `middle`：可选项，代表库表名之间的分隔符。
- `{table}`：可选项，用于匹配表名。
- `suffix`：可选项，代表 Topic Name 的后缀。

其中 `prefix`、`middle` 以及 `suffix` 仅允许出现大小写字母（`a-z`、`A-Z`）、数字（`0-9`）、点号（`.`）、下划线（`_`）和中划线（`-`）；`{schema}`、`{table}` 均为小写，诸如 `{Schema}` 以及 `{TABLE}` 这样的占位符是无效的。

一些示例如下：

- `matcher = ['test1.table1', 'test2.table2'], topic = "hello_{schema}_{table}"`
    - 对于表 `test1.table1` 对应的数据变更事件，发送到名为 `hello_test1_table1` 的 topic 中
    - 对于表 `test2.table2` 对应的数据变更事件，发送到名为 `hello_test2_table2` 的 topic 中
- `matcher = ['test3.*', 'test4.*'], topic = "hello_{schema}_world"`
    - 对于 `test3` 下的所有表对应的数据变更事件，发送到名为 `hello_test3_world` 的 topic 中
    - 对于 `test4` 下的所有表对应的数据变更事件，发送到名为 `hello_test4_ world` 的 topic 中
- `matcher = ['*.*'], topic = "{schema}_{table}"`
    - 对于 TiCDC 监听的所有表，按照“库名_表名”的规则分别分发到独立的 topic 中；例如对于 `test.account` 表，TiCDC 会将其数据变更日志分发到名为 `test_account` 的 Topic 中。

### DDL 事件的分发

#### 库级别 DDL

诸如 `create database`、`drop database` 这类和某一张具体的表无关的 DDL，称之为库级别 DDL。对于库级别 DDL 对应的事件，被发送到 `--sink-uri` 中指定的默认 topic 中。

#### 表级别 DDL

诸如 `alter table`、`create table` 这类和某一张具体的表相关的 DDL，称之为表级别 DDL。对于表级别 DDL 对应的事件，按照 dispatchers 的配置，被发送到相应的 topic 中。

例如，对于 `matcher = ['test.*'], topic = {schema}_{table}` 这样的 dispatchers 配置，DDL 事件分发情况如下：

- 若 DDL 事件中涉及单张表，则将 DDL 事件原样发送到相应的 topic 中。
    - 对于 DDL 事件 `drop table test.table1`，该事件会被发送到名为 `test_table1` 的 topic 中。
- 若 DDL 事件中涉及多张表（`rename table` / `drop table` / `drop view` 都可能涉及多张表），则将单个 DDL 事件拆分为多个发送到相应的 topic 中。
    - 对于 DDL 事件 `rename table test.table1 to test.table10, test.table2 to test.table20`，则将 `rename table test.table1 to test.table10` 的 DDL 事件发送到名为 `test_table1` 的 topic 中，将 `rename table test.table2 to test.table20` 的 DDL 事件发送到名为 `test.table2` 的 topic 中。

### Partition 分发器

partition 分发器用 partition = "xxx" 来指定，支持 default、ts、index-value、table 四种 partition 分发器，分发规则如下：

- default：有多个唯一索引（包括主键）时按照 table 模式分发；只有一个唯一索引（或主键）按照 index-value 模式分发；如果开启了 old value 特性，按照 table 分发
- ts：以行变更的 commitTs 做 Hash 计算并进行 event 分发
- index-value：以表的主键或者唯一索引的值做 Hash 计算并进行 event 分发
- table：以表的 schema 名和 table 名做 Hash 计算并进行 event 分发

> **注意：**
>
> 从 v6.1 开始，为了明确配置项的含义，用来指定 partition 分发器的配置项由原来的 `dispatcher` 改为 `partition`，`partition` 为 `dispatcher` 的别名。例如，以下两条规则完全等价：
>
> ```
> [sink]
> dispatchers = [
>    {matcher = ['*.*'], dispatcher = "ts"},
>    {matcher = ['*.*'], partition = "ts"},
> ]
> ```
>
> 但是 `dispatcher` 与 `partition` 不能出现在同一条规则中。例如，以下规则非法：
>
> ```
> {matcher = ['*.*'], dispatcher = "ts", partition = "table"},
> ```

## 横向扩展大单表的负载到多个 TiCDC 节点

该功能通过将大单表按 Region 个数切分成多个数据范围，将这些数据范围分布到多个 TiCDC 节点上，使得多个 TiCDC 节点可以同时同步大单表。该功能可以解决以下两个问题：

- 单个 TiCDC 节点不能及时同步大单表。
- TiCDC 节点之间资源（CPU、内存等）消耗不均匀。

> **警告：**
>
> TiCDC v7.0.0 仅支持在 Kafka 同步任务上开启大单表的横向扩展功能。

配置样例如下所示：

```toml
[scheduler]
# 设置为 "true" 以打开该功能。
enable-table-across-nodes = true
# 打开该功能后，该功能只对 Region 个数大于 `region-threshold` 值的表生效。
region-threshold = 100000
```

一个表包含的 Region 个数可用如下 SQL 查询：

```sql
SELECT COUNT(*) FROM INFORMATION_SCHEMA.TIKV_REGION_STATUS WHERE DB_NAME="database1" AND TABLE_NAME="table1" AND IS_INDEX=0;
```
