---
title: TiDB 性能分析和优化手册
---

# TiDB 性能分析和优化手册

## 目标
长久以来，数据库性能分析和优化是一件困难的事情，在 TiDB 这样一个分布式的数据库进行性能分析和优化更加困难。本文的目标是提供 TiDB 用户一种自顶向下的，可靠的方法，让普通的 TiDB 用户可以自行进行瓶颈分析和性能优化，做到数据库优化不求人。

## 用户响应时间和数据库时间
### 用户响应时间
用户响应时间是指应用系统为用户返回请求结果所花的时间。一个典型的用户请求的处理时序图如下，包含了用户和应用系统的网络延迟，应用的处理时间，应用和数据库的交互次数和网络延迟，数据库时间等。用户响应时间受到请求链路上所有子系统的影响，比如网络延迟和带宽，系统并发用户数和请求类型，以及应用和数据库服务器 CPU、IO 和网络等资源使用率等。只有知道用户响应时间的的瓶颈，才能针对性的对整个系统进行优化。
`ΔT` 时间内总的用户响应时间等于平均 TPS 乘以平均的用户响应时间乘以 `ΔT`

`ΔT Total user response time = TPS × user avg reponse time × ΔT`

![用户响应时间](/media/performance/performance-overview/user_response_time_cn.png)

### 数据库时间
`ΔT` 时间内数据库时间为数据库处理所有应用请求的时间和。数据库时间可以通过多种方式求得：

1. QPS 乘以 平均 query 延迟 乘以 ΔT
2. 平均活跃会话数 乘以 ΔT
3. 通过 TiDB 内部的 Promtheus 指标 TiDB_server_handle_query_duration_seconds_sum 求得

```
ΔT DB Time = QPS × avg latency × ΔT
ΔT DB Time = avg active connections × ΔT 
ΔT DB Time = rate(TiDB_server_handle_query_duration_seconds_sum) × ΔT 
```
TiDB 内部对 SQL 的处理路径进行了完善的测量，方便定位数据库内部的性能瓶颈。

## 基于数据库时间的性能优化方法论

通过对比用户响应时间和数据库时间，TiDB 的用户可以回答两个问题：
1. 整个系统的瓶颈是否在 TiDB 中
2. 如果瓶颈在 TiDB 内部，如何定位

### 整个系统的瓶颈是否在 TiDB 中

如果数据库时间占用户响应时间比例小，可以确认瓶颈不在数据库中，需要关注数据库外面的组件，比如应用服务器硬件资源是否存在瓶颈，网络延迟是否过高等。反之，如果数据库时间占用户响应时间比例大，可以确认瓶颈在数据库中，需要在数据库内部进行性能分析和优化。

### 如果瓶颈在 TiDB 内部，如何定位
一个典型的 SQL 的处理流程如下所以，TiDB 的性能指标覆盖了绝大部分的处理路径。
![数据库时间分解图](/media/dashboard/dashboard-diagnostics-time-relation.png)

数据库时间是所有 SQL 处理时间的总和。通过对数据库时间进行以下三个维度的分解，可以快速的的对 TiDB 内部瓶颈进行定位
1. 按 SQL 处理类型分解，可知哪种类型的 SQL 语句消耗数据库时间最多
2. 按 SQL 处理的 4 个步骤分解，可知哪个步骤 get_token/parse/compile/execute 消耗时间最多
3. 对于 execute 耗时，按照 TiDB 执行器本身的时间、TSO 等待时间和 kv 请求时间分解，可知执行阶段的瓶颈

这三种分解对应三个公式：
```
DB Time = Select Time + Insert Time + Update Time + Delete Time + Commit Time + ...
DB Time = Get Token Time + Parse Time + Comiple Time + Execute Time
Execute Time = TiDB Executor Time + KV Request Time + PD TSO Wait Time 
```

## 利用 Performance Overview 面板进行性能分析和优化
Performance Overview Grafana 面板从版本 v6.0.0 发布。本章会介绍利用这个面板，TiDB 用户如何快速进行性能分析和优化。
Performance Overview 包含三种数据：
1. 数据库时间和 SQL 执行时间分解
2. TiDB 关键指标和资源利用率
3. Query 延迟分解

### 数据库时间和 SQL 执行时间分解
DB time 指标为 TiDB 每秒处理 SQL 的延迟总和，等于 TiDB 集群每秒并发处理应用 SQL 请求的总时间(等于活跃连接数)。通过三个面积堆叠图，用户可以了解数据库负载的类型，可以快速定位在数据库的瓶颈集中在哪个执行阶段，主要是处理什么语句，SQL 执行阶段主要等待 TiKV 或者 PD 什么请求类型。 以下举例说明：

