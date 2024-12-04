---
title: TiCDC Changefeed 命令行参数和配置参数
summary: 了解 TiCDC Changefeed 详细的命令行参数和配置文件定义。
---

# TiCDC Changefeed 命令行参数和配置参数

## TiCDC Changefeed 命令行参数

本章节将以创建同步任务为例，介绍 TiCDC Changefeed 的命令行参数：

```shell
cdc cli changefeed create --server=http://10.0.10.25:8300 --sink-uri="mysql://root:123456@127.0.0.1:3306/" --changefeed-id="simple-replication-task"
```

```shell
Create changefeed successfully!
ID: simple-replication-task
Info: {"upstream_id":7178706266519722477,"namespace":"default","id":"simple-replication-task","sink_uri":"mysql://root:xxxxx@127.0.0.1:4000/?time-zone=","create_time":"2024-11-11T15:05:46.679218+08:00","start_ts":438156275634929669,"engine":"unified","config":{"case_sensitive":false,"enable_old_value":true,"force_replicate":false,"ignore_ineligible_table":false,"check_gc_safe_point":true,"enable_sync_point":true,"bdr_mode":false,"sync_point_interval":30000000000,"sync_point_retention":3600000000000,"filter":{"rules":["test.*"],"event_filters":null},"mounter":{"worker_num":16},"sink":{"protocol":"","schema_registry":"","csv":{"delimiter":",","quote":"\"","null":"\\N","include_commit_ts":false},"column_selectors":null,"transaction_atomicity":"none","encoder_concurrency":16,"terminator":"\r\n","date_separator":"none","enable_partition_separator":false},"consistent":{"level":"none","max_log_size":64,"flush_interval":2000,"storage":""}},"state":"normal","creator_version":"v8.4.0"}
```

