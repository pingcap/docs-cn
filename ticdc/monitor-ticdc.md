---
title: TiCDC 详细监控指标
summary: 了解 TiCDC 详细的监控指标。
aliases: ['/zh/tidb/dev/ticdc-grafana-dashboard']
---

# TiCDC 详细监控指标

本文档对 TiCDC 监控面板上的各项指标进行详细说明。在日常运维中，运维人员可通过观察 TiCDC 面板上的指标了解 TiCDC 当前的状态。

本文档的对指标的介绍基于以下同步任务，即使用默认配置同步数据到 MySQL。

```shell
cdc cli changefeed create --server=http://10.0.10.25:8300 --sink-uri="mysql://root:123456@127.0.0.1:3306/" --changefeed-id="simple-replication-task"
```

## TiCDC 新架构监控指标

[TiCDC 新架构](/ticdc/ticdc-architecture.md)的监控面板为 **TiCDC-New-Arch**。对于 v8.5.4 及以上版本的 TiDB 集群，该监控面板已在集群部署或升级时自动集成到 Grafana 中，无需手动操作。

如果你的集群版本低于 v8.5.4，需要手动导入 TiCDC 监控指标文件：

1. 下载 TiCDC 新架构监控指标文件

    ```shell
    wget https://raw.githubusercontent.com/pingcap/ticdc/refs/heads/release-8.5/metrics/grafana/ticdc_new_arch.json
    ```

2. 在 Grafana 页面导入下载的监控指标文件

    ![导入监控指标文件](/media/ticdc/ticdc-new-arch-import-grafana.png)

TiCDC 新架构的监控面板主要包括以下部分：

