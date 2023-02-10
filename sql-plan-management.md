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

You can create a binding for a SQL statement according to a SQL statement or a historical execution plan.

#### Create a binding according to a SQL statement

{{< copyable "sql" >}}

```sql
CREATE [GLOBAL | SESSION] BINDING FOR BindableStmt USING BindableStmt
```

This statement binds SQL execution plans at the GLOBAL or SESSION level. Currently, supported bindable SQL statements (BindableStmt) in TiDB include `SELECT`, `DELETE`, `UPDATE`, and `INSERT` / `REPLACE` with `SELECT` subqueries.

> **Note:**
>
> Bindings have higher priority over manually added hints. Therefore, when you execute a statement containing a hint while a corresponding binding is present, the hint controlling the behavior of the optimizer does not take effect. However, other types of hints are still effective.

Specifically, two types of these statements cannot be bound to execution plans due to syntax conflicts. See the following examples:

```sql
-- Type one: Statements that get the Cartesian product by using the `JOIN` keyword and not specifying the associated columns with the `USING` keyword.
CREATE GLOBAL BINDING for
    SELECT * FROM t t1 JOIN t t2
USING
    SELECT * FROM t t1 JOIN t t2;

-- Type two: `DELETE` statements that contain the `USING` keyword.
CREATE GLOBAL BINDING for
    DELETE FROM t1 USING t1 JOIN t2 ON t1.a = t2.a
USING
    DELETE FROM t1 USING t1 JOIN t2 ON t1.a = t2.a;
```

You can bypass syntax conflicts by using equivalent statements. For example, you can rewrite the above statements in the following ways:

```sql
-- First rewrite of type one statements: Add a `USING` clause for the `JOIN` keyword.
CREATE GLOBAL BINDING for
    SELECT * FROM t t1 JOIN t t2 USING (a)
USING
    SELECT * FROM t t1 JOIN t t2 USING (a);

-- Second rewrite of type one statements: Delete the `JOIN` keyword.
CREATE GLOBAL BINDING for
    SELECT * FROM t t1, t t2
USING
    SELECT * FROM t t1, t t2;

-- Rewrite of type two statements: Remove the `USING` keyword from the `delete` statement.
CREATE GLOBAL BINDING for
    DELETE t1 FROM t1 JOIN t2 ON t1.a = t2.a
using
    DELETE t1 FROM t1 JOIN t2 ON t1.a = t2.a;
```

> **Note:**
>
> When creating execution plan bindings for `INSERT` / `REPLACE` statements with `SELECT` subqueries, you need to specify the optimizer hints you want to bind in the `SELECT` subquery, not after the `INSERT` / `REPLACE` keyword. Otherwise, the optimizer hints do not take effect as intended.

Here are two examples:

```sql
-- The hint takes effect in the following statement.
CREATE GLOBAL BINDING for
    INSERT INTO t1 SELECT * FROM t2 WHERE a > 1 AND b = 1
using
    INSERT INTO t1 SELECT /*+ use_index(@sel_1 t2, a) */ * FROM t2 WHERE a > 1 AND b = 1;

-- The hint cannot take effect in the following statement.
CREATE GLOBAL BINDING for
    INSERT INTO t1 SELECT * FROM t2 WHERE a > 1 AND b = 1
using
    INSERT /*+ use_index(@sel_1 t2, a) */ INTO t1 SELECT * FROM t2 WHERE a > 1 AND b = 1;
```

If you do not specify the scope when creating an execution plan binding, the default scope is SESSION. The TiDB optimizer normalizes bound SQL statements and stores them in the system table. When processing SQL queries, if a normalized statement matches one of the bound SQL statements in the system table and the system variable `tidb_use_plan_baselines` is set to `on` (the default value is `on`), TiDB then uses the corresponding optimizer hint for this statement. If there are multiple matchable execution plans, the optimizer chooses the least costly one to bind.

`Normalization` is a process that converts a constant in an SQL statement to a variable parameter and explicitly specifies the database for tables referenced in the query, with standardized processing on the spaces and line breaks in the SQL statement. See the following example:

```sql
SELECT * FROM t WHERE a >    1
-- After normalization, the above statement is as follows:
SELECT * FROM test . t WHERE a > ?
```

