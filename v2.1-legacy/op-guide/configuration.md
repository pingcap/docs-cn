---
title: 参数解释
category: deployment
---

# 参数解释

## TiDB

### `-V`

+ 输出 TiDB 的版本
+ 默认: ""

### `--config`

+ 配置文件
+ 默认: ""
+ 如果你指定了配置文件，TiDB 会首先读取配置文件的配置。然后如果对应的配置在命令行参数里面也存在，TiDB 就会使用命令行参数的配置来覆盖配置文件里面的。详细的配置项可以看看[这里](../op-guide/tidb-config-file.md)

### `--store`

+ 用来指定 TiDB 底层使用的存储引擎
+ 默认: "mocktikv"
+ 你可以选择 "mocktikv" 或者 "tikv"。（mocktikv 是本地存储引擎，而 tikv 是一个分布式存储引擎）

### `--path`

+ 对于本地存储引擎 "mocktikv" 来说，path 指定的是实际的数据存放路径
+ 对于 `--store = tikv` 时必须指定path，`--store = mocktikv` 时，如果不指定 path，会使用默认值。
+ 对于 "TiKV" 存储引擎来说，path 指定的是实际的 PD 地址。假设我们在 192.168.100.113:2379, 192.168.100.114:2379 和 192.168.100.115:2379 上面部署了 PD，那么 path 为 "192.168.100.113:2379, 192.168.100.114:2379, 192.168.100.115:2379"
+ 默认: "/tmp/tidb"
+ 我们可以通过 `tidb-server --store=mocktikv --path=""` 来启动一个纯内存引擎的 TiDB。

### `--advertise-address`

+ 登录 TiDB 的 IP 地址
+ 默认: ""
+ 这个 IP 地址必须确保用户和集群中的其他机器都能够访问到。

### `--host`

+ TiDB 服务监听 host
+ 默认: "0.0.0.0"
+ TiDB 服务会监听这个 host
+ 0.0.0.0 默认会监听所有的网卡 address。如果有多块网卡，可以指定对外提供服务的网卡，譬如192.168.100.113

### `-P`

+ TiDB 服务监听端口
+ 默认: "4000"
+ TiDB 服务将会使用这个端口接受 MySQL 客户端发过来的请求

### `--socket string`

+ TiDB 服务使用 unix socket file 方式接受外部连接
+ 默认: ""
+ 譬如我们可以使用 "/tmp/tidb.sock" 来打开 unix socket file

### `--binlog-socket`

+ TiDB 服务使用 unix socket file 方式接受内部连接，如 PUMP 服务
+ 默认: ""
+ 譬如我们可以使用 "/tmp/pump.sock" 来接受 PUMP unix socket file 通信

### `--run-ddl`

+ tidb-server 是否运行 DDL 语句，集群内大于两台以上 tidb-server 时设置
+ 默认: true
+ 值可以为 (true) 或者 (false). (true) 表明自身会运行 DDL. (false) 表明自身不会运行 DDL

### `-L`

+ Log 级别
+ 默认: "info"
+ 我们能选择 debug, info, warn, error 或者 fatal

### `--log-file`

+ Log 文件
+ 默认: ""
+ 如果没设置这个参数，log 会默认输出到 "stderr"，如果设置了，log 就会输出到对应的文件里面，在每天凌晨，log 会自动轮转使用一个新的文件，并且将以前的文件改名备份

### `--log-slow-query`

+ 慢查询日志文件路径
+ 默认: ""
+ 如果没有设置这个参数，log 会默认输出到 `--log-file` 指定的文件中。

### `--report-status`

+ 打开 (true) 或者关闭 (false) 服务状态监听端口
+ 默认: true
+ 值可以为 (true) 或者 (false). (true) 表明我们开启状态监听端口。 (false) 表明关闭

### `--status`

