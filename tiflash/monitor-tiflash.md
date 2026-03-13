---
title: TiFlash 集群监控
aliases: ['/docs-cn/dev/tiflash/monitor-tiflash/','/docs-cn/dev/reference/tiflash/monitor/']
summary: TiFlash 集群监控包括 TiFlash-Summary、TiFlash-Proxy-Summary 和 TiFlash-Proxy-Details。监控指标包括存储、内存、CPU 使用率、请求处理、错误数量、线程数、任务调度、DDL、写入、读取、Raft 等信息。注意低版本监控信息不完善，建议使用 v4.0.5 或更高版本的 TiDB 集群。
---

# TiFlash 集群监控

使用 TiUP 部署 TiDB 集群时，一键部署监控系统 (Prometheus & Grafana)，监控架构参见 [TiDB 监控框架概述](/tidb-monitoring-framework.md)。

目前 Grafana Dashboard 整体分为 PD、TiDB、TiKV、Node\_exporter、Overview 等。

TiFlash 面板一共包括 **TiFlash-Summary**、**TiFlash-Proxy-Summary**、**TiFlash-Proxy-Details**。通过面板上的指标，可以了解 TiFlash 当前的状态。其中 **TiFlash-Proxy-Summary**、**TiFlash-Proxy-Details** 主要为 TiFlash 的 Raft 层信息，其监控指标与 TiKV 有大量重合，详细含义可结合 [TiKV 监控指标详解](/grafana-tikv-dashboard.md)。

> **注意：**
>
> 低版本的 TiFlash 监控信息较不完善，如有需要推荐使用 v4.0.5 或更高版本的 TiDB 集群。

以下为 **TiFlash-Summary** 默认的监控信息：

## Server

- Store size：每个 TiFlash 实例的使用的存储空间的大小。
- Available size：每个 TiFlash 实例的可用的存储空间的大小。
- Capacity size：每个 TiFlash 实例的存储容量的大小。
- Uptime：自上次重启以来 TiFlash 正常运行的时间。
- Memory：每个 TiFlash 实例内存的使用情况。
- CPU Usage：每个 TiFlash 实例 CPU 的使用率。
- FSync OPS：每个 TiFlash 实例每秒进行 fsync 操作的次数。
- File Open OPS：每个 TiFlash 实例每秒进行 open 操作的次数。
- Opened File Count：当前每个 TiFlash 实例打开的文件句柄数。
- Region：每个 TiFlash 实例持有的 Region 数量。
- IO Throughput：每个 TiFlash 实例的 I/O 吞吐量。
- Threads CPU：各线程 CPU 使用情况。
- SST Import Service：SST 导入服务相关指标。
- SST Apply：SST 应用相关指标。
- Region Task：Region 任务统计。
- Region Worker：Region worker 线程统计。
- Raft Store：Raft Store 相关状态与统计。
- Apply Worker：Apply worker 相关统计。
- Storage Background (Small Tasks)：存储层小型后台任务统计。
- Storage Background (Large Tasks)：存储层大型后台任务统计。
- Manual Compaction：手动压缩任务统计。
- GRPC Async Server：gRPC 异步服务端相关统计。
- GRPC Async Client：gRPC 异步客户端相关统计。
- FAP builder：FAP 构建相关统计。
- Snapshot Sender：Snapshot 发送相关统计。
- Segment Scheduler：Segment 调度器相关统计。
- Local Index Pool：本地索引池相关统计。
- Segment Reader：Segment Reader 相关统计。
- Threads：线程数统计。
- Threads state：线程状态分布。
- Threads IO：线程 I/O 相关统计。
- Thread Voluntary Context Switches：线程自愿上下文切换次数。
- Thread Nonvoluntary Context Switches：线程非自愿上下文切换次数。

> **注意：**
>
> Store size、FSync OPS、File Open OPS、Opened File Count 目前仅包含了 TiFlash 存储层的统计指标，未包括 TiFlash-Proxy 内的信息。

## Coprocessor

