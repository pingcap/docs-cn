---
title: Replicate Data to Pulsar
summary: Learn how to replicate data to Pulsar using TiCDC.
---

# Replicate Data to Pulsar

This document describes how to create a changefeed that replicates incremental data to Pulsar using TiCDC.

## Create a replication task to replicate incremental data to Pulsar

Create a replication task by running the following command:

```shell
cdc cli changefeed create \
    --server=http://127.0.0.1:8300 \
--sink-uri="pulsar://127.0.0.1:6650/persistent://public/default/yktest?protocol=canal-json" \
--config=./t_changefeed.toml \
--changefeed-id="simple-replication-task"
```

```shell

Create changefeed successfully!
ID: simple-replication-task
Info: {"upstream_id":7277814241002263370,"namespace":"default","id":"simple-replication-task","sink_uri":"pulsar://127.0.0.1:6650/consumer-test?protocol=canal-json","create_time":"2023-11-28T14:42:32.000904+08:00","start_ts":444203257406423044,"config":{"memory_quota":1073741824,"case_sensitive":false,"force_replicate":false,"ignore_ineligible_table":false,"check_gc_safe_point":true,"enable_sync_point":false,"bdr_mode":false,"sync_point_interval":600000000000,"sync_point_retention":86400000000000,"filter":{"rules":["pulsar_test.*"]},"mounter":{"worker_num":16},"sink":{"protocol":"canal-json","csv":{"delimiter":",","quote":"\"","null":"\\N","include_commit_ts":false,"binary_encoding_method":"base64"},"dispatchers":[{"matcher":["pulsar_test.*"],"partition":"","topic":"test_{schema}_{table}"}],"encoder_concurrency":16,"terminator":"\r\n","date_separator":"day","enable_partition_separator":true,"enable_kafka_sink_v2":false,"only_output_updated_columns":false,"delete_only_output_handle_key_columns":false,"pulsar_config":{"connection-timeout":30,"operation-timeout":30,"batching-max-messages":1000,"batching-max-publish-delay":10,"send-timeout":30},"advance_timeout":150},"consistent":{"level":"none","max_log_size":64,"flush_interval":2000,"use_file_backend":false},"scheduler":{"enable_table_across_nodes":false,"region_threshold":100000,"write_key_threshold":0},"integrity":{"integrity_check_level":"none","corruption_handle_level":"warn"}},"state":"normal","creator_version":"v7.5.0","resolved_ts":444203257406423044,"checkpoint_ts":444203257406423044,"checkpoint_time":"2023-09-12 14:42:31.410"}
```

The meaning of each parameter is as follows:

