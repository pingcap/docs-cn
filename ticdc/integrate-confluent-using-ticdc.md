---
title: 与 Confluent Cloud 进行数据集成
summary: 了解如何使用 TiCDC 从 TiDB 同步数据至 Confluent Cloud。
---

# 与 Confluent Cloud 进行数据集成

Confluent 是一个兼容 Apache Kafka 的数据流平台，能够访问、存储和管理连续的实时流数据，具备丰富的数据集成能力。自 v6.1.0 开始，TiCDC 支持将增量变更数据以 Avro 格式输出到 Confluent。本文档介绍如何使用 [TiCDC](/ticdc/ticdc-overview.md) 将 TiDB 的增量数据同步到 Confluent Cloud，并借助 Confluent Cloud 的能力最终将数据分别同步到 ksqlDB、Snowflake、SQL Server。主要内容包括：

- 快速搭建包含 TiCDC 的 TiDB 集群
- 创建将数据输出到 Confluent Cloud 的 changefeed
- 创建将数据从 Confluent Cloud 输出到 ksqlDB、Snowflake、SQL Server 的连接器 (Connector)
- 使用 go-tpc 写入数据到上游 TiDB，并观察 ksqlDB、Snowflake、SQL Server 中的数据

上述过程将会基于实验环境进行，你也可以参考上述执行步骤，搭建生产级别的集群。

## 输出增量数据到 Confluent Cloud

### 第 1 步：搭建环境

1. 部署包含 TiCDC 的 TiDB 集群。

    在实验或测试环境中，可以使用 TiUP Playground 功能快速部署 TiCDC，命令如下：

    ```shell
    tiup playground --host 0.0.0.0 --db 1 --pd 1 --kv 1 --tiflash 0 --ticdc 1
    # 查看集群状态
    tiup status
    ```

    如果尚未安装 TiUP，可以参考[安装 TiUP](/tiup/tiup-overview.md)。在生产环境下，可以参考[使用 TiUP 安装部署 TiCDC 集群](/ticdc/deploy-ticdc.md)，完成 TiCDC 集群部署工作。

