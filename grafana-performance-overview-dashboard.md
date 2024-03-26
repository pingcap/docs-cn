---
title: Performance Overview 面板重要监控指标详解
summary: 本文介绍 Performance Overview 面板上监控指标的含义。
---

# Performance Overview 面板重要监控指标详解

使用 TiUP 部署 TiDB 集群时，你可以一键部署监控系统 (Prometheus & Grafana)。监控架构参见 [TiDB 监控框架概述](/tidb-monitoring-framework.md)。

目前 Grafana Dashboard 整体分为 PD、TiDB、TiKV、Node\_exporter、Overview、Performance\_overview 等。

Performance Overview Dashboard 按总分结构对 TiDB、TiKV、PD 的性能指标进行编排组织，包含了以下三部分内容：

- 总的概览：数据库时间和 SQL 执行时间概览。通过颜色优化法，你可以快速识别数据库负载特征和性能瓶颈。
- 资源负载：关键指标和资源利用率，包含数据库 QPS、应用和数据库的连接信息和请求命令类型、数据库内部 TSO 和 KV 请求 OPS、TiDB 和 TiKV 的资源使用概况。
- 自上而下的延迟分解：Query 延迟和连接空闲时间对比、Query 延迟分解、execute 阶段 TSO 请求和 KV 请求的延迟、TiKV 内部写延迟的分解等。

借助 Performance Overview Dashboard，你可以高效地进行性能分析，确认用户响应时间的瓶颈是否在数据库中。如果数据库是整个系统的瓶颈，通过数据库时间概览和 SQL 延迟的分解，定位数据库内部的瓶颈点，并进行针对性的优化。详情请参考 [TiDB 性能分析和优化方法](/performance-tuning-methods.md)。

以下为 Performance Overview Dashboard 监控说明：

## Performance Overview

### Database Time by SQL Type

- database time: 每秒的总数据库时间
- sql_type: 每种 SQL 语句每秒消耗的数据库时间

### Database Time by SQL Phase

- database time: 每秒的总数据库时间
- get token/parse/compile/execute: 4 个 SQL 处理阶段每秒消耗的数据库时间

execute 执行阶段为绿色，其他三个阶段偏红色系，如果非绿色的颜色占比明显，意味着在执行阶段之外数据库消耗了过多时间，需要进一步分析根源。

### SQL Execute Time Overview

- execute time: execute 阶段每秒消耗的数据库时间
- tso_wait: execute 阶段每秒同步等待 TSO 的时间
- kv request type: execute 阶段每秒等待每种 KV 请求类型的时间，总的 KV request 等待时间可能超过 execute time，因为 KV request 是并发的。
- tiflash_mpp: execute 阶段每秒 TiFlash 请求处理时间。

绿色系标识代表常规的写 KV 请求（例如 Prewrite 和 Commit），蓝色系标识代表常规的读 KV 请求，紫色系标识代表 TiFlash MPP 请求，其他色系标识需要注意的问题。例如，悲观锁加锁请求为红色，TSO 等待为深褐色。如果非蓝色系或者非绿色系占比明显，意味着执行阶段存在异常的瓶颈。例如，当发生严重锁冲突时，红色的悲观锁时间会占比明显；当负载中 TSO 等待的消耗时间过长时，深褐色会占比明显。

### QPS

QPS：按 `SELECT`、`INSERT`、`UPDATE` 等类型统计所有 TiDB 实例上每秒执行的 SQL 语句数量

### CPS By Type

CPS By Type：按照类型统计所有 TiDB 实例每秒处理的命令数（Command Per Second）

### Queries Using Plan Cache OPS

- avg-hit：所有 TiDB 实例每秒执行计划缓存的命中次数
- avg-miss：所有 TiDB 实例每秒执行计划缓存的未命中次数

`avg-hit + avg-miss` 等于 StmtExecute 每秒执行次数。

### KV/TSO Request OPS

- kv request total: 所有 TiDB 实例每秒总的 KV 请求数量
- kv request by type: 按 `Get`、`Prewrite`、 `Commit` 等类型统计在所有 TiDB 实例每秒的请求数据
- tso - cmd：在所有 TiDB 实例每秒 tso cmd 的请求数量
- tso - request：在所有 TiDB 实例每秒 tso request 的请求数量

