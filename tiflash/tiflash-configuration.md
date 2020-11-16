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

- [`store-balance-rate`](/pd-configuration-file.md#store-balance-rate)：用于限制每个 TiKV store 或 TiFlash store 的 Region 调度速度。注意这个参数只对新加入集群的 store 有效，如果想立刻生效请用下面的方式。

    > **注意：**
    >
    > 4.0.2 版本之后（包括 4.0.2 版本）废弃了 `store-balance-rate` 参数且 `store limit` 命令有部分变化。该命令变化的细节请参考 [store-limit 文档](/configure-store-limit.md)。

    - 使用 `pd-ctl -u <pd_ip:pd_port> store limit <store_id> <value>` 命令单独设置某个 store 的 Region 调度速度。（`store_id` 可通过 `pd-ctl -u <pd_ip:pd_port> store` 命令获得）如果没有单独设置，则继承 `store-balance-rate` 的设置。你也可以使用 `pd-ctl -u <pd_ip:pd_port> store limit` 命令查看当前设置值。

## TiFlash 配置参数

### 配置文件 tiflash.toml

```toml
tmp_path = tiflash 临时文件存放路径
path = tiflash 数据存储路径     # 如果有多个目录，以英文逗号分隔
path_realtime_mode = false # 默认为 false。如果设为 true，且 path 配置了多个目录，表示在第一个目录存放最新数据，较旧的数据存放于其他目录。
listen_host = tiflash # TCP/HTTP 等辅助服务的监听 host，建议配置成 0.0.0.0
tcp_port = tiflash tcp 服务端口
http_port = tiflash http 服务端口
mark_cache_size = 5368709120 # 数据块元信息的内存 cache 大小限制，通常不需要修改
minmax_index_cache_size = 5368709120 # 数据块 min-max 索引的内存 cache 大小限制，通常不需要修改
```

```toml
[flash]
    tidb_status_addr = tidb status 端口地址 # 多个地址以逗号分割
    service_addr =  tiflash raft 服务 和 coprocessor 服务监听地址
```

多个 TiFlash 节点会选一个 master 来负责往 PD 增删 placement rule，需要 3 个参数控制。

```toml
[flash.flash_cluster]
    refresh_interval = master 定时刷新有效期
    update_rule_interval = master 定时向 tidb 获取 tiflash 副本状态并与 pd 交互
    master_ttl = master 选出后的有效期
    cluster_manager_path = pd buddy 所在目录的绝对路径
    log = pd buddy log 路径

[flash.proxy]
    addr = proxy 监听地址
    advertise-addr = 外部访问 addr 的地址，不填则默认是 addr
    data-dir = proxy 数据存储路径
    config = proxy 配置文件路径
    log-file = proxy log 路径
    status-addr = 拉取 proxy metrics｜status 信息的监听地址
    advertise-status-addr = 外部访问 status-addr 的地址，不填则默认是 status-addr

[logger]
    level = log 级别（支持 trace、debug、information、warning、error）
    log = tiflash log 路径
    errorlog = tiflash error log 路径
    size = 单个日志文件的大小
    count = 最多保留日志文件个数
[raft]
    kvstore_path = kvstore 数据存储路径 # 默认为 "{path 的第一个目录}/kvstore"
    pd_addr = pd 服务地址 # 多个地址以逗号隔开
[status]
    metrics_port = Prometheus 拉取 metrics 信息的端口
[profiles]
[profiles.default]
    dt_enable_logical_split = true # 存储引擎的 segment 分裂是否使用逻辑分裂。使用逻辑分裂可以减小写放大，提高写入速度，但是会造成一定的空间浪费。默认为 true
    max_memory_usage = 0 # 单次 coprocessor 查询过程中，对中间数据的内存限制，单位为 byte，默认为 0，表示不限制
    max_memory_usage_for_all_queries = 0 # 所有查询过程中，对中间数据的内存限制，单位为 byte，默认为 0，表示不限制
```

### 配置文件 tiflash-learner.toml

```toml
[server]
    engine-addr = 外部访问 tiflash coprocessor 服务的地址
[raftstore]
    snap-handle-pool-size = 控制处理 snapshot 的线程数，默认为 2。设为 0 则关闭多线程优化
    store-batch-retry-recv-timeout = 控制 raft store 持久化 WAL 的最小间隔。通过适当增大延迟以减少 IOPS 占用，默认为 4ms，设为 0ms 则关闭该优化。
```

除以上几项外，其余功能参数和 TiKV 的配置相同。需要注意的是：`tiflash.toml [flash.proxy]` 中的配置项会覆盖 `tiflash-learner.toml` 中的重合参数；`key` 为 `engine` 的 `label` 是保留项，不可手动配置。

### 多盘部署

TiFlash 支持多盘部署，主要通过[配置文件 `tiflash.toml`](#配置文件-tiflashtoml) 中的 `path` 和 `path_realtime_mode` 这两个参数控制。

多个数据存储目录在 `path` 中以英文逗号分隔，比如 `/ssd_a/data/tiflash,/hdd_b/data/tiflash,/hdd_c/data/tiflash`。如果你的环境有多块磁盘，推荐一个数据存储目录对应一块磁盘，并且把性能最好的磁盘放在最前面，以发挥所有磁盘的全部性能。

`path_realtime_mode` 参数默认值为 false，表示数据会在所有的存储目录之间进行均衡。如果设为 true，且 `path` 配置了多个目录，表示第一个目录只会存放最新数据，较旧的数据会在其他目录之间进行均衡。
