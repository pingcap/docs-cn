---
title: TiDB Cloud Top RU 页面
summary: 在 PingCAP Clinic 中使用 Top RU 定位 RU 消耗较高的 SQL 与数据库用户
---

# TiDB Cloud Top RU 页面

Top RU 是 TiDB Cloud 在 PingCAP Clinic 中提供的一项 SQL 资源观测能力，用于按资源单元（RU）消耗对 SQL 进行排序和分析，帮助你快速定位高资源消耗 SQL。Top RU 复用 Top SQL 的采集和上报链路，但观测维度从 CPU 扩展为 RU，并按照 `(user, sql_digest, plan_digest)` 进行聚合。因此，Top RU 不仅可以帮助你找出哪些 SQL 消耗了更多 RU，还可以帮助你识别是哪些数据库用户在持续消耗资源。

Top RU 与 Top SQL 可以共存。启用 Top RU 不会改变 Top SQL 现有的 CPU 观测语义。

## 功能简介

Top RU 适合用来回答以下问题：

- 哪些 SQL 在持续消耗较多 RU。
- 某段时间内 RU 消耗升高是否由少数用户或少数 SQL 引起。
- 某些 SQL 的 CPU 并不高，但为什么资源消耗仍然很大。

Top RU 的数据来自 SQL 执行过程中的运行时 RU 统计信息，因此能够反映近实时的资源消耗趋势。为了控制额外开销，Top RU 会对用户和 SQL 做 TopN 聚合，并将低优先级项目合并展示，而不是输出完整的逐条明细流。

## 推荐适用场景

Top RU 适用于以下场景：

- 在开启 [Resource Control](/tidb-resource-control-ru-groups.md) 的集群中，定位高 RU 消耗 SQL。
- CPU 使用率并不突出，但查询仍然消耗大量资源，需要从 RU 维度继续排查。
- 需要从用户维度识别“谁在消耗更多 RU”，而不仅仅是“哪条 SQL 消耗更多 CPU”。
- 需要在高负载时快速找出主要的资源消耗来源，以便后续做 SQL 优化、资源组治理或业务侧限流。

Top RU 不适用于以下场景：

- 不适合作为账单、对账或精确审计工具。
- 不适合替代慢日志、`statements_summary` 或资源组日级统计等离线分析手段。

## 使用前提

使用 Top RU 前，需要满足以下条件：

- 你可以访问 TiDB Cloud 的 PingCAP Clinic。
- 集群已开启 [Resource Control](/tidb-resource-control-ru-groups.md)。如果未开启 Resource Control，TiDB 不会采集和上报有效的 RU 数据。
- 订阅端需要支持 Top SQL 的 `PubSubService` 订阅模式，并显式请求 Top RU 能力。
- 集群需要使用支持 Top RU 的 TiDB 内核版本（请以控制台发布说明或支持团队通知为准）。

> **注意：**
>
> Top RU 当前没有独立的 SQL 系统变量，也没有单独的 `SET GLOBAL ...` 开关。Top RU 是否启用由 Top SQL PubSub 订阅协商触发，而不是由独立的 TiDB 系统变量直接控制。

## 页面视图

Top RU 页面当前包含以下两个主要视图：

- 实例视图（Instance-level）：用于从实例整体观察 RU 消耗较高的 SQL。
- 数据库用户视图（DB user-level）：用于按数据库用户聚合，快速定位某个用户下最消耗 RU 的 SQL。

![Top RU 实例视图](/media/dashboard/top-ru-instance-view.png)

![Top RU 实例视图详情](/media/dashboard/top-ru-instance-detail.png)

![Top RU 数据库用户视图](/media/dashboard/top-ru-db-user-view.png)

![Top RU 数据库用户视图详情](/media/dashboard/top-ru-db-user-detail.png)

从诊断路径看，通常可以先在实例视图定位 RU 热点，再切换到数据库用户视图观察是否由特定用户驱动。

## 使用 Top RU

以下是使用 Top RU 的常见步骤：

1. 打开 Top RU 页面并选择时间范围。
2. 在实例视图中观察 RU 排名靠前的 SQL，确定热点时段和热点 SQL。
3. 切换到数据库用户视图，确认是否由少数用户持续消耗 RU。
4. 进入 SQL 明细后，结合 SQL Digest / Plan Digest、执行次数和执行时长判断优化优先级。
5. 结合 Top SQL、慢查询和执行计划继续深入分析。

Top RU 的趋势通常和 RU、QPS 指标趋势具有相关性，可用于交叉验证：

![Top RU 与 RU 指标趋势](/media/dashboard/top-ru-vs-ru-trend.png)

![Top RU 与 QPS 指标趋势](/media/dashboard/top-ru-vs-qps-trend.png)

## Top RU 观测维度

Top RU 以 `(user, sql_digest, plan_digest)` 作为聚合键。每个时间点通常包含以下统计项：

- `Total RU`：该时间段内聚合后的 RU 消耗总量。
- `Exec Count`：该时间段内对应 SQL 的执行次数统计。
- `Exec Duration`：该时间段内对应 SQL 的累计执行时长。

Top RU 支持按 `15s`、`30s` 或 `60s` 粒度输出观测点。若订阅请求未提供有效粒度，则默认回退到 `60s`。在内部实现中，RU 数据按 60 秒对齐窗口进行汇总和上报，因此通常表现为分钟级近实时刷新。

为了限制内存和网络开销，Top RU 会对用户和 SQL 进行 TopN 聚合。高优先级项目会保留独立记录，其余低优先级项目会被合并，而不是完整保留所有明细。

## 限制与注意事项

使用 Top RU 时，需要注意以下限制：

- Top RU 当前仅支持 `PubSubService` 订阅模式。
- Top RU 当前不支持通过 `SingleTargetDataSink` 固定目标 gRPC 推送模式导出。
- Top RU 展示的 RU 来自运行时 `RUDetails` 观测值，不等同于 Billing RU。
- 如果未开启 Resource Control，Top RU 不会生成有效的 RU 数据。
- 为了控制采集和上报开销，Top RU 会对输出结果做 TopN 压缩，不保证保留全部低 RU 项。

> **注意：**
>
> Top RU 适合用来做实时资源热点定位，而不适合用来替代账单结算、精确核对或长期离线审计。

## 常见问题

**1. Top RU 和 Top SQL 有什么区别？**

Top SQL 主要按 CPU 开销观察 SQL；Top RU 主要按 RU 消耗观察 SQL。Top RU 复用 Top SQL 的基础链路，但聚合键增加了用户维度，并且关注的是资源单元而不是 CPU。

**2. 为什么开启后仍然看不到 Top RU 数据？**

最常见的原因是集群没有开启 [Resource Control](/tidb-resource-control-ru-groups.md)，或者订阅端虽然建立了 Top SQL 订阅，但没有显式请求 Top RU 能力。此时 TiDB 不会输出有效的 Top RU 数据。

**3. Top RU 是否等于账单 RU？**

不是。Top RU 使用的是运行时 `RUDetails` 观测值，适合用于定位高资源消耗 SQL；账单、对账等场景仍应使用 Billing RU 或相应的离线统计数据。

**4. 是否支持通过固定 gRPC 目标导出 Top RU？**

不支持。当前 Top RU 仅支持 `PubSubService` 订阅模式，不支持通过 `SingleTargetDataSink` 固定目标 gRPC 推送模式导出。
