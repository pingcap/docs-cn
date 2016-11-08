# 参数解释

## TiDB

### --store
+ 用来指定 TiDB 实际的存储引擎
+ 默认: "goleveldb"
+ 你可以选择 "memory", "goleveldb", "BoltDB" 或者 "TiKV"。前面三个是本地存储引擎，而 TiKV 是一个分布式存储引擎。

### --path
+ 对于本地存储引擎 "goleveldb", "BoltDB" 来说，path 指定的是实际的数据存放路径。
+ 对于 "memory" 存储引擎来说，path 不用设置。
+ 对于 "TiKV" 存储引擎来说，path 指定的是实际的 PD 地址。假设我们在 127.0.0.1:2379, 127.0.0.2:2379 和 127.0.0.3:2379 上面部署了 PD，那么 path 为 "127.0.0.1:2379,127.0.0.2:2379,127.0.0.3:2379"。
+ 默认: "/tmp/tidb"

### -L
+ Log 级别
+ 默认: "info"
+ 我们能选择 debug, info, warn, error 或者 fatal.

### --log-file
+ Log 文件
+ 默认: ""
+ 如果没设置这个参数，log 会默认输出到 "stderr"，如果设置了，log 就会输出到对应的文件里面，在每天凌晨，log 会自动轮转使用一个新的文件，并且将以前的文件改名备份。

### --host
+ TiDB 服务监听 host。
+ 默认: "0.0.0.0"
+ TiDB 服务会监听这个 host。

### -P
+ TiDB 服务监听端口。
+ 默认: "4000"
+ TiDB 服务将会使用这个端口接受 MySQL 客户端发过来的请求。

### --status
+ TiDB 服务状态监听端口。
+ 默认: "10080"
+ 这个端口是为了展示 TiDB 内部数据用的。包括 [prometheus 统计](https://prometheus.io/) 以及 [pprof](https://golang.org/pkg/net/http/pprof/)。
+ Prometheus 统计可以通过 "http://host:status_port/metrics" 访问。
+ Pprof 数据可以通过 "http://host:status_port/debug/pprof" 访问。

### --lease
+ Schema 的租约时间，单位：秒。
+ 默认: "1"
+ Schema 的 lease 主要用在 online schema changes 上面。这个值会影响到实际的 DDL 语句的执行时间。千万不要随便改动这个值，除非你能知道相关的内部机制。

### --socket
+ TiDB 服务使用 unix socket file 方式接受外部连接。
+ 默认: ""
+ 譬如我们可以使用 "/tmp/tidb.sock" 来打开 unix socket file。

### --perfschema
+ 使用 true/false 来打开或者关闭性能 schema。
+ 默认: false
+ 值可以是 (true) or (false)。性能 Schema 可以帮助我们在运行时检测内部的执行情况。可以通过 [performance schema](http://dev.mysql.com/doc/refman/5.7/en/performance-schema.html) 获取更多信息。但需要注意，开启性能 Schema，会影响 TiDB 的性能。

### --report-status
+ 打开 (true) 或者关闭 (false) 服务状态监听端口.
+ 默认: true
+ 值可以为 (true) 或者 (false). (true) 表明我们开启状态监听端口。 (false) 表明关闭。

### --metrics-addr
+ Prometheus Push Gateway 地址。
+ 默认: ""
+ 如果为空，TiDB 不会将统计信息推送给 Push Gateway。

### --metrics-intervel
+ 推送统计信息到 Prometheus Push Gateway 的时间间隔。
+ 默认: 15s
+ 设置为 0 表明不推送统计信息给 Push Gateway。

## Placement Driver (PD)

### -L
+ Log 级别
+ 默认: "info"
+ 我们能选择 debug, info, warn, error 或者 fatal.

### --log-file
+ Log 文件
+ 默认: ""
+ 如果没设置这个参数，log 会默认输出到 "stderr"，如果设置了，log 就会输出到对应的文件里面，在每天凌晨，log 会自动轮转使用一个新的文件，并且将以前的文件改名备份。

### --config

+ 配置文件
+ 默认: ""
+ 如果你指定了配置文件，PD 会首先读取配置文件的配置。然后如果对应的配置在命令行参数里面也存在，PD 就会使用命令行参数的配置来覆盖配置文件里面的。

### --name

+ 当前 PD 的名字。
+ 默认: "pd"
+ 如果你需要启动多个 PD，一个要给 PD 使用不同的名字。

### --data-dir

+ PD 存储数据路径。
+ 默认: "default.${name}"

### --client-urls

+ 处理客户端请求监听 URLs。
+ 默认: "http://127.0.0.1:2379"

###  --advertise-client-urls

+ 给外部客户端请求建议的 URL 列表。
+ 默认: ${client-urls}
+ 在某些情况下，譬如 docker，或者 NAT 网络环境，客户端并不能通过 PD 自己监听的 client URLs 来访问到 PD，这时候，你就可以设置 advertise urls 来让客户端访问。

### --peer-urls

+ 处理其他 PD 节点请求监听 URLs。
+ default: "http://127.0.0.1:2380"

### --advertise-peer-urls

+ 给其他节点请求建议的 URL 列表。
+ 默认: ${peer-urls}
+ 在某些情况下，譬如 docker，或者 NAT 网络环境，其他节点并不能通过 PD 自己监听的 peer URLs 来访问到 PD，这时候，你就可以设置 advertise urls 来让其他节点访问。

### --initial-cluster

+ 初始化 PD 集群配置。
+ 默认: "{name}=http://{advertise-peer-url}"
+ 例如，如果 `name` 是 "pd", 并且 `advertise-peer-urls` 是 "http://127.0.0.1:2380", 那么 `initial-cluster` 就是 "pd=http://127.0.0.1:2380。
+ 如果你需要启动三台 PD，那么 `initial-cluster` 可能就是 "pd1=http://127.0.0.1:2380,pd2=http://127.0.0.2:2380,pd3=http://127.0.0.3:2380"。

### --join

+ 动态加入 PD 集群。
+ 默认: ""
+ 如果你想动态将一台 PD 加入集群，你可以使用 `--join="${advertise-client-urls}"`， `advertise-client-url` 是当前集群里面任意 PD 的 `advertise-client-url`，你也可以使用多个 PD 的，需要用逗号分隔。

## TiKV

TiKV 在命令行参数上面支持一些可读性好的单位转换.

 - 文件大小（以 bytes 为单位）: KB, MB, GB, TB, PB（也可以全小写）。
 - 时间（以毫秒为单位）: ms, s, m, h。

### -A, --addr

+ TiKV 服务监听地址。
+ 默认: "127.0.0.1:20160"

### --advertise-addr

+ TiKV 给外部客户端访问建议的地址。
+ 默认: ${addr}
+ 在某些情况下，譬如 docker，或者 NAT 网络环境，客户端并不能通过  TiKV 自己监听的地址来访问到 TiKV，这时候，你就可以设置 advertise addr 来让 客户端访问。

### -L, --Log
+ Log 级别
+ 默认: "info"
+ 我们能选择 trace, debug, info, warn, error, 或者 off。

### --log-file
+ Log 文件
+ 默认: ""
+ 如果没设置这个参数，log 会默认输出到 "stderr"，如果设置了，log 就会输出到对应的文件里面，在每天凌晨，log 会自动轮转使用一个新的文件，并且将以前的文件改名备份。

### -C, --config

+ 配置文件
+ 默认: ""
+ 如果你指定了配置文件，TiKV 会首先读取配置文件的配置。然后如果对应的配置在命令行参数里面也存在，TiKV 就会使用命令行参数的配置来覆盖配置文件里面的。

### -s, --store

+ TiKV 数据存储路径。
+ 默认: "/tmp/tikv/store"

### --capacity

+ TiKV 存储数据的容量。
+ 默认: 0 (无限)
+ PD 需要使用这个值来对整个集群做 balance 操作。（提示：你可以使用 10GB 来替代 1073741824，从而简化参数的传递）。


### --pd

+ PD 地址列表。
+ 默认: ""
+ TiKV 必须使用这个值连接 PD，才能正常工作。使用逗号来分隔多个 PD 地址，例如："pd1:2379,pd2:2379"。

