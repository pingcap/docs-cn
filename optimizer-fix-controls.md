---
title: Optimizer Fix Controls
summary: 了解 Optimizer Fix Controls 以及如何使用 tidb_opt_fix_control 细粒度地控制 TiDB 优化器的行为
aliases: ['/docs-cn/dev/optimizer-fix-controls/']
---

# Optimizer Fix Controls

TiDB 优化器的实现包含很多行为细节。随着产品演进，这些细节往往会发生变化。通常，这些变化都是优化器的改进，但有时仍会有导致执行计划回退等非预期情况的风险：

- 对于某些实现细节，不同的使用场景更适合不同的行为。
- 有时，行为细节的变化和其导致的结果之间的关系十分复杂。即使是对某处行为细节的改进，也可能在整体上导致执行计划回退。

因此我们提供了 [`tidb_opt_fix_control`](/system-variables.md#tidb_opt_fix_control-从-v710-版本开始引入) 系统变量来更细粒度地控制优化器的行为。

一个 Fix 通常以一个数字编号表示，这个数字编号通常对应一个 GitHub Issue，在 Issue 中会有对技术细节的描述。例如 Fix `44262` 对应 [Issue 44262](https://github.com/pingcap/tidb/issues/44262)。

该变量支持设置多个 Fix，不同 Fix 之间使用逗号 (`,`) 分隔。格式形如 `"<#issue1>:<value1>,<#issue2>:<value2>,...,<#issueN>:<valueN>"`，其中 `<#issueN>` 代表 Fix 编号。例如：

```sql
SET SESSION tidb_opt_fix_control = '44262:ON,44389:ON';
```

## Optimizer Fix Controls 参考

### [`44262`](https://github.com/pingcap/tidb/issues/44262) <span class="version-mark">从 v7.1.1 版本开始引入</span>

- 默认值：`OFF`
- 可选值：`ON`、`OFF`
- 是否允许在缺少 [GlobalStats](/statistics.md#动态裁剪模式下的分区表统计信息) 的情况下使用[动态裁剪模式](/partitioned-table.md#动态裁剪模式)访问分区表。

### [`44389`](https://github.com/pingcap/tidb/issues/44389) <span class="version-mark">从 v7.1.1 版本开始引入</span>

- 默认值：`OFF`
- 可选值：`ON`、`OFF`
- 对形如 `c = 10 and (a = 'xx' or (a = 'kk' and b = 1)` 的过滤条件，是否尝试为 `IndexRangeScan` 更加完整地构造扫描范围，即 `range`。
