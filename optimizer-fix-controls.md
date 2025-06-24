---
title: 优化器修复控制
summary: 了解优化器修复控制功能以及如何使用 tidb_opt_fix_control 更细粒度地控制 TiDB 优化器。
---

# 优化器修复控制

随着产品的迭代演进，TiDB 优化器的行为会发生变化，从而生成更合理的执行计划。然而，在某些特定场景下，新的行为可能会导致意外结果。例如：

- 某些行为的效果依赖于特定场景。对大多数场景有改进的变更可能会导致其他场景的性能回退。
- 有时，行为细节的变化与其后果之间的关系非常复杂。某个行为的改进可能会导致整体性能回退。

因此，TiDB 提供了优化器修复控制功能，允许你通过设置一组修复项的值来对 TiDB 优化器行为进行细粒度控制。本文档描述了优化器修复控制功能及其使用方法，并列出了 TiDB 当前支持的所有优化器修复控制项。

## `tidb_opt_fix_control` 简介

从 v6.5.3 和 v7.1.0 开始，TiDB 提供了 [`tidb_opt_fix_control`](/system-variables.md#tidb_opt_fix_control-new-in-v653-and-v710) 系统变量，用于更细粒度地控制优化器的行为。

每个修复项都是一个控制项，用于调整 TiDB 优化器中针对特定目的的行为。它用一个数字表示，对应包含行为变更技术细节的 GitHub Issue。例如，对于修复项 `44262`，你可以在 [Issue 44262](https://github.com/pingcap/tidb/issues/44262) 中查看它控制的内容。

[`tidb_opt_fix_control`](/system-variables.md#tidb_opt_fix_control-new-in-v653-and-v710) 系统变量接受多个修复项作为一个值，用逗号（`,`）分隔。格式为 `"<#issue1>:<value1>,<#issue2>:<value2>,...,<#issueN>:<valueN>"`，其中 `<#issueN>` 是修复项编号。例如：

```sql
SET SESSION tidb_opt_fix_control = '44262:ON,44389:ON';
```

## 优化器修复控制参考

### [`33031`](https://github.com/pingcap/tidb/issues/33031) <span class="version-mark">v8.0.0 新增</span>

- 默认值：`OFF`
- 可选值：`ON`，`OFF`
- 该变量控制是否允许对分区表使用计划缓存。如果设置为 `ON`，[预处理语句计划缓存](/sql-prepared-plan-cache.md)和[非预处理语句计划缓存](/sql-non-prepared-plan-cache.md)都不会对[分区表](/partitioned-table.md)启用。

### [`44262`](https://github.com/pingcap/tidb/issues/44262) <span class="version-mark">v6.5.3 和 v7.2.0 新增</span>

- 默认值：`OFF`
- 可选值：`ON`，`OFF`
- 该变量控制在缺少 [GlobalStats](/statistics.md#collect-statistics-of-partitioned-tables-in-dynamic-pruning-mode) 时是否允许使用[动态裁剪模式](/partitioned-table.md#dynamic-pruning-mode)访问分区表。

### [`44389`](https://github.com/pingcap/tidb/issues/44389) <span class="version-mark">v6.5.3 和 v7.2.0 新增</span>

- 默认值：`OFF`
- 可选值：`ON`，`OFF`
- 对于类似 `c = 10 and (a = 'xx' or (a = 'kk' and b = 1))` 的过滤条件，该变量控制是否尝试为 `IndexRangeScan` 构建更全面的扫描范围。

### [`44823`](https://github.com/pingcap/tidb/issues/44823) <span class="version-mark">v7.3.0 新增</span>

- 默认值：`200`
- 可选值：`[0, 2147483647]`
- 为了节省内存，计划缓存不会缓存参数数量超过该变量指定值的查询。`0` 表示无限制。

### [`44830`](https://github.com/pingcap/tidb/issues/44830) <span class="version-mark">v6.5.7 和 v7.3.0 新增</span>

- 默认值：`OFF`
- 可选值：`ON`，`OFF`
- 该变量控制计划缓存是否允许缓存在物理优化阶段生成的带有 `PointGet` 算子的执行计划。

### [`44855`](https://github.com/pingcap/tidb/issues/44855) <span class="version-mark">v6.5.4 和 v7.3.0 新增</span>

- 默认值：`OFF`
- 可选值：`ON`，`OFF`
- 在某些场景下，当 `IndexJoin` 算子的 `Probe` 端包含 `Selection` 算子时，TiDB 会严重高估 `IndexScan` 的行数。这可能导致选择次优的查询计划而不是 `IndexJoin`。
- 为了缓解这个问题，TiDB 引入了一项改进。但由于可能存在查询计划回退风险，该改进默认是禁用的。
- 该变量控制是否启用上述改进。

### [`45132`](https://github.com/pingcap/tidb/issues/45132) <span class="version-mark">v7.4.0 新增</span>

- 默认值：`1000`
- 可选值：`[0, 2147483647]`
- 该变量设置优化器选择访问路径的启发式策略阈值。如果某个访问路径（如 `Index_A`）的估算行数远小于其他访问路径（默认为 `1000` 倍），优化器会跳过成本比较直接选择 `Index_A`。
- `0` 表示禁用该启发式策略。

### [`45798`](https://github.com/pingcap/tidb/issues/45798) <span class="version-mark">v7.5.0 新增</span>

- 默认值：`ON`
- 可选值：`ON`，`OFF`
- 该变量控制计划缓存是否允许缓存访问[生成列](/generated-columns.md)的执行计划。

### [`46177`](https://github.com/pingcap/tidb/issues/46177) <span class="version-mark">v6.5.6、v7.1.3 和 v7.5.0 新增</span>

- 默认值：`OFF`
- 可选值：`ON`，`OFF`
- 该变量控制优化器在找到非强制计划后是否继续探索强制计划。

### [`52869`](https://github.com/pingcap/tidb/issues/52869) <span class="version-mark">v8.1.0 新增</span>

- 默认值：`OFF`
- 可选值：`ON`，`OFF`
- 如[使用索引合并的 Explain 语句](/explain-index-merge.md#examples)中的**注意**所述，如果优化器可以为查询计划选择单索引扫描方法（而不是全表扫描），优化器将不会自动使用索引合并。
- 你可以通过启用此修复控制来移除这个限制。移除此限制可以让优化器在更多查询中自动选择索引合并，但可能会导致优化器忽略最优执行计划。因此，建议在移除此限制之前，对实际使用场景进行充分测试，以确保不会导致性能回退。

### [`56318`](https://github.com/pingcap/tidb/issues/56318)

> **注意：**
>
> 此功能仅适用于 [TiDB Cloud Serverless](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-serverless)。

- 默认值：`ON`
- 可选值：`ON`，`OFF`
- 该变量控制是否避免重复计算 `ORDER BY` 语句中使用的重表达式。
