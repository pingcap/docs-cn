---
title: TiKV 监控指标详解
category: reference
aliases: ['/docs-cn/dev/reference/key-monitoring-metrics/tikv-dashboard/']
---

# TiKV 监控指标详解

使用 TiUP 部署 TiDB 集群时，可以一键部署监控系统 (Prometheus/Grafana)，监控架构请看 [TiDB 监控框架概述](/tidb-monitoring-framework.md)。

目前默认的 Grafana Dashboard 整体分为 PD、TiDB、TiKV、Node_exporter、Overview 等。

对于日常运维，我们通过观察 **TiKV-Details** 面板上的指标，可以了解 TiKV 当前的状态。根据 [性能地图](https://asktug.com/_/tidb-performance-map/#/) 可以检查集群的状态是否符合预期。

以下为 **TiKV-Details** 默认的监控信息：

## Cluster

- Store size：每个 TiKV 实例的使用的存储空间的大小
- Available size：每个 TiKV 实例的可用的存储空间的大小
- Capacity size：每个 TiKV 实例的存储容量的大小
- CPU：每个 TiKV 实例 CPU 的使用率
- Memory：每个 TiKV 实例内存的使用情况
- IO utilization：每个 TiKV 实例 IO 的使用率
- MBps：每个 TiKV 实例写入和读取的数据量大小
- QPS：每个 TiKV 实例上各种命令的 QPS
- Errps：每个 TiKV 实例上 gRPC 消息失败的个数
- leader：每个 TiKV 实例 leader 的个数
- Region：每个 TiKV 实例 Region 的个数
- Uptime：自上次重启以来 TiKV 正常运行的时间

![TiKV Dashboard - Cluster metrics](/media/tikv-dashboard-cluster.png)

## Errors

- Critical error：严重错误的数量
- Server is busy：各种会导致 TiKV 实例暂时不可用的事件个数，如 write stall，channel full 等，正常情况下应当为 0
- Server report failures：server 报错的消息个数，正常情况下应当为 0
- Raftstore error：每个 TiKV 实例上 raftstore 发生错误的个数
- Scheduler error：每个 TiKV 实例上 scheduler 发生错误的个数
- Coprocessor error：每个 TiKV 实例上 coprocessor 发生错误的个数
- gRPC message error：每个 TiKV 实例上 gRPC 消息发生错误的个数
- Leader drop：每个 TiKV 实例上 drop leader 的个数
- Leader missing：每个 TiKV 实例上 missing leader 的个数

![TiKV Dashboard - Errors metrics](/media/tikv-dashboard-errors.png)

## Server

- CF size：每个列族的大小
- Store size：每个 TiKV 实例的使用的存储空间的大小
- Channel full：每个 TiKV 实例上 channel full 错误的数量，正常情况下应当为 0
- Active written leaders：各个 TiKV 实例中正在被写入的 Leader 的数量
- Approximate Region size：每个 Region 近似的大小
- Approximate Region size Histogram：每个 Region 近似大小的直方图
- Region average written keys：每个 TiKV 实例上所有 Region 的平均 key 写入个数
- Region average written bytes：每个 TiKV 实例上所有 Region 的平均写入大小
- Request batch ratio：每个 TiKV 实例的 request batch 输出和输入的比率
- Request batch input：每个 TiKV 实例的 request batch 中的请求大小

![TiKV Dashboard - Server metrics](/media/tikv-dashboard-server.png)

## gRPC

- gRPC message count：每种 gRPC 消息的个数
- gRPC message failed：失败的 gRPC 消息的个数
- 99% gRPC message duration：在 99% gRPC 消息的执行时间
- Average gRPC message duration：gRPC 消息平均的执行时间
- gRPC batch size：gRPC 请求的 batch 大小
- raft message batch size：raft 消息的 batch 大小

## Thread CPU

- Raft store CPU：raftstore 线程的 CPU 使用率，通常应低于 80%
- Async apply CPU：async apply 线程的 CPU 使用率，通常应低于 90%
- Scheduler worker CPU：scheduler worker 线程的 CPU 使用率
- gRPC poll CPU：gRPC 线程的 CPU 使用率，通常应低于 80%
- Unified read pool CPU：unified read pool 线程的 CPU 使用率
- Storage ReadPool CPU：storage read pool 线程的 CPU 使用率
- Coprocessor CPU：coprocessor 线程的 CPU 使用率
- RocksDB CPU：RocksDB 线程的 CPU 使用率
- Split check CPU：split check 线程的 CPU 使用率
- GC worker CPU：GC worker 线程的 CPU 使用率
- Snapshot worker CPU：snapshot worker 线程的 CPU 使用率

## PD

- PD requests：TiKV 发送给 PD 的请求个数
- PD request duration (average)：TiKV 发送给 PD 的请求所需的平均时间
- PD heartbeats：发送给 PD 的心跳个数
- PD validate peers：通过 PD 验证 TiKV 的 peer 有效的个数

## Raft IO

- Apply log duration：Raft apply 日志所花费的时间
- Apply log duration per server：每个 TiKV 实例上 Raft apply 日志所花费的时间
- Append log duration：Raft append 日志所花费的时间
- Append log duration per server：每个 TiKV 实例上 Raft append 日志所花费的时间
- Commit log duration：Raft commit 日志所花费的时间
- Commit log duration per server：每个 TiKV 实例上 Raft commit 日志所花费的时间

![TiKV Dashboard - Raft IO metrics](/media/tikv-dashboard-raftio.png)

## Raft process

- Ready handled：Raft 中不同 ready 类型的个数
- 0.99 Duration of Raft store events：99% 的 raftstore 事件所花费的时间
- Process ready duration：处理 ready 所花费的时间
- Process ready duration per server：每个 TiKV 实例处理 ready 所花费的时间，99.99% 的情况下，应该小于 2s

![TiKV Dashboard - Raft process metrics](/media/tikv-dashboard-raft-process.png)

## Raft message

- Sent messages per server：每个 TiKV 实例发送 Raft 消息的个数
- Flush messages per server：每个 TiKV 实例持久化 Raft 消息的个数
- Receive messages per server：每个 TiKV 实例接受 Raft 消息的个数
- Messages：发送不同类型的 Raft 消息的个数
- Vote：Raft 投票消息发送的个数
- Raft dropped messages：丢弃不同类型的 Raft 消息的个数

![TiKV Dashboard - Raft message metrics](/media/tikv-dashboard-raft-message.png)

## Raft propose

- Raft proposals per ready：在一个 tick 内，所有 Region proposal 的个数
- Raft read/write proposals：不同类型的 proposal 的个数
- Raft read proposals per server：每个 TiKV 实例发起读 proposal 的个数
- Raft write proposals per server：每个 TiKV 实例发起写 proposal 的个数
- Propose wait duration：每个 proposal 的等待时间
- Propose wait duration per server：每个 TiKV 实例上每个 proposal 的等待时间
- Apply wait duration：每个 apply 的等待时间
- Apply wait duration per server：每个 TiKV 实例上每个 apply 的等待时间
- Raft log speed：peer propose 日志的速度

![TiKV Dashboard - Raft propose metrics](/media/tikv-dashboard-raft-propose.png)

## Raft admin

- Admin proposals：admin proposal 的个数
- Admin apply：apply 命令的个数
- Check split：split check 命令的个数
- 99.99% Check split duration：99.99% 的情况下，split check 所需花费的时间

![TiKV Dashboard - Raft admin metrics](/media/tikv-dashboard-raft-admin.png)

## Local reader

- Local reader requests：所有请求的总数以及 local read 线程拒绝的请求数量

![TiKV Dashboard - Local reader metrics](/media/tikv-dashboard-local-reader.png)

## Unified Read Pool

- Time used by level：在 unified read pool 中每个级别使用的时间，级别 0 指小查询
- Level 0 chance：在 unified read pool 中调度的 level 0 任务的比例
- Running tasks：在 unified read pool 中并发运行的任务数量

## Storage

- Storage command total：收到不同命令的个数
- Storage async request error：异步请求出错的个数
- Storage async snapshot duration：异步处理 snapshot 所花费的时间，99% 的情况下，应该小于 1s
- Storage async write duration：异步写所花费的时间，99% 的情况下，应该小于 1s

![TiKV Dashboard - Storage metrics](/media/tikv-dashboard-storage.png)

## Scheduler

- Scheduler stage total：每种命令不同阶段的个数，正常情况下，不会在短时间内出现大量的错误
- Scheduler writing bytes：在每个 stage 中命令的总写入字节数量
- Scheduler priority commands：不同优先级命令的个数
- Scheduler pending commands：每个 TiKV 实例上 pending 命令的个数

![TiKV Dashboard - Scheduler metrics](/media/tikv-dashboard-scheduler.png)

## Scheduler - commit

- Scheduler stage total：commit 中每个命令所处不同阶段的个数，正常情况下，不会在短时间内出现大量的错误
- Scheduler command duration：执行 commit 命令所需花费的时间，正常情况下，应该小于 1s
- Scheduler latch wait duration：由于 latch wait 造成的时间开销，正常情况下，应该小于 1s
- Scheduler keys read：commit 命令读取 key 的个数
- Scheduler keys written：commit 命令写入 key 的个数
- Scheduler scan details：执行 commit 命令时，扫描每个 CF 中 key 的详细情况
- Scheduler scan details [lock]：执行 commit 命令时，扫描每个 lock CF 中 key 的详细情况
- Scheduler scan details [write]：执行 commit 命令时，扫描每个 write CF 中 key 的详细情况
- Scheduler scan details [default]：执行 commit 命令时，扫描每个 default CF 中 key 的详细情况

![TiKV Dashboard - Scheduler commit metrics](/media/tikv-dashboard-scheduler-commit.png)

## Scheduler - pessimistic_rollback

- Scheduler stage total：pessimistic_rollback 中每个命令所处不同阶段的个数，正常情况下，不会在短时间内出现大量的错误
- Scheduler command duration：执行 pessimistic_rollback 命令所需花费的时间，正常情况下，应该小于 1s
- Scheduler latch wait duration：由于 latch wait 造成的时间开销，正常情况下，应该小于 1s
- Scheduler keys read：pessimistic_rollback 命令读取 key 的个数
- Scheduler keys written：pessimistic_rollback 命令写入 key 的个数
- Scheduler scan details：执行 pessimistic_rollback 命令时，扫描每个 CF 中 key 的详细情况
- Scheduler scan details [lock]：执行 pessimistic_rollback 命令时，扫描每个 lock CF 中 key 的详细情况
- Scheduler scan details [write]：执行 pessimistic_rollback 命令时，扫描每个 write CF 中 key 的详细情况
- Scheduler scan details [default]：执行 pessimistic_rollback 命令时，扫描每个 default CF 中 key 的详细情况

## Scheduler - prewrite

- Scheduler stage total：prewrite 中每个命令所处不同阶段的个数，正常情况下，不会在短时间内出现大量的错误
- Scheduler command duration：执行 prewrite 命令所需花费的时间，正常情况下，应该小于 1s
- Scheduler latch wait duration：由于 latch wait 造成的时间开销，正常情况下，应该小于 1s
- Scheduler keys read：prewrite 命令读取 key 的个数
- Scheduler keys written：prewrite 命令写入 key 的个数
- Scheduler scan details：执行 prewrite 命令时，扫描每个 CF 中 key 的详细情况
- Scheduler scan details [lock]：执行 prewrite 命令时，扫描每个 lock CF 中 key 的详细情况
- Scheduler scan details [write]：执行 prewrite 命令时，扫描每个 write CF 中 key 的详细情况
- Scheduler scan details [default]：执行 prewrite 命令时，扫描每个 default CF 中 key 的详细情况

## Scheduler - rollback

- Scheduler stage total：rollback 中每个命令所处不同阶段的个数，正常情况下，不会在短时间内出现大量的错误
- Scheduler command duration：执行 rollback 命令所需花费的时间，正常情况下，应该小于 1s
- Scheduler latch wait duration：由于 latch wait 造成的时间开销，正常情况下，应该小于 1s
- Scheduler keys read：rollback 命令读取 key 的个数
- Scheduler keys written：rollback 命令写入 key 的个数
- Scheduler scan details：执行 rollback 命令时，扫描每个 CF 中 key 的详细情况
- Scheduler scan details [lock]：执行 rollback 命令时，扫描每个 lock CF 中 key 的详细情况
- Scheduler scan details [write]：执行 rollback 命令时，扫描每个 write CF 中 key 的详细情况
- Scheduler scan details [default]：执行 rollback 命令时，扫描每个 default CF 中 key 的详细情况

## GC

- MVCC versions：每个 key 的版本个数
- MVCC delete versions：GC 删除掉的每个 key 的版本个数
- GC tasks：由 gc_worker 处理的 GC 任务的个数
- GC tasks Duration：执行 GC 任务时所花费的时间
- GC keys (write CF)：在 GC 过程中，write CF 中 受影响的 key 的个数
- TiDB GC worker actions：TiDB GC worker 的不同 action 的个数
- TiDB GC seconds：TiDB 执行 GC 花费的时间
- GC speed：GC 每秒进行的 key 的数量
- TiKV AutoGC Working：Auto GC 管理器的工作状态
- ResolveLocks Progress：GC 第一阶段即 ResolveLocks 的进度
- TiKV Auto GC Progress：TiKV GC 的进度
- TiKV Auto GC SafePoint：TiKV GC 的 safe point 的数值
- GC lifetime：TiDB 设置的 GC lifetime
- GC interval：TiDB 设置的 GC 间隔

## Snapshot

- Rate snapshot message：发送 Raft snapshot 消息的速率
- 99% Handle snapshot duration：99% 的情况下，处理 snapshot 所需花费的时间
- Snapshot state count：不同状态的 snapshot 的个数
- 99.99% Snapshot size：99.99% 的 snapshot 的大小
- 99.99% Snapshot KV count：99.99% 的 snapshot 包含的 key 的个数

## Task

- Worker handled tasks：worker 处理的任务个数
- Worker pending tasks：当前 worker 中，pending 和 running 的任务个数，正常情况下，应该小于 1000
- FuturePool handled tasks：future pool 处理的任务个数
- FuturePool pending tasks：当前 future pool 中，pending 和 running 的任务个数

## Coprocessor Overview

- Request duration：处理 coprocessor 读请求所花费的时间
- Total Requests：对于每种类型的总请求数量
- Handle duration：处理 coprocessor 请求所花费的时间
- Total Request Errors：下推的请求发生错误的个数，正常情况下，短时间内不应该有大量的错误
- Total KV Cursor Operations：各种类型的 KV cursor 操作的总数量
- KV Cursor Operations：各种类型的 KV cursor 操作的数量
- Total RocksDB Perf Statistics：RocksDB 性能统计数据
- Total Response Size：coprocessor 回应的数据大小

## Coprocessor Detail

- Handle duration：处理 coprocessor 请求所花费的时间
- 95% Handle duration by store：95% 的情况下，每个 TiKV 实例处理 coprocessor 请求所花费的时间
- Wait duration：coprocessor 请求的等待时间，99.99% 的情况下，应该小于 10s
- 95% Wait duration by store：95% 的情况下，每个 TiKV 实例上 coprocessor 请求的等待时间
- Total DAG Requests：DAG 请求的总数量
- Total DAG executors：DAG executor 的总数量
- Total Ops Details (Table Scan)：coprocessor 中请求为 select 的 scan 情况
- Total Ops Details (Index Scan)：coprocessor 中请求为 index 的 scan 情况
- Total Ops Details by CF (Table Scan)：coprocessor 中对于每个 CF 请求为 select 的 scan 情况
- Total Ops Details by CF (Index Scan)：coprocessor 中对于每个 CF 请求为 index 的 scan 情况

## Threads

- Threads state：TiKV 线程的状态
- Threads IO：TiKV 各个线程的 I/O 使用量
- Thread Voluntary Context Switches：TiKV 线程自主切换的次数
- Thread Nonvoluntary Context Switches：TiKV 线程被动切换的次数

## RocksDB - kv

- Get operations：get 操作的个数
- Get duration：get 操作的耗时
- Seek operations：seek 操作的个数
- Seek duration：seek 操作的耗时
- Write operations：write 操作的个数
- Write duration：write 操作的耗时
- WAL sync operations：sync WAL 操作的个数
- Write WAL duration：write 操作中写 WAL 的耗时
- WAL sync duration：sync WAL 操作的耗时
- Compaction operations：compaction 和 flush 操作的个数
- Compaction duration：compaction 和 flush 操作的耗时
- SST read duration：读取 SST 所需的时间
- Write stall duration：由于 write stall 造成的时间开销，正常情况下应为 0
- Memtable size：每个 CF 的 memtable 的大小
- Memtable hit：memtable 的命中率
- Block cache size：block cache 的大小。如果将 `shared block cache` 禁用，即为每个 CF 的 block cache 的大小
- Block cache hit：block cache 的命中率
- Block cache flow：不同 block cache 操作的流量
- Block cache operations 不同 block cache 操作的个数
- Keys flow：不同操作造成的 key 的流量
- Total keys：每个 CF 中 key 的个数
- Read flow：不同读操作的流量
- Bytes / Read：每次读的大小
- Write flow：不同写操作的流量
- Bytes / Write：每次写的大小
- Compaction flow：compaction 相关的流量
- Compaction pending bytes：等待 compaction 的大小
- Read amplification：每个 TiKV 实例的读放大
- Compression ratio：每一层的压缩比
- Number of snapshots：每个 TiKV 的 snapshot 的数量
- Oldest snapshots duration：最旧的 snapshot 保留的时间
- Number files at each level：每一层的文件个数
- Ingest SST duration seconds：ingest SST 所花费的时间
- Stall conditions changed of each CF：每个 CF stall 的原因

## RocksDB - raft

- Get operations：get 操作的个数
- Get duration：get 操作的耗时
- Seek operations：seek 操作的个数
- Seek duration：seek 操作的耗时
- Write operations：write 操作的个数
- Write duration：write 操作的耗时
- WAL sync operations：sync WAL 操作的个数
- Write WAL duration：write 操作中写 WAL 的耗时
- WAL sync duration：sync WAL 操作的耗时
- Compaction operations：compaction 和 flush 操作的个数
- Compaction duration：compaction 和 flush 操作的耗时
- SST read duration：读取 SST 所需的时间
- Write stall duration：由于 write stall 造成的时间开销，正常情况下应为 0
- Memtable size：每个 CF 的 memtable 的大小
- Memtable hit：memtable 的命中率
- Block cache size：block cache 的大小。如果将 `shared block cache` 禁用，即为每个 CF 的 block cache 的大小
- Block cache hit：block cache 的命中率
- Block cache flow：不同 block cache 操作的流量
- Block cache operations 不同 block cache 操作的个数
- Keys flow：不同操作造成的 key 的流量
- Total keys：每个 CF 中 key 的个数
- Read flow：不同读操作的流量
- Bytes / Read：每次读的大小
- Write flow：不同写操作的流量
- Bytes / Write：每次写的大小
- Compaction flow：compaction 相关的流量
- Compaction pending bytes：等待 compaction 的大小
- Read amplification：每个 TiKV 实例的读放大
- Compression ratio：每一层的压缩比
- Number of snapshots：每个 TiKV 的 snapshot 的数量
- Oldest snapshots duration：最旧的 snapshot 保留的时间
- Number files at each level：每一层的文件个数
- Ingest SST duration seconds：ingest SST 所花费的时间
- Stall conditions changed of each CF：每个 CF stall 的原因

## Titan - All

- Blob file count：Titan blob 文件的数量
- Blob file size：Titan blob 文件总大小
- Live blob size：有效 blob record 的总大小
- Blob cache hit：Titan 的 blob cache 命中率
- Iter touched blob file count：单个 Iterator 所涉及到 blob 文件的数量
- Blob file discardable ratio distribution：blob 文件的失效 blob record 比例的分布情况
- Blob key size：Titan 中 blob key 的大小
- Blob value size：Titan 中 blob value 的大小
- Blob get operations：blob 的 get 操作的数量
- Blob get duration：blob 的 get 操作的耗时
- Blob iter operations：blob 的 iter 操作的耗时
- Blob seek duration：blob 的 seek 操作的耗时
- Blob next duration：blob 的 next 操作的耗时
- Blob prev duration：blob 的 prev 操作的耗时
- Blob keys flow：Titan blob 读写的 key 数量
- Blob bytes flow：Titan blob 读写的 bytes 数量
- Blob file read duration：blob 文件的读取耗时
- Blob file write duration：blob 文件的写入耗时
- Blob file sync operations：blob 文件 sync 次数
- Blob file sync duration：blob 文件 sync 耗时
- Blob GC action：Titan GC 细分动作的次数
- Blob GC duration：Titan GC 的耗时
- Blob GC keys flow：Titan GC 读写的 key 数量
- Blob GC bytes flow：Titan GC 读写的 bytes 数量
- Blob GC input file size：Titan GC 输入文件的大小
- Blob GC output file size：Titan GC 输出文件的大小
- Blob GC file count：Titan GC 涉及的 blob 文件数量

## Lock manager

- Thread CPU：lock manager 的线程使用率
- Handled tasks：收到的任务的总数量
- Waiter lifetime duration：waiter 的持续时间
- Wait table：wait table 的状态信息
- Deadlock detect duration：处理死锁检测请求的耗时
- Detect error：检测的错误数量
- Deadlock detector leader：死锁检测者 leader 数量

## Memory

- Allocator Stats：内存分配器的统计信息

## Backup

- Backup CPU：backup 的线程使用率
- Range Size：backup range 的大小直方图
- Backup Duration：backup 的耗时
- Backup Flow：backup 总的字节大小
- Disk Throughput：实例磁盘的吞吐量
- Backup Range Duration：backup range 的耗时
- Backup Errors：backup 中发生的错误数量

## Encryption

- Encryption data keys：正在使用的加密 data key 的总数量
- Encrypted files：被加密的文件数量
- Encryption initialized：显示加密是否被启用，`1` 代表已经启用
- Encryption meta files size：加密相关的元数据文件的大小
- Encrypt/decrypt data nanos：加密/解密数据所耗费的时间
- Read/write encryption meta duration：读写加密文件所耗费的时间

## 面板常见参数的解释

### gRPC 消息类型

1. 使用事务型接口的命令：

    - kv_get：一个事务型的 get 命令，在带有一个开始时间戳的事务中使用 key 查询 value
    - kv_scan：在带有一个开始时间戳的事务中，根据一个 key 的范围扫描 value
    - kv_prewrite：写入 TiKV 的第一个阶段，包含一个事务中所有要写入的数据
    - kv_pessimistic_lock：锁定一系列的 key 以准备写入它们
    - kv_pessimistic_rollback：解锁一系列的 key
    - kv_txn_heart_beat：用于更新悲观事务或大事物的 `lock_ttl` 以防止其被杀掉
    - kv_check_txn_status：检查事务的状态
    - kv_commit：写入 TiKV 的第二个阶段，这个请求命令将会提交一个事务
    - kv_cleanup：清理一个 key（此命令将会在 4.0 中废除）
    - kv_batch_get：与 `kv_get` 类似，带有批量的 key
    - kv_batch_rollback：回滚一个预写的事务，这将从数据库中移除初步写入的数据，解锁相关的锁，置入一个回滚的墓碑
    - kv_scan_lock：扫面数据库的锁，用于在 GC 的初始阶段找到所有的旧锁
    - kv_resolve_lock：对于所有被 `start_version` 标记的事务锁定的 key，要么提交要么回滚
    - kv_gc：触发垃圾回收以清理 `safe_point` 之前的数据
    - kv_delete_range：从 TiKV 中删除一系列的数据

2. 非事务型的裸命令：

    - raw_get：使用 key 查询 value
    - raw_batch_get：批量地使用 key 查询 value
    - raw_scan：根据一个 key 的范围扫描 value
    - raw_batch_scan：根据多个 key 的范围扫描 value
    - raw_put：直接写入一对 key 和 value，需要提供写入的 CF
    - raw_batch_put：直接写入多对 key 和 value，需要提供写入的 CF
    - raw_delete：删除指定的 key，需要提供删除所在的 CF
    - raw_batch_delete：批量删除多个指定的 key，需要提供删除所在的 CF
    - raw_delete_range：删除一个范围的 key，需要提供删除所在的 CF

3. 存储命令（发送到集群中所有的 TiKV 节点）：

    - unsafe_destroy_range：绕过 raft 层直接从存储引擎删除一个范围的 key
    - register_lock_observer：注册一个 observer，用于监听 max_ts 之前的锁
    - check_lock_observer：检查之前 observer 的状态，取得其收集的锁
    - remove_lock_observer：关闭相应的 observer，不再进行监听
    - physical_scan_lock：绕过 raft 层直接在物理层扫描 Lock CF，返回 max_tx 之前的锁

4. 在 Coprocessor 中执行 SQL 的命令（下推到 TiKV 执行的命令）：

    - coprocessor：由 TiDB 发送的 coprocessor 请求
    - coprocessor_stream：由 TiDB 发送的 coprocessor 请求，以流形式返回
    - batch_coprocessor：由 TiDB 发送的多个 coprocessor 请求

5. Raft 命令：

    - raft：TiKV 节点间 raft 协议的消息
    - batch_raft：批量发送的 raft 协议的消息
    - snapshot：发送 raft 中状态机数据的一份快照，以流的形式发送多个打散的快照块

6. 调试事务命令：

    - mvcc_get_by_key：通过给定 key 返回 mvcc 信息
    - mvcc_get_by_start_ts：通过给定 start ts 返回 mvcc 信息

7. 其它命令：

    - batch_commands：批量发送多个命令，用于减少传输量提高性能
    - split_region：PD 发送 split region 请求给 TiKV 节点，同时指定需要 split 的 key
    - read_index：通过 raft 的一些元数据来获取 read index

### 底层数据库类型

- raft：用于存储 raft 日志的底层数据库
- kv：用于存储 key value 数据的底层数据库

### Raftstore 错误类型

- err_not_leader：对应的 peer 不是所查询 region 的 leader
- err_region_not_found：没有在当前 store 中找到需要的 region
- err_key_not_in_region：key 不在对应的 region 范围内
- err_epoch_not_match：访问的 region 的 epoch 不匹配，意即此 snapshot 的数据过时，可能由于当前还未 merge 最新的 commit
- err_server_is_busy：服务器太忙碌无法及时处理到达 TiKV 的请求，原因主要是 write stall、scheduler busy、线程池排队、raftstore 组件忙碌等
- err_stale_command：命令已经失效，当前 leader 抛弃了该请求导致其无法继续处理
- err_store_not_match：发送到错误的 store 节点上
- err_raft_entry_too_large：用户一次进行了过多的操作，导致产生的 raft entry 过大而拒绝掉本次请求

### Scheduler 错误类型

- snapshot_err：获取 snapshot 失败
- prepare_write_err：在 prewrite 阶段写入失败

### Coprocessor 错误类型

- meet_lock：当前的 key 已经被锁住
- deadline_exceeded：由于超过了处理的截止期，Coprocessor 任务被终止
- max_pending_tasks_exceeded：由于超过了最大挂起任务数量，Coprocessor 任务被终止

### 请求 PD 的消息类型

- get_region：获取给定 key 的 region 和该 region 的 leader
- bootstrap_cluster：作为集群中第一个启动的 TiKV 节点尝试启动整个集群
- is_cluster_bootstrapped：向 PD 查询当前集群是否已经被启动
- alloc_id：取得一个新的 store id
- put_store：上传一个 store 的元数据信息
- get_store：通过 store id 获取相关的元数据信息
- get_all_stores：获取集群所有 store 的元数据信息
- get_cluster_config：获取当前集群的配置信息，如 id、单个 region 的最大 peer 数量等信息
- get_region_by_id：通过 id 获取 region 的相关信息，如 region 范围、leader、follower 等信息
- ask_split：请求分割一个 region，获取新 region id 和 peer id 信息
- ask_batch_split：请求将一个 region 分成多个 region
- store_heartbeat：发送关于当前 store 的心跳消息
- report_batch_split：当 TiKV 完成了 split region 后将相关的 region 信息汇报给 PD 以更新 region 信息
- get_gc_safe_point：获取当前 gc 的时间戳 safe point，参考 [GC doc](https://pingcap.com/docs-cn/dev/garbage-collection-overview/)
- get_operator：获取给定 region 的 operator 的相关状态信息
- tso：从 PD 获取全局时间戳 tso，仅给 CDC 使用
- get_members：获取当前集群的成员列表，不用提供对应集群的 id

### PD 心跳类型

- send：发送到 PD 的心跳
- noop：PD 返回的心跳没有包含任何命令
- merge：PD 返回的心跳包含 merge 命令
- change peer：PD 返回的心跳 change peer 命令
- transfer leader：PD 返回的心跳包含 transfer leader 的命令
- split region：PD 返回的心跳包含 split region 的命令

### Raft ready 类型

- message：raft ready 产生的需要发出给其它节点的消息
- commit：raft ready 产生的需要 commit 的 entry 数量
- append：raft ready 产生的需要 append 的 entry 数量
- snapshot：raft ready 产生的需要应用的 snapshot 的数量
- has_ready_region：具有 ready 消息的 raft group 的数量

### Scheduler priority 级别

- normal：SQL 提交会携带优先级，如果不指定则为 normal 优先级
- high：SQL 提交会携带优先级，可以指定为 high，TiDB 在执行阶段会优先处理这条语句
- low：SQL 提交会携带优先级，可以指定为 low，TiDB 在执行阶段会降低执行这条语句的优先级

### Store tick 类型

tick 为驱动 Raft 状态机的行为，下面是对于一个 TiKV store 层面具备的 tick 类型：

- compact_check：驱动以检测当前的 TiKV store 是否有 region 需要开始进行 compaction
- pd_store_heartbeat：驱动以发送心跳到 PD 节点以上传当前 store 的状态信息
- snap_gc：驱动以将当前 store 内所有没有正在使用即空闲状态的 snapshot 删除
- compact_lock_cf：驱动以创建一个合并 lock cf 的任务并直接调度，lock cf 是事务中存放 key 的 lock 的区域，但有时候大量读写操作会使这个区域过大影响性能，需要合并以增加检索效率
- consistency_check：驱动以对当前 store 的所有 region 的数据进行一致性检查
- cleanup_import_sst：驱动以将失效的 sst 删除，判断的规则是所在的 region 的 epoch 过期或者本地无法找到相关 region 信息，但是从 PD 中验证后可以删除

### Peer tick 类型

- raft：驱动 raft 消息在集群中发送
- raft_log_gc：驱动删除过时的 raft log，判断标准是当 replicated index 和 compact index 的差值大于阈值即删除这部分差值的 log
- split_region_check：驱动以在 leader peer 中检查是否需要将当前管理的 region 进行 split
- pd_heartbeat：驱动以发送心跳到 PD 节点上传当前 region 的状态信息
- check_merge：检测是否需要将相邻的小 region 进行合并
- check_peer_stale_state：检查其它 peer 的状态，对于 follower 而言，如果检测到 leader 无法 ping 成功即发起新一轮选举

### Raft 消息类型

在发送阶段统计 raft 消息类型：

- append：发送 append raft log
- append_resp：回应 append raft log
- prevote：预选举消息，和普通 vote 的区别在于当前 peer 的状态并未变成选举状态，因而不会阻塞正常的操作，减少了网络隔离之后的集群的网络抖动
- prevote_resp：回应预选举消息
- vote：raft 协议中的选举
- vote_resp：回应选举消息
- snapshot：发送 snapshot 给其它 peer，leader 用此方式快速同步 raft log 给其它 peer
- request_snapshot：回应 snapshot 的接收状况
- heartbeat：raft group 中的心跳消息
- heartbeat_resp：回应 raft group 中的心跳消息
- transfer_leader：发起转换 leader 给希望成为 leader 的 peer
- timeout_now：在 transfer leader 过程中旧 leader 的租约提前到期
- read_index：向 leader 发送最新的 read index 的请求，用于 follower read 的场景
- read_index_resp：leader 回复自己的 read index

### Raft 消息 drop 原因

- mismatch_store_id：发到了错误的 store 上
- mismatch_region_epoch：访问的 region 的 epoch 不匹配，意即此 snapshot 的数据过时，可能由于当前还未 merge 最新的 commit
- stale_msg：raft 消息已经失效，当前 leader 抛弃了该请求导致无法继续处理
- region_overlap：两个 region 重叠了，这里使用最新的 snapshot 的范围进行比对
- region_no_peer：snapshot 没有包含对应的 peer //todo why
- region_tombstone_peer：
- region_nonexistent：
- applying_snap：

### Raft proposal 消息类型 

- local_read：
- read_index：
- normal：
- conf_change：
- transfer_leader：

### Local read 拒绝类型

- store_id_mismatch：
- peer_id_mismatch：
- term_mismatch：
- lease_expire：
- no_region：
- rejected_by_no_lease：
- rejected_by_epoch：
- rejected_by_appiled_term：
- rejected_by_channel_full：
- local_executed_requests：

### 工作线程名字

### Future poll 名字前缀

