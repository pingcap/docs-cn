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

- 该集群包含两个 TiFlash 节点，每个16C 48G内存，CH 负载运行时，CPU 利用率最大达到 1500%，内存最大 20GB，IO 使用率达到 91%。说明 TiFlash 节点资源接近满载。

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
- Request Duration Overview: 每秒所有 TiFlash 实例所有请求类型总处理时间的堆叠图
  - 如果类型为 `mpp_establish_conn` 和 `run_mpp_task`，说明 SQL 语句的执行都下推到 TiFlash 执行，这是 TiFlash 提供服务最常见的类型。
  - 如果类型为 `Cop`，说明整个语句没有完整下推到 TiFlash，TiDB 通常把全扫扫描算子下推到 TiFlash 进行数据访问和过滤，通常有两种情况，当 `Cop` 在堆叠图中占主导时，需要仔细权衡是否合理
    - SQL 访问大量数据，优化器根据成本模型估算 TiFlash 全表扫描成本更低
    - 表结构缺失合适的索引，下推到 TiFlash 属于优化的无奈之举，这种情况通过索引优化，通过 `TiKV` 访问数据效率更高。

- Request Duration: 所有 TiFlash 实例每种 MPP 和 coprocessor 请求类型的总处理时间，包含平均和 P99 处理延迟。
- Request Handle Duration：所有 TiFlash 实例 MPP 和 coprocessor 请求的处理时间，此时间为该 coprocessor 请求从开始执行到结束的时间，包含平均和 P99 延迟

**示例 1 ：TiFlash MPP 请求处理时间概览 **

- 该负载中 `run_mpp_task` 和 `mpp_establish_conn` 请求的处理时间占比最高，说明 发送到 TiFlash 请求大部分都是完全下推的 MPP 任务。
- `Cop` 请求处理时间占比小，说明存在部分请求是通过 `Cop` 下推到 TiFlash 进行数据访问和过滤。 

![CH-TiFlash-MPP](/media/performance/tiflash/ch-2tiflash-op.png)
  
**示例 2 ：TiFlash Cop 请求处理时间占比高 **

该负载中 `Cop` 请求的处理时间占比最高，Cop 请求产生的原因可以通过 SQL 执行计划确认。

![Cop](/media/performance/tiflash/tiflash_request_duration_by_type.png)
  
### Raft 相关指标
- Raft Wait Index Duration：所有 TiFlash 实例在进行 wait_index 消耗的时间，即拿到 read_index 请求后，等待本地的 Region index >= read_index 所花费的时间，如果 Wait Index 延迟过高，意味着 TiKV 到 TiFlash 存在明显的延迟，通常原因是：
  - TiKV 资源过载
  - TiFlash 资源过载，尤其可能是 IO 资源
  - TiKV 和 TiFlash 之间有网络瓶颈

- Raft Batch Read Index Duration：所有 TiFlash 实例在进行 read_index 消耗的时间，主要消耗在于和 Region leader 的交互和重试时间，如果该指标过高，以为着 TiFlash 到 TiKV 交互慢，可能原因：
  - TiFlash 资源过载
  - TiKV 资源过载
  - TiFLash 和 TiKV 之前的网络有瓶颈

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

Raft Wait Index 等待时间 99 分位数最大为3.24 秒，Raft Batch Read Index 等待时间 99 分位数最大为 753 毫秒。Wait Index 和 Read Index 99分位数较高，因为该环境 TiFlash 负载高，数据同步存在延迟。
该集群存在两个 TiFlash 节点，每秒 TiKV 同步到 TiFlash 增量数据为 28MB 左右。
稳定层 File Descriptor 最大写流量为 939MB/s，最大读流量为 1.1 GiB/s
Delta 层 Page 最大写流量为 74 MB/s，最大读流量为 111 MB/s
此环境 TiFlash 为独立 NVME 盘，IO 吞吐能力较强。
![CH-2TiFlash-OP](/media/performance/tiflash/ch-2tiflash-raft-io-flow.png)

**示例 2 ：CH 负载 公有云环境 Raft 和 IO 指标 **

Raft Wait Index 等待时间 99 分位数最大为 438 毫秒，Raft Batch Read Index 等待时间 99 分位数最大为 125 毫秒。
该集群存在一个 TiFlash 节点，每秒 TiKV 同步到 TiFlash 增量数据为 5MB 左右。
稳定层 File Descriptor 最大写流量为 78 MB/s，最大读流量为 221 MB/s
Delta 层 Page 最大写流量为 8 MB/s，最大读流量为 18 MB/s
此环境 TiFlash 为 AWS EBS 云盘，IO 吞吐能力较弱。

![CH-TiFlash-MPP](/media/performance/tiflash/ch-1tiflash-raft-io-flow-cloud.png)