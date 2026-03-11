---
title: TiDB Dashboard Top SQL 页面
summary: 使用 Top SQL 找到消耗 CPU、网络和逻辑 IO 资源较多的查询
---

# TiDB Dashboard Top SQL 页面

TiDB Dashboard 的 Top SQL 页面用于可视化分析指定 TiDB 或 TiKV 实例在一段时间内最消耗资源的查询。默认情况下，Top SQL 会持续采集各个 TiDB 及 TiKV 实例的 CPU 负载数据，并保留至多 30 天。对于 TiKV 实例，你还可以在设置中开启 TiKV 网络 IO 采集（多维度），进一步查看 `Network Bytes`、`Logical IO Bytes` 等指标，并按 `Query`、`Table`、`DB` 或 `Region` 维度聚合分析。

Top SQL 具有以下功能：

* 通过图表及表格展示当前时间范围内负载最高的 Top `5`、`20` 或 `100` 项记录，并自动汇总为 `Others`。
* 支持按 `CPU Time`、`Network Bytes` 排序查看负载热点；选择 TiKV 实例时，还支持 `Logical IO Bytes`。
* 支持按 `Query` 查看 SQL 与执行计划明细；选择 TiKV 实例时，还支持按 `Table`、`DB` 和 `Region` 聚合分析。
* 支持框选图表缩放时间范围、手动刷新、自动刷新以及导出 CSV。
* 支持统计所有正在执行、尚未执行完毕的 SQL 语句。
* 支持查看集群中指定 TiDB 及 TiKV 实例的情况。

## 推荐适用场景

Top SQL 适用于分析性能问题。以下列举了一些典型的 Top SQL 适用场景：

* 通过监控发现个别 TiDB 或 TiKV 实例 CPU 很高，希望快速定位是哪类 SQL 正在消耗大量 CPU 资源。
* 集群整体查询变慢，希望找出当前最消耗资源的 SQL，或者对比负载变化前后最主要的查询差异。
* 需要从更高维度定位热点，希望按 `Table`、`DB` 或 `Region` 聚合查看 TiKV 侧的资源消耗。
* 需要从网络流量或逻辑 IO 角度排查 TiKV 热点，而不仅仅局限于 CPU 视角。

Top SQL 不适用于分析以下问题：

- 不能用于解答与性能无关的问题，例如数据正确性或异常崩溃问题。
- 不适合直接分析锁冲突、事务语义错误等并非由资源消耗导致的问题。

## 访问页面

你可以通过以下任一方式访问 Top SQL 页面：

- 登录 TiDB Dashboard 后，在左侧导航栏中点击**Top SQL**。

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

启用后，你只能查看开启之后新采集到的数据；开启之前的细粒度数据不会补采。另外，数据展示通常会有约 1 分钟延迟，因此需要等待片刻才能看到新数据。关闭 Top SQL 后，如果历史数据尚未过期，页面仍然可以继续查看已有历史数据，但不会再采集新的 Top SQL 数据。

