---
title: TiDB Lightning 配置参数
summary: 使用配置文件或命令行配置 TiDB Lightning。
aliases: ['/docs-cn/v3.0/tidb-lightning/tidb-lightning-configuration/','/docs-cn/v3.0/reference/tools/tidb-lightning/config/']
---

# TiDB Lightning 配置参数

你可以使用配置文件或命令行配置 TiDB Lightning。本文主要介绍 TiDB Lightning 的全局配置、任务配置和 TiKV Importer 的配置，以及如何使用命令行进行参数配置。

## 配置文件

TiDB Lightning 的配置文件分为“全局”和“任务”两种类别，二者在结构上兼容。只有当[服务器模式](/tidb-lightning/tidb-lightning-web-interface.md)开启时，全局配置和任务配置才会有区别；默认情况下，服务器模式为禁用状态，此时 TiDB Lightning 只会执行一个任务，且全局和任务配置使用同一配置文件。

### TiDB Lightning 全局配置

```toml
### tidb-lightning 全局配置

[lightning]
# 用于拉取 web 界面和 Prometheus 监控项的 HTTP 端口。设置为 0 时为禁用状态。
status-addr = ':8289'

# 切换为服务器模式并使用 web 界面
# 详情参见“TiDB Lightning web 界面”文档
server-mode = false

# 日志
level = "info"
file = "tidb-lightning.log"
max-size = 128 # MB
max-days = 28
max-backups = 14
```

### TiDB Lightning 任务配置

