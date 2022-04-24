---
title: Performance Overview 面板重要监控指标详解
aliases: ['/docs-cn/dev/grafana-performance-overview-dashboard/','/docs-cn/dev/reference/key-monitoring-metrics/performance-overview-dashboard/']
---

# Performance Overview 面板重要监控指标详解

使用 TiUP 部署 TiDB 集群时，一键部署监控系统 (Prometheus & Grafana)，监控架构参见 [TiDB 监控框架概述](/tidb-monitoring-framework.md)。

目前 Grafana Dashboard 整体分为 PD、TiDB、TiKV、Node\_exporter、Overview、Performance\_overview 等。

Performance Overview Dashboard 包含了以下三部分内容：
- 数据库时间和 SQL 执行时间概览
- TiDB 关键指标和集群资源利用率
- Query 延迟分解和关键的延迟指标

借助 Performance Overview Dashboard，TiDB 用户可以进行高效性能分析，确认用户响应时间的瓶颈是否在数据库中；如果数据库是整个系统的瓶颈，通过数据库时间概览和 SQL 延迟的分解，定位数据库内部的瓶颈点，并进行针对性的优化。使用方法和实际案例请参考 [TiDB 性能分析和优化手册](/performance/performance_tuning_guide.md) 和 [OLTP 负载优化案例](/performance/real-world-tuning-case.md)

以下为 Performance Overview Dashboard 监控说明：

以下为 Overview Dashboard 监控说明：

## Database Time by SQL Type
- database time: 每秒的总数据库时间
- sql_type: 每种 SQL 语句每秒消耗的数据库时间

## Database Time by SQL Phase
- database time: 每秒的总数据库时间
- get token/parse/compile/execute: 4 个 SQL 执行阶段每秒消耗的数据库时间

execute 执行阶段为绿色，其他三个阶段偏红色系，如果非绿色的颜色占比明显，意味着在执行阶段之外数据库消耗了过多时间，需要进一步分析根源。

## SQL Execute Time Overview
- execute time: 每秒的 execute 阶段消耗的数据库时间
- tso_wait: execute 阶段每秒同步等待 tso 的时间
- kv request type: execute 阶段每秒等待每种 kv 请求类型的时间，总的 kv request 等待时间可能超过 execute time，因为 kv request 是并发的。

对于常规的写 kv 请求，Prewrite 和 Commit，颜色为绿色系；对于常规的读 kv 请求，颜色为 蓝色系；除此之外的类型，被赋予了让人不舒服的颜色，比如悲观锁加锁请求为红色，tso 等待为深褐色。如果非蓝色系或者非绿色系占比明显，意味着执行阶段存在异常的瓶颈。比如锁冲突严重，红色的悲观锁时间会占比明显；比如负载中 tso wait 消耗的时间过长，深褐色占比明显。

## QPS
QPS：按 `SELECT`、`INSERT`、`UPDATE` 类型统计所有 TiDB 实例上每秒执行的 SQL 语句数量。

## CPS By Type
Command Per Second By Type：按照类型统计所有 TiDB 实例每秒处理的命令数。

## Queries Using Plan Cache OPS
Queries Using Plan Cache OPS：所有 TiDB 实例每秒使用 Plan Cache 的查询数量。

## KV/TSO Request OPS
- kv request total: 所有 TiDB 实例每秒总的 kv 请求数量
- kv request by type: 按 `Get`、`Prewrite`、 `Commit`类型统计在所有 TiDB 实例每秒的请求数据
- tso - cmd：在所有 TiDB 实例每秒 tso cmd 的请求数量
- tso - request：在所有 TiDB 实例每秒 tso request 的请求数量

通常 tso - cmd 除以 tso - request 平均请求的 batch 大小

## Connection Count
- 每个 TiDB 的连接数。
- 所有 TiDB 总连接数。
- 所有 TiDB 总的活跃连接数

