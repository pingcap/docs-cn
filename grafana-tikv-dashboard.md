---
title: TiKV 重要监控指标详解
category: reference
aliases: ['/docs-cn/dev/reference/key-monitoring-metrics/tikv-dashboard/']
---

# TiKV 重要监控指标详解

使用 TiUP 部署 TiDB 集群时，可以一键部署监控系统 (Prometheus/Grafana)，监控架构请看 [TiDB 监控框架概述](/tidb-monitoring-framework.md)。

目前默认的 Grafana Dashboard 整体分为 PD、TiDB、TiKV、Node_exporter、Overview 等。

对于日常运维，我们通过观察 TiKV-Details 面板上的指标，可以了解 TiKV 当前的状态。根据 [性能地图](https://asktug.com/_/tidb-performance-map/#/) 可以检查集群的状态是否符合预期。

以下为 TiKV-Details 默认的监控信息：

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
- Uptime： 自上次重启以来 TiKV 正常运行的时间

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
- Active written leaders：各个 TiKV 实例中正在被写入的 leader 的数量
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
- TiKV AutoGC Working：
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
- Total Request Errors：
- Handle duration：处理 coprocessor 请求所花费的时间
- Total Request Errors：下推的请求发生错误的个数，正常情况下，短时间内不应该有大量的错误
- Total KV Cursor Operations：各种类型的 kv cursor 操作的总数量
- KV Cursor Operations：各种类型的 kv cursor 操作的数量
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
- Threads IO：TiKV 各个线程的 IO 使用量
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

## Lock manager

## Memory

## Backup

## Encryption
