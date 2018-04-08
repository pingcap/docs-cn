---
title: TiDB 配置文件解释
category: deployment
---

# TiDB 配置文件

TiDB 配置文件比命令行参数支持更多的选项。大家可以在 [config/config.toml.example](https://github.com/pingcap/tidb/blob/master/config/config.toml.example) 找到默认的配置文件。大家重命名为 `config.toml` 即可。

这里只阐述在命令行参数中没有的参数，命令行参数大家可以看[这里](configuration.md)

### `split-table`

+ 为每个 table 建立单独的 region。
+ 默认: true
+ 如果需要创建大量的表，我们建议把这个参数设置为 false。

### `oom-action`

+ 指定 TiDB 发生 out-of-memory 错误时的操作。
+ 默认: "log"
+ 现在合法的选项是 ["log", "cancel"]，如果为 "log", 仅仅是打印日志，不作实质处理。如果为 "cancel"，我们会取消执行这个操作，并且输出日志。

### `enable-streaming`

+ 开启 coprocessor 的 streaming 获取数据模式。
+ 默认: false

### `lower-case-table-names`

+ 这个选项可以设置 TiDB 的系统变量 `lower_case_table_names` 的值。
+ 默认: 2
+ 具体可以查看 MySQL 关于这个变量的[描述](https://dev.mysql.com/doc/refman/5.7/en/server-system-variables.html#sysvar_lower_case_table_names)

## log 

日志相关的配置项。

### `format`

+ 指定日志输出的格式，可选项为 [json, text, console]。
+ 默认: "text"

### `disable-timestamp`

+ 是否禁止在日志中输出时间戳。
+ 默认: false
+ 如果设置为 true，那么日志里面将不会输出时间戳。

### `slow-threshold`

+ 输出慢日志的耗时阈值。
+ 默认: 300ms
+ 当查询大于这个值，就会当做是一个慢查询，输出到慢查询日志。

### `expensive-threshold`

+ 输出 `expensive` 操作的行数阈值。
+ 默认: 10000
+ 当查询的行数(包括中间结果，基于统计信息)大于这个值，我们就会当成是一个 `expensive` 的操作，输出一个前缀带有 `[EXPENSIVE_QUERY]` 的日志。

### `query-log-max-len`

+ 最长的 SQL 输出长度。
+ 默认: 2048
+ 当语句的长度大于 `query-log-max-len`，将会被截断输出。

### log.file

#### `filename`

+ 一般日志文件名字。
+ 默认: ""
+ 如果设置，会输出一般日志到这个文件。

#### `max-size`

+ 日志文件的大小限制。
+ 默认: 300MB
+ 最大设置上限为 4GB。

#### `max-days`

+ 日志最大保留的天数。
+ 默认: 0
+ 默认是不清理的，如果设置了，在 `max-days` 之后 TiDB 会清理过期的日志文件。

#### `max-backups`

+ 保留的日志的最大数量。
+ 默认: 0
+ 默认全部保存，如果设置为7，会最多保留 7 个老的日志文件。

#### `log-rotate`

+ 是否每日创建一个新的日志文件。
+ 默认: true
+ 如果设置为 true，每天会新建新的日志文件，如果设置为 false，那么只会输出到一个日志文件。

## security

安全相关配置。

### `ssl-ca`

+ PEM 格式的受信任 CA 的证书文件路径
+ 默认: ""
+ 当同时设置了该选项和 `--ssl-cert`、`--ssl-key` 选项时，TiDB 将在客户端出示证书的情况下根据该选项指定的受信任的 CA 列表验证客户端证书。若验证失败，则连接会被终止。
+ 即使设置了该选项，若客户端没有出示证书，则安全连接仍然继续，不会进行客户端证书验证。

### `ssl-cert`

+ PEM 格式的 SSL 证书文件路径
+ 默认: ""
+ 当同时设置了该选项和 `--ssl-key` 选项时，TiDB 将接受（但不强制）客户端使用 TLS 安全地连接到 TiDB。
+ 若指定的证书或私钥无效，则 TiDB 会照常启动，但无法接受安全连接。

### `ssl-key`

+ PEM 格式的 SSL 证书密钥文件路径，即 `--ssl-cert` 所指定的证书的私钥
+ 默认: ""
+ 目前 TiDB 不支持加载由密码保护的私钥。

## performance

性能相关配置。

### `max-procs`

+ TiDB 的 CPU 使用数量。
+ 默认: 0
+ 默认为 0 表示使用机器上所有的 CPU，也可以设置成 `max-procs`， 那么 TiDB 会使用 `max-procs` 个 CPU 数量。

### `stmt-count-limit`

+ TiDB 一个事务允许的最大语句条数限制。
+ 默认: 5000
+ 在一个事务中，超过 `stmt-count-limit` 条语句后还没有 roolback 或者 commit，TiDB 将会返回 `statement count 5001 exceeds the transaction limitation, autocommit = false` 错误。

### `tcp-keep-alive`

+ TiDB 在 tcp 层开启 keepalive 
+ 默认: false

### `retry-limit`

+ TiDB 在提交事务的时候遇到 key 冲突或者其他错误时进行的重试次数。
+ 默认: 10
+ 如果 TiDB 超过 `retry-limit` 次重试还是没有成功，将会返回错误。

### `join-concurrency`

+ join-concurrency 并发执行 join 的 goroutine 数量
+ 默认: 5
+ 看数据量和数据分布情况，一般情况下是越多越好，数值越大对 CPU 开销越大

### `cross-join`

+ 默认: true
+ 在做 join 的时候，两边表没有任何条件（where 字段），默认可以执行这样的语句。但是设置为 false，则如有这样的 join 语句出现，server 会拒绝执行

### `stats-lease`

+ TiDB 统计信息做 Analyze 和 重载统计信息的时间间隔。
+ 默认: xxx
+ xxxx

### `run-auto-analyze`

TiDB 是否做自动的 Analyze。
+ 默认: true

### `feedback-probability`

+ xxx
+ 默认: xxx

## plan-cache

Plan cache 相关配置。

### `enabled`

+ 开启 Plan cache。
+ 默认: false
+ 开启 Plan cache 会省去相同 SQL 语句的查询优化开销。

### `capacity`

+ 缓存语句的数量。
+ 默认: 2560

### `shards`

+ plan-cache 桶的数量。
+ 默认: 256
+ 这个数量越大，锁的粒度越小。

### prepared-plan-cache

prepare 语句的 Plan cache 设置。

### `enabled`

+ 开启 prepare 语句的 plan cache。
+ 默认: false

### `capacity`

+ 缓存语句的数量。
+ 默认: 100

## tikv-client

### `grpc-connection-count`

+ 跟每个 tikv 之间建立的最大连接数。
+ 默认: 16

### `commit-timeout`

+ 执行事务提交时，最大的超时时间。
+ 默认: 41s
+ 这个值必须是大于两倍 raft 选举的超时时间。