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

# 是否开启诊断日志。默认为 false，即只输出和导入有关的日志，不会输出依赖的其他组件的日志。
# 设置为 true 后，既输出和导入相关的日志，也输出依赖的其他组件的日志，并开启 GRPC debug，可用于问题诊断。
# 该参数自 v7.3.0 开始引入。
enable-diagnose-logs = false
```

### TiDB Lightning 任务配置

```toml
### tidb-lightning 任务配置

[lightning]
# 启动之前检查集群是否满足最低需求，以及运行过程中检查 TiKV 的可用存储空间是否大于 10%。
# check-requirements = true

# 引擎文件的最大并行数。
# 每张表被切分成一个用于存储索引的“索引引擎”和若干存储行数据的“数据引擎”。
# 这两项设置控制两种引擎文件的最大并发数。通常情况下，你可以使用默认值。
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
# 若不设置该路径，则默认存储路径为“/tmp/CHECKPOINT_SCHEMA.pb”。
# 若 driver = "mysql"，则 dsn 为“用户:密码@tcp(地址:端口)/”格式的 URL。
# 若不设置该 URL，则默认会使用 [tidb] 部分指定的 TiDB 服务器来存储断点。
# 为减少目标 TiDB 集群的压力，建议指定另一台兼容 MySQL 的数据库服务器来存储断点。
# dsn = "/tmp/tidb_lightning_checkpoint.pb"

# 所有数据导入成功后是否保留断点。设置为 false 时为删除断点。
# 保留断点有利于进行调试，但会泄漏关于数据源的元数据。
# keep-after-success = false

[conflict]
# 从 v7.3.0 开始引入的新版冲突数据处理策略。默认值为 ""。从 v8.0.0 开始，TiDB Lightning 优化了物理导入模式和逻辑导入模式的冲突策略。
# - ""：在物理导入模式下，不进行冲突数据检测和处理。如果源文件存在主键或唯一键冲突的记录，后续步骤会报错。在逻辑导入模式下，"" 策略将被转换为 "error" 策略处理。
# - "error"：检测到导入的数据存在主键或唯一键冲突的数据时，终止导入并报错。
# - "replace"：遇到主键或唯一键冲突的数据时，保留最新的数据，覆盖旧的数据。
#              使用物理导入模式时，冲突数据将被记录到目标 TiDB 集群中的 `lightning_task_info.conflict_view` 视图中。
#              在 `lightning_task_info.conflict_view` 视图中，如果某行的 `is_precheck_conflict` 字段为 `0`，表示该行记录的冲突数据是通过后置冲突检测发现的；如果某行的 `is_precheck_conflict` 字段为 `1`，表示该行记录的冲突数据是通过前置冲突检测发现的。
#              你可以根据业务需求选择正确的记录重新手动写入到目标表中。注意，该方法要求目标 TiKV 的版本为 v5.2.0 或更新版本。
# - "ignore"：遇到主键或唯一键冲突的数据时，保留旧的数据，忽略新的数据。仅当导入模式为逻辑导入模式时可以使用该选项。
strategy = ""
# 控制是否开启前置冲突检测，即导入数据到 TiDB 前，先检查所需导入的数据是否存在冲突。该参数默认值为 false，表示仅开启后置冲突检测。取值为 true 时，表示同时开启前置冲突检测和后置冲突检测。仅当导入模式为物理导入模式时可以使用该参数。冲突记录数量高于 1,000,000 的场景建议配置 `precheck-conflict-before-import = true`，可以提升冲突检测的性能，反之建议关闭。
# precheck-conflict-before-import = false
# 控制 strategy 为 "replace" 或 "ignore" 时，能处理的冲突错误数的上限。仅在 strategy 为 "replace" 或 "ignore" 时可配置。默认为 10000。如果设置的值大于 10000，导入过程可能会出现性能下降的情况。
# threshold = 10000
# 控制冲突数据记录表 (`conflict_records`) 中记录的冲突数据的条数上限，默认为 10000。
# 从 v8.1.0 开始，TiDB Lightning 会自动将 `max-record-rows` 的值设置为 `threshold` 的值，并忽略用户输入，因此无需再单独配置 `max-record-rows`。`max-record-rows` 将在未来版本中废弃。
# 在物理导入模式下，当 strategy 为 "replace" 时会记录被覆盖的冲突记录。
# 在逻辑导入模式下，当 strategy 为 "ignore" 时会记录被忽略写入的冲突记录，当 strategy 为 "replace" 时，不会记录冲突记录。
# max-record-rows = 10000

