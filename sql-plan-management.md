---
title: SQL Plan Management (SPM)
summary: Learn about SQL Plan Management in TiDB.
aliases: ['/docs/dev/sql-plan-management/','/docs/dev/reference/performance/execution-plan-bind/','/docs/dev/execution-plan-binding/']
---

# SQL Plan Management (SPM)

SQL Plan Management is a set of functions that execute SQL bindings to manually interfere with SQL execution plans. These functions include SQL binding, baseline capturing, and baseline evolution.

## SQL binding

An SQL binding is the basis of SPM. The [Optimizer Hints](/optimizer-hints.md) document introduces how to select a specific execution plan using hints. However, sometimes you need to interfere with execution selection without modifying SQL statements. With SQL bindings, you can select a specified execution plan without modifying SQL statements.

### Create a binding

{{< copyable "sql" >}}

```sql
CREATE [GLOBAL | SESSION] BINDING FOR BindableStmt USING BindableStmt
```

This statement binds SQL execution plans at the GLOBAL or SESSION level. Currently, supported bindable SQL statements (BindableStmt) in TiDB include `SELECT`, `DELETE`, `UPDATE`, and `INSERT` / `REPLACE` with `SELECT` subqueries.

Specifically, two types of these statements cannot be bound to execution plans due to syntax conflicts. See the following examples:

```sql
-- Type one: Statements that get the Cartesian product by using the `join` keyword and not specifying the associated columns with the `using` keyword.
create global binding for
    select * from t t1 join t t2
using
    select * from t t1 join t t2;

-- Type two: `DELETE` statements that contain the `using` keyword.
create global binding for
    delete from t1 using t1 join t2 on t1.a = t2.a
using
    delete from t1 using t1 join t2 on t1.a = t2.a;
```

You can bypass syntax conflicts by using equivalent statements. For example, you can rewrite the above statements in the following ways:

```sql
-- First rewrite of type one statements: Add a `using` clause for the `join` keyword.
create global binding for
    select * from t t1 join t t2 using (a)
using
    select * from t t1 join t t2 using (a);

-- Second rewrite of type one statements: Delete the `join` keyword.
create global binding for
    select * from t t1, t t2
using
    select * from t t1, t t2;

-- Rewrite of type two statements: Remove the `using` keyword from the `delete` statement.
create global binding for
    delete t1 from t1 join t2 on t1.a = t2.a
using
    delete t1 from t1 join t2 on t1.a = t2.a;
```

> **Note:**
>
> When creating execution plan bindings for `INSERT` / `REPLACE` statements with `SELECT` subqueries, you need to specify the optimizer hints you want to bind in the `SELECT` subquery, not after the `INSERT` / `REPLACE` keyword. Otherwise, the optimizer hints do not take effect as intended.

Here are two examples:

```sql
-- The hint takes effect in the following statement.
create global binding for
    insert into t1 select * from t2 where a > 1 and b = 1
using
    insert into t1 select /*+ use_index(@sel_1 t2, a) */ * from t2 where a > 1 and b = 1;

-- The hint cannot take effect in the following statement.
create global binding for
    insert into t1 select * from t2 where a > 1 and b = 1
using
    insert /*+ use_index(@sel_1 t2, a) */ into t1 select * from t2 where a > 1 and b = 1;
```

If you do not specify the scope when creating an execution plan binding, the default scope is SESSION. The TiDB optimizer normalizes bound SQL statements and stores them in the system table. When processing SQL queries, if a normalized statement matches one of the bound SQL statements in the system table and the system variable `tidb_use_plan_baselines` is set to `on` (the default value is `on`), TiDB then uses the corresponding optimizer hint for this statement. If there are multiple matchable execution plans, the optimizer chooses the least costly one to bind.

`Normalization` is a process that converts a constant in an SQL statement to a variable parameter and explicitly specifies the database for tables referenced in the query, with standardized processing on the spaces and line breaks in the SQL statement. See the following example:

```sql
select * from t where a >    1
-- Normalized:
select * from test . t where a > ?
```

