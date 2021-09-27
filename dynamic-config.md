---
title: 在线修改集群配置
summary: 介绍在线修改集群配置的功能。
aliases: ['/docs-cn/stable/dynamic-config/','/docs-cn/v4.0/dynamic-config/']
---

# 在线修改集群配置

> **警告：**
>
> 该功能目前是实验性阶段，不建议在生产环境中使用。

在线配置变更主要是通过利用 SQL 对包括 TiDB、TiKV 以及 PD 在内的各组件的配置进行在线更新。用户可以通过在线配置变更对各组件进行性能调优而无需重启集群组件。但目前在线修改 TiDB 实例配置的方式和修改其他组件 (TiKV, PD) 的有所不同。

## 常用操作

### 查看实例配置

可以通过 SQL 语句 `show config` 来直接查看集群所有实例的配置信息，结果如下：

{{< copyable "sql" >}}

```sql
show config;
```

```sql
+------+-----------------+-----------------------------------------------------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| Type | Instance        | Name                                                      | Value                                                                                                                                                                                                                                                                            |
+------+-----------------+-----------------------------------------------------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| tidb | 127.0.0.1:4001  | advertise-address                                         | 127.0.0.1                                                                                                                                                                                                                                                                        |
| tidb | 127.0.0.1:4001  | alter-primary-key                                         | false                                                                                                                                                                                                                                                                            |
| tidb | 127.0.0.1:4001  | binlog.binlog-socket                                      |                                                                                                                                                                                                                                                                                  |
| tidb | 127.0.0.1:4001  | binlog.enable                                             | false                                                                                                                                                                                                                                                                            |
| tidb | 127.0.0.1:4001  | binlog.ignore-error                                       | false                                                                                                                                                                                                                                                                            |
| tidb | 127.0.0.1:4001  | binlog.strategy                                           | range                                                                                                                                                                                                                                                                            |
| tidb | 127.0.0.1:4001  | binlog.write-timeout                                      | 15s                                                                                                                                                                                                                                                                              |
| tidb | 127.0.0.1:4001  | check-mb4-value-in-utf8                                   | true                                                                                                                                                                                                                                                                             |

...
```

还可以根据对应的字段进行过滤，如：

{{< copyable "sql" >}}

```sql
show config where type='tidb'
show config where instance in (...)
show config where name like '%log%'
show config where type='tikv' and name='log-level'
```

### 在线修改 TiKV 配置

