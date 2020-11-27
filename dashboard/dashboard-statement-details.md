---
title: TiDB Dashboard SQL 语句分析执行详情页面
summary: 查看单个 SQL 语句执行的详细情况
aliases: ['/docs-cn/dev/dashboard/dashboard-statement-details/','/docs-cn/dev/dashboard/dashboard-statement-detail/']
---

# TiDB Dashboard SQL 语句分析执行详情页面

在列表中点击任意一行可以进入该 SQL 语句的详情页查看更详细的信息，这此信息包括三大部分：

- SQL 语句概况：包括 SQL 模板，SQL 模板 ID，当前查看的时间范围，执行计划个数以及执行所在的数据库（下图区域 1）
- 执行计划列表：如果该 SQL 语句有多个执行计划，则显示该列表，可以选择不同的执行计划，在列表下方会显示选中的执行计划详情；如果只有一个执行计划，则该列表不显示（下图区域 2）
- 执行计划详情：显示选中的执行计划的详细信息，具体见下一小节（下图区域 3）

![详情](/media/dashboard/dashboard-statement-detail.png)

## 执行计划详情

执行计划详情包括以下内容：

- SQL 样本：该计划对应的实际执行的某一条 SQL 语句文本。时间范围内任何出现过的 SQL 都可能作为 SQL 样本。
- 执行计划：执行计划的完整内容，参阅[理解 TiDB 执行计划](/explain-overview.md)文档了解如何解读执行计划。如果选择了多个执行计划，则显示的是其中任意一个。
- 其他关于该 SQL 的基本信息、执行时间、Coprocessor 读取、事务、慢查询等信息，可点击相应标签页标题切换。

![执行计划详情](/media/dashboard/dashboard-statement-plans-detail.png)

### 基本信息

包含关于表名、索引名、执行次数、累计耗时等信息。**描述**（Description）列对各个字段进行了具体描述。

![基本信息](/media/dashboard/dashboard-statement-plans-basic.png)

### 执行时间

显示执行计划执行的各阶段所耗费时间。

> **注意：**
>
> 由于单个 SQL 语句内部可能有并行执行的操作，因此各阶段累加时间可能超出该 SQL 语句的实际执行时间。

![执行时间](/media/dashboard/dashboard-statement-plans-time.png)

### Coprocessor 读取

显示 Coprocessor 读取的相关信息。

![Coprocessor 读取](/media/dashboard/dashboard-statement-plans-cop-read.png)

### 事务

显示执行计划与事务相关的信息，比如平均写入 key 个数，最大写入 key 个数等。

![事务](/media/dashboard/dashboard-statement-plans-transaction.png)

### 慢查询

如果该执行计划执行过慢，则在慢查询标签页下可以看到其关联的慢查询记录。

![慢查询](/media/dashboard/dashboard-statement-plans-slow-queries.png)

该区域显示的内容结构与慢查询页面一致，详见[慢查询页面](/dashboard/dashboard-slow-query.md)。
