---
title: TiDB 配置参数
summary: TiDB 配置参数包括启动参数和环境变量。启动参数包括 advertise-address、config、config-check、config-strict、cors 等。其中默认端口为 4000 和 10080。其他参数包括 log-file、metrics-addr、metrics-interval 等。注意配置文件的有效性和安全模式下的启动。
---

# TiDB 配置参数

在启动 TiDB 时，你可以使用命令行参数或环境变量来配置 TiDB。

要快速了解 TiDB 的参数体系与参数作用域，建议先观看下面的培训视频（时长 17 分钟）。

<video src="https://docs-download.pingcap.com/media/videos/docs-cn%2FLesson10_config.mp4" width="600px" height="450px" controls="controls" poster="https://docs-download.pingcap.com/media/videos/docs-cn/poster_lesson10.png"></video>

本文将详细介绍 TiDB 的命令行启动参数。TiDB 的默认端口为 4000（客户端请求）与 10080（状态报告）。

## `--advertise-address`

+ 登录 TiDB 的 IP 地址
+ 默认：""
+ 必须确保用户和集群中的其他机器都能够访问到该 IP 地址

## `--config`

+ 配置文件
+ 默认：""
+ 如果你指定了配置文件，TiDB 会首先读取配置文件的配置。如果对应的配置在命令行参数里面也存在，TiDB 就会使用命令行参数的配置来覆盖配置文件中的配置。详细的配置项请参阅 [TiDB 配置文件描述](/tidb-configuration-file.md)。

## `--config-check`

- 检查配置文件的有效性并退出
- 默认：false

## `--config-strict`

- 增强配置文件的有效性
- 默认：false

## `--cors`

+ 用于设置 TiDB HTTP 状态服务的 Access-Control-Allow-Origin
+ 默认：""

## `--host`

+ TiDB 服务监听的 host
+ 默认："0.0.0.0"
+ 0.0.0.0 默认会监听所有的网卡地址。如果有多块网卡，可以指定对外提供服务的网卡，如 192.168.100.113

## `--initialize-insecure`

- 在不安全模式下启动 tidb-server
- 默认：true

## `--initialize-secure`

- 控制在 tidb-server 初始化过程中是否使用 `auth_socket` 认证方式创建 `root` 账户。如果设置为 `true`，首次连接 TiDB 时必须使用 socket 连接，这样安全性更高。
- 默认：false

## `--initialize-sql-file`