When a SQL statement has bound execution plans in both GLOBAL and SESSION scopes, because the optimizer ignores the bound execution plan in the GLOBAL scope when it encounters the SESSION binding, the bound execution plan of this statement in the SESSION scope shields the execution plan in the GLOBAL scope.

For example:

```sql
--  Creates a GLOBAL binding and specifies using `sort merge join` in this binding.
create global binding for
    select * from t1, t2 where t1.id = t2.id
using
    select /*+ merge_join(t1, t2) */ * from t1, t2 where t1.id = t2.id;

-- The execution plan of this SQL statement uses the `sort merge join` specified in the GLOBAL binding.
explain select * from t1, t2 where t1.id = t2.id;

-- Creates another SESSION binding and specifies using `hash join` in this binding.
create binding for
    select * from t1, t2 where t1.id = t2.id
using
    select /*+ hash_join(t1, t2) */ * from t1, t2 where t1.id = t2.id;

-- In the execution plan of this statement, `hash join` specified in the SESSION binding is used, instead of `sort merge join` specified in the GLOBAL binding.
explain select * from t1, t2 where t1.id = t2.id;
```

When the first `select` statement is being executed, the optimizer adds the `sm_join(t1, t2)` hint to the statement through the binding in the GLOBAL scope. The top node of the execution plan in the `explain` result is MergeJoin. When the second `select` statement is being executed, the optimizer uses the binding in the SESSION scope instead of the binding in the GLOBAL scope and adds the `hash_join(t1, t2)` hint to the statement. The top node of the execution plan in the `explain` result is HashJoin.

Each standardized SQL statement can have only one binding created using `CREATE BINDING` at a time. When multiple bindings are created for the same standardized SQL statement, the last created binding is retained, and all previous bindings (created and evolved) are marked as deleted. But session bindings and global bindings can coexist and are not affected by this logic.

In addition, when you create a binding, TiDB requires that the session is in a database context, which means that a database is specified when the client is connected or `use ${database}` is executed.

The original SQL statement and the bound statement must have the same text after normalization and hint removal, or the binding will fail. Take the following examples:

- This binding can be created successfully because the texts before and after parameterization and hint removal are the same: `select * from test . t where a > ?`

     ```sql
     CREATE BINDING FOR SELECT * FROM t WHERE a > 1 USING SELECT * FROM t use index  (idx) WHERE a > 2
     ```

- This binding will fail because the original SQL statement is processed as `select * from test . t where a > ?`, while the bound SQL statement is processed differently as `select * from test . t where b > ?`.

     ```sql
     CREATE BINDING FOR SELECT * FROM t WHERE a > 1 USING SELECT * FROM t use index(idx) WHERE b > 2
     ```

> **Note:**
>
> For `PREPARE` / `EXECUTE` statements and for queries executed with binary protocols, you need to create execution plan bindings for the real query statements, not for the `PREPARE` / `EXECUTE` statements.

### Remove binding

{{< copyable "sql" >}}

```sql
DROP [GLOBAL | SESSION] BINDING FOR BindableStmt;
```

This statement removes a specified execution plan binding at the GLOBAL or SESSION level. The default scope is SESSION.

Generally, the binding in the SESSION scope is mainly used for test or in special situations. For a binding to take effect in all TiDB processes, you need to use the GLOBAL binding. A created SESSION binding shields the corresponding GLOBAL binding until the end of the SESSION, even if the SESSION binding is dropped before the session closes. In this case, no binding takes effect and the plan is selected by the optimizer.

The following example is based on the example in [create binding](#create-a-binding) in which the SESSION binding shields the GLOBAL binding:

```sql
-- Drops the binding created in the SESSION scope.
drop session binding for select * from t1, t2 where t1.id = t2.id;

-- Views the SQL execution plan again.
explain select * from t1,t2 where t1.id = t2.id;
```

In the example above, the dropped binding in the SESSION scope shields the corresponding binding in the GLOBAL scope. The optimizer does not add the `sm_join(t1, t2)` hint to the statement. The top node of the execution plan in the `explain` result is not fixed to MergeJoin by this hint. Instead, the top node is independently selected by the optimizer according to the cost estimation.

> **Note:**
>
> Executing `DROP GLOBAL BINDING` drops the binding in the current tidb-server instance cache and changes the status of the corresponding row in the system table to 'deleted'. This statement does not directly delete the records in the system table, because other tidb-server instances need to read the 'deleted' status to drop the corresponding binding in their cache. For the records in these system tables with the status of 'deleted', at every 100 `bind-info-lease` (the default value is `3s`, and `300s` in total) interval, the background thread triggers an operation of reclaiming and clearing on the bindings of `update_time` before 10 `bind-info-lease` (to ensure that all tidb-server instances have read the 'deleted' status and updated the cache).

### View binding

{{< copyable "sql" >}}

```sql
SHOW [GLOBAL | SESSION] BINDINGS [ShowLikeOrWhere]
```

This statement outputs the execution plan bindings at the GLOBAL or SESSION level according to the order of binding update time from the latest to earliest. The default scope is SESSION. Currently `SHOW BINDINGS` outputs eight columns, as shown below:

| Column Name | Note |
| :-------- | :------------- |
| original_sql  |  Original SQL statement after parameterization |
| bind_sql | Bound SQL statement with hints |
| default_db | Default database |
| status | Status including Using, Deleted, Invalid, Rejected, and Pending verification|
| create_time | Creating time |
| update_time | Updating time |
| charset | Character set |
| collation | Ordering rule |
| source | The way in which a binding is created, including `manual` (created by the `create [global] binding` SQL statement), `capture` (captured automatically by TiDB), and `evolve` (evolved automatically by TiDB) |

### Troubleshoot binding

{{< copyable "sql" >}}

```sql
SELECT [SESSION] @@last_plan_from_binding;
```

This statement uses the system variable [`last_plan_from_binding`](/system-variables.md#last_plan_from_binding-new-in-v40) to show whether the execution plan used by the last executed statement is from the binding.

In addition, when you use the `explain format = 'verbose'` statement to view the query plan of a SQL statement, if the SQL statement uses binding, the `explain` statement will return a warning. In this situation, you can check the warning message to learn which binding is used in the SQL statement.

```sql
-- Create a global binding.

create global binding for
    select * from t
using
    select * from t;

-- Use the `explain format = 'verbose'` statement to check the SQL execution plan. Check the warning message to view the binding used in the query.

explain format = 'verbose' select * from t;
show warnings;
```

## Baseline capturing

To enable baseline capturing, set `tidb_capture_plan_baselines` to `on`. The default value is `off`.

> **Note:**
>
> Because the automatic binding creation function relies on [Statement Summary](/statement-summary-tables.md), make sure to enable Statement Summary before using automatic binding.

After automatic binding creation is enabled, the historical SQL statements in the Statement Summary are traversed every `bind-info-lease` (the default value is `3s`), and a binding is automatically created for SQL statements that appear at least twice. For these SQL statements, TiDB automatically binds the execution plan recorded in Statement Summary.

However, TiDB does not automatically capture bindings for the following types of SQL statements:

- `EXPLAIN` and `EXPLAIN ANALYZE` statements.
- SQL statements executed internally in TiDB, such as `SELECT` queries used for automatically loading statistical information.
- SQL statements that are bound to a manually created execution plan.

For `PREPARE` / `EXECUTE` statements and for queries executed with binary protocols, TiDB automatically captures bindings for the real query statements, not for the `PREPARE` / `EXECUTE` statements.

> **Note:**
>
> Because TiDB has some embedded SQL statements to ensure the correctness of some features, baseline capturing by default automatically shields these SQL statements.

## Baseline evolution

Baseline evolution is an important feature of SPM introduced in TiDB v4.0.

As data updates, the previously bound execution plan might no longer be optimal. The baseline evolution feature can automatically optimize the bound execution plan.

In addition, baseline evolution, to a certain extent, can also avoid the jitter brought to the execution plan caused by the change of statistical information.

### Usage

Use the following statement to enable automatic binding evolution:

{{< copyable "sql" >}}

```sql
set global tidb_evolve_plan_baselines = on;
```

The default value of `tidb_evolve_plan_baselines` is `off`.

> **Warning:**
>
> + Baseline evolution is an experimental feature. Unknown risks might exist. It is **NOT** recommended that you use it in the production environment.
> + This variable is forcibly set to `off` until the baseline evolution feature becomes generally available (GA). If you try to enable this feature, an error is returned. If you have already used this feature in a production environment, disable it as soon as possible. If you find that the binding status is not as expected, contact PingCAP's technical support for help.

After the automatic binding evolution feature is enabled, if the optimal execution plan selected by the optimizer is not among the binding execution plans, the optimizer marks the plan as an execution plan that waits for verification. At every `bind-info-lease` (the default value is `3s`) interval, an execution plan to be verified is selected and compared with the binding execution plan that has the least cost in terms of the actual execution time. If the plan to be verified has shorter execution time (the current criterion for the comparison is that the execution time of the plan to be verified is no longer than 2/3 that of the binding execution plan), this plan is marked as a usable binding. The following example describes the process above.

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

- Set `tidb_evolve_plan_task_max_time` to limit the maximum execution time of each execution plan. The default value is `600s`. In the actual verification process, the maximum execution time is also limited to no more than twice the time of the verified execution plan.
- Set `tidb_evolve_plan_task_start_time` (`00:00 +0000` by default) and `tidb_evolve_plan_task_end_time` (`23:59 +0000` by default) to limit the time window.

### Notes

Because the baseline evolution automatically creates a new binding, when the query environment changes, the automatically created binding might have multiple behavior choices. Pay attention to the following notes:

+ Baseline evolution only evolves standardized SQL statements that have at least one global binding.

+ Because creating a new binding deletes all previous bindings (for a standardized SQL statement), the automatically evolved binding will be deleted after manually creating a new binding.

+ All hints related to the calculation process are retained during the evolution. These hints are as follows:

    | Hint | Description            |
    | :-------- | :------------- |
    | `memory_quota` | The maximum memory that can be used for a query. |
    | `use_toja` | Whether the optimizer transforms sub-queries to Join. |
    | `use_cascades` | Whether to use the cascades optimizer. |
    | `no_index_merge` | Whether the optimizer uses Index Merge as an option for reading tables. |
    | `read_consistent_replica` | Whether to forcibly enable Follower Read when reading tables. |
    | `max_execution_time` | The longest duration for a query. |

+ `read_from_storage` is a special hint in that it specifies whether to read data from TiKV or from TiFlash when reading tables. Because TiDB provides isolation reads, when the isolation condition changes, this hint has a great influence on the evolved execution plan. Therefore, when this hint exists in the initially created binding, TiDB ignores all its evolved bindings.

## Upgrade checklist

During cluster upgrade, SQL Plan Management (SPM) might cause compatibility issues and make the upgrade fail. To ensure a successful upgrade, you need to include the following list for upgrade precheck:

* When you upgrade from a version earlier than v5.2.0 (that is, v4.0, v5.0, and v5.1) to the current version, make sure that `tidb_evolve_plan_baselines` is disabled before the upgrade. To disable this variable, perform the following steps. 

    {{< copyable "sql" >}}

    ```sql
    -- Check whether `tidb_evolve_plan_baselines` is disabled in the earlier version. 
  
    select @@global.tidb_evolve_plan_baselines;
  
    -- If `tidb_evolve_plan_baselines` is still enabled, disable it. 
  
    set global tidb_evolve_plan_baselines = off;
    ```

* Before you upgrade from v4.0 to the current version, you need to check whether the syntax of all queries corresponding to the available SQL bindings is correct in the new version. If any syntax errors exist, delete the corresponding SQL binding. To do that, perform the following steps.

    {{< copyable "sql" >}}

    ```sql
    -- Check the query corresponding to the available SQL binding in the version to be upgraded.
  
    select bind_sql from mysql.bind_info where status = 'using';
  
    -- Verify the result from the above SQL query in the test environment of the new version. 
  
    bind_sql_0;
    bind_sql_1;
    ...
  
    -- In the case of a syntax error (ERROR 1064 (42000): You have an error in your SQL syntax), delete the corresponding binding. 
    -- For any other errors (for example, tables are not found), it means that the syntax is compatible. No other operation is needed. 
    ```
