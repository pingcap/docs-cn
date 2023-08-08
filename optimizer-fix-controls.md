---
title: Optimizer Fix Controls
summary: Learn about the Optimizer Fix Controls feature and how to use `tidb_opt_fix_control` to control the TiDB optimizer in a more fine-grained way.
---

# Optimizer Fix Controls

As the product evolves iteratively, the behavior of the TiDB optimizer changes, which in turn generates more reasonable execution plans. However, in some particular scenarios, the new behavior might lead to unexpected results. For example:

- The effect of some behaviors relies on a specific scenario. Changes that bring improvements to most scenarios might cause regressions to others.
- Sometimes, the relationship between changes in the behavior details and their consequences is very complicated. An improvement in a certain behavior might cause overall regression.

Therefore, TiDB provides the Optimizer Fix Controls feature that allows you to make fine-grained control of TiDB optimizer behaviors by setting values for a group of fixes. This document describes the Optimizer Fix Controls feature and how to use them, and lists all the fixes that TiDB currently supports for Optimizer Fix Controls.

## Introduction to `tidb_opt_fix_control`

Starting from v7.1.0, TiDB provides the [`tidb_opt_fix_control`](/system-variables.md#tidb_opt_fix_control-new-in-v710) system variable to control the behavior of the optimizer in a more fine-grained way.

Each fix is a control item used to adjust the behavior in the TiDB optimizer for one particular purpose. It is denoted by a number that corresponds to a GitHub Issue that contains the technical details of the behavior change. For example, for fix `44262`, you can review what it controls in [Issue 44262](https://github.com/pingcap/tidb/issues/44262).

The [`tidb_opt_fix_control`](/system-variables.md#tidb_opt_fix_control-new-in-v710) system variable accepts multiple fixes as one value, separated by commas (`,`). The format is `"<#issue1>:<value1>,<#issue2>:<value2>,...,<#issueN>:<valueN>"`, where `<#issueN>` is the fix number. For example:

```sql
SET SESSION tidb_opt_fix_control = '44262:ON,44389:ON';
```

## Optimizer Fix Controls reference

### [`44262`](https://github.com/pingcap/tidb/issues/44262) <span class="version-mark">New in v7.2.0</span>

- Default value: `OFF`
- Possible values: `ON`, `OFF`
- This variable controls whether to allow the use of [Dynamic pruning mode](/partitioned-table.md#dynamic-pruning-mode) to access the partitioned table when the [GlobalStats](/statistics.md#collect-statistics-of-partitioned-tables-in-dynamic-pruning-mode) are missing.

### [`44389`](https://github.com/pingcap/tidb/issues/44389) <span class="version-mark">New in v7.2.0</span>

- Default value: `OFF`
- Possible values: `ON`, `OFF`
- For filters such as `c = 10 and (a = 'xx' or (a = 'kk' and b = 1))`, this variable controls whether to try to build more comprehensive scan ranges for `IndexRangeScan`.

### [`44823`](https://github.com/pingcap/tidb/issues/44823) <span class="version-mark">New in v7.3.0</span>

- Default value: `200`
- Possible values: `[0, 2147483647]`
- To save memory, Plan Cache does not cache queries with parameters exceeding the specified number of this variable. `0` means no limit.

### [`44830`](https://github.com/pingcap/tidb/issues/44830) <span class="version-mark">New in v7.3.0</span>

- Default value: `OFF`
- Possible values: `ON`, `OFF`
- This variable controls whether Plan Cache is allowed to cache execution plans with the `PointGet` operator generated during physical optimization.

### [`44855`](https://github.com/pingcap/tidb/issues/44855) <span class="version-mark">New in v7.3.0</span>

- Default value: `OFF`
- Possible values: `ON`, `OFF`
- In some scenarios, when the `Probe` side of an `IndexJoin` operator contains a `Selection` operator, TiDB severely overestimates the row count of `IndexScan`. This might cause suboptimal query plans to be selected instead of `IndexJoin`.
- To mitigate this issue, TiDB has introduced an improvement. However, due to potential query plan fallback risks, this improvement is disabled by default.
- This variable controls whether to enable the preceding improvement.
