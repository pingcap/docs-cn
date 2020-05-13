---
title: TiDB 配置文件描述
category: reference
---

<!-- markdownlint-disable MD001 -->

# TiDB 配置文件描述

TiDB 配置文件比命令行参数支持更多的选项。你可以在 [config/config.toml.example](https://github.com/pingcap/tidb/blob/master/config/config.toml.example) 找到默认值的配置文件，重命名为 `config.toml` 即可。本文档只介绍未包含在[命令行参数](https://pingcap.com/docs-cn/dev/reference/configuration/tidb-server/configuration)中的参数。

### `split-table`

+ 为每个 table 建立单独的 Region。
+ 默认值：true
+ 如果需要创建大量的表，我们建议把这个参数设置为 false。

### `mem-quota-query`

+ 单条 SQL 语句可以占用的最大内存阈值。
+ 默认值：1073741824
+ 超过该值的请求会被 `oom-action` 定义的行为所处理。
+ 该值作为系统变量 [`tidb_mem_quota_query`](/reference/configuration/tidb-server/tidb-specific-variables.md#tidb_mem_quota_query) 的初始值。

### `oom-use-tmp-storage`

+ 设置是否在单条 SQL 语句的内存使用超出 `mem-quota-query` 限制时为某些算子启用临时磁盘。
+ 默认值：true

### `tmp-storage-path`

+ 单条 SQL 语句的内存使用超出 `mem-quota-query` 限制时，某些算子的临时磁盘存储位置。
+ 默认值：`<操作系统临时文件夹>/tidb/tmp-storage`
+ 此配置仅在 `oom-use-tmp-storage` 为 true 时有效。

### `tmp-storage-quota`

+ `tmp-storage-path` 存储使用的限额，单位为字节。
+ 当单条 SQL 语句使用临时磁盘，导致 TiDB server 的总体临时磁盘总量超过 `tmp-storage-quota` 时，当前 SQL 操作会被取消，并返回 `Out Of Global Storage Quota!` 错误。
+ 当 `tmp-storage-quota` 小于 0 时则没有上述检查与限制。
+ 默认值: -1
+ 当 `tmp-storage-path` 的剩余可用容量低于 `tmp-storage-quota` 所定义的值时，TiDB server 启动时将会报出错误并退出。

### `oom-action`

+ 当 TiDB 中单条 SQL 的内存使用超出 `mem-quota-query` 限制且不能再利用临时磁盘时的行为。
+ 默认值："cancel"
+ 目前合法的选项为 ["log", "cancel"]。设置为 "log" 时，仅输出日志。设置为 "cancel" 时，取消执行该 SQL 操作，并输出日志。

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
+ 这种区别很重要，因为当用户按下 <kbd>Ctrl</kbd>+<kbd>C</kbd> 时，MySQL 命令行客户端的默认行为是：创建与后台的新连接，并在该新连接中执行 `KILL` 语句。如果负载均衡器或代理已将该新连接发送到与原始会话不同的 TiDB 服务器实例，则该错误会话可能被终止，从而导致使用 TiDB 集群的业务中断。只有当您确定在 `KILL` 语句中引用的连接正好位于 `KILL` 语句发送到的服务器上时，才可以启用 `compatible-kill-query`。

### `check-mb4-value-in-utf8`

+ 开启检查 utf8mb4 字符的开关，如果开启此功能，字符集是 utf8，且在 utf8 插入 mb4 字符，系统将会报错。
+ 默认值：true

### `treat-old-version-utf8-as-utf8mb4`

+ 将旧表中的 utf8 字符集当成 utf8mb4的开关。
+ 默认值：true

### `alter-primary-key`

+ 用于控制添加或者删除主键功能。
+ 默认值：false
+ 默认情况下，不支持增删主键。将此变量被设置为 true 后，支持增删主键功能。不过对在此开关开启前已经存在的表，且主键是整型类型时，即使之后开启此开关也不支持对此列表删除主键。

### `server-version`

+ 用来修改 TiDB 在以下情况下返回的版本号:
    - 当使用内置函数 `VERSION()` 时。
    - 当与客户端初始连接，TiDB 返回带有服务端版本号的初始握手包时。具体可以查看 MySQL 初始握手包的[描述](https://dev.mysql.com/doc/internals/en/connection-phase-packets.html#packet-Protocol::Handshake)。
+ 默认值：""
+ 默认情况下，TiDB 版本号格式为：`5.7.${mysql_latest_minor_version}-TiDB-${tidb_version}`。

### `repair-mode`

+ 用于开启非可信修复模式，启动该模式后，可以过滤 `repair-table-list` 名单中坏表的加载。
+ 默认值：false
+ 默认情况下，不支持修复语法，默认启动时会加载所有表信息。

### `repair-table-list`

+ 配合 `repair-mode` 为 true 时使用，用于列出实例中需要修复的坏表的名单，该名单的写法为 ["db.table1","db.table2"...]。
+ 默认值：[]
+ 默认情况下，该 list 名单为空，表示没有所需修复的坏表信息。

### `new_collations_enabled_on_first_bootstrap`

+ 用于开启新的 collation 支持
+ 默认值：false
+ 注意：该配置项只有在初次初始化集群时生效，初始化集群后，无法通过更改该配置项打开或关闭新的 collation 框架；4.0 版本之前的 TiDB 集群升级到 4.0 时，由于集群已经初始化过，该参数无论如何配置，都作为 false 处理。

### `max-server-connections`

+ TiDB 中同时允许的最大客户端连接数，用于资源控制。
+ 默认值：0
+ 默认情况下，TiDB 不限制客户端连接数。当本配置项的值大于 `0` 且客户端连接数到达此值时，TiDB 服务端将会拒绝新的客户端连接。

### `max-index-length`

+ 用于设置新建索引的长度限制。
+ 默认值：3072
+ 单位：byte。
+ 目前的合法值范围 `[3072, 3072*4]`。MySQL 和 TiDB v3.0.11 之前版本（不包含 v3.0.11）没有此配置项，不过都对新建索引的长度做了限制。MySQL 对此的长度限制为 `3072`，TiDB 在 v3.0.7 以及之前版本该值为 `3072*4`，在 v3.0.7 之后版本（包含 v3.0.8、v3.0.9 和 v3.0.10）的该值为 `3072`。为了与 MySQL 和 TiDB 之前版本的兼容，添加了此配置项。

## log

日志相关的配置项。

### `format`

+ 指定日志输出的格式，可选项为 [json, text, console]。
+ 默认值："text"

### `enable-timestamp`

+ 是否在日志中输出时间戳。
+ 默认值：true
+ 如果设置为 false，那么日志里面将不会输出时间戳。

> **注意：**
>
> 考虑后向兼容性，原来的配置项 `disable-timestamp` 仍然有效，但如果和 `enable-timestamp` 配置的值在语义上冲突（例如在配置中把 `enable-timestamp` 和 `disable-timestamp` 同时设置为 `true`），则 TiDB 会忽略 `disable-timestamp` 的值。在未来的版本中，`disable-timestamp` 配置项将被彻底移除，请废弃 `disable-timestamp` 的用法，使用语义上更易于理解的 `enable-timestamp`。

### `enable-slow-log`

+ 是否开启慢查询日志
+ 默认值：true
+ 可以设置成 `true` 或 `false` 来启用或或禁用慢查询日志。

### `slow-query-file`

+ 慢查询日志的文件名。
+ 默认值："tidb-slow.log"，注：由于 TiDB V2.1.8 更新了慢日志格式，所以将慢日志单独输出到了慢日志文件。V2.1.8 之前的版本，该变量的默认值是 ""。
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
+ 默认值：4096
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
+ 默认不清理；如果设置了参数值，在 `max-days` 之后 TiDB 会清理过期的日志文件。

#### `max-backups`

+ 保留的日志的最大数量。
+ 默认值：0
+ 默认全部保存；如果设置为 7，会最多保留 7 个老的日志文件。

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
+ 默认值为 0 表示使用机器上所有的 CPU；如果设置成 n，那么 TiDB 会使用 n 个 CPU 数量。

### `max-memory`

+ Prepare cache LRU 使用的最大内存限制，超过 performance.max-memory * (1 - prepared-plan-cache.memory-guard-ratio) 会剔除 LRU 中的元素。
+ 默认值：0
+ 这个配置只有在 prepared-plan-cache.enabled 为 true 的情况才会生效。在 LRU 的 size 大于 prepared-plan-cache.capacity 的情况下，也会剔除 LRU 中的元素。

### `txn-total-size-limit`

+ TiDB 事务大小限制
+ 默认值：104857600 (Byte)
+ 单个事务中，所有 key-value 记录的总大小不能超过该限制。该配置项的最大值不超过 `10737418240`（表示 10GB）。注意，如果使用了以 `Kafka` 为下游消费者的 `binlog`，如：`arbiter` 集群，该配置项的值不能超过 `1073741824`（表示 1GB），因为这是 `Kafka` 的处理单条消息的最大限制，超过该限制 `Kafka` 将会报错。

### `stmt-count-limit`

+ TiDB 一个事务允许的最大语句条数限制。
+ 默认值：5000
+ 在一个事务中，超过 `stmt-count-limit` 条语句后还没有 rollback 或者 commit，TiDB 将会返回 `statement count 5001 exceeds the transaction limitation, autocommit = false` 错误。该限制只在可重试的乐观事务中生效，如果使用悲观事务或者关闭了[事务重试](/reference/transactions/transaction-optimistic.md#事务的重试)，事务中的语句数将不受此限制。

### `tcp-keep-alive`

+ TiDB 在 TCP 层开启 keepalive。
+ 默认值：false

### `cross-join`

+ 默认值：true
+ 默认可以执行在做 join 时两边表没有任何条件（where 字段）的语句；如果设置为 false，则有这样的 join 语句出现时，server 会拒绝执行

### `stats-lease`

+ TiDB 重载统计信息，更新表行数，检查是否需要自动 analyze，利用 feedback 更新统计信息以及加载列的统计信息的时间间隔。
+ 默认值：3s
    - 每隔 `stats-lease` 时间，TiDB 会检查统计信息是否有更新，如果有会将其更新到内存中
    - 每隔 `20 * stats-lease` 时间，TiDB 会将 DML 产生的总行数以及修改的行数变化更新到系统表中
    - 每隔 `stats-lease` 时间，TiDB 会检查是否有表或者索引需要自动 analyze
    - 每隔 `stats-lease` 时间，TiDB 会检查是否有列的统计信息需要被加载到内存中
    - 每隔 `200 * stats-lease` 时间，TiDB 会将内存中缓存的 feedback 写入系统表中
    - 每隔 `5 * stats-lease` 时间，TiDB 会读取系统表中的 feedback，更新内存中缓存的统计信息
+ 当 `stats-lease` 为 0 时，TiDB 会以 3s 的时间间隔周期性的读取系统表中的统计信息并更新内存中缓存的统计信息。但不会自动修改统计信息相关系统表，具体来说，TiDB 不再自动修改这些表：
    - `mysql.stats_meta`：TiDB 不再自动记录事务中对某张表的修改行数，也不会更新到这个系统表中
    - `mysql.stats_histograms`/`mysql.stats_buckets` 和 `mysql.stats_top_n`：TiDB 不再自动 analyze 和主动更新统计信息
    - `mysql.stats_feedback`：TiDB 不再根据被查询的数据反馈的部分统计信息更新表和索引的统计信息

### `run-auto-analyze`

+ TiDB 是否做自动的 Analyze。
+ 默认值：true

### `feedback-probability`

+ TiDB 对查询收集统计信息反馈的概率。
+ 默认值：0.05
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

### `distinct-agg-push-down`

+ 设置优化器是否执行将带有 `Distinct` 的聚合函数（比如 `select count(distinct a) from t`）下推到 Coprocessor 的优化操作。
+ 默认值：false
+ 该变量作为系统变量 [`tidb_opt_distinct_agg_push_down`](/reference/configuration/tidb-server/tidb-specific-variables.md#tidb_opt_distinct_agg_push_down) 的初始值。

## prepared-plan-cache

prepare 语句的 Plan cache 设置。

### `enabled`

+ 开启 prepare 语句的 plan cache。
+ 默认值：false

### `capacity`

+ 缓存语句的数量。
+ 默认值：100
+ 类型为 uint，小于 0 的值会被转化为大整数。

### `memory-guard-ratio`

+ 用于防止超过 performance.max-memory, 超过 max-memory * (1 - prepared-plan-cache.memory-guard-ratio) 会剔除 LRU 中的元素。
+ 默认值：0.1
+ 最小值为 0；最大值为 1。

## tikv-client

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
+ 默认值：2048000

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
+ 如果设置为 `true`，发生错误时，TiDB 会停止写入 binlog，并且在监控项 `tidb_server_critical_error_total` 上计数加 1；如果设置为 `false`，写入 binlog 失败，会停止整个 TiDB 的服务。

### `binlog-socket`

+ binlog 输出网络地址。
+ 默认值：""

### `strategy`

+ binlog 输出时选择 pump 的策略，仅支持 hash，range 方法。
+ 默认值："range"

## status

TiDB 服务状态相关配置。

### `report-status`

+ 开启 HTTP API 服务的开关。
+ 默认值：true

### `record-db-qps`

+ 输与 database 相关的 QPS metrics 到 Prometheus 的开关。
+ 默认值：false

## stmt-summary <span class="version-mark">从 v3.0.4 版本开始引入</span>

系统表 `events_statement_summary_by_digest` 的相关配置。

### max-stmt-count

+ `events_statement_summary_by_digest` 表中保存的 SQL 种类的最大数量。
+ 默认值：100

### max-sql-length

+ `events_statement_summary_by_digest` 表中`DIGEST_TEXT` 和 `QUERY_SAMPLE_TEXT` 列的最大显示长度。
+ 默认值：4096

## pessimistic-txn

### enable

+ 开启悲观事务支持，悲观事务使用方法请参考 [TiDB 悲观事务模式](/reference/transactions/transaction-pessimistic.md)。
+ 默认值：true

### max-retry-count

+ 悲观事务中每个语句最大重试次数，超出该限制将会报错。
+ 默认值：256

## experimental

experimental 部分为 TiDB 实验功能相关的配置。该部分从 v3.1.0 开始引入。

### `allow-auto-random` <span class="version-mark">从 v3.1.0 版本开始引入</span>

+ 用于控制是否允许使用 `AUTO_RANDOM`。
+ 默认值：false
+ 默认情况下，不支持使用 `AUTO_RANDOM`。当该值为 true 时，不允许同时设置 alter-primary-key 为 true。

### `allow-expression-index` <span class="version-mark">从 v4.0.0 版本开始引入</span>

+ 用于控制是否能创建表达式索引。
+ 默认值：false
