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

[TiCDC 新架构](/ticdc/ticdc-architecture.md)的监控面板 **TiCDC-New-Arch** 暂时未集成到 TiUP 中。要在 Grafana 中查看相关监控信息，你需要手动导入 TiCDC 监控指标文件：

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

### Log Puller 面板

**Log Puller** 面板示例如下：

![Log Puller](/media/ticdc/ticdc-new-arch-metric-log-puller.png)

**Log Puller** 面板的各指标说明如下：

- Input Events/s：TiCDC 每秒收到的事件数
- Unresolved Region Request Count：TiCDC 已经发送但尚未完成的 Region 增量扫描请求数
- Region Request Finish Scan Duration：Region 增量扫描的耗时
- Subscribed Region Count：订阅的 Region 总数
- Memory Quota：Log Puller 内存配额及使用量，使用量过大会导致限流
- Resolved Ts Batch Size (Regions)：单个 Resolved Ts 事件包含的 Region 数量

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
- Write Batch Size：单次写入操作的批量数据大小
- Write Batch Event Count：单次写入批次中包含的行变更数
- Data Size On Disk：Event Store 在磁盘上占用的数据总量
- Data Size In Memory：Event Store 在内存中占用的数据总量
- Scan Requests/s：Event Store 每秒执行的扫描请求数量
- Scan Bytes/s：Event Store 每秒扫描的数据量

### Sink 面板

**Sink** 面板示例如下：

![Sink](/media/ticdc/ticdc-new-arch-metric-sink.png)

**Sink** 面板的各指标说明如下：

- Output Row Batch Count：Sink 每批次写入 DML 的平均行数。
- Output Row Count (per second)：每秒向下游写入的 DML 行数
- Output DDL Executing Duration：当前节点上对应 Changefeed 执行 DDL Event 的耗时
- Sink Error Count / m：Sink 模块每分钟的报错信息数量
- Output DDL Count / Minutes：当前节点上对应 Changefeed 每分钟执行的 DDL 数量

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