> **Note:**
>
> Multiple constants joined by commas `,` are normalized as `...` instead of `?`.
>
> For example:
>
> ```sql
> SELECT * FROM t limit 10
> SELECT * FROM t limit 10, 20
> SELECT * FROM t WHERE a IN (1)
> SELECT * FROM t WHERE a IN (1,2,3)
> -- After normalization, the above statements are as follows:
> SELECT * FROM test . t limit ?
> SELECT * FROM test . t limit ...
> SELECT * FROM test . t WHERE a IN ( ? )
> SELECT * FROM test . t WHERE a IN ( ... )
> ```
>
> When bindings are created, TiDB treats SQL statements that contain a single constant and SQL statements that contain multiple constants joined by commas differently. Therefore, you need to create bindings for the two SQL types separately.

When a SQL statement has bound execution plans in both GLOBAL and SESSION scopes, because the optimizer ignores the bound execution plan in the GLOBAL scope when it encounters the SESSION binding, the bound execution plan of this statement in the SESSION scope shields the execution plan in the GLOBAL scope.

For example:

```sql
--  Creates a GLOBAL binding and specifies using `sort merge join` in this binding.
CREATE GLOBAL BINDING for
    SELECT * FROM t1, t2 WHERE t1.id = t2.id
USING
    SELECT /*+ merge_join(t1, t2) */ * FROM t1, t2 WHERE t1.id = t2.id;

-- The execution plan of this SQL statement uses the `sort merge join` specified in the GLOBAL binding.
explain SELECT * FROM t1, t2 WHERE t1.id = t2.id;

-- Creates another SESSION binding and specifies using `hash join` in this binding.
CREATE BINDING for
    SELECT * FROM t1, t2 WHERE t1.id = t2.id
USING
    SELECT /*+ hash_join(t1, t2) */ * FROM t1, t2 WHERE t1.id = t2.id;

-- In the execution plan of this statement, `hash join` specified in the SESSION binding is used, instead of `sort merge join` specified in the GLOBAL binding.
explain SELECT * FROM t1, t2 WHERE t1.id = t2.id;
```

When the first `SELECT` statement is being executed, the optimizer adds the `sm_join(t1, t2)` hint to the statement through the binding in the GLOBAL scope. The top node of the execution plan in the `explain` result is MergeJoin. When the second `SELECT` statement is being executed, the optimizer uses the binding in the SESSION scope instead of the binding in the GLOBAL scope and adds the `hash_join(t1, t2)` hint to the statement. The top node of the execution plan in the `explain` result is HashJoin.

Each standardized SQL statement can have only one binding created using `CREATE BINDING` at a time. When multiple bindings are created for the same standardized SQL statement, the last created binding is retained, and all previous bindings (created and evolved) are marked as deleted. But session bindings and global bindings can coexist and are not affected by this logic.

In addition, when you create a binding, TiDB requires that the session is in a database context, which means that a database is specified when the client is connected or `use ${database}` is executed.

The original SQL statement and the bound statement must have the same text after normalization and hint removal, or the binding will fail. Take the following examples:

- This binding can be created successfully because the texts before and after parameterization and hint removal are the same: `SELECT * FROM test . t WHERE a > ?`

     ```sql
     CREATE BINDING FOR SELECT * FROM t WHERE a > 1 USING SELECT * FROM t use index  (idx) WHERE a > 2
     ```

- This binding will fail because the original SQL statement is processed as `SELECT * FROM test . t WHERE a > ?`, while the bound SQL statement is processed differently as `SELECT * FROM test . t WHERE b > ?`.

     ```sql
     CREATE BINDING FOR SELECT * FROM t WHERE a > 1 USING SELECT * FROM t use index(idx) WHERE b > 2
     ```

> **Note:**
>
> For `PREPARE` / `EXECUTE` statements and for queries executed with binary protocols, you need to create execution plan bindings for the real query statements, not for the `PREPARE` / `EXECUTE` statements.

#### Create a binding according to a historical execution plan

To make the execution plan of a SQL statement fixed to a historical execution plan, you can use `plan_digest` to bind that historical execution plan to the SQL statement, which is more convenient than binding it according to a SQL statement.

Currently, this feature has the following limitations:

