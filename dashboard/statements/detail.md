## 执行计划详情

执行计划详情包括以下内容：

- SQL 样本：该计划对应的实际执行的某一条 SQL 语句文本。时间范围内任何出现过的 SQL 都可能作为 SQL 样本。
- 执行计划：执行计划的完整内容，参阅「[理解 TiDB 执行计划](https://pingcap.com/docs-cn/dev/query-execution-plan/)」文档了解如何解读执行计划。如果选择了多个执行计划，则显示的是其中任意一个。
- 其他关于该 SQL 的基本信息、执行时间、Coprocessor 读取、事务、慢查询等信息，可点击相应标签页标题切换。

![详情](/media/dashboard/statement/detail.png)

### 基本信息

包含关于表名、索引名、执行次数、累计耗时等信息。「描述」（Description）列对各个字段进行了具体描述。

![基本信息](/media/dashboard/statement/plans-basic.png)

### 执行时间

显示执行计划执行的各阶段所耗费时间。

> **注意：**
>
> 由于单个 SQL 内部可能有并行执行，因此各阶段累加时间可能超出该 SQL 实际执行时间。

![执行时间](/media/dashboard/statement/plans-time.png)

### Coprocessor 读取

显示 Coprocessor 读取的相关信息。

![Coprocessor 读取](/media/dashboard/statement/plans-cop-read.png)

### 事务

显示执行计划与事务相关的信息，比如平均写入 key 个数，最大写入 key 个数等。

![事务](/media/dashboard/statement/plans-transaction.png)

### 慢查询

如果该执行计划执行过慢，则在慢查询标签页下可以看到其关联的慢查询记录。

![慢查询](/media/dashboard/statement/plans-slow-queries.png)

该区域显示的内容结构与「慢查询」页面一致，详见「慢查询页面」。
