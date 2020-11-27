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
# tiflash TCP/HTTP 等辅助服务的监听 host，建议配置成 0.0.0.0
listen_host = "0.0.0.0"
## tiflash tcp 服务端口
tcp_port = 9000
## tiflash http 服务端口
http_port = 8123
## 数据块元信息的内存 cache 大小限制，通常不需要修改
mark_cache_size = 5368709120
## 数据块 min-max 索引的内存 cache 大小限制，通常不需要修改
minmax_index_cache_size = 5368709120

## tiflash 数据存储路径，如果有多个目录，以英文逗号分隔。
## 从 v4.0.9 版本开始 path 及 path_realtime_mode 参数不再推荐使用，推荐使用 [storage] 下的配置项代替，在多盘部署的情况下能更好地利用节点性能。
# path = "/tidb-data/tiflash-9000"
## 或
# path = "/ssd0/tidb-data/tiflash,/ssd1/tidb-data/tiflash,/ssd2/tidb-data/tiflash"
## 默认为 false。如果设为 true，且 path 配置了多个目录，表示在第一个目录存放最新数据，较旧的数据存放于其他目录。
# path_realtime_mode = false

## tiflash 临时文件存放路径
# tmp_path = "/tidb-data/tiflash-9000/tmp"

## 存储路径相关配置， 从 v4.0.9 开始生效
[storage]
    ## 如果节点上有多块 SSD 硬盘，推荐一个数据存储目录对应一块硬盘，并把数据目录填到列表 `storage.main.dir` 中，
    ## 以更好地利用节点性能。

    ## 如果节点上有多块 IO 性能相差较大的硬盘（如一块 SSD 硬盘加上多块 HDD 硬盘），如下配置可以更好地利用节点性能。
    ## * 把 SSD 硬盘的数据存储目录配置在 `storage.latest.dir` 中
    ## * 把 HDD 硬盘的数据存储目录配置在 `storage.main.dir` 中

    [storage.main]
    ## 用于存储主要数据的目录列表
    dir = [ "/tidb-data/tiflash-9000" ] 
    ## 或
    # dir = [ "/ssd0/tidb-data/tiflash", "/ssd1/tidb-data/tiflash" ]

    ## storage.main.dir 存储目录列表中，每个目录的最大可用容量。
    ## * 在未定义配置项，或者列表中全填 0时，会使用目录所在的硬盘容量
    ## * 以 byte 为单位，目前不支持如 "10GB" 类似的设置
    ## * capacity 列表的长度应当与 dir 长度保持一致
    ## 例如：
    # capacity = [ 10737418240, 10737418240 ]

    [storage.latest]
    ## 用于存储新数据的目录列表。
    ## 在未配置或者为空列表的情况下，会使用 `storage.main.dir` 的值。
    # dir = [ ]
    ## storage.latest.dir 存储目录列表中，每个目录的最大可用容量。
    # capacity = [ 10737418240, 10737418240 ]

    [storage.raft]
    ## 用于存储 Raft 数据的目录列表。
    ## 在未定义配置项或者为空列表的情况下，会以 `storage.latest.dir` 的列表目录中每一项添加 "/kvstore" 作为此项的值。
    # dir = [ ]

[flash]
    tidb_status_addr = tidb status 端口地址 # 多个地址以逗号分割
    service_addr =  tiflash raft 服务 和 coprocessor 服务监听地址

# 多个 TiFlash 节点会选一个 master 来负责往 PD 增删 placement rule，通过 flash.flash_cluster 中的参数控制。
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
    pd_addr = pd 服务地址 # 多个地址以逗号隔开
    ## 用于存储 Raft 数据的目录，默认为 "{path 的第一个目录}/kvstore"
    ## 从 v4.0.9 版本开始 raft.kvstore_path 参数不再推荐使用，推荐使用 "storage.raft.dir" 配置项代替，在多盘部署的情况下能更好地利用节点性能。
    # kvstore_path = "/tidb-data/tiflash-9000/kvstore"

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
```

### 配置文件 tiflash-learner.toml

```toml
[server]
    engine-addr = 外部访问 tiflash coprocessor 服务的地址
[raftstore]
    ## 控制处理 snapshot 的线程数，默认为 2。设为 0 则关闭多线程优化
    snap-handle-pool-size = 2
    ## 控制 raft store 持久化 WAL 的最小间隔。通过适当增大延迟以减少 IOPS 占用，默认为 4ms，设为 0ms 则关闭该优化。
    store-batch-retry-recv-timeout = "4ms"
