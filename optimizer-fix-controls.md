---
title: Optimizer Fix Controls
summary: 了解 Optimizer Fix Controls 以及如何使用 `tidb_opt_fix_control` 细粒度地控制 TiDB 优化器的行为。
---

# Optimizer Fix Controls

随着产品迭代演进，TiDB 优化器的行为会发生变化，进而生成更加合理的执行计划。但在某些特定场景下，新的行为可能会导致非预期结果。例如：

- 部分行为的效果和场景相关。有的行为改变，能在大多数场景下带来改进，但可能在极少数场景下导致回退。
- 有时，行为细节的变化和其导致的结果之间的关系十分复杂。即使是对某处行为细节的改进，也可能在整体上导致执行计划回退。

因此，TiDB 提供了 Optimizer Fix Controls 功能，允许用户通过设置一系列 Fix 控制 TiDB 优化器的行为细节。本文档介绍了 Optimizer Fix Controls 及其使用方法，并列举了当前 TiDB 支持调整的所有 Fix。

## `tidb_opt_fix_control` 介绍

从 TiDB v6.5.3 开始，提供了 [`tidb_opt_fix_control`](/system-variables.md#tidb_opt_fix_control-从-v653-版本开始引入) 系统变量来更细粒度地控制优化器的行为。

一个 Fix 是用于调整 TiDB 优化器中一处行为的控制项。它以一个数字编号表示，该数字编号对应一个 GitHub Issue，在 Issue 中会有对技术细节的描述。例如 Fix `44262` 对应 [Issue 44262](https://github.com/pingcap/tidb/issues/44262)。

`tidb_opt_fix_control` 支持设置多个 Fix，不同 Fix 之间使用逗号 (`,`) 分隔。格式形如 `"<#issue1>:<value1>,<#issue2>:<value2>,...,<#issueN>:<valueN>"`，其中 `<#issueN>` 代表 Fix 编号。例如：

```sql
SET SESSION tidb_opt_fix_control = '44262:ON,44389:ON';
```

## Optimizer Fix Controls 参考

### [`44262`](https://github.com/pingcap/tidb/issues/44262) <span class="version-mark">从 v6.5.3 版本开始引入</span>

- 默认值：`OFF`
- 可选值：`ON`、`OFF`
- 是否允许在缺少 [GlobalStats](/statistics.md#动态裁剪模式下的分区表统计信息) 的情况下使用[动态裁剪模式](/partitioned-table.md#动态裁剪模式)访问分区表。

### [`44389`](https://github.com/pingcap/tidb/issues/44389) <span class="version-mark">从 v6.5.3 版本开始引入</span>

- 默认值：`OFF`
- 可选值：`ON`、`OFF`
- 对形如 `c = 10 and (a = 'xx' or (a = 'kk' and b = 1))` 的过滤条件，是否尝试为 `IndexRangeScan` 更加完整地构造扫描范围，即 `range`。

### [`44830`](https://github.com/pingcap/tidb/issues/44830) <span class="version-mark">从 v6.5.7 版本开始引入</span>

- 默认值：`OFF`
- 可选值：`ON`、`OFF`
- 此开关控制是否让 Plan Cache 对在物理优化阶段形成的 `PointGet` 计划进行缓存。

### [`44855`](https://github.com/pingcap/tidb/issues/44855) <span class="version-mark">从 v6.5.4 版本开始引入</span>

- 默认值：`OFF`
- 可选值：`ON`、`OFF`
- 在某些场景下，当 `IndexJoin` 算子的 `Probe` 端包含 `Selection` 算子时，TiDB 会严重高估 `IndexScan` 的行数，导致在 `IndexJoin` 更好的时候选择了其它的执行计划。
- TiDB 已经引入了缓解这类问题的改进逻辑。但是由于潜在的计划回退风险，该改进并没有被默认启用。
- 此开关控制是否启用这个改进。

### [`46177`](https://github.com/pingcap/tidb/issues/46177) <span class="version-mark">从 v6.5.6 版本开始引入</span>

- 默认值：`OFF`
- 可选值：`ON`、`OFF`
- 此开关控制优化器在查询优化的过程中，找到非强制执行计划后，是否继续查找强制执行计划进行查询优化。
