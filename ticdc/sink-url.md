---
title: Configure Sink URI
summary: Learn how to configure sink URI.
category: reference
aliases: ['/docs/dev/reference/tools/ticdc/sink/']
---

# Configure Sink URI

You need to configure sink URI in the following format. Currently, the `scheme` supports `mysql`, `tidb`, and `kafka`.

{{< copyable "" >}}

```
[scheme]://[userinfo@][host]:[port][/path]?[query_parameters]
```

## Configure sink URI with `mysql` or `tidb`

The following command is a configuration example:

{{< copyable "shell-regular" >}}

```shell
--sink-uri="mysql://root:123456@127.0.0.1:3306/?worker-count=16&max-txn-row=5000"
```

The parameters in the above command are described as follows:

| Parameter         | Description                                             |
| :------------ | :------------------------------------------------ |
| `root`        | The username of the downstream database                             |
| `123456`       |  The password of the downstream database                                   |
| `127.0.0.1`    |  The IP of the downstream database                              |
| `3306`         |  The port of the downstream database                               |
| `worker-count` |   The number of SQL statements that can be concurrently executed to the downstream (optional, `16` by default)    |
| `max-txn-row`  |  The size of a transaction batch that can be executed to the downstream (optional, `256` by default)  |

## Configure sink URI with `kafka`

The following command is an configuration example:

{{< copyable "shell-regular" >}}

```shell
--sink-uri="kafka://127.0.0.1:9092/cdc-test?kafka-version=2.4.0&partition-num=6&max-message-bytes=67108864&replication-factor=1"
```

The parameters in the above command are described as follows:

| Parameter               | Description                                                         |
| :------------------ | :------------------------------------------------------------ |
| `127.0.0.1`          |  The IP of downstream Kafka services                              |
| `9092`               |  The port of downstream Kafka                                        |
| `cdc-test`           |  The name of the Kafka topic                                    |
| `kafka-version`      |  The version of downstream Kafka (optional, `2.4.0` by default)                    |
| `partition-num`      | The number of downstream Kafka partitions (optional. The value must be **no greater than** the actual number of partitions. If you do not configure this parameter, the partition number will be obtained automatically.) |
| `max-message-bytes`  |  The maximum size of data that is sent to Kafka broker each time (optional, `64MB` by default)  |
| `replication-factor` |  The number of Kafka message replicas that can be saved (optional, `1` by default)                       |
