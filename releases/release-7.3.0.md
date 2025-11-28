---
title: TiDB 7.3.0 Release Notes
summary: 了解 TiDB 7.3.0 版本的新功能、兼容性变更、改进提升，以及错误修复。
---

# TiDB 7.3.0 Release Notes

发版日期：2023 年 8 月 14 日

TiDB 版本：7.3.0

试用链接：[快速体验](https://docs.pingcap.com/zh/tidb/v7.3/quick-start-with-tidb)

v7.3.0 引入了以下主要功能。[功能详情](#功能详情)中列出的部分功能旨在增强 TiDB 和 TiFlash 的查询稳定性，不直接面向用户，因此未包含在下表中。

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
    <td>可扩展性与性能</td>
    <td>TiDB Lightning 支持 <a href="https://docs.pingcap.com/zh/tidb/v7.3/partitioned-raft-kv">Partitioned Raft KV</a>（实验特性）</td>
    <td>TiDB Lightning 的数据导入服务支持新的 Partitioned Raft KV 架构，为 Partitioned Raft KV 在 TiDB 后续版本中 GA 做好准备。
    </td>
  </tr>
  <tr>
    <td rowspan="2">稳定性与高可用</td>
    <td><a href="https://docs.pingcap.com/zh/tidb/v7.3/tidb-lightning-physical-import-mode-usage#冲突数据检测">TiDB Lightning 引入冲突数据的自动检测和处理机制</a></td>
    <td>TiDB Lightning 物理导入模式支持新版本的冲突检测机制，支持在遇到数据冲突时替换 (<code>replace</code>) 或忽略 (<code>ignore</code>) 冲突数据的语义。TiDB Lightning 会自动处理冲突数据，同时提高了冲突处理的性能。</td>
  </tr>
  <tr>
    <td><a href="https://docs.pingcap.com/zh/tidb/v7.3/tidb-resource-control#query-watch-语句说明">手动标记资源使用超出预期的查询</a>（实验特性）</td>
    <td>查询耗费的时间有时会超出预期。通过资源组新增的 Runaway Queries 监控列表，你可以设置降低 Runaway Queries 的优先级或终止查询，从而更有效地管理查询。该功能允许算子在资源组级别通过匹配 SQL 文本、SQL digest 或执行计划标记查询，并对这些查询进行处理，从而更好地控制非预期的大型查询可能对集群产生的影响。</td>
  </tr>
  <tr>
    <td>SQL</td>
    <td><a href="https://docs.pingcap.com/zh/tidb/v7.3/optimizer-hints">添加更多优化器提示，加强对算子的控制，提升查询稳定性</a></td>
    <td>新增优化器提示：<code>NO_INDEX_JOIN()</code>、<code>NO_MERGE_JOIN()</code>、<code>NO_INDEX_MERGE_JOIN()</code>、<code>NO_HASH_JOIN()</code>、<code>NO_INDEX_HASH_JOIN()</code></td>
  </tr>
  <tr>
    <td>数据库管理与可观测性</td>
    <td><a href="https://docs.pingcap.com/zh/tidb/v7.3/sql-statement-show-analyze-status">显示统计信息收集的进度</a></td>
    <td>支持使用 <code>SHOW ANALYZE STATUS</code> 语句或通过 <code>mysql.analyze_jobs</code> 系统表查看 <code>ANALYZE</code> 任务的进度。</td>
  </tr>
</tbody>
</table>

## 功能详情

### 性能

* TiFlash 支持副本选择策略 [#44106](https://github.com/pingcap/tidb/issues/44106) @[XuHuaiyu](https://github.com/XuHuaiyu)

    在 v7.3.0 之前，当 TiFlash 进行数据扫描和 MPP 计算时，会尽可能使用其所有节点的副本，以提供最强大的性能。从 v7.3.0 起，TiFlash 引入副本选择策略，该策略由系统变量 [`tiflash_replica_read`](/system-variables.md#tiflash_replica_read-从-v730-版本开始引入) 控制，可以根据节点的[区域属性](/schedule-replicas-by-topology-labels.md#设置-tidb-的-labels可选)选择特定的副本，调度部分节点进行数据扫描及 MPP 计算。

    当集群部署在多个机房且每个机房都拥有完整的 TiFlash 数据副本时，你可以设置该策略只选择使用当前机房的 TiFlash 副本，即只在当前机房的 TiFlash 节点中进行数据扫描和 MPP 计算，从而避免大量跨机房的网络数据传输。

    更多信息，请参考[用户文档](/system-variables.md#tiflash_replica_read-从-v730-版本开始引入)。

* TiFlash 支持节点内的 Runtime Filter [#40220](https://github.com/pingcap/tidb/issues/40220) @[elsa0520](https://github.com/elsa0520)

    Runtime Filter 是在查询规划阶段生成的一种**动态取值谓词**。在表连接的过程中，这些动态谓词能够有效过滤掉不满足连接条件的行，减少扫描时间和网络开销，提升表连接的效率。自 v7.3.0 起，TiFlash 支持节点内的 Runtime Filter，提升了数据分析类查询的整体性能，在部分 TPC-DS 数据集的查询中可达到 10% ~ 50% 的性能提升。

    该功能在 v7.3.0 默认关闭。要启用此功能，需将变量 [`tidb_runtime_filter_mode`](/system-variables.md#tidb_runtime_filter_mode-从-v720-版本开始引入) 设置为 `LOCAL`。

    更多信息，请参考[用户文档](/runtime-filter.md)。

* TiFlash 支持执行公共表表达式 (CTE)（实验特性）[#43333](https://github.com/pingcap/tidb/issues/43333) @[winoros](https://github.com/winoros)

    在 v7.3.0 版本之前，TiFlash 的 MPP 引擎默认无法执行包含 CTE 的查询，你需要通过系统变量 [`tidb_opt_force_inline_cte`](/system-variables.md#tidb_opt_force_inline_cte-从-v630-版本开始引入) 强制 inline CTE，达到让查询尽可能在 MPP 框架下执行的效果。在 v7.3.0 中，TiFlash MPP 引擎支持执行包含 CTE 的查询，无需强制 inline CTE 也可以尽可能地在 MPP 框架中执行查询。在 TPC-DS 基准测试中，与强制 inline 的执行方式相比，该功能可以将包含 CTE 的查询的总执行速度提升 20%。

    该功能为实验特性，默认关闭，由变量 [`tidb_opt_enable_mpp_shared_cte_execution`](/system-variables.md#tidb_opt_enable_mpp_shared_cte_execution-从-v720-版本开始引入) 控制。

### 稳定性

* 新增部分优化器提示 [#45520](https://github.com/pingcap/tidb/issues/45520) @[qw4990](https://github.com/qw4990)

    TiDB 在 v7.3.0 新增了几个优化器提示，用来控制表之间的连接方式，包括：

    - [`NO_MERGE_JOIN()`](/optimizer-hints.md#no_merge_joint1_name--tl_name-) 选择除 Merge Join 以外的连接方式。
    - [`NO_INDEX_JOIN()`](/optimizer-hints.md#no_index_joint1_name--tl_name-) 选择除 Index Nested Loop Join 以外的连接方式。
    - [`NO_INDEX_MERGE_JOIN()`](/optimizer-hints.md#no_index_merge_joint1_name--tl_name-) 选择除 Index Nested Loop Merge Join 以外的连接方式。
    - [`NO_HASH_JOIN()`](/optimizer-hints.md#no_hash_joint1_name--tl_name-) 选择哈希连接以外的连接方式。
    - [`NO_INDEX_HASH_JOIN()`](/optimizer-hints.md#no_index_hash_joint1_name--tl_name-) 选择除 [Index Nested Loop Hash Join](/optimizer-hints.md#inl_hash_join) 以外的连接方式。

  更多信息，请参考[用户文档](/optimizer-hints.md)。

* 手动标记资源使用超出预期的查询（实验特性）[#43691](https://github.com/pingcap/tidb/issues/43691) @[Connor1996](https://github.com/Connor1996) @[CabinfeverB](https://github.com/CabinfeverB)

    在 v7.2.0 中，TiDB 自动管理资源使用超出预期的查询 (Runaway Query)，即自动降级或取消运行时间超出预期的查询。在实际运行时，只依靠规则无法覆盖所有情况。因此，TiDB v7.3.0 新增手动标记查询的功能。利用新增的命令 [`QUERY WATCH`](/sql-statements/sql-statement-query-watch.md)，你可以根据 SQL 的文本、SQL Digest 或执行计划标记查询，命中的查询可以被降级或取消。

    手动标记 Runaway Query 的功能为数据库中突发的性能问题提供了有效的干预手段。针对由查询引发的性能问题，在定位根本原因之前，该功能可以快速缓解其对整体性能的影响，从而提升系统服务质量。

    更多信息，请参考[用户文档](/tidb-resource-control.md#query-watch-语句说明)。

### SQL 功能

* List 和 List COLUMNS 分区表支持默认分区 [#20679](https://github.com/pingcap/tidb/issues/20679) @[mjonss](https://github.com/mjonss) @[bb7133](https://github.com/bb7133)

    在 v7.3.0 以前，当使用 `INSERT` 语句向 List 或 List COLUMNS 分区表插入数据时，这些数据需要满足分区表指定的分区条件。如果要插入的数据不匹配任何分区条件，该语句将执行失败或忽略不符合分区条件的数据。

    在 v7.3.0 中，List 和 List COLUMNS 分区表支持默认分区功能。在创建默认分区后，如果要插入的数据不匹配任何分区条件，则数据将被写入默认分区。默认分区功能可以提升 List 分区和 List COLUMNS 分区的使用便捷性，避免不符合分区条件的数据导致 `INSERT` 语句执行失败或者数据被忽略。

    需要注意的是，该功能是 TiDB 对 MySQL 语法的扩展。创建默认分区后，该分区表的数据无法直接同步到 MySQL 中。

    更多信息，请参考[用户文档](/partitioned-table.md#list-分区)。

### 可观测性

* 显示统计信息收集的进度 [#44033](https://github.com/pingcap/tidb/issues/44033) @[hawkingrei](https://github.com/hawkingrei)

    收集大表的统计信息经常会持续较长时间。在之前的版本中，无法了解统计信息收集的进度，进而无法预测完成时间。TiDB v7.3.0 新增显示统计信息收集进度的功能。你可以通过系统表 `mysql.analyze_jobs` 或者 `SHOW ANALYZE STATUS` 查看各个子任务的总体工作量、当前进度以及预计的完成时间。在大规模数据导入、SQL 性能优化等场景下，该功能有助于了解整体任务进度，提升用户体验。

    更多信息，请参考[用户文档](/sql-statements/sql-statement-show-analyze-status.md)。

* Plan Replayer 支持导出历史统计信息 [#45038](https://github.com/pingcap/tidb/issues/45038) @[time-and-fate](https://github.com/time-and-fate)

    自 v7.3.0 起，通过新增的 [`dump with stats as of timestamp`](/sql-plan-replayer.md) 子句，你可以使用 Plan Replayer 导出指定 SQL 相关对象在指定时间点的统计信息。在执行计划问题的诊断过程中，通过对历史统计信息的准确抓取，能够更精确地分析出执行计划在问题发生的时间点是如何生成的，从而找到问题的根本原因，大大提升执行计划问题的诊断效率。

    更多信息，请参考[用户文档](/sql-plan-replayer.md)。

### 数据迁移

* TiDB Lightning 引入新版冲突数据检测和处理机制 [#41629](https://github.com/pingcap/tidb/issues/41629) @[lance6716](https://github.com/lance6716)

    在之前的版本中，TiDB Lightning 的逻辑导入模式和物理导入模式各自使用独立的冲突检测和处理方式，其配置较为复杂且不易理解。另外，在物理导入模式下，无法通过替换 (`replace`) 或忽略 (`ignore`) 策略处理冲突的数据。从 v7.3.0 开始，TiDB Lightning 引入新版冲突检测和处理机制，逻辑导入模式和物理导入模式都使用相同的冲突检测和处理方式，即可以选择在遇到冲突数据时报错 (`error`)、替换 (`replace`) 或忽略 (`ignore`)。同时还支持设置冲突记录的上限，例如在处理指定数量冲突记录后任务中断退出，也可以记录哪些数据发生了冲突，以便后续排查。

    当导入数据存在大量冲突时，推荐使用新版冲突检测和处理机制，以获得更好的性能。在实验环境下，相比旧版，新版机制最高可将冲突检测和处理的性能提升 3 倍。该性能数据仅供参考，实际性能会受到环境配置、表结构、冲突数据的占比等因素影响。注意新版和旧版冲突处理机制不能同时使用。未来将废弃旧版冲突检测和处理机制。

    更多信息，请参考[用户文档](/tidb-lightning/tidb-lightning-physical-import-mode-usage.md#冲突数据检测)。

* TiDB Lightning 支持 Partitioned Raft KV（实验特性）[#14916](https://github.com/tikv/tikv/issues/14916) @[GMHDBJD](https://github.com/GMHDBJD)

    TiDB Lightning 支持 Partitioned Raft KV，该功能可以提升 TiDB Lightning 导入数据的性能。

* TiDB Lightning 引入新的参数 `enable-diagnose-log` 用于打印更多的诊断日志，方便定位问题 [#45497](https://github.com/pingcap/tidb/issues/45497) @[D3Hunter](https://github.com/D3Hunter)

    默认情况下，该功能未启用，即只打印包含 `lightning/main` 的日志。开启该功能后，将打印所有包（包括 `client-go` 和 `tidb`）的日志，以帮助诊断与 `client-go` 和 `tidb` 相关的问题。

    更多信息，请参考[用户文档](/tidb-lightning/tidb-lightning-configuration.md#tidb-lightning-全局配置)。

## 兼容性变更

> **注意：**
>
> 以下为从 v7.2.0 升级至当前版本 (v7.3.0) 所需兼容性变更信息。如果从 v7.1.0 或之前版本升级到当前版本，可能也需要考虑和查看中间版本 release notes 中提到的兼容性变更信息。

### 行为变更

* TiDB

    - MPP 是 TiFlash 引擎提供的分布式计算框架，允许节点之间的数据交换并提供高性能、高吞吐的 SQL 算法。相对其他协议，MPP 协议更加成熟，能提供更好的任务和资源管理。从 v7.3.0 起，当 TiDB 向 TiFlash 下推计算任务时，优化器默认只生成使用 MPP 协议的执行计划。如果设置了 [`tidb_allow_mpp`](/system-variables.md#tidb_allow_mpp-从-v50-版本开始引入) 为 `OFF`，在升级 TiDB 后查询可能会报错，建议在升级前检查 `tidb_allow_mpp` 的值并将其设置为 `ON`。如果仍然需要优化器根据成本估算从 Cop、BatchCop 和 MPP 协议中选择一个用于生成执行计划，可以将 [`tidb_allow_tiflash_cop`](/system-variables.md#tidb_allow_tiflash_cop-从-v730-版本开始引入) 变量设置为 `ON`。

* Backup & Restore (BR)

    - 全量恢复前增加了空集群检查，默认不支持恢复到非空集群。如果强制恢复，可以使用 `--filter` 指定对应表名。

* TiDB Lightning

    - 废弃 `tikv-importer.on-duplicate`，由 [`conflict.strategy`](/tidb-lightning/tidb-lightning-configuration.md#tidb-lightning-任务配置) 替代。
    - TiDB Lightning 停止迁移任务之前能容忍的最大非严重 (non-fatal errors) 错误数的配置项 `max-error` 不再包含导入数据冲突记录的上限，由 [`conflict.threshold`](/tidb-lightning/tidb-lightning-configuration.md#tidb-lightning-任务配置) 控制可容忍的最大冲突的记录数。

* TiCDC

    - 当 Kafka sink 使用 Avro 协议时，如果开启了 `force-replicate` 参数，创建 changefeed 会报错。
    - 由于 `delete-only-output-handle-key-columns` 和 `force-replicate` 参数不兼容，同时开启两个参数时，创建 changefeed 会报错。
    - 当使用 Open Protocol 作为输出协议时，`UPDATE` 类型的事件将仅输出变更的列。

### 系统变量

| 变量名 | 修改类型 | 描述 |
|---|----|------|
| [`tidb_opt_enable_mpp_shared_cte_execution`](/system-variables.md#tidb_opt_enable_mpp_shared_cte_execution-从-v720-版本开始引入) | 修改 | 该变量从 v7.3.0 开始生效，用于控制非递归的公共表表达式 (CTE) 是否可以在 TiFlash MPP 执行。 |
| [`tidb_allow_tiflash_cop`](/system-variables.md#tidb_allow_tiflash_cop-从-v730-版本开始引入) | 新增 | 用于在 TiDB 给 TiFlash 下推计算任务时选择生成执行计划的协议。 |
| [`tidb_lock_unchanged_keys`](/system-variables.md#tidb_lock_unchanged_keys-从-v711-和-v730-版本开始引入) | 新增 | 用于控制部分场景下，对于事务中涉及但并未修改值的 key 是否进行上锁。 |
| [`tidb_opt_enable_non_eval_scalar_subquery`](/system-variables.md#tidb_opt_enable_non_eval_scalar_subquery-从-v730-版本开始引入) | 新增 | 这个变量用于控制 `EXPLAIN` 语句是否禁止提前执行可以在优化阶段展开的常量子查询。 |
| [`tidb_skip_missing_partition_stats`](/system-variables.md#tidb_skip_missing_partition_stats-从-v730-版本开始引入) | 新增 | 这个变量用于控制当分区统计信息缺失时生成 GlobalStats 的行为。 |
| [`tiflash_replica_read`](/system-variables.md#tiflash_replica_read-从-v730-版本开始引入) | 新增 | 这个变量用于设置当查询需要使用 TiFlash 引擎时，TiFlash 副本的选择策略。 |

### 配置文件参数

| 配置文件 | 配置项 | 修改类型 | 描述 |
| -------- | -------- | -------- | -------- |
| TiDB | [`enable-32bits-connection-id`](/tidb-configuration-file.md#enable-32bits-connection-id-从-v730-版本开始引入) | 新增 | 这个变量用于控制是否开启生成 32 位 connection ID 的功能。 |
| TiDB | [`in-mem-slow-query-recent-num`](/tidb-configuration-file.md#in-mem-slow-query-recent-num-从-v730-版本开始引入) | 新增 | 这个变量用于控制缓存在内存中的最近使用的 slow query 个数。 |
| TiDB | [`in-mem-slow-query-topn-num`](/tidb-configuration-file.md#in-mem-slow-query-topn-num-从-v730-版本开始引入) | 新增 | 这个变量用于控制缓存在内存中的最慢的 slow query 个数。 |
| TiKV | [`coprocessor.region-bucket-size`](/tikv-configuration-file.md#region-bucket-size-从-v610-版本开始引入) | 修改 | 为降低客户端超时的可能性，默认值从 `96MiB` 修改为 `50MiB`。 |
| TiKV | [`raft-engine.format-version`](/tikv-configuration-file.md#format-version-从-v630-版本开始引入) | 修改 | 当使用 Partitioned Raft KV (`storage.engine="partitioned-raft-kv"`) 时，会引入 Ribbon filter，因此将默认值从 `2` 修改为 `5`。 |
| TiKV | [`raftdb.max-total-wal-size`](/tikv-configuration-file.md#max-total-wal-size-1) | 修改 | 当使用 Partitioned Raft KV (`storage.engine="partitioned-raft-kv"`) 时，TiKV 会跳过写 WAL，因此默认值从 `"4GB"` 修改为 `1`，即禁用 WAL。 |
| TiKV | [<code>rocksdb.\[defaultcf\|writecf\|lockcf\].compaction-guard-min-output-file-size</code>](/tikv-configuration-file.md#compaction-guard-min-output-file-size) | 修改 | 为解决大数据写入情况下 compaction 速度跟不上写入速度的问题，默认值从 `"1MB"` 修改为 `"8MB"`。 |
| TiKV | [<code>rocksdb.\[defaultcf\|writecf\|lockcf\].format-version</code>](/tikv-configuration-file.md#format-version-从-v620-版本开始引入) | 修改 | 当使用 Partitioned Raft KV (`storage.engine="partitioned-raft-kv"`) 时，会引入 Ribbon filter，因此将默认值从 `2` 修改为 `5`。 |
| TiKV | [`rocksdb.lockcf.write-buffer-size`](/tikv-configuration-file.md#write-buffer-size) | 修改 | 当使用 Partitioned Raft KV (`storage.engine="partitioned-raft-kv"`) 时，为加快 lockcf 上 compaction 的速度，默认值从 `"32MB"` 修改为 `"4MB"`。 |
| TiKV | [`rocksdb.max-total-wal-size`](/tikv-configuration-file.md#max-total-wal-size) | 修改 | 当使用 Partitioned Raft KV (`storage.engine="partitioned-raft-kv"`) 时，TiKV 会跳过写 WAL，因此默认值从 `"4GB"` 修改为 `1`，即禁用 WAL。 |
| TiKV | [`rocksdb.stats-dump-period`](/tikv-configuration-file.md#stats-dump-period) | 修改 | 当使用 Partitioned Raft KV (`storage.engine="partitioned-raft-kv"`) 时，为关闭冗余日志的打印，默认值从 `"10m"` 修改为 `"0"`。|
| TiKV | [`rocksdb.write-buffer-limit`](/tikv-configuration-file.md#write-buffer-limit-从-v660-版本开始引入) | 修改 | 为减小 memtable 的内存开销，当 `storage.engine="raft-kv"` 时，默认值从本机内存的 25% 修改为 `0`，即不限制。当使用 Partitioned Raft KV (`storage.engine="partitioned-raft-kv"`) 时，默认值从本机内存的 25% 修改为本机内存的 20%。 |
| TiKV | [`storage.block-cache.capacity`](/tikv-configuration-file.md#capacity) | 修改 | 当使用 Partitioned Raft KV (`storage.engine="partitioned-raft-kv"`) 时，为弥补 memtable 的内存开销，将默认值从系统总内存大小的 45% 修改为系统总内存大小的 30%。 |
| TiFlash | [`storage.format_version`](/tiflash/tiflash-configuration.md) | 修改 | 引入新的 DTFile 储存文件格式 `format_version = 5`，该格式可以合并小文件从而减少物理文件数量。注意该格式目前为实验特性，默认未启用。 |
| TiDB Lightning | `tikv-importer.incremental-import` | 删除 | TiDB Lightning 并行导入参数。因为该参数名容易被误认为是增量导入的参数，因此更名为 `tikv-importer.parallel-import`。如果用户传入旧的参数名，会被自动转成新的参数名。|
|TiDB Lightning  | `tikv-importer.on-duplicate` | 废弃 | TiDB Lightning 逻辑导入模式插入冲突数据时执行的操作。从 v7.3.0 起，该参数由 [`conflict.strategy`](/tidb-lightning/tidb-lightning-configuration.md#tidb-lightning-任务配置) 取代。|
| TiDB Lightning  | [`conflict.max-record-rows`](/tidb-lightning/tidb-lightning-configuration.md) | 新增 | TiDB Lightning 新版冲突检测与处理策略，用于记录在数据导入过程中遇到的冲突记录，并允许设置最大上限，默认值为 `100`。 |
| TiDB Lightning  | [`conflict.strategy`](/tidb-lightning/tidb-lightning-configuration.md) | 新增 | TiDB Lightning 新版冲突检测与处理的策略，包含 `""`（不做冲突检测），`"error"`（遇到冲突数据即报错并停止导入），`"replace"`（遇到冲突记录替换已有的冲突记录），`"ignore"`（遇到冲突记录忽略需要插入的该条冲突记录）四种策略。默认值为 `""`，即不做冲突检测。 |
| TiDB Lightning  | [`conflict.threshold`](/tidb-lightning/tidb-lightning-configuration.md) | 新增 |TiDB Lightning 新版冲突检测与处理策略允许的冲突上限，`conflict.strategy="error"` 时默认值为 `0`，当 `conflict.strategy="replace"` 或 `conflict.strategy="ignore"` 时默认值为 maxint。 |
| TiDB Lightning  | [`enable-diagnose-logs`](/tidb-lightning/tidb-lightning-configuration.md) | 新增 | 是否开启诊断日志。默认为 `false`，即只输出和导入有关的日志，不会输出依赖的其他组件的日志。设置为 `true` 后，既输出和导入相关的日志，也输出依赖的其他组件的日志，并开启 GRPC debug，可用于问题诊断。 |
| TiDB Lightning | [`tikv-importer.parallel-import`](/tidb-lightning/tidb-lightning-configuration.md) | 新增 | TiDB Lightning 并行导入参数。用于替代原有的 `tikv-importer.incremental-import` 参数，因为原有参数会被误认为是增量导入的参数而误用。 |
| BR | `azblob.encryption-key` | 新增 |BR 为外部存储 Azure Blob Storage 提供加密密钥支持 |
| BR | `azblob.encryption-scope` | 新增 |BR 为外部存储 Azure Blob Storage 提供加密范围支持 |
| TiCDC | [`large-message-handle-option`](/ticdc/ticdc-sink-to-kafka.md#处理超过-kafka-topic-限制的消息) | 新增 | 默认为空，即消息大小超过 Kafka Topic 的限制后，同步任务失败。设置为 "handle-key-only" 时，如果消息超过大小，只发送 handle key 以减少消息的大小；如果依旧超过大小，则同步任务失败。 |
| TiCDC | [`sink.csv.binary-encoding-method`](/ticdc/ticdc-changefeed-config.md#ticdc-changefeed-配置文件说明) | 新增 | CSV 协议中二进制类型数据的编码方式，可选 `'base64'` 与 `'hex'`。默认值为 `'base64'`。 |

### 系统表

- 新增系统表 `mysql.tidb_timers` 用来存储系统内部定时器的元信息。

## 废弃功能

* TiDB

    - 统计信息的[快速分析](/system-variables.md#tidb_enable_fast_analyze)(实验特性)计划在 v7.5.0 中废弃。
    - 统计信息的[增量收集](https://docs.pingcap.com/zh/tidb/v7.3/statistics#增量收集)(实验特性)计划在 v7.5.0 中废弃。

## 改进提升

+ TiDB

    - 新增 [`tidb_opt_enable_non_eval_scalar_subquery`](/system-variables.md#tidb_opt_enable_non_eval_scalar_subquery-从-v730-版本开始引入) 系统变量用于控制 `EXPLAIN` 语句是否在优化阶段提前执行子查询 [#22076](https://github.com/pingcap/tidb/issues/22076) @[winoros](https://github.com/winoros)
    - 在启用 [Global Kill](/tidb-configuration-file.md#enable-global-kill-从-v610-版本开始引入) 的情况下，可以通过 <kbd>Control+C</kbd> 终止当前会话 [#8854](https://github.com/pingcap/tidb/issues/8854) @[pingyu](https://github.com/pingyu)
    - 支持锁函数 `IS_FREE_LOCK()` 和 `IS_USED_LOCK()` [#44493](https://github.com/pingcap/tidb/issues/44493) @[dveeden](https://github.com/dveeden)
    - 优化与落盘相关的 chunk 读取的性能 [#45125](https://github.com/pingcap/tidb/issues/45125) @[YangKeao](https://github.com/YangKeao)
    - 以 Optimizer Fix Controls 的方式改进了 Index Join 内表的高估问题 [#44855](https://github.com/pingcap/tidb/issues/44855) @[time-and-fate](https://github.com/time-and-fate)

+ TiKV

    - 添加 `Max gap of safe-ts` 和 `Min safe ts region` 监控项以及 `tikv-ctl get-region-read-progress` 命令，用于更好地观测和诊断 resolved-ts 和 safe-ts 的状态 [#15082](https://github.com/tikv/tikv/issues/15082) @[ekexium](https://github.com/ekexium)

+ PD

    - 未开启 Swagger server 时，PD 默认屏蔽 Swagger API [#6786](https://github.com/tikv/pd/issues/6786) @[bufferflies](https://github.com/bufferflies)
    - 提升 etcd 的高可用性 [#6554](https://github.com/tikv/pd/issues/6554) [#6442](https://github.com/tikv/pd/issues/6442) @[lhy1024](https://github.com/lhy1024)
    - 减少 `GetRegions` 请求的内存占用 [#6835](https://github.com/tikv/pd/issues/6835) @[lhy1024](https://github.com/lhy1024)

+ TiFlash

    - 支持新的 DTFile 格式版本 [`storage.format_version = 5`](/tiflash/tiflash-configuration.md)，可以合并小文件从而减少物理文件数量（实验特性） [#7595](https://github.com/pingcap/tiflash/issues/7595) @[hongyunyan](https://github.com/hongyunyan)

+ Tools

    + Backup & Restore (BR)

        - 使用 BR 备份数据到 Azure Blob Storage 时，支持使用加密范围或加密密钥对数据进行服务端加密 [#45025](https://github.com/pingcap/tidb/issues/45025) @[Leavrth](https://github.com/Leavrth)

    + TiCDC

        - 优化了 Open Protocol 输出的消息大小，在发送 `UPDATE` 类型事件时仅输出被更新的列值 [#9336](https://github.com/pingcap/tiflow/issues/9336) @[3AceShowHand](https://github.com/3AceShowHand)
        - Storage Sink 支持对 HEX 格式的数据进行十六进制编码输出，使其兼容 AWS DMS 的格式规范 [#9373](https://github.com/pingcap/tiflow/issues/9373) @[CharlesCheung96](https://github.com/CharlesCheung96)
        - Kafka Sink 支持在消息过大时[只发送 Handle Key 数据](/ticdc/ticdc-sink-to-kafka.md#处理超过-kafka-topic-限制的消息)，减少数据大小 [#9382](https://github.com/pingcap/tiflow/issues/9382) @[3AceShowHand](https://github.com/3AceShowHand)

## 错误修复

+ TiDB

    - 修复当使用 MySQL 的 Cursor Fetch 协议时，结果集占用的内存超过 `tidb_mem_quota_query` 的限制导致 TiDB OOM 的问题。修复后，TiDB 会自动将结果集写入磁盘以释放内存资源 [#43233](https://github.com/pingcap/tidb/issues/43233) @[YangKeao](https://github.com/YangKeao)
    - 修复数据争用导致 TiDB panic 的问题 [#45561](https://github.com/pingcap/tidb/issues/45561) @[genliqi](https://github.com/gengliqi)
    - 修复带 `indexMerge` 的查询被 kill 时可能会卡住的问题 [#45279](https://github.com/pingcap/tidb/issues/45279) @[xzhangxian1008](https://github.com/xzhangxian1008)
    - 修复当开启 `tidb_enable_parallel_apply` 时，MPP 模式下的查询结果出错的问题 [#45299](https://github.com/pingcap/tidb/issues/45299) @[windtalker](https://github.com/windtalker)
    - 修复 resolve lock 在 PD 时间跳变的情况下可能卡住的问题 [#44822](https://github.com/pingcap/tidb/issues/44822) @[zyguan](https://github.com/zyguan)
    - 修复 GC resolve lock 可能错过一些悲观锁的问题 [#45134](https://github.com/pingcap/tidb/issues/45134) @[MyonKeminta](https://github.com/MyonKeminta)
    - 修复动态裁剪模式下使用了排序的查询返回结果错误的问题 [#45007](https://github.com/pingcap/tidb/issues/45007) @[Defined2014](https://github.com/Defined2014)
    - 修复 `AUTO_INCREMENT` 与列的默认值 `DEFAULT` 可以指定在同一列上的问题 [#45136](https://github.com/pingcap/tidb/issues/45136) @[Defined2014](https://github.com/Defined2014)
    - 修复某些情况下查询系统表 `INFORMATION_SCHEMA.TIKV_REGION_STATUS` 返回结果错误的问题 [#45531](https://github.com/pingcap/tidb/issues/45531) @[Defined2014](https://github.com/Defined2014)
    - 修复某些情况下分区表分区裁剪不正确的问题 [#42273](https://github.com/pingcap/tidb/issues/42273) @[jiyfhust](https://github.com/jiyfhust)
    - 修复 `TRUNCATE` 分区表的某个分区时，全局索引无法清除的问题 [#42435](https://github.com/pingcap/tidb/issues/42435) @[L-maple](https://github.com/L-maple)
    - 修复在 TiDB 节点故障后其它 TiDB 节点没有接管 TTL 任务的问题 [#45022](https://github.com/pingcap/tidb/issues/45022) @[lcwangchao](https://github.com/lcwangchao)
    - 修复 TTL 运行过程中内存泄漏的问题 [#45510](https://github.com/pingcap/tidb/issues/45510) @[lcwangchao](https://github.com/lcwangchao)
    - 修复向分区表插入数据时某些报错信息不准确的问题 [#44966](https://github.com/pingcap/tidb/issues/44966) @[lilinghai](https://github.com/lilinghai)
    - 修复 `INFORMATION_SCHEMA.TIFLASH_REPLICA` 表的读取权限有误的问题 [#7795](https://github.com/pingcap/tiflash/issues/7795) @[Lloyd-Pottiger](https://github.com/Lloyd-Pottiger)
    - 修复使用错误分区表名时报错的问题 [#44967](https://github.com/pingcap/tidb/issues/44967) @[River2000i](https://github.com/River2000i)
    - 修复某些情况下启用 `tidb_enable_dist_task` 时，创建索引卡住的问题 [#44440](https://github.com/pingcap/tidb/issues/44440) @[tangenta](https://github.com/tangenta)
    - 修复通过 BR 恢复 `AUTO_ID_CACHE=1` 的表时，会遇到 `duplicate entry` 报错的问题 [#44716](https://github.com/pingcap/tidb/issues/44716) @[tiancaiamao](https://github.com/tiancaiamao)
    - 修复执行 `TRUNCATE TABLE` 消耗的时间和 `ADMIN SHOW DDL JOBS` 显示的任务执行时间不一致的问题 [#44785](https://github.com/pingcap/tidb/issues/44785) @[tangenta](https://github.com/tangenta)
    - 修复读取元数据时间超过一个 DDL lease 导致升级 TiDB 卡住的问题 [#45176](https://github.com/pingcap/tidb/issues/45176) @[zimulala](https://github.com/zimulala)
    - 修复 `SELECT CAST(n AS CHAR)` 语句中的 `n` 为负数时，查询结果出错的问题 [#44786](https://github.com/pingcap/tidb/issues/44786) @[xhebox](https://github.com/xhebox)
    - 修复开启 `tidb_opt_agg_push_down` 时查询可能返回错误结果的问题 [#44795](https://github.com/pingcap/tidb/issues/44795) @[AilinKid](https://github.com/AilinKid)
    - 修复带有 `current_date()` 的查询使用 Plan Cache 导致结果错误的问题 [#45086](https://github.com/pingcap/tidb/issues/45086) @[qw4990](https://github.com/qw4990)

+ TiKV

    - 修复在一些罕见的情况下，在 GC 的同时读取数据可能导致 TiKV panic 的问题 [#15109](https://github.com/tikv/tikv/issues/15109) @[MyonKeminta](https://github.com/MyonKeminta)

+ PD

    - 修复重启 PD 可能导致 `default` 资源组被重新初始化的问题 [#6787](https://github.com/tikv/pd/issues/6787) @[glorv](https://github.com/glorv)
    - 修复当 etcd 已经启动，但 client 尚未连接上 etcd 时，调用 client 会导致 PD panic 的问题 [#6860](https://github.com/tikv/pd/issues/6860) @[HuSharp](https://github.com/HuSharp)
    - 修复 Region 的 `health-check` 输出可能与通过 ID 所查到的 Region 信息不一致的问题 [#6560](https://github.com/tikv/pd/issues/6560) @[JmPotato](https://github.com/JmPotato)
    - 修复 `unsafe recovery` 中失败的 learner peer 在 `auto-detect` 模式中被忽略的问题 [#6690](https://github.com/tikv/pd/issues/6690) @[v01dstar](https://github.com/v01dstar)
    - 修复 Placement Rules 选择了不满足规则的 TiFlash learner 的问题 [#6662](https://github.com/tikv/pd/issues/6662) @[rleungx](https://github.com/rleungx)
    - 修复在 rule checker 选定 peer 时，unhealthy peer 无法被移除的问题 [#6559](https://github.com/tikv/pd/issues/6559) @[nolouch](https://github.com/nolouch)

+ TiFlash

    - 修复由于死锁导致 TiFlash 无法成功同步分区表的问题 [#7758](https://github.com/pingcap/tiflash/issues/7758) @[hongyunyan](https://github.com/hongyunyan)
    - 修复系统表 `INFORMATION_SCHEMA.TIFLASH_REPLICA` 包含用户没有访问权限的表的问题 [#7795](https://github.com/pingcap/tiflash/issues/7795) @[Lloyd-Pottiger](https://github.com/Lloyd-Pottiger)
    - 修复当同一个 MPP Task 内有多个 HashAgg 算子时，可能导致 MPP Task 编译时间过长而严重影响查询性能的问题 [#7810](https://github.com/pingcap/tiflash/issues/7810) @[SeaRise](https://github.com/SeaRise)

+ Tools

    + TiCDC

        - 修复由于 PD 短暂不可用而导致同步任务报错的问题 [#9294](https://github.com/pingcap/tiflow/issues/9294) @[asddongmen](https://github.com/asddongmen)
        - 修复 TiCDC 部分节点发生网络隔离时可能引发的数据不一致问题 [#9344](https://github.com/pingcap/tiflow/issues/9344) @[CharlesCheung96](https://github.com/CharlesCheung96)
        - 修复当 Kafka Sink 遇到错误时可能会无限阻塞同步任务推进的问题 [#9309](https://github.com/pingcap/tiflow/issues/9309) @[hicqu](https://github.com/hicqu)
        - 修复在 TiCDC 节点状态发生改变时可能引发的 panic 问题 [#9354](https://github.com/pingcap/tiflow/issues/9354) @[sdojjy](https://github.com/sdojjy)
        - 修复对默认 `ENUM` 值编码错误的问题 [#9259](https://github.com/pingcap/tiflow/issues/9259) @[3AceShowHand](https://github.com/3AceShowHand)

    + TiDB Lightning

        - 修复 TiDB Lightning 导入完成后执行 checksum 可能遇到 SSL 错误的问题 [#45462](https://github.com/pingcap/tidb/issues/45462) @[D3Hunter](https://github.com/D3Hunter)
        - 修复逻辑导入模式下，导入期间下游删除表可能导致 TiDB Lightning 元信息未及时更新的问题 [#44614](https://github.com/pingcap/tidb/issues/44614) @[dsdashun](https://github.com/dsdashun)

## 贡献者

感谢来自 TiDB 社区的贡献者们：

- [charleszheng44](https://github.com/charleszheng44)
- [dhysum](https://github.com/dhysum)
- [haiyux](https://github.com/haiyux)
- [Jiang-Hua](https://github.com/Jiang-Hua)
- [Jille](https://github.com/Jille)
- [jiyfhust](https://github.com/jiyfhust)
- [krishnaduttPanchagnula](https://github.com/krishnaduttPanchagnula)
- [L-maple](https://github.com/L-maple)
- [pingandb](https://github.com/pingandb)
- [testwill](https://github.com/testwill)
- [tisonkun](https://github.com/tisonkun)
- [xuyifangreeneyes](https://github.com/xuyifangreeneyes)
- [yumchina](https://github.com/yumchina)
