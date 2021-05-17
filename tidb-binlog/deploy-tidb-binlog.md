---
title: TiDB Binlog 集群部署
aliases: ['/docs-cn/dev/tidb-binlog/deploy-tidb-binlog/','/docs-cn/dev/reference/tidb-binlog/deploy/','/docs-cn/dev/how-to/deploy/tidb-binlog/','/docs-cn/dev/reference/tools/tidb-binlog/deploy/']
---

# TiDB Binlog 集群部署

## 服务器要求

Pump 和 Drainer 均可部署和运行在 Intel x86-64 架构的 64 位通用硬件服务器平台上。在开发、测试和生产环境下，对服务器硬件配置的要求和建议如下：

| 服务     | 部署数量       | CPU   | 磁盘          | 内存   |
| :-------- | :-------- | :--------| :--------------- | :------ |
| Pump | 3 | 8核+   | SSD, 200 GB+ | 16G |
| Drainer | 1 | 8核+ | SAS, 100 GB+ （如果输出 binlog 为本地文件，磁盘大小视保留数据天数而定） | 16G |

## 使用 TiUP 部署 TiDB Binlog

推荐使用 TiUP 部署 TiDB Binlog，详细部署方式参考 [TiUP 部署 TiDB Binlog](/production-deployment-using-tiup.md)。

## 使用 Binary 部署 TiDB Binlog

### 下载官方 Binary

{{< copyable "shell-regular" >}}

```bash
wget https://download.pingcap.org/tidb-{version}-linux-amd64.tar.gz &&
wget https://download.pingcap.org/tidb-{version}-linux-amd64.sha256
```

检查文件完整性，返回 ok 则正确：

{{< copyable "shell-regular" >}}

```bash
sha256sum -c tidb-{version}-linux-amd64.sha256
```

对于 v2.1.0 GA 及以上版本，Pump 和 Drainer 已经包含在 TiDB 的下载包中，其他版本需要单独下载 Pump 和 Drainer:

{{< copyable "shell-regular" >}}

```bash
wget https://download.pingcap.org/tidb-binlog-latest-linux-amd64.tar.gz &&
wget https://download.pingcap.org/tidb-binlog-latest-linux-amd64.sha256
```

检查文件完整性，返回 ok 则正确：

{{< copyable "shell-regular" >}}

```bash
sha256sum -c tidb-binlog-latest-linux-amd64.sha256
```

### 使用样例

假设有三个 PD，一个 TiDB，另外有两台机器用于部署 Pump，一台机器用于部署 Drainer。各个节点信息如下：

```
TiDB="192.168.0.10"
PD1="192.168.0.16"
PD2="192.168.0.15"
PD3="192.168.0.14"
Pump="192.168.0.11"
Pump="192.168.0.12"
Drainer="192.168.0.13"
```

下面以此为例，说明 Pump/Drainer 的使用。

