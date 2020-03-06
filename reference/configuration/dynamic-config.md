# 动态配置变更使用文档

动态配置变更主要是支持包括 TiDB，TiKV，PD 在内的各组件的配置进行在线更新。用户可以通过利用动态配置变更对各组件进行性能调优而无需重启集群组件。

## 开启动态配置变更

4.0 版本默认开启该参数，可通过修改 TiDB，TiKV，PD 配置文件中的 `enable-dynamic-config = false` 关闭该功能。

## 常用操作

目前可通过 pd-ctl 对各组件（TiDB，TiKV，PD）进行修改和查看。

### 查看组件实例

可通过 `component ids <component>` 查看组件实例。其中 `component` 为组件类型，目前支持 `tidb`，`tikv`，`pd` 三种类型。

示例如下：

```bash
>> component ids tikv
[
    "127.0.0.1:20160",
    "127.0.0.1:20161",
    "127.0.0.1:20162"
]
```

### 修改配置

#### 修改全局配置

可通过 `component set <component> <key> <value>` 进行设置，其中 `component` 为组件类型，含义同上。`key` 为参数名称，`value` 为参数值。

示例如下：

```bash
>> component set tikv gc.batch-keys 1024
```

上述命令会将所有 TiKV 实例的 GC 的参数 `batch-keys` 设置为 1024。

#### 修改实例配置

可通过 `component set <component ID> <key> <value>` 进行设置，其中 `component ID` 为实例的 IP 地址加端口，如 `127.0.0.1:20160`。可通过使用 `ids` 命令进行查看。

示例如下：

```bash
>> component set 127.0.0.1:20160 gc.batch-keys 1024
```

上述命令仅将 `127.0.0.1:20160` 这个 TiKV 实例的 GC 的参数 `batch-keys` 设置为 1024。

### 查看配置

可通过 `component show <component ID>` 查看具体实例的配置。`component ID` 为实例的 IP 地址加端口，含义同上。

示例如下：

```bash
>> component show 127.0.0.1:20160
```

```bash
dynamic-config = true
log-file = ""
log-level = "info"
log-rotation-size = "300MiB"
log-rotation-timespan = "1d"
panic-when-unexpected-key-or-data = false
refresh-config-interval = "30s"

[coprocessor]
  batch-split-limit = 10
  region-max-keys = 1440000
  region-max-size = "144MiB"
  region-split-keys = 960000
  region-split-size = "96MiB"
  split-region-on-table = false

[gc]
  batch-keys = 512
  max-write-bytes-per-sec = "0KiB"
  ratio-threshold = 1.1

[import]
  num-threads = 8
  stream-channel-window = 128

[metric]
  address = ""
  interval = "15s"
  job = "tikv"

[pd]
  endpoints = ["127.0.0.1:2379"]
  retry-interval = "300ms"
  retry-log-every = 10
  retry-max-count = 9223372036854775807

[pessimistic-txn]
  enabled = true
  wait-for-lock-timeout = 1000
  wake-up-delay-duration = 20
...
```

### 删除实例配置

可通过 `component delete <component ID>` 进行删除，其中 `component ID` 为实例的 IP 地址加端口，如 `127.0.0.1:20160`。可通过使用 `ids` 命令进行查看。主要用于下线节点后，将配置删除。通常该命令无需手动操作。

## 支持的参数列表

### TiDB

| 参数 | 简介 |
| --- | --- |
| performance.max-procs | Go 使用最大线程数，动态修改可能引起系统抖动  |
| performance.max-memory | prepare plan 使用的最大内存  |
| performance.cross-join | 是否允许在没有等值条件时使用 Join (相当于做笛卡尔积) |
| performance.feedback-probability | 统计信息使用 feedback 方式搜集数据的比例 |
| performance.query-feedback-limit | 内存中缓存的 feedback 信息数 |
| performance.pseudo-estimate-ratio | 修改过的行数/表的总行数的比值，超过该值时系统会认为统计信息已经过期，会采用 pseudo 的统计信息 |
| performance.stmt-count-limit | TiDB 一个事务允许的最大语句条数限制 |
| performance.tcp-keep-alive | TiDB 在 TCP 层开启 keepalive |
| oom-action | 指定 TiDB 发生 out-of-memory 错误时的操作 |
| mem-quota-query | 单条 SQL 语句可以占用的最大内存阈值 |
| tikv-client.store-limit | Store 的调度限流阈值 |
| log.level | 日志等级 |
| log.slow-threshold| 输出慢日志的耗时阈值 |
| log.query-log-max-len | 最长的 SQL 输出长度 |
| log.expensive-threshold | 输出 expensive 操作的行数阈值 |
| check-mb4-value-in-utf8 | 开启检查 utf8mb4 字符的开关，如果开启此功能，字符集是 utf8，且在 utf8 插入 mb4 字符，系统将会报错 |
| enable-streaming | 开启 coprocessor 的 streaming 获取数据模式 |
| txn-local-latches.capacity | Hash 对应的 slot 数，会自动向上调整为 2 的指数倍。每个 slot 占 32 Bytes 内存。当写入数据的范围比较广时（如导数据），设置过小会导致变慢，性能下降 |
| compatible-kill-query | 设置 KILL 语句的兼容性 |
| treat-old-version-utf8-as-utf8mb4 | 将旧表中的 utf8 字符集当成 utf8mb4的开关 |
| opentracing.enable | 是否开启 opentracing 功能 |
| prepared-plan-cache.enable | 是否开启 prepare 语句的 plan cache | 

