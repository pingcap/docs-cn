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

如果数据库时间占用户响应时间比例小，可以确认瓶颈不在数据库中。如果数据库时间占用户响应时间比例大，可以确认瓶颈在数据库中，需要在数据库内部进行性能分析和优化。

### 如果瓶颈在 TiDB 内部，如何定位
一个典型的 SQL 的处理流程如下所以，TiDB 的性能指标覆盖了绝大部分的路径。
![数据库时间分解图](/media/dashboard/dashboard-diagnostics-time-relation.png)

通过对数据库时间进行以下三个维度的分解，可以快速的的对 TiDB 内部瓶颈进行定位
1. 按 SQL 处理类型分解，可知哪种类型的 SQL 语句消耗数据库时间最多
2. 按 SQL 处理的 4 个步骤分解，可知哪个步骤 get_token/parse/compile/execute 消耗时间最多
3. 对于 execute 耗时，按照 TiDB 执行器本身的时间、TSO 等待时间和 kv 请求时间分解，可知执行阶段的瓶颈

## 利用 Performance Overview 面板进行性能分析和优化
Performance Overview Grafana 面板从版本 v6.0.0 发布。本章会介绍利用这个面板，TiDB 用户如何快速进行性能分析和优化。

### 数据库时间概览
### Query Per Second，Command Per Second, Prepared-Plan-Cache
### KV/TSO Request OPS 和连接信息
### TiDB 和 TiKV CPU 和 IO 使用情况
### Duration 和 Connection Idle Duration
### Parse Duration、Compile、Execution Duration 和 PD TSO Wait Duration
### KV 和 TSO Request Duration
### Storage Async Write Duration、Store Duration 和 Apply Duration
### Commit Log Duration、Append Log Duration 和 Apply Log Duration

## 老版本如何使用 Performance overview
需要手工导入 Performance Overview 面板

https://github.com/pingcap/tidb/blob/master/metrics/grafana/performance_overview.json