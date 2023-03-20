---
title: SQL Non-Prepared Execution Plan Cache
summary: Learn about the principle, usage, and examples of the SQL non-prepared execution plan cache in TiDB.
---

# SQL Non-Prepared Execution Plan Cache

> **Warning:**
>
> The non-prepared execution plan cache is an experimental feature. It is not recommended that you use it in the production environment. This feature might be changed or removed without prior notice. If you find a bug, you can report an [issue](https://github.com/pingcap/tidb/issues) on GitHub.

TiDB supports execution plan caching for some non-`PREPARE` statements, similar to the [`Prepare`/`Execute` statements](/sql-prepared-plan-cache.md). This feature allows these statements to skip the optimization phase and improve performance.

## Principle

The non-prepared plan cache is a session-level feature that is independent of the [prepared plan cache](/sql-prepared-plan-cache.md), and the cached plans do not affect each other. The basic principle of the non-prepared plan cache is as follows:

1. After you enable the non-prepared plan cache, TiDB first parameterizes the query based on the abstract syntax tree (AST). For example, `SELECT * FROM t WHERE b < 10 AND a = 1` is parameterized as `SELECT * FROM t WHERE b < ? and a = ?`.
2. Then, TiDB uses the parameterized query to search the non-prepared plan cache.
3. If a reusable plan is found, it is directly used and the optimization phase is skipped.
4. Otherwise, the optimizer generates a new plan and adds it back into the cache for reuse in the subsequent query.

## Usage

To enable or disable the non-prepared plan cache, you can set the [`tidb_enable_non_prepared_plan_cache`](/system-variables.md#tidb_enable_non_prepared_plan_cache) system variable. You can also control the size of the non-prepared plan cache using the [`tidb_non_prepared_plan_cache_size`](/system-variables.md#tidb_non_prepared_plan_cache_size) system variable. When the number of cached plans exceeds `tidb_non_prepared_plan_cache_size`, TiDB evicts plans using the least recently used (LRU) strategy.

## Example

The following example shows how to use the non-prepared plan cache:

1. Create a table `t` for testing:

    ```sql
    CREATE TABLE t (a INT, b INT, KEY(b));
    ```

2. Enable the non-prepared plan cache:

    ```sql
    SET tidb_enable_non_prepared_plan_cache = true;
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

TiDB only caches one plan for a parameterized query. For example, the queries `SELECT * FROM t WHERE a < 1` and `SELECT * FROM t WHERE a < 100000` share the same parameterized form, `SELECT * FROM t WHERE a < ?`, and thus share the same plan.

If this causes performance issues, you can use the `ignore_plan_cache()` hint to ignore plans in the cache, so that the optimizer generates a new execution plan for the SQL every time. If the SQL cannot be modified, you can create a binding to solve the problem. For example, `CREATE BINDING FOR SELECT ... USING SELECT /*+ ignore_plan_cache() */ ...`.

Due to the preceding risks and the fact that the execution plan cache only provides significant benefits for simple queries (if a query is complex and takes a long time to execute, using the execution plan cache might not be very helpful), TiDB has strict restrictions on the scope of non-prepared plan cache. The restrictions are as follows:

- Queries or plans that are not supported by the [Prepared plan cache](/sql-prepared-plan-cache.md) are also not supported by the non-prepared plan cache.
- Currently, only point get or range queries on a single table that contain `Scan`, `Selection`, or `Projection` operators are supported, such as `SELECT * FROM t WHERE a < 10 AND b in (1, 2)`.
- Queries that contain complex operators such as `Agg`, `Limit`, `Window`, or `Sort` are not supported.
- Queries that contain non-range query conditions are not supported, such as:
    - `LIKE` is not supported, such as `c LIKE 'c%'`.
    - `+` operation is not supported, such as `a+1 < 2`.
- Queries that filter on columns of `JSON`, `ENUM`, `SET`, or `BIT` type are not supported, such as `SELECT * FROM t WHERE json_col = '{}'`.
- Queries that filter on `NULL` values are not supported, such as `SELECT * FROM t WHERE a is NULL`.
- Queries with more than 50 parameters after parameterization are not supported, such as `SELECT * FROM t WHERE a in (1, 2, 3, ... 51)`.
- Queries that access partitioned tables, virtual columns, temporary tables, views, or memory tables are not supported, such as `SELECT * FROM INFORMATION_SCHEMA.COLUMNS`, where `COLUMNS` is a TiDB memory table.
- Queries with hints, subqueries, or locks are not supported.
- DML statements are not supported.

## Diagnostics

After enabling the non-prepared plan cache, you can execute the `EXPLAIN FORMAT='plan_cache' SELECT ...` statement to verify whether the query can hit the cache. For queries that cannot hit the cache, the system returns the reason in a warning.

Note that if you do not add `FORMAT='plan_cache'`, the `EXPLAIN` statement will never hit the cache.

To verify whether the query hits the cache, execute the following `EXPLAIN FORMAT='plan_cache'` statement:

```sql
EXPLAIN FORMAT='plan_cache' SELECT * FROM t WHERE a+2 < 10;
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
+---------+------+-----------------------------------------------------------------------+
| Level   | Code | Message                                                               |
+---------+------+-----------------------------------------------------------------------+
| Warning | 1105 | skip non-prep plan cache: query has some unsupported binary operation |
+---------+------+-----------------------------------------------------------------------+
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
    SET @@tidb_enable_non_prepared_plan_cache=1;
    ```

3. Execute the following three queries:

    ```sql
    SELECT * FROM t WHERE a<1;
    SELECT * FROM t WHERE a<2;
    SELECT * FROM t WHERE a<3;
    ```

4. Query the `statements_summary` table to view the cache hit rate:

    ```sql
    SELECT digest_text, query_sample_text, exec_count, plan_in_cache, plan_cache_hits FROM INFORMATION_SCHEMA.STATEMENTS_SUMMARY WHERE digest_text LIKE '%SELECT * FROM %';
    ```

    The output is as follows:

    ```sql
    +---------------------------------+------------------------------------------+------------+---------------+-----------------+
    | digest_text                     | query_sample_text                        | exec_count | plan_in_cache | plan_cache_hits |
    +---------------------------------+------------------------------------------+------------+---------------+-----------------+
    | SELECT * FROM `t` WHERE `a` < ? | SELECT * FROM t WHERE a<1 [arguments: 1] |          3 |             1 |               2 |
    +---------------------------------+------------------------------------------+------------+---------------+-----------------+
    1 row in set (0.01 sec)
    ```

    From the output, you can see that the query was executed three times and hit the cache twice.
