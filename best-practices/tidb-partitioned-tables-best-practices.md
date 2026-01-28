---
title: 使用 TiDB 分区表的最佳实践
summary: 了解使用 TiDB 分区表的最佳实践，以提高性能、简化数据管理并高效处理大规模数据集。
---

# 使用 TiDB 分区表的最佳实践

本指南介绍如何在 TiDB 中使用分区表 (Partitioned Table) 以提升性能、简化数据管理，并高效处理大规模数据集。

TiDB 的分区表提供了一种灵活的方式来管理大规模数据集，提升查询效率、便于批量删除历史数据并缓解写入热点问题。通过将数据划分为逻辑分区，TiDB 能利用分区裁剪（Partition Pruning）在查询执行时跳过不相关的分区，从而减少资源消耗并提升性能，尤其适用于包含大量数据的联机分析处理 (Online Analytical Processing, OLAP) 工作负载。

一个常见用例是将范围分区 [Range 分区](/partitioned-table.md#range-分区)与本地索引结合，以通过例如 [`ALTER TABLE ... DROP PARTITION`](/sql-statements/sql-statement-alter-table.md) 等操作高效清理历史数据。此方法能几乎瞬间删除过期数据，并在按分区键过滤时保持高查询效率。然而，从非分区表迁移到分区表后，无法利用分区裁剪的查询（例如未包含分区键的查询）可能出现性能下降。在这种情况下，可以使用[全局索引](/global-indexes.md)通过在所有分区间提供统一的索引结构来缓解性能影响。

另一种场景是使用哈希或 Key 分区来解决写入热点问题，尤其是当工作负载使用 [`AUTO_INCREMENT`](/auto-increment.md) ID 时，顺序插入会使得特定 TiKV Region 过载。将写入分散到不同分区可以平衡负载，但与范围分区类似，未能利用分区裁剪的查询可能再次出现性能下降，此时全局索引可以提供帮助。

尽管分区化带来明显好处，但也会引入挑战。例如，新创建的范围分区可能会产生临时热点。为了解决此问题，TiDB 支持自动或手动的 Region 预分裂 (Pre-splitting) 来平衡数据分布并避免瓶颈。

本文从查询优化、数据清理、写入扩展性和索引管理等多个角度审视 TiDB 的分区表，并通过详细场景与最佳实践提供如何优化分区表设计与调优 TiDB 性能的实用指导。

> **注意：**
>
> 要了解基础概念，请参阅[分区表](/partitioned-table.md)，其中解释了分区裁剪、索引类型和分区方法等关键概念。

## 提升查询效率

本节说明通过以下方法提升查询效率：

- [分区裁剪](#分区裁剪)
- [二级索引查询性能：非分区表 vs 本地索引 vs 全局索引](#二级索引查询性能非分区表-vs-本地索引-vs-全局索引)

### 分区裁剪

分区裁剪是一种优化技术，可减少 TiDB 在查询分区表时扫描的数据量。TiDB 会评估查询过滤条件以识别可能包含匹配数据的分区，仅扫描这些分区，从而减少 I/O 和计算开销，大幅提升查询性能。

当查询谓词与分区策略对齐时，分区裁剪效果最佳。典型用例包括：

- 时间序列数据查询：当按时间范围（如按天或按月）分区时，限定在特定时间窗口的查询可以快速跳过无关分区。
- 多租户或按类别划分的数据集：按租户 ID 或类别分区可以让查询仅聚焦少量分区。
- HTAP（混合事务和分析处理）：尤其是对范围分区，TiDB 可以对 TiFlash 上的分析型工作负载应用分区裁剪，从而跳过无关分区，避免对大表进行全表扫描。

更多用例请参阅[分区裁剪](/partition-pruning.md)。

### 二级索引查询性能：非分区表 vs 本地索引 vs 全局索引

在 TiDB 中，分区表默认使用本地索引 (Local Index)，每个分区维护自己的索引集；而全局索引覆盖整张表并跨分区跟踪行。

对于访问多个分区的数据查询，全局索引通常能提供更好的性能。原因在于：使用本地索引的查询需要在每个相关分区分别进行索引查找，而使用全局索引的查询仅需在整表范围内进行一次查找。

#### 测试表类型

本测试比较以下表配置的查询性能：

- 非分区表
- 使用本地索引的分区表
- 使用全局索引的分区表

#### 测试设置

测试配置如下：

- 分区表包含 365 个范围分区，按 `date` 列定义。
- 工作负载模拟高频 OLTP 查询模式，每个索引键匹配多行。
- 测试还评估不同分区数量以衡量分区粒度对查询延迟和索引效率的影响。

#### Schema

示例使用以下表结构。

```sql
CREATE TABLE `fa` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `account_id` bigint(20) NOT NULL,
  `sid` bigint(20) DEFAULT NULL,
  `user_id` bigint NOT NULL,
  `date` int NOT NULL,
  PRIMARY KEY (`id`,`date`) /*T![clustered_index] CLUSTERED */,
  KEY `index_fa_on_sid` (`sid`),
  KEY `index_fa_on_account_id` (`account_id`),
  KEY `index_fa_on_user_id` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin
PARTITION BY RANGE (`date`)(
  PARTITION `fa_2024001` VALUES LESS THAN (2025001),
  PARTITION `fa_2024002` VALUES LESS THAN (2025002),
  PARTITION `fa_2024003` VALUES LESS THAN (2025003),
  ...
  PARTITION `fa_2024365` VALUES LESS THAN (2025365)
);
```

#### SQL

以下 SQL 在二级索引 (`sid`) 上过滤，但未包含分区键 (`date`)：

```sql
SELECT `fa`.*
FROM `fa`
WHERE `fa`.`sid` IN (
  1696271179344,
  1696317134004,
  1696181972136,
  ...
  1696159221765
);
```

该查询模式具有代表性，因为它：

- 在二级索引上过滤但不包含分区键。
- 由于缺乏裁剪，会在每个分区触发本地索引查找。
- 为分区表产生显著更多的表查找任务。

#### 测试结果

下表展示了在包含 365 个范围分区的表上返回 400 行查询的结果。

| 配置 | 平均查询时间 | Cop 任务（索引扫描） | Cop 任务（表查找） | Cop 任务总数 |
|---|---:|---:|---:|---:|
| 非分区表 | 12.6 ms | 72 | 79 | 151 |
| 使用本地索引的分区表 | 108 ms | 600 | 375 | 975 |
| 使用全局索引的分区表 | 14.8 ms | 69 | 383 | 452 |

- 非分区表：提供最佳性能和最少任务数，适合大多数 OLTP 工作负载。
- 使用全局索引的分区表：提升索引扫描效率，但当匹配大量行时表查找仍然昂贵。
- 使用本地索引的分区表：当查询条件不包含分区键时，本地索引查询会扫描所有分区。

> **注意：**
>
> - **平均查询时间** (Average query time) 来源于 `statement_summary` 视图。
> - **Cop 任务**(Cop tasks) 指标取自执行计划。

#### 执行计划示例

下列示例展示了各配置的执行计划。

<details>
<summary><b>非分区表</b></summary>

```
| id                        | estRows | estCost   | actRows | task      | access object                        | execution info | operator info | memory   | disk |
|---------------------------|---------|-----------|---------|-----------|--------------------------------------|----------------|---------------|----------|------|
| IndexLookUp_7             | 398.73  | 787052.13 | 400     | root      |                                      | time:11.5ms, loops:2, index_task:{total_time:3.34ms, fetch_handle:3.34ms, build:600ns, wait:2.86µs}, table_task:{total_time:7.55ms, num:1, concurrency:5}, next:{wait_index:3.49ms, wait_table_lookup_build:492.5µs, wait_table_lookup_resp:7.05ms} |  | 706.7 KB | N/A  |
| IndexRangeScan_5(Build)   | 398.73  | 90633.86  | 400     | cop[tikv] | table:fa, index:index_fa_on_sid(sid) | time:3.16ms, loops:3, cop_task:{num:72, max:780.4µs, min:394.2µs, avg:566.7µs, p95:748µs, max_proc_keys:20, p95_proc_keys:10, tot_proc:3.66ms, tot_wait:18.6ms, copr_cache_hit_ratio:0.00, build_task_duration:94µs, max_distsql_concurrency:15}, rpc_info:{Cop:{num_rpc:72, total_time:40.1ms}}, tikv_task:{proc max:1ms, min:0s, avg:27.8µs, p80:0s, p95:0s, iters:72, tasks:72}, scan_detail:{total_process_keys:400, total_process_keys_size:22800, total_keys:480, get_snapshot_time:17.7ms, rocksdb:{key_skipped_count:400, block:{cache_hit_count:160}}}, time_detail:{total_process_time:3.66ms, total_wait_time:18.6ms, total_kv_read_wall_time:2ms, tikv_wall_time:27.4ms} | range:[1696125963161,1696125963161], …, [1696317134004,1696317134004], keep order:false | N/A | N/A |
| TableRowIDScan_6(Probe)   | 398.73  | 166072.78 | 400     | cop[tikv] | table:fa                             | time:7.01ms, loops:2, cop_task:{num:79, max:4.98ms, min:0s, avg:514.9µs, p95:3.75ms, max_proc_keys:10, p95_proc_keys:5, tot_proc:15ms, tot_wait:21.4ms, copr_cache_hit_ratio:0.00, build_task_duration:341.2µs, max_distsql_concurrency:1, max_extra_concurrency:7, store_batch_num:62}, rpc_info:{Cop:{num_rpc:17, total_time:40.5ms}}, tikv_task:{proc max:0s, min:0s, avg:0s, p80:0s, p95:0s, iters:79, tasks:79}, scan_detail:{total_process_keys:400, total_process_keys_size:489856, total_keys:800, get_snapshot_time:20.8ms, rocksdb:{key_skipped_count:400, block:{cache_hit_count:1600}}}, time_detail:{total_process_time:15ms, total_wait_time:21.4ms, tikv_wall_time:10.9ms} | keep order:false | N/A | N/A |
```

</details>

<details>
<summary><b>使用全局索引的分区表</b></summary>

```
| id                     | estRows | estCost   | actRows | task      | access object                                   | execution info | operator info | memory   | disk |
|------------------------|---------|-----------|---------|-----------|-------------------------------------------------|----------------|---------------|----------|------|
| IndexLookUp_8          | 398.73  | 786959.21 | 400     | root      | partition:all                                   | time:12.8ms, loops:2, index_task:{total_time:2.71ms, fetch_handle:2.71ms, build:528ns, wait:3.23µs}, table_task:{total_time:9.03ms, num:1, concurrency:5}, next:{wait_index:3.27ms, wait_table_lookup_build:1.49ms, wait_table_lookup_resp:7.53ms} |  | 693.9 KB | N/A  |
| IndexRangeScan_5(Build)| 398.73  | 102593.43 | 400     | cop[tikv] | table:fa, index:index_fa_on_sid_global(sid, id)| time:2.49ms, loops:3, cop_task:{num:69, max:997µs, min:213.8µs, avg:469.8µs, p95:986.6µs, max_proc_keys:15, p95_proc_keys:10, tot_proc:13.4ms, tot_wait:1.52ms, copr_cache_hit_ratio:0.00, build_task_duration:498.4µs, max_distsql_concurrency:15}, rpc_info:{Cop:{num_rpc:69, total_time:31.8ms}}, tikv_task:{proc max:1ms, min:0s, avg:101.4µs, p80:0s, p95:1ms, iters:69, tasks:69}, scan_detail:{total_process_keys:400, total_process_keys_size:31200, total_keys:480, get_snapshot_time:679.9µs, rocksdb:{key_skipped_count:400, block:{cache_hit_count:189, read_count:54, read_byte:347.7 KB, read_time:6.17ms}}}, time_detail:{total_process_time:13.4ms, total_wait_time:1.52ms, total_kv_read_wall_time:7ms, tikv_wall_time:19.3ms} | range:[1696125963161,1696125963161], …, keep order:false, stats:partial[...] | N/A | N/A |
| TableRowIDScan_6(Probe)| 398.73  | 165221.64 | 400     | cop[tikv] | table:fa                                        | time:7.47ms, loops:2, cop_task:{num:383, max:4.07ms, min:0s, avg:488.5µs, p95:2.59ms, max_proc_keys:2, p95_proc_keys:1, tot_proc:203.3ms, tot_wait:429.5ms, copr_cache_hit_ratio:0.00, build_task_duration:1.3ms, max_distsql_concurrency:1, max_extra_concurrency:31, store_batch_num:305}, rpc_info:{Cop:{num_rpc:78, total_time:186.3ms}}, tikv_task:{proc max:3ms, min:0s, avg:517µs, p80:1ms, p95:1ms, iters:383, tasks:383}, scan_detail:{total_process_keys:400, total_process_keys_size:489856, total_keys:800, get_snapshot_time:2.99ms, rocksdb:{key_skipped_count:400, block:{cache_hit_count:1601, read_count:799, read_byte:10.1 MB, read_time:131.6ms}}}, time_detail:{total_process_time:203.3ms, total_suspend_time:6.31ms, total_wait_time:429.5ms, total_kv_read_wall_time:198ms, tikv_wall_time:163ms} | keep order:false, stats:partial[...] | N/A | N/A |
```

</details>

<details>
<summary><b>使用本地索引的分区表</b></summary>

```
| id                     | estRows | estCost   | actRows | task      | access object                        | execution info | operator info | memory  | disk  |
|------------------------|---------|-----------|---------|-----------|--------------------------------------|----------------|---------------|---------|-------|
| IndexLookUp_7          | 398.73  | 784450.63 | 400     | root      | partition:all                        | time:290.8ms, loops:2, index_task:{total_time:103.6ms, fetch_handle:7.74ms, build:133.2µs, wait:95.7ms}, table_task:{total_time:551.1ms, num:217, concurrency:5}, next:{wait_index:179.6ms, wait_table_lookup_build:391µs, wait_table_lookup_resp:109.5ms} |  | 4.30 MB | N/A  |
| IndexRangeScan_5(Build)| 398.73  | 90633.73  | 400     | cop[tikv] | table:fa, index:index_fa_on_sid(sid) | time:10.8ms, loops:800, cop_task:{num:600, max:65.6ms, min:1.02ms, avg:22.2ms, p95:45.1ms, max_proc_keys:5, p95_proc_keys:3, tot_proc:6.81s, tot_wait:4.77s, copr_cache_hit_ratio:0.00, build_task_duration:172.8ms, max_distsql_concurrency:3}, rpc_info:{Cop:{num_rpc:600, total_time:13.3s}}, tikv_task:{proc max:54ms, min:0s, avg:13.9ms, p80:20ms, p95:30ms, iters:600, tasks:600}, scan_detail:{total_process_keys:400, total_process_keys_size:22800, total_keys:29680, get_snapshot_time:2.47s, rocksdb:{key_skipped_count:400, block:{cache_hit_count:117580, read_count:29437, read_byte:104.9 MB, read_time:3.24s}}}, time_detail:{total_process_time:6.81s, total_suspend_time:1.51s, total_wait_time:4.77s, total_kv_read_wall_time:8.31s, tikv_wall_time:13.2s}} | range:[1696125963161,...,1696317134004], keep order:false, stats:partial[...] | N/A | N/A |
| TableRowIDScan_6(Probe)| 398.73  | 165221.49 | 400     | cop[tikv] | table:fa                             | time:514ms, loops:434, cop_task:{num:375, max:31.6ms, min:0s, avg:1.33ms, p95:1.67ms, max_proc_keys:2, p95_proc_keys:2, tot_proc:220.7ms, tot_wait:242.2ms, copr_cache_hit_ratio:0.00, build_task_duration:27.8ms, max_distsql_concurrency:1, max_extra_concurrency:1, store_batch_num:69}, rpc_info:{Cop:{num_rpc:306, total_time:495.5ms}}, tikv_task:{proc max:6ms, min:0s, avg:597.3µs, p80:1ms, p95:1ms, iters:375, tasks:375}, scan_detail:{total_process_keys:400, total_process_keys_size:489856, total_keys:800, get_snapshot_time:158.3ms, rocksdb:{key_skipped_count:400, block:{cache_hit_count:3197, read_count:803, read_byte:10.2 MB, read_time:113.5ms}}}, time_detail:{total_process_time:220.7ms, total_suspend_time:5.39ms, total_wait_time:242.2ms, total_kv_read_wall_time:224ms, tikv_wall_time:430.5ms}} | keep order:false, stats:partial[...] | N/A | N/A |
```

</details>

#### 在分区表上创建全局索引

你可以使用以下方法之一在分区表上创建全局索引。

> **注意：**
>
> - 在 TiDB v8.5.3 及更早版本中，你只能在唯一列上创建全局索引。从 v8.5.4 开始，TiDB 支持在非唯一列上创建全局索引。此限制将在未来的 LTS 版本中移除。
> - 对于非唯一全局索引，使用 `ADD INDEX` 而不是 `ADD UNIQUE INDEX`。
> - 必须显式指定 `GLOBAL` 关键字。

##### 方式 1：使用 `ALTER TABLE`

向现有分区表添加全局索引：

```sql
ALTER TABLE <table_name>
ADD UNIQUE INDEX <index_name> (col1, col2) GLOBAL;
```

##### 方式 2：在建表时定义索引

在 `CREATE TABLE` 语句中内联定义全局索引以创建表时同时创建该索引：

```sql
CREATE TABLE t (
  id BIGINT NOT NULL,
  col1 VARCHAR(50),
  col2 VARCHAR(50),
  -- other columns...
  UNIQUE GLOBAL INDEX idx_col1_col2 (col1, col2)
)
PARTITION BY RANGE (id) (
  PARTITION p0 VALUES LESS THAN (10000),
  PARTITION p1 VALUES LESS THAN (20000),
  PARTITION pMax VALUES LESS THAN MAXVALUE
);
```

#### 性能总结

TiDB 分区表的性能开销取决于分区数量和索引类型。

- 分区数量：分区数量越多，性能会下降。对于少量分区，影响可能可忽略，但这取决于具体工作负载。
- 本地索引：如果查询未包含有效的分区裁剪条件，则分区数量直接决定[远程过程调用 (Remote Procedure Calls, RPCs)](https://docs.pingcap.com/tidb/stable/glossary/#remote-procedure-call-rpc) 的次数。这意味着更多的分区通常导致更多 RPC 和更高延迟。
- 全局索引：性能取决于涉及的分区数量以及需要表查找的行数。对于数据分布在多个 Region 的超大表，通过全局索引访问数据的性能与非分区表相似，因为两者都涉及多个跨 Region 的 RPC。

#### 建议

在设计 TiDB 分区表和索引时遵循以下指导：

- 仅在必要时使用分区表。对于大多数 OLTP 工作负载，良好索引的非分区表提供更好的性能和更简单的管理。
- 当所有查询都包含能有效裁剪为少量分区的条件时，使用本地索引。
- 对于关键查询（缺乏有效分区裁剪且匹配大量分区），使用全局索引。
- 当优先考虑 DDL 操作效率（例如快速 `DROP PARTITION`）且可接受潜在性能影响时，仅使用本地索引。

## 便于批量删除数据

在 TiDB 中，你可以使用 [TTL (Time to Live)](/time-to-live.md) 或手动删除分区来移除历史数据。尽管两者都能删除数据，但其性能特性差异明显。下列测试结果表明，删除分区通常更快且消耗更少资源，是处理大规模数据或频繁清理数据的更好选择。

### TTL 与 `DROP PARTITION` 的区别

- TTL：基于数据年龄自动删除数据。此方法可能较慢，因为它会增量扫描并删除行。
- `DROP PARTITION`：一次性删除整个分区。该方法通常更快，尤其针对大数据量时。

#### 测试用例

此测试比较 TTL 和 `DROP PARTITION` 的性能。

- TTL 配置：每 10 分钟运行一次。
- 分区配置：每 10 分钟删除一个分区。
- 工作负载：后台写入负载，50 和 100 并发线程。

测试衡量执行时间、系统资源使用和删除的总行数。

#### 发现

> **注意：**
>
> 本节描述的性能优势仅适用于没有全局索引的分区表。

关于 TTL 的发现：

- 在 50 线程情况下，每个 TTL 作业耗时 8 到 10 分钟，删除 700 到 1100 万行。
- 在 100 线程情况下，TTL 能处理最多约 2000 万行，但执行时间增加到 15 到 30 分钟且波动较大。
- 在高负载下，TTL 作业因额外的扫描和删除开销会降低整体 QPS。

关于 `DROP PARTITION` 的发现：

- `ALTER TABLE ... DROP PARTITION` 语句几乎即时删除整个分区。
- 该操作消耗资源少，因为其主要在元数据层面发生。
- 对于大型历史数据集，`DROP PARTITION` 比 TTL 更快且更可预测。

#### 在 TiDB 中使用 TTL 与 `DROP PARTITION`

下面示例使用匿名表结构。有关 TTL 的更多信息，请参阅[使用 TTL (Time to Live) 定期删除过期数据](/time-to-live.md)。

以下示例展示了启用 TTL 的表模式：

```sql
CREATE TABLE `ad_cache` (
  `session_id` varchar(255) NOT NULL,
  `external_id` varbinary(255) NOT NULL,
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `id_suffix` bigint(20) NOT NULL,
  `expire_time` timestamp NULL DEFAULT NULL,
  `cache_data` mediumblob DEFAULT NULL,
  `data_version` int(11) DEFAULT NULL,
  `is_deleted` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`session_id`, `external_id`, `create_time`, `id_suffix`)
)
ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin
TTL=`expire_time` + INTERVAL 0 DAY TTL_ENABLE='ON'
TTL_JOB_INTERVAL='10m';
```

以下示例展示使用 Range INTERVAL 分区的表：

```sql
CREATE TABLE `ad_cache` (
  `session_id` varchar(255) NOT NULL,
  `external_id` varbinary(255) NOT NULL,
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `id_suffix` bigint(20) NOT NULL,
  `expire_time` timestamp NULL DEFAULT NULL,
  `cache_data` mediumblob DEFAULT NULL,
  `data_version` int(11) DEFAULT NULL,
  `is_deleted` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (
    `session_id`, `external_id`,
    `create_time`, `id_suffix`
  ) NONCLUSTERED
)
SHARD_ROW_ID_BITS=7
PRE_SPLIT_REGIONS=2
PARTITION BY RANGE COLUMNS (create_time)
INTERVAL (10 MINUTE)
FIRST PARTITION LESS THAN ('2025-02-19 18:00:00')
...
LAST PARTITION LESS THAN ('2025-02-19 20:00:00');
```

要定期更新 `FIRST PARTITION` 和 `LAST PARTITION`，运行类似以下的 DDL 语句以删除旧分区并创建新分区。

```sql
ALTER TABLE ad_cache FIRST PARTITION LESS THAN ("${nextTimestamp}");
ALTER TABLE ad_cache LAST PARTITION LESS THAN ("${nextTimestamp}");
```

#### 建议

- 对于大规模或基于时间的数据清理，使用分区表并通过 `DROP PARTITION` 删除数据。该方法提供更好的性能、更低的系统影响和更简单的运维行为。
- 对于细粒度或后台数据清理，使用 TTL。TTL 不适合具有高写入吞吐或需要快速删除大量数据的工作负载。

### 分区删除效率：本地索引 vs 全局索引

对于带有全局索引的分区表，DDL 操作（例如 `DROP PARTITION`、`TRUNCATE PARTITION` 和 `REORGANIZE PARTITION`）必须同步更新全局索引条目。这些更新会显著增加 DDL 执行时间。

本节展示在使用全局索引的表上执行 `DROP PARTITION` 会比使用本地索引的表慢得多。在设计分区表时需考虑这一点。

#### 测试用例

本测试在创建了 365 个分区、约 10 亿行的数据表上比较使用全局索引与本地索引时 `DROP PARTITION` 的性能。

| 索引类型  | 删除分区耗时 |
|----------|------------:|
| 全局索引  | 76.02 秒    |
| 本地索引  | 0.52 秒     |

#### 发现

在带有全局索引的表上删除分区耗时 **76.02 秒**，而在带有本地索引的表上仅需 **0.52 秒**。差异来源于全局索引跨所有分区，需要额外的索引更新，而本地索引随分区数据一起被删除。

你可以使用下列 SQL 删除分区：

```sql
ALTER TABLE A DROP PARTITION A_2024363;
```

#### 建议

- 如果分区表使用全局索引，预期诸如 `DROP PARTITION`、`TRUNCATE PARTITION` 和 `REORGANIZE PARTITION` 的执行时间会更长。
- 如果需要频繁删除分区并尽量减少性能影响，应使用本地索引以实现更快、更高效的分区管理。

## 缓解热点问题

在 TiDB 中，热点发生于读写流量在 [Regions](/tidb-storage.md#region) 之间分布不均的情况。热点通常出现于下列场景：

- 单调递增的主键，例如 `AUTO_INCREMENT` 主键且 `AUTO_ID_CACHE=1`。
- 在 datetime 列上有默认值为 `CURRENT_TIMESTAMP` 的二级索引。

TiDB 会将新行和索引条目追加到“最右侧”的 Region。随着时间推移，这会导致以下问题：

- 单个 Region 承担大部分写入工作，而其他 Region 闲置。
- 读写延迟增加，总体吞吐下降。
- 即使添加更多 TiKV 节点，也难以显著提升性能，因为瓶颈仍在单个 Region。

为缓解这些问题，可以使用分区表。对主键应用哈希或 Key 分区，可以将插入操作分散到多个分区和 Region，从而减少单个 Region 的热点争用。

> **注意：**
>
> 本节以分区表为示例说明缓解读写热点。TiDB 还提供其他热点缓解功能，例如 [`AUTO_INCREMENT`](/auto-increment.md) 和 [`SHARD_ROW_ID_BITS`](/shard-row-id-bits.md)。
>
> 在特定场景下使用分区表时，将 `merge_option=deny` 用于保留分区边界的策略。更多信息见 [issue #58128](https://github.com/pingcap/tidb/issues/58128)。

### 分区如何工作

TiDB 将表数据和索引存储在 Region 中，每个 Region 覆盖一段连续的行键范围。表使用 `AUTO_INCREMENT` 主键或单调递增的 datetime 索引时，写入负载的分布取决于表是否分区。

非分区表：

- 在非分区表中，新行总是具有最大的键值并写入同一个“最后”Region。该 Region（由单个 TiKV 节点服务）可能成为写入瓶颈。

哈希或 Key 分区表：

- TiDB 对主键或被索引列应用哈希或 Key 函数，将表和索引拆分为多个分区。
- 每个分区有自己的 Region 集，通常分布在不同的 TiKV 节点上。
- 插入操作并行分布在多个 Region 上，从而改善负载平衡与写入吞吐。

### 何时使用分区

如果具有 [`AUTO_INCREMENT`](/auto-increment.md) 主键的表发生大量批量插入并出现写热点，请对主键应用哈希或 Key 分区以更均匀地分布写入负载。

下列 SQL 创建了一个基于主键的 16 分区表：

```sql
CREATE TABLE server_info (
  id bigint NOT NULL AUTO_INCREMENT,
  serial_no varchar(100) DEFAULT NULL,
  device_name varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  device_type varchar(50) DEFAULT NULL,
  modified_ts timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (id) /*T![clustered_index] CLUSTERED */,
  KEY idx_serial_no (serial_no),
  KEY idx_modified_ts (modified_ts)
) /*T![auto_id_cache] AUTO_ID_CACHE=1 */
PARTITION BY KEY (id) PARTITIONS 16;
```

### 优势

分区表具有以下优势：

- **平衡写入负载**：热点被分布到多个分区和 Region，减少争用并提升插入性能。
- **通过分区裁剪改善查询性能**：对于按分区键过滤的查询，TiDB 会跳过无关分区，减少扫描数据并提升查询延迟。

### 限制

在使用分区表前，请考虑以下限制：

- 将非分区表转换为分区表会增加 Region 总数，因为 TiDB 为每个分区创建独立的 Region。
- 未按分区键过滤的查询无法使用分区裁剪。TiDB 必须扫描所有分区或在所有分区上执行索引查找，这会增加 coprocessor 任务数并降低性能。

    例如，下面的查询未使用分区键 (`id`)，可能会出现性能下降：

    ```sql
    SELECT * FROM server_info WHERE `serial_no` = ?;
    ```

- 为了减少未使用分区键查询的扫描开销，需要创建全局索引。尽管全局索引会降低 `DROP PARTITION` 的速度，但哈希和 Key 分区表不支持 `DROP PARTITION`，因此全局索引在这种场景中是实际的解决方案，因为这些分区通常不会被截断 (Truncate)。例如：

    ```sql
    ALTER TABLE server_info ADD UNIQUE INDEX(serial_no, id) GLOBAL;
    ```

## 分区管理的挑战

新的范围分区在 TiDB 中可能导致热点问题。本节描述常见场景并提供缓解策略。

### 读热点

在范围分区表中，如果查询未按分区键过滤，新创建的空分区可能成为读热点。

根本原因：

- 默认情况下，TiDB 在创建表时为每个分区创建一个空 Region。如果一段时间内没有写入数据，TiDB 可能会将多个空分区的 Region 合并为单个 Region。

影响：

- 当查询未按分区键过滤时，执行计划中会显示为 `partition:all`，TiDB 会扫描所有分区。单个包含多个空分区的 Region 会被反复扫描，导致读热点。

### 写热点

使用基于时间的列作为分区键，当流量转移到新分区时可能产生写热点。

根本原因：

- 在 TiDB 中，新创建的分区最初只有单个 Region 位于某个 TiKV 节点。所有写入都会定向到该单个 Region，直到其拆分并重新分布数据。在此期间，TiKV 节点需要同时处理应用写入和 Region 拆分任务。
- 如果新分区的初始写入流量非常高，TiKV 节点可能没有足够资源（如 CPU 或 I/O）来及时拆分和打散 (Scatter) Regions，导致写入在较长时间内集中在同一节点。

影响：

- 这种不平衡可能触发 TiKV 节点的流控，导致 QPS 急剧下降、写入延迟上升和 CPU 利用率升高，从而影响整个集群性能。

### 分区表类型比较

下表比较了非聚簇 (Non-clustered) 分区表、聚簇 (Clustered) 分区表和聚簇非分区表：

| 表类型                      | Region 预分裂 | 读性能     | 写扩展性 | 按分区清理数据 |
|---|---:|---|---|---|
| 非聚簇分区表 | 自动 | 较低（需要额外查找） | 高 | 支持 |
| 聚簇分区表     | 手动 | 高（查找更少） | 高（需手动管理） | 支持 |
| 聚簇非分区表 | 不适用 | 高 | 稳定 | 不支持 |

### 非聚簇分区表的解决方案

#### 优势

- 当你创建配置了 [`SHARD_ROW_ID_BITS`](/shard-row-id-bits.md) 和 [`PRE_SPLIT_REGIONS`](/sql-statements/sql-statement-split-region.md#pre_split_regions) 的非聚簇分区表时，TiDB 会自动预分裂 Regions，显著降低手动工作量。
- 运维开销低。

#### 缺点

- 使用点查 (Point Get) 或表范围扫描 (Table Range Scan) 时需要额外的表查找，可能导致读性能下降。

#### 适用场景

当写扩展性和运维简便优于低延迟读取时，使用非聚簇分区表。

#### 最佳实践

为缓解新范围分区引发的热点问题，执行以下步骤。

##### 第 1 步：使用 `SHARD_ROW_ID_BITS` 和 `PRE_SPLIT_REGIONS`

创建带 [`SHARD_ROW_ID_BITS`](/shard-row-id-bits.md) 和 [`PRE_SPLIT_REGIONS`](/sql-statements/sql-statement-split-region.md#pre_split_regions) 的分区表以预分裂 Regions。

要求：

- `PRE_SPLIT_REGIONS` 的值必须小于或等于 `SHARD_ROW_ID_BITS`。
- 每个分区会被预分裂为 `2^(PRE_SPLIT_REGIONS)` 个 Region。

```sql
CREATE TABLE employees (
  id INT NOT NULL,
  fname VARCHAR(30),
  lname VARCHAR(30),
  hired DATE NOT NULL DEFAULT '1970-01-01',
  separated DATE DEFAULT '9999-12-31',
  job_code INT,
  store_id INT,
  PRIMARY KEY (`id`,`hired`) NONCLUSTERED,
  KEY `idx_employees_on_store_id` (`store_id`)
) SHARD_ROW_ID_BITS = 2 PRE_SPLIT_REGIONS = 2
PARTITION BY RANGE ( YEAR(hired) ) (
  PARTITION p0 VALUES LESS THAN (1991),
  PARTITION p1 VALUES LESS THAN (1996),
  PARTITION p2 VALUES LESS THAN (2001),
  PARTITION p3 VALUES LESS THAN (2006)
);
```

##### 第 2 步：添加 `merge_option=deny` 属性

在表级或分区级添加 [`merge_option=deny`](/table-attributes.md#使用表属性控制-region-合并) 属性，以防止空 Region 被合并。当你删除分区时，TiDB 仍会合并属于被删除分区的 Regions。

```sql
-- 表级
ALTER TABLE employees ATTRIBUTES 'merge_option=deny';
-- 分区级
ALTER TABLE employees PARTITION `p3` ATTRIBUTES 'merge_option=deny';
```

##### 第 3 步：根据业务数据确定拆分边界

在创建表或添加分区前，为避免热点进行预分裂。为有效预分裂，基于实际业务数据分布配置 Region 拆分的上下界。避免设置过宽的边界，因为这会阻碍数据在 TiKV 节点间的有效分布，失去预分裂的意义。

确定现有生产数据的最小值和最大值，使得后续写入能落到不同的预分配 Region。以下查询示例用于获取现有数据范围：

```sql
SELECT MIN(id), MAX(id) FROM employees;
```

- 如果表没有历史数据，请根据业务需求和预期数据范围估算最小值和最大值。
- 对于复合主键或复合索引，仅使用最左列来定义拆分边界。
- 如果最左列是字符串，需考虑其长度和值分布以确保均匀分布。

##### 第 4 步：预分裂并打散 (Scatter) Regions

常见做法是将 Region 数与 TiKV 节点数量匹配，或设置为 TiKV 节点数量的两倍。这有助于从一开始就使数据更均匀地分布在集群中。

##### 第 5 步：按需为主键和二级索引拆分 Regions

要为分区表中所有分区的主键拆分 Regions，请使用以下 SQL：

```sql
SPLIT PARTITION TABLE employees INDEX `PRIMARY` BETWEEN (1, "1970-01-01") AND (100000, "9999-12-31") REGIONS <number_of_regions>;
```

该示例将在指定边界内将每个分区的主键范围拆分为 `<number_of_regions>` 个 Region。

要为分区表中所有分区的二级索引拆分 Regions，请使用以下 SQL：

```sql
SPLIT PARTITION TABLE employees INDEX `idx_employees_on_store_id` BETWEEN (1) AND (1000) REGIONS <number_of_regions>;
```

##### （可选）第 6 步：在添加新分区时手动拆分 Regions

在添加分区时，你可以为其主键和索引手动拆分 Regions。

```sql
ALTER TABLE employees ADD PARTITION (PARTITION p4 VALUES LESS THAN (2011));

SHOW TABLE employees PARTITION (p4) regions;

SPLIT PARTITION TABLE employees INDEX `PRIMARY` BETWEEN (1, "2006-01-01") AND (100000, "2011-01-01") REGIONS <number_of_regions>;

SPLIT PARTITION TABLE employees PARTITION (p4) INDEX `idx_employees_on_store_id` BETWEEN (1) AND (1000) REGIONS <number_of_regions>;

SHOW TABLE employees PARTITION (p4) regions;
```

### 聚簇分区表的解决方案

#### 优势

使用点查 (Point Get) 或表范围扫描 (Table Range Scan) 时无需额外查找，可提升读性能。

#### 缺点

在创建新分区时必须手动拆分 Regions，增加运维复杂度。

#### 适用场景

当低延迟点查询至关重要且能够管理手动 Region 拆分时，使用聚簇分区表。

#### 最佳实践

为缓解新范围分区引发的热点问题，请参阅[非聚簇分区表的最佳实践](#非聚簇分区表的解决方案)。

### 聚簇非分区表的解决方案

#### 优势

- 不会有因新范围分区产生的热点风险。
- 对点查和范围查询具有良好读取性能。

#### 缺点

- 无法使用 `DROP PARTITION` 高效删除大量历史数据。

#### 适用场景

当需要稳定性能且不需要基于分区的数据生命周期管理时，使用聚簇非分区表。

## 在分区表与非分区表之间转换

对于大型表（例如 1.2 亿行），你可能需要在分区与非分区模式之间转换以进行性能调优或模式重构。TiDB 支持以下方法：

- [Pipelined DML](/pipelined-dml.md)：`INSERT INTO ... SELECT ...`
- [`IMPORT INTO`](/sql-statements/sql-statement-import-into.md)：`IMPORT INTO ... FROM SELECT ...`
- [在线 DDL](/dm/feature-online-ddl.md)：使用 `ALTER TABLE` 直接变更模式

本节比较这些方法在两种转换方向上的效率与影响，并给出最佳实践建议。

### 分区表模式：`fa`

```sql
CREATE TABLE `fa` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `account_id` bigint(20) NOT NULL,
  `sid` bigint(20) DEFAULT NULL,
  `user_id` bigint NOT NULL,
  `date` int NOT NULL,
  PRIMARY KEY (`id`,`date`) /*T![clustered_index] CLUSTERED */,
  KEY `index_fa_on_sid` (`sid`),
  KEY `index_fa_on_account_id` (`account_id`),
  KEY `index_fa_on_user_id` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin
PARTITION BY RANGE (`date`)
(PARTITION `fa_2024001` VALUES LESS THAN (2025001),
PARTITION `fa_2024002` VALUES LESS THAN (2025002),
PARTITION `fa_2024003` VALUES LESS THAN (2025003),
...
PARTITION `fa_2024365` VALUES LESS THAN (2025365));
```

### 非分区表模式：`fa_new`

```sql
CREATE TABLE `fa_new` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `account_id` bigint(20) NOT NULL,
  `sid` bigint(20) DEFAULT NULL,
  `user_id` bigint NOT NULL,
  `date` int NOT NULL,
  PRIMARY KEY (`id`,`date`) /*T![clustered_index] CLUSTERED */,
  KEY `index_fa_on_sid` (`sid`),
  KEY `index_fa_on_account_id` (`account_id`),
  KEY `index_fa_on_user_id` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;
```

这些示例展示了将分区表转换为非分区表的过程。将非分区表转换为分区表时也可使用相同方法。

### 方法 1：Pipelined DML `INSERT INTO ... SELECT`

```sql
SET tidb_dml_type = "bulk";
SET tidb_mem_quota_query = 0;
SET tidb_enable_mutation_checker = OFF;
INSERT INTO fa_new SELECT * FROM fa;
-- 1.2 亿行复制耗时 58m 42s
```

### 方法 2：`IMPORT INTO ... FROM SELECT`

```sql
IMPORT INTO fa_new FROM SELECT * FROM fa WITH thread = 32, disable_precheck;
```

```
Query OK, 120000000 rows affected, 1 warning (16 min 49.90 sec)
Records: 120000000, ID: c1d04eec-fb49-49bb-af92-bf3d6e2d3d87
```

### 方法 3：在线 DDL

下列 SQL 将分区表转换为非分区表：

```sql
SET @@global.tidb_ddl_REORGANIZE_worker_cnt = 16;
SET @@global.tidb_ddl_REORGANIZE_batch_size = 4096;
ALTER TABLE fa REMOVE PARTITIONING;
-- 实际耗时：170m 12.024s（约 2 小时 50 分钟）
```

下列 SQL 将非分区表转换为分区表：

```sql
SET @@global.tidb_ddl_REORGANIZE_worker_cnt = 16;
SET @@global.tidb_ddl_REORGANIZE_batch_size = 4096;
ALTER TABLE fa_new PARTITION BY RANGE (`date`)
(PARTITION `fa_2024001` VALUES LESS THAN (2025001),
PARTITION `fa_2024002` VALUES LESS THAN (2025002),
...
PARTITION `fa_2024365` VALUES LESS THAN (2025365),
PARTITION `fa_2024366` VALUES LESS THAN (2025366));

Query OK, 0 rows affected, 1 warning (2 hours 31 min 57.05 sec)
```

### 发现

下表展示了对 1.2 亿行表，各方法所耗时间：

| 方法 | 耗时 |
|--------|------------:|
| 方法 1：Pipelined DML (`INSERT INTO ... SELECT ...`) | 58m 42s |
| 方法 2：`IMPORT INTO ... FROM SELECT ...` | 16m 59s |
| 方法 3：在线 DDL（从分区表到非分区表） | 2h 50m |
| 方法 3：在线 DDL（从非分区表到分区表） | 2h 31m |
