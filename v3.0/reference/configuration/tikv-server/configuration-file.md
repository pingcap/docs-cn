---
title: TiKV 配置文件描述
category: reference

---

# TiKV 配置文件描述

TiKV 配置文件比命令行参数支持更多的选项。你可以在 [etc/config-template.toml](https://github.com/tikv/tikv/blob/master/etc/config-template.toml) 找到默认值的配置文件，重命名为 config.toml 即可。

本文档只阐述未包含在命令行参数中的参数，命令行参数参见[这里](/dev/reference/configuration/tikv-server/configuration.md)。

### `status-thread-pool-size`

+ Http API 服务的工作线程数量。
+ 默认值：1
+ 最小值：1

### `grpc-compression-type`

+ gRPC 消息的压缩算法，取值：none， deflate， gzip。
+ 默认值：none

### `grpc-concurrency`

+ gRPC 工作线程的数量。
+ 默认值：4
+ 最小值：1

### `grpc-concurrent-stream`

+ 一个 gRPC 链接中最多允许的并发请求数量。
+ 默认值：1024
+ 最小值：1

### `server.grpc-raft-conn-num`

+ tikv 节点之间用于 raft 通讯的链接最大数量。
+ 默认值：10
+ 最小值：1

### `server.grpc-stream-initial-window-size`

+ gRPC stream 的 window 大小。
+ 默认值：2MB
+ 单位：KB|MB|GB
+ 最小值：1KB

### `server.grpc-keepalive-time`

+ gRPC 发送 keep alive ping 消息的间隔时长。
+ 默认值：10s
+ 最小值：1s

### `server.grpc-keepalive-timeout`

+ 关闭 gRPC 链接的超时时长。
+ 默认值：3s
+ 最小值：1s

### `server.concurrent-send-snap-limit`

+ 同时发送 snapshot 的最大个数，默认值：32
+ 默认值：32
+ 最小值：1

### `server.concurrent-recv-snap-limit`

+ 同时接受 snapshot 的最大个数，默认值：32
+ 默认值：32
+ 最小值：1

### `server.end-point-recursion-limit`

+ endpoint 下推查询请求解码消息时，最多允许的递归层数。
+ 默认值：1000
+ 最小值：1

### `server.end-point-request-max-handle-duration`

+ endpoint 下推查询请求处理任务最长允许的时长。
+ 默认值：60s
+ 最小值：1s

### `server.snap-max-write-bytes-per-sec`

+ 处理 snapshot 时最大允许使用的磁盘带宽
+ 默认值：1000MB
+ 单位：KB|MB|GB
+ 最小值：1KB

## readpool.storage

存储线程池相关的配置项。

### `high-concurrency`

+ 处理高优先级读请求的线程池线程数量。
+ 默认值：4
+ 最小值：1

### `normal-concurrency`

+ 处理普通优先级读请求的线程池线程数量。
+ 默认值：4
+ 最小值：1

### `low-concurrency`

+ 处理低优先级读请求的线程池线程数量。
+ 默认值：4
+ 最小值：1

### `max-tasks-per-worker-high`

+ 高优先级线程池中单个线程允许积压的最大任务数量，超出后会返回 Server Is Busy。
+ 默认值：2000
+ 最小值：2

### `max-tasks-per-worker-normal`

+ 普通优先级线程池中单个线程允许积压的最大任务数量，超出后会返回 Server Is Busy。
+ 默认值：2000
+ 最小值：2

### `max-tasks-per-worker-low`

+ 低优先级线程池中单个线程允许积压的最大任务数量，超出后会返回 Server Is Busy。
+ 默认值：2000
+ 最小值：2

### `stack-size`

+ Storage 读线程池中线程的栈大小。
+ 默认值：10MB
+ 单位：KB|MB|GB
+ 最小值：2MB

## readpool.coprocessor

协处理器线程池相关的配置项。

### `high-concurrency`

+ 处理高优先级 Coprocessor 请求（如点查）的线程池线程数量。
+ 默认值：CPU * 0.8
+ 最小值：1

### `normal-concurrency`

+ 处理普通优先级 Coprocessor 请求的线程池线程数量。
+ 默认值：CPU * 0.8
+ 最小值：1

### `low-concurrency`

+ 处理低优先级 Coprocessor 请求（如扫表）的线程池线程数量。
+ 默认值：CPU * 0.8
+ 最小值：1

### `max-tasks-per-worker-high`

+ 高优先级线程池中单个线程允许积压的任务数量，超出后会返回 Server Is Busy。
+ 默认值：2000
+ 最小值：2

### `max-tasks-per-worker-normal`

+ 普通优先级线程池中单个线程允许积压的任务数量，超出后会返回 Server Is Busy。
+ 默认值：2000
+ 最小值：2

### `max-tasks-per-worker-low`

+ 低优先级线程池中单个线程允许积压的任务数量，超出后会返回 Server Is Busy。
+ 默认值：2000
+ 最小值：2

### `stack-size`

Coprocessor 线程池中线程的栈大小，默认值：10，单位：KiB|MiB|GiB。

+ 默认值：10MB
+ 单位：KB|MB|GB
+ 最小值：2MB

## storage

存储相关的配置项。

### `scheduler-notify-capacity`

+ scheduler 一次获取最大消息个数
+ 默认值：10240
+ 最小值：1

### `scheduler-concurrency`

+ scheduler 内置一个内存锁机制，防止同时对一个 key 进行操作。每个 key hash 到不同的槽。
+ 默认值：2048000
+ 最小值：1

### `scheduler-worker-pool-size`

+ scheduler 线程个数，主要负责写入之前的事务一致性检查工作。
+ 默认值：4
+ 最小值：1

### `scheduler-pending-write-threshold`

+ 写入数据队列的最大值，超过该值之后对于新的写入 TiKV 会返回 Server Is Busy 错误。
+ 默认值：100MB
+ 单位: MB|GB

## raftstore

raftstore 相关的配置项。

### `sync-log`

+ 数据、log 落盘是否 sync，注意：设置成 false 可能会丢数据。
+ 默认值：true

### `prevote`

+ 开启 Prevote 的开关，开启有助于减少隔离恢复后对系统造成的抖动。
+ 默认值：true

### `raftdb-path`

+ raft 库的路径，默认存储在 storage.data-dir/raft 下。
+ 默认值：""

### `raft-base-tick-interval`

+ 状态机 tick 一次的间隔时间。
+ 默认值：1s
+ 最小值：大于 0

### `raft-heartbeat-ticks`

+ 发送心跳时经过的 tick 个数，即每隔 raft-base-tick-interval * raft-heartbeat-ticks 时间发送一次心跳。
+ 默认值：2
+ 最小值：大于 0

### `raft-election-timeout-ticks`

+ 发起选举时经过的 tick 个数，即如果处于无主状态，大约经过 raft-base-tick-interval * raft-election-timeout-ticks 时间以后发起选举。
+ 默认值：10
+ 最小值：raft-heartbeat-ticks

### `raft-min-election-timeout-ticks`

+ 发起选举时至少经过的 tick 个数，如果为 0，则表示使用 raft-election-timeout-ticks，不能比 raft-election-timeout-ticks 小。
+ 默认值：0
+ 最小值：0

### `raft-max-election-timeout-ticks`

+ 发起选举时最多经过的 tick 个数，如果为 0，则表示使用 raft-election-timeout-ticks * 2。
+ 默认值：0
+ 最小值：0

### `raft-max-size-per-message`

+ 产生的单个消息包的大小限制，软限制。
+ 默认值：1MB
+ 最小值：0
+ 单位：MB

### `raft-max-inflight-msgs`

+ 待确认日志个数的数量，如果超过这个数量将会减缓发送日志的个数。
+ 默认值：256
+ 最小值：大于0

### `raft-entry-max-size`

+ 单个日志最大大小，硬限制。
+ 默认值：8MB
+ 最小值：0
+ 单位：MB|GB

### `raft-log-gc-tick-interval`

+ 删除 raft 日志的轮询任务调度间隔时间，0 表示不启用。
+ 默认值：10s
+ 最小值：0

### `raft-log-gc-threshold`

+ 允许残余的 raft 日志个数，这是一个软限制。
+ 默认值：50
+ 最小值：1

### `raft-log-gc-count-limit`

+ 允许残余的 raft 日志个数，这是一个硬限制。默认值为按照每个日志 1MB 而计算出来的 3/4 region 大小所能容纳的日志个数。
+ 最小值：0

### `raft-log-gc-size-limit`

+ 允许残余的 raft 日志大小，这是一个硬限制，默认为 region 大小的 3/4。
+ 最小值：大于 0

### `raft-entry-cache-life-time`

+ 内存中日志 cache 允许的最长残留时间。
+ 默认值：30s
+ 最小值：0

### `raft-reject-transfer-leader-duration`

+ 新节点保护时间，控制迁移 leader 到新加节点的最小时间，设置过小容易导致迁移 leader 失败。
+ 默认值：3s
+ 最小值：0

### `split-region-check-tick-interval`

+ 检查 region 是否需要分裂的时间间隔，0 表示不启用。
+ 默认值：10s
+ 最小值：0

### `region-split-check-diff`

+ 允许 region 数据超过指定大小的最大值，默认为 region 大小的 1/16。
+ 最小值：0

### `region-compact-check-interval`

+ 检查是否需要人工触发 rocksdb compaction 的时间间隔，0 表示不启用。
+ 默认值：5m
+ 最小值：0

### `clean-stale-peer-delay`

+ 延迟删除过期副本数据的时间。
+ 默认值：10m
+ 最小值：0

### `region-compact-check-step`

+ 每轮校验人工 compaction 时，一次性检查的 region 个数。
+ 默认值：100
+ 最小值：0

### `region-compact-min-tombstones`

+ 触发 rocksdb compaction 需要的 tombstone 个数。
+ 默认值：10000
+ 最小值：0

### `region-compact-tombstones-percent`

+ 触发 rocksdb compaction 需要的 tombstone 所占比例。
+ 默认值：30
+ 最小值：1
+ 最大值：100

### `pd-heartbeat-tick-interval`

+ 触发 region 对 PD 心跳的时间间隔，0 表示不启用。
+ 默认值：1m
+ 最小值：0

### `pd-store-heartbeat-tick-interval`

+ 触发 store 对 PD 心跳的时间间隔，0 表示不启用。
+ 默认值：10s
+ 最小值：0

### `snap-mgr-gc-tick-interval`

+ 触发回收过期 snapshot 文件的时间间隔，0 表示不启用。
+ 默认值：5s
+ 最小值：0

### `snap-gc-timeout`

+ snapshot 文件的最长保存时间。
+ 默认值：4h
+ 最小值：0

### `lock-cf-compact-interval`

+ 触发对 lock CF compact 检查的时间间隔。
+ 默认值：10m
+ 最小值：0

### `lock-cf-compact-bytes-threshold`

+ 触发对 lock CF 进行 compact 的大小。
+ 默认值：256MB
+ 最小值：0
+ 单位：MB

### `notify-capacity`

+ region 消息队列的最长长度。
+ 默认值：40960
+ 最小值：0

### `messages-per-tick`

+ 每轮处理的消息最大个数。
+ 默认值：4096
+ 最小值：0

### `max-peer-down-duration`

+ 副本允许的最长未响应时间，超过将被标记为 down，后续 PD 会尝试将其删掉。
+ 默认值：5m
+ 最小值：0

### `max-leader-missing-duration`

+ 允许副本处于无主状态的最长时间，超过将会向 PD 校验自己是否已经被删除。
+ 默认值：2h
+ 最小值：> abnormal-leader-missing-duration

### `abnormal-leader-missing-duration`

+ 允许副本处于无主状态的时间，超过将视为异常，标记在 metrics 和日志中。
+ 默认值：10m
+ 最小值：> peer-stale-state-check-interval

### `peer-stale-state-check-interval`

+ 触发检验副本是否处于无主状态的时间间隔。
+ 默认值：5m
+ 最小值：> 2 * election-timeout

### `leader-transfer-max-log-lag`

+ 尝试转移领导权时被转移者允许的最大日志缺失个数。
+ 默认值：10
+ 最小值：10

### `snap-apply-batch-size`

+ 当导入 snapshot 文件需要写数据时，内存写缓存的大小
+ 默认值：10MB
+ 最小值：0
+ 单位：MB

### `consistency-check-interval`

+ 触发一致性检查的时间间隔, 0 表示不启用。
+ 默认值：0s
+ 最小值：0

### `raft-store-max-leader-lease`

+ region 主可信任期的最长时间。
+ 默认值：9s
+ 最小值：0

### `right-derive-when-split`

+ 为 true 时，以最大分裂 key 为起点的 region 复用原 region 的 key；否则以原 region 起点 key 作为起点的 region 复用原 region 的 key。
+ 默认值：true

### `allow-remove-leader`

+ 允许删除主开关。
+ 默认值：false

### `merge-max-log-gap`

+ 进行 merge 时，允许的最大日志缺失个数。
+ 默认值：10
+ 最小值：> raft-log-gc-count-limit

### `merge-check-tick-interval`

+ 触发 merge 完成检查的时间间隔。
+ 默认值：10s
+ 最小值：大于 0

### `use-delete-range`

+ 开启 rocksdb delete_range 接口删除数据的开关。
+ 默认值：false

### `cleanup-import-sst-interval`

+ 触发检查过期 SST 文件的时间间隔，0 表示不启用。
+ 默认值：10m
+ 最小值：0

### `local-read-batch-size`

+ 一轮处理读请求的最大个数。
+ 默认值：1024
+ 最小值：大于 0

### `apply-max-batch-size`

+ 一轮处理数据落盘的最大请求个数。
+ 默认值：1024
+ 最小值：大于 0

### `apply-pool-size`

+ 处理数据落盘的线程池线程数。
+ 默认值：2
+ 最小值：大于 0

### `store-max-batch-size`

+ 一轮处理的最大请求个数。
+ 默认值：1024
+ 最小值：大于 0

### `store-pool-size`

+ 处理 raft 的线程池线程数。
+ 默认值：2
+ 最小值：大于 0

### `future-poll-size`

+ 驱动 future 的线程池线程数。
+ 默认值：1
+ 最小值：大于 0

## coprocessor

协处理器相关的配置项。

### `split-region-on-table`

+ 开启按 table 分裂 Region的开关，建议仅在 TiDB 模式下使用。
+ 默认值：true


### `batch-split-limit`

+ 批量分裂 Region 的阈值，调大该值可加速分裂 Region。
+ 默认值：10
+ 最小值：1

### `region-max-size`

+ Region 容量空间最大值，超过时系统分裂成多个 Region。
+ 默认值：144MB
+ 单位：KB|MB|GB

### `region-split-size`

+ 分裂后新 Region 的大小，此值属于估算值。
+ 默认值：96MB
+ 单位：KB|MB|GB

### `region-max-keys`

+ Region 最多允许的 key 的个数，超过时系统分裂成多个 Region。
+ 默认值：1440000

### `region-split-keys`

+ 分裂后新 Region 的 key 的个数，此值属于估算值。
+ 默认值：960000

## rocksdb

rocksdb 相关的配置项。

### `max-background-jobs`

+ RocksDB 后台线程个数。
+ 默认值：8
+ 最小值：1

### `max-sub-compactions`

+ RocksDB 进行 subcompaction 的并发个数。
+ 默认值：1
+ 最小值：1

### `max-open-files`

+ RocksDB 可以打开的文件总数。
+ 默认值：40960
+ 最小值：-1

### `max-manifest-file-size`

+ RocksDB Manifest 文件最大大小。
+ 默认值：128MB
+ 最小值：0
+ 单位：B|KB|MB|GB

### `create-if-missing`

+ 自动创建 DB 开关。
+ 默认值：true

### `wal-recovery-mode`

+ WAL 恢复模式，取值：0（TolerateCorruptedTailRecords），1（AbsoluteConsistency），2（PointInTimeRecovery），3（SkipAnyCorruptedRecords）。
+ 默认值：2
+ 最小值：0
+ 最大值：3

### `wal-dir`

+ WAL 存储目录，默认：“tmp/tikv/store”。
+ 默认值：/tmp/tikv/store

### `wal-ttl-seconds`

+ 归档 WAL 生存周期，超过该值时，系统会删除相关 WAL。
+ 默认值：0
+ 最小值：0
+ 单位：秒

### `wal-size-limit`

+ 归档 WAL 大小限制，超过该值时，系统会删除相关 WAL。
+ 默认值：0
+ 最小值：0
+ 单位：B|KB|MB|GB

### `enable-statistics`

+ 开启自动优化 Rate LImiter 的配置的开关。
+ 默认值：false

### `stats-dump-period`

+ 开启或关闭 Pipelined Write。
+ 默认值：true

### `compaction-readahead-size`

+ 异步 Sync 限速速率。
+ 默认值：0
+ 最小值：0
+ 单位：B|KB|MB|GB

### `writable-file-max-buffer-size`

+ WritableFileWrite 所使用的最大的 buffer 大小。
+ 默认值：1MB
+ 最小值：0
+ 单位：B|KB|MB|GB

### `use-direct-io-for-flush-and-compaction`

+ flush 或者 compaction 开启 DirectIO 的开关。
+ 默认值：false

### `rate-bytes-per-sec`

+ Rate Limiter 限制速率。
+ 默认值：0
+ 最小值：0
+ 单位：Bytes

### `rate-limiter-mode`

+ Rate LImiter 模式，取值：1（ReadOnly），2（WriteOnly），3（AllIo）。
+ 默认值：2
+ 最小值：1
+ 最大值：3

### `auto-tuned`

+ 开启自动优化 Rate LImiter 的配置的开关。
+ 默认值：false

### `enable-pipelined-write`

+ 开启 Pipelined Write 的开关。
+ 默认值：true

### `bytes-per-sync`

+ 异步 Sync 限速速率。
+ 默认值：1MB
+ 最小值：0
+ 单位：B|KB|MB|GB

### `wal-bytes-per-sync`

+ WAL Sync 限速速率，默认：512KB。
+ 默认值：512KB
+ 最小值：0
+ 单位：B|KB|MB|GB

### `info-log-max-size`

+ Info 日志的最大大小。
+ 默认值：1GB
+ 最小值：0
+ 单位：B|KB|MB|GB

### `info-log-roll-time`

+ 日志截断间隔时间，如果为0则不截断。
+ 默认值：0

### `info-log-keep-log-file-num`

+ 保留日志文件最大个数。
+ 默认值：10
+ 最小值：0

### `info-log-dir`

+ 日志存储目录。
+ 默认值：""

## rocksdb.titan

Titan 相关的配置项。

### `enabled`

+ 开启或关闭 Titan。
+ 默认值：false

### `dirname`

+ Titan Blob 文件存储目录。
+ 默认值：titandb

### `disable-gc`

+ 控制是否关闭 Titan 对 Blob 文件的 GC。
+ 默认值：false

### `max-background-gc`

+ Titan 后台 GC 的线程个数。
+ 默认值：1
+ 最小值：1

## rocksdb.defaultcf

rocksdb defaultcf 相关的配置项。

### `block-size`

+ rocksdb block size。
+ 默认值：64KB
+ 最小值：1KB
+ 单位：KB|MB|GB

### `block-cache-size`

+ 设置 rocksdb block 缓存大小。
+ 默认值：机器总内存 / 4
+ 最小值：0
+ 单位：KB|MB|GB

### `disable-block-cache`

+ 开启或关闭 block cache。
+ 默认值：false

### `cache-index-and-filter-blocks`

+ 开启或关闭缓存 index 和 filter。
+ 默认值：true 

### `pin-l0-filter-and-index-blocks`

+ 是否 pin 住 L0 的 index 和 filter。
+ 默认值：true 

### `use-bloom-filter`

+ 开启 bloom filter 的开关。
+ 默认值：true 

### `optimize-filters-for-hits`

+ 开启优化 filter 的命中率的开关。
+ 默认值：true 

### `whole_key_filtering`

+ 开启将整个 key 放到 bloom filter 中的开关。
+ 默认值：true 

### `bloom-filter-bits-per-key`

bloom filter 为每个 key 预留的长度。
+ 默认值：10
+ 单位：字节

### `block-based-bloom-filter`

+ 开启每个 block 建立 bloom filter 的开关。
+ 默认值：false

### `read-amp-bytes-per-bit`

+ 开启读放大统计的开关，0：不开启，> 0 开启。
+ 默认值：0
+ 最小值：0

### `compression-per-level`

+ 每一层默认压缩算法，默认：前两层为 No，后面 5 层为 lz4。
+ 默认值：["no", "no", "lz4", "lz4", "lz4", "zstd", "zstd"]

### `write-buffer-size`

+ memtable 大小。
+ 默认值：128MB
+ 最小值：0
+ 单位：KB|MB|GB

### `max-write-buffer-number`

+ 最大 memtable 个数。
+ 默认值：5
+ 最小值：0

### `min-write-buffer-number-to-merge`

+ 触发 flush 的最小 memtable 个数。
+ 默认值：1
+ 最小值：0


### `max-bytes-for-level-base`

+ base level (L1) 最大字节数，一般设置为 memtable 大小 4 倍。
+ 默认值：512MB
+ 最小值：0
+ 单位：KB|MB|GB

### `target-file-size-base`

+ base level 的目标文件大小。
+ 默认值：8MB
+ 最小值：0
+ 单位：KB|MB|GB

### `level0-file-num-compaction-trigger`

+ 触发 compaction 的 L0 文件最大个数。
+ 默认值：4
+ 最小值：0

### `level0-slowdown-writes-trigger`

+ 触发 write stall 的 L0 文件最大个数。
+ 默认值：20
+ 最小值：0

### `level0-stop-writes-trigger`

+ 完全阻停写入的 L0 文件最大个数。
+ 默认值：36
+ 最小值：0

### `max-compaction-bytes`

+ 一次 compaction 最大写入字节数，默认 2GB。
+ 默认值：2GB
+ 最小值：0
+ 单位：KB|MB|GB

### `compaction-pri`

Compaction 优先类型，默认：3（MinOverlappingRatio），0（ByCompensatedSize），
1（OldestLargestSeqFirst），2（OldestSmallestSeqFirst）。
+ 默认值：3

### `dynamic-level-bytes`

+ 开启 dynamic level bytes 优化的开关。
+ 默认值：true

### `num-levels`

+ RocksDB 文件最大层数。
+ 默认值：7

### `max-bytes-for-level-multiplier`

+ 每一层的默认放大倍数。
+ 默认值：10

### `rocksdb.defaultcf.compaction-style`

+ Compaction 方法，可选值为 level，universal。
+ 默认值：level

### `disable-auto-compactions`

+ 开启自动 compaction 的开关。
+ 默认值：false

### `soft-pending-compaction-bytes-limit`

+ pending compaction bytes 的软限制。
+ 默认值：64GB
+ 单位：KB|MB|GB

### `hard-pending-compaction-bytes-limit`

+ pending compaction bytes 的硬限制。
+ 默认值：256GB
+ 单位：KB|MB|GB

## rocksdb.defaultcf.titan

rocksdb defaultcf titan 相关的配置项。

### `min-blob-size`

+ 最小存储在 Blob 文件中 value 大小，低于该值的 value 还是存在 LSM-Tree 中。
+ 默认值：1KB
+ 最小值：0
+ 单位：KB|MB|GB

### `blob-file-compression`

+ Blob 文件所使用的压缩算法，可选值：no, snappy, zlib, bzip2, lz4, lz4hc, zstd。
+ 默认值：lz4

### `blob-cache-size`

+ Blob 文件的 cache 大小，默认：0GB。
+ 默认值：0GB
+ 最小值：0
+ 单位：KB|MB|GB

### `min-gc-batch-size`

+ 做一次 GC 所要求的最低 Blob 文件大小总和。
+ 默认值：16MB
+ 最小值：0
+ 单位：KB|MB|GB

### `max-gc-batch-size`

+ 做一次 GC 所要求的最高 Blob 文件大小总和。
+ 默认值：64MB
+ 最小值：0
+ 单位：KB|MB|GB

### `discardable-ratio`

+ Blob 文件 GC 的触发比例，如果某 Blob 文件中的失效 value 的比例高于该值才可能被 GC 选中。
+ 默认值：0.5
+ 最小值：0
+ 最大值：1

### `sample-ratio`

+ 进行 GC 时，对 Blob 文件进行采样时读取数据占整个文件的比例。
+ 默认值：0.1
+ 最小值：0
+ 最大值：1

### `merge-small-file-threshold`

+ Blob 文件的大小小于该值时，无视 discardable-ratio 仍可能被 GC 选中。
+ 默认值：8MB
+ 最小值：0
+ 单位：KB|MB|GB

## rocksdb.writecf

rocksdb writecf 相关的配置项。

### `block-cache-size`

+ block cache size。
+ 默认值：机器总内存 * 15%
+ 单位：MB|GB

### `optimize-filters-for-hits`

+ 开启优化 filter 的命中率的开关。
+ 默认值：false

### `whole-key-filtering`

+ 开启将整个 key 放到 bloom filter 中的开关。
+ 默认值：false

## rocksdb.lockcf

rocksdb lockcf 相关配置项。

### `block-cache-size`

+ block cache size。
+ 默认值：机器总内存 * 2%
+ 单位：MB|GB

### `optimize-filters-for-hits`

+ 开启优化 filter 的命中率的开关。
+ 默认值：false

### `level0-file-num-compaction-trigger`

+ 触发 compaction 的 L0 文件个数。
+ 默认值：1

## raftdb

raftdb 相关配置项。

### `max-background-jobs`

+ RocksDB 后台线程个数。
+ 默认值：2
+ 最小值：1

### `max-sub-compactions`

+ RocksDB 进行 subcompaction 的并发数。
+ 默认值：1
+ 最小值：1

### `wal-dir`

+ WAL 存储目录。
+ 默认值：/tmp/tikv/store

## import

import 相关的配置项。

### `num-threads`

+ 处理 RPC 请求线程数。
+ 默认值：8
+ 最小值：1

### `num-import-jobs`

+ 并发导入工作任务数。
+ 默认值：8
+ 最小值：1