```

除以上几项外，其余功能参数和 TiKV 的配置相同。需要注意的是：`tiflash.toml [flash.proxy]` 中的配置项会覆盖 `tiflash-learner.toml` 中的重合参数；`key` 为 `engine` 的 `label` 是保留项，不可手动配置。

### 多盘部署

TiFlash 支持单节点多盘部署。如果你的部署节点上有多块硬盘，可以通过以下的方式配置参数，提高节点的硬盘IO利用率。

#### 全新部署

如果你部署的 TiDB 集群版本 >= v4.0.9：

可以通过配置文件 [`tiflash.toml`](#配置文件-tiflashtoml) 中的 `[storage]` 项控制。下方所述的 v4.0.9 版本之前的参数，在新版本中仍然支持。但 `[storage]` 中的参数在多盘部署时，新增支持对 Raft 数据以及存储引擎中的新数据分布到多盘的特性，以便更好地利用所有硬盘性能，因此新版本中推荐使用新的配置项来配置存储路径。

如果节点上有多块 SSD 硬盘，推荐一个数据存储目录对应一块硬盘，并把数据目录填到列表 `storage.main.dir` 中，以更好地利用节点性能。

如果节点上有多块 IO 性能相差较大的硬盘，把 SSD 硬盘的数据存储目录配置在 `storage.latest.dir` 中，把 HDD 硬盘的数据存储目录配置在 `storage.main.dir` 中，可以更好地利用节点性能。例如 TiFlash 节点上有一块 SSD 硬盘加上两块 HDD 硬盘，你可以把 `storage.latest.dir` 设为 `["/ssd_a/data/tiflash"]` 以及把 `storage.main.dir` 设为 `["/hdd_b/data/tiflash", "/hdd_c/data/tiflash"]`。

> **注意：**
>
> [storage] 参数在 TiUP v1.2.5 版本开始支持。请确保你的 TiUP 版本不低于 v1.2.5，否则 [storage] 中定义数据目录不会被纳入 TiUP 管理。

如果你部署的 TiDB 集群版本 < v4.0.9：

通过配置文件 [`tiflash.toml`](#配置文件-tiflashtoml) 中的 `path` 和 `path_realtime_mode` 这两个参数控制。

多个数据存储目录在 `path` 中以英文逗号分隔，比如 `/ssd_a/data/tiflash,/hdd_b/data/tiflash,/hdd_c/data/tiflash`。如果你的节点上有多块硬盘，推荐一个数据存储目录对应一块硬盘，并且把性能最好的硬盘放在最前面，以更好地利用节点性能。

`path_realtime_mode` 参数默认值为 false，表示数据会在所有的存储目录之间进行均衡，适用于单节点多块 SSD 硬盘的部署。

`path_relatime_mode` 如果设为 true，且 `path` 配置了多个目录，表示第一个目录只会存放最新数据，较旧的数据会在其他目录之间进行均衡。适用于单个节点上一块 SSD 硬盘加上多块 HDD 硬盘的部署。

#### 升级节点版本至不低于 v4.0.9

v4.0.9 之前的版本中，TiFlash 只支持将存储引擎中的主要数据分布在多盘上。v4.0.9 及之后的版本中，TiFlash 支持将存储引擎的主要数据、新数据，以及 Raft 数据分布在多盘上。

如果你的节点上只有单个存储路径，或者是一块 SSD 硬盘加上多块 HDD 硬盘的部署方式，新的配置项对此没有性能提升的效果，因此升级后可直接保留旧的配置项。

如果节点上是多个 SSD 硬盘存储路径，适当使用新的配置项可以提高硬盘的 IO 资源利用效率。如果你的 TiFlash 节点遇到硬盘 IO 瓶颈，可参考以下指引，利用 TiUP 升级配置项：

> **注意：**
>
> 升级后并且把 TiFlash 节点修改为使用 [storage] 配置后，如果将进群版本降级到低于 v4.0.9 的版本操作，可能导致 TiFlash 部分数据丢失。

1. 保证 TiUP 版本不低于 v1.2.5，否则新的 TiFlash 配置项中的数据存储目录不会被纳入 TiUP 管理

2. 使用 TiUP 正常[升级集群](/upgrade-tidb-using-tiup.md#使用-tiup-升级-tidb)至你所需要的版本

3. 阅读下述新旧配置参数说明，理解 TiFlash 的行为并决定你所需要设置的配置项的值

4. 使用 TiUP [修改节点的配置项](/maintain-tidb-using-tiup.md#修改配置参数)。在你的 TiFlash 节点配置的 `config` 一项中，添加 `storage.main.dir`, `storage.latest.dir` 等配置项，格式可参照 [详细 TiFlash 配置模版](https://github.com/pingcap/docs-cn/blob/master/config-templates/complex-tiflash.yaml)

TiUP 配置参数新旧对比说明：

对于未配置 `path_realtime_mode` 或者其值为 false 的情况：

```yaml
tiflash_servers:
  - host: 10.0.1.14
    data_dir: "/nvme_ssd0/tiflash,/nvme_ssd1/tiflash"
    config:
      # path_realtime_mode: false # 默认值
```

等价于以下配置。可以参考里面的注释，调整 `storage.latest.dir` 的值，以获得更好的性能。

```yaml
tiflash_servers:
  - host: 10.0.1.14
    data_dir: "/nvme_ssd0/tiflash,/nvme_ssd1/tiflash"
    config:
      storage.main.dir:     [ "/nvme_ssd0/tiflash", "/nvme_ssd1/tiflash" ]
      ## 旧的配置项，相当于新的数据只会写到第一块硬盘
      storage.latest.dir:   [ "/nvme_ssd0/tiflash" ]
      ## 可以把该列表扩展至与 storage.main.dir 一致，以更好地利用多块硬盘的 IO 性能
      # storage.latest.dir: [ "/nvme_ssd0/tiflash", "/nvme_ssd1/tiflash" ]
```

对于配置了 `path_realtime_mode` 为 true 的情况：

```yaml
tiflash_servers:
  - host: 10.0.1.14
    data_dir: "/nvme_ssd0/tiflash,/hdd1/tiflash,/hdd2/tiflash"
    config:
      path_realtime_mode: true
```

等价于以下配置。此情况下建议保留此行为以获得更好的性能。

```yaml
tiflash_servers:
  - host: 10.0.1.14
    data_dir: "/nvme_ssd0/tiflash,/hdd1/tiflash,/hdd2/tiflash"
    config:
      ## HDD 盘作为主要存储
      storage.main.dir:   [ "/hdd1/tiflash", "/hdd2/tiflash" ]
      ## SSD 盘作为新数据的存储
      storage.latest.dir: [ "/nvme_ssd0/tiflash" ]
```

> **注意：**
>
> 对于非 TiUP 管理的集群，可以参考上述说明，修改 tiflash.toml 中对应的配置项。
