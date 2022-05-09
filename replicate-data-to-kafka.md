---
title: Replicate data from TiDB to Apache Kafka
summary: Learn how to replicate data from TiDB to Apache Kafka
---

# Replicate Data from TiDB to Apache Kafka

This document describes how to replicate data from TiDB to Apache Kafka by using [TiCDC](/ticdc/ticdc-overview.md), which includes the following steps:

- Deploy a TiCDC cluster and a Kafka cluster.
- Create a changefeed with Kafka as the sink.
- Write data to the TiDB cluster by using go-tpc. On Kafka console consumer, check that the data is replicated to a specified Kafka topic.

These steps are performed in a lab environment. You can also deploy a cluster for a production environment by referring to these steps.

## Step 1. Set up the environment

1. Deploy a TiCDC cluster.

    You can deploy a TiCDC quickly by running the `tiup playground` command.

    {{< copyable "shell-regular" >}}

    ```shell
    tiup playground --host 0.0.0.0 --db 1 --pd 1 --kv 1 --tiflash 0 --ticdc 1

    # View cluster status
    tiup status
    ```

    In a production environment, you can deploy a TiCDC as instructed in [Deploy TiCDC](/ticdc/deploy-ticdc.md).

2. Deploy a Kafka cluster.

    - To quickly deploy a Kafka cluster, refer to [Apache Kakfa Quickstart](https://kafka.apache.org/quickstart).
    - To deploy a Kafka cluster in production environments, refer to [Running Kafka in Production](https://docs.confluent.io/platform/current/kafka/deployment.html).

## Step 2. Create a changefeed

Use tiup ctl to create a changefeed with Kafka as the downstream node.

{{< copyable "shell-regular" >}}

```shell
tiup ctl cdc changefeed create --pd="http://127.0.0.1:2379" --sink-uri="kafka://127.0.0.1:9092/kafka-topic-name?protocol=canal-json" --changefeed-id="kafka-changefeed"
```

If the command is executed successfully, information about the changefeed is displayed, such as the changefeed ID and the sink URI.

{{< copyable "shell-regular" >}}

```shell
Create changefeed successfully!
ID: kafka-changefeed
Info: {"sink-uri":"kafka://127.0.0.1:9092/kafka-topic-name?protocol=canal-json","opts":{},"create-time":"2022-04-06T14:45:10.824475+08:00","start-ts":432335096583028737,"target-ts":0,"admin-job-type":0,"sort-engine":"unified","sort-dir":"","config":{"case-sensitive":true,"enable-old-value":true,"force-replicate":false,"check-gc-safe-point":true,"filter":{"rules":["*.*"],"ignore-txn-start-ts":null},"mounter":{"worker-num":16},"sink":{"dispatchers":null,"protocol":"canal-json","column-selectors":null},"cyclic-replication":{"enable":false,"replica-id":0,"filter-replica-ids":null,"id-buckets":0,"sync-ddl":false},"scheduler":{"type":"table-number","polling-time":-1},"consistent":{"level":"none","max-log-size":64,"flush-interval":1000,"storage":""}},"state":"normal","error":null,"sync-point-enabled":false,"sync-point-interval":600000000000,"creator-version":"v6.0.0-master"}
 ```

If the command does not return any information, you should check network connectivity from the server where the command is executed to the target Kafka cluster.

In production environments, a Kafka cluster has multiple broker nodes. Therefore, you can add the addresses of multiple brokers to the sink UIR. This improves stable access to the Kafka cluster. When a Kafka cluster is faulty, the changefeed still works. Suppose that a Kafka cluster has three broker nodes, with IP addresses being 127.0.0.1:9092, 127.0.0.2:9092, and 127.0.0.3:9092, respectively. You can create a changefeed with the following sink URI.

{{< copyable "shell-regular" >}}

```shell
tiup ctl cdc changefeed create --pd="http://127.0.0.1:2379" --sink-uri="kafka://127.0.0.1:9092,127.0.0.2:9092,127.0.0.3:9092/kafka-topic-name?protocol=canal-json&partition-num=3&replication-factor=1&max-message-bytes=1048576"
```

After executing the preceding command, run the following command to check the status of the changefeed.

{{< copyable "shell-regular" >}}

```shell
tiup ctl cdc changefeed list --pd="http://127.0.0.1:2379"
```

You can manage the status of a changefeed as instructed in [Manage replication tasks (`changefeed`)](/ticdc/manage-ticdc.md#manage-replication-tasks-changefeed).

## Step 3. Generate data changes in the TiDB cluster

After a changefeed is created, once there is any event change in the TiDB cluster, such as an `INSERT`, `UPDATE`, or `DELETE` operation, data change is generated in TiCDC. Then TiCDC replicates the data change to the sink specified in the changefeed. In this document, the sink is Kafka and the data change is written to the specified Kafka topic.

1. Simulate service workload.

    In the lab environment, you can use `go-tpc` to write data to the TiDB cluster, which is used as the source of the changefeed. Specifically, run the following command to create a database `tpcc` in the upstream TiDB cluster. Then use `TiUP bench` to write data to this new database.

    {{< copyable "shell-regular" >}}

    ```shell
    create database tpcc;
    tiup bench tpcc -H 127.0.0.1 -P 4000 -D tpcc --warehouses 4 prepare
    tiup bench tpcc -H 127.0.0.1 -P 4000 -D tpcc --warehouses 4 run --time 300s
    ```

    For more details about `go-tpc`, refer to [How to Run TPC-C Test on TiDB](/benchmark/benchmark-tidb-using-tpcc.md).

2. Consume data change from Kafka.

    When a changefeed works normally, it writes data to the Kafka topic. You can run `kafka-console-consumer.sh` to view the written data.

    {{< copyable "shell-regular" >}}

    ```shell
    ./bin/kafka-console-consumer.sh --bootstrap-server 127.0.0.1:9092 --from-beginning --topic `${topic-name}`
    ```

    In production environments, you need to develop Kafka Consumer to consume the data in the Kafka topic.
