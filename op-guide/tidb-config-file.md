---
title: TiDB 配置文件解释
category: deployment
---

# TiDB 配置文件

TiDB 配置文件比命令行参数支持更多的选项。你可以在 [config/config.toml.example](https://github.com/pingcap/tidb/blob/master/config/config.toml.example) 找到默认的配置文件，重命名为 config.toml 即可。

本文档只阐述未包含在命令行参数中的参数，命令行参数参见[这里](configuration.md)。

### `split-table`

+ 为每个 table 建立单独的 Region。
+ 默认: true
+ 如果需要创建大量的表，我们建议把这个参数设置为 false。

### `oom-action`

+ 指定 TiDB 发生 out-of-memory 错误时的操作。
+ 默认: "log"
+ 现在合法的选项是 ["log", "cancel"]，如果为 "log"，仅仅是打印日志，不作实质处理。如果为 "cancel"，我们会取消执行这个操作，并且输出日志。

### `enable-streaming`

+ 开启 coprocessor 的 streaming 获取数据模式。
+ 默认: false

### `lower-case-table-names`

+ 这个选项可以设置 TiDB 的系统变量 `lower_case_table_names` 的值。
+ 默认: 2
+ 具体可以查看 MySQL 关于这个变量的[描述](https://dev.mysql.com/doc/refman/5.7/en/server-system-variables.html#sysvar_lower_case_table_names)
+ 注意：目前 TiDB 只支持将该选项的值设为 2，即按照大小写来保存表名，按照小写来比较（不区分大小写）。

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
+ 默认全部保存，如果设置为 7，会最多保留 7 个老的日志文件。

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
+ 默认为 0 表示使用机器上所有的 CPU，也可以设置成 n， 那么 TiDB 会使用 n 个 CPU 数量。

### `stmt-count-limit`

+ TiDB 一个事务允许的最大语句条数限制。
+ 默认: 5000
+ 在一个事务中，超过 `stmt-count-limit` 条语句后还没有 rollback 或者 commit，TiDB 将会返回 `statement count 5001 exceeds the transaction limitation, autocommit = false` 错误。

### `tcp-keep-alive`

+ TiDB 在 TCP 层开启 keepalive 
+ 默认: false

### `retry-limit`

+ TiDB 在提交事务的时候遇到 key 冲突或者其他错误时进行的重试次数。
+ 默认: 10
+ 如果 TiDB 超过 `retry-limit` 次重试还是没有成功，将会返回错误。

### `cross-join`

+ 默认: true
+ 在做 join 的时候，两边表没有任何条件（where 字段），默认可以执行这样的语句。但是设置为 false，则如有这样的 join 语句出现，server 会拒绝执行

### `stats-lease`

+ TiDB 重载统计信息, 更新表行数, 检查是否需要自动 analyze 以及加载列的统计信息的时间间隔
+ 默认: 3s
    - 每隔 `stats-lease` 时间， TiDB 会检查统计信息是否有更新，如果有会将其更新到内存中
    - 每隔 `5 * stats-lease` 时间，TiDB 会将 DML 产生的总行数以及修改的行数变化持久化下来
    - 每隔 `stats-lease` 时间，TiDB 会检查是否有表或者索引需要自动 analyze
    - 每隔 `stats-lease` 时间，TiDB 会检查是否有列的统计信息需要被加载到内存中

### `run-auto-analyze`

+ TiDB 是否做自动的 Analyze。
+ 默认: true

### `feedback-probability`

+ TiDB 对查询收集统计信息反馈的概率
+ 默认: 0
+ 对于每一个查询，TiDB 会以 `feedback-probability` 的概率收集查询的反馈，用于更新统计信息。

## prepared-plan-cache

prepare 语句的 Plan cache 设置。

### `enabled`

+ 开启 prepare 语句的 plan cache。
+ 默认: false

### `capacity`

+ 缓存语句的数量。
+ 默认: 100

## tikv-client

### `grpc-connection-count`

+ 跟每个 TiKV 之间建立的最大连接数。
+ 默认: 16

### `commit-timeout`

+ 执行事务提交时，最大的超时时间。
+ 默认: 41s
+ 这个值必须是大于两倍 Raft 选举的超时时间。

## txn-local-latches

事务内存锁相关配置，当本地事务冲突比较多时建议开启。

### `enable`
+ 开启
+ 默认: false

### `capacity`
+ Hash 对应的 slot 数, 会自动向上调整为 2 的指数倍。每个 slot 占 32 Bytes 内存。当写入数据的范围比较广时（如导数据），设置过小会导致变慢，性能下降。
+ 默认：1024000