- Request QPS：所有 TiFlash 实例收到的 coprocessor 请求数量。其中 batch 是 batch 请求数量，batch_cop 是 batch 请求中的 coprocessor 请求数量，cop 是直接通过 coprocessor 接口发送的 coprocessor 请求数量，cop_dag 是所有 coprocessor 请求中 dag 请求数量，super_batch 是开启 super batch 特性的请求数量。
- Executor QPS：所有 TiFlash 实例收到的请求中，每种 dag 算子的数量，其中 table_scan 是扫表算子，selection 是过滤算子，aggregation 是聚合算子，top_n 是 TopN 算子，limit 是 limit 算子。
- Request Duration：所有 TiFlash 实例处理 coprocessor request 总时间，总时间为接收到该 coprocessor 请求至请求应答完毕的时间。
- Error QPS：所有 TiFlash 实例处理 coprocessor 请求的错误数量。其中 meet_lock 为读取的数据有锁，region_not_found 为 Region 不存在，epoch_not_match 为读取的 Region epoch 与本地不一致，kv_client_error 为与 TiKV 通信产生的错误，internal_error 为 TiFlash 内部系统错误，other 为其他错误。
- Request Handle Duration：所有 TiFlash 实例处理 coprocessor 请求处理时间，处理时间为该 coprocessor 请求开始执行到执行结束的时间。
- Response Bytes/Seconds：所有 TiFlash 实例应答总字节数。
- Cop task memory usage：所有 TiFlash 实例处理 coprocessor 请求占用的总内存。
- Handling Request Number：所有 TiFlash 实例正在处理的 coprocessor 请求数量之和。请求的分类与 Request QPS 中的分类相同。
- Threads of RPC：每个 TiFlash 实例使用的实时 RPC 线程数。
- Max Threads of RPC：最近一段时间每个 TiFlash 实例使用的 RPC 线程数峰值。
- Threads：每个 TiFlash 实例使用的实时线程数。
- Max Threads：最近一段时间每个 TiFlash 实例使用的线程数峰值。
- Exchange Bytes/Seconds：Exchange 阶段的吞吐量。
- MPP Query count：MPP 查询数量。
- Time of the Longest Live MPP Task：最长存活 MPP 任务的持续时间。
- Data size in send and receive queue：发送与接收队列中的数据量。
- Network Transmission：网络传输统计。
- Establish calldata details：建立 calldata 的细节统计。

## Task Scheduler

- Min TSO：每个 TiFlash 实例上正在运行的查询语句中的最小 TSO，该值确保具有最小 TSO 的查询可以被调度。如果当前没有正在运行的查询，则该值为 `uint64` 整数型最大值。
- Estimated Thread Usage and Limit：每个 TiFlash 实例上正在运行的所有任务占用的线程估值，以及该实例上任务调度器设置的估算线程用量的软限制和硬限制。
- Active and Waiting Queries Count：每个 TiFlash 实例上正在运行的查询数量和正在等待的查询数量。
- Active and Waiting Tasks Count：每个 TiFlash 实例上正在运行的任务数量和正在等待的任务数量。
- Hard Limit Exceeded Count：每个 TiFlash 实例上运行中任务的估算线程用量超过了设置的硬限制的次数。
- Task Waiting Duration：每个 TiFlash 实例上任务从初始化到被调度的等待时长。

## DDL

- Schema Version：每个 TiFlash 实例目前缓存的 schema 版本。
- Schema Apply OPM：所有 TiFlash 实例每分钟 apply 同步 TiDB schema diff 的次数。diff apply 是正常的单次 apply 过程，如果 diff apply 失败，则 failed apply +1，并回退到 full apply，拉取最新的 schema 信息以更新 TiFlash 的 schema 版本。
- Schema Internal DDL OPM：所有 TiFlash 实例每分钟执行的内部 DDL 次数。
- Schema Apply Duration：所有 TiFlash 实例 apply schema 消耗的时间。

## Imbalance read/write

- CPU Usage (irate)：CPU 使用率的瞬时变化率。
- Segment Reader：Segment Reader 相关统计。
- Request QPS by instance：按实例统计的请求 QPS。
- Read Throughput by instance：按实例统计的读取吞吐量。
- Write Command OPS By Instance：按实例统计的写命令次数。
- Write Throughput By Instance：按实例统计的写入吞吐量。

## Memory trace

- Number of Keyspaces：Keyspace 数量。
- Number of Physical Tables：物理表数量。
- Number of Segments：Segment 数量。
- Bytes of MemTables：MemTable 占用字节数。
- Mark Cache and Minmax Index Cache Memory Usage：Mark Cache 与 Minmax Index Cache 内存占用。
- Effectiveness of Mark Cache：Mark Cache 命中效率。
- Schema of Column File：Column File 的 schema 统计。
- Read Snapshots：读取快照相关统计。
- Memory by thread：按线程统计的内存使用。
- Memory by thread (proxy)：Proxy 线程内存使用统计。
- Memory by class：按内存类别统计的使用情况。
- KVStore memory：KVStore 内存使用。

