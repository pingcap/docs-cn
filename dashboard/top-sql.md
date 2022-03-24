---
title: Top SQL
summary: 本文介绍如何使用 Top SQL 找到消耗负载较大的 SQL 查询。
---

# Top SQL

本文介绍如何在 Top SQL 页面找到一段时间内对某个 TiDB 或 TiKV 节点消耗负载较大的 SQL 查询。例如，你可以通过 Top SQL 找出一个低负载的数据库上执行的一条消耗 99% 负载的分析查询。

针对指定的 TiDB 或 TiKV 节点，Top SQL 可以提供以下功能：

* 展示指定时间范围内消耗负载最多的 5 类 SQL 查询。
* 展示某一查询的 CPU 使用量、每秒请求数、平均延迟、查询计划等信息，作为改善业务的潜在性能优化点。

## 使用 Top SQL

Top SQL 功能默认开启。要使用该功能查看消耗负载较大的 SQL 查询，只需在登录 TiDB Dashboard 后点击左侧面板中的 **Top SQL** 即可。

![Top SQL](/media/dashboard/top-sql-overview.png)

使用提示：

* 你可以在页面顶部的下拉列表里选择要展示的节点和时间范围，也可以在图表中选择时间范围。
* 如果图表中显示的数据已过时，你可以点击**刷新** (Refresh) 按钮，也可以在**刷新** (Refresh) 下拉列表中选择是否自动刷新，以及自动刷新间隔。
* 列表中展示了选中节点、选中时间范围内消耗负载最多的 5 类查询。
* 点击选中列表中的某个查询类型，可以查看这类查询在这个节点上的执行计划，以及详细执行信息，例如 Call/sec （平均每秒请求数）、 Scan Rows/sec （平均每秒扫描行数）、 Scan Indexes/sec （平均每秒扫描索引数）、Latency/call （平均延迟）。

![Top SQL Details](/media/dashboard/top-sql-details.png)

## 关闭 Top SQL

Top SQL 会对集群的性能产生轻微的影响。如需在整个集群范围内关闭该功能，你可以使用以下任一方法：

- 方法一：登录 TiDB Dashboard，点击左侧面板中的 **Top SQL**，然后点击页面右上角的齿轮按钮，关闭 Top SQL 功能开关。
- 方法二：配置 TiDB 系统变量 [`tidb_enable_top_sql`](/system-variables.md#tidb_enable_top_sql-从-v540-版本开始引入)的值为 `OFF`。