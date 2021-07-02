---
title: TiDB Dashboard 慢查询页面
summary: 了解如何在 TiDB Dashboard 中查看慢查询。
aliases: ['/docs-cn/dev/dashboard/dashboard-slow-query/']
---

# TiDB Dashboard 慢查询页面

该页面上能检索和查看集群中所有慢查询。

默认情况下，执行时间超过 300ms 的 SQL 查询就会被视为慢查询，被记录到[慢查询日志](/identify-slow-queries.md)中，并可通过本功能对记录到的慢查询进行查询。可调整 [`tidb_slow_log_threshold`](/system-variables.md#tidb_slow_log_threshold) SESSION 变量或 TiDB [`slow-threshold`](/tidb-configuration-file.md#slow-threshold) 参数调整慢查询阈值。

> **注意：**
>
> 若关闭了慢查询日志，则本功能不可用。慢查询日志默认开启，可通过修改 TiDB 配置 [`enable-slow-log`](/tidb-configuration-file.md#enable-slow-log) 开启或禁用。

## 访问列表页面

可以通过以下两种方法访问慢查询页面：

* 登录后，左侧导航条点击**慢查询** (**Slow Queries**)：

![access 访问页面](/media/dashboard/dashboard-slow-queries-access.png)

* 在浏览器中访问 <http://127.0.0.1:2379/dashboard/#/slow_query>（将 `127.0.0.1:2379` 替换为任意实际 PD 地址和端口）。

慢查询页面所展示的所有数据都来自于 TiDB 慢查询系统表及慢查询日志，参见[慢查询日志](/identify-slow-queries.md)文档了解详细情况。

### 修改列表过滤条件

可按时间范围、慢查询语句关联的数据库、SQL 关键字、SQL 类型、显示的慢查询语句数量等条件过滤，筛选慢查询句。如下所示，默认显示 30 分钟内最近 100 条慢查询。

![修改列表过滤条件](/media/dashboard/dashboard-slow-queries-list1.png)

### 显示更多列信息

页面顶部**选择列** (**Columns**) 选项中可选择显示更多列，可将鼠标移动到列名右侧的 **(i)** 图标处查看列的说明：

![显示更多列信息](/media/dashboard/dashboard-slow-queries-list2.png)

### 修改列表排序依据

列表默认以**结束运行时间** (**Finish Time**) 逆序排序，点击不同的列标题可以修改排序依据或切换排序顺序：

![修改列表排序依据](/media/dashboard/dashboard-slow-queries-list3.png)

## 查看执行详情

在列表中点击任意一行可以显示该慢查询的详细执行信息，包含：

- SQL：慢查询 SQL 文本（下图中区域 1）
- 执行计划：慢查询的执行计划，参阅[理解 TiDB 执行计划](/explain-overview.md)文档了解如何解读执行计划（下图中区域 2）
- 其他分类好的 SQL 执行信息（下图中区域 3）

![查看执行详情](/media/dashboard/dashboard-slow-queries-detail1.png)

点击**展开** (**Expand**) 链接可以展开相应项的完整内容，点击**复制** (**Copy**) 链接可以复制完整内容到剪贴板。

点击标签页标题可切换显示不同分类的 SQL 执行信息：

![显示不同分类执行信息](/media/dashboard/dashboard-slow-queries-detail2.png)
