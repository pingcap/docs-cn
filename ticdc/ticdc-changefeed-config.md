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

### `memory-quota`

- 指定该 Changefeed 在 Capture Server 中内存配额的上限。对于超额使用部分，会在运行中被 Go runtime 优先回收。默认值为 `1073741824`，即 1 GB。
- 默认值：`1073741824`

### `case-sensitive`

- 指定配置文件中涉及的库名、表名是否为大小写敏感
- 该配置会同时影响 filter 和 sink 相关配置。自 v6.5.6、v7.1.3 和 v7.5.0 起，默认值由 true 改为 false
- 默认值：`false`

### `enable-sync-point`

- 是否开启 Syncpoint 功能，从 v6.3.0 开始支持，该功能默认关闭。
- 从 v6.4.0 开始，使用 Syncpoint 功能需要同步任务拥有下游集群的 SYSTEM_VARIABLES_ADMIN 或者 SUPER 权限。
- 注意：该参数只有当下游为 TiDB 时，才会生效。
- 默认值：`false`

### `sync-point-interval`

- Syncpoint 功能对齐上下游 snapshot 的时间间隔
- 配置格式为 h m s，例如 "1h30m30s"
- 默认值为 10m，最小值为 30s
- 注意：该参数只有当下游为 TiDB 时，才会生效。
- 默认值：`"10m"`
- 最小值：`"30s"`

### `sync-point-retention`

- Syncpoint 功能在下游表中保存的数据的时长，超过这个时间的数据会被清理
- 配置格式为 h m s，例如 "24h30m30s"
- 默认值为 24h
- 注意：该参数只有当下游为 TiDB 时，才会生效
- 默认值：`"24h"`

### `sql-mode`

- 从 v6.5.6、v7.1.3、v7.5.0 起引入，用于设置解析 DDL 时使用的 SQL 模式，多个模式之间用逗号分隔
- 默认值和 TiDB 的默认 SQL 模式一致

### `bdr-mode`

- 默认值为 false，表示不处于 BDR 模式。
- 如果要使用 TiCDC 搭建 BDR 集群，需要将该参数设置为 true，同时要将 TiDB 集群设置为 BDR 模式。
- 详情请参考：https://docs.pingcap.com/zh/tidb/stable/ticdc-bidirectional-replication#ticdc-双向复制
- 默认值：`false`

### `changefeed-error-stuck-duration`

- changefeed 发生内部错误或异常时允许自动重试的时间，默认值为 30 分钟。
- 若 changefeed 发生内部错误或异常，且持续时间超过该参数设置的时间，changefeed 会进入 Failed 状态。
- 当 changefeed 处于 failed 状态时，需要手动重启 changefeed 才能恢复。
- 配置格式为 "h m s"，例如 "1h30m30s"。
- 默认值：`"30m"`

### `mounter`

- mounter 解码 KV 数据的线程数
- 默认值：`16`

#### `worker-num`

- mounter 解码 KV 数据的线程数，默认值为 16

### `filter`

#### `ignore-txn-start-ts`

- 忽略指定 start_ts 的事务

#### `rules`

- 过滤器规则
- 过滤规则语法：https://docs.pingcap.com/zh/tidb/stable/table-filter#表库过滤语法

#### `event-filters`

##### First Filter Rule

###### `matcher`

- matcher 是一个白名单，表示该过滤规则只应用于 test 库中的 worker 表

###### `ignore-event`

- 过滤掉 insert 事件

###### `ignore-sql`

- 过滤掉以 "drop" 开头或者包含 "add column" 的 DDL

###### `ignore-delete-value-expr`

- 过滤掉包含 name = 'john' 条件的 delete DML

###### `ignore-insert-value-expr`

- 过滤掉包含 id >= 100 条件的 insert DML

###### `ignore-update-old-value-expr`

- 过滤掉旧值 age < 18 的 update DML

###### `ignore-update-new-value-expr`

- 过滤掉新值 gender = 'male' 的 update DML

##### Second Filter Rule

###### `matcher`

- 该事件过滤器只应用于 test.fruit 表

###### `ignore-event`

- 忽略 drop table 的 DDL 事件和 delete 类型的 DML 事件
- 需要注意的是，在更新 TiDB 中聚簇索引的列值时，TiCDC 会将一个 UPDATE 事件拆分成为 DELETE 和 INSERT 事件，TiCDC 无法将该类事件识别为 UPDATE 事件，因此无法正确地进行过滤

###### `ignore-sql`

- 忽略以 drop table 开头的，或者包含 alter table 的 DDL 语句

