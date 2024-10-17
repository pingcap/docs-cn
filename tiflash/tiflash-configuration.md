---
title: TiFlash 配置参数
aliases: ['/docs-cn/dev/tiflash/tiflash-configuration/','/docs-cn/dev/reference/tiflash/configuration/']
summary: TiFlash 配置参数包括 PD 调度参数和 TiFlash 配置参数。PD 调度参数可通过 pd-ctl 调整，包括 replica-schedule-limit 和 store-balance-rate。TiFlash 配置参数包括 tiflash.toml 和 tiflash-learner.toml，用于配置 TiFlash TCP/HTTP 服务的监听和存储路径。另外，通过拓扑 label 进行副本调度和多盘部署也是可行的。
---

# TiFlash 配置参数

本文介绍了与部署使用 TiFlash 相关的配置参数。

## PD 调度参数

可通过 [pd-ctl](/pd-control.md) 调整参数。如果你使用 TiUP 部署，可以用 `tiup ctl:v<CLUSTER_VERSION> pd` 代替 `pd-ctl -u <pd_ip:pd_port>` 命令。

- [`replica-schedule-limit`](/pd-configuration-file.md#replica-schedule-limit)：用来控制 replica 相关 operator 的产生速度（涉及到下线、补副本的操作都与该参数有关）

  > **注意：**
  >
  > 不要超过 `region-schedule-limit`，否则会影响正常 TiKV 之间的 Region 调度。

- `store-balance-rate`：用于限制每个 TiKV store 或 TiFlash store 的 Region 调度速度。注意这个参数只对新加入集群的 store 有效，如果想立刻生效请用下面的方式。

  > **注意：**
  >
  > 4.0.2 版本之后（包括 4.0.2 版本）废弃了 `store-balance-rate` 参数且 `store limit` 命令有部分变化。该命令变化的细节请参考 [store-limit 文档](/configure-store-limit.md)。

    - 使用 `pd-ctl -u <pd_ip:pd_port> store limit <store_id> <value>` 命令单独设置某个 store 的 Region 调度速度。（`store_id` 可通过 `pd-ctl -u <pd_ip:pd_port> store` 命令获得）如果没有单独设置，则继承 `store-balance-rate` 的设置。你也可以使用 `pd-ctl -u <pd_ip:pd_port> store limit` 命令查看当前设置值。

- [`replication.location-labels`](/pd-configuration-file.md#location-labels)：用来表示 TiKV 实例的拓扑关系，其中 key 的顺序代表了不同标签的层次关系。在 TiFlash 开启的情况下需要使用 [`pd-ctl config placement-rules`](/pd-control.md#config-show--set-option-value--placement-rules) 来设置默认值，详细可参考 [geo-distributed-deployment-topology](/geo-distributed-deployment-topology.md)。

## TiFlash 配置参数

> **Tip:**
>
> 如果你需要调整配置项的值，请参考[修改配置参数](/maintain-tidb-using-tiup.md#修改配置参数)进行操作。

### 配置文件 tiflash.toml

```toml
## TiFlash TCP/HTTP 等辅助服务的监听 host。建议配置成 0.0.0.0，即监听本机所有 IP 地址。
listen_host = "0.0.0.0"
## TiFlash TCP 服务的端口。TCP 服务为内部测试接口，默认使用 9000 端口。在 TiFlash v7.1.0 之前的版本中，该端口默认开启，但存在安全风险。为了提高安全性，建议对该端口进行访问控制，只允许白名单 IP 访问。从 TiFlash v7.1.0 起，可以通过注释掉该端口的配置避免安全风险。当 TiFlash 配置文件未声明该端口时，该端口也不会开启。
## 建议在任何 TiFlash 的部署中都不配置该端口。(注: 从 TiFlash v7.1.0 起，由 TiUP >= v1.12.5 或 TiDB Operator >= v1.5.0 部署的 TiFlash 默认为安全版本，即默认未开启该端口)
# tcp_port = 9000
## 数据块元信息的内存 cache 大小限制，通常不需要修改
mark_cache_size = 1073741824
## 数据块 min-max 索引的内存 cache 大小限制，通常不需要修改
minmax_index_cache_size = 1073741824
## DeltaIndex 内存 cache 大小限制，默认为 0，代表没有限制
delta_index_cache_size = 0

## TiFlash 数据的存储路径。如果有多个目录，以英文逗号分隔。
## 从 v4.0.9 版本开始，不推荐使用 path 及 path_realtime_mode 参数。推荐使用 [storage] 下的配置项代替，这样在多盘部署的场景下能更好地利用节点性能。
## 从 v5.2.0 版本开始，如果要使用配置项 storage.io_rate_limit，需要同时将 TiFlash 的数据存储路径设置为 storage.main.dir。
## 当 [storage] 配置项存在的情况下，path 和 path_realtime_mode 两个配置会被忽略。
# path = "/tidb-data/tiflash-9000"
## 或
# path = "/ssd0/tidb-data/tiflash,/ssd1/tidb-data/tiflash,/ssd2/tidb-data/tiflash"
## 默认为 false。如果设为 true，且 path 配置了多个目录，表示在第一个目录存放最新数据，在其他目录存放较旧的数据。
# path_realtime_mode = false

## TiFlash 临时文件的存放路径。默认使用 [`path` 或者 `storage.latest.dir` 的第一个目录] + "/tmp"
# tmp_path = "/tidb-data/tiflash-9000/tmp"

## 存储路径相关配置，从 v4.0.9 开始生效
[storage]

    ## DTFile 储存文件格式
    ## * format_version = 2 v6.0.0 以前版本的默认文件格式
    ## * format_version = 3 v6.0.0 及 v6.1.x 版本的默认文件格式，具有更完善的检验功能
    ## * format_version = 4 v6.2.0 ~ v7.3.0 的默认文件格式，优化了写放大问题，同时减少了后台线程消耗。
    ## * format_version = 5 v7.4.0 ~ v8.3.0 的默认文件格式（从 v7.3.0 开始引入），该格式可以合并小文件从而减少了物理文件数量。
    ## * format_version = 6 从 v8.4.0 开始引入，部分支持了向量索引的构建与存储。
    ## * format_version = 7 v8.4.0 及以后版本的默认文件格式 (从 v8.4.0 开始引入)，该格式用于支持向量索引的构建与存储。
    # format_version = 7

    [storage.main]
    ## 用于存储主要的数据，该目录列表中的数据占总数据的 90% 以上。
    dir = [ "/tidb-data/tiflash-9000" ]
    ## 或
    # dir = [ "/ssd0/tidb-data/tiflash", "/ssd1/tidb-data/tiflash" ]

    ## storage.main.dir 存储目录列表中每个目录的最大可用容量。
    ## * 在未定义配置项，或者列表中全填 0 时，会使用目录所在的硬盘容量
    ## * 以 byte 为单位。目前不支持如 "10GB" 的设置
    ## * capacity 列表的长度应当与 dir 列表长度保持一致
    ## 例如：
    # capacity = [ 10737418240, 10737418240 ]

    [storage.latest]
    ## 用于存储最新的数据，大约占总数据量的 10% 以内，需要较高的 IOPS。
    ## 默认情况该项可留空。在未配置或者为空列表的情况下，会使用 storage.main.dir 的值。
    # dir = [ ]
    ## storage.latest.dir 存储目录列表中，每个目录的最大可用容量。
    # capacity = [ 10737418240, 10737418240 ]

    ## [storage.io_rate_limit] 相关配置从 v5.2.0 开始引入。
    [storage.io_rate_limit]
    ## 该配置项是 I/O 限流功能的开关，默认关闭。TiFlash 的 I/O 限流功能适用于磁盘带宽较小且磁盘带宽大小明确的云盘场景。
    ## I/O 限流功能限制下的读写流量总带宽，单位为 Byte，默认值为 0，即默认关闭 I/O 限流功能。
    # max_bytes_per_sec = 0
    ## max_read_bytes_per_sec 和 max_write_bytes_per_sec 的含义和 max_bytes_per_sec 类似，分别指 I/O 限流功能限制下的读流量总带宽和写流量总带宽。
    ## 分别用两个配置项控制读写带宽限制，适用于一些读写带宽限制分开计算的云盘，例如 Google Cloud 上的 persistent disk。
    ## 当 max_bytes_per_sec 配置不为 0 时，优先使用 max_bytes_per_sec。
    # max_read_bytes_per_sec = 0
    # max_write_bytes_per_sec = 0

    ## 下面的参数用于控制不同 I/O 流量类型分配到的带宽权重，一般不需要调整。
    ## TiFlash 内部将 I/O 请求分成 4 种类型：前台写、后台写、前台读、后台读。
    ## I/O 限流初始化时，TiFlash 会根据下面的权重 (weight) 比例分配带宽。
    ## 以下默认配置表示每一种流量将获得 25 / (25 + 25 + 25 + 25) = 25% 的权重。
    ## 如果将 weight 配置为 0，则对应的 I/O 操作不会被限流。
    # foreground_write_weight = 25
    # background_write_weight = 25
    # foreground_read_weight = 25
    # background_read_weight = 25
    ## TiFlash 支持根据当前的 I/O 负载情况自动调整各种 I/O 类型的限流带宽，有可能会超过设置的权重。
    ## auto_tune_sec 表示自动调整的执行间隔，单位为秒。设为 0 表示关闭自动调整。
    # auto_tune_sec = 5

    ## 下面的配置只针对存算分离模式生效，详细请参考 TiFlash 存算分离架构与 S3 支持文档 https://docs.pingcap.com/zh/tidb/dev/tiflash-disaggregated-and-s3
    # [storage.s3]
    # endpoint: http://s3.{region}.amazonaws.com # S3 的 endpoint 地址
    # bucket: mybucket                           # TiFlash 的所有数据存储在这个 bucket 中
    # root: /cluster1_data                       # S3 bucket 中存储数据的根目录
    # access_key_id: {ACCESS_KEY_ID}             # 访问 S3 的 ACCESS_KEY_ID
    # secret_access_key: {SECRET_ACCESS_KEY}     # 访问 S3 的 SECRET_ACCESS_KEY

    # [storage.remote.cache]
    # dir: /data1/tiflash/cache        # TiFlash Compute Node 的本地数据缓存目录
    # capacity: 858993459200           # 800 GiB

[flash]
    ## TiFlash coprocessor 服务监听地址
    service_addr = "0.0.0.0:3930"

    ## 从 v7.4.0 引入，在当前 Raft 状态机推进的 applied_index 和上次落盘时的 applied_index 的差值高于 compact_log_min_gap 时，
    ## TiFlash 将执行来自 TiKV 的 CompactLog 命令，并进行数据落盘。调大该差值可能降低 TiFlash 的落盘频率，从而减少随机写场景下的读延迟，但会增大内存开销。调小该差值可能提升 TiFlash 的落盘频率，从而缓解 TiFlash 内存压力。但无论如何，在目前阶段，TiFlash 的落盘频率不会高于 TiKV，即使设置该差值为 0。
    ## 建议保持默认值。
    # compact_log_min_gap = 200
    ## 从 v5.0 引入，当 TiFlash 缓存的 Region 行数或者大小超过以下任一阈值时，TiFlash 将执行来自 TiKV 的 CompactLog 命令，并进行落盘。
    ## 建议保持默认值。
    # compact_log_min_rows = 40960 # 40k
    # compact_log_min_bytes = 33554432 # 32MB

    ## 下面的配置只针对存算分离模式生效，详情请参考 TiFlash 存算分离架构与 S3 支持文档 https://docs.pingcap.com/zh/tidb/dev/tiflash-disaggregated-and-s3
    # disaggregated_mode = tiflash_write # 可选值为 tiflash_write 或者 tiflash_compute

[flash.proxy]
    ## proxy 监听地址，不填则默认是 127.0.0.1:20170
    addr = "127.0.0.1:20170"
    ## 外部访问 addr 的地址，不填则默认使用 "addr" 的值
    ## 当集群部署在多个节点时，需要保证 `advertise-addr` 的地址可以从其他节点连接
    advertise-addr = ""
    ## 拉取 proxy metrics 或 status 信息的监听地址，不填则默认是 127.0.0.1:20292
    status-addr = "127.0.0.1:20292"
    ## 外部访问 status-addr 的地址，不填则默认使用 "status-addr" 的值
    ## 当集群部署在多个节点时，需要保证 `advertise-addr` 的地址可以从其他节点连接
    advertise-status-addr = ""
    ## 外部访问 TiFlash coprocessor 服务的地址
    engine-addr = "10.0.1.20:3930"
    ## proxy 数据存储路径
    data-dir = "/tidb-data/tiflash-9000/flash"
    ## proxy 配置文件路径
    config = "/tidb-deploy/tiflash-9000/conf/tiflash-learner.toml"
    ## proxy log 路径
    log-file = "/tidb-deploy/tiflash-9000/log/tiflash_tikv.log"

[logger]
    ## 注意，以下参数只对 tiflash.log、tiflash_error.log 生效。TiFlash Proxy 的日志参数配置需要在 tiflash-learner.toml 中指定。

    ## log 级别（支持 "trace"、"debug"、"info"、"warn"、"error"），默认是 "info"
    level = "info"
    ## TiFlash 日志
    log = "/tidb-deploy/tiflash-9000/log/tiflash.log"
    ## TiFlash 错误日志。对于 "warn"、"error" 级别的日志，会额外输出到该日志文件中。
    errorlog = "/tidb-deploy/tiflash-9000/log/tiflash_error.log"
    ## 单个日志文件的大小，默认是 "100M"
    size = "100M"
    ## 最多保留日志文件个数，默认是 10。对于 TiFlash 日志和 TiFlash 错误日志各自最多保留 `count` 个日志文件。
    count = 10

[raft]
    ## PD 服务地址. 多个地址以逗号隔开
    pd_addr = "10.0.1.11:2379,10.0.1.12:2379,10.0.1.13:2379"

[status]
    ## Prometheus 拉取 metrics 信息的端口，默认是 8234
    metrics_port = 8234

[profiles]

[profiles.default]
    ## 存储引擎的 segment 分裂是否使用逻辑分裂。使用逻辑分裂可以减小写放大，但是会造成一定程度的硬盘空间回收不及时。默认为 false。
    ## 在 v6.2.0 以及后续版本，强烈建议保留默认值 `false`，不要将其修改为 `true`。具体请参考已知问题 [#5576](https://github.com/pingcap/tiflash/issues/5576)。
    # dt_enable_logical_split = false

    ## `max_threads` 指的是执行一个 MMP Task 的内部线程并发度，默认值为 0。当值为 0 时，TiFlash 执行 MMP Task 的线程并发度为 CPU 核数。
    ## 该参数只有在系统变量 `tidb_max_tiflash_threads` 设置为 -1 时才会生效。
    max_threads = 0

    ## 单次查询过程中，节点对中间数据的内存限制
    ## 设置为整数时，单位为 byte，比如 34359738368 表示 32 GiB 的内存限制，0 表示无限制
    ## 设置为 [0.0, 1.0) 之间的浮点数时，指节点总内存的比值，比如 0.8 表示总内存的 80%，0.0 表示无限制
    ## 默认值为 0，表示不限制
    ## 当查询试图申请超过限制的内存时，查询终止执行并且报错
    max_memory_usage = 0

    ## 所有查询过程中，节点对中间数据的内存限制
    ## 设置为整数时，单位为 byte，比如 34359738368 表示 32 GiB 的内存限制，0 表示无限制
    ## 设置为 [0.0, 1.0) 之间的浮点数时，指节点总内存的比值，比如 0.8 表示总内存的 80%，0.0 表示无限制
    ## 默认值为 0.8，表示总内存的 80%
    ## 当查询试图申请超过限制的内存时，查询终止执行并且报错
    max_memory_usage_for_all_queries = 0.8

    ## 从 v5.0 引入，表示 TiFlash Coprocessor 最多同时执行的 cop 请求数量。如果请求数量超过了该配置指定的值，多出的请求会排队等待。如果设为 0 或不设置，则使用默认值，即物理核数的两倍。
    cop_pool_size = 0

    ## 从 v5.0 引入，表示 TiFlash Coprocessor 最多同时执行的 batch 请求数量。如果请求数量超过了该配置指定的值，多出的请求会排队等待。如果设为 0 或不设置，则使用默认值，即物理核数的两倍。
    batch_cop_pool_size = 0

    ## 从 v6.1 引入，指定 TiFlash 执行来自 TiDB 的 ALTER TABLE ... COMPACT 请求时，能同时并行处理的请求数量。
    ## 如果这个值没有设置或设为了 0，则会采用默认值（1）。
    manual_compact_pool_size = 1

    ## 从 v5.4.0 引入，表示是否启用弹性线程池，这项功能可以显著提高 TiFlash 在高并发场景的 CPU 利用率。默认为 true。
    # enable_elastic_threadpool = true

    ## TiFlash 存储引擎的压缩算法，支持 LZ4、zstd 和 LZ4HC，大小写不敏感。默认使用 LZ4 算法。
    dt_compression_method = "LZ4"

    ## TiFlash 存储引擎的压缩级别，默认为 1。
    ## 如果 dt_compression_method 设置为 LZ4，推荐将该值设为 1；
    ## 如果 dt_compression_method 设置为 zstd，推荐将该值设为 -1 或 1，设置为 -1 的压缩率更小，但是读性能会更好；
    ## 如果 dt_compression_method 设置为 LZ4HC，推荐将该值设为 9。
    dt_compression_level = 1

    ## 从 v6.2.0 引入，表示 PageStorage 单个数据文件中有效数据的最低比例。当某个数据文件的有效数据比例低于该值时，会触发 GC 对该文件的数据进行整理。默认为 0.5。
    dt_page_gc_threshold = 0.5

    ## 从 v7.0.0 引入，表示带 group by key 的 HashAggregation 算子在触发 spill 之前的最大可用内存，超过该阈值之后 HashAggregation 会采用 spill to disk 的方式来减小内存使用。默认值为 0，表示内存使用无限制，即不会触发 spill。
    max_bytes_before_external_group_by = 0

    ## 从 v7.0.0 引入，表示 sort/topN 算子在触发 spill 之前的最大可用内存，超过该阈值之后 sort/TopN 会采用 spill to disk 的方式来减小内存使用。默认值为 0，表示内存使用无限制，即不会触发 spill。
    max_bytes_before_external_sort = 0

    ## 从 v7.0.0 引入，表示带等值 join 条件的 HashJoin 算子在触发 spill 之前的最大可用内存，超过该阈值之后 HashJoin 算子会采用 spill to disk 的方式来减小内存使用。默认值为 0，表示内存使用无限制，即不会触发 spill。
    max_bytes_before_external_join = 0

    ## 从 v7.4.0 引入，表示是否开启 TiFlash 资源管控功能。当设置为 true 时，TiFlash 会使用 Pipeline Model 执行模型。
    enable_resource_control = true

## 安全相关配置，从 v4.0.5 开始生效
[security]
    ## 从 v5.0 引入，控制是否开启日志脱敏。可选值为 `true`、`false`、`"on"`、`"off"` 和 `"marker"`。其中，`"on"`、`"off"` 和 `"marker"` 从 v8.2.0 开始支持。
    ## 若设置为 `false` 或 `"off"`，即对用户日志不做处理。
    ## 若设置为 `true` 或 `"on"`，日志中的用户数据会以 `?` 代替显示。
    ## 若设置为 `"marker"`，日志中的用户数据会被标记符号 `‹ ›` 包裹。用户数据中的 `‹` 会转义成 `‹‹`，`›` 会转义成 `››`。基于标记后的日志，你可以在展示日志时决定是否对被标记信息进行脱敏处理。
    ## 默认值为 `false`。
    ## 注意，tiflash-learner 对应的安全配置选项为 `security.redact-info-log`，需要在 tiflash-learner.toml 中另外设置。
    # redact_info_log = false

    ## 包含可信 SSL CA 列表的文件路径。如果你设置了该值，`cert_path` 和 `key_path` 中的路径也需要填写
    # ca_path = "/path/to/ca.pem"
    ## 包含 PEM 格式的 X509 certificate 文件路径
    # cert_path = "/path/to/tiflash-server.pem"
    ## 包含 PEM 格式的 X509 key 文件路径
    # key_path = "/path/to/tiflash-server-key.pem"
```

### 配置文件 tiflash-learner.toml

`tiflash-learner.toml` 中的功能参数和 TiKV 基本一致，可以参照 [TiKV 配置](/tikv-configuration-file.md)来进行配置。下面只列了常用的部分参数。需要注意的是：

- 相对于 TiKV，TiFlash Proxy 新增了 `raftstore.snap-handle-pool-size` 参数。
- `key` 为 `engine` 的 `label` 是保留项，不可手动配置。

```toml
[log]
    ## TiFlash Proxy 的 log 级别，可选值为 "trace"、"debug"、"info"、"warn"、"error"，默认值为 "info"。从 v5.4.0 版本开始引入。
    level = "info"

[log.file]
    ## 可保留的 log 文件的最大数量。从 v5.4.0 版本开始引入。
    ## 如果未设置该参数或把该参数设置为默认值 `0`，TiFlash Proxy 会保存所有的日志文件；
    ## 如果把此参数设置为非 `0` 的值，TiFlash Proxy 最多会保留 `max-backups` 中指定数量的旧日志文件。比如，如果该值设置为 `7`，TiFlash Proxy 最多会保留 7 个旧的日志文件。
    max-backups = 0
    ## 保留 log 文件的最长天数。从 v5.4.0 版本开始引入。
    ## 如果未设置本参数或把此参数设置为默认值 `0`，TiFlash Proxy 会保存所有的日志文件。
    ## 如果把此参数设置为非 `0` 的值，在 `max-days` 之后，TiFlash Proxy 会清理过期的日志文件。
    max-days = 0

[raftstore]
    ## 处理 Raft 数据落盘的线程池中线程的数量
    apply-pool-size = 4
    ## 处理 Raft 的线程池中线程的数量，即 Raftstore 线程池的大小。
    store-pool-size = 4
    ## 控制处理 snapshot 的线程数，默认为 2。设为 0 则关闭多线程优化
    ## TiFlash Proxy 特有参数，从 v4.0.0 版本开始引入。
    snap-handle-pool-size = 2

[security]
    ## 从 v5.0 引入，控制是否开启日志脱敏。可选值为 `true`、`false`、`"on"`、`"off"` 和 `"marker"`。其中，`"on"`、`"off"` 和 `"marker"` 从 v8.3.0 开始支持。
    ## 若设置为 `false` 或 `"off"`，即对用户日志不做处理。
    ## 若设置为 `true` 或 "on"，日志中的用户数据会以 `?` 代替显示。
    ## 若设置为 `"marker"`，日志中的用户数据会被标记符号 `‹ ›` 包裹。用户数据中的 `‹` 会转义成 `‹‹`，`›` 会转义成 `››`。基于标记后的日志，你可以在展示日志时决定是否对被标记信息进行脱敏处理。
    ## 默认值为 `false`。
    # redact-info-log = false

[security.encryption]
    ## 数据文件的加密方法。
    ## 可选值为 "aes128-ctr"、"aes192-ctr"、"aes256-ctr"、"sm4-ctr" (仅 v6.4.0 及之后版本) 和 "plaintext"。
    ## 默认值为 "plaintext"，即默认不开启加密功能。选择 "plaintext" 以外的值则表示启用加密功能。此时必须指定主密钥。
    data-encryption-method = "aes128-ctr"
    ## 轮换密钥的频率，默认值：`7d`。
    data-key-rotation-period = "168h" # 7 days

[security.encryption.master-key]
    ## 指定启用加密时的主密钥。若要了解如何配置主密钥，可以参考《静态加密 - 配置加密》：https://docs.pingcap.com/zh/tidb/dev/encryption-at-rest#配置加密

[security.encryption.previous-master-key]
    ## 指定轮换新主密钥时的旧主密钥。旧主密钥的配置格式与主密钥相同。若要了解如何配置主密钥，可以参考《静态加密 - 配置加密》：https://docs.pingcap.com/zh/tidb/dev/encryption-at-rest#配置加密
```

### 通过拓扑 label 进行副本调度

[TiFlash 设置可用区](/tiflash/create-tiflash-replicas.md#设置可用区)

### 多盘部署

TiFlash 支持单节点多盘部署。如果你的部署节点上有多块硬盘，可以通过以下的方式配置参数，提高节点的硬盘 I/O 利用率。TiUP 中参数配置格式参照[详细 TiFlash 配置模版](/tiflash-deployment-topology.md#拓扑模版)。

#### TiDB 集群版本低于 v4.0.9

TiDB v4.0.9 之前的版本中，TiFlash 只支持将存储引擎中的主要数据分布在多盘上。通过 `path`（TiUP 中为 `data_dir`）和 `path_realtime_mode` 这两个参数配置多盘部署。

多个数据存储目录在 `path` 中以英文逗号分隔，比如 `/nvme_ssd_a/data/tiflash,/sata_ssd_b/data/tiflash,/sata_ssd_c/data/tiflash`。如果你的节点上有多块硬盘，推荐把性能最好的硬盘目录放在最前面，以更好地利用节点性能。

如果节点上有多块相同规格的硬盘，可以把 `path_realtime_mode` 参数留空（或者把该值明确地设为 `false`）。这表示数据会在所有的存储目录之间进行均衡。但由于最新的数据仍然只会被写入到第一个目录，因此该目录所在的硬盘会较其他硬盘繁忙。

如果节点上有多块规格不一致的硬盘，推荐把 `path_relatime_mode` 参数设置为 `true`，并且把性能最好的硬盘目录放在 `path` 参数内的最前面。这表示第一个目录只会存放最新数据，较旧的数据会在其他目录之间进行均衡。注意此情况下，第一个目录规划的容量大小需要占总容量的约 10%。

#### TiDB 集群版本为 v4.0.9 及以上

TiDB v4.0.9 及之后的版本中，TiFlash 支持将存储引擎的主要数据和新数据都分布在多盘上。多盘部署时，推荐使用 `[storage]` 中的参数，以更好地利用节点的 I/O 性能。但 TiFlash 仍然支持 [TiDB 集群版本低于 v4.0.9](#tidb-集群版本低于-v409) 中的参数。

如果节点上有多块相同规格的硬盘，推荐把硬盘目录填到 `storage.main.dir` 列表中，`storage.latest.dir` 列表留空。TiFlash 会在所有存储目录之间分摊 I/O 压力以及进行数据均衡。

如果节点上有多块规格不同的硬盘，推荐把 I/O 性能较好的硬盘目录配置在 `storage.latest.dir` 中，把 I/O 性能较一般的硬盘目录配置在 `storage.main.dir` 中。例如节点上有一块 NVMe-SSD 硬盘加上两块 SATA-SSD 硬盘，你可以把 `storage.latest.dir` 设为 `["/nvme_ssd_a/data/tiflash"]` 以及把 `storage.main.dir` 设为 `["/sata_ssd_b/data/tiflash", "/sata_ssd_c/data/tiflash"]`。TiFlash 会根据两个目录列表分别进行 I/O 压力分摊及数据均衡。需要注意此情况下，`storage.latest.dir` 中规划的容量大小需要占总规划容量的约 10%。

> **警告：**
>
> `[storage]` 参数从 TiUP v1.2.5 版本开始支持。如果你的 TiDB 版本为 v4.0.9 及以上，请确保你的 TiUP 版本不低于 v1.2.5，否则 `[storage]` 中定义的数据目录不会被 TiUP 纳入管理。
