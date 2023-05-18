---
title: TiDB Lightning 配置参数
summary: 使用配置文件或命令行配置 TiDB Lightning。
aliases: ['/docs-cn/dev/tidb-lightning/tidb-lightning-configuration/','/docs-cn/dev/reference/tools/tidb-lightning/config/']
---

# TiDB Lightning 配置参数

你可以使用配置文件或命令行配置 TiDB Lightning。本文主要介绍 TiDB Lightning 的全局配置、任务配置，以及如何使用命令行进行参数配置。

## 配置文件

TiDB Lightning 的配置文件分为“全局”和“任务”两种类别，二者在结构上兼容。只有当[服务器模式](/tidb-lightning/tidb-lightning-web-interface.md)开启时，全局配置和任务配置才会有区别；默认情况下，服务器模式为禁用状态，此时 TiDB Lightning 只会执行一个任务，且全局和任务配置使用同一配置文件。

### TiDB Lightning 全局配置

```toml
### tidb-lightning 全局配置

[lightning]
# 用于进度展示 web 界面、拉取 Prometheus 监控项、暴露调试数据和提交导入任务（服务器模式下）的 HTTP 端口。设置为 0 时为禁用状态。
status-addr = ':8289'

# 服务器模式，默认值为 false，命令启动后会开始导入任务。如果改为 true，命令启动后会等待用户在 web 界面上提交任务。
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

# TiDB Lightning 停止迁移任务之前能容忍的最大非严重 (non-fatal errors) 错误数。
# 在忽略非严重错误所在的行数据之后，迁移任务可以继续执行。
# 将该值设置为 N，表示 TiDB Lightning 会在遇到第 (N+1) 个错误时停止迁移任务。
# 被忽略的行会被记录到位于目标集群的 "task info" 数据库中。最大错误数可以通过下面参数配置。
# 默认值为 MaxInt64 字节，即 9223372036854775807 字节。
max-error = 0
# 参数 task-info-schema-name 指定用于存储 TiDB Lightning 执行结果的数据库。
# 要关闭该功能，需要将该值设置为空字符串。
# task-info-schema-name = 'lightning_task_info'

# 在并行导入模式下，在目标集群保存各个 TiDB Lightning 实例元信息的 schema 名字，默认为 "lightning_metadata"。
# 如果未开启并行导入模式，无须设置此配置项。
# **注意：**
# - 对于参与同一批并行导入的每个 TiDB Lightning 实例，该参数设置的值必须相同，否则将无法确保导入数据的正确性。
# - 如果开启并行导入模式，需要确保导入使用的用户（对于 tidb.user 配置项）有权限创建和访问此配置对应的库。
# - TiDB Lightning 在导入完成后会删除此 schema，因此不要使用已存在的库名配置该参数。
meta-schema-name = "lightning_metadata"

[security]
# 指定集群中用于 TLS 连接的证书和密钥。
# CA 的公钥证书。如果留空，则禁用 TLS。
# ca-path = "/path/to/ca.pem"
# 此服务的公钥证书。
# cert-path = "/path/to/lightning.pem"
# 该服务的密钥。
# key-path = "/path/to/lightning.key"

[checkpoint]
# 是否启用断点续传。
# 导入数据时，TiDB Lightning 会记录当前表导入的进度。
# 所以即使 TiDB Lightning 或其他组件异常退出，在重启时也可以避免重复再导入已完成的数据。
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
# "local"：Physical Import Mode，默认使用。适用于 TB 级以上大数据量，但导入期间下游 TiDB 无法对外提供服务。
# "tidb"：Logical Import Mode。TB 级以下数据量可以采用，下游 TiDB 可正常提供服务。
# backend = "local"
# 是否允许启动多个 TiDB Lightning 实例（**physical import mode**）并行导入到一个或多个目标表。默认取值为 false。注意，这个参数**不是用于增量导入数据**，仅限目标表为空的场景使用。
# 多个 TiDB Lightning 实例（physical import mode）同时导入一张表时，此开关必须设置为 true。但前提是目标表不能存在数据，即所有的数据都只能是由 TiDB Lightning 导入。
# incremental-import = false
# 当后端是 “importer” 时，tikv-importer 的监听地址（需改为实际地址）。
addr = "172.16.31.10:8287"
# Logical Import Mode 插入冲突数据时执行的操作。关于冲突检测详细信息请查阅：https://docs.pingcap.com/zh/tidb/dev/tidb-lightning-logical-import-mode-usage#冲突数据检测
# - replace：新数据替代已有数据
# - ignore：保留已有数据，忽略新数据
# - error：中止导入并报错
# on-duplicate = "replace"

# Physical Import Mode 设置是否检测和解决重复的记录（唯一键冲突）。
# 目前支持三种解决方法：
#  - record: 数据写入目标表后，将目标表中重复记录添加到目标 TiDB 中的 `lightning_task_info.conflict_error_v1` 表中。注意，该方法要求目标 TiKV 的版本为 v5.2.0 或更新版本。如果版本过低，则会启用下面的 'none' 模式。
#  - none: 不检测重复记录。该模式是三种模式中性能最佳的，但是如果数据源存在重复记录，会导致 TiDB 中出现数据不一致的情况。
#  - remove: 记录所有目标表中的重复记录，和 'record' 模式相似。但是会删除目标表所有的重复记录，以确保目标 TiDB 中的数据状态保持一致。
# duplicate-resolution = 'none'
# Physical Import Mode 一次请求中发送的 KV 数量。
# send-kv-pairs = 32768
# Physical Import Mode 向 TiKV 发送 KV 时是否启用压缩。目前只支持 Gzip 压缩算法，可填写 "gzip" 或者 "gz"。默认不启用压缩。
# compress-kv-pairs = ""
# Physical Import Mode 本地进行 KV 排序的路径。如果磁盘性能较低（如使用机械盘），建议设置成与 `data-source-dir` 不同的磁盘，这样可有效提升导入性能。
# sorted-kv-dir = ""
# Physical Import Mode TiKV 写入 KV 数据的并发度。当 TiDB Lightning 和 TiKV 直接网络传输速度超过万兆的时候，可以适当增加这个值。
# range-concurrency = 16
# Physical Import Mode 限制 TiDB Lightning 向每个 TiKV 节点写入的带宽大小，默认为 0，表示不限制。
# store-write-bwlimit = "128MiB"

# 使用 Physical Import Mode 时，配置 TiDB Lightning 本地临时文件使用的磁盘配额 (disk quota)。当磁盘配额不足时，TiDB Lightning 会暂停读取源数据以及写入临时文件的过程，优先将已经完成排序的 key-value 写入到 TiKV，TiDB Lightning 删除本地临时文件后，再继续导入过程。
# 需要同时配合把 `backend` 设置为 `local` 模式才能生效。
# 默认值为 MaxInt64 字节，即 9223372036854775807 字节。
# disk-quota = "10GB" 

# Physical Import Mode 是否通过 SQL 方式添加索引。默认为 `false`，表示 TiDB Lightning 会将行数据以及索引数据都编码成 KV pairs 后一同导入 TiKV，实现机制和历史版本保持一致。如果设置为 `true`，即 TiDB Lightning 会在导入数据完成后，使用 add index 的 SQL 来添加索引。
# 通过 SQL 方式添加索引的优点是将导入数据与导入索引分开，可以快速导入数据，即使导入数据后，索引添加失败，也不会影响数据的一致性。
# add-index-by-sql = false

# 在使用 TiDB Lightning 导入多租户的 TiDB cluster 的场景下，指定对应的 key space 名称。默认取值为空字符串，表示 TiDB Lightning 会自动获取导入对应租户的 key space 名称；如果指定了值，则使用指定的 key space 名称来导入。
# keyspace-name = ""
[mydumper]
# 设置文件读取的区块大小，确保该值比数据源的最长字符串长。
read-block-size = "64KiB" # 默认值

# 引擎文件需按顺序导入。由于并行处理，多个数据引擎几乎在同时被导入，
# 这样形成的处理队列会造成资源浪费。因此，为了合理分配资源，TiDB Lightning
# 稍微增大了前几个区块的大小。该参数也决定了比例系数，即在完全并发下
# “导入”和“写入”过程的持续时间比。这个值可以通过计算 1 GiB 大小的
# 单张表的（导入时长/写入时长）得到。在日志文件中可以看到精确的时间。
# 如果“导入”更快，区块大小的差异就会更小；比值为 0 时则说明区块大小一致。
# 取值范围为（0 <= batch-import-ratio < 1）。
batch-import-ratio = 0.75

# 本地源数据目录或外部存储 URI。关于外部存储 URI 详情可参考 https://docs.pingcap.com/zh/tidb/v6.6/backup-and-restore-storages#uri-%E6%A0%BC%E5%BC%8F。
data-source-dir = "/data/my_database"

# 指定包含 `CREATE TABLE` 语句的表结构文件的字符集。只支持下列选项：
#  - utf8mb4：表结构文件必须使用 UTF-8 编码，否则会报错。
#  - gb18030：表结构文件必须使用 GB-18030 编码，否则会报错。
#  - auto：自动判断文件编码是 UTF-8 还是 GB-18030，两者皆非则会报错（默认）。
#  - binary：不尝试转换编码。
character-set = "auto"

# 指定源数据文件的字符集，Lightning 会在导入过程中将源文件从指定的字符集转换为 UTF-8 编码。
# 该配置项目前仅用于指定 CSV 文件的字符集。只支持下列选项：
#  - utf8mb4：源数据文件使用 UTF-8 编码。
#  - GB18030：源数据文件使用 GB-18030 编码。
#  - GBK：源数据文件使用 GBK 编码（GBK 编码是对 GB-2312 字符集的拓展，也被称为 Code Page 936）。
#  - binary：不尝试转换编码（默认）。
# 留空此配置将默认使用 "binary"，即不尝试转换编码。
# 需要注意的是，Lightning 不会对源数据文件的字符集做假定，仅会根据此配置对数据进行转码并导入。
# 如果字符集设置与源数据文件的实际编码不符，可能会导致导入失败、导入缺失或导入数据乱码。
data-character-set = "binary"
# 指定在源数据文件的字符集转换过程中，出现不兼容字符时的替换字符。
# 此项不可与字段分隔符、引用界定符和换行符号重复。
# 默认值为 "\uFFFD"，即 UTF-8 编码中的 "error" Rune 或 Unicode replacement character。
# 改变默认值可能会导致潜在的源数据文件解析性能下降。
data-invalid-char-replace = "\uFFFD"

# “严格”格式的导入数据可加快处理速度。
# strict-format = true 要求：
# 在 CSV 文件的所有记录中，每条数据记录的值不可包含字符换行符（U+000A 和 U+000D，即 \r 和 \n）
# 甚至被引号包裹的字符换行符都不可包含，即换行符只可用来分隔行。
# 导入数据源为严格格式时，TiDB Lightning 会快速定位大文件的分割位置进行并行处理。
# 但是如果输入数据为非严格格式，可能会将一条完整的数据分割成两部分，导致结果出错。
# 为保证数据安全而非追求处理速度，默认值为 false。
strict-format = false

# 如果 strict-format = true，TiDB Lightning 会将 CSV 大文件分割为多个文件块进行并行处理。max-region-size 是分割后每个文件块的最大大小。
# max-region-size = "256MiB" # 默认值

# 只导入与该通配符规则相匹配的表。详情见相应章节。
filter = ['*.*', '!mysql.*', '!sys.*', '!INFORMATION_SCHEMA.*', '!PERFORMANCE_SCHEMA.*', '!METRICS_SCHEMA.*', '!INSPECTION_SCHEMA.*']

# 配置 CSV 文件的解析方式。
[mydumper.csv]
# 字段分隔符，支持一个或多个字符，默认值为 ','。
separator = ','
# 引用定界符，设置为空表示字符串未加引号。
delimiter = '"'
# 行尾定界字符，支持一个或多个字符。设置为空（默认值）表示 "\n"（换行）和 "\r\n" （回车+换行），均表示行尾。
terminator = ""
# CSV 文件是否包含表头。
# 如果 header = true，将把首行的内容作为表头处理，不作为数据导入。如果设置为 false，首行也作为 CSV 数据导入，此时请确保 CSV 文件的列顺序与目标表的列顺序一致，否则可能会导致数据差异。
header = true
# CSV 表头是否匹配目标表的表结构。
# 默认为 true，表示在导入数据时，会根据 CSV 表头的字段名去匹配目标表对应的列名，这样即使 CSV 文件和目标表列的顺序不一致也能按照对应的列名进行导入。
# 如果 CSV 表头中的字段名和目标表的列名不匹配（例如，CSV 表头中的某些字段名在目标表中可能找不到对应的同名列）但列的顺序是一致的，请将该配置设置为 false。
# 这时，在导入的时候，会直接忽略 CSV 表头的内容，以避免导入错误。在这种情况下，直接把 CSV 数据按照目标表列的顺序导入。
# 因此，如果列的顺序不一致，请手动调整一致后再导入，否则可能会导致数据差异。
# 注意：只有在 header = true 时，该参数才会生效。如果 header = false ，表示 CSV 文件没有表头，此时不需要考虑相关列名匹配的问题。
header-schema-match = true
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

# [[mydumper.files]]
# 解析 AWS Aurora parquet 文件所需的表达式
# pattern = '(?i)^(?:[^/]*/)*([a-z0-9_]+)\.([a-z0-9_]+)/(?:[^/]*/)*(?:[a-z0-9\-_.]+\.(parquet))$'
# schema = '$1'
# table = '$2'
# type = '$3'

[tidb]
# 目标集群的信息。tidb-server 的地址，填一个即可。
host = "172.16.31.1"
port = 4000
user = "root"
# 设置连接 TiDB 的密码，可为明文或 Base64 编码。
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
distsql-scan-concurrency = 15
index-serial-scan-concurrency = 20
checksum-table-concurrency = 2

# 解析和执行 SQL 语句的默认 SQL 模式。
sql-mode = "ONLY_FULL_GROUP_BY,NO_ENGINE_SUBSTITUTION"
# `max-allowed-packet` 设置数据库连接允许的最大数据包大小，
# 对应于系统参数中的 `max_allowed_packet`。 如果设置为 0，
# 会使用下游数据库 global 级别的 `max_allowed_packet`。
max-allowed-packet = 67_108_864

# SQL 连接是否使用 TLS。可选值为：
#  * ""            - 如果填充了 [tidb.security] 部分，则强制使用 TLS（与 "cluster" 情况相同），否则与 "false" 情况相同
#  * "false"       - 禁用 TLS
#  * "cluster"     - 强制使用 TLS 并使用 [tidb.security] 部分中指定的 CA 验证服务器的证书
#  * "skip-verify" - 强制使用 TLS，但不验证服务器的证书（不安全！）
#  * "preferred"   - 与 "skip-verify" 相同，但是如果服务器不支持 TLS，则会退回到未加密的连接
# tls = ""
# 指定证书和密钥用于 TLS 连接 MySQL。
# 默认为 [security] 部分的副本。
# [tidb.security]
# CA 的公钥证书。设置为空字符串可禁用 SQL 的 TLS。
# ca-path = "/path/to/ca.pem"
# 该服务的公钥证书。默认为 `security.cert-path` 的副本
# cert-path = "/path/to/lightning.pem"
# 此服务的私钥。默认为 `security.key-path` 的副本
# key-path = "/path/to/lightning.key"

# 对于 Physical Import Mode，数据导入完成后，TiDB Lightning 可以自动执行 Checksum 和 Analyze 操作。
# 在生产环境中，建议总是开启 Checksum 和 Analyze。
# 执行的顺序为：Checksum -> Analyze。
# 注意：对于 Logical Import Mode, 无须执行这两个阶段，因此在实际运行时总是会直接跳过。
[post-restore]
# 配置是否在导入完成后对每一个表执行 `ADMIN CHECKSUM TABLE <table>` 操作来验证数据的完整性。
# 可选的配置项：
# - "required"（默认）。在导入完成后执行 CHECKSUM 检查，如果 CHECKSUM 检查失败，则会报错退出。
# - "optional"。在导入完成后执行 CHECKSUM 检查，如果报错，会输出一条 WARN 日志并忽略错误。
# - "off"。导入结束后不执行 CHECKSUM 检查。
# 默认值为 "required"。从 v4.0.8 开始，checksum 的默认值由此前的 "true" 改为 "required"。
#
# 注意：
# 1. Checksum 对比失败通常表示导入异常（数据丢失或数据不一致），因此建议总是开启 Checksum。
# 2. 考虑到与旧版本的兼容性，依然可以在本配置项设置 `true` 和 `false` 两个布尔值，其效果与 `required` 和 `off` 相同。
checksum = "required"
# 配置是否在 CHECKSUM 结束后对所有表逐个执行 `ANALYZE TABLE <table>` 操作。
# 此配置的可选配置项与 `checksum` 相同，但默认值为 "optional"。
analyze = "optional"


# 设置周期性后台操作。
# 支持的单位：h（时）、m（分）、s（秒）。
[cron]
# TiDB Lightning 自动刷新导入模式状态的持续时间，该值应小于 TiKV 对应的设定值。
switch-mode = "5m"
# 在日志中打印导入进度的持续时间。
log-progress = "5m"

# 使用 Physical Import Mode 时，检查本地磁盘配额的时间间隔，默认为 60 秒。
# check-disk-quota = "60s"
```