1. 使用 binary 部署 Pump

    - Pump 命令行参数说明（以在 “192.168.0.11” 上部署为例）

        ```bash
        Usage of Pump:
        -L string
            日志输出信息等级设置：debug，info，warn，error，fatal (默认 "info")
        -V
            打印版本信息
        -addr string
            Pump 提供服务的 RPC 地址(-addr="192.168.0.11:8250")
        -advertise-addr string
            Pump 对外提供服务的 RPC 地址(-advertise-addr="192.168.0.11:8250")
        -config string
            配置文件路径，如果你指定了配置文件，Pump 会首先读取配置文件的配置;
            如果对应的配置在命令行参数里面也存在，Pump 就会使用命令行参数的配置来覆盖配置文件里的配置。
        -data-dir string
            Pump 数据存储位置路径
        -gc int
            Pump 只保留多少天以内的数据 (默认 7)
        -heartbeat-interval int
            Pump 向 PD 发送心跳间隔 (单位 秒)
        -log-file string
            log 文件路径
        -log-rotate string
            log 文件切换频率，hour/day
        -metrics-addr string
            Prometheus Pushgateway 地址，不设置则禁止上报监控信息
        -metrics-interval int
            监控信息上报频率 (默认 15，单位 秒)
        -node-id string
            Pump 节点的唯一识别 ID，如果不指定，程序会根据主机名和监听端口自动生成
        -pd-urls string
            PD 集群节点的地址 (-pd-urls="http://192.168.0.16:2379,http://192.168.0.15:2379,http://192.168.0.14:2379")
        -fake-binlog-interval int
            Pump 节点生成 fake binlog 的频率 (默认 3，单位 秒)
        ```

    - Pump 配置文件（以在 “192.168.0.11” 上部署为例）

        ```toml
        # Pump Configuration

        # Pump 绑定的地址
        addr = "192.168.0.11:8250"

        # Pump 对外提供服务的地址
        advertise-addr = "192.168.0.11:8250"

        # Pump 只保留多少天以内的数据 (默认 7)
        gc = 7

        # Pump 数据存储位置路径
        data-dir = "data.pump"

        # Pump 向 PD 发送心跳的间隔 (单位 秒)
        heartbeat-interval = 2

        # PD 集群节点的地址 (英文逗号分割，中间不加空格)
        pd-urls = "http://192.168.0.16:2379,http://192.168.0.15:2379,http://192.168.0.14:2379"

        # [security]
        # 如无特殊安全设置需要，该部分一般都注解掉
        # 包含与集群连接的受信任 SSL CA 列表的文件路径
        # ssl-ca = "/path/to/ca.pem"
        # 包含与集群连接的 PEM 形式的 X509 certificate 的路径
        # ssl-cert = "/path/to/drainer.pem"
        # 包含与集群链接的 PEM 形式的 X509 key 的路径
        # ssl-key = "/path/to/drainer-key.pem"

        # [storage]
        # 设置为 true（默认值）来保证可靠性，确保 binlog 数据刷新到磁盘
        # sync-log = true

        # 当可用磁盘容量小于该设置值时，Pump 将停止写入数据
        # 42 MB -> 42000000, 42 mib -> 44040192
        # default: 10 gib
        # stop-write-at-available-space = "10 gib"

        # Pump 内嵌的 LSM DB 设置，除非对该部分很了解，否则一般注解掉
        # [storage.kv]
        # block-cache-capacity = 8388608
        # block-restart-interval = 16
        # block-size = 4096
        # compaction-L0-trigger = 8
        # compaction-table-size = 67108864
        # compaction-total-size = 536870912
        # compaction-total-size-multiplier = 8.0
        # write-buffer = 67108864
        # write-L0-pause-trigger = 24
        # write-L0-slowdown-trigger = 17
        ```

    - 启动示例

        {{< copyable "shell-regular" >}}

        ```bash
        ./bin/pump -config pump.toml
        ```

        如果命令行参数与配置文件中的参数重合，则使用命令行设置的参数的值。

