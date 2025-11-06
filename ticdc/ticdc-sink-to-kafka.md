---
title: 同步数据到 Kafka
summary: 了解如何使用 TiCDC 将数据同步到 Kafka。
---

# 同步数据到 Kafka

本文介绍如何使用 TiCDC 创建一个将增量数据复制到 Kafka 的 Changefeed。

## 创建同步任务，复制增量数据到 Kafka

使用以下命令来创建同步任务：

```shell
cdc cli changefeed create \
    --server=http://10.0.10.25:8300 \
    --sink-uri="kafka://127.0.0.1:9092,127.0.0.1:9093,127.0.0.1:9094/topic-name?protocol=canal-json&kafka-version=2.4.0&partition-num=6&max-message-bytes=67108864&replication-factor=1" \
    --changefeed-id="simple-replication-task"
```

```shell
Create changefeed successfully!
ID: simple-replication-task
Info: {"sink-uri":"kafka://127.0.0.1:9092,127.0.0.1:9093,127.0.0.1:9094/topic-name?protocol=canal-json&kafka-version=2.4.0&partition-num=6&max-message-bytes=67108864&replication-factor=1","opts":{},"create-time":"2023-11-28T22:04:08.103600025+08:00","start-ts":415241823337054209,"target-ts":0,"admin-job-type":0,"sort-engine":"unified","sort-dir":".","config":{"case-sensitive":false,"filter":{"rules":["*.*"],"ignore-txn-start-ts":null,"ddl-allow-list":null},"mounter":{"worker-num":16},"sink":{"dispatchers":null},"scheduler":{"type":"table-number","polling-time":-1}},"state":"normal","history":null,"error":null}
```

