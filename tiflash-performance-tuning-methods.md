---
title: TiFlash 性能分析和优化方法
summary: 本文介绍了 Performance Overview 仪表盘中 TiFlash 部分，帮助 TiDB 用户了解和监控 TiFlash MPP 工作负载。
---

# TiFlash 性能分析和优化方法
本文介绍 TiFlash MPP 资源使用率和关键的性能指标，用户通过 TiFlash 仪表盘，可以用来监控和评估 TiFlash 集群性能。

## TiFlash 集群资源利用率

通过以下三个数据，可以快速判断 TiFlash 集群的资源使用率

- CPU: 每个 TiFlash 实例 CPU 的使用率
- Memory：每个 TiFlash 实例内存的使用情况
- IO utilization：每个 TiFlash 实例的 IO 使用率


**示例：CH 负载资源使用率 **

- 该 TiFlash 集群包含两个节点，每个节点配置为 16 核心、48G 内存。当 CH 负载运行时，CPU 利用率最高可达到 1500%，内存占用最大可达 20GB，IO 利用率达到 91%。这表明 TiFlash 节点资源接近饱和状态。

![CH-TiFlash-MPP](/media/performance/tiflash/ch-2tiflash-op.png)

## TiFlash 关键指标

### 吞吐指标
- MPP Query count: 每个 TiFlash 实例每秒 MPP 查询数量
- Request QPS: 所有 TiFlash 实例收到的 coprocessor 请求数量。
    - `batch`：batch 请求数量
    - `batch_cop`：batch 请求中的 coprocessor 请求数量
    - `cop`：直接通过 coprocessor 接口发送的 coprocessor 请求数量
    - `cop_dag`：所有 coprocessor 请求中 dag 请求数量
    - `super_batch`：开启 super batch 特性的请求数量
- Executor QPS：所有 TiFlash 实例收到的请求中，每种 dag 算子的数量，其中 `table_scan` 是扫表算子，`selection` 是过滤算子，`aggregation` 是聚合算子，`top_n` 是 TopN 算子，`limit` 是 limit 算子

### 延迟指标
- Request Duration Overview: 每秒所有 TiFlash 实例处理所有请求类型的总时长堆叠图。
  - 如果请求类型为 mpp_establish_conn 和 run_mpp_task，说明 SQL 语句的执行已经完全下推到 TiFlash 上进行，这是 TiFlash 最常见的服务类型。
  - 如果请求类型为 Cop，说明整个语句并没有完全下推到 TiFlash，通常 TiDB 会将全表扫描算子下推到 TiFlash 上进行数据访问和过滤。在堆叠图中，如果 Cop 占据主导地位，需要仔细权衡是否合理。
    - 如果 SQL 访问的数据量很大，优化器可能根据成本模型估算 TiFlash 全表扫描的成本更低。
    - 如果表结构缺少合适的索引，将查询下推到 TiFlash 上是一种无奈之举。在这种情况下，通过索引优化或使用 TiKV 访问数据可能更加高效。

- Request Duration: 所有 TiFlash 实例每种 MPP 和 coprocessor 请求类型的总处理时间，包含平均和 P99 处理延迟。
- Request Handle Duration：所有 TiFlash 实例 MPP 和 coprocessor 请求的处理时间，此时间为该 coprocessor 请求从开始执行到结束的时间，包含平均和 P99 延迟

**示例 1 ：TiFlash MPP 请求处理时间概览 **

在此负载中，run_mpp_task 和 mpp_establish_conn 请求的处理时间占比最高，表明大部分请求都是完全下推到 TiFlash 上执行的 MPP 任务。

而 Cop 请求处理时间占比较小，说明存在一部分请求是通过 Cop 下推到 TiFlash 上进行数据访问和过滤的。
![CH-TiFlash-MPP](/media/performance/tiflash/ch-2tiflash-op.png)
  
**示例 2 ：TiFlash Cop 请求处理时间占比高 **

在此负载中，Cop 请求的处理时间占比最高，可以通过查看 SQL 执行计划来确认 Cop 请求产生的原因。
![Cop](/media/performance/tiflash/tiflash_request_duration_by_type.png)
  
### Raft 相关指标
- Raft Wait Index Duration：所有 TiFlash 实例等待本地 Region index >= read_index 所花费的时间，即进行 wait_index 操作的延迟。如果 Wait Index 延迟过高，这意味着 TiKV 和 TiFlash 之间数据同步存在明显的延迟，通常可能是以下原因导致的：
  - TiKV 资源过载
  - TiFlash 资源过载，特别是 IO 资源
  - TiKV 和 TiFlash 之间存在网络瓶颈
- Raft Batch Read Index Duration：所有 TiFlash 实例 Read Index 的延迟。如果该指标过高，说明 TiFlash 和 TiKV 之间的交互速度较慢，可能的原因包括：
  - TiFlash 资源过载
  - TiKV 资源过载
  - TiFlash 和 TiKV 之间存在网络瓶颈

### IO 流量指标
- Write Throughput By Instance：每个 TiFlash 实例写入数据的吞吐量，包括 apply Raft 数据日志以及 Raft 快照的写入吞吐量
- Write flow：所有 TiFlash 实例磁盘写操作的流量
  - File Descriptor：TiFlash 所使用的的 DeltaTree 存储引擎的稳定层
  - Page:  指 Pagestore，TiFlash 所使用的的 DeltaTree 存储引擎的 Delta 变更层
- Read flow：所有 TiFlash 实例磁盘读操作的流量
  - File Descriptor：TiFlash 所使用的的 DeltaTree 存储引擎的稳定层
  - Page:  指 Pagestore，TiFlash 所使用的的 DeltaTree 存储引擎的 Delta 变更层
  
Read flow 加上 Write flow，除以 总的Write Throughput By Instance, 为整个 TiFlash 集群的写放大倍数


**示例 1 ：CH 负载 OP 环境 Raft 和 IO 指标 **

该 TiFlash 集群的 Raft Wait Index 和 Raft Batch Read Index 99 分位数较高，分别为 3.24 秒和 753 毫秒。这是因为该集群的 TiFlash 负载较高，数据同步存在延迟。

该集群包含两个 TiFlash 节点，每秒 TiKV 同步到 TiFlash 的增量数据约为 28MB。稳定层(File Descriptor)的文件描述符最大写流量为 939MB/s，最大读流量为 1.1 GiB/s，而 Delta 层(Page)最大写流量为 74 MB/s，最大读流量为 111 MB/s。该环境中的 TiFlash 使用独立的 NVME 盘，具有较强的 IO 吞吐能力。
![CH-2TiFlash-OP](/media/performance/tiflash/ch-2tiflash-raft-io-flow.png)

**示例 2 ：CH 负载 公有云环境 Raft 和 IO 指标 **

Raft Wait Index 等待时间 99 分位数最大为 438 毫秒，Raft Batch Read Index 等待时间 99 分位数最大为 125 毫秒。该集群只有一个 TiFlash 节点，每秒 TiKV 同步到 TiFlash 的增量数据约为 5MB。稳定层((File Descriptor))的最大写入流量为78 MB/s，最大读取流量为221 MB/s，Delta 层(Page)最大写入流量为8 MB/s，最大读取流量为18 MB/s。这个环境中的 TiFlash 使用的是 AWS EBS 云盘，其 IO 吞吐能力相对较弱。

![CH-TiFlash-MPP](/media/performance/tiflash/ch-1tiflash-raft-io-flow-cloud.png)