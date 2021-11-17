---
title: SQL Prepare Execution Plan Cache
summary: Learn about SQL Prepare Execution Plan Cache in TiDB.
---

# SQL Prepare Execution Plan Cache

TiDB supports execution plan caching for `Prepare` and `Execute` queries. This includes both forms of prepared statements:

- Using the `COM_STMT_PREPARE` and `COM_STMT_EXECUTE` protocol features.
- Using the SQL statements `PREPARE` and `EXECUTE`.

The TiDB optimizer handles these two types of queries in the same way: when preparing, the parameterized query is parsed into an AST (Abstract Syntax Tree) and cached; in later execution, the execution plan is generated based on the stored AST and specific parameter values.

When the execution plan cache is enabled, in the first execution every `Prepare` statement checks whether the current query can use the execution plan cache, and if the query can use it, then put the generated execution plan into a cache implemented by LRU (Least Recently Used) linked list. In the subsequent `Execute` queries, the execution plan is obtained from the cache and checked for availability. If the check succeeds, the step of generating an execution plan is skipped. Otherwise, the execution plan is regenerated and saved in the cache.

In the current version of TiDB, if a `Prepare` statement meets any of the following conditions, the query or the plan is not cached:

- The query contains SQL statements other than `SELECT`, `UPDATE`, `INSERT`, `DELETE`, `Union`, `Intersect`, and `Except`.
- The query accesses partitioned tables or temporary tables, or a table that contains generated columns.
- The query contains sub-queries, such as `select * from t where a > (select ...)`.
- The query contains the `ignore_plan_cache` hint, such as `select /*+ ignore_plan_cache() */ * from t`.
- The query contains variables other than `?` (including system variables or user-defined variables), such as `select * from t where a>? and b>@x`.
- The query contains the functions that cannot be cached: `database()`, `current_user`, `current_role`, `user`, `connection_id`, `last_insert_id`, `row_count`, `version`, and `like`.
- The query contains `?` after `Limit`, such as `Limit ?` and `Limit 10, ?`. Such queries are not cached because the specific value of `?` has a great impact on query performance.
- The query contains `?` after `Order By`, such as `Order By ?`. Such queries sort data based on the column specified by `?`. If the queries targeting different columns use the same execution plan, the results will be wrong. Therefore, such queries are not cached. However, if the query is a common one, such as `Order By a+?`, it is cached.
- The query contains `?` after `Group By`, such as `Group By?`. Such queries group data based on the column specified by `?`. If the queries targeting different columns use the same execution plan, the results will be wrong. Therefore, such queries are not cached. However, if the query is a common one, such as `Group By a+?`, it is cached.
- The query contains `?` in the definition of the `Window Frame` window function, such as `(partition by year order by sale rows ? preceding)`. If `?` appears elsewhere in the window function, the query is cached.
- The query contains parameters for comparing `int` and `string`, such as `c_int >= ?` or `c_int in (?, ?)`, in which `?` indicates the string type, such as `set @x='123'`. To ensure that the query result is compatible with MySQL, parameters need to be adjusted in each query, so such queries are not cached.
- The plan attempts to access `TiFlash`.

The LRU linked list is designed as a session-level cache because `Prepare` / `Execute` cannot be executed across sessions. Each element of the LRU list is a key-value pair. The value is the execution plan, and the key is composed of the following parts:

- The name of the database where `Execute` is executed
- The identifier of the `Prepare` statement, that is, the name after the `PREPARE` keyword
- The current schema version, which is updated after every successfully executed DDL statement
- The SQL mode when executing `Execute`
- The current time zone, which is the value of the `time_zone` system variable

Any change in the above information (for example, switching databases, renaming `Prepare` statement, executing DDL statements, or modifying the value of SQL mode / `time_zone`), or the LRU cache elimination mechanism causes the execution plan cache miss when executing.

After the execution plan cache is obtained from the cache, TiDB first checks whether the execution plan is still valid. If the current `Execute` statement is executed in an explicit transaction, and the referenced table is modified in the transaction pre-order statement, the cached execution plan accessing this table does not contain the `UnionScan` operator, then it cannot be executed.

After the validation test is passed, the scan range of the execution plan is adjusted according to the current parameter values, and then used to perform data querying.