[tikv-importer]
# "local"：物理导入模式（Physical Import Mode），默认使用。适用于 TB 级以上大数据量，但导入期间下游 TiDB 无法对外提供服务。
# "tidb"：逻辑导入模式 (Logical Import Mode)。TB 级以下数据量可以采用，下游 TiDB 可正常提供服务。
# backend = "local"
# 是否允许启动多个 TiDB Lightning 实例（物理导入模式）并行导入数据到一个或多个目标表。默认取值为 false。
# 注意，该参数仅限目标表为空的场景使用。
# 多个 TiDB Lightning 实例（物理导入模式）同时导入一张表时，此开关必须设置为 true。
# 但前提是目标表不能存在数据，即所有的数据都只能是由 TiDB Lightning 导入。
# parallel-import = false

# `duplicate-resolution` 参数从 v8.0.0 开始已被废弃，并将在未来版本中被移除。详情参考 <https://docs.pingcap.com/zh/tidb/stable/tidb-lightning-physical-import-mode-usage#旧版冲突检测从-v800-开始已被废弃>。
# 物理导入模式设置是否检测和解决重复的记录（唯一键冲突）。
# 目前支持两种解决方法：
#  - 'none'：不检测重复记录。
#          如果数据源存在重复记录，会导致 TiDB 中出现数据不一致的情况。
#          如果 `duplicate-resolution` 设置为 'none' 且 `conflict.strategy` 未设置，TiDB Lightning 会自动将 `conflict.strategy` 赋值为 ""。
#  - 'remove'：如果 `duplicate-resolution` 设置为 'remove' 且 `conflict.strategy` 未设置，TiDB Lightning 会自动将 `conflict.strategy` 赋值为 "replace" 开启新版冲突检测。
# 默认值为 'none'。
# duplicate-resolution = 'none'
# 物理导入模式下，向 TiKV 发送数据时一次请求中最大 KV 数量。
# 自 v7.2.0 开始，该参数废弃，设置后不再生效。如果希望调整一次请求中向 TiKV 发送的数据量，请使用 `send-kv-size` 参数。
# send-kv-pairs = 32768
# 物理导入模式下，向 TiKV 发送数据时一次请求的最大大小。
# 默认值为 "16K"，一般情况下不建议调整该参数。
# 该参数自 v7.2.0 开始引入。
# send-kv-size = "16K"
# 物理导入模式向 TiKV 发送 KV 时是否启用压缩。目前只支持 Gzip 压缩算法，可填写 "gzip" 或者 "gz"。默认不启用压缩。
# compress-kv-pairs = ""
# 物理导入模式本地进行 KV 排序的路径。如果磁盘性能较低（如使用机械盘），建议设置成与 `data-source-dir` 不同的磁盘，这样可有效提升导入性能。
# sorted-kv-dir = ""
# 物理导入模式TiKV 写入 KV 数据的并发度。当 TiDB Lightning 和 TiKV 直接网络传输速度超过万兆的时候，可以适当增加这个值。
# range-concurrency = 16
# 物理导入模式限制 TiDB Lightning 向每个 TiKV 节点写入的带宽大小，默认为 0，表示不限制。
# store-write-bwlimit = "128MiB"

# 使用物理导入模式时，配置 TiDB Lightning 本地临时文件使用的磁盘配额 (disk quota)。
# 当磁盘配额不足时，TiDB Lightning 会暂停读取源数据以及写入临时文件的过程，
# 优先将已经完成排序的 key-value 写入到 TiKV，TiDB Lightning 删除本地临时文件后，再继续导入过程。
# 需要同时配合把 `backend` 设置为 `local` 模式才能生效。
# 默认值为 MaxInt64 字节，即 9223372036854775807 字节。
# disk-quota = "10GB"

