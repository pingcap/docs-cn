---
title: TiDB Dashboard SQL 语句分析执行详情页面
summary: 查看单个 SQL 语句执行的详细情况
---

# TiDB Dashboard SQL 语句分析执行详情页面

在列表中点击任意一行可以进入该 SQL 语句的详情页查看更详细的信息，此信息包括三大部分：

- SQL 语句概况：包括 SQL 模板、SQL 模板 ID、当前查看的时间范围、执行计划个数、执行所在的数据库以及快速绑定执行计划功能（下图区域 1）
- 执行计划列表：如果一个 SQL 语句有多个执行计划，则显示执行计划列表。除了文本信息显示，TiDB 自 v6.2.0 开始引入图形化执行计划，通过图形化的执行计划，你可以更清晰地了解一个语句的具体算子和对应的内容。可以选择不同的执行计划，在列表和图形下方会显示该执行计划详情（下图区域 2）
- 执行计划详情：显示选中的执行计划的详细信息，具体见下一小节（下图区域 3）

![详情](/media/dashboard/dashboard-statement-detail-v660.png)

## 快速绑定执行计划

自 v6.6.0 起，TiDB 引入了快速绑定执行计划的功能。你可以在 TiDB Dashboard 中，快速完成 SQL 语句与特定计划的绑定。

### 使用方式

#### 绑定一个执行计划

1. 点击**执行计划绑定** (Plan Binding)，弹出弹窗。

    ![快速绑定执行计划-未绑定-入口](/media/dashboard/dashboard-quick-binding-entry-notbound.png)

2. 选择一个需要绑定的执行计划，点击**绑定** (Bind)。

    ![快速绑定执行计划-弹窗](/media/dashboard/dashboard-quick-binding-popup-notbound.png)

3. 绑定成功后，可以看到**已绑定** (Bound) 提示。

    ![快速绑定执行计划-弹窗-绑定成功](/media/dashboard/dashboard-quick-binding-popup-bound.png)

#### 取消已有的执行计划绑定

1. 在已经绑定了执行计划的 SQL 语句页面上，点击**执行计划绑定** (Plan Binding)，弹出弹窗。

    ![快速绑定执行计划-已绑定-入口](/media/dashboard/dashboard-quick-binding-entry-bound.png)

2. 点击**取消绑定** (Drop)。

    ![快速绑定执行计划-弹窗-绑定成功](/media/dashboard/dashboard-quick-binding-popup-bound.png)

3. 取消成功后，可以看到**未绑定** (Not Bound) 提示。

    ![快速绑定执行计划-弹窗](/media/dashboard/dashboard-quick-binding-popup-notbound.png)

### 使用限制

目前还不支持通过 TiDB Dashboard 绑定下列语句的执行计划：

- 非 `SELECT`、`DELETE`、`UPDATE`、`INSERT`、`REPLACE` 类型语句
- 带有子查询的查询
- 访问 TiFlash 的查询
- 对三张表或更多表进行 Join 的查询

目前该功能需用户拥有 `SUPER` 权限才可使用。如果在使用过程中提示权限不足，请参考 [TiDB Dashboard 用户管理](/dashboard/dashboard-user.md)补充所需权限。

## 执行计划详情

执行计划详情包括以下内容：

- SQL 样本：该计划对应的实际执行的某一条 SQL 语句文本。时间范围内任何出现过的 SQL 都可能作为 SQL 样本。
- 执行计划：执行计划的完整内容，有表格、图形和文本三种展示形式。参阅[理解 TiDB 执行计划](/explain-overview.md)文档了解如何解读执行计划。如果选择了多个执行计划，则显示的是其中任意一个。
- 其他关于该 SQL 的基本信息、执行时间、Coprocessor 读取、事务、慢查询等信息，可点击相应标签页标题切换。

![执行计划详情](/media/dashboard/dashboard-statement-plans-detail.png)

### SQL 样本

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

![图形形态的执行计划](/media/dashboard/dashboard-visual-plan-2.png)

- 执行计划的展示顺序是从左到右，从上到下。
- 上面的节点是父算子，下面的节点是子算子。
- 节点顶栏的颜色代表算子执行的组件：黄色代表 TiDB，蓝色代表 TiKV，粉色代表 TiFlash。
- 节点的顶栏为算子的名称，正文为算子的基本信息。

点击节点区域，右侧将弹出算子的详细信息。

![图形形态的执行计划-侧栏](/media/dashboard/dashboard-visual-plan-popup.png)

### SQL 执行相关信息

其他关于该 SQL 的基本信息、执行时间、Coprocessor 读取、事务、慢查询等信息，可点击相应标签页标题切换。

![显示不同分类执行信息](/media/dashboard/dashboard-slow-queries-detail2-v620.png)

#### 基本信息

包含关于表名、索引名、执行次数、累计耗时等信息。**描述** (Description) 列对各个字段进行了具体描述。

![基本信息](/media/dashboard/dashboard-statement-plans-basic.png)

#### 执行时间

显示执行计划执行的各阶段所耗费时间。

> **注意：**
>
> 由于单个 SQL 语句内部可能有并行执行的操作，因此各阶段累加时间可能超出该 SQL 语句的实际执行时间。

![执行时间](/media/dashboard/dashboard-statement-plans-time.png)

#### Coprocessor 读取

显示 Coprocessor 读取的相关信息。

![Coprocessor 读取](/media/dashboard/dashboard-statement-plans-cop-read.png)

#### 事务

显示执行计划与事务相关的信息，比如平均写入 key 个数，最大写入 key 个数等。

![事务](/media/dashboard/dashboard-statement-plans-transaction.png)

#### 慢查询

如果该执行计划执行过慢，则在慢查询标签页下可以看到其关联的慢查询记录。

![慢查询](/media/dashboard/dashboard-statement-plans-slow-queries.png)

该区域显示的内容结构与慢查询页面一致，详见[慢查询页面](/dashboard/dashboard-slow-query.md)。
