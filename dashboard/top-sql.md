---
title: TiDB Dashboard Top SQL 页面
summary: 使用 Top SQL 找到 CPU 开销较大的 SQL 语句
---

# TiDB Dashboard Top SQL 页面

TiDB Dashboard 的 Top SQL 功能允许你可视化地监控和探索数据库中各个 SQL 语句在执行过程中的 CPU 开销情况，从而对数据库性能问题进行优化和处理。Top SQL 持续收集各个 TiDB 及 TiKV 实例每秒的实时 CPU 负载等数据（按 SQL 类型分别统计），并存储至多 30 天。你可以通过 Top SQL 展示的图表及表格快速分析某个 TiDB 或 TiKV 实例在某段时间中高 CPU 负载是来自于哪些 SQL 语句。

Top SQL 具有以下功能：

* 通过图表及表格，可视化地展示 CPU 开销最多的 5 类 SQL 语句。
* 展示每秒请求数、平均延迟、查询计划等详细执行信息。
* 支持统计所有正在执行、尚未执行完毕的 SQL 语句。
* 支持查看集群中指定 TiDB 及 TiKV 实例的情况。

## 推荐适用场景

Top SQL 适用于分析性能问题。以下列举了一些典型的 Top SQL 适用场景：

* 通过监控图发现集群中有个别 TiKV 实例的 CPU 非常高，期望了解 CPU 热点来自于哪些 SQL 语句，以便对其进行优化、更好地利用上分布式资源。
* 集群整体 CPU 占用率非常高、数据库查询缓慢，期望快速知悉目前哪些 SQL 语句开销了最多的 CPU 资源，以便对它们进行优化。
* 集群整体 CPU 占用率突然发生了显著变化，期望了解变化前后主要的 SQL 资源开销区别。
* 分析集群当前最消耗资源的 SQL 语句情况，希望对它们进行优化以便降低硬件开支。