```toml
### tidb-lightning 任务配置

[lightning]
# 启动之前检查集群是否满足最低需求。
# check-requirements = true

# 引擎文件的最大并行数。
# 每张表被切分成一个用于存储索引的“索引引擎”和若干存储行数据的“数据引擎”。
# 这两项设置控制两种引擎文件的最大并发数。
# 这两项设置的值会影响 tikv-importer 的内存和磁盘用量。
# 两项数值之和不能超过 tikv-importer 的 max-open-engines 的设定。
index-concurrency = 2
table-concurrency = 6

# 数据的并发数。默认与逻辑 CPU 的数量相同。
# 混合部署的情况下可以将其大小配置为逻辑 CPU 数的 75%，以限制 CPU 的使用。
# region-concurrency =

# I/O 最大并发数。I/O 并发量太高时，会因硬盘内部缓存频繁被刷新
# 而增加 I/O 等待时间，导致缓存未命中和读取速度降低。
# 对于不同的存储介质，此参数可能需要调整以达到最佳效率。
io-concurrency = 5

[checkpoint]
# 是否启用断点续传。
# 导入数据时，TiDB Lightning 会记录当前表导入的进度。
# 所以即使 Lightning 或其他组件异常退出，在重启时也可以避免重复再导入已完成的数据。
enable = true
# 存储断点的数据库名称。
schema = "tidb_lightning_checkpoint"
# 存储断点的方式。
#  - file：存放在本地文件系统。
#  - mysql：存放在兼容 MySQL 的数据库服务器。
driver = "file"

# dsn 是数据源名称 (data source name)，表示断点的存放位置。
# 若 driver = "file"，则 dsn 为断点信息存放的文件路径。
#若不设置该路径，则默认存储路径为“/tmp/CHECKPOINT_SCHEMA.pb”。
# 若 driver = "mysql"，则 dsn 为“用户:密码@tcp(地址:端口)/”格式的 URL。
# 若不设置该 URL，则默认会使用 [tidb] 部分指定的 TiDB 服务器来存储断点。
# 为减少目标 TiDB 集群的压力，建议指定另一台兼容 MySQL 的数据库服务器来存储断点。
# dsn = "/tmp/tidb_lightning_checkpoint.pb"

# 所有数据导入成功后是否保留断点。设置为 false 时为删除断点。
# 保留断点有利于进行调试，但会泄漏关于数据源的元数据。
# keep-after-success = false

[tikv-importer]
# 选择后端：“importer” 或 “tidb“
# backend = "importer"
# 当后端是 “importer” 时，tikv-importer 的监听地址（需改为实际地址）。
addr = "172.16.31.10:8287"
# 当后端是 “tidb” 时，插入重复数据时执行的操作。
# - replace：新数据替代已有数据
# - ignore：保留已有数据，忽略新数据
# - error：中止导入并报错
# on-duplicate = "replace"

[mydumper]
# 设置文件读取的区块大小，确保该值比数据源的最长字符串长。
read-block-size = 65536 # Byte (默认为 64 KB)

# （源数据文件）单个导入区块大小的最小值。
# Lightning 根据该值将一张大表分割为多个数据引擎文件。
batch-size = 107_374_182_400 # Byte (默认为 100 GB)

# 引擎文件需按顺序导入。由于并行处理，多个数据引擎几乎在同时被导入，
# 这样形成的处理队列会造成资源浪费。因此，为了合理分配资源，Lightning
# 稍微增大了前几个区块的大小。该参数也决定了比例系数，即在完全并发下
# “导入”和“写入”过程的持续时间比。这个值可以通过计算 1 GB 大小的
# 单张表的（导入时长/写入时长）得到。在日志文件中可以看到精确的时间。
# 如果“导入”更快，区块大小的差异就会更小；比值为 0 时则说明区块大小一致。
# 取值范围为（0 <= batch-import-ratio < 1）。
batch-import-ratio = 0.75

# mydumper 本地源数据目录。
data-source-dir = "/data/my_database"
# 如果 no-shcema = true，那么 TiDB Lightning 假设目标 TiDB 集群上
# 已有表结构，并且不会执行 `CREATE TABLE` 语句。
no-schema = false
# 指定包含 `CREATE TABLE` 语句的表结构文件的字符集。只支持下列选项：
#  - utf8mb4：表结构文件必须使用 UTF-8 编码，否则 Lightning 会报错。
#  - gb18030：表结构文件必须使用 GB-18030 编码，否则 Lightning 会报错。
#  - auto：自动判断文件编码是 UTF-8 还是 GB-18030，两者皆非则会报错（默认）。
#  - binary：不尝试转换编码。
# 注意：**数据** 文件始终解析为 binary 文件。
character-set = "auto"

# 只导入与该通配符规则相匹配的表。详情见相应章节。
filter = ['*.*']

# 配置 CSV 文件的解析方式。
[mydumper.csv]
# 字段分隔符，应为单个 ASCII 字符。
separator = ','
# 引用定界符，可为单个 ASCII 字符或空字符串。
delimiter = '"'
# CSV 文件是否包含表头。
# 如果 header = true，将跳过首行。
header = true
# CSV 文件是否包含 NULL。
# 如果 not-null = true，CSV 所有列都不能解析为 NULL。
not-null = false
# 如果 not-null = false（即 CSV 可以包含 NULL），
# 为以下值的字段将会被解析为 NULL。
null = '\N'
# 是否对字段内“\“进行转义
backslash-escape = true
# 如果有行以分隔符结尾，删除尾部分隔符。
trim-last-separator = false

[tidb]
# 目标集群的信息。tidb-server 的地址，填一个即可。
host = "172.16.31.1"
port = 4000
user = "root"
password = ""
# 表结构信息从 TiDB 的“status-port”获取。
status-port = 10080
# pd-server 的地址，填一个即可。
pd-addr = "172.16.31.4:2379"
# tidb-lightning 引用了 TiDB 库，并生成产生一些日志。
# 设置 TiDB 库的日志等级。
log-level = "error"

# 设置 TiDB 会话变量，提升 Checksum 和 Analyze 的速度。
# 各参数定义可参阅”控制 Analyze 并发度“文档
build-stats-concurrency = 20
distsql-scan-concurrency = 100
index-serial-scan-concurrency = 20
checksum-table-concurrency = 16

# 解析和执行 SQL 语句的默认 SQL 模式。
sql-mode = "STRICT_TRANS_TABLES,NO_ENGINE_SUBSTITUTION"
# `max-allowed-packet` 设置数据库连接允许的最大数据包大小，
# 对应于系统参数中的 `max_allowed_packet`。 如果设置为 0，
# 会使用下游数据库 global 级别的 `max_allowed_packet`。
max-allowed-packet = 67_108_864

# 数据导入完成后，tidb-lightning 可以自动执行 Checksum、Compact 和 Analyze 操作。
# 在生产环境中，建议这将些参数都设为 true。
# 执行的顺序为：Checksum -> Compact -> Analyze。
[post-restore]
# 如果设置为 true，会对所有表逐个执行 `ADMIN CHECKSUM TABLE <table>` 操作
# 来验证数据的完整性。
checksum = true
# 如果设置为 true，会在导入每张表后执行一次 level-1 Compact。
# 默认值为 false。
level-1-compact = false
# 如果设置为 true，会在导入过程结束时对整个 TiKV 集群执行一次 full Compact。
# 默认值为 false。
compact = false
# 如果设置为 true，会对所有表逐个执行 `ANALYZE TABLE <table>` 操作。
analyze = true

# 设置周期性后台操作。
# 支持的单位：h（时）、m（分）、s（秒）。
[cron]
# Lightning 自动刷新导入模式状态的持续时间，该值应小于 TiKV 对应的设定值。
switch-mode = "5m"
# 在日志中打印导入进度的持续时间。
log-progress = "5m"
```

