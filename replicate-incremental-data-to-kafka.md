---
title: 从 TiDB 同步增量数据至 Kafka
summary: 了解如何从 TiDB 集群同步增量数据至 Kafka 集群。
---

# 从 TiDB 同步增量数据至 Kafka

本文档介绍如何使用 [TiCDC](/ticdc/ticdc-overview.md) 将 TiDB 的增量数据同步到 Kafka。主要包含以下内容：

- 快速搭建 TiCDC 集群和 Kafka 集群
- 创建以 Kafka 为 sink 的 changefeed
- 使用 go-tpc 写入数据到上游 TiDB，使用 Kafka console consumer 观察数据被写入到指定的 Topic

上述过程将会基于实验环境进行，你可以参考上述执行步骤，搭建生产级别的集群。

## 第 1 步：搭建环境

1. 部署 TiCDC 集群。

    你可以使用 TiUP Playground 功能，快速部署 TiCDC ，命令如下：

    {{< copyable "shell-regular" >}}

    ```shell
    tiup playground --host 0.0.0.0 --db 1 --pd 1 --kv 1 --tiflash 0 --ticdc 1
    # 查看集群状态
    tiup status
    ```

    生产环境下，可以参考 [TiCDC 部署](/ticdc/deploy-ticdc.md)，完成 TiCDC 集群部署工作。

2. 部署 Kafka 集群。

    - 快速体验，你可以参考 [Apache Kakfa Quickstart](https://kafka.apache.org/quickstart) 启动 Kafka 节点。
    - 生产环境下，可以参考 [Running Kafka in Production](https://docs.confluent.io/platform/current/kafka/deployment.html) 完成 Kafka 集群搭建。

## 第 2 步：创建 Kafka Changefeed

使用 TiUP，执行如下命令，创建一个将 Kafka 作为下游节点的 changefeed:

{{< copyable "shell-regular" >}}

```shell
tiup ctl cdc changefeed create --pd="http://127.0.0.1:2379" --sink-uri="kafka://127.0.0.1:9092/kafka-topic-name?protocol=canal-json" --changefeed-id="kafka-changefeed"
```

如果命令执行成功，将会返回被创建的 changefeed 的相关信息，包含被创建的 changefeed 的 ID 以及相信信息，内容如下：

{{< copyable "shell-regular" >}}

```shell
Create changefeed successfully!
ID: kafka-changefeed
Info: {"sink-uri":"kafka://127.0.0.1:9092/kafka-topic-name?protocol=canal-json","opts":{},"create-time":"2022-04-06T14:45:10.824475+08:00","start-ts":432335096583028737,"target-ts":0,"admin-job-type":0,"sort-engine":"unified","sort-dir":"","config":{"case-sensitive":true,"enable-old-value":true,"force-replicate":false,"check-gc-safe-point":true,"filter":{"rules":["*.*"],"ignore-txn-start-ts":null},"mounter":{"worker-num":16},"sink":{"dispatchers":null,"protocol":"canal-json","column-selectors":null},"cyclic-replication":{"enable":false,"replica-id":0,"filter-replica-ids":null,"id-buckets":0,"sync-ddl":false},"scheduler":{"type":"table-number","polling-time":-1},"consistent":{"level":"none","max-log-size":64,"flush-interval":1000,"storage":""}},"state":"normal","error":null,"sync-point-enabled":false,"sync-point-interval":600000000000,"creator-version":"v6.0.0-master"}
```

如果命令长时间没有返回，你需要检查当前执行命令所在服务器到 sink-uri 中指定的 Kafka 机器的网络可达性，保证二者之间的网络连接正常。

生产环境下 Kafka 集群通常有多个 broker 节点，你可以在 sink-uri 中配置多个 broker 的访问地址，这有助于提升 changefeed 到 Kafka 集群访问的稳定性，当部分被配置的 Kafka 节点故障的时候，changefeed 依旧可以正常工作。假设 Kafka 集群中有 3 个 broker 节点，地址分别为 127.0.0.1:9092 / 127.0.0.2:9092 / 127.0.0.3:9092，可以参考如下 sink-uri 创建 changefeed:

{{< copyable "shell-regular" >}}

```shell
tiup ctl cdc changefeed create --pd="http://127.0.0.1:2379" --sink-uri="kafka://127.0.0.1:9092,127.0.0.2:9092,127.0.0.3:9092/kafka-topic-name?protocol=canal-json&partition-num=3&replication-factor=1&max-message-bytes=1048576"
```

上述命令执行返回之后，可以通过如下命令，查看 changefeed 的状态:

{{< copyable "shell-regular" >}}

```shell
tiup ctl cdc changefeed list --pd="http://127.0.0.1:2379"
```

你可以参考 [TiCDC 运维操作及任务管理](/ticdc/manage-ticdc.md#管理同步任务-changefeed)，对 changefeed 状态进行管理。

## 第 3 步：TiDB 产生事件变更数据

完成以上步骤后，只要上游 TiDB 有事件变更操作，比如 `INSERT`、`UPDATE`、`DELETE` 或其他 DDL 操作，即会产生数据到 TiCDC，然后 TiCDC 会将数据发送到 changefeed 指定的 sink，当下游 sink 是 Kafka 时，数据将会被写入指定的 Kafka Topic 中。

1. 模拟业务负载

    在测试实验环境下，我们可以使用 `go-tpc` 向上游 TiDB 集群写入数据，以让 TiDB 产生事件变更数据。如下命令，首先在上游 TiDB 创建名为 `tpcc` 的数据库，然后使用 TiUP bench 写入数据到刚创建的 `tpcc` 数据库中。

    {{< copyable "shell-regular" >}}

    ```shell
    create database tpcc;
    tiup bench tpcc -H 127.0.0.1 -P 4000 -D tpcc --warehouses 4 prepare
    tiup bench tpcc -H 127.0.0.1 -P 4000 -D tpcc --warehouses 4 run --time 300s
    ```

    关于 go-tpc 的更多详细内容，可以参考[如何对 TiDB 进行 TPC-C 测试](/benchmark/benchmark-tidb-using-tpcc.md)。

2. 消费 Kafka Topic 中的数据

    changefeed 正常运行时，会向 Kafka Topic 写入数据，你可以通过由 Kafka 提供的 `kafka-console-consumer.sh`, 观测到数据成功被写入到 Kafka Topic 中：

    {{< copyable "shell-regular" >}}

    ```shell
    ./bin/kafka-console-consumer.sh --bootstrap-server 127.0.0.1:9092 --from-beginning --topic `${topic-name}`
    ```

    生产环境下，你需要自行开发 Kafka Consumer 程序，对 Kafka Topic 中的数据进行消费。