## Storage

- Write Command OPS：所有 TiFlash 实例存储层每秒收到的写请求数量。
- Write Amplification：每个 TiFlash 实例写放大倍数（实际磁盘写入量/逻辑数据写入量）。total 为自此次启动以来的写放大倍数，5min 为最近 5 分钟内的写放大倍数。
- Read Tasks OPS：每个 TiFlash 实例每秒存储层内部读取任务的数量。
- Rough Set Filter Rate：每个 TiFlash 实例最近 1 分钟内读取的 packet 数被存储层粗糙索引过滤的比例。
- Internal Tasks OPS：所有 TiFlash 实例每秒进行内部数据整理任务的次数。
- Internal Tasks Duration：所有 TiFlash 实例进行内部数据整理任务消耗的时间。
- Page GC Tasks OPM：所有 TiFlash 实例每分钟进行 Delta 部分数据整理任务的次数。
- Page GC Tasks Duration：所有 TiFlash 实例进行 Delta 部分数据整理任务消耗的时间分布。
- FSync Status：fsync 状态统计。
- Disk Write OPS：所有 TiFlash 实例每秒进行磁盘写入的次数。
- Disk Read OPS：所有 TiFlash 实例每秒进行磁盘读取的次数。
- Write flow：所有 TiFlash 实例磁盘写操作的流量。
- Read flow：所有 TiFlash 实例磁盘读操作的流量。
- SubTasks Write Throughput (bytes)：子任务写入吞吐量（字节）。
- SubTasks Write Throughput (rows)：子任务写入吞吐量（行数）。
- Small Internal Tasks OPS：小型内部任务每秒次数。
- Small Internal Tasks Duration：小型内部任务耗时。
- Large Internal Tasks OPS：大型内部任务每秒次数。
- Large Internal Tasks Duration：大型内部任务耗时。
- Current Data Management Tasks：当前数据管理任务数量。
- Compression Ratio：压缩比。
- Compression Algorithm Count：不同压缩算法的计数。

> **注意：**
>
> 目前这部分监控指标仅包含了 TiFlash 存储层的统计指标，未包括 TiFlash-Proxy 内的信息。

## Storage Read Pool & Data Sharing

- Read Tasks OPS：读取任务每秒次数。
- Read Snapshots：读取快照相关统计。
- Read Thread Internal Duration：读线程内部处理耗时。
- Read Thread Scheduling：读线程调度耗时。
- Data Sharing：数据共享相关统计。
- Segment MergedTask：Segment 合并任务统计。
- Segment MergedTask Duration：Segment 合并任务耗时。
- VersionChain：版本链相关统计。
- DeltaIndexError：DeltaIndex 错误统计。

## PageStorage

- PageStorage Disk Usage：PageStorage 磁盘使用量。
- PageStorage File Num：PageStorage 文件数量。
- PageStorage WriteBatch Size：WriteBatch 大小分布。
- Page write Duration：Page 写入耗时。
- Page GC Tasks OPM：Page GC 任务每分钟次数。
- Page GC Duration：Page GC 耗时。
- Numer of Pages：Page 数量。
- PageStorage Pending Writers Num：等待写入的 writer 数量。
- PageStorage stored bytes by type：按类型统计的 PageStorage 字节数。
- Number of Tables：表数量。
- PS Command OPS By Instance：按实例统计的 PageStorage 命令次数。
- PS Apply edits OPS By Instance：按实例统计的 PageStorage apply edits 次数。

## Rate Limiter

- I/O Limiter Throughput：I/O 限速吞吐量。
- I/O Limiter Threshold：I/O 限速阈值。
- I/O Limiter Pending Rate and Duration：I/O 限速排队速率与排队时长。
- I/O Limiter Current Pending Count：I/O 限速当前排队数量。

## Storage Write Stall

- Write & Delta Management Throughput：所有实例写入及数据整理的吞吐量。
    - `throughput_write` 表示通过 Raft 进行数据同步的吞吐量。
    - `throughput_delta-management` 表示数据整理的吞吐量。
    - `total_write` 表示自上次启动以来的总写入字节数。
    - `total_delta-management` 表示自上次启动以来数据整理的总字节数。
