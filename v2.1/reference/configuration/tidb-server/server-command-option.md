---
title: TiDB 进程启动参数
category: user guide
---

## TiDB 进程启动参数

启动 TiDB 进程时，可以指定一些程序启动参数。

TiDB 接受许多的启动参数，执行这个命令可以得到一个简要的说明：

```
./tidb-server --help
```

获取版本信息可以使用下面命令：

```
./tidb-server -V
```

以下是启动参数的完整描述。

### -L

+ Log 级别
+ 默认: "info"
+ 可选值包括 debug, info, warn, error 或者 fatal

### -P

+ TiDB 服务监听端口
+ 默认: "4000"
+ TiDB 服务将会使用这个端口接受 MySQL 客户端发过来的请求

### \-\-binlog-socket

+ TiDB 服务使用 unix socket file 方式接受内部连接，如 PUMP 服务
+ 默认: ""
+ 譬如使用 "/tmp/pump.sock" 来接受 PUMP unix socket file 通信

### \-\-config

+ TiDB 配置文件
+ 默认: ""
+ 配置文件的路径

### \-\-lease

+ Schema 的租约时间，单位：秒
+ 默认: "10"
+ Schema 的 lease 主要用在 online schema changes 上面。这个值会影响到实际的 DDL 语句的执行时间。大多数情况下，用户不需要修改这个值，除非您清晰的了解 TiDB DDL 的内部实现机制

### \-\-host

+ TiDB 服务监听 host
+ 默认: "0.0.0.0"
+ TiDB 服务会监听这个 host
+ 0.0.0.0 默认会监听所有的网卡 address。如果有多块网卡，可以指定对外提供服务的网卡，譬如 192.168.100.113

### \-\-log-file

+ Log 文件
+ 默认: ""
+ 如果没设置这个参数，log 会默认输出到 "stderr"，如果设置了， log 就会输出到对应的文件里面，在每天凌晨，log 会自动轮转使用一个新的文件，并且将以前的文件改名备份

### \-\-metrics-addr

+ Prometheus Push Gateway 地址
+ 默认: ""
+ 如果为空，TiDB 不会将统计信息推送给 Push Gateway ，参数格式 如 `--metrics-addr=192.168.100.115:9091`

### \-\-metrics-interval

+ 推送统计信息到 Prometheus Push Gateway 的时间间隔
+ 默认: 15s
+ 设置为 0 表明不推送统计信息给 Push Gateway ，如: `--metrics-interval=2` 是每两秒推送到 Pushgateway

### \-\-path

+ 对于本地存储引擎 "goleveldb", "BoltDB" 来说，path 指定的是实际的数据存放路径
+ 对于 "memory" 存储引擎来说，path 不用设置
+ 对于 "TiKV" 存储引擎来说，path 指定的是实际的 PD 地址。例如 PD 部署在 192.168.100.113:2379, 192.168.100.114:2379 和 192.168.100.115:2379 上面，那么 path 为 "192.168.100.113:2379, 192.168.100.114:2379, 192.168.100.115:2379"
+ 默认: "/tmp/tidb"

### \-\-report-status

+ 打开 (true) 或者关闭 (false) 服务状态监听端口
+ 默认: true
+ 值可以为 (true) 或者 (false). (true) 表明开启状态监听端口。 (false) 表明关闭。状态监听端口用于通过 HTTP 方式对外报告一些服务内部信息

### \-\-run-ddl

+ tidb-server 是否运行 DDL 语句，集群内大于两台以上 tidb-server 时设置
+ 默认: true
+ 值可以为 (true) 或者 (false). (true) 表明自身会运行 DDL. (false) 表明自身不会运行 DDL

### \-\-socket string

+ TiDB 服务使用 unix socket file 方式接受外部连接
+ 默认: ""
+ 譬如可以使用 "/tmp/tidb.sock" 来打开 unix socket file

### \-\-status

