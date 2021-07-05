---
title: TiDB 配置文件描述
aliases: ['/docs-cn/dev/tidb-configuration-file/','/docs-cn/dev/reference/configuration/tidb-server/configuration-file/']
---

<!-- markdownlint-disable MD001 -->

# TiDB 配置文件描述

TiDB 配置文件比命令行参数支持更多的选项。你可以在 [config/config.toml.example](https://github.com/pingcap/tidb/blob/master/config/config.toml.example) 找到默认值的配置文件，重命名为 `config.toml` 即可。本文档只介绍未包含在[命令行参数](/command-line-flags-for-tidb-configuration.md)中的参数。

### `split-table`

+ 为每个 table 建立单独的 Region。
+ 默认值：true
+ 如果需要创建大量的表，建议将此参数设置为 false。

### `token-limit`

+ 可以同时执行请求的 session 个数
+ 类型：Integer
+ 默认值：1000
+ 最小值：1
+ 最大值（64 位平台）：`18446744073709551615`
+ 最大值（32 位平台）：`4294967295`

### `mem-quota-query`

+ 单条 SQL 语句可以占用的最大内存阈值，单位为字节。
+ 默认值：1073741824
+ 注意：当集群从 v2.0.x 或 v3.0.x 版本直接升级至 v4.0.9 及以上版本时，该配置默认值为 34359738368。
+ 超过该值的请求会被 `oom-action` 定义的行为所处理。
+ 该值作为系统变量 [`tidb_mem_quota_query`](/system-variables.md#tidb_mem_quota_query) 的初始值。

### `oom-use-tmp-storage`

+ 设置是否在单条 SQL 语句的内存使用超出 `mem-quota-query` 限制时为某些算子启用临时磁盘。
+ 默认值：true

### `tmp-storage-path`

+ 单条 SQL 语句的内存使用超出 `mem-quota-query` 限制时，某些算子的临时磁盘存储位置。
+ 默认值：`<操作系统临时文件夹>/<操作系统用户ID>_tidb/MC4wLjAuMDo0MDAwLzAuMC4wLjA6MTAwODA=/tmp-storage`。其中 `MC4wLjAuMDo0MDAwLzAuMC4wLjA6MTAwODA=` 是对 `<host>:<port>/<statusHost>:<statusPort>` 进行 `Base64` 编码的输出结果。
+ 此配置仅在 `oom-use-tmp-storage` 为 true 时有效。

### `tmp-storage-quota`

+ `tmp-storage-path` 存储使用的限额。
+ 单位：Byte
+ 当单条 SQL 语句使用临时磁盘，导致 TiDB server 的总体临时磁盘总量超过 `tmp-storage-quota` 时，当前 SQL 操作会被取消，并返回 `Out Of Global Storage Quota!` 错误。
+ 当 `tmp-storage-quota` 小于 0 时则没有上述检查与限制。
+ 默认值: -1
+ 当 `tmp-storage-path` 的剩余可用容量低于 `tmp-storage-quota` 所定义的值时，TiDB server 启动时将会报出错误并退出。

### `oom-action`

+ 当 TiDB 中单条 SQL 的内存使用超出 `mem-quota-query` 限制且不能再利用临时磁盘时的行为。
+ 默认值："cancel"
+ 目前合法的选项为 ["log", "cancel"]。设置为 "log" 时，仅输出日志。设置为 "cancel" 时，取消执行该 SQL 操作，并输出日志。

### `lower-case-table-names`

+ 这个选项可以设置 TiDB 的系统变量 `lower-case-table-names` 的值。
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

+ 将旧表中的 utf8 字符集当成 utf8mb4 的开关。
+ 默认值：true

### `alter-primary-key`（已废弃）

+ 用于控制添加或者删除主键功能。
+ 默认值：false
+ 默认情况下，不支持增删主键。将此变量被设置为 true 后，支持增删主键功能。不过对在此开关开启前已经存在的表，且主键是整型类型时，即使之后开启此开关也不支持对此列表删除主键。

> **注意：**
>
> 该配置项已被废弃，目前仅在 `@@tidb_enable_clustered_index` 取值为 `INT_ONLY` 时生效。如果需要增删主键，请在建表时使用 `NONCLUSTERED` 关键字代替。要了解关于 `CLUSTERED` 主键的详细信息，请参考[聚簇索引](/clustered-indexes.md)。

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
+ 单位：Byte
+ 目前的合法值范围 `[3072, 3072*4]`。MySQL 和 TiDB v3.0.11 之前版本（不包含 v3.0.11）没有此配置项，不过都对新建索引的长度做了限制。MySQL 对此的长度限制为 `3072`，TiDB 在 v3.0.7 以及之前版本该值为 `3072*4`，在 v3.0.7 之后版本（包含 v3.0.8、v3.0.9 和 v3.0.10）的该值为 `3072`。为了与 MySQL 和 TiDB 之前版本的兼容，添加了此配置项。

### `table-column-count-limit` <span class="version-mark">从 v5.0 版本开始引入</span>

+ 用于设置单个表中列的数量限制
+ 默认值：1017
+ 目前的合法值范围 `[1017, 4096]`。

### `index-limit` <span class="version-mark">从 v5.0 版本开始引入</span>

+ 用于设置单个表中索引的数量限制
+ 默认值：64
+ 目前的合法值范围 `[64, 512]`。

### `enable-telemetry` <span class="version-mark">从 v4.0.2 版本开始引入</span>

+ 是否开启 TiDB 遥测功能。
+ 默认值：true
+ 如果所有 TiDB 实例上该选项都设置为 `false`，那么将完全禁用 TiDB 遥测功能，且忽略 [`tidb_enable_telemetry`](/system-variables.md#tidb_enable_telemetry-从-v402-版本开始引入) 系统变量。参阅[遥测](/telemetry.md)了解该功能详情。

### `enable-tcp4-only` <span class="version-mark">从 v5.0 版本开始引入</span>

+ 控制是否只监听 TCP4。
+ 默认值：false
+ 当使用 LVS 为 TiDB 做负载均衡时，可开启此配置项。这是因为 [LVS 的 TOA 模块](https://github.com/alibaba/LVS/tree/master/kernel/net/toa)可以通过 TCP4 协议从 TCP 头部信息中解析出客户端的真实 IP。

### `enable-enum-length-limit` <span class="version-mark">从 v5.0 版本开始引入</span>

+ 是否限制单个 `ENUM` 元素和单个 `SET` 元素的最大长度
+ 默认值：true
+ 当该配置项值为 `true` 时，`ENUM` 和 `SET` 单个元素的最大长度为 255 个字符，[与 MySQL 8 兼容](https://dev.mysql.com/doc/refman/8.0/en/string-type-syntax.html)；当该配置项值为 `false` 时，不对单个元素的长度进行限制，与 TiDB v5.0 之前的版本兼容。

#### `graceful-wait-before-shutdown` <span class="version-mark">从 v5.0 版本开始引入</span>

- 指定关闭服务器时 TiDB 等待的秒数，使得客户端有时间断开连接。
- 默认值：0
- 在 TiDB 等待服务器关闭期间，HTTP 状态会显示失败，使得负载均衡器可以重新路由流量。

## log

日志相关的配置项。

### `level`

+ 指定日志的输出级别, 可选项为 [debug, info, warn, error, fatal]
+ 默认值："info"

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

### `record-plan-in-slow-log`

+ 在慢日志中记录执行计划
+ 默认值：1
+ 0 表示关闭，1 表示开启，默认开启，该值作为系统变量 [`tidb_record_plan_in_slow_log`](/system-variables.md#tidb_record_plan_in_slow_log) 的初始值。

### `expensive-threshold`

+ 输出 `expensive` 操作的行数阈值。
+ 默认值：10000
+ 当查询的行数（包括中间结果，基于统计信息）大于这个值，该操作会被认为是 `expensive` 查询，并输出一个前缀带有 `[EXPENSIVE_QUERY]` 的日志。

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

## security

安全相关配置。

### `enable-sem`

- 启用安全增强模式 (SEM)。
- 默认值：`false`
- 可以通过系统变量 [`tidb_enable_enhanced_security`](/system-variables.md#tidb_enable_enhanced_security) 获取安全增强模式的状态。

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

### `spilled-file-encryption-method`

+ 内存落盘文件的加密方式。
+ 默认值: `"plaintext"`，表示不进行加密
+ 可选值：`"plaintext"`、`"aes128-ctr"`

## performance

性能相关配置。

### `max-procs`

+ TiDB 的 CPU 使用数量。
+ 默认值：0
+ 默认值为 0 表示使用机器上所有的 CPU；如果设置成 n，那么 TiDB 会使用 n 个 CPU 数量。

### `server-memory-quota` <span class="version-mark">从 v4.0.9 版本开始引入</span>

> **警告：**
>
> `server-memory-quota` 目前为实验性特性，不建议在生产环境中使用。

+ tidb-server 实例内存的使用限制，单位为字节。<!-- 从 TiDB v5.0 起 -->该配置项完全取代原有的 [`max-memory`](https://docs.pingcap.com/zh/tidb/stable/tidb-configuration-file#max-memory)。

+ 默认值：0
+ 默认值为 0 表示无内存限制。

### `memory-usage-alarm-ratio` <span class="version-mark">从 v4.0.9 版本开始引入</span>

+ tidb-server 实例内存使用占总内存的比例超过一定阈值时会报警。该配置项的有效范围为 `0` 到 `1`。如果配置该选项为 `0` 或 `1`，则表示关闭内存阈值报警功能。
+ 默认值：0.8
+ 当内存阈值报警功能开启时，如果配置项 [`server-memory-quota`](/tidb-configuration-file.md#server-memory-quota-从-v409-版本开始引入) 未设置，则内存报警阈值为 `memory-usage-alarm-ratio * 系统内存大小`；如果 `server-memory-quota` 被设置且大于 0，则内存报警阈值为 `memory-usage-alarm-ratio * server-memory-quota`。
+ 当 TiDB 检测到 tidb-server 的内存使用超过了阈值，则会认为存在内存溢出的风险，会将当前正在执行的所有 SQL 语句中内存使用最高的 10 条语句和运行时间最长的 10 条语句以及 heap profile 记录到目录 [`tmp-storage-path/record`](/tidb-configuration-file.md#tmp-storage-path) 中，并输出一条包含关键字 `tidb-server has the risk of OOM` 的日志。
+ 该值作为系统变量 [`tidb_memory_usage_alarm_ratio`](/system-variables.md#tidb_memory_usage_alarm_ratio) 的初始值。

### `txn-entry-size-limit` <span class="version-mark">从 v5.0 版本开始引入</span>

+ TiDB 单行数据的大小限制
+ 默认值：6291456
+ 单位：Byte
+ 事务中单个 key-value 记录的大小限制。若超出该限制，TiDB 将会返回 `entry too large` 错误。该配置项的最大值不超过 `125829120`（表示 120MB）。
+ 注意，TiKV 有类似的限制。若单个写入请求的数据量大小超出 [`raft-entry-max-size`](/tikv-configuration-file.md#raft-entry-max-size)，默认为 8MB，TiKV 会拒绝处理该请求。当表的一行记录较大时，需要同时修改这两个配置。

### `txn-total-size-limit`

+ TiDB 单个事务大小限制
+ 默认值：104857600
+ 单位：Byte
+ 单个事务中，所有 key-value 记录的总大小不能超过该限制。该配置项的最大值不超过 `10737418240`（表示 10GB）。注意，如果使用了以 `Kafka` 为下游消费者的 `binlog`，如：`arbiter` 集群，该配置项的值不能超过 `1073741824`（表示 1GB），因为这是 `Kafka` 的处理单条消息的最大限制，超过该限制 `Kafka` 将会报错。

### `max-txn-ttl`

+ 单个事务持锁的最长时间，超过该时间，该事务的锁可能会被其他事务清除，导致该事务无法成功提交。
+ 默认值：3600000
+ 单位：毫秒
+ 超过此时间的事务只能执行提交或者回滚，提交不一定能够成功。

### `committer-concurrency`

+ 在单个事务的提交阶段，用于执行提交操作相关请求的 goroutine 数量
+ 默认值：16
+ 若提交的事务过大，事务提交时的流控队列等待耗时可能会过长，可以通过调大该配置项来加速提交。

### `stmt-count-limit`

+ TiDB 单个事务允许的最大语句条数限制。
+ 默认值：5000
+ 在一个事务中，超过 `stmt-count-limit` 条语句后还没有 rollback 或者 commit，TiDB 将会返回 `statement count 5001 exceeds the transaction limitation, autocommit = false` 错误。该限制只在可重试的乐观事务中生效，如果使用悲观事务或者关闭了[事务重试](/optimistic-transaction.md#事务的重试)，事务中的语句数将不受此限制。

### `tcp-keep-alive`

+ TiDB 在 TCP 层开启 keepalive。
+ 默认值：true

### `tcp-no-delay`

+ 控制 TiDB 是否在 TCP 层开启 TCP_NODELAY。开启后，TiDB 将禁用 TCP/IP 协议中的 Nagle 算法，允许小数据包的发送，可以降低网络延时，适用于延时敏感型且数据传输量比较小的应用。
+ 默认值：true

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
+ 当 `stats-lease` 为 0s 时，TiDB 会以 3s 的时间间隔周期性的读取系统表中的统计信息并更新内存中缓存的统计信息。但不会自动修改统计信息相关系统表，具体来说，TiDB 不再自动修改这些表：
    - `mysql.stats_meta`：TiDB 不再自动记录事务中对某张表的修改行数，也不会更新到这个系统表中
    - `mysql.stats_histograms`/`mysql.stats_buckets` 和 `mysql.stats_top_n`：TiDB 不再自动 analyze 和主动更新统计信息
    - `mysql.stats_feedback`：TiDB 不再根据被查询的数据反馈的部分统计信息更新表和索引的统计信息

### `run-auto-analyze`

+ TiDB 是否做自动的 Analyze。
+ 默认值：true

### `feedback-probability`

+ TiDB 对查询收集统计信息反馈的概率。
+ 默认值：0
+ 此功能默认关闭，暂不建议开启。如果开启此功能，对于每一个查询，TiDB 会以 `feedback-probability` 的概率收集查询的反馈，用于更新统计信息。

### `query-feedback-limit`

+ 在内存中缓存的最大 Query Feedback 数量，超过这个数量的 Feedback 会被丢弃。
+ 默认值：1024

### `pseudo-estimate-ratio`

+ 修改过的行数/表的总行数的比值，超过该值时系统会认为统计信息已经过期，会采用 pseudo 的统计信息。
+ 默认值：0.8
+ 最小值：0
+ 最大值：1

### `force-priority`

+ 把所有的语句优先级设置为 force-priority 的值。
+ 默认值：NO_PRIORITY
+ 可选值：NO_PRIORITY, LOW_PRIORITY, HIGH_PRIORITY, DELAYED。

### `distinct-agg-push-down`

+ 设置优化器是否执行将带有 `Distinct` 的聚合函数（比如 `select count(distinct a) from t`）下推到 Coprocessor 的优化操作。
+ 默认值：false
+ 该变量作为系统变量 [`tidb_opt_distinct_agg_push_down`](/system-variables.md#tidb_opt_distinct_agg_push_down) 的初始值。

### `nested-loop-join-cache-capacity`

+ nested loop join cache LRU 使用的最大内存限制。可以占用的最大内存阈值。
+ 单位：Byte
+ 默认值：20971520
+ 当 `nested-loop-join-cache-capacity = 0` 时，默认关闭 nested loop join cache。 当 LRU 的 size 大于 `nested-loop-join-cache-capacity` 时，也会剔除 LRU 中的元素。

### `enforce-mpp`

+ 用于控制是否忽略优化器代价估算，强制使用 TiFlash 的 MPP 模式执行查询.
+ 默认值：false
+ 该配置项可以控制系统变量 [`tidb_enforce_mpp`](/system-variables.md#tidb_enforce_mpp-从-v51-版本开始引入) 的初始值。例如，当设置该配置项为 true 时，`tidb_enforce_mpp` 的默认值为 ON。

## prepared-plan-cache

prepare 语句的 plan cache 设置。

> **警告：**
>
> 当前该功能仍为实验特性，不建议在生产环境中使用。

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
+ 最小值：0
+ 最大值：1

## tikv-client

### `grpc-connection-count`

+ 跟每个 TiKV 之间建立的最大连接数。
+ 默认值：4

### `grpc-keepalive-time`

+ TiDB 与 TiKV 节点之间 rpc 连接 keepalive 时间间隔，如果超过该值没有网络包，grpc client 会 ping 一下 TiKV 查看是否存活。
+ 默认值：10
+ 单位：秒

### `grpc-keepalive-timeout`

+ TiDB 与 TiKV 节点 rpc keepalive 检查的超时时间
+ 默认值：3
+ 单位：秒

### `commit-timeout`

+ 执行事务提交时，最大的超时时间。
+ 默认值：41s
+ 这个值必须是大于两倍 Raft 选举的超时时间。

### `max-batch-size`

+ 批量发送 rpc 封包的最大数量，如果不为 0，将使用 BatchCommands api 发送请求到 TiKV，可以在并发度高的情况降低 rpc 的延迟，推荐不修改该值。
+ 默认值：128

### `max-batch-wait-time`

+ 等待 `max-batch-wait-time` 纳秒批量将此期间的数据包封装成一个大包发送给 TiKV 节点，仅在 `tikv-client.max-batch-size` 值大于 0 时有效，不推荐修改该值。
+ 默认值：0
+ 单位：纳秒

### `batch-wait-size`

+ 批量向 TiKV 发送的封包最大数量，不推荐修改该值。
+ 默认值：8
+ 若此值为 0 表示关闭此功能。

### `overload-threshold`

+ TiKV 的负载阈值，如果超过此阈值，会收集更多的 batch 封包，来减轻 TiKV 的压力。仅在 `tikv-client.max-batch-size` 值大于 0 时有效，不推荐修改该值。
+ 默认值：200

## tikv-client.copr-cache <span class="version-mark">从 v4.0.0 版本开始引入</span>

本部分介绍 Coprocessor Cache 相关的配置项。

### `capacity-mb`

+ 缓存的总数据量大小。当缓存空间满时，旧缓存条目将被逐出。值为 0.0 时表示关闭 Coprocessor Cache。
+ 默认值：1000.0
+ 单位：MB
+ 类型：Float

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

+ `events_statement_summary_by_digest` 表中 `DIGEST_TEXT` 和 `QUERY_SAMPLE_TEXT` 列的最大显示长度。
+ 默认值：4096

## pessimistic-txn

悲观事务使用方法请参考 [TiDB 悲观事务模式](/pessimistic-transaction.md)。

### max-retry-count

+ 悲观事务中单个语句最大重试次数，重试次数超过该限制，语句执行将会报错。
+ 默认值：256

### deadlock-history-capacity

+ 单个 TiDB 节点的 [`INFORMATION_SCHEMA.DEADLOCKS`](/information-schema/information-schema-deadlocks.md) 表最多可记录的死锁事件个数。当表的容量已满时，如果再次发生死锁错误，最早的一次死锁错误的信息将从表中移除。
+ 默认值：10
+ 最小值：0
+ 最大值：10000

## experimental

experimental 部分为 TiDB 实验功能相关的配置。该部分从 v3.1.0 开始引入。

### `allow-expression-index` <span class="version-mark">从 v4.0.0 版本开始引入</span>

+ 用于控制是否能创建表达式索引。
+ 默认值：false
