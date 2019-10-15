---
title: TiDB 命令行参数
category: reference
aliases: ['/docs-cn/op-guide/configuration/','/docs-cn/sql/server-command-option/','/docs-cn/sql/tidb-server/']
---

# TiDB 命令行参数

在启动 TiDB 时，你可以使用命令行参数或环境变量来配置 TiDB。本文将详细介绍 TiDB 的命令行启动参数。TiDB 的默认端口为 4000（客户端请求）与 10080（状态报告）。

## `--advertise-address`

+ 登录 TiDB 的 IP 地址
+ 默认：""
+ 必须确保用户和集群中的其他机器都能够访问到该 IP 地址

## `--binlog-socket`

+ TiDB 服务使用 unix socket file 方式接受内部连接，如 Pump 服务
+ 默认：""
+ 例如，可以使用 "/tmp/pump.sock" 来接受 Pump unix socket file 通信

## `--config`

+ 配置文件
+ 默认：""
+ 如果你指定了配置文件，TiDB 会首先读取配置文件的配置。如果对应的配置在命令行参数里面也存在，TiDB 就会使用命令行参数的配置来覆盖配置文件中的配置。详细的配置项请参阅 [TiDB 配置文件描述](/v3.0/reference/configuration/tidb-server/configuration-file.md)。

## `--cors`

+ 用于设置 TiDB HTTP 状态服务的 Access-Control-Allow-Origin
+ 默认：""

## `--host`

+ TiDB 服务监听的 host
+ 默认："0.0.0.0"
+ 0.0.0.0 默认会监听所有的网卡地址。如果有多块网卡，可以指定对外提供服务的网卡，如 192.168.100.113

## `-L`

+ Log 级别
+ 默认："info"
+ 可选项为：debug、info、warn、error、fatal

## `--log-file`

+ Log 文件
+ 默认：""
+ 如果未设置该参数，log 会默认输出到 "stderr"；如果设置了该参数，log 会输出到对应的文件中。每天凌晨，log 会自动轮转使用一个新的文件，并且将以前的文件改名备份

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

+ 对于本地存储引擎 "mocktikv" 来说，path 指定的是实际的数据存放路径
+ 当 `--store = tikv` 时，必须指定 path；当 `--store = mocktikv` 时，如果不指定 path，会使用默认值。
+ 对于 "TiKV" 存储引擎来说，path 指定的是实际的 PD 地址。假如在 192.168.100.113:2379、192.168.100.114:2379 和 192.168.100.115:2379 上面部署了 PD，那么 path 为 "192.168.100.113:2379, 192.168.100.114:2379, 192.168.100.115:2379"
+ 默认："/tmp/tidb"
+ 可以通过 `tidb-server --store=mocktikv --path=""` 来启动一个纯内存引擎的 TiDB

## `--proxy-protocol-networks`

+ PROXY Protocol 允许的代理服务器地址列表。如需配置多个地址，用 `,` 分隔。
+ 默认：""
+ 如果该参数为空，TiDB 会禁用 PROXY Protocol 功能。地址可以使用 IP 地址 (192.168.1.50) 或者 CIDR (192.168.1.0/24)，`*` 代表所有地址。

## `--proxy-protocol-header-timeout`

+ PROXY Protocol 请求头读取超时时间
+ 默认：5
+ 单位：秒

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
+ 该端口用于展示 TiDB 内部数据，包括 [prometheus 统计](https://prometheus.io/) 和 [pprof](https://golang.org/pkg/net/http/pprof/)
+ Prometheus 统计可以通过 `http://host:status_port/metrics` 访问
+ pprof 数据可以通过 `http://host:status_port/debug/pprof` 访问

## `--status-host`

+ TiDB 服务状态监听 host
+ 默认："0.0.0.0"

## `--store`

+ 用来指定 TiDB 底层使用的存储引擎
+ 默认："mocktikv"
+ 可以选择 "mocktikv"（本地存储引擎）或者 "tikv"（分布式存储引擎）

## `--token-limit`

+ TiDB 中同时允许运行的 Session 数量，用于流量控制
+ 默认：1000
+ 如果当前运行的连接多于该 token-limit，那么请求会阻塞，等待已经完成的操作释放 Token

## `-V`

+ 输出 TiDB 的版本
+ 默认：""