### TiKV Importer 配置参数

```toml
# TiKV Importer 配置文件模版

# 日志文件
log-file = "tikv-importer.log"
# 日志等级：trace, debug, info, warn, error 和 off
log-level = "info"

[server]
# tikv-importer 的监听地址，tidb-lightning 需要连到这个地址进行数据写入。
addr = "192.168.20.10:8287"
# gRPC 服务器的线程池大小。
grpc-concurrency = 16

[metric]
# 给 Prometheus 客户端推送的 job 名称。
job = "tikv-importer"
# 给 Prometheus 客户端推送的间隔。
interval = "15s"
# Prometheus Pushgateway 的地址。
address = ""

[rocksdb]
# background job 的最大并发数。
max-background-jobs = 32

[rocksdb.defaultcf]
# 数据在刷新到硬盘前能存于内存的容量上限。
write-buffer-size = "1GB"
# 内存中写缓冲器的最大数量。
max-write-buffer-number = 8

# 各个压缩层级使用的算法。
# 第 0 层的算法用于压缩 KV 数据。
# 第 6 层的算法用于压缩 SST 文件。
# 第 1 至 5 层的算法目前尚未使用。
compression-per-level = ["lz4", "no", "no", "no", "no", "no", "lz4"]

[rocksdb.writecf]
# 同上
compression-per-level = ["lz4", "no", "no", "no", "no", "no", "lz4"]

[import]
# 存储引擎文件的文件夹路径
import-dir = "/mnt/ssd/data.import/"
# 处理 RPC 请求的线程数
num-threads = 16
# 导入 job 的并发数。
num-import-jobs = 24
# 预处理 Region 最长时间。
# max-prepare-duration = "5m"
# 把要导入的数据切分为这个大小的 Region。
#region-split-size = "512MB"
# 设置 stream-channel-window 的大小。
# channel 满了之后 stream 会处于阻塞状态。
# stream-channel-window = 128
# 同时打开引擎文档的最大数量。
max-open-engines = 8
# Importer 上传至 TiKV 的最大速度（字节/秒）。
# upload-speed-limit = "512MB"
# 目标存储可用空间比率（store_available_space/store_capacity）的最小值。
# 如果目标存储空间的可用比率低于该值，Importer 将会暂停上传 SST
# 来为 PD 提供足够时间进行 Regions 负载均衡。
min-available-ratio = 0.05
```

