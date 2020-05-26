---
title: 动态配置变更
category: reference
---

# 动态配置变更

> **注意：**
>
> 该功能目前是实验性阶段，不建议在生产环境中使用。

动态配置变更主要是通过利用 SQL 对包括 TiKV、PD 在内的各组件的配置进行在线更新。用户可以通过利用动态配置变更对各组件进行性能调优而无需重启集群组件。

动态配置不可用于更新 TiDB 的配置，如果想动态改变 TiDB 的行为，请直接修改其对应的 SQL 变量。

## 常用操作

### 查看实例配置

可以通过 SQL `show config` 来直接查看集群所有实例的配置信息，结果如下：

```
mysql> show config;
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

```
mysql> show config where type='tidb'
mysql> show config where instance in (...)
mysql> show config where name like '%log%'
mysql> show config where type='tikv' and name='log-level'
```

### 修改实例配置

执行 SQL 语句 `set config`，可以结合实例地址和类型来修改配置，如：

```
set config tikv log.level="info"
set config "127.0.0.1:2379" log.level="info"
```

设置成功会返回 `Query OK`：

```
mysql> set config '127.0.0.1:2379' log.level='info';
Query OK, 0 rows affected (0.01 sec)
```

在批量修改时如果有错误发生，会以 warning 的形式返回：

```
mysql> set config tikv log-level='warn';
Query OK, 0 rows affected, 1 warning (0.04 sec)

mysql> show warnings;
+---------+------+---------------------------------------------------------------------------------------------------------------+
| Level   | Code | Message                                                                                                       |
+---------+------+---------------------------------------------------------------------------------------------------------------+
| Warning | 1105 | bad request to http://127.0.0.1:20180/config: fail to update, error: "config log-level can not be change" |
+---------+------+---------------------------------------------------------------------------------------------------------------+
1 row in set (0.00 sec)
```

> **注意：**
>
> 为了避免和 SQL 变量混淆，TiDB 的配置可以通过 `show config` 查看但是不能进行修改，动态配置时会返回错误；如果想动态修改 TiDB 行为，请用对应的 SQL 变量去控制。
>
> 某些配置项名称可能和 TiDB 预留关键字冲突，如 `limit`，`key` 等，对于此类配置项，需要用反引号 ``` ` ``` 包裹起来，如 ``tikv-client.`store-limit` ``；
>
> 批量修改配置不保证原子性，可能出现某些实例成功，而某些失败。如使用 `set tikv key=val` 修改整个 tikv 集群配置时，可能有部分实例失败，请使用 `show warnings` 进行查看。

## 支持参数列表

### PD

| 参数 | 简介 |
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
| pd-server.use-region-storage | 开启独立的 region 存储 |
| pd-server.max-gap-reset-ts | 用于设置最大的重置 timestamp 的间隔（BR）|
| pd-server.key-type| 用于设置集群 key 的类型 |
| pd-server.metric-storage | 用于设置集群 metrics 的存储地址 |
| pd-server.dashboard-address | 用于设置 dashboard 的地址 |
| replication-mode.replication-mode | 备份的模式 |

具体参数意义可参考 [PD 配置文件描述](/pd-configuration-file.md)

### TiKV

| 参数 | 简介 |
| --- | --- |
| refresh-config-interval | 尝试更新配置的时间间隔 |
| raftstore.sync-log | 数据、log 落盘是否 sync |
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
| raftstore.region-compact-check-step | 每轮校验人工 compaction 时，一次性检查的 region 个数 |
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
| coprocessor.split-region-on-table | 开启按 table 分裂 Region的开关 |
| coprocessor.batch-split-limit | 批量分裂 Region 的阈值 |
| coprocessor.region-max-size | Region 容量空间最大值 |
| coprocessor.region-split-size | 分裂后新 Region 的大小 |
| coprocessor.region-max-keys | Region 最多允许的 key 的个数 |
| coprocessor.region-split-keys | 分裂后新 Region 的 key 的个数 |
| pessimistic-txn.wait-for-lock-timeout | 悲观事务遇到锁后的等待的最长时间 |
| pessimistic-txn.wake-up-delay-duration | 悲观事务被重新唤醒的时间 |
| gc.ratio-threshold | 跳过 Region GC 的阈值（GC 版本个数/key 个数）|
| gc.batch-keys | 一轮处理 key 的个数 |
| gc.max-write-bytes-per-sec | 一秒可写入 RocksDB 的最大字节数 |
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

上述前缀为 `{db-name}` 或 `{db-name}.{cf-name}` 的参数是 RocksDB 相关的配置。`db-name` 的取值可以为是 `rocksdb`，`raftdb`。

- 当 `db-name` 为 `rocksdb` 时，cf-name 的取值有: `defaultcf`，`writecf`，`lockcf`，`raftcf`；
- 当 `db-name` 为 `raftdb` 时，cf-name 的取值有: `defaultcf`。

具体参数意义可参考 [TiKV 配置文件描述](/tikv-configuration-file.md)