## TiDB CPU
- avg：所有 TiDB 实例平均 CPU 利用率
- delta：所有 TiDB 实例最大 CPU 利用率 减去 所有 TiDB 实例最小 CPU 利用率
- max：所有 TiDB 实例最大 CPU 利用率

## TiKV CPU/IO MBps
- CPU-Avg：所有 TiKV 实例平均 CPU 利用率
- CPU-Delta：所有 TiKV 实例最大 CPU 利用率 减去 所有 TiKV 实例最小 CPU 利用率
- CPU-MAX：所有 TiKV 实例最大 CPU 利用率
- IO-Avg：所有 TiKV 实例平均 MBps
- IO-Delta：所有 TiKV 实例最大 MBps 减去 所有 TiKV 实例最小 MBps
- IO-MAX：所有 TiKV 实例最大 MBps

## Duration
- Duration：执行时间解释
  - 客户端网络请求发送到 TiDB，到 TiDB 执行结束后返回给客户端的时间。一般情况下，客户端请求都是以 SQL 语句的形式发送，但也可以包含 `COM_PING`、`COM_SLEEP`、`COM_STMT_FETCH`、`COM_SEND_LONG_DATA` 之类的命令执行时间。
  - 由于 TiDB 支持 Multi-Query，因此，客户端可以一次性发送多条 SQL 语句，如 `select 1; select 1; select 1;`。此时的执行时间是
所有 SQL 语句执行完之后的总时间。
- avg：所有请求命令的平均时间
- 99： 所有请求命令的 p99 时间
- avg by type：按 `SELECT`、`INSERT`、`UPDATE` 类型统计所有 TiDB 实例上所有请求命令的平均执行时间

## Connection Idle Duration
- Connection Idle Duration：空闲连接的持续时间。
- avg-in-txn：处于事务中，空闲连接的平均持续时间
- avg-not-in-txn：没有处于事务中，空闲连接的平均持续时间
- 99-in-txn：处于事务中，空闲连接的 P99 持续时间
- 99-not-in-txn：没有处于事务中，空闲连接的 P99 持续时间

## Parse Duration / Compile Duration / Execute Duration
- Parse Duration：SQL 语句解析耗时统计。
- Compile Duration：将解析后的 SQL AST 编译成执行计划的耗时。
- Execution Duration：执行 SQL 语句执行计划耗时。

每个面板包含所有 TiDB 实例的平均值和 P99 值

## Avg TiDB KV Request Duration
按 `Get`、`Prewrite`、 `Commit`类型统计在所有 TiDB 实例平均 KV Request 执行时间

## Avg TiKV GRPC Duration
按 `get`、`kv_prewrite`、 `kv_commit`类型统计在所有 TiKV 实例对 gRPC 请求平均的执行时间

## PD TSO Wait/RPC Duration
- wait - avg：所有 TiDB 实例等待从 PD 返回 TSO 的平均时间
- rpc - avg：所有 TiDB 实例从向 PD 发送获取 TSO 的请求到接收到 TSO 的平均耗时
- wait - 99：所有 TiDB 实例等待从 PD 返回 TSO 的 P99 时间
- wait - 99：所有 TiDB 实例从向 PD 发送获取 TSO 的请求到接收到 TSO 的 P99 耗时

## Storage Async Write Duration、Store Duration 和 Apply Duration

- Storage async write duration：异步写所花费的时间
- Store Duration：异步写 Store 步骤所花费的时间
- Apply Duration：异步写 Apply 步骤所花费的时间
  
这三个时间指标都包含所有 TiKV 实例的平均值和 P99 值
平均 Storage async write duration = 平均 Store Duration + 平均 Apply Duration

## Append Log Duration、Commmit Log Duration 和 Apply Log Duration

- Append log duration：Raft append 日志所花费的时间
- Commit log duration：Raft commit 日志所花费的时间
- Apply log duration：Raft apply 日志所花费的时间
  
这三个时间指标都包含所有 TiKV 实例的平均值和 P99 值

## 图例

![performance overview](/media/performance/grafana_performance_overview.png)