> **注意：**
>
> 在线修改 TiKV 配置项后，同时会自动修改 TiKV 的配置文件。但还需要使用 `tiup edit-config` 命令来修改对应的配置项，否则 `upgrade` 和 `reload` 等运维操作会将在线修改配置后的结果覆盖。修改配置的操作请参考：[使用 TiUP 修改配置](/maintain-tidb-using-tiup.md#修改配置参数)。执行 `tiup edit-config` 后不需要执行 `tiup reload` 操作。

执行 SQL 语句 `set config`，可以结合实例地址或组件类型来修改单个实例配置或全部实例配置，如：

修改全部 TiKV 实例配置：

> **注意：**
>
> 建议使用反引号包裹变量名称。

{{< copyable "sql" >}}

```sql
set config tikv `split.qps-threshold`=1000
```

修改单个 TiKV 实例配置：

{{< copyable "sql" >}}

```sql
set config "127.0.0.1:20180" `split.qps-threshold`=1000
```

设置成功会返回 `Query OK`：

{{< copyable "sql" >}}

```sql
Query OK, 0 rows affected (0.01 sec)
```

在批量修改时如果有错误发生，会以 warning 的形式返回：

{{< copyable "sql" >}}

```sql
set config `tikv log-level`='warn';
```

```sql
Query OK, 0 rows affected, 1 warning (0.04 sec)
```

{{< copyable "sql" >}}

```sql
show warnings;
```

```sql
+---------+------+---------------------------------------------------------------------------------------------------------------+
| Level   | Code | Message                                                                                                       |
+---------+------+---------------------------------------------------------------------------------------------------------------+
| Warning | 1105 | bad request to http://127.0.0.1:20180/config: fail to update, error: "config log-level can not be changed" |
+---------+------+---------------------------------------------------------------------------------------------------------------+
1 row in set (0.00 sec)
```

批量修改配置不保证原子性，可能出现某些实例成功，而某些失败的情况。如使用 `set tikv key=val` 命令修改整个 TiKV 集群配置时，可能有部分实例失败，请执行 `show warnings` 进行查看。

如遇到部分修改失败的情况，需要重新执行对应的修改语句，或通过修改单个实例的方式完成修改。如果因网络或者机器故障等原因无法访问到的 TiKV，需要等到恢复后再次进行修改。

针对 TiKV 可在线修改的配置项，如果成功修改后，修改的结果会被持久化到配置文件中，后续以配置文件中的配置为准。某些配置项名称可能和 TiDB 预留关键字冲突，如 `limit`、`key` 等，对于此类配置项，需要用反引号 ``` ` ``` 包裹起来，如 ``` `raftstore.raft-log-gc-size-limit` ```。

支持的配置项列表如下：

| 配置项 | 简介 |
| --- | --- |
| raftstore.sync-log | 数据、log 落盘是否同步 |
| raftstore.raft-entry-max-size | 单个日志最大大小 |
| raftstore.raft-log-gc-tick-interval | 删除 Raft 日志的轮询任务调度间隔时间 |
| raftstore.raft-log-gc-threshold | 允许残余的 Raft 日志个数，软限制 |
| raftstore.raft-log-gc-count-limit | 允许残余的 Raft 日志个数，硬限制 |
| raftstore.raft-log-gc-size-limit | 允许残余的 Raft 日志大小，硬限制 |
| raftstore.raft-entry-cache-life-time | 内存中日志 cache 允许的最长残留时间 |
| raftstore.raft-reject-transfer-leader-duration | 控制迁移 leader 到新加节点的最小时间 |
| raftstore.split-region-check-tick-interval | 检查 Region 是否需要分裂的时间间隔 |
| raftstore.region-split-check-diff | 允许 Region 数据超过指定大小的最大值 |
| raftstore.region-compact-check-interval | 检查是否需要人工触发 RocksDB compaction 的时间间隔 |
| raftstore.region-compact-check-step | 每轮校验人工 compaction 时，一次性检查的 Region 个数 |
| raftstore.region-compact-min-tombstones | 触发 RocksDB compaction 需要的 tombstone 个数 |
| raftstore.region-compact-tombstones-percent | 触发 RocksDB compaction 需要的 tombstone 所占比例 |
| raftstore.pd-heartbeat-tick-interval | 触发 Region 对 PD 心跳的时间间隔 |
| raftstore.pd-store-heartbeat-tick-interval | 触发 store 对 PD 心跳的时间间隔 |
| raftstore.snap-mgr-gc-tick-interval | 触发回收过期 snapshot 文件的时间间隔 |
| raftstore.snap-gc-timeout | snapshot 文件的最长保存时间 |
| raftstore.lock-cf-compact-interval | 触发对 lock CF compact 检查的时间间隔 |
| raftstore.lock-cf-compact-bytes-threshold | 触发对 lock CF 进行 compact 的大小 |
| raftstore.messages-per-tick | 每轮处理的消息最大个数 |
| raftstore.max-peer-down-duration | 副本允许的最长未响应时间 |
| raftstore.max-leader-missing-duration | 允许副本处于无主状态的最长时间，超过将会向 PD 校验自己是否已经被删除 |
| raftstore.abnormal-leader-missing-duration | 允许副本处于无主状态的时间，超过将视为异常，标记在 metrics 和日志中 |
| raftstore.peer-stale-state-check-interval | 触发检验副本是否处于无主状态的时间间隔 |
| raftstore.consistency-check-interval | 触发一致性检查的时间间隔 |
| raftstore.raft-store-max-leader-lease | Region 主可信任期的最长时间 |
| raftstore.allow-remove-leader | 允许删除主开关 |
| raftstore.merge-check-tick-interval | 触发 Merge 完成检查的时间间隔 |
| raftstore.cleanup-import-sst-interval | 触发检查过期 SST 文件的时间间隔 |
| raftstore.local-read-batch-size | 一轮处理读请求的最大个数 |
| raftstore.hibernate-timeout | 启动后进入静默状态前需要等待的最短时间，在该时间段内不会进入静默状态（未 release）|
| coprocessor.split-region-on-table | 开启按 table 分裂 Region 的开关 |
| coprocessor.batch-split-limit | 批量分裂 Region 的阈值 |
| coprocessor.region-max-size | Region 容量空间的最大值 |
| coprocessor.region-split-size | 分裂后新 Region 的大小 |
| coprocessor.region-max-keys | Region 最多允许的 key 的个数 |
| coprocessor.region-split-keys | 分裂后新 Region 的 key 的个数 |
| pessimistic-txn.wait-for-lock-timeout | 悲观事务遇到锁后的最长等待时间 |
| pessimistic-txn.wake-up-delay-duration | 悲观事务被重新唤醒的时间 |
| pessimistic-txn.pipelined | 是否开启流水线式加悲观锁流程 |
| gc.ratio-threshold | 跳过 Region GC 的阈值（GC 版本个数/key 个数）|
| gc.batch-keys | 一轮处理 key 的个数 |
| gc.max-write-bytes-per-sec | 一秒可写入 RocksDB 的最大字节数 |
| gc.enable-compaction-filter | 是否使用 compaction filter |
| gc.compaction-filter-skip-version-check | 是否跳过 compaction filter 的集群版本检查（未 release）|
| {db-name}.max-total-wal-size | WAL 总大小限制 |
| {db-name}.max-background-jobs | RocksDB 后台线程个数 |
| {db-name}.max-open-files | RocksDB 可以打开的文件总数 |
| {db-name}.compaction-readahead-size | Compaction 时候 readahead 的大小 |
| {db-name}.bytes-per-sync | 异步同步的限速速率 |
| {db-name}.wal-bytes-per-sync | WAL 同步的限速速率 |
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
| storage.block-cache.capacity | 共享 block cache 的大小（自 v4.0.3 起支持） |
| backup.num-threads | backup 线程的数量（自 v4.0.3 起支持） |
| split.qps-threshold | 对 Region 执行 load-base-split 的阈值。如果读 QPS 连续 10 秒内均超过这个值，则进行 split |
| split.split-balance-score | load-base-split 的控制参数，确保 split 后左右访问尽量均匀 |
| split.split-contained-score | load-base-split 的控制参数，尽量减少 split 后跨 Region 访问 |
| cdc.incremental-scan-concurrency | 增量扫描历史数据任务的最大并发执行个数（自 v4.0.15 起支持） |
| cdc.incremental-scan-speed-limit| 增量扫描历史数据的速度上限（自 v4.0.15 起支持） |
| cdc.min-ts-interval | 定期推进 Resolved TS 的时间间隔（自 v4.0.15 起支持）  |
| cdc.sink-memory-quota| 缓存在内存中的 TiCDC 数据变更事件占用内存的上限（自 v4.0.15 起支持）  |

上述前缀为 `{db-name}` 或 `{db-name}.{cf-name}` 的是 RocksDB 相关的配置项。`db-name` 的取值可为 `rocksdb` 或 `raftdb`。

- 当 `db-name` 为 `rocksdb` 时，`cf-name` 的可取值有：`defaultcf`、`writecf`、`lockcf`、`raftcf`；
- 当 `db-name` 为 `raftdb` 时，`cf-name` 的可取值有：`defaultcf`。

具体配置项的意义可参考 [TiKV 配置文件描述](/tikv-configuration-file.md)

### 在线修改 PD 配置

PD 暂不支持单个实例拥有独立配置。所有实例共享一份配置，可以通过下列方式修改 PD 的配置项：

{{< copyable "sql" >}}

```sql
set config pd `log.level`='info'
```

设置成功会返回 `Query OK`：

```sql
Query OK, 0 rows affected (0.01 sec)
```

针对 PD 可在线修改的配置项，成功修改后则会持久化到 etcd 中，不会对配置文件进行持久化，后续以 etcd 中的配置为准。同上，若和 TiDB 预留关键字冲突，需要用反引号 ``` ` ``` 包裹此类配置项，例如 ``` `schedule.leader-schedule-limit` ```。

支持配置项列表如下：

| 配置项 | 简介 |
| --- | --- |
| log.level| 日志级别 |
| cluster-version | 集群的版本 |
| schedule.max-merge-region-size |  控制 Region Merge 的 size 上限（单位是 MB） |
| schedule.max-merge-region-keys | 控制 Region Merge 的 key 数量上限 |
| schedule.patrol-region-interval | 控制 replicaChecker 检查 Region 健康状态的运行频率 |
| schedule.split-merge-interval | 控制对同一个 Region 做 split 和 merge 操作的间隔 |
| schedule.max-snapshot-count | 控制单个 store 最多同时接收或发送的 snapshot 数量 |
| schedule.max-pending-peer-count | 控制单个 store 的 pending peer 上限 |
| schedule.max-store-down-time | PD 认为失联 store 无法恢复的时间 |
| schedule.leader-schedule-policy | 用于控制 leader 调度的策略 |
| schedule.leader-schedule-limit | 可以控制同时进行 leader 调度的任务个数 |
| schedule.region-schedule-limit | 可以控制同时进行 Region 调度的任务个数 |
| schedule.replica-schedule-limit | 可以控制同时进行 replica 调度的任务个数 |
| schedule.merge-schedule-limit | 控制同时进行的 Region Merge 调度的任务 |
| schedule.hot-region-schedule-limit | 可以控制同时进行的热点调度的任务个数 |
| schedule.hot-region-cache-hits-threshold | 用于设置 Region 被视为热点的阈值 |
| schedule.high-space-ratio | 用于设置 store 空间充裕的阈值 |
| schedule.low-space-ratio | 用于设置 store 空间不足的阈值 |
| schedule.tolerant-size-ratio | 控制 balance 缓冲区大小 |
| schedule.enable-remove-down-replica | 用于开启自动删除 DownReplica 的特性 |
| schedule.enable-replace-offline-replica | 用于开启迁移 OfflineReplica 的特性 |
| schedule.enable-make-up-replica | 用于开启补充副本的特性 |
| schedule.enable-remove-extra-replica | 用于开启删除多余副本的特性 |
| schedule.enable-location-replacement | 用于开启隔离级别检查 |
| schedule.enable-cross-table-merge | 用于开启跨表 Merge |
| schedule.enable-one-way-merge | 用于开启单向 Merge（只允许和下一个相邻的 Region Merge） |
| replication.max-replicas | 用于设置副本的数量 |
| replication.location-labels | 用于设置 TiKV 集群的拓扑信息 |
| replication.enable-placement-rules | 开启 Placement Rules |
| replication.strictly-match-label | 开启 label 检查 |
| pd-server.use-region-storage | 开启独立的 Region 存储 |
| pd-server.max-gap-reset-ts | 用于设置最大的重置 timestamp 的间隔（BR）|
| pd-server.key-type| 用于设置集群 key 的类型 |
| pd-server.metric-storage | 用于设置集群 metrics 的存储地址 |
| pd-server.dashboard-address | 用于设置 dashboard 的地址 |
| replication-mode.replication-mode | 备份的模式 |

具体配置项意义可参考 [PD 配置文件描述](/pd-configuration-file.md)。

### 在线修改 TiDB 配置

在线修改 TiDB 配置的方式和 TiKV/PD 有所不同，用户通过[系统变量](/system-variables.md)来完成修改。

下面例子展示了如何通过变量 `tidb_slow_log_threshold` 在线修改配置项 `slow-threshold`。

`slow-threshold` 默认值是 300 毫秒，可以通过设置系统变量 `tidb_slow_log_threshold` 将其修改为 200 毫秒：

{{< copyable "sql" >}}

```sql
set tidb_slow_log_threshold = 200;
```

```sql
Query OK, 0 rows affected (0.00 sec)
```

{{< copyable "sql" >}}

```sql
select @@tidb_slow_log_threshold;
```

```sql
+---------------------------+
| @@tidb_slow_log_threshold |
+---------------------------+
| 200                       |
+---------------------------+
1 row in set (0.00 sec)
```

支持在线修改的配置项和相应的 TiDB 系统变量如下：

| 配置项 | 对应变量 | 简介 |
| --- | --- | --- |
| mem-quota-query | tidb_mem_quota_query | 查询语句的内存使用限制 |
| log.enable-slow-log | tidb_enable_slow_log | 慢日志的开关 |
| log.slow-threshold | tidb_slow_log_threshold | 慢日志阈值 |
| log.expensive-threshold | tidb_expensive_query_time_threshold | expensive 查询阈值 |