###### `ignore-insert-value-expr`

- 忽略包含 price > 1000 和 origin = 'no where' 条件的 insert DML

### `scheduler`

- 将表以 Region 为单位分配给多个 TiCDC 节点进行同步
- 注意：该功能只在 Kafka changefeed 上生效，暂不支持 MySQL changefeed

#### `enable-table-across-nodes`

- 默认为 "false"。设置为 "true" 以打开该功能
- 默认值：`false`

#### `region-threshold`

- enable-table-across-nodes 开启后的分配模式之一：按 Region 的数量分配，即每个 CDC 节点处理 region 的个数基本相等。当某个表 Region 个数大于 `region-threshold` 值时，会将表分配到多个节点处理
- 默认值：`10000`

#### `write-key-threshold`

- enable-table-across-nodes 开启后的分配模式之一：按写入的流量分配，即每个 CDC 节点处理 region 总修改行数基本相当。只有当表中每分钟修改行数超过 `write-key-threshold` 值时，该表才会生效
- 默认值：`0`
- 注意：
 - `write-key-threshold` 参数默认值为 0，代表默认不会采用流量的分配模式
 - 两种方式配置一种即可生效，当 `region-threshold` 和 `write-key-threshold` 同时配置时，TiCDC 将优先采用按流量分配的模式，即 `write-key-threshold`

### `sink`

#### MQ 类型 sink 配置

##### `dispatchers`

- 对于 MQ 类的 Sink，可以通过 dispatchers 配置 event 分发器
- 支持 partition 及 topic（从 v6.1 开始支持）两种 event 分发器
- matcher 的匹配语法和过滤器规则语法相同
- 注意：该参数只有当下游为消息队列时，才会生效
- 注意：当下游 MQ 为 Pulsar 时，如果 partition 的路由规则未指定为 'ts', 'index-value', 'table', 'default' 中的任意一个，那么将会使用你设置的字符串作为每一条 Pulsar message 的 key 进行路由

##### `column-selectors`

- 从 v7.5.0 开始引入，仅对 Kafka Sink 生效
- 用于选择部分列进行同步

##### `protocol`

- 用于指定编码消息时使用的格式协议
- 当下游类型是 Kafka 时，支持 canal-json、avro、debezium、open-protocol、simple
- 当下游类型是 Pulsar 时，仅支持 canal-json 协议
- 当下游类型是存储服务时，目前仅支持 canal-json、csv 两种协议
- 注意：该参数只有当下游为 Kafka、Pulsar，或存储服务时，才会生效

##### `delete-only-output-handle-key-columns`

- 用于指定 Delete 事件的输出内容，只对 canal-json 和 open-protocol 协议有效。从 v7.2.0 开始引入
- 该参数和 `force-replicate` 参数不兼容，如果同时将该参数和 `force-replicate` 设置为 true，创建 changefeed 会报错
- 默认值：`false`

##### `schema-registry`

- Schema 注册表的 URL
- 注意：该参数只有当下游为消息队列时，才会生效

##### `encoder-concurrency`

- 编码数据时所用编码器的线程数
- 默认值：`32`
- 注意：该参数只有当下游为消息队列时，才会生效

##### `enable-kafka-sink-v2`

- 是否开启 Kafka Sink V2。Kafka Sink V2 内部使用 kafka-go 实现
- 默认值：`false`
- 注意：该参数是一个实验特性，并且只有当下游为消息队列时才会生效

##### `only-output-updated-columns`

- 是否只向下游同步有内容更新的列。从 v7.1.0 开始支持
- 默认值：`false`
- 注意：该参数只有当下游为消息队列，并且使用 Open Protocol 或 Canal-JSON 时，才会生效

#### 存储服务类型 sink 配置

##### `terminator`

- 换行符，用来分隔两个数据变更事件
- 默认值：`\r\n`

##### `date-separator`

- 文件路径的日期分隔类型
- 可选值：`none`, `year`, `month`, `day`
- 默认值：`day`
- 注意：该参数只有当下游为存储服务时，才会生效

##### `enable-partition-separator`

- 是否使用 partition 作为分隔字符串
- 默认值：`true`
- 注意：该参数只有当下游为存储服务时，才会生效

##### `debezium-disable-schema`

- 是否关闭 schema 信息的输出
- 默认值：`false`
- 注意：该参数只有当 sink 类型为 MQ 且输出协议为 Debezium 时才生效

#### `csv`

##### `delimiter`

- 字段之间的分隔符
- 必须为 ASCII 字符
- 默认值：`,`