具体参数意义可参考 [TiDB 配置文件描述](https://github.com/pingcap/docs-cn/blob/master/reference/configuration/tidb-server/configuration-file.md)。

### TiKV

| 参数 | 简介 |
| --- | --- |
| refresh-config-interval | 尝试更新配置的时间间隔 |
| raftstore.sync-log | 数据、log 落盘是否 sync |
| raftstore.raft-entry-max-size | 单个日志最大大小 |
| raftstore.raft-log-gc-tick-interval | 删除 raft 日志的轮询任务调度间隔时间 |
| raftstore.raft-log-gc-threshold | 允许残余的 raft 日志个数，软限制 |
| raftstore.raft-log-gc-count-limit | 允许残余的 raft 日志个数，硬限制 |
| raftstore.raft-log-gc-size-limit | 允许残余的 raft 日志大小，硬限制 |
| raftstore.raft-entry-cache-life-time | 内存中日志 cache 允许的最长残留时间 |
| raftstore.raft-reject-transfer-leader-duration | 控制迁移 leader 到新加节点的最小时间 |
| raftstore.split-region-check-tick-interval | 检查 region 是否需要分裂的时间间隔 |
| raftstore.region-split-check-diff | 允许 region 数据超过指定大小的最大值 |
| raftstore.region-compact-check-interval | 检查是否需要人工触发 rocksdb compaction 的时间间隔 |
| raftstore.region-compact-check-step | 每轮校验人工 compaction 时，一次性检查的 region 个数 |
| raftstore.region-compact-min-tombstones | 触发 rocksdb compaction 需要的 tombstone 个数 |
| raftstore.region-compact-tombstones-percent | 触发 rocksdb compaction 需要的 tombstone 所占比例 |
| raftstore.pd-heartbeat-tick-interval | 触发 region 对 PD 心跳的时间间隔 |
| raftstore.pd-store-heartbeat-tick-interval | 触发 store 对 PD 心跳的时间间隔 |
| raftstore.snap-mgr-gc-tick-interval | 触发回收过期 snapshot 文件的时间间隔 |
| raftstore.snap-gc-timeout | snapshot 文件的最长保存时间 |
| raftstore.lock-cf-compact-interval | 触发对 lock CF compact 检查的时间间隔 |
| raftstore.lock-cf-compact-bytes-threshold | 触发对 lock CF 进行 compact 的大小 |
| raftstore.messages-per-tick | 每轮处理的消息最大个数 |
| raftstore.max-peer-down-duration | 副本允许的最长未响应时间 |
| raftstore.max-leader-missing-duration | 允许副本处于无主状态的最长时间 |
| raftstore.abnormal-leader-missing-duration | 允许副本处于无主状态的时间 |
| raftstore.peer-stale-state-check-interval | 触发检验副本是否处于无主状态的时间间隔 |
| raftstore.consistency-check-interval | 触发一致性检查的时间间隔 |
| raftstore.raft-store-max-leader-lease | region 主可信任期的最长时间 |
| raftstore.allow-remove-leader | 允许删除主开关 |
| raftstore.merge-check-tick-interval | 触发 merge 完成检查的时间间隔 |
| raftstore.cleanup-import-sst-interval | 触发检查过期 SST 文件的时间间隔 |
| raftstore.local-read-batch-size | 一轮处理读请求的最大个数 |
| coprocessor.split-region-on-table | 开启按 table 分裂 Region的开关 |
| coprocessor.batch-split-limit | 批量分裂 Region 的阈值 |
| coprocessor.region-max-size | Region 容量空间最大值 |
| coprocessor.region-split-size | 分裂后新 Region 的大小 |
| coprocessor.region-max-keys | Region 最多允许的 key 的个数 |
| coprocessor.region-split-keys | 分裂后新 Region 的 key 的个数 |
| pessimistic-txn.wait-for-lock-timeout | 悲观事务遇到锁后的等待的最长时间 |
| pessimistic-txn.wake-up-delay-duration | 悲观事务被重新唤醒的时间 |
| gc.ratio-threshold | 跳过 Region GC 的阈值（GC 版本个数/key 个数）
| gc.batch-keys | 一轮处理 key 的个数 |
| gc.max-write-bytes-per-sec | 一秒可写入 rocksdb 的最大字节数 |
| {db-name}.max-total-wal-size | WAL 总大小限制 |
| {db-name}.max-background-jobs | RocksDB 后台线程个数 |
| {db-name}.max-open-files | RocksDB 可以打开的文件总数 |
| {db-name}.compaction-readahead-size | Compaction 时候 readahead 的大小 |
| {db-name}.bytes-per-sync | 异步 Sync 限速速率 |
| {db-name}.wal-bytes-per-sync | WAL Sync 限速速率 |
| {db-name}.writable-file-max-buffer-size | WritableFileWrite 所使用的最大的 buffer 大小 |
| {db-name}.{cf-name}.block-cache-size | block cache size 大小 |
| {db-name}.{cf-name}.write-buffer-size | memtable 大小 |
| {db-name}.{cf-name}.max-write-buffer-number | 最大 memtable 个数 |
| {db-name}.{cf-name}.max-bytes-for-level-base | base level (L1) 最大字节数 |
| {db-name}.{cf-name}.target-file-size-base | base level 的目标文件大小 |
| {db-name}.{cf-name}.level0-file-num-compaction-trigger | 触发 compaction 的 L0 文件最大个数 |
| {db-name}.{cf-name}.level0-slowdown-writes-trigger | 触发 write stall 的 L0 文件最大个数 |
| {db-name}.{cf-name}.level0-stop-writes-trigger | 完全阻停写入的 L0 文件最大个数 |
| {db-name}.{cf-name}.max-compaction-bytes | 一次 compaction 最大写入字节数 |
| {db-name}.{cf-name}.max-bytes-for-level-multiplier | 每一层的默认放大倍数 |
| {db-name}.{cf-name}.disable-auto-compactions | 自动 compaction 的开关 |
| {db-name}.{cf-name}.soft-pending-compaction-bytes-limit | pending compaction bytes 的软限制 |
| {db-name}.{cf-name}.hard-pending-compaction-bytes-limit | pending compaction bytes 的硬限制 |
| {db-name}.{cf-name}.titan.blob-run-mode | 处理 blob 文件的模式 |

上述前缀为 {db-name} 或 {db-name}.{cf-name} 的参数是 rocksdb 相关的配置
`db-name` 的取值可以为是 `rocksdb`, `raftdb`
当 `db-name` 为 `rocksdb` 时，cf-name 的取值有: `defaultcf`，`writecf`，`lockcf`，`raftcf`
当 `db-name` 为 `raftdb` 时，cf-name 的取值有: `defaultcf`

具体参数意义可参考 [TiKV 配置文件描述](https://github.com/pingcap/docs-cn/blob/master/reference/configuration/tikv-server/configuration-file.md)。

### PD

| 参数 | 简介 |
| --- | --- |
| log.level| 日志级别 |
| schedule.max-merge-region-size |  控制 Region Merge 的 size 上限（单位是 M） |
| schedule.max-merge-region-keys | 控制 Region Merge 的 keyCount 上限 |
| schedule.patrol-region-interval | 控制 replicaChecker 检查 Region 健康状态的运行频率 |
| schedule.split-merge-interval | 控制对同一个 Region 做 split 和 merge 操作的间隔 |
| schedule.max-snapshot-count | 控制单个 store 最多同时接收或发送的 snapshot 数量 |
| schedule.max-pending-peer-count | 控制单个 store 的 pending peer 上限 |
| schedule.max-store-down-time | PD 认为失联 store 无法恢复的时间 |
| schedule.leader-schedule-limit | 可以控制同时进行 leader 调度的任务个数 |
| schedule.region-schedule-limit | 可以控制同时进行 Region 调度的任务个数 |
| schedule.replica-schedule-limit | 可以控制同时进行 replica 调度的任务个数 |
| schedule.merge-schedule-limit | 控制同时进行的 Region Merge 调度的任务 |
| schedule.high-space-ratio | 用于设置 store 空间充裕的阈值 |
| schedule.low-space-ratio | 用于设置 store 空间不足的阈值 |
| schedule.tolerant-size-ratio | 控制 balance 缓冲区大小 |
| schedule.disable-remove-down-replica | 用于关闭自动删除 DownReplica 的特性 |
| schedule.disable-replace-offline-replica | 用于关闭迁移 OfflineReplica 的特性 |
| schedule.disable-make-up-replica | 用于关闭补充副本的特性 |
| schedule.disable-remove-extra-replica | 用于关闭删除多余副本的特性 |
| schedule.disable-location-replacement | 用于关闭隔离级别检查 |
| replication.max-replicas | 用于设置副本的数量 |
| replication.location-labels | 用于设置 TiKV 集群的拓扑信息 |
| label-property | 标签相关的配置项 |
| pd-server.use-region-storage | 开启独立的 region 存储 |

具体参数意义可参考 [PD 配置文件描述](https://github.com/pingcap/docs-cn/blob/master/reference/configuration/pd-server/configuration-file.md)。