- `--changefeed-id`：同步任务的 ID，格式需要符合正则表达式 `^[a-zA-Z0-9]+(\-[a-zA-Z0-9]+)*$`。如果不指定该 ID，TiCDC 会自动生成一个 UUID（version 4 格式）作为 ID。
- `--sink-uri`：同步任务下游的地址，需要按照以下格式进行配置，目前 scheme 支持 `mysql`、`tidb` 和 `kafka`。

    ```
    [scheme]://[userinfo@][host]:[port][/path]?[query_parameters]
    ```

    URI 中包含特殊字符时，如 `! * ' ( ) ; : @ & = + $ , / ? % # [ ]`，需要对 URI 特殊字符进行转义处理。你可以在 [URI Encoder](https://www.urlencoder.org/) 中对 URI 进行转义。

- `--start-ts`：指定 changefeed 的开始 TSO。TiCDC 集群将从这个 TSO 开始拉取数据。默认为当前时间。
- `--target-ts`：指定 changefeed 的目标 TSO。TiCDC 集群拉取数据直到这个 TSO 停止。默认为空，即 TiCDC 不会自动停止。
- `--config`：指定 changefeed 配置文件。

## TiCDC Changefeed 配置文件说明

本章节详细介绍了同步任务的配置。

```toml
# 指定该 Changefeed 在 Capture Server 中内存配额的上限。对于超额使用部分，
# 会在运行中被 Go runtime 优先回收。默认值为 `1073741824`，即 1 GB。
# memory-quota = 1073741824

# 指定配置文件中涉及的库名、表名是否为大小写敏感
# 该配置会同时影响 filter 和 sink 相关配置。自 v6.5.6、v7.1.3 和 v7.5.0 起，默认值由 true 改为 false
case-sensitive = false

# 指定是否强制同步不存在有效索引的表，默认值为 false
# 详情请参考：https://docs.pingcap.com/zh/tidb/stable/ticdc-manage-changefeed#同步没有有效索引的表
force-replicate=false

# 是否开启 Syncpoint 功能，从 v6.3.0 开始支持，该功能默认关闭。
# 从 v6.4.0 开始，使用 Syncpoint 功能需要同步任务拥有下游集群的 SYSTEM_VARIABLES_ADMIN 或者 SUPER 权限。
# 注意：该参数只有当下游为 TiDB 时，才会生效。
# enable-sync-point = false

# Syncpoint 功能对齐上下游 snapshot 的时间间隔
# 配置格式为 h m s，例如 "1h30m30s"
# 默认值为 10m，最小值为 30s
# 注意：该参数只有当下游为 TiDB 时，才会生效。
# sync-point-interval = "5m"

# Syncpoint 功能在下游表中保存的数据的时长，超过这个时间的数据会被清理
# 配置格式为 h m s，例如 "24h30m30s"
# 默认值为 24h
# 注意：该参数只有当下游为 TiDB 时，才会生效。
# sync-point-retention = "1h"

# 从 v6.5.6、v7.1.3、v7.5.0 起引入，用于设置解析 DDL 时使用的 SQL 模式，多个模式之间用逗号分隔
# 默认值和 TiDB 的默认 SQL 模式一致
# sql-mode = "ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION"

# 默认值为 false，表示不处于 BDR 模式。
# 如果要使用 TiCDC 搭建 BDR 集群，需要将该参数设置为 true，同时要将 TiDB 集群设置为 BDR 模式。
# 详情请参考：https://docs.pingcap.com/zh/tidb/stable/ticdc-bidirectional-replication#ticdc-双向复制
# bdr-mode = false

# changefeed 发生内部错误或异常时允许自动重试的时间，默认值为 30 分钟。
# 若 changefeed 发生内部错误或异常，且持续时间超过该参数设置的时间，changefeed 会进入 Failed 状态。
# 当 changefeed 处于 failed 状态时，需要手动重启 changefeed 才能恢复。
# 配置格式为 "h m s"，例如 "1h30m30s"。
changefeed-error-stuck-duration = "30m"

[mounter]
# mounter 解码 KV 数据的线程数，默认值为 16
# worker-num = 16

[filter]
# 忽略指定 start_ts 的事务
# ignore-txn-start-ts = [1, 2]

# 过滤器规则
# 过滤规则语法：https://docs.pingcap.com/zh/tidb/stable/table-filter#表库过滤语法
rules = ['*.*', '!test.*']

# 事件过滤器规则
# 事件过滤器的详细配置规则可参考：https://docs.pingcap.com/zh/tidb/stable/ticdc-filter
# 第一个事件过滤器规则
# [[filter.event-filters]]
# matcher = ["test.worker"] # matcher 是一个白名单，表示该过滤规则只应用于 test 库中的 worker 表
# ignore-event = ["insert"] # 过滤掉 insert 事件
# ignore-sql = ["^drop", "add column"] # 过滤掉以 "drop" 开头或者包含 "add column" 的 DDL
# ignore-delete-value-expr = "name = 'john'" # 过滤掉包含 name = 'john' 条件的 delete DML
# ignore-insert-value-expr = "id >= 100" # 过滤掉包含 id >= 100 条件的 insert DML
# ignore-update-old-value-expr = "age < 18" # 过滤掉旧值 age < 18 的 update DML
# ignore-update-new-value-expr = "gender = 'male'" # 过滤掉新值 gender = 'male' 的 update DML

# 第二个事件过滤器规则
# [[filter.event-filters]]
# matcher = ["test.fruit"] # 该事件过滤器只应用于 test.fruit 表
# ignore-event = ["drop table", "delete"] # 忽略 drop table 的 DDL 事件和 delete 类型的 DML 事件。需要注意的是，在更新 TiDB 中聚簇索引的列值时，TiCDC 会将一个 UPDATE 事件拆分成为 DELETE 和 INSERT 事件，TiCDC 无法将该类事件识别为 UPDATE 事件，因此无法正确地进行过滤。
# ignore-sql = ["^drop table", "alter table"] # 忽略以 drop table 开头的，或者包含 alter table 的 DDL 语句
# ignore-insert-value-expr = "price > 1000 and origin = 'no where'" # 忽略包含 price > 1000 和 origin = 'no where' 条件的 insert DML

[scheduler]
# 将表以 Region 为单位分配给多个 TiCDC 节点进行同步。
# 注意：该功能只在 Kafka changefeed 上生效，暂不支持 MySQL changefeed。
# 默认为 "false"。设置为 "true" 以打开该功能。
enable-table-across-nodes = false
# enable-table-across-nodes 开启后，有两种分配模式
# 1. 按 Region 的数量分配，即每个 CDC 节点处理 region 的个数基本相等。当某个表 Region 个数大于 `region-threshold` 值时，会将表分配到多个节点处理。`region-threshold` 默认值为 10000。
# region-threshold = 10000
# 2. 按写入的流量分配，即每个 CDC 节点处理 region 总修改行数基本相当。只有当表中每分钟修改行数超过 `write-key-threshold` 值时，该表才会生效。
# write-key-threshold = 30000
# 注意：
# `write-key-threshold` 参数默认值为 0，代表默认不会采用流量的分配模式。
# 两种方式配置一种即可生效，当 `region-threshold` 和 `write-key-threshold` 同时配置时，TiCDC 将优先采用按流量分配的模式，即 `write-key-threshold`。


[sink]
############ 以下是 MQ 类型 sink 配置 ############
# 对于 MQ 类的 Sink，可以通过 dispatchers 配置 event 分发器
# 支持 partition 及 topic（从 v6.1 开始支持）两种 event 分发器。二者的详细说明见下一节。
# matcher 的匹配语法和过滤器规则语法相同，matcher 匹配规则的详细说明见下一节。
# 注意：该参数只有当下游为消息队列时，才会生效。
# 注意：当下游 MQ 为 Pulsar 时，如果 partition 的路由规则未指定为 'ts', 'index-value', 'table', 'default' 中的任意一个，那么将会使用你设置的字符串作为每一条 Pulsar message 的 key 进行路由。例如，如果你指定的路由规则为 'code' 字符串，那么符合该 matcher 的所有 Pulsar message 都将会以 'code' 作为 key 进行路由。
# dispatchers = [
#    {matcher = ['test1.*', 'test2.*'], topic = "Topic 表达式 1", partition = "index-value"},
#    {matcher = ['test3.*', 'test4.*'], topic = "Topic 表达式 2", partition = "index-value", index = "index1"},
#    {matcher = ['test1.*', 'test5.*'], topic = "Topic 表达式 3", partition = "table"},
#    {matcher = ['test6.*'], partition = "columns", columns = "['a', 'b']"}
#    {matcher = ['test7.*'], partition = "ts"}
# ]

# column-selectors 从 v7.5.0 开始引入，仅对 Kafka Sink 生效。
# column-selectors 用于选择部分列进行同步。
# column-selectors = [
#     {matcher = ['test.t1'], columns = ['a', 'b']},
#     {matcher = ['test.*'], columns = ["*", "!b"]},
#     {matcher = ['test1.t1'], columns = ['column*', '!column1']},
#     {matcher = ['test3.t'], columns = ["column?", "!column1"]},
# ]

# protocol 用于指定编码消息时使用的格式协议
# 当下游类型是 Kafka 时，支持 canal-json、avro、debezium、open-protocol、simple。
# 当下游类型是 Pulsar 时，仅支持 canal-json 协议。
# 当下游类型是存储服务时，目前仅支持 canal-json、csv 两种协议。
# 注意：该参数只有当下游为 Kafka、Pulsar，或存储服务时，才会生效。
# protocol = "canal-json"

# delete-only-output-handle-key-columns 用于指定 Delete 事件的输出内容，只对 canal-json 和 open-protocol 协议有效。从 v7.2.0 开始引入。
# 该参数和 `force-replicate` 参数不兼容，如果同时将该参数和 `force-replicate` 设置为 true，创建 changefeed 会报错。
# 默认值为 false，即输出所有列的内容。当设置为 true 时，只输出主键列，或唯一索引列的内容。
# Avro 协议不受该参数控制，总是只输出主键列，或唯一索引列的内容。
# CSV 协议不受该参数控制，总是输出所有列的内容。
delete-only-output-handle-key-columns = false

# Schema 注册表的 URL。
# 注意：该参数只有当下游为消息队列时，才会生效。
# schema-registry = "http://localhost:80801/subjects/{subject-name}/versions/{version-number}/schema"

# 编码数据时所用编码器的线程数。
# 默认值为 32。
# 注意：该参数只有当下游为消息队列时，才会生效。
# encoder-concurrency = 32

# 是否开启 Kafka Sink V2。Kafka Sink V2 内部使用 kafka-go 实现。
# 默认值为 false。
# 注意：该参数是一个实验特性，并且只有当下游为消息队列时才会生效。
# enable-kafka-sink-v2 = false

# 是否只向下游同步有内容更新的列。从 v7.1.0 开始支持。
# 默认值为 false。
# 注意：该参数只有当下游为消息队列，并且使用 Open Protocol 或 Canal-JSON 时，才会生效。
# only-output-updated-columns = false

############ 以下是存储服务类型 sink 配置 ############
# 以下三个配置项仅在同步到存储服务的 sink 中使用，在 MQ 和 MySQL 类 sink 中无需设置。
# 换行符，用来分隔两个数据变更事件。默认值为空，表示使用 "\r\n" 作为换行符。
# terminator = ''

# 文件路径的日期分隔类型。可选类型有 `none`、`year`、`month` 和 `day`。默认值为 `day`，即按天分隔。详见 <https://docs.pingcap.com/zh/tidb/stable/ticdc-sink-to-cloud-storage#数据变更记录>。
# 注意：该参数只有当下游为存储服务时，才会生效。
date-separator = 'day'

# 是否使用 partition 作为分隔字符串。默认值为 true，即一张表中各个 partition 的数据会分不同的目录来存储。建议保持该配置项为 true 以避免下游分区表可能丢数据的问题 <https://github.com/pingcap/tiflow/issues/8581>。使用示例详见 <https://docs.pingcap.com/zh/tidb/dev/ticdc-sink-to-cloud-storage#数据变更记录>。
# 注意：该参数只有当下游为存储服务时，才会生效。
enable-partition-separator = true

# 是否关闭 schema 信息的输出。默认值为 false，即输出 schema 信息。
# 注意：该参数只有当 sink 类型为 MQ 且输出协议为 Debezium 时才生效。
debezium-disable-schema = false

# 从 v6.5.0 开始，TiCDC 支持以 CSV 格式将数据变更记录保存至存储服务中，在 MQ 和 MySQL 类 sink 中无需设置。
# [sink.csv]
# 字段之间的分隔符。必须为 ASCII 字符，默认值为 `,`。
# delimiter = ','
# 用于包裹字段的引号字符。空值代表不使用引号字符。默认值为 `"`。
# quote = '"'
# CSV 中列为 NULL 时将以什么字符来表示。默认值为 `\N`。
# null = '\N'
# 是否在 CSV 行中包含 commit-ts。默认值为 false。
# include-commit-ts = false
# 二进制类型数据的编码方式，可选 'base64' 或 'hex'。默认值为 'base64'。
# binary-encoding-method = 'base64'
# 是否输出 handle 列信息。默认值为 false。该配置项仅用于内部实现，不推荐设置该配置项。
# output-handle-key = false
# 是否输出行数据更改前的值。默认值为 false。开启后，Update 事件会输出两行数据：第一行为 Delete 事件，输出更改前的数据；第二行为 Insert 事件，输出更改后的数据。
# 开启后，即当该参数设为 true 时，会在变更数据列前增加 "is-update" 列。该列用来标识当前行的变更数据是来自 Update 事件，还是原始的 Insert/Delete 事件。
# 如果当前行的变更数据来自 Update 事件，则 "is-update" 列为 true，否则为 false。
# output-old-value = false

# 从 v8.0.0 开始，TiCDC 新增了 Simple Protocol 消息编码协议，以下为该协议的配置参数。
# 关于该协议的详情，请参考 <https://docs.pingcap.com/zh/tidb/stable/ticdc-simple-protocol>。
# 以下为 Simple Protocol 参数，用来控制 bootstrap 消息的发送行为。
# send-bootstrap-interval-in-sec 用来控制发送 bootstrap 消息的时间间隔，单位为秒。
# 默认值为 120 秒，即每张表每隔 120 秒发送一次 bootstrap 消息。
# send-bootstrap-interval-in-sec = 120

# send-bootstrap-in-msg-count 用来控制发送 bootstrap 的消息间隔，单位为消息数。
# 默认值为 10000，即每张表每发送 10000 条行变更消息就发送一次 bootstrap 消息。
# send-bootstrap-in-msg-count = 10000
# 注意：如果要关闭 bootstrap 消息的发送，则将 send-bootstrap-interval-in-sec 和 send-bootstrap-in-msg-count 均设置为 0。

# send-bootstrap-to-all-partition 用来控制是否发送 bootstrap 消息到所有的 partition。
# 默认值为 true，即发送 bootstrap 消息到对应表 topic 的所有的 partition。
# 如果设置为 false，则只发送 bootstrap 消息到对应表 topic 的第一个 partition。
# send-bootstrap-to-all-partition = true

[sink.kafka-config.codec-config]
# encoding-format 用来控制 simple protocol 的消息的编码格式，目前支持 "json" 和 "avro" 两种格式。
# 默认值为 "json"。
# encoding-format = "json"

[sink.open]
# 是否输出行数据更改前的值。默认值为 true。关闭后，Update 事件不会输出 "p" 字段的数据。
# output-old-value = true

[sink.debezium]
# 是否输出行数据更改前的值。默认值为 true。关闭后，Update 事件不会输出 "before" 字段的数据。
# output-old-value = true

# consistent 中的字段用于配置 Changefeed 的数据一致性。详细的信息，请参考 <https://docs.pingcap.com/tidb/stable/ticdc-sink-to-mysql#eventually-consistent-replication-in-disaster-scenarios>。
# 注意：一致性相关参数只有当下游为数据库并且开启 redo log 功能时，才会生效。
[consistent]
# 数据一致性级别。默认值为 "none"，可选值为 "none" 和 "eventual"。
# 设置为 "none" 时将关闭 redo log。
level = "none"
# redo log 的最大日志大小，单位为 MB。默认值为 64。
max-log-size = 64
# 两次 redo log 刷新的时间间隔，单位为毫秒。默认值为 2000。
flush-interval = 2000
# redo log 使用存储服务的 URI。默认值为空。
storage = ""
# 是否将 redo log 存储到本地文件中。默认值为 false。
use-file-backend = false
# 控制 redo 模块中编解码 worker 的数量，默认值为 16。
encoding-worker-num = 16
# 控制 redo 模块中上传文件 worker 的数量，默认值为 8。
flush-worker-num = 8
# redo log 文件的压缩行为，可选值为 "" 和 "lz4"。默认值为 ""，表示不进行压缩。
compression = ""
# redo log 上传单个文件的并发数，默认值为 1，表示禁用并发。
flush-concurrency = 1

[integrity]
# 是否开启单行数据的 Checksum 校验功能，默认值为 "none"，即不开启。可选值为 "none" 和 "correctness"。
integrity-check-level = "none"
# 当单行数据的 Checksum 校验失败时，Changefeed 打印错误行数据相关日志的级别。默认值为 "warn"，可选值为 "warn" 和 "error"。
corruption-handle-level = "warn"

# 以下参数仅在下游为 Kafka 时生效。
[sink.kafka-config]
# Kafka SASL 认证机制。该参数默认值为空，表示不使用 SASL 认证。
sasl-mechanism = "OAUTHBEARER"
# Kafka SASL OAUTHBEARER 认证机制中的 client-id。默认值为空。在使用该认证机制时，该参数必填。
sasl-oauth-client-id = "producer-kafka"
# Kafka SASL OAUTHBEARER 认证机制中的 client-secret。默认值为空。需要 Base64 编码。在使用该认证机制时，该参数必填。
sasl-oauth-client-secret = "cHJvZHVjZXIta2Fma2E="
# Kafka SASL OAUTHBEARER 认证机制中的 token-url 用于获取 token。默认值为空。在使用该认证机制时，该参数必填。
sasl-oauth-token-url = "http://127.0.0.1:4444/oauth2/token"
# Kafka SASL OAUTHBEARER 认证机制中的 scopes。默认值为空。在使用该认证机制时，该参数可选填。
sasl-oauth-scopes = ["producer.kafka", "consumer.kafka"]
# Kafka SASL OAUTHBEARER 认证机制中的 grant-type。默认值为 "client_credentials"。在使用该认证机制时，该参数可选填。
sasl-oauth-grant-type = "client_credentials"
# Kafka SASL OAUTHBEARER 认证机制中的 audience。默认值为空。在使用该认证机制时，该参数可选填。
sasl-oauth-audience = "kafka"

# 控制是否输出原始的数据变更事件，默认值为 false。更多信息，请参考 https://docs.pingcap.com/zh/tidb/dev/ticdc-split-update-behavior#控制是否拆分主键或唯一键-update-事件
# output-raw-change-event = false

# 以下配置仅在选用 avro 作为协议，并且使用 AWS Glue Schema Registry 时需要配置
# 请参考 "同步数据到 Kafka" 这一文档中 "使用 AWS Glue Schema Registry" 这一节内容：https://docs.pingcap.com/zh/tidb/dev/ticdc-sink-to-kafka#ticdc-集成-aws-glue-schema-registry
# [sink.kafka-config.glue-schema-registry-config]
# region="us-west-1"
# registry-name="ticdc-test"
# access-key="xxxx"
# secret-access-key="xxxx"
# token="xxxx"

# 以下参数仅在下游为 Pulsar 时生效。
[sink.pulsar-config]
# 使用 token 进行 Pulsar 服务端的认证，此处为 token 的值。
authentication-token = "xxxxxxxxxxxxx"
# 指定使用 token 进行 Pulsar 服务端的认证，此处为 token 所在文件的路径。
token-from-file="/data/pulsar/token-file.txt"
# Pulsar 使用 basic 账号密码验证身份。
basic-user-name="root"
# Pulsar  使用 basic 账号密码验证身份，此处为密码。
basic-password="password"
# Pulsar TLS 加密认证证书路径。
auth-tls-certificate-path="/data/pulsar/certificate"
# Pulsar TLS 加密认证私钥路径。
auth-tls-private-key-path="/data/pulsar/certificate.key"
# Pulsar TLS 加密可信证书文件路径。
tls-trust-certs-file-path="/data/pulsar/tls-trust-certs-file"
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
# Pulsar 数据压缩方式，默认不压缩，可选 "lz4"、"zlib"、"zstd"。
compression-type=""
# Pulsar 客户端与服务端建立 TCP 连接的超时时间，默认 5 秒。
connection-timeout=5
# Pulsar 客户端发起创建、订阅等操作的超时时间，默认为 30 秒。
operation-timeout=30
# Pulsar Producer 发送消息时的单个 batch 内的消息数量上限，默认值为 1000。
batching-max-messages=1000
# Pulsar Producer 消息攒批的时间间隔，默认 10 毫秒。
batching-max-publish-delay=10
# Pulsar Producer 发送消息的超时时间，默认 30 秒。
send-timeout=30

# 控制是否输出原始的数据变更事件，默认值为 false。更多信息，请参考 https://docs.pingcap.com/zh/tidb/dev/ticdc-split-update-behavior#控制是否拆分主键或唯一键-update-事件
# output-raw-change-event = false

[sink.cloud-storage-config]
# 向下游存储服务保存数据变更记录的并发度，默认值为 16。
worker-count = 16
# 向下游存储服务保存数据变更记录的间隔，默认值为 "2s"。
flush-interval = "2s"
# 单个数据变更文件的字节数超过 `file-size` 时将其保存至存储服务中，默认值为 67108864，即 64 MiB。
file-size = 67108864
# 文件保留的时长，仅在 date-separator 配置为 day 时生效，默认值为 0，表示禁用文件清理。假设 `file-expiration-days = 1` 且 `file-cleanup-cron-spec = "0 0 0 * * *"`，TiCDC 将在每天 00:00:00 时刻清理已保存超过 24 小时的文件。例如，2023/12/02 00:00:00 将清理 2023/12/01 之前（注意：不包括 2023/12/01）的文件。
file-expiration-days = 0
# 定时清理任务的运行周期，与 crontab 配置兼容，格式为 `<Second> <Minute> <Hour> <Day of the month> <Month> <Day of the week (Optional)>`，默认值为 "0 0 2 * * *"，表示每天凌晨两点执行清理任务
file-cleanup-cron-spec = "0 0 2 * * *"
# 上传单个文件的并发数，默认值为 1，表示禁用并发。
flush-concurrency = 1
# 控制是否输出原始的数据变更事件，默认值为 false。更多信息，请参考 https://docs.pingcap.com/zh/tidb/dev/ticdc-split-update-behavior#控制是否拆分主键或唯一键-update-事件
output-raw-change-event = false
```