There are several points worth noting about execution plan caching and query performance:

- The first `Execute` (no cache plan yet) is affected by existing SQL Bindings. Cached plans are not affected by new SQL Bindings. Similarly, cached plans are not affected by changes in statistics, optimization rules, and blacklist pushdown by expressions.
- When restarting a TiDB instance (for example, online rolling upgrade of a TiDB cluster), the `Prepare` statement gets lost. `Prepared Statement not found` is returned if executing `execute stmt...`. To address the error, execute `prepare stmt ...` again.
- Considering that the parameters of `Execute` are different, the execution plan cache prohibits some aggressive query optimization methods that are closely related to specific parameter values to ensure adaptability. This causes that the query plan may not be optimal for certain parameter values. For example, the filter condition of the query is `where a > ? And a < ?`, the parameters of the first `Execute` statement are `2` and `1` respectively. Considering that these two parameters maybe be `1` and `2` in the next execution time, the optimizer does not generate the optimal `TableDual` execution plan that is specific to current parameter values;
- If cache invalidation and elimination are not considered, an execution plan cache is applied to various parameter values, which in theory also results in non-optimal execution plans for certain values. For example, if the filter condition is `where a < ?` and the parameter value used for the first execution is `1`, then the optimizer generates the optimal `IndexScan` execution plan and puts it into the cache. In the subsequent executions, if the value becomes `10000`, the `TableScan` plan might be the better one. But due to the execution plan cache, the previously generated `IndexScan` is used for execution. Therefore, the execution plan cache is more suitable for application scenarios where the query is simple (the ratio of compilation is high) and the execution plan is relatively fixed.

Currently, the execution plan cache is disabled by default. You can enable this feature by enabling the [`prepare-plan-cache`](/tidb-configuration-file.md#prepared-plan-cache) in the TiDB configuration file.

> **Note：**
>
> The execution plan cache feature applies only to `Prepare` / `Execute` queries and does not take effect for normal queries.

After the execution plan cache feature is enabled, you can use the session-level system variable `last_plan_from_cache` to see whether the previous `Execute` statement used the cached execution plan, for example:

{{< copyable "sql" >}}

```sql
MySQL [test]> create table t(a int);
Query OK, 0 rows affected (0.00 sec)
MySQL [test]> prepare stmt from 'select * from t where a = ?';
Query OK, 0 rows affected (0.00 sec)
MySQL [test]> set @a = 1;
Query OK, 0 rows affected (0.00 sec)

-- The first execution generates an execution plan and saves it in the cache.
MySQL [test]> execute stmt using @a;
Empty set (0.00 sec)
MySQL [test]> select @@last_plan_from_cache;
+------------------------+
| @@last_plan_from_cache |
+------------------------+
| 0                      |
+------------------------+
1 row in set (0.00 sec)

-- The second execution hits the cache.
MySQL [test]> execute stmt using @a;
Empty set (0.00 sec)
MySQL [test]> select @@last_plan_from_cache;
+------------------------+
| @@last_plan_from_cache |
+------------------------+
| 1                      |
+------------------------+
1 row in set (0.00 sec)
```

If you find that a certain set of `Prepare` / `Execute` has unexpected behavior due to the execution plan cache, you can use the `ignore_plan_cache()` SQL hint to skip using the execution plan cache for the current statement. Still, use the above statement as an example:

{{< copyable "sql" >}}

```sql
MySQL [test]> prepare stmt from 'select /*+ ignore_plan_cache() */ * from t where a = ?';
Query OK, 0 rows affected (0.00 sec)
MySQL [test]> set @a = 1;
Query OK, 0 rows affected (0.00 sec)
MySQL [test]> execute stmt using @a;
Empty set (0.00 sec)
MySQL [test]> select @@last_plan_from_cache;
+------------------------+
| @@last_plan_from_cache |
+------------------------+
| 0                      |
+------------------------+
1 row in set (0.00 sec)
MySQL [test]> execute stmt using @a;
Empty set (0.00 sec)
MySQL [test]> select @@last_plan_from_cache;
+------------------------+
| @@last_plan_from_cache |
+------------------------+
| 0                      |
+------------------------+
1 row in set (0.00 sec)
```