+ TiDB 服务状态监听端口
+ 默认: "10080"
+ 这个端口是为了展示 TiDB 内部数据用的。包括 [prometheus 统计](https://prometheus.io/) 以及 [pprof](https://golang.org/pkg/net/http/pprof/)
+ Prometheus 统计可以通过 `http://host:status_port/metrics` 访问
+ Pprof 数据可以通过 `http://host:status_port/debug/pprof` 访问

### \-\-store

+ 用来指定 TiDB 底层使用的存储引擎
+ 默认: "mocktikv"
+ 可选值包括 "memory", "goleveldb", "boltdb", "mocktikv" 或者 "tikv"。（前面都是本地存储引擎，而 TiKV 是一个分布式存储引擎）
+ 例如，通过 `tidb-server --store=memory` 来启动一个纯内存引擎的 TiDB

## TiDB 服务器配置文件

启动 TiDB 服务器时，通过 `--config path` 可以指定服务器的配置文件。对于配置中重叠的选项，命令行启动参数的优先级高于配置文件。

配置文件的示例参见 <https://github.com/pingcap/tidb/blob/master/config/config.toml.example>。

以下是启动参数的完整描述。

### host

同启动参数 host

### port

同启动参数 P

### path

同启动参数 path

### socket

同启动参数 socket

### binlog-socket

同启动参数 binlog-socket

### run-ddl

同启动参数 run-ddl

### cross-join

+ 默认: true
+ 在做 join 的时候，两边表没有任何条件（where 字段），默认可以执行这样的语句。但是设置为 false，则如有这样的 join 语句出现，server 会拒绝执行

### force-priority

- 语句的默认优先级
- 默认: `NO_PRIORITY`
- TiDB 支持的语句优先级包括：`NO_PRIORITY`、`LOW_PRIORITY`、`DELAYED` 以及 `HIGH_PRIORITY`。例如，如果你需要为 OLAP 查询指定专属服务器池，可将该值设置为 `LOW_PRIORITY`，以保证 TiKV 服务器优先处理其他 TiDB 服务器池收到的 OLTP 请求。这样可以使 OLTP 性能更稳定，但 OLAP 性能可能会稍有下降
- TiDB 自动将 table scan 设置为 `LOW_PRIORITY`，通过将 [DML modifier](../sql/dml.md) 设置为 `HIGH PRIORITY` 或 `LOW PRIORITY`，可重写一条语句的优先级

### join-concurrency

+ join-concurrency 并发执行 join 的 goroutine 数量
+ 默认: 5
+ 看数据量和数据分布情况，一般情况下是越多越好，数值越大对 CPU 开销越大

### query-log-max-len

+ 日志中记录最大 sql 语句长度
+ 默认: 2048
+ 过长的请求输出到 log 时会被截断

### slow-threshold int

+ 大于这个值得 sql 语句将被记录
+ 默认: 300
+ 值只能是一个整数 (int) ，单位是毫秒

### slow-query-file

+ 慢查询日志文件
+ 默认: ""
+ 值是文件名，若指定了一个非空字符串，则慢查询日志会被重定向到相应的文件

### retry-limit

+ 事务遇见冲突时，提交事物最大重试次数
+ 默认: 10
+ 设置较大的重试次数会影响 TiDB 集群性能

### skip-grant-table

+ 允许任何人不带密码连接，并且所有的操作不检查权限
+ 默认: false
+ 值可以是(true) or (false)。启用此选项需要本机的 root 权限，一般用于忘记密码时重置

### stats-lease

+ 增量扫描全表并分析表的数据量 索引等一些信息
+ 默认: "3s"
+ 使用此参数需要先手动执行 analyze table name; 自动更新统计信息,持久化存储到 TiKV，会耗费一些内存开销,

### tcp-keep-alive

+ TiDB 在 tcp 层开启 keepalive
+ 默认: false

### ssl-cert

+ PEM 格式的 SSL 证书文件路径
+ 默认: ""
+ 当同时设置了该选项和 `--ssl-key` 选项时，TiDB 将接受（但不强制）客户端使用 TLS 安全地连接到 TiDB。
+ 若指定的证书或私钥无效，则 TiDB 会照常启动，但无法接受安全连接。

### ssl-key

+ PEM 格式的 SSL 证书密钥文件路径，即 `--ssl-cert` 所指定的证书的私钥
+ 默认: ""
+ 目前 TiDB 不支持加载由密码保护的私钥。

### ssl-ca

+ PEM 格式的受信任 CA 的证书文件路径
+ 默认: ""
+ 当同时设置了该选项和 `--ssl-cert`、`--ssl-key` 选项时，TiDB 将在客户端出示证书的情况下根据该选项指定的受信任的 CA 列表验证客户端证书。若验证失败，则连接会被终止。
+ 即使设置了该选项，若客户端没有出示证书，则安全连接仍然继续，不会进行客户端证书验证。
