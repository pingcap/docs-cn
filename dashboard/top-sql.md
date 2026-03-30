---
title: TiDB Dashboard Top SQL 页面
summary: 使用 Top SQL 找到消耗 CPU、网络和逻辑 IO 资源较多的查询
---

# TiDB Dashboard Top SQL 页面

在 TiDB Dashboard 的 Top SQL 页面，你可以查看和分析指定的 TiDB 或 TiKV 节点在一段时间内最消耗资源的 SQL 查询。

- 开启 Top SQL 后，该功能会持续采集现有 TiDB 和 TiKV 节点的 CPU 负载数据，并保留至多 30 天。
- 从 v8.5.6 和 v9.0.0 起，你还可以在 Top SQL 设置中开启 **TiKV 网络 IO 采集（多维度）**，以进一步查看指定 TiKV 节点的 `Network Bytes`、`Logical IO Bytes` 等指标，并按 `By Query`、`By Table`、`By DB` 或 `By Region` 维度进行聚合分析。

Top SQL 具有以下功能：

* 通过图表和表格展示当前时间范围内资源消耗最高的 Top `5`、`20` 或 `100` 类 SQL 查询，其余记录自动汇总为 `Others`。
* 支持按 CPU 耗时、网络字节数排序查看资源消耗热点；选择 TiKV 节点时，还支持按逻辑 IO 字节数排序。
* 支持按 Query 查看 SQL 及其执行计划详情；选择 TiKV 节点时，还支持按 `By Table`、`By DB` 和 `By Region` 聚合分析。
* 支持框选图表缩放时间范围、手动刷新、自动刷新以及导出 CSV。
* 支持统计所有正在执行、尚未执行完毕的 SQL 语句。
* 支持查看集群中指定 TiDB 及 TiKV 节点的情况。

## 推荐适用场景

Top SQL 适用于分析性能问题。以下列举了一些典型的 Top SQL 适用场景：

* 通过监控发现个别 TiDB 或 TiKV 节点 CPU 负载很高，希望快速定位是哪类 SQL 正在消耗大量 CPU 资源。
* 集群整体查询变慢，希望找出当前最消耗资源的 SQL，或者对比负载变化前后最主要的查询差异。
* 需要从更高维度定位热点，希望按 `Table`、`DB` 或 `Region` 聚合查看 TiKV 侧的资源消耗。
* 需要从网络流量或逻辑 IO 角度排查 TiKV 热点，而不仅仅局限于 CPU 维度。

Top SQL 不适用于分析以下问题：

- 不能用于解答与性能无关的问题，例如数据正确性或异常崩溃问题。
- 不适合直接分析锁冲突、事务语义错误等并非由资源消耗导致的问题。

## 访问页面

你可以通过以下任一方式访问 Top SQL 页面：

- 登录 TiDB Dashboard 后，在左侧导航栏中点击**Top SQL**。

  ![Top SQL](/media/dashboard/v8.5-top-sql-access.png)

- 在浏览器中访问 <http://127.0.0.1:2379/dashboard/#/topsql>（将 `127.0.0.1:2379` 替换为实际 PD 节点地址和端口）。

## 启用 Top SQL

