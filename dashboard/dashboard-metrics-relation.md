---
title: TiDB Dashboard 监控关系图
aliases: ['/docs-cn/dev/dashboard/dashboard-metrics-relation/']
---

# TiDB Dashboard 监控关系图
监控关系图是 TiDB v4.0.7 起提供的新功能，可以将集群中各个内部流程的耗时监控数据绘制为关系图，帮助用户快速了解集群中各个环节的耗时及关系。

## 访问

登录 Dashboard 后点击左侧导航的**集群诊断**可以进入此功能页面：

![生成监控关系图首页](/media/dashboard/dashboard-metrics-relation-home.png)

设置 **区间起始时间** 和 **区间长度** 参数后，点击**生成监控关系图**按钮后，会进入监控关系图页面。

## 关系图解读

下面是一份监控耗时关系图示例，描述的是某个 TiDB 集群在 2020-07-29 16:36:00 开始往后 5 分钟内，TiDB 集群中各个监控的总耗时比例，以及各项监控之间的关系。

![监控关系图示例](/media/dashboard/dashboard-metrics-relation-example.png)

例如下面监控节点表示：tidb_execute 监控项的总耗时为 19306.46 秒，占总查询耗时的 89.4%，其中本身的耗时是 9070.18 秒，占总查询耗时的 42%。将鼠标悬停在该方框上，可以看到监控项的注释说明，总次数，平均耗时，平均 P99 耗时等更多该监控的信息。

![监控关系图 tidb_execute 节点示例](/media/dashboard/dashboard-metrics-relation-node-example.png)

### 节点的含义

每个方框节点代表一个监控项，包含了以下信息：

* 监控项的名称
* 监控项的总耗时
* 监控项总耗时和查询总耗时的比例

节点监控的总耗时 = 自己的耗时 + 孩子节点的耗时，所以有些节点还会显示自己的耗时和总耗时的比例。例如 tidb_execute 监控：

![监控关系图 tidb_execute 节点示例](/media/dashboard/dashboard-metrics-relation-node-example1.png)

* tidb_execute 是监控项的名字，该监控是指 SQL 请求在 TiDB 的执行引擎的执行消耗的时间。
* 19306.46s 表示 tidb_execute 监控项消耗的总时间为 19306.46 秒。
    * 89.40%表示19306.46 秒占所有 SQL 查询总耗时（包括用户 SQL 和 TiDB 内部的 SQL ）的比例为 89.40%，总查询耗时是 tidb_query 监控项的总耗时。
* 9070.18s 表示 tidb_execute 监控自己执行消耗的总耗时是 9070.18 秒，其余部分是被其孩子节点消耗的时间。
    * 42.00% 表示 9070.18 秒占所有查询总耗时的比例为 42.00%。

将鼠标悬停在该节点后，会看到监控项的更多详细的信息：

![监控关系图 tidb_execute 节点注释](/media/dashboard/dashboard-metrics-relation-node-example2.png)

以上信息包括该项监控的注释说明，总耗时，总次数，平均耗时和平均 P99, P90, P80 耗时。

### 监控项之间的父子关系

下面以 tidb_execute 监控为例介绍其的相关孩子节点：

![监控关系图 tidb_execute 节点注释](/media/dashboard/dashboard-metrics-relation-relation-example1.png)

可以看到，tidb_execute 包含 2 个孩子节点，分别是：

* pd_start_tso_wait: 等待事务 start_tso 的耗时，其总耗时是 300.66 秒。
* tidb_txn_cmd： TiDB 执行事务相关命令的耗时，其总耗时是 9935.62 秒。

另外，tidb_execute 还有一条虚拟线箭头指向 tidb_cop 监控，这里虚拟箭头表示：

tidb_execute 包含 tidb_cop 监控的耗时，但是由于 cop 有可能并发执行，例如两个表的 join 查询的 execute 耗时 60 秒，其中 join 的 2 个表会并行的执行 cop 扫表请求，假如 cop 请求时间分别为 40 秒和 30 秒，那 cop 的总耗时是 70 秒，但是 execute 耗时只有 60 s。所以如果父亲节点的耗时不完全包含孩子节点的耗时，就用虚线箭头来指向孩子节点。

>注意：
>
>当节点有虚线箭头指向的孩子节点时，该节点的本身的耗时是不准的，例如 tidb_execute 监控中，本身的耗时 9070.18 = 19306.46 - 300.66 - 9935.62，这里 tidb_cop 节点的耗时并不会计入孩子耗时的计算，但实际上，tidb_execute 监控本身的耗时 9070.18 秒中肯定包含一部分耗时是 tidb_cop 监控节点的耗时，但具体包含多少就能不确定了。

另一个关于虚线箭头的示例是：

![监控关系图虚线节点关系](/media/dashboard/dashboard-metrics-relation-relation-example2.png)

tidb_cop 和 tidb_txn_cmd.get 都用虚拟箭头指向 tidb_kv_request ，这里表示：

* tidb_cop 的耗时包含部分 tidb_kv_request 的耗时
* tidb_txn_cmd.get 的耗时也包含部分的 tidb_kv_request 的耗时。

但是 tidb_cop 具体有多少耗时是 tidb_kv_request 消耗的，是未知的。

最后介绍一个特殊的“父子”关系，tidb_kv_request 和它的“孩子”节点：

* tidb_kv_request.Get： tidb 发送 Get 类型的 kv 请求的耗时
* tidb_kv_request.Cop： tidb 发送 Cop 类型的 kv 请求的耗时

其实这里并不是父节点包含子节点的关系，而是组成关系，孩子节点的名字前缀是父节点的名字加上 `.xxx` 的节点是父节点的子类。这里可以理解为，tidb 发送 kv 请求的总时间为 14745.07 秒，其中 `Get` 和 `Cop` 类型的 kv 请求的总耗时分别为 9798.02 秒 和 4946.46 秒。
