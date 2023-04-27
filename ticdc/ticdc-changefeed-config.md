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
Info: {"upstream_id":7178706266519722477,"namespace":"default","id":"simple-replication-task","sink_uri":"mysql://root:xxxxx@127.0.0.1:4000/?time-zone=","create_time":"2022-12-19T15:05:46.679218+08:00","start_ts":438156275634929669,"engine":"unified","config":{"case_sensitive":true,"enable_old_value":true,"force_replicate":false,"ignore_ineligible_table":false,"check_gc_safe_point":true,"enable_sync_point":true,"bdr_mode":false,"sync_point_interval":30000000000,"sync_point_retention":3600000000000,"filter":{"rules":["test.*"],"event_filters":null},"mounter":{"worker_num":16},"sink":{"protocol":"","schema_registry":"","csv":{"delimiter":",","quote":"\"","null":"\\N","include_commit_ts":false},"column_selectors":null,"transaction_atomicity":"none","encoder_concurrency":16,"terminator":"\r\n","date_separator":"none","enable_partition_separator":false},"consistent":{"level":"none","max_log_size":64,"flush_interval":2000,"storage":""}},"state":"normal","creator_version":"v6.5.0"}
```

- `--changefeed-id`：同步任务的 ID，格式需要符合正则表达式 `^[a-zA-Z0-9]+(\-[a-zA-Z0-9]+)*$`。如果不指定该 ID，TiCDC 会自动生成一个 UUID（version 4 格式）作为 ID。
- `--sink-uri`：同步任务下游的地址，需要按照以下格式进行配置，目前 scheme 支持 `mysql`、`tidb` 和 `kafka`。

    ```
    [scheme]://[userinfo@][host]:[port][/path]?[query_parameters]
    ```

    URI 中包含特殊字符时，如 `! * ' ( ) ; : @ & = + $ , / ? % # [ ]`，需要对 URI 特殊字符进行转义处理。你可以在 [URI Encoder](https://meyerweb.com/eric/tools/dencoder/) 中对 URI 进行转义。

- `--start-ts`：指定 changefeed 的开始 TSO。TiCDC 集群将从这个 TSO 开始拉取数据。默认为当前时间。
- `--target-ts`：指定 changefeed 的目标 TSO。TiCDC 集群拉取数据直到这个 TSO 停止。默认为空，即 TiCDC 不会自动停止。
- `--config`：指定 changefeed 配置文件。

## TiCDC Changefeed 配置文件说明

本章节详细介绍了同步任务的配置。