> **注意：**
>
> Top SQL 在该版本中不支持统计那些开启 Top SQL 功能前就已在运行、当前仍然还在运行中的 SQL 语句的 CPU 开销情况。因此，建议尽早[开启 Top SQL 功能](#启用-top-sql)，而非等到已经遇到了性能问题再开启。

Top SQL 不能用于解答与性能无关的问题，例如数据正确性或异常崩溃问题。

当前 Top SQL 仍然处于早期阶段，功能正在持续加强。以下列举了一些目前暂不支持的场景，供参考：

* 暂时不支持分析 Top 5 以外 SQL 语句的开销情况（如多业务混合时）。
* 暂时不支持按 User、Database 等不同维度分析 Top N SQL 语句的开销情况。
* 暂时不支持分析并非由于 CPU 负载高导致的数据库性能问题，例如锁冲突。

## 访问页面

你可以通过以下任一方式访问 Top SQL 页面：

- 登录 TiDB Dashboard 后，在左侧导航栏中点击**Top SQL**

  ![Top SQL](/media/dashboard/top-sql-access.png)

- 在浏览器中访问 <http://127.0.0.1:2379/dashboard/#/topsql>（将 `127.0.0.1:2379` 替换为实际 PD 实例地址和端口）。

## 启用 Top SQL

> **注意：**
>
> 要使用 Top SQL，你需要使用 TiUP（v1.9.0 及以上版本）或 TiDB Operator（v1.3.0 及以上版本）部署或升级集群。如果你已经使用旧版本 TiUP 或 TiDB Operator 进行了集群升级，请参见 [FAQ](/dashboard/dashboard-faq.md#界面提示-集群中未启动必要组件-ngmonitoring) 进行处理。

Top SQL 开启后会对集群性能产生轻微的影响（平均 3% 以内），因此该功能默认关闭。你可以通过以下方法启用 Top SQL：

1. 访问 [Top SQL 页面](#访问页面)。
2. 点击**打开设置** (Open Settings)。在右侧**设置** (Settings) 页面，将**启用特性** (Enable Feature) 下方的开关打开。
3. 点击**保存** (Save)。

你仅能看到开启功能之后的 CPU 负载细节情况，在开启功能之前的 CPU 负载细节无法在界面上呈现。另外，数据有至多 1 分钟左右的延迟，因此你可能需要等待片刻才能看到数据。

> **提示：**
>
> 除了通过图形化界面以外，你也可以配置 TiDB 系统变量 [`tidb_enable_top_sql`](/system-variables.md#tidb_enable_top_sql-从-v540-版本开始引入) 来启用 Top SQL 功能：
>
> ```sql
> SET GLOBAL tidb_enable_top_sql = 1;
> ```

## 使用 Top SQL 

以下是 Top SQL 的常用步骤：

1. 访问 [Top SQL 页面](#访问页面)。

2. 选择一个你想要观察负载的具体 TiDB 或 TiKV 实例。

   ![选择实例](/media/dashboard/top-sql-usage-select-instance.png)

   如果你不知道要观察哪一个 TiDB 或 TiKV 实例，可以选择任意一个实例。在集群 CPU 开销非常不均衡的情况下，你可以首先通过 Grafana 中的 CPU 监控来确定具体期望观察的实例。

3. 观察 Top SQL 呈现的 Top 5 图表及表格。

   ![图表表格](/media/dashboard/top-sql-usage-chart.png)

   柱状图中色块的大小代表了 SQL 语句在该时刻消耗的 CPU 资源的多少，不同颜色区分了不同类型的 SQL 语句。大多数情况下，你都应该关注图表中相应时间范围内 CPU 资源开销较大的 SQL 语句。

4. 点击表格中的某一个 SQL 语句后，可以展开查看该语句不同执行计划的执行情况，例如 Call/sec（平均每秒请求数）、Scan Indexes/sec（平均每秒扫描索引数）等。

   ![详情](/media/dashboard/top-sql-details.png)

5. 基于这些初步线索，进一步在 [SQL 语句分析](/dashboard/dashboard-statement-list.md)或[慢查询](/dashboard/dashboard-slow-query.md)界面中了解该 SQL 语句开销大量 CPU 资源、或扫大量数据的详细原因。

除此以外：

* 你可以在时间选择器中调整时间范围，或在图表中框选一个时间范围，来更精确、细致地观察问题。更小的时间范围将能提供细节更丰富的数据，数据最高精度可达 1 秒。

  ![修改时间范围](/media/dashboard/top-sql-usage-change-timerange.png)

* 如果图表中显示的数据已过时，你可以点击**刷新** (Refresh) 按钮，或在**刷新** (Refresh) 下拉列表中选择自动刷新。

  ![刷新](/media/dashboard/top-sql-usage-refresh.png)

## 停用 Top SQL

你可以通过以下步骤停用该功能：

1. 访问 [Top SQL 页面](#访问页面)。
2. 点击右上角**齿轮按钮**打开设置界面，将**启用特性** (Enable Feature) 下方的开关关闭。
3. 点击**保存** (Save)。
4. 在弹出的**关闭 Top SQL 功能** (Disable Top SQL Feature) 对话框中，点击**确认** (Disable)。

> **提示：**
>
> 除了通过图形化界面以外，你也可以配置 TiDB 系统变量 [`tidb_enable_top_sql`](/system-variables.md#tidb_enable_top_sql-从-v540-版本开始引入) 来停用 Top SQL 功能：
>
> ```sql
> SET GLOBAL tidb_enable_top_sql = 0;
> ```

## 常见问题

**1. 界面上提示“集群中未启动必要组件 NgMonitoring”无法启用功能**

请参见 [TiDB Dashboard FAQ](/dashboard/dashboard-faq.md#界面提示-集群中未启动必要组件-ngmonitoring)。

**2. 该功能开启后对集群是否有性能影响？**

该功能对集群性能有轻微影响。根据我们的测算，该功能对集群的平均性能影响小于 3%。

**3. 该功能目前是什么状态？**

该功能是正式特性，在生产环境中可用。

**4. 界面中显示的其他语句（Other Statements）是什么意思？**

其他所有非 Top 5 语句产生的 CPU 开销或执行情况都会被统计在该项中。你可以基于这一项了解 Top 5 的 SQL 语句开销在整体所有 SQL 语句的 CPU 开销中的比例。

**5. Top SQL 展示的 CPU 开销总和与进程的实际 CPU 开销是什么关系？**

它们之间有很强的相关性，但不完全一致。以 TiKV 为例，TiKV 的 CPU 开销还可能来自于其他副本的数据同步写入，这些开销不会被计入 Top SQL。但总的来说，Top SQL 中开销比例比较大的 SQL 语句实际的 CPU 资源开销也确实会更大。

**6. Top SQL 图表的纵坐标是什么意思？**

代表消耗 CPU 资源的多少。消耗资源越多的 SQL 语句，该值越大。在绝大多数情况下，你都不需要关心纵坐标具体数值的含义。

**7. 还没有执行完毕的 SQL 语句会被统计到吗？**

会。Top SQL 图表上所展示的每一时刻 CPU 开销比例即为这一时刻所有正在运行的 SQL 语句的 CPU 开销情况。