2. 使用 binary 部署 Drainer

    - Drainer 命令行参数说明（以在 “192.168.0.13” 上部署为例）

        ```bash
        Usage of Drainer
        -L string
            日志输出信息等级设置：debug，info，warn，error，fatal (默认 "info")
        -V
            打印版本信息
        -addr string
            Drainer 提供服务的地址(-addr="192.168.0.13:8249")
        -c int
            同步下游的并发数，该值设置越高同步的吞吐性能越好 (default 1)
        -cache-binlog-count int
            缓存中的 binlog 数目限制（默认 8）
            如果上游的单个 binlog 较大导致 Drainer 出现 OOM 时，可尝试调小该值减少内存使用
        -config string
            配置文件路径，Drainer 会首先读取配置文件的配置；
            如果对应的配置在命令行参数里面也存在，Drainer 就会使用命令行参数的配置来覆盖配置文件里面的配置
        -data-dir string
            Drainer 数据存储位置路径 (默认 "data.drainer")
        -dest-db-type string
            Drainer 下游服务类型 (默认为 mysql，支持 tidb、kafka、file)
        -detect-interval int
            向 PD 查询在线 Pump 的时间间隔 (默认 10，单位 秒)
        -disable-detect
            是否禁用冲突监测
        -disable-dispatch
            是否禁用拆分单个 binlog 的 SQL 的功能，如果设置为 true，则每个 binlog
            按顺序依次还原成单个事务进行同步（下游服务类型为 MySQL，该项设置为 False）
        -ignore-schemas string
            db 过滤列表 (默认 "INFORMATION_SCHEMA,PERFORMANCE_SCHEMA,mysql,test")，
            不支持对 ignore schemas 的 table 进行 rename DDL 操作
        -initial-commit-ts（默认为 `-1`）
            如果 Drainer 没有相关的断点信息，可以通过该项来设置相关的断点信息
            该参数值为 `-1` 时，Drainer 会自动从 PD 获取一个最新的时间戳
        -log-file string
            log 文件路径
        -log-rotate string
            log 文件切换频率，hour/day
        -metrics-addr string
            Prometheus Pushgateway 地址，不设置则禁止上报监控信息
        -metrics-interval int
            监控信息上报频率（默认 15，单位：秒）
        -node-id string
            drainer 节点的唯一识别 ID，如果不指定，程序会根据主机名和监听端口自动生成
        -pd-urls string
            PD 集群节点的地址 (-pd-urls="http://192.168.0.16:2379,http://192.168.0.15:2379,http://192.168.0.14:2379")
        -safe-mode
            是否开启安全模式使得下游 MySQL/TiDB 可被重复写入
            即将 insert 语句换为 replace 语句，将 update 语句拆分为 delete + replace 语句
        -txn-batch int
            输出到下游数据库一个事务的 SQL 数量（默认 1）
        ```

    - Drainer 配置文件（以在 “192.168.0.13” 上部署为例）

        ```toml
        # Drainer Configuration.

        # Drainer 提供服务的地址("192.168.0.13:8249")
        addr = "192.168.0.13:8249"

        # Drainer 对外提供服务的地址
        advertise-addr = "192.168.0.13:8249"

        # 向 PD 查询在线 Pump 的时间间隔 (默认 10，单位 秒)
        detect-interval = 10

        # Drainer 数据存储位置路径 (默认 "data.drainer")
        data-dir = "data.drainer"

        # PD 集群节点的地址 (英文逗号分割，中间不加空格)
        pd-urls = "http://192.168.0.16:2379,http://192.168.0.15:2379,http://192.168.0.14:2379"

        # log 文件路径
        log-file = "drainer.log"

        # Drainer 从 Pump 获取 binlog 时对数据进行压缩，值可以为 "gzip"，如果不配置则不进行压缩
        # compressor = "gzip"

        # [security]
        # 如无特殊安全设置需要，该部分一般都注解掉
        # 包含与集群连接的受信任 SSL CA 列表的文件路径
        # ssl-ca = "/path/to/ca.pem"
        # 包含与集群连接的 PEM 形式的 X509 certificate 的路径
        # ssl-cert = "/path/to/pump.pem"
        # 包含与集群链接的 PEM 形式的 X509 key 的路径
        # ssl-key = "/path/to/pump-key.pem"

        # Syncer Configuration
        [syncer]
        # 如果设置了该项，会使用该 sql-mode 解析 DDL 语句，此时如果下游是 MySQL 或 TiDB 则
        # 下游的 sql-mode 也会被设置为该值
        # sql-mode = "STRICT_TRANS_TABLES,NO_ENGINE_SUBSTITUTION"

        # 输出到下游数据库一个事务的 SQL 语句数量 (默认 20)
        txn-batch = 20

        # 同步下游的并发数，该值设置越高同步的吞吐性能越好 (默认 16)
        worker-count = 16

        # 是否禁用拆分单个 binlog 的 SQL 的功能，如果设置为 true，则按照每个 binlog
        # 顺序依次还原成单个事务进行同步（下游服务类型为 MySQL, 该项设置为 False）
        disable-dispatch = false

        # safe mode 会使写下游 MySQL/TiDB 可被重复写入
        # 会用 replace 替换 insert 语句，用 delete + replace 替换 update 语句
        safe-mode = false

        # Drainer 下游服务类型（默认为 mysql）
        # 参数有效值为 "mysql"，"tidb"，"file"，"kafka"
        db-type = "mysql"

        # 事务的 commit ts 若在该列表中，则该事务将被过滤，不会同步至下游
        ignore-txn-commit-ts = []

        # db 过滤列表 (默认 "INFORMATION_SCHEMA,PERFORMANCE_SCHEMA,mysql,test")，
        # 不支持对 ignore schemas 的 table 进行 rename DDL 操作
        ignore-schemas = "INFORMATION_SCHEMA,PERFORMANCE_SCHEMA,mysql"

        # replicate-do-db 配置的优先级高于 replicate-do-table。如果配置了相同的库名，支持使用正则表达式进行配置。
        # 以 '~' 开始声明使用正则表达式

        # replicate-do-db = ["~^b.*","s1"]

        # [syncer.relay]
        # 保存 relay log 的目录，空值表示不开启。
        # 只有下游是 TiDB 或 MySQL 时该配置才生效。
        # log-dir = ""
        # 每个文件的大小上限
        # max-file-size = 10485760

        # [[syncer.replicate-do-table]]
        # db-name ="test"
        # tbl-name = "log"

        # [[syncer.replicate-do-table]]
        # db-name ="test"
        # tbl-name = "~^a.*"

        # 忽略同步某些表
        # [[syncer.ignore-table]]
        # db-name = "test"
        # tbl-name = "log"

        # db-type 设置为 mysql 时，下游数据库服务器参数
        [syncer.to]
        host = "192.168.0.13"
        user = "root"
        # 如果你不想在配置文件中写明文密码，则可以使用 `./binlogctl -cmd encrypt -text string` 生成加密的密码
        # encrypted_password 非空时 password 会被忽略, encrypted_password 和 password 二选一即可。
        password = ""
        encrypted_password = ""
        port = 3306

        [syncer.to.checkpoint]
        # 当 checkpoint type 是 mysql 或 tidb 时可以开启该选项，以改变保存 checkpoint 的数据库
        # schema = "tidb_binlog"
        # 目前只支持 mysql 或者 tidb 类型。可以去掉注释来控制 checkpoint 保存的位置。
        # db-type 默认的 checkpoint 保存方式是:
        # mysql/tidb -> 对应的下游 mysql/tidb
        # file/kafka -> file in `data-dir`
        # type = "mysql"
        # host = "127.0.0.1"
        # user = "root"
        # password = ""
        # 使用 `./binlogctl -cmd encrypt -text string` 加密的密码
        # encrypted_password 非空时 password 会被忽略
        # encrypted_password = ""
        # port = 3306

        # db-type 设置为 file 时，存放 binlog 文件的目录
        # [syncer.to]
        # dir = "data.drainer"

        # db-type 设置为 kafka 时，Kafka 相关配置
        # [syncer.to]
        # kafka-addrs 和 zookeeper-addrs 只需要一个，两者都有时程序会优先用 zookeeper 中的 kafka 地址
        # zookeeper-addrs = "127.0.0.1:2181"
        # kafka-addrs = "127.0.0.1:9092"
        # kafka-version = "0.8.2.0"
        # kafka-max-messages = 1024

        # 保存 binlog 数据的 Kafka 集群的 topic 名称，默认值为 <cluster-id>_obinlog
        # 如果运行多个 Drainer 同步数据到同一个 Kafka 集群，每个 Drainer 的 topic-name 需要设置不同的名称
        # topic-name = ""
        ```

    - 启动示例

        > **注意：**
        >
        > 如果下游为 MySQL/TiDB，为了保证数据的完整性，在 Drainer 初次启动前需要获取 `initial-commit-ts` 的值，并进行全量数据的备份与恢复。

        初次启动时使用参数 `initial-commit-ts`， 命令如下：

        {{< copyable "shell-regular" >}}

        ```bash
        ./bin/drainer -config drainer.toml -initial-commit-ts {initial-commit-ts}
        ```

        如果命令行参数与配置文件中的参数重合，则使用命令行设置的参数的值。

