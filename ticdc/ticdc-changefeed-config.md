---
title: TiCDC 配置文件参数
summary: TODO
---

# Title

TODO



## 同步任务配置文件描述

本部分详细介绍了同步任务的配置。

```toml
# 指定配置文件中涉及的库名、表名是否为大小写敏感
# 该配置会同时影响 filter 和 sink 相关配置，默认为 true
case-sensitive = true

# 是否输出 old value，从 v4.0.5 开始支持，从 v5.0 开始默认为 true
enable-old-value = true

# 是否开启 Syncpoint 功能，从 v6.3.0 开始支持
enable-sync-point = true

# Syncpoint 功能对齐上下游 snapshot 的时间间隔
# 配置格式为 h m s，例如 "1h30m30s"
# 默认值为 10m，最小值为 30s
sync-point-interval = "5m"

# Syncpoint 功能在下游表中保存的数据的时长，超过这个时间的数据会被清理
# 配置格式为 h m s，例如 "24h30m30s"
# 默认值为 24h
sync-point-retention = "1h"

[filter]
# 忽略指定 start_ts 的事务
ignore-txn-start-ts = [1, 2]

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
