---
title: Optimizer Hints
summary: Use Optimizer Hints to influence query execution plans
aliases: ['/docs/dev/optimizer-hints/','/docs/dev/reference/performance/optimizer-hints/']
---

# Optimizer Hints

TiDB supports optimizer hints, which are based on the comment-like syntax introduced in MySQL 5.7. For example, one of the common syntaxes is `/*+ HINT_NAME([t1_name [, t2_name] ...]) */`. Use of optimizer hints is recommended in cases where the TiDB optimizer selects a less optimal query plan.

> **Note:**
>
> MySQL command-line clients earlier than 5.7.7 strip optimizer hints by default. If you want to use the `Hint` syntax in these earlier versions, add the `--comments` option when starting the client. For example: `mysql -h 127.0.0.1 -P 4000 -uroot --comments`.

## Syntax

Optimizer hints are specified within `/*+ ... */` comments and follow behind the `SELECT`, `UPDATE` or `DELETE` keyword in a SQL statement. The hint names are case insensitive. If you want to use multiple hints, separate them with commas.

For example, the following query uses three different hints:

{{< copyable "sql" >}}

```sql
select /*+ USE_INDEX(t1, idx1), HASH_AGG(), HASH_JOIN(t1) */ count(*) from t t1, t t2 where t1.a = t2.b;
```

Currently, TiDB supports two categories of hints, which are slightly different in usage. The first category of hints is used to control the optimizer's behaviors, such as [`/*+ HASH_AGG() */`](#hash_agg); the second category of hints is used to set operation parameters for a single query, such as [`/*+ MEMORY_QUOTA(1024 MB)*/`](#memory_quotan).

## Hints for controlling the optimizer

A hint for controlling the optimizer follows behind **any** `SELECT`, `UPDATE` or `DELETE` keyword in a SQL statement. You can specify the applicable scope of a hint or of a table used in a hint by a **query block** introduced below. If you do not explicitly specify a query block for a hint, the hint affects the current query block by default.

### Query block

Each query or sub-query in a statement corresponds to a different query block, and each query block has its own `QB_NAME`. For example:

{{< copyable "sql" >}}

```sql
select * from (select * from t) t1, (select * from t) t2;
```

The above query statement has three query blocks: the outermost `SELECT` corresponds to the first query block, whose `QB_NAME` is `sel_1`; the two `SELECT` sub-queries correspond to the second and the third query block, whose `QB_NAME`s are `sel_2` and `sel_3`, respectively. The sequence of the numbers is based on the appearance of `SELECT` from left to right. If you replace the first `SELECT` with `DELETE` or `UPDATE`, then the corresponding `QB_NAME` is `del_1` or `upd_1`.

### QB_NAME

You can specify a query block's `QB_NAME` to a value that is different from the default name. In this case, the specified `QB_NAME` and the default `QB_NAME` are both valid. For example:

{{< copyable "sql" >}}

```sql
select /*+ QB_NAME(QB1) */ * from (select * from t) t1, (select * from t) t2;
```

This hint means that the `SELECT` query block's name is specified to `QB1`, which makes `QB1` and the default name `sel_1` both valid for the query block.

> **Note:**
>
> In the above example, if the hint specifies the `QB_NAME` to `sel_2` and does not specify a new `QB_NAME` for the original second `SELECT` query block, then `sel_2` becomes an invalid name for the second `SELECT` query block.

### @QB_NAME

`@QB_NAME` is an optional parameter that specifies the query block to which an optimizer-controlling hint (except `QB_NAME`) applies. If the hint includes a leading `@QB_NAME`, the hint applies to the named query block. If there is no leading `@QB_NAME`, the hint applies to the query block where it occurs. Also, you can append `@QB_NAME` to each table name of a hint to specify which query block the table belongs to. For example:

{{< copyable "sql" >}}

```sql
select /*+ HASH_JOIN(@sel_1 t1@sel_1, t3) */ * from (select t1.a, t1.b from t t1, t t2 where t1.a = t2.a) t1, t t3 where t1.b = t3.b;
```

### MERGE_JOIN(t1_name [, tl_name ...])

The `MERGE_JOIN(t1_name [, tl_name ...])` hint tells the optimizer to use the sort-merge join algorithm for the given table(s). Generally, this algorithm consumes less memory but takes longer processing time. If there is a very large data volume or insufficient system memory, it is recommended to use this hint. For example:

{{< copyable "sql" >}}

```sql
select /*+ MERGE_JOIN(t1, t2) */ * from t1，t2 where t1.id = t2.id;
```

> **Note:**
>
> `TIDB_SMJ` is the alias for `MERGE_JOIN` in TiDB 3.0.x and earlier versions. If you are using any of these versions, you must apply the `TIDB_SMJ(t1_name [, tl_name ...])` syntax for the hint. For the later versions of TiDB, `TIDB_SMJ` and `MERGE_JOIN` are both valid names for the hint.

### INL_JOIN(t1_name [, tl_name ...])

