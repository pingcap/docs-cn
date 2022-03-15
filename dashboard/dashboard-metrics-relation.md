---
title: TiDB Dashboard 监控关系图
summary: 了解 TiDB Dashboard 监控关系图
---

# TiDB Dashboard 监控关系图

TiDB Dashboard 监控关系图是 TiDB v4.0.7 起提供的新功能，可以将集群中各个内部流程的耗时监控数据绘制为关系图，帮助用户快速了解集群中各个环节的耗时及关系。

## 访问关系图

登录 TiDB Dashboard 后点击左侧导航的**集群诊断**可以进入此功能页面：

![生成监控关系图首页](/media/dashboard/dashboard-metrics-relation-home.png)

设置**区间起始时间**和**区间长度**参数后，点击**生成监控关系图**按钮后，会进入监控关系图页面。

## 关系图解读

下面是一份监控耗时关系图示例，描述的是某个 TiDB 集群在 2020-07-29 16:36:00 开始往后 5 分钟内，TiDB 集群中各个监控的总耗时比例，以及各项监控之间的关系。

![监控关系图示例](/media/dashboard/dashboard-metrics-relation-example.png)

例如以下 `tidb_execute` 节点监控图表示：`tidb_execute` 监控项的总耗时为 19306.46 秒，占总查询耗时的 89.4%，其中 `tidb_execute` 节点自身的耗时是 9070.18 秒，占总查询耗时的 42%。将鼠标悬停在该方框上，可以看到监控项的注释说明，总耗时、平均耗时、平均 P99 耗时等详细信息。

![监控关系图 tidb_execute 节点示例](/media/dashboard/dashboard-metrics-relation-node-example.png)

### 节点的含义

每个方框节点代表一个监控项，包含了以下信息：

* 监控项的名称
* 监控项的总耗时
* 监控项总耗时和查询总耗时的比例

`节点监控的总耗时 = 节点自身的耗时 + 子节点的耗时`，所以某些节点监控图会显示节点自身的耗时和总耗时的比例。例如 `tidb_execute` 监控：

![监控关系图 tidb_execute 节点示例](/media/dashboard/dashboard-metrics-relation-node-example1.png)

* `tidb_execute` 是监控项的名字。该监控是指一条 SQL 请求在 TiDB 执行引擎中的执行耗时。
* `19306.46s` 表示 `tidb_execute` 监控项消耗的总时间为 19306.46 秒。`89.40%` 表示 19306.46 秒占所有 SQL 查询总耗时（包括用户 SQL 和 TiDB 内部的 SQL）的比例为 89.40%。查询总耗时是 `tidb_query` 监控项的总耗时。
* `9070.18s` 表示 `tidb_execute` 节点自身总执行耗时是 9070.18 秒，其余部分是被其子节点消耗的时间。`42.00%` 表示 9070.18 秒占所有查询总耗时的比例为 42.00%。

将鼠标悬停在该节点后，会显示监控项的更多详细信息：

![监控关系图 tidb_execute 节点注释](/media/dashboard/dashboard-metrics-relation-node-example2.png)

上图信息为该项监控的注释说明，包括总耗时、总次数、平均耗时和平均 P99、P90、P80 耗时。

### 监控项之间的父子关系

下面以 `tidb_execute` 监控为例介绍该监控项相关的子节点：

![监控关系图 tidb_execute 节点注释](/media/dashboard/dashboard-metrics-relation-relation-example1.png)

可以看到，`tidb_execute` 包含两个子节点，分别是：

* `pd_start_tso_wait`：等待事务 `start_tso` 的耗时，其总耗时是 300.66 秒。
* `tidb_txn_cmd`：TiDB 执行事务相关命令的耗时，其总耗时是 9935.62 秒。

另外，`tidb_execute` 还有一条虚线箭头指向 `tidb_cop` 监控，这里虚线箭头的含义如下：

`tidb_execute` 包含 `tidb_cop` 监控的耗时，但是 cop 请求有可能并发执行。例如对两个表的进行 `join` 查询的 `execute` 耗时为 60 秒，其中 `join` 的两个表会并行地执行 cop 扫表请求。假如 cop 请求执行时间分别为 40 秒和 30 秒，那 cop 请求的总耗时是 70 秒，但是 `execute` 执行耗时只有 60 秒。所以如果父节点的耗时不完全包含子节点的耗时，就用虚线箭头来指向子节点。

> **注意：**
>
> 当节点有虚线箭头指向的子节点时，该节点的本身的耗时是不准确的。例如 `tidb_execute` 监控中，`tidb_execute` 节点本身的耗时为 `9070.18 = 19306.46 - 300.66 - 9935.62`。这里 `tidb_cop` 节点的耗时并不会计入子节点耗时的计算，但实际上，`tidb_execute` 监控本身的耗时 9070.18 秒中包含了 `tidb_cop` 一部分监控节点的耗时，但无法确认具体包含了多少耗时。

### `tidb_kv_request` 及其父节点

![监控关系图虚线节点关系](/media/dashboard/dashboard-metrics-relation-relation-example2.png)

`tidb_kv_request` 的父节点 `tidb_cop` 和 `tidb_txn_cmd.get` 都用虚拟箭头指向 `tidb_kv_request`，这里表示：

* `tidb_cop` 的耗时包含部分 `tidb_kv_request` 的耗时
* `tidb_txn_cmd.get` 的耗时也包含部分的 `tidb_kv_request` 的耗时。

但是 `tidb_cop` 具体有多少耗时是 `tidb_kv_request` 消耗的，无法进行确认。

* `tidb_kv_request.Get`：TiDB 发送 Get 类型的 kv 请求的耗时。
* `tidb_kv_request.Cop`：TiDB 发送 Cop 类型的 kv 请求的耗时。

`tidb_kv_request` 与 `tidb_kv_request.Get` 和 `tidb_kv_request.Cop` 并不是父节点包含子节点的关系，而是组成关系。子节点的名称前缀是父节点的名称加上 `.xxx`，即为父节点的子类。这里可以理解为，TiDB 发送 kv 请求的总耗时为 14745.07 秒，其中 `Get` 和 `Cop` 类型的 kv 请求的总耗时分别为 9798.02 秒和 4946.46 秒。
