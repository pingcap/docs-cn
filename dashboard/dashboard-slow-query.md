---
title: TiDB Dashboard 慢查询页面
summary: 了解如何在 TiDB Dashboard 中查看慢查询。
---

# TiDB Dashboard 慢查询页面

该页面上能检索和查看集群中所有慢查询。

默认情况下，执行时间超过 300ms 的 SQL 查询就会被视为慢查询，被记录到[慢查询日志](/identify-slow-queries.md)中，并可通过本功能对记录到的慢查询进行查询。可调整 [`tidb_slow_log_threshold`](/system-variables.md#tidb_slow_log_threshold) SESSION 变量或 TiDB [`instance.tidb_slow_log_threshold`](/tidb-configuration-file.md#tidb_slow_log_threshold) 参数调整慢查询阈值。

> **注意：**
>
> 若关闭了慢查询日志，则本功能不可用。慢查询日志默认开启，可通过修改 TiDB 系统变量 [`tidb_enable_slow_log`](/system-variables.md#tidb_enable_slow_log) 开启或禁用。

## 访问列表页面

可以通过以下两种方法访问慢查询页面：

* 登录 TiDB Dashboard 后，在左侧导航栏中点击**慢查询** (Slow Queries)。

* 在浏览器中访问 <http://127.0.0.1:2379/dashboard/#/slow_query>（将 `127.0.0.1:2379` 替换为你的实际 PD 地址和端口）。

慢查询页面所展示的所有数据都来自于 TiDB 慢查询系统表及慢查询日志，参见[慢查询日志](/identify-slow-queries.md)文档了解详细情况。

### 修改列表过滤条件

可按时间范围、慢查询语句关联的数据库、SQL 关键字、SQL 类型、显示的慢查询语句数量等条件过滤，筛选慢查询句。如下所示，默认显示 30 分钟内最近 100 条慢查询。

![修改列表过滤条件](/media/dashboard/dashboard-slow-queries-list1-v620.png)

### 显示更多列信息

页面顶部**选择列** (**Columns**) 选项中可选择显示更多列，可将鼠标移动到列名右侧的 **(i)** 图标处查看列的说明：

![显示更多列信息](/media/dashboard/dashboard-slow-queries-list2-v620.png)

### 导出慢查询到本地

点击页面右上角 ☰ (**更多**) 可以显示**导出** (**Export**) 选项。点击**导出** (**Export**) 后，TiDB Dashboard 会将当前列表中的慢查询以 CSV 文件的格式进行导出。

![导出慢查询到本地](/media/dashboard/dashboard-slow-queries-export-v651.png)

### 修改列表排序依据

列表默认以**结束运行时间** (**Finish Time**) 逆序排序，点击不同的列标题可以修改排序依据或切换排序顺序：

![修改列表排序依据](/media/dashboard/dashboard-slow-queries-list3-v620.png)

## 查看执行详情

在列表中点击任意一行可以显示该慢查询的详细执行信息，包含：

- SQL：慢查询 SQL 文本（下图中区域 1）
- 执行计划：慢查询的执行计划（下图中区域 2）
- 其他分类好的 SQL 执行信息（下图中区域 3）

![查看执行详情](/media/dashboard/dashboard-slow-queries-detail1-v620.png)

### SQL

>**注意：**
>
> 记录在 `Query` 中的查询的长度会受到 [`tidb_stmt_summary_max_sql_length`](/system-variables.md#tidb_stmt_summary_max_sql_length-从-v40-版本开始引入) 系统变量的限制。

点击**展开** (**Expand**) 可以展开相应项的完整内容，点击**复制** (**Copy**) 可以复制内容到剪贴板。

### 执行计划

TiDB Dashboard 提供三种方式查看执行计划：表格、文本和图形。关于如何解读执行计划，请参考[理解 TiDB 执行计划](/explain-overview.md)。

#### 表格形态的执行计划

表格形态的执行计划提供详细的执行计划信息，便于你快速识别算子指标的异常情况，以及对比不同算子的状态。下图是一个表格形态的执行计划示例：

![表格形态的执行计划](/media/dashboard/dashboard-table-plan.png)

表格形态展示的内容与文本形态类似，但具有更易用的交互：

- 支持自由调整列宽
- 当内容超出列宽时，支持自动截断并提供悬浮窗展示完整信息
- 如果执行计划内容较多，可以下载 txt 格式到本地分析
- 允许隐藏任意列，并且能够在列选择中进行管理

![表格形态的执行计划-选择列](/media/dashboard/dashboard-table-plan-columnpicker.png)

#### 图形形态的执行计划

图形形态的执行计划更适合宏观地查看一个复杂 SQL 的执行计划树，并且详细了解每个算子及对应的内容。下图是一个图形形态的执行计划示例：

![可视化执行计划弹窗](/media/dashboard/dashboard-visual-plan-2.png)

- 执行计划的展示顺序是从左到右，从上到下。
- 上面的节点是父算子，下面的节点是子算子。
- 节点顶栏的颜色代表算子执行的组件：黄色代表 TiDB，蓝色代表 TiKV，粉色代表 TiFlash。
- 节点的顶栏为算子的名称，正文为算子的基本信息。

点击节点区域，右侧将弹出算子的详细信息。

![可视化执行计划弹窗-侧栏](/media/dashboard/dashboard-visual-plan-popup.png)

### SQL 执行相关信息

其他关于该 SQL 的基本信息、执行时间、Coprocessor 读取、事务、报错等信息，可点击相应标签页标题切换。

![显示不同分类执行信息](/media/dashboard/dashboard-slow-queries-detail2-v620.png)

#### 基本信息

包含关于表名、索引名、执行次数、累计耗时等信息。**描述** (Description) 列对各个字段进行了具体描述。

![基本信息](/media/dashboard/dashboard-slow-queries-detail-plans-basic.png)

#### 执行时间

显示执行计划执行的各阶段所耗费时间。

> **注意：**
>
> 由于单个 SQL 语句内部可能有并行执行的操作，因此各阶段累加时间可能超出该 SQL 语句的实际执行时间。

![执行时间](/media/dashboard/dashboard-slow-queries-detail-plans-time.png)

#### Coprocessor 读取

显示 Coprocessor 读取的相关信息。

![Coprocessor 读取](/media/dashboard/dashboard-slow-queries-detail-plans-cop-read.png)

#### 事务

显示执行计划与事务相关的信息，比如平均写入 key 个数，最大写入 key 个数等。

![事务](/media/dashboard/dashboard-slow-queries-detail-plans-transaction.png)