The `INL_JOIN(t1_name [, tl_name ...])` hint tells the optimizer to use the index nested loop join algorithm for the given table(s). This algorithm might consume less system resources and take shorter processing time in some scenarios and might produce an opposite result in other scenarios. If the result set is less than 10,000 rows after the outer table is filtered by the `WHERE` condition, it is recommended to use this hint. For example:

{{< copyable "sql" >}}

```sql
select /*+ INL_JOIN(t1, t2) */ * from t1，t2 where t1.id = t2.id;
```

The parameter(s) given in `INL_JOIN()` is the candidate table for the inner table when you create the query plan. For example, `INL_JOIN(t1)` means that TiDB only considers using `t1` as the inner table to create a query plan. If the candidate table has an alias, you must use the alias as the parameter in `INL_JOIN()`; if it does not has an alias, use the table's original name as the parameter. For example, in the `select /*+ INL_JOIN(t1) */ * from t t1, t t2 where t1.a = t2.b;` query, you must use the `t` table's alias `t1` or `t2` rather than `t` as `INL_JOIN()`'s parameter.

> **Note:**
>
> `TIDB_INLJ` is the alias for `INL_JOIN` in TiDB 3.0.x and earlier versions. If you are using any of these versions, you must apply the `TIDB_INLJ(t1_name [, tl_name ...])` syntax for the hint. For the later versions of TiDB, `TIDB_INLJ` and `INL_JOIN` are both valid names for the hint.

### INL_HASH_JOIN

The `INL_HASH_JOIN(t1_name [, tl_name])` hint tells the optimizer to use the index nested loop hash join algorithm. The conditions for using this algorithm are the same with the conditions for using the index nested loop join algorithm, but in some scenarios the index nested loop hash join algorithm uses less memory.

### INL_MERGE_JOIN

The `INL_MERGE_JOIN(t1_name [, tl_name])` hint tells the optimizer to use the index nested loop merge join algorithm, which consumes less memory than using `INL_JOIN`. The conditions for using this algorithm include all the conditions for using `INL_JOIN` but with one more: the column sets of the inner table in join keys is the prefix of the inner table, or the index of the inner table is the prefix of the column sets of the inner table in join keys.

### HASH_JOIN(t1_name [, tl_name ...])

The `HASH_JOIN(t1_name [, tl_name ...])` hint tells the optimizer to use the hash join algorithm for the given table(s). This algorithm allows the query to be executed concurrently with multiple threads, which achieves a higher processing speed but consumes more memory. For example:

{{< copyable "sql" >}}

```sql
select /*+ HASH_JOIN(t1, t2) */ * from t1，t2 where t1.id = t2.id;
```

> **Note:**
>
> `TIDB_HJ` is the alias for `HASH_JOIN` in TiDB 3.0.x and earlier versions. If you are using any of these versions, you must apply the `TIDB_HJ(t1_name [, tl_name ...])` syntax for the hint. For the later versions of TiDB, `TIDB_HJ` and `HASH_JOIN` are both valid names for the hint.

### HASH_AGG()

The `HASH_AGG()` hint tells the optimizer to use the hash aggregation algorithm. This algorithm allows the query to be executed concurrently with multiple threads, which achieves a higher processing speed but consumes more memory. For example:

{{< copyable "sql" >}}

```sql
select /*+ HASH_AGG() */ count(*) from t1，t2 where t1.a > 10 group by t1.id;
```

### STREAM_AGG()

The `STREAM_AGG()` hint tells the optimizer to use the stream aggregation algorithm. Generally, this algorithm consumes less memory but takes longer processing time. If there is a very large data volume or insufficient system memory, it is recommended to use this hint. For example:

{{< copyable "sql" >}}

```sql
select /*+ STREAM_AGG() */ count(*) from t1，t2 where t1.a > 10 group by t1.id;
```

### USE_INDEX(t1_name, idx1_name [, idx2_name ...])

The `USE_INDEX(t1_name, idx1_name [, idx2_name ...])` hint tells the optimizer to use only the given index(es) for a specified `t1_name` table. For example, applying the following hint has the same effect as executing the `select * from t t1 use index(idx1, idx2);` statement.

{{< copyable "sql" >}}

```sql
select /*+ USE_INDEX(t1, idx1, idx2) */ * from t t1;
```

### IGNORE_INDEX(t1_name, idx1_name [, idx2_name ...])

The `IGNORE_INDEX(t1_name, idx1_name [, idx2_name ...])` hint tells the optimizer to ignore the given index(es) for a specified `t1_name` table. For example, applying the following hint has the same effect as executing the `select * from t t1 ignore index(idx1, idx2);` statement.

{{< copyable "sql" >}}

```sql
select /*+ IGNORE_INDEX(t1, idx1, idx2) */ * from t t1;
```

### AGG_TO_COP()

The `AGG_TO_COP()` hint tells the optimizer to push down the aggregate operation to the coprocessor. If the optimizer does not push down some aggregate function that is suitable for pushdown, then it is recommended to use this hint. For example:

{{< copyable "sql" >}}

```sql
select /*+ AGG_TO_COP() */ sum(t1.a) from t t1;
```