- Write & Delta Management Total：写入与数据整理的累计量。
- Write Stall Duration：每个实例写入和移除 Region 数据产生的卡顿时长。
- Write Throughput By Instance：每个实例写入数据的吞吐量，包括 apply Raft 数据日志以及 Raft 快照的写入吞吐量。
- Write Command OPS By Instance：每个实例收到各种命令的总计数。
    - `write block` 表示通过 Raft 同步数据日志。
    - `delete_range` 表示从该实例中删除一些 Region 或移动一些 Region 到该实例中。
    - `ingest` 表示这些 Region 的快照被应用到这个实例中。

## Raft

- Raft Read Index OPS：每个 TiFlash 实例每秒触发 read_index 请求的次数，等于请求触发的 Region 总数。
- Read Index Duration：所有 TiFlash 实例在进行 read_index 消耗的时间，主要消耗在于和 Region leader 的交互和重试时间。
- Raft Wait Index Duration：所有 TiFlash 实例在进行 wait_index 消耗的时间，即拿到 read_index 请求后，等待本地的 Region index >= read_index 所花费的时间。
- Stale Read OPS：Stale Read 每秒请求次数。
- Learner Read Failures：Learner 读失败次数。
- Read Index Events：Read Index 事件统计。
- Raft Batch Read Index Duration：批量 Read Index 耗时。
- Apply Raft write logs Duration：应用 Raft 写日志耗时。
- Region write Duration (decode)：Region 写入解码耗时。
- Region write Duration (write blocks)：Region 写入写块耗时。
- Apply Raft write logs Duration [Heatmap]：应用 Raft 写日志耗时热力图。
- Apply Raft admin logs Duration [Heatmap]：应用 Raft 管理日志耗时热力图。
- Raft Events QPS：Raft 事件 QPS。
- Raft Frequent Events QPS：Raft 高频事件 QPS。
- Raft Log Gap Heatmap：Raft 日志间隔热力图。
- Raft Entry Batch Size Heatmap：Raft Entry 批大小热力图。
- Region Size (by event) Heatmap：按事件统计的 Region 大小热力图。
- Big Write To Region Size Heatmap：大写入 Region 大小热力图。
- Write Committed Size Heatmap：提交写入大小热力图。
- Raft Eager GC OPS：Raft Eager GC 次数。
- Raft Eager GC Duration：Raft Eager GC 耗时。
- Keys flow：Key 流量统计。
- Raft throughput：Raft 吞吐量。
- Upstream Latency [Heatmap]：上游延迟热力图。
- Upstream Latency：上游延迟统计。
- Log Replication Rejected：日志复制被拒绝次数。

## Raft Snapshot / IngestSST

- Heavy Raft Apply Duration：重负载 Raft Apply 耗时。
- Applying snapshots Count：正在应用的 snapshot 数量。
- Snapshot Uncommitted Size Heatmap：未提交 snapshot 大小热力图。
- Ongoing raft snapshot：进行中的 Raft snapshot 数量。
- Snapshot Size Heatmap：Snapshot 大小热力图。
- Snapshot Predecode Duration：Snapshot 预解码耗时。
- Snapshot Prehandle Throughput Heatmap：Snapshot 预处理吞吐量热力图。
- Snapshot Flush Duration：Snapshot Flush 耗时。
- Ingest Uncommitted Size Heatmap：未提交 Ingest SST 大小热力图。
- Snapshot Predecode SST to DT Duration：Snapshot 预解码 SST 到 DT 耗时。
- Ingest SST Duration：Ingest SST 耗时。
- Rough Set Filter Rate Histogram：粗糙索引过滤率直方图。
- Rough Set Filter Rate：粗糙索引过滤率。

## Disaggregated-Write

- Checkpoint Upload Duration：Checkpoint 上传耗时。
- Checkpoint Upload flow：Checkpoint 上传流量。
- Checkpoint Upload keys speed by type (all)：Checkpoint 上传 keys 速率（按类型）。
- Checkpoint Upload flow by type (incremental+compaction)：Checkpoint 上传流量（增量与压缩）。
- Remote File Num：远端文件数量。
- Remote Store Usage：远端存储使用量。
- Remote Object Lock Request QPS：远端对象锁请求 QPS。
- Remote Object Lock Duration：远端对象锁耗时。
- Remote GC Duration Breakdown：远端 GC 耗时分布。
- Remote GC Status：远端 GC 状态。
- FAP result：FAP 结果统计。
- FAP state：FAP 状态统计。
- FAP time by stage：FAP 各阶段耗时。
- FAP no match reason：FAP 未匹配原因统计。

