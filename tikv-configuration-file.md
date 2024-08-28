---
title: TiKV 配置文件描述
---

# TiKV 配置文件描述

TiKV 配置文件比命令行参数支持更多的选项。你可以在 [etc/config-template.toml](https://github.com/tikv/tikv/blob/master/etc/config-template.toml) 找到默认值的配置文件，重命名为 config.toml 即可。

本文档只阐述未包含在命令行参数中的参数，命令行参数参见 [TiKV 配置参数](/command-line-flags-for-tikv-configuration.md)。

> **Tip:**
>
> 如果你需要调整配置项的值，请参考[修改配置参数](/maintain-tidb-using-tiup.md#修改配置参数)进行操作。

<!-- markdownlint-disable MD001 -->

## 全局配置

### `abort-on-panic`

+ 设置 TiKV panic 时是否调用 `abort()` 退出进程。此选项影响 TiKV 是否允许系统生成 core dump 文件。

    + 如果此配置项值为 false ，当 TiKV panic 时，TiKV 调用 `exit()` 退出进程。
    + 如果此配置项值为 true ，当 TiKV panic 时，TiKV 调用 `abort()` 退出进程。此时 TiKV 允许系统在退出时生成 core dump 文件。要生成 core dump 文件，你还需要进行 core dump 相关的系统配置（比如打开 `ulimit -c` 和配置 core dump 路径，不同操作系统配置方式不同）。建议将 core dump 生成路径设置在 TiKV 数据的不同磁盘分区，避免 core dump 文件占用磁盘空间过大，造成 TiKV 磁盘空间不足。

+ 默认值：false

### `slow-log-file`

+ 存储慢日志的文件。
+ 如果未设置本项但设置了 `log.file.filename`，慢日志将输出至 `log.file.filename` 指定的日志文件中。
+ 如果本项和 `log.file.filename` 均未设置，所有日志默认输出到 `"stderr"`。
+ 如果同时设置了两项，普通日志会输出至 `log.file.filename` 指定的日志文件中，而慢日志则会输出至本配置项指定的日志文件中。
+ 默认值：""

### `slow-log-threshold`

+ 输出慢日志的阈值。处理时间超过该阈值后会输出慢日志。
+ 默认值："1s"

## log <span class="version-mark">从 v5.4.0 版本开始引入</span>

日志相关的配置项。

自 v5.4.0 版本起，废弃原 log 参数 `log-rotation-timespan`，并将 `log-level`、`log-format`、`log-file`、`log-rotation-size` 变更为下列参数，与 TiDB 的 log 参数保持一致。如果只设置了原参数、且把其值设为非默认值，原参数与新参数会保持兼容；如果同时设置了原参数和新参数，则会使用新参数。

### `level` <span class="version-mark">从 v5.4.0 版本开始引入</span>

+ 日志等级。
+ 可选值："debug"，"info"，"warn"，"error"，"fatal"
+ 默认值："info"

### `format` <span class="version-mark">从 v5.4.0 版本开始引入</span>

+ 日志的格式。
+ 可选值："json"，"text"
+ 默认值："text"

### `enable-timestamp` <span class="version-mark">从 v5.4.0 版本开始引入</span>

+ 是否开启日志中的时间戳。
+ 可选值："true"，"false"
+ 默认值："true"

## log.file <span class="version-mark">从 v5.4.0 版本开始引入</span>

日志文件相关的配置项。

### `filename` <span class="version-mark">从 v5.4.0 版本开始引入</span>

+ log 文件。如果未设置该参数，日志会默认输出到 `"stderr"`；如果设置了该参数，log 会输出到对应的文件中。
+ 默认值：""

### `max-size` <span class="version-mark">从 v5.4.0 版本开始引入</span>

+ 单个 log 文件最大大小，超过设定的参数值后，系统自动切分成多个文件。
+ 默认值：300
+ 最大值：4096
+ 单位：MiB

### `max-days` <span class="version-mark">从 v5.4.0 版本开始引入</span>

+ 保留 log 文件的最长天数。
    + 如果未设置本参数或把此参数设置为默认值 `0`，TiKV 不清理 log 文件。
    + 如果把此参数设置为非 `0` 的值，在 `max-days` 之后，TiKV 会清理过期的日志文件。
+ 默认值：0

### `max-backups` <span class="version-mark">从 v5.4.0 版本开始引入</span>

+ 可保留的 log 文件的最大数量。
    + 如果未设置本参数或把此参数设置为默认值 `0`，TiKV 会保存所有的 log 文件；
    + 如果把此参数设置为非 `0` 的值，TiKV 最多会保留 `max-backups` 中指定的数量的旧日志文件。比如，如果该值设置为 `7`，TiKV 最多会保留 7 个旧的日志文件。
+ 默认值：0

## server

服务器相关的配置项。

### `status-thread-pool-size`

+ HTTP API 服务的工作线程数量。
+ 默认值：1
+ 最小值：1

### `grpc-compression-type`

+ gRPC 消息的压缩算法，取值：none，deflate，gzip。
+ 默认值：none

### `grpc-concurrency`

+ gRPC 工作线程的数量。调整 gRPC 线程池的大小时，请参考 [TiKV 线程池调优](/tune-tikv-thread-performance.md#tikv-线程池调优)。
+ 默认值：5
+ 最小值：1

### `grpc-concurrent-stream`

+ 一个 gRPC 链接中最多允许的并发请求数量。
+ 默认值：1024
+ 最小值：1

### `grpc-memory-pool-quota`

+ gRPC 可使用的内存大小限制。
+ 默认值：无限制
+ 建议仅在出现内存不足 (OOM) 的情况下限制内存使用。需要注意，限制内存使用可能会导致卡顿。

### `grpc-raft-conn-num`

+ TiKV 节点之间用于 Raft 通信的连接最大数量。
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

### `raft-client-queue-size`

+ 该配置项指定 TiKV 中发送 Raft 消息的缓冲区大小。如果存在消息发送不及时导致缓冲区满、消息被丢弃的情况，可以适当调大该配置项值以提升系统运行的稳定性。
+ 默认值：8192

### `simplify-metrics` <span class="version-mark">从 v6.1.1 版本开始引入</span>

+ 是否精简返回的监控指标 Metrics 数据。设置为 `true` 后，TiKV 可以通过过滤部分 Metrics 采样数据以减少每次请求返回的 Metrics 数据量。
+ 默认值：false

### `forward-max-connections-per-address` <span class="version-mark">从 v5.0.0 版本开始引入</span>

+ 设置服务与转发请求的连接池大小。设置过小会影响请求的延迟和负载均衡。
+ 默认值：4

## readpool.unified

统一处理读请求的线程池相关的配置项。该线程池自 4.0 版本起取代原有的 storage 和 coprocessor 线程池。

### `min-thread-count`

+ 统一处理读请求的线程池最少的线程数量。
+ 默认值：1

### `max-thread-count`

+ 统一处理读请求的线程池最多的线程数量，即 UnifyReadPool 线程池的大小。调整该线程池的大小时，请参考 [TiKV 线程池调优](/tune-tikv-thread-performance.md#tikv-线程池调优)。
+ 可调整范围：`[min-thread-count, MAX(4, CPU)]`。其中，`MAX(4, CPU)` 表示：如果 CPU 核心数量小于 `4`，取 `4`；如果 CPU 核心数量大于 `4`，则取 CPU 核心数量。
+ 默认值：MAX(4, CPU * 0.8)

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
+ 当 `8` ≤ `cpu num` ≤ `16` 时，默认值为 `cpu_num * 0.5`；当 `cpu num` 小于 `8` 时，默认值为 `4`；当 `cpu num` 大于 `16` 时，默认值为 `8`。
+ 最小值：`1`

### `normal-concurrency`

+ 处理普通优先级读请求的线程池线程数量。
+ 当 `8` ≤ `cpu num` ≤ `16` 时，默认值为 `cpu_num * 0.5`；当 `cpu num` 小于 `8` 时，默认值为 `4`；当 `cpu num` 大于 `16` 时，默认值为 `8`。
+ 最小值：`1`

### `low-concurrency`

+ 处理低优先级读请求的线程池线程数量。
+ 当 `8` ≤ `cpu num` ≤ `16` 时，默认值为 `cpu_num * 0.5`；当 `cpu num` 小于 `8` 时，默认值为 `4`；当 `cpu num` 大于 `16` 时，默认值为 `8`。
+ 最小值：`1`

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

+ Coprocessor 线程池中线程的栈大小。
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

+ Scheduler 线程池中线程的数量。Scheduler 线程主要负责写入之前的事务一致性检查工作。如果 CPU 核心数量大于等于 16，默认为 8；否则默认为 4。调整 scheduler 线程池的大小时，请参考 [TiKV 线程池调优](/tune-tikv-thread-performance.md#tikv-线程池调优)。
+ 默认值：4
+ 可调整范围：`[1, MAX(4, CPU)]`。其中，`MAX(4, CPU)` 表示：如果 CPU 核心数量小于 `4`，取 `4`；如果 CPU 核心数量大于 `4`，则取 CPU 核心数量。

### `scheduler-pending-write-threshold`

+ 写入数据队列的最大值，超过该值之后对于新的写入 TiKV 会返回 Server Is Busy 错误。
+ 默认值：100MB
+ 单位：MB|GB

### `reserve-space`

+ TiKV 启动时会预留一块空间用于保护磁盘空间。当磁盘剩余空间小于该预留空间时，TiKV 会限制部分写操作。预留空间形式上分为两个部分：预留空间的 80% 用作磁盘空间不足时的运维操作所需要的额外磁盘空间，剩余的 20% 为磁盘临时文件。在回收空间的过程中，如果额外使用的磁盘空间过多，导致存储耗尽时，该临时文件会成为恢复服务的最后一道防御。
+ 临时文件名为 `space_placeholder_file`，位于 `storage.data-dir` 目录下。当 TiKV 因磁盘空间耗尽而下线时，重启 TiKV 会自动删除该临时文件，并自动尝试回收空间。
+ 当剩余空间不足时，TiKV 不会创建该临时文件。防御的有效性与预留空间的大小有关。预留空间大小的计算方式为磁盘容量的 5% 与该配置项之间的最大值。当该配置项的值为 `0MB` 时，TiKV 会关闭磁盘防护功能。
+ 默认值：5GB
+ 单位：MB|GB

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

### `background-error-recovery-window` <span class="version-mark">从 v6.1.0 版本开始引入</span>

+ RocksDB 检测到可恢复的后台错误后，所允许的最长恢复时间。如果后台 SST 文件出现损坏，RocksDB 在检测到故障 SST 文件所属的 Peer 后，会通过心跳上报到 PD。PD 随后会进行调度操作移除该 Peer。最后故障 SST 文件将会被直接删除，随后 TiKV 后台恢复正常。
+ 在恢复操作完成之前，损坏的 SST 文件将一直存在。此时 RocksDB 可以继续写入新的内容，但读到损坏的数据范围时会返回错误。
+ 如果恢复操作未能在该时间窗口内完成，TiKV 会崩溃。
+ 默认值：1h

### `api-version` <span class="version-mark">从 v6.1.0 版本开始引入</span>

+ TiKV 作为 Raw Key Value 存储数据时使用的存储格式与接口版本。
+ 可选值：
    + `1`：使用 API V1。不对客户端传入的数据进行编码，而是原样存储。在 v6.1.0 之前的版本，TiKV 都使用 API V1。
    + `2`：使用 API V2：
        + 数据采用 MVCC（Multi Version Concurrency Control）方式存储，其中时间戳由 tikv-server 从 PD 获取（即 TSO）。
        + 需要同时设置 `storage.enable-ttl = true`。由于 API V2 支持 TTL 特性，因此强制要求打开 `enable-ttl` 以避免这个参数出现歧义。
        + 启用 API V2 后需要在集群中额外部署至少一个 tidb-server 以回收过期数据。注意该 tidb-server 不可提供读写服务。可以部署多个 tidb-server 以保证高可用。
        + 需要客户端的支持。请参考对应客户端的 API V2 使用说明。
+ 默认值：1

> **警告：**
>
> - API V2 是 TiKV 在 v6.1.0 中引入的实验特性，不建议在生产环境中使用。
> - **只能**在部署新的 TiKV 集群时将 `api-version` 的值设置为 `2`，**不能**在已有的 TiKV 集群中修改该配置项的值。由于 API V1 和 API V2 存储的数据格式不相同，如果在已有的 TiKV 集群中修改该配置项，会造成不同格式的数据存储在同一个集群，导致数据损坏。这种情况下，启动 TiKV 集群时会报 "unable to switch storage.api_version" 错误。
> - 启用 API V2 后，**不能**将 TiKV 集群回退到 v6.1.0 之前的版本，否则可能导致数据损坏。

## storage.block-cache

RocksDB 多个 CF 之间共享 block cache 的配置选项。当开启时，为每个 CF 单独配置的 block cache 将无效。

### `shared`

+ 是否开启共享 block cache。
+ 默认值：true

### `capacity`

+ 共享 block cache 的大小。
+ 默认值：系统总内存大小的 45%
+ 单位：KB|MB|GB

## storage.flow-control

在 scheduler 层进行流量控制代替 RocksDB 的 write stall 机制，可以避免 write stall 机制卡住 Raftstore 或 Apply 线程导致的次生问题。本节介绍 TiKV 流量控制机制相关的配置项。

### `enable`

+ 是否开启流量控制机制。开启后，TiKV 会自动关闭 KvDB 的 write stall 机制，还会关闭 RaftDB 中除 memtable 以外的 write stall 机制。
+ 默认值：true

### `memtables-threshold`

+ 当 KvDB 的 memtable 的个数达到该阈值时，流控机制开始工作。当 `enable` 的值为 `true` 时，会覆盖 `rocksdb.(defaultcf|writecf|lockcf).max-write-buffer-number` 的配置。
+ 默认值：5

### `l0-files-threshold`

+ 当 KvDB 的 L0 文件个数达到该阈值时，流控机制开始工作。当 `enable` 的值为 `true` 时，会覆盖 `rocksdb.(defaultcf|writecf|lockcf).level0-slowdown-writes-trigger`的配置。
+ 默认值：20

### `soft-pending-compaction-bytes-limit`

+ 当 KvDB 的 pending compaction bytes 达到该阈值时，流控机制开始拒绝部分写入请求，报错 `ServerIsBusy`。当 `enable` 的值为 `true` 时，会覆盖 `rocksdb.(defaultcf|writecf|lockcf).soft-pending-compaction-bytes-limit` 的配置。
+ 默认值："192GB"

### `hard-pending-compaction-bytes-limit`

+ 当 KvDB 的 pending compaction bytes 达到该阈值时，流控机制拒绝所有写入请求，报错 `ServerIsBusy`。当 `enable` 的值为 `true` 时，会覆盖 `rocksdb.(defaultcf|writecf|lockcf).hard-pending-compaction-bytes-limit` 的配置。
+ 默认值："1024GB"

## storage.io-rate-limit

I/O rate limiter 相关的配置项。

### `max-bytes-per-sec`

+ 限制服务器每秒从磁盘读取数据或写入数据的最大 I/O 字节数，I/O 类型由下面的 `mode` 配置项决定。达到该限制后，TiKV 倾向于放缓后台操作为前台操作节流。该配置项值应设为磁盘的最佳 I/O 带宽，例如云盘厂商指定的最大 I/O 带宽。
+ 默认值："0MB"

### `mode`

+ 确定哪些类型的 I/O 操作被计数并受 `max-bytes-per-sec` 阈值的限流。当前 TiKV 只支持 write-only 只写模式。
+ 可选值：write-only
+ 默认值：write-only

## pd

### `enable-forwarding` <span class="version-mark">从 v5.0.0 版本开始引入</span>

+ 控制 TiKV 中的 PD client 在疑似网络隔离的情况下是否通过 follower 将请求转发给 leader。
+ 默认值：false
+ 如果确认环境存在网络隔离的可能，开启这个参数可以减少服务不可用的窗口期。
+ 如果无法准确判断隔离、网络中断、宕机等情况，这个机制存在误判情况从而导致可用性、性能降低。如果网络中从未发生过网络故障，不推荐开启此选项。

### `endpoints`

+ PD 的地址。当指定多个地址时，需要用逗号 `,` 分隔。
+ 默认值：`["127.0.0.1:2379"]`

### `retry-interval`

+ 设置 PD 连接的重试间隔。
+ 默认值：`"300ms"`

### `retry-log-every`

+ 指定 PD 客户端在观察到错误时跳过报错的频率。例如，当配置项值为 `5` 时，每次 PD 观察到错误时，将跳过 4 次报错，直到第 5 次错误时才报告。
+ 要禁用此功能，请将值设置为 `1`。
+ 默认值：`10`

### `retry-max-count`

+ 初始化 PD 连接的最大重试次数。
+ 要禁用重试，请将该值设置为 `0`。要解除重试次数的限制，请将该值设置为 `-1`。
+ 默认值：`-1`

## raftstore

raftstore 相关的配置项。

### `prevote`

+ 开启 Prevote 的开关，开启有助于减少隔离恢复后对系统造成的抖动。
+ 默认值：true

### `capacity`

+ 存储容量，即允许的最大数据存储大小。如果没有设置，则使用当前磁盘容量。如果要将多个 TiKV 实例部署在同一块物理磁盘上，需要在 TiKV 配置中添加该参数，参见[混合部署的关键参数介绍](/hybrid-deployment-topology.md#混合部署的关键参数介绍)。
+ 默认值：0
+ 单位：KB|MB|GB

### `raftdb-path`

+ raft 库的路径，默认存储在 storage.data-dir/raft 下。
+ 默认值：""

### `raft-base-tick-interval`

> **注意：**
>
> 该配置项不支持通过 SQL 语句查询，但支持在配置文件中进行配置。

+ 状态机 tick 一次的间隔时间。
+ 默认值：1s
+ 最小值：大于 0

### `raft-heartbeat-ticks`

> **注意：**
>
> 该配置项不支持通过 SQL 语句查询，但支持在配置文件中进行配置。

+ 发送心跳时经过的 tick 个数，即每隔 raft-base-tick-interval * raft-heartbeat-ticks 时间发送一次心跳。
+ 默认值：2
+ 最小值：大于 0

### `raft-election-timeout-ticks`

> **注意：**
>
> 该配置项不支持通过 SQL 语句查询，但支持在配置文件中进行配置。

+ 发起选举时经过的 tick 个数，即如果处于无主状态，大约经过 raft-base-tick-interval * raft-election-timeout-ticks 时间以后发起选举。
+ 默认值：10
+ 最小值：raft-heartbeat-ticks

### `raft-min-election-timeout-ticks`

> **注意：**
>
> 该配置项不支持通过 SQL 语句查询，但支持在配置文件中进行配置。

+ 发起选举时至少经过的 tick 个数，如果为 0，则表示使用 raft-election-timeout-ticks，不能比 raft-election-timeout-ticks 小。
+ 默认值：0
+ 最小值：0

### `raft-max-election-timeout-ticks`

> **注意：**
>
> 该配置项不支持通过 SQL 语句查询，但支持在配置文件中进行配置。

+ 发起选举时最多经过的 tick 个数，如果为 0，则表示使用 raft-election-timeout-ticks * 2。
+ 默认值：0
+ 最小值：0

### `raft-max-size-per-msg`

+ 产生的单个消息包的大小限制，软限制。
+ 默认值：1MB
+ 最小值：大于 0
+ 最大值: 3GB
+ 单位：KB|MB|GB

### `raft-max-inflight-msgs`

+ 待确认的日志个数，如果超过这个数量，Raft 状态机会减缓发送日志的速度。
+ 默认值：256
+ 最小值：大于 0
+ 最大值: 16384

### `raft-entry-max-size`

+ 单个日志最大大小，硬限制。
+ 默认值：8MB
+ 最小值：0
+ 单位：MB|GB

### `raft-log-compact-sync-interval` <span class="version-mark">从 v5.3 版本开始引入</span>

+ 压缩非必要 Raft 日志的时间间隔
+ 默认值："2s"
+ 最小值："0s"

### `raft-log-gc-tick-interval`

+ 删除 Raft 日志的轮询任务调度间隔时间，0 表示不启用。
+ 默认值："3s"
+ 最小值："0s"

### `raft-log-gc-threshold`

+ 允许残余的 Raft 日志个数，这是一个软限制。
+ 默认值：50
+ 最小值：1

### `raft-log-gc-count-limit`

+ 允许残余的 Raft 日志个数，这是一个硬限制。默认值为按照每个日志 1MB 而计算出来的 3/4 region 大小所能容纳的日志个数。
+ 最小值：0

### `raft-log-gc-size-limit`

+ 允许残余的 Raft 日志大小，这是一个硬限制，默认为 region 大小的 3/4。
+ 最小值：大于 0

### `raft-log-reserve-max-ticks` <span class="version-mark">从 v5.3 版本开始引入</span>

+ 超过本配置项设置的的 tick 数后，即使剩余 Raft 日志的数量没有达到 `raft-log-gc-threshold` 设置的值，TiKV 也会进行 GC 操作。
+ 默认值：6
+ 最小值：大于 0

### `raft-entry-cache-life-time`

+ 内存中日志 cache 允许的最长残留时间。
+ 默认值：30s
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

### `report-region-buckets-tick-interval` <span class="version-mark">从 v6.1.0 版本开始引入</span>

> **警告：**
>
> `report-region-buckets-tick-interval` 是 TiDB 在 v6.1.0 中引入的实验特性，不建议在生产环境中使用。

+ 启用 `enable-region-bucket` 后，该配置项设置 TiKV 向 PD 上报 bucket 信息的间隔时间。
+ 默认值：10s

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

### `snap-generator-pool-size` <span class="version-mark">从 v5.4.0 版本开始引入</span>

+ 用于配置 `snap-generator` 线程池的大小。
+ 为了让 TiKV 在恢复场景下加快 Region 生成 Snapshot 的速度，需要调大对应 Worker 的 `snap-generator` 线程数量。可通过本配置项调大对应线程的数量。
+ 默认值：`2`
+ 最小值：`1`

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
+ 默认值：10m
+ 最小值：当 Hibernate Region 功能启用时，为 peer-stale-state-check-interval * 2；Hibernate Region 功能关闭时，为 0。

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

### `max-snapshot-file-raw-size` <span class="version-mark">从 v6.1.0 版本开始引入</span>

+ 当 snapshot 文件大于该配置项指定的大小时，snapshot 文件会被切割为多个文件。
+ 默认值：100MiB
+ 最小值：100MiB

### `snap-apply-batch-size`

+ 当导入 snapshot 文件需要写数据时，内存写缓存的大小
+ 默认值：10MB
+ 最小值：0
+ 单位：MB

### `consistency-check-interval`

> **警告：**
>
> 开启一致性检查对集群性能有影响，并且和 TiDB GC 操作不兼容，不建议在生产环境中使用。

+ 触发一致性检查的时间间隔，0 表示不启用。
+ 默认值：0s
+ 最小值：0

### `raft-store-max-leader-lease`

+ region 主可信任期的最长时间。
+ 默认值：9s
+ 最小值：0

### `right-derive-when-split`

+ 指定 Region 分裂时新 Region 的起始 key。当此配置项设置为 `true` 时，起始 key 为最大分裂 key；当此配置项设置为 `false` 时，起始 key 为原 Region 的起始 key。
+ 默认值：true

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

+ Raft 状态机由 BatchSystem 批量执行数据写入请求，该配置项指定每批可执行请求的最多 Raft 状态机个数。
+ 默认值：256
+ 最小值：大于 0
+ 最大值: 10240

### `apply-pool-size`

+ Apply 线程池负责把数据落盘至磁盘。该配置项为 Apply 线程池中线程的数量，即 Apply 线程池的大小。调整 Apply 线程池的大小时，请参考 [TiKV 线程池调优](/tune-tikv-thread-performance.md#tikv-线程池调优)。
+ 默认值：2
+ 可调整范围：[1, CPU * 10]

### `store-max-batch-size`

+ Raft 状态机由 BatchSystem 批量执行把日志落盘至磁盘的请求，该配置项指定每批可执行请求的最多 Raft 状态机个数。
+ 如果开启 `hibernate-regions`，默认值为 256；如果关闭 `hibernate-regions`，默认值为 1024
+ 最小值：大于 0
+ 最大值: 10240

### `store-pool-size`

+ 表示处理 Raft 的线程池中线程的数量，即 Raftstore 线程池的大小。调整该线程池的大小时，请参考 [TiKV 线程池调优](/tune-tikv-thread-performance.md#tikv-线程池调优)。
+ 默认值：2
+ 可调整范围：[1, CPU * 10]

### `store-io-pool-size` <span class="version-mark">从 v5.3.0 版本开始引入</span>

+ 表示处理 Raft I/O 任务的线程池中线程的数量，即 StoreWriter 线程池的大小。调整该线程池的大小时，请参考 [TiKV 线程池调优](/tune-tikv-thread-performance.md#tikv-线程池调优)。
+ 默认值：0
+ 最小值：0

### `future-poll-size`

+ 驱动 future 的线程池中线程的数量。
+ 默认值：1
+ 最小值：大于 0

### `cmd-batch`

+ 对请求进行攒批的控制开关，开启后可显著提升写入性能。
+ 默认值：true

### `inspect-interval`

+ TiKV 每隔一段时间会检测 Raftstore 组件的延迟情况，该配置项设置检测的时间间隔。当检测的延迟超过该时间，该检测会被记为超时。
+ 根据超时的检测延迟的比例计算判断 TiKV 是否为慢节点。
+ 默认值：500ms
+ 最小值：1ms

### `raft-write-size-limit` <span class="version-mark">从 v5.3.0 版本开始引入</span>

+ 触发 Raft 数据写入的阈值。当数据大小超过该配置项值，数据会被写入磁盘。当 `store-io-pool-size` 的值为 `0` 时，该配置项不生效。
+ 默认值：1MB
+ 最小值：0

### `report-min-resolved-ts-interval` <span class="version-mark">从 v6.0.0 版本开始引入</span>

+ 设置 PD leader 收到 Resolved TS 的间隔时间。如果该值设置为 `0`，表示禁用该功能。
+ 默认值：`"0s"`
+ 最小值：0
+ 单位：秒

## coprocessor

coprocessor 相关的配置项。

### `split-region-on-table`

+ 开启按 table 分裂 Region 的开关，建议仅在 TiDB 模式下使用。
+ 默认值：false

### `batch-split-limit`

+ 批量分裂 Region 的阈值，调大该值可加速分裂 Region。
+ 默认值：10
+ 最小值：1

### `region-max-size`

+ Region 容量空间最大值，超过时系统分裂成多个 Region。
+ 默认值：`region-split-size / 2 * 3`
+ 单位：KiB|MiB|GiB

### `region-split-size`

+ 分裂后新 Region 的大小，此值属于估算值。
+ 默认值：96MiB
+ 单位：KiB|MiB|GiB

### `region-max-keys`

+ Region 最多允许的 key 的个数，超过时系统分裂成多个 Region。
+ 默认值：`region-split-keys / 2 * 3`

### `region-split-keys`

+ 分裂后新 Region 的 key 的个数，此值属于估算值。
+ 默认值：960000

### `enable-region-bucket` <span class="version-mark">从 v6.1.0 版本开始引入</span>

+ 是否将 Region 划分为更小的区间 bucket，并且以 bucket 作为并发查询单位，以提高扫描数据的并发度。bucket 的详细设计可见 [Dynamic size Region](https://github.com/tikv/rfcs/blob/master/text/0082-dynamic-size-region.md)。
+ 默认值：false

> **警告：**
>
> - `enable-region-bucket` 是 TiDB 在 v6.1.0 中引入的实验特性，不建议在生产环境中使用。
> - 这个参数仅在 `region-split-size` 调到两倍 `region-bucket-size` 及以上时才有意义，否则不会真正生成 bucket。
> - 将 `region-split-size` 调大可能会有潜在的性能回退、数据调度缓慢的风险。

### `region-bucket-size` <span class="version-mark">从 v6.1.0 版本开始引入</span>

+ 设置 `enable-region-bucket` 启用时 bucket 的预期大小。
+ 默认值：96MiB

> **警告：**
>
> `region-bucket-size` 是 TiDB 在 v6.1.0 中引入的实验特性，不建议在生产环境中使用。

## rocksdb

rocksdb 相关的配置项。

### `max-background-jobs`

+ RocksDB 后台线程个数。调整 RocksDB 线程池的大小时，请参考 [TiKV 线程池调优](/tune-tikv-thread-performance.md#tikv-线程池调优)。
+ 默认值：
    + CPU 核数为 10 时，默认值为 `9`
    + CPU 核数为 8 时，默认值为 `7`
    + CPU 核数为 `N` 时，默认值为 `max(2, min(N - 1, 9))`
+ 最小值：2

### `max-background-flushes`

+ RocksDB 用于刷写 memtable 的最大后台线程数量。
+ 默认值：
    + CPU 核数为 10 时，默认值为 `3`
    + CPU 核数为 8 时，默认值为 `2`
    + CPU 核数为 `N` 时，默认值为 `[(max-background-jobs + 3) / 4]`
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

+ 预写式日志 (WAL, Write Ahead Log) 的恢复模式。
+ 可选值：
    + `"tolerate-corrupted-tail-records"`：容忍并丢弃位于日志尾部的不完整的数据 (trailing data)。
    + `"absolute-consistency"`：当发现待恢复的日志中有被损坏的日志时，放弃恢复所有日志。
    + `"point-in-time"`：按顺序恢复日志。遇到第一个损坏的日志时，停止恢复剩余的日志。
    + `"skip-any-corrupted-records"`：灾难后恢复。跳过日志中的损坏记录，尽可能多地恢复数据。
+ 默认值：`"point-in-time"`

### `wal-dir`

+ WAL 存储目录，若未指定，WAL 将存储在数据目录。
+ 默认值：`""`

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

+ 开启 RocksDB compaction 过程中的预读功能，该项指定预读数据的大小。如果使用的是机械磁盘，建议该值至少为 2MB。
+ 默认值：0
+ 最小值：0
+ 单位：B|KB|MB|GB

### `writable-file-max-buffer-size`

+ WritableFileWrite 所使用的最大的 buffer 大小。
+ 默认值：1MB
+ 最小值：0
+ 单位：B|KB|MB|GB

### `use-direct-io-for-flush-and-compaction`

+ 决定后台 flush 或者 compaction 的读写是否设置 O_DIRECT 的标志。该选项对性能的影响：开启 O_DIRECT 可以绕过并防止污染操作系统 buffer cache，但后续文件读取需要把内容重新读到 buffer cache。
+ 默认值：false

### `rate-bytes-per-sec`

+ RocksDB compaction rate limiter 的限制速率。
+ 默认值：10GB
+ 最小值：0
+ 单位：B|KB|MB|GB

### `rate-limiter-mode`

+ RocksDB 的 compaction rate limiter 模式。
+ 可选值："read-only"，"write-only"，"all-io"
+ 默认值："write-only"

### `rate-limiter-auto-tuned` <span class="version-mark">从 v5.0 版本开始引入</span>

+ 控制是否依据最近的负载量自动优化 RocksDB 的 compaction rate limiter 配置。此配置项开启后，compaction pending bytes 监控指标值会比一般情况下稍微高些。
+ 默认值：true

### `enable-pipelined-write`

+ 控制是否开启 Pipelined Write。开启时会使用旧的 Pipelined Write，关闭时会使用新的 Pipelined Commit 机制。
+ 默认值：false

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

> **警告：**
>
> 自 v5.4.0 起，RocksDB 的日志改为由 TiKV 的日志模块进行管理，因此该配置项被废弃，其功能由配置参数 [`log.file.max-size`](#max-size-从-v540-版本开始引入) 代替。

+ Info 日志的最大大小。
+ 默认值：1GB
+ 最小值：0
+ 单位：B|KB|MB|GB

### `info-log-roll-time`

> **警告：**
>
> 自 v5.4.0 起，RocksDB 的日志改为由 TiKV 的日志模块进行管理，因此该配置项被废弃。TiKV 不再支持按照时间自动切分日志，请使用配置参数 [`log.file.max-size`](#max-size-从-v540-版本开始引入) 配置按照文件大小自动切分日志的阈值。

+ 日志截断间隔时间，如果为 0s 则不截断。
+ 默认值：0s

### `info-log-keep-log-file-num`

> **警告：**
>
> 自 v5.4.0 起，RocksDB 的日志改为由 TiKV 的日志模块进行管理，因此该配置项被废弃，其功能由配置参数 [`log.file.max-backups`](#max-backups-从-v540-版本开始引入) 代替。

+ 保留日志文件最大个数。
+ 默认值：10
+ 最小值：0

### `info-log-dir`

+ 日志存储目录。
+ 默认值：""

### `info-log-level`

> **警告：**
>
> 自 v5.4.0 起，RocksDB 的日志改为由 TiKV 的日志模块进行管理，因此该配置项被废弃，其功能由配置参数 [`log.level`](#level-从-v540-版本开始引入) 代替。

+ RocksDB 的日志级别。
+ 默认值：`"info"`

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

+ 控制第 0 层 SST 文件的 index block 和 filter block 是否常驻在内存中的开关。
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

+ 最大 memtable 个数。当 `storage.flow-control.enable` 的值为 `true` 时，`storage.flow-control.memtables-threshold` 会覆盖此配置。
+ 默认值：5
+ 最小值：0

### `min-write-buffer-number-to-merge`

+ 触发 flush 的最小 memtable 个数。
+ 默认值：1
+ 最小值：0

### `max-bytes-for-level-base`

+ base level (L1) 最大字节数，一般设置为 memtable 大小 4 倍。当 L1 的数据量大小达到 `max-bytes-for-level-base` 限定的值的时候，会触发 L1 的 SST 文件和 L2 中有 overlap 的 SST 文件进行 compaction。
+ `defaultcf` 默认值：`"512MB"`
+ `writecf` 默认值：`"512MB"`
+ `lockcf` 默认值：`"128MB"`
+ 最小值：0
+ 单位：KB|MB|GB
+ 建议 `max-bytes-for-level-base` 的取值和 L0 的数据量大致相等，以减少不必要的 compaction。假如压缩方式为 "no:no:lz4:lz4:lz4:lz4:lz4"，那么 `max-bytes-for-level-base` 的值应该是 `write-buffer-size * 4`，因为 L0 和 L1 均没有压缩，且 L0 触发 compaction 的条件是 SST 文件的个数到达 4（默认值）。当 L0 和 L1 都发生了 compaction 时，需要分析 RocksDB 的日志了解由一个 memtable 压缩成的 SST 文件的大小。如果文件大小为 32MB，那么 `max-bytes-for-level-base` 的值建议设为 32MB * 4 = 128MB。

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

+ 触发 write stall 的 L0 文件最大个数。当 `storage.flow-control.enable` 的值为 `true` 时，`storage.flow-control.l0-files-threshold` 会覆盖此配置。
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

+ 优先处理 compaction 的类型
+ 可选值：
    + `"by-compensated-size"`：根据大小顺序，优先对大文件进行 compaction。
    + `"oldest-largest-seq-first"`：根据时间顺序，优先对数据更新时间晚的文件进行 compaction。当你只在小范围内更新部分热点键 (hot keys) 时，可以使用此配置。
    + `"oldest-smallest-seq-first"`：根据时间顺序，优先对长时间没有被 compact 到下一级的文件进行 compaction。如果你在大范围内随机更新了部分热点键，使用该配置可以轻微缓解写放大。
    + `"min-overlapping-ratio"`：根据重叠比例，优先对在不同层之间文件重叠比例高的文件进行 compaction，即一个文件在 `下一层的大小`/`本层的大小` 的值越小，compaction 的优先级越高。在诸多场景下，该配置可以有效缓解写放大。
+ 默认值：
    + `defaultcf` 和 `writecf` 的默认值：`"min-overlapping-ratio"`
    + `lockcf` 的默认值：`"by-compensated-size"`

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

+ compaction 方法。
+ 可选值："level"，"universal"，"fifo"
+ 默认值："level"

### `disable-auto-compactions`

+ 是否关闭自动 compaction。
+ 默认值：false

### `soft-pending-compaction-bytes-limit`

+ pending compaction bytes 的软限制。当 `storage.flow-control.enable` 的值为 `true` 时，`storage.flow-control.soft-pending-compaction-bytes-limit` 会覆盖此配置。
+ 默认值：192GB
+ 单位：KB|MB|GB

### `hard-pending-compaction-bytes-limit`

+ pending compaction bytes 的硬限制。当 `storage.flow-control.enable` 的值为 `true` 时，`storage.flow-control.hard-pending-compaction-bytes-limit` 会覆盖此配置。
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

+ Blob 文件的 cache 大小。
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

## raftdb

raftdb 相关配置项。

### `max-background-jobs`

+ RocksDB 后台线程个数。调整 RocksDB 线程池的大小时，请参考 [TiKV 线程池调优](/tune-tikv-thread-performance.md#tikv-线程池调优)。
+ 默认值：4
+ 最小值：2

### `max-sub-compactions`

+ RocksDB 进行 subcompaction 的并发数。
+ 默认值：2
+ 最小值：1

### `wal-dir`

+ WAL 存储目录。
+ 默认值：/tmp/tikv/store

## raft-engine

Raft Engine 相关的配置项。

> **注意：**
>
> - 第一次开启 Raft Engine 时，TiKV 会将原有的 RocksDB 数据转移至 Raft Engine 中。因此，TiKV 的启动时间会比较长，你需要额外等待几十秒。
> - 如果你要将 TiDB 集群降级至 v5.4.0 以前的版本（不含 v5.4.0），你需要在降级**之前**先关闭 Raft Engine（即把 `enable` 配置项设置为 `false`，并重启 TiKV 使配置生效），否则会导致集群降级后无法正常开启。

### `enable`

+ 决定是否使用 Raft Engine 来存储 Raft 日志。开启该配置项后，`raftdb` 的配置不再生效
+ 默认值：`true`

### `dir`

+ 存储 Raft 日志文件的目录。如果该目录不存在，则在启动 TiKV 时创建该目录。
+ 如果未设置此配置，则使用 `{data-dir}/raft-engine`。
+ 如果你的机器上有多个磁盘，建议将 Raft Engine 的数据存储在单独的磁盘上，以提高 TiKV 性能。
+ 默认值：`""`

### `batch-compression-threshold`

+ 指定日志批处理的阈值大小。大于此配置的日志批次将被压缩。如果将此配置项设置为 `0`，则禁用压缩。
+ 默认值：`"8KB"`

### `bytes-per-sync`

+ 指定缓存写入的最大累积大小。当超过此配置值时，缓存的写入将被刷写到磁盘。
+ 如果将此配置项设置为 `0`，则禁用增量同步。
+ 默认值：`"4MB"`

### `target-file-size`

+ 指定日志文件的最大大小。当日志文件大于此值时，将对其进行轮转。
+ 默认值：`"128MB"`

### `purge-threshold`

+ 指定主日志队列的阈值大小。当超过此配置值时，将对主日志队列执行垃圾回收。
+ 此参数可用于调整 Raft Engine 的空间占用大小。
+ 默认值：`"10GB"`

### `recovery-mode`

+ 确定在日志恢复过程中如何处理文件损坏。
+ 可选值：`"absolute-consistency"`, `"tolerate-tail-corruption"`, `"tolerate-any-corruption"`
+ 默认值：`"tolerate-tail-corruption"`

### `recovery-read-block-size`

+ 恢复期间读取日志文件的最小 I/O 大小。
+ 默认值：`"16KB"`
+ 最小值：`"512B"`

### `recovery-threads`

+ 用于扫描和恢复日志文件的线程数。
+ 默认值：`4`
+ 最小值：`1`

### `memory-limit`

+ 指定 Raft Engine 使用内存的上限。
+ 当该配置项未设置时，Raft Engine 默认使用系统总内存的 15%。
+ 默认值：`系统总内存 * 15%`

## security

安全相关配置项。

### `ca-path`

+ CA 文件路径
+ 默认值：""

### `cert-path`

+ 包含 X.509 证书的 PEM 文件路径
+ 默认值：""

### `key-path`

+ 包含 X.509 key 的 PEM 文件路径
+ 默认值：""

### `cert-allowed-cn`

+ 客户端提供的证书中，可接受的 X.509 通用名称列表。仅当提供的通用名称与列表中的条目之一完全匹配时，才会允许其请求。
+ 默认值：`[]`。这意味着默认情况下禁用客户端证书 CN 检查。

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

+ 处理 RPC 请求的线程数量。
+ 默认值：8
+ 最小值：1

## gc

### `enable-compaction-filter` <span class="version-mark">从 v5.0 版本开始引入</span>

+ 是否开启 GC in Compaction Filter 特性
+ 默认值：true

## backup

用于 BR 备份相关的配置项。

### `num-threads`

+ 处理备份的工作线程数量。
+ 默认值：CPU * 0.5，但最大为 8
+ 可调整范围：[1, CPU]
+ 最小值：1

### `enable-auto-tune` <span class="version-mark">从 v5.4 版本开始引入</span>

+ 在集群资源占用率较高的情况下，是否允许 BR 自动限制备份使用的资源，减少对集群的影响。详情见[自动调节](/br/br-auto-tune.md)。
+ 默认值：true

### `s3-multi-part-size` <span class="version-mark">从 v5.3.2 版本开始引入</span>

> **注意：**
>
> 引入该配置项是为了解决备份期间遇到的 S3 限流导致备份失败的问题。该问题已通过[优化 BR 备份数据存储的目录结构](/br/backup-and-restore-design.md#备份文件布局)得到解决。因此，该配置项自 v6.1.1 起开始废弃，不再推荐使用。

+ 备份阶段 S3 分块上传的块大小。可通过调整该参数来控制备份时发往 S3 的请求数量。
+ TiKV 备份数据到 S3 时，如果备份文件大于该配置项的值，会自动进行[分块上传](https://docs.aws.amazon.com/zh_cn/AmazonS3/latest/API/API_UploadPart.html)。根据压缩率的不同，96 MiB Region 产生的备份文件大约在 10 MiB~30 MiB 之间。
+ 默认值：5MiB

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

### `in-memory` <span class="version-mark">从 v6.0.0 版本开始引入</span>

+ 开启内存悲观锁功能。开启该功能后，悲观事务会尽可能在 TiKV 内存中存储悲观锁，而不将悲观锁写入磁盘，也不将悲观锁同步给其他副本，从而提升悲观事务的性能。但有较低概率出现悲观锁丢失的情况，可能会导致悲观事务提交失败。
+ 默认值：true
+ 注意：`in-memory` 仅在 `pipelined` 为 true 时生效。

## quota

用于前台限流 (Quota Limiter) 相关的配置项。

当 TiKV 部署的机型资源有限（如 4v CPU，16 G 内存）时，如果 TiKV 前台处理的读写请求量过大，以至于占用 TiKV 后台处理请求所需的 CPU 资源，最终影响 TiKV 性能的稳定性。此时，你可以使用前台限流相关的 quota 配置项以限制前台各类请求占用的 CPU 资源。触发该限制的请求会被强制等待一段时间以让出 CPU 资源。具体等待时间与新增请求量相关，最多不超过 [`max-delay-duration`](#max-delay-duration从-v600-版本开始引入) 的值。

> **警告：**
>
> - 前台限流是 TiDB 在 v6.0.0 中引入的实验特性，不建议在生产环境中使用。
> - 该功能仅适合在资源有限的环境中使用，以保证 TiKV 在该环境下可以长期稳定地运行。如果在资源丰富的机型环境中开启该功能，可能会导致读写请求量达到峰值时 TiKV 的性能下降的问题。

### `foreground-cpu-time`（从 v6.0.0 版本开始引入）

+ 限制处理 TiKV 前台读写请求所使用的 CPU 资源使用量，这是一个软限制。
+ 默认值：0（即无限制）
+ 单位：millicpu （当该参数值为 `1500` 时，前端请求会消耗 1.5v CPU）。

### `foreground-write-bandwidth`（从 v6.0.0 版本开始引入）

+ 限制事务写入的带宽，这是一个软限制。
+ 默认值：0KB（即无限制）

### `foreground-read-bandwidth`（从 v6.0.0 版本开始引入）

+ 限制事务读取数据和 Coprocessor 读取数据的带宽，这是一个软限制。
+ 默认值：0KB（即无限制）

### `max-delay-duration`（从 v6.0.0 版本开始引入）

+ 单次前台读写请求被强制等待的最大时间。
+ 默认值：500ms

## causal-ts <span class="version-mark">从 v6.1.0 版本开始引入</span>

用于 TiKV API V2（`storage.api-version = 2`）中时间戳获取相关的配置项。

为了降低写请求延迟，TiKV 会定期获取一批时间戳缓存在本地，避免频繁访问 PD。当本地缓存的时间戳用完，会立即发起一次时间戳请求。这种情况下，部分写请求的延迟会增大。TiKV 会根据负载情况动态调整时间戳缓存的大小，以减少这种情况的发生，大部分情况下不需要做参数调整。

> **警告：**
>
> - API V2 是 TiKV 在 v6.1.0 中引入的实验特性，不建议在生产环境中使用。

### `renew-interval`

+ 刷新本地缓存时间戳的周期。
+ TiKV 会每隔 `renew-interval` 发起一次时间戳更新，并根据前一周期的使用情况，来调整时间戳的缓存数量。这个参数配置过大会导致不能及时反映最新的 TiKV 负载变化。而配置过小则会增加 PD 的负载。如果写流量剧烈变化、频繁出现时间戳耗尽、写延迟增加，可以适当调小这个参数，但需要同时关注 PD 的负载情况。
+ 默认值：100ms

### `renew-batch-min-size`

+ 时间戳缓存的最小数量。
+ TiKV 会根据前一周期的使用情况，来调整时间戳的缓存数量。如果本地缓存使用率偏低，TiKV 会逐步降低缓存数量，直至等于 `renew-batch-min-size`。如果业务中经常出现突发的大流量写入，可以适当调大这个参数。注意这个参数是单个 tikv-server 的缓存大小，如果配置过大、而同时集群中 tikv-server 较多，会导致 TSO 消耗过快。
+ Grafana **TiKV-Raw** 面板下 **Causal timestamp** 中的 **TSO batch size** 是根据业务负载动态调整后的本地缓存数量。可以参考该监控指标值调整这个参数的大小。
+ 默认值：100
