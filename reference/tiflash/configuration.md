---
title: TiFlash 配置参数
category: reference
---

# TiFlash 配置参数

本文介绍了与部署使用 TiFlash 相关的配置参数。

## PD 调度参数

可通过 [pd-ctl](/reference/tools/pd-control.md)（tidb-ansible 目录下的 `resources/bin` 包含对应的二进制文件）调整参数：

- [`replica-schedule-limit`](/reference/configuration/pd-server/configuration-file.md#replica-schedule-limit)：用来控制 replica 相关 operator 的产生速度（涉及到下线、补副本的操作都与该参数有关）

    > **注意：**
    >
    > 不要超过 `region-schedule-limit`，否则会影响正常 TiKV 之间的 Region 调度。

- [`store-balance-rate`](/reference/configuration/pd-server/configuration-file.md#store-balance-rate)：用于限制每个 store 的调度速度

## TiFlash 配置参数

### 配置文件 tiflash.toml

```
tmp_path = tiflash 临时文件存放路径
path = tiflash 数据存储路径     # 如果有多个目录，以英文逗号分割，比如 `/ssd_a/data/tiflash,/hdd_b/data/tiflash,/hdd_c/data/tiflash`。如果您的环境有多块磁盘，推荐一个路径对应一块磁盘，并且把性能最好的磁盘放在最前面，以发挥所有磁盘的全部性能。
path_realtime_mode = false # 默认为 false。如果设为 true，且 path 配置了多个目录，表示在第一个目录存放最新数据，较旧的数据存放于其他目录。
listen_host = tiflash 服务监听 host # 一般配置成 0.0.0.0
tcp_port = tiflash tcp 服务端口
http_port = tiflash http 服务端口
```

```
[flash]
    tidb_status_addr = tidb status 端口地址 # 多个地址以逗号分割
    service_addr =  tiflash raft 服务 和 coprocessor 服务监听地址
```

多个 TiFlash 节点会选一个 master 来负责往 PD 增删 placement rule，需要 3 个参数控制。

```
[flash.flash_cluster]
    refresh_interval = master 定时刷新有效期
    update_rule_interval = master 定时向 tidb 获取 tiflash 副本状态并与 pd 交互
    master_ttl = master 选出后的有效期
    cluster_manager_path = pd buddy 所在目录的绝对路径
    log = pd buddy log 路径

[flash.proxy]
    addr = proxy 监听地址
    advertise-addr = proxy 对外访问地址
    data-dir = proxy 数据存储路径
    config = proxy 配置文件路径
    log-file = proxy log 路径

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
```

### 配置文件 tiflash-learner.toml

```
[server]
    engine-addr = tiflash raft 服务监听地址
    status-addr = Prometheus 拉取 proxy metrics 信息的 ip + 端口
```