## Disaggregated-Compute

- Read Duration Breakdown：读取耗时拆分。
- Remote Cache Operations：远端缓存操作统计。
- Remote Cache Flow：远端缓存流量。
- Remote Cache Usage：远端缓存使用量。
- Memory Usage of Storage Tasks：存储任务内存使用。
- MVCCIndexCache：MVCC 索引缓存统计。
- PlaceIndex Tasks Duration：PlaceIndex 任务耗时。
- PlaceIndexTask/Reuse OPS：PlaceIndex 任务/复用次数。
- PlaceIndex update rows/deletes：PlaceIndex 更新行数/删除数。

## S3

- S3 Bytes：S3 传输字节数。
- S3 OPS：S3 请求次数。
- S3 Retry OPS：S3 重试次数。
- S3 Request Duration：S3 请求耗时。
- S3 HTTP OPS：S3 HTTP 请求次数。
- S3 HTTP Request Duration：S3 HTTP 请求耗时。
- S3 on-going instances：S3 进行中的实例数量。
- S3RandomAccessFile OPS：S3 RandomAccessFile 操作次数。

## Pipeline Model

- Task Thread Pool Size：任务线程池大小。
- Task Count：任务数量。
- Task Status Change OPS：任务状态变更次数。
- Task Duration：任务耗时。
- Task Max Execute Time Per Round：每轮任务最大执行时间。
- Threads CPU of CPU Task Thread Pool：CPU 任务线程池 CPU 使用。
- Threads CPU of IO Task Thread Pool：IO 任务线程池 CPU 使用。
- Threads CPU of Wait Reactor：Wait Reactor 线程 CPU 使用。
- Wait notify task details：Wait notify 任务详情。

## TiFlash Resource Control

- TiFlash Resource Group：TiFlash 资源组统计。
- Request Unit：请求资源单元统计。

## Status Server

- Status API Request Duration：Status API 请求耗时。
- Status API Request (op/s)：Status API 请求速率。

## Vector Search

- In-Memory Vector Index Instances：内存向量索引实例数量。
- Vector Index Estimated Memory Usage：向量索引估算内存使用。
- 99.9% Vector Search Duration (Per Request)：向量检索请求 99.9% 耗时。
- 99.9% Vector Index Build Duration (Per DMFile Column)：向量索引构建 99.9% 耗时。

## TiFlash-Proxy-Summary

### Cluster
- IO utilization：IO utilization 相关指标。
- Region：Region 相关指标。

### Errors
- Server is busy：Server is busy 相关指标。
- Leader missing：Leader missing 相关指标。

### Server
- CF size：CF size 相关指标。

### Thread CPU
- Raft store CPU：Raft store CPU 相关指标。
- RocksDB CPU：RocksDB CPU 相关指标。
- Split check CPU：Split check CPU 相关指标。
- Background worker CPU：Background worker CPU 相关指标。
- GC worker CPU：GC worker CPU 相关指标。
- Region task worker pre-handle/generate snapshot CPU：Region task worker pre-handle/generate snapshot CPU 相关指标。

### PD
- PD requests：PD requests 相关指标。
- PD request duration (average)：PD request duration (average) 相关指标。

## TiFlash-Proxy-Details

### Cluster
- CPU：CPU 相关指标。
- Memory：Memory 相关指标。
- IO utilization：IO utilization 相关指标。
- Uptime：Uptime 相关指标。
- Leader：Leader 相关指标。
- Region：Region 相关指标。
- Memory trace：Memory trace 相关指标。

### Raft Engine
- Operation：Operation 相关指标。
- Write Duration：Write Duration 相关指标。
- Flow：Flow 相关指标。
- Write Duration Breakdown (99%)：Write Duration Breakdown (99%) 相关指标。
- Bytes / Written：Bytes / Written 相关指标。
- WAL Duration Breakdown (999%)：WAL Duration Breakdown (999%) 相关指标。
- File Count：File Count 相关指标。
- Other Durations (99%)：Other Durations (99%) 相关指标。
- Entry Count：Entry Count 相关指标。
- Write Compression Ratio：Write Compression Ratio 相关指标。