- `--server`: the address of a TiCDC server in the TiCDC cluster.
- `--changefeed-id`: the ID of the replication task. The format must match the regular expression `^[a-zA-Z0-9]+(\-[a-zA-Z0-9]+)*$`. If the ID is not specified, TiCDC automatically generates a UUID (in the version 4 format) as the ID.
- `--sink-uri`: the downstream address of the replication task. See [Use Sink URI to configure Pulsar](#sink-uri).
- `--start-ts`: the start TSO of the changefeed. The TiCDC cluster starts pulling data from this TSO. The default value is the current time.
- `--target-ts`: the target TSO of the changefeed. The TiCDC cluster stops pulling data at this TSO. It is empty by default, which means that TiCDC does not automatically stop pulling data.
- `--config`: the changefeed configuration file. See [TiCDC changefeed configuration parameters](/ticdc/ticdc-changefeed-config.md).

## Use Sink URI and changefeed config to configure Pulsar

You can use Sink URI to specify the connection information for the TiCDC target system, and use changefeed config to configure parameters related to Pulsar.

### Sink URI

A Sink URI follows the following format:

```shell
[scheme]://[userinfo@][host]:[port][/path]?[query_parameters]
```

Configuration example 1:

```shell
--sink-uri="pulsar://127.0.0.1:6650/persistent://abc/def/yktest?protocol=canal-json"
```

Configuration example 2:

```shell
--sink-uri="pulsar://127.0.0.1:6650/yktest?protocol=canal-json"
```

The configurable parameters in a URI are as follows:

| Parameter           | Description                                                   |
| :------------------ | :------------------------------------------------------------ |
| `127.0.0.1`          | The IP address by which the downstream Pulsar provides service.             |
| `6650`               | The connection port for the downstream Pulsar.                              |
| `persistent://abc/def/yktest`   |  As shown in the preceding configuration example 1, this parameter is used to specify the tenant, namespace, and topic of Pulsar.   |
| `yktest`    | As shown in the preceding configuration example 2, if the topic you want to specify is in the default namespace `default` of the default tenant `public` in Pulsar, you can configure the URI with just the topic name, for example, `yktest`. This is equivalent to specifying the topic as `persistent://public/default/yktest`. |

### Changefeed config parameters

The following are examples of changefeed config parameters:

```toml
[sink]
# `dispatchers` is used to specify matching rules.
# Note: When the downstream MQ is Pulsar, if the routing rule for `partition` is not specified as any of `ts`, `index-value`, `table`, or `default`, each Pulsar message will be routed using the string you set as the key.
# For example, if you specify the routing rule for a matcher as the string `code`, then all Pulsar messages that match that matcher will be routed with `code` as the key.
# dispatchers = [
#    {matcher = ['test1.*', 'test2.*'], topic = "Topic expression 1", partition = "ts" },
#    {matcher = ['test3.*', 'test4.*'], topic = "Topic expression 2", partition = "index-value" },
#    {matcher = ['test1.*', 'test5.*'], topic = "Topic expression 3", partition = "table"},
#    {matcher = ['test6.*'], partition = "default"},
#    {matcher = ['test7.*'], partition = "test123"}
# ]

# `protocol` is used to specify the protocol format for encoding messages.
# When the downstream is Pulsar, the protocol can only be canal-json.
# protocol = "canal-json"

# The following parameters only take effect when the downstream is Pulsar.
[sink.pulsar-config]
# Authentication on the Pulsar server is done using a token. Specify the value of the token.
authentication-token = "xxxxxxxxxxxxx"
# When you use a token for Pulsar server authentication, specify the path to the file where the token is located.
token-from-file="/data/pulsar/token-file.txt"
# Pulsar uses the basic account and password to authenticate the identity. Specify the account.
basic-user-name="root"
# Pulsar uses the basic account and password to authenticate the identity. Specify the password.
basic-password="password"
# The certificate path for Pulsar TLS encrypted authentication.
auth-tls-certificate-path="/data/pulsar/certificate"
# The private key path for Pulsar TLS encrypted authentication.
auth-tls-private-key-path="/data/pulsar/certificate.key"
# Path to trusted certificate file of the Pulsar TLS encrypted authentication.
tls-trust-certs-file-path="/data/pulsar/tls-trust-certs-file"
# Pulsar oauth2 issuer-url. For more information, see the Pulsar website: https://pulsar.apache.org/docs/2.10.x/client-libraries-go/#tls-encryption-and-authentication
oauth2.oauth2-issuer-url="https://xxxx.auth0.com"
# Pulsar oauth2 audience
oauth2.oauth2-audience="https://xxxx.auth0.com/api/v2/"
# Pulsar oauth2 private-key
oauth2.oauth2-private-key="/data/pulsar/privateKey"
# Pulsar oauth2 client-id
oauth2.oauth2-client-id="0Xx...Yyxeny"
# Pulsar oauth2 oauth2-scope
oauth2.oauth2-scope="xxxx"
# The number of cached Pulsar producers in TiCDC. The value is 10240 by default. Each Pulsar producer corresponds to one topic. If the number of topics you need to replicate is larger than the default value, you need to increase the number.
pulsar-producer-cache-size=10240
# Pulsar data compression method. No compression is used by default. Optional values are "lz4", "zlib", and "zstd".
compression-type=""
# The timeout for the Pulsar client to establish a TCP connection with the server. The value is 5 seconds by default.
connection-timeout=5
# The timeout for Pulsar clients to initiate operations such as creating and subscribing to a topic. The value is 30 seconds by default.
operation-timeout=30
# The maximum number of messages in a single batch for a Pulsar producer to send. The value is 1000 by default.
batching-max-messages=1000
# The interval at which Pulsar producer messages are saved for batching. The value is 10 milliseconds by default.
batching-max-publish-delay=10
# The timeout for a Pulsar producer to send a message. The value is 30 seconds by default.
send-timeout=30
```

### Best practice

* You need to specify the `protocol` parameter when creating a changefeed. Currently, only the `canal-json` protocol is supported for replicating data to Pulsar.
* The `pulsar-producer-cache-size` parameter indicates the number of producers cached in the Pulsar client. Because each producer in Pulsar can only correspond to one topic, TiCDC adopts the LRU method to cache producers, and the default limit is 10240. If the number of topics you need to replicate is larger than the default value, you need to increase the number.

### TiCDC authentication and authorization for Pulsar

The following is a sample configuration when you use token authentication with Pulsar:

- Token

    Sink URI: 

    ```shell
    --sink-uri="pulsar://127.0.0.1:6650/persistent://public/default/yktest?protocol=canal-json"
    ```

    Config parameter: 

    ```shell
    [sink.pulsar-config]
    authentication-token = "xxxxxxxxxxxxx"
    ```

- Token from file

    Sink URI: 

    ```shell
    --sink-uri="pulsar://127.0.0.1:6650/persistent://public/default/yktest?protocol=canal-json"
    ```

    Config parameter: 

    ```toml
    [sink.pulsar-config]
    # Pulsar uses tokens for authentication on the Pulsar server. Specify the path to the token file, which will be read from the TiCDC server.
    token-from-file="/data/pulsar/token-file.txt"
    ```

- TLS encrypted authentication

    Sink URI: 

    ```shell
    --sink-uri="pulsar+ssl://127.0.0.1:6650/persistent://public/default/yktest?protocol=canal-json"
    ```

    Config parameters: 

    ```toml
    [sink.pulsar-config]
    # Certificate path of the Pulsar TLS encrypted authentication
    auth-tls-certificate-path="/data/pulsar/certificate"
    # Private key path of the Pulsar TLS encrypted authentication
    auth-tls-private-key-path="/data/pulsar/certificate.key"
    # Path to trusted certificate file of the Pulsar TLS encrypted authentication
    tls-trust-certs-file-path="/data/pulsar/tls-trust-certs-file"
    ```

- OAuth2 authentication

    Sink URI: 

    ```shell
    --sink-uri="pulsar+ssl://127.0.0.1:6650/persistent://public/default/yktest?protocol=canal-json"
    ```

    Config parameters: 

    ```toml
    [sink.pulsar-config]
    # Pulsar oauth2 issuer-url. For more information, see the Pulsar website: https://pulsar.apache.org/docs/2.10.x/client-libraries-go/#oauth2-authentication
    oauth2.oauth2-issuer-url="https://xxxx.auth0.com"
    # Pulsar oauth2 audience
    oauth2.oauth2-audience="https://xxxx.auth0.com/api/v2/"
    # Pulsar oauth2 private-key
    oauth2.oauth2-private-key="/data/pulsar/privateKey"
    # Pulsar oauth2 client-id
    oauth2.oauth2-client-id="0Xx...Yyxeny"
    # Pulsar oauth2 oauth2-scope
    oauth2.oauth2-scope="xxxx"
    ```

## Customize the dispatching rules for topics and partitions in Pulsar Sink

### Matching rules for Matcher

Take the `dispatchers` configuration item in the following sample configuration file as an example:

```toml
[sink]
dispatchers = [
  {matcher = ['test1.*', 'test2.*'], topic = "Topic expression 1", partition = "ts" },
  {matcher = ['test3.*', 'test4.*'], topic = "Topic expression 2", partition = "index-value" },
  {matcher = ['test1.*', 'test5.*'], topic = "Topic expression 3", partition = "table"},
  {matcher = ['test6.*'], partition = "default"},
  {matcher = ['test7.*'], partition = "test123"}
]
```

- The tables that match a matcher rule are dispatched according to the policy specified by the corresponding topic expression. For example, the table `test3.aa` is dispatched according to `Topic expression 2`, and the table `test5.aa` is dispatched according to `Topic expression 3`.
- For a table that matches more than one matcher rule, it is dispatched according to the first matching topic expression. For example, the table `test1.aa` is dispatched according to `Topic expression 1`.
- For tables that do not match any matcher, the corresponding data change events are sent to the default topic specified in `-sink-uri`. For example, the table `test10.aa` is sent to the default topic.
- For tables that match the matcher rule but do not have a topic dispatcher specified, the corresponding data changes are sent to the default topic specified in `-sink-uri`. For example, the table `test6.abc` is sent to the default topic.

### Topic dispatcher

You can use `topic = "xxx"` to specify a topic dispatcher and use topic expressions to implement flexible topic dispatching policies. It is recommended that the total number of topics be less than 1000.

The format of a topic expression is `[prefix]{schema}[middle][{table}][suffix]`. The following are the meanings of each part:

- `prefix`: Optional. Represents the prefix of the topic name.
- `{schema}`: Optional. Represents the database name.
- `middle`: Optional. Represents the separator between a database name and a table name.
- `{table}`: Optional. Represents the table name.
- `suffix`: Optional. Represents the suffix of the topic name.

`prefix`, `middle`, and `suffix` only support uppercase and lowercase letters (`a-z`, `A-Z`), numbers (`0-9`), dots (`.`), underscores (`_`), and hyphens (`-`). `{schema}` and `{table}` must be lowercase. Placeholders such as `{Schema}` and `{TABLE}` that contain uppercase letters are invalid.

The following are some examples:

- `matcher = ['test1.table1', 'test2.table2'], topic = "hello_{schema}_{table}"`
    - Data change events corresponding to the table `test1.table1` are despatched to a topic named `hello_test1_table1`.
    - Data change events corresponding to the table `test2.table2` are despatched to a topic named `hello_test2_table2`.

- `matcher = ['test3.*', 'test4.*'], topic = "hello_{schema}_world"`
    - Data change events for all tables under `test3` are despatched to a topic named `hello_test3_world`.
    - Data change events for all tables under `test4` are despatched to a topic named `hello_test4_world`.

- `matcher = ['*.*'], topic = "{schema}_{table}"`
    - For all tables that TiCDC listens on, they are despatched to separate topics according to the `databaseName_tableName` rule. For example, for the table `test.account`, TiCDC despatches its data change log to a topic named `test_account`.

### Dispatch DDL events

#### Database-level DDL events

DDL statements such as `CREATE DATABASE` and `DROP DATABASE` that are not related to a specific table are called database-level DDL statements. Events corresponding to database-level DDL statements are dispatched to the default topic specified in `--sink-uri`.

#### Table-level DDL events

DDL statements such as `ALTER TABLE` and `CREATE TABLE` that are related to a specific table are called table-level DDL statements. Events corresponding to table-level DDL statements are dispatched to an appropriate topic according to the configuration of `dispatchers`.

For example, for a `dispatchers` configuration like `matcher = ['test.*'], topic = {schema}_{table}`, the DDL events are despatched as follows:

- If a DDL event only involves a single table, the DDL event is dispatched to the appropriate topic as it is. For example, for the DDL event `DROP TABLE test.table1`, the event is dispatched to the topic named `test_table1`.

- If a DDL event involves more than one table (`RENAME TABLE`, `DROP TABLE`, and `DROP VIEW` might all involve more than one table), the single DDL event is split into multiple ones and dispatched to appropriate topics. For example, for the DDL event `RENAME TABLE test.table1 TO test.table10, test.table2 TO test.table20`, the processing is as follows:

    - Dispatch the DDL event for `RENAME TABLE test.table1 TO test.table10` to a topic named `test_table1`.
    - Dispatch the DDL event for `RENAME TABLE test.table2 TO test.table20` to a topic named `test_table2`.

### Partition dispatcher

Currently, TiCDC only supports consumers to consume messages using the exclusive subscription model, that is, each consumer can consume messages from all partitions in a topic.

You can specify a partition dispatcher with `partition = "xxx"`. The following partition dispatches are supported: `default`, `ts`, `index-value`, and `table`. If you fill in any other string, TiCDC will pass that string as the `key` of the message in the messages sent to the Pulsar server.

The dispatching rules are as follows:

- `default`: By default, events are dispatched by the schema name and table name, which is the same as when `table` is specified.
- `ts`: Use commitTs of row changes to perform hash calculation and dispatch events.
- `index-value`: Use the value of the table primary key or unique index to perform hash calculation and dispatch events.
- `table`: Use the schema name and table name to perform hash calculation and dispatch events.
- Other self-defined string: The self-defined string is used directly as the key for the Pulsar message, and the Pulsar producer uses this key value for dispatching.