通常 tso - cmd 除以 tso - request 等于平均请求的 batch 大小。

### KV Request Time By Source

- kv request total time: 所有 TiDB 实例每秒总的 KV 和 TiFlash 请求处理时间。

- 每种 KV 请求和请求来源组成柱状堆叠图，`external` 标识正常业务的请求，`internal` 标识内部活动的请求（比如 DDL、auto analyze 等请求）。

### TiDB CPU

- avg：所有 TiDB 实例平均 CPU 利用率
- delta：所有 TiDB 实例中最大 CPU 利用率减去所有 TiDB 实例中最小 CPU 利用率
- max：所有 TiDB 实例中最大 CPU 利用率

### TiKV CPU/IO MBps

- CPU-Avg：所有 TiKV 实例平均 CPU 利用率
- CPU-Delta：所有 TiKV 实例中最大 CPU 利用率减去所有 TiKV 实例中最小 CPU 利用率
- CPU-MAX：所有 TiKV 实例中最大 CPU 利用率
- IO-Avg：所有 TiKV 实例平均 MBps
- IO-Delta：所有 TiKV 实例中最大 MBps 减去所有 TiKV 实例中最小 MBps
- IO-MAX：所有 TiKV 实例中最大 MBps

### Duration

- Duration：执行时间解释

    - 从客户端网络请求发送到 TiDB，到 TiDB 执行结束后返回给客户端的时间。一般情况下，客户端请求都是以 SQL 语句的形式发送，但也可以包含 `COM_PING`、`COM_SLEEP`、`COM_STMT_FETCH`、`COM_SEND_LONG_DATA` 之类的命令执行时间。
    - 由于 TiDB 支持 Multi-Query，因此，客户端可以一次性发送多条 SQL 语句，如 `select 1; select 1; select 1;`。此时的执行时间是所有 SQL 语句执行完成的总时间。

- avg：所有请求命令的平均执行时间
- 99： 所有请求命令的 P99 执行时间
- avg by type：按 `SELECT`、`INSERT`、`UPDATE` 类型统计所有 TiDB 实例上所有请求命令的平均执行时间

### Connection Idle Duration

Connection Idle Duration 指空闲连接的持续时间。

- avg-in-txn：处于事务中，空闲连接的平均持续时间
- avg-not-in-txn：没有处于事务中，空闲连接的平均持续时间
- 99-in-txn：处于事务中，空闲连接的 P99 持续时间

### Connection Count

- total：所有 TiDB 节点的总连接数
- active connections：所有 TiDB 节点的总活跃连接数
- tidb-{node-number}-peer：各个 TiDB 节点的连接数
- disconnection/s：集群每秒断开连接的数量
- 99-not-in-txn：没有处于事务中，空闲连接的 P99 持续时间

### Parse Duration、Compile Duration 和 Execute Duration

- Parse Duration：SQL 语句解析耗时统计
- Compile Duration：将解析后的 SQL AST 编译成执行计划的耗时
- Execution Duration：执行 SQL 语句执行计划耗时

这三个时间指标均包含均所有 TiDB 实例的平均值和 P99 值。

### Avg TiDB KV Request Duration

按 `Get`、`Prewrite`、 `Commit` 等类型统计在所有 TiDB 实例 KV 请求的平均执行时间。

### Avg TiKV GRPC Duration

按 `get`、`kv_prewrite`、 `kv_commit` 等类型统计所有 TiKV 实例对 gRPC 请求的平均执行时间。

### PD TSO Wait/RPC Duration

- wait - avg：所有 TiDB 实例等待从 PD 返回 TSO 的平均时间
- rpc - avg：所有 TiDB 实例从向 PD 发送获取 TSO 的请求到接收到 TSO 的平均耗时
- wait - 99：所有 TiDB 实例等待从 PD 返回 TSO 的 P99 时间
- rpc - 99：所有 TiDB 实例从向 PD 发送获取 TSO 的请求到接收到 TSO 的 P99 耗时

### Storage Async Write Duration、Store Duration 和 Apply Duration

- Storage Async Write Duration：异步写所花费的时间
- Store Duration：异步写 Store 步骤所花费的时间
- Apply Duration：异步写 Apply 步骤所花费的时间

