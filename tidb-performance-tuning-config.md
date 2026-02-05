---
title: 配置 TiDB 以优化性能
summary: 了解如何通过配置关键参数和应对边缘场景来优化 TiDB 性能。
---

# 配置 TiDB 以优化性能

本文档介绍如何优化 TiDB 的性能，包括：

- 常见负载的最佳实践。
- 针对复杂性能场景的优化策略。

> **注意：**
>
> 本文介绍的优化技术有助于提升 TiDB 的性能，但性能调优通常需要在多个因素之间权衡，并不存在一劳永逸的方案解决所有的性能问题。部分优化方法涉及实验特性，已在文中标注。虽然这些优化可以显著提升性能，但可能并不适合生产环境，实施前请充分评估。

## 概述

要实现 TiDB 的最佳性能，需要对多项配置进行细致调优。很多情况下，达到最佳性能需要调大默认值的配置。

默认的配置优先考虑的是稳定性而不是性能。若要最大化性能，可能需要配置更激进的参数，甚至启用实验特性。本文推荐的配置基于生产环境经验和对性能优化的研究。

本文档详细说明了非默认配置项，包括其优势和潜在权衡。请根据实际业务需求合理调整。

## 常见负载的关键配置

以下配置项常用于优化 TiDB 性能：

- 增强执行计划缓存，如 [SQL 预处理执行计划缓存](/sql-prepared-plan-cache.md)、[非预处理计划缓存](/sql-non-prepared-plan-cache.md)和[实例级执行计划缓存](/system-variables.md#tidb_enable_instance_plan_cache-从-v840-版本开始引入)。
- 通过 [Optimizer Fix Controls](/optimizer-fix-controls.md) 优化 TiDB 优化器行为。
- 更积极地使用 [Titan](/storage-engine/titan-overview.md) 存储引擎。
- 微调 TiKV 的压缩与流控配置，确保写入密集型负载下的性能与稳定性。

这些配置可显著提升多种负载的性能。但和所有的优化措施一样，请务必在生产环境部署前进行充分测试。

### 系统变量

执行以下 SQL 命令应用推荐配置：

```sql
SET GLOBAL tidb_enable_instance_plan_cache=on;
SET GLOBAL tidb_instance_plan_cache_max_size=2GiB;
SET GLOBAL tidb_enable_non_prepared_plan_cache=on;
SET GLOBAL tidb_ignore_prepared_cache_close_stmt=on;
SET GLOBAL tidb_analyze_column_options='ALL';
SET GLOBAL tidb_stats_load_sync_wait=2000;
SET GLOBAL tidb_opt_limit_push_down_threshold=10000;
SET GLOBAL tidb_opt_derive_topn=on;
SET GLOBAL tidb_runtime_filter_mode=LOCAL;
SET GLOBAL tidb_opt_enable_mpp_shared_cte_execution=on;
SET GLOBAL tidb_rc_read_check_ts=on;
SET GLOBAL tidb_guarantee_linearizability=off;
SET GLOBAL pd_enable_follower_handle_region=on;
SET GLOBAL tidb_opt_fix_control = '44262:ON,44389:ON,44823:10000,44830:ON,44855:ON,52869:ON';
```

下表简要说明了主要系统变量的作用及注意事项：

| 系统变量 | 说明 | 注意事项 |
| ---------| ---- | ----|
| [`tidb_enable_instance_plan_cache`](/system-variables.md#tidb_enable_instance_plan_cache-从-v840-版本开始引入) 和 [`tidb_instance_plan_cache_max_size`](/system-variables.md#tidb_instance_plan_cache_max_size-从-v840-版本开始引入) | 启用实例级计划缓存而不是会话级缓存，在高并发连接或频繁使用预处理语句的场景中，可以显著提升负载的性能。 | 实验特性，建议先在测试环境验证，并关注内存占用。 |
| [`tidb_enable_non_prepared_plan_cache`](/system-variables.md#tidb_enable_non_prepared_plan_cache) | 启用[非 Prepare 语句执行计划缓存](/sql-non-prepared-plan-cache.md)，降低不使用预处理语句应用的编译开销。 | 无 |
| [`tidb_ignore_prepared_cache_close_stmt`](/system-variables.md#tidb_ignore_prepared_cache_close_stmt-从-v600-版本开始引入) | 针对使用预处理语句但在每次执行后关闭执行计划的应用，为该应用混存执行计划。 | 无 |
| [`tidb_analyze_column_options`](/system-variables.md#tidb_analyze_column_options-从-v830-版本开始引入) | 收集所有列的统计信息，避免因缺失统计导致执行计划不佳。 | 无 |
| [`tidb_stats_load_sync_wait`](/system-variables.md#tidb_stats_load_sync_wait-从-v540-版本开始引入) | 将同步加载统计信息的超时时间从默认 100ms 提高到 2s，确保编译前加载完毕。 | 调大该变量的值会导致编译等待时间变长。 |
| [`tidb_opt_limit_push_down_threshold`](/system-variables.md#tidb_opt_limit_push_down_threshold) | 提高将 `Limit` 或 `TopN` 下推到 TiKV 的阈值。 | 当存在多个索引选项时，调大该变量的值后，优化器更倾向于选择能优化 `ORDER BY` 和 `Limit` 算子的索引。 |
| [`tidb_opt_derive_topn`](/system-variables.md#tidb_opt_derive_topn-从-v700-版本开始引入) | 启用[从窗口函数中推导 `TopN` 或 `Limit`](/derive-topn-from-window.md)。 | 仅支持 `ROW_NUMBER()` 窗口函数。 |
| [`tidb_runtime_filter_mode`](/system-variables.md#tidb_runtime_filter_mode-从-v720-版本开始引入) | 启用本地模式的 [Runtime Filter](/runtime-filter.md#runtime-filter-mode)，提升 Hash Join 效率。 | v7.2.0 引入，出于安全考虑默认关闭。 |
| [`tidb_opt_enable_mpp_shared_cte_execution`](/system-variables.md#tidb_opt_enable_mpp_shared_cte_execution-从-v720-版本开始引入) | 启用非递归公共表表达式 [Common Table Expressions (CTE)](/sql-statements/sql-statement-with.md) 下推到 TiFlash。 | 实验特性。 |
| [`tidb_rc_read_check_ts`](/system-variables.md#tidb_rc_read_check_ts-从-v600-版本开始引入) | 对于 read-committed 隔离级别，启用该变量可以避免获取全局时间戳带来的延迟和开销，从而优化事务级读取延迟。 | 该特性与可重复读 (Repeatable Read) 隔离级别不兼容。 |
| [`tidb_guarantee_linearizability`](/system-variables.md#tidb_guarantee_linearizability-从-v50-版本开始引入) | 通过跳过从 PD 获取提交时间戳，提升性能。 | 为了提升性能，这种方式牺牲了线性一致性 (Linearizability)，仅保证因果一致性。不适用于需要严格线性一致性的场景。|
| [`pd_enable_follower_handle_region`](/system-variables.md#pd_enable_follower_handle_region-从-v760-版本开始引入) | 启用 PD Follower 特性，允许 PD Follower 节点处理 Region 请求。该特性有助于将负载均匀分摊到所有 PD 节点，降低 PD Leader 的 CPU 压力。 | N/A |
| [`tidb_opt_fix_control`](/system-variables.md#tidb_opt_fix_control-从-v653-和-v710-版本开始引入) | 启用高级查询优化策略，通过引入额外的优化规则和启发式方法来提升性能。 | 不同负载的性能提升效果不同，因此请进行充分测试。 |

以下为优化器控制配置项的详细说明，这些配置项可启用额外的优化能力：

- [`44262:ON`](/optimizer-fix-controls.md#44262-从-v653-和-v720-版本开始引入)：当分区表缺少[全局统计信息](/statistics.md#收集动态裁剪模式下的分区表统计信息)时，使用[动态裁剪模式](/partitioned-table.md#动态裁剪模式)访问分区表。
- [`44389:ON`](/optimizer-fix-controls.md#44389-从-v653-和-v720-版本开始引入)：对于如 `c = 10 and (a = 'xx' or (a = 'kk' and b = 1))` 这样的过滤条件，为 `IndexRangeScan` 构建更全面的扫描范围。
- [`44823:10000`](/optimizer-fix-controls.md#44823-从-v730-版本开始引入)：为节省内存，计划缓存不会缓存参数数量超过该变量值的查询。将参数上限从默认的 `200` 提高到 `10000`，使带有超长 `in-list` 的查询也能命中计划缓存。
- [`44830:ON`](/optimizer-fix-controls.md#44830-从-v657-和-v730-版本开始引入)：允许计划缓存缓存物理优化阶段生成的包含 `PointGet` 算子的执行计划。
- [`44855:ON`](/optimizer-fix-controls.md#44855-从-v654-和-v730-版本开始引入)：当 `IndexJoin` 的 `Probe` 端包含 `Selection` 算子时，优化器可选择 `IndexJoin` 算子。
- [`52869:ON`](/optimizer-fix-controls.md#52869-从-v810-版本开始引入)：当优化器能为查询选择单一索引扫描（非全表扫描）时，自动选择索引合并（Index Merge）方式。

### TiKV 配置

在 TiKV 配置文件中添加如下配置项：

```toml
[server]
concurrent-send-snap-limit = 64
concurrent-recv-snap-limit = 64
snap-io-max-bytes-per-sec = "400MiB"

[pessimistic-txn]
in-memory-peer-size-limit = "32MiB"
in-memory-instance-size-limit = "512MiB"

[rocksdb]
max-manifest-file-size = "256MiB"
[rocksdb.titan]
enabled = true
[rocksdb.defaultcf.titan]
min-blob-size = "1KB"
blob-file-compression = "zstd"

[storage]
scheduler-pending-write-threshold = "512MiB"
[storage.flow-control]
l0-files-threshold = 50
soft-pending-compaction-bytes-limit = "512GiB"

[rocksdb.writecf]
level0-slowdown-writes-trigger = 20
soft-pending-compaction-bytes-limit = "192GiB"
[rocksdb.defaultcf]
level0-slowdown-writes-trigger = 20
soft-pending-compaction-bytes-limit = "192GiB"
[rocksdb.lockcf]
level0-slowdown-writes-trigger = 20
soft-pending-compaction-bytes-limit = "192GiB"
```

下表简要说明主要配置项及注意事项：

| 配置项 | 说明 | 注意事项 |
| ---------| ---- | ----|
| <ul><li>[`concurrent-send-snap-limit`](/tikv-configuration-file.md#concurrent-send-snap-limit)</li><li>[`concurrent-recv-snap-limit`](/tikv-configuration-file.md#concurrent-recv-snap-limit)</li><li>[`snap-io-max-bytes-per-sec`](/tikv-configuration-file.md#snap-io-max-bytes-per-sec)</li></ul> | 在 TiKV 扩缩容过程中，为并发快照传输和 I/O 带宽设置限制。提高这些限制可以加快数据迁移，从而缩短扩缩容时间。 | 需权衡扩容速度与在线业务性能。 |
| <ul><li>[`in-memory-peer-size-limit`](/tikv-configuration-file.md#in-memory-peer-size-limit-从-v840-版本开始引入)</li><li>[`in-memory-instance-size-limit`](/tikv-configuration-file.md#in-memory-instance-size-limit-从-v840-版本开始引入)</li></ul> | 控制悲观锁缓存的 Region 级和实例级的内存分配，将锁存储在内存中可减少磁盘 I/O 并提升事务性能。 | 提高上限会提升性能，但也会增加内存消耗。 |
| [`rocksdb.max-manifest-file-size`](/tikv-configuration-file.md#max-manifest-file-size) | 设置 RocksDB Manifest 文件的最大大小。Manifest 文件记录 SST 文件和数据库状态变更的元数据。增大该值可减少 Manifest 文件的写频率，从而降低其对前台写入性能的影响。 | 默认值为 `128MiB`。在存在大量 SST 文件（如数十万级别）的环境下，Manifest 文件频繁的写操作会影响写入性能。建议将该参数调高至 `256MiB` 或更大，以保持最佳性能。 |
| <ul><li>[`rocksdb.titan`](/tikv-configuration-file.md#rocksdbtitan)</li><li>[`rocksdb.defaultcf.titan`](/tikv-configuration-file.md#rocksdbdefaultcftitan)</li><li>[`min-blob-size`](/tikv-configuration-file.md#min-blob-size) </li><li> [`blob-file-compression`](/tikv-configuration-file.md#blob-file-compression)</li></ul> | 启用 Titan 存储引擎以降低写放大并缓解磁盘 I/O 瓶颈。尤其适用于 RocksDB 压缩无法跟上写入压力、待压缩字节持续积压的场景。 | 仅当写放大成为主要瓶颈时建议开启。需权衡以下因素：<ul><li>主键范围扫描可能受影响。</li><li>空间放大会增加（极端情况下最高 2 倍）。</li><li>Blob 缓存会占用更多内存。</li></ul> |
| [`storage.scheduler-pending-write-threshold`](/tikv-configuration-file.md#scheduler-pending-write-threshold) | 设置 TiKV 调度器写入队列的最大大小。当待写入任务的总大小超过该阈值时，TiKV 会拒绝新的写入请求并返回 `Server Is Busy` 错误。 | 默认值为 `100MiB`。在高并发写入或短时写入突发场景下，适当提高该阈值（如 `512MiB`）有助于缓解压力。但若写入队列持续积压并反复超限，可能说明存在底层性能瓶颈，需进一步排查。 |
| [`storage.flow-control.l0-files-threshold`](/tikv-configuration-file.md#l0-files-threshold) | 根据 kvDB L0 文件数量控制写入流控的触发时机。提高该阈值可在高写入负载下减少写入阻塞。 | 阈值过高时，若 L0 文件数量较多，可能导致更激进的压缩操作。 |
| [`storage.flow-control.soft-pending-compaction-bytes-limit`](/tikv-configuration-file.md#soft-pending-compaction-bytes-limit) | 控制待压缩字节数的阈值，用于管理写入流控。超过阈值后会部分拒绝写入请求。 | 默认软阈值为 `192GiB`。在写入密集型场景下，如果压缩进程跟不上，待压缩字节会持续积压，可能触发流控。适当调高该阈值可增加缓冲空间，但若持续积压，说明底层存在性能瓶颈，需进一步排查。 |
| <ul><li>[`rocksdb.(defaultcf\|writecf\|lockcf).level0-slowdown-writes-trigger`](/tikv-configuration-file.md#level0-slowdown-writes-trigger)</li><li>[`rocksdb.(defaultcf\|writecf\|lockcf).soft-pending-compaction-bytes-limit`](/tikv-configuration-file.md#level0-slowdown-writes-trigger) </li></ul>| 需要手动将 `level0-slowdown-writes-trigger` 和 `soft-pending-compaction-bytes-limit` 设置回默认值，以避免受流控参数影响。同时，建议将 RocksDB 相关参数设置为默认值，以保持压缩效率。 | 详情参见 [Issue 18708](https://github.com/tikv/tikv/issues/18708)。 |

请注意，上述表格中的压缩与流控参数调整，主要适用于以下规格的 TiKV 部署实例：

- CPU：32 核
- 内存：128 GiB
- 存储：5 TiB EBS
- 磁盘吞吐：1 GiB/s

#### 写入密集型负载推荐调整

为优化 TiKV 在写入密集型负载下的性能与稳定性，建议根据实例的硬件规格，调整部分压缩与流控参数。例如：

- [`rocksdb.rate-bytes-per-sec`](/tikv-configuration-file.md#rate-bytes-per-sec)：通常建议保持默认值。如果发现压缩 I/O 占用了大量磁盘带宽，可将该速率限制为磁盘最大吞吐量的约 60%，以平衡压缩与前台写入，避免磁盘饱和。例如，若磁盘吞吐为 **1 GiB/s**，可设置为约 `600MiB`。

- [`storage.flow-control.soft-pending-compaction-bytes-limit`](/tikv-configuration-file.md#soft-pending-compaction-bytes-limit-1) 和 [`storage.flow-control.hard-pending-compaction-bytes-limit`](/tikv-configuration-file.md#hard-pending-compaction-bytes-limit-1)：可根据磁盘空间适当提高这两个阈值（如分别设置为 1 TiB 和 2 TiB），为压缩进程提供更大的缓冲空间。

这些设置有助于提升资源利用率，并在高峰写入期间减少潜在瓶颈。

> **注意：**
>
> TiKV 在调度器层实现流控以确保系统稳定性。当超过关键阈值（包括待压缩字节数或写入队列大小等）时，TiKV 会开始拒绝写入请求并返回 ServerIsBusy 错误。该错误表示后台压缩进程无法跟上当前前台写入操作的速率。流控被触发后，通常会导致延迟升高并降低查询吞吐量（QPS 下降）。为避免这些性能劣化，需要进行充分的容量规划，并合理配置压缩参数和存储相关设置。

### TiFlash-learner 配置

在 TiFlash-learner 配置文件中添加如下内容：

```toml
[server]
snap-io-max-bytes-per-sec = "300MiB"
```

| 配置项 | 说明 | 注意事项 |
| ---------| ---- | ----|
| [`snap-io-max-bytes-per-sec`](/tikv-configuration-file.md#snap-io-max-bytes-per-sec) | 控制从 TiKV 到 TiFlash 的数据复制时允许使用的最大磁盘带宽。提高该值可以加快初始数据加载和追赶同步的速度。 | 带宽占用增加可能影响在线业务性能，请在同步速度与系统稳定性之间进行合理权衡。 |

## Benchmark 

本节对比了默认配置（基线）与基于前文[常见负载的关键配置](#常见负载的关键配置)优化后的性能表现。

### 在 1000 张表上运行的 Sysbench 负载

#### 测试环境

测试环境如下：

- 3 台 TiDB 服务器（16 核 CPU，64 GiB 内存）
- 3 台 TiKV 服务器（16 核 CPU，64 GiB 内存）
- TiDB 版本：v8.4.0
- 测试负载：[sysbench oltp_read_only](https://github.com/akopytov/sysbench/blob/master/src/lua/oltp_read_only.lua)

#### 性能对比

下表对比了基线配置与优化配置下的吞吐量、延迟和执行计划缓存命中率。

| 指标 | 基线配置 | 优化配置 | 提升幅度 |
| ---------| ---- | ----| ----|
| QPS | 89,100 | 100,128 | +12.38% |
| 平均延迟（毫秒）| 35.87 | 31.92 | -11.01% |
| P95 延迟（毫秒）| 58.92 | 51.02 | -13.41% |
| 执行计划缓存命中率 (%) | 56.89% | 87.51% | +53.82% |
| 计划缓存内存占用 (MiB) | 95.3 | 70.2 | -26.34% |

#### 主要优势

相比基线配置，实例级执行计划缓存 (Instance Plan Cache) 带来了显著的性能提升：

- 更高的命中率：提升 53.82%（从 56.89% 增加到 87.51%）。
- 更低的内存占用：降低 26.34%（从 95.3 MiB 降至 70.2 MiB）。
- 更优的性能表现：

    - QPS 提升 12.38%。
    - 平均延迟降低 11.01%。
    - P95 延迟降低 13.41%。

#### 工作原理

实例级执行计划缓存通过以下机制提升性能：

- 将 `SELECT` 语句的执行计划缓存在内存中。
- 在同一 TiDB 实例的所有连接（最多 200 个）之间共享缓存的执行计划。
- 可高效存储多达 1000 张表、5000 条 `SELECT` 语句的执行计划。
- 仅 `BEGIN` 和 `COMMIT` 语句会出现缓存未命中的情况。

#### 实际应用收益

虽然基于简单 sysbench `oltp_read_only` 查询（每个执行计划约 14 KB）的基准测试仅显示了有限的提升，但在真实业务场景下，实例级执行计划缓存的收益会更显著：

- 复杂查询的执行速度可提升至原来的 20 倍。
- 相比会话级计划缓存，内存利用率更高。

实例级执行计划缓存特别适用于以下场景：

- 有大量列的大表。
- 复杂的 SQL 查询。
- 高并发连接。
- 多样化的查询模式。

#### 内存效率

实例级执行计划缓存 (Instance Plan Cache) 相比会话级计划缓存 (Session Plan Cache) 具有更高的内存利用率，原因如下：

- 执行计划在所有连接间共享
- 无需为每个会话重复存储执行计划
- 更高的内存利用率和更高的命中率

在多连接和复杂查询场景下，若使用会话级计划缓存，为达到类似命中率需消耗更多内存，因此实例级计划缓存更高效。

![Instance plan cache: Queries Using Plan Cache OPS](/media/performance/instance-plan-cache.png)

#### 测试负载

执行以下 `sysbench oltp_read_only prepare` 命令加载数据：

```bash
sysbench oltp_read_only prepare --mysql-host={host} --mysql-port={port} --mysql-user=root --db-driver=mysql --mysql-db=test --threads=100 --time=900 --report-interval=10 --tables=1000 --table-size=10000
```

执行以下 `sysbench oltp_read_only run` 命令运行测试负载：

```bash
sysbench oltp_read_only run --mysql-host={host} --mysql-port={port} --mysql-user=root --db-driver=mysql --mysql-db=test --threads=200 --time=900 --report-interval=10 --tables=1000 --table-size=10000
```

更多信息，请参阅[如何用 Sysbench 测试 TiDB](/benchmark/benchmark-tidb-using-sysbench.md)。

### 大记录值下的 YCSB 测试负载

#### 测试环境

测试环境如下：

- 3 台 TiDB 服务器（16 核 CPU，64 GiB 内存）
- 3 台 TiKV 服务器（16 核 CPU，64 GiB 内存）
- TiDB 版本：v8.4.0
- 测试负载：[go-ycsb workloada](https://github.com/pingcap/go-ycsb/blob/master/workloads/workloada)

#### 性能对比

下表对比了基线配置与优化配置下的吞吐量（每秒操作数，OPS）。

| 指标 | 基线配置 (OPS) | 优化配置 (OPS) | 提升幅度 |
| ---------| ---- | ----| ----|
| Load data | 2858.5 | 5074.3  | +77.59%  |
| Workloada | 2243.0 | 12804.3 | +470.86% |

#### 性能分析

从 v7.6.0 开始，Titan 默认启用。TiDB v8.4.0 中，Titan 的 `min-blob-size` 默认值为 `32KiB`。基线配置采用 `31KiB` 的记录大小，确保数据存储在 RocksDB 中。而在关键配置中，将 `min-blob-size` 设置为 `1KiB`，使数据存储在 Titan。

关键配置下的性能提升，主要归因于 Titan 显著减少了 RocksDB 的压缩操作。如下图所示：

- 基线配置：RocksDB 压缩总吞吐量超过 1 GiB/s，峰值超过 3 GiB/s。
- 关键配置：RocksDB 压缩峰值吞吐量低于 100 MiB/s。

压缩开销的大幅降低有助于整体吞吐量的提升，这一提升体现在关键参数配置的优化效果中。

![Titan RocksDB compaction:](/media/performance/titan-rocksdb-compactions.png)

#### 测试负载

执行以下 `go-ycsb load` 命令加载数据：

```bash
go-ycsb load mysql -P /ycsb/workloads/workloada -p {host} -p mysql.port={port} -p threadcount=100 -p recordcount=5000000 -p operationcount=5000000 -p workload=core -p requestdistribution=uniform -pfieldcount=31 -p fieldlength=1024
```

执行以下 `go-ycsb run` 命令运行测试负载：

```bash
go-ycsb run mysql -P /ycsb/workloads/workloada -p {host} -p mysql.port={port} -p mysql.db=test -p threadcount=100 -p recordcount=5000000 -p operationcount=5000000 -p workload=core -prequestdistribution=uniform -p fieldcount=31 -p fieldlength=1024
```

## 边缘场景与专项优化

本节介绍如何针对特定场景进行专项优化，超越基础参数调优，帮助你根据实际业务需求对 TiDB 进行更有针对性的配置和调整。

### 识别边缘场景

执行以下步骤识别边缘场景：

1. 分析查询模式和负载特征。
2. 监控系统指标，定位性能瓶颈。
3. 收集应用团队关于具体问题的反馈。

### 常见边缘场景

以下列举了一些常见的边缘场景：

- 高频小查询导致 TSO 等待时间过高
- 针对不同负载选择合适的最大 chunk 大小
- 针对读密集型负载调优 coprocessor cache
- 根据负载特性优化 chunk 大小
- 针对不同负载优化事务模式和 DML 类型
- 通过 TiKV 下推优化 `GROUP BY` 和 `DISTINCT` 操作
- 使用内存引擎缓解 MVCC 版本积压
- 批量操作期间优化统计信息收集
- 针对不同实例类型优化线程池设置

后续小节将分别介绍如何应对这些场景。针对每种情况，你需要调整不同参数或使用 TiDB 的特定功能。

> **注意：**
>
> 请谨慎应用这些优化措施，并在生产环境部署前充分测试，因为其效果会因业务场景和数据特性而异。

### 高频小查询导致 TSO 等待时间过高

#### 问题排查

如果你的业务负载包含大量高频小事务或频繁请求时间戳的查询，[TSO (Timestamp Oracle）](/glossary.md#timestamp-oracle-tso) 可能成为性能瓶颈。你可以通过 [**Performance Overview > SQL Execute Time Overview**](/grafana-performance-overview-dashboard.md#sql-execute-time-overview) 面板检查 TSO 等待时间是否占据 SQL 执行时间的较大比例。如果 TSO 等待时间较高，可考虑以下优化措施：

- 对于不需要严格一致性的读操作，启用低精度 TSO ([`tidb_low_resolution_tso`](/system-variables.md#tidb_low_resolution_tso))。详见 [方案 1：低精度 TSO](#方案-1低精度-tso)。
- 尽量将多个小事务合并为较大的事务。详见[方案 2：TSO 请求并行模式](#方案-2tso-请求并行模式)。

#### 方案 1：低精度 TSO

你可以通过启用低精度 TSO 功能 ([`tidb_low_resolution_tso`](/system-variables.md#tidb_low_resolution_tso)) 来减少 TSO 等待时间。启用后，TiDB 会使用缓存的时间戳进行读取，从而降低 TSO 等待，但可能会读取到过时的数据。

此优化特别适用于以下场景：

- 以读操作为主的负载，且对数据新鲜度要求不高。
- 对查询延迟要求高于绝对一致性的场景。
- 应用可以容忍读取到几秒内的历史数据。

优势与权衡：

- 通过启用使用缓存 TSO 的读取过时数据的功能，可以减少查询延迟，无需请求新的时间戳。
- 在性能与数据一致性之间取得平衡：该功能仅适用于可接受读取过时数据的场景。不建议在需要严格数据一致性的场景中使用。

启用方法：

```sql
SET GLOBAL tidb_low_resolution_tso=ON;
```

#### 方案 2：TSO 请求并行模式

[`tidb_tso_client_rpc_mode`](/system-variables.md#tidb_tso_client_rpc_mode-从-v840-版本开始引入) 系统变量用于切换 TiDB 向 PD 发送 TSO RPC 请求的模式。默认值为 `DEFAULT`。当满足以下条件时，可以考虑将该变量切换为 `PARALLEL` 或 `PARALLEL-FAST`，以获得潜在的性能提升：

- TSO 等待时间在 SQL 查询总执行时间中占比较高。
- PD 的 TSO 分配尚未成为瓶颈。
- PD 和 TiDB 节点的 CPU 资源充足。
- TiDB 与 PD 之间的网络延迟明显高于 PD 分配 TSO 的耗时（即，TSO RPC 的耗时主要由网络延迟决定）。
    - 可通过 Grafana TiDB 面板的 **PD Client > PD TSO RPC Duration** 查看 TSO RPC 请求耗时。
    - 可通过 Grafana PD 面板的 **TiDB > PD server TSO handle duration** 查看 PD 分配 TSO 的耗时。
- TiDB 与 PD 之间因更多 TSO RPC 请求（`PARALLEL` 模式下为 2 倍，`PARALLEL-FAST` 模式下为 4 倍）带来的额外网络流量在可接受范围内。

切换并行模式的方法如下：

```sql
-- Use the PARALLEL mode
SET GLOBAL tidb_tso_client_rpc_mode=PARALLEL;

-- Use the PARALLEL-FAST mode
SET GLOBAL tidb_tso_client_rpc_mode=PARALLEL-FAST;
```

### 针对读密集型负载调优下推计算结果缓存 (Coprocessor Cache)

通过优化[下推计算结果缓存](/coprocessor-cache.md)，可以提升读密集型负载下的查询性能。该缓存用于存储协处理器请求的结果，减少对热点数据的重复计算。优化建议如下：

1. 通过[下推计算结果缓存](/coprocessor-cache.md#查看-grafana-监控面板)监控面板观察缓存命中率。
2. 增大缓存容量，以提升大工作集下的命中率。
3. 根据查询模式调整缓存准入阈值。

以下为读密集型负载推荐配置：

```toml
[tikv-client.copr-cache]
capacity-mb = 4096
admission-max-ranges = 5000
admission-max-result-mb = 10
admission-min-process-ms = 0
```

### 根据负载特性优化 chunk 大小

[`tidb_max_chunk_size`](/system-variables.md#tidb_max_chunk_size) 系统变量用于设置执行过程中每个 chunk 的最大行数。根据不同负载调整该值，可提升查询性能。

- 对于高并发、小事务的 OLTP 负载：

    - 建议设置为 `128`~`256`（默认值为 `1024`）。
    - 可降低内存占用，提升 limit 查询的速度。
    - 适用场景：点查、小范围扫描。

    ```sql
    SET GLOBAL tidb_max_chunk_size = 128;
    ```

- 对于复杂查询、大结果集的 OLAP 或分析型负载：

    - 建议将其值设置为 `1024`~`4096`。
    - 扫描大量数据时可提升吞吐量。
    - 适用场景：聚合、大表扫描。

    ```sql
    SET GLOBAL tidb_max_chunk_size = 4096;
    ```

### 针对不同负载优化事务模式与 DML 类型

TiDB 提供多种事务模式和 DML 执行类型，你可以根据不同负载模式优化性能。

#### 事务模式

你可以通过 [`tidb_txn_mode`](/system-variables.md#tidb_txn_mode) 系统变量设置事务模式。

- [悲观事务模式](/pessimistic-transaction.md)（默认模式）：

    - 适用于可能存在写冲突的一般负载。
    - 提供更强的一致性保障。

  ```sql
  SET SESSION tidb_txn_mode = "pessimistic";
  ```

- [乐观事务模式](/optimistic-transaction.md)：

    - 适用于写冲突较少的负载。
    - 多语句事务下性能更优。
    - 示例：`BEGIN; INSERT...; INSERT...; COMMIT;`。

  ```sql
  SET SESSION tidb_txn_mode = "optimistic";
  ```

#### DML 类型

你可以通过 [`tidb_dml_type`](/system-variables.md#tidb_dml_type-从-v800-版本开始引入) 系统变量（自 v8.0.0 引入）控制 DML 语句的执行模式。

如需使用批量 DML 执行模式，将 `tidb_dml_type` 设置为 `"bulk"`。该模式适用于无冲突的大批量数据写入，可降低大规模写入时的内存消耗。使用前请确保：

- 已开启自动提交事务 [`autocommit`](/system-variables.md#autocommit)。
- [`pessimistic-auto-commit`](/tidb-configuration-file.md#pessimistic-auto-commit) 配置项设置为 `false`。

```sql
SET SESSION tidb_dml_type = "bulk";
```

### 通过 TiKV 下推优化 `GROUP BY` 和 `DISTINCT` 操作

TiDB 支持将聚合操作下推到 TiKV 层执行，以减少数据传输和处理开销。性能提升幅度取决于数据分布和查询特征。

#### 适用场景

- **理想场景**（性能提升明显）：
    - 分组列的基数较低（NDV 较小）。
    - 数据中存在大量重复值。
    - 典型示例：状态字段、类别编码、日期分组等。

- **非理想场景**（可能出现性能下降）：
    - 分组列的基数很高（NDV 较大）。
    - 不重复的标识符或时间戳。
    - 典型示例：用户 ID、交易 ID 等。

#### 配置方法

可在会话级或全局级别启用聚合下推优化：

```sql
-- Enable regular aggregation pushdown
SET GLOBAL tidb_opt_agg_push_down = ON;

-- Enable distinct aggregation pushdown
SET GLOBAL tidb_opt_distinct_agg_push_down = ON;
```

### 使用内存引擎缓解 MVCC 版本积压

在高读写热点区域或垃圾回收、压缩不及时的情况下，过多的 MVCC 版本会导致性能瓶颈。自 v8.5.0 起，你可以通过启用 [TiKV MVCC 内存引擎 (In-Memory Engine, IME)](/tikv-in-memory-engine.md) 来缓解该问题。只需在 TiKV 配置文件中添加如下内容：

> **注意：**
>
> 内存引擎有助于降低 MVCC 版本积压带来的影响，但会增加内存消耗。启用后请关注系统内存使用情况。

```toml
[in-memory-engine]
enable = true
```

### 在批量操作期间优化统计信息收集

通过管理统计信息的收集方式，可以在保持查询优化能力的同时提升批量操作的性能。本节介绍如何有效管理该过程。

#### 何时关闭自动统计信息分析 (Auto Analyze)

在以下场景中，可以通过将系统变量 [`tidb_enable_auto_analyze`](/system-variables.md#tidb_enable_auto_analyze-从-v610-版本开始引入) 设置为 `OFF` 来关闭自动统计信息分析：

- 进行大规模数据导入时。
- 执行批量更新操作时。
- 处理对时间敏感的批处理任务时。
- 需要完全控制统计信息收集时机时。

#### 最佳实践

- 批量操作之前：

   ```sql
   -- Disable auto analyze
   SET GLOBAL tidb_enable_auto_analyze = OFF;
   ```

- 批量操作之后：

   ```sql
   -- Manually collect statistics
   ANALYZE TABLE your_table;
   
   -- Re-enable auto analyze
   SET GLOBAL tidb_enable_auto_analyze = ON;
   ```

### 为不同实例类型优化线程池设置

为提升 TiKV 的性能，应根据实例的 CPU 资源配置线程池。你可以参考以下原则进行优化：

- 对于 8 至 16 核的实例，默认设置通常已经足够。

- 对于 32 核及以上的实例，建议增大线程池大小，以更充分地利用资源。可按如下方式调整设置：

    ```toml
    [server]
    # Increase gRPC thread pool 
    grpc-concurrency = 10
    
    [raftstore]
    # Optimize for write-intensive workloads
    apply-pool-size = 4
    store-pool-size = 4
    store-io-pool-size = 2
    ```
