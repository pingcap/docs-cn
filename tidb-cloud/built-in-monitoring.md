---
title: TiDB Cloud 内置指标
summary: 了解如何查看 TiDB Cloud 内置指标并理解这些指标的含义。
---

# TiDB Cloud 内置指标

TiDB Cloud 在指标页面上收集和显示集群的一整套标准指标。通过查看这些指标，您可以轻松识别性能问题并确定当前的数据库部署是否满足您的需求。

## 查看指标页面

要在**指标**页面上查看指标，请执行以下步骤：

1. 在项目的[**集群**](https://tidbcloud.com/project/clusters)页面上，点击目标集群的名称进入其概览页面。

    > **提示：**
    >
    > 您可以使用左上角的组合框在组织、项目和集群之间切换。

2. 在左侧导航栏中，点击**监控** > **指标**。

## 指标保留策略

对于 TiDB Cloud Dedicated 集群和 TiDB Cloud Serverless 集群，指标数据保留 7 天。

## TiDB Cloud Dedicated 集群的指标

以下部分说明了 TiDB Cloud Dedicated 集群的**指标**页面上的指标。

### 概览

| 指标名称  | 标签 | 描述                                   |
| :------------| :------| :-------------------------------------------- |
| Database Time by SQL types | database time, {SQL type} | database time：每秒总数据库时间。<br/> {SQL type}：每秒 SQL 语句消耗的数据库时间，按 SQL 类型收集，如 `SELECT`、`INSERT` 和 `UPDATE`。 |
| Query Per Second | {SQL type} | 所有 TiDB 实例中每秒执行的 SQL 语句数量，按 SQL 类型收集，如 `SELECT`、`INSERT` 和 `UPDATE`。 |
| Query Duration | avg-{SQL type}, 99-{SQL type} | 从客户端向 TiDB 发送请求到 TiDB 执行请求并将结果返回给客户端的持续时间。通常，客户端请求以 SQL 语句的形式发送；但是，此持续时间可以包括执行 `COM_PING`、`COM_SLEEP`、`COM_STMT_FETCH` 和 `COM_SEND_LONG_DATA` 等命令的时间。TiDB 支持多查询，这意味着客户端可以一次发送多个 SQL 语句，如 `select 1; select 1; select 1;`。在这种情况下，此查询的总执行时间包括所有 SQL 语句的执行时间。 |
| Failed Queries | All, {Error type} @ {instance} | 每分钟在每个 TiDB 实例上根据 SQL 语句执行错误的错误类型统计（如语法错误和主键冲突）。它包含错误发生的模块和错误代码。 |
| Command Per Second | Query, StmtExecute, and StmtPrepare | 所有 TiDB 实例每秒处理的命令数量，基于命令类型。 |
| Queries Using Plan Cache OPS | hit, miss | hit：所有 TiDB 实例中每秒使用计划缓存的查询数量。<br/> miss：所有 TiDB 实例中每秒未命中计划缓存的查询数量。 |
| Transaction Per Second | {types}-{transaction model} | 每秒执行的事务数量。 |
| Transaction Duration | avg-{transaction model}, 99-{transaction model} | 事务的平均或 99 百分位持续时间。 |
| Connection Count | All, active connection | All：到所有 TiDB 实例的连接数量。<br/> Active connections：到所有 TiDB 实例的活动连接数量。 |
| Disconnection Count | {instance}-{result} | 每个 TiDB 实例断开连接的客户端数量。 |

### 高级

| 指标名称  | 标签 | 描述                                   |
| :------------| :------| :-------------------------------------------- |
| Average Idle Connection Duration | avg-in-txn, avg-not-in-txn | 连接空闲持续时间表示连接处于空闲状态的持续时间。<br/> avg-in-txn：连接在事务内时的平均空闲持续时间。<br/>avg-not-in-txn：连接不在事务内时的平均空闲持续时间。 |
| Get Token Duration | avg, 99 | 获取 SQL 语句令牌所消耗的平均或 99 百分位持续时间。 |
| Parse Duration | avg, 99 | 解析 SQL 语句所消耗的平均或 99 百分位持续时间。 |
| Compile Duration | avg, 99 | 将解析的 SQL AST 编译为执行计划所消耗的平均或 99 百分位持续时间。 |
| Execute Duration | avg, 99 | 执行 SQL 语句执行计划所消耗的平均或 99 百分位持续时间。 |
| Average TiDB KV Request Duration | {Request Type} | 所有 TiDB 实例中执行 KV 请求所消耗的平均时间，基于请求类型，如 `Get`、`Prewrite` 和 `Commit`。 |
| Average TiKV gRPC Duration | {Request Type} | 所有 TiKV 实例中执行 gRPC 请求所消耗的平均时间，基于请求类型，如 `kv_get`、`kv_prewrite` 和 `kv_commit`。 |
| Average / P99 PD TSO Wait/RPC Duration | wait-avg/99, rpc-avg/99 | Wait：所有 TiDB 实例中等待 PD 返回 TSO 的平均或 99 百分位持续时间。<br/> RPC：所有 TiDB 实例中从发送 TSO 请求到 PD 到接收 TSO 的平均时间或 99 百分位持续时间。 |
| Average / P99 Storage Async Write Duration | avg, 99 | 异步写入所消耗的平均或 99 百分位持续时间。平均存储异步写入持续时间 = 平均存储持续时间 + 平均应用持续时间。 |
| Average / P99 Store Duration | avg, 99 | 异步写入期间存储循环所消耗的平均或 99 百分位持续时间。 |
| Average / P99 Apply Duration | avg, 99 | 异步写入期间应用循环所消耗的平均或 99 百分位持续时间。 |
| Average / P99 Append Log Duration | avg, 99 | Raft 追加日志所消耗的平均或 99 百分位持续时间。 |
| Average / P99 Commit Log Duration | avg, 99 | Raft 提交日志所消耗的平均或 99 百分位持续时间。 |
| Average / P99 Apply Log Duration | avg, 99 | Raft 应用日志所消耗的平均或 99 百分位持续时间。 |

### 服务器

| 指标名称  | 标签 | 描述                                   |
| :------------| :------| :-------------------------------------------- |
| TiDB Uptime | node | 每个 TiDB 节点自上次重启以来的运行时间。 |
| TiDB CPU Usage | node, limit | 每个 TiDB 节点的 CPU 使用统计或上限。 |
| TiDB Memory Usage | node, limit | 每个 TiDB 节点的内存使用统计或上限。 |
| TiKV Uptime | node | 每个 TiKV 节点自上次重启以来的运行时间。 |
| TiKV CPU Usage | node, limit | 每个 TiKV 节点的 CPU 使用统计或上限。 |
| TiKV Memory Usage | node, limit | 每个 TiKV 节点的内存使用统计或上限。 |
| TiKV IO Bps | node-write, node-read | 每个 TiKV 节点读写的每秒总输入/输出字节数。 |
| TiKV Storage Usage | node, limit | 每个 TiKV 节点的存储使用统计或上限。 |
| TiFlash Uptime | node | 每个 TiFlash 节点自上次重启以来的运行时间。 |
| TiFlash CPU Usage | node, limit | 每个 TiFlash 节点的 CPU 使用统计或上限。 |
| TiFlash Memory Usage | node, limit | 每个 TiFlash 节点的内存使用统计或上限。 |
| TiFlash IO MBps | node-write, node-read | 每个 TiFlash 节点读写的总字节数。 |
| TiFlash Storage Usage | node, limit | 每个 TiFlash 节点的存储使用统计或上限。 |

## TiDB Cloud Serverless 集群的指标

**指标**页面为 TiDB Cloud Serverless 集群提供了两个标签页：

- **集群状态**：显示集群级别的主要指标。
- **数据库状态**：显示数据库级别的主要指标。

### 集群状态

下表说明了**集群状态**标签页下的集群级别主要指标。

| 指标名称  | 标签 | 描述                                   |
| :------------| :------| :-------------------------------------------- |
| Request Units | RU per second | 请求单元（RU）是用于跟踪查询或事务资源消耗的度量单位。除了您运行的查询外，后台活动也会消耗请求单元，因此当 QPS 为 0 时，每秒请求单元可能不为零。 |
| Used Storage Size | Row-based storage, Columnar storage | 行存储的大小和列存储的大小。 |
| Query Per Second | All, {SQL type} | 每秒执行的 SQL 语句数量，按 SQL 类型收集，如 `SELECT`、`INSERT` 和 `UPDATE`。 |
| Average Query Duration | All, {SQL type} | 从客户端向 TiDB Cloud Serverless 集群发送请求到集群执行请求并将结果返回给客户端的持续时间。 |
| Failed Query | All | 每秒 SQL 语句执行错误的数量。 |
| Transaction Per Second | All | 每秒执行的事务数量。 |
| Average Transaction Duration | All | 事务的平均执行持续时间。 |
| Total Connection | All | 到 TiDB Cloud Serverless 集群的连接数量。 |

### 数据库状态

下表说明了**数据库状态**标签页下的数据库级别主要指标。

| 指标名称  | 标签 | 描述                                   |
| :------------| :------| :-------------------------------------------- |
| QPS Per DB | All, {Database name} | 每个数据库每秒执行的 SQL 语句数量，按 SQL 类型收集，如 `SELECT`、`INSERT` 和 `UPDATE`。 |
| Average Query Duration Per DB | All, {Database name} | 从客户端向数据库发送请求到数据库执行请求并将结果返回给客户端的持续时间。|
| Failed Query Per DB | All, {Database name} | 每个数据库每秒根据 SQL 语句执行错误的错误类型统计。|

## 常见问题

**1. 为什么此页面上的某些面板是空的？**

如果面板没有提供任何指标，可能的原因如下：

- 相应集群的工作负载没有触发此指标。例如，在没有失败查询的情况下，失败查询指标始终为空。
- 集群版本较低。您需要升级到最新版本的 TiDB 才能看到这些指标。

如果排除了所有这些原因，您可以联系 [PingCAP 支持团队](/tidb-cloud/tidb-cloud-support.md)进行故障排查。

**2. 为什么在罕见情况下指标可能不连续？**

在某些罕见情况下，指标可能会丢失，例如当指标系统承受高压力时。

如果您遇到此问题，可以联系 [PingCAP 支持团队](/tidb-cloud/tidb-cloud-support.md)进行故障排查。
