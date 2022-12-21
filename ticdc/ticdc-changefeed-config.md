---
title: TiCDC Changefeed 命令行参数和配置参数
summary: 了解 TiCDC Changefeed 详细的命令行参数和配置文件定义。
---

# TiCDC Changefeed 命令行参数和配置参数

## TiCDC Changefeed 命令行参数

本章节将以创建同步任务为例，介绍 TiCDC Changefeed 的命令行参数：

```shell
cdc cli changefeed create --server=http://10.0.10.25:8300 --sink-uri="mysql://root:123456@127.0.0.1:3306/" --changefeed-id="simple-replication-task" --sort-engine="unified"
```

```shell
Create changefeed successfully!
ID: simple-replication-task
Info: {"sink-uri":"mysql://root:123456@127.0.0.1:3306/","opts":{},"create-time":"2020-03-12T22:04:08.103600025+08:00","start-ts":415241823337054209,"target-ts":0,"admin-job-type":0,"sort-engine":"unified","sort-dir":".","config":{"case-sensitive":true,"filter":{"rules":["*.*"],"ignore-txn-start-ts":null,"ddl-allow-list":null},"mounter":{"worker-num":16},"sink":{"dispatchers":null},"scheduler":{"type":"table-number","polling-time":-1}},"state":"normal","history":null,"error":null}
```

- `--changefeed-id`：同步任务的 ID，格式需要符合正则表达式 `^[a-zA-Z0-9]+(\-[a-zA-Z0-9]+)*$`。如果不指定该 ID，TiCDC 会自动生成一个 UUID（version 4 格式）作为 ID。
- `--sink-uri`：同步任务下游的地址，需要按照以下格式进行配置，目前 scheme 支持 `mysql`、`tidb` 和 `kafka`。

    ```
    [scheme]://[userinfo@][host]:[port][/path]?[query_parameters]
    ```

    URI 中包含特殊字符时，如 `! * ' ( ) ; : @ & = + $ , / ? % # [ ]`，需要对 URI 特殊字符进行转义处理。你可以在 [URI Encoder](https://meyerweb.com/eric/tools/dencoder/) 中对 URI 进行转义。

- `--start-ts`：指定 changefeed 的开始 TSO。TiCDC 集群将从这个 TSO 开始拉取数据。默认为当前时间。
- `--target-ts`：指定 changefeed 的目标 TSO。TiCDC 集群拉取数据直到这个 TSO 停止。默认为空，即 TiCDC 不会自动停止。
- `--sort-engine`：指定 changefeed 使用的排序引擎。因 TiDB 和 TiKV 使用分布式架构，TiCDC 需要对数据变更记录进行排序后才能输出。该项支持 `unified`（默认）/`memory`/`file`：

    - `unified`：优先使用内存排序，内存不足时则自动使用硬盘暂存数据。该选项默认开启。
    - `memory`：在内存中进行排序。 **已经弃用，不建议在任何情况使用。**
    - `file`：完全使用磁盘暂存数据。**已经弃用，不建议在任何情况使用。**

- `--config`：指定 changefeed 配置文件。
- `--sort-dir`：用于指定排序器使用的临时文件目录。**自 TiDB v4.0.13, v5.0.3 和 v5.1.0 起已经无效，请不要使用**。

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

# 对于 MQ 类的 Sink，可以指定消息的协议格式
# 目前支持 canal-json、open-protocol、canal、avro 和 maxwell 五种协议。
protocol = "canal-json"
```
