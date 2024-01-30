---
title: Control Execution Plan
summary: This chapter introduces methods to control the generation of execution plans in TiDB. It includes using hints, SQL plan management, and the blocklist of optimization rules. Additionally, system variables and the `tidb_opt_fix_control` variable can be modified to control the execution plan. These methods help prevent performance regression caused by behavior changes in the optimizer after cluster upgrades.
---

# Control Execution Plan

The first two chapters of SQL Tuning introduce how to understand TiDB's execution plan and how TiDB generates an execution plan. This chapter introduces what methods can be used to control the generation of the execution plan when you determine the problems with the execution plan. This chapter mainly includes the following three aspects:

- In [Optimizer Hints](/optimizer-hints.md), you will learn how to use hints to guide TiDB to generate an execution plan.
- But hints change the SQL statement intrusively. In some scenarios, hints cannot be simply inserted. In [SQL Plan Management](/sql-plan-management.md), you will know how TiDB uses another syntax to non-intrusively control the generation of execution plans, and the methods of automatic execution plan evolution in the background. This method helps address issues such as execution plan instability caused by version upgrades and cluster performance degradation.
- Finally, you will learn how to use the blocklist in [Blocklist of Optimization Rules and Expression Pushdown](/blocklist-control-plan.md).

<CustomContent platform="tidb">

Besides the preceding methods, the execution plan is also affected by some system variables. By modifying these variables at the system level or session level, you can control the generation of the execution plan. Starting from v6.5.3 and v7.1.0, TiDB introduces a relatively special variable [`tidb_opt_fix_control`](/system-variables.md#tidb_opt_fix_control-new-in-v653-and-v710). This variable can accept multiple control items to control the behavior of the optimizer in a more fine-grained way, to prevent performance regression caused by behavior changes in the optimizer after cluster upgrade. Refer to [Optimizer Fix Controls](/optimizer-fix-controls.md) for a more detailed introduction.

</CustomContent>

<CustomContent platform="tidb-cloud">

Besides the preceding methods, the execution plan is also affected by some system variables. By modifying these variables at the system level or session level, you can control the generation of the execution plan. Starting from v6.5.3 and v7.1.0, TiDB introduces a relatively special variable [`tidb_opt_fix_control`](/system-variables.md#tidb_opt_fix_control-new-in-v653-and-v710). This variable can accept multiple control items to control the behavior of the optimizer in a more fine-grained way, to prevent performance regression caused by behavior changes in the optimizer after cluster upgrade. Refer to [Optimizer Fix Controls](https://docs.pingcap.com/tidb/v7.2/optimizer-fix-controls) for a more detailed introduction.

</CustomContent>