> **注意：**
>
> 要使用 Top SQL，你需要使用 TiUP（v1.9.0 及以上版本）或 TiDB Operator（v1.3.0 及以上版本）部署或升级集群。如果你已经使用旧版本 TiUP 或 TiDB Operator 进行了集群升级，请参见 [FAQ](/dashboard/dashboard-faq.md#界面提示-集群中未启动必要组件-ngmonitoring) 进行处理。

Top SQL 开启后会对集群性能产生轻微的影响（平均 3% 以内），因此该功能默认关闭。你可以通过以下方法启用 Top SQL：

1. 访问 [Top SQL 页面](#访问页面)。
2. 点击**打开设置** (Open Settings)。在右侧**设置** (Settings) 页面，将**启用功能** (Enable Feature) 下方的开关打开。
3. 点击**保存** (Save)。

启用 Top SQL 后，你只能查看开启之后新采集到的数据；开启之前的历史数据不会补采。数据展示通常会有约 1 分钟的延迟，因此需要等待片刻才能看到新数据。关闭 Top SQL 后，如果历史数据尚未过期，Top SQL 页面仍然会展示这些历史数据，但不会再采集和展示新的数据。

除了通过图形化界面以外，你也可以配置 TiDB 系统变量 [`tidb_enable_top_sql`](/system-variables.md#tidb_enable_top_sql-从-v540-版本开始引入) 来启用 Top SQL 功能：

{{< copyable "sql" >}}

```sql
SET GLOBAL tidb_enable_top_sql = 1;
```

### 开启 TiKV 网络 IO 采集（可选）<span class="version-mark">从 v8.5.6 和 v9.0.0 开始引入</span>

针对 TiKV 节点，如需按照 `Order By Network`、`Order By Logical IO` 查看 Top SQL，或者使用 `By Region` 聚合，请在 Top SQL 设置面板中打开 **开启 TiKV 网络 IO 采集（多维度）** (Enable TiKV Network IO collection (multi-dimensional)) 开关并保存。

- **Order By Network**：按照 TiKV 请求处理过程中产生的网络字节数排序。
- **Order By Logical IO**：按照 TiKV 请求在 TiKV 存储层处理的逻辑数据字节数排序，例如读取过程中扫描或处理的数据量，以及写请求写入的数据量。

如下图所示，右侧**设置** (Settings) 面板中会同时显示 **启用功能** (Enable Feature) 和 **开启 TiKV 网络 IO 采集（多维度）** (Enable TiKV Network IO collection (multi-dimensional)) 两个开关。

![开启 TiKV 网络 IO 采集](/media/dashboard/v8.5-top-sql-settings-enable-tikv-network-io.png)

**开启 TiKV 网络 IO 采集（多维度）**会增加一定的存储和查询开销。开启后，系统会将配置下发到当前所有 TiKV 节点；数据展示可能同样存在约 1 分钟延迟。如果部分 TiKV 节点未成功开启该功能，页面会给出告警提示，此时新数据可能不完整。

对于后续新扩容的 TiKV 节点，这个开关不会自动生效。你需要在 Top SQL 设置面板中将 **开启 TiKV 网络 IO 采集（多维度）** 开关设置为全开并保存，使配置重新下发到所有 TiKV 节点。如果你希望新增的 TiKV 节点自动开启该功能，可以在 TiUP 集群拓扑文件的 `server_configs.tikv` 下增加以下配置，并通过 TiUP 重新下发 TiKV 配置：

```yaml
server_configs:
  tikv:
    resource-metering.enable-network-io-collection: true
```

关于 TiUP 拓扑配置的更多信息，请参见 [TiUP 集群拓扑文件配置](/tiup/tiup-cluster-topology-reference.md)。

## 使用 Top SQL

以下是 Top SQL 的常用步骤：

1. 访问 [Top SQL 页面](#访问页面)。

2. 选择一个你想要观察负载的具体 TiDB 或 TiKV 节点。

    ![选择 TiDB 或 TiKV 节点](/media/dashboard/top-sql-usage-select-instance.png)

    如果你不知道要观察哪一个节点，可以先从 Grafana 或 [TiDB Dashboard 概况页面](/dashboard/dashboard-overview.md)中定位负载异常的节点，再返回 Top SQL 页面进一步分析。

3. 设置时间范围，并根据需要刷新数据。

    你可以在时间选择器中调整时间范围，或在图表中框选一个时间范围来缩放观察窗口。更小的时间范围能够展示更细粒度的数据，精度最高可达 1 秒。

    ![修改时间范围](/media/dashboard/v8.5-top-sql-usage-change-timerange.png)

    如果图表中显示的数据已过时，你可以点击**刷新** (Refresh) 按钮执行一次刷新，或在**刷新** (Refresh) 下拉列表中选择数据自动刷新的频率。

    ![刷新](/media/dashboard/v8.5-top-sql-usage-refresh.png)

4. 选择观察模式。

    - 通过 `Limit` 选择展示 Top `5`、`20` 或 `100` 类 SQL 查询。
    - 默认的聚合维度为 `By Query`。如果当前选择的是 TiKV 节点，还可以选择按照 `By Table`、`By DB` 或 `By Region` 维度进行聚合。

        ![选择聚合维度](/media/dashboard/v8.5-top-sql-usage-select-agg-by.png)

    - 默认的排序方式是 `Order By CPU`（按 CPU 耗时排序）。如果当前选择的是 TiKV 节点且已[开启 TiKV 网络 IO 采集（多维度）](#开启-tikv-网络-io-采集可选)，还可以选择 `Order By Network`（按网络字节数排序） 或 `Order By Logical IO`（按逻辑 IO 字节数排序）。

        ![选择排序方式](/media/dashboard/v8.5-top-sql-usage-select-order-by.png)

    > **注意**
    >
    > `By Region` 以及 `Order By Network`、`Order By Logical IO` 仅在 [TiKV 网络 IO 采集（多维度）](#开启-tikv-网络-io-采集可选)开启时可选。若该功能未开启，但历史数据仍然存在，页面会继续展示历史数据，并提示新数据无法完整采集。

5. 观察图表和表格中的资源消耗热点记录。

    ![图表表格](/media/dashboard/v8.5-top-sql-usage-chart.png)

    柱状图表示当前排序维度下的资源消耗，不同颜色表示不同记录。表格会按照当前排序维度展示累计值，并在最后提供 `Others` 行，用于汇总所有非 Top N 记录。

6. 在 `By Query` 视图中，点击表格中的某一行 SQL，即可查看该类 SQL 的执行计划详情。

    ![详情](/media/dashboard/v8.5-top-sql-details.png)

    你可以在 SQL 详情中查看对应的 SQL 模板、SQL 模板 ID、Plan 模板 ID 以及执行计划文本。SQL 详情表会根据节点类型展示不同指标：

    - TiDB 节点通常显示 `Call/sec` 与 `Latency/call`。
    - TiKV 节点通常显示 `Call/sec`、`Scan Rows/sec` 和 `Scan Indexes/sec`。

    > **注意**
    >
    > 如果当前选择的是 `By Table`、`By DB` 或 `By Region` 聚合视图，页面展示的是聚合结果，不再按 SQL 执行计划展开详情。

    在 `By Query` 视图中，你也可以直接点击 Top SQL 表格中的**在 SQL 语句分析中搜索** (Search in SQL Statements) 跳转到对应的 SQL 语句分析页面。若需要离线分析当前表格结果，可以点击表格上方的 **Download to CSV** 导出当前表格数据。

7. 在 TiKV 节点上，如果需要从更高维度定位热点，可以切换到 `By Table`、`By DB` 或 `By Region`，查看聚合后的结果。

    ![按 DB 维度聚合结果页面](/media/dashboard/v8.5-top-sql-usage-agg-by-db-detail.png)

8. 基于这些初步线索，进一步在 [SQL 语句分析](/dashboard/dashboard-statement-list.md)或[慢查询](/dashboard/dashboard-slow-query.md)页面中分析根因。

## 停用 Top SQL

你可以通过以下步骤停用该功能：

1. 访问 [Top SQL 页面](#访问页面)。
2. 点击右上角**齿轮按钮**打开设置界面，将**启用功能** (Enable Feature) 下方的开关关闭。
3. 点击**保存** (Save)。
4. 在弹出的**关闭 Top SQL 功能** (Disable Top SQL Feature) 对话框中，点击**确认** (Disable)。

停用后将停止采集新的 Top SQL 数据，但历史数据在过期前仍可查看。

除了通过图形化界面以外，你也可以配置 TiDB 系统变量 [`tidb_enable_top_sql`](/system-variables.md#tidb_enable_top_sql-从-v540-版本开始引入) 来停用 Top SQL 功能：

{{< copyable "sql" >}}

```sql
SET GLOBAL tidb_enable_top_sql = 0;
```

### 停用 TiKV 网络 IO 采集

如果你只想停止采集 TiKV 的 `Network Bytes`、`Logical IO Bytes` 等多维度数据，而保留 Top SQL 的 CPU 维度分析能力，可以在 Top SQL 设置面板中关闭 **开启 TiKV 网络 IO 采集（多维度）** 开关。

关闭后：

- Top SQL 页面仍可查看之前已采集到的尚未过期的历史网络 IO 和逻辑 IO 数据。
- 新的网络 IO 和逻辑 IO 数据，以及 `By Region` 数据将不再继续采集。

## 常见问题

**1. 界面上提示“集群中未启动必要组件 NgMonitoring”无法启用功能**

请参见 [TiDB Dashboard FAQ](/dashboard/dashboard-faq.md#界面提示-集群中未启动必要组件-ngmonitoring)。

**2. 该功能开启后对集群是否有性能影响？**

开启 Top SQL 对集群性能有轻微影响。根据测算，该功能对集群的平均性能影响小于 3%。如果你同时开启了 TiKV 网络 IO 采集（多维度），还会额外增加一定的存储和查询开销。

**3. 该功能目前是什么状态？**

该功能是正式特性，在生产环境中可用。

**4. 界面中的 `Others` 是什么意思？**

`Others` 表示当前排序维度下所有非 Top N 记录的汇总结果。你可以基于这一项了解 Top N 记录在整体负载中的占比。

**5. Top SQL 展示的 CPU 开销总和与进程的实际 CPU 开销是什么关系？**

它们之间有很强的相关性，但不完全一致。以 TiKV 为例，TiKV 的 CPU 开销还可能来自于其他副本的数据同步写入，这些开销不会被计入 Top SQL。但总的来说，Top SQL 中开销比例比较大的 SQL 语句实际的 CPU 资源开销也确实会更大。

**6. Top SQL 图表的纵坐标是什么意思？**

Top SQL 图表纵坐标表示当前排序维度下的资源消耗大小。

- 选择 `Order By CPU` 时，纵坐标表示 CPU 耗时。
- 选择 `Order By Network` 时，纵坐标表示网络字节数。
- 选择 `Order By Logical IO` 时，纵坐标表示逻辑 IO 字节数。

**7. 还没有执行完毕的 SQL 语句会被统计到吗？**

会。TiDB Dashboard 会统计 Top SQL 开启后所有正在运行或已经执行完成的 SQL 的资源消耗，因此尚未执行完毕的 SQL 也会被统计在内。

**8. 为什么看不到 `Order By Network`、`Order By Logical IO` 或 `By Region` 的新数据？**

这些视图依赖 TiKV 网络 IO 采集（多维度）。请确认以下事项：

- 你当前选择的是 TiKV 节点。
- Top SQL 设置面板中的**开启 TiKV 网络 IO 采集（多维度）**已经打开。
- 集群中的相关 TiKV 节点都已成功开启该配置；如果只有部分节点开启，Top SQL 页面会提示新数据可能不完整。
- 如果是新扩容的 TiKV 节点，需要重新在 Top SQL 设置面板中手工操作一次 **开启 TiKV 网络 IO 采集（多维度）** 开关并保存；如果希望后续扩容节点自动生效，请在 TiUP 的 TiKV 默认配置中同步开启 `resource-metering.enable-network-io-collection`。
