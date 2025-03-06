---
title: TiDB Lightning 配置参数
summary: 使用配置文件或命令行配置 TiDB Lightning。
aliases: ['/docs-cn/dev/tidb-lightning/tidb-lightning-configuration/','/docs-cn/dev/reference/tools/tidb-lightning/config/']
---

# TiDB Lightning 配置参数

你可以使用配置文件或命令行配置 TiDB Lightning。本文主要介绍 TiDB Lightning 的全局配置、任务配置，以及如何使用命令行进行参数配置。你可以在 [`lightning/tidb-lightning.toml`](https://github.com/pingcap/tidb/blob/master/lightning/tidb-lightning.toml) 找到配置文件示例。

TiDB Lightning 的配置文件分为“全局”和“任务”两种类别，二者在结构上兼容。只有当[服务器模式](/tidb-lightning/tidb-lightning-web-interface.md)开启时，全局配置和任务配置才会有区别；默认情况下，服务器模式为禁用状态，此时 TiDB Lightning 只会执行一个任务，且全局和任务配置使用同一配置文件。

## TiDB Lightning 全局配置

### lightning

#### `status-addr`

- 用于在 Web 界面显示任务进度、拉取 Prometheus 监控指标、暴露调试数据，以及提交导入任务（服务器模式下）的 HTTP 端口。
- 将其设置为 `0` 可禁用该功能。

<!-- 示例值：`:8289` -->

#### `server-mode`

- 设置服务器模式。
- 默认值：`false`
- 可选值：
    - `false`：命令启动后会开始导入任务。
    - `true`：命令启动后，会等待用户在 Web 界面上提交任务。详情参见 [TiDB Lightning Web 界面](/tidb-lightning/tidb-lightning-web-interface.md)。

#### `level`

- 示例值：`"info"`

#### `file`

- 示例值：`"tidb-lightning.log"`

#### `max-size`

- 示例值：`128` <!-- MB -->

#### `max-days`

- 示例值：`28`

#### `max-backups`

- 示例值：`14`

#### `enable-diagnose-logs` <span class="version-mark">从 v7.3.0 版本开始引入</span>

- 设置是否开启诊断日志。
- 默认值：`false`
- 可选值：
    - `false`：即只输出和导入有关的日志，不会输出依赖的其他组件的日志。
    - `true`：既输出和导入相关的日志，也输出依赖的其他组件的日志，并开启 GRPC debug，可用于问题诊断。

## TiDB Lightning 任务配置

### lightning

#### `check-requirements`

- 启动之前检查集群是否满足最低需求，以及运行过程中检查 TiKV 的可用存储空间是否大于 10%。

<!-- 示例值：`true` -->

#### `index-concurrency`

- 索引引擎的最大并行数。每张表被切分成一个用于存储索引的“索引引擎”和若干存储行数据的“数据引擎”。`index-concurrency` 和 `table-concurrency` 这两项设置控制两种引擎文件的最大并发数。通常情况下使用默认值。

<!-- 示例值：`2` -->

#### `table-concurrency`

- 数据引擎的最大并行数。每张表被切分成一个用于存储索引的“索引引擎”和若干存储行数据的“数据引擎”。`index-concurrency` 和 `table-concurrency` 这两项设置控制两种引擎文件的最大并发数。通常情况下使用默认值。

<!-- 示例值：`6` -->

#### `region-concurrency`

- 数据的并发数。混合部署的情况下可以将其大小配置为逻辑 CPU 数的 75%，以限制 CPU 的使用。
- 默认值：与逻辑 CPU 的数量相同

#### `io-concurrency`

- I/O 最大并发数。I/O 并发量太高时，会因硬盘内部缓存频繁被刷新而增加 I/O 等待时间，导致缓存未命中和读取速度降低。对于不同的存储介质，你可能需要调整此参数以达到最佳效率。

<!-- 示例值：`5` -->

#### `max-error`

- TiDB Lightning 停止迁移任务之前能容忍的最大非严重错误 (non-fatal errors) 的数量。
- 在忽略非严重错误所在的行数据之后，迁移任务可以继续执行。
- 将该值设置为 N，表示 TiDB Lightning 会在遇到第 (N+1) 个错误时停止迁移任务。
- 被忽略的行会被记录到位于目标集群的 `task info` 数据库中。
- 默认值：MaxInt64 字节，即 `9223372036854775807` 字节

#### `task-info-schema-name`

- 指定用于存储 TiDB Lightning 执行结果的数据库。
- 将值设置为空字符串可以关闭该功能。

<!-- 示例值：`'lightning_task_info'` -->

#### `meta-schema-name`

- 在[并行导入模式](/tidb-lightning/tidb-lightning-distributed-import.md)下，在目标集群保存各个 TiDB Lightning 实例元信息的 schema 名字。如果未开启并行导入模式，无须设置此配置项。
- 对于参与同一批并行导入的每个 TiDB Lightning 实例，该参数设置的值必须相同，否则将无法确保导入数据的正确性。
- 如果开启并行导入模式，需要确保执行导入操作的用户（对于 `tidb.user` 配置项）有权限创建和访问此配置对应的库。
- TiDB Lightning 在导入完成后会删除此 schema，因此不要使用已存在的库名配置该参数。
- 默认值：`"lightning_metadata"`

### security

指定集群中用于 TLS 连接的证书和密钥。

#### `ca-path`

- CA 的公钥证书。如果留空，则禁用 TLS。

<!-- 示例值：`"/path/to/ca.pem"` -->

#### `cert-path`

- 此服务的公钥证书。

<!-- 示例值：`"/path/to/lightning.pem"` -->

#### `key-path`

- 该服务的密钥。

<!-- 示例值：`"/path/to/lightning.key"` -->

### checkpoint

#### `enable`

- 是否启用断点续传。
- 导入数据时，TiDB Lightning 会记录当前表导入的进度，所以即使 TiDB Lightning 或其他组件异常退出，在重启时也可以避免重复再导入已完成的数据。

<!-- 示例值：`true` -->

#### `schema`

- 存储断点的数据库名称。

<!-- 示例值：`"tidb_lightning_checkpoint"` -->

#### `driver`

- 存储断点的方式。
- 可选值：
    - `"file"`：存放在本地文件系统
    - `"mysql"`：存放在兼容 MySQL 的数据库服务器

#### `dsn`

- 数据源名称 (data source name)，表示断点的存放位置。
- 若 `driver = "file"`，则 `dsn` 为断点信息存放的文件路径。若不设置该路径，则默认存储路径为 `/tmp/CHECKPOINT_SCHEMA.pb`。
- 若 `driver = "mysql"`，则 `dsn` 为 `username:password@tcp(host:port)/` 格式的 URL。
- 若不设置该 URL，则默认会使用 `[tidb]` 部分指定的 TiDB 服务器来存储断点。
- 为减少目标 TiDB 集群的压力，建议指定另一台兼容 MySQL 的数据库服务器来存储断点。

<!-- 示例值：`"/tmp/tidb_lightning_checkpoint.pb"` -->

#### `keep-after-success`

- 所有数据导入成功后是否保留断点。设置为 `false` 时为删除断点。
- 保留断点有利于进行调试，但会泄漏关于数据源的元数据。

<!-- 示例值：`false` -->

### conflict

#### `strategy`

- 从 v7.3.0 开始引入的新版冲突数据处理策略。从 v8.0.0 开始，TiDB Lightning 优化了物理导入模式和逻辑导入模式的冲突策略。
- 默认值：`""`
- 可选值：
    - `""`：不同的导入模式下，设置该选项的结果不同：
        - 在物理导入模式下，不进行冲突数据检测和处理。如果源文件存在主键或唯一键冲突的记录，后续步骤会报错。
        - 在逻辑导入模式下，`""` 策略将被转换为 `"error"` 策略处理。
    - `"error"`：检测到导入的数据存在主键或唯一键冲突的数据时，终止导入并报错。
    - `"replace"`：遇到主键或唯一键冲突的数据时，保留最新的数据，覆盖旧的数据。
        - 使用物理导入模式时，冲突数据将被记录到目标 TiDB 集群中的 `lightning_task_info.conflict_view` 视图中。
        - 在 `lightning_task_info.conflict_view` 视图中，如果某行的 `is_precheck_conflict` 字段为 `0`，表示该行记录的冲突数据是通过后置冲突检测发现的；如果某行的 `is_precheck_conflict` 字段为 `1`，表示该行记录的冲突数据是通过前置冲突检测发现的。你可以根据业务需求选择正确的记录重新手动写入到目标表中。
        - 注意，该方法要求目标 TiKV 的版本为 v5.2.0 或更新版本。
    - `"ignore"`：遇到主键或唯一键冲突的数据时，保留旧的数据，忽略新的数据。该选项仅适用于逻辑导入模式。

#### `precheck-conflict-before-import`

- 控制是否开启前置冲突检测，即导入数据到 TiDB 前，先检查将要导入的数据是否存在冲突。该参数仅适用于物理导入模式。
- 在冲突记录数量高于 1,000,000 的场景中，建议开启前置冲突检测，可以提升冲突检测的性能。
- 在冲突记录数量少于 1,000,000 的场景中，建议关闭前置冲突检测。
- 默认值：`false`
- 可选值：
    - `false`：仅开启后置冲突检测。
    - `true`：同时开启前置冲突检测和后置冲突检测。

#### `threshold`

- 控制 [`strategy`](#strategy) 为 `"replace"` 或 `"ignore"` 时，能处理的冲突错误数的上限。仅在 `strategy` 为 `"replace"` 或 `"ignore"` 时可配置。
- 注意如果设置的值大于 `10000`，导入过程可能会出现性能下降的情况。
- 默认值：`10000`

#### `max-record-rows`

- 控制冲突数据记录表 (`conflict_records`) 中记录的冲突数据的条数上限。
- 从 v8.1.0 开始，TiDB Lightning 会自动将该配置项的值设置为 [`threshold`](#threshold) 的值，并忽略用户输入，因此无需再单独配置该配置项。
- `max-record-rows` 将在未来版本中废弃。
- 在物理导入模式下，当 `strategy` 为 `"replace"` 时会记录被覆盖的冲突记录。
- 在逻辑导入模式下，当 `strategy` 为 `"ignore"` 时会记录被忽略写入的冲突记录。当 `strategy` 为 `"replace"` 时，不会记录冲突记录。
- 默认值：`10000`

### tikv-importer

#### `backend`

- 设置 TiDB Lightning 导入数据的模式。
- 默认值：`"local"`
- 可选值：
    - `"local"`：[物理导入模式 (Physical Import Mode)](/tidb-lightning/tidb-lightning-physical-import-mode.md)。适用于导入 TiB 级以上的数据量。采用该导入模式时，在数据导入期间，下游 TiDB 无法对外提供服务。
    - `"tidb"`：[逻辑导入模式 (Logical Import Mode)](/tidb-lightning/tidb-lightning-logical-import-mode.md)。适用于导入 TiB 级以下的数据量。采用该导入模式时，在数据导入期间，下游 TiDB 仍可正常提供服务。

#### `parallel-import`

- 是否允许启动多个 TiDB Lightning 实例（物理导入模式）[并行导入数据](/tidb-lightning/tidb-lightning-distributed-import.md)到一个或多个目标表。该参数仅限目标表为空的场景使用。
- 默认值：`false`
- 可选值：`true`、`false`
- 多个 TiDB Lightning 实例（物理导入模式）同时导入一张表时，此开关必须设置为 `true`。但前提是目标表不能存在数据，即所有的数据都只能是由 TiDB Lightning 导入。

#### `duplicate-resolution`

> **警告：**
>
> 从 v8.0.0 开始，`duplicate-resolution` 被废弃，并将在未来版本中被移除。详情参考[旧版冲突检测](/tidb-lightning/tidb-lightning-physical-import-mode-usage.md#旧版冲突检测从-v800-开始已被废弃)。

- 物理导入模式设置是否检测和解决重复的记录（唯一键冲突）。
- 默认值：`'none'`
- 可选值：
    - `'none'`：不检测重复记录。如果数据源存在重复记录，会导致 TiDB 中出现数据不一致的情况。如果 `duplicate-resolution` 设置为 `'none'` 且 `conflict.strategy` 未设置，TiDB Lightning 会自动将 `conflict.strategy` 赋值为 `""`。
    - `'remove'`：如果 `duplicate-resolution` 设置为 `'remove'` 且 `conflict.strategy` 未设置，TiDB Lightning 会自动将 `conflict.strategy` 赋值为 `"replace"` 开启新版冲突检测。

#### `send-kv-pairs`

> **警告：**
>
> 从 v7.2.0 开始，该参数废弃，设置后不再生效。如果希望调整一次请求中向 TiKV 发送的数据量，请使用 [`send-kv-size`](#send-kv-size-从-v720-版本开始引入) 参数。

- 物理导入模式下，向 TiKV 发送数据时一次请求中最大 KV 数量。

<!-- 示例值：32768 -->

#### `send-kv-size` <span class="version-mark">从 v7.2.0 版本开始引入</span>

- 物理导入模式下，向 TiKV 发送数据时一次请求的最大大小。一般情况下不建议调整该参数。
- 默认值：`"16K"`

#### `compress-kv-pairs`

- 物理导入模式下，向 TiKV 发送 KV 时是否启用压缩。
- 目前仅支持 Gzip 压缩算法，可填写 `"gzip"` 或 `"gz"`。
- 默认值：`""`，即不启用压缩。
- 可选值：`""`、`"gzip"`、`"gz"`

#### `sorted-kv-dir`

- 物理导入模式本地进行 KV 排序的路径。如果磁盘性能较低（如使用机械盘），建议设置成与 `data-source-dir` 不同的磁盘以提升导入性能。

#### `range-concurrency`

- 物理导入模式 TiKV 写入 KV 数据的并发度。
- 当 TiDB Lightning 和 TiKV 直接网络传输速度超过万兆的时候，可以适当增加这个值。

<!-- 示例值：`16` -->

#### `store-write-bwlimit`

- 物理导入模式限制 TiDB Lightning 向每个 TiKV 节点写入的带宽大小。
- 默认值：`0`，表示不限制

#### `disk-quota`

- 使用物理导入模式时，配置 TiDB Lightning 本地临时文件使用的磁盘配额 (disk quota)。
- 当磁盘配额不足时，TiDB Lightning 会暂停读取源数据以及写入临时文件的过程，优先将已经完成排序的 key-value 写入到 TiKV，TiDB Lightning 删除本地临时文件后，再继续导入过程。
- 需要同时配合把 [`backend`](#backend) 设置为 `local` 模式才能生效。
- 默认值：`MaxInt64` 字节（9223372036854775807 字节）

#### `add-index-by-sql`

- 物理导入模式是否通过 SQL 方式添加索引。
- 通过 SQL 方式添加索引的优点是将导入数据与导入索引分开，可以快速导入数据，即使导入数据后，索引添加失败，也不会影响数据的一致性。
- 默认值：`false`
- 可选值：
    - `false`：TiDB Lightning 会将行数据以及索引数据都编码成 KV pairs 后一同导入 TiKV，实现机制和历史版本保持一致。
    - `true`：TiDB Lightning 会在导入数据完成后，使用 `ADD INDEX` 的 SQL 来添加索引。

#### `keyspace-name`

- 在使用 TiDB Lightning 导入多租户的 TiDB 集群的场景下，指定对应的 key space 名称。
- 默认值：`""`，表示 TiDB Lightning 会自动获取导入数据对应租户的 key space 名称。
- 如果指定了值，则使用指定的 key space 名称导入数据。

#### `pause-pd-scheduler-scope` <span class="version-mark">从 v7.1.0 版本开始引入</span>

- 物理导入模式下，用于控制 TiDB Lightning 暂停 PD 调度的范围。
- 默认值：`"table"`
- 可选值：
    - `"table"`：仅暂停目标表数据所在 Region 的调度。该选项仅适用于 TiDB v6.1.0 及以上版本的目标集群。
    - `"global"`：暂停全局调度。当导入数据到无业务流量的集群时，建议设置为 `"global"`，以避免其他调度的干扰。

#### `region-split-batch-size` <span class="version-mark">从 v7.1.0 版本开始引入</span>

- 物理导入模式下，用于控制批量 Split Region 时的 Region 个数。
- 每个 TiDB Lightning 实例最多同时 Split Region 的个数为：`region-split-batch-size * region-split-concurrency * table-concurrency`
- 默认值：`4096`

#### `region-split-concurrency` <span class="version-mark">从 v7.1.0 版本开始引入</span>

- 物理导入模式下，用于控制 Split Region 时的并发度。
- 默认值：CPU 核数

#### `region-check-backoff-limit` <span class="version-mark">从 v7.1.0 版本开始引入</span>

- 物理导入模式下，用于控制 split 和 scatter 操作后等待 Region 上线的重试次数。
- 重试符合指数回退策略，最大重试间隔为 2 秒。若两次重试之间有任何 Region 上线，该次操作不会被计为重试次数。
- 默认值：`1800`

#### `block-size` <span class="version-mark">从 v7.6.0 版本开始引入</span>

- 物理导入模式下，用于控制本地文件排序的 I/O 区块大小。当 IOPS 成为瓶颈时，你可以调大该参数的值以缓解磁盘 IOPS，从而提升数据导入性能。
- 取值必须大于或等于 `1B`。注意，如果仅指定数字（如 `16`），则单位为 Byte 而不是 KiB。
- 默认值：`"16KiB"`

#### `logical-import-batch-size` <span class="version-mark">从 v8.0.0 版本开始引入</span>

- 在逻辑导入模式下，用于设置下游 TiDB 服务器上执行的每条 SQL 语句的最大值。
- 该参数指定了单个事务中执行的每个 `INSERT` 或 `REPLACE` 语句的 `VALUES` 部分的期望最大大小。
- 该参数不是一个严格限制。实际执行的 SQL 语句长度可能会根据导入数据的具体内容而有所不同。
- 默认值：`"96KiB"`，在 TiDB Lightning 是集群中唯一的客户端时，这是导入速度的最佳值。
- 由于 TiDB Lightning 的实现限制，该参数最大值为 `"96KiB"`。设置更大的值不会生效。你可以减小该值以减轻大事务对集群的压力。

#### `logical-import-batch-rows` <span class="version-mark">从 v8.0.0 版本开始引入</span>

- 在逻辑导入模式下，限制每个事务中可插入的最大行数。
- 当同时指定 [`logical-import-batch-size`](#logical-import-batch-size-从-v800-版本开始引入) 和 `logical-import-batch-rows` 时，首先达到阈值的参数将生效。
- 你可以减小该值以减轻大事务对集群的压力。
- 默认值：`65536`

#### `logical-import-prep-stmt`

- 在逻辑导入模式下，控制是否使用[预处理语句](/sql-statements/sql-statement-prepare.md)和语句缓存来提高性能。
- 默认值：`false`

### mydumper

#### `read-block-size`

- 设置文件读取的区块大小，确保该值比数据源的最长字符串长。
- 默认值：`"64KiB"`

#### `batch-import-ratio`

- 引擎文件需按顺序导入。由于并行处理，多个数据引擎几乎同时被导入，这样形成的处理队列会造成资源浪费。因此，为了合理分配资源，TiDB Lightning 稍微增大了前几个区块的大小。
- 该参数用于设置在完全并发下，导入和写入过程的持续时间比。该值可以通过计算 1 GiB 大小的单张表的（导入时长/写入时长）得到。你可以在日志文件中查看精确的时间。
- 如果导入更快，区块大小的差异就会更小。比值为 `0` 表示区块大小相同。
- 取值范围：`[0, 1)`

<!-- 示例值：`0.75` -->

#### `data-source-dir`

- 本地源数据目录或外部存储 URI。关于外部存储 URI 详情可参考 [URI 格式](/br/backup-and-restore-storages.md#uri-格式)。

<!-- 示例值：`"/data/my_database"` -->

#### `character-set`

- 指定包含 `CREATE TABLE` 语句的表结构文件的字符集。
- 默认值：`"auto"`
- 可选值：
    - `"auto"`：自动判断文件编码是 UTF-8 还是 GB-18030，两者皆非则会报错
    - `"utf8mb4"`：表结构文件必须使用 UTF-8 编码，否则会报错
    - `"gb18030"`：表结构文件必须使用 GB-18030 编码，否则会报错
    - `"latin1"`：源数据文件使用 MySQL latin1 字符集编码（也被称为 Code Page 1252）
    - `"binary"`：不尝试转换编码

#### `data-character-set`

- 指定源数据文件的字符集，TiDB Lightning 会在导入过程中将源文件从指定的字符集转换为 UTF-8 编码。
- 该配置项目前仅用于指定 CSV 文件的字符集。留空此配置将默认使用 `"binary"`，即不尝试转换编码。
- TiDB Lightning 不会对源数据文件的字符集做假定，仅会根据此配置对数据进行转码并导入。
- 如果字符集设置与源数据文件的实际编码不符，可能会导致导入失败、导入缺失或导入数据乱码。
- 默认值：`"binary"`
- 可选值：
    - `"binary"`：不尝试转换编码
    - `"utf8mb4"`：源数据文件使用 UTF-8 编码
    - `"GB18030"`：源数据文件使用 GB-18030 编码
    - `"GBK"`：源数据文件使用 GBK 编码（GBK 编码是对 GB-2312 字符集的拓展，也被称为 Code Page 936）
    - `"latin1"`：源数据文件使用 MySQL latin1 字符集编码（也被称为 Code Page 1252）

#### `data-invalid-char-replace`

- 指定在源数据文件的字符集转换过程中，出现不兼容字符时的替换字符。
- 此项不可与字段分隔符、引用界定符和换行符号重复。改变默认值可能会导致潜在的源数据文件解析性能下降。
- 默认值：`"\uFFFD"`，即 UTF-8 编码中的 "error" Rune 或 Unicode replacement character

#### `strict-format`

- 启用[严格格式](/tidb-lightning/tidb-lightning-data-source.md#启用严格格式)可加快导入数据的速度。为保证数据安全而非追求处理速度，默认值为 `false`，即关闭严格格式。
- 默认值：`false`
- 可选值：`true`、`false`
- 当设置为 `true` 开启严格格式时，有如下限制：
    - 在 CSV 文件的所有记录中，每条数据记录的值不可包含字符换行符（`U+000A` 和 `U+000D`，即 `\r` 和 `\n`）甚至被引号包裹的字符换行符都不可包含，即换行符只可用来分隔行。
    - 导入数据源为严格格式时，TiDB Lightning 会快速定位大文件的分割位置进行并行处理。但是如果输入数据为非严格格式，可能会将一条完整的数据分割成两部分，导致结果出错。

#### `max-region-size`

- 如果严格模式 [`strict-format`](#strict-format) 设置为 `true`，TiDB Lightning 会将 CSV 大文件分割为多个文件块进行并行处理。`max-region-size` 用于设置分割后每个文件块的最大大小。
- 默认值：`"256MiB"`

#### `filter`

- 只导入与该通配符规则相匹配的表。

<!-- 示例值：`['*.*', '!mysql.*', '!sys.*', '!INFORMATION_SCHEMA.*', '!PERFORMANCE_SCHEMA.*', '!METRICS_SCHEMA.*', '!INSPECTION_SCHEMA.*']` -->

### mydumper.csv

配置 CSV 文件的解析方式。

#### `separator`

- 字段分隔符，支持一个或多个字符。
- 默认值：`','`

#### `delimiter`

- 引用定界符，设置为空表示字符串未加引号。
- 默认值：`'"'`

#### `terminator`

- 行尾定界字符，支持一个或多个字符。
- 默认值：`""`，表示 `"\n"`（换行）和 `"\r\n"`（回车+换行），均表示行尾

#### `header`

- CSV 文件是否包含表头。
- 可选值：
    - `true`：将把首行的内容作为表头处理，不作为数据导入。
    - `false`：首行也作为 CSV 数据导入，此时请确保 CSV 文件的列顺序与目标表的列顺序一致，否则可能会导致数据差异。

#### `header-schema-match`

- CSV 表头是否匹配目标表的表结构。
- 默认为 `true`，表示在导入数据时，会根据 CSV 表头的字段名去匹配目标表对应的列名，这样即使 CSV 文件和目标表列的顺序不一致也能按照对应的列名进行导入。
- 如果 CSV 表头中的字段名和目标表的列名不匹配（例如，CSV 表头中的某些字段名在目标表中可能找不到对应的同名列）但列的顺序是一致的，请将该配置设置为 `false`。这时，在导入的时候，会直接忽略 CSV 表头的内容，以避免导入错误。在这种情况下，直接把 CSV 数据按照目标表列的顺序导入。因此，如果列的顺序不一致，请手动调整一致后再导入，否则可能会导致数据差异。
- 默认值：`true`
- 可选值：`true`、`false`

> **注意：**
>
> 只有在 `header = true` 时，该参数才会生效。如果 `header = false`，表示 CSV 文件没有表头，此时不需要考虑相关列名匹配的问题。

#### `not-null`

- CSV 文件是否包含 NULL。
- 可选值：
    - `true`：CSV 所有列都不能解析为 NULL。
    - `false`：CSV 可以包含 NULL。

#### `null`

- 如果 `not-null` 设置为 `false`，即 CSV 可以包含 NULL，为 `null` 指定的值的字段将会被解析为 NULL。

<!-- 示例值：`'\N'` -->

#### `backslash-escape`

- 是否对字段内 `\` 进行转义。

<!-- 示例值：`true` -->

#### `trim-last-separator`

- 如果有行以分隔符结尾，是否删除尾部分隔符。

<!-- 示例值：`false` -->

### mydumper.files

#### `pattern`

- 解析 AWS Aurora Parquet 文件所需的表达式。
- 示例值：`'(?i)^(?:[^/]*/)*([a-z0-9_]+)\.([a-z0-9_]+)/(?:[^/]*/)*(?:[a-z0-9\-_.]+\.(parquet))$'`

#### `schema`

- 示例值：`'$1'`

#### `table`

- 示例值：`'$2'`

#### `type`

- 示例值：`'$3'`

### tidb

#### `host`

- 目标集群的信息。tidb-server 的地址，填一个即可。

<!-- 示例值：`"172.16.31.1"` -->

#### `port`

- 示例值：`4000`

#### `user`

- 示例值：`"root"`

#### `password`

- 设置连接 TiDB 的密码，可为明文或 Base64 编码。

#### `status-port`

- 表结构信息从 TiDB 的 `status-port` 获取。

<!-- 示例值：`10080` -->

#### `pd-addr`

- pd-server 的地址，从 v7.6.0 开始支持设置多个地址。

<!-- 示例值：`"172.16.31.4:2379,56.78.90.12:3456"` -->

#### `log-level`

- 设置 TiDB 库的日志等级。TiDB Lightning 引用了 TiDB 库，并生成日志。

<!-- 示例值：`"error"` -->

#### `build-stats-concurrency`

- 设置 TiDB 会话变量，提升 Checksum 和 Analyze 的速度。详情参考[控制 `ANALYZE` 并发度](/statistics.md#控制-analyze-并发度)。

<!-- 示例值：`20` -->

#### `distsql-scan-concurrency`

- 设置 TiDB 会话变量，提升 Checksum 和 Analyze 的速度。详情参考[控制 `ANALYZE` 并发度](/statistics.md#控制-analyze-并发度)。
- 如果将 [`checksum-via-sql`](#checksum-via-sql) 设置为 `"true"`，则会通过 TiDB 执行 `ADMIN CHECKSUM TABLE <table>` SQL 语句来进行 Checksum 操作。在这种情况下，`distsql-scan-concurrency` 参数设置不会生效。

<!-- 示例值：`15` -->

#### `index-serial-scan-concurrency`

- 设置 TiDB 会话变量，提升 Checksum 和 Analyze 的速度。详情参考[控制 `ANALYZE` 并发度](/statistics.md#控制-analyze-并发度)。

<!-- 示例值：`20` -->

#### `checksum-table-concurrency`

- 设置 TiDB 会话变量，提升 Checksum 和 `ANALYZE` 的速度。详情参考[控制 `ANALYZE` 并发度](/statistics.md#控制-analyze-并发度)。
- 如果将 [`checksum-via-sql`](#checksum-via-sql) 设置为 `"true"`，则会通过 TiDB 执行 `ADMIN CHECKSUM TABLE <table>` SQL 语句来进行 Checksum 操作。在这种情况下，`checksum-table-concurrency` 参数设置不会生效。

<!-- 示例值：`2` -->

#### `sql-mode`

- 解析和执行 SQL 语句的默认 SQL 模式。

<!-- 示例值：`"ONLY_FULL_GROUP_BY,NO_AUTO_CREATE_USER"` -->

#### `max-allowed-packet`

- 设置数据库连接允许的最大数据包大小，对应于系统参数中的 `max_allowed_packet`。
- 如果设置为 `0`，会使用下游数据库 global 级别的 `max_allowed_packet`。

<!-- 示例值：`67_108_864` -->

#### `tls`

- SQL 连接是否使用 TLS。
- 可选值：
    * `""`：如果填充了 [`[tidb.security]`](#tidbsecurity) 部分，则强制使用 TLS（与 `"cluster"` 情况相同），否则与 `"false"` 情况相同
    * `"false"`：禁用 TLS
    * `"cluster"`：强制使用 TLS 并使用 [`[tidb.security]`](#tidbsecurity) 部分中指定的 CA 验证服务器的证书
    * `"skip-verify"`：强制使用 TLS，但不验证服务器的证书（不安全）
    * `"preferred"`：与 `"skip-verify"` 相同，但是如果服务器不支持 TLS，则会退回到未加密的连接

### tidb.security

- 指定证书和密钥用于 TLS 连接 MySQL。
- 默认值：[`security`](#security) 部分的副本。

#### `ca-path`

- CA 的公钥证书。设置为空字符串可禁用 SQL 的 TLS。

<!-- 示例值：`"/path/to/ca.pem"` -->

#### `cert-path`

- 该服务的公钥证书。
- 默认值：[`security.cert-path`](#cert-path) 的副本。

<!-- 示例值：`"/path/to/lightning.pem"` -->

#### `key-path`

- 此服务的私钥。
- 默认值：[`security.key-path`](#key-path) 的副本。

<!-- 示例值：`"/path/to/lightning.key"` -->

### tidb.session-vars

设置其他 TiDB 会话变量。

<!-- tidb_enable_clustered_index = "OFF" -->

### post-restore

- 对于物理导入模式，数据导入完成后，TiDB Lightning 可以自动执行 Checksum 和 `ANALYZE` 操作。
- 在生产环境中，建议总是开启 Checksum 和 `ANALYZE`。
- 执行的顺序为：Checksum -> `ANALYZE`。
- 注意：对于逻辑导入模式，无须执行这两个阶段，因此在实际运行时总是会直接跳过。

#### `checksum`

- 配置是否在导入完成后对每一个表执行 `ADMIN CHECKSUM TABLE <table>` 操作来验证数据的完整性。
- 默认值：`"required"`，从 v4.0.8 开始，默认值由 `"true"` 改为 `"required"`
- 可选值：
    - `"required"`：在导入完成后执行 Checksum 检查，如果 Checksum 检查失败，则会报错退出
    - `"optional"`：在导入完成后执行 Checksum 检查，如果报错，会输出一条 WARN 日志并忽略错误
    - `"off"`：导入结束后不执行 Checksum 检查
- Checksum 对比失败通常表示导入异常（数据丢失或数据不一致），因此建议总是开启 Checksum。
- 考虑到与旧版本的兼容性，依然可以在本配置项设置 `true` 和 `false` 两个布尔值，其效果与 `required` 和 `off` 相同。

#### `checksum-via-sql`

- 设置是否通过 TiDB 执行 `ADMIN CHECKSUM TABLE <table>` 操作。
- 默认值：`"false"`
- 可选值：
    - `"false"`：表示通过 TiDB Lightning 下发 `ADMIN CHECKSUM TABLE <table>` 命令给 TiKV 执行。
    - `"true"`：当该值为 `"true"` 时，如果要调整并发，需要在 TiDB 中设置 [`tidb_checksum_table_concurrency`](/system-variables.md#tidb_checksum_table_concurrency) 系统变量。
- 建议将该值设为 `"true"`，以便在执行 Checksum 失败时更容易定位问题。

#### `analyze`

- 配置是否在 Checksum 结束后对所有表逐个执行 `ANALYZE TABLE <table>` 操作。
- 默认值：`"optional"`
- 可选值：`"required"`、`"optional"`、`"off"`

### cron

- 设置周期性后台操作
- 支持的单位：h（时）、m（分）、s（秒）

#### `switch-mode`

- TiDB Lightning 自动刷新导入模式状态的持续时间，该值应小于 TiKV 对应的设定值。

<!-- 示例值：`"5m"` -->

#### `log-progress`

- 在日志中打印导入进度的持续时间。

<!-- 示例值：`"5m"` -->

#### `check-disk-quota`

- 使用物理导入模式时，检查本地磁盘配额的时间间隔。
- 默认值：`"60s"`，即 60 秒