> **注意：**
>
> - 在运行 TiDB 时，需要保证至少一个 Pump 正常运行。
> - 通过给 TiDB 增加启动参数 `enable-binlog` 来开启 binlog 服务。尽量保证同一集群的所有 TiDB 都开启了 binlog 服务，否则在同步数据时可能会导致上下游数据不一致。如果要临时运行一个不开启 binlog 服务的 TiDB 实例，需要在 TiDB 的配置文件中设置 `run_ddl= false`。
> - Drainer 不支持对 ignore schemas（在过滤列表中的 schemas）的 table 进行 rename DDL 操作。
> - 在已有的 TiDB 集群中启动 Drainer，一般需要全量备份并且获取**快照时间戳**，然后导入全量备份，最后启动 Drainer 从对应的快照时间戳开始同步增量数据。
> - 下游使用 MySQL 或 TiDB 时应当保证上下游数据库的 sql_mode 具有一致性，即下游数据库同步每条 SQL 语句时的 sql_mode 应当与上游数据库执行该条 SQL 语句时的 sql_mode 保持一致。可以在上下游分别执行 `select @@sql_mode;` 进行查询和比对。
> - 如果存在上游 TiDB 能运行但下游 MySQL 不支持的 DDL 语句时（例如下游 MySQL 使用 InnoDB 引擎时同步语句 `CREATE TABLE t1(a INT) ROW_FORMAT=FIXED;`），Drainer 也会同步失败，此时可以在 Drainer 配置中跳过该事务，同时在下游手动执行兼容的语句，详见[跳过事务](/tidb-binlog/tidb-binlog-faq.md#同步时出现上游数据库支持但是下游数据库执行会出错的-ddl应该怎么办)。
