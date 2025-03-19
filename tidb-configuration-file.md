---
title: TiDB 配置文件描述
---

<!-- markdownlint-disable MD001 -->

# TiDB 配置文件描述

TiDB 配置文件比命令行参数支持更多的选项。你可以在 [config/config.toml.example](https://github.com/pingcap/tidb/blob/release-6.1/config/config.toml.example) 找到默认值的配置文件，重命名为 `config.toml` 即可。本文档只介绍未包含在[命令行参数](/command-line-flags-for-tidb-configuration.md)中的参数。

> **Tip:**
>
> 如果你需要调整配置项的值，请参考[修改配置参数](/maintain-tidb-using-tiup.md#修改配置参数)进行操作。

### `split-table`

+ 为每个 table 建立单独的 Region。
+ 默认值：true
+ 如果需要创建大量的表（例如 10 万张以上），建议将此参数设置为 false。

### `token-limit`

+ 可以同时执行请求的 session 个数
+ 类型：Integer
+ 默认值：1000
+ 最小值：1
+ 最大值（64 位平台）：`18446744073709551615`
+ 最大值（32 位平台）：`4294967295`

### `oom-use-tmp-storage`

+ 设置是否在单条 SQL 语句的内存使用超出系统变量 [`tidb_mem_quota_query`](/system-variables.md#tidb_mem_quota_query) 限制时为某些算子启用临时磁盘。
+ 默认值：true

### `tmp-storage-path`

+ 单条 SQL 语句的内存使用超出系统变量 [`tidb_mem_quota_query`](/system-variables.md#tidb_mem_quota_query) 限制时，某些算子的临时磁盘存储位置。
+ 默认值：`<操作系统临时文件夹>/<操作系统用户ID>_tidb/MC4wLjAuMDo0MDAwLzAuMC4wLjA6MTAwODA=/tmp-storage`。其中 `MC4wLjAuMDo0MDAwLzAuMC4wLjA6MTAwODA=` 是对 `<host>:<port>/<statusHost>:<statusPort>` 进行 `Base64` 编码的输出结果。
+ 此配置仅在 `oom-use-tmp-storage` 为 true 时有效。

### `tmp-storage-quota`

+ `tmp-storage-path` 存储使用的限额。
+ 单位：Byte
+ 当单条 SQL 语句使用临时磁盘，导致 TiDB server 的总体临时磁盘总量超过 `tmp-storage-quota` 时，当前 SQL 操作会被取消，并返回 `Out Of Global Storage Quota!` 错误。
+ 当 `tmp-storage-quota` 小于 0 时则没有上述检查与限制。
+ 默认值：-1
+ 当 `tmp-storage-path` 的剩余可用容量低于 `tmp-storage-quota` 所定义的值时，TiDB server 启动时将会报出错误并退出。

### `lease`

+ DDL 租约超时时间。
+ 默认值：45s
+ 单位：秒

### `compatible-kill-query`

+ 设置 `KILL` 语句的兼容性。
+ 默认值：false
+ `compatible-kill-query` 仅在 [`enable-global-kill`](#enable-global-kill-从-v610-版本开始引入) 为 `false` 时生效。
+ 当 [`enable-global-kill`](#enable-global-kill-从-v610-版本开始引入) 为 `false` 时，`compatible-kill-query` 控制杀死一条查询时是否需要加上 `TIDB` 关键词。
    - `compatible-kill-query` 为 `false` 时，TiDB 中 `KILL xxx` 的行为和 MySQL 中的行为不同。为杀死一条查询，在 TiDB 中需要加上 `TIDB` 关键词，即 `KILL TIDB xxx`。
    - `compatible-kill-query` 为 `true` 时，为杀死一条查询，在 TiDB 中无需加上 `TIDB` 关键词。**强烈不建议**设置 `compatible-kill-query` 为 `true`，**除非**你确定客户端将始终连接到同一个 TiDB 节点。这是因为当你在默认的 MySQL 客户端按下 <kbd>Control</kbd>+<kbd>C</kbd> 时，客户端会开启一个新连接，并在这个新连接中执行 `KILL` 语句。此时，如果客户端和 TiDB 之间存在代理，新连接可能会被路由到其他 TiDB 节点，从而错误地终止其他会话。
+ 当 [`enable-global-kill`](#enable-global-kill-从-v610-版本开始引入) 为 `true` 时，`KILL xxx` 和 `KILL TIDB xxx` 的作用相同，但是暂不支持 <kbd>Control</kbd>+<kbd>C</kbd> 终止查询。
+ 关于 `KILL` 语句的更多信息，请参考 [KILL [TIDB]](/sql-statements/sql-statement-kill.md)。

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

+ 用来修改 TiDB 在以下情况下返回的版本号：
    - 当使用内置函数 `VERSION()` 时。
    - 当与客户端初始连接，TiDB 返回带有服务端版本号的初始握手包时。具体可以查看 MySQL 初始握手包的[描述](https://dev.mysql.com/doc/internals/en/connection-phase-packets.html#packet-Protocol::Handshake)。
+ 默认值：""
+ 默认情况下，TiDB 版本号格式为：`5.7.${mysql_latest_minor_version}-TiDB-${tidb_version}`。

### `repair-mode`

+ 用于开启非可信修复模式，启动该模式后，可以过滤 `repair-table-list` 名单中坏表的加载。
+ 默认值：false
+ 默认情况下，不支持修复语法，默认启动时会加载所有表信息。

### `repair-table-list`

+ 配合 `repair-mode` 为 true 时使用，用于列出实例中需要修复的坏表的名单，该名单的写法为 ["db.table1","db.table2", ……]。
+ 默认值：[]
+ 默认情况下，该 list 名单为空，表示没有所需修复的坏表信息。

### `new_collations_enabled_on_first_bootstrap`

+ 用于开启新的 collation 支持
+ 默认值：true
+ 注意：该配置项只有在初次初始化集群时生效，初始化集群后，无法通过更改该配置项打开或关闭新的 collation 框架。

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
+ 默认值：对于 TiDB v6.1.0 ~ v6.1.4，默认值为 true；对于 v6.1.5 以及之后的 v6.1.x 版本，默认值为 false。
+ 如果在 TiDB 实例上该配置项设为 `true`，且 [`tidb_enable_telemetry`](/system-variables.md#tidb_enable_telemetry-从-v402-版本开始引入) 系统变量设置为 `ON`，该 TiDB 实例上将开启遥测功能。
+ 如果所有 TiDB 实例上该选项都设置为 `false`，那么将完全禁用 TiDB 遥测功能，且忽略 `tidb_enable_telemetry` 系统变量。参阅[遥测](/telemetry.md)了解该功能详情。

### `enable-tcp4-only` <span class="version-mark">从 v5.0 版本开始引入</span>

+ 控制是否只监听 TCP4。
+ 默认值：false
+ 当使用 LVS 为 TiDB 做负载均衡时，可开启此配置项。这是因为 [LVS 的 TOA 模块](https://github.com/alibaba/LVS/tree/master/kernel/net/toa)可以通过 TCP4 协议从 TCP 头部信息中解析出客户端的真实 IP。

### `enable-enum-length-limit` <span class="version-mark">从 v5.0 版本开始引入</span>

+ 是否限制单个 `ENUM` 元素和单个 `SET` 元素的最大长度
+ 默认值：true
+ 当该配置项值为 `true` 时，`ENUM` 和 `SET` 单个元素的最大长度为 255 个字符，[与 MySQL 8 兼容](https://dev.mysql.com/doc/refman/8.0/en/string-type-syntax.html)；当该配置项值为 `false` 时，不对单个元素的长度进行限制，与 TiDB v5.0 之前的版本兼容。

### `graceful-wait-before-shutdown` <span class="version-mark">从 v5.0 版本开始引入</span>

- 指定关闭服务器时 TiDB 等待的秒数，使得客户端有时间断开连接。
- 默认值：0
- 在 TiDB 等待服务器关闭期间，HTTP 状态会显示失败，使得负载均衡器可以重新路由流量。

### `enable-global-kill` <span class="version-mark">从 v6.1.0 版本开始引入</span>

+ 用于开启 Global Kill（跨节点终止查询或连接）功能。
+ 默认值：true
+ 当该配置项值为 `true` 时，`KILL` 语句和 `KILL TIDB` 语句均能跨节点终止查询或连接，无需担心错误地终止其他查询或连接。当你使用客户端连接到任何一个 TiDB 节点执行 `KILL` 语句或 `KILL TIDB` 语句时，该语句会被转发给对应的 TiDB 节点。当客户端和 TiDB 中间有代理时，`KILL` 语句或 `KILL TIDB` 语句也会被转发给对应的 TiDB 节点执行。目前暂时不支持在 `enable-global-kill` 为 `true` 时用 MySQL 命令行 <kbd>ctrl</kbd>+<kbd>c</kbd> 终止查询或连接。关于 `KILL` 语句的更多信息，请参考 [KILL [TIDB]](/sql-statements/sql-statement-kill.md)。

### `enable-forwarding` <span class="version-mark">从 v5.0.0 版本开始引入</span>

+ 控制 TiDB 中的 PD client 以及 TiKV client 在疑似网络隔离的情况下是否通过 follower 将请求转发给 leader。
+ 默认值：false
+ 如果确认环境存在网络隔离的可能，开启这个参数可以减少服务不可用的窗口期。
+ 如果无法准确判断隔离、网络中断、宕机等情况，这个机制存在误判情况从而导致可用性、性能降低。如果网络中从未发生过网络故障，不推荐开启此选项。

### `enable-table-lock` <span class="version-mark">从 v4.0.0 版本开始引入</span>

> **警告：**
>
> 表级锁 (Table Lock) 为实验特性，不建议在生产环境中使用。

+ 控制是否开启表级锁特性。
+ 默认值：false
+ 表级锁用于协调多个 session 之间对同一张表的并发访问。目前已支持的锁种类包括 `READ`、`WRITE` 和 `WRITE LOCAL`。当该配置项为 `false` 时，执行 `LOCK TABLES` 和 `UNLOCK TABLES` 语句不会生效，并且会报 "LOCK/UNLOCK TABLES is not supported" 的警告。更多信息，请参考 [`LOCK TABLES` 和 `UNLOCK TABLES`](/sql-statements/sql-statement-lock-tables-and-unlock-tables.md)。

## log

日志相关的配置项。

### `level`

+ 指定日志的输出级别，可选项为 [debug, info, warn, error, fatal]
+ 默认值："info"

### `format`

+ 指定日志输出的格式，可选项为 [json, text]。
+ 默认值："text"

### `enable-timestamp`

+ 是否在日志中输出时间戳。
+ 默认值：null
+ 如果设置为 false，那么日志里面将不会输出时间戳。

> **注意：**
>
> - 考虑后向兼容性，原来的配置项 `disable-timestamp` 仍然有效，但如果和 `enable-timestamp` 配置的值在语义上冲突（例如在配置中把 `enable-timestamp` 和 `disable-timestamp` 同时设置为 `true`），则 TiDB 会忽略 `disable-timestamp` 的值。
> - 当前 TiDB 默认使用 `disable-timestamp` 来决定是否在日志中输出时间戳，此时 `enable-timestamp` 的值为 `null`。
> - 在未来的版本中，`disable-timestamp` 配置项将被彻底移除，请废弃 `disable-timestamp` 的用法，使用语义上更易于理解的 `enable-timestamp`。

### `enable-slow-log`

+ 是否开启慢查询日志
+ 默认值：true
+ 可以设置成 `true` 或 `false` 来启用或或禁用慢查询日志。

### `slow-query-file`

+ 慢查询日志的文件名。
+ 默认值："tidb-slow.log"。注：由于 TiDB V2.1.8 更新了慢日志格式，所以将慢日志单独输出到了慢日志文件。V2.1.8 之前的版本，该变量的默认值是 ""。
+ 设置后，慢查询日志会单独输出到该文件。

### `slow-threshold`

+ 输出慢日志的耗时阈值。
+ 默认值：300
+ 单位：毫秒
+ 如果查询耗时大于这个值，会视作一个慢查询，并记录到慢查询日志。注意，当日志的输出级别 [`log.level`](#level) 是 `"debug"` 时，所有查询都会记录到慢日志，不受该参数的限制。
+ 自 v6.1.0 起，已改用配置项 `instance.tidb_slow_log_threshold` 或系统变量 `tidb_slow_log_threshold` 来设置输出慢日志的耗时阈值。`slow-threshold` 仍可使用，但如果同时设置了 `slow-threshold` 与 `instance.tidb_slow_log_threshold`，TiDB 将采用 `instance.tidb_slow_log_threshold` 的值。

### `record-plan-in-slow-log`

+ 在慢日志中记录执行计划
+ 默认值：1
+ 0 表示关闭，1 表示开启，默认开启，该值作为系统变量 [`tidb_record_plan_in_slow_log`](/system-variables.md#tidb_record_plan_in_slow_log) 的初始值。

### `expensive-threshold`

> **警告：**
>
> 自 v5.4.0 起，该配置项被废弃。请使用 [`tidb_expensive_query_time_threshold`](/system-variables.md#tidb_expensive_query_time_threshold) 系统变量进行设置。

+ 输出 `expensive` 操作的行数阈值。
+ 默认值：10000
+ 当查询的行数（包括中间结果，基于统计信息）大于这个值，该操作会被认为是 `expensive` 查询，并输出一个前缀带有 `[EXPENSIVE_QUERY]` 的日志。

## log.file

日志文件相关的配置项。

#### `filename`

+ 一般日志文件名字。
+ 默认值：""
+ 如果设置，会输出一般日志到这个文件。

#### `max-size`

+ 日志文件的大小限制。
+ 默认值：300
+ 单位：MB
+ 最大设置上限为 4096。

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

### `cluster-verify-cn`

+ 客户端提供的证书中，可接受的 X.509 通用名称列表。仅当提供的通用名称与列表中的条目之一完全匹配时，才会允许其请求。
+ 默认值：[]，表示禁用客户端证书 CN 检查。

### `spilled-file-encryption-method`

+ 内存落盘文件的加密方式。
+ 默认值：`"plaintext"`，表示不进行加密。
+ 可选值：`"plaintext"`、`"aes128-ctr"`。

### `auto-tls`

+ 控制 TiDB 启动时是否自动生成 TLS 证书。
+ 默认值：`false`

### `tls-version`

+ 设置用于连接 MySQL 协议的最低 TLS 版本。
+ 默认值：""，支持 TLSv1.1 及以上版本。
+ 可选值：`"TLSv1.0"`、`"TLSv1.1"`、`"TLSv1.2"` 和 `"TLSv1.3"`

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

+ 设置 tidb-server 实例的最大内存用量，单位为字节。
+ 默认值：0
+ 默认值为 0 表示无内存限制。

### `memory-usage-alarm-ratio` <span class="version-mark">从 v4.0.9 版本开始引入</span>

+ tidb-server 实例内存使用占总内存的比例超过一定阈值时会报警。该配置项的有效范围为 `0` 到 `1`。如果配置该选项为 `0` 或 `1`，则表示关闭内存阈值报警功能。
+ 默认值：0.8
+ 当内存阈值报警功能开启时，如果配置项 [`server-memory-quota`](/tidb-configuration-file.md#server-memory-quota-从-v409-版本开始引入) 未设置，则内存报警阈值为 `memory-usage-alarm-ratio * 系统内存大小`；如果 `server-memory-quota` 被设置且大于 0，则内存报警阈值为 `memory-usage-alarm-ratio * server-memory-quota`。
+ 当 TiDB 检测到 tidb-server 的内存使用超过了阈值，则会认为存在内存溢出的风险，会将当前正在执行的所有 SQL 语句中内存使用最高的 10 条语句和运行时间最长的 10 条语句以及 heap profile 记录到目录 [`tmp-storage-path/record`](/tidb-configuration-file.md#tmp-storage-path) 中，并输出一条包含关键字 `tidb-server has the risk of OOM` 的日志。
+ 该值作为系统变量 [`tidb_memory_usage_alarm_ratio`](/system-variables.md#tidb_memory_usage_alarm_ratio) 的初始值。

### `txn-entry-size-limit` <span class="version-mark">从 v4.0.10 和 v5.0.0 版本开始引入</span>

+ TiDB 单行数据的大小限制
+ 默认值：6291456
+ 单位：Byte
+ 事务中单个 key-value 记录的大小限制。若超出该限制，TiDB 将会返回 `entry too large` 错误。该配置项的最大值不超过 `125829120`（表示 120MB）。
+ 注意，TiKV 有类似的限制。若单个写入请求的数据量大小超出 [`raft-entry-max-size`](/tikv-configuration-file.md#raft-entry-max-size)，默认为 8MB，TiKV 会拒绝处理该请求。当表的一行记录较大时，需要同时修改这两个配置。
+ [`max_allowed_packet`](/system-variables.md#max_allowed_packet-从-v610-版本开始引入) (MySQL 协议的最大数据包大小) 的默认值为 `67108864`（64 MiB）。如果一行记录的大小超过 `max_allowed_packet`，该行记录会被截断。
+ [`txn-total-size-limit`](#txn-total-size-limit)（TiDB 单个事务大小限制）的默认值为 100 MiB。如果将 `txn-entry-size-limit` 的值设置为 100 MiB 以上，需要相应地调大 `txn-total-size-limit` 的值。

### `txn-total-size-limit`

+ TiDB 单个事务大小限制
+ 默认值：104857600
+ 单位：Byte
+ 单个事务中，所有 key-value 记录的总大小不能超过该限制。该配置项的最大值不超过 `1099511627776`（表示 1TB）。注意，如果使用了以 `Kafka` 为下游消费者的 `binlog`，如：`arbiter` 集群，该配置项的值不能超过 `1073741824`（表示 1GB），因为这是 `Kafka` 的处理单条消息的最大限制，超过该限制 `Kafka` 将会报错。

### `max-txn-ttl`

+ 单个事务持锁的最长时间，超过该时间，该事务的锁可能会被其他事务清除，导致该事务无法成功提交。
+ 默认值：3600000
+ 单位：毫秒
+ 超过此时间的事务只能执行提交或者回滚，提交不一定能够成功。

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

### `feedback-probability`

> **警告：**
>
> 从 v5.4 起，该功能已被废弃。不建议开启此功能。

+ TiDB 对查询收集统计信息反馈的概率。
+ 默认值：0
+ 此功能默认关闭，暂不建议开启。如果开启此功能，对于每一个查询，TiDB 会以 `feedback-probability` 的概率收集查询的反馈，用于更新统计信息。

### `query-feedback-limit`

+ 在内存中缓存的最大 Query Feedback 数量，超过这个数量的 Feedback 会被丢弃。
+ 默认值：512

### `pseudo-estimate-ratio`

+ 修改过的行数/表的总行数的比值，超过该值时系统会认为统计信息已经过期，会采用 pseudo 的统计信息。
+ 默认值：0.8
+ 最小值：0
+ 最大值：1

### `force-priority`

+ 把所有的语句优先级设置为 force-priority 的值。
+ 默认值：NO_PRIORITY
+ 可选值：默认值 NO_PRIORITY 表示不强制改变执行语句的优先级，其它优先级从低到高可设置为 LOW_PRIORITY、DELAYED 或 HIGH_PRIORITY。

### `distinct-agg-push-down`

+ 设置优化器是否执行将带有 `Distinct` 的聚合函数（比如 `select count(distinct a) from t`）下推到 Coprocessor 的优化操作。
+ 默认值：false
+ 该变量作为系统变量 [`tidb_opt_distinct_agg_push_down`](/system-variables.md#tidb_opt_distinct_agg_push_down) 的初始值。

### `enforce-mpp`

+ 用于控制是否忽略优化器代价估算，强制使用 TiFlash 的 MPP 模式执行查询。
+ 默认值：false
+ 该配置项可以控制系统变量 [`tidb_enforce_mpp`](/system-variables.md#tidb_enforce_mpp-从-v51-版本开始引入) 的初始值。例如，当设置该配置项为 true 时，`tidb_enforce_mpp` 的默认值为 ON。

### `stats-load-concurrency` <span class="version-mark">从 v5.4.0 版本开始引入</span>

> **警告：**
>
> 统计信息同步加载功能目前为实验性特性，不建议在生产环境中使用。

+ TiDB 统计信息同步加载功能可以并发处理的最大列数
+ 默认值：5
+ 目前的合法值范围：`[1, 128]`

### `stats-load-queue-size` <span class="version-mark">从 v5.4.0 版本开始引入</span>

> **警告：**
>
> 统计信息同步加载功能目前为实验性特性，不建议在生产环境中使用。

+ 用于设置 TiDB 统计信息同步加载功能最多可以缓存多少列的请求
+ 默认值：1000
+ 目前的合法值范围：`[1, 100000]`

### `enable-stats-cache-mem-quota` <span class="version-mark">从 v6.1.0 版本开始引入</span>

> **警告：**
>
> 该变量为实验特性，不推荐在生产环境中使用。

+ 用于控制 TiDB 是否开启统计信息缓存的内存上限。
+ 默认值：false

## opentracing

opentracing 的相关的设置。

### `enable`

+ 开启 opentracing 跟踪 TiDB 部分组件的调用开销。注意开启后会有一定的性能损失。
+ 默认值：false

### `rpc-metrics`

+ 开启 rpc metrics。
+ 默认值：false

## opentracing.sampler

opentracing.sampler 相关的设置。

### `type`

+ opentracing 采样器的类型。字符串取值大小写不敏感。
+ 默认值："const"
+ 可选值："const"，"probabilistic"，"ratelimiting"，remote"

### `param`

+ 采样器参数。
    - 对于 const 类型，可选值为 0 或 1，表示是否开启。
    - 对于 probabilistic 类型，参数为采样概率，可选值为 0 到 1 之间的浮点数。
    - 对于 ratelimiting 类型，参数为每秒采样 span 的个数。
    - 对于 remote 类型，参数为采样概率，可选值为 0 到 1 之间的浮点数。
+ 默认值：1.0

### `sampling-server-url`

+ jaeger-agent 采样服务器的 HTTP URL 地址。
+ 默认值：""

### `max-operations`

+ 采样器可追踪的最大操作数。如果一个操作没有被追踪，会启用默认的 probabilistic 采样器。
+ 默认值：0

### `sampling-refresh-interval`

+ 控制远程轮询 jaeger-agent 采样策略的频率。
+ 默认值：0

## opentracing.reporter

opentracing.reporter 相关的设置。

### `queue-size`

+ reporter 在内存中记录 spans 个数的队列容量。
+ 默认值：0

### `buffer-flush-interval`

+ reporter 缓冲区的刷新频率。
+ 默认值：0

### `log-spans`

+ 是否为所有提交的 span 打印日志。
+ 默认值：false

### `local-agent-host-port`

+ reporter 向 jaeger-agent 发送 span 的地址。
+ 默认值：""

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

### `grpc-compression-type`

+ 控制 TiDB 向 TiKV 节点传输数据使用的压缩算法类型。默认值为 "none" 即不压缩。修改为 "gzip" 可以使用 gzip 算法压缩数据。
+ 默认值："none"
+ 可选值："none", "gzip"

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

+ 输出与 database 相关的 QPS metrics 到 Prometheus 的开关。
+ 默认值：false

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

### deadlock-history-collect-retryable

+ 控制 [`INFORMATION_SCHEMA.DEADLOCKS`](/information-schema/information-schema-deadlocks.md) 表中是否收集可重试的死锁错误信息。详见 `DEADLOCKS` 表文档的[可重试的死锁错误](/information-schema/information-schema-deadlocks.md#可重试的死锁错误)小节。
+ 默认值：false

### pessimistic-auto-commit

+ 用来控制开启全局悲观事务模式下 (`tidb_txn_mode='pessimistic'`) 时，自动提交的事务使用的事务模式。默认情况下，即使开启全局悲观事务模式，自动提交事务依然使用乐观事务模式来执行。当开启该配置项后（设置为 `true`），在全局悲观事务模式下，自动提交事务将也使用悲观事务模式执行。行为与其他显式提交的悲观事务相同。
+ 对于存在冲突的场景，开启本开关可以将自动提交事务纳入全局等锁管理中，从而避免死锁，改善冲突造成死锁带来的时延尖刺。
+ 对于不存在冲突的场景，如果有大量自动提交事务（例如自动提交事务数量占业务数量的比例超过一半甚至更多，需要根据实际情况分析）且单个事务操作数据量较大的情况下，开启该配置项会造成性能回退。例如，自动提交的 `INSERT INTO SELECT` 语句。

+ 默认值：false

## isolation-read

读取隔离相关的配置项。

### `engines`

+ 用于控制 TiDB 节点允许从哪种类型的引擎读取数据。
+ 默认值：["tikv", "tiflash", "tidb"]，表示由优化器自动选择存储引擎。
+ 可选值："tikv", "tiflash", "tidb" 的组合，如：["tikv", "tidb"]、["tiflash", "tidb"]。

## instance

### `tidb_enable_collect_execution_info`

+ 用于控制是否同时将各个执行算子的执行信息记录入 slow query log 中。
+ 默认值：true
+ 在 v6.1.0 之前，该功能通过配置项 `enable-collect-execution-info` 进行设置。

### `tidb_enable_slow_log`

+ 是否开启慢查询日志。
+ 默认值：true
+ 可以设置成 `true` 或 `false` 来启用或禁用慢查询日志。
+ 在 v6.1.0 之前，该功能通过配置项 `enable-slow-log` 进行设置。

### `tidb_slow_log_threshold`

+ 输出慢日志的耗时阈值。
+ 默认值：300
+ 范围：`[-1, 9223372036854775807]`
+ 单位：毫秒
+ 如果查询耗时大于这个值，会视作一个慢查询，并记录到慢查询日志。注意，当日志的输出级别 [`log.level`](#level) 是 `"debug"` 时，所有查询都会记录到慢日志，不受该参数的限制。
+ 在 v6.1.0 之前，该功能通过配置项 `slow-threshold` 进行设置。

### `tidb_expensive_query_time_threshold`

+ 控制打印 expensive query 日志的阈值时间，默认值是 60 秒。expensive query 日志和慢日志的差别是，慢日志是在语句执行完后才打印，expensive query 日志可以把正在执行中且执行时间超过该阈值的语句及其相关信息打印出来。
+ 默认值：60
+ 范围：`[10, 2147483647]`
+ 单位：秒
+ 在 v5.4.0 之前，该功能通过配置项 `expensive-threshold` 进行设置。

### `tidb_record_plan_in_slow_log`

+ 在慢日志中记录执行计划。
+ 默认值：1
+ 0 表示关闭，1 表示开启，默认开启，该值作为系统变量 [`tidb_record_plan_in_slow_log`](/system-variables.md#tidb_record_plan_in_slow_log) 的初始值。
+ 在 v6.1.0 之前，该功能通过配置项 `record-plan-in-slow-log` 进行设置。

### `tidb_force_priority`

+ 把所有的语句优先级设置为系统变量 `tidb_force_priority` 的值。
+ 默认值：NO_PRIORITY
+ 默认值 NO_PRIORITY 表示不强制改变执行语句的优先级，其它优先级从低到高可设置为 LOW_PRIORITY、DELAYED 或 HIGH_PRIORITY。
+ 在 v6.1.0 之前，该功能通过配置项 `force-priority` 进行设置。

## proxy-protocol

PROXY 协议相关的配置项。

### `networks`

+ 允许使用 [PROXY 协议](https://www.haproxy.org/download/1.8/doc/proxy-protocol.txt)连接 TiDB 的代理服务器地址列表。
+ 默认值：""
+ 通常情况下，通过反向代理使用 TiDB 时，TiDB 会将反向代理服务器的 IP 地址视为客户端 IP 地址。对于支持 PROXY 协议的反向代理（如 HAProxy），开启 PROXY 协议后能让反向代理透传客户端真实的 IP 地址给 TiDB。
+ 配置该参数后，TiDB 将允许配置的源 IP 地址使用 PROXY 协议连接到 TiDB，且拒绝这些源 IP 地址使用非 PROXY 协议连接。若该参数为空，则任何源 IP 地址都不能使用 PROXY 协议连接到 TiDB。地址可以使用 IP 地址格式 (192.168.1.50) 或者 CIDR 格式 (192.168.1.0/24)，并可用 `,` 分隔多个地址，或用 `*` 代表所有 IP 地址。

> **警告：**
>
> 需谨慎使用 `*` 符号，因为 `*` 允许来自任何 IP 的客户端自行汇报其 IP 地址，从而可能引入安全风险。另外，`*` 可能导致部分直接连接 TiDB 的内部组件无法使用，例如 TiDB Dashboard。

## experimental

experimental 部分为 TiDB 实验功能相关的配置。该部分从 v3.1.0 开始引入。

### `allow-expression-index` <span class="version-mark">从 v4.0.0 版本开始引入</span>

+ 用于控制是否能创建表达式索引。自 v5.2.0 版本起，如果表达式中的函数是安全的，你可以直接基于该函数创建表达式索引，不需要打开该配置项。如果要创建基于其他函数的表达式索引，可以打开该配置项，但可能存在正确性问题。通过查询 `tidb_allow_function_for_expression_index` 变量可得到能直接用于创建表达式的安全函数。
+ 默认值：false