##### `quote`

- 用于包裹字段的引号字符
- 空值代表不使用引号字符
- 默认值：`"`

##### `null`

- CSV 中列为 NULL 时将以什么字符来表示
- 默认值：`\N`

##### `include-commit-ts`

- 是否在 CSV 行中包含 commit-ts
- 默认值：`false`

##### `binary-encoding-method`

- 二进制类型数据的编码方式
- 可选值：`base64`, `hex`
- 默认值：`base64`

##### `output-handle-key`

- 是否输出 handle 列信息
- 默认值：`false`
- 该配置项仅用于内部实现，不推荐设置该配置项

##### `output-old-value`

- 是否输出行数据更改前的值
- 默认值：`false`

#### Simple Protocol 配置

##### `send-bootstrap-interval-in-sec`

- 用来控制发送 bootstrap 消息的时间间隔，单位为秒
- 默认值：`120`

##### `send-bootstrap-in-msg-count`

- 用来控制发送 bootstrap 的消息间隔，单位为消息数
- 默认值：`10000`

##### `send-bootstrap-to-all-partition`

- 用来控制是否发送 bootstrap 消息到所有的 partition
- 默认值：`true`

#### `kafka-config.codec-config`

##### `encoding-format`

- 用来控制 simple protocol 的消息的编码格式
- 可选值：`json`, `avro`
- 默认值：`json`

#### `open`

##### `output-old-value`

- 是否输出行数据更改前的值
- 默认值：`true`
- 关闭后，Update 事件不会输出 "p" 字段的数据

#### `debezium`

##### `output-old-value`

- 是否输出行数据更改前的值
- 默认值：`true`
- 关闭后，Update 事件不会输出 "before" 字段的数据

### `consistent`

- consistent 中的字段用于配置 Changefeed 的数据一致性
- 注意：一致性相关参数只有当下游为数据库并且开启 redo log 功能时，才会生效

#### `level`

- 数据一致性级别
- 默认值：`none`
- 可选值：`none`, `eventual`
- 设置为 "none" 时将关闭 redo log

#### `max-log-size`

- redo log 的最大日志大小，单位为 MB
- 默认值：`64`

#### `flush-interval`

- 两次 redo log 刷新的时间间隔，单位为毫秒
- 默认值：`2000`

#### `storage`

- redo log 使用存储服务的 URI
- 默认值：``

#### `use-file-backend`

- 是否将 redo log 存储到本地文件中
- 默认值：`false`

#### `encoding-worker-num`

- 控制 redo 模块中编解码 worker 的数量
- 默认值：`16`

#### `flush-worker-num`

- 控制 redo 模块中上传文件 worker 的数量
- 默认值：`8`

#### `compression`

- redo log 文件的压缩行为
- 可选值：`""`, `lz4`
- 默认值：`""`（表示不进行压缩）

#### `flush-concurrency`

- redo log 上传单个文件的并发数
- 默认值：`1`（表示禁用并发）

### `integrity`

#### `integrity-check-level`

- 是否开启单行数据的 Checksum 校验功能
- 默认值：`none`
- 可选值：`none`, `correctness`

#### `corruption-handle-level`

- 当单行数据的 Checksum 校验失败时，Changefeed 打印错误行数据相关日志的级别
- 默认值：`warn` 
- 可选值：`warn`, `error`

### `sink.kafka-config`

- 以下参数仅在下游为 Kafka 时生效

#### `sasl-mechanism`

- Kafka SASL 认证机制
- 默认值：``（表示不使用 SASL 认证）
- 可选值：`OAUTHBEARER`

#### `sasl-oauth-client-id`

- Kafka SASL OAUTHBEARER 认证机制中的 client-id
- 默认值：``
- 在使用 OAUTHBEARER 认证机制时，该参数必填

#### `sasl-oauth-client-secret`

- Kafka SASL OAUTHBEARER 认证机制中的 client-secret
- 默认值：``
- 需要 Base64 编码
- 在使用 OAUTHBEARER 认证机制时，该参数必填

#### `sasl-oauth-token-url`

- Kafka SASL OAUTHBEARER 认证机制中的 token-url，用于获取 token
- 默认值：``
- 在使用 OAUTHBEARER 认证机制时，该参数必填

#### `sasl-oauth-scopes`

- Kafka SASL OAUTHBEARER 认证机制中的 scopes
- 默认值：``
- 在使用 OAUTHBEARER 认证机制时，该参数可选填

#### `sasl-oauth-grant-type`