- 用于指定 TiDB 集群初次启动时执行的 SQL 脚本。参考[配置项 `initialize-sql-file`](/tidb-configuration-file.md#initialize-sql-file-从-v660-版本开始引入)
- 默认：""

## `-L`

+ Log 级别
+ 默认："info"
+ 可选："debug"，"info"，"warn"，"error"，"fatal"

## `--lease`

- Schema lease 的持续时间。除非你知道更改该值带来的后果，否则你的更改操作是**危险的**。
- 默认：45s

## `--log-file`

+ Log 文件
+ 默认：""
+ 如果未设置该参数，log 会默认输出到 "stderr"；如果设置了该参数，log 会输出到对应的文件中。

## `--log-general`

+ [General Log](/system-variables.md#tidb_general_log) 文件名
+ 默认：""
+ 如果未设置该参数，general log 会默认输出到 [`--log-file`](#--log-file) 指定的文件中。

## `--log-slow-query`

+ 慢查询日志文件路径
+ 默认：""
+ 如果未设置该参数，log 会默认输出到 `--log-file` 指定的文件中

## `--metrics-addr`

+ Prometheus Pushgateway 地址
+ 默认：""
+ 如果该参数为空，TiDB 不会将统计信息推送给 Pushgateway。参数格式示例：`--metrics-addr=192.168.100.115:9091`

## `--metrics-interval`

+ 推送统计信息到 Prometheus Pushgateway 的时间间隔
+ 默认：15s
+ 设置为 0 表示不推送统计信息给 Pushgateway。示例：`--metrics-interval=2` 指每两秒推送到 Pushgateway

## `-P`

+ TiDB 服务监听端口
+ 默认："4000"
+ TiDB 服务会使用该端口接受 MySQL 客户端发来的请求

## `--path`

+ 对于本地存储引擎 "unistore" 来说，path 指定的是实际的数据存放路径
+ 当 `--store = tikv` 时，必须指定 path；当 `--store = unistore` 时，如果不指定 path，会使用默认值。
+ 对于 "TiKV" 存储引擎来说，path 指定的是实际的 PD 地址。假如在 192.168.100.113:2379、192.168.100.114:2379 和 192.168.100.115:2379 上面部署了 PD，那么 path 为 "192.168.100.113:2379, 192.168.100.114:2379, 192.168.100.115:2379"
+ 默认："/tmp/tidb"
+ 可以通过 `tidb-server --store=unistore --path=""` 来启动一个纯内存引擎的 TiDB

## `--proxy-protocol-networks`

+ 允许使用 [PROXY 协议](https://www.haproxy.org/download/1.8/doc/proxy-protocol.txt)连接 TiDB 的代理服务器地址列表。
+ 默认：""
+ 通常情况下，通过反向代理使用 TiDB 时，TiDB 会将反向代理服务器的 IP 地址视为客户端 IP 地址。对于支持 [PROXY 协议](https://www.haproxy.org/download/1.8/doc/proxy-protocol.txt)的反向代理（如 HAProxy），开启 PROXY 协议后能让反向代理透传客户端真实的 IP 地址给 TiDB。
+ 配置该参数后，TiDB 将允许配置的源 IP 地址使用 PROXY 协议连接到 TiDB，且拒绝这些源 IP 地址使用非 PROXY 协议连接。其他地址可以使用非 PROXY 协议连接到 TiDB。若该参数为空，则任何源 IP 地址都不能使用 PROXY 协议连接到 TiDB。地址可以使用 IP 地址格式 (192.168.1.50) 或者 CIDR 格式 (192.168.1.0/24)，并可用 `,` 分隔多个地址，或用 `*` 代表所有 IP 地址。

> **警告：**
>
> 需谨慎使用 `*` 符号，因为它可能引入安全风险，允许来自任何 IP 的客户端自行汇报其 IP 地址。另外，当 [`--proxy-protocol-fallbackable`](#--proxy-protocol-fallbackable) 设置为 `true` 以外的值时，使用 `*` 可能会导致部分直接连接 TiDB 的内部组件无法使用，例如 TiDB Dashboard。

> **注意：**
>
> 如果使用 AWS 的 Network Load Balancer (NLB) 并开启 PROXY 协议，需要设置 NLB 的 `target group` 属性：将 `proxy_protocol_v2.client_to_server.header_place` 设为 `on_first_ack`。同时向 AWS 的 Support 提工单开通此功能的支持。注意，AWS NLB 在开启 PROXY 协议后，客户端将无法获取服务器端的握手报文，因此报文会一直阻塞到客户端超时。这是因为，NLB 默认只在客户端发送数据之后才会发送 PROXY 的报文，而在客户端发送数据包之前，服务器端发送的任何数据包都会在内网被丢弃。

## `--proxy-protocol-fallbackable`

+ 用于控制是否启用 PROXY 协议回退模式。如果设置为 `true`，TiDB 可以接受属于 `--proxy-protocol-networks` 的客户端使用非 PROXY 协议规范或者没有发送 PROXY 协议头的客户端连接。默认情况下，TiDB 仅接受属于 `--proxy-protocol-networks` 的客户端发送 PROXY 协议头的客户端连接。
+ 默认：`false`

## `--proxy-protocol-header-timeout`

+ PROXY 协议请求头读取超时时间
+ 默认：5
+ 单位：秒

> **警告：**
>
> 自 v6.3.0 起，该参数被废弃。因为自 v6.3.0 起，读取 PROXY 协议报头的操作会在第一次读取网络数据时进行，废弃该参数可避免影响首次读取网络数据时设置的超时时间。

> **注意：**
>
> 不要将该参数配置为 `0`。除非特殊情况，一般使用默认值即可。

## `--report-status`

+ 用于打开或者关闭服务状态监听端口
+ 默认：true
+ 将参数值设置为 `true` 表明开启状态监听端口；设置为 `false` 表明关闭状态监听端口

## `--run-ddl`

+ tidb-server 是否运行 DDL 语句，集群内至少需要有一台 tidb-server 设置该参数
+ 默认：true
+ 值可以为 `true` 或者 `false`。设置为 `true` 表明自身会运行 DDL；设置为 `false` 表明自身不会运行 DDL

## `--socket string`

+ TiDB 服务使用 unix socket file 方式接受外部连接
+ 默认：""
+ 例如可以使用 "/tmp/tidb.sock" 来打开 unix socket file

## `--status`

+ TiDB 服务状态监听端口
+ 默认："10080"
+ 该端口用于展示 TiDB 内部数据，包括 [prometheus 统计](https://prometheus.io/)和 [pprof](https://golang.org/pkg/net/http/pprof/)
+ Prometheus 统计可以通过 `http://host:status_port/metrics` 访问
+ pprof 数据可以通过 `http://host:status_port/debug/pprof` 访问

## `--status-host`

+ TiDB 服务状态监听 host
+ 默认："0.0.0.0"

## `--store`

+ 用来指定 TiDB 底层使用的存储引擎
+ 默认："unistore"
+ 可以选择 "unistore"（本地存储引擎）或者 "tikv"（分布式存储引擎）

## `--temp-dir`

- TiDB 用于存放临时文件的目录
- 默认："/tmp/tidb"

## `--tidb-service-scope`

+ 用于设置当前 TiDB 实例 [`tidb_service_scope`](/system-variables.md#tidb_service_scope-从-v740-版本开始引入) 的初始值。
+ 默认：`""`

## `--token-limit`

+ TiDB 中同时允许运行的 Session 数量，用于流量控制
+ 默认：1000
+ 如果当前运行的连接多于该 token-limit，那么请求会阻塞，等待已经完成的操作释放 Token

## `-V`

+ 输出 TiDB 的版本
+ 默认：""

## `--plugin-dir`

+ plugin 存放目录
+ 默认："/data/deploy/plugin"

## `--plugin-load`

+ 需要加载的 plugin 名称，多个 plugin 以 "," 逗号分隔
+ 默认：""

## `--affinity-cpus`

+ 设置 TiDB server CPU 亲和性，以 "," 逗号分隔，例如 "1,2,3"
+ 默认：""

## `--redact`

+ 设置 TiDB server 是否在使用子命令 `collect-log` 时脱敏日志文件。
+ 默认：false
+ 取值为 `true` 时为脱敏操作，所有被标记符号 `‹ ›` 包裹的字段会被替换为 `?`。取值为 `false` 时为还原操作，所有标记符号会被去除。具体使用方法为：执行 `./tidb-server --redact=xxx collect-log <input> <output>` 将 `<input>` 指向的 TiDB server 日志文件进行脱敏或者还原，并输出到 `<output>`。更多详情，请参考系统变量 [`tidb_redact_log`](/system-variables.md#tidb_redact_log)。

## `--repair-mode`

+ 是否开启修复模式，仅用于数据修复场景
+ 默认：false

## `--repair-list`

+ 修复模式下需要修复的表名
+ 默认：""