- `--server`：TiCDC 集群中任意一个 TiCDC 服务器的地址。
- `--changefeed-id`：同步任务的 ID，格式需要符合正则表达式 `^[a-zA-Z0-9]+(\-[a-zA-Z0-9]+)*$`。如果不指定该 ID，TiCDC 会自动生成一个 UUID（version 4 格式）作为 ID。
- `--sink-uri`：同步任务下游的地址，详见：[Sink URI 配置 Kafka](/ticdc/ticdc-sink-to-kafka.md#sink-uri-配置-kafka)。
- `--start-ts`：指定 changefeed 的开始 TSO。TiCDC 集群将从这个 TSO 开始拉取数据。默认为当前时间。
- `--target-ts`：指定 changefeed 的目标 TSO。TiCDC 集群拉取数据直到这个 TSO 停止。默认为空，即 TiCDC 不会自动停止。
- `--config`：指定 changefeed 配置文件，详见：[TiCDC Changefeed 配置参数](/ticdc/ticdc-changefeed-config.md)。

## 支持的 Kafka 版本

TiCDC 与支持的 Kafka 最低版本对应关系如下：

| TiCDC 版本               | 支持的 Kafka 最低版本 |
| :-----------------------| :------------------ |
| TiCDC >= v8.1.0          | 2.1.0              |
| v7.6.0 <= TiCDC < v8.1.0 | 2.4.0              |
| v7.5.2 <= TiCDC < v7.6.0 | 2.1.0              |
| v7.5.0 <= TiCDC < v7.5.2 | 2.4.0              |
| v6.5.0 <= TiCDC < v7.5.0 | 2.1.0              |
| v6.1.0 <= TiCDC < v6.5.0 | 2.0.0              |

## Sink URI 配置 `kafka`

Sink URI 用于指定 TiCDC 目标系统的连接信息，遵循以下格式：

```shell
[scheme]://[host]:[port][/path]?[query_parameters]
```

> **Tip:**
>
> 如果下游 Kafka 有多个主机或端口，可以在 Sink URI 中配置多个 `[host]:[port]`。例如：
>
> ```shell
> [scheme]://[host]:[port],[host]:[port],[host]:[port][/path]?[query_parameters]
> ```

一个通用的配置样例如下所示：

```shell
--sink-uri="kafka://127.0.0.1:9092/topic-name?protocol=canal-json&kafka-version=2.4.0&partition-num=6&max-message-bytes=67108864&replication-factor=1"
```

URI 中可配置的的参数如下：

| 参数               | 描述                                                         |
| :------------------ | :------------------------------------------------------------ |
| `host`              | 下游 Kafka 对外提供服务的 IP。                                 |
| `port`               | 下游 Kafka 的连接端口。                                          |
| `topic-name`         | 变量，使用的 Kafka topic 名字。                                      |
| `protocol`           | 输出到 Kafka 的消息协议。可选值有 [`canal-json`](/ticdc/ticdc-canal-json.md)、[`open-protocol`](/ticdc/ticdc-open-protocol.md)、[`avro`](/ticdc/ticdc-avro-protocol.md)、[`debezium`](/ticdc/ticdc-debezium.md) 和 [`simple`](/ticdc/ticdc-simple-protocol.md)。 |
| `kafka-version`      | 下游 Kafka 版本号。该值需要与下游 Kafka 的实际版本保持一致。 |
| `kafka-client-id`    | 指定同步任务的 Kafka 客户端的 ID（可选，默认值为 `TiCDC_sarama_producer_同步任务的 ID`）。 |
| `partition-num`      | 下游 Kafka partition 数量（可选，不能大于实际 partition 数量，否则创建同步任务会失败，默认值 `3`）。|
| `max-message-bytes`  | 每次向 Kafka broker 发送消息的最大数据量（可选，默认值 `10MB`，最大值为 `100MB`）。从 v5.0.6 和 v4.0.6 开始，默认值分别从 `64MB` 和 `256MB` 调整至 `10MB`。|
| `replication-factor` | Kafka 消息保存副本数（可选，默认值 `1`），需要大于等于 Kafka 中 [`min.insync.replicas`](https://kafka.apache.org/33/documentation.html#brokerconfigs_min.insync.replicas) 的值。 |
| `required-acks`      | 在 `Produce` 请求中使用的配置项，用于告知 broker 需要收到多少副本确认后才进行响应。可选值有：`0`（`NoResponse`：不发送任何响应，只有 TCP ACK），`1`（`WaitForLocal`：仅等待本地提交成功后再响应）和 `-1`（`WaitForAll`：等待所有同步副本提交后再响应。最小同步副本数量可通过 broker 的 [`min.insync.replicas`](https://kafka.apache.org/33/documentation.html#brokerconfigs_min.insync.replicas) 配置项进行配置）。（可选，默认值为 `-1`）。                      |
| `compression`        | 设置发送消息时使用的压缩算法（可选值为 `none`、`lz4`、`gzip`、`snappy` 和 `zstd`，默认值为 `none`）。注意 Snappy 压缩文件必须遵循[官方 Snappy 格式](https://github.com/google/snappy)。不支持其他非官方压缩格式。|
| `auto-create-topic` | 当传入的 `topic-name` 在 Kafka 集群不存在时，TiCDC 是否要自动创建该 topic（可选，默认值 `true`）。 |
| `enable-tidb-extension` | 可选，默认值是 `false`。当输出协议为 `canal-json` 时，如果该值为 `true`，TiCDC 会发送 [WATERMARK 事件](/ticdc/ticdc-canal-json.md#watermark-event)，并在 Kafka 消息中添加 TiDB 扩展字段。从 6.1.0 开始，该参数也可以和输出协议 `avro` 一起使用。如果该值为 `true`，TiCDC 会在 Kafka 消息中添加[三个 TiDB 扩展字段](/ticdc/ticdc-avro-protocol.md#tidb-扩展字段)。|
| `max-batch-size` |  从 v4.0.9 开始引入。当消息协议支持把多条变更记录输出至一条 Kafka 消息时，该参数用于指定这一条 Kafka 消息中变更记录的最多数量。目前，仅当 Kafka 消息的 `protocol` 为 `open-protocol` 时有效（可选，默认值 `16`）。|
| `enable-tls` | 连接下游 Kafka 实例是否使用 TLS（可选，默认值 `false`）。 |
| `ca`       | 连接下游 Kafka 实例所需的 CA 证书文件路径（可选）。 |
| `cert`     | 连接下游 Kafka 实例所需的证书文件路径（可选）。 |
| `key`      | 连接下游 Kafka 实例所需的证书密钥文件路径（可选）。 |
| `insecure-skip-verify` | 连接下游 Kafka 实例时是否跳过证书验证（可选，默认值 `false`）。 |
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
| `avro-bigint-unsigned-handling-mode` | 仅在输出协议是 `avro` 时有效。该参数决定了如何处理 BIGINT UNSIGNED 类型的字段，值可以是 `string` 或 `long`，表明映射成字符串还是 64 位整型。|

### 最佳实践

* TiCDC 推荐用户自行创建 Kafka Topic，你至少需要设置该 Topic 每次向 Kafka broker 发送消息的最大数据量和下游 Kafka partition 的数量。在创建 changefeed 的时候，这两项设置分别对应 `max-message-bytes` 和 `partition-num` 参数。
* 如果你在创建 changefeed 时，使用了尚未存在的 Topic，那么 TiCDC 会尝试使用 `partition-num` 和 `replication-factor` 参数自行创建 Topic，建议明确指定这两个参数。
* 在大多数情况下，建议使用 `canal-json` 协议。
* 如果 TiCDC 上游的数据变更很少，比如可能会出现超过 10 分钟没有数据变更的情况，建议在 Kafka broker 的配置文件中调大 Kafka 的连接空闲超时时间，详情参考[为什么 TiCDC 同步到 Kafka 的任务经常因 `broken pipe` 报错而失败](/ticdc/ticdc-faq.md#为什么-ticdc-同步到-kafka-的任务经常因-broken-pipe-报错而失败)。

> **注意：**
>
> 当 `protocol` 为 `open-protocol` 时，TiCDC 会将多个事件编码到同一个 Kafka 消息中，并尽量避免在此过程中生成长度超过 `max-message-bytes` 的消息。
> 如果单条数据变更编码得到的消息大小超过了 `max-message-bytes` 个字节，changefeed 会报错，并打印错误日志。

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

    - 对 Topic [资源类型](https://docs.confluent.io/platform/current/kafka/authorization.html#resources)的 `Create` 、`Write` 和 `Describe` 权限。
    - 对 Cluster 资源类型的 `DescribeConfig` 权限。

  各权限的使用场景如下：
  
    | 资源类型 | 操作类型      |  使用场景                            |
    | :-------------| :------------- | :--------------------------------|
    | Cluster      | `DescribeConfig` | Changefeed 运行过程中，获取集群元数据 |
    | Topic         | `Describe`           | Changefeed 启动时，尝试创建 Topic   |                
    | Topic         | `Create`              | Changefeed 启动时，尝试创建 Topic   |
    | Topic         | `Write`                | 发送数据到 Topic                   | 

    创建或启动 Changefeed 时，如果指定的 Kafka Topic 已存在，可以不用开启 `Describe` 和 `Create` 权限。

### TiCDC 集成 Kafka Connect (Confluent Platform)

如要使用 Confluent 提供的 [data connectors](https://docs.confluent.io/current/connect/managing/connectors.html) 向关系型或非关系型数据库传输数据，请选择 [Avro 协议](/ticdc/ticdc-avro-protocol.md)协议，并在 `schema-registry` 中提供 [Confluent Schema Registry](https://www.confluent.io/product/confluent-platform/data-compatibility/) 的 URL。

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

### TiCDC 集成 AWS Glue Schema Registry

从 v7.4.0 开始，TiCDC 支持在用户选择  [Avro 协议](/ticdc/ticdc-avro-protocol.md)同步数据时使用 [AWS Glue Schema Registry](https://docs.aws.amazon.com/glue/latest/dg/schema-registry.html) 作为 Schema Registry。配置样例如下所示：

```shell
./cdc cli changefeed create --server=127.0.0.1:8300 --changefeed-id="kafka-glue-test" --sink-uri="kafka://127.0.0.1:9092/topic-name?&protocol=avro&replication-factor=3" --config changefeed_glue.toml
```

```toml
[sink]
[sink.kafka-config.glue-schema-registry-config]
region="us-west-1"
registry-name="ticdc-test"
access-key="xxxx"
secret-access-key="xxxx"
token="xxxx"
```

在以上配置中，`region` 和 `registry-name` 是必填项，`access-key`、`secret-access-key` 和 `token` 是可选项。最佳实践是将 AWS 连接凭证设置为环境变量或存储在 `~/.aws/credentials` 文件中，而不是将它们设置在 changefeed 的配置文件中。

更多信息，请参阅 [AWS官方文档](https://aws.github.io/aws-sdk-go-v2/docs/configuring-sdk/#specifying-credentials)。

## 自定义 Kafka Sink 的 Topic 和 Partition 的分发规则

### Matcher 匹配规则

以如下示例配置文件中的 `dispatchers` 配置项为例：

```toml
[sink]
dispatchers = [
  {matcher = ['test1.*', 'test2.*'], topic = "Topic 表达式 1", partition = "ts" },
  {matcher = ['test3.*', 'test4.*'], topic = "Topic 表达式 2", partition = "index-value" },
  {matcher = ['test1.*', 'test5.*'], topic = "Topic 表达式 3", partition = "table"},
  {matcher = ['test6.*'], partition = "ts"}
]
```

- 对于匹配了 matcher 规则的表，按照对应的 topic 表达式指定的策略进行分发。例如表 test3.aa，按照 topic 表达式 2 分发；表 test5.aa，按照 topic 表达式 3 分发。
- 对于匹配了多个 matcher 规则的表，以靠前的 matcher 对应的 topic 表达式为准。例如表 test1.aa，按照 topic 表达式 1 分发。
- 对于没有匹配任何 matcher 的表，将对应的数据变更事件发送到 --sink-uri 中指定的默认 topic 中。例如表 test10.aa 发送到默认 topic。
- 对于匹配了 matcher 规则但是没有指定 topic 分发器的表，将对应的数据变更发送到 --sink-uri 中指定的默认 topic 中。例如表 test6.aa 发送到默认 topic。

### Topic 分发器

Topic 分发器用 topic = "xxx" 来指定，并使用 topic 表达式来实现灵活的 topic 分发策略。topic 的总数建议小于 1000。

Topic 表达式的基本规则为 `[prefix]{schema}[middle][{table}][suffix]`，详细解释如下：

- `prefix`：可选项，代表 Topic Name 的前缀。
- `{schema}`：必选项，用于匹配库名。从 v7.1.4 开始，该参数为可选项。
- `middle`：可选项，代表库表名之间的分隔符。
- `{table}`：可选项，用于匹配表名。
- `suffix`：可选项，代表 Topic Name 的后缀。

其中 `prefix`、`middle` 以及 `suffix` 仅允许出现大小写字母（`a-z`、`A-Z`）、数字（`0-9`）、点号（`.`）、下划线（`_`）和中划线（`-`）；`{schema}`、`{table}` 均为小写，诸如 `{Schema}` 以及 `{TABLE}` 这样的占位符是无效的。

一些示例如下：

- `matcher = ['test1.table1', 'test2.table2'], topic = "hello_{schema}_{table}"`
    - 对于表 `test1.table1` 对应的数据变更事件，发送到名为 `hello_test1_table1` 的 topic 中。
    - 对于表 `test2.table2` 对应的数据变更事件，发送到名为 `hello_test2_table2` 的 topic 中。
- `matcher = ['test3.*', 'test4.*'], topic = "hello_{schema}_world"`
    - 对于 `test3` 下的所有表对应的数据变更事件，发送到名为 `hello_test3_world` 的 topic 中。
    - 对于 `test4` 下的所有表对应的数据变更事件，发送到名为 `hello_test4_world` 的 topic 中。
- `matcher = ['test5.*, 'test6.*'], topic = "hard_code_topic_name"`
    - 对于 `test5` 和 `test6` 下的所有表对应的数据变更事件，发送到名为 `hard_code_topic_name` 的 topic 中。你可以直接指定 topic 名称。
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

partition 分发器用 `partition = "xxx"` 来指定，支持 `default`、`index-value`、`columns`、`table` 和 `ts` 共五种 partition 分发器，分发规则如下：

- `default`：默认使用 table 分发规则。使用所属库名和表名计算 partition 编号，一张表的数据被发送到相同的 partition。单表数据只存在于一个 partition 中并保证有序，但是发送吞吐量有限，无法通过添加消费者的方式提升消费速度。
- `index-value`：使用事件所属表的主键、唯一索引或由 `index` 配置指定的索引的值计算 partition 编号，一张表的数据被发送到多个 partition。单表数据被发送到多个 partition 中，每个 partition 中的数据有序，可以通过添加消费者的方式提升消费速度。
- `columns`：使用由 `columns` 指定的列的值计算 partition 编号。一张表的数据被发送到多个 partition。单表数据被发送到多个 partition 中，每个 partition 中的数据有序，可以通过添加消费者的方式提升消费速度。
- `table`：使用事件所属的表的库名和表名计算 partition 编号。
- `ts`：使用事件的 commitTs 计算 partition 编号。一张表的数据被发送到多个 partition。单表数据被发送到多个 partition 中，每个 partition 中的数据有序，可以通过添加消费者的方式提升消费速度。一条数据的多次修改可能被发送到不同的 partition 中。消费者消费进度不同可能导致消费端数据不一致。因此，消费端需要对来自多个 partition 的数据按 commitTs 排序后再进行消费。

以如下示例配置文件中的 `dispatchers` 配置项为例：

```toml
[sink]
dispatchers = [
    {matcher = ['test.*'], partition = "index-value"},
    {matcher = ['test1.*'], partition = "index-value", index = "index1"},
    {matcher = ['test2.*'], partition = "columns", columns = ["id", "a"]},
    {matcher = ['test3.*'], partition = "table"},
]
```

- 任何属于库 `test` 的表均使用 `index-value` 分发规则，即使用主键或者唯一索引的值计算 partition 编号。如果有主键则使用主键，否则使用最短的唯一索引。
- 任何属于库 `test1` 的表均使用 `index-value` 分发规则，并且使用名为 `index1` 的索引的所有列的值计算 partition 编号。如果指定的索引不存在，则报错。注意，`index` 指定的索引必须是唯一索引。
- 任何属于库 `test2` 的表均使用 `columns` 分发规则，并且使用列 `id` 和 `a` 的值计算 partition 编号。如果任一列不存在，则报错。
- 任何属于库 `test3` 的表均使用 `table` 分发规则。
- 对于属于库 `test4` 的表，因为不匹配上述任何一个规则，所以使用默认的 `default`，即 `table` 分发规则。

如果一张表，匹配了多个分发规则，以第一个匹配的规则为准。

> **注意：**
>
> 从 v6.1 开始，为了明确配置项的含义，用来指定 partition 分发器的配置项由原来的 `dispatcher` 改为 `partition`，`partition` 为 `dispatcher` 的别名。例如，以下两条规则完全等价：
>
> ```
> [sink]
> dispatchers = [
>    {matcher = ['*.*'], dispatcher = "index-value"},
>    {matcher = ['*.*'], partition = "index-value"},
> ]
> ```
>
> 但是 `dispatcher` 与 `partition` 不能出现在同一条规则中。例如，以下规则非法：
>
> ```
> {matcher = ['*.*'], dispatcher = "index-value", partition = "table"},
> ```

## 列选择功能

列选择功能支持对事件中的列进行选择，只将指定的列的数据变更事件发送到下游。

以如下示例配置文件中的 `column-selectors` 配置项为例：

```toml
[sink]
column-selectors = [
    {matcher = ['test.t1'], columns = ['a', 'b']},
    {matcher = ['test.*'], columns = ["*", "!b"]},
    {matcher = ['test1.t1'], columns = ['column*', '!column1']},
    {matcher = ['test3.t'], columns = ["column?", "!column1"]},
]
```

- 对于表 `test.t1`，只发送 `a` 和 `b` 两列的数据。
- 对于属于库 `test` 的表（除 `t1` 外），发送除 `b` 列之外的所有列的数据。
- 对于表 `test1.t1`，发送所有以 `column` 开头的列，但是不发送 `column1` 列的数据。
- 对于表 `test3.t`，发送所有以 `column` 开头且列名长度为 7 的列，但是不发送 `column1` 列的数据。
- 不匹配任何规则的表将不进行列过滤，发送所有列的数据。

> **注意：**
>
> 经过 `column-selectors` 规则过滤后，表中的数据必须要有主键或者唯一键被同步，否则在 changefeed 创建或运行时会报错。

## 横向扩展大单表的负载到多个 TiCDC 节点

该功能可以按照大单表的数据量和每分钟的修改行数将表的同步范围切分为多个，并使各个范围之间所同步的数据量和修改行数基本相同。该功能将这些范围分布到多个 TiCDC 节点进行同步，使得多个 TiCDC 节点可以同时同步大单表。该功能可以解决以下两个问题：

- 单个 TiCDC 节点不能及时同步大单表。
- TiCDC 节点之间资源（CPU、内存等）消耗不均匀。

> **警告：**
>
> TiCDC v7.0.0 仅支持在 Kafka 同步任务上开启大单表的横向扩展功能。

配置样例如下所示：

```toml
[scheduler]
# 默认值为 "false"，设置为 "true" 以打开该功能。
enable-table-across-nodes = true
# 打开该功能后，该功能只对 Region 个数大于 `region-threshold` 值的表生效。
region-threshold = 100000
# 打开该功能后，该功能会对每分钟修改行数大于 `write-key-threshold` 值的表生效。
# 注意：
# * 该参数默认值为 0，代表该功能默认不会按表的修改行数来切分表的同步范围。
# * 你可以根据集群负载来配置该参数，如 30000，代表当表每分钟的更新行数超过 30000 时，该功能将会切分表的同步范围。
# * 当 `region-threshold` 和 `write-key-threshold` 同时配置时，
#   TiCDC 将优先检查修改行数是否大于 `write-key-threshold`，
#   如果不超过，则再检查 Region 个数是否大于 `region-threshold`。
write-key-threshold = 30000
```

一个表包含的 Region 个数可用如下 SQL 查询：

```sql
SELECT COUNT(*) FROM INFORMATION_SCHEMA.TIKV_REGION_STATUS WHERE DB_NAME="database1" AND TABLE_NAME="table1" AND IS_INDEX=0;
```

## 处理超过 Kafka Topic 限制的消息

Kafka Topic 对可以接收的消息大小有限制，该限制由 [`max.message.bytes`](https://kafka.apache.org/documentation/#topicconfigs_max.message.bytes) 参数控制。当 TiCDC Kafka sink 在发送数据时，如果发现数据大小超过了该限制，会导致 changefeed 报错，无法继续同步数据。为了解决这个问题，TiCDC 新增一个参数 `large-message-handle-option` 并提供如下解决方案。

目前，如下功能支持 Canal-JSON 和 Open Protocol 两种编码协议。使用 Canal-JSON 协议时，你需要在 `sink-uri` 中设置 `enable-tidb-extension=true`。

### TiCDC 层数据压缩功能

从 v7.4.0 开始，TiCDC Kafka sink 支持在编码消息后立即对数据进行压缩，并与消息大小限制参数比较。该功能能够有效减少超过消息大小限制的情况发生。

配置样例如下所示：

```toml
[sink.kafka-config.large-message-handle]
# 该参数从 v7.4.0 开始引入
# 默认为 "none"，即不开启编码时的压缩功能
# 可选值有 "none"、"lz4"、"snappy"，默认为 "none"
large-message-handle-compression = "none"
```

开启了 `large-message-handle-compression` 之后，消费者收到的消息经过特定压缩协议编码，消费者应用程序需要使用指定的压缩协议进行数据解码。

该功能和 Kafka producer 的压缩功能不同：

* `large-message-handle-compression` 中指定的压缩算法是对单条 Kafka 消息进行压缩，并且压缩是在与消息大小限制参数比较之前进行。
* 你也可以同时通过 [`sink-uri`](#sink-uri-配置-kafka) 的 `compression` 参数配置压缩算法，该配置启用的压缩功能应用在整个发送数据请求，其中包含多条 Kafka 消息。

如果设置了 `large-message-handle-compression`，TiCDC 在收到一条消息后，先将该消息与消息大小限制参数的值进行对比，大于该消息大小限制的消息会被压缩。如果同时还设置了 [`sink-uri`](#sink-uri-配置-kafka) 的 `compression`，TiCDC 会根据 `sink-uri` 的设置，在 sink 级别再次对整个发送数据请求进行压缩。

两种压缩方法的压缩率的计算方法均为：`compression ratio = 压缩前的大小 / 压缩后的大小 * 100`

### 只发送 Handle Key

从 v7.3.0 开始，TiCDC Kafka sink 支持在消息大小超过限制时只发送 Handle Key 的数据。这样可以显著减少消息的大小，避免因为消息大小超过 Kafka Topic 限制而导致 changefeed 发生错误和同步任务失败的情况。

Handle Key 指的是：

* 如果被同步的表有定义主键，主键即为 Handle Key 。
* 如果没有主键，但是有定义 Not NULL Unique Key，Unique Key 即为 Handle Key。

配置样例如下所示：

```toml
[sink.kafka-config.large-message-handle]
# 该参数从 v7.3.0 开始引入
# 默认为空，即消息超过大小限制后，同步任务失败
# 设置为 "handle-key-only" 时，如果消息超过大小，data 字段内容只发送 handle key；如果依旧超过大小，同步任务失败
large-message-handle-option = "handle-key-only"
```

### 消费只有 Handle Key 的消息

只有 Handle Key 数据的消息格式如下：

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
        "id": 4
    },
    "mysqlType": {
        "id": "int"
    },
    "data": [
        {
          "id": "2"
        }
    ],
    "old": null,
    "_tidb": {     // TiDB 的扩展字段
        "commitTs": 429918007904436226,  // TiDB TSO 时间戳
        "onlyHandleKey": true
    }
}
```

Kafka 消费者收到消息之后，首先检查 `onlyHandleKey` 字段。如果该字段存在且为 `true`，表示该消息只包含 Handle Key 的数据。此时，你需要查询上游 TiDB，通过 [`tidb_snapshot` 读取历史数据](/read-historical-data.md)来获取完整的数据。

> **警告：**
>
> 在 Kafka 消费者处理数据并查询 TiDB 时，可能发生数据已经被 GC 的情况。你需要[调整 TiDB 集群的 GC Lifetime 设置](/system-variables.md#tidb_gc_life_time-从-v50-版本开始引入) 为一个较大的值，以避免该情况。

### 发送大消息到外部存储

从 v7.4.0 开始，TiCDC Kafka sink 支持在消息大小超过限制时将该条消息发送到外部存储服务，同时向 Kafka 发送一条含有该大消息在外部存储服务中地址的消息。这样可以避免因为消息大小超过 Kafka Topic 限制而导致 changefeed 失败的情况。

配置样例如下所示：

```toml
[sink.kafka-config.large-message-handle]
# large-message-handle-option 从 v7.3.0 开始引入
# 默认为 "none"，即消息超过大小限制后，同步任务失败
# 设置为 "handle-key-only" 时，如果消息超过大小，data 字段内容只发送 Handle Key。如果依旧超过大小，同步任务失败
# 设置为 "claim-check" 时，如果消息超过大小，将该条消息发送到外部存储服务
large-message-handle-option = "claim-check"
claim-check-storage-uri = "s3://claim-check-bucket"
```

当指定 `large-message-handle-option` 为 `claim-check` 时，`claim-check-storage-uri` 必须设置为一个有效的外部存储服务地址，否则创建 changefeed 将会报错。

> **建议：**
>
> 关于 Amazon S3、GCS 以及 Azure Blob Storage 的 URI 参数的详细参数说明，请参考[外部存储服务的 URI 格式](/external-storage-uri.md)。

TiCDC 不会清理外部存储服务上的消息，数据消费者需要自行管理外部存储服务。

### 消费外部存储中的大消息

Kafka 消费者会收到一条含有大消息在外部存储服务中的地址的消息，格式如下：

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
        "id": 4
    },
    "mysqlType": {
        "id": "int"
    },
    "data": [
        {
          "id": "2"
        }
    ],
    "old": null,
    "_tidb": {     // TiDB 的扩展字段
        "commitTs": 429918007904436226,  // TiDB TSO 时间戳
        "claimCheckLocation": "s3:/claim-check-bucket/${uuid}.json"
    }
}
```

如果收到的消息有 `claimCheckLocation` 字段，Kafka 消费者根据该字段提供的地址读取以 JSON 格式存储的大消息数据。消息格式如下：

```json
{
  key: "xxx",
  value: "xxx",
}
```

`key` 和 `value` 分别存有编码后的大消息，该消息原本应该发送到 Kafka 消息中的对应字段。消费者可以通过解析这两部分的数据，还原大消息的内容。
