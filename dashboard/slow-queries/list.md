---
title: 访问列表页面
category: how-to
aliases: ['/docs-cn/dev/how-to/???']
---

# 访问列表页面

该功能可以查询整个集群中指定时间内执行时间较长的 SQL 查询。

默认情况下，执行时间超过 300ms 的 SQL 就会被视为慢查询，被记录到 [慢查询日志](https://pingcap.com/docs-cn/stable/identify-slow-queries/) 中，并可通过本功能对记录到的慢查询进行查询。可调整 [tidb_slow_log_threshold](https://pingcap.com/docs-cn/stable/tidb-specific-system-variables/#tidb_slow_log_threshold) SESSION 变量或 TiDB [slow-threshold](https://pingcap.com/docs-cn/stable/tidb-configuration-file/#slow-threshold) 参数调整慢查询阈值。

> 注意：
> 若关闭了慢查询日志，则本功能不可用。慢查询日志默认开启，可通过修改 TiDB 配置 [enable-slow-log](https://pingcap.com/docs-cn/stable/tidb-configuration-file/#enable-slow-log) 开启或禁用。

## 访问列表页面

可以通过以下两种方法访问集群诊断页面：

* 登录后，左侧导航条点击「慢查询」（Slow Queries）：

![access 访问页面](/media/dashboard/slow-queries/access.png)

* 在浏览器中访问 [http://127.0.0.1:2379/dashboard/#/slow_query](http://127.0.0.1:2379/dashboard/#/slow_query)（将 127.0.0.1:2379 替换为任意实际 PD 地址和端口）。

慢查询页面所展示的所有数据都来自于 TiDB 慢查询系统表及慢查询日志，参见 [慢查询日志](https://pingcap.com/docs-cn/stable/identify-slow-queries/) 文档了解详细情况。

### 修改列表过滤条件

页面顶部可修改显示的时间范围、按执行慢查询所在数据库进行过滤、按 SQL 关键字过滤、按 SQL 类型进行过滤及显示的数据条数，如下所示。默认显示 30 分钟内最近 100 条慢查询。

![图 1 ](/media/dashboard/slow-queries/list1.png)


### 显示其他字段

页面顶部「选择列」（Columns）选项中可选择显示更多列，可将鼠标移动到列名右侧的 (i) 图标处查看列的说明：

![图 2 ](/media/dashboard/slow-queries/list2.png)

### 修改列表排序依据

列表默认以「结束运行时间」（Finish Time）逆序排序，点击不同的列标题可以修改排序依据或切换排序顺序：

![图 3 ](/media/dashboard/slow-queries/list3.png)

## 查看执行详情

在列表中点击任意一行可以显示该慢查询的详细执行信息，包含：

SQL：慢查询 SQL 文本（下图中区域 1）
执行计划：慢查询的执行计划，参阅「理解 TiDB 执行计划」文档了解如何解读执行计划（下图中区域 2）
其他分类好的 SQL 执行信息（下图中区域 3）

![detail 示例 ](/media/dashboard/slow-queries/detail1.png)

点击「展开」（Expand）链接可以展开相应项的完整内容，点击「复制」（Copy）链接可以复制完整内容到剪贴板。

点击标签页标题可切换显示不同分类的 SQL 执行信息：

![detail 执行示例 ](/media/dashboard/slow-queries/detail2.png)