# 物理导入模式是否通过 SQL 方式添加索引。
# 默认为 `false`，表示 TiDB Lightning 会将行数据以及索引数据都编码成 KV pairs 后一同导入 TiKV，实现机制和历史版本保持一致。
# 如果设置为 `true`，即 TiDB Lightning 会在导入数据完成后，使用 add index 的 SQL 来添加索引。
# 通过 SQL 方式添加索引的优点是将导入数据与导入索引分开，可以快速导入数据，即使导入数据后，索引添加失败，也不会影响数据的一致性。
# add-index-by-sql = false

# 在使用 TiDB Lightning 导入多租户的 TiDB cluster 的场景下，指定对应的 key space 名称。
# 默认取值为空字符串，表示 TiDB Lightning 会自动获取导入对应租户的 key space 名称；
# 如果指定了值，则使用指定的 key space 名称来导入。
# keyspace-name = ""

# 物理导入模式下，用于控制 TiDB Lightning 暂停 PD 调度的范围，可选值包括：
# - "table"：仅暂停目标表数据所在 Region 的调度。默认值为 "table"。
# - "global"：暂停全局调度。当导入数据到无业务流量的集群时，建议设置为 "global"，以避免其他调度的干扰。
# 该参数自 v7.1.0 版本开始引入。注意："table" 选项仅适用于 TiDB v6.1.0 及以上版本的目标集群。
# pause-pd-scheduler-scope = "table"

# 物理导入模式下，用于控制批量 Split Region 时的 Region 个数。
# 每个 TiDB Lightning 实例最多同时 Split Region 的个数为：
# region-split-batch-size * region-split-concurrency * table-concurrency
# 该参数自 v7.1.0 版本开始引入，默认值为 `4096`。
# region-split-batch-size = 4096

# 物理导入模式下，用于控制 Split Region 时的并发度。默认值为 CPU 核数。
# 该参数自 v7.1.0 版本开始引入。
# region-split-concurrency =

# 物理导入模式下，用于控制 split 和 scatter 操作后等待 Region 上线的重试次数，默认值为 `1800`。
# 重试符合指数回退策略，最大重试间隔为 2 秒。
# 若两次重试之间有任何 Region 上线，该次操作不会被计为重试次数。
# 该参数自 v7.1.0 版本开始引入。
# region-check-backoff-limit = 1800

# 物理导入模式下，用于控制本地文件排序的 I/O 区块大小。当 IOPS 成为瓶颈时，你可以调大该参数的值以缓解磁盘 IOPS，从而提升数据导入性能。
# 该参数自 v7.6.0 版本开始引入。默认值为 "16KiB"。取值必须大于或等于 `1B`。注意，如果仅指定数字（如 `16`），则单位为 Byte 而不是 KiB。
# block-size = "16KiB"

# 在逻辑导入模式下，用于设置下游 TiDB 服务器上执行的每条 SQL 语句的最大值。
# 该参数自 v8.0.0 版本开始引入。
# 该参数指定了单个事务中执行的每个 INSERT 或 REPLACE 语句的 VALUES 部分的期望最大大小。
# 该参数不是一个严格限制。实际执行的 SQL 语句长度可能会根据导入数据的具体内容而有所不同。
# 默认值为 "96KiB"，在 TiDB Lightning 是集群中唯一的客户端时，这是导入速度的最佳值。
# 由于 TiDB Lightning 的实现细节，该参数最大值为 96 KiB。设置更大的值将不会生效。
# 你可以减小该值以减轻大事务对集群的压力。
# logical-import-batch-size = "96KiB"

# 在逻辑导入模式下，限制每个事务中可插入的最大行数。
# 该参数自 v8.0.0 版本开始引入。默认值为 65536 行。
# 当同时指定 `logical-import-batch-size` 和 `logical-import-batch-rows` 时，首先达到阈值的参数将生效。
# 你可以减小该值以减轻大事务对集群的压力。
# logical-import-batch-rows = 65536

# 在逻辑导入模式下，该参数控制是否使用预处理语句和语句缓存来提高性能。默认值为 `false`。
logical-import-prep-stmt = false

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
#  - latin1：源数据文件使用 MySQL latin1 字符集编码（也被称为 Code Page 1252）。
#  - binary：不尝试转换编码。
character-set = "auto"

