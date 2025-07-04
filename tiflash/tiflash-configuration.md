---
title: TiFlash 配置参数
aliases: ['/docs-cn/dev/tiflash/tiflash-configuration/','/docs-cn/dev/reference/tiflash/configuration/']
summary: 介绍 TiFlash 的配置参数，包括 tiflash.toml 和 tiflash-learner.toml，用于配置 TiFlash TCP/HTTP 服务的监听和存储路径。另外，通过拓扑 label 进行副本调度和多盘部署也是可行的。
---

# TiFlash 配置参数

本文介绍了与部署使用 TiFlash 相关的配置参数。

## TiFlash 配置参数

> **Tip:**
>
> 如果你需要调整配置项的值，请参考[修改配置参数](/maintain-tidb-using-tiup.md#修改配置参数)进行操作。

### 配置文件 tiflash.toml

#### `listen_host`

- TiFlash TCP/HTTP 等辅助服务的监听 host。
- 建议配置成 `"0.0.0.0"`，即监听本机所有 IP 地址。

#### `tcp_port`

- TiFlash TCP 服务的端口。TCP 服务为内部测试接口，默认使用 9000 端口。
- 在 TiFlash v7.1.0 之前的版本中，该端口默认开启，但存在安全风险。为了提高安全性，建议对该端口进行访问控制，只允许白名单 IP 访问。从 TiFlash v7.1.0 起，可以通过注释掉该端口的配置避免安全风险。当 TiFlash 配置文件未声明该端口时，该端口也不会开启。
- 建议在任何 TiFlash 的部署中都不配置该端口。从 TiFlash v7.1.0 起，由 TiUP >= v1.12.5 或 TiDB Operator >= v1.5.0 部署的 TiFlash 默认为安全版本，即默认未开启该端口。
- 默认值：`9000`

#### `mark_cache_size`

- 数据块元信息的内存 cache 大小限制，通常不需要修改。
- 默认值：`1073741824`

#### `minmax_index_cache_size`

- 数据块 min-max 索引的内存 cache 大小限制，通常不需要修改。
- 默认值：`1073741824`

#### `delta_index_cache_size`

- DeltaIndex 内存 cache 大小限制。
- 默认值：`0`，代表没有限制

#### `path`

- TiFlash 数据的存储路径。如果有多个目录，以英文逗号分隔。
- 从 v4.0.9 版本开始，不推荐使用 `path` 及 [`path_realtime_mode`](#path_realtime_mode) 参数。推荐使用 [`storage`](#storage-从-v409-版本开始引入) 下的配置项代替，这样在多盘部署的场景下能更好地利用节点性能。
- 从 v5.2.0 版本开始，如果要使用配置项 [`storage.io_rate_limit`](#storageio_rate_limit-从-v520-版本开始引入)，需要同时将 TiFlash 的数据存储路径设置为 [`storage.main.dir`](#dir)。
- 当 `storage` 配置项存在的情况下，`path` 及 [`path_realtime_mode`](#path_realtime_mode) 两个配置会被忽略。

<!-- 示例值：`"/tidb-data/tiflash-9000"` 或 `"/ssd0/tidb-data/tiflash,/ssd1/tidb-data/tiflash,/ssd2/tidb-data/tiflash"` -->

#### `path_realtime_mode`

- 如果设为 `true`，且 `path` 配置了多个目录，表示在第一个目录存放最新数据，在其他目录存放较旧的数据。
- 从 v4.0.9 版本开始，不推荐使用 [`path`](#path) 及 `path_realtime_mode` 参数。推荐使用 [`storage`](#storage-从-v409-版本开始引入) 下的配置项代替，这样在多盘部署的场景下能更好地利用节点性能。
- 当 `storage` 配置项存在的情况下，[`path`](#path) 及 `path_realtime_mode` 两个配置会被忽略。
- 默认值：`false`

#### `tmp_path`

- TiFlash 临时文件的存放路径。
- 默认使用 \[[`path`](#path) 或者 [`storage.latest.dir`](#dir-1) 的第一个目录\] + "/tmp"

<!-- 示例值：`"/tidb-data/tiflash-9000/tmp"` -->

#### storage <span class="version-mark">从 v4.0.9 版本开始引入</span>

存储路径相关配置。

##### `format_version`

- DTFile 储存文件格式
- 默认值：`7`
- 可选值：`2`、`3`、`4`、`5`、`6`、`7`
    - `format_version = 2`：v6.0.0 以前版本的默认文件格式
    - `format_version = 3`：v6.0.0 及 v6.1.x 版本的默认文件格式，具有更完善的检验功能
    - `format_version = 4`：v6.2.0 ~ v7.3.0 的默认文件格式，优化了写放大问题，同时减少了后台线程消耗
    - `format_version = 5`：v7.4.0 ~ v8.3.0 的默认文件格式（从 v7.3.0 开始引入），该格式可以合并小文件从而减少了物理文件数量
    - `format_version = 6`：从 v8.4.0 开始引入，部分支持了向量索引的构建与存储
    - `format_version = 7`：v8.4.0 及以后版本的默认文件格式（从 v8.4.0 开始引入），该格式用于支持向量索引的构建与存储

#### storage.main

##### `dir`

- 用于存储主要数据的路径，例如 `[ "/tidb-data/tiflash-9000" ]` 或 `[ "/ssd0/tidb-data/tiflash", "/ssd1/tidb-data/tiflash" ]`。
- 该目录列表中的数据占总数据的 90% 以上。

##### `capacity`

- [`storage.main.dir`](#dir) 存储目录列表中每个目录的最大可用容量。例如 `[10737418240, 10737418240]`。
- 在该配置项未配置或者列表中全为 `0` 时，会使用目录所在的硬盘容量。
- 单位：Byte。目前不支持如 `"10GB"` 的设置。
- `capacity` 列表的长度应当与 [`storage.main.dir`](#dir) 列表长度保持一致。

#### storage.latest

##### `dir`

- 用于存储最新的数据，大约占总数据量的 10% 以内，需要较高的 IOPS。
- 默认情况该项可留空，即 `[ ]`。在未配置或者为空列表的情况下，会使用 [`storage.main.dir`](#dir) 的值。

<!-- 示例值：`[]` -->

##### `capacity`

- [`storage.latest.dir`](#dir-1) 存储目录列表中，每个目录的最大可用容量。

<!-- 示例值：`[10737418240, 10737418240]` -->

#### storage.io_rate_limit <span class="version-mark">从 v5.2.0 版本开始引入</span>

I/O 限流功能相关配置。

##### `max_bytes_per_sec`

- I/O 限流功能限制下的读写流量总带宽。该配置项是 I/O 限流功能的开关，默认关闭。TiFlash 的 I/O 限流功能适用于磁盘带宽较小且磁盘带宽大小明确的云盘场景。
- 默认值：`0`，即默认关闭 I/O 限流功能
- 单位：Byte

##### `max_read_bytes_per_sec`

- I/O 限流功能限制下的读流量总带宽。
- 分别用 `max_read_bytes_per_sec` 和 `max_write_bytes_per_sec` 两个配置项控制读写带宽限制，适用于一些读写带宽限制分开计算的云盘，例如 Google Cloud 上的 persistent disk。
- 当 `max_bytes_per_sec` 配置不为 `0` 时，优先使用 [`max_bytes_per_sec`](#max_bytes_per_sec)。
- 默认值：`0`

##### `max_write_bytes_per_sec`

- I/O 限流功能限制下的写流量总带宽。
- 分别用 `max_read_bytes_per_sec` 和 `max_write_bytes_per_sec` 两个配置项控制读写带宽限制，适用于一些读写带宽限制分开计算的云盘，例如 Google Cloud 上的 persistent disk。
- 当 `max_bytes_per_sec` 配置不为 `0` 时，优先使用 [`max_bytes_per_sec`](#max_bytes_per_sec)。
- 默认值：`0`

##### `foreground_write_weight`

<!-- 下面的参数用于控制不同 I/O 流量类型分配到的带宽权重，一般不需要调整。以下默认配置表示每一种流量将获得 25 / (25 + 25 + 25 + 25) = 25% 的权重。-->

- TiFlash 内部将 I/O 请求分成 4 种类型：前台写、后台写、前台读、后台读。`foreground_write_weight` 用于控制前台写 I/O 流量类型分配到的带宽权重，一般不需要调整。
- I/O 限流初始化时，TiFlash 会根据 `foreground_write_weight`、[`background_write_weight`](/tiflash/tiflash-configuration.md#background_write_weight)、[`foreground_read_weight`](/tiflash/tiflash-configuration.md#foreground_read_weight)、[`background_read_weight`](/tiflash/tiflash-configuration.md#background_read_weight) 的比例值分配这 4 种请求的带宽。
- 如果将 weight 配置为 `0`，则对应的 I/O 操作不会被限流。
- 默认值：`25`，代表分配到 25% 的带宽比例。

##### `background_write_weight`

- TiFlash 内部将 I/O 请求分成 4 种类型：前台写、后台写、前台读、后台读。`background_write_weight` 用于控制后台写 I/O 流量类型分配到的带宽权重，一般不需要调整。
- I/O 限流初始化时，TiFlash 会根据 [`foreground_write_weight`](/tiflash/tiflash-configuration.md#foreground_write_weight)、`background_write_weight`、[`foreground_read_weight`](/tiflash/tiflash-configuration.md#foreground_read_weight)、[`background_read_weight`](/tiflash/tiflash-configuration.md#background_read_weight) 的比例值分配这 4 种请求的带宽。
- 如果将 weight 配置为 `0`，则对应的 I/O 操作不会被限流。
- 默认值：`25`，代表分配到 25% 的带宽比例。

##### `foreground_read_weight`

- TiFlash 内部将 I/O 请求分成 4 种类型：前台写、后台写、前台读、后台读。`foreground_read_weight` 用于控制前台读 I/O 流量类型分配到的带宽权重，一般不需要调整。
- I/O 限流初始化时，TiFlash 会根据 [`foreground_write_weight`](/tiflash/tiflash-configuration.md#foreground_write_weight)、[`background_write_weight`](/tiflash/tiflash-configuration.md#background_write_weight)、`foreground_read_weight`、[`background_read_weight`](/tiflash/tiflash-configuration.md#background_read_weight) 的比例值分配这 4 种请求的带宽。
- 如果将 weight 配置为 `0`，则对应的 I/O 操作不会被限流。
- 默认值：`25`，代表分配到 25% 的带宽比例。

##### `background_read_weight`

- TiFlash 内部将 I/O 请求分成 4 种类型：前台写、后台写、前台读、后台读。`background_read_weight` 用于控制后台读 I/O 流量类型分配到的带宽权重，一般不需要调整。
- I/O 限流初始化时，TiFlash 会根据 [`foreground_write_weight`](/tiflash/tiflash-configuration.md#foreground_write_weight)、[`background_write_weight`](/tiflash/tiflash-configuration.md#background_write_weight)、[`foreground_read_weight`](/tiflash/tiflash-configuration.md#foreground_read_weight)、`background_read_weight` 的比例值分配这 4 种请求的带宽。
- 如果将 weight 配置为 `0`，则对应的 I/O 操作不会被限流。
- 默认值：`25`，代表分配到 25% 的带宽比例。

##### `auto_tune_sec`

- TiFlash 支持根据当前的 I/O 负载情况自动调整各种 I/O 类型的限流带宽，有可能会超过设置的权重。
- `auto_tune_sec` 表示自动调整的执行间隔。设为 `0` 表示关闭自动调整。
- 默认值：`5`
- 单位：秒

#### storage.s3

下面的配置只针对存算分离模式生效，详细请参考 [TiFlash 存算分离架构与 S3 支持](/tiflash/tiflash-disaggregated-and-s3.md)。

##### `endpoint`

- S3 的 endpoint 地址。例如，`http://s3.{region}.amazonaws.com`。

##### `bucket`

- TiFlash 的所有数据存储在这个 bucket 中。

##### `root`

- S3 bucket 中存储数据的根目录。例如，`/cluster1_data`。

##### `access_key_id`

- 访问 S3 的 ACCESS_KEY_ID。

##### `secret_access_key`

- 访问 S3 的 SECRET_ACCESS_KEY。

#### storage.remote.cache

##### `dir`

- 存算分离架构下，TiFlash Compute Node 的本地数据缓存目录。

<!-- 示例值：`"/data1/tiflash/cache"` -->

##### `capacity`

- 示例值：`858993459200` (800 GiB)

#### flash

##### `service_addr`

- TiFlash coprocessor 服务监听地址。

<!-- 示例值：`"0.0.0.0:3930"` -->

##### `compact_log_min_gap` <span class="version-mark">从 v7.4.0 版本开始引入</span>

- 在当前 Raft 状态机推进的 applied_index 和上次落盘时的 applied_index 的差值高于 `compact_log_min_gap` 时，TiFlash 将执行来自 TiKV 的 CompactLog 命令，并进行数据落盘。
- 调大该差值可能降低 TiFlash 的落盘频率，从而减少随机写场景下的读延迟，但会增大内存开销。调小该差值可能提升 TiFlash 的落盘频率，从而缓解 TiFlash 内存压力。但无论如何，在目前阶段，TiFlash 的落盘频率不会高于 TiKV，即使设置该差值为 `0`。
- 建议保持默认值。
- 默认值：`200`

##### `compact_log_min_rows` <span class="version-mark">从 v5.0 版本开始引入</span>

- 当 TiFlash 缓存的 Region 行数或者大小超过 `compact_log_min_rows` 或 `compact_log_min_bytes` 任一阈值时，TiFlash 将执行来自 TiKV 的 CompactLog 命令，并进行落盘。
- 建议保持默认值。
- 默认值：`40960`

##### `compact_log_min_bytes` <span class="version-mark">从 v5.0 版本开始引入</span>

- 当 TiFlash 缓存的 Region 行数或者大小超过 `compact_log_min_rows` 或 `compact_log_min_bytes` 任一阈值时，TiFlash 将执行来自 TiKV 的 CompactLog 命令，并进行落盘。
- 建议保持默认值。
- 默认值：`33554432`

##### `disaggregated_mode`

- 该配置只针对存算分离模式生效，详细请参考 [TiFlash 存算分离架构与 S3 支持](/tiflash/tiflash-disaggregated-and-s3.md)。
- 可选值：`"tiflash_write"`、`"tiflash_compute"`

#### flash.proxy

##### `addr`

- proxy 监听地址。
- 默认值：`"127.0.0.1:20170"`

##### `advertise-addr`

- 外部访问 addr 的地址，不填则默认使用 `addr` 的值。
- 当集群部署在多个节点时，需要保证 `advertise-addr` 的地址可以从其他节点连接。

##### `status-addr`

- 拉取 proxy metrics 或 status 信息的监听地址。
- 默认值：`"127.0.0.1:20292"`

##### `advertise-status-addr`

- 外部访问 status-addr 的地址，不填则默认使用 `status-addr` 的值。
- 当集群部署在多个节点时，需要保证 `advertise-status-addr` 的地址可以从其他节点连接。

##### `engine-addr`

- 外部访问 TiFlash coprocessor 服务的地址。

<!-- 示例值：`"10.0.1.20:3930"` -->

##### `data-dir`

- proxy 数据存储路径。

<!-- 示例值：`"/tidb-data/tiflash-9000/flash"` -->

##### `config`

- proxy 配置文件路径。

<!-- 示例值：`"/tidb-deploy/tiflash-9000/conf/tiflash-learner.toml"` -->

##### `log-file`

- proxy log 路径。

<!-- 示例值：`"/tidb-deploy/tiflash-9000/log/tiflash_tikv.log"` -->

#### logger

以下参数只对 TiFlash 日志和 TiFlash 错误日志生效。TiFlash Proxy 的日志参数配置需要在 [`tiflash-learner.toml`](#配置文件-tiflash-learnertoml) 中指定。

##### `level`

- log 级别。
- 默认值：`"info"`
- 可选值：`"trace"`、`"debug"`、`"info"`、`"warn"`、`"error"`

##### `log`

- TiFlash 日志。

<!-- 示例值：`"/tidb-deploy/tiflash-9000/log/tiflash.log"` -->

##### `errorlog`

- TiFlash 错误日志。对于 `"warn"` 或 `"error"` 级别的日志，会额外输出到该日志文件中。

<!-- 示例值：`"/tidb-deploy/tiflash-9000/log/tiflash_error.log"` -->

##### `size`

- 单个日志文件的大小。
- 默认值：`"100M"`

##### `count`

- 最多保留日志文件个数。对于 TiFlash 日志和 TiFlash 错误日志各自最多保留 `count` 个日志文件。
- 默认值：`10`

#### raft

##### `pd_addr`

- PD 的地址。
- 当指定多个地址时，需要用逗号 `,` 分隔。例如 `"10.0.1.11:2379,10.0.1.12:2379,10.0.1.13:2379"`。

#### status

##### `metrics_port`

- Prometheus 拉取 metrics 信息的端口。
- 默认值：`8234`

#### profiles.default

##### `dt_enable_logical_split`

- 存储引擎的 segment 分裂是否使用逻辑分裂。使用逻辑分裂可以减小写放大，但是会造成一定程度的硬盘空间回收不及时。
- 在 v6.2.0 以及后续版本，强烈建议保留默认值 `false`，不要将其修改为 `true`。具体请参考已知问题 [#5576](https://github.com/pingcap/tiflash/issues/5576)。
- 默认值：`false`

##### `max_threads`

- `max_threads` 指的是执行一个 MPP Task 的内部线程并发度。当值为 `0` 时，TiFlash 执行 MPP Task 的线程并发度为 CPU 逻辑核数。
- 该参数只有在系统变量 [`tidb_max_tiflash_threads`](/system-variables.md#tidb_max_tiflash_threads-从-v610-版本开始引入) 设置为 `-1` 时才会生效。
- 默认值：`0`

##### `max_memory_usage`

- 单次查询过程中，节点对中间数据的内存限制。
- 设置为整数时，单位为 byte，比如 `34359738368` 表示 32 GiB 的内存限制。
- 设置为 `[0.0, 1.0)` 之间的浮点数时，指节点总内存的比值，比如 `0.8` 表示总内存的 80%，`0.0` 表示无限制。
- 当查询试图申请超过限制的内存时，查询终止执行并且报错。
- 默认值：`0`，表示不限制

##### `max_memory_usage_for_all_queries`

- 所有查询过程中，节点对中间数据的内存限制。
- 设置为整数时，单位为 byte，例如 `34359738368` 表示 32 GiB 的内存限制，`0` 表示无限制。
- 从 v6.6.0 开始，支持设置为 `[0.0, 1.0)` 之间的浮点数，表示节点总内存的比值。例如，`0.8` 表示总内存的 80%，`0.0` 表示无限制。
- 当查询试图申请超过限制的内存时，查询终止执行并且报错。
- 默认值：`0.8`，表示总内存的 80%。在 v6.6.0 之前，默认值为 `0`，表示不限制。

##### `cop_pool_size` <span class="version-mark">从 v5.0 版本开始引入</span>

- 表示 TiFlash Coprocessor 最多同时执行的 cop 请求数量。如果请求数量超过了该配置指定的值，多出的请求会排队等待。如果设为 `0` 或不设置，则使用默认值，即物理核数的两倍。
- 默认值：物理核数的两倍

##### `cop_pool_handle_limit` <span class="version-mark">从 v5.0 版本开始引入</span>

- 表示 TiFlash Coprocessor 最多同时处理的 cop 请求数量，包括正在执行的 cop 请求与正在排队等待的 cop 请求。如果请求数量超过了该配置指定的值，则会返回 `TiFlash Server is Busy` 的错误。
- 设置为 `-1` 表示无限制。设置为 `0` 表示使用默认值，即 `10 * cop_pool_size`。

##### `cop_pool_max_queued_seconds` <span class="version-mark">从 v5.0 版本开始引入</span>

- 表示 TiFlash 中 cop 请求排队的最长时间。如果一个 cop 请求在请求队列中等待的时间超过该配置指定的值，则会返回 `TiFlash Server is Busy` 的错误。
- 配置为一个小于等于 `0` 的值时表示无限制。
- 默认值：`15`

##### `batch_cop_pool_size` <span class="version-mark">从 v5.0 版本开始引入</span>

- 表示 TiFlash Coprocessor 最多同时执行的 batch 请求数量。如果请求数量超过了该配置指定的值，多出的请求会排队等待。如果设为 `0` 或不设置，则使用默认值，即物理核数的两倍。
- 默认值：物理核数的两倍

##### `manual_compact_pool_size` <span class="version-mark">从 v6.1 版本开始引入</span>

- 指定 TiFlash 执行来自 TiDB 的 `ALTER TABLE ... COMPACT` 请求时，能同时并行处理的请求数量。
- 如果设为 `0` 或不设置，则会采用默认值 (`1`)。
- 默认值：`1`

##### `enable_elastic_threadpool` <span class="version-mark">从 v5.4.0 版本开始引入</span>

- 是否启用弹性线程池，这项功能可以显著提高 TiFlash 在高并发场景的 CPU 利用率。
- 默认值：`true`

##### `dt_compression_method`

- TiFlash 存储引擎的压缩算法。
- 默认值：`LZ4`
- 可选值：`LZ4`、`zstd`、`LZ4HC`，大小写不敏感

##### `dt_compression_level`

- TiFlash 存储引擎的压缩级别。
- 如果 `dt_compression_method` 设置为 `LZ4`，推荐将该值设为 `1`。
- 如果 `dt_compression_method` 设置为 `zstd`，推荐将该值设为 `-1` 或 `1`，设置为 `-1` 的压缩率更小，但是读性能会更好。
- 如果 `dt_compression_method` 设置为 `LZ4HC`，推荐将该值设为 `9`。
- 默认值：`1`

##### `dt_page_gc_threshold` <span class="version-mark">从 v6.2.0 版本开始引入</span>

- 表示 PageStorage 单个数据文件中有效数据的最低比例。当某个数据文件的有效数据比例低于该值时，会触发 GC 对该文件的数据进行整理。
- 默认值：`0.5`

##### `max_bytes_before_external_group_by` <span class="version-mark">从 v7.0.0 版本开始引入</span>

- 表示带 `GROUP BY` key 的 Hash Aggregation 算子在触发 spill 之前的最大可用内存，超过该阈值之后 Hash Aggregation 会采用[数据落盘](/tiflash/tiflash-spill-disk.md)的方式来减小内存使用。
- 默认值：`0`，表示内存使用无限制，即不会触发 spill

##### `max_bytes_before_external_sort` <span class="version-mark">从 v7.0.0 版本开始引入</span>

- 表示 sort/topN 算子在触发 spill 之前的最大可用内存，超过该阈值之后 sort/TopN 会采用[数据落盘](/tiflash/tiflash-spill-disk.md)的方式来减小内存使用。
- 默认值：`0`，表示内存使用无限制，即不会触发 spill

##### `max_bytes_before_external_join` <span class="version-mark">从 v7.0.0 版本开始引入</span>

- 表示带等值 join 条件的 Hash Join 算子在触发 spill 之前的最大可用内存，超过该阈值之后 HashJoin 算子会采用[数据落盘](/tiflash/tiflash-spill-disk.md)的方式来减小内存使用。
- 默认值：`0`，表示内存使用无限制，即不会触发 spill

##### `enable_resource_control` <span class="version-mark">从 v7.4.0 版本开始引入</span>

- 表示是否开启 TiFlash 资源管控功能。当设置为 `true` 时，TiFlash 会使用 [Pipeline Model 执行模型](/tiflash/tiflash-pipeline-model.md)。

##### `task_scheduler_thread_soft_limit` <span class="version-mark">从 v6.0.0 版本开始引入</span>

- 用于 MinTSO 调度器，表示一个资源组中最多可使用的线程数量。关于 MinTSO 调度器，详见 [TiFlash MinTSO 调度器](/tiflash/tiflash-mintso-scheduler.md)。
- 默认值：`5000`

##### `task_scheduler_thread_hard_limit` <span class="version-mark">从 v6.0.0 版本开始引入</span>

- 用于 MinTSO 调度器，表示全局最多可使用的线程数量。关于 MinTSO 调度器，详见 [TiFlash MinTSO 调度器](/tiflash/tiflash-mintso-scheduler.md)。
- 默认值：`10000`

##### `task_scheduler_active_set_soft_limit` <span class="version-mark">从 v6.4.0 版本开始引入</span>

- 用于 MinTSO 调度器，表示一个 TiFlash 实例中最多可同时运行的查询数量。关于 MinTSO 调度器，详见 [TiFlash MinTSO 调度器](/tiflash/tiflash-mintso-scheduler.md)。
- 默认值：在 v7.4.0 之前，默认值为 `vcpu * 0.25`，即 vCPU 数量的四分之一。从 v7.4.0 开始，默认值为 `vcpu * 2`，即两倍的 vCPU 数量。

#### security <span class="version-mark">从 v4.0.5 版本开始引入</span>

安全相关配置。

##### `redact_info_log` <span class="version-mark">从 v5.0 版本开始引入</span>

- 控制是否开启日志脱敏。
- 默认值：`false`
- 可选值：`true`、`false`、`"on"`、`"off"` 和 `"marker"`。其中，`"on"`、`"off"` 和 `"marker"` 从 v8.2.0 开始支持。
- 若设置为 `false` 或 `"off"`，即对用户日志不做处理。
- 若设置为 `true` 或 `"on"`，日志中的用户数据会以 `?` 代替显示。
- 若设置为 `"marker"`，日志中的用户数据会被标记符号 `‹ ›` 包裹。用户数据中的 `‹` 会转义成 `‹‹`，`›` 会转义成 `››`。基于标记后的日志，你可以在展示日志时决定是否对被标记信息进行脱敏处理。
- 注意，tiflash-learner 对应的安全配置选项为 `security.redact-info-log`，需要在 [`tiflash-learner.toml`](#配置文件-tiflash-learnertoml) 中另外设置。

##### `ca_path`

- 包含可信 SSL CA 列表的文件路径。如果你设置了该值，[`cert_path`](#cert_path) 和 [`key_path`](#key_path) 中的路径也需要填写。

<!-- 示例值：`"/path/to/ca.pem"` -->

##### `cert_path`

- 包含 PEM 格式的 X509 certificate 文件路径。

<!-- 示例值：`"/path/to/tiflash-server.pem"` -->

##### `key_path`

- 包含 PEM 格式的 X509 key 文件路径。

<!-- 示例值：`"/path/to/tiflash-server-key.pem"` -->

### 配置文件 tiflash-learner.toml

`tiflash-learner.toml` 中的功能参数和 TiKV 基本一致，可以参照 [TiKV 配置](/tikv-configuration-file.md)来进行配置。下面只列了常用的部分参数。需要注意的是：

- 相对于 TiKV，TiFlash Proxy 新增了 [`raftstore.snap-handle-pool-size`](#snap-handle-pool-size-从-v400-版本开始引入) 参数。
- `key` 为 `engine` 的 `label` 是保留项，不可手动配置。

#### log

##### `level` <span class="version-mark">从 v5.4.0 版本开始引入</span>

- TiFlash Proxy 的 log 级别。
- 默认值：`"info"`
- 可选值：`"trace"`、`"debug"`、`"info"`、`"warn"`、`"error"`

#### log.file

##### `max-backups` <span class="version-mark">从 v5.4.0 版本开始引入</span>

- 可保留的 log 文件的最大数量。
- 如果未设置该参数或把该参数设置为默认值 `0`，TiFlash Proxy 会保存所有的日志文件。
- 如果把此参数设置为非 `0` 的值，TiFlash Proxy 最多会保留 `max-backups` 中指定数量的旧日志文件。比如，如果该值设置为 `7`，TiFlash Proxy 最多会保留 7 个旧的日志文件。
- 默认值：`0`

##### `max-days` <span class="version-mark">从 v5.4.0 版本开始引入</span>

- 保留 log 文件的最长天数。
- 如果未设置本参数或把此参数设置为默认值 `0`，TiFlash Proxy 会保存所有的日志文件。
- 如果把此参数设置为非 `0` 的值，在 `max-days` 之后，TiFlash Proxy 会清理过期的日志文件。
- 默认值：`0`

#### raftstore

##### `apply-pool-size`

- 处理 Raft 数据落盘的线程池中线程的数量。

<!-- 示例值：`4` -->

##### `store-pool-size`

- 处理 Raft 的线程池中线程的数量，即 Raftstore 线程池的大小。

<!-- 示例值：`4` -->

##### `snap-handle-pool-size` <span class="version-mark">从 v4.0.0 版本开始引入</span>

- TiFlash Proxy 特有参数，控制处理 snapshot 的线程数。设为 `0` 则关闭多线程优化。
- 默认值：`2`

#### security

##### `redact-info-log` <span class="version-mark">从 v5.0 版本开始引入</span>

- 控制是否开启日志脱敏。
- 默认值：`false`
- 可选值：`true`、`false`、`"on"`、`"off"` 和 `"marker"`。其中，`"on"`、`"off"` 和 `"marker"` 从 v8.3.0 开始支持。
- 若设置为 `false` 或 `"off"`，即对用户日志不做处理。
- 若设置为 `true` 或 `"on"`，日志中的用户数据会以 `?` 代替显示。
- 若设置为 `"marker"`，日志中的用户数据会被标记符号 `‹ ›` 包裹。用户数据中的 `‹` 会转义成 `‹‹`，`›` 会转义成 `››`。基于标记后的日志，你可以在展示日志时决定是否对被标记信息进行脱敏处理。

#### security.encryption

##### `data-encryption-method`

- 数据文件的加密方法。选择 `"plaintext"` 以外的值则表示启用加密功能。此时必须指定主密钥。
- 默认值：`"plaintext"`，即默认不开启加密功能。
- 可选值：`"aes128-ctr"`、`"aes192-ctr"`、`"aes256-ctr"`、`"sm4-ctr"` 和 `"plaintext"`。其中，`"sm4-ctr"` 从 v6.4.0 开始支持。

##### `data-key-rotation-period`

- 轮换密钥的频率。
- 默认值：`7d`

#### security.encryption.master-key

- 指定启用加密时的主密钥。若要了解如何配置主密钥，可以参考[静态加密 - 配置加密](/encryption-at-rest.md#配置加密)。

#### security.encryption.previous-master-key

- 指定轮换新主密钥时的旧主密钥。旧主密钥的配置格式与主密钥相同。若要了解如何配置主密钥，可以参考[静态加密 - 配置加密](/encryption-at-rest.md#配置加密)。

#### server

##### `labels`

- 指定服务器属性，例如 `{ zone = "us-west-1", disk = "ssd" }`。要了解如何使用 label 实现副本的拓扑调度，请参考 [TiFlash 设置可用区](/tiflash/create-tiflash-replicas.md#设置可用区)。
- 默认值：`{}`

### 多盘部署

TiFlash 支持单节点多盘部署。如果你的部署节点上有多块硬盘，可以通过以下的方式配置参数，提高节点的硬盘 I/O 利用率。TiUP 中参数配置格式参照[详细 TiFlash 配置模版](/tiflash-deployment-topology.md#拓扑模版)。

TiDB v4.0.9 及之后的版本中，TiFlash 支持将存储引擎的主要数据和新数据都分布在多盘上。多盘部署时，推荐使用 `[storage]` 中的参数，以更好地利用节点的 I/O 性能。

如果节点上有多块相同规格的硬盘，推荐把硬盘目录填到 `storage.main.dir` 列表中，`storage.latest.dir` 列表留空。TiFlash 会在所有存储目录之间分摊 I/O 压力以及进行数据均衡。

如果节点上有多块规格不同的硬盘，推荐把 I/O 性能较好的硬盘目录配置在 `storage.latest.dir` 中，把 I/O 性能较一般的硬盘目录配置在 `storage.main.dir` 中。例如节点上有一块 NVMe-SSD 硬盘加上两块 SATA-SSD 硬盘，你可以把 `storage.latest.dir` 设为 `["/nvme_ssd_a/data/tiflash"]` 以及把 `storage.main.dir` 设为 `["/sata_ssd_b/data/tiflash", "/sata_ssd_c/data/tiflash"]`。TiFlash 会根据两个目录列表分别进行 I/O 压力分摊及数据均衡。需要注意此情况下，`storage.latest.dir` 中规划的容量大小需要占总规划容量的约 10%。

> **警告：**
>
> `[storage]` 参数从 TiUP v1.2.5 版本开始支持。如果你的 TiDB 版本为 v4.0.9 及以上，请确保你的 TiUP 版本不低于 v1.2.5，否则 `[storage]` 中定义的数据目录不会被 TiUP 纳入管理。
