---
title: 控制执行计划
summary: 本章介绍在 TiDB 中控制执行计划生成的方法。包括使用 Hints、SQL 计划管理和优化规则黑名单。此外，还可以通过修改系统变量和 `tidb_opt_fix_control` 变量来控制执行计划。这些方法有助于防止集群升级后优化器行为变化导致的性能回退。
---

# 控制执行计划

SQL 调优的前两章介绍了如何理解 TiDB 的执行计划以及 TiDB 如何生成执行计划。本章介绍当你确定执行计划存在问题时，可以使用哪些方法来控制执行计划的生成。本章主要包括以下三个方面：

- 在[优化器 Hints](/optimizer-hints.md)中，你将学习如何使用 hints 来指导 TiDB 生成执行计划。
- 但是 hints 会对 SQL 语句产生侵入性修改。在某些场景下，无法简单地插入 hints。在 [SQL 计划管理](/sql-plan-management.md)中，你将了解 TiDB 如何使用另一种语法来非侵入式地控制执行计划的生成，以及后台自动执行计划演进的方法。这种方法有助于解决版本升级导致的执行计划不稳定和集群性能下降等问题。
- 最后，你将学习如何使用[优化规则和表达式下推的黑名单](/blocklist-control-plan.md)。

<CustomContent platform="tidb">

除了上述方法外，执行计划还受一些系统变量的影响。通过在系统级别或会话级别修改这些变量，可以控制执行计划的生成。从 v6.5.3 和 v7.1.0 版本开始，TiDB 引入了一个相对特殊的变量 [`tidb_opt_fix_control`](/system-variables.md#tidb_opt_fix_control-new-in-v653-and-v710)。这个变量可以接受多个控制项，以更细粒度的方式控制优化器的行为，防止集群升级后优化器行为变化导致的性能回退。更详细的介绍请参考[优化器修复控制](/optimizer-fix-controls.md)。

</CustomContent>

<CustomContent platform="tidb-cloud">

除了上述方法外，执行计划还受一些系统变量的影响。通过在系统级别或会话级别修改这些变量，可以控制执行计划的生成。从 v6.5.3 和 v7.1.0 版本开始，TiDB 引入了一个相对特殊的变量 [`tidb_opt_fix_control`](/system-variables.md#tidb_opt_fix_control-new-in-v653-and-v710)。这个变量可以接受多个控制项，以更细粒度的方式控制优化器的行为，防止集群升级后优化器行为变化导致的性能回退。更详细的介绍请参考[优化器修复控制](https://docs.pingcap.com/tidb/v7.2/optimizer-fix-controls)。

</CustomContent>
