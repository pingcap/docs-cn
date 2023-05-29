---
title: TiDB 7.1.0 Release Notes
summary: 了解 TiDB 7.1.0 版本的新功能、兼容性变更、改进提升，以及错误修复。
---

# TiDB 7.1.0 Release Notes

TiDB 版本：7.1.0 (upcoming)

> **注意：**
>
> TiDB v7.1.0 尚未正式发布。此 Release Notes 旨在帮助你提前了解即将发布的版本，但其中内容可能会有所调整。本文列出的功能并不保证会包含在最终发布的版本中。

在 7.1.0 版本中，你可以获得以下关键特性：

<table>
<thead>
  <tr>
    <th>分类</th>
    <th>功能</th>
    <th>描述</th>
  </tr>
</thead>
<tbody>
  <tr>
    <td rowspan="2">可扩展性与性能</td>
    <td><a href="https://docs.pingcap.com/zh/tidb/dev/sql-non-prepared-plan-cache" target="_blank">会话级别非 Prepare 语句执行计划缓存</a> (GA)</td>
    <td>支持在会话级别自动重用执行计划缓存，减少查询计划时间，缩短相同 SQL 查询的时间，而无需事先手动准备 Prepare Statement 语句。</td>
  </tr>
  <tr>
    <td><a href="https://docs.pingcap.com/zh/tidb/dev/troubleshoot-hot-spot-issues#打散读热点" target="_blank">基于负载的副本读取</a></td>
    <td>在读热点场景中，TiDB 可以将热点 TiKV 节点的读请求转发到副本。该功能有效地打散了读热点并优化了集群资源的利用。你可以通过调整系统变量 <a href="https://docs.pingcap.com/zh/tidb/dev/system-variables#tidb_load_based_replica_read_threshold-从-v700-版本开始引入" target="_blank"><code>tidb_load_based_replica_read_threshold</code></a> 控制基于负载的副本读取的触发阈值。</td>
  </tr>
  <tr>
    <td rowspan="1">稳定性与高可用</td>
    <td><a href="https://docs.pingcap.com/zh/tidb/dev/tidb-resource-control" target="_blank">资源管控</a> (GA)</td>
   <td>支持基于资源组的资源管控，将数据库用户映射到对应的资源组中，并根据实际需求设置每个资源组的配额。</td>
 </tr>
  <tr>
    <td rowspan="2">SQL</td>
    <td><a href="https://docs.pingcap.com/zh/tidb/dev/sql-statement-create-index#多值索引" target="_blank">多值索引</a> (GA)</td>
    <td>引入 MySQL 兼容的多值索引，增强 JSON 类型，提升 TiDB 对 MySQL 8.0 的兼容性。该功能提升了对多值列进行成员检查的效率。</td>
  </tr>
  <tr>
    <td><a href="https://docs.pingcap.com/zh/tidb/dev/generated-columns" target="_blank">生成列</a> (GA)</td>
    <td>生成列 (Generated Columns) 的值是通过实时计算列定义中的 SQL 表达式得到的。该功能将一些应用逻辑推向数据库层，从而提升查询效率。</td>
  </tr>
</tbody>
</table>

## 功能详情

### 性能