```toml
# 指定配置文件中涉及的库名、表名是否为大小写敏感
# 该配置会同时影响 filter 和 sink 相关配置，默认为 true
case-sensitive = true

# 是否输出 old value，从 v4.0.5 开始支持，从 v5.0 开始默认为 true
enable-old-value = true

# 是否开启 Syncpoint 功能，从 v6.3.0 开始支持，该功能默认关闭。
# 从 v6.4.0 开始，使用 Syncpoint 功能需要同步任务拥有下游集群的 SYSTEM_VARIABLES_ADMIN 或者 SUPER 权限
# enable-sync-point = false

# Syncpoint 功能对齐上下游 snapshot 的时间间隔
# 配置格式为 h m s，例如 "1h30m30s"
# 默认值为 10m，最小值为 30s
# sync-point-interval = "5m"

# Syncpoint 功能在下游表中保存的数据的时长，超过这个时间的数据会被清理
# 配置格式为 h m s，例如 "24h30m30s"
# 默认值为 24h
# sync-point-retention = "1h"

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
# 事件过滤器的详细配置规则在下方的 Event Filter 配置规则中描述
# 第一个事件过滤器规则
[[filter.event-filters]]
matcher = ["test.worker"] # matcher 是一个白名单，表示该过滤规则只应用于 test 库中的 worker 表
ignore-event = ["insert"] # 过滤掉 insert 事件
ignore-sql = ["^drop", "add column"] # 过滤掉以 "drop" 开头或者包含 "add column" 的 DDL
ignore-delete-value-expr = "name = 'john'" # 过滤掉包含 name = 'john' 条件的 delete DML
ignore-insert-value-expr = "id >= 100" # 过滤掉包含 id >= 100 条件的 insert DML
ignore-update-old-value-expr = "age < 18" # 过滤掉旧值 age < 18 的 update DML
ignore-update-new-value-expr = "gender = 'male'" # 过滤掉新值 gender = 'male' 的 update DML

# 第二个事件过滤器规则
[[filter.event-filters]]
matcher = ["test.fruit"] # 该事件过滤器只应用于 test.fruit 表
ignore-event = ["drop table"] # 忽略 drop table 事件
ignore-sql = ["delete"] # 忽略 delete DML
ignore-insert-value-expr = "price > 1000 and origin = 'no where'" # 忽略包含 price > 1000 和 origin = 'no where' 条件的 insert DML

[scheduler]
# 将表按 Region 个数划分成多个同步范围，这些范围可由多个 TiCDC 节点同步。
# 注意：该功能只在 Kafka changefeed 上生效，暂不支持 MySQL changefeed。
# 默认为 "false"。设置为 "true" 以打开该功能。
enable-table-across-nodes = false
# 打开该功能后，该功能只对 Region 个数大于 `region-threshold` 值的表生效。
region-threshold = 100000

[sink]
# 对于 MQ 类的 Sink，可以通过 dispatchers 配置 event 分发器
# 支持 partition 及 topic（从 v6.1 开始支持）两种 event 分发器。二者的详细说明见下一节。
# matcher 的匹配语法和过滤器规则语法相同，matcher 匹配规则的详细说明见下一节。
dispatchers = [
    {matcher = ['test1.*', 'test2.*'], topic = "Topic 表达式 1", partition = "ts" },
    {matcher = ['test3.*', 'test4.*'], topic = "Topic 表达式 2", partition = "index-value" },
    {matcher = ['test1.*', 'test5.*'], topic = "Topic 表达式 3", partition = "table"},
    {matcher = ['test6.*'], partition = "ts"}
]

# protocol 用于指定传递到下游的协议格式
# 当下游类型是 Kafka 时，支持 canal-json、avro 两种协议。
# 当下游类型是存储服务时，目前仅支持 canal-json、csv 两种协议。
protocol = "canal-json"

# 以下三个配置项仅在同步到存储服务的 sink 中使用，在 MQ 和 MySQL 类 sink 中无需设置。
# 换行符，用来分隔两个数据变更事件。默认值为空，表示使用 "\r\n" 作为换行符。
terminator = ''
# 文件路径的日期分隔类型。可选类型有 `none`、`year`、`month` 和 `day`。默认值为 `none`，即不使用日期分隔。详见 <https://docs.pingcap.com/zh/tidb/v7.0/ticdc-sink-to-cloud-storage#数据变更记录>。
date-separator = 'none'
# 是否使用 partition 作为分隔字符串。默认值为 true，即一张表中各个 partition 的数据会分不同的目录来存储。详见 <https://docs.pingcap.com/zh/tidb/v7.0/ticdc-sink-to-cloud-storage#数据变更记录>。
enable-partition-separator = true

# 从 v6.5.0 开始，TiCDC 支持以 CSV 格式将数据变更记录保存至存储服务中，在 MQ 和 MySQL 类 sink 中无需设置。
[sink.csv]
# 字段之间的分隔符。必须为 ASCII 字符，默认值为 `,`。
delimiter = ','
# 用于包裹字段的引号字符。空值代表不使用引号字符。默认值为 `"`。
quote = '"'
# CSV 中列为 NULL 时将以什么字符来表示。默认值为 `\N`。
null = '\N'
# 是否在 CSV 行中包含 commit-ts。默认值为 false。
include-commit-ts = false
```
