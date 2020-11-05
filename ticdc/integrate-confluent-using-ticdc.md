---
title: Confluent Platform 集成 TiDB 快速上手指南
summary: 了解如何使用 TiCDC 将 TiDB 数据流式传输到 Confluent Platform。
---

# TiDB 集成 Confluent Platform 快速上手指南

本文档介绍如何使用 [TiCDC](/ticdc/ticdc-overview.md) 集成 TiDB 与 Confluent Platform。

> **警告：**
>
> 当前该功能为实验特性，不建议在生产环境中使用。

[Confluent Platform](https://docs.confluent.io/current/platform.html) 是一个以 Kafka 为核心的流数据处理平台。它可以借助官方或第三方的 sink connector 将数据源连接到关系型或非关系型数据库中。

你可以使用遵循 Avro 协议的 TiCDC 组件来集成 TiDB 和 Confluent Platform。TiCDC 可以将数据变化以 Confluent Platform 能识别的格式流式传输到 Kafka。下文详细介绍了集成的操作步骤。

## 环境准备

> **注意：**
>
> 在本教程中，[JDBC sink connector](https://docs.confluent.io/current/connect/kafka-connect-jdbc/sink-connector/index.html#load-the-jdbc-sink-connector) 用于将 TiDB 的数据复制到下游的关系型数据库中。为了简化操作，此处以 SQLite 为例。

+ 确保 Zookeeper、Kafka 和 Schema Registry 已正确安装。推荐参照 [Confluent Platform 快速入门指南](https://docs.confluent.io/current/quickstart/ce-quickstart.html#ce-quickstart)部署本地测试环境。

+ 确保通过以下命令安装 JDBC sink connector。返回结果中需包含 `jdbc-sink`。

    {{< copyable "shell-regular" >}}

    ```shell
    confluent local services connect connector list
    ```

## 集成步骤

1. 将下方的配置样例保存为 `jdbc-sink-connector.json` 文件：

    {{< copyable "" >}}

    ```json
    {
      "name": "jdbc-sink-connector",
      "config": {
        "connector.class": "io.confluent.connect.jdbc.JdbcSinkConnector",
        "tasks.max": "1",
        "topics": "testdb_test",
        "connection.url": "sqlite:test.db",
        "connection.ds.pool.size": 5,
        "table.name.format": "test",
        "auto.create": true,
        "auto.evolve": true
      }
    }
    ```

2. 运行下方命令新建一个 JDBC sink connector 实例（假设 Kafka 监听的 IP 地址是 `127.0.0.1:8083`）：

    {{< copyable "shell-regular" >}}

    ```shell
    curl -X POST -H "Content-Type: application/json" -d jdbc-sink-connector.json http://127.0.0.1:8083/connectors
    ```

3. 通过以下任一方式部署 TiCDC。如果已经部署了 TiCDC，可以跳过这一步。

    - [Deploy and install TiCDC using TiUP](/ticdc/manage-ticdc.md#使用-tiup-部署安装-ticdc)
    - [Use Binary](/ticdc/manage-ticdc.md#在原有-tidb-集群上使用-binary-部署-ticdc-组件)

    在继续接下来的操作之前，请先确保 TiDB 和 TiCDC 集群可以正常运行。

4. 运行下面的 `cdc cli` 命令，新建一个同步任务 `changefeed` ：

    {{< copyable "shell-regular" >}}

    ```shell
    ./cdc cli changefeed create --pd="http://127.0.0.1:2379" --sink-uri="kafka://127.0.0.1:9092/testdb_test?protocol=avro" --opts "registry=http://127.0.0.1:8081"
    ```

    > **注意：**
    >
    > 请确保 PD、Kafka 和 Schema Registry 在各自的默认端口上运行。

## 数据复制测试

TiDB 与 Confluent Platform 成功集成后，你可以按照以下步骤来测试数据复制功能。

1. 在 TiDB 集群中新建 `testdb` 数据库：

    {{< copyable "sql" >}}

    ```sql
    CREATE DATABASE IF NOT EXISTS testdb;
    ```

    Create the `test` table in `testdb`:

    {{< copyable "sql" >}}

    ```sql
    USE testdb;
    CREATE TABLE test (
        id INT PRIMARY KEY,
        v TEXT
    );
    ```

    > **注意：**
    >
    > 如果你需要修改数据库名或数据表名，要相应地修改 `jdbc-sink-connector.json` 文件中 `topics` 的参数值。

2. 向 TiDB 数据库中插入数据：

    {{< copyable "sql" >}}

    ```sql
    INSERT INTO test (id, v) values (1, 'a');
    INSERT INTO test (id, v) values (2, 'b');
    INSERT INTO test (id, v) values (3, 'c');
    INSERT INTO test (id, v) values (4, 'd');
    ```

3. 等待数据被复制到下游数据库中，并检查下游的数据：

    {{< copyable "shell-regular" >}}

    ```shell
    sqlite3 test.db
    sqlite> SELECT * from test;
    ```