* TiFlash 查询支持延迟物化功能 (GA) [#5829](https://github.com/pingcap/tiflash/issues/5829) @[Lloyd-Pottiger](https://github.com/Lloyd-Pottiger)

    在 v7.0.0 中，TiFlash 引入了延迟物化实验特性，用于优化查询性能。该特性默认关闭（系统变量 [`tidb_opt_enable_late_materialization`](/system-variables.md#tidb_opt_enable_late_materialization-从-v700-版本开始引入) 默认为 `OFF`）。当 `SELECT` 语句中包含过滤条件（`WHERE` 子句）时，TiFlash 默认会先读取该查询所需列的全部数据，然后再根据查询条件对数据进行过滤、聚合等计算任务。开启该特性后，TiFlash 支持下推部分过滤条件到 TableScan 算子，即先扫描过滤条件相关的列数据，过滤得到符合条件的行后，再扫描这些行的其他列数据，继续后续计算，从而减少 IO 扫描和数据处理的计算量。

    从 v7.1.0 开始，TiFlash 延迟物化功能正式 GA，默认开启（系统变量 [`tidb_opt_enable_late_materialization`](/system-variables.md#tidb_opt_enable_late_materialization-从-v700-版本开始引入) 默认为 `ON`），TiDB 优化器会根据统计信息和查询的过滤条件，决定哪些过滤条件会被下推到 TableScan 算子。

    更多信息，请参考[用户文档](/tiflash/tiflash-late-materialization.md)。

* TiFlash 支持根据网络交换数据量自动选择 MPP 模式的 Join 算法 [#7084](https://github.com/pingcap/tiflash/issues/7084) @[solotzg](https://github.com/solotzg)

    TiFlash MPP 模式有多种 Join 算法。在 v7.1.0 之前的版本中，TiDB 根据变量 [`tidb_broadcast_join_threshold_count`](/system-variables.md#tidb_broadcast_join_threshold_count-从-v50-版本开始引入) 和 [`tidb_broadcast_join_threshold_size`](/system-variables.md#tidb_broadcast_join_threshold_count-从-v50-版本开始引入) 以及实际数据量决定 TiFlash MPP 模式是否使用 Broadcast Hash Join 算法。

    在 v7.1.0 中，TiDB 引入变量 [`tidb_prefer_broadcast_join_by_exchange_data_size`](/system-variables.md#tidb_prefer_broadcast_join_by_exchange_data_size-从-v710-版本开始引入)，控制是否基于最小网络数据交换策略选择 MPP Join 算法。该变量默认关闭，表示默认保持 v7.1.0 之前的算法选择策略。如需开启，请设置该变量为 `ON`。开启后，你无需再手动调整 [`tidb_broadcast_join_threshold_count`](/system-variables.md#tidb_broadcast_join_threshold_count-从-v50-版本开始引入) 和 [`tidb_broadcast_join_threshold_size`](/system-variables.md#tidb_broadcast_join_threshold_count-从-v50-版本开始引入) 的阈值（此时这两个变量将不再生效），TiDB 会自动估算不同 Join 算法所需进行网络交换的数据量，然后选择综合开销较小的算法，从而减少网络流量，提升 MPP 查询性能。

    更多信息，请参考[用户文档](/tiflash/use-tiflash-mpp-mode.md#mpp-模式的算法支持)。

* 支持自适应副本读取缓解读热点 [#14151](https://github.com/tikv/tikv/issues/14151) @[sticnarf](https://github.com/sticnarf) @[you06](https://github.com/you06)

    在读热点场景中，热点 TiKV 无法及时处理读请求，导致读请求排队。但是，此时并非所有 TiKV 资源都已耗尽。为了降低延迟，TiDB v7.1.0 引入了负载自适应副本读取功能，允许从其他有可用资源的 TiKV 节点读取副本，而无需在热点 TiKV 节点排队等待。你可以通过 [`tidb_load_based_replica_read_threshold`](/system-variables.md#tidb_load_based_replica_read_threshold-从-v700-版本开始引入) 系统变量控制读请求的排队长度。当 leader 节点的预估排队时间超过该阈值时，TiDB 会优先从 follower 节点读取数据。在读热点的情况下，与不打散读热点相比，该功能可提高读取吞吐量 70%～200%。

    更多信息，请参考[用户文档](/troubleshoot-hot-spot-issues.md#打散读热点)。

* 支持缓存非 Prepare 语句的执行计划 (GA) [#36598](https://github.com/pingcap/tidb/issues/36598) @[qw4990](https://github.com/qw4990)

    TiDB v7.0.0 引入了非 Prepare 语句的执行计划缓存作为实验特性，以提升在线交易场景的并发处理能力。该功能在 v7.1.0 正式 GA 并默认打开，支持缓存更多模式的 SQL。

    为了提升内存利用率，TiDB v7.1.0 将非 Prepare 与 Prepare 语句的缓存池合并。你可以通过系统变量 [`tidb_session_plan_cache_size`](/system-variables.md#tidb_session_plan_cache_size-从-v710-版本开始引入) 设置缓存大小。原有的系统变量 [`tidb_prepared_plan_cache_size`](/system-variables.md#tidb_prepared_plan_cache_size-从-v610-版本开始引入) 和 [`tidb_non_prepared_plan_cache_size`](/system-variables.md#tidb_non_prepared_plan_cache_size) 被废弃。

    为保持向前兼容，从旧版本升级到 v7.1.0 时，缓存池大小 `tidb_session_plan_cache_size` 的值与 `tidb_prepared_plan_cache_size` 保持一致，[`tidb_enable_non_prepared_plan_cache`](/system-variables.md#tidb_enable_non_prepared_plan_cache) 保持升级前的设置。经过性能测试后，你可通过 `tidb_enable_non_prepared_plan_cache` 开启非 Parepare 语句的执行计划缓存功能。对于新创建的 v7.1.0 集群，非 Parepare 语句的缓存功能默认打开。

    更多信息，请参考[用户文档](/sql-non-prepared-plan-cache.md)。

### 稳定性

* 资源管控成为正式功能 (GA) [#38825](https://github.com/pingcap/tidb/issues/38825) @[nolouch](https://github.com/nolouch) @[BornChanger](https://github.com/BornChanger) @[glorv](https://github.com/glorv) @[tiancaiamao](https://github.com/tiancaiamao) @[Connor1996](https://github.com/Connor1996) @[JmPotato](https://github.com/JmPotato) @[hnes](https://github.com/hnes) @[CabinfeverB](https://github.com/CabinfeverB) @[HuSharp](https://github.com/HuSharp)

    TiDB 持续增强资源管控能力，在 v7.1.0 该功能正式 GA。该特性将极大地提升 TiDB 集群的资源利用率和性能表现。资源管控特性的引入对 TiDB 具有里程碑的意义，你可以将一个分布式数据库集群划分成多个逻辑单元，将不同的数据库用户映射到对应的资源组中，并根据实际需求设置每个资源组的配额。当集群资源紧张时，同一资源组内的会话所使用的全部资源将受到配额限制，防止某一资源组的过度消耗对其他资源组的会话造成影响。

    该特性也可以将多个来自不同系统的中小型应用整合到同一个 TiDB 集群中。即使某个应用的负载增加，也不会影响其他应用的正常运行。而在系统负载较低的时候，繁忙的应用即使超出设定的配额，仍可获得所需系统资源，实现资源的最大化利用。此外，合理利用资源管控特性可以减少集群数量，降低运维难度及管理成本。

    在 TiDB v7.1.0 中，该特性增加了基于实际负载和硬件部署来估算系统容量上限的能力，为你进行容量规划提供更准确的参考。这有助于你更好地管理 TiDB 的资源分配，从而满足企业级场景的稳定性需求。

    更多信息，请参考[用户文档](/tidb-resource-control.md)。

* 支持 Fast Online DDL 的检查点机制，提升容错性和自动恢复能力 [#42164](https://github.com/pingcap/tidb/issues/42164) @[tangenta](https://github.com/tangenta)

    TiDB v7.1.0 引入 [Fast Online DDL](/ddl-introduction.md) 的检查点机制，可以大幅提升 Fast Online DDL 的容错性和自动恢复能力。即使 TiDB owner 因故障重启或者切换，TiDB 也能够通过自动定期保存的检查点恢复部分进度，从而让 DDL 执行更加稳定高效。

    更多信息，请参考[用户文档](/system-variables.md#tidb_ddl_enable_fast_reorg-从-v630-版本开始引入)。

* BR 备份恢复工具支持断点恢复 [#42339](https://github.com/pingcap/tidb/issues/42339) @[Leavrth](https://github.com/Leavrth)

    快照恢复或日志恢复会因为一些可恢复性错误导致提前结束，例如硬盘空间占满、节点宕机等突发情况。在 TiDB v7.1.0 之前，即使错误被及时处理，之前恢复的进度也会作废，你需要重新进行恢复。对大规模集群来说，会造成大量额外成本。

    为了尽可能继续上一次的恢复，从 TiDB v7.1.0 起，备份恢复特性引入了断点恢复的功能。该功能可以在意外中断后保留上一次恢复的大部分进度。

    更多信息，请参考[用户文档](/br/br-checkpoint-restore.md)。

* 优化统计信息缓存加载策略 [#42160](https://github.com/pingcap/tidb/issues/42160) @[xuyifangreeneyes](https://github.com/xuyifangreeneyes)

    开启统计信息同步加载后，TiDB 可以大幅减少启动时必须载入的统计信息的数量，从而提升启动过程中统计信息的加载速度。该特性提升了 TiDB 在复杂运行环境下的稳定性，并降低了部分 TiDB 节点重启对整体服务的影响。

    更多信息，请参考[用户文档](/statistics.md#统计信息的加载)。

### SQL 功能

* 支持通过 `INSERT INTO SELECT` 语句保存 TiFlash 查询结果 (GA) [#37515](https://github.com/pingcap/tidb/issues/37515) @[gengliqi](https://github.com/gengliqi)

    从 v6.5.0 起，TiDB 支持下推 `INSERT INTO SELECT` 语句中的 `SELECT` 子句（分析查询）到 TiFlash，你可以将 TiFlash 的查询结果方便地保存到 `INSERT INTO` 指定的 TiDB 表中供后续分析使用，起到了结果缓存（即结果物化）的效果。

    在 v7.1.0 版本中，该功能正式 GA。当 TiDB 执行 `INSERT INTO SELECT` 语句中的 `SELECT` 子句时，优化器将根据 [SQL 模式](/sql-mode.md)及 TiFlash 副本的代价估算自行决定是否将查询下推至 TiFlash。因此，在实验特性阶段引入的系统变量 `tidb_enable_tiflash_read_for_write_stmt` 将被废弃。需要注意的是，TiFlash 对于 `INSERT INTO SELECT` 语句的计算规则不满足 `STRICT SQL Mode` 要求，因此只有当前会话的 [SQL 模式](/sql-mode.md)为非严格模式（即 `sql_mode` 值不包含 `STRICT_TRANS_TABLES` 和 `STRICT_ALL_TABLES`），TiDB 才允许将 `INSERT INTO SELECT` 语句中的 `SELECT` 子句下推至 TiFlash。

    更多信息，请参考[用户文档](/tiflash/tiflash-results-materialization.md)。

* MySQL 兼容的多值索引 (Multi-Valued Index) 成为正式功能 (GA) [#39592](https://github.com/pingcap/tidb/issues/39592) @[xiongjiwei](https://github.com/xiongjiwei) @[qw4990](https://github.com/qw4990) @[YangKeao](https://github.com/YangKeao)

    过滤 JSON 列中某个数组的值是一种常见操作，但使用普通索引无法加速此过程。在数组上创建多值索引可以大幅提升过滤性能。如果 JSON 列中的某个数组上存在多值索引，则函数 `MEMBER OF()`、`JSON_CONTAINS()` 和 `JSON_OVERLAPS()` 的检索条件可以利用该多值索引进行过滤，从而减少大量的 I/O 消耗，提升执行速度。

    在 v7.1.0 中，TiDB 多值索引成为正式功能 (GA)，支持更完整的数据类型，并与 TiDB 的工具链兼容。你可以在生产环境利用多值索引来加速对 JSON 数组的检索操作。

    更多信息，请参考[用户文档](/sql-statements/sql-statement-create-index.md#多值索引)。

* 完善 Hash 分区表和 Key 分区表的分区管理功能 [#42728](https://github.com/pingcap/tidb/issues/42728) @[mjonss](https://github.com/mjonss)

    在 v7.1.0 之前，TiDB 中的 Hash 分区表和 Key 分区表只支持 `TRUNCATE PARTITION` 分区管理。从 v7.1.0 开始，Hash 分区表和 Key 分区表新增支持 `ADD PARTITION` 和 `COALESCE PARTITION` 分区管理。你可以根据需要灵活调整 Hash 分区表和 Key 分区表的分区数量。例如，通过 `ADD PARTITION` 语句增加分区数量，或通过 `COALESCE PARTITION` 语句减少分区数量。

    更多信息，请参考[用户文档](/partitioned-table.md#管理-hash-分区和-key-分区)。

* Range INTERVAL 分区定义语法成为正式功能 (GA) [#35683](https://github.com/pingcap/tidb/issues/35683) @[mjonss](https://github.com/mjonss)

    在 v6.3.0 中引入的 Range INTERVAL 的分区定义语法成为正式功能 (GA)。通过该语法，你可以根据所需的间隔 (interval) 定义 Range 分区，不需要枚举所有分区，可大幅度缩短 Range 分区表的定义语句长度。语义与原有 Range 分区等价。

    更多信息，请参考[用户文档](/partitioned-table.md#range-interval-分区)。

* 生成列 (Generated Columns) 成为正式功能 (GA) @[bb7133](https://github.com/bb7133)

    生成列是数据库中非常有价值的一个功能。在创建表时，可以定义一列的值由表中其他列的值计算而来，而不是由用户显式插入或更新。这个生成列可以是虚拟列 (Virtual Column) 或存储列 (Stored Column)。TiDB 在早期版本就提供了与 MySQL 兼容的生成列功能，在 v7.1.0 中这个功能正式 GA。

    使用生成列可以提升 TiDB 对 MySQL 的兼容性，方便从 MySQL 平滑迁移到 TiDB，同时也能简化数据维护复杂度，增强数据一致性并提高查询效率。

    更多信息，请参考[用户文档](/generated-columns.md)。

### 数据库管理

* DDL 任务支持暂停和恢复操作（实验特性）[#18015](https://github.com/pingcap/tidb/issues/18015) @[godouxm](https://github.com/godouxm)

    TiDB v7.1.0 之前的版本中，当 DDL 任务执行期间遇到业务高峰时间点时，为了减少对业务的影响，只能手动取消 DDL 任务。TiDB v7.1.0 引入了 DDL 任务的暂停和恢复功能，你可以在高峰时间点暂停 DDL 任务，等到业务高峰时间结束后再恢复 DDL 任务，从而避免了 DDL 操作对业务负载的影响。

    例如，可以通过如下 `ADMIN PAUSE DDL JOBS` 或 `ADMIN RESUME DDL JOBS` 语句暂停或者恢复多个 DDL 任务：

    ```sql
    ADMIN PAUSE DDL JOBS 1,2;
    ADMIN RESUME DDL JOBS 1,2;
    ```

    更多信息，请参考[用户文档](/ddl-introduction.md#ddl-相关的命令介绍)。

### 可观测性

* 增加优化器诊断信息 [#43122](https://github.com/pingcap/tidb/issues/43122) @[time-and-fate](https://github.com/time-and-fate)

    获取充足的信息是 SQL 性能诊断的关键。在 v7.1.0 中，TiDB 持续为各种诊断工具增加优化器运行信息，以便更好地解释执行计划如何被选择，从而协助定位 SQL 性能问题。这些信息包括：

    * 在 [`PLAN REPLAYER`](/sql-plan-replayer.md) 的输出中增加 `debug_trace.json` 文件。
    * 在 [`EXPLAIN`](/explain-walkthrough.md) 的输出中为 `operator info` 添加部分统计信息详情。
    * 为[慢日志](/identify-slow-queries.md)的 `Stats` 字段添加部分统计信息详情。

  更多信息，请参考[使用 `PLAN REPLAYER` 保存和恢复集群线程信息](/sql-plan-replayer.md)、[使用 `EXPLAIN` 解读执行计划](/explain-walkthrough.md)和[慢日志查询](/identify-slow-queries.md)。

### 安全

* 更换 TiFlash 系统表信息的查询接口 [#6941](https://github.com/pingcap/tiflash/issues/6941) @[flowbehappy](https://github.com/flowbehappy)

    从 v7.1.0 起，TiFlash 在向 TiDB 提供 [`INFORMATION_SCHEMA.TIFLASH_TABLES`](/information-schema/information-schema-tiflash-tables.md) 和 [`INFORMATION_SCHEMA.TIFLASH_SEGMENTS`](/information-schema/information-schema-tiflash-segments.md) 系统表的查询服务时，不再使用 HTTP 端口，而是使用 gRPC 端口，从而避免 HTTP 服务的安全风险。

## 兼容性变更

> **注意：**
>
> 以下为从 v7.0.0 升级至当前版本 (v7.1.0) 所需兼容性变更信息。如果从 v6.6.0 或之前版本升级到当前版本，可能也需要考虑和查看中间版本 Release Notes 中提到的兼容性变更信息。

### 行为变更

* 为了提高安全性，TiFlash 废弃了 HTTP 服务端口（默认 `8123`），采用 gRPC 端口作为替代

    如果你已经将 TiFlash 升级到 v7.1.0，那么在升级 TiDB 到 v7.1.0 的过程中，TiDB 无法读取 TiFlash 系统表（[`INFORMATION_SCHEMA.TIFLASH_TABLES`](/information-schema/information-schema-tiflash-tables.md) 和 [`INFORMATION_SCHEMA.TIFLASH_SEGMENTS`](/information-schema/information-schema-tiflash-segments.md)）。

### 系统变量

| 变量名 | 修改类型 | 描述 |
|--------|------------------------------|------|
| [`tidb_enable_tiflash_read_for_write_stmt`](/system-variables.md#tidb_enable_tiflash_read_for_write_stmt-从-v630-版本开始引入) | 废弃 | 从 v7.1.0 开始，该变量废弃并且默认值从 `OFF` 修改为 `ON`。当 [`tidb_allow_mpp = ON`](/system-variables.md#tidb_allow_mpp-从-v50-版本开始引入) 时，优化器将根据 [SQL 模式](/sql-mode.md)及 TiFlash 副本的代价估算自行决定是否将查询下推至 TiFlash。 |
| [`tidb_non_prepared_plan_cache_size`](/system-variables.md#tidb_non_prepared_plan_cache_size) | 废弃 | 从 v7.1.0 起，该变量被废弃，你可以使用 [`tidb_session_plan_cache_size`](/system-variables.md#tidb_session_plan_cache_size-从-v710-版本开始引入) 控制 Plan Cache 最多能够缓存的计划数量。 |
| [`tidb_prepared_plan_cache_size`](/system-variables.md#tidb_prepared_plan_cache_size-从-v610-版本开始引入) | 废弃 | 从 v7.1.0 起，该变量被废弃，你可以使用 [`tidb_session_plan_cache_size`](/system-variables.md#tidb_session_plan_cache_size-从-v710-版本开始引入) 控制 Plan Cache 最多能够缓存的计划数量。 |
| `tidb_ddl_distribute_reorg` | 删除 | 重命名为 [`tidb_enable_dist_task`](/system-variables.md#tidb_enable_dist_task-从-v710-版本开始引入)。 |
| [`tidb_enable_non_prepared_plan_cache`](/system-variables.md#tidb_enable_non_prepared_plan_cache) | 修改 | 经进一步的测试后，该变量默认值从 `OFF` 修改为 `ON`，表示默认开启非 Prepare 语句执行计划缓存。 |
| [`tidb_load_based_replica_read_threshold`](/system-variables.md#tidb_load_based_replica_read_threshold-从-v700-版本开始引入) | 修改 | 该变量从 v7.1.0 开始生效，用于设置基于负载的 replica read 的触发阈值。经进一步的测试后，该变量默认值从 `"0s"` 修改为 `"1s"`。 |
| [`tidb_opt_enable_late_materialization`](/system-variables.md#tidb_opt_enable_late_materialization-从-v700-版本开始引入) | 修改 | 默认值从 `OFF` 修改为 `ON`，代表 [TiFlash 延迟物化](/tiflash/tiflash-late-materialization.md)功能默认开启。 |
| [`tidb_enable_dist_task`](/system-variables.md#tidb_enable_dist_task-从-v710-版本开始引入) | 新增 | 控制是否开启分布式执行框架。开启分布式执行后，DDL、Import 等支持的后端任务将会由集群中多个 TiDB 节点共同完成。该变量由 `tidb_ddl_distribute_reorg` 改名而来。|
| [`tidb_enable_non_prepared_plan_cache_for_dml`](/system-variables.md#tidb_enable_non_prepared_plan_cache_for_dml-从-v710-版本开始引入) | 新增 | 控制非 Prepare 语句执行计划缓存是否支持 DML 语句。 |
| [`tidb_opt_fix_control`](/system-variables.md#tidb_opt_fix_control-从-v710-版本开始引入) | 新增 | 通过设置该变量，你可以更细粒度地控制优化器的行为，并且避免集群升级后优化器行为变化导致的性能回退。 |
| [`tidb_plan_cache_invalidation_on_fresh_stats`](/system-variables.md#tidb_plan_cache_invalidation_on_fresh_stats-从-v710-版本开始引入) | 新增 | 控制当某张表上的统计信息更新后，与该表相关的 Plan Cache 是否自动失效。 |
| [`tidb_plan_cache_max_plan_size`](/system-variables.md#tidb_plan_cache_max_plan_size-从-v710-版本开始引入) | 新增 | 控制可以缓存的 Prepare 或非 Prepare 语句执行计划的最大大小。 |
| [`tidb_prefer_broadcast_join_by_exchange_data_size`](/system-variables.md#tidb_prefer_broadcast_join_by_exchange_data_size-从-v710-版本开始引入) | 新增 | 控制是否使用最小网络数据交换策略。使用该策略时，TiDB 会估算 Broadcast Hash Join 和 Shuffled Hash Join 两种算法所需进行网络交换的数据量，并选择网络交换数据量较小的算法。该功能开启后，[`tidb_broadcast_join_threshold_size`](/system-variables.md#tidb_broadcast_join_threshold_size-从-v50-版本开始引入) 和 [`tidb_broadcast_join_threshold_count`](/system-variables.md#tidb_broadcast_join_threshold_count-从-v50-版本开始引入) 将不再生效。 |
| [`tidb_session_plan_cache_size`](/system-variables.md#tidb_session_plan_cache_size-从-v710-版本开始引入) | 新增 | 控制 Plan Cache 最多能够缓存的计划数量。其中，Prepare 语句执行计划缓存和非 Prepare 语句执行计划缓存共用一个缓存。 |

### 配置文件参数

| 配置文件 | 配置项 | 修改类型 | 描述 |
| -------- | -------- | -------- | -------- |
| TiDB | [`force-init-stats`](/tidb-configuration-file.md#force-init-stats-从-v710-版本开始引入) | 新增 | 用于控制 TiDB 启动时是否在统计信息初始化完成后再对外提供服务。 |
| TiDB | [`lite-init-stats`](/tidb-configuration-file.md#lite-init-stats-从-v710-版本开始引入) | 新增 | 用于控制 TiDB 启动时是否采用轻量级的统计信息初始化。 |
| TiDB | [`timeout`](/tidb-configuration-file.md#timeout-从-v710-版本开始引入) | 新增 | 用于控制 TiDB 写日志操作的超时时间，当磁盘故障导致日志无法写入时，该配置可以让 TiDB 进程崩溃而不是卡死。默认值为 `0`，即不设定超时时间。 |
| TiKV | [`optimize-filters-for-memory`](/tikv-configuration-file.md#optimize-filters-for-memory-从-v710-版本开始引入) | 新增 | 控制是否生成能够最小化内存碎片的 Bloom/Ribbon filter。 |
| TiKV | [`ribbon-filter-above-level`](/tikv-configuration-file.md#ribbon-filter-above-level-从-v710-版本开始引入) | 新增 | 控制是否对于大于等于该值的 level 使用 Ribbon filter，对于小于该值的 level，使用非 block-based bloom filter。 |
| TiKV | [`split.byte-threshold`](/tikv-configuration-file.md#byte-threshold-从-v50-版本开始引入) | 修改 | 当 [`region-split-size`](/tikv-configuration-file.md#region-split-size) 大于等于 4 GB 时，默认值从 `30MiB` 修改为 `100MiB`。 |
| TiKV | [`split.qps-threshold`](/tikv-configuration-file.md#qps-threshold) | 修改 | 当 [`region-split-size`](/tikv-configuration-file.md#region-split-size) 大于等于 4 GB 时，默认值从 `3000` 修改为 `7000`。 |
| TiKV | [`split.region-cpu-overload-threshold-ratio`](/tikv-configuration-file.md#region-cpu-overload-threshold-ratio-从-v620-版本开始引入) | 修改 | 当 [`region-split-size`](/tikv-configuration-file.md#region-split-size) 大于等于 4 GB 时，默认值从 `0.25` 修改为 `0.75`。 |
| PD | [`store-limit-version`](/pd-configuration-file.md#store-limit-version-从-v710-版本开始引入) | 新增 | 用于设置 store limit 工作模式。可选值为 `"v1"` 和 `"v2"`。 |
| PD | [`schedule.enable-diagnostic`](/pd-configuration-file.md#enable-diagnostic-从-v630-版本开始引入) | 修改 | 默认值从 `false` 修改为 `true`，默认打开调度器的诊断功能。 |
| TiFlash | `http_port` | 删除 | 废弃 TiFlash HTTP 服务端口（默认 `8123`）。 |
| TiCDC | [`sink.enable-partition-separator`](/ticdc/ticdc-changefeed-config.md#ticdc-changefeed-配置文件说明) | 修改 | 默认值从 `false` 修改为 `true`，代表默认会将表中各个分区的数据分不同的目录来存储。建议保持该配置项为 `true` 以避免同步分区表到存储服务时可能丢数据的问题。 |

## 改进提升

+ TiFlash

    - 提升 TiFlash 在存算分离架构下的性能和稳定性 [#6882](https://github.com/pingcap/tiflash/issues/6882) @[JaySon-Huang](https://github.com/JaySon-Huang) @[breezewish](https://github.com/breezewish) @[JinheLin](https://github.com/JinheLin)
    - 支持在 Semi Join 或 Anti Semi Join 中，通过选择较小的表作为 Build 端来优化查询性能 [#7280](https://github.com/pingcap/tiflash/issues/7280) @[yibin87](https://github.com/yibin87)

+ TiCDC

    - TiCDC 过滤了由有损 DDL 语句导致的数据变更，避免发送无效数据变更 [#43227](https://github.com/pingcap/tidb/issues/43227) @[hi-rustin](https://github.com/hi-rustin)

## 贡献者

感谢来自 TiDB 社区的贡献者们：

- [ethercflow](https://github.com/ethercflow)
- [hihihuhu](https://github.com/hihihuhu)
- [jiyfhust](https://github.com/jiyfhust)
- [L-maple](https://github.com/L-maple)
- [lqs](https://github.com/lqs)
- [pingandb](https://github.com/pingandb)
- [yorkhellen](https://github.com/yorkhellen)
- [yujiarista](https://github.com/yujiarista)