## 命令行参数

### `tidb-lightning`

使用 `tidb-lightning` 可以对下列参数进行配置：

| 参数 | 描述 | 对应配置项 |
|:----|:----|:----|
| --config *file* | 从 *file* 读取全局设置。如果没有指定则使用默认设置。 | |
| -V | 输出程序的版本 | |
| -d *directory* | 读取数据的本地目录或[外部存储 URI](/br/backup-and-restore-storages.md#uri-格式) | `mydumper.data-source-dir` |
| -L *level* | 日志的等级： debug、info、warn、error 或 fatal (默认为 info) | `lightning.log-level` |
| -f *rule* | [表库过滤的规则](/table-filter.md) (可多次指定) | `mydumper.filter` |
| --backend [*backend*](/tidb-lightning/tidb-lightning-overview.md) | 选择导入的模式：`local`为 Physical Import Mode，`tidb`为 Logical Import Mode  | `local` |
| --log-file *file* | 日志文件路径（默认值为 `/tmp/lightning.log.{timestamp}`，设置为 '-' 表示日志输出到终端） | `lightning.log-file` |
| --status-addr *ip:port* | TiDB Lightning 服务器的监听地址 | `lightning.status-port` |
| --importer *host:port* | TiKV Importer 的地址 | `tikv-importer.addr` |
| --pd-urls *host:port* | PD endpoint 的地址 | `tidb.pd-addr` |
| --tidb-host *host* | TiDB Server 的 host | `tidb.host` |
| --tidb-port *port* | TiDB Server 的端口（默认为 4000） | `tidb.port` |
| --tidb-status *port* | TiDB Server 的状态端口的（默认为 10080） | `tidb.status-port` |
| --tidb-user *user* | 连接到 TiDB 的用户名 | `tidb.user` |
| --tidb-password *password* | 连接到 TiDB 的密码，可为明文或 Base64 编码 | `tidb.password` |
| --enable-checkpoint *bool* | 是否启用断点 (默认值为 true) | `checkpoint.enable` |
| --analyze *level* | 导入后分析表信息，可选值为 required、optional（默认值）、off | `post-restore.analyze` |
| --checksum *level* | 导入后比较校验和，可选值为 required（默认值）、optional、off | `post-restore.checksum` |
| --check-requirements *bool* | 开始之前检查集群版本兼容性（默认值为 true）| `lightning.check-requirements` |
| --ca *file* | TLS 连接的 CA 证书路径 | `security.ca-path` |
| --cert *file* | TLS 连接的证书路径 | `security.cert-path` |
| --key *file* | TLS 连接的私钥路径 | `security.key-path` |
| --server-mode | 在服务器模式下启动 TiDB Lightning | `lightning.server-mode` |

如果同时对命令行参数和配置文件中的对应参数进行更改，命令行参数将优先生效。例如，在 `cfg.toml` 文件中，不管对日志等级做出什么修改，运行 `./tidb-lightning -L debug --config cfg.toml` 命令总是将日志级别设置为 “debug”。

### `tidb-lightning-ctl`

使用 `tidb-lightning-ctl` 可以对下列参数进行配置：

| 参数 | 描述 |
|:----|:----------|
| --compact | 执行 full compact |
| --switch-mode *mode* | 将每个 TiKV Store 切换到指定模式（normal 或 import） |
| --fetch-mode | 打印每个 TiKV Store 的当前模式 |
| --import-engine *uuid* | 将 TiKV Importer 上关闭的引擎文件导入到 TiKV 集群 |
| --cleanup-engine *uuid* | 删除 TiKV Importer 上的引擎文件 |
| --checkpoint-dump *folder* | 将当前的断点以 CSV 格式存储到文件夹中 |
| --checkpoint-error-destroy *tablename* | 删除断点，如果报错则删除该表 |
| --checkpoint-error-ignore *tablename* | 忽略指定表中断点的报错 |
| --checkpoint-remove *tablename* | 无条件删除表的断点 |

*tablename* 必须是`` `db`.`tbl` `` 中的限定表名（包括反引号），或关键词 `all`。

此外，上表中所有 `tidb-lightning` 的参数也适用于 `tidb-lightning-ctl`。
