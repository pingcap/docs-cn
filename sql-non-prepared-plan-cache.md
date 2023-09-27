---
title: SQL Non-Prepared Execution Plan Cache
summary: Learn about the principle, usage, and examples of the SQL non-prepared execution plan cache in TiDB.
---

# SQL Non-Prepared Execution Plan Cache

TiDB supports execution plan caching for some non-`PREPARE` statements, similar to the [`Prepare`/`Execute` statements](/sql-prepared-plan-cache.md). This feature allows these statements to skip the optimization phase and improve performance.

Enabling the non-prepared plan cache might incur additional memory and CPU overhead and might not be suitable for all situations. To determine whether to enable this feature in your scenario, refer to the [Performance benefits](#performance-benefits) and [Memory monitoring](#monitoring) sections.

## Principle

The non-prepared plan cache is a session-level feature that shares a cache with the [prepared plan cache](/sql-prepared-plan-cache.md). The basic principle of the non-prepared plan cache is as follows:

1. After you enable the non-prepared plan cache, TiDB first parameterizes the query based on the abstract syntax tree (AST). For example, `SELECT * FROM t WHERE b < 10 AND a = 1` is parameterized as `SELECT * FROM t WHERE b < ? and a = ?`.
2. Then, TiDB uses the parameterized query to search the plan cache.
3. If a reusable plan is found, it is directly used and the optimization phase is skipped.
4. Otherwise, the optimizer generates a new plan and adds it back into the cache for reuse in the subsequent query.

## Usage

To enable or disable the non-prepared plan cache, you can set the [`tidb_enable_non_prepared_plan_cache`](/system-variables.md#tidb_enable_non_prepared_plan_cache) system variable. You can also control the size of the non-prepared plan cache using the [`tidb_session_plan_cache_size`](/system-variables.md#tidb_session_plan_cache_size-new-in-v710) system variable. When the number of cached plans exceeds `tidb_session_plan_cache_size`, TiDB evicts plans using the least recently used (LRU) strategy.

Starting from v7.1.0, you can control the maximum size of a plan that can be cached using the system variable [`tidb_plan_cache_max_plan_size`](/system-variables.md#tidb_plan_cache_max_plan_size-new-in-v710). The default value is 2 MB. If the size of a plan exceeds this value, the plan will not be cached.

> **Note:**
>
> The memory specified by `tidb_session_plan_cache_size` is shared between the prepared and non-prepared plan cache. If you have enabled the prepared plan cache for the current cluster, enabling the non-prepared plan cache might reduce the hit rate of the original prepared plan cache.

## Example

The following example shows how to use the non-prepared plan cache:

1. Create a table `t` for testing:

    ```sql
    CREATE TABLE t (a INT, b INT, KEY(b));
    ```

2. Enable the non-prepared plan cache:

    ```sql
    SET tidb_enable_non_prepared_plan_cache = ON;
    ```

3. Execute the following two queries:

    ```sql
    SELECT * FROM t WHERE b < 10 AND a = 1;
    SELECT * FROM t WHERE b < 5 AND a = 2;
    ```

4. Check whether the second query hits the cache:

    ```sql
    SELECT @@last_plan_from_cache;
    ```

    If the value of `last_plan_from_cache` in the output is `1`, it means that the execution plan of the second query comes from the cache:

    ```sql
    +------------------------+
    | @@last_plan_from_cache |
    +------------------------+
    |                      1 |
    +------------------------+
    1 row in set (0.00 sec)
    ```

## Restrictions

### Cache suboptimal plans

TiDB only caches one plan for a parameterized query. For example, the queries `SELECT * FROM t WHERE a < 1` and `SELECT * FROM t WHERE a < 100000` share the same parameterized form, `SELECT * FROM t WHERE a < ?`, and thus share the same plan.

If this causes performance issues, you can use the `ignore_plan_cache()` hint to ignore plans in the cache, so that the optimizer generates a new execution plan for the SQL every time. If the SQL cannot be modified, you can create a binding to solve the problem. For example, `CREATE BINDING FOR SELECT ... USING SELECT /*+ ignore_plan_cache() */ ...`.

### Usage restrictions

Due to the preceding risks and the fact that the execution plan cache only provides significant benefits for simple queries (if a query is complex and takes a long time to execute, using the execution plan cache might not be very helpful), TiDB has strict restrictions on the scope of non-prepared plan cache. The restrictions are as follows:

- Queries or plans that are not supported by the [Prepared plan cache](/sql-prepared-plan-cache.md) are also not supported by the non-prepared plan cache.
- Queries that contain complex operators such as `Window` or `Having` are not supported.
- Queries that contain three or more `Join` tables or subqueries are not supported.
- Queries that contain numbers or expressions directly after `ORDER BY` or `GROUP BY` are not supported, such as `ORDER BY 1` and `GROUP BY a+1`. Only `ORDER BY column_name` and `GROUP BY column_name` are supported.
- Queries that filter on columns of `JSON`, `ENUM`, `SET`, or `BIT` type are not supported, such as `SELECT * FROM t WHERE json_col = '{}'`.
- Queries that filter on `NULL` values are not supported, such as `SELECT * FROM t WHERE a is NULL`.
- Queries with more than 200 parameters after parameterization are not supported by default, such as `SELECT * FROM t WHERE a in (1, 2, 3, ... 201)`. Starting from v7.3.0, you can modify this limit by setting the [`44823`](/optimizer-fix-controls.md#44823-new-in-v730) fix in the [`tidb_opt_fix_control`](/system-variables.md#tidb_opt_fix_control-new-in-v710) system variable.
- Queries that access partitioned tables, virtual columns, temporary tables, views, or memory tables are not supported, such as `SELECT * FROM INFORMATION_SCHEMA.COLUMNS`, where `COLUMNS` is a TiDB memory table.
- Queries with hints or bindings are not supported.
- DML statements or `SELECT` statements with the `FOR UPDATE` clause are not supported by default. To remove this restriction, you can execute `SET tidb_enable_non_prepared_plan_cache_for_dml = ON`.

After you enable this feature, the optimizer quickly evaluates the query. If it does not meet the support conditions for non-prepared plan cache, the query falls back to the regular optimization process.

## Performance benefits

In internal tests, enabling the non-prepared plan cache feature can achieve significant performance benefits in most TP scenarios. For example, a performance improvement of about 4% in TPC-C tests, over 10% in some banking workloads, and 15% in Sysbench RangeScan.

However, this feature also introduces some additional memory and CPU overhead, including determining whether the query is supported, parameterizing the query, and searching for a plan in the cache. If the cache cannot hit the majority of queries in your workload, enabling it might actually adversely affect performance.

In this case, you need to observe the `non-prepared` metric in the **Queries Using Plan Cache OPS** panel and the `non-prepared-unsupported` metric in the **Plan Cache Miss OPS** panel on Grafana. If most queries are not supported and only a few can hit the plan cache, you can disable this feature.

![non-prepared-unsupported](/media/non-prepapred-plan-cache-unsupprot.png)

## Diagnostics

After enabling the non-prepared plan cache, you can execute the `EXPLAIN FORMAT='plan_cache' SELECT ...` statement to verify whether the query can hit the cache. For queries that cannot hit the cache, the system returns the reason in a warning.

Note that if you do not add `FORMAT='plan_cache'`, the `EXPLAIN` statement will never hit the cache.

To verify whether the query hits the cache, execute the following `EXPLAIN FORMAT='plan_cache'` statement:

```sql
EXPLAIN FORMAT='plan_cache' SELECT * FROM (SELECT a+1 FROM t1) t;
```

The output is as follows:

```sql
3 rows in set, 1 warning (0.00 sec)
```

To view the queries that cannot hit the cache, execute `SHOW warnings;`:

```sql
SHOW warnings;
```

The output is as follows:

```sql
+---------+------+-------------------------------------------------------------------------------+
| Level   | Code | Message                                                                       |
+---------+------+-------------------------------------------------------------------------------+
| Warning | 1105 | skip non-prepared plan-cache: queries that have sub-queries are not supported |
+---------+------+-------------------------------------------------------------------------------+
1 row in set (0.00 sec)
```

In the preceding example, the query cannot hit the cache because the non-prepared plan cache does not support the `+` operation.

## Monitoring

After enabling the non-prepared plan cache, you can monitor the memory usage, number of plans in the cache, and cache hit rate in the following panes:

![non-prepare-plan-cache](/media/tidb-non-prepared-plan-cache-metrics.png)

You can also monitor the cache hit rate in the `statements_summary` table and slow query log. The following shows how to view the cache hit rate in the `statements_summary` table:

1. Create a table `t`:

    ```sql
    CREATE TABLE t (a int);
    ```

2. Enable the non-prepared plan cache:

    ```sql
    SET @@tidb_enable_non_prepared_plan_cache=ON;
    ```

3. Execute the following three queries:

    ```sql
    SELECT * FROM t WHERE a<1;
    SELECT * FROM t WHERE a<2;
    SELECT * FROM t WHERE a<3;
    ```

4. Query the `statements_summary` table to view the cache hit rate:

    ```sql
    SELECT digest_text, query_sample_text, exec_count, plan_in_cache, plan_cache_hits FROM INFORMATION_SCHEMA.STATEMENTS_SUMMARY WHERE query_sample_text LIKE '%SELECT * FROM %';
    ```

    The output is as follows:

    ```sql
    +---------------------------------+------------------------------------------+------------+---------------+-----------------+
    | digest_text                     | query_sample_text                        | exec_count | plan_in_cache | plan_cache_hits |
    +---------------------------------+------------------------------------------+------------+---------------+-----------------+
    | SELECT * FROM `t` WHERE `a` < ? | SELECT * FROM t WHERE a<1                |          3 |             1 |               2 |
    +---------------------------------+------------------------------------------+------------+---------------+-----------------+
    1 row in set (0.01 sec)
    ```

    From the output, you can see that the query was executed three times and hit the cache twice.