# 指定源数据文件的字符集，Lightning 会在导入过程中将源文件从指定的字符集转换为 UTF-8 编码。
# 该配置项目前仅用于指定 CSV 文件的字符集。只支持下列选项：
#  - utf8mb4：源数据文件使用 UTF-8 编码。
#  - GB18030：源数据文件使用 GB-18030 编码。
#  - GBK：源数据文件使用 GBK 编码（GBK 编码是对 GB-2312 字符集的拓展，也被称为 Code Page 936）。
#  - latin1：源数据文件使用 MySQL latin1 字符集编码（也被称为 Code Page 1252）。
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

# 如果 strict-format = true，TiDB Lightning 会将 CSV 大文件分割为多个文件块进行并行处理。
# max-region-size 是分割后每个文件块的最大大小。
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
# 如果 header = true，将把首行的内容作为表头处理，不作为数据导入。如果设置为 false，首行也作为 CSV 数据导入，
# 此时请确保 CSV 文件的列顺序与目标表的列顺序一致，否则可能会导致数据差异。
header = true
# CSV 表头是否匹配目标表的表结构。
# 默认为 true，表示在导入数据时，会根据 CSV 表头的字段名去匹配目标表对应的列名，
# 这样即使 CSV 文件和目标表列的顺序不一致也能按照对应的列名进行导入。
# 如果 CSV 表头中的字段名和目标表的列名不匹配（例如，CSV 表头中的某些字段名在目标表中可能找不到对应的同名列）但列的顺序是一致的，
# 请将该配置设置为 false。
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
# pd-server 的地址，从 v7.6.0 开始支持设置多个地址。
pd-addr = "172.16.31.4:2379,56.78.90.12:3456"
# tidb-lightning 引用了 TiDB 库，并生成产生一些日志。
# 设置 TiDB 库的日志等级。
log-level = "error"

# 设置 TiDB 会话变量，提升 Checksum 和 Analyze 的速度。注意，如果将 checksum-via-sql 设置为 "true"，则会通过 TiDB 执行 ADMIN CHECKSUM TABLE <table> SQL 语句来进行 Checksum 操作。在这种情况下，以下参数设置 `distsql-scan-concurrency = 15` 和 `checksum-table-concurrency = 2` 将不会生效。
# 各参数定义可参阅 “控制 Analyze 并发度文档” (https://docs.pingcap.com/zh/tidb/stable/statistics#%E6%8E%A7%E5%88%B6-analyze-%E5%B9%B6%E5%8F%91%E5%BA%A6)。
build-stats-concurrency = 20
distsql-scan-concurrency = 15
index-serial-scan-concurrency = 20
checksum-table-concurrency = 2

# 解析和执行 SQL 语句的默认 SQL 模式。
sql-mode = "ONLY_FULL_GROUP_BY,NO_AUTO_CREATE_USER"
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

# 设置其他 TiDB 会话变量
# [tidb.session-vars]
# tidb_enable_clustered_index = "OFF"

# 对于物理导入模式，数据导入完成后，TiDB Lightning 可以自动执行 Checksum 和 Analyze 操作。
# 在生产环境中，建议总是开启 Checksum 和 Analyze。
# 执行的顺序为：Checksum -> Analyze。
# 注意：对于逻辑导入模式, 无须执行这两个阶段，因此在实际运行时总是会直接跳过。
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
# 设置是否通过 TiDB 执行 ADMIN CHECKSUM TABLE <table> 操作。
# 默认值为 "false"，表示通过 TiDB Lightning 下发 ADMIN CHECKSUM TABLE <table> 命令给 TiKV 执行。
# 建议将该值设为 "true"，以便在 checksum 失败时更容易定位问题。
# 同时，当该值为 "true" 时，如果需要调整并发，请在 TiDB 中设置 `tidb_checksum_table_concurrency` 变量 (https://docs.pingcap.com/zh/tidb/stable/system-variables#tidb_checksum_table_concurrency)。
checksum-via-sql = "false"
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

# 使用物理导入模式时，检查本地磁盘配额的时间间隔，默认为 60 秒。
# check-disk-quota = "60s"
```
