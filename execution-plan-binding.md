---
title: Execution Plan Binding
summary: Learn about execution plan binding operations in TiDB.
category: reference
aliases: ['/docs/dev/reference/performance/execution-plan-bind/']
---

# Execution Plan Binding

The [Optimizer Hints](/optimizer-hints.md) document introduces how to select a specific execution plan using Hint. However, sometimes you need to interfere with execution selection without modifying SQL statements. Execution Plan Binding provides a set of functionalities to do this.

## Syntax

### Create binding

{{< copyable "sql" >}}

```sql
CREATE [GLOBAL | SESSION] BINDING FOR SelectStmt USING SelectStmt
```

This statement binds SQL execution plans at the GLOBAL or SESSION level. The default scope is SESSION. The bound SQL statement is parameterized and stored in the system table. When a SQL query is processed, as long as the parameterized SQL statement and a bound one in the system table are consistent and the system variable `tidb_use_plan_baselines` is set to `on` (the default value is `on`), the corresponding optimizer hint is available. If multiple execution plans are available, the optimizer chooses to bind the plan with the least cost.

When a SQL statement has bound execution plans in both GLOBAL and SESSION scopes, because the optimizer ignores the bound execution plan in the GLOBAL scope when it encounters the SESSION binding, the bound execution plan of this statement in the SESSION scope shields the execution plan in the GLOBAL scope.

For example:

```sql
--  Creates a GLOBAL binding and specifies using `sort merge join` in this binding.
create global binding for
    select * from t1, t2 where t1.id = t2.id
using
    select /*+ TIDB_SMJ(t1, t2) */ * from t1, t2 where t1.id = t2.id;

-- The execution plan of this SQL statement uses the `sort merge join` specified in the GLOBAL binding.
explain select * from t1, t2 where t1.id = t2.id;

-- Creates another SESSION binding and specifies using `hash join` in this binding.
create binding for
    select * from t1, t2 where t1.id = t2.id
using
    select /*+ TIDB_HJ(t1, t2) */ * from t1, t2 where t1.id = t2.id;

-- In the execution plan of this statement, `hash join` specified in the SESSION binding is used, instead of `sort merge join` specified in the GLOBAL binding.
explain select * from t1, t2 where t1.id = t2.id;
```

When the first `select` statement is being executed, the optimizer adds the `TIDB_SMJ(t1, t2)` hint to the statement through the binding in the GLOBAL scope. The top node of the execution plan in the `explain` result is MergeJoin. When the second `select` statement is being executed, the optimizer uses the binding in the SESSION scope instead of the binding in the GLOBAL scope and adds the `TIDB_HJ(t1, t2)` hint to the statement. The top node of the execution plan in the `explain` result is HashJoin.

`Parameterization` is a process that converts a constant in SQL to a variable parameter, with standardized processing on the spaces and line breaks in the SQL statement, for example,

{{< copyable "sql" >}}

```sql
select * from t where a >    1
-- parameterized:
select * from t where a > ？
```

> **Note:**
>
> The text must be the same before and after parameterization and hint removal for both the original SQL statement and the bound statement, or the binding will fail. Take the following examples:
>
> - This binding can be created successfully because the texts before and after parameterization and hint removal are the same: `select * from t where a > ?`
>
>     ```sql
>     CREATE BINDING FOR SELECT * FROM t WHERE a > 1 USING SELECT * FROM t use index  (idx) WHERE a > 2
>     ```
>
> - This binding will fail because the original SQL statement is processed as `select * from t where a > ?`, while the bound SQL statement is processed differently as `select * from t where b > ?`.
>
>     ```sql
>     CREATE BINDING FOR SELECT * FROM t WHERE a > 1 USING SELECT * FROM t use index(idx) WHERE b > 2
>     ```

### Remove binding

{{< copyable "sql" >}}

```sql
DROP [GLOBAL | SESSION] BINDING FOR SelectStmt
```

This statement removes a specified execution plan binding at the GLOBAL or SESSION level. The default scope is SESSION.

Generally, the binding in the SESSION scope is mainly used for test or in special situations. For a binding to take effect in all TiDB processes, you need to use the GLOBAL binding. A created SESSION binding shields the corresponding GLOBAL binding until the end of the SESSION, even if the SESSION binding is dropped before the session closes. In this case, no binding takes effect and the plan is selected by the optimizer.