2. 注册 Confluent Cloud 并创建 Confluent 集群。

    创建 Basic 集群并开放 Internet 访问，详见 [Quick Start for Confluent Cloud](https://docs.confluent.io/cloud/current/get-started/index.html)。

### 第 2 步：创建 Access Key Pair

1. 创建 Cluster API Key。

    在 Confluent 集群控制面板中依次点击 **Data Integration** > **API Keys** > **Create key** 来创建 Cluster API Key。创建成功后会得到一个 Key Pair 文件，内容如下：

    ```
    === Confluent Cloud API key: xxx-xxxxx ===

    API key:
    L5WWA4GK4NAT2EQV

    API secret:
    xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

    Bootstrap server:
    xxx-xxxxx.ap-east-1.aws.confluent.cloud:9092
    ```

2. 记录 Schema Registry Endpoints。

    在 Confluent 集群控制面板中，选择 **Schema Registry** > **API endpoint**，记录 Schema Registry Endpoints，如下：

    ```
    https://yyy-yyyyy.us-east-2.aws.confluent.cloud
    ```

3. 创建 Schema Registry API Key。

    在 Confluent 集群控制面板中，选择 **Schema Registry** > **API credentials** > **Create Key** 来创建 Schema Registry API Key。创建成功后会得到一个 Key Pair 文件，内容如下：

    ```
    === Confluent Cloud API key: yyy-yyyyy ===

    API key:
    7NBH2CAFM2LMGTH7

    API secret:
    xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
    ```

    以上步骤也可以通过 Confluent CLI 实现，详见 [Connect Confluent CLI to Confluent Cloud Cluster](https://docs.confluent.io/confluent-cli/current/connect.html)。

### 第 3 步：创建 Kafka changefeed

1. 创建 changefeed 配置文件。

    根据 Avro 协议和 Confluent Connector 的要求和规范，每张表的增量数据需要发送到独立的 Topic 中，并且每个事件需要按照主键值分发 Partition。因此，需要创建一个名为 `changefeed.conf` 的配置文件，填写如下内容：

    ```
    [sink]
    dispatchers = [
    {matcher = ['*.*'], topic = "tidb_{schema}_{table}", partition="index-value"},
    ]
    ```

    关于配置文件中 `dispatchers` 的详细解释，参考[自定义 Kafka Sink 的 Topic 和 Partition 的分发规则](/ticdc/manage-ticdc.md#自定义-kafka-sink-的-topic-和-partition-的分发规则)。

2. 创建一个 changefeed，将增量数据输出到 Confluent Cloud：

    ```shell
    tiup ctl:v6.1.0 cdc changefeed create --pd="http://127.0.0.1:2379" --sink-uri="kafka://<broker_endpoint>/ticdc-meta?protocol=avro&replication-factor=3&enable-tls=true&auto-create-topic=true&sasl-mechanism=plain&sasl-user=<broker_api_key>&sasl-password=<broker_api_secret>" --schema-registry="https://<schema_registry_api_key>:<schema_registry_api_secret>@<schema_registry_endpoint>" --changefeed-id="confluent-changefeed" --config changefeed.conf
    ```

    将如下字段替换为[第 2 步：创建 Access Key Pair](#第-2-步创建-access-key-pair)中创建和记录的值：

    - `<broker_endpoint>`
    - `<broker_api_key>`
    - `<broker_api_secret>`
    - `<schema_registry_api_key>`
    - `<schema_registry_api_secret>`
    - `<schema_registry_endpoint>`

    其中 `<schema_registry_api_secret>` 需要经过 [HTML URL 编码](https://www.w3schools.com/tags/ref_urlencode.asp)后再替换，替换完毕后示例如下：

    ```shell
    tiup ctl:v6.1.0 cdc changefeed create --pd="http://127.0.0.1:2379" --sink-uri="kafka://xxx-xxxxx.ap-east-1.aws.confluent.cloud:9092/ticdc-meta?protocol=avro&replication-factor=3&enable-tls=true&auto-create-topic=true&sasl-mechanism=plain&sasl-user=L5WWA4GK4NAT2EQV&sasl-password=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx" --schema-registry="https://7NBH2CAFM2LMGTH7:xxxxxxxxxxxxxxxxxx@yyy-yyyyy.us-east-2.aws.confluent.cloud" --changefeed-id="confluent-changefeed" --config changefeed.conf
    ```

    - 如果命令执行成功，将会返回被创建的 changefeed 的相关信息，包含被创建的 changefeed 的 ID 以及相关信息，内容如下：

        ```shell
        Create changefeed successfully!
        ID: confluent-changefeed
        Info: {... changfeed info json struct ...}
        ```

    - 如果命令长时间没有返回，请检查当前执行命令所在服务器到 Confluent Cloud 之间网络可达性，参考 [Test connectivity to Confluent Cloud](https://docs.confluent.io/cloud/current/networking/testing.html)。

3. Changefeed 创建成功后，执行如下命令，查看 changefeed 的状态：

    ```shell
    tiup ctl:v6.1.0 cdc changefeed list --pd="http://127.0.0.1:2379"
    ```

    可以参考 [TiCDC 运维操作及任务管理](/ticdc/manage-ticdc.md)对 changefeed 状态进行管理。

### 第 4 步：写入数据以产生变更日志

完成以上步骤后，TiCDC 会将上游 TiDB 的增量数据变更日志发送到 Confluent Cloud。本小节将对 TiDB 写入数据，以产生增量数据变更日志。

1. 模拟业务负载。

    在测试实验环境下，可以使用 go-tpc 向上游 TiDB 集群写入数据，以让 TiDB 产生事件变更数据。执行以下命令，会首先在上游 TiDB 创建名为 `tpcc` 的数据库，然后使用 TiUP bench 写入数据到这个数据库中。

    ```shell
    tiup bench tpcc -H 127.0.0.1 -P 4000 -D tpcc --warehouses 4 prepare
    tiup bench tpcc -H 127.0.0.1 -P 4000 -D tpcc --warehouses 4 run --time 300s
    ```

    关于 go-tpc 的更多详细内容，可以参考[如何对 TiDB 进行 TPC-C 测试](/benchmark/benchmark-tidb-using-tpcc.md)。

2. 观察 Confluent 中数据传输情况。

    ![Confluent topics](/media/integrate/confluent-topics.PNG)

    在 Confluent 集群控制面板中，可以观察到相应的 Topic 已经被自动创建，并有数据正在写入。至此，TiDB 数据库中的增量数据就被成功输出到了 Confluent Cloud。

## 与 ksqlDB 进行数据集成

ksqlDB 是一种面向流式数据处理的数据库。你可以直接在 Confluent Cloud 上创建 ksqlDB 集群，并且直接读取 TiCDC 输出到 Confluent 的增量数据。

1. 在 Confluent 集群控制面板中选择 ksqlDB，按照引导创建 ksqlDB 集群。

    等待集群状态为 Running 后，进入下一步操作，这个过程可能持续数分钟。

2. 在 ksqlDB Editor 中执行如下命令，创建一个用于读取 `tidb_tpcc_orders` Topic 的 STREAM。

    ```sql
    CREATE STREAM orders (o_id INTEGER, o_d_id INTEGER, o_w_id INTEGER, o_c_id INTEGER, o_entry_d STRING, o_carrier_id INTEGER, o_ol_cnt INTEGER, o_all_local INTEGER) WITH (kafka_topic='tidb_tpcc_orders', partitions=3, value_format='AVRO');
    ```

3. 执行如下命令查询 orders STREAM 数据：

    ```sql
    SELECT * FROM ORDERS EMIT CHANGES;
    ```

    ![Select from orders](/media/integrate/select-from-orders.png)

可以观察到 TiDB 中的增量数据实时同步到了 ksqlDB，如上图。至此，就完成了 TiDB 与 ksqlDB 的数据集成。

## 与 Snowflake 进行数据集成

Snowflake 是一种云原生数据仓库。借助 Confluent 的能力，你只需要创建 Snowflake Sink Connector，就可以将 TiDB 的增量数据输出到 Snowflake。

### 准备工作

- 注册和创建 Snowflake 集群，参考 [Getting Started with Snowflake](https://docs.snowflake.com/en/user-guide-getting-started.html)。

- 连接到 Snowflake 前，为 Snowflake 添加 Private Key，参考 [Key Pair Authentication & Key Pair Rotation](https://docs.snowflake.com/en/user-guide/key-pair-auth.html)。

### 集成步骤

1. 在 Snowflake 中创建 Database 和 Schema。

    在 Snowflake 控制面板中，选择 **Data** > **Database**。创建名为 `TPCC` 的 Database 和名为 `TiCDC` 的 Schema。

2. 在 Confluent 集群控制面板中，选择 **Data Integration** > **Connectors** > **Snowflake Sink**，进入如下页面：

    ![Add snowflake sink connector](/media/integrate/add-snowflake-sink-connector.png)

3. 选择需要同步到 Snowflake 的 Topic 后，进入下一页面：

    ![Credentials](/media/integrate/credentials.png)

4. 填写 Snowflake 连接认证信息，其中 Database name 和 Schema name 填写在上一步创建的 Database 和 Schema 名，随后进入下一页面：

    ![Configuration](/media/integrate/configuration.png)

5. 在 **Configuration** 页面中，`record value format` 和 `record key format` 都选择 `AVRO`，点击 **Continue**，直到 Connector 创建完成。等待 Connector 状态变为 `RUNNING`，这个过程可能持续数分钟。

    ![Data preview](/media/integrate/data-preview.png)

6. 在 Snowflake 控制面板中，选择 **Data** > **Database** > **TPCC** > **TiCDC**，可以观察到 TiDB 中的增量数据实时同步到了 Snowflake，如上图。至此，就完成了 TiDB 与 Snowflake 的数据集成。

## 与 SQL Server 进行数据集成

SQL Server 是 Microsoft 推出的关系型数据库软件。借助 Confluent 的能力，你只需要创建 SQL Server Sink Connector，就可以将 TiDB 的增量数据输出到 SQL Server。

1. 连接 SQL Server 服务器，创建名为 `tpcc` 的数据库：

    ```shell
    [ec2-user@ip-172-1-1-1 bin]$ sqlcmd -S 10.61.43.14,1433 -U admin
    Password:
    1> create database tpcc
    2> go
    1> select name from master.dbo.sysdatabases
    2> go
    name
    ----------------------------------------------------------------------
    master
    tempdb
    model
    msdb
    rdsadmin
    tpcc

    (6 rows affected)
    ```

2. 在 Confluent 集群控制面板中，选择 **Data Integration** > **Connectors** > **Microsoft SQL Server Sink**，进入如下页面：

    ![Topic selection](/media/integrate/topic-selection.png)

3. 选择需要同步到 SQL Server 的 Topic 后，进入下一页面：

    ![Authentication](/media/integrate/authentication.png)

4. 在填写 SQL Server 的连接和认证信息后，进入下一页面：

    ![Configuration](/media/integrate/configuration.png)

5. 在 **Configuration** 界面，按下表进行配置：

    | Input Kafka record value format | AVRO |
    | :- | :- |
    | Insert mode | UPSERT |
    | Auto create table | true |
    | Auto add columns | true |
    | PK mode | record\_key |
    | Input Kafka record key format | AVRO |
    | Delete on null | true |

6. 配置完成后，选择 **Continue**，等待 Connector 状态变为 **RUNNING**，这个过程可能持续数分钟。

    ![Results](/media/integrate/results.png)

7. 连接 SQL Server。观察 TiDB 中的增量数据实时同步到了 SQL Server，如上图。至此，就完成了 TiDB 与 SQL Server 的数据集成。