- [**Summary**](#summary-面板)：TiCDC 集群的概要信息
- [**Server**](#server-面板)：TiDB 集群中 TiKV 节点和 TiCDC 节点的概要信息
- [**Log Puller**](#log-puller-面板)：TiCDC Log Puller 模块的详细信息
- [**Event Store**](#event-store-面板)：TiCDC Event Store 模块的详细信息
- [**Sink**](#sink-面板)：TiCDC Sink 模块的详细信息

### Summary 面板

**Summary** 面板示例如下：

![Summary](/media/ticdc/ticdc-new-arch-metric-summary.png)

**Summary** 面板的各指标说明如下：

- Changefeed Checkpoint Lag：同步任务在下游与上游之间的时序差距
- Changefeed ResolvedTs Lag：TiCDC 节点内部处理进度与上游数据库的时序差距
- Upstream Write Bytes/s：上游数据库的写入吞吐量
- TiCDC Input Bytes/s：TiCDC 每秒从上游接收的数据量
- Sink Event Row Count/s：TiCDC 每秒向下游写入的数据行数
- Sink Write Bytes/s：TiCDC 每秒向下游写入的数据量
- Upstream Write Bytes / s：上游数据库的写入吞吐量
- TiCDC Input Bytes / s：TiCDC 每秒从上游接收的数据量
- Sink Event Row Count / s：TiCDC 每秒向下游写入的数据行数
- Sink Write Bytes / s：TiCDC 每秒向下游写入的数据量
- The Status of Changefeeds：各 Changefeed 的状态
- Table Dispatcher Count：各 Changefeed 对应的 Dispatcher 数量
- Memory Quota：Event Collector 内存配额及使用量，使用量过大时会导致限流

### Server 面板

**Server** 面板示例如下：

![Server](/media/ticdc/ticdc-new-arch-metric-server.png)

**Server** 面板的各指标说明如下：

- Uptime：TiKV 节点和 TiCDC 节点已经运行的时间
- Goroutine Count：TiCDC 节点 Goroutine 的个数
- Open FD Count：TiCDC 节点打开的文件句柄个数
- CPU Usage：TiCDC 节点使用的 CPU
- Memory Usage：TiCDC 节点使用的内存
- Ownership History：TiCDC 集群中 Owner 节点的历史记录
- PD Leader History：上游 TiDB 集群中 PD Leader 节点的历史记录
- Build Info：TiCDC 构建信息。
- Log Write Speed：日志写入速度。
- Log Size & Disk Usage：日志大小与磁盘占用。

### Log Puller 面板

**Log Puller** 面板示例如下：

![Log Puller](/media/ticdc/ticdc-new-arch-metric-log-puller.png)

**Log Puller** 面板的各指标说明如下：

- Input Events/s：TiCDC 每秒收到的事件数
- Input Events / s：TiCDC 每秒收到的事件数
- Unresolved Region Request Count ：TiCDC 已经发送但尚未完成的 Region 增量扫描请求数
- Region Request Finish Scan Duration：Region 增量扫描的耗时
- Subscribed Region Count：订阅的 Region 总数
- Memory Quota：Log Puller 内存配额及使用量，使用量过大会导致限流
- Resolved Ts Batch Size (Regions)：单个 Resolved Ts 事件包含的 Region 数量
- Region Event Handle Duration：Region 事件处理耗时。
- Region Event Consume Callback Duration：Region 事件回调消费耗时。
- Dropped Resolve Lock Tasks / s：丢弃的 Resolve Lock 任务速率。

### Event Store 面板

**Event Store** 面板示例如下：

![Event Store](/media/ticdc/ticdc-new-arch-metric-event-store.png)

**Event Store** 面板的各指标说明如下：

- Resolved Ts Lag：Event Store 处理进度与上游数据库的时序差距
- Register Dispatcher StartTs Lag：Dispatcher 注册请求的 StartTs 与当前时间点之间的时序差距
- Subscriptions Resolved Ts Lag：Subscription 处理进度与上游数据库的时序差距
- Subscriptions Data GC Lag：Subscription 数据 GC 进度与当前时间点的时序差距
- Input Event Count/s：Event Store 每秒处理的事件数
- Input Bytes/s：Event Store 每秒处理的数据量
- Write Requests/s：Event Store 每秒执行的写入请求数量
- Write Worker Busy Ratio：Event Store 写线程的 I/O 时间占总运行时间的比例
- Compressed Rows/s：Event Store 每秒压缩的数据行数（仅当行大小超过设定阈值时触发压缩）
- Write Duration：Event Store 写入操作的耗时
- Write Queue Duration：Event Store 写入队列耗时。
- Write Prepare Duration：Event Store 写入准备耗时。
- Write Batch Size：单次写入操作的批量数据大小
- Write Batch Event Count：单次写入批次中包含的行变更数
- Data Size On Disk：Event Store 在磁盘上占用的数据总量
- Data Size In Memory：Event Store 在内存中占用的数据总量
- Scan Requests/s：Event Store 每秒执行的扫描请求数量
- Scan Bytes/s：Event Store 每秒扫描的数据量
- EventStore Resolved Ts Lag ：Event Store 的 Resolved Ts 延迟。
- EventService Resolved Ts Lag ：Event Service 的 Resolved Ts 延迟。
- Input Event Count / s：Event Store 每秒处理的事件数。
- Input Bytes / s：Event Store 每秒处理的数据量。
- Write Requests / s：Event Store 每秒执行的写入请求数量。
- Compressed Rows / s：Event Store 每秒压缩的数据行数。
- Scan Requests / s：Event Store 每秒执行的扫描请求数量。
- Scan Bytes / s：Event Store 每秒扫描的数据量。
- Scan Operation Duration ：Event Store 扫描操作耗时。
- Subscription Num：订阅数量。
- pebble block cache access /s：Pebble block cache 访问次数。
- pebble block cache hit ratio：Pebble block cache 命中率。
- pebble compaction duration seconds：Pebble compaction 耗时。
- pebble flush duration seconds：Pebble flush 耗时。
- pebble compaction bytes：Pebble compaction 数据量。
- pebble level files：Pebble 各层文件数。
- pebble write stall / s：Pebble 写入阻塞速率。

### Sink 面板

**Sink** 面板示例如下：

![Sink](/media/ticdc/ticdc-new-arch-metric-sink.png)

**Sink** 面板的各指标说明如下：

- Output Row Batch Count：Sink 每批次写入 DML 的平均行数。
- Output Row Count (per second)：每秒向下游写入的 DML 行数
- Output DDL Executing Duration：当前节点上对应 Changefeed 执行 DDL Event 的耗时
- Sink Error Count / m：Sink 模块每分钟的报错信息数量
- Output DDL Count / Minutes：当前节点上对应 Changefeed 每分钟执行的 DDL 数量
- Conflict Detect Duration：冲突检测耗时。
- Full Flush Duration：全量 Flush 耗时。
- Backend Flush Duration：后端 Flush 耗时。
- Worker Input Rows / s：Worker 输入行数速率。
- Worker Batch Duration Percentile：Worker 批处理耗时分位数。
- Worker Batch Size Percentile：Worker 批大小分位数。
- Worker Send Message Duration Percentile：Worker 发送消息耗时分位数。
- Kafka Outgoing Bytes：Kafka 发送字节数。
- Kafka Inflight Requests：Kafka 在途请求数。
- Kafka Request Latency：Kafka 请求延迟。
- Kafka Request Rate：Kafka 请求速率。
- Kafka Records Per Request：每次 Kafka 请求的记录数。
- Kafka Producer Compression Ratio：Kafka 生产端压缩比。
- Encoder Group Input Channel Size：Encoder 组输入通道大小。
- Encoder Group Output Channel Size：Encoder 组输出通道大小。
- Claim Check Send Message Count：Claim Check 发送消息数量。
- Claim Check Send Message Duration Percentile：Claim Check 发送消息耗时分位数。
- Worker Send CheckpointTs Message Count：Worker 发送 CheckpointTs 消息数量。
- Worker Encode and Send Checkpoint Message Duration：Worker 编码并发送 Checkpoint 消息耗时。
- Row Affected Count / m：每分钟受影响行数。
- Write Bytes/s：写入字节速率。
- File Count：文件数量。
- Flush duration：Flush 操作耗时。

### 其他面板补充

#### Lag Summary

- Maintainer Checkpoint Lag：Maintainer Checkpoint Lag 相关指标。
- Maintainer Resolved Ts lag：Maintainer Resolved Ts lag 相关指标。
- EventStore Resolved Ts Lag ：EventStore Resolved Ts Lag  相关指标。
- EventService Resolved Ts Lag ：EventService Resolved Ts Lag  相关指标。
- DispatcherManager Checkpoint Lag：DispatcherManager Checkpoint Lag 相关指标。
- DispatcherManager Resolved Ts Lag：DispatcherManager Resolved Ts Lag 相关指标。
- EventCollector Resolved Ts Lag：EventCollector Resolved Ts Lag 相关指标。

#### Dataflow

- Puller Output Events / s：Puller Output Events / s 相关指标。
- Puller Output Event Rows：Puller Output Event Rows 相关指标。
- EventService Output Event Row / s：EventService Output Event Row / s 相关指标。
- EventService Output Event Rows：EventService Output Event Rows 相关指标。
- Event Collector Received Event Rows / s：Event Collector Received Event Rows / s 相关指标。
- Event Collector Received Event Rows：Event Collector Received Event Rows 相关指标。
- Sink Flush Rows / s：Sink Flush Rows / s 相关指标。
- Sink Flush Rows：Sink Flush Rows 相关指标。

#### Changefeed

- Node Table Count：Node Table Count 相关指标。
- Changefeed Table Count：Changefeed Table Count 相关指标。
- GC Time：GC Time 相关指标。
- Changefeed Checkpoint：Changefeed Checkpoint 相关指标。
- Changefeed Resolved Ts：Changefeed Resolved Ts 相关指标。
- Changefeed Checkpoint Lag：Changefeed Checkpoint Lag 相关指标。
- Changefeed Resolved Ts Lag：Changefeed Resolved Ts Lag 相关指标。

#### Lag analyze

- Changefeed Checkpoint Lag：Changefeed Checkpoint Lag 相关指标。
- Changefeed Resolved Ts Lag：Changefeed Resolved Ts Lag 相关指标。
- Eventfeed Error / m：Eventfeed Error / m 相关指标。
- PD Operator / m：PD Operator / m 相关指标。
- TiDB Query Duration：TiDB Query Duration 相关指标。
- TiKV Min Resolved Ts Lag：TiKV Min Resolved Ts Lag 相关指标。
- Sink Write Rows / s：Sink Write Rows / s 相关指标。
- Sink Write Duration：Sink Write Duration 相关指标。
- TiKV Scan Tasks / m：TiKV Scan Tasks / m 相关指标。
- TiKV Scan Region Time / m：TiKV Scan Region Time / m 相关指标。
- TiKV Leader Change：TiKV Leader Change 相关指标。
- TiKV Admin Apply / s：TiKV Admin Apply / s 相关指标。
- TiKV Advance Resolved Ts / s：TiKV Advance Resolved Ts / s 相关指标。
- TiKV Unresolved Region Count：TiKV Unresolved Region Count 相关指标。
- TiKV Check Leader Region Count Percentile：TiKV Check Leader Region Count Percentile 相关指标。
- TiKV Advance Resolved Ts Fail / m：TiKV Advance Resolved Ts Fail / m 相关指标。
- TiKV Check Leader Duration Percentile：TiKV Check Leader Duration Percentile 相关指标。
- TiKV CDC Incremental Scan Long Duration Region Count：TiKV CDC Incremental Scan Long Duration Region Count 相关指标。

#### Coordinator

- Changefeed Status：Changefeed Status 相关指标。
- Coordinator Operator Cost Duration：Coordinator Operator Cost Duration 相关指标。
- Coordinator History：Coordinator History 相关指标。

#### Maintainer

- Maintainer Checkpoint Lag：Maintainer Checkpoint Lag 相关指标。
- Maintainer Resolved Ts Lag：Maintainer Resolved Ts Lag 相关指标。
- Changefeed Maintainer Count：Changefeed Maintainer Count 相关指标。
- Maintainer Handle Event Duration：Maintainer Handle Event Duration 相关指标。
- Maintainer Event Channel Length：Maintainer Event Channel Length 相关指标。

#### Schema Store

- Resolved Ts Lag：Resolved Ts Lag 相关指标。
- Register Table Num：Register Table Num 相关指标。
- Get Table Info Count / s：Get Table Info Count / s 相关指标。
- Get Table Info Duration：Get Table Info Duration 相关指标。
- Shared Column Schema Count：Shared Column Schema Count 相关指标。
- Wait Resolved Ts Duration：Wait Resolved Ts Duration 相关指标。

#### Event Service

- Scan window interval：Scan window interval 相关指标。
- Scan window base ts：Scan window base ts 相关指标。
- Event Service Scan Duration：Event Service Scan Duration 相关指标。
- Event Service Scan Duration：Event Service Scan Duration 相关指标。
- Event Service Scanned Entry Count：Event Service Scanned Entry Count 相关指标。
- Event Service Scanned Transaction Count：Event Service Scanned Transaction Count 相关指标。
- Event Service Scanned Entry Bytes / s：Event Service Scanned Entry Bytes / s 相关指标。
- Event Service Scanned Transaction Bytes / s：Event Service Scanned Transaction Bytes / s 相关指标。
- Event Service Finished Scan Task Count：Event Service Finished Scan Task Count 相关指标。
- Event Service Resolved Ts Lag：Event Service Resolved Ts Lag 相关指标。
- Event Service Pending Scan Task：Event Service Pending Scan Task 相关指标。
- Event Service Dispatcher Status：Event Service Dispatcher Status 相关指标。
- Event Service Available Memory：Event Service Available Memory 相关指标。
- Event Service Channel Size：Event Service Channel Size 相关指标。
- Scanned Entry Count / s：Scanned Entry Count / s 相关指标。
- Reset Dispatcher / s：Reset Dispatcher / s 相关指标。
- Skip Scan Count / s：Skip Scan Count / s 相关指标。
- Intterrupt Scan Count / s：Intterrupt Scan Count / s 相关指标。
- Decode DMLEvent Duration：Decode DMLEvent Duration 相关指标。
- EventService Output Different DML Event Types / s：EventService Output Different DML Event Types / s 相关指标。

#### Message Center

- Sent Message Count Per Second：Sent Message Count Per Second 相关指标。
- Slow Message Count：Slow Message Count 相关指标。

#### Dispatcher

- Table Dispatcher Manager Count：Table Dispatcher Manager Count 相关指标。
- Table Dispatcher Count：Table Dispatcher Count 相关指标。
- Table Trigger Dispatcher Count：Table Trigger Dispatcher Count 相关指标。
- Create Dispatcher Duration：Create Dispatcher Duration 相关指标。
- Dispatcher Request Handle Result：Dispatcher Request Handle Result 相关指标。
- Event Collector Registered Dispatcher Count：Event Collector Registered Dispatcher Count 相关指标。
- Event Collector Received Resolved Ts / s：Event Collector Received Resolved Ts / s 相关指标。
- Event Collector Handle Message Duration：Event Collector Handle Message Duration 相关指标。
- Block Statuses Channel Length：Block Statuses Channel Length 相关指标。
- Block Status Request Queue Length：Block Status Request Queue Length 相关指标。
- Event Collector Receive Event Lag：Event Collector Receive Event Lag 相关指标。

#### Dynamic Stream

- DS Input Channel Length：DS Input Channel Length 相关指标。
- DS Pending Queue Length：DS Pending Queue Length 相关指标。
- P99 - Batch Count：P99 - Batch Count 相关指标。
- Avg - Batch Count：Avg - Batch Count 相关指标。
- P99 - Batch Bytes：P99 - Batch Bytes 相关指标。
- Avg - Batch Bytes：Avg - Batch Bytes 相关指标。
- P99 - Batch Duration：P99 - Batch Duration 相关指标。
- Avg - Batch Duration：Avg - Batch Duration 相关指标。

#### Scheduler

- Table Replication State：Table Replication State 相关指标。
- Schedule Tasks：Schedule Tasks 相关指标。
- Span Count：Span Count 相关指标。
- Table Count：Table Count 相关指标。
- Operator Count：Operator Count 相关指标。
- Total Operator Count：Total Operator Count 相关指标。
- Split Span Check Duration：Split Span Check Duration 相关指标。
- Operator Cost Duration：Operator Cost Duration 相关指标。
- Slowest Table Checkpoint：Slowest Table Checkpoint 相关指标。
- Slowest Table ID：Slowest Table ID 相关指标。
- Slowest Table Replication State：Slowest Table Replication State 相关指标。
- Slowest Table Resolved Ts：Slowest Table Resolved Ts 相关指标。

#### Active Active

- Conflict Skip Rows / s：Conflict Skip Rows / s 相关指标。

#### TiKV

- gRPC Message Count：gRPC Message Count 相关指标。
- CDC Network Traffic：CDC Network Traffic 相关指标。
- CDC CPU：CDC CPU 相关指标。
- CDC Memory Quota：CDC Memory Quota 相关指标。
- Captured Region Count：Captured Region Count 相关指标。
- Initial Scan Tasks Status：Initial Scan Tasks Status 相关指标。
- Incremental Scan Duration Percentile：Incremental Scan Duration Percentile 相关指标。
- Initial Scan Duration：Initial Scan Duration 相关指标。
- Incremental Scan Sink Duration Percentile：Incremental Scan Sink Duration Percentile 相关指标。
- CDC Total Scan Bytes：CDC Total Scan Bytes 相关指标。
- Incremental Scan Speed：Incremental Scan Speed 相关指标。
- Incremental Scan Disk Speed：Incremental Scan Disk Speed 相关指标。
- Min Resolved Ts：Min Resolved Ts 相关指标。
- Resolved Ts Lag Duration Percentile：Resolved Ts Lag Duration Percentile 相关指标。
- Old Value Cache Hit：Old Value Cache Hit 相关指标。
- Min Resolved Region：Min Resolved Region 相关指标。
- Old Value Seek Duration：Old Value Seek Duration 相关指标。
- Old Value Cache Size：Old Value Cache Size 相关指标。
- Old Value Seek Duration：Old Value Seek Duration 相关指标。
- Old Value Seek Operation：Old Value Seek Operation 相关指标。

#### Redo

- Redo Fsync Duration：Redo Fsync Duration 相关指标。
- Redo Flushall Duration：Redo Flushall Duration 相关指标。
- Redo Write Log Duration：Redo Write Log Duration 相关指标。
- Redo Flush Log Duration：Redo Flush Log Duration 相关指标。
- Redo Write Rows / s：Redo Write Rows / s 相关指标。
- Redo Write Bytes / s：Redo Write Bytes / s 相关指标。
- Worker Busy Ratio：Worker Busy Ratio 相关指标。
- Memory Quota：Memory Quota 相关指标。

#### Runtime $runtime_instance

- Memory Usage：Memory Usage 相关指标。
- Estimated Live Objects：Estimated Live Objects 相关指标。
- GC STW Duration (last 256 GC cycles)：GC STW Duration (last 256 GC cycles) 相关指标。
- Allocator Throughput：Allocator Throughput 相关指标。

#### Pulsar Sink

- Pulsar Published DDL Schema Count：Pulsar Published DDL Schema Count 相关指标。
- Pulsar Published DDL Schema Success：Pulsar Published DDL Schema Success 相关指标。
- Pulsar Published DDL Schema Fail：Pulsar Published DDL Schema Fail 相关指标。
- Pulsar Published DML Schema Count：Pulsar Published DML Schema Count 相关指标。
- Pulsar Published DML Schema Success：Pulsar Published DML Schema Success 相关指标。
- Pulsar Published DML Schema Fail：Pulsar Published DML Schema Fail 相关指标。
- Pulsar Client Bytes Published：Pulsar Client Bytes Published 相关指标。
- Pulsar Client Connections Opened：Pulsar Client Connections Opened 相关指标。
- Pulsar Client RPC Count：Pulsar Client RPC Count 相关指标。
- Pulsar Client Producer Latency：Pulsar Client Producer Latency 相关指标。
- Pulsar Client Producer RPC Latency：Pulsar Client Producer RPC Latency 相关指标。
- Pulsar Client Producer Pending Messages：Pulsar Client Producer Pending Messages 相关指标。
- Pulsar Client Producer Pending Messages：Pulsar Client Producer Pending Messages 相关指标。

#### DDL

- Output DDL Executing Duration：Output DDL Executing Duration 相关指标。
- Sink Running DDL Count：Sink Running DDL Count 相关指标。
- Maintainer Blocking DDL Count：Maintainer Blocking DDL Count 相关指标。
- Sink DDL Count / m：Sink DDL Count / m 相关指标。
- Handle DDL Duration：Handle DDL Duration 相关指标。

## TiCDC 老架构监控指标

使用 TiUP 部署 TiDB 集群时，一键部署的监控系统面板包含 [TiCDC 老架构](/ticdc/ticdc-classic-architecture.md)监控面板。TiCDC 老架构主要监控面板说明如下：

- [**Server**](#server-面板)：TiDB 集群中 TiKV 节点和 TiCDC 节点的概要信息
- [**Changefeed**](#changefeed-面板)：TiCDC 同步任务的详细信息
- [**Events**](#events-面板)：TiCDC 内部数据流转的详细信息
- [**TiKV**](#tikv-面板)：TiKV 中和 TiCDC 相关的详细信息

### Server 面板

**Server** 面板示例如下：

![TiCDC Dashboard - Server metrics](/media/ticdc/ticdc-dashboard-server.png)

**Server** 面板的各指标说明如下：

- Uptime：TiKV 节点和 TiCDC 节点已经运行的时间
- Goroutine count：TiCDC 节点 Goroutine 的个数
- Open FD count：TiCDC 节点打开的文件句柄个数
- Ownership：TiCDC 集群中节点的当前状态
- Ownership history：TiCDC 集群中 Owner 节点的历史记录
- CPU usage：TiCDC 节点使用的 CPU
- Memory usage：TiCDC 节点使用的内存

### Changefeed 面板

**Changefeed** 面板示例如下：

![TiCDC Dashboard - Changefeed metrics 1](/media/ticdc/ticdc-dashboard-changefeed-1.png)

- Changefeed table count：一个同步任务中分配到各个 TiCDC 节点同步的数据表个数
- Processor resolved ts：TiCDC 节点内部状态中已同步的时间点
- Table resolved ts：同步任务中各数据表的同步进度
- Changefeed checkpoint：同步任务同步到下游的进度，正常情况下绿柱应和黄线相接
- PD etcd requests/s：TiCDC 节点每秒向 PD 读写数据的次数
- Exit error count/m：每分钟内导致同步中断的错误发生次数
- Changefeed checkpoint lag：同步任务上下游数据的进度差（以时间计算）
- Processor resolved ts lag：TiCDC 节点内部同步状态与上游的进度差（以时间计算）

![TiCDC Dashboard - Changefeed metrics 2](/media/ticdc/ticdc-dashboard-changefeed-2.png)

- Sink write duration：TiCDC 将一个事务的更改写到下游的耗时直方图
- Sink write duration percentile：每秒钟中 95%、99% 和 99.9% 的情况下，TiCDC 将一个事务的更改写到下游所花费的时间
- Flush sink duration：TiCDC 异步刷写数据入下游的耗时直方图
- Flush sink duration percentile：每秒钟中 95%、99% 和 99.9% 的情况下，TiCDC 异步刷写数据入下游所花费的时间

![TiCDC Dashboard - Changefeed metrics 3](/media/ticdc/ticdc-dashboard-changefeed-3.png)

- MySQL sink conflict detect duration：MySQL 写入冲突检测耗时直方图
- MySQL sink conflict detect duration percentile：每秒钟中 95%、99% 和 99.9% 的情况下，MySQL 写入冲突检测耗时
- MySQL sink worker load：TiCDC 节点中写 MySQL 线程的负载情况

![TiCDC Dashboard - Changefeed metrics 4](/media/ticdc/ticdc-dashboard-changefeed-4.png)

- Changefeed catch-up ETA：同步完上游写入的数据所需时间的估计值。当上游的写入速度大于 TiCDC 同步速度时，该值可能会异常的大。（由于 TiCDC 的同步速度受到较多因素制约，因此该值仅供参考，不能完全代表实际所需的同步时间。）

### Events 面板

**Events** 面板示例如下：

![TiCDC Dashboard - Events metrics 2](/media/ticdc/ticdc-dashboard-events-1.png)
![TiCDC Dashboard - Events metrics 2](/media/ticdc/ticdc-dashboard-events-2.png)
![TiCDC Dashboard - Events metrics 2](/media/ticdc/ticdc-dashboard-events-3.png)

**Events** 面板的各指标说明如下：

- Eventfeed count：TiCDC 节点中 Eventfeed RPC 的个数
- Event size percentile：每秒钟中 95% 和 99.9% 的情况下，TiCDC 收到的来自 TiKV 的数据变更消息大小
- Eventfeed error/m：TiCDC 节点中每分钟 Eventfeed RPC 遇到的错误个数
- KV client receive events/s：TiCDC 节点中 KV client 模块每秒收到来自 TiKV 的数据变更个数
- Puller receive events/s：TiCDC 节点中 Puller 模块每秒收到来自 KV client 模块的数据变更个数
- Puller output events/s：TiCDC 节点中 Puller 模块每秒输出到 Sorter 模块的数据变更个数
- Sink flush rows/s：TiCDC 节点每秒写到下游的数据变更的个数
- Puller buffer size：TiCDC 节点中缓存在 Puller 模块中的数据变更个数
- Entry sorter buffer size：TiCDC 节点中缓存在 Sorter 模块中的数据变更个数
- Processor/Mounter buffer size：TiCDC 节点中缓存在 Processor 模块和 Mounter 模块中的数据变更个数
- Sink row buffer size：TiCDC 节点中缓存在 Sink 模块中的数据变更个数
- Entry sorter sort duration：TiCDC 节点对数据变更进行排序的耗时直方图
- Entry sorter sort duration percentile：每秒钟中 95%，99% 和 99.9% 的情况下，TiCDC 排序数据变更所花费的时间
- Entry sorter merge duration：TiCDC 节点合并排序后的数据变更的耗时直方图
- Entry sorter merge duration percentile：每秒钟中 95%，99% 和 99.9% 的情况下，TiCDC 合并排序后的数据变更所花费的时间
- Mounter unmarshal duration：TiCDC 节点解码数据变更的耗时直方图
- Mounter unmarshal duration percentile：每秒钟中 95%，99% 和 99.9% 的情况下，TiCDC 解码数据变更所花费的时间
- KV client dispatch events/s：TiCDC 节点内部 KV client 模块每秒分发数据变更的个数
- KV client batch resolved size：TiKV 批量发给 TiCDC 的 resolved ts 消息的大小

### TiKV 面板

**TiKV** 面板示例如下：

![TiCDC Dashboard - TiKV metrics 1](/media/ticdc/ticdc-dashboard-tikv-1.png)
![TiCDC Dashboard - TiKV metrics 2](/media/ticdc/ticdc-dashboard-tikv-2.png)

**TiKV** 面板的各指标说明如下：

- CDC endpoint CPU：TiKV 节点上 CDC endpoint 线程使用的 CPU
- CDC worker CPU：TiKV 节点上 CDC worker 线程使用的 CPU
- Min resolved ts：TiKV 节点上最小的 resolved ts
- Min resolved region：TiKV 节点上最小的 resolved ts 的 Region ID
- Resolved ts lag duration percentile：TiKV 节点上最小的 resolved ts 与当前时间的差距
- Initial scan duration：TiKV 节点与 TiCDC 建立链接时增量扫的耗时直方图
- Initial scan duration percentile：每秒钟中 95%、99% 和 99.9% 的情况下，TiKV 节点增量扫的耗时
- Memory without block cache：TiKV 节点在减去 RocksDB block cache 后使用的内存
- CDC pending bytes in memory：TiKV 节点中 CDC 模块使用的内存
- Captured region count：TiKV 节点上捕获数据变更的 Region 个数