除了通过图形化界面以外，你也可以配置 TiDB 系统变量 [`tidb_enable_top_sql`](/system-variables.md#tidb_enable_top_sql-从-v540-版本开始引入) 来启用 Top SQL 功能：

{{< copyable "sql" >}}

```sql
SET GLOBAL tidb_enable_top_sql = 1;
```

### 开启 TiKV 网络 IO 采集（可选）

如果你需要在 TiKV 实例上查看 `Network Bytes`、`Logical IO Bytes`，或者使用 `By REGION` 聚合，请在同一设置面板中继续打开 **开启 TiKV 网络 IO 采集（多维度）** (Enable TiKV Network IO collection (multi-dimensional)) 开关并保存。

该设置会增加一定的存储和查询开销。开启后，系统会将配置下发到当前所有 TiKV 节点；数据同样可能有约 1 分钟延迟。若仍有部分 TiKV 节点未成功开启，页面会给出告警提示，此时新数据可能不完整。

对于后续新扩容的 TiKV 节点，这个开关不会自动生效。如果你希望新节点自动开启该能力，可以在 TiUP 集群拓扑的 `server_configs.tikv` 下增加以下配置，并通过 TiUP 重新下发 TiKV 配置：

```yaml
server_configs:
  tikv:
    resource-metering.enable-network-io-collection: true
```

关于 TiUP 拓扑配置的更多信息，请参见 [TiUP 集群拓扑文件配置](/tiup/tiup-cluster-topology-reference.md)。

## 使用 Top SQL

以下是 Top SQL 的常用步骤：

1. 访问 [Top SQL 页面](#访问页面)。

2. 选择一个你想要观察负载的具体 TiDB 或 TiKV 实例。

    ![选择实例](/media/dashboard/top-sql-usage-select-instance.png)

    如果你不知道要观察哪一个实例，可以先从 Grafana 或概况页中确认负载异常的节点，再返回 Top SQL 进一步分析。

3. 设置时间范围，并根据需要使用**刷新** (Refresh) 或自动刷新获取最新数据。

    你可以在时间选择器中调整时间范围，或在图表中框选一个时间范围来缩放观察窗口。更小的时间范围能够展示更细粒度的数据，精度最高可达 1 秒。

    ![修改时间范围](/media/dashboard/top-sql-usage-change-timerange.png)

    如果图表中显示的数据已过时，你可以点击**刷新** (Refresh) 按钮，或在**刷新** (Refresh) 下拉列表中选择自动刷新。

    ![刷新](/media/dashboard/top-sql-usage-refresh.png)

4. 选择观察模式。

    - 通过 `Limit` 选择展示 Top `5`、`20` 或 `100` 条记录。
    - 通过 `Order By` 选择按 `CPU Time` 或 `Network Bytes` 排序；如果当前选择的是 TiKV 实例，还可以按 `Logical IO Bytes` 排序。
    - 如果当前选择的是 TiKV 实例，还可以通过 `By QUERY`、`By TABLE`、`By DB` 或 `By REGION` 切换聚合维度。

    ![选择聚合维度](/media/dashboard/top-sql-usage-select-agg-by.png)

    其中，`By TABLE`、`By DB` 和 `By REGION` 仅在 TiKV 实例下可用；`By REGION` 以及 TiKV 的 `Network Bytes`、`Logical IO Bytes` 依赖于 TiKV 网络 IO 采集（多维度）已经开启。若该功能未开启，但历史数据仍然存在，页面会继续展示历史数据，并提示新数据无法完整采集。

5. 观察图表和表格中的热点记录。

    ![图表表格](/media/dashboard/top-sql-usage-chart.png)

    柱状图中的色块代表当前排序维度下的资源消耗，不同颜色表示不同记录。表格会按照当前排序维度展示累计值，并在最后额外给出 `Others` 行，用于汇总所有非 Top N 记录。

6. 在 `By QUERY` 视图中，点击表格中的某一行，展开查看该 SQL 在不同执行计划上的明细。

    ![详情](/media/dashboard/top-sql-details.png)

    你可以在明细区域查看 SQL 模板、SQL 模板 ID、Plan 模板 ID 以及执行计划文本。明细表会根据实例类型展示不同指标：

    - TiDB 实例通常显示 `Call/sec` 与 `Latency/call`。
    - TiKV 实例通常显示 `Call/sec`、`Scan Rows/sec` 和 `Scan Indexes/sec`。

    如果当前选择的是 `By TABLE`、`By DB` 或 `By REGION` 聚合视图，页面展示的是聚合结果，不再按 SQL 执行计划展开详情。

7. 在 TiKV 实例上，如果需要从更高维度定位热点，可以切换到 `By TABLE`、`By DB` 或 `By REGION`，查看聚合后的结果。

    ![按 DB 维度聚合结果页面](/media/dashboard/top-sql-usage-agg-by-db-detail.png)

8. 基于这些初步线索，进一步在 [SQL 语句分析](/dashboard/dashboard-statement-list.md)或[慢查询](/dashboard/dashboard-slow-query.md)页面中分析根因。

    在 `By QUERY` 视图中，你也可以直接点击表格中的**在 SQL 语句分析中搜索** (Search in SQL Statements) 跳转到对应的 SQL 语句分析页面。若需要离线分析当前表格结果，可以使用表格上方的 `Download to CSV` 导出数据。

## 停用 Top SQL

你可以通过以下步骤停用该功能：

1. 访问 [Top SQL 页面](#访问页面)。
2. 点击右上角**齿轮按钮**打开设置界面，将**启用特性** (Enable Feature) 下方的开关关闭。
3. 点击**保存** (Save)。
4. 在弹出的**关闭 Top SQL 功能** (Disable Top SQL Feature) 对话框中，点击**确认** (Disable)。

停用后将停止采集新的 Top SQL 数据；历史数据如果尚未过期，仍然可以继续查看。

除了通过图形化界面以外，你也可以配置 TiDB 系统变量 [`tidb_enable_top_sql`](/system-variables.md#tidb_enable_top_sql-从-v540-版本开始引入) 来停用 Top SQL 功能：

{{< copyable "sql" >}}

```sql
SET GLOBAL tidb_enable_top_sql = 0;
```

### 停用 TiKV 网络 IO 采集

如果你只想停止采集 TiKV 的 `Network Bytes`、`Logical IO Bytes` 等多维度数据，而保留 Top SQL 的 CPU 维度分析能力，可以在设置面板中关闭 **开启 TiKV 网络 IO 采集（多维度）** 开关。

关闭后：

- 页面仍可查看已经保留的历史网络 IO / 逻辑 IO 数据（如果历史数据尚未过期）。
- 新的 `Network Bytes`、`Logical IO Bytes` 和 `By REGION` 数据将不再继续采集。

## 常见问题

**1. 界面上提示“集群中未启动必要组件 NgMonitoring”无法启用功能**

请参见 [TiDB Dashboard FAQ](/dashboard/dashboard-faq.md#界面提示-集群中未启动必要组件-ngmonitoring)。

**2. 该功能开启后对集群是否有性能影响？**

Top SQL 本身对集群性能有轻微影响。根据测算，该功能对集群的平均性能影响小于 3%。如果你同时开启了 TiKV 网络 IO 采集（多维度），还会额外增加一定的存储和查询开销。

**3. 该功能目前是什么状态？**

该功能是正式特性，在生产环境中可用。

**4. 界面中的 `Others` 是什么意思？**

`Others` 表示当前排序维度下所有非 Top N 记录的汇总结果。你可以基于这一项了解 Top N 记录在整体负载中的占比。

**5. Top SQL 展示的 CPU 开销总和与进程的实际 CPU 开销是什么关系？**

它们之间有很强的相关性，但不完全一致。以 TiKV 为例，TiKV 的 CPU 开销还可能来自于其他副本的数据同步写入，这些开销不会被计入 Top SQL。但总的来说，Top SQL 中开销比例比较大的 SQL 语句实际的 CPU 资源开销也确实会更大。

**6. Top SQL 图表的纵坐标是什么意思？**

纵坐标表示当前排序维度下的资源消耗大小。选择 `CPU Time` 时表示 CPU 耗时；选择 `Network Bytes` 时表示网络字节数；选择 `Logical IO Bytes` 时表示逻辑 IO 字节数。

**7. 还没有执行完毕的 SQL 语句会被统计到吗？**

会。Top SQL 图表在每一个时间点展示的是当前所选维度下所有正在运行 SQL 的负载情况，因此尚未执行完毕的 SQL 也会被统计在内。

**8. 为什么看不到 `Network Bytes`、`Logical IO Bytes` 或 `By REGION` 的新数据？**

这些视图依赖 TiKV 网络 IO 采集（多维度）。请确认以下事项：

- 你当前选择的是 TiKV 实例。
- 设置面板中的**开启 TiKV 网络 IO 采集（多维度）**已经打开。
- 集群中的相关 TiKV 节点都已成功开启该配置；如果只有部分节点开启，页面会提示新数据可能不完整。
- 如果是新扩容的 TiKV 节点，请在 TiUP 的 TiKV 默认配置中同步开启 `resource-metering.enable-network-io-collection`，否则新节点不会自动生效。
