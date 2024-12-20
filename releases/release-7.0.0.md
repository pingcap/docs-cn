---
title: TiDB 7.0.0 Release Notes
summary: 了解 TiDB 7.0.0 版本的新功能、兼容性变更、改进提升，以及错误修复。
---

# TiDB 7.0.0 Release Notes

发版日期：2023 年 3 月 30 日

TiDB 版本：7.0.0

试用链接：[快速体验](https://docs.pingcap.com/zh/tidb/v7.0/quick-start-with-tidb) | [下载离线包](https://cn.pingcap.com/product-community/?version=v7.0.0-DMR#version-list)

在 7.0.0 版本中，你可以获得以下关键特性：

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
    <td>会话级别内<a href="https://docs.pingcap.com/zh/tidb/v7.0/sql-non-prepared-plan-cache" target="_blank">无需手动准备 SQL 执行计划缓存</a>（实验特性）</td>
    <td>支持在会话级别自动重用执行计划缓存，可以减少编译并缩短相同 SQL 查询的时间，而无需事先手动准备 Prepare Statement 语句。</td>
  </tr>
  <tr>
    <td>TiFlash 支持<a href="https://docs.pingcap.com/zh/tidb/v7.0/tiflash-disaggregated-and-s3" target="_blank">存储计算分离和 S3 共享存储</a>（实验特性）</td>
    <td>TiFlash 增加云原生架构的支持作为可选项：
      <ul>
        <li>支持存算分离架构，提升 HTAP 资源的弹性能力。</li>
        <li>支持基于 S3 的存储引擎，以更低的成本提供共享存储。</li>
      </ul>
    </td>
  </tr>
  <tr>
    <td rowspan="2">稳定性与高可用</td>
    <td><a href="https://docs.pingcap.com/zh/tidb/v7.0/tidb-resource-control" target="_blank">增强了资源管控</a>（实验特性）</td>
    <td>支持使用资源组来为一个集群中的不同应用或工作负载分配和隔离资源。在这个版本中，TiDB 增加了对不同资源的绑定模式（用户级、会话级、语句级）和用户定义的优先级的支持，你还可以使用命令来对集群整体资源量进行预估。</td>
  </tr>
  <tr>
    <td>TiFlash 支持<a href="https://docs.pingcap.com/zh/tidb/v7.0/tiflash-spill-disk" target="_blank">数据落盘</a></td>
    <td>TiFlash 支持将中间结果落盘，以缓解数据密集型操作（如聚合、排序和 Hash Join）中的 OOM 问题。</td>
  </tr>
  <tr>
    <td rowspan="2">SQL</td>
    <td><a href="https://docs.pingcap.com/zh/tidb/v7.0/time-to-live" target="_blank">行级 TTL</a> (GA)</td>
    <td>支持通过后台任务自动删除超过生命周期（Time to live）的数据，并以此来自动管理数据规模并提高性能。</td>
  </tr>
  <tr>
    <td><a href="https://docs.pingcap.com/zh/tidb/v7.0/partitioned-table#重组分区" target="_blank">支持 <code>REORGANIZE PARTITION</code> 语法（List/Range 分区表）</a></td>
    <td><code>REORGANIZE PARTITION</code> 语句可用于合并相邻分区，或将一个分区拆分为多个分区，从而提升分区表的易用性。</td>
  </tr>
  <tr>
    <td rowspan="2">数据库管理与可观测性<br/></td>
    <td><a href="https://docs.pingcap.com/zh/tidb/v7.0/sql-statement-load-data" target="_blank"><code>LOAD DATA</code> 语句功能增强</a>（实验特性）</td>
    <td><code>LOAD DATA</code> 语句功能增强，例如支持从 S3/GCS 导入数据。</td>
  </tr>
  <tr>
    <td>TiCDC 支持<a href="https://docs.pingcap.com/zh/tidb/v7.0/ticdc-sink-to-cloud-storage" target="_blank">对象存储 Sink</a> (GA)</td>
    <td>TiCDC 支持将行变更事件同步到对象存储服务，包括 Amazon S3、GCS、Azure Blob Storage 和 NFS 等。</td>
  </tr>
</tbody>
</table>

## 功能详情

### 可扩展性

* TiFlash 支持存算分离和对象存储（实验特性）[#6882](https://github.com/pingcap/tiflash/issues/6882) @[flowbehappy](https://github.com/flowbehappy) @[JaySon-Huang](https://github.com/JaySon-Huang) @[breezewish](https://github.com/breezewish) @[JinheLin](https://github.com/JinheLin) @[lidezhu](https://github.com/lidezhu) @[CalvinNeo](https://github.com/CalvinNeo)

    在 v7.0.0 之前的版本中，TiFlash 为存算一体架构。在此架构下，TiFlash 节点既是存储节点，也是计算节点，TiFlash 的计算能力和存储能力无法独立扩展；同时，TiFlash 节点只能使用本地存储。

    从 v7.0.0 起，TiFlash 新增存算分离架构。在此架构下，TiFlash 节点分为 Compute Node （计算节点）和 Write Node（写入节点）两种类型，并支持兼容 S3 API 的对象存储。这两种节点都可以单独扩缩容，独立调整计算或数据存储能力。TiFlash 的存算分离架构和存算一体架构不能混合使用、相互转换，需要在部署 TiFlash 时进行相应的配置指定使用其中的一种架构。

    更多信息，请参考[用户文档](/tiflash/tiflash-disaggregated-and-s3.md)。

### 性能

* 实现 Fast Online DDL 和 PITR 的兼容 [#38045](https://github.com/pingcap/tidb/issues/38045) @[Leavrth](https://github.com/Leavrth)

    TiDB v6.5.0 中 [Fast Online DDL](/system-variables.md#tidb_ddl_enable_fast_reorg-从-v630-版本开始引入) 功能和 [PITR](/br/backup-and-restore-overview.md) 未完全兼容。在使用 TiDB v6.5.0 时，建议先停止 PITR 后台备份任务，以 Fast Online DDL 方式快速添加索引，然后再启动 PITR 备份任务实现全量数据备份。

    从 TiDB v7.0.0 开始，Fast Online DDL 和 PITR 已经完全兼容。通过 PITR 恢复集群数据时，系统将自动回放日志备份期间记录的通过 Fast Online DDL 方式添加的索引操作，达到兼容效果。

    更多信息，请参考[用户文档](/ddl-introduction.md)。

* TiFlash 引擎支持 Null-Aware Semi Join 和 Null-Aware Anti Semi Join 算子 [#6674](https://github.com/pingcap/tiflash/issues/6674) @[gengliqi](https://github.com/gengliqi)

    当使用 `IN`、`NOT IN`、`= ANY` 或 `!= ALL` 算子引导的关联子查询时，TiDB 会将其转化为 Semi Join 或 Anti Semi Join，从而提升计算性能。如果转换后的 Join key 列可能为 `NULL`，则需要具有 Null-Aware 特性的 Join 算法，即 [Null-Aware Semi Join](/explain-subqueries.md#null-aware-semi-joinin-和--any-子查询) 和 [Null-Aware Anti Semi Join](/explain-subqueries.md#null-aware-anti-semi-joinnot-in-和--all-子查询) 算子。

    在 v7.0.0 之前的版本中，TiFlash 引擎不支持 Null-Aware Semi Join 和 Null-Aware Anti Semi Join 算子，因此无法将这些子查询直接下推至 TiFlash 引擎进行计算。从 TiDB v7.0.0 开始，TiFlash 引擎支持了 Null-Aware Semi Join 和 Null-Aware Anti Semi Join 算子。如果 SQL 包含这几种关联子查询，查询的表包含 TiFlash 副本，并且启用了 [MPP 模式](/tiflash/use-tiflash-mpp-mode.md)，优化器将自动判断是否将 Null-Aware Semi Join 和 Null-Aware Anti Semi Join 算子下推至 TiFlash 引擎进行计算以提升整体性能。

    更多信息，请参考[用户文档](/tiflash/tiflash-supported-pushdown-calculations.md)。

* TiFlash 引擎支持 FastScan 功能 (GA) [#5252](https://github.com/pingcap/tiflash/issues/5252) @[hongyunyan](https://github.com/hongyunyan)

    从 v6.3.0 开始，TiFlash 引擎引入了快速扫描功能 (FastScan) 作为实验特性。在 v7.0.0 中，该功能正式 GA。你可以使用系统变量 [`tiflash_fastscan`](/system-variables.md#tiflash_fastscan-从-v630-版本开始引入) 启用快速扫描功能。通过牺牲强一致性保证，该功能可以大幅提升扫表性能。如果对应的表仅进行 `INSERT` 操作，而没有 `UPDATE`/`DELETE` 操作，则快速扫描功能在提升扫表性能的同时不会损失强一致性。

    更多信息，请参考[用户文档](/tiflash/use-fastscan.md)。

* TiFlash 查询支持延迟物化功能（实验特性）[#5829](https://github.com/pingcap/tiflash/issues/5829) @[Lloyd-Pottiger](https://github.com/Lloyd-Pottiger)

    当 `SELECT` 语句中包含过滤条件（`WHERE` 子句）时，TiFlash 默认会先读取该查询所需列的全部数据，然后再根据查询条件对数据进行过滤、聚合等计算任务。延迟物化是一种优化方式，它支持下推部分过滤条件到 TableScan 算子，即先扫描过滤条件相关的列数据，过滤得到符合条件的行后，再扫描这些行的其他列数据，继续后续计算，从而减少 IO 扫描和数据处理的计算量。

    TiFlash 延迟物化默认关闭，可以通过将系统变量 [`tidb_opt_enable_late_materialization`](/system-variables.md#tidb_opt_enable_late_materialization-从-v700-版本开始引入) 设置为 `ON` 开启。开启后，TiDB 优化器会根据统计信息和查询的过滤条件，决定哪些过滤条件会被下推到 TableScan 算子。

    更多信息，请参考[用户文档](/tiflash/tiflash-late-materialization.md)。

* 支持缓存非 Prepare 语句的执行计划（实验特性）[#36598](https://github.com/pingcap/tidb/issues/36598) @[qw4990](https://github.com/qw4990)

    执行计划缓存是提高并发 OLTP 负载能力的重要手段，TiDB 已经支持 [Prepare 语句的计划缓存](/sql-prepared-plan-cache.md)。在 v7.0.0 中，非 Prepare 语句的执行计划也能够被缓存，使执行计划缓存能够应用于更广泛的场景，从而提升 TiDB 的并发处理能力。

    这个功能目前默认关闭，你可以通过系统变量 [`tidb_enable_non_prepared_plan_cache`](/system-variables.md#tidb_enable_non_prepared_plan_cache) 打开。出于稳定性考虑，在当前版本中，TiDB 开辟了一块新的区域用于缓存非 Prepare 语句的执行计划，你可以通过系统变量 [`tidb_non_prepared_plan_cache_size`](/system-variables.md#tidb_non_prepared_plan_cache_size) 设置缓存大小。此外，该功能对 SQL 的模式也有一定的限制，具体参见[使用限制](/sql-non-prepared-plan-cache.md#限制)。

    更多信息，请参考[用户文档](/sql-non-prepared-plan-cache.md)。

* 解除执行计划缓存对子查询的限制 [#40219](https://github.com/pingcap/tidb/issues/40219) @[fzzf678](https://github.com/fzzf678)

    TiDB v7.0.0 移除了计划缓存对子查询的限制。带有子查询的 SQL 语句的执行计划可以被缓存，例如 `SELECT * FROM t WHERE a > (SELECT ...)`。这进一步扩大了执行计划缓存的应用范围，提高了 SQL 的执行效率。

    更多信息，请参考[用户文档](/sql-prepared-plan-cache.md)。

* TiKV 支持自动生成空的日志文件用于日志回收 [#14371](https://github.com/tikv/tikv/issues/14371) @[LykxSassinator](https://github.com/LykxSassinator)

    TiKV 在 v6.3.0 中引入了 [Raft 日志回收](/tikv-configuration-file.md#enable-log-recycle-从-v630-版本开始引入)特性，用以减少写负载的长尾延迟。但是，日志回收需要在 Raft 日志文件数量达到一定阈值后才能生效，使得用户无法直观感受到该特性对写负载吞吐的提升。

    为了改善用户体验，v7.0.0 正式引入了 [`raft-engine.prefill-for-recycle`](/tikv-configuration-file.md#prefill-for-recycle-从-v700-版本开始引入) 配置项，用以控制 TiKV 是否在进程启动时自动生成空的日志文件用于日志回收。该配置项启用时，TiKV 将在初始化时自动填充一批空日志文件用于日志回收，保证日志回收在初始化后立即生效。

    更多信息，请参考[用户文档](/tikv-configuration-file.md#prefill-for-recycle-从-v700-版本开始引入)。

* 支持从[窗口函数](/functions-and-operators/expressions-pushed-down.md)中推导 TopN 或 Limit 的优化规则，提升窗口函数的性能 [#13936](https://github.com/tikv/tikv/issues/13936) @[windtalker](https://github.com/windtalker)

    该功能默认关闭，需要将 session 变量 [tidb_opt_derive_topn](/system-variables.md#tidb_opt_derive_topn-从-v700-版本开始引入) 设置为 `ON` 开启。

    更多信息，请参考[用户文档](/derive-topn-from-window.md)。

* 支持通过 Fast Online DDL 创建唯一索引 [#40730](https://github.com/pingcap/tidb/issues/40730) @[tangenta](https://github.com/tangenta)

    TiDB v6.5.0 支持通过 [Fast Online DDL](/system-variables.md#tidb_ddl_enable_fast_reorg-从-v630-版本开始引入) 方式创建普通的二级索引。从 v7.0.0 开始，TiDB 支持通过 Fast Online DDL 方式创建唯一索引。相比于 TiDB v6.1.0，大表添加唯一索引的性能预期将提升数倍。

    更多信息，请参考[用户文档](/ddl-introduction.md)。

### 稳定性

* 增强了资源管控特性 (实验特性) [#38825](https://github.com/pingcap/tidb/issues/38825) @[nolouch](https://github.com/nolouch) @[BornChanger](https://github.com/BornChanger) @[glorv](https://github.com/glorv) @[tiancaiamao](https://github.com/tiancaiamao) @[Connor1996](https://github.com/Connor1996) @[JmPotato](https://github.com/JmPotato) @[hnes](https://github.com/hnes) @[CabinfeverB](https://github.com/CabinfeverB) @[HuSharp](https://github.com/HuSharp)

    TiDB 优化了基于资源组的资源管控特性。该特性将会极大地提升 TiDB 集群的资源利用效率和性能表现。资源管控特性的引入对 TiDB 具有里程碑的意义，你可以将一个分布式数据库集群划分成多个逻辑单元，将不同的数据库用户映射到对应的资源组中，并根据需要设置每个资源组的配额。当集群资源紧张时，来自同一个资源组的会话所使用的全部资源将被限制在配额内，避免其中一个资源组过度消耗，从而影响其他资源组中的会话正常运行。

    该特性也可以将多个来自不同系统的中小型应用合入一个 TiDB 集群中，个别应用的负载提升，不会影响其他应用的正常运行。而在系统负载较低的时候，繁忙的应用即使超过设定的配额，也仍然可以被分配到所需的系统资源，达到资源的最大化利用。此外，合理利用资源管控特性可以减少集群数量，降低运维难度及管理成本。

    该特性不仅提供了 Grafana 内置的 Resource Control Dashboard 展示资源的实际使用情况，协助你更合理地配置资源，还支持基于会话和语句级别（Hint）的动态资源管控能力。这些功能的引入将帮助你更精确地掌控 TiDB 集群的资源使用情况，并根据实际需要动态调整配额。

    在 v7.0.0 中，支持为资源组设置绝对的调度优先级 (PRIORITY)，保障重要业务能够获取到资源，同时也扩展了资源组的设置方式。

    你可以通过以下方式使用资源组：

    - 用户级别。通过 [`CREATE USER`](/sql-statements/sql-statement-create-user.md) 或 [`ALTER USER`](/sql-statements/sql-statement-alter-user.md) 语句将用户绑定到特定的资源组。绑定后，对应的用户新创建的会话会自动绑定对应的资源组。
    - 会话级别。通过 [`SET RESOURCE GROUP`](/sql-statements/sql-statement-set-resource-group.md) 设置当前会话的资源组。
    - 语句级别。通过 [`RESOURCE_GROUP()`](/optimizer-hints.md#resource_groupresource_group_name) 设置当前语句的资源组。

    更多信息，请参考[用户文档](/tidb-resource-control.md)。

* 支持 Fast Online DDL 的检查点机制，提升容错性和自动恢复能力 [#42164](https://github.com/pingcap/tidb/issues/42164) @[tangenta](https://github.com/tangenta)

    TiDB v7.0.0 引入 [Fast Online DDL](/system-variables.md#tidb_ddl_enable_fast_reorg-从-v630-版本开始引入) 的检查点机制，大幅提升 Fast Online DDL 的容错性和自动恢复能力。通过周期性记录并同步 DDL 进度，即使在 TiDB DDL Owner 故障重启或切换时，正在执行中的 DDL 仍能以 Fast Online DDL 方式继续执行，从而让 DDL 执行更加稳定高效。

    更多信息，请参考[用户文档](/ddl-introduction.md)。

* TiFlash 引擎支持数据落盘 (Spill to disk) [#6528](https://github.com/pingcap/tiflash/issues/6528) @[windtalker](https://github.com/windtalker)

    为了提高执行性能，TiFlash 引擎尽可能将数据全部放在内存中运行。当数据量超过内存总大小时，TiFlash 会终止查询，避免内存耗尽导致系统崩溃。因此，TiFlash 可处理的数据量受限于可用的内存大小。

    从 v7.0.0 开始，TiFlash 引擎支持数据落盘功能，通过调整算子内存使用阈值 [`tidb_max_bytes_before_tiflash_external_group_by`](/system-variables.md#tidb_max_bytes_before_tiflash_external_group_by-从-v700-版本开始引入)、[`tidb_max_bytes_before_tiflash_external_sort`](/system-variables.md#tidb_max_bytes_before_tiflash_external_sort-从-v700-版本开始引入)、[`tidb_max_bytes_before_tiflash_external_join`](/system-variables.md#tidb_max_bytes_before_tiflash_external_join-从-v700-版本开始引入)，控制对应算子的最大内存使用量。当算子使用内存超过一定阈值时，会自动将数据落盘，牺牲一定的性能，从而处理更多数据。

    更多信息，请参考[用户文档](/tiflash/tiflash-spill-disk.md)。

* 提升统计信息的收集效率 [#41930](https://github.com/pingcap/tidb/issues/41930) @[xuyifangreeneyes](https://github.com/xuyifangreeneyes)

    在 v7.0.0 中，TiDB 进一步优化了统计信息收集的逻辑，收集时间降低了约 25%。这一优化提升了中大型数据库集群的运行效率和稳定性，减少了统计信息收集对集群性能的影响。

* 新增优化器 Hint 对 MPP 进行干预 [#39710](https://github.com/pingcap/tidb/issues/39710) @[Reminiscent](https://github.com/Reminiscent)

    TiDB 在 v7.0.0 中增加了一系列优化器 Hint，来影响 MPP 操作执行计划的生成。

    - [`SHUFFLE_JOIN()`](/optimizer-hints.md#shuffle_joint1_name--tl_name-)：针对 MPP 生效。提示优化器对指定表使用 Shuffle Join 算法。
    - [`BROADCAST_JOIN()`](/optimizer-hints.md#broadcast_joint1_name--tl_name-)：针对 MPP 生效。提示优化器对指定表使用 Broadcast Join 算法。
    - [`MPP_1PHASE_AGG()`](/optimizer-hints.md#mpp_1phase_agg)：针对 MPP 生效。提示优化器对指定查询块中所有聚合函数使用一阶段聚合算法。
    - [`MPP_2PHASE_AGG()`](/optimizer-hints.md#mpp_2phase_agg)：针对 MPP 生效。提示优化器对指定查询块中所有聚合函数使用二阶段聚合算法。

  MPP 优化器 Hint 能够协助你干预 HTAP 查询，提升 HTAP 负载下的性能和稳定性。

  更多信息，请参考[用户文档](/optimizer-hints.md)。

* 优化器 Hint 可兼容指定连接方式与连接顺序 [#36600](https://github.com/pingcap/tidb/issues/36600) @[Reminiscent](https://github.com/Reminiscent)

    在 v7.0.0 中，优化器 Hint [`LEADING()`](/optimizer-hints.md#leadingt1_name--tl_name-) 能够和影响连接方式的 Hint 配合使用，两者行为兼容。在多表连接的情况下，可以有效指定最佳的连接方式和连接顺序，提升优化器 Hint 对执行计划的控制能力。

    新的 Hint 行为会有微小的变化。为确保向前兼容，TiDB 引入了变量 [`tidb_opt_advanced_join_hint`](/system-variables.md#tidb_opt_advanced_join_hint-从-v700-版本开始引入)。当此变量为 `OFF` 时，行为向前兼容。从旧版本升级到 v7.0.0 及之后版本的集群，该变量会被设置成 `OFF`。为了获取更灵活的 Hint 行为，强烈建议在确保无性能回退的情况下，将该变量切换为 `ON`。

    更多信息，请参考[用户文档](/optimizer-hints.md)。

### 高可用

* TiDB 支持 `prefer-leader` 选项，在网络不稳定的情况下提供更高的读可用性，降低响应延迟 [#40905](https://github.com/pingcap/tidb/issues/40905) @[LykxSassinator](https://github.com/LykxSassinator)

    你可以通过系统变量 [`tidb_replica_read`](/system-variables.md#tidb_replica_read-从-v40-版本开始引入) 控制 TiDB 的数据读取行为。在 v7.0.0 中，该变量新增 `prefer-leader` 选项。当设置为 `prefer-leader` 时，TiDB 会优先选择 leader 副本执行读取操作。当 leader 副本的处理速度明显变慢时，例如由于磁盘或网络性能抖动，TiDB 将选择其他可用的 follower 副本来执行读取操作，从而提高可用性并降低响应延迟。

    更多信息，请参考[用户文档](/develop/dev-guide-use-follower-read.md)。

### SQL 功能

* Time to live (TTL) 已基本可用 (GA) [#39262](https://github.com/pingcap/tidb/issues/39262) @[lcwangchao](https://github.com/lcwangchao) @[YangKeao](https://github.com/YangKeao)

    TTL 提供了行级别的生命周期控制策略。在 TiDB 中，设置了 TTL 属性的表会根据配置自动检查并删除过期的行数据。TTL 的目标是帮助用户周期性且及时地清理不需要的数据，并尽量减少对用户负载的影响。

    更多信息，请参考[用户文档](/time-to-live.md)。

* 支持 `ALTER TABLE ... REORGANIZE PARTITION` [#15000](https://github.com/pingcap/tidb/issues/15000) @[mjonss](https://github.com/mjonss)

    TiDB 支持 `ALTER TABLE... REORGANIZE PARTITION` 语法。通过该语法，你可以对表的部分或所有分区进行重新组织，包括合并、拆分、或者其他修改，并且不丢失数据。

    更多信息，请参考[用户文档](/partitioned-table.md#重组分区)。

* 支持 Key 分区 [#41364](https://github.com/pingcap/tidb/issues/41364) @[TonsnakeLin](https://github.com/TonsnakeLin)

    TiDB 支持 Key 分区。Key 分区与 Hash 分区都可以保证将数据均匀地分散到一定数量的分区里面，区别是 Hash 分区只能根据一个指定的整数表达式或字段进行分区，而 Key 分区可以根据字段列表进行分区，且 Key 分区的分区字段不局限于整数类型。

    更多信息，请参考[用户文档](/partitioned-table.md#key-分区)。

### 数据库管理

* TiCDC 支持同步变更数据至存储服务 (GA) [#6797](https://github.com/pingcap/tiflow/issues/6797) @[zhaoxinyu](https://github.com/zhaoxinyu)

    TiCDC 支持将变更数据同步到兼容 Amazon S3 协议的存储服务、GCS、Azure Blob Storage 以及 NFS 中。存储服务价格便宜，使用方便。对于不使用 Kafka 的用户，可以选择同步变更数据到存储服务。使用该功能，TiCDC 会将变更数据保存到文件，发送到存储服务中。用户自研的消费程序可以定时从存储服务读取新产生的变更数据进行数据处理。目前，TiCDC 支持将格式为 canal-json 和 CSV 的变更数据同步至存储服务。

    更多信息，请参考[用户文档](/ticdc/ticdc-sink-to-cloud-storage.md)。

* TiCDC OpenAPI v2 [#8019](https://github.com/pingcap/tiflow/issues/8019) @[sdojjy](https://github.com/sdojjy)

    TiCDC 提供 OpenAPI v2。相比 OpenAPI v1，OpenAPI v2 提供了更完整的同步任务支持。OpenAPI 提供的功能是 [`cdc cli` 工具](/ticdc/ticdc-manage-changefeed.md)的一个子集。你可以通过 OpenAPI v2 对 TiCDC 集群进行查询和运维操作，如获取 TiCDC 节点状态、检查集群健康状态、管理同步任务等。

    更多信息，请参考[用户文档](/ticdc/ticdc-open-api-v2.md)。

* [DBeaver](https://dbeaver.io/) v23.0.1 默认支持 TiDB [#17396](https://github.com/dbeaver/dbeaver/issues/17396) @[Icemap](https://github.com/Icemap)

    - 提供独立的 TiDB 模块、Icon 和标识。
    - 默认配置支持 [TiDB Cloud Serverless](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-serverless)，你可以更方便地连接 TiDB Cloud Serverless。
    - 支持识别 TiDB 版本，从而显示或隐藏外键 Tab。
    - 支持 Explain SQL 计划显示。
    - 支持 TiDB 语法高亮，如 `PESSIMISTIC`、`OPTIMISTIC`、`AUTO_RANDOM`、`PLACEMENT`、`POLICY`、`REORGANIZE`、`EXCHANGE`、`CACHE`、`NONCLUSTERED`、`CLUSTERED` 等。
    - 支持 TiDB 函数高亮，如 `TIDB_BOUNDED_STALENESS`、`TIDB_DECODE_KEY`、`TIDB_DECODE_PLAN`、`TIDB_IS_DDL_OWNER`、`TIDB_PARSE_TSO`、`TIDB_VERSION`、`TIDB_DECODE_SQL_DIGESTS`、`TIDB_SHARD` 等。

  更多信息，请参考 [DBeaver 用户文档](https://github.com/dbeaver/dbeaver/wiki)。

### 数据迁移

* 增强 `LOAD DATA` 语句功能，支持导入云存储中的数据（实验特性）[#40499](https://github.com/pingcap/tidb/issues/40499) @[lance6716](https://github.com/lance6716)

    之前，`LOAD DATA` 语句只能用于导入客户端的数据文件，如果你需要从云存储导入数据，不得不借助 TiDB Lightning 来实现。但是单独部署 TiDB Lightning 又会带来额外的部署成本和管理成本。现在可直接通过`LOAD DATA` 语句导入云存储中的数据。功能举例说明如下：

    - 支持从 Amazon S3 和 Google Cloud Storage 导入数据到 TiDB，且支持使用通配符一次性匹配多个源文件导入到 TiDB。
    - 支持 `DEFINED NULL BY` 来定义 null。
    - 支持 CSV、TSV 格式的源文件。

  更多信息，请参考[用户文档](/sql-statements/sql-statement-load-data.md)。

* TiDB Lightning 向 TiKV 传输键值对时支持启用压缩传输 [#41163](https://github.com/pingcap/tidb/issues/41163) @[sleepymole](https://github.com/sleepymole)

     自 v7.0.0 起，TiDB Lightning 正式支持将本地编码排序后的键值对在网络传输时进行压缩再发送到 TiKV，从而减少网络传输的数据量，降低 50% ~ 80% 网络带宽开销。在 v6.6.0 版本之前不支持该功能，在数据量较大的情况下，TiDB Lightning 对网络带宽要求相对较高，且会产生较高的流量费。相比 v6.6.0, v7.0.0 优化了压缩算法，能以更快的速度将数据导入到 TiKV 中。同样是开启压缩选项，v6.6.0 会增加 2 倍导入时间，而 v7.0.0 只会增加大约 60% 时间。以上的压缩率和导入时长仅供参考，不同的使用场景会有差异。

    该功能默认关闭，你可以通过将 TiDB Lightning 配置项 `compress-kv-pairs` 设置为 `"gzip"` 或者 `"gz"` 开启此功能。

    更多信息，请参考[用户文档](/tidb-lightning/tidb-lightning-configuration.md#tidb-lightning-任务配置)。

## 兼容性变更

> **注意：**
>
> 以下为从 v6.6.0 升级至当前版本 (v7.0.0) 所需兼容性变更信息。如果从 v6.5.0 或之前版本升级到当前版本，可能也需要考虑和查看中间版本 release notes 中提到的兼容性变更信息。

### MySQL 兼容性

* TiDB 移除了自增列必须是索引的约束 [#40580](https://github.com/pingcap/tidb/issues/40580) @[tiancaiamao](https://github.com/tiancaiamao)

    在 v7.0.0 之前，TiDB 自增列的行为与 MySQL 一致，要求自增列必须是索引或索引前缀。自 TiDB v7.0.0 起，TiDB 移除了自增列必须是索引或索引前缀的限制。这意味着用户现在可以更灵活地定义表的主键，并方便地使用自增列实现排序和分页，同时避免自增列带来的写入热点问题，并通过使用聚簇索引表提升查询性能。现在，你可以使用以下语法创建表：

    ```sql
    CREATE TABLE test1 (
        `id` int(11) NOT NULL AUTO_INCREMENT,
        `k` int(11) NOT NULL DEFAULT '0',
        `c` char(120) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '',
        PRIMARY KEY(`k`, `id`)
    );
    ```

    此功能不影响 TiCDC 同步数据。

    更多信息，请参考[用户文档](/mysql-compatibility.md#自增-id)。

* TiDB 支持 Key 分区类型，如下所示。

    ```sql
    CREATE TABLE employees (
    id INT NOT NULL,
    fname VARCHAR(30),
    lname VARCHAR(30),
    hired DATE NOT NULL DEFAULT '1970-01-01',
    separated DATE DEFAULT '9999-12-31',
    job_code INT,
    store_id INT) PARTITION BY KEY(store_id) PARTITIONS 4;
    ```

    自 TiDB v7.0.0 起，TiDB 支持 Key 分区，并支持解析 MySQL 的 `PARTITION BY LINEAR KEY` 语法，但会忽略其中的 `LINEAR` 关键字，只采用非线性 Hash 算法。Key 分区类型暂不支持分区字段列表为空的语句。

    更多信息，请参考[用户文档](/partitioned-table.md#key-分区)。

### 行为变更

* TiCDC 修复了 Avro 编码 `FLOAT` 类型数据错误的问题 [#8490](https://github.com/pingcap/tiflow/issues/8490) @[3AceShowHand](https://github.com/3AceShowHand)

    在升级 TiCDC 集群到 v7.0.0 时，如果使用 Avro 同步的表包含 `FLOAT` 类型数据，请在升级前手动调整 Confluent Schema Registry 的兼容性策略为 `None`，使 changefeed 能够成功更新 schema。否则，在升级之后 changefeed 将无法更新 schema 并进入错误状态。

* 自 v7.0.0 起，[`tidb_dml_batch_size`](/system-variables.md#tidb_dml_batch_size) 对 [`LOAD DATA` 语句](/sql-statements/sql-statement-load-data.md)不再生效。

### 系统变量

| 变量名  | 修改类型 | 描述 |
|--------|--|------|
| `tidb_pessimistic_txn_aggressive_locking` | 删除 | 更名为 [`tidb_pessimistic_txn_fair_locking`](/system-variables.md#tidb_pessimistic_txn_fair_locking-从-v700-版本开始引入)。|
| [`tidb_enable_non_prepared_plan_cache`](/system-variables.md#tidb_enable_non_prepared_plan_cache) | 修改 | 该变量从 v7.0.0 开始生效，用来控制是否开启[非 Prepare 语句执行计划缓存](/sql-non-prepared-plan-cache.md)。 |
| [`tidb_enable_null_aware_anti_join`](/system-variables.md#tidb_enable_null_aware_anti_join-从-v630-版本开始引入) | 修改 | 经进一步的测试后，该变量默认值从 `OFF` 修改为 `ON`，表示 TiDB 默认开启对特殊集合算子 `NOT IN` 和 `!= ALL` 引导的子查询产生的 Anti Join 采用 Null-Aware Hash Join 的执行方式。 |
| [`tidb_enable_resource_control`](/system-variables.md#tidb_enable_resource_control-从-v660-版本开始引入) | 修改 | 该变量默认值从 `OFF` 修改为 `ON`，表示默认开启集群按照资源组做资源隔离。资源管控功能在 v7.0.0 默认开启，便于你随时使用此功能。 |
| [`tidb_non_prepared_plan_cache_size`](/system-variables.md#tidb_non_prepared_plan_cache_size) | 修改 | 该变量从 v7.0.0 开始生效，用来控制[非 Prepare 语句执行计划缓存](/sql-non-prepared-plan-cache.md)最多能够缓存的计划数量。 |
| [`tidb_rc_read_check_ts`](/system-variables.md#tidb_rc_read_check_ts-从-v600-版本开始引入) | 修改 | 从 v7.0.0 开始，该变量对于使用 Prepared Statement 协议下 cursor fetch read 游标模式不再生效。  |
| [`tidb_enable_inl_join_inner_multi_pattern`](/system-variables.md#tidb_enable_inl_join_inner_multi_pattern-从-v700-版本开始引入) | 新增 | 该变量用于控制当内表上有 `Selection`/`Projection` 算子时是否支持 Index Join。 |
| [`tidb_enable_plan_cache_for_subquery`](/system-variables.md#tidb_enable_plan_cache_for_subquery-从-v700-版本开始引入) | 新增 | 该变量用于控制 Prepared Plan Cache 是否缓存包含子查询的查询。 |
| [`tidb_enable_plan_replayer_continuous_capture`](/system-variables.md#tidb_enable_plan_replayer_continuous_capture-从-v700-版本开始引入) | 新增 | 这个变量用来控制是否开启 [`PLAN REPLAYER CONTINUOUS CAPTURE`](/sql-plan-replayer.md#使用-plan-replayer-continuous-capture) 功能。默认值 `OFF` 代表关闭功能。 |
| [`tidb_load_based_replica_read_threshold`](/system-variables.md#tidb_load_based_replica_read_threshold-从-v700-版本开始引入) | 新增 | 该变量用于设置基于负载的 replica read 的触发阈值。在 v7.0.0，该变量控制的功能尚未完全生效，请保留默认值。 |
|[`tidb_opt_advanced_join_hint`](/system-variables.md#tidb_opt_advanced_join_hint-从-v700-版本开始引入) | 新增 | 这个变量用来控制用于控制连接算法的 Join Method Hint 是否会影响 Join Reorder 的优化过程。默认值为 `ON`，即采用新的兼容控制模式；`OFF` 则与 v7.0.0 以前的行为保持一致。为了向前兼容，从旧版本升级到 v7.0.0 及之后版本的集群，该变量会被设置成 `OFF`。|
| [`tidb_opt_derive_topn`](/system-variables.md#tidb_opt_derive_topn-从-v700-版本开始引入) | 新增 | 这个变量用来控制是否开启[从窗口函数中推导 TopN 或 Limit](/derive-topn-from-window.md) 的优化规则。默认值为 `OFF`，即未开启该优化规则。|
| [`tidb_opt_enable_late_materialization`](/system-variables.md#tidb_opt_enable_late_materialization-从-v700-版本开始引入) | 新增 | 这个变量用来控制是否启用 [TiFlash 延迟物化](/tiflash/tiflash-late-materialization.md)功能。默认值为 `OFF`，即未开启 TiFlash 延迟物化功能。|
| [`tidb_opt_ordering_index_selectivity_threshold`](/system-variables.md#tidb_opt_ordering_index_selectivity_threshold-从-v700-版本开始引入) | 新增 | 该变量用于当 SQL 中存在 `ORDER BY` 和 `LIMIT` 子句且带有过滤条件时，控制优化器选择索引的行为。 |
|[`tidb_pessimistic_txn_fair_locking`](/system-variables.md#tidb_pessimistic_txn_fair_locking-从-v700-版本开始引入) | 新增 | 是否对悲观锁启用加强的悲观锁唤醒模型，以降低单行冲突场景下事务的尾延迟。默认值为 `ON`，从旧版本升级到 v7.0.0 或之后版本，该变量会被设置成 `OFF`。 |
| [`tidb_ttl_running_tasks`](/system-variables.md#tidb_ttl_running_tasks-从-v700-版本开始引入) | 新增 | 这个变量用于限制整个集群内 TTL 任务的并发量。默认值 `-1` 表示与 TiKV 节点的数量相同。 |

### 配置文件参数

| 配置文件 | 配置项 | 修改类型 | 描述 |
| -------- | -------- | -------- | -------- |
| TiKV | `server.snap-max-write-bytes-per-sec` | 删除 | 更名为 [`server.snap-io-max-bytes-per-sec`](/tikv-configuration-file.md#snap-io-max-bytes-per-sec)。 |
| TiKV | [`raft-engine.enable-log-recycle`](/tikv-configuration-file.md#enable-log-recycle-从-v630-版本开始引入) | 修改 | 默认值由 `false` 变更为 `true`。 |
| TiKV | [`resolved-ts.advance-ts-interval`](/tikv-configuration-file.md#advance-ts-interval) | 修改 | 默认值由 `"1s"` 变更为 `"20s"`。该修改可以延长定期推进 Resolved TS 的时间间隔，从而减少 TiKV 节点之间的流量消耗。 |
| TiKV | [`resource-control.enabled`](/tikv-configuration-file.md#resource-control) | 修改 | 默认值由 `false` 变更为 `true`。 |
| TiKV | [`raft-engine.prefill-for-recycle`](/tikv-configuration-file.md#prefill-for-recycle-从-v700-版本开始引入) | 新增 | 控制 Raft Engine 是否自动生成空的日志文件用于日志回收。默认值为 `false`。|
| PD         | [`degraded-mode-wait-duration`](/pd-configuration-file.md#degraded-mode-wait-duration)         | 新增 | PD 中内置的 [Resource Control](/tidb-resource-control.md) 相关配置项。用于配置触发降级模式需要等待的时间。默认值为 `"0s"`。|
| PD         |  [`read-base-cost`](/pd-configuration-file.md#read-base-cost)      | 新增         |  PD 中内置的 [Resource Control](/tidb-resource-control.md) 相关配置项。用于设置每次读请求转换成 RU 的基准系数。默认值为 `0.25`。 |
| PD         |  [`read-cost-per-byte`](/pd-configuration-file.md#read-cost-per-byte)      | 新增         |  PD 中内置的 [Resource Control](/tidb-resource-control.md) 相关配置项。用于设置读流量转换成 RU 的基准系数。默认值为 `1/(64 * 1024)`。 |
| PD         |  [`read-cpu-ms-cost`](/pd-configuration-file.md#read-cpu-ms-cost)      | 新增         |  PD 中内置的 [Resource Control](/tidb-resource-control.md) 相关配置项。用于设置 CPU 转换成 RU 的基准系数。默认值为 `1/3`。 |
| PD         |  [`write-base-cost`](/pd-configuration-file.md#write-base-cost)      | 新增         |  PD 中内置的 [Resource Control](/tidb-resource-control.md) 相关配置项。用于设置每次写请求转换成 RU 的基准系数。默认值为 `1`。 |
| PD         |  [`write-cost-per-byte`](/pd-configuration-file.md#write-cost-per-byte)      | 新增         |  PD 中内置的 [Resource Control](/tidb-resource-control.md) 相关配置项。用于设置写流量转换成 RU 的基准系数。默认值为 `1/1024`。 |
| TiFlash | [`mark_cache_size`](/tiflash/tiflash-configuration.md) |  修改  | TiFlash 中数据块元信息的内存 cache 上限，默认值从 `5368709120` 修改为 `1073741824`，以减少不必要的内存占用 |
| TiFlash | [`minmax_index_cache_size`](/tiflash/tiflash-configuration.md) |  修改  | TiFlash 中数据块 min-max 索引的内存 cache 上限，默认值从 `5368709120` 修改为 `1073741824`，以减少不必要的内存占用  |
| TiFlash | [`flash.disaggregated_mode`](/tiflash/tiflash-disaggregated-and-s3.md) |  新增  | 在 TiFlash 的存算分离架构中，表示此 TiFlash 节点是 Write Node 还是 Compute Node。可选值为 `tiflash_write` 或者 `tiflash_compute`。 |
| TiFlash | [`storage.s3.endpoint`](/tiflash/tiflash-disaggregated-and-s3.md) |  新增  | S3 的 endpoint 地址。 |
| TiFlash | [`storage.s3.bucket`](/tiflash/tiflash-disaggregated-and-s3.md) |  新增  | TiFlash 的所有数据存储的 bucket。 |
| TiFlash | [`storage.s3.root`](/tiflash/tiflash-disaggregated-and-s3.md) |  新增  | S3 bucket 中数据存储的根目录。 |
| TiFlash | [`storage.s3.access_key_id`](/tiflash/tiflash-disaggregated-and-s3.md) |  新增  | 访问 S3 的 ACCESS_KEY_ID。 |
| TiFlash | [`storage.s3.secret_access_key`](/tiflash/tiflash-disaggregated-and-s3.md) |  新增  | 访问 S3 的 SECRET_ACCESS_KEY。 |
| TiFlash | [`storage.remote.cache.dir`](/tiflash/tiflash-disaggregated-and-s3.md) |  新增  | TiFlash Compute Node 的本地数据缓存目录。 |
| TiFlash | [`storage.remote.cache.capacity`](/tiflash/tiflash-disaggregated-and-s3.md) |  新增  | TiFlash Compute Node 的本地数据缓存目录的大小。 |
| TiDB Lightning   | [`add-index-by-sql`](/tidb-lightning/tidb-lightning-configuration.md#tidb-lightning-任务配置)       |    新增     |  控制物理导入模式是否通过 SQL 方式添加索引。默认为 `false`，表示 TiDB Lightning 会将行数据以及索引数据都编码成 KV pairs 后一同导入 TiKV，实现机制和历史版本保持一致。通过 SQL 方式添加索引的优点是将导入数据与导入索引分开，可以快速导入数据，即使导入数据后，索引添加失败，也不会影响数据的一致性。        |
| TiCDC      | [`enable-table-across-nodes`](/ticdc/ticdc-changefeed-config.md#ticdc-changefeed-配置文件说明)          |   新增    |    将表按 Region 个数划分成多个同步范围，这些范围可由多个 TiCDC 节点同步。    |
| TiCDC      | [`region-threshold`](/ticdc/ticdc-changefeed-config.md#ticdc-changefeed-配置文件说明)    | 新增         | 开启了 `enable-table-across-nodes` 后，该功能只对 Region 个数大于 `region-threshold` 值的表生效。      |
| DM | [`analyze`](/dm/task-configuration-file-full.md#完整配置文件示例)  | 新增 | 配置是否在 CHECKSUM 结束后对所有表逐个执行 `ANALYZE TABLE <table>` 操作，可配置 `"required"`/`"optional"`/`"off"`。默认为 `"optional"`。|
| DM | [`range-concurrency`](/dm/task-configuration-file-full.md#完整配置文件示例)  | 新增 | 配置 dm-worker 向 TiKV 写入 KV 数据的并发数。 |
| DM | [`compress-kv-pairs`](/dm/task-configuration-file-full.md#完整配置文件示例)  | 新增 | 配置 dm-worker 向 TiKV 发送 KV 数据时是否启用压缩，可配置 `"gzip"`，默认为空表示不压缩。 |
| DM | [`pd-addr`](/dm/task-configuration-file-full.md#完整配置文件示例)  | 新增 | 配置物理导入模式时连接下游 PD server 的地址，填一个或多个均可。配置项为空时，默认使用 TiDB 中查询到的 PD 地址信息。 |

## 改进提升

+ TiDB

    - 引入 `EXPAND` 算子辅助优化单个 `SELECT` 中包含多个 `DISTINCT` 的 SQL 性能 [#16581](https://github.com/pingcap/tidb/issues/16581) @[AilinKid](https://github.com/AilinKid)
    - Index Join 支持更多的 SQL 格式 [#40505](https://github.com/pingcap/tidb/issues/40505) @[Yisaer](https://github.com/Yisaer)
    - 避免某些情况下分区表数据需要在 TiDB 全局排序 [#26166](https://github.com/pingcap/tidb/issues/26166) @[Defined2014](https://github.com/Defined2014)
    - 支持同时使用 `fair lock mode` 和 `lock only if exists` 功能 [#42068](https://github.com/pingcap/tidb/issues/42068) @[MyonKeminta](https://github.com/MyonKeminta)
    - 支持打印事务慢日志以及相关事务内部事件 [#41863](https://github.com/pingcap/tidb/issues/41863) @[ekexium](https://github.com/ekexium)
    - 支持 `ILIKE` 操作符 [#40943](https://github.com/pingcap/tidb/issues/40943) @[xzhangxian1008](https://github.com/xzhangxian1008)

+ PD

    - 新增监控指标以展示 store limit 限制导致的调度生成失败 [#6043](https://github.com/tikv/pd/issues/6043) @[nolouch](https://github.com/nolouch)

+ TiFlash

    - 减少 TiFlash 在写路径上的内存使用量 [#7144](https://github.com/pingcap/tiflash/issues/7144) @[hongyunyan](https://github.com/hongyunyan)
    - 减少 TiFlash 在有较多表的情况下的重启时间 [#7146](https://github.com/pingcap/tiflash/issues/7146) @[hongyunyan](https://github.com/hongyunyan)
    - 支持下推 `ILIKE` 操作符 [#6740](https://github.com/pingcap/tiflash/issues/6740) @[xzhangxian1008](https://github.com/xzhangxian1008)

+ Tools

    + TiCDC

        - 支持在 Kafka 为下游的场景中将单个大表的数据变更分布到多个 TiCDC 节点，从而解决大规模 TiDB 集群的数据集成场景下单表扩展性的问题 [#8247](https://github.com/pingcap/tiflow/issues/8247) @[overvenus](https://github.com/overvenus)

            你可以通过设置 TiCDC 配置项 `enable_table_across_nodes` 为 `true` 来启用这个功能，并通过设置 `region_threshold` 来指定当一张表的 region 个数超过阀值时，TiCDC 开始将对应的表上的数据变更分布到多个 TiCDC 节点。

        - 支持在 redo applier 中拆分事务以提升 apply 吞吐，降低灾难场景的 RTO [#8318](https://github.com/pingcap/tiflow/issues/8318) @[CharlesCheung96](https://github.com/CharlesCheung96)
        - 改进表的调度策略，可以将单个表更均匀地拆分到各个 TiCDC 节点上 [#8247](https://github.com/pingcap/tiflow/issues/8247) @[overvenus](https://github.com/overvenus)
        - 在 MQ sink 中添加了 Large Row 监控指标 [#8286](https://github.com/pingcap/tiflow/issues/8286) @[hi-rustin](https://github.com/Rustin170506)
        - 在一个 Region 包含多个表的数据的场景下，减少了 TiKV 与 TiCDC 节点间的网络流量 [#6346](https://github.com/pingcap/tiflow/issues/6346) @[overvenus](https://github.com/overvenus)
        - 将 Checkpoint TS 和 Resolved TS 的 P99 指标的面板移动到 Lag analyze 面板 [#8524](https://github.com/pingcap/tiflow/issues/8524) @[hi-rustin](https://github.com/Rustin170506)
        - 支持在 redo log 里 apply DDL 事件 [#8361](https://github.com/pingcap/tiflow/issues/8361) @[CharlesCheung96](https://github.com/CharlesCheung96)
        - 支持根据上游写入吞吐来拆分调度表到 TiCDC 节点 [#7720](https://github.com/pingcap/tiflow/issues/7720) @[overvenus](https://github.com/overvenus)

    + TiDB Lightning

        - TiDB Lightning 的物理导入模式 (Physical Import Mode) 支持导入数据和索引分离导入，提升导入速度和稳定性 [#42132](https://github.com/pingcap/tidb/issues/42132) @[sleepymole](https://github.com/sleepymole)

            TiDB Lightning 增加 `add-index-by-sql` 参数。默认值为 `false`，表示仍然会用 TiDB Lightning 将行数据以及索引数据编码成 KV pairs 后再一同导入到 TiKV。如果设置为 `true`，表示在物理导入模式 (Physical Import Mode) 下，会在导入数据完成后，通过 `ADD INDEX` 的 SQL 语句帮你建索引，提升导入数据的速度和稳定性。

        - TiDB Lightning 增加 `tikv-importer.keyspace-name` 参数。默认值为空字符串，表示 TiDB Lightning 会去自动获取这次导入对应的 keyspace 名字。如果指定了值，那么使用指定的 keyspace 名字来导入。这个参数使得 TiDB Lightning 导入多租户的 TiDB 集群场景下可以进行灵活配置。[#41915](https://github.com/pingcap/tidb/issues/41915) @[lichunzhu](https://github.com/lichunzhu)

## 错误修复

+ TiDB

    - 修复 TiDB 从 v6.5.1 升级到新版本时遗漏部分更新的问题 [#41502](https://github.com/pingcap/tidb/issues/41502) @[chrysan](https://github.com/chrysan)
    - 修复部分系统变量升级后默认值没有修改的问题 [#41423](https://github.com/pingcap/tidb/issues/41423) @[crazycs520](https://github.com/crazycs520)
    - 修复加索引相关 Coprocessor 请求类型显示为 unknown 的问题 [#41400](https://github.com/pingcap/tidb/issues/41400) @[tangenta](https://github.com/tangenta)
    - 修复加索引时报 `PessimisticLockNotFound` 错误的问题 [#41515](https://github.com/pingcap/tidb/issues/41515) @[tangenta](https://github.com/tangenta)
    - 修复加唯一索引时误报 `found duplicate key` 错误的问题 [#41630](https://github.com/pingcap/tidb/issues/41630) @[tangenta](https://github.com/tangenta)
    - 修复加索引时 panic 的问题 [#41880](https://github.com/pingcap/tidb/issues/41880) @[tangenta](https://github.com/tangenta)
    - 修复 TiFlash 执行中遇到生成列会报错的问题 [#40663](https://github.com/pingcap/tidb/issues/40663) @[guo-shaoge](https://github.com/guo-shaoge)
    - 修复当存在时间类型时，TiDB 可能无法正确获取统计信息的问题 [#41938](https://github.com/pingcap/tidb/issues/41938) @[xuyifangreeneyes](https://github.com/xuyifangreeneyes)
    - 修复在开启 Prepared Plan Cache 的情况下，索引全表扫可能会报错的问题 [#42150](https://github.com/pingcap/tidb/issues/42150) @[fzzf678](https://github.com/fzzf678)
    - 修复 `IFNULL(NOT NULL COLUMN, ...)` 可能返回错误结果的问题 [#41734](https://github.com/pingcap/tidb/issues/41734) @[LittleFall](https://github.com/LittleFall)
    - 修复当分区表的所有数据落在单个 Region 时，TiDB 可能执行得到错误结果的问题 [#41801](https://github.com/pingcap/tidb/issues/41801) @[Defined2014](https://github.com/Defined2014)
    - 修复当同一个 SQL 中出现多个不同的分区表时，TiDB 可能执行得到错误结果的问题 [#42135](https://github.com/pingcap/tidb/issues/42135) @[mjonss](https://github.com/mjonss)
    - 修复在为分区表添加新的索引之后，该分区表可能无法正确触发统计信息的自动收集的问题 [#41638](https://github.com/pingcap/tidb/issues/41638) @[xuyifangreeneyes](https://github.com/xuyifangreeneyes)
    - 修复在连续两次收集统计信息后，TiDB 可能读取到错误的列统计信息的问题 [#42073](https://github.com/pingcap/tidb/issues/42073) @[xuyifangreeneyes](https://github.com/xuyifangreeneyes)
    - 修复在开启 Prepared Plan Cache 时 Index Merge 可能得到错误结果的问题 [#41828](https://github.com/pingcap/tidb/issues/41828) @[qw4990](https://github.com/qw4990)
    - 修复 IndexMerge 中 goroutine 泄露的问题 [#41605](https://github.com/pingcap/tidb/issues/41605) @[guo-shaoge](https://github.com/guo-shaoge)
    - 修复非 `BIGINT` 类型的无符号整数与 `STRING`/`DECIMAL` 比较时可能出现错误结果的问题 [#41736](https://github.com/pingcap/tidb/issues/41736) @[LittleFall](https://github.com/LittleFall)
    - 修复 `ANALYZE` 语句可能会因为当前 session 的前一个 `ANALYZE` 语句因为内存超限被 kill 导致当前 `ANALYZE` 语句也被 kill 的问题 [#41825](https://github.com/pingcap/tidb/issues/41825) @[XuHuaiyu](https://github.com/XuHuaiyu)
    - 修复 batch coprocessor 搜集信息过程中存在的数据竞争问题 [#41412](https://github.com/pingcap/tidb/issues/41412) @[you06](https://github.com/you06)
    - 修复 assertion 错误导致无法为分区表打印 MVCC 信息的问题 [#40629](https://github.com/pingcap/tidb/issues/40629) @[ekexium](https://github.com/ekexium)
    - 修复 `fair lock mode` 对不存在的 key 加锁处理的问题 [#41527](https://github.com/pingcap/tidb/issues/41527) @[ekexium](https://github.com/ekexium)
    - 修复 `INSERT IGNORE` 和 `REPLACE` 语句对不修改 value 的 key 没有加锁的问题 [#42121](https://github.com/pingcap/tidb/issues/42121) @[zyguan](https://github.com/zyguan)

+ PD

    - 修复了 Scatter Region 操作后 leader 分布不均衡的问题 [#6017](https://github.com/tikv/pd/issues/6017) @[HunDunDM](https://github.com/HunDunDM)
    - 修复了启动过程中获取 PD 成员时的数据竞争问题 [#6069](https://github.com/tikv/pd/issues/6069) @[rleungx](https://github.com/rleungx)
    - 修复了热点统计信息中的数据竞争问题 [#6069](https://github.com/tikv/pd/issues/6069) @[lhy1024](https://github.com/lhy1024)
    - 修复了切换 Placement Rule 时可能存在的 leader 分布不均衡的问题 [#6195](https://github.com/tikv/pd/issues/6195) @[bufferflies](https://github.com/bufferflies)

+ TiFlash

    - 修复了 Decimal 除法在某些情况下最后一位未进位的问题 [#7022](https://github.com/pingcap/tiflash/issues/7022) @[LittleFall](https://github.com/LittleFall)
    - 修复了 Decimal 转换在某些情况下进位错误的问题 [#6994](https://github.com/pingcap/tiflash/issues/6994) @[windtalker](https://github.com/windtalker)
    - 修复了开启 new collation 后 TopN/Sort 算子结果可能出错的问题 [#6807](https://github.com/pingcap/tiflash/issues/6807) @[xzhangxian1008](https://github.com/xzhangxian1008)
    - 修复了单个 TiFlash 节点聚合结果集过大（超过 1200 万）时可能会导致 TiFlash 报错的问题 [#6993](https://github.com/pingcap/tiflash/issues/6993) @[windtalker](https://github.com/windtalker)

+ Tools

    + Backup & Restore (BR)

        - 修复了在 PITR 恢复过程中等待 split Region 重试的时间不足的问题 [#42001](https://github.com/pingcap/tidb/issues/42001) @[joccau](https://github.com/joccau)
        - 修复了在 PITR 恢复过程遇到 `memory is limited` 错误导致恢复失败的问题 [#41983](https://github.com/pingcap/tidb/issues/41983) @[joccau](https://github.com/joccau)
        - 修复了 PD 节点宕机可能导致 PITR 日志备份进度不推进的问题 [#14184](https://github.com/tikv/tikv/issues/14184) @[YuJuncen](https://github.com/YuJuncen)
        - 缓解了 Region leadership 迁移导致 PITR 日志备份进度延迟变高的问题 [#13638](https://github.com/tikv/tikv/issues/13638) @[YuJuncen](https://github.com/YuJuncen)

    + TiCDC

        - 修复了重启 changefeed 可能导致数据丢失或者 checkpoint 无法推进的问题 [#8242](https://github.com/pingcap/tiflow/issues/8242) @[overvenus](https://github.com/overvenus)
        - 修复了 DDL sink 出现的数据竞争问题 [#8238](https://github.com/pingcap/tiflow/issues/8238) @[3AceShowHand](https://github.com/3AceShowHand)
        - 修复了状态为 `stopped` 的 changefeed 可能会自动重启的问题 [#8330](https://github.com/pingcap/tiflow/issues/8330) @[sdojjy](https://github.com/sdojjy)
        - 修复了当所有 Kafka server 不可访问时会导致 TiCDC server panic 的问题 [#8523](https://github.com/pingcap/tiflow/issues/8523) @[3AceShowHand](https://github.com/3AceShowHand)
        - 修复了下游为 MySQL 且执行语句和 TiDB 行为不兼容时可能导致数据丢失的问题 [#8453](https://github.com/pingcap/tiflow/issues/8453) @[asddongmen](https://github.com/asddongmen)
        - 修复了 rolling upgrade 可能导致 TiCDC OOM 或者 checkpoint 卡住的问题 [#8329](https://github.com/pingcap/tiflow/issues/8329) @[overvenus](https://github.com/overvenus)
        - 修复了 Kubernetes 上不能平滑升级 (graceful upgrade) TiCDC 集群的问题 [#8484](https://github.com/pingcap/tiflow/issues/8484) @[overvenus](https://github.com/overvenus)

    + TiDB Data Migration (DM)

        - 修复了 DM worker 节点使用 Google Cloud Storage 时，由于断点续传信息记录过于频繁，达到了 Google Cloud Storage 的请求频次上限，导致 DM worker 无法把数据写入 Google Cloud Storage 中，从而导致全量数据加载失败的问题 [#8482](https://github.com/pingcap/tiflow/issues/8482) @[maxshuang](https://github.com/maxshuang)
        - 修复了在多个导入任务同时同步同一个下游的数据，并且都使用了下游元数据表来记录断点续传信息时，所有任务的断点续传信息被写入了同一张元数据表，并且使用了相同的任务 ID 的问题 [#8500](https://github.com/pingcap/tiflow/issues/8500) @[maxshuang](https://github.com/maxshuang)

    + TiDB Lightning

        - 修复了当使用物理导入模式导入数据时，如果目标表的复合主键中存在 `auto_random` 列，但源数据中没有指定该列的值，TiDB Lightning 不能为 `auto_random` 列自动生成数据的问题 [#41454](https://github.com/pingcap/tidb/issues/41454) @[D3Hunter](https://github.com/D3Hunter)
        - 修复了当使用 TiDB Lightning 的逻辑导入模式导入数据时，由于目标集群用户没有 `CONFIG` 权限导致导入失败的问题 [#41915](https://github.com/pingcap/tidb/issues/41915) @[lichunzhu](https://github.com/lichunzhu)

## 贡献者

感谢来自 TiDB 社区的贡献者们：

- [AntiTopQuark](https://github.com/AntiTopQuark)
- [blacktear23](https://github.com/blacktear23)
- [BornChanger](https://github.com/BornChanger)
- [Dousir9](https://github.com/Dousir9)
- [erwadba](https://github.com/erwadba)
- [happy-v587](https://github.com/happy-v587)
- [jiyfhust](https://github.com/jiyfhust)
- [L-maple](https://github.com/L-maple)
- [liumengya94](https://github.com/liumengya94)
- [woofyzhao](https://github.com/woofyzhao)
- [xiaguan](https://github.com/xiaguan)
