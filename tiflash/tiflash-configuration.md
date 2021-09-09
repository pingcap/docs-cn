---
title: TiFlash 配置参数
aliases: ['/docs-cn/dev/tiflash/tiflash-configuration/','/docs-cn/dev/reference/tiflash/configuration/']
---

# TiFlash 配置参数

本文介绍了与部署使用 TiFlash 相关的配置参数。

## PD 调度参数

可通过 [pd-ctl](/pd-control.md) 调整参数。如果你使用 TiUP 部署，可以用 `tiup ctl pd` 代替 `pd-ctl -u <pd_ip:pd_port>` 命令。

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

### 配置文件 tiflash.toml

```toml
## TiFlash TCP/HTTP 等辅助服务的监听 host。建议配置成 0.0.0.0，即监听本机所有 IP 地址。
listen_host = "0.0.0.0"
## TiFlash TCP 服务的端口
tcp_port = 9000
## TiFlash HTTP 服务的端口
http_port = 8123
## 数据块元信息的内存 cache 大小限制，通常不需要修改
mark_cache_size = 5368709120
## 数据块 min-max 索引的内存 cache 大小限制，通常不需要修改
minmax_index_cache_size = 5368709120
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
    ## 该参数从 v5.2.0 开始废弃，请使用 `[storage.io_rate_limit]` 相关配置
    # bg_task_io_rate_limit = 0

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
    ## 分别用两个配置项控制读写带宽限制，适用于一些读写带宽限制分开计算的云盘，例如 GCP 上的 persistent disk。
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

[flash]
    tidb_status_addr = tidb status 端口地址 # 多个地址以逗号分割
    service_addr =  TiFlash raft 服务 和 coprocessor 服务监听地址

# 多个 TiFlash 节点会选一个 master 来负责往 PD 增删 placement rule，通过 flash.flash_cluster 中的参数控制。
[flash.flash_cluster]
    refresh_interval = master 定时刷新有效期
    update_rule_interval = master 定时向 tidb 获取 TiFlash 副本状态并与 pd 交互
    master_ttl = master 选出后的有效期
    cluster_manager_path = pd buddy 所在目录的绝对路径
    log = pd buddy log 路径

[flash.proxy]
    addr = proxy 监听地址
    advertise-addr = 外部访问 addr 的地址，不填则默认是 addr
    data-dir = proxy 数据存储路径
    config = proxy 配置文件路径
    log-file = proxy log 路径
    log-level = proxy log 级别，默认为 "info"
    status-addr = 拉取 proxy metrics｜status 信息的监听地址
    advertise-status-addr = 外部访问 status-addr 的地址，不填则默认是 status-addr

[logger]
    level = log 级别（支持 trace、debug、information、warning、error）
    log = TiFlash log 路径
    errorlog = TiFlash error log 路径
    size = 单个日志文件的大小
    count = 最多保留日志文件个数

[raft]
    pd_addr = pd 服务地址 # 多个地址以逗号隔开

[status]
    metrics_port = Prometheus 拉取 metrics 信息的端口

[profiles]

[profiles.default]
    ## 存储引擎的 segment 分裂是否使用逻辑分裂。使用逻辑分裂可以减小写放大，提高写入速度，但是会造成一定程度的硬盘空间回收不及时。默认为 true
    dt_enable_logical_split = true
    ## 单次 coprocessor 查询过程中，对中间数据的内存限制，单位为 byte，默认为 0，表示不限制
    max_memory_usage = 0
    ## 所有查询过程中，对中间数据的内存限制，单位为 byte，默认为 0，表示不限制
    max_memory_usage_for_all_queries = 0
    ## 从 v5.0 引入，表示 TiFlash Coprocessor 最多同时执行的 cop 请求数量。如果请求数量超过了该配置指定的值，多出的请求会排队等待。如果设为 0 或不设置，则使用默认值，即物理核数的两倍。
    cop_pool_size = 0
    ## 从 v5.0 引入，表示 TiFlash Coprocessor 最多同时执行的 batch 请求数量。如果请求数量超过了该配置指定的值，多出的请求会排队等待。如果设为 0 或不设置，则使用默认值，即物理核数的两倍。
    batch_cop_pool_size = 0

## 安全相关配置，从 v4.0.5 开始生效
[security]
    ## 若开启该选项，日志中的用户数据会以 `?` 代替显示
    ## 注意，tiflash-learner 对应的安全配置选项为 `security.redact-info-log`，需要在 tiflash-learner.toml 中另外开启
    # redact_info_log = false

    ## 包含可信 SSL CA 列表的文件路径。如果你设置了该值，`cert_path` 和 `key_path` 中的路径也需要填写
    # ca_path = "/path/to/ca.pem"
    ## 包含 PEM 格式的 X509 certificate 文件路径
    # cert_path = "/path/to/tiflash-server.pem"
    ## 包含 PEM 格式的 X509 key 文件路径
    # key_path = "/path/to/tiflash-server-key.pem"
```

### 配置文件 tiflash-learner.toml

```toml
[server]
    engine-addr = 外部访问 TiFlash coprocessor 服务的地址
[raftstore]
    ## 控制处理 snapshot 的线程数，默认为 2。设为 0 则关闭多线程优化
    snap-handle-pool-size = 2
    ## 控制 raft store 持久化 WAL 的最小间隔。通过适当增大延迟以减少 IOPS 占用，默认为 4ms，设为 0ms 则关闭该优化。
    store-batch-retry-recv-timeout = "4ms"
```

除以上几项外，其余功能参数和 TiKV 的配置相同。需要注意的是：`tiflash.toml [flash.proxy]` 中的配置项会覆盖 `tiflash-learner.toml` 中的重合参数；`key` 为 `engine` 的 `label` 是保留项，不可手动配置。

### 多盘部署

TiFlash 支持单节点多盘部署。如果你的部署节点上有多块硬盘，可以通过以下的方式配置参数，提高节点的硬盘 I/O 利用率。TiUP 中参数配置格式参照[详细 TiFlash 配置模版](https://github.com/pingcap/docs-cn/blob/master/config-templates/complex-tiflash.yaml)。

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
> * `[storage]` 参数从 TiUP v1.2.5 版本开始支持。如果你的 TiDB 版本为 v4.0.9 及以上，请确保你的 TiUP 版本不低于 v1.2.5，否则 `[storage]` 中定义的数据目录不会被 TiUP 纳入管理。
> * 在 TiFlash 节点改为使用 `[storage]` 配置后，如果将集群版本降级到低于 v4.0.9，可能导致 TiFlash 部分数据丢失。