+ TiDB 服务状态监听端口
+ 默认: "10080"
+ 这个端口是为了展示 TiDB 内部数据用的。包括 [prometheus 统计](https://prometheus.io/) 以及 [pprof](https://golang.org/pkg/net/http/pprof/)
+ Prometheus 统计可以通过 "http://host:status_port/metrics" 访问
+ Pprof 数据可以通过 "http://host:status_port/debug/pprof" 访问

### `--metrics-addr`

+ Prometheus Pushgateway 地址
+ 默认: ""
+ 如果为空，TiDB 不会将统计信息推送给 Pushgateway,参数格式 如 `--metrics-addr=192.168.100.115:9091`

### `--metrics-interval`

+ 推送统计信息到 Prometheus Pushgateway 的时间间隔
+ 默认: 15s
+ 设置为 0 表明不推送统计信息给 Pushgateway,如: `--metrics-interval=2` 是每两秒推送到 Pushgateway

### `--token-limit`

+ TiDB 中同时允许运行的 Session 数量，用于流量控制。
+ 默认: 1000
+ 如果当前运行的连接多余这个 token-limit，那么请求会阻塞等待已经完成的操作释放 Token。

### `--proxy-protocol-networks`

+ PROXY Protocol 允许的代理服务器地址列表，如果需要配置多个地址用`,`分隔。
+ 默认: ""
+ 如果为空，TiDB 会禁用 PROXY Protocol 功能。地址可以使用 IP 地址（192.168.1.50）或者 CIDR （192.168.1.0/24），`*` 代表所有地址。

### `--proxy-protocol-header-timeout`

+ PROXY Protocol 请求头读取超时时间。
+ 默认: 5
+ 单位为秒。

> **注意：**
>
> 请不要配置成0，除非特殊情况，一般使用默认值即可。

## Placement Driver (PD)

### `--advertise-client-urls`

+ 对外客户端访问 URL 列表
+ 默认: ${client-urls}
+ 在某些情况下，譬如 docker，或者 NAT 网络环境，客户端并不能通过 PD 自己监听的 client URLs 来访问到 PD，这时候，你就可以设置 advertise urls 来让客户端访问
+ 例如，docker 内部 IP 地址为 172.17.0.1，而宿主机的 IP 地址为 192.168.100.113 并且设置了端口映射 -p 2379:2379，那么可以设置为 \-\-advertise-client-urls="http://192.168.100.113:2379"，客户端可以通过 http://192.168.100.113:2379 来找到这个服务

### `--advertise-peer-urls`

+ 对外其他 PD 节点访问 URL 列表。
+ 默认: ${peer-urls}
+ 在某些情况下，譬如 docker，或者 NAT 网络环境，其他节点并不能通过 PD 自己监听的 peer URLs 来访问到 PD，这时候，你就可以设置 advertise urls 来让其他节点访问
+ 例如，docker 内部 IP 地址为 172.17.0.1，而宿主机的 IP 地址为 192.168.100.113 并且设置了端口映射 -p 2380:2380，那么可以设置为 \-\-advertise-peer-urls="http://192.168.100.113:2380"，其他 PD 节点可以通过 http://192.168.100.113:2380 来找到这个服务

### `--client-urls`

+ 处理客户端请求监听 URL 列表
+ 默认: "http://127.0.0.1:2379"
+ 如果部署一个集群，\-\-client-urls 必须指定当前主机的 IP 地址，例如 "http://192.168.100.113:2379"，如果是运行在 docker 则需要指定为 "http://0.0.0.0:2379"

### `--peer-urls`

+ 处理其他 PD 节点请求监听 URL 列表。
+ default: "http://127.0.0.1:2380"
+ 如果部署一个集群，\-\-peer-urls 必须指定当前主机的 IP 地址，例如 "http://192.168.100.113:2380"，如果是运行在 docker 则需要指定为 "http://0.0.0.0:2380"

### `--config`

+ 配置文件
+ 默认: ""
+ 如果你指定了配置文件，PD 会首先读取配置文件的配置。然后如果对应的配置在命令行参数里面也存在，PD 就会使用命令行参数的配置来覆盖配置文件里面的

### `--data-dir`

+ PD 存储数据路径
+ 默认: "default.${name}"

### `--initial-cluster`

+ 初始化 PD 集群配置。
+ 默认: "{name}=http://{advertise-peer-url}"
+ 例如，如果 name 是 "pd", 并且 `advertise-peer-urls` 是 "http://192.168.100.113:2380", 那么 `initial-cluster` 就是 pd=http://192.168.100.113:2380
+ 如果你需要启动三台 PD，那么 `initial-cluster` 可能就是
  `pd1=http://192.168.100.113:2380, pd2=http://192.168.100.114:2380, pd3=192.168.100.115:2380`

### `--join`

+ 动态加入 PD 集群
+ 默认: ""
+ 如果你想动态将一台 PD 加入集群，你可以使用 `--join="${advertise-client-urls}"`， `advertise-client-url` 是当前集群里面任意 PD 的 `advertise-client-url`，你也可以使用多个 PD 的，需要用逗号分隔

### `-L`

+ Log 级别
+ 默认: "info"
+ 我们能选择 debug, info, warn, error 或者 fatal

### `--log-file`

+ Log 文件
+ 默认: ""
+ 如果没设置这个参数，log 会默认输出到 "stderr"，如果设置了，log 就会输出到对应的文件里面，在每天凌晨，log 会自动轮转使用一个新的文件，并且将以前的文件改名备份

### `--log-rotate`

+ 是否开启日志切割
+ 默认：true
+ 当值为 true 时,按照 PD 配置文件中 `[log.file]` 信息执行。

### `--name`

+ 当前 PD 的名字
+ 默认: "pd"
+ 如果你需要启动多个 PD，一定要给 PD 使用不同的名字

### `--cacert`

+ CA 文件路径，用于开启 TLS。
+ 默认: ""

### `--cert`

+ 包含 X509 证书的 PEM 文件路径，用户开启 TLS。
+ 默认: ""

### `--key`

+ 包含 X509 key 的 PEM 文件路径，用于开启 TLS。
+ 默认: ""

### `--namespace-classifier`

+ 指定 PD 使用的 namespace 分类器。
+ 默认: "table"
+ 如果 TiKV 不与 TiDB 集群配合运行，建议配置为 'default'。

## TiKV

TiKV 在命令行参数上面支持一些可读性好的单位转换。

+ 文件大小（以 bytes 为单位）: KB, MB, GB, TB, PB（也可以全小写）
+ 时间（以毫秒为单位）: ms, s, m, h

### `-A, --addr`

+ TiKV 监听地址
+ 默认: "127.0.0.1:20160"
+ 如果部署一个集群，\-\-addr 必须指定当前主机的 IP 地址，例如 "192.168.100.113:20160"，如果是运行在 docker 则需要指定为 "0.0.0.0:20160"

### `--advertise-addr`

+ TiKV 对外访问地址。
+ 默认: ${addr}
+ 在某些情况下，譬如 docker，或者 NAT 网络环境，客户端并不能通过  TiKV 自己监听的地址来访问到 TiKV，这时候，你就可以设置 advertise addr 来让 客户端访问
+ 例如，docker 内部 IP 地址为 172.17.0.1，而宿主机的 IP 地址为 192.168.100.113 并且设置了端口映射 -p 20160:20160，那么可以设置为 \-\-advertise-addr="192.168.100.113:20160"，客户端可以通过 192.168.100.113:20160 来找到这个服务

### `-C, --config`

+ 配置文件
+ 默认: ""
+ 如果你指定了配置文件，TiKV 会首先读取配置文件的配置。然后如果对应的配置在命令行参数里面也存在，TiKV 就会使用命令行参数的配置来覆盖配置文件里面的

### `--capacity`

+ TiKV 存储数据的容量
+ 默认: 0 (无限)
+ PD 需要使用这个值来对整个集群做 balance 操作。（提示：你可以使用 10GB 来替代 10737418240，从而简化参数的传递）

### `--data-dir`

+ TiKV 数据存储路径
+ 默认: "/tmp/tikv/store"

### `-L, --log`

+ Log 级别
+ 默认: "info"
+ 我们能选择 trace, debug, info, warn, error, 或者 off

### `--log-file`

+ Log 文件
+ 默认: ""
+ 如果没设置这个参数，log 会默认输出到 "stderr"，如果设置了，log 就会输出到对应的文件里面，在每天凌晨，log 会自动轮转使用一个新的文件，并且将以前的文件改名备份

### `--pd`

+ PD 地址列表。
+ 默认: ""
+ TiKV 必须使用这个值连接 PD，才能正常工作。使用逗号来分隔多个 PD 地址，例如：
  192.168.100.113:2379, 192.168.100.114:2379, 192.168.100.115:2379