### Errors
- Critical error：Critical error 相关指标。
- Server is busy：Server is busy 相关指标。
- Server report failures：Server report failures 相关指标。
- Raftstore error：Raftstore error 相关指标。
- Scheduler error：Scheduler error 相关指标。
- Coprocessor error：Coprocessor error 相关指标。
- gRPC message error：gRPC message error 相关指标。
- Leader drop：Leader drop 相关指标。
- Leader missing：Leader missing 相关指标。

### Server
- CF size：CF size 相关指标。
- Store size：Store size 相关指标。
- Channel full：Channel full 相关指标。
- Active written leaders：Active written leaders 相关指标。
- Approximate Region size：Approximate Region size 相关指标。
- Approximate Region size Histogram：Approximate Region size Histogram 相关指标。
- Region average written bytes：Region average written bytes 相关指标。
- Region written bytes：Region written bytes 相关指标。
- Region average written keys：Region average written keys 相关指标。
- Region written keys：Region written keys 相关指标。
- Request batch ratio：Request batch ratio 相关指标。
- Request batch input：Request batch input 相关指标。

### gRPC
- gRPC message count：gRPC message count 相关指标。
- gRPC message failed：gRPC message failed 相关指标。
- 99% gRPC messge duration：99% gRPC messge duration 相关指标。
- Average gRPC messge duration：Average gRPC messge duration 相关指标。
- gRPC batch size：gRPC batch size 相关指标。
- raft message batch size：raft message batch size 相关指标。

### Thread CPU
- Raft store CPU：Raft store CPU 相关指标。
- Async apply CPU：Async apply CPU 相关指标。
- Scheduler worker CPU：Scheduler worker CPU 相关指标。
- gRPC poll CPU：gRPC poll CPU 相关指标。
- Unified read pool CPU：Unified read pool CPU 相关指标。
- Storage ReadPool CPU：Storage ReadPool CPU 相关指标。
- Coprocessor CPU：Coprocessor CPU 相关指标。
- RocksDB CPU：RocksDB CPU 相关指标。
- Read Index Worker CPU：Read Index Worker CPU 相关指标。
- GC worker CPU：GC worker CPU 相关指标。
- Background worker CPU：Background worker CPU 相关指标。
- Region task worker pre-handle/generate snapshot CPU：Region task worker pre-handle/generate snapshot CPU 相关指标。

### PD
- PD requests：PD requests 相关指标。
- PD request duration (average)：PD request duration (average) 相关指标。
- PD heartbeats：PD heartbeats 相关指标。
- PD validate peers：PD validate peers 相关指标。

### Raft IO
- Apply log duration：Apply log duration 相关指标。
- Apply log duration per server：Apply log duration per server 相关指标。
- Append log duration：Append log duration 相关指标。
- Append log duration per server：Append log duration per server 相关指标。
- Commit log duration：Commit log duration 相关指标。
- Commit log duration per server：Commit log duration per server 相关指标。

### Raft process
- Ready handled：Ready handled 相关指标。
- Process ready duration per server：Process ready duration per server 相关指标。
- 0.99 Duration of raft store events：0.99 Duration of raft store events 相关指标。

### Raft message
- Sent messages per server：Sent messages per server 相关指标。
- Flush messages per server：Flush messages per server 相关指标。
- Receive messages per server：Receive messages per server 相关指标。
- Messages：Messages 相关指标。
- Vote：Vote 相关指标。
- Raft dropped messages：Raft dropped messages 相关指标。

### Raft propose
- Raft proposals per ready：Raft proposals per ready 相关指标。
- Raft read/write proposals：Raft read/write proposals 相关指标。
- Raft read proposals per server：Raft read proposals per server 相关指标。
- Raft write proposals per server：Raft write proposals per server 相关指标。
- Propose wait duration：Propose wait duration 相关指标。
- Propose wait duration per server：Propose wait duration per server 相关指标。
- Apply wait duration：Apply wait duration 相关指标。
- Apply wait duration per server：Apply wait duration per server 相关指标。
- Raft log speed：Raft log speed 相关指标。
- Perf Context duration：Perf Context duration 相关指标。

### Raft admin
- Admin proposals：Admin proposals 相关指标。
- Admin apply：Admin apply 相关指标。
- Check split：Check split 相关指标。
- 99.99% Check split duration：99.99% Check split duration 相关指标。

### Unified Read Pool
- Time used by level：Time used by level 相关指标。
- Level 0 chance：Level 0 chance 相关指标。
- Running tasks：Running tasks 相关指标。