## 命令行参数

### `tidb-lightning`

使用 `tidb-lightning` 可以对下列参数进行配置：

| 参数 | 描述 | 对应配置项 |
|:----|:----|:----|
| --config *file* | 从 *file* 读取全局设置。如果没有指定则使用默认设置。 | |
| -V | 输出程序的版本 | |
| -d *directory* | 读取数据的目录 | `mydumper.data-source-dir` |
| -L *level* | 日志的等级： debug、info、warn、error 或 fatal (默认为 info) | `lightning.log-level` |
| -f *rule* | [表库过滤的规则](/table-filter.md) (可多次指定) | `mydumper.filter` |
| --backend *backend* | 选择后端的模式：`importer` 或 [`tidb`](/tidb-lightning/tidb-lightning-tidb-backend.md) | `tikv-importer.backend` |
| --log-file *file* | 日志文件路径 | `lightning.log-file` |
| --status-addr *ip:port* | TiDB Lightning 服务器的监听地址 | `lightning.status-port` |
| --importer *host:port* | TiKV Importer 的地址 | `tikv-importer.addr` |
| --pd-urls *host:port* | PD endpoint 的地址 | `tidb.pd-addr` |
| --tidb-host *host* | TiDB Server 的 host | `tidb.host` |
| --tidb-port *port* | TiDB Server 的端口（默认为 4000） | `tidb.port` |
| --tidb-status *port* | TiDB Server 的状态端口的（默认为 10080） | `tidb.status-port` |
| --tidb-user *user* | 连接到 TiDB 的用户名 | `tidb.user` |
| --tidb-password *password* | 连接到 TiDB 的密码 | `tidb.password` |

如果同时对命令行参数和配置文件中的对应参数进行更改，命令行参数将优先生效。例如，在 `cfg.toml` 文件中，不管对日志等级做出什么修改，运行 `./tidb-lightning -L debug --config cfg.toml` 命令总是将日志级别设置为 “debug”。

### `tidb-lightning-ctl`

使用 `tidb-lightning-ctl` 可以对下列参数进行配置：

| 参数 | 描述 |
|:----|:----------|
| --compact | 执行 full compact |
| --switch-mode *mode* | 将每个 TiKV Store 切换到指定模式（normal 或 import） |
| --import-engine *uuid* | 将 TiKV Importer 上关闭的引擎文件导入到 TiKV 集群 |
| --cleanup-engine *uuid* | 删除 TiKV Importer 上的引擎文件 |
| --checkpoint-dump *folder* | 将当前的断点以 CSV 格式存储到文件夹中 |
| --checkpoint-error-destroy *tablename* | 删除断点，如果报错则删除该表 |
| --checkpoint-error-ignore *tablename* | 忽略指定表中断点的报错 |
| --checkpoint-remove *tablename* | 无条件删除表的断点 |

*tablename* 必须是`` `db`.`tbl` `` 中的限定表名（包括反引号），或关键词 `all`。

此外，上表中所有 `tidb-lightning` 的参数也适用于 `tidb-lightning-ctl`。

### `tikv-importer`

使用 `tikv-importer` 可以对下列参数进行配置：

| 参数 | 描述 | 对应配置项 |
|:----|:----|:-------|
| -C, --config *file* | 从 *file* 读取配置。如果没有指定，则使用默认设置| |
| -V, --version | 输出程序的版本 | |
| -A, --addr *ip:port* | TiKV Importer 服务器的监听地址 | `server.addr` |
| --import-dir *dir* | 引擎文件的存储目录 | `import.import-dir` |
| --log-level *level* | 日志的等级： trace、debug、info、warn、error 或 off | `log-level` |
| --log-file *file* | 日志文件路径 | `log-file` |
