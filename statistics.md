---
title: 统计信息简介
summary: 了解统计信息如何收集表级和列级信息。
---

# 统计信息简介

TiDB 使用统计信息作为优化器的输入，以估计 SQL 语句中每个计划步骤处理的行数。优化器估计每个可用计划选择的成本，包括[索引访问](/choose-index.md)和表连接的顺序，并为每个可用计划生成成本。然后，优化器选择总体成本最低的执行计划。

## 收集统计信息

本节描述收集统计信息的两种方式：自动更新和手动收集。

### 自动更新

对于 [`INSERT`](/sql-statements/sql-statement-insert.md)、[`DELETE`](/sql-statements/sql-statement-delete.md) 或 [`UPDATE`](/sql-statements/sql-statement-update.md) 语句，TiDB 会自动更新统计信息中的行数和修改行数。

<CustomContent platform="tidb">

TiDB 定期持久化更新信息，更新周期为 20 * [`stats-lease`](/tidb-configuration-file.md#stats-lease)。`stats-lease` 的默认值为 `3s`。如果将该值指定为 `0`，TiDB 将停止自动更新统计信息。

</CustomContent>

<CustomContent platform="tidb-cloud">

TiDB 每 60 秒持久化一次更新信息。

</CustomContent>

根据表的变更数量，TiDB 会自动调度 [`ANALYZE`](/sql-statements/sql-statement-analyze-table.md) 来收集这些表的统计信息。这由系统变量 [`tidb_enable_auto_analyze`](/system-variables.md#tidb_enable_auto_analyze-new-in-v610) 和以下 `tidb_auto_analyze%` 变量控制。

|  系统变量 | 默认值 | 描述 |
|---|---|---|
| [`tidb_enable_auto_analyze`](/system-variables.md#tidb_enable_auto_analyze-new-in-v610) | `ON` | 控制 TiDB 是否自动执行 `ANALYZE`。 |
| [`tidb_auto_analyze_ratio`](/system-variables.md#tidb_auto_analyze_ratio) | `0.5` | 自动更新的阈值。 |
| [`tidb_auto_analyze_start_time`](/system-variables.md#tidb_auto_analyze_start_time) | `00:00 +0000` | TiDB 一天中可以执行自动更新的开始时间。 |
| [`tidb_auto_analyze_end_time`](/system-variables.md#tidb_auto_analyze_end_time)   | `23:59 +0000` | TiDB 一天中可以执行自动更新的结束时间。 |
| [`tidb_auto_analyze_partition_batch_size`](/system-variables.md#tidb_auto_analyze_partition_batch_size-new-in-v640) | `128` | TiDB 在分析分区表时自动分析的分区数量（即在自动更新分区表的统计信息时）。 |
| [`tidb_enable_auto_analyze_priority_queue`](/system-variables.md#tidb_enable_auto_analyze_priority_queue-new-in-v800) | `ON` | 控制是否启用优先级队列来调度自动收集统计信息的任务。启用此变量后，TiDB 会优先收集更有价值的表的统计信息，例如新创建的索引和分区变更的分区表。此外，TiDB 会优先处理健康分数较低的表，将它们放在队列前面。 |

当表 `tbl` 中修改的行数与总行数的比率大于 `tidb_auto_analyze_ratio`，并且当前时间在 `tidb_auto_analyze_start_time` 和 `tidb_auto_analyze_end_time` 之间时，TiDB 会在后台执行 `ANALYZE TABLE tbl` 语句，自动更新这个表的统计信息。

为了避免频繁修改小表数据触发自动更新的情况，当表的行数少于 1000 行时，修改不会触发 TiDB 的自动更新。您可以使用 `SHOW STATS_META` 语句查看表中的行数。

> **注意：**
>
> 目前，自动更新不会记录手动 `ANALYZE` 时输入的配置项。因此，当您使用 [`WITH`](/sql-statements/sql-statement-analyze-table.md) 语法控制 `ANALYZE` 的收集行为时，您需要手动设置定时任务来收集统计信息。