这三个时间指标都包含所有 TiKV 实例的平均值和 P99 值

平均 Storage async write duration = 平均 Store Duration + 平均 Apply Duration

### Append Log Duration、Commit Log Duration 和 Apply Log Duration

- Append Log Duration：Raft append 日志所花费的时间
- Commit Log Duration：Raft commit 日志所花费的时间
- Apply Log Duration：Raft apply 日志所花费的时间

这三个时间指标均包含所有 TiKV 实例的平均值和 P99 值。

### 图例

![performance overview](/media/performance/grafana_performance_overview.png)

## TiFlash

- CPU：每个 TiFlash 实例 CPU 的使用率
- Memory：每个 TiFlash 实例内存的使用情况
- IO utilization：每个 TiFlash 实例的 IO 使用率
- MPP Query count：每个 TiFlash 实例每秒 MPP 查询数量
- Request QPS：所有 TiFlash 实例收到的 coprocessor 请求数量。

    - `batch`：batch 请求数量
    - `batch_cop`：batch 请求中的 coprocessor 请求数量
    - `cop`：直接通过 coprocessor 接口发送的 coprocessor 请求数量
    - `cop_dag`：所有 coprocessor 请求中 dag 请求数量
    - `super_batch`：开启 super batch 特性的请求数量
- Executor QPS：所有 TiFlash 实例收到的请求中，每种 dag 算子的数量，其中 `table_scan` 是扫表算子，`selection` 是过滤算子，`aggregation` 是聚合算子，`top_n` 是 TopN 算子，`limit` 是 limit 算子
- Request Duration Overview：每秒所有 TiFlash 实例所有请求类型总处理时间的堆叠图
- Request Duration：所有 TiFlash 实例每种 MPP 和 coprocessor 请求类型的总处理时间，此时间为接收到该 coprocessor 请求至请求应答完毕的时间，包含平均和 P99 处理延迟
- Request Handle Duration：所有 TiFlash 实例每种 MPP 和 coprocessor 请求的处理时间，此时间为该 coprocessor 请求从开始执行到结束的时间，包含平均和 P99 延迟
- Raft Wait Index Duration：所有 TiFlash 实例在进行 wait_index 消耗的时间，即拿到 read_index 请求后，等待本地的 Region index >= read_index 所花费的时间
- Raft Batch Read Index Duration：所有 TiFlash 实例在进行 read_index 消耗的时间，主要消耗在于和 Region leader 的交互和重试时间
- Write Throughput By Instance：每个实例写入数据的吞吐量，包括 apply Raft 数据日志以及 Raft 快照的写入吞吐量
- Write flow：所有 TiFlash 实例磁盘写操作的流量
- Read flow：所有 TiFlash 实例磁盘读操作的流量

## CDC

- CPU usage：TiCDC 节点的 CPU 使用情况
- Memory usage：TiCDC 节点的内存使用情况
- Goroutine count：TiCDC 节点 Goroutine 的个数
- Changefeed checkpoint lag：同步任务上下游数据的进度差（以时间单位秒计算）
- Changefeed resolved ts lag：TiCDC 节点内部同步状态与上游的进度差（以时间单位秒计算）
- The status of changefeeds：changefeed 的状态

    - 0：Normal
    - 1：Error
    - 2：Failed
    - 3：Stopped
    - 4：Finished
    - -1：Unknown
- Puller output events/s：TiCDC 节点中 Puller 模块每秒输出到 Sorter 模块的数据变更行数
- Sorter output events/s：TiCDC 节点中 Sorter 模块每秒输出到 Mounter 模块的行数
- Mounter output events/s：TiCDC 节点中 Mounter 模块每秒输出到 Sink 模块的行数
- Table sink output events/s：TiCDC 节点中 Table Sorter 模块每秒输出到 Sink 模块的行数
- SinkV2 - Sink flush rows/s：TiCDC 节点中 Sink 模块每秒输出到下游的行数
- Transaction Sink Full Flush Duration：TiCDC 节点中 MySQL Sink 写下游事务的平均延迟和 p999 延迟
- MQ Worker Send Message Duration Percentile：下游为 Kafka 时 MQ worker 发送消息的延迟
- Kafka Outgoing Bytes：MQ Workload 写下游事务的流量
