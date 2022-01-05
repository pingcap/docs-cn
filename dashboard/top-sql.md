---
title: Top SQL
summary: Top SQL -- 找到负载贡献较大的查询
---

# Top SQL

> **警告：**
>
> Top SQL 目前为实验特性，不建议在生产环境中使用。

Top SQL 会显示在一段时间内对某个 TiDB 或 TiKV 节点负载贡献较大的查询。例如，在一个低负载的数据库上执行一条消耗 99% 负载的分析查询。 Top SQL 针对某一节点，提供以下功能：

* 展示一段时间内前 5 CPU 负载贡献的查询。
* 对某一查询，展示出 CPU 使用量，每秒请求数，平均延迟，查询计划等信息，用于改善潜在的性能优化点。

## 启用

打开 TiDB Dashboard，登陆后，在左侧菜单点击 “Top SQL”，然后在右上角点击齿轮按钮，即可在整个集群范围内启用或禁用该功能。

> **注意：**
>
> 启用 Top SQL 会些许影响集群的性能。

## 使用 Top SQL

要使用 Top SQL，只需要打开 TiDB Dashboard，登陆后，在左侧菜单点击 “Top SQL” 即可。

![Top SQL](/media/dashboard/top-sql-overview.png)

使用提示：

* 上方可选择展示的节点，时间范围，也可以在图表中选择时间范围。
* 如果数据已过时，可以点击刷新按钮，也可以在刷新下拉框中选择是否自动刷新，以及自动刷新间隔。
* 列表中展示了选中节点，选中时间范围内前 5 负载贡献的查询。
* 点击选中单个查询，可以进一步展示详情。针对这类查询，统计执行计划，以及这类查询和其中执行计划在这个节点上的 Call/sec （平均每秒请求数），Scan Rows/sec （平均每秒扫描行数），Scan Indexes/sec （平均每秒扫描索引数），以及 Latency/call （平均延迟）。

![Top SQL Details](/media/dashboard/top-sql-details.png)
