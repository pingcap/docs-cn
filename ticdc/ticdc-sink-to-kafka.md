---
title: Replicate Data to Kafka
summary: Learn how to replicate data to Apache Kafka using TiCDC.
---

# Replicate Data to Kafka

This document describes how to create a changefeed that replicates incremental data to Apache Kafka using TiCDC.

## Create a replication task

Create a replication task by running the following command:

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

- `--server`: The address of any TiCDC server in the TiCDC cluster.
- `--changefeed-id`: The ID of the replication task. The format must match the `^[a-zA-Z0-9]+(\-[a-zA-Z0-9]+)*$` regular expression. If this ID is not specified, TiCDC automatically generates a UUID (the version 4 format) as the ID.
- `--sink-uri`: The downstream address of the replication task. For details, see [Configure sink URI with `kafka`](#configure-sink-uri-for-kafka).
- `--start-ts`: Specifies the starting TSO of the changefeed. From this TSO, the TiCDC cluster starts pulling data. The default value is the current time.
- `--target-ts`: Specifies the ending TSO of the changefeed. To this TSO, the TiCDC cluster stops pulling data. The default value is empty, which means that TiCDC does not automatically stop pulling data.
- `--config`: Specifies the changefeed configuration file. For details, see [TiCDC Changefeed Configuration Parameters](/ticdc/ticdc-changefeed-config.md).

## Configure sink URI for Kafka

Sink URI is used to specify the connection information of the TiCDC target system. The format is as follows:

```shell
[scheme]://[userinfo@][host]:[port][/path]?[query_parameters]
```

Sample configuration:

```shell
--sink-uri="kafka://127.0.0.1:9092/topic-name?protocol=canal-json&kafka-version=2.4.0&partition-num=6&max-message-bytes=67108864&replication-factor=1"
```

The following are descriptions of sink URI parameters and values that can be configured for Kafka:

| Parameter/Parameter value               | Description                                                        |
| :------------------ | :------------------------------------------------------------ |
| `127.0.0.1`          | The IP address of the downstream Kafka services.                                 |
| `9092`               | The port for the downstream Kafka.                                          |
| `topic-name` | Variable. The name of the Kafka topic. |
| `kafka-version`      | The version of the downstream Kafka (optional, `2.4.0` by default. Currently, the earliest supported Kafka version is `0.11.0.2` and the latest one is `3.2.0`. This value needs to be consistent with the actual version of the downstream Kafka).                      |
| `kafka-client-id`    | Specifies the Kafka client ID of the replication task (optional. `TiCDC_sarama_producer_replication ID` by default). |
| `partition-num`      | The number of the downstream Kafka partitions (optional. The value must be **no greater than** the actual number of partitions; otherwise, the replication task cannot be created successfully. `3` by default). |
| `max-message-bytes`  | The maximum size of data that is sent to Kafka broker each time (optional, `10MB` by default). From v5.0.6 and v4.0.6, the default value has changed from `64MB` and `256MB` to `10MB`. |
| `replication-factor` | The number of Kafka message replicas that can be saved (optional, `1` by default).                       |
| `required-acks` | A parameter used in the `Produce` request, which notifies the broker of the number of replica acknowledgements it needs to receive before responding. Value options are `0` (`NoResponse`: no response, only `TCP ACK` is provided), `1` (`WaitForLocal`: responds only after local commits are submitted successfully), and `-1` (`WaitForAll`: responds after all replicated replicas are committed successfully. You can configure the minimum number of replicated replicas using the [`min.insync.replicas`](https://kafka.apache.org/33/documentation.html#brokerconfigs_min.insync.replicas) configuration item of the broker). (Optional, the default value is `-1`).    |
| `compression` | The compression algorithm used when sending messages (value options are `none`, `lz4`, `gzip`, `snappy`, and `zstd`; `none` by default). |
| `protocol` | The protocol with which messages are output to Kafka. The value options are `canal-json`, `open-protocol`, `canal`, `avro` and `maxwell`.   |
| `auto-create-topic` | Determines whether TiCDC creates the topic automatically when the `topic-name` passed in does not exist in the Kafka cluster (optional, `true` by default). |
| `enable-tidb-extension` | Optional. `false` by default. When the output protocol is `canal-json`, if the value is `true`, TiCDC sends [WATERMARK events](/ticdc/ticdc-canal-json.md#watermark-event) and adds the [TiDB extension field](/ticdc/ticdc-canal-json.md#tidb-extension-field) to Kafka messages. From v6.1.0, this parameter is also applicable to the `avro` protocol. If the value is `true`, TiCDC adds [three TiDB extension fields](/ticdc/ticdc-avro-protocol.md#tidb-extension-fields) to the Kafka message. |
| `max-batch-size` | New in v4.0.9. If the message protocol supports outputting multiple data changes to one Kafka message, this parameter specifies the maximum number of data changes in one Kafka message. It currently takes effect only when Kafka's `protocol` is `open-protocol` (optional, `16` by default). |
| `enable-tls` | Whether to use TLS to connect to the downstream Kafka instance (optional, `false` by default). |
| `ca` | The path of the CA certificate file needed to connect to the downstream Kafka instance (optional).  |
| `cert` | The path of the certificate file needed to connect to the downstream Kafka instance (optional). |
| `key` | The path of the certificate key file needed to connect to the downstream Kafka instance (optional). |
| `insecure-skip-verify` | Whether to skip certificate verification when connecting to the downstream Kafka instance (optional, `false` by default). |
| `sasl-user` | The identity (authcid) of SASL/PLAIN or SASL/SCRAM authentication needed to connect to the downstream Kafka instance (optional). |
| `sasl-password` | The password of SASL/PLAIN or SASL/SCRAM authentication needed to connect to the downstream Kafka instance (optional). If it contains special characters, they need to be URL encoded. |
| `sasl-mechanism` | The name of SASL authentication needed to connect to the downstream Kafka instance. The value can be `plain`, `scram-sha-256`, `scram-sha-512`, or `gssapi`. |
| `sasl-gssapi-auth-type` | The gssapi authentication type. Values can be `user` or `keytab` (optional). |
| `sasl-gssapi-keytab-path` | The gssapi keytab path (optional).|
| `sasl-gssapi-kerberos-config-path` | The gssapi kerberos configuration path (optional). |
| `sasl-gssapi-service-name` | The gssapi service name (optional). |
| `sasl-gssapi-user` | The user name of gssapi authentication (optional). |
| `sasl-gssapi-password` | The password of gssapi authentication (optional). If it contains special characters, they need to be URL encoded. |
| `sasl-gssapi-realm` | The gssapi realm name (optional). |
| `sasl-gssapi-disable-pafxfast` | Whether to disable the gssapi PA-FX-FAST (optional). |
| `dial-timeout` | The timeout in establishing a connection with the downstream Kafka. The default value is `10s`. |
| `read-timeout` | The timeout in getting a response returned by the downstream Kafka. The default value is `10s`. |
| `write-timeout` | The timeout in sending a request to the downstream Kafka. The default value is `10s`. |
| `avro-decimal-handling-mode` | Only effective with the `avro` protocol. Determines how Avro handles the DECIMAL field. The value can be `string` or `precise`, indicating either mapping the DECIMAL field to a string or a precise floating number.  |
| `avro-bigint-unsigned-handling-mode` | Only effective with the `avro` protocol. Determines how Avro handles the BIGINT UNSIGNED field. The value can be `string` or `long`, indicating either mapping the BIGINT UNSIGNED field to a 64-bit signed number or a string.  |

### Best practices

* It is recommended that you create your own Kafka Topic. At a minimum, you need to set the maximum amount of data of each message that the Topic can send to the Kafka broker, and the number of downstream Kafka partitions. When you create a changefeed, these two settings correspond to `max-message-bytes` and `partition-num`, respectively.
* If you create a changefeed with a Topic that does not yet exist, TiCDC will try to create the Topic using the `partition-num` and `replication-factor` parameters. It is recommended that you specify these parameters explicitly.
* In most cases, it is recommended to use the `canal-json` protocol.

> **Note:**
>
> When `protocol` is `open-protocol`, TiCDC tries to avoid generating messages that exceed `max-message-bytes` in length. However, if a row is so large that a single change alone exceeds `max-message-bytes` in length, to avoid silent failure, TiCDC tries to output this message and prints a warning in the log.

### TiCDC uses the authentication and authorization of Kafka

The following are examples when using Kafka SASL authentication:

- SASL/PLAIN

  ```shell
  --sink-uri="kafka://127.0.0.1:9092/topic-name?kafka-version=2.4.0&sasl-user=alice-user&sasl-password=alice-secret&sasl-mechanism=plain"
  ```

- SASL/SCRAM

  SCRAM-SHA-256 and SCRAM-SHA-512 are similar to the PLAIN method. You just need to specify `sasl-mechanism` as the corresponding authentication method.

- SASL/GSSAPI

  SASL/GSSAPI `user` authentication:

  ```shell
  --sink-uri="kafka://127.0.0.1:9092/topic-name?kafka-version=2.4.0&sasl-mechanism=gssapi&sasl-gssapi-auth-type=user&sasl-gssapi-kerberos-config-path=/etc/krb5.conf&sasl-gssapi-service-name=kafka&sasl-gssapi-user=alice/for-kafka&sasl-gssapi-password=alice-secret&sasl-gssapi-realm=example.com"
  ```

  Values of `sasl-gssapi-user` and `sasl-gssapi-realm` are related to the [principle](https://web.mit.edu/kerberos/krb5-1.5/krb5-1.5.4/doc/krb5-user/What-is-a-Kerberos-Principal_003f.html) specified in kerberos. For example, if the principle is set as `alice/for-kafka@example.com`, then `sasl-gssapi-user` and `sasl-gssapi-realm` are specified as `alice/for-kafka` and `example.com` respectively.

  SASL/GSSAPI `keytab` authentication:

  ```shell
  --sink-uri="kafka://127.0.0.1:9092/topic-name?kafka-version=2.4.0&sasl-mechanism=gssapi&sasl-gssapi-auth-type=keytab&sasl-gssapi-kerberos-config-path=/etc/krb5.conf&sasl-gssapi-service-name=kafka&sasl-gssapi-user=alice/for-kafka&sasl-gssapi-keytab-path=/var/lib/secret/alice.key&sasl-gssapi-realm=example.com"
  ```

  For more information about SASL/GSSAPI authentication methods, see [Configuring GSSAPI](https://docs.confluent.io/platform/current/kafka/authentication_sasl/authentication_sasl_gssapi.html).

- TLS/SSL encryption

    If the Kafka broker has TLS/SSL encryption enabled, you need to add the `-enable-tls=true` parameter to `--sink-uri`. If you want to use self-signed certificates, you also need to specify `ca`, `cert` and `key` in `--sink-uri`.

- ACL authorization

    The minimum set of permissions required for TiCDC to function properly is as follows.

    - The `Create`, `Write`, and `Describe` permissions for the Topic [resource type](https://docs.confluent.io/platform/current/kafka/authorization.html#resources).
    - The `DescribeConfigs` permission for the Cluster resource type.

### Integrate TiCDC with Kafka Connect (Confluent Platform)

To use the [data connectors](https://docs.confluent.io/current/connect/managing/connectors.html) provided by Confluent to stream data to relational or non-relational databases, you need to use the `avro` protocol and provide a URL for [Confluent Schema Registry](https://www.confluent.io/product/confluent-platform/data-compatibility/) in `schema-registry`.

Sample configuration:

```shell
--sink-uri="kafka://127.0.0.1:9092/topic-name?&protocol=avro&replication-factor=3" --schema-registry="http://127.0.0.1:8081" --config changefeed_config.toml
```

```shell
[sink]
dispatchers = [
 {matcher = ['*.*'], topic = "tidb_{schema}_{table}"},
]
```

For detailed integration guide, see [Quick Start Guide on Integrating TiDB with Confluent Platform](/ticdc/integrate-confluent-using-ticdc.md).

## Customize the rules for Topic and Partition dispatchers of Kafka Sink

### Matcher rules

Take the following configuration of `dispatchers` as an example:

```toml
[sink]
dispatchers = [
  {matcher = ['test1.*', 'test2.*'], topic = "Topic expression 1", partition = "ts" },
  {matcher = ['test3.*', 'test4.*'], topic = "Topic expression 2", partition = "index-value" },
  {matcher = ['test1.*', 'test5.*'], topic = "Topic expression 3", partition = "table"},
  {matcher = ['test6.*'], partition = "ts"}
]
```

- For the tables that match the matcher rule, they are dispatched according to the policy specified by the corresponding topic expression. For example, the `test3.aa` table is dispatched according to "Topic expression 2"; the `test5.aa` table is dispatched according to "Topic expression 3".
- For a table that matches multiple matcher rules, it is dispatched according to the first matching topic expression. For example, the `test1.aa` table is distributed according to "Topic expression 1".
- For tables that do not match any matcher rule, the corresponding data change events are sent to the default topic specified in `--sink-uri`. For example, the `test10.aa` table is sent to the default topic.
- For tables that match the matcher rule but do not specify a topic dispatcher, the corresponding data changes are sent to the default topic specified in `--sink-uri`. For example, the `test6.aa` table is sent to the default topic.

### Topic dispatchers

You can use topic = "xxx" to specify a Topic dispatcher and use topic expressions to implement flexible topic dispatching policies. It is recommended that the total number of topics be less than 1000.

The format of the Topic expression is `[prefix]{schema}[middle][{table}][suffix]`.

- `prefix`: optional. Indicates the prefix of the Topic Name.
- `{schema}`: required. Used to match the schema name.
- `middle`: optional. Indicates the delimiter between schema name and table name.
- `{table}`: optional. Used to match the table name.
- `suffix`: optional. Indicates the suffix of the Topic Name.

`prefix`, `middle` and `suffix` can only include the following characters: `a-z`, `A-Z`, `0-9`, `.`, `_` and `-`. `{schema}` and `{table}` are both lowercase. Placeholders such as `{Schema}` and `{TABLE}` are invalid.

Some examples:

- `matcher = ['test1.table1', 'test2.table2'], topic = "hello_{schema}_{table}"`
    - The data change events corresponding to `test1.table1` are sent to the topic named `hello_test1_table1`.
    - The data change events corresponding to `test2.table2` are sent to the topic named `hello_test2_table2`.
- `matcher = ['test3.*', 'test4.*'], topic = "hello_{schema}_world"`
    - The data change events corresponding to all tables in `test3` are sent to the topic named `hello_test3_world`.
    - The data change events corresponding to all tables in `test4` are sent to the topic named `hello_test4_world`.
- `matcher = ['*.*'], topic = "{schema}_{table}"`
    - All tables listened by TiCDC are dispatched to separate topics according to the "schema_table" rule. For example, for the `test.account` table, TiCDC dispatches its data change log to a Topic named `test_account`.

### Dispatch DDL events

#### Schema-level DDLs

DDLs that are not related to a specific table are called schema-level DDLs, such as `create database` and `drop database`. The events corresponding to schema-level DDLs are sent to the default topic specified in `--sink-uri`.

#### Table-level DDLs

DDLs that are related to a specific table are called table-level DDLs, such as `alter table` and `create table`. The events corresponding to table-level DDLs are sent to the corresponding topic according to dispatcher configurations.

For example, for a dispatcher like `matcher = ['test.*'], topic = {schema}_{table}`, DDL events are dispatched as follows:

- If a single table is involved in the DDL event, the DDL event is sent to the corresponding topic as is. For example, for the DDL event `drop table test.table1`, the event is sent to the topic named `test_table1`.
- If multiple tables are involved in the DDL event (`rename table` / `drop table` / `drop view` may involve multiple tables), the DDL event is split into multiple events and sent to the corresponding topics. For example, for the DDL event `rename table test.table1 to test.table10, test.table2 to test.table20`, the event `rename table test.table1 to test.table10` is sent to the topic named `test_table1` and the event `rename table test.table2 to test.table20` is sent to the topic named `test.table2`.

### Partition dispatchers

You can use `partition = "xxx"` to specify a partition dispatcher. It supports four dispatchers: default, ts, index-value, and table. The dispatcher rules are as follows:

- default: When multiple unique indexes (including the primary key) exist or the Old Value feature is enabled, events are dispatched in the table mode. When only one unique index (or the primary key) exists, events are dispatched in the index-value mode.
- ts: Use the commitTs of the row change to hash and dispatch events.
- index-value: Use the value of the primary key or the unique index of the table to hash and dispatch events.
- table: Use the schema name of the table and the table name to hash and dispatch events.

> **Note:**
>
>
> Since v6.1.0, to clarify the meaning of the configuration, the configuration used to specify the partition dispatcher has been changed from `dispatcher` to `partition`, with `partition` being an alias for `dispatcher`. For example, the following two rules are exactly equivalent.
>
> ```
> [sink]
> dispatchers = [
>    {matcher = ['*.*'], dispatcher = "ts"},
>    {matcher = ['*.*'], partition = "ts"},
> ]
> ```
>
> However, `dispatcher` and `partition` cannot appear in the same rule. For example, the following rule is invalid.
>
> ```
> {matcher = ['*.*'], dispatcher = "ts", partition = "table"},
> ```

> **Warning:**
>
> When the [Old Value feature](/ticdc/ticdc-manage-changefeed.md#output-the-historical-value-of-a-row-changed-event) is enabled (`enable-old-value = true`), using the index-value dispatcher might fail to ensure the order of row changes with the same index value. Therefore, it is recommended to use the default dispatcher.
>
> For more information, see [What changes occur to the change event format when TiCDC enables the Old Value feature?](/ticdc/ticdc-faq.md#what-changes-occur-to-the-change-event-format-when-ticdc-enables-the-old-value-feature).

## Scale out the load of a single large table to multiple TiCDC nodes

This feature splits the data replication range of a single large table into multiple ranges, according to the data volume and the number of modified rows per minute, and it makes the data volume and the number of modified rows replicated in each range approximately the same. This feature distributes these ranges to multiple TiCDC nodes for replication, so that multiple TiCDC nodes can replicate a large single table at the same time. This feature can solve the following two problems:

- A single TiCDC node cannot replicate a large single table in time.
- The resources (such as CPU and memory) consumed by TiCDC nodes are not evenly distributed.

> **Warning:**
>
> TiCDC v7.0.0 only supports scaling out the load of a large single table on Kafka changefeeds.

Sample configuration:

```toml
[scheduler]
# The default value is "false". You can set it to "true" to enable this feature.
enable-table-across-nodes = true
# When you enable this feature, it only takes effect for tables with the number of regions greater than the `region-threshold` value.
region-threshold = 100000
# When you enable this feature, it takes effect for tables with the number of rows modified per minute greater than the `write-key-threshold` value.
# Note:
# * The default value of `write-key-threshold` is 0, which means that the feature does not split the table replication range according to the number of rows modified in a table by default.
# * You can configure this parameter according to your cluster workload. For example, if it is configured as 30000, it means that the feature will split the replication range of a table when the number of modified rows per minute in the table exceeds 30000.
# * When `region-threshold` and `write-key-threshold` are configured at the same time:
#   TiCDC will check whether the number of modified rows is greater than `write-key-threshold` first.
#   If not, next check whether the number of Regions is greater than `region-threshold`.
write-key-threshold = 30000
```

You can query the number of Regions a table contains by the following SQL statement:

```sql
SELECT COUNT(*) FROM INFORMATION_SCHEMA.TIKV_REGION_STATUS WHERE DB_NAME="database1" AND TABLE_NAME="table1" AND IS_INDEX=0;
```

## Handle messages that exceed the Kafka topic limit

Kafka topic sets a limit on the size of messages it can receive. This limit is controlled by the [`max.message.bytes`](https://kafka.apache.org/documentation/#topicconfigs_max.message.bytes) parameter. If TiCDC Kafka sink sends data that exceeds this limit, the changefeed reports an error and cannot proceed to replicate data. To solve this problem, TiCDC provides the following solution.

### Send handle keys only

Starting from v7.3.0, TiCDC Kafka sink supports sending only the handle keys when the message size exceeds the limit. This can significantly reduce the message size and avoid changefeed errors and task failures caused by the message size exceeding the Kafka topic limit. Handle Key refers to the following:

* If the table to be replicated has primary key, the primary key is the handle key.
* If the table does not have primary key but has NOT NULL Unique Key, the NOT NULL Unique Key is the handle key.

Currently, this feature supports two encoding protocols: Canal-JSON and Open Protocol. When using the Canal-JSON protocol, you must specify `enable-tidb-extension=true` in `sink-uri`.

The sample configuration is as follows:

```toml
[sink.kafka-config.large-message-handle]
# This configuration is introduced in v7.3.0.
# Empty by default, which means when the message size exceeds the limit, the changefeed fails.
# If this configuration is set to "handle-key-only", when the message size exceeds the limit, only the handle key is sent in the data field. If the message size still exceeds the limit, the changefeed fails.
large-message-handle-option = "handle-key-only"
```

### Consume messages with handle keys only

The message format with handle keys only is as follows:

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
    "_tidb": {     // TiDB extension fields
        "commitTs": 163963314122145239,
        "onlyHandleKey": true
    }
}
```

When a Kafka consumer receives a message, it first checks the `onlyHandleKey` field. If this field exists and is `true`, it means that the message only contains the handle key of the complete data. In this case, to get the complete data, you need to query the upstream TiDB and use [`tidb_snapshot` to read historical data](/read-historical-data.md).

> **Warning:**
>
> When the Kafka consumer processes data and queries TiDB, the data might have been deleted by GC. You need to [modify the GC Lifetime of the TiDB cluster](/system-variables.md#tidb_gc_life_time-new-in-v50) to a larger value to avoid this situation.
