---
title: 在线修改集群配置
summary: 介绍在线修改集群配置的功能。
---

# 在线配置变更

> **注意：**
>
> 该功能目前是实验性阶段，不建议在生产环境中使用。

在线配置变更主要是通过利用 SQL 对包括 TiDB、TiKV 以及 PD 在内的各组件的配置进行在线更新。用户可以通过利用在线配置变更对各组件进行性能调优而无需重启集群组件。但目前在线修改 TiDB 实例配置的方式和其他组件（TiKV、PD）有所不同。

## 常用操作

### 查看实例配置

可以通过 SQL `show config` 来直接查看集群所有实例的配置信息，结果如下：

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

```sql
show config where type='tidb'
show config where instance in (...)
show config where name like '%log%'
show config where type='tikv' and name='log-level'
```

### 在线修改 TiKV 配置

> **注意：**
>
> 在线修改 TiKV 配置项后，同时会自动修改 TiKV 的配置文件。但还需要使用 `tiup edit-config` 修改对应的配置项，否则 `upgrade` `reload` 等运维操作会将在线修改配置后的结果覆盖。修改配置的操作请参考：[修改配置](/maintain-tidb-using-tiup.md#修改配置参数)，`tiup edit-config` 后不需要执行 `tiup reload` 操作。

执行 SQL 语句 `set config`，可以结合实例地址或组件类型来修改单个实例配置或全部实例配置，如：

修改全部 TiKV 实例配置：

```sql
set config tikv log.level="info"
```

修改单个 TiKV 实例配置：

```sql
set config "127.0.0.1:20180" log.level="info"
```

设置成功会返回 `Query OK`：

```sql
Query OK, 0 rows affected (0.01 sec)
```

在批量修改时如果有错误发生，会以 warning 的形式返回：

```sql
set config tikv log-level='warn';
```

```sql
Query OK, 0 rows affected, 1 warning (0.04 sec)
```

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

批量修改配置不保证原子性，可能出现某些实例成功，而某些失败。如使用 `set tikv key=val` 修改整个 TiKV 集群配置时，可能有部分实例失败，请使用 `show warnings` 进行查看。

如遇到部分修改失败的情况，需要重新执行对应的修改语句，或通过修改单个实例的方式完成修改。对于由于网络或者机器故障等原因无法访问到的 TiKV，需要等到恢复后再次进行修改。

针对 TiKV 可在线修改的配置项，如果成功修改后，修改的结果会被持久化到配置文件中，后续以配置文件中的配置为准。某些配置项名称可能和 TiDB 预留关键字冲突，如 `limit`，`key` 等，对于此类配置项，需要用反引号 ``` ` ``` 包裹起来，如 ``raftstore.raft-log-gc-size-limit` ``；

支持配置项列表如下：

| 配置项 | 简介 |
| --- | --- |
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
| coprocessor.split-region-on-table | 开启按 table 分裂 Region的开关 |
| coprocessor.batch-split-limit | 批量分裂 Region 的阈值 |
| coprocessor.region-max-size | Region 容量空间最大值 |
| coprocessor.region-split-size | 分裂后新 Region 的大小 |
| coprocessor.region-max-keys | Region 最多允许的 key 的个数 |
| coprocessor.region-split-keys | 分裂后新 Region 的 key 的个数 |
| pessimistic-txn.wait-for-lock-timeout | 悲观事务遇到锁后的等待的最长时间 |
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
| storage.block-cache.capacity | 共享 block cache 的大小（自 4.0.3 起支持） |
| backup.num-threads | backup 线程的数量（自 4.0.3 起支持） |
| split.qps-threshold | 对 Region 执行 load-base-split 的阈值，如果读 qps 连续 10s 内均超过这个值，则进行 split |
| split.split-balance-score | load-base-split 控制参数，确保 split 后左右访问尽量均匀 |
| split.split-contained-score | load-base-split 控制参数，尽量减少 split 后跨 region 访问 |

上述前缀为 `{db-name}` 或 `{db-name}.{cf-name}` 的是 RocksDB 相关的配置项。`db-name` 的取值可为 `rocksdb`，`raftdb`。

- 当 `db-name` 为 `rocksdb` 时，cf-name 的取值有: `defaultcf`，`writecf`，`lockcf`，`raftcf`；
- 当 `db-name` 为 `raftdb` 时，cf-name 的取值有: `defaultcf`。

具体配置项意义可参考 [TiKV 配置文件描述](/tikv-configuration-file.md)

### 在线修改 PD 配置

PD 暂不支持单个实例拥有独立配置。所有实例共享一份配置，可以通过下列方式修改 PD 的配置项：

```sql
set config pd log.level="info"
```

设置成功会返回 `Query OK`：

```sql
Query OK, 0 rows affected (0.01 sec)
```

针对 PD 可在线修改的配置项，成功修改后则会持久化到 etcd 中，不会对配置文件进行持久化，后续以 etcd 中的配置为准。同上，若和 TiDB 预留关键字冲突，需要用反引号 ``` ` ``` 包裹起来，如 ``schedule.`leader-schedule-limit` ``；

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

具体配置项意义可参考 [PD 配置文件描述](/pd-configuration-file.md)

### 在线修改 TiDB 配置

在线修改 TiDB 配置的方式和 TiKV/PD 有所不同，我们通过 [SQL 变量](/system-variables.md) 来完成。

下面例子展示了如何通过变量 `tidb_slow_log_threshold` 在线修改配置项 `slow-threshold`。`slow-threshold` 默认值是 200 毫秒，可以通过设置 `tidb_slow_log_threshold` 将其修改为 200 毫秒：

```sql
set tidb_slow_log_threshold = 200;
```

```sql
Query OK, 0 rows affected (0.00 sec)
```

```sql
mysql> select @@tidb_slow_log_threshold;
```

```sql
+---------------------------+
| @@tidb_slow_log_threshold |
+---------------------------+
| 200                       |
+---------------------------+
1 row in set (0.00 sec)
```

支持在线修改的配置项和相应的系统变量如下：

| 变量 | 简介 |
| --- | --- |
| autocommit | 这个变量用来设置是否自动 Commit 事务 |
| ddl_slow_threshold | 耗时超过该阈值的 DDL 操作会被输出到日志，单位为毫秒 |
| foreign_key_checks | 为保持兼容，TiDB 对外键检查返回 OFF |
| hostname | 这个变量一个只读变量，表示 TiDB server 的主机名 |
| innodb_lock_wait_timeout | 悲观事务语句等锁时间，单位为秒 |
| last_plan_from_cache | 这个变量用来显示上一个 `execute` 语句所使用的执行计划是不是直接从 plan cache 中取出来的 |
| max_execution_time | 语句最长执行时间，单位为毫秒。默认值 (0) 表示无限制 |
| sql_select_limit | `SELECT` 语句返回的最大行数 |
| tidb_allow_batch_cop | 这个变量用于控制 TiDB 向 TiFlash 发送 coprocessor 请求的方式，有以下几种取值 |
| tidb_allow_remove_auto_inc | 这个变量用来控制是否允许通过 `ALTER TABLE MODIFY` 或 `ALTER TABLE CHANGE` 来移除某个列的 `AUTO_INCREMENT` 属性。默认 (`0`) 为不允许 |
| tidb_auto_analyze_end_time | 这个变量用来设置一天中允许自动 ANALYZE 更新统计信息的结束时间。例如，只允许在凌晨 1:00 至 3:00 之间自动更新统计信息，可以设置如下 |
| tidb_auto_analyze_ratio | 这个变量用来设置 TiDB 在后台自动执行 [`ANALYZE TABLE`](/sql-statements/sql-statement-analyze-table.md) 更新统计信息的阈值。`0.5` 指的是当表中超过 50% 的行被修改时，触发自动 ANALYZE 更新。可以指定 `tidb_auto_analyze_start_time` 和 `tidb_auto_analyze_end_time` 来限制自动 ANALYZE 的时 |
| tidb_auto_analyze_start_time | 这个变量用来设置一天中允许自动 ANALYZE 更新统计信息的开始时间。例如，只允许在凌晨 1:00 至 3:00 之间自动更新统计信息，可以设置如下 |
| tidb_backoff_lock_fast | 这个变量用来设置读请求遇到锁的 backoff 时间 |
| tidb_backoff_weight | 这个变量用来给 TiDB 的 `backoff` 最大时间增加权重，即内部遇到网络或其他组件（TiKV、PD）故障时，发送重试请求的最大重试时间。可以通过这个变量来调整最大重试时间，最小值为 1 |
| tidb_build_stats_concurrency | 这个变量用来设置 ANALYZE 语句执行时并发度 |
| tidb_capture_plan_baselines | 这个变量用于控制是否开启[自动捕获绑定](/sql-plan-management.md#自动捕获绑定-baseline-capturing)功能。该功能依赖 Statement Summary，因此在使用自动绑定之前需打开 Statement Summary 开关 |
| tidb_check_mb4_value_in_utf8 | 这个变量用来设置是否开启对字符集为 UTF8 类型的数据做合法性检查，默认值 `1` 表示开启检查。这个默认行为和 MySQL 是兼容的 |
| tidb_checksum_table_concurrency | 这个变量用来设置 `ADMIN CHECKSUM TABLE` 语句执行时扫描索引的并发度 |
| tidb_config | 这个变量是一个只读变量，用来获取当前 TiDB Server 的配置信息 |
| tidb_constraint_check_in_place | TiDB 支持乐观事务模型，即在执行写入时，假设不存在冲突。冲突检查是在最后 commit 提交时才去检查。这里的检查指 unique key 检查 |
| tidb_current_ts | 这个变量是一个只读变量，用来获取当前事务的时间戳 |
| tidb_ddl_error_count_limit | 这个变量用来控制 DDL 操作失败重试的次数。失败重试次数超过该参数的值后，会取消出错的 DDL 操作 |
| tidb_ddl_reorg_priority | 这个变量用来设置 `ADD INDEX` 操作 `re-organize` 阶段的执行优先级，可设置为 `PRIORITY_LOW`/`PRIORITY_NORMAL`/`PRIORITY_HIGH` |
| tidb_ddl_reorg_worker_cnt | 这个变量用来设置 DDL 操作 `re-organize` 阶段的并发度 |
| tidb_disable_txn_auto_retry | 这个变量用来设置是否禁用显式事务自动重试，设置为 `on` 时，不会自动重试，如果遇到事务冲突需要在应用层重试 |
| tidb_distsql_scan_concurrency | 这个变量用来设置 scan 操作的并发度 |
| tidb_enable_cascades_planner | 这个变量用于控制是否开启 cascades planner |
| tidb_enable_chunk_rpc | 这个变量用来设置是否启用 Coprocessor 的 `Chunk` 数据编码格式 |
| tidb_enable_fast_analyze | 这个变量用来控制是否启用统计信息快速分析功能。默认值 0 表示不开启 |
| tidb_enable_index_merge | 这个变量用于控制是否开启 index merge 功能 |
| tidb_enable_noop_functions | 这个变量用于控制是否开启 `get_lock` 和 `release_lock` 这两个没有实现的函数。需要注意的是，当前版本的 TiDB 这两个函数永远返回 1 |
| tidb_enable_slow_log | 这个变量用于控制是否开启 slow log 功能，默认开启 |
| tidb_enable_stmt_summary | 这个变量用来控制是否开启 statement summary 功能。如果开启，SQL 的耗时等执行信息将被记录到系统表 `information_schema.STATEMENTS_SUMMARY` 中，用于定位和排查 SQL 性能问题 |
| tidb_enable_streaming | 这个变量用来设置是否启用 Streaming |
| tidb_enable_table_partition | 这个变量用来设置是否开启 `TABLE PARTITION` 特性。目前变量支持以下三种值 |
| tidb_enable_telemetry | 这个变量用于动态地控制 TiDB 遥测功能是否开启。设置为 `0` 可以关闭 TiDB 遥测功能。当所有 TiDB 实例都设置 [`enable-telemetry`](/tidb-configuration-file.md#enable-telemetry-从-v402-版本开始引入) 为 `false` 时将忽略该系统变量并总是关闭 TiDB 遥测功能。参阅[遥测](/telemetry.md)了解该功能详情 |
| tidb_enable_vectorized_expression | 这个变量用于控制是否开启向量化执行 |
| tidb_enable_window_function | 这个变量用来控制是否开启窗口函数的支持。默认值 1 代表开启窗口函数的功能 |
| tidb_evolve_plan_baselines | 这个变量用于控制是否启用自动演进绑定功能。该功能的详细介绍和使用方法可以参考[自动演进绑定](/sql-plan-management.md#自动演进绑定-baseline-evolution) |
| tidb_evolve_plan_task_end_time | 这个变量用来设置一天中允许自动演进的结束时间 |
| tidb_evolve_plan_task_max_time | 该变量用于限制自动演进功能中，每个执行计划运行的最长时间，单位为秒 |
| tidb_evolve_plan_task_start_time | 这个变量用来设置一天中允许自动演进的开始时间 |
| tidb_expensive_query_time_threshold | 这个变量用来控制打印 expensive query 日志的阈值时间，单位是秒，默认值是 60 秒。expensive query 日志和慢日志的差别是，慢日志是在语句执行完后才打印，expensive query 日志可以把正在执行中的语句且执行时间超过阈值的语句及其相关信息打印出来 |
| tidb_force_priority | 这个变量用于改变 TiDB server 上执行的语句的默认优先级。例如，你可以通过设置该变量来确保正在执行 OLAP 查询的用户优先级低于正在执行 OLTP 查询的用户 |
| tidb_general_log | 这个变量用来设置是否在日志里记录所有的 SQL 语句 |
| tidb_hash_join_concurrency | 这个变量用来设置 hash join 算法的并发度 |
| tidb_hashagg_final_concurrency | 这个变量用来设置并行 hash aggregation 算法 final 阶段的执行并发度。对于聚合函数参数不为 distinct 的情况，HashAgg 分为 partial 和 final 阶段分别并行执行 |
| tidb_hashagg_partial_concurrency | 这个变量用来设置并行 hash aggregation 算法 partial 阶段的执行并发度。对于聚合函数参数不为 distinct 的情况，HashAgg 分为 partial 和 final 阶段分别并行执行 |
| tidb_index_join_batch_size | 这个变量用来设置 index lookup join 操作的 batch 大小，AP 类应用适合较大的值，TP 类应用适合较小的值 |
| tidb_index_lookup_concurrency | 这个变量用来设置 index lookup 操作的并发度，AP 类应用适合较大的值，TP 类应用适合较小的值 |
| tidb_index_lookup_join_concurrency | 这个变量用来设置 index lookup join 算法的并发度 |
| tidb_index_lookup_size | 这个变量用来设置 index lookup 操作的 batch 大小，AP 类应用适合较大的值，TP 类应用适合较小的值 |
| tidb_index_serial_scan_concurrency | 这个变量用来设置顺序 scan 操作的并发度，AP 类应用适合较大的值，TP 类应用适合较小的值 |
| tidb_init_chunk_size | 这个变量用来设置执行过程中初始 chunk 的行数。默认值是 32，可设置的范围是 1～32 |
| tidb_isolation_read_engines | 这个变量用于设置 TiDB 在读取数据时可以使用的存储引擎列表 |
| tidb_low_resolution_tso | 这个变量用来设置是否启用低精度 tso 特性，开启该功能之后新事务会使用一个每 2s 更新的 ts 来读取数据 |
| tidb_max_chunk_size | 最小值� |
| tidb_max_delta_schema_count | 这个变量用来设置缓存 schema 版本信息（对应版本修改的相关 table IDs）的个数限制，可设置的范围 100 - 16384。此变量在 2.1.18 及之后版本支持 |
| tidb_mem_quota_hashjoin | 这个变量用来设置 `HashJoin` 算子的内存使用阈值 |
| tidb_mem_quota_indexlookupjoin | 这个变量用来设置 `IndexLookupJoin` 算子的内存使用阈值 |
| tidb_mem_quota_indexlookupreader | 这个变量用来设置 `IndexLookupReader` 算子的内存使用阈值 |
| tidb_mem_quota_mergejoin | 这个变量用来设置 `MergeJoin` 算子的内存使用阈值 |
| tidb_mem_quota_nestedloopapply | 这个变量用来设置 `NestedLoopApply` 算子的内存使用阈值 |
| tidb_mem_quota_query | 这个变量用来设置一条查询语句的内存使用阈值 |
| tidb_mem_quota_sort | 这个变量用来设置 `Sort` 算子的内存使用阈值 |
| tidb_mem_quota_topn | 这个变量用来设置 `TopN` 算子的内存使用阈值 |
| tidb_metric_query_range_duration | 这个变量设置了查询 `METRIC_SCHEMA` 时生成的 Prometheus 语句的 range duration，单位为秒 |
| tidb_metric_query_step | 这个变量设置了查询 `METRIC_SCHEMA` 时生成的 Prometheus 语句的 step，单位为秒 |
| tidb_opt_agg_push_down | 这个变量用来设置优化器是否执行聚合函数下推到 Join 之前的优化操作 |
| tidb_opt_correlation_exp_factor | 当交叉估算方法不可用时，会采用启发式估算方法。这个变量用来控制启发式方法的行为。当值为 0 时不用启发式估算方法，大于 0 时，该变量值越大，启发式估算方法越倾向 index scan，越小越倾向 table scan |
| tidb_opt_correlation_threshold | 这个变量用来设置优化器启用交叉估算 row count 方法的阈值。如果列和 handle 列之间的顺序相关性超过这个阈值，就会启用交叉估算方法 |
| tidb_opt_distinct_agg_push_down | 这个变量用来设置优化器是否执行带有 `Distinct` 的聚合函数（比如 `select count(distinct a) from t`）下推到 Coprocessor 的优化操作 |
| tidb_opt_insubq_to_join_and_agg | 这个变量用来设置是否开启优化规则：将子查询转成 join 和 aggregation |
| tidb_opt_write_row_id | 这个变量用来设置是否允许 `INSERT`、`REPLACE` 和 `UPDATE` 操作 `_tidb_rowid` 列，默认是不允许操作。该选项仅用于 TiDB 工具导数据时使用 |
| tidb_projection_concurrency | 这个变量用来设置 `Projection` 算子的并发度 |
| tidb_query_log_max_len | 最长的 SQL 输出长度。当语句的长度大于 query-log-max-len，将会被截断输出 |
| tidb_pprof_sql_cpu | 这个变量用来控制是否在 profile 输出中标记出对应的 SQL 语句，用于定位和排查性能问题 |
| tidb_record_plan_in_slow_log | 这个变量用于控制是否在 slow log 里包含慢查询的执行计划 |
| tidb_replica_read | 这个变量用于控制 TiDB 读取数据的位置，有以下三个选择 |
| tidb_retry_limit | 这个变量用来设置最大重试次数。一个事务执行中遇到可重试的错误（例如事务冲突、事务提交过慢或表结构变更）时，会根据该变量的设置进行重试。注意当 `tidb_retry_limit = 0` 时，也会禁用自动重试 |
| tidb_row_format_version | 控制新保存数据的表数据格式版本。TiDB v4.0 中默认使用版本号为 2 的[新表数据格式](https://github.com/pingcap/tidb/blob/master/docs/design/2018-07-19-row-format.md)保存新数据 |
| tidb_scatter_region | TiDB 默认会在建表时为新表分裂 Region。开启该变量后，会在建表语句执行时，同步打散刚分裂出的 Region。适用于批量建表后紧接着批量写入数据，能让刚分裂出的 Region 先在 TiKV 分散而不用等待 PD 进行调度。为了保证后续批量写入数据的稳定性，建表语句会等待打散 Region 完成后再返回建表成功，建表语句执行时间会是关闭该变量的数倍 |
| tidb_skip_isolation_level_check | 开启这个开关之后，如果对 `tx_isolation` 赋值一个 TiDB 不支持的隔离级别，不会报错，有助于兼容其他设置了（但不依赖于）不同隔离级别的应用 |
| tidb_skip_utf8_check | 这个变量用来设置是否跳过 UTF-8 字符的验证 |
| tidb_slow_log_threshold | 输出慢日志的耗时阈值。当查询大于这个值，就会当做是一个慢查询，输出到慢查询日志。默认为 300ms |
| tidb_slow_query_file | 查询 `INFORMATION_SCHEMA.SLOW_QUERY` 只会解析配置文件中 `slow-query-file` 设置的慢日志文件名，默认是 "tidb-slow.log"。但如果想要解析其他的日志文件，可以通过设置 session 变量 `tidb_slow_query_file` 为具体的文件路径，然后查询 `INFORMATION_SCHEMA.SLOW_QUERY` 就会按照设置的路径去解析慢日志文件。更多详情可以参考 [SLOW_QUERY 文档](/identify-slow-queries.md) |
| tidb_snapshot | 这个变量用来设置当前会话期待读取的历史数据所处时刻。比如当设置为 `"2017-11-11 20:20:20"` 时或者一个 TSO 数字 "400036290571534337"，当前会话将能读取到该时刻的数据 |
| tidb_stmt_summary_history_size | 这个变量设置了 statement summary 的历史记录容量 |
| tidb_stmt_summary_internal_query | 这个变量用来控制是否在 statement summary 中包含 TiDB 内部 SQL 的信息 |
| tidb_stmt_summary_max_sql_length | 这个变量控制 statement summary 显示的 SQL 字符串长度 |
| tidb_stmt_summary_max_stmt_count | 这个变量设置了 statement summary 在内存中保存的语句的最大数量 |
| tidb_stmt_summary_refresh_interval | 这个变量设置了 statement summary 的刷新时间，单位为秒 |
| tidb_store_limit | 这个变量用于限制 TiDB 同时向 TiKV 发送的请求的最大数量，0 表示没有限制 |
| tidb_txn_mode | 这个变量用于设置事务模式。TiDB v3.0 支持了悲观事务，自 v3.0.8 开始，默认使用[悲观事务模式](/pessimistic-transaction.md) |
| tidb_use_plan_baselines | 这个变量用于控制是否开启执行计划绑定功能，默认打开，可通过赋值 off 来关闭。关于执行计划绑定功能的使用可以参考[执行计划绑定文档](/sql-plan-management.md#创建绑定) |
| tidb_wait_split_region_finish | 由于打散 region 的时间可能比较长，主要由 PD 调度以及 TiKV 的负载情况所决定。这个变量用来设置在执行 `SPLIT REGION` 语句时，是否同步等待所有 region 都打散完成后再返回结果给客户端。默认 1 代表等待打散完成后再返回结果。0 代表不等待 Region 打散完成就返回 |
| tidb_wait_split_region_timeout | 这个变量用来设置 `SPLIT REGION` 语句的执行超时时间，单位是秒，默认值是 300 秒，如果超时还未完成，就返回一个超时错误 |
| tidb_window_concurrency | 这个变量用于设置 window 算子的并行度 |
| time_zone | 数据库所使用的时区。这个变量值可以写成时区偏移的形式，如 '-8:00'，也可以写成一个命名时区，如 'America/Los_Angeles' |
| transaction_isolation | 这个变量用于设置事务隔离级别。TiDB 为了兼容 MySQL，支持可重复读 (`REPEATABLE-READ`)，但实际的隔离级别是快照隔离。详情见[事务隔离级别](/transaction-isolation-levels.md) |
| version | 这个变量的值是 MySQL 的版本和 TiDB 的版本，例如 '5.7.25-TiDB-v4.0.0-beta.2-716-g25e003253' |
| version_comment | 这个变量的值是 TiDB 版本号的其他信息，例如 'TiDB Server (Apache License 2.0) Community Edition, MySQL 5.7 compatible' |
| wait_timeout | 这个变量表示用户会话的空闲超时，单位为秒。`0` 代表没有时间限制 |
| windowing_use_high_precision | 这个变量用于控制计算窗口函数时是否采用高精度模式 |