### READ_FROM_STORAGE(TIFLASH[t1_name [, tl_name ...]], TIKV[t2_name [, tl_name ...]])

The `READ_FROM_STORAGE(TIFLASH[t1_name [, tl_name ...]], TIKV[t2_name [, tl_name ...]])` hint tells the optimizer to read specific table(s) from specific storage engine(s). Currently, this hint supports two storage engine parameters - `TIKV` and `TIFLASH`. For example:

{{< copyable "sql" >}}

```sql
select /*+ READ_FROM_STORAGE(TIFLASH[t1], TIKV[t2]) */ t1.a from t t1, t t2 where t1.a = t2.a;
```

### USE_INDEX_MERGE(t1_name, idx1_name [, idx2_name ...])

The `USE_INDEX_MERGE(t1_name, idx1_name [, idx2_name ...])` hint tells the optimizer to access a specific table with the index merge method. The given list of indexes are optional parameters. If you explicitly specify the list, TiDB selects indexes from the list to build index merge; if you do not give the list of indexes, TiDB selects indexes from all available indexes to build index merge. For example:

{{< copyable "sql" >}}

```sql
select /*+ USE_INDEX_MERGE(t1, idx_a, idx_b, idx_c) */ * from t t1 where t1.a > 10 or t1.b > 10;
```

> **Note:**
>
> The parameters of `USE_INDEX_MERGE` refer to index names, rather than column names. The index name of the primary key is `primary`.

### NO_INDEX_MERGE()

The `NO_INDEX_MERGE()` hint disables the index merge feature of the optimizer.

For example, the following query will not use index merge:

{{< copyable "sql" >}}

```sql
select /*+ NO_INDEX_MERGE() */ * from t where t.a > 0 or t.b > 0;
```

In addition to this hint, setting the `tidb_enable_index_merge` environment variable also controls whether to enable this feature.

### USE_TOJA(boolean_value)

The `boolean_value` parameter can be `TRUE` or `FALSE`. The `USE_TOJA(TRUE)` hint enables the optimizer to convert an `in` condition (containing a sub-query) to join and aggregation operations. Comparatively, the `USE_TOJA(FALSE)` hint disables this feature.

For example, the following query will convert `in (select t2.a from t2) subq` to corresponding join and aggregation operations:

{{< copyable "sql" >}}

```sql
select /*+ USE_TOJA(TRUE) */ t1.a, t1.b from t1 where t1.a in (select t2.a from t2) subq;
```

In addition to this hint, setting the `tidb_opt_insubq_to_join_and_agg` environment variable also controls whether to enable this feature.

## Hints for setting operation parameters

A hint for setting operation parameters follows behind **the first** `SELECT`, `UPDATE` or `DELETE` keyword in a SQL statement. A hint of this category modifies the operation parameter of the query to which this hint applies.

The hints' priority is higher than the default setting and the environment setting.

### MAX_EXECUTION_TIME(N)

The `MAX_EXECUTION_TIME(N)` hint places a limit `N` (a timeout value in milliseconds) on how long a statement is permitted to execute before the server terminates it. In the following hint, `MAX_EXECUTION_TIME(1000)` means that the timeout is 1000 milliseconds (that is, 1 second):

{{< copyable "sql" >}}

```sql
select /*+ MAX_EXECUTION_TIME(1000) */ * from t1 inner join t2 where t1.id = t2.id;
```

In addition to this hint, the `global.max_execution_time` global variable can also limit the execution time of a statement.

### MEMORY_QUOTA(N)

The `MEMORY_QUOTA(N)` hint places a limit `N` (a threshold value in MB or GB) on how much memory a statement is permitted to use. When a statement's memory usage exceeds this limit, TiDB produces a log message based on the statement's over-limit behavior or just terminates it.

In the following hint, `MEMORY_QUOTA(1024 MB)` means that the memory usage is limited to 1024 MB:

{{< copyable "sql" >}}

```sql
select /*+ MEMORY_QUOTA(1024 MB) */ * from t;
```

In addition to this hint, the `tidb_mem_quota_query` environment variable can also limit the memory usage of a statement.

### READ_FROM_REPLICA()

The `READ_FROM_REPLICA()` hint enables the feature of reading consistent data from the TiKV follower node. For example:

{{< copyable "sql" >}}

```sql
select /*+ READ_FROM_REPLICA() */ * from t;
```

In addition to this hint, setting the `tidb_replica_read` environment variable to `'follower'` or `'leader'` also controls whether to enable this feature.

### IGNORE_PLAN_CACHE()

`IGNORE_PLAN_CACHE()` reminds the optimizer not to use the Plan Cache when handling the current `prepare` statement.

This hint is used to temporarily disable the Plan Cache when [prepare-plan-cache](/tidb-configuration-file.md#prepared-plan-cache) is enabled.

In the following example, the Plan Cache is forcibly disabled when executing the `prepare` statement.

{{< copyable "sql" >}}

```sql
prepare stmt from 'select  /*+ IGNORE_PLAN_CACHE() */ * from t where t.id = ?';
```