- Kafka SASL OAUTHBEARER 认证机制中的 grant-type
- 默认值：`client_credentials`
- 在使用 OAUTHBEARER 认证机制时，该参数可选填

#### `sasl-oauth-audience`

- Kafka SASL OAUTHBEARER 认证机制中的 audience
- 默认值：``
- 在使用 OAUTHBEARER 认证机制时，该参数可选填

#### `output-raw-change-event`

- 控制是否输出原始的数据变更事件
- 默认值：`false`

### `sink.kafka-config.glue-schema-registry-config`

- 以下配置仅在选用 avro 作为协议，并且使用 AWS Glue Schema Registry 时需要配置

#### `region`

- AWS 区域名称

#### `registry-name`

- Schema Registry 的名称

#### `access-key`

- AWS 访问密钥 ID

#### `secret-access-key`

- AWS 密钥访问密钥

#### `token`

- AWS 会话令牌

### `sink.pulsar-config`

- 以下参数仅在下游为 Pulsar 时生效

#### `authentication-token`

- 使用 token 进行 Pulsar 服务端的认证，此处为 token 的值

#### `token-from-file`

- 指定使用 token 进行 Pulsar 服务端的认证，此处为 token 所在文件的路径

#### `basic-user-name`

- Pulsar 使用 basic 账号密码验证身份

#### `basic-password`

- Pulsar 使用 basic 账号密码验证身份，此处为密码

#### `auth-tls-certificate-path`

- Pulsar TLS 加密认证证书路径

#### `auth-tls-private-key-path`

- Pulsar TLS 加密认证私钥路径

#### `tls-trust-certs-file-path`

- Pulsar TLS 加密可信证书文件路径

#### `oauth2.oauth2-issuer-url`

- Pulsar oauth2 issuer-url

#### `oauth2.oauth2-audience`

- Pulsar oauth2 audience

#### `oauth2.oauth2-private-key`

- Pulsar oauth2 private-key

#### `oauth2.oauth2-client-id`

- Pulsar oauth2 client-id

#### `oauth2.oauth2-scope`

- Pulsar oauth2 oauth2-scope

#### `pulsar-producer-cache-size`

- TiCDC 中缓存 Pulsar Producer 的个数
- 默认值：`10240`

#### `compression-type`

- Pulsar 数据压缩方式
- 默认值：``（表示不压缩）
- 可选值：`lz4`, `zlib`, `zstd`

#### `connection-timeout`

- Pulsar 客户端与服务端建立 TCP 连接的超时时间
- 默认值：`5`（秒）

#### `operation-timeout`

- Pulsar 客户端发起创建、订阅等操作的超时时间
- 默认值：`30`（秒）

#### `batching-max-messages`

- Pulsar Producer 发送消息时的单个 batch 内的消息数量上限
- 默认值：`1000`

#### `batching-max-publish-delay`

- Pulsar Producer 消息攒批的时间间隔
- 默认值：`10`（毫秒）

#### `send-timeout`

- Pulsar Producer 发送消息的超时时间
- 默认值：`30`（秒）

#### `output-raw-change-event`

- 控制是否输出原始的数据变更事件
- 默认值：`false`

### `sink.cloud-storage-config`

#### `worker-count`

- 向下游存储服务保存数据变更记录的并发度
- 默认值：`16`

#### `flush-interval`

- 向下游存储服务保存数据变更记录的间隔
- 默认值：`2s`

#### `file-size`

- 单个数据变更文件的字节数超过 `file-size` 时将其保存至存储服务中
- 默认值：`67108864`（64 MiB）

#### `file-expiration-days`

- 文件保留的时长，仅在 date-separator 配置为 day 时生效
- 默认值：`0`（表示禁用文件清理）
- 示例：假设 `file-expiration-days = 1` 且 `file-cleanup-cron-spec = "0 0 0 * * *"`，TiCDC 将在每天 00:00:00 时刻清理已保存超过 24 小时的文件。例如，2023/12/02 00:00:00 将清理 2023/12/01 之前（注意：不包括 2023/12/01）的文件

#### `file-cleanup-cron-spec`

- 定时清理任务的运行周期，与 crontab 配置兼容
- 格式：`<Second> <Minute> <Hour> <Day of the month> <Month> <Day of the week (Optional)>`
- 默认值：`0 0 2 * * *`（表示每天凌晨两点执行清理任务）

#### `flush-concurrency`

- 上传单个文件的并发数
- 默认值：`1`（表示禁用并发）

#### `output-raw-change-event`

- 控制是否输出原始的数据变更事件
- 默认值：`false`