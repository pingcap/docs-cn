---
title: TiDB Dashboard 概况页面
---

# TiDB Dashboard 概况页面

该页面显示了整个集群的概况，包含以下信息：

- 整个集群的 QPS
- 整个集群的查询延迟
- 最近一段时间内累计耗时最多的若干 SQL 语句
- 最近一段时间内运行时间超过一定阈值的慢查询
- 各个实例的节点数和状态
- 监控及告警信息

## 访问

登录 TiDB Dashboard 后默认进入该页面，也可以左侧导航条点击**概况**（Overview）进入：

![访问](/media/dashboard/dashboard-overview-access.png)

## QPS

该区域显示最近一小时整个集群的每秒成功和失败查询数量：

![界面](/media/dashboard/dashboard-overview-qps.png)

> **注意：**
>
> 该功能仅在部署了 Prometheus 监控组件的集群上可用，未部署监控组件的情况下会显示为失败。

## 延迟

该区域显示最近一小时整个集群中 99.9%、99% 和 90% 查询的延迟：

![界面](/media/dashboard/dashboard-overview-latency.png)

> **注意：**
>
> 该功能仅在部署了 Prometheus 监控组件的集群上可用，未部署监控组件的情况下会显示为失败。

## Top SQL 语句

该区域显示最近一段时间内整个群集中累计耗时最长的 10 类 SQL 语句。查询参数不一样但结构一样的 SQL 会归为同一类 SQL 语句，在同一行中显示：

![界面](/media/dashboard/dashboard-overview-top-statements.png)

该区域显示的内容与 [SQL 语句分析页面](/dashboard/dashboard-statement-list.md)一致，可点击 **Top SQL 语句** (Top SQL Statements) 标题查看完整列表。关于该表格中各列详情，见 [SQL 语句分析页面](/dashboard/dashboard-statement-list.md)。

> **注意：**
>
> 该功能仅在开启了 SQL 语句分析功能的集群上可用。

## 最近的慢查询

该区域默认显示最近 30 分钟内整个集群中最新的 10 条慢查询：

![界面](/media/dashboard/dashboard-overview-slow-query.png)

默认情况下运行时间超过 300ms 的SQL 查询即会被计为慢查询并显示在该表格中。可通过调整 [tidb_slow_log_threshold](/system-variables.md#tidb_slow_log_threshold) 变量或 TiDB [slow-threshold](/tidb-configuration-file.md#slow-threshold) 参数调整阈值。

该区域显示的内容与[慢查询页面](/dashboard/dashboard-slow-query.md)一致，可点击**最近的慢查询** (Recent Slow Queries) 标题查看完整列表。关于该表格中各列详情，见[慢查询页面](/dashboard/dashboard-slow-query.md)。

> **注意：**
>
> 该功能仅在配置开启了慢查询日志的集群中可用，使用 TiUP 部署的集群默认开启慢查询日志。

## 实例

该区域汇总显示了整个集群中 TiDB、TiKV、PD、TiFlash 的总实例数量及异常实例数量：

![界面](/media/dashboard/dashboard-overview-instances.png)

状态描述如下：

- Up：实例运行正常（含下线中的存储实例）。
- Down：实例运行异常，例如网络无法连接、进程已崩溃等。

点击**实例**标题可进入[集群信息页面](/dashboard/dashboard-cluster-info.md)查看各个实例的详细运行状态。

## 监控和告警

该区域提供了便捷的链接方便用户查看详细监控或告警：

![界面](/media/dashboard/dashboard-overview-monitor.png)

- **查看监控**链接：点击后跳转至 Grafana 页面，可查看集群详细监控信息。关于 Grafana 监控面板中各个详细监控指标的解释，参见[监控指标](/grafana-overview-dashboard.md)文档。
- **查看告警**链接：点击后跳转至 AlertManager 页面，可查看集群详细告警信息。当集群中已有告警时，告警数量将会直接显示在链接文本上。
- **运行诊断**链接：点击后跳转至集群诊断页面，参见[集群诊断页面](/dashboard/dashboard-diagnostics-access.md)了解详情。

> **注意：**
>
> **查看监控**链接仅在集群中部署了 Grafana 节点时可用，**查看告警**链接仅在集群中部署了 AlertManager 节点时可用。
