---
title: Quick Start Guide on Integrating TiDB with Confluent Platform
summary: Learn how to stream TiDB data to the Confluent Platform using TiCDC.
---

# Quick Start Guide on Integrating TiDB with Confluent Platform

This document introduces how to integrate TiDB to Confluent Platform using [TiCDC](/ticdc/ticdc-overview.md).

> **Note:**
>
> This is still an experimental feature. Do **NOT** use it in a production environment.

[Confluent Platform](https://docs.confluent.io/current/platform.html) is a data streaming platform with Kafka at its core. With many official and third-party sink connectors, Confluent Platform enables you to easily connect stream sources to relational or non-relational databases.

To integrate TiDB with Confluent Platform, you can use the TiCDC component with the Avro protocol. TiCDC can stream data changes to Kafka in the format that Confluent Platform recognizes. For the detailed integration guide, see the following sections:

## Prerequisites

> **Note:**
>
> In this tutorial, the [JDBC sink connector](https://docs.confluent.io/current/connect/kafka-connect-jdbc/sink-connector/index.html#load-the-jdbc-sink-connector) is used to replicate TiDB data to a downstream relational database. To make it simple, **SQLite** is used here as an example.

+ Make sure that Zookeeper, Kafka, and Schema Registry are properly installed. It is recommended that you follow the [Confluent Platform Quick Start Guide](https://docs.confluent.io/current/quickstart/ce-quickstart.html#ce-quickstart) to deploy a local test environment.

+ Make sure that JDBC sink connector is installed by running the following command. The result should contain `jdbc-sink`.

    {{< copyable "shell-regular" >}}

    ```shell
    confluent local services connect connector list
    ```

## Integration procedures

1. Save the following configuration into `jdbc-sink-connector.json`:

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

2. Create an instance of the JDBC sink connector by running the following command (assuming Kafka is listening on `127.0.0.1:8083`):

    {{< copyable "shell-regular" >}}

    ```shell
    curl -X POST -H "Content-Type: application/json" -d jdbc-sink-connector.json http://127.0.0.1:8083/connectors
    ```

3. Deploy TiCDC in one of the following ways. If TiCDC is already deployed, you can skip this step.

    - [Deploy and install TiCDC using TiUP](/ticdc/manage-ticdc.md#deploy-and-install-ticdc-using-tiup)
    - [Use Binary](/ticdc/manage-ticdc.md#use-binary)

    Make sure that your TiDB and TiCDC clusters are healthy before proceeding.

4. Create a `changefeed` by running the `cdc cli` command:

    {{< copyable "shell-regular" >}}

    ```shell
    ./cdc cli changefeed create --pd="http://127.0.0.1:2379" --sink-uri="kafka://127.0.0.1:9092/testdb_test?protocol=avro" --opts "registry=http://127.0.0.1:8081"
    ```

    > **Note:**
    >
    > Make sure that PD, Kafka, and Schema Registry are running on their respective default ports.

## Test data replication

After TiDB is integrated with Confluent Platform, you can follow the example procedures below to test the data replication.

1. Create the `testdb` database in your TiDB cluster:

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

    > **Note:**
    >
    > If you need to change the database name or the table name, change `topics` in `jdbc-sink-connector.json` accordingly.

2. Insert data into TiDB:

    {{< copyable "sql" >}}

    ```sql
    INSERT INTO test (id, v) values (1, 'a');
    INSERT INTO test (id, v) values (2, 'b');
    INSERT INTO test (id, v) values (3, 'c');
    INSERT INTO test (id, v) values (4, 'd');
    ```

3. Wait a moment for data to be replicated to the downstream. Then check the downstream for data:

    {{< copyable "shell-regular" >}}

    ```shell
    sqlite3 test.db
    sqlite> SELECT * from test;
    ```
