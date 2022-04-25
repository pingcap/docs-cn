---
title: TiKV 配置文件描述
---

# TiKV 配置文件描述

TiKV 配置文件比命令行参数支持更多的选项。你可以在 [etc/config-template.toml](https://github.com/tikv/tikv/blob/master/etc/config-template.toml) 找到默认值的配置文件，重命名为 config.toml 即可。

本文档只阐述未包含在命令行参数中的参数，命令行参数参见 [TiKV 配置参数](/command-line-flags-for-tikv-configuration.md)。

<!-- markdownlint-disable MD001 -->

## 全局配置

### abort-on-panic

+ 设置 TiKV panic 时是否调用 `abort()` 退出进程。此选项影响 TiKV 是否允许系统生成 core dump 文件。

    + 如果此配置项值为 false ，当 TiKV panic 时，TiKV 调用 `exit()` 退出进程。
    + 如果此配置项值为 true ，当 TiKV panic 时，TiKV 调用 `abort()` 退出进程。此时 TiKV 允许系统在退出时生成 core dump 文件。要生成 core dump 文件，你还需要进行 core dump 相关的系统配置（比如打开 `ulimit -c` 和配置 core dump 路径，不同操作系统配置方式不同）。建议将 core dump 生成路径设置在 TiKV 数据的不同磁盘分区，避免 core dump 文件占用磁盘空间过大，造成 TiKV 磁盘空间不足。
    
+ 默认值：false

### `log-level`

+ 日志等级。
+ 可选值："trace"，"debug"，"info"，"warning"，"error"，"critical"
+ 默认值："info"

### `log-file`

+ 日志文件。如果未设置该项，日志会默认输出到 "stderr"。
+ 默认值：""

### `log-format`

+ 日志的格式。
+ 可选值："json"，"text"
+ 默认值："text"

### `log-rotation-timespan`

+ 轮换日志的时间跨度。当超过该时间跨度，日志文件会被轮换，即在当前日志文件的文件名后附加一个时间戳，并创建一个新文件。
+ 默认值："24h"

### `log-rotation-size`

+ 触发日志轮换的文件大小。一旦日志文件大小超过指定的阈值，日志文件将被轮换，将旧文件被置于新文件中，新文件名即旧文件名加上时间戳后缀。
+ 默认值："300MB"

### `slow-log-file`

+ 存储慢日志的文件。
+ 如果未设置本项但设置了 `log-file`，慢日志将输出至 `log-file` 指定的日志文件中。如果本项和 `log-file` 均未设置，所有日志默认输出到 "stderr"。
+ 默认值：""

### `slow-log-threshold`

+ 输出慢日志的阈值。处理时间超过该阈值后会输出慢日志。
+ 默认值："1s"

## server

服务器相关的配置项。

### `status-thread-pool-size`

+ HTTP API 服务的工作线程数量。
+ 默认值：1
+ 最小值：1

### `grpc-compression-type`

+ gRPC 消息的压缩算法，取值：none， deflate， gzip。
+ 默认值：none

> **注意：**
>
> 取值为 `gzip` 时，部分 TiDB Dashboard 可能无法完成对应的压缩运算，会显示异常。调整回默认值 `none` 后，TiDB Dashboard 可正常显示。

### `grpc-concurrency`

+ gRPC 工作线程的数量。
+ 默认值：5
+ 最小值：1

### `grpc-concurrent-stream`

+ 一个 gRPC 链接中最多允许的并发请求数量。
+ 默认值：1024
+ 最小值：1

### `grpc-memory-pool-quota`

+ gRPC 可使用的内存大小限制。
+ 默认值: 无限制
+ 建议仅在出现内存不足 (OOM) 的情况下限制内存使用。需要注意，限制内存使用可能会导致卡顿。

### `grpc-raft-conn-num`

+ tikv 节点之间用于 raft 通讯的链接最大数量。
+ 默认值：1
+ 最小值：1

### `max-grpc-send-msg-len`

+ 设置可发送的最大 gRPC 消息长度。
+ 默认值：10485760
+ 单位：Bytes
+ 最大值：2147483647

### `grpc-stream-initial-window-size`

+ gRPC stream 的 window 大小。
+ 默认值：2MB
+ 单位：KB|MB|GB
+ 最小值：1KB

### `grpc-keepalive-time`

+ gRPC 发送 keep alive ping 消息的间隔时长。
+ 默认值：10s
+ 最小值：1s

### `grpc-keepalive-timeout`

+ 关闭 gRPC 链接的超时时长。
+ 默认值：3s
+ 最小值：1s

### `concurrent-send-snap-limit`

+ 同时发送 snapshot 的最大个数。
+ 默认值：32
+ 最小值：1

### `concurrent-recv-snap-limit`

+ 同时接受 snapshot 的最大个数。
+ 默认值：32
+ 最小值：1

### `end-point-recursion-limit`

+ endpoint 下推查询请求解码消息时，最多允许的递归层数。
+ 默认值：1000
+ 最小值：1

### `end-point-request-max-handle-duration`

+ endpoint 下推查询请求处理任务最长允许的时长。
+ 默认值：60s
+ 最小值：1s

### `snap-max-write-bytes-per-sec`

+ 处理 snapshot 时最大允许使用的磁盘带宽。
+ 默认值：100MB
+ 单位：KB|MB|GB
+ 最小值：1KB

### `end-point-slow-log-threshold`

+ endpoint 下推查询请求输出慢日志的阈值，处理时间超过阈值后会输出慢日志。
+ 默认值：1s
+ 最小值：0

## readpool.unified

统一处理读请求的线程池相关的配置项。该线程池自 4.0 版本起取代原有的 storage 和 coprocessor 线程池。

### `min-thread-count`

+ 统一处理读请求的线程池最少的线程数量。
+ 默认值：1

### `max-thread-count`

+ 统一处理读请求的线程池最多的线程数量。
+ 默认值：CPU * 0.8，但最少为 4

### `stack-size`

+ 统一处理读请求的线程池中线程的栈大小。
+ 类型：整数 + 单位
+ 默认值：10MB
+ 单位：KB|MB|GB
+ 最小值：2MB
+ 最大值：在系统中执行 `ulimit -sH` 命令后，输出的千字节数。

### `max-tasks-per-worker`

+ 统一处理读请求的线程池中单个线程允许积压的最大任务数量，超出后会返回 Server Is Busy。
+ 默认值：2000
+ 最小值：2

## readpool.storage

存储线程池相关的配置项。

### `use-unified-pool`

+ 是否使用统一的读取线程池（在 [`readpool.unified`](#readpoolunified) 中配置）处理存储请求。该选项值为 false 时，使用单独的存储线程池。通过本节 (`readpool.storage`) 中的其余配置项配置单独的线程池。
+ 默认值：如果本节 (`readpool.storage`) 中没有其他配置，默认为 true。否则，为了升级兼容性，默认为 false，请根据需要更改 [`readpool.unified`](#readpoolunified) 中的配置后再启用该选项。

### `high-concurrency`

+ 处理高优先级读请求的线程池线程数量。
+ 当 8 ≤ cpu num ≤ 16 时，默认值为 cpu_num * 0.5；当 cpu num 大于 8 时，默认值为 4；当 cpu num 大于 16 时，默认值为 8。
+ 最小值：1

### `normal-concurrency`

+ 处理普通优先级读请求的线程池线程数量。
+ 当 8 ≤ cpu num ≤ 16 时，默认值为 cpu_num * 0.5；当 cpu num 大于 8 时，默认值为 4；当 cpu num 大于 16 时，默认值为 8。
+ 最小值：1

### `low-concurrency`

+ 处理低优先级读请求的线程池线程数量。
+ 当 8 ≤ cpu num ≤ 16 时，默认值为 cpu_num * 0.5；当 cpu num 大于 8 时，默认值为 4；当 cpu num 大于 16 时，默认值为 8。
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
+ 类型：整数 + 单位
+ 默认值：10MB
+ 单位：KB|MB|GB
+ 最小值：2MB
+ 最大值：在系统中执行 `ulimit -sH` 命令后，输出的千字节数。

## readpool.coprocessor

协处理器线程池相关的配置项。

### `use-unified-pool`

+ 是否使用统一的读取线程池（在 [`readpool.unified`](#readpoolunified) 中配置）处理协处理器请求。该选项值为 false 时，使用单独的协处理器线程池。通过本节 (`readpool.coprocessor`) 中的其余配置项配置单独的线程池。
+ 默认值：如果本节 (`readpool.coprocessor`) 中没有其他配置，默认为 true。否则，为了升级兼容性，默认为 false，请根据需要更改 [`readpool.unified`](#readpoolunified) 中的配置后再启用该选项。

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

+ Coprocessor 线程池中线程的栈大小，默认值：10，单位：KiB|MiB|GiB。
+ 类型：整数 + 单位
+ 默认值：10MB
+ 单位：KB|MB|GB
+ 最小值：2MB
+ 最大值：在系统中执行 `ulimit -sH` 命令后，输出的千字节数。

## storage

存储相关的配置项。

### `scheduler-concurrency`

+ scheduler 内置一个内存锁机制，防止同时对一个 key 进行操作。每个 key hash 到不同的槽。
+ 默认值：524288
+ 最小值：1

### `scheduler-worker-pool-size`

+ scheduler 线程个数，主要负责写入之前的事务一致性检查工作。如果 CPU 核心数量大于等于 16，默认为 8；否则默认为 4。
+ 默认值：4
+ 最小值：1

### `scheduler-pending-write-threshold`

+ 写入数据队列的最大值，超过该值之后对于新的写入 TiKV 会返回 Server Is Busy 错误。
+ 默认值：100MB
+ 单位: MB|GB

### `reserve-space`

+ TiKV 启动时预占额外空间的临时文件大小。临时文件名为 `space_placeholder_file`，位于 `storage.data-dir` 目录下。TiKV 磁盘空间耗尽无法正常启动需要紧急干预时，可以删除该文件，并且将 `reserve-space` 设置为 `0MB`。
+ 默认值：5GB
+ 单位: MB|GB

### `enable-ttl`

> **警告：**
>
> - 你**只能**在部署新的 TiKV 集群时将 `enable-ttl` 的值设置为 `true` 或 `false`，**不能**在已有的 TiKV 集群中修改该配置项的值。由于该配置项为 `true` 和 `false` 的 TiKV 集群所存储的数据格式不相同，如果你在已有的 TiKV 集群中修改该配置项的值，会造成不同格式的数据存储在同一个集群，导致重启对应的 TiKV 集群时 TiKV 报 "can't enable ttl on a non-ttl instance" 错误。
> - 你**只能**在 TiKV 集群中使用 `enable-ttl`，**不能**在有 TiDB 节点的集群中使用该配置项（即在此类集群中把 `enable-ttl` 设置为 `true`），否则会导致数据损坏、TiDB 集群升级失败等严重后果。

+ TTL 即 Time to live。数据超过 TTL 时间后会被自动删除。用户需在客户端写入请求中指定 TTL。不指定 TTL 即表明相应数据不会被自动删除。
+ 默认值：false

### `ttl-check-poll-interval`

+ 回收数据物理空间的检查周期。如果数据超过了 TTL 时间，数据的物理空间会在检查时被强制回收。
+ 默认值：12h
+ 最小值：0s

## storage.block-cache

RocksDB 多个 CF 之间共享 block cache 的配置选项。当开启时，为每个 CF 单独配置的 block cache 将无效。

### `shared`

+ 是否开启共享 block cache。
+ 默认值：true

### `capacity`

+ 共享 block cache 的大小。
+ 默认值：系统总内存大小的 45%
+ 单位：KB|MB|GB

## storage.io-rate-limit

I/O rate limiter 相关的配置项。

### `max-bytes-per-sec`

+ 限制服务器每秒从磁盘读取数据或写入数据的最大 I/O 字节数，I/O 类型由下面的 `mode` 配置项决定。达到该限制后，TiKV 倾向于放缓后台操作为前台操作节流。该配置项值应设为磁盘的最佳 I/O 带宽，例如云盘厂商指定的最大 I/O 带宽。
+ 默认值："0MB"

### `mode`

+ 确定哪些类型的 I/O 操作被计数并受 `max-bytes-per-sec` 阈值的限流。当前 TiKV 只支持 write-only 只写模式。 
+ 可选值：write-only
+ 默认值：write-only

## raftstore

raftstore 相关的配置项。

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

### `raft-max-size-per-msg`

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

### `hibernate-regions`

+ 打开或关闭静默 Region。打开后，如果 Region 长时间处于非活跃状态，即被自动设置为静默状态。静默状态的 Region 可以降低 Leader 和 Follower 之间心跳信息的系统开销。可以通过 `peer-stale-state-check-interval` 调整 Leader 和 Follower 之间的心跳间隔。
+ 默认值：v5.0.2 及以后版本默认值为 true，v5.0.2 以前的版本默认值为 false

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
+ 默认值：1m
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
+ 默认值：128
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
+ 默认值：2s
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
+ 默认值：256
+ 最小值：大于 0

### `apply-pool-size`

+ 处理数据落盘的线程池线程数。
+ 默认值：2
+ 最小值：大于 0

### `store-max-batch-size`

+ 一轮处理的最大请求个数。
+ 如果开启 `hibernate-regions`，默认值为 256；如果关闭 `hibernate-regions`，默认值为 1024
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

coprocessor 相关的配置项。

### `split-region-on-table`

+ 开启按 table 分裂 Region的开关，建议仅在 TiDB 模式下使用。
+ 默认值：false

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
+ 最小值：2

### `max-background-flushes`

+ RocksDB 用于刷写 memtable 的最大后台线程数。
+ 默认值：2
+ 最小值：1

### `max-sub-compactions`

+ RocksDB 进行 subcompaction 的并发个数。
+ 默认值：3
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

+ 开启 RocksDB 的统计信息。
+ 默认值：true

### `stats-dump-period`

+ 将统计信息输出到日志中的间隔时间。
+ 默认值：10m

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

+ RocksDB compaction rate limiter 的限制速率。
+ 默认值：10GB
+ 最小值：0
+ 单位：B|KB|MB|GB

### `rate-limiter-mode`

+ RocksDB 的 compaction rate limiter 模式。
+ 可选值：1 (ReadOnly)，2 (WriteOnly)，3 (AllIo)
+ 默认值：2
+ 最小值：1
+ 最大值：3

### `rate-limiter-auto-tuned` <span class="version-mark">从 v5.0 版本开始引入</span>

+ 控制是否依据最近的负载量自动优化 RocksDB 的 compaction rate limiter 配置。此配置项开启后，compaction pending bytes 监控指标值会比一般情况下稍微高些。
+ 默认值：true

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

+ 日志截断间隔时间，如果为 0s 则不截断。
+ 默认值：0s

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

+ 开启 Titan 开关。
+ 默认值：false

### `dirname`

+ Titan Blob 文件存储目录。
+ 默认值：titandb

### `disable-gc`

+ 关闭 Titan 对 Blob 文件的 GC 的开关。
+ 默认值：false

### `max-background-gc`

+ Titan 后台 GC 的线程个数。
+ 默认值：4
+ 最小值：1

## rocksdb.defaultcf | rocksdb.writecf | rocksdb.lockcf

rocksdb defaultcf、rocksdb writecf 和 rocksdb lockcf 相关的配置项。

### `block-size`

+ 一个 RocksDB block 的默认大小。
+ `defaultcf` 默认值：64KB
+ `writecf` 默认值：64KB
+ `lockcf` 默认值：16KB
+ 最小值：1KB
+ 单位：KB|MB|GB

### `block-cache-size`

+ 一个 RocksDB block 的默认缓存大小。
+ `defaultcf` 默认值：机器总内存 * 25%
+ `writecf` 默认值：机器总内存 * 15%
+ `lockcf` 默认值：机器总内存 * 2%
+ 最小值：0
+ 单位：KB|MB|GB

### `disable-block-cache`

+ 开启 block cache 开关。
+ 默认值：false

### `cache-index-and-filter-blocks`

+ 开启缓存 index 和 filter 的开关。
+ 默认值：true

### `pin-l0-filter-and-index-blocks`

+ 是否 pin 住 L0 的 index 和 filter。
+ 默认值：true

### `use-bloom-filter`

+ 开启 bloom filter 的开关。
+ 默认值：true

### `optimize-filters-for-hits`

+ 开启优化 filter 的命中率的开关。
+ `defaultcf` 默认值：`true`
+ `writecf` 默认值：`false`
+ `lockcf` 默认值：`false`

### `whole-key-filtering`

+ 开启将整个 key 放到 bloom filter 中的开关。
+ `defaultcf` 默认值：`true`
+ `writecf` 默认值：`false`
+ `lockcf` 默认值：`false`

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

+ 每一层默认压缩算法。
+ `defaultcf` 的默认值：["no", "no", "lz4", "lz4", "lz4", "zstd", "zstd"]
+ `writecf` 的默认值：["no", "no", "lz4", "lz4", "lz4", "zstd", "zstd"]
+ `lockcf` 的默认值：["no", "no", "no", "no", "no", "no", "no"]

### `bottommost-level-compression`

+ 设置最底层的压缩算法。该设置将覆盖 `compression-per-level` 的设置。
+ 因为最底层并非从数据开始写入 LSM-tree 起就直接采用 `compression-per-level` 数组中的最后一个压缩算法，使用 `bottommost-level-compression` 可以让最底层从一开始就使用压缩效果最好的压缩算法。
+ 如果不想设置最底层的压缩算法，可以将该配置项的值设为 `disable`。
+ 默认值："zstd"

### `write-buffer-size`

+ memtable 大小。
+ `defaultcf` 默认值：`"128MB"`
+ `writecf` 默认值：`"128MB"`
+ `lockcf` 默认值：`"32MB"`
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
+ `defaultcf` 默认值：`"512MB"`
+ `writecf` 默认值：`"512MB"`
+ `lockcf` 默认值：`"128MB"`
+ 最小值：0
+ 单位：KB|MB|GB

### `target-file-size-base`

+ base level 的目标文件大小。当 `enable-compaction-guard` 的值为 `true` 时，`compaction-guard-max-output-file-size` 会覆盖此配置。
+ 默认值：8MB
+ 最小值：0
+ 单位：KB|MB|GB

### `level0-file-num-compaction-trigger`

+ 触发 compaction 的 L0 文件最大个数。
+ `defaultcf` 默认值：`4`
+ `writecf` 默认值：`4`
+ `lockcf` 默认值：`1`
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

+ Compaction 优先类型
+ 可选择值：`0` (`ByCompensatedSize`)，`1` (`OldestLargestSeqFirst`)，`2` (`OldestSmallestSeqFirst`)，`3` (`MinOverlappingRatio`)。
+ `defaultcf` 默认值：`3`
+ `writecf` 默认值：`3`
+ `lockcf` 默认值：`1`

### `dynamic-level-bytes`

+ 开启 dynamic level bytes 优化的开关。
+ 默认值：true

### `num-levels`

+ RocksDB 文件最大层数。
+ 默认值：7

### `max-bytes-for-level-multiplier`

+ 每一层的默认放大倍数。
+ 默认值：10

### `compaction-style`

+ Compaction 方法。
+ 可选值（仅可输入数字）：`0` (`Level`)，`1` (`Universal`)，`2` (`Fifo`)
+ 默认值：`0`

### `disable-auto-compactions`

+ 是否关闭自动 compaction
+ 默认值：false

### `soft-pending-compaction-bytes-limit`

+ pending compaction bytes 的软限制。
+ 默认值：192GB
+ 单位：KB|MB|GB

### `hard-pending-compaction-bytes-limit`

+ pending compaction bytes 的硬限制。
+ 默认值：256GB
+ 单位：KB|MB|GB

### `enable-compaction-guard`

+ 设置 compaction guard 的启用状态。compaction guard 优化通过使用 TiKV Region 边界分割 SST 文件，帮助降低 compaction I/O，让 TiKV 能够输出较大的 SST 文件，并且在迁移 Region 时及时清理过期数据。
+ `defaultcf` 默认值：`true`
+ `writecf` 默认值：`true`
+ `lockcf` 默认值：`false`

### `compaction-guard-min-output-file-size`

+ 设置 compaction guard 启用时 SST 文件大小的最小值，防止 SST 文件过小。
+ 默认值：8MB
+ 单位：KB|MB|GB

### `compaction-guard-max-output-file-size`

+ 设置 compaction guard 启用时 SST 文件大小的最大值，防止 SST 文件过大。对于同一列族，此配置项的值会覆盖 `target-file-size-base`。
+ 默认值：128MB
+ 单位：KB|MB|GB

## rocksdb.defaultcf.titan

rocksdb defaultcf titan 相关的配置项。

### `min-blob-size`

+ 最小存储在 Blob 文件中 value 大小，低于该值的 value 还是存在 LSM-Tree 中。
+ 默认值：1KB
+ 最小值：0
+ 单位：KB|MB|GB

### `blob-file-compression`

+ Blob 文件所使用的压缩算法，可选值：no、snappy、zlib、bz2、lz4、lz4hc、zstd。
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

### `blob-run-mode`

+ Titan 的运行模式选择，可选值：
    + "normal"：value size 超过 min-blob-size 的数据会写入到 blob 文件。
    + "read_only"：不再写入新数据到 blob，原有 blob 内的数据仍然可以读取。
    + "fallback"：将 blob 内的数据写回 LSM。
+ 默认值："normal"

### `level-merge`

+ 是否通过开启 level-merge 来提升读性能，副作用是写放大会比不开启更大。
+ 默认值：false

### `gc-merge-rewrite`

+ 是否开启使用 merge operator 来进行 Titan GC 写回操作，减少 Titan GC 对于前台写入的影响。
+ 默认值：false

raftdb 相关配置项。

### `max-background-jobs`

+ RocksDB 后台线程个数。
+ 默认值：4
+ 最小值：2

### `max-sub-compactions`

+ RocksDB 进行 subcompaction 的并发数。
+ 默认值：2
+ 最小值：1

### `wal-dir`

+ WAL 存储目录。
+ 默认值：/tmp/tikv/store

## security

安全相关配置项。

### `ca-path`

+ CA 文件路径
+ 默认值：""

### `cert-path`

+ 包含 X509 证书的 PEM 文件路径
+ 默认值：""

### `key-path`

+ 包含 X509 key 的 PEM 文件路径
+ 默认值：""

### `redact-info-log` <span class="version-mark">从 v4.0.8 版本开始引入</span>

+ 若开启该选项，日志中的用户数据会以 `?` 代替。
+ 默认值：`false`

## security.encryption

[静态加密](/encryption-at-rest.md) (TDE) 有关的配置项。

### `data-encryption-method`

+ 数据文件的加密方法。
+ 可选值：`"plaintext"`，`"aes128-ctr"`，`"aes192-ctr"`，`"aes256-ctr"`
+ 选择 `"plaintext"` 以外的值则表示启用加密功能。此时必须指定主密钥。
+ 默认值：`"plaintext"`

### `data-key-rotation-period`

+ 指定 TiKV 轮换数据密钥的频率。
+ 默认值：`7d`

### enable-file-dictionary-log

+ 启用优化，以减少 TiKV 管理加密元数据时的 I/O 操作和互斥锁竞争。
+ 此配置参数默认启用，为避免可能出现的兼容性问题，请参考[静态加密 - TiKV 版本间兼容性](/encryption-at-rest.md#tikv-版本间兼容性)。
+ 默认值：`true`

### master-key

+ 指定启用加密时的主密钥。若要了解如何配置主密钥，可以参考[静态加密 - 配置加密](/encryption-at-rest.md#配置加密)。

### previous-master-key

+ 指定轮换新主密钥时的旧主密钥。旧主密钥的配置格式与主密钥相同。若要了解如何配置主密钥，可以参考[静态加密 - 配置加密](/encryption-at-rest.md#配置加密)。

## import

用于 TiDB Lightning 导入及 BR 恢复相关的配置项。

### `num-threads`

+ 处理 RPC 请求线程数。
+ 默认值：8
+ 最小值：1

### `num-import-jobs`

+ 并发导入工作任务数。
+ 默认值：8
+ 最小值：1

## gc

### `enable-compaction-filter` <span class="version-mark">从 v5.0 版本开始引入</span>

+ 是否开启 GC in Compaction Filter 特性
+ 默认值：true

## backup

用于 BR 备份相关的配置项。

### `num-threads`

+ 处理备份的工作线程数。
+ 默认值：CPU * 0.75，但最大为 32
+ 最小值：1

## cdc

用于 TiCDC 捕捉变更数据相关的配置项。

### `min-ts-interval`

+ 定期推进 Resolved TS 的时间间隔。
+ 默认值：1s

### `old-value-cache-memory-quota`

+ 缓存在内存中的 TiCDC Old Value 的条目占用内存的上限。
+ 默认值：512MB

### `sink-memory-quota`

+ 缓存在内存中的 TiCDC 数据变更事件占用内存的上限。
+ 默认值：512MB

### `incremental-scan-speed-limit`

+ 增量扫描历史数据的速度上限。
+ 默认值：128MB，即 128MB 每秒。

### `incremental-scan-threads`

+ 增量扫描历史数据任务的线程个数。
+ 默认值：4，即 4 个线程

### `incremental-scan-concurrency`

+ 增量扫描历史数据任务的最大并发执行个数。
+ 默认值：6，即最多并发执行 6 个任务
+ 注意：`incremental-scan-concurrency` 需要大于等于 `incremental-scan-threads`，否则 TiKV 启动会报错。

## resolved-ts

用于维护 Resolved TS 以服务 Stale Read 请求的相关配置项。

### `enable`

+ 是否为所有 Region 维护 Resolved TS
+ 默认值：true

### `advance-ts-interval`

+ 定期推进 Resolved TS 的时间间隔。
+ 默认值：1s

### `scan-lock-pool-size`

+ 初始化 Resolved TS 时 TiKV 扫描 MVCC（多版本并发控制）锁数据的线程个数。
+ 默认值：2，即 2 个线程

## pessimistic-txn

悲观事务使用方法请参考 [TiDB 悲观事务模式](/pessimistic-transaction.md)。

### `wait-for-lock-timeout`

+ 悲观事务在 TiKV 中等待其他事务释放锁的最长时间。若超时则会返回错误给 TiDB 并由 TiDB 重试加锁，语句最长等锁时间由 `innodb_lock_wait_timeout` 控制。
+ 默认值：1s
+ 最小值：1ms

### `wake-up-delay-duration`

+ 悲观事务释放锁时，只会唤醒等锁事务中 `start_ts` 最小的事务，其他事务将会延迟 `wake-up-delay-duration` 之后被唤醒。
+ 默认值：20ms

### `pipelined`

+ 开启流水线式加悲观锁流程。开启该功能后，TiKV 在检测数据满足加锁要求后，立刻通知 TiDB 执行后面的请求，并异步写入悲观锁，从而降低大部分延迟，显著提升悲观事务的性能。但有较低概率出现悲观锁异步写入失败的情况，可能会导致悲观事务提交失败。
+ 默认值：true
