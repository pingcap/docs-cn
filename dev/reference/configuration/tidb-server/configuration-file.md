---
title: TiDB 配置文件描述
category: reference
---

# TiDB 配置文件描述

TiDB 配置文件比命令行参数支持更多的选项。你可以在 [config/config.toml.example](https://github.com/pingcap/tidb/blob/master/config/config.toml.example) 找到默认值的配置文件，重命名为 config.toml 即可。

本文档只阐述未包含在命令行参数中的参数，命令行参数参见[这里](/reference/configuration/tidb-server/configuration.md)。

### `split-table`

+ 为每个 table 建立单独的 Region。
+ 默认值：true
+ 如果需要创建大量的表，我们建议把这个参数设置为 false。

### `oom-action`

+ 指定 TiDB 发生 out-of-memory 错误时的操作。
+ 默认值："log"
+ 现在合法的选项是 ["log", "cancel"]，如果为 "log"，仅仅是打印日志，不作实质处理。如果为 "cancel"，我们会取消执行这个操作，并且输出日志。

### `mem-quota-query`
+ 单条 SQL 语句可以占用的最大内存阈值。
+ 默认值：34359738368
+ 超过该值的请求会被 `oom-action` 定义的行为所处理。

### `enable-streaming`

+ 开启 coprocessor 的 streaming 获取数据模式。
+ 默认值：false

### `lower-case-table-names`

+ 这个选项可以设置 TiDB 的系统变量 `lower_case_table_names` 的值。
+ 默认值：2
+ 具体可以查看 MySQL 关于这个变量的[描述](https://dev.mysql.com/doc/refman/5.7/en/server-system-variables.html#sysvar_lower_case_table_names)

> **注意：**
>
> 目前 TiDB 只支持将该选项的值设为 2，即按照大小写来保存表名，按照小写来比较（不区分大小写）。

### `lease`

+ DDL 租约超时时间。
+ 默认值：45s
+ 单位：秒

### `compatible-kill-query`

+ 设置 `KILL` 语句的兼容性。
+ 默认值：false
+ TiDB 中 `KILL xxx` 的行为和 MySQL 中的行为不相同。为杀死一条查询，在 TiDB 里需要加上 `TIDB` 关键词，即 `KILL TIDB xxx`。但如果把 `compatible-kill-query` 设置为 true，则不需要加上 `TIDB` 关键词。
+ 这种区别很重要，因为当用户按下 <kbd>Ctrl</kbd>+<kbd>C</kbd> 时，MySQL 命令行客户端的默认值行为是：创建与后台的新连接，并在该新连接中执行 `KILL` 语句。如果负载均衡器或代理已将该新连接发送到与原始会话不同的 TiDB 服务器实例，则该错误会话可能被终止，从而导致使用 TiDB 集群的业务中断。只有当您确定在 `KILL` 语句中引用的连接正好位于 `KILL` 语句发送到的服务器上时，才可以启用 `compatible-kill-query`。

### `check-mb4-value-in-utf8`

+ 开启检查 utf8mb4 字符的开关，如果开启此功能，字符集是 utf8，且在 utf8 插入 mb4 字符，系统将会报错。
+ 默认值：true

### `treat-old-version-utf8-as-utf8mb4`

+ 将旧表中的 utf8 字符集当成 utf8mb4的开关。
+ 默认值：true

## log 

日志相关的配置项。

### `format`

+ 指定日志输出的格式，可选项为 [json, text, console]。
+ 默认值："text"

### `disable-timestamp`

+ 是否禁止在日志中输出时间戳。
+ 默认值：false
+ 如果设置为 true，那么日志里面将不会输出时间戳。

### `slow-query-file`

+ 慢查询日志的文件名。
+ 默认值："tidb-slow.log"，注：由于 TiDB V2.1.8 更新了慢日志格式，所以将慢日志单独输出到了慢日志文件。V2.1.8 之前的版本，该变量的默认值值是 ""。
+ 设置后，慢查询日志会单独输出到该文件。

### `slow-threshold`

+ 输出慢日志的耗时阈值。
+ 默认值：300ms
+ 当查询大于这个值，就会当做是一个慢查询，输出到慢查询日志。

### `expensive-threshold`

+ 输出 `expensive` 操作的行数阈值。
+ 默认值：10000
+ 当查询的行数（包括中间结果，基于统计信息）大于这个值，我们就会当成是一个 `expensive` 的操作，输出一个前缀带有 `[EXPENSIVE_QUERY]` 的日志。

### `query-log-max-len`

+ 最长的 SQL 输出长度。
+ 默认值：2048
+ 当语句的长度大于 `query-log-max-len`，将会被截断输出。

## log.file

日志文件相关的配置项。

#### `filename`

+ 一般日志文件名字。
+ 默认值：""
+ 如果设置，会输出一般日志到这个文件。

#### `max-size`

+ 日志文件的大小限制。
+ 默认值：300MB
+ 最大设置上限为 4GB。

#### `max-days`

+ 日志最大保留的天数。
+ 默认值：0
+ 默认值是不清理的，如果设置了，在 `max-days` 之后 TiDB 会清理过期的日志文件。

#### `max-backups`

+ 保留的日志的最大数量。
+ 默认值：0
+ 默认值全部保存，如果设置为 7，会最多保留 7 个老的日志文件。

#### `log-rotate`

+ 是否每日创建一个新的日志文件。
+ 默认值：true
+ 如果设置为 true，每天会新建新的日志文件，如果设置为 false，那么只会输出到一个日志文件。

## security

安全相关配置。

### `ssl-ca`

+ PEM 格式的受信任 CA 的证书文件路径。
+ 默认值：""
+ 当同时设置了该选项和 `--ssl-cert`、`--ssl-key` 选项时，TiDB 将在客户端出示证书的情况下根据该选项指定的受信任的 CA 列表验证客户端证书。若验证失败，则连接会被终止。
+ 即使设置了该选项，若客户端没有出示证书，则安全连接仍然继续，不会进行客户端证书验证。

### `ssl-cert`

+ PEM 格式的 SSL 证书文件路径。
+ 默认值：""
+ 当同时设置了该选项和 `--ssl-key` 选项时，TiDB 将接受（但不强制）客户端使用 TLS 安全地连接到 TiDB。
+ 若指定的证书或私钥无效，则 TiDB 会照常启动，但无法接受安全连接。

### `ssl-key`

+ PEM 格式的 SSL 证书密钥文件路径，即 `--ssl-cert` 所指定的证书的私钥。
+ 默认值：""
+ 目前 TiDB 不支持加载由密码保护的私钥。

### `cluster-ssl-ca`

+ CA 根证书，用于用 tls 连接 TiKV/PD
+ 默认值：""

### `cluster-ssl-cert`

+ ssl 证书文件路径，用于用 tls 连接 TiKV/PD
+ 默认值：""

### `cluster-ssl-key`

+ ssl 私钥文件路径，用于用 tls 连接 TiKV/PD
+ 默认值：""

### `skip-grant-table`

+ 是否跳过权限检查
+ 默认值：false

## performance

性能相关配置。

### `max-procs`

+ TiDB 的 CPU 使用数量。
+ 默认值：0
+ 默认值为 0 表示使用机器上所有的 CPU，也可以设置成 n，那么 TiDB 会使用 n 个 CPU 数量。

### `max-memory`

+ Prepare cache LRU 使用的最大内存限制，超过 performance.max-memory * (1 - prepared-plan-cache.memory-guard-ratio)会 剔除 LRU 中的元素。 
+ 默认值：0
+ 这个配置只有在 prepared-plan-cache.enabled 为 true 的情况才会生效。在 LRU 的 size 大于 prepared-plan-cache.capacity 的情况下，也会剔除 LRU 中的元素。

### `stmt-count-limit`

+ TiDB 一个事务允许的最大语句条数限制。
+ 默认值：5000
+ 在一个事务中，超过 `stmt-count-limit` 条语句后还没有 rollback 或者 commit，TiDB 将会返回 `statement count 5001 exceeds the transaction limitation, autocommit = false` 错误。

### `tcp-keep-alive`

+ TiDB 在 TCP 层开启 keepalive。
+ 默认值：false

### `retry-limit`

+ TiDB 在提交事务的时候遇到 key 冲突或者其他错误时进行的重试次数。
+ 默认值：10
+ 如果 TiDB 超过 `retry-limit` 次重试还是没有成功，将会返回错误。

### `cross-join`

+ 默认值：true
+ 在做 join 的时候，两边表没有任何条件（where 字段），默认值可以执行这样的语句。但是设置为 false，则如有这样的 join 语句出现，server 会拒绝执行

### `stats-lease`

+ TiDB 重载统计信息，更新表行数，检查是否需要自动 analyze 以及加载列的统计信息的时间间隔。
+ 默认值：3s
    - 每隔 `stats-lease` 时间，TiDB 会检查统计信息是否有更新，如果有会将其更新到内存中
    - 每隔 `5 * stats-lease` 时间，TiDB 会将 DML 产生的总行数以及修改的行数变化持久化下来
    - 每隔 `stats-lease` 时间，TiDB 会检查是否有表或者索引需要自动 analyze
    - 每隔 `stats-lease` 时间，TiDB 会检查是否有列的统计信息需要被加载到内存中

### `run-auto-analyze`

+ TiDB 是否做自动的 Analyze。
+ 默认值：true

### `feedback-probability`

+ TiDB 对查询收集统计信息反馈的概率。
+ 默认值：0.0
+ 对于每一个查询，TiDB 会以 `feedback-probability` 的概率收集查询的反馈，用于更新统计信息。

### `query-feedback-limit`

+ 在内存中缓存的最大 Query Feedback 数量，超过这个数量的 Feedback 会被丢弃。
+ 默认值：1024

### `pseudo-estimate-ratio`

+ 修改过的行数/表的总行数的比值，超过该值时系统会认为统计信息已经过期，会采用 pseudo 的统计信息。
+ 默认值：0.8
+ 最小值为 0；最大值为 1。

### `force-priority`

+ 把所有的语句优先级设置为 force-priority 的值。
+ 默认值：NO_PRIORITY
+ 可选值：NO_PRIORITY, LOW_PRIORITY, HIGH_PRIORITY, DELAYED。

## prepared-plan-cache

prepare 语句的 Plan cache 设置。

### `enabled`

+ 开启 prepare 语句的 plan cache。
+ 默认值：false

### `capacity`

+ 缓存语句的数量。
+ 默认值：100

### `memory-guard-ratio`

+ 用于防止超过 performance.max-memory, 超过 max-proc * (1 - prepared-plan-cache.memory-guard-ratio)会剔除 LRU 中的元素。
+ 默认值：0.1
+ 最小值为 0；最大值为 1。

## tikv-client

TiKV Client 相关配置。

### `grpc-connection-count`

+ 跟每个 TiKV 之间建立的最大连接数。
+ 默认值：16

### `grpc-keepalive-time`

+ TiDB 与 TiKV 节点之间 rpc 连接 keepalive 时间间隔，如果超过该值没有网络包，grpc client 会 ping 一下 TiKV 查看是否存活。
+ 默认值：10
+ 单位：秒

### `grpc-keepalive-timeout`

+ TiDB 与 TiKV 节点  rpc keepalive 检查的超时时间
+ 默认值：3
+ 单位：秒

### `commit-timeout`

+ 执行事务提交时，最大的超时时间。
+ 默认值：41s
+ 这个值必须是大于两倍 Raft 选举的超时时间。

### `max-txn-time-use`

+ 单个事务允许的最大执行时间。
+ 默认值：590
+ 单位：秒

### `max-batch-size`

+ 批量发送 rpc 封包的最大数量，如果不为 0，将使用 BatchCommands api 发送请求到 TiKV，可以在并发度高的情况降低 rpc 的延迟，推荐不修改该值。
+ 默认值：128

### `max-batch-wait-time`

+ 等待 `max-batch-wait-time` 纳秒批量将此期间的数据包封装成一个大包发送给 TiKV 节点，仅在 `tikv-client.max-batch-size`  值大于 0 时有效，不推荐修改该值。
+ 默认值：0
+ 单位：纳秒

### `batch-wait-size`

+ 批量向 TiKV 发送的封包最大数量，不推荐修改该值。
+ 默认值：8
+ 若此值为 0 表示关闭此功能。

### `overload-threshold`

+ TiKV 的负载阈值，如果超过此阈值，会收集更多的 batch 封包，来减轻 TiKV 的压力。仅在 `tikv-client.max-batch-size` 值大于 0 时有效，不推荐修改该值。
+ 默认值：200

## txn-local-latches

事务内存锁相关配置，当本地事务冲突比较多时建议开启。

### `enable`

+ 开启或关闭事务内存锁
+ 默认值：false

### `capacity`

+ Hash 对应的 slot 数，会自动向上调整为 2 的指数倍。每个 slot 占 32 Bytes 内存。当写入数据的范围比较广时（如导数据），设置过小会导致变慢，性能下降。
+ 默认：1024000

### `max-batch-size`

+ 设置在双工流 RPC（Duplex stream RPC）模式下，一个 batch 命令请求中最多可以包含的业务请求数量。设置为 0 可以完全禁用掉双工流 ，回退至 2.1 或更老版本兼容的 Unary RPC 请求方式。
+ 默认值：128

### `max-batch-wait-time`

+ 设置当 TiKV 出现 gRPC 层负载过高的时候，TiDB 需要等待的纳秒数（ns）。该参数为非负整数，控制 TiDB 合并小请求为批请求的最长等待时间。在此时间范围内，TiDB 会采用尽力而为的策略合并请求。
+ 默认值：0

### `batch-wait-size` 

+ 在等待过程中 batch 命令的大小上限。当 batch 超过此大小，等待结束，合并完成。这样可以降低等待策略引入的不必要的延迟。
+ 默认值：8

### `overload-threshold`

+ 设置 gRPC 的 CPU 使用率上限。超过此上限后之后，TiDB 就认为 TiKV 的网络传输层处于过载状态，从而开启等待策略。
+ 默认值：200，即 200%
+ 默认值：1024000

## binlog

TiDB Binlog 相关配置。

### `enable`

+ binlog 开关。
+ 默认值：false

### `write-timeout`

+ 写 binlog 的超时时间，推荐不修改该值。
+ 默认值：15s
+ 单位：秒

### `ignore-error`

+ 忽略写 binlog 发生的错误时处理开关，推荐不修改该值。
+ 默认值：false
+ "true"，发生错误时，停止写入 binlog, 并且在监控项 tidb_server_critical_error_total 上计数加1；"false": 写入 binlog 失败，会停止整个 TiDB 的服务。

### `binlog-socket`

+ binlog 输出网络地址。
+ 默认值：""

### `strategy`

+ binlog 输出时选择 pump 的策略，仅支持 hash ，range 方法。
+ 默认值："range"

## status

TiDB 服务状态相关配置。

### `record-db-qps`

+ 输与 database 相关的 QPS metrics 到 promethus的开关。
+ 默认值：false
