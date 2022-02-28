# 从 TiDB 输出数据变更流到 Kafka

TiCDC 支持将 Kafka 作为下游节点，以达到将上游 TiDB 事件变更记录同步到下游 Kafka 的目的。

## Quick start

用户可以参考该部分内容，快速实验使用 TiCDC 同步 TiDB 事件变更记录同步到下游 Kafka 的整个过程。

参考如下资料，快速搭建环境：

搭建 TiCDC 集群 [Deploy TiCDC](./deploy-ticdc.md)。
搭建 Kafka 环境 [Kafka Quick Start](https://kafka.apache.org/quickstart)。

使用 TiCDC Cli 执行如下命令，即可创建一个将数据同步到下游 Kafka 的 changefeed:

{{< copyable "shell-regular" >}}

```shell
cdc cli changefeed create --pd="http://127.0.0.1:2379" --sink-uri="kafka://127.0.0.1:9092/topic-name?protocol=canal-json&partition-num=3&replication-factor=1&max-message-bytes=1048576&kafka-version=2.4.0"
```

为了让 TiDB 产生数据变更记录，可以使用 [go-tpc](https://github.com/pingcap/go-tpc) 向上游 TiDB 节点写入数据，也可以参考 [benchmark tidb using tpcc](../benchmark/benchmark-tidb-using-tpcc.md) 完成这一过程。

后续，可以通过 Kafka 提供的 `kafka-console-consumer.sh`, 观测到数据成功被写入到 Kafka Topic 中:

{{< copyable "shell-regular" >}}

```shell
./bin/kafka-console-consumer.sh --bootstrap-server 127.0.0.1:9092 --from-beginning --topic topic-name
```

至此即完成了使用 TiCDC 同步 TiDB 事件变更记录同步到 Kafka 的整个过程。

## 配置 Kafka changefeed 相关参数

用户可以在 `sink-uri` 中指定 Kafka changefeed 相关参数，具体内容如下表所示:

| 参数                     | 解析                                                                                                                    |
| :---------------------- | :-------------------------------------------------------------------------------------------------------------------- |
| `127.0.0.1:9092`        | 下游 Kafka 对外提供服务的 IP:PORT 地址。支持配置多个 Kafka broker 地址                                                        |
| `topic-name`            | Kafka Topic 名字，事件变更数据将会被写入该 Topic                                                                            |
| `kafka-version`         | 下游 Kafka 版本号（可选，默认值 `2.4.0`，目前支持的最低版本为 `0.11.0.2`，最高版本为 `2.7.0`。该值需要与下游 Kafka 的实际版本保持一致） |
| `kafka-client-id`       | 指定同步任务的 Kafka 客户端的 ID（可选，默认值为 `TiCDC_sarama_producer_同步任务的 ID`）                                        |
| `partition-num`         | 下游 Kafka partition 数量（默认值 `3`，不能大于实际的 Topic partition 数量，否则创建同步任务会失败）                              |
| `max-message-bytes`     | 每次向 Kafka broker 发送消息的最大数据量（可选，默认值 `10MB`）。从 v5.0.6 和 v4.0.6 开始，默认值分别从 64MB 和 256MB 调整至 10MB。  |
| `replication-factor`    | Kafka 消息保存副本数（可选，默认值 `1`）                                                                                   |
| `protocol`              | 输出到 Kafka 的消息协议，可选值有 `canal-json`、`open-protocol`、`canal`、`avro`、`maxwell`                                  |
| `auto-create-topic`     | 当传入的 `topic-name` 在 Kafka 集群不存在时，TiCDC 是否要自动创建该 topic（可选，默认值 `true`）                                 |
| `enable-tidb-extension` | 当输出协议为 `canal-json` 时，如果该值为 `true`，TiCDC 会发送 Resolved 事件，并在 Kafka 消息中添加 TiDB 扩展字段（可选，默认值 `false`）|
| `max-batch-size`        |  从 v4.0.9 开始引入。当消息协议支持把多条变更记录输出至一条 Kafka 消息时，该参数用于指定这一条 Kafka 消息中变更记录的最多数量。目前，仅当 Kafka 消息的 `protocol` 为 `open-protocol` 时有效（可选，默认值 `16`）|
| `ca`                    | 连接下游 Kafka 实例所需的 CA 证书文件路径（可选） |
| `cert`                  | 连接下游 Kafka 实例所需的证书文件路径（可选） |
| `key`                   | 连接下游 Kafka 实例所需的证书密钥文件路径（可选） |
| `sasl-user`             | 连接下游 Kafka 实例所需的 SASL/PLAIN 或 SASL/SCRAM 验证的用户名（authcid）（可选） |
| `sasl-password`         | 连接下游 Kafka 实例所需的 SASL/PLAIN 或 SASL/SCRAM 验证的密码（可选） |
| `sasl-mechanism`        | 连接下游 Kafka 实例所需的 SASL/PLAIN 或 SASL/SCRAM 验证的名称（可选） |

### 参数详解

* `partition-num`
* `replication-factor`
* `max-message-bytes`
* `max-batch-size`

最佳实践：

* TiCDC 推荐用户自行创建 Kafka Topic，你至少需要设置该 Topic 每次向 Kafka broker 发送消息的最大数据量和下游 Kafka partition 的数量。在创建 changefeed 的时候，这两项设置分别对应 `max-message-bytes` 和 `partition-num` 参数。
* 如果你在创建 changefeed 时，使用了尚未存在的 Topic，那么 TiCDC 会尝试使用 `partition-num` 和 `replication-factor` 参数自行创建 Topic。建议明确指定这两个参数。
* 在大多数情况下，建议使用 `canal-json` 协议。

> **注意：**
>
> 当 `protocol` 为 `open-protocol` 时，TiCDC 会尽量避免产生长度超过 `max-message-bytes` 的消息。但如果单条数据变更记录需要超过 `max-message-bytes` 个字节来表示，为了避免静默失败，TiCDC 会试图输出这条消息并在日志中输出 Warning。

#### TiCDC 集成 Kafka Connect (Confluent Platform)

> **警告：**
>
> 当前该功能为实验特性，不建议在生产环境中使用。

配置样例如下所示：

{{< copyable "shell-regular" >}}

```shell
--sink-uri="kafka://127.0.0.1:9092/topic-name?protocol=canal-json&kafka-version=2.4.0&protocol=avro&partition-num=6&max-message-bytes=67108864&replication-factor=1"
--opts registry="http://127.0.0.1:8081"
```

如要使用 Confluent 提供的 [data connectors](https://docs.confluent.io/current/connect/managing/connectors.html) 向关系型或非关系型数据库传输数据，应当选择 `avro` 协议，并在 `opts` 中提供 [Confluent Schema Registry](https://www.confluent.io/product/confluent-platform/data-compatibility/) 的 URL。请注意，`avro` 协议和 Confluent 集成目前均为**实验特性**。

集成具体步骤详见 [TiDB 集成 Confluent Platform 快速上手指南](/ticdc/integrate-confluent-using-ticdc.md)。

* kafka producer 说明，以及相关配置项
* changefeed 创建过程说明，sink-uri 示例
* 介绍常用配置 filter / dispatcher

## Protocol

### Canal-JSON

* 引导用户使用 canal-json 协议，其他协议不必体现

### Open-protocol

* open protocol 问题

# 运维操作

* 修改 topic 的 partitions 数量

# Kafka 集群配置推荐

# FAQ

频繁遇到 kafka message size too large 问题