#### 例子 1 TPC-C 负载
- 第一个图，Database Time by SQL Type， 主要消耗时间的语句为 commit、update、select 和 insert 语句。
- 第二个图，Ddatabase Time By SQL Phase，主要消耗时间的为 execute 阶段。
- 第三个图，execute 阶段，主要消耗时间为 kv 请求 Prewrite 和 Commit。
    > **注意：**
    >
    > kv request 时间比的总和大于 execute 时间长是正常的，因为 TiDB 执行器可能并发向多个 TiKV 发送 kv 请求，导致总的 kv 请求等待时间大于执行时间。TPC-C 负载中，事务提交时，TiDB 会向多个 TiKV 并行发送 Prewrite 和 Commit，所以这个例子中 Prewrite、Commit 和 PessimisticsLock 请求的总和明显大于 execute 时间。

![TPC-C](/media/performance/performance-overview/tpcc_db_time.png)

#### 例子 2 OLTP 读密集负载
- 第一个图，Database Time by SQL Type， 主要消耗时间的语句为 select、commit、update和 insert 语句。select 占据绝大部分的数据库时间。
- 第二个图，Ddatabase Time By SQL Phase，主要消耗时间的为 execute 阶段。
- 第三个图，execute 阶段，主要消耗时间为 pd tso_wait 和 kv Get、Prewrite 和 Commit。
![OLTP](/media/performance/performance-overview/oltp_normal_db_time.png)

#### 例子 3 只读 OLTP 负载
1. 第一个图，Database Time by SQL Type， 几乎所有语句为 select。
1. 第二个图，Ddatabase Time By SQL Phase，主要消耗时间的为 compile 和 execute 阶段。
1. 第三个图，execute 阶段，主要消耗时间为 kv 请求 BatchGet。
![OLTP](/media/performance/performance-overview/oltp_long_compile_db_time.png)
    > **注意：**
    >
    > BatchGet 请求的总时间远大于 execute 时间，是因为 select 语句需要从多个 TiKV 并行读取几千行数据。

### TiDB 关键指标和资源利用率
#### Query Per Second，Command Per Second, Prepared-Plan-Cache
QPS 的面板可能是大家最熟悉的，可以看到应用的 sql 语句类型分布。command 的类型主要是 StmtExecute 为主，并且 StmtExecute 每秒的数据基本等于 Queries Using Plan Cache OPS. 这是 OLTP 负载理想的情况，客户端执行使用 prepared statement，并且在客户端缓存了 prepared statement对象，执行每条 sql 语句时直接调用 Statement Execute。执行执行时都命中 plan cache，不需要重新 compile 生成执行计划.
#### 例子 1 TPC-C 负载
![TPC-C](/media/performance/performance-overview/tpcc_qps.png)
#### 例子 2 OLTP 读密集负载
![OLTP](/media/performance/performance-overview/oltp_normal_qps.png)
#### 例子 3 只读 OLTP 负载
![OLTP](/media/performance/performance-overview/oltp_long_compile_qps.png)
####
#### KV/TSO Request OPS 和连接信息
kv 和 tso 每秒请求数据统计，其他 kv request total 是 tidb 到 tikv 所有请求的总和。除了常规的总的连接数和每个 tidb 连接数，可以判断连接总数是否正常，每个 tidb 的连接数是否不均衡。active connections 记录着活跃连接数，等于每秒的数据库时间。

#### TiDB 和 TiKV CPU 和 IO 使用情况
这两个面板可以观察到 TiDB 和 TiKV的逻辑 cpu 使用率，包含平均、最大和 Delta(最大 cpu利用率 减去 最小 cpu 使用率），可以用来判定tidb 和 tikv 总体的 cpu 利用率；tidb 是否存在 cpu 使用负载不均衡(通常伴随着应用连接不均衡)，tikv 是否存在热点。

### Query 延迟分解
#### Duration 和 Connection Idle Duration
#### Parse Duration、Compile、Execution Duration 和 PD TSO Wait Duration
#### KV 和 TSO Request Duration
#### Storage Async Write Duration、Store Duration 和 Apply Duration
#### Commit Log Duration、Append Log Duration 和 Apply Log Duration

## 老版本如何使用 Performance overview
需要手工导入 Performance Overview 面板

https://github.com/pingcap/tidb/blob/master/metrics/grafana/performance_overview.json