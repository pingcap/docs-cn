---
title: 同步数据到 Pulsar
summary: 了解如何使用 TiCDC 将数据同步到 Pulsar。
---

# 同步数据到 Pulsar

本文介绍如何使用 TiCDC 创建一个将增量数据复制到 Pulsar 的 Changefeed。

## 创建同步任务，复制增量数据到 Pulsar

使用以下命令来创建同步任务：

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
Info: {"upstream_id":7277814241002263370,"namespace":"default","id":"simple-replication-task","sink_uri":"pulsar://127.0.0.1:6650/consumer-test?protocol=canal-json","create_time":"2024-07-04T14:42:32.000904+08:00","start_ts":444203257406423044,"config":{"memory_quota":1073741824,"case_sensitive":false,"force_replicate":false,"ignore_ineligible_table":false,"check_gc_safe_point":true,"enable_sync_point":false,"bdr_mode":false,"sync_point_interval":600000000000,"sync_point_retention":86400000000000,"filter":{"rules":["pulsar_test.*"]},"mounter":{"worker_num":16},"sink":{"protocol":"canal-json","csv":{"delimiter":",","quote":"\"","null":"\\N","include_commit_ts":false,"binary_encoding_method":"base64"},"dispatchers":[{"matcher":["pulsar_test.*"],"partition":"","topic":"test_{schema}_{table}"}],"encoder_concurrency":16,"terminator":"\r\n","date_separator":"day","enable_partition_separator":true,"only_output_updated_columns":false,"delete_only_output_handle_key_columns":false,"pulsar_config":{"connection-timeout":30,"operation-timeout":30,"batching-max-messages":1000,"batching-max-publish-delay":10,"send-timeout":30},"advance_timeout":150},"consistent":{"level":"none","max_log_size":64,"flush_interval":2000,"use_file_backend":false},"scheduler":{"enable_table_across_nodes":false,"region_threshold":100000,"write_key_threshold":0},"integrity":{"integrity_check_level":"none","corruption_handle_level":"warn"}},"state":"normal","creator_version":"v8.3.0","resolved_ts":444203257406423044,"checkpoint_ts":444203257406423044,"checkpoint_time":"2024-08-22 14:42:31.410"}
```

各参数的含义如下：

- `--server`：TiCDC 集群中任意一个 TiCDC 服务器的地址。
- `--changefeed-id`：同步任务的 ID，格式需要符合正则表达式 `^[a-zA-Z0-9]+(\-[a-zA-Z0-9]+)*$`。如果不指定该 ID，TiCDC 会自动生成一个 UUID（version 4 格式）作为 ID。
- `--sink-uri`：同步任务下游的地址，详见：[使用 Sink URI 配置 Pulsar](#sink-uri)。
- `--start-ts`：指定 changefeed 的开始 TSO。TiCDC 集群将从这个 TSO 开始拉取数据。默认为当前时间。
- `--target-ts`：指定 changefeed 的目标 TSO。TiCDC 集群拉取数据直到这个 TSO 停止。默认为空，即 TiCDC 不会自动停止。
- `--config`：指定 changefeed 配置文件，详见：[TiCDC Changefeed 配置参数](/ticdc/ticdc-changefeed-config.md)。

## 使用 Sink URI 和 Changefeed config 配置 Pulsar

Sink URI 用于指定 TiCDC 目标系统的连接信息，Changefeed config 用来配置 Pulsar 相关的参数。

### Sink URI

Sink URI 遵循以下格式：

```shell
[scheme]://[userinfo@][host]:[port][/path]?[query_parameters]
```

配置示例 1：

```shell
--sink-uri="pulsar://127.0.0.1:6650/persistent://abc/def/yktest?protocol=canal-json"
```

配置示例 2：

```shell
--sink-uri="pulsar://127.0.0.1:6650/yktest?protocol=canal-json"
```

URI 中可配置的的参数如下：

| 参数               | 描述                                                         |
| :------------------ | :------------------------------------------------------------ |
| `pulsar` | 下游 Pulsar 的连接协议，支持 `pulsar`、`pulsar+ssl`、`pulsar+http` 和 `pulsar+https` 四种协议，其中 `pulsar+http` 和 `pulsar+https` 从 v8.2.0 开始支持。|
| `127.0.0.1`          | 下游 Pulsar 对外提供服务的 IP。                                 |
| `6650`               | 下游 Pulsar 的连接端口。                                          |
| `persistent://abc/def/yktest`   |  参考上面的示例 1，该参数用于指定 Pulsar 的租户、命名空间、topic。                                      |
| `yktest`    | 参考上面的示例 2，如果你想要指定的 topic 在 Pulsar 的默认租户 `public` 下的默认命名空间 `default` 中，你可以在 URI 中只配置 topic 名，例如 `yktest`。该写法相当于指定 topic 为 `persistent://public/default/yktest`。 |

### Changefeed config 参数

以下为 Changefeed config 参数示例：

```toml
[sink]
# `dispatchers` 用于指定 matcher 匹配规则
# 注意：当下游 MQ 为 Pulsar 时，如果 `partition` 的路由规则未被指定为 `ts`、`index-value`、`table`、或 `default` 中的任意一种，将会使用你设置的字符串作为每一条 Pulsar message 的 key 进行路由。例如，如果你指定的路由规则为字符串 `code`，那么符合该 matcher 的所有 Pulsar message 都将会以 `code` 作为 key 进行路由。
# dispatchers = [
#    {matcher = ['test1.*', 'test2.*'], topic = "Topic 表达式 1", partition = "ts" },
#    {matcher = ['test3.*', 'test4.*'], topic = "Topic 表达式 2", partition = "index-value" },
#    {matcher = ['test1.*', 'test5.*'], topic = "Topic 表达式 3", partition = "table"},
#    {matcher = ['test6.*'], partition = "default"},
#    {matcher = ['test7.*'], partition = "test123"}
# ]

# `protocol` 用于指定编码消息时使用的格式协议。
# 当下游类型是 Pulsar 时，仅支持 canal-json 协议
# protocol = "canal-json"

# 以下参数仅在下游为 Pulsar 时生效。
[sink.pulsar-config]
# 使用 token 进行 Pulsar 服务端的认证，此处为 token 的值。
authentication-token = "xxxxxxxxxxxxx"
# 指定使用 token 进行 Pulsar 服务端的认证，此处为 token 所在文件的路径。
token-from-file="/data/pulsar/token-file.txt"
# Pulsar 使用 basic 账号密码验证身份。
basic-user-name="root"
# Pulsar 使用 basic 账号密码验证身份，此处为密码。
basic-password="password"
# Pulsar 启用 mTLS 认证时，客户端的证书路径。
auth-tls-certificate-path="/data/pulsar/certificate"
# Pulsar 启用 mTLS 认证时，客户端的私钥路径。
auth-tls-private-key-path="/data/pulsar/certificate.key"
# Pulsar TLS 可信证书文件路径，在 Pulsar 启用 mTLS 认证或者 TLS 加密传输时，需要指定该参数。
tls-trust-certs-file-path="/data/pulsar/tls-trust-certs-file"
# Pulsar 启用 TLS 加密传输时，客户端的加密私钥路径。
tls-key-file-path="/data/pulsar/tls-key-file"
# Pulsar 启用 TLS 加密传输时，客户端的加密证书文件路径。
tls-certificate-file="/data/pulsar/tls-certificate-file"
# Pulsar oauth2 issuer-url 更多详细配置请看 Pulsar 官方介绍：https://pulsar.apache.org/docs/2.10.x/client-libraries-go/#tls-encryption-and-authentication
oauth2.oauth2-issuer-url="https://xxxx.auth0.com"
# Pulsar oauth2 audience
oauth2.oauth2-audience="https://xxxx.auth0.com/api/v2/"
# Pulsar oauth2 private-key
oauth2.oauth2-private-key="/data/pulsar/privateKey"
# Pulsar oauth2 client-id
oauth2.oauth2-client-id="0Xx...Yyxeny"
# Pulsar oauth2 oauth2-scope
oauth2.oauth2-scope="xxxx"
# TiCDC 中缓存 Pulsar Producer 的个数，默认上限为 10240 个。每个 Pulsar Producer 对应一个 topic，如果你需要同步的 topic 数量大于默认值，则需要调大该数量。
pulsar-producer-cache-size=10240
# Pulsar 数据压缩方式，默认不压缩，可选值为 "lz4"、"zlib"、"zstd"
compression-type=""
# Pulsar 客户端与服务端建立 TCP 连接的超时时间，默认 5 秒。
connection-timeout=5
# Pulsar 客户端发起创建、订阅等操作的超时时间，默认为 30 秒。
operation-timeout=30
# Pulsar producer 发送消息时的单个 batch 内的消息数量上限，默认值为 1000。
batching-max-messages=1000
# Pulsar producer 消息攒批的时间间隔，默认 10 毫秒。
batching-max-publish-delay=10
# Pulsar producer 发送消息的超时时间，默认 30 秒。
send-timeout=30
```

### 最佳实践

* 你需要在创建 Changefeed 的时候设置 `protocol` 参数。目前同步数据到 Pulsar 仅支持使用 `canal-json` 协议。
* `pulsar-producer-cache-size` 参数表示 Pulsar 客户端中缓存 Producer 的数量，因为 Pulsar 的每个 Producer 只能对应一个 topic，TiCDC 采用 LRU 方式缓存 Producer，默认限制为 10240 个。如果你需要同步的 topic 数量大于默认值，则需要调大该数量。

### TLS 加密传输

TiCDC 从 v7.5.1 和 v8.0.0 开始支持 Pulsar 的 TLS 加密传输，配置样例如下所示：

Sink URI：

```shell
--sink-uri="pulsar+ssl://127.0.0.1:6651/persistent://public/default/yktest?protocol=canal-json"
```

config 参数：

```toml
[sink.pulsar-config]
tls-trust-certs-file-path="/data/pulsar/tls-trust-certs-file"
```

如果你的 Pulsar 服务端设置了 `tlsRequireTrustedClientCertOnConnect=true` 参数，那么你需要同时在 changefeed 的配置文件中设置 `tls-key-file-path` 和 `tls-certificate-file` 参数。如下所示：

```toml
[sink.pulsar-config]
tls-trust-certs-file-path="/data/pulsar/tls-trust-certs-file"
tls-certificate-file="/data/pulsar/tls-certificate-file"
tls-key-file-path="/data/pulsar/tls-key-file"
```

### TiCDC 使用 Pulsar 的认证与授权

使用 Pulsar 的 token 认证时配置样例如下所示：

- Token

    Sink URI：

    ```shell
    --sink-uri="pulsar://127.0.0.1:6650/persistent://public/default/yktest?protocol=canal-json"
    ```

    config 参数：

    ```shell
    [sink.pulsar-config]
    authentication-token = "xxxxxxxxxxxxx"
    ```

- Token from file

    Sink URI：

    ```shell
    --sink-uri="pulsar://127.0.0.1:6650/persistent://public/default/yktest?protocol=canal-json"
    ```

    config 参数：

    ```toml
    [sink.pulsar-config]
    # Pulsar 使用 token 进行 Pulsar 服务端的认证，但这里配置的是 token 文件的路径，会从 TiCDC Server 所在机器上读取。
    token-from-file="/data/pulsar/token-file.txt"
    ```

- mTLS 认证

    Sink URI：

    ```shell
    --sink-uri="pulsar+ssl://127.0.0.1:6651/persistent://public/default/yktest?protocol=canal-json"
    ```

    config 参数：

    ```toml
    [sink.pulsar-config]
    # Pulsar mTLS 认证证书路径
    auth-tls-certificate-path="/data/pulsar/certificate"
    # Pulsar mTLS 认证私钥路径
    auth-tls-private-key-path="/data/pulsar/certificate.key"
    # Pulsar mTLS 可信证书文件路径
    tls-trust-certs-file-path="/data/pulsar/tls-trust-certs-file"
    ```

- OAuth2 认证

    TiCDC 从 v7.5.1 和 v8.0.0 开始支持 Pulsar 的 OAuth2 认证，配置样例如下所示：

    Sink URI：

    ```shell
    --sink-uri="pulsar://127.0.0.1:6650/persistent://public/default/yktest?protocol=canal-json"
    ```

    config 参数：

    ```toml
    [sink.pulsar-config]
    # Pulsar oauth2 issuer-url 更多详细配置请参见 Pulsar 官方介绍：https://pulsar.apache.org/docs/2.10.x/client-libraries-go/#oauth2-authentication
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

## 自定义 Pulsar Sink 的 Topic 和 Partition 的分发规则

### Matcher 匹配规则

以如下示例配置文件中的 `dispatchers` 配置项为例：

```toml
[sink]
dispatchers = [
  {matcher = ['test1.*', 'test2.*'], topic = "Topic 表达式 1", partition = "ts" },
  {matcher = ['test3.*', 'test4.*'], topic = "Topic 表达式 2", partition = "index-value" },
  {matcher = ['test1.*', 'test5.*'], topic = "Topic 表达式 3", partition = "table"},
  {matcher = ['test6.*'], partition = "default"},
  {matcher = ['test7.*'], partition = "test123"}
]
```

- 对于匹配了 matcher 规则的表，按照对应的 topic 表达式指定的策略进行分发。例如，表 `test3.aa` 会按照 `Topic 表达式 2` 分发，表 `test5.aa` 会按照 `Topic 表达式 3` 分发。
- 对于匹配了多个 matcher 规则的表，以靠前的 matcher 对应的 topic 表达式为准。例如，表 `test1.aa` 会按照 `Topic 表达式 1` 分发。
- 对于没有匹配任何 matcher 的表，将对应的数据变更事件发送到 `--sink-uri` 中指定的默认 topic 中。例如，表 `test10.aa` 会发送到默认 topic。
- 对于匹配了 matcher 规则但是没有指定 topic 分发器的表，将对应的数据变更发送到 `--sink-uri` 中指定的默认 topic 中。例如，表 `test6.abc` 会发送到默认 topic。

### Topic 分发器

Topic 分发器用 `topic = "xxx"` 来指定，并使用 topic 表达式来实现灵活的 topic 分发策略。topic 的总数建议小于 1000。

Topic 表达式的基本规则为 `[tenant_and_namespace][prefix]{schema}[middle][{table}][suffix]`，详细解释如下：

- `tenant_and_namespace`：可选项，代表 Topic 所在的租户和命名空间，比如 `persistent://abc/def/`。如果不配置，则代表 Topic 在 Pulsar 的默认租户 `public` 下的默认命名空间 `default` 中。
- `prefix`：可选项，代表 Topic Name 的前缀。
- `{schema}`：可选项，用于匹配库名。
- `middle`：可选项，代表库表名之间的分隔符。
- `{table}`：可选项，用于匹配表名。
- `suffix`：可选项，代表 Topic Name 的后缀。

其中 `prefix`、`middle` 以及 `suffix` 仅允许出现大小写字母（`a-z`、`A-Z`）、数字（`0-9`）、点号（`.`）、下划线（`_`）和中划线（`-`）。`{schema}`、`{table}` 均为小写，诸如 `{Schema}` 以及 `{TABLE}` 等包含大写字母的占位符是无效的。

下面是一些示例：

- `matcher = ['test1.table1', 'test2.table2'], topic = "hello_{schema}_{table}"`
    - 对于表 `test1.table1` 对应的数据变更事件，发送到名为 `hello_test1_table1` 的 topic 中。
    - 对于表 `test2.table2` 对应的数据变更事件，发送到名为 `hello_test2_table2` 的 topic 中。

- `matcher = ['test3.*', 'test4.*'], topic = "hello_{schema}_world"`
    - 对于 `test3` 下的所有表对应的数据变更事件，发送到名为 `hello_test3_world` 的 topic 中。
    - 对于 `test4` 下的所有表对应的数据变更事件，发送到名为 `hello_test4_world` 的 topic 中。

- `matcher = ['*.*'], topic = "{schema}_{table}"`
    - 对于 TiCDC 监听的所有表，按照“库名_表名”的规则分别分发到独立的 topic 中。例如，对于 `test.account` 表，TiCDC 会将其数据变更日志分发到名为 `test_account` 的 topic 中。

### DDL 事件的分发

#### 库级别 DDL

诸如 `CREATE DATABASE` 和 `DROP DATABASE` 等和某一张具体的表无关的 DDL，称为库级别 DDL。对于库级别 DDL 对应的事件，被发送到 `--sink-uri` 中指定的默认 topic 中。

#### 表级别 DDL

诸如 `ALTER TABLE`、`CREATE TABLE` 这类和某一张具体的表相关的 DDL，称之为表级别 DDL。对于表级别 DDL 对应的事件，按照 `dispatchers` 的配置，被发送到相应的 topic 中。

例如，对于 `matcher = ['test.*'], topic = {schema}_{table}` 这样的 `dispatchers` 配置，DDL 事件分发情况如下：

- 若 DDL 事件中涉及单张表，则将 DDL 事件原样发送到相应的 topic 中。例如，对于 DDL 事件 `DROP TABLE test.table1`，该事件会被发送到名为 `test_table1` 的 topic 中。

- 若 DDL 事件中涉及多张表（`RENAME TABLE`、`DROP TABLE`、`DROP VIEW` 都可能涉及多张表），则将单个 DDL 事件拆分为多个发送到相应的 topic 中。例如，对于 DDL 事件 `RENAME TABLE test.table1 TO test.table10, test.table2 TO test.table20`，处理如下：

    - 将 `RENAME TABLE test.table1 TO test.table10` 的 DDL 事件发送到名为 `test_table1` 的 topic 中，
    - 将 `RENAME TABLE test.table2 TO test.table20` 的 DDL 事件发送到名为 `test.table2` 的 topic 中。

### Partition 分发器

目前 TiCDC 仅支持消费者使用 Exclusive 的订阅模式对消息进行消费，即每个消费者将会消费一个 topic 中所有 Partition 中的消息。

Partition 分发器用 `partition = "xxx"` 来指定，支持 `default`、`ts`、`index-value`、`table` 四种 Partition 分发器。但如果你填入其他字段，则会在发送给 Pulsar Server 的消息中将该字段透传给 Message 的 `key`。

具体分发规则如下：

- `default`：默认按照 schema 名和 table 名进行 event 分发，和指定 `table` 时相同。
- `ts`：以行变更的 commitTs 做 Hash 计算并进行 event 分发。
- `index-value`：以表的主键或者唯一索引的值做 Hash 计算并进行 event 分发。
- `table`：以表的 schema 名和 table 名做 Hash 计算并进行 event 分发。
- 其他：将会直接把该值作为 Pulsar message 的 key，Pulsar Producer 会使用该 key 值进行分发。
