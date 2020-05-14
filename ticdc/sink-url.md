---
title: Sink URI 配置规则
category: reference
aliases: ['/docs-cn/dev/reference/tools/ticdc/sink/']
---

# Sink URI 配置规则

sink URI 需要按照以下格式进行配置，目前 scheme 支持 `mysql`/`tidb`/`kafka`。

{{< copyable "" >}}

```
[scheme]://[userinfo@][host]:[port][/path]?[query_parameters]
```

## Sink URI 配置 `mysql`/`tidb`

配置样例如下所示：

{{< copyable "shell-regular" >}}

```shell
--sink-uri="mysql://root:123456@127.0.0.1:3306/?worker-count=16&max-txn-row=5000"
```

以上配置命令中的参数解析如下：

| 参数         | 解析                                             |
| :------------ | :------------------------------------------------ |
| `root`        | 下游数据库的用户名                             |
| `123456`       | 下游数据库密码                                     |
| `127.0.0.1`    | 下游数据库的 IP                                |
| `3306`         | 下游数据的连接端口                                 |
| `worker-count` | 向下游执行 SQL 的并发度（可选，默认值为 `16`）       |
| `max-txn-row`  | 向下游执行 SQL 的 batch 大小（可选，默认值为 `256`） |

## Sink URI 配置 `kafka`

配置样例如下所示：

{{< copyable "shell-regular" >}}

```shell
--sink-uri="kafka://127.0.0.1:9092/cdc-test?kafka-version=2.4.0&partition-num=6&max-message-bytes=67108864&replication-factor=1"
```

以上配置命令中的参数解析如下：

| 参数               | 解析                                                         |
| :------------------ | :------------------------------------------------------------ |
| `127.0.0.1`          | 下游 Kafka 对外提供服务的 IP                                 |
| `9092`               | 下游 Kafka 的连接端口                                          |
| `cdc-test`           | 使用的 Kafka topic 名字                                      |
| `kafka-version`      | 下游 Kafka 版本号（可选，默认值 `2.4.0`）                      |
| `partition-num`      | 下游 Kafka partition 数量（可选，不能大于实际 partition 数量。如果不填会自动获取 partition 数量。） |
| `max-message-bytes`  | 每次向 Kafka broker 发送消息的最大数据量（可选，默认值 `64MB`） |
| `replication-factor` | kafka 消息保存副本数（可选，默认值 `1`）                       |