### Storage
- Storage command total：Storage command total 相关指标。
- Storage async request error：Storage async request error 相关指标。
- Storage async snapshot duration：Storage async snapshot duration 相关指标。
- Storage async write duration：Storage async write duration 相关指标。

### Scheduler
- Scheduler stage total：Scheduler stage total 相关指标。
- Scheduler writing bytes：Scheduler writing bytes 相关指标。
- Scheduler priority commands：Scheduler priority commands 相关指标。
- Scheduler pending commands：Scheduler pending commands 相关指标。

### Scheduler - $command
- Scheduler stage total：Scheduler stage total 相关指标。
- Scheduler command duration：Scheduler command duration 相关指标。
- Scheduler latch wait duration：Scheduler latch wait duration 相关指标。
- Scheduler keys read：Scheduler keys read 相关指标。
- Scheduler keys written：Scheduler keys written 相关指标。
- Scheduler scan details：Scheduler scan details 相关指标。
- Scheduler scan details [lock]：Scheduler scan details [lock] 相关指标。
- Scheduler scan details [write]：Scheduler scan details [write] 相关指标。
- Scheduler scan details [default]：Scheduler scan details [default] 相关指标。

### Snapshot
- Rate snapshot message：Rate snapshot message 相关指标。
- 99% Handle snapshot duration：99% Handle snapshot duration 相关指标。
- Snapshot state count：Snapshot state count 相关指标。
- 99.99% Snapshot size：99.99% Snapshot size 相关指标。
- 99.99% Snapshot KV count：99.99% Snapshot KV count 相关指标。

### Task
- Worker handled tasks：Worker handled tasks 相关指标。
- Worker pending tasks：Worker pending tasks 相关指标。
- FuturePool handled tasks：FuturePool handled tasks 相关指标。
- FuturePool pending tasks：FuturePool pending tasks 相关指标。

### Threads
- Threads state：Threads state 相关指标。
- Threads IO：Threads IO 相关指标。
- Thread Voluntary Context Switches：Thread Voluntary Context Switches 相关指标。
- Thread Nonvoluntary Context Switches：Thread Nonvoluntary Context Switches 相关指标。

### RocksDB - $db
- Get operations：Get operations 相关指标。
- Get duration：Get duration 相关指标。
- Seek operations：Seek operations 相关指标。
- Seek duration：Seek duration 相关指标。
- Write operations：Write operations 相关指标。
- Write duration：Write duration 相关指标。
- WAL sync operations：WAL sync operations 相关指标。
- Write WAL duration：Write WAL duration 相关指标。
- Compaction operations：Compaction operations 相关指标。
- WAL sync duration：WAL sync duration 相关指标。
- SST read duration：SST read duration 相关指标。
- Compaction duration：Compaction duration 相关指标。
- Block cache size：Block cache size 相关指标。
- Compaction reason：Compaction reason 相关指标。
- Block cache flow：Block cache flow 相关指标。
- Memtable hit：Memtable hit 相关指标。
- Keys flow：Keys flow 相关指标。
- Block cache hit：Block cache hit 相关指标。
- Read flow：Read flow 相关指标。
- Block cache operations：Block cache operations 相关指标。
- Write flow：Write flow 相关指标。
- Total keys：Total keys 相关指标。
- Compaction flow：Compaction flow 相关指标。
- Bytes / Read：Bytes / Read 相关指标。
- Read amplication：Read amplication 相关指标。
- Bytes / Write：Bytes / Write 相关指标。
- Number of snapshots：Number of snapshots 相关指标。
- Compaction pending bytes：Compaction pending bytes 相关指标。
- Number files at each level：Number files at each level 相关指标。
- Compression ratio：Compression ratio 相关指标。
- Stall conditions changed of each CF：Stall conditions changed of each CF 相关指标。
- Oldest snapshots duration：Oldest snapshots duration 相关指标。
- Write Stall Reason：Write Stall Reason 相关指标。
- Ingest SST duration seconds：Ingest SST duration seconds 相关指标。
- Write stall duration：Write stall duration 相关指标。
- Memtable size：Memtable size 相关指标。

### Encryption
- Encryption data keys：Encryption data keys 相关指标。
- Encrypted files：Encrypted files 相关指标。
- Encryption initialized：Encryption initialized 相关指标。
- Encryption meta files size：Encryption meta files size 相关指标。
- Read/write encryption meta duration：Read/write encryption meta duration 相关指标。
