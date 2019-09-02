---
title: TiDB 配置参数
category: reference
---

# TiDB 配置参数

TiDB 通过命令行参数或环境变量配置。默认的 TiDB 端口为 4000（客户端请求）与 10080（状态报告）。

## `-V`

+ 输出 TiDB 的版本
+ 默认：""

## `--config`

+ 配置文件
+ 默认：""
+ 如果你指定了配置文件，TiDB 会首先读取配置文件的配置。然后如果对应的配置在命令行参数里面也存在，TiDB 就会使用命令行参数的配置来覆盖配置文件里面的。详细的配置项请参阅 [TiDB 配置文件描述](v2.1/reference/configuration/tidb-server/configuration-file.md)。

## `--store`

+ 用来指定 TiDB 底层使用的存储引擎
+ 默认："mocktikv"
+ 你可以选择 "mocktikv" 或者 "tikv"。（mocktikv 是本地存储引擎，而 tikv 是一个分布式存储引擎）

## `--path`

+ 对于本地存储引擎 "mocktikv" 来说，path 指定的是实际的数据存放路径
+ 对于 `--store = tikv` 时必须指定path，`--store = mocktikv` 时，如果不指定 path，会使用默认值。
+ 对于 "TiKV" 存储引擎来说，path 指定的是实际的 PD 地址。假设我们在 192.168.100.113:2379, 192.168.100.114:2379 和 192.168.100.115:2379 上面部署了 PD，那么 path 为 "192.168.100.113:2379, 192.168.100.114:2379, 192.168.100.115:2379"
+ 默认："/tmp/tidb"
+ 我们可以通过 `tidb-server --store=mocktikv --path=""` 来启动一个纯内存引擎的 TiDB。

## `--advertise-address`

+ 登录 TiDB 的 IP 地址
+ 默认：""
+ 这个 IP 地址必须确保用户和集群中的其他机器都能够访问到。

## `--host`

+ TiDB 服务监听 host
+ 默认："0.0.0.0"
+ TiDB 服务会监听这个 host
+ 0.0.0.0 默认会监听所有的网卡 address。如果有多块网卡，可以指定对外提供服务的网卡，譬如192.168.100.113

## `-P`

+ TiDB 服务监听端口
+ 默认："4000"
+ TiDB 服务将会使用这个端口接受 MySQL 客户端发过来的请求

## `--socket string`

+ TiDB 服务使用 unix socket file 方式接受外部连接
+ 默认：""
+ 譬如我们可以使用 "/tmp/tidb.sock" 来打开 unix socket file

## `--binlog-socket`

+ TiDB 服务使用 unix socket file 方式接受内部连接，如 PUMP 服务
+ 默认：""
+ 譬如我们可以使用 "/tmp/pump.sock" 来接受 PUMP unix socket file 通信

## `--run-ddl`

+ tidb-server 是否运行 DDL 语句，集群内大于两台以上 tidb-server 时设置
+ 默认：true
+ 值可以为 (true) 或者 (false). (true) 表明自身会运行 DDL. (false) 表明自身不会运行 DDL

## `-L`

+ Log 级别
+ 默认："info"
+ 我们能选择 debug, info, warn, error 或者 fatal

## `--log-file`

+ Log 文件
+ 默认：""
+ 如果没设置这个参数，log 会默认输出到 "stderr"，如果设置了，log 就会输出到对应的文件里面，在每天凌晨，log 会自动轮转使用一个新的文件，并且将以前的文件改名备份

## `--log-slow-query`

+ 慢查询日志文件路径
+ 默认：""
+ 如果没有设置这个参数，log 会默认输出到 `--log-file` 指定的文件中。

## `--report-status`

+ 打开 (true) 或者关闭 (false) 服务状态监听端口
+ 默认：true
+ 值可以为 (true) 或者 (false). (true) 表明我们开启状态监听端口。 (false) 表明关闭

## `--status`

+ TiDB 服务状态监听端口
+ 默认："10080"
+ 这个端口是为了展示 TiDB 内部数据用的。包括 [prometheus 统计](https://prometheus.io/) 以及 [pprof](https://golang.org/pkg/net/http/pprof/)
+ Prometheus 统计可以通过 `http://host:status_port/metrics` 访问
+ Pprof 数据可以通过 `http://host:status_port/debug/pprof` 访问

## `--metrics-addr`

+ Prometheus Pushgateway 地址
+ 默认：""
+ 如果为空，TiDB 不会将统计信息推送给 Pushgateway,参数格式 如 `--metrics-addr=192.168.100.115:9091`

## `--metrics-interval`

+ 推送统计信息到 Prometheus Pushgateway 的时间间隔
+ 默认：15s
+ 设置为 0 表明不推送统计信息给 Pushgateway,如: `--metrics-interval=2` 是每两秒推送到 Pushgateway

## `--token-limit`

+ TiDB 中同时允许运行的 Session 数量，用于流量控制。
+ 默认：1000
+ 如果当前运行的连接多余这个 token-limit，那么请求会阻塞等待已经完成的操作释放 Token。

## `--proxy-protocol-networks`

+ PROXY Protocol 允许的代理服务器地址列表，如果需要配置多个地址用`,`分隔。
+ 默认：""
+ 如果为空，TiDB 会禁用 PROXY Protocol 功能。地址可以使用 IP 地址（192.168.1.50）或者 CIDR （192.168.1.0/24），`*` 代表所有地址。

## `--proxy-protocol-header-timeout`

+ PROXY Protocol 请求头读取超时时间。
+ 默认：5
+ 单位：秒。

> **注意：**
>
> 请不要配置成 0，除非特殊情况，一般使用默认值即可。