The following example is based on the example in [create binding](#create-binding) in which the SESSION binding shields the GLOBAL binding:

```sql
-- Drops the binding created in the SESSION scope.
drop session binding for select * from t1, t2 where t1.id = t2.id;

-- Views the SQL execution plan again.
explain select * from t1,t2 where t1.id = t2.id;
```

In the example above, the dropped binding in the SESSION scope shields the corresponding binding in the GLOBAL scope. The optimizer does not add the `TIDB_SMJ(t1, t2)` hint to the statement. The top node of the execution plan in the `explain` result is not fixed to MergeJoin by this hint. Instead, the top node is independently selected by the optimizer according to the cost estimation.

### View binding

{{< copyable "sql" >}}

```sql
SHOW [GLOBAL | SESSION] BINDINGS [ShowLikeOrWhere]
```

This statement outputs the execution plan bindings at the GLOBAL or SESSION level. The default scope is SESSION. Currently `SHOW BINDINGS` outputs eight columns, as shown below:

| Column Name | Note |
| :-------- | :------------- |
| original_sql  |  Original SQL statement after parameterization |
| bind_sql | Bound SQL statement with hints |
| default_db | Default database |
| status | Status including Using, Deleted, and Invalid |
| create_time | Creating time |
| update_time | Updating time |
| charset | Character set |
| collation | Ordering rule |

### Automatically create binding

To enable automatic binding creation, set `tidb_capture_plan_baselines` to `on`. The default value is `off`.

> **Note:**
>
> Because the automatic binding creation function relies on [Statement Summary](/statement-summary-tables.md), make sure to enable Statement Summary before using automatic binding.

After automatic binding creation is enabled, the historical SQL statements in the Statement Summary are traversed every `bind-info-lease` (the default value is `3s`), and bindings are automatically created for SQL statements that appear at least twice.

### Automatically evolve binding

As data updates, the previously bound execution plan might no longer be optimal. The automatic binding evolution feature can optimize the bound execution plan. Use the following statement to enable automatic binding evolution:

{{< copyable "sql" >}}

```sql
set global tidb_evolve_plan_baselines = on;
```

The default value of `tidb_evolve_plan_baselines` is `off`.

> **Note:**
>
> The global variable does not take effect in the current session. It only takes effect in a newly created session. To enable automatic binding evolution in the current session, change the keyword `global` to `session`.

After the automatic binding evolution feature is enabled, if the optimal execution plan selected by the optimizer is not among the binding execution plans, the optimizer marks the plan as an execution plan that waits for verification. At every `bind-info-lease` (the default value is `3s`) interval, an execution plan to be verified is selected and compared with the binding execution plan that has the least cost in terms of the actual execution time. If the plan to be verified has shorter execution time, this plan is marked as a usable binding. The following example describes the process above.

Assume that table `t` is defined as follows:

{{< copyable "sql" >}}

```sql
create table t(a int, b int, key(a), key(b));
```

Perform the following query on table `t`:

{{< copyable "sql" >}}

```sql
select * from t where a < 100 and b < 100;
```

In the table defined above, few rows meet the `a < 100` condition. But for some reason, the optimizer mistakenly selects the full table scan instead of the optimal execution plan that uses index `a`. You can first use the following statement to create a binding:

{{< copyable "sql" >}}

```sql
create global binding for select * from t where a < 100 and b < 100 using select * from t use index(a) where a < 100 and b < 100;
```

When the query above is executed again, the optimizer selects index `a` (influenced by the binding created above) to reduce the query time.

Assuming that as insertions and deletions are performed on table `t`, an increasing number of rows meet the `a < 100` condition and a decreasing number of rows meet the `b < 100` condition. At this time, using index `a` under the binding might no longer be the optimal plan.

The binding evolution can address this kind of issues. When the optimizer recognizes data change in a table, it generates an execution plan for the query that uses index `b`. However, because the binding of the current plan exists, this query plan is not adopted and executed. Instead, this plan is stored in the backend evolution list. During the evolution process, if this plan is verified to have an obviously shorter execution time than that of the current execution plan that uses index `a`, index `b` is added into the available binding list. After this, when the query is executed again, the optimizer first generates the execution plan that uses index `b` and makes sure that this plan is in the binding list. Then the optimizer adopts and executes this plan to reduce the query time after data changes.

To reduce the impact that the automatic evolution has on clusters, use the following configurations:

- Set `tidb_evolve_plan_task_max_time` to limit the maximum execution time of each execution plan. The default value is `600s`.
- Set `tidb_evolve_plan_task_start_time` (`00:00 +0000` by default) and `tidb_evolve_plan_task_end_time` (`23:59 +0000` by default) to limit the time window.