- The feature generates hints according to historical execution plans and uses the generated hints for binding. Because historical execution plans are stored in [Statement Summary Tables](/statement-summary-tables.md), before using this feature, you need to enable the [`tidb_enable_stmt_summary`](/system-variables.md#tidb_enable_stmt_summary-new-in-v304) system variable first.
- Currently, this feature only supports binding historical execution plans in the `statements_summary` and `statements_summary_history` tables of the current TiDB node. If you get a `can't find any plans` error, you can connect to another TiDB node in the cluster and retry the binding.

The SQL statement of this binding method is as follows:

```sql
CREATE [GLOBAL | SESSION] BINDING FROM HISTORY USING PLAN DIGEST 'plan_digest';
```

This statement binds an execution plan to a SQL statement using `plan_digest`. The default scope is SESSION. The applicable SQL statements, priorities, scopes, and effective conditions of the created bindings are the same as that of [bindings created according to SQL statements](#create-a-binding-according-to-a-sql-statement).

To use this binding method, you need to first get the `plan_digest` corresponding to the target historical execution plan in `statements_summary`, and then create a binding using the `plan_digest`. The detailed steps are as follows:

1. Get the `plan_digest` corresponding to the target execution plan in `statements_summary`.

    For example:

    ```sql
    CREATE TABLE t(id INT PRIMARY KEY , a INT, KEY(a));
    SELECT /*+ IGNORE_INDEX(t, a) */ * FROM t WHERE a = 1;
    SELECT * FROM INFORMATION_SCHEMA.STATEMENTS_SUMMARY WHERE QUERY_SAMPLE_TEXT = 'SELECT /*+ IGNORE_INDEX(t, a) */ * FROM t WHERE a = 1'\G;
    ```

    The following is a part of the example query result of `statements_summary`:

    ```
    SUMMARY_BEGIN_TIME: 2022-12-01 19:00:00
    ...........
          DIGEST_TEXT: select * from `t` where `a` = ?
    ...........
          PLAN_DIGEST: 4e3159169cc63c14b139a4e7d72eae1759875c9a9581f94bb2079aae961189cb
                 PLAN:  id                  task        estRows operator info                           actRows execution info                                                                                                                                             memory      disk
                        TableReader_7       root        10      data:Selection_6                        0       time:4.05ms, loops:1, cop_task: {num: 1, max: 598.6µs, proc_keys: 0, rpc_num: 2, rpc_time: 609.8µs, copr_cache_hit_ratio: 0.00, distsql_concurrency: 15}   176 Bytes   N/A
                        └─Selection_6       cop[tikv]   10      eq(test.t.a, 1)                         0       tikv_task:{time:560.8µs, loops:0}                                                                                                                          N/A         N/A
                          └─TableFullScan_5 cop[tikv]   10000   table:t, keep order:false, stats:pseudo 0       tikv_task:{time:560.8µs, loops:0}                                                                                                                          N/A         N/A
          BINARY_PLAN: 6QOYCuQDCg1UYWJsZVJlYWRlcl83Ev8BCgtTZWxlY3Rpb25fNhKOAQoPBSJQRnVsbFNjYW5fNSEBAAAAOA0/QSkAAQHwW4jDQDgCQAJKCwoJCgR0ZXN0EgF0Uh5rZWVwIG9yZGVyOmZhbHNlLCBzdGF0czpwc2V1ZG9qInRpa3ZfdGFzazp7dGltZTo1NjAuOMK1cywgbG9vcHM6MH1w////CQMEAXgJCBD///8BIQFzCDhVQw19BAAkBX0QUg9lcSgBfCAudC5hLCAxKWrmYQAYHOi0gc6hBB1hJAFAAVIQZGF0YTo9GgRaFAW4HDQuMDVtcywgCbYcMWKEAWNvcF8F2agge251bTogMSwgbWF4OiA1OTguNsK1cywgcHJvY19rZXlzOiAwLCBycGNfBSkAMgkMBVcQIDYwOS4pEPBDY29wcl9jYWNoZV9oaXRfcmF0aW86IDAuMDAsIGRpc3RzcWxfY29uY3VycmVuY3k6IDE1fXCwAXj///////////8BGAE=
    ```

    In this example, you can see that the execution plan corresponding to `plan_digest` is `4e3159169cc63c14b139a4e7d72eae1759875c9a9581f94bb2079aae961189cb`.

2. Use `plan_digest` to create a binding:

    ```sql
    CREATE BINDING FROM HISTORY USING PLAN DIGEST '4e3159169cc63c14b139a4e7d72eae1759875c9a9581f94bb2079aae961189cb';
    ```

To verify whether the created binding takes effect, you can [view bindings](#view-bindings):

```sql
SHOW BINDINGS\G;
```

```
*************************** 1. row ***************************
Original_sql: select * from `test` . `t` where `a` = ?
    Bind_sql: SELECT /*+ use_index(@`sel_1` `test`.`t` ) ignore_index(`t` `a`)*/ * FROM `test`.`t` WHERE `a` = 1
       ...........
  Sql_digest: 6909a1bbce5f64ade0a532d7058dd77b6ad5d5068aee22a531304280de48349f
 Plan_digest:
1 row in set (0.01 sec)

ERROR:
No query specified
```

```sql
SELECT * FROM t WHERE a = 1;
SELECT @@LAST_PLAN_FROM_BINDING;
```

```
+--------------------------+
| @@LAST_PLAN_FROM_BINDING |
+--------------------------+
|                        1 |
+--------------------------+
1 row in set (0.00 sec)
```

### Remove a binding

You can remove a binding according to a SQL statement or `sql_digest`.

#### Remove a binding according to a SQL statement

{{< copyable "sql" >}}

```sql
DROP [GLOBAL | SESSION] BINDING FOR BindableStmt;
```

This statement removes a specified execution plan binding at the GLOBAL or SESSION level. The default scope is SESSION.

Generally, the binding in the SESSION scope is mainly used for test or in special situations. For a binding to take effect in all TiDB processes, you need to use the GLOBAL binding. A created SESSION binding shields the corresponding GLOBAL binding until the end of the SESSION, even if the SESSION binding is dropped before the session closes. In this case, no binding takes effect and the plan is selected by the optimizer.

The following example is based on the example in [create binding](#create-a-binding) in which the SESSION binding shields the GLOBAL binding:

```sql
-- Drops the binding created in the SESSION scope.
drop session binding for SELECT * FROM t1, t2 WHERE t1.id = t2.id;

-- Views the SQL execution plan again.
explain SELECT * FROM t1,t2 WHERE t1.id = t2.id;
```

In the example above, the dropped binding in the SESSION scope shields the corresponding binding in the GLOBAL scope. The optimizer does not add the `sm_join(t1, t2)` hint to the statement. The top node of the execution plan in the `explain` result is not fixed to MergeJoin by this hint. Instead, the top node is independently selected by the optimizer according to the cost estimation.

#### Remove a binding according to `sql_digest`

In addition to removing a binding according to a SQL statement, you can also remove a binding according to `sql_digest`.

```sql
DROP [GLOBAL | SESSION] BINDING FOR SQL DIGEST 'sql_digest';
```

This statement removes an execution plan binding corresponding to `sql_digest` at the GLOBAL or SESSION level. The default scope is SESSION. You can get the `sql_digest` by [viewing bindings](#view-bindings).

> **Note:**
>
> Executing `DROP GLOBAL BINDING` drops the binding in the current tidb-server instance cache and changes the status of the corresponding row in the system table to 'deleted'. This statement does not directly delete the records in the system table, because other tidb-server instances need to read the 'deleted' status to drop the corresponding binding in their cache. For the records in these system tables with the status of 'deleted', at every 100 `bind-info-lease` (the default value is `3s`, and `300s` in total) interval, the background thread triggers an operation of reclaiming and clearing on the bindings of `update_time` before 10 `bind-info-lease` (to ensure that all tidb-server instances have read the 'deleted' status and updated the cache).

### Change binding status

#### Change binding status according to a SQL statement

{{< copyable "sql" >}}

```sql
SET BINDING [ENABLED | DISABLED] FOR BindableStmt;
```

You can execute this statement to change the status of a binding. The default status is ENABLED. The effective scope is GLOBAL by default and cannot be modified.

When executing this statement, you can only change the status of a binding from `Disabled` to `Enabled` or from `Enabled` to `Disabled`. If no binding is available for status changes, a warning message is returned, saying `There are no bindings can be set the status. Please check the SQL text`. Note that a binding in `Disabled` status is not used by any query.

#### Change binding status according to `sql_digest`

In addition to changing the binding status according to a SQL statement, you can also change the binding status according to `sql_digest`:

```sql
SET BINDING [ENABLED | DISABLED] FOR SQL DIGEST 'sql_digest';
```

The binding status that can be changed by `sql_digest` and the effect is the same as those changed [according to a SQL statement](#change-binding-status-according-to-a-sql-statement). If no binding is available for status changes, a warning message `can't find any binding for 'sql_digest'` is returned.

### View bindings

{{< copyable "sql" >}}

```sql
SHOW [GLOBAL | SESSION] BINDINGS [ShowLikeOrWhere]
```

This statement outputs the execution plan bindings at the GLOBAL or SESSION level according to the order of binding update time from the latest to earliest. The default scope is SESSION. Currently `SHOW BINDINGS` outputs 11 columns, as shown below:

| Column Name | Note |
| :-------- | :------------- |
| original_sql  |  Original SQL statement after parameterization |
| bind_sql | Bound SQL statement with hints |
| default_db | Default database |
| status | Status including `enabled` (replacing the `using` status from v6.0), `disabled`, `deleted`, `invalid`, `rejected`, and `pending verify`|
| create_time | Creating time |
| update_time | Updating time |
| charset | Character set |
| collation | Ordering rule |
| source | The way in which a binding is created, including `manual` (created according to a SQL statement), `history` (created according to a historical execution plan), `capture` (captured automatically by TiDB), and `evolve` (evolved automatically by TiDB) |
| sql_digest | Digest of a normalized SQL statement |
| plan_digest | Digest of an execution plan |

### Troubleshoot a binding

You can use either of the following methods to troubleshoot a binding:

- Use the system variable [`last_plan_from_binding`](/system-variables.md#last_plan_from_binding-new-in-v40) to show whether the execution plan used by the last executed statement is from the binding.

     {{< copyable "sql" >}}

    ```sql
    -- Create a global binding
    CREATE GLOBAL BINDING for
        SELECT * FROM t
    USING
        SELECT /*+ USE_INDEX(t, idx_a) */ * FROM t;

    SELECT * FROM t;
    SELECT @@[SESSION.]last_plan_from_binding;
    ```

    ```sql
    +--------------------------+
    | @@last_plan_from_binding |
    +--------------------------+
    |                        1 |
    +--------------------------+
    1 row in set (0.00 sec)
    ```

- Use the `explain format = 'verbose'` statement to view the query plan of a SQL statement. If the SQL statement uses a binding, you can run `show warnings` to check which binding is used in the SQL statement.

    ```sql
    -- Create a global binding

    CREATE GLOBAL BINDING for
        SELECT * FROM t
    USING
        SELECT /*+ USE_INDEX(t, idx_a) */ * FROM t;

    -- Use explain format = 'verbose' to view the execution plan of a SQL statement

    explain format = 'verbose' SELECT * FROM t;

    -- Run `show warnings` to view the binding used in the query.

    show warnings;
    ```

    ```sql
    +-------+------+--------------------------------------------------------------------------+
    | Level | Code | Message                                                                  |
    +-------+------+--------------------------------------------------------------------------+
    | Note  | 1105 | Using the bindSQL: SELECT /*+ USE_INDEX(`t` `idx_a`)*/ * FROM `test`.`t` |
    +-------+------+--------------------------------------------------------------------------+
    1 row in set (0.01 sec)

    ```

### Cache bindings

Each TiDB instance has a least recently used (LRU) cache for bindings. The cache capacity is controlled by the system variable [`tidb_mem_quota_binding_cache`](/system-variables.md#tidb_mem_quota_binding_cache-new-in-v600). You can view bindings that are cached in the TiDB instance.

To view the cache status of bindings, run the `SHOW binding_cache status` statement. In this statement, the effective scope is GLOBAL by default and cannot be modified. This statement returns the number of available bindings in the cache, the total number of available bindings in the system, memory usage of all cached bindings, and the total memory for the cache.

{{< copyable "sql" >}}

```sql

SHOW binding_cache status;
```

```sql
+-------------------+-------------------+--------------+--------------+
| bindings_in_cache | bindings_in_table | memory_usage | memory_quota |
+-------------------+-------------------+--------------+--------------+
|                 1 |                 1 | 159 Bytes    | 64 MB        |
+-------------------+-------------------+--------------+--------------+
1 row in set (0.00 sec)
```

## Baseline capturing

Used for [preventing regression of execution plans during an upgrade](#prevent-regression-of-execution-plans-during-an-upgrade), this feature captures queries that meet capturing conditions and creates bindings for these queries.

### Enable capturing

To enable baseline capturing, set `tidb_capture_plan_baselines` to `on`. The default value is `off`.

> **Note:**
>
> Because the automatic binding creation function relies on [Statement Summary](/statement-summary-tables.md), make sure to enable Statement Summary before using automatic binding.

After automatic binding creation is enabled, the historical SQL statements in the Statement Summary are traversed every `bind-info-lease` (the default value is `3s`), and a binding is automatically created for SQL statements that appear at least twice. For these SQL statements, TiDB automatically binds the execution plan recorded in Statement Summary.

However, TiDB does not automatically capture bindings for the following types of SQL statements:

- `EXPLAIN` and `EXPLAIN ANALYZE` statements.
- SQL statements executed internally in TiDB, such as `SELECT` queries used for automatically loading statistical information.
- Statements that contain `Enabled` or `Disabled` bindings.
- Statements that are filtered out by capturing conditions.

> **Note:**
>
> Currently, a binding generates a group of hints to fix an execution plan generated by a query statement. In this way, for the same query, the execution plan does not change. For most OLTP queries, including queries using the same index or Join algorithm (such as HashJoin and IndexJoin), TiDB guarantees plan consistency before and after the binding. However, due to the limitations of hints, TiDB cannot guarantee plan consistency for some complex queries, such as Join of more than two tables, MPP queries, and complex OLAP queries.

For `PREPARE` / `EXECUTE` statements and for queries executed with binary protocols, TiDB automatically captures bindings for the real query statements, not for the `PREPARE` / `EXECUTE` statements.

> **Note:**
>
> Because TiDB has some embedded SQL statements to ensure the correctness of some features, baseline capturing by default automatically shields these SQL statements.

### Filter out bindings

This feature allows you to configure a blocklist to filter out queries whose bindings you do not want to capture. A blocklist has three dimensions, table name, frequency, and user name.

#### Usage

Insert filtering conditions into the system table `mysql.capture_plan_baselines_blacklist`. Then the filtering conditions take effect in the entire cluster immediately.

```sql
-- Filter by table name
 INSERT INTO mysql.capture_plan_baselines_blacklist(filter_type, filter_value) VALUES('table', 'test.t');

-- Filter by database name and table name through wildcards
 INSERT INTO mysql.capture_plan_baselines_blacklist(filter_type, filter_value) VALUES('table', 'test.table_*');
 INSERT INTO mysql.capture_plan_baselines_blacklist(filter_type, filter_value) VALUES('table', 'db_*.table_*');

-- Filter by frequency
 INSERT INTO mysql.capture_plan_baselines_blacklist(filter_type, filter_value) VALUES('frequency', '2');

-- Filter by user name
 INSERT INTO mysql.capture_plan_baselines_blacklist(filter_type, filter_value) VALUES('user', 'user1');
```

| **Dimension name** | **Description**                                                     | Remarks                                                     |
| :----------- | :----------------------------------------------------------- | ------------------------------------------------------------ |
| table        | Filter by table name. Each filtering rule is in the `db.table` format. The supported filtering syntax includes [Plain table names](/table-filter.md#plain-table-names) and [Wildcards](/table-filter.md#wildcards). | Case insensitive. If a table name contains illegal characters, the log returns a warning message `[sql-bind] failed to load mysql.capture_plan_baselines_blacklist`. |
| frequency    | Filter by frequency. SQL statements executed more than once are captured by default. You can set a high frequency to capture statements that are frequently executed. | Setting frequency to a value smaller than 1 is considered illegal, and the log returns a warning message `[sql-bind] frequency threshold is less than 1, ignore it`. If multiple frequency filter rules are inserted, the value with the highest frequency prevails. |
| user         | Filter by user name. Statements executed by blocklisted users are not captured.                           | If multiple users execute the same statement and their user names are all in the blocklist, this statement is not captured. |

> **Note:**
>
> - Modifying a blocklist requires the super privilege.
>
> - If a blocklist contains illegal filters, TiDB returns the warning message `[sql-bind] unknown capture filter type, ignore it` in the log.

### Prevent regression of execution plans during an upgrade

 Before upgrading a TiDB cluster, you can use baseline capturing to prevent regression of execution plans by performing the following steps:

1. Enable baseline capturing and keep it working.

    > **Note:**
    >
    > Test data shows that long-term working of baseline capturing has a slight impact on the performance of the cluster load. Therefore, it is recommended to enable baseline capturing as long as possible so that important plans (appear twice or above) are captured.

2. Upgrade the TiDB cluster. After the upgrade, TiDB uses those captured bindings to ensure execution plan consistency.

3. After the upgrade, delete bindings as required.

    - Check the binding source by running the [`SHOW GLOBAL BINDINGS`](#view-bindings) statement.

        In the output, check the `Source` field to see whether a binding is captured (`capture`) or manually created (`manual`).

    - Determine whether to retain the captured bindings:

        ```
        -- View the plan with the binding enabled
        SET @@SESSION.TIDB_USE_PLAN_BASELINES = true;
        EXPLAIN FORMAT='VERBOSE' SELECT * FROM t1 WHERE ...;

        -- View the plan with the binding disabled
        SET @@SESSION.TIDB_USE_PLAN_BASELINES = false;
        EXPLAIN FORMAT='VERBOSE' SELECT * FROM t1 WHERE ...;
        ```

        - If the execution plan is consistent, you can delete the binding safely.

        - If the execution plan is inconsistent, you need to identify the cause, for example, by checking statistics. In this case, you need to retain the binding to ensure plan consistency.

## Baseline evolution

Baseline evolution is an important feature of SPM introduced in TiDB v4.0.

As data updates, the previously bound execution plan might no longer be optimal. The baseline evolution feature can automatically optimize the bound execution plan.

In addition, baseline evolution, to a certain extent, can also avoid the jitter brought to the execution plan caused by the change of statistical information.

### Usage

Use the following statement to enable automatic binding evolution:

{{< copyable "sql" >}}

```sql
SET GLOBAL tidb_evolve_plan_baselines = ON;
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
CREATE TABLE t(a INT, b INT, KEY(a), KEY(b));
```

Perform the following query on table `t`:

{{< copyable "sql" >}}

```sql
SELECT * FROM t WHERE a < 100 AND b < 100;
```

In the table defined above, few rows meet the `a < 100` condition. But for some reason, the optimizer mistakenly selects the full table scan instead of the optimal execution plan that uses index `a`. You can first use the following statement to create a binding:

{{< copyable "sql" >}}

```sql
CREATE GLOBAL BINDING for SELECT * FROM t WHERE a < 100 AND b < 100 using SELECT * FROM t use index(a) WHERE a < 100 AND b < 100;
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

    SELECT @@global.tidb_evolve_plan_baselines;

    -- If `tidb_evolve_plan_baselines` is still enabled, disable it.

    SET GLOBAL tidb_evolve_plan_baselines = OFF;
    ```

* Before you upgrade from v4.0 to the current version, you need to check whether the syntax of all queries corresponding to the available SQL bindings is correct in the new version. If any syntax errors exist, delete the corresponding SQL binding. To do that, perform the following steps.

    {{< copyable "sql" >}}

    ```sql
    -- Check the query corresponding to the available SQL binding in the version to be upgraded.

    SELECT bind_sql FROM mysql.bind_info WHERE status = 'using';

    -- Verify the result from the above SQL query in the test environment of the new version.

    bind_sql_0;
    bind_sql_1;
    ...

    -- In the case of a syntax error (ERROR 1064 (42000): You have an error in your SQL syntax), delete the corresponding binding.
    -- For any other errors (for example, tables are not found), it means that the syntax is compatible. No other operation is needed.
    ```
