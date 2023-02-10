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

Optimizer hints are case insensitive and specified within `/*+ ... */` comments following the `SELECT`, `UPDATE` or `DELETE` keyword in a SQL statement. Optimizer hints are not currently supported for `INSERT` statements.

 Multiple hints can be specified by separating with commas. For example, the following query uses three different hints:

{{< copyable "sql" >}}

```sql
SELECT /*+ USE_INDEX(t1, idx1), HASH_AGG(), HASH_JOIN(t1) */ count(*) FROM t t1, t t2 WHERE t1.a = t2.b;
```

How optimizer hints affect query execution plans can be observed in the output of [`EXPLAIN`](/sql-statements/sql-statement-explain.md) and [`EXPLAIN ANALYZE`](/sql-statements/sql-statement-explain-analyze.md).

An incorrect or incomplete hint will not result in a statement error. This is because hints are intended to have only a _hint_ (suggestion) semantic to query execution. Similarly, TiDB will at most return a warning if a hint is not applicable.

> **Note:**
>
> If the comments do not follow behind the specified keywords, they will be treated as common MySQL comments. The comments do not take effect, and no warning is reported.

Currently, TiDB supports two categories of hints, which are different in scope. The first category of hints takes effect in the scope of query blocks, such as [`/*+ HASH_AGG() */`](#hash_agg); the second category of hints takes effect in the whole query, such as [`/*+ MEMORY_QUOTA(1024 MB)*/`](#memory_quotan).

Each query or sub-query in a statement corresponds to a different query block, and each query block has its own name. For example:

{{< copyable "sql" >}}

```sql
SELECT * FROM (SELECT * FROM t) t1, (SELECT * FROM t) t2;
```

The above query statement has three query blocks: the outermost `SELECT` corresponds to the first query block, whose name is `sel_1`; the two `SELECT` sub-queries correspond to the second and the third query block, whose names are `sel_2` and `sel_3`, respectively. The sequence of the numbers is based on the appearance of `SELECT` from left to right. If you replace the first `SELECT` with `DELETE` or `UPDATE`, then the corresponding query block names are `del_1` or `upd_1`.

## Hints that take effect in query blocks

This category of hints can follow behind **any** `SELECT`, `UPDATE` or `DELETE` keywords. To control the effective scope of the hint, use the name of the query block in the hint. You can make the hint parameters clear by accurately identifying each table in the query (in case of duplicated table names or aliases). If no query block is specified in the hint, the hint takes effect in the current block by default.

For example:

{{< copyable "sql" >}}

```sql
SELECT /*+ HASH_JOIN(@sel_1 t1@sel_1, t3) */ * FROM (SELECT t1.a, t1.b FROM t t1, t t2 WHERE t1.a = t2.a) t1, t t3 WHERE t1.b = t3.b;
```

This hint takes effect in the `sel_1` query block, and its parameters are the `t1` and `t3` tables in `sel_1` (`sel_2` also contains a `t1` table).

As described above, you can specify the name of the query block in the hint in the following ways:

- Set the query block name as the first parameter of the hint, and separate it from other parameters with a space. In addition to `QB_NAME`, all the hints listed in this section also have another optional hidden parameter `@QB_NAME`. By using this parameter, you can specify the effective scope of this hint.
- Append `@QB_NAME` to a table name in the parameter to explicitly specify which query block this table belongs to.

> **Note:**
>
> You must put the hint in or before the query block where the hint takes effect. If the hint is put after the query block, it cannot take effect.

### QB_NAME

If the query statement is a complicated statement that includes multiple nested queries, the ID and name of a certain query block might be mistakenly identified. The hint `QB_NAME` can help us in this regard.

`QB_NAME` means Query Block Name. You can specify a new name to a query block. The specified `QB_NAME` and the previous default name are both valid. For example:

{{< copyable "sql" >}}

```sql
SELECT /*+ QB_NAME(QB1) */ * FROM (SELECT * FROM t) t1, (SELECT * FROM t) t2;
```

This hint specifies the outer `SELECT` query block's name to `QB1`, which makes `QB1` and the default name `sel_1` both valid for the query block.

> **Note:**
>
> In the above example, if the hint specifies the `QB_NAME` to `sel_2` and does not specify a new `QB_NAME` for the original second `SELECT` query block, then `sel_2` becomes an invalid name for the second `SELECT` query block.

### MERGE_JOIN(t1_name [, tl_name ...])

The `MERGE_JOIN(t1_name [, tl_name ...])` hint tells the optimizer to use the sort-merge join algorithm for the given table(s). Generally, this algorithm consumes less memory but takes longer processing time. If there is a very large data volume or insufficient system memory, it is recommended to use this hint. For example:

{{< copyable "sql" >}}

```sql
select /*+ MERGE_JOIN(t1, t2) */ * from t1, t2 where t1.id = t2.id;
```

> **Note:**
>
> `TIDB_SMJ` is the alias for `MERGE_JOIN` in TiDB 3.0.x and earlier versions. If you are using any of these versions, you must apply the `TIDB_SMJ(t1_name [, tl_name ...])` syntax for the hint. For the later versions of TiDB, `TIDB_SMJ` and `MERGE_JOIN` are both valid names for the hint, but `MERGE_JOIN` is recommended.

### INL_JOIN(t1_name [, tl_name ...])

The `INL_JOIN(t1_name [, tl_name ...])` hint tells the optimizer to use the index nested loop join algorithm for the given table(s). This algorithm might consume less system resources and take shorter processing time in some scenarios and might produce an opposite result in other scenarios. If the result set is less than 10,000 rows after the outer table is filtered by the `WHERE` condition, it is recommended to use this hint. For example:

{{< copyable "sql" >}}

```sql
select /*+ INL_JOIN(t1, t2) */ * from t1, t2 where t1.id = t2.id;
```

The parameter(s) given in `INL_JOIN()` is the candidate table for the inner table when you create the query plan. For example, `INL_JOIN(t1)` means that TiDB only considers using `t1` as the inner table to create a query plan. If the candidate table has an alias, you must use the alias as the parameter in `INL_JOIN()`; if it does not has an alias, use the table's original name as the parameter. For example, in the `select /*+ INL_JOIN(t1) */ * from t t1, t t2 where t1.a = t2.b;` query, you must use the `t` table's alias `t1` or `t2` rather than `t` as `INL_JOIN()`'s parameter.

> **Note:**
>
> `TIDB_INLJ` is the alias for `INL_JOIN` in TiDB 3.0.x and earlier versions. If you are using any of these versions, you must apply the `TIDB_INLJ(t1_name [, tl_name ...])` syntax for the hint. For the later versions of TiDB, `TIDB_INLJ` and `INL_JOIN` are both valid names for the hint, but `INL_JOIN` is recommended.

### INL_HASH_JOIN

The `INL_HASH_JOIN(t1_name [, tl_name])` hint tells the optimizer to use the index nested loop hash join algorithm. The conditions for using this algorithm are the same with the conditions for using the index nested loop join algorithm. The difference between the two algorithms is that `INL_JOIN` creates a hash table on the joined inner table, but `INL_HASH_JOIN` creates a hash table on the joined outer table. `INL_HASH_JOIN` has a fixed limit on memory usage, while the memory used by `INL_JOIN` depends on the number of rows matched in the inner table.

### HASH_JOIN(t1_name [, tl_name ...])

The `HASH_JOIN(t1_name [, tl_name ...])` hint tells the optimizer to use the hash join algorithm for the given table(s). This algorithm allows the query to be executed concurrently with multiple threads, which achieves a higher processing speed but consumes more memory. For example:

{{< copyable "sql" >}}

```sql
select /*+ HASH_JOIN(t1, t2) */ * from t1, t2 where t1.id = t2.id;
```

> **Note:**
>
> `TIDB_HJ` is the alias for `HASH_JOIN` in TiDB 3.0.x and earlier versions. If you are using any of these versions, you must apply the `TIDB_HJ(t1_name [, tl_name ...])` syntax for the hint. For the later versions of TiDB, `TIDB_HJ` and `HASH_JOIN` are both valid names for the hint, but `HASH_JOIN` is recommended.

### HASH_JOIN_BUILD(t1_name [, tl_name ...])

The `HASH_JOIN_BUILD(t1_name [, tl_name ...])` hint tells the optimizer to use the hash join algorithm on specified tables with these tables working as the build side. In this way, you can build hash tables using specific tables. For example:

```sql
SELECT /*+ HASH_JOIN_BUILD(t1) */ * FROM t1, t2 WHERE t1.id = t2.id;
```

### HASH_JOIN_PROBE(t1_name [, tl_name ...])

The `HASH_JOIN_PROBE(t1_name [, tl_name ...])` hint tells the optimizer to use the hash join algorithm on specified tables with these tables working as the probe side. In this way, you can execute the hash join algorithm with specific tables as the probe side. For example:

```sql
SELECT /*+ HASH_JOIN_PROBE(t2) */ * FROM t1, t2 WHERE t1.id = t2.id;
```

### SEMI_JOIN_REWRITE()

The `SEMI_JOIN_REWRITE()` hint tells the optimizer to rewrite the semi-join query to an ordinary join query. Currently, this hint only works for `EXISTS` subqueries.

If this hint is not used to rewrite the query, when the hash join is selected in the execution plan, the semi-join query can only use the subquery to build a hash table. In this case, when the result of the subquery is bigger than that of the outer query, the execution speed might be slower than expected.

Similarly, when the index join is selected in the execution plan, the semi-join query can only use the outer query as the driving table. In this case, when the result of the subquery is smaller than that of the outer query, the execution speed might be slower than expected.

When `SEMI_JOIN_REWRITE()` is used to rewrite the query, the optimizer can extend the selection range to select a better execution plan.

{{< copyable "sql" >}}

```sql
-- Does not use SEMI_JOIN_REWRITE() to rewrite the query.
EXPLAIN SELECT * FROM t WHERE EXISTS (SELECT 1 FROM t1 WHERE t1.a = t.a);
```

```sql
+-----------------------------+---------+-----------+------------------------+---------------------------------------------------+
| id                          | estRows | task      | access object          | operator info                                     |
+-----------------------------+---------+-----------+------------------------+---------------------------------------------------+
| MergeJoin_9                 | 7992.00 | root      |                        | semi join, left key:test.t.a, right key:test.t1.a |
| ├─IndexReader_25(Build)     | 9990.00 | root      |                        | index:IndexFullScan_24                            |
| │ └─IndexFullScan_24        | 9990.00 | cop[tikv] | table:t1, index:idx(a) | keep order:true, stats:pseudo                     |
| └─IndexReader_23(Probe)     | 9990.00 | root      |                        | index:IndexFullScan_22                            |
|   └─IndexFullScan_22        | 9990.00 | cop[tikv] | table:t, index:idx(a)  | keep order:true, stats:pseudo                     |
+-----------------------------+---------+-----------+------------------------+---------------------------------------------------+
```

{{< copyable "sql" >}}

```sql
-- Uses SEMI_JOIN_REWRITE() to rewrite the query.
EXPLAIN SELECT * FROM t WHERE EXISTS (SELECT /*+ SEMI_JOIN_REWRITE() */ 1 FROM t1 WHERE t1.a = t.a);
```

```sql
+------------------------------+---------+-----------+------------------------+---------------------------------------------------------------------------------------------------------------+
| id                           | estRows | task      | access object          | operator info                                                                                                 |
+------------------------------+---------+-----------+------------------------+---------------------------------------------------------------------------------------------------------------+
| IndexJoin_16                 | 1.25    | root      |                        | inner join, inner:IndexReader_15, outer key:test.t1.a, inner key:test.t.a, equal cond:eq(test.t1.a, test.t.a) |
| ├─StreamAgg_39(Build)        | 1.00    | root      |                        | group by:test.t1.a, funcs:firstrow(test.t1.a)->test.t1.a                                                      |
| │ └─IndexReader_34           | 1.00    | root      |                        | index:IndexFullScan_33                                                                                        |
| │   └─IndexFullScan_33       | 1.00    | cop[tikv] | table:t1, index:idx(a) | keep order:true                                                                                               |
| └─IndexReader_15(Probe)      | 1.25    | root      |                        | index:Selection_14                                                                                            |
|   └─Selection_14             | 1.25    | cop[tikv] |                        | not(isnull(test.t.a))                                                                                         |
|     └─IndexRangeScan_13      | 1.25    | cop[tikv] | table:t, index:idx(a)  | range: decided by [eq(test.t.a, test.t1.a)], keep order:false, stats:pseudo                                   |
+------------------------------+---------+-----------+------------------------+---------------------------------------------------------------------------------------------------------------+
```

From the preceding example, you can see that when using the `SEMI_JOIN_REWRITE()` hint, TiDB can select the execution method of IndexJoin based on the driving table `t1`.

### NO_DECORRELATE()

The `NO_DECORRELATE()` hint tells the optimizer not to try to perform decorrelation for the correlated subquery in the specified query block. This hint is applicable to the `EXISTS`, `IN`, `ANY`, `ALL`, `SOME` subqueries and scalar subqueries that contain correlated columns (that is, correlated subqueries).

When this hint is used in a query block, the optimizer will not try to perform decorrelation for the correlated columns between the subquery and its outer query block, but always use the Apply operator to execute the query.

By default, TiDB tries to [perform decorrelation](/correlated-subquery-optimization.md) for correlated subqueries to achieve higher execution efficiency. However, in [some scenarios](/correlated-subquery-optimization.md#restrictions), decorrelation might actually reduce the execution efficiency. In this case, you can use this hint to manually tell the optimizer not to perform decorrelation. For example:

{{< copyable "sql" >}}

```sql
create table t1(a int, b int);
create table t2(a int, b int, index idx(b));
```

{{< copyable "sql" >}}

```sql
-- Not using NO_DECORRELATE().
explain select * from t1 where t1.a < (select sum(t2.a) from t2 where t2.b = t1.b);
```

```sql
+----------------------------------+----------+-----------+---------------+--------------------------------------------------------------------------------------------------------------+
| id                               | estRows  | task      | access object | operator info                                                                                                |
+----------------------------------+----------+-----------+---------------+--------------------------------------------------------------------------------------------------------------+
| HashJoin_11                      | 9990.00  | root      |               | inner join, equal:[eq(test.t1.b, test.t2.b)], other cond:lt(cast(test.t1.a, decimal(10,0) BINARY), Column#7) |
| ├─HashAgg_23(Build)              | 7992.00  | root      |               | group by:test.t2.b, funcs:sum(Column#8)->Column#7, funcs:firstrow(test.t2.b)->test.t2.b                      |
| │ └─TableReader_24               | 7992.00  | root      |               | data:HashAgg_16                                                                                              |
| │   └─HashAgg_16                 | 7992.00  | cop[tikv] |               | group by:test.t2.b, funcs:sum(test.t2.a)->Column#8                                                           |
| │     └─Selection_22             | 9990.00  | cop[tikv] |               | not(isnull(test.t2.b))                                                                                       |
| │       └─TableFullScan_21       | 10000.00 | cop[tikv] | table:t2      | keep order:false, stats:pseudo                                                                               |
| └─TableReader_15(Probe)          | 9990.00  | root      |               | data:Selection_14                                                                                            |
|   └─Selection_14                 | 9990.00  | cop[tikv] |               | not(isnull(test.t1.b))                                                                                       |
|     └─TableFullScan_13           | 10000.00 | cop[tikv] | table:t1      | keep order:false, stats:pseudo                                                                               |
+----------------------------------+----------+-----------+---------------+--------------------------------------------------------------------------------------------------------------+
```

From the preceding execution plan, you can see that the optimizer has automatically performed decorrelation. The decorrelated execution plan does not have the Apply operator. Instead, the plan has join operations between the subquery and the outer query block. The original filter condition (`t2.b = t1.b`) with the correlated column becomes a regular join condition.

{{< copyable "sql" >}}

```sql
-- Using NO_DECORRELATE().
explain select * from t1 where t1.a < (select /*+ NO_DECORRELATE() */ sum(t2.a) from t2 where t2.b = t1.b);
```

```sql
+------------------------------------------+-----------+-----------+------------------------+--------------------------------------------------------------------------------------+
| id                                       | estRows   | task      | access object          | operator info                                                                        |
+------------------------------------------+-----------+-----------+------------------------+--------------------------------------------------------------------------------------+
| Projection_10                            | 10000.00  | root      |                        | test.t1.a, test.t1.b                                                                 |
| └─Apply_12                               | 10000.00  | root      |                        | CARTESIAN inner join, other cond:lt(cast(test.t1.a, decimal(10,0) BINARY), Column#7) |
|   ├─TableReader_14(Build)                | 10000.00  | root      |                        | data:TableFullScan_13                                                                |
|   │ └─TableFullScan_13                   | 10000.00  | cop[tikv] | table:t1               | keep order:false, stats:pseudo                                                       |
|   └─MaxOneRow_15(Probe)                  | 10000.00  | root      |                        |                                                                                      |
|     └─StreamAgg_20                       | 10000.00  | root      |                        | funcs:sum(Column#14)->Column#7                                                       |
|       └─Projection_45                    | 100000.00 | root      |                        | cast(test.t2.a, decimal(10,0) BINARY)->Column#14                                     |
|         └─IndexLookUp_44                 | 100000.00 | root      |                        |                                                                                      |
|           ├─IndexRangeScan_42(Build)     | 100000.00 | cop[tikv] | table:t2, index:idx(b) | range: decided by [eq(test.t2.b, test.t1.b)], keep order:false, stats:pseudo         |
|           └─TableRowIDScan_43(Probe)     | 100000.00 | cop[tikv] | table:t2               | keep order:false, stats:pseudo                                                       |
+------------------------------------------+-----------+-----------+------------------------+--------------------------------------------------------------------------------------+
```

From the preceding execution plan, you can see that the optimizer does not perform decorrelation. The execution plan still contains the Apply operator. The filter condition (`t2.b = t1.b`) with the correlated column is still the filter condition when accessing the `t2` table.

### HASH_AGG()

The `HASH_AGG()` hint tells the optimizer to use the hash aggregation algorithm in all the aggregate functions in the specified query block. This algorithm allows the query to be executed concurrently with multiple threads, which achieves a higher processing speed but consumes more memory. For example:

{{< copyable "sql" >}}

```sql
select /*+ HASH_AGG() */ count(*) from t1, t2 where t1.a > 10 group by t1.id;
```

### STREAM_AGG()

The `STREAM_AGG()` hint tells the optimizer to use the stream aggregation algorithm in all the aggregate functions in the specified query block. Generally, this algorithm consumes less memory but takes longer processing time. If there is a very large data volume or insufficient system memory, it is recommended to use this hint. For example:

{{< copyable "sql" >}}

```sql
select /*+ STREAM_AGG() */ count(*) from t1, t2 where t1.a > 10 group by t1.id;
```

### USE_INDEX(t1_name, idx1_name [, idx2_name ...])

The `USE_INDEX(t1_name, idx1_name [, idx2_name ...])` hint tells the optimizer to use only the given index(es) for a specified `t1_name` table. For example, applying the following hint has the same effect as executing the `select * from t t1 use index(idx1, idx2);` statement.

{{< copyable "sql" >}}

```sql
SELECT /*+ USE_INDEX(t1, idx1, idx2) */ * FROM t1;
```

> **Note:**
>
> If you specify only the table name but not index name in this hint, the execution does not consider any index but scan the entire table.

### FORCE_INDEX(t1_name, idx1_name [, idx2_name ...])

The `FORCE_INDEX(t1_name, idx1_name [, idx2_name ...])` hint tells the optimizer to use only the given index(es).

The usage and effect of `FORCE_INDEX(t1_name, idx1_name [, idx2_name ...])` are the same as the usage and effect of `USE_INDEX(t1_name, idx1_name [, idx2_name ...])`.

The following 4 queries have the same effect:

{{< copyable "sql" >}}

```sql
SELECT /*+ USE_INDEX(t, idx1) */ * FROM t;
SELECT /*+ FORCE_INDEX(t, idx1) */ * FROM t;
SELECT * FROM t use index(idx1);
SELECT * FROM t force index(idx1);
```

### IGNORE_INDEX(t1_name, idx1_name [, idx2_name ...])

The `IGNORE_INDEX(t1_name, idx1_name [, idx2_name ...])` hint tells the optimizer to ignore the given index(es) for a specified `t1_name` table. For example, applying the following hint has the same effect as executing the `select * from t t1 ignore index(idx1, idx2);` statement.

{{< copyable "sql" >}}

```sql
select /*+ IGNORE_INDEX(t1, idx1, idx2) */ * from t t1;
```

### ORDER_INDEX(t1_name, idx1_name [, idx2_name ...])

The `ORDER_INDEX(t1_name, idx1_name [, idx2_name ...])` hint tells the optimizer to use only the given index for a specified table and read the specified index in order.

> **Warning:**
>
> This hint might cause SQL statements to fail. It is recommended to test it first. If an error occurs during the test, remove the hint. If the test runs normally, you can continue using it.

This hint is usually applied in the following scenario:

```sql
CREATE TABLE t(a INT, b INT, key(a), key(b));
EXPLAIN SELECT /*+ ORDER_INDEX(t, a) */ a FROM t ORDER BY a LIMIT 10;
```

```sql
+----------------------------+---------+-----------+---------------------+-------------------------------+
| id                         | estRows | task      | access object       | operator info                 |
+----------------------------+---------+-----------+---------------------+-------------------------------+
| Limit_10                   | 10.00   | root      |                     | offset:0, count:10            |
| └─IndexReader_14           | 10.00   | root      |                     | index:Limit_13                |
|   └─Limit_13               | 10.00   | cop[tikv] |                     | offset:0, count:10            |
|     └─IndexFullScan_12     | 10.00   | cop[tikv] | table:t, index:a(a) | keep order:true, stats:pseudo |
+----------------------------+---------+-----------+---------------------+-------------------------------+
```

The optimizer generates two types of plan for this query: `Limit + IndexScan(keep order: true)` and `TopN + IndexScan(keep order: false)`. When the `ORDER_INDEX` hint is used, the optimizer chooses the first plan that reads the index in order.

> **Note:**
>
> - If the query itself does not need to read the index in order (that is, without a hint, the optimizer does not generate a plan that reads the index in order in any situation), when the `ORDER_INDEX` hint is used, the error `Can't find a proper physical plan for this query` occurs. In this case, you need to remove the corresponding `ORDER_INDEX` hint.
> - The index on a partitioned table cannot be read in order, so do not use the `ORDER_INDEX` hint on the partitioned table and its related indexes.

### NO_ORDER_INDEX(t1_name, idx1_name [, idx2_name ...])

The `NO_ORDER_INDEX(t1_name, idx1_name [, idx2_name ...])` hint tells the optimizer to use only the given index for a specified table and not to read the specified index in order. This hint is usually applied in the following scenario.

The following example shows that the effect of the query statement is equivalent to `SELECT * FROM t t1 use index(idx1, idx2);`:

```sql
CREATE TABLE t(a INT, b INT, key(a), key(b));
EXPLAIN SELECT /*+ NO_ORDER_INDEX(t, a) */ a FROM t ORDER BY a LIMIT 10;
```

```sql
+----------------------------+----------+-----------+---------------------+--------------------------------+
| id                         | estRows  | task      | access object       | operator info                  |
+----------------------------+----------+-----------+---------------------+--------------------------------+
| TopN_7                     | 10.00    | root      |                     | test.t.a, offset:0, count:10   |
| └─IndexReader_14           | 10.00    | root      |                     | index:TopN_13                  |
|   └─TopN_13                | 10.00    | cop[tikv] |                     | test.t.a, offset:0, count:10   |
|     └─IndexFullScan_12     | 10000.00 | cop[tikv] | table:t, index:a(a) | keep order:false, stats:pseudo |
+----------------------------+----------+-----------+---------------------+--------------------------------+
```

The same as the example of `ORDER_INDEX` hint, the optimizer generates two types of plans for this query: `Limit + IndexScan(keep order: true)` and `TopN + IndexScan(keep order: false)`. When the `NO_ORDER_INDEX` hint is used, the optimizer will choose the latter plan to read the index out of order.

### AGG_TO_COP()

The `AGG_TO_COP()` hint tells the optimizer to push down the aggregate operation in the specified query block to the coprocessor. If the optimizer does not push down some aggregate function that is suitable for pushdown, then it is recommended to use this hint. For example:

{{< copyable "sql" >}}

```sql
select /*+ AGG_TO_COP() */ sum(t1.a) from t t1;
```

### LIMIT_TO_COP()

The `LIMIT_TO_COP()` hint tells the optimizer to push down the `Limit` and `TopN` operators in the specified query block to the coprocessor. If the optimizer does not perform such an operation, it is recommended to use this hint. For example:

{{< copyable "sql" >}}

```sql
SELECT /*+ LIMIT_TO_COP() */ * FROM t WHERE a = 1 AND b > 10 ORDER BY c LIMIT 1;
```

### READ_FROM_STORAGE(TIFLASH[t1_name [, tl_name ...]], TIKV[t2_name [, tl_name ...]])

The `READ_FROM_STORAGE(TIFLASH[t1_name [, tl_name ...]], TIKV[t2_name [, tl_name ...]])` hint tells the optimizer to read specific table(s) from specific storage engine(s). Currently, this hint supports two storage engine parameters - `TIKV` and `TIFLASH`. If a table has an alias, use the alias as the parameter of `READ_FROM_STORAGE()`; if the table does not has an alias, use the table's original name as the parameter. For example:

{{< copyable "sql" >}}

```sql
select /*+ READ_FROM_STORAGE(TIFLASH[t1], TIKV[t2]) */ t1.a from t t1, t t2 where t1.a = t2.a;
```

> **Note:**
>
> If you want the optimizer to use a table from another schema, you need to explicitly specify the schema name. For example:
>
> ```sql
> SELECT /*+ READ_FROM_STORAGE(TIFLASH[test1.t1,test2.t2]) */ t1.a FROM test1.t t1, test2.t t2 WHERE t1.a = t2.a;
> ```

### USE_INDEX_MERGE(t1_name, idx1_name [, idx2_name ...])

The `USE_INDEX_MERGE(t1_name, idx1_name [, idx2_name ...])` hint tells the optimizer to access a specific table with the index merge method. Index merge has two types: intersection type and union type. For details, see [Explain Statements Using Index Merge](/explain-index-merge.md).

If you explicitly specify the list of indexes, TiDB selects indexes from the list to build index merge; if you do not specify the list of indexes, TiDB selects indexes from all available indexes to build index merge.

For the intersection-type index merge, the given list of indexes is a required parameter in the hint. For the union-type index merge, the given list of indexes is an optional parameter in the hint. See the following example.

{{< copyable "sql" >}}

```sql
SELECT /*+ USE_INDEX_MERGE(t1, idx_a, idx_b, idx_c) */ * FROM t1 WHERE t1.a > 10 OR t1.b > 10;
```

When multiple `USE_INDEX_MERGE` hints are made to the same table, the optimizer tries to select the index from the union of the index sets specified by these hints.

> **Note:**
>
> The parameters of `USE_INDEX_MERGE` refer to index names, rather than column names. The index name of the primary key is `primary`.

### LEADING(t1_name [, tl_name ...])

The `LEADING(t1_name [, tl_name ...])` hint reminds the optimizer that, when generating the execution plan, to determine the order of multi-table joins according to the order of table names specified in the hint. For example:

{{< copyable "sql" >}}

```sql
SELECT /*+ LEADING(t1, t2) */ * FROM t1, t2, t3 WHERE t1.id = t2.id and t2.id = t3.id;
```

In the above query with multi-table joins, the order of joins is determined by the order of table names specified in the `LEADING()` hint. The optimizer will first join `t1` and `t2` and then join the result with `t3`. This hint is more general than [`STRAIGHT_JOIN`](#straight_join).

The `LEADING` hint does not take effect in the following situations:

+ Multiple `LEADING` hints are specified.
+ The table name specified in the `LEADING` hint does not exist.
+ A duplicated table name is specified in the `LEADING` hint.
+ The optimizer cannot perform join operations according to the order as specified by the `LEADING` hint.
+ The `straight_join()` hint already exists.
+ The query contains an outer join together with the Cartesian product.
+ Any of the `MERGE_JOIN`, `INL_JOIN`, `INL_HASH_JOIN`, and `HASH_JOIN` hints is used at the same time.

In the above situations, a warning is generated.

```sql
-- Multiple `LEADING` hints are specified.
SELECT /*+ LEADING(t1, t2) LEADING(t3) */ * FROM t1, t2, t3 WHERE t1.id = t2.id and t2.id = t3.id;

-- To learn why the `LEADING` hint fails to take effect, execute `show warnings`.
SHOW WARNINGS;
```

```sql
+---------+------+-------------------------------------------------------------------------------------------------------------------+
| Level   | Code | Message                                                                                                           |
+---------+------+-------------------------------------------------------------------------------------------------------------------+
| Warning | 1815 | We can only use one leading hint at most, when multiple leading hints are used, all leading hints will be invalid |
+---------+------+-------------------------------------------------------------------------------------------------------------------+
```

> **Note:**
>
> If the query statement includes an outer join, in the hint you can specify only the tables whose join order can be swapped. If there is a table in the hint whose join order cannot be swapped, the hint will be invalid. For example, in `SELECT * FROM t1 LEFT JOIN (t2 JOIN t3 JOIN t4) ON t1.a = t2.a;`, if you want to control the join order of `t2`, `t3`, and `t4` tables, you cannot specify `t1` in the `LEADING` hint.

### MERGE()

Using the `MERGE()` hint in queries with common table expressions (CTE) can disable the materialization of the subqueries and expand the subquery inlines into CTE. This hint is only applicable to non-recursive CTE. In some scenarios, using `MERGE()` brings higher execution efficiency than the default behavior of allocating a temporary space. For example, pushing down query conditions or in nesting CTE queries:

```sql
-- Uses the hint to push down the predicate of the outer query.
WITH CTE AS (SELECT /*+ MERGE() */ * FROM tc WHERE tc.a < 60) SELECT * FROM CTE WHERE CTE.a < 18;

-- Uses the hint in a nested CTE query to expand a CTE inline into the outer query.
WITH CTE1 AS (SELECT * FROM t1), CTE2 AS (WITH CTE3 AS (SELECT /*+ MERGE() */ * FROM t2), CTE4 AS (SELECT * FROM t3) SELECT * FROM CTE3, CTE4) SELECT * FROM CTE1, CTE2;
```

> **Note:**
>
> `MERGE()` is only applicable to simple CTE queries. It is not applicable in the following situations:
>
> - [Recursive CTE](https://docs.pingcap.com/tidb/stable/dev-guide-use-common-table-expression#recursive-cte)
> - Subqueries with inlines that cannot be expanded, such as aggregate operators, window functions, and `DISTINCT`.
>
> When the number of CTE references is too high, the query performance might be lower than the default materialization behavior.

## Hints that take effect globally

The global hint works in [views](/views.md). When specified as a global hint, the hint defined in a query can take effect inside the view. To specify a global hint, first use the `QB_NAME` hint to define a query block name, and then add the target hints in the form of `ViewName@QueryBlockName`.

### Step 1: Define the query block name of the view using the `QB_NAME` hint

Use the [`QB_NAME` hint](#qb_name) to define a new name for each query block of the view. The definition of the `QB_NAME` hint for views is the same as that for [query blocks](#qb_name), but the syntax is extended from `QB_NAME(QB)` to `QB_NAME(QB, ViewName@QueryBlockName [.ViewName@QueryBlockName .ViewName@QueryBlockName ...])`.

> **Note:**
>
> There is a white space between `@QueryBlockName` and the immediately following `.ViewName@QueryBlockName`. Otherwise, the `.ViewName@QueryBlockName` will be treated as a part of the `QueryBlockName`. For example, `QB_NAME(v2_1, v2@SEL_1 .@SEL_1)` is valid, while `QB_NAME(v2_1, v2@SEL_1.@SEL_1)` cannot be parsed correctly.

- For a simple statement with a single view and no subqueries, the following example specifies the first query block name of view `v`:

    ```sql
    SELECT /* Comment: The name of the current query block is the default @SEL_1 */ * FROM v;
    ```

    For view `v`, the first view name in the list (`ViewName@QueryBlockName [.ViewName@QueryBlockName .ViewName@QueryBlockName ...]`) starting from the query statement is `v@SEL_1`. The first query block of the view `v` can be declared as `QB_NAME(v_1, v@SEL_1 .@SEL_1)`, or simply written as `QB_NAME(v_1, v)`, omitting `@SEL_1`:

    ```sql
    CREATE VIEW v AS SELECT /* Comment: The name of the current query block is the default @SEL_1 */ * FROM t;

    -- Specifies the global hint
    SELECT /*+ QB_NAME(v_1, v) USE_INDEX(t@v_1, idx) */ * FROM v;
    ```

- For a complex statement with nested views and subqueries, the following example specifies the names for each of two query blocks of the view `v1` and `v2`:

    ```sql
    SELECT /* Comment: The name of the current query block is the default @SEL_1 */ * FROM v2 JOIN (
        SELECT /* Comment: The name of the current query block is the default @SEL_2 */ * FROM v2) vv;
    ```

    For the first view `v2`, the first view name in the list starting from the first query statement is `v2@SEL_1`. For the second view `v2`, the first view name is `v2@SEL_2`. The following example only considers the first view `v2`.

    The first query block of view `v2` can be declared as `QB_NAME(v2_1, v2@SEL_1 .@SEL_1)`, and the second query block of the view `v2` can be declared as `QB_NAME(v2_2, v2@SEL_1 .@SEL_2)`:

    ```sql
    CREATE VIEW v2 AS
        SELECT * FROM t JOIN /* Comment: For view v2, the name of the current query block is the default @SEL_1. So, the current query block view list is v2@SEL_1 .@SEL_1 */
        (
            SELECT COUNT(*) FROM t1 JOIN v1 /* Comment: For view v2, the name of the current query block is the default @SEL_2. So, the current query block view list is v2@SEL_1 .@SEL_2 */
        ) tt;
    ```

    For view `v1`, the first view name in the list starting from the preceding statement is `v2@SEL_1 .v1@SEL_2`. The first query block in view `v1` can be declared as `QB_NAME(v1_1, v2@SEL_1 .v1@SEL_2 .@SEL_1)`, and the second query block in view `v1` can be declared as `QB_NAME(v1_2, v2@SEL_1 .v1@SEL_2 .@SEL_2)`:

    ```sql
    CREATE VIEW v1 AS SELECT * FROM t JOIN /* Comment: For view `v1`, the name of the current query block is the default @SEL_1. So, the current query block view list is v2@SEL_1 .@SEL_2 .v1@SEL_1 */
        (
            SELECT COUNT(*) FROM t1 JOIN t2 /* Comment: For view `v1`, the name of the current query block is the default @SEL_2. So, the current query block view list is v2@SEL_1 .@SEL_2 .v1@SEL_2 */
        ) tt;
    ```

> **Note:**
>
> - To use global hints with views, you must define the corresponding `QB_NAME` hints in the view. Otherwise, the global hints will not take effect.
>
> - When using a hint to specify multiple table names in a view, you need to ensure that the table names appearing in the same hint are in the same query block of the same view.
>
> - When you define the `QB_NAME` hint in a view for the outermost query block:
>
>     - For the first item of the view list in the `QB_NAME`, if the `@SEL_` is not explicitly declared, the default is consistent with the query block position where the `QB_NAME` is defined. That is, the query `SELECT /*+ QB_NAME(qb1, v2) */ * FROM v2 JOIN (SELECT /*+ QB_NAME(qb2, v2) */ * FROM v2) vv;` is equivalent to `SELECT /*+ QB_NAME(qb1, v2@SEL_1) */ * FROM v2 JOIN (SELECT /*+ QB_NAME(qb2, v2@SEL_2) */ * FROM v2) vv;`.
>     - For items other than the first item of the view list in the `QB_NAME`, only `@SEL_1` can be omitted. That is, if `@SEL_1` is declared in the first query block of the current view, `@SEL_1` can be omitted. Otherwise, `@SEL_` cannot be omitted. For the preceding example:
>
>         - The first query block of the view `v2` can be declared as `QB_NAME(v2_1, v2)`.
>         - The second query block of the view `v2` can be declared as `QB_NAME(v2_2, v2.@SEL_2)`.
>         - The first query block of the view `v1` can be declared as `QB_NAME(v1_1, v2.v1@SEL_2)`.
>         - The second query block of the view `v1` can be declared as `QB_NAME(v1_2, v2.v1@SEL_2 .@SEL_2)`.

### Step 2: Add the target hints

After defining the `QB_NAME` hint for query blocks of the view, you can add required [hints that take effect in query blocks](#hints-that-take-effect-in-query-blocks) in the form of `ViewName@QueryBlockName` to make them effective inside the view. For example:

- Specify the `MERGE_JOIN()` hint for the first query block of the view `v2`:

    ```sql
    SELECT /*+ QB_NAME(v2_1, v2) merge_join(t@v2_1) */ * FROM v2;
    ```

- Specify the `MERGE_JOIN()` and `STREAM_AGG()` hints for the second query block of the view `v2`:

    ```sql
    SELECT /*+ QB_NAME(v2_2, v2.@SEL_2) merge_join(t1@v2_2) stream_agg(@v2_2) */ * FROM v2;
    ```

- Specify the `HASH_JOIN()` hint for the first query block of the view `v1`:

    ```sql
    SELECT /*+ QB_NAME(v1_1, v2.v1@SEL_2) hash_join(t@v1_1) */ * FROM v2;
    ```

- Specify the `HASH_JOIN()` and `HASH_AGG()` hints for the second query block of the view `v1`:

    ```sql
    SELECT /*+ QB_NAME(v1_2, v2.v1@SEL_2 .@SEL_2) hash_join(t1@v1_2) hash_agg(@v1_2) */ * FROM v2;
    ```

## Hints that take effect in the whole query

This category of hints can only follow behind the **first** `SELECT`, `UPDATE` or `DELETE` keyword, which is equivalent to modifying the value of the specified system variable when this query is executed. The priority of the hint is higher than that of existing system variables.

> **Note:**
>
> This category of hints also has an optional hidden variable `@QB_NAME`, but the hint takes effect in the whole query even if you specify the variable.

### NO_INDEX_MERGE()

The `NO_INDEX_MERGE()` hint disables the index merge feature of the optimizer.

For example, the following query will not use index merge:

{{< copyable "sql" >}}

```sql
select /*+ NO_INDEX_MERGE() */ * from t where t.a > 0 or t.b > 0;
```

In addition to this hint, setting the `tidb_enable_index_merge` system variable also controls whether to enable this feature.

> **Note:**
>
> - `NO_INDEX_MERGE` has a higher priority over `USE_INDEX_MERGE`. When both hints are used, `USE_INDEX_MERGE` does not take effect.
> - For a subquery, `NO_INDEX_MERGE` only takes effect when it is placed at the outermost level of the subquery.

### USE_TOJA(boolean_value)

The `boolean_value` parameter can be `TRUE` or `FALSE`. The `USE_TOJA(TRUE)` hint enables the optimizer to convert an `in` condition (containing a sub-query) to join and aggregation operations. Comparatively, the `USE_TOJA(FALSE)` hint disables this feature.

For example, the following query will convert `in (select t2.a from t2) subq` to corresponding join and aggregation operations:

{{< copyable "sql" >}}

```sql
select /*+ USE_TOJA(TRUE) */ t1.a, t1.b from t1 where t1.a in (select t2.a from t2) subq;
```

In addition to this hint, setting the `tidb_opt_insubq_to_join_and_agg` system variable also controls whether to enable this feature.

### MAX_EXECUTION_TIME(N)

The `MAX_EXECUTION_TIME(N)` hint places a limit `N` (a timeout value in milliseconds) on how long a statement is permitted to execute before the server terminates it. In the following hint, `MAX_EXECUTION_TIME(1000)` means that the timeout is 1000 milliseconds (that is, 1 second):

{{< copyable "sql" >}}

```sql
select /*+ MAX_EXECUTION_TIME(1000) */ * from t1 inner join t2 where t1.id = t2.id;
```

In addition to this hint, the `global.max_execution_time` system variable can also limit the execution time of a statement.

### MEMORY_QUOTA(N)

The `MEMORY_QUOTA(N)` hint places a limit `N` (a threshold value in MB or GB) on how much memory a statement is permitted to use. When a statement's memory usage exceeds this limit, TiDB produces a log message based on the statement's over-limit behavior or just terminates it.

In the following hint, `MEMORY_QUOTA(1024 MB)` means that the memory usage is limited to 1024 MB:

{{< copyable "sql" >}}

```sql
select /*+ MEMORY_QUOTA(1024 MB) */ * from t;
```

In addition to this hint, the [`tidb_mem_quota_query`](/system-variables.md#tidb_mem_quota_query) system variable can also limit the memory usage of a statement.

### READ_CONSISTENT_REPLICA()

The `READ_CONSISTENT_REPLICA()` hint enables the feature of reading consistent data from the TiKV follower node. For example:

{{< copyable "sql" >}}

```sql
select /*+ READ_CONSISTENT_REPLICA() */ * from t;
```

In addition to this hint, setting the `tidb_replica_read` environment variable to `'follower'` or `'leader'` also controls whether to enable this feature.

### IGNORE_PLAN_CACHE()

The `IGNORE_PLAN_CACHE()` hint reminds the optimizer not to use the Plan Cache when handling the current `prepare` statement.

This hint is used to temporarily disable the Plan Cache for a certain type of queries when [prepare-plan-cache](/sql-prepared-plan-cache.md) is enabled.

In the following example, the Plan Cache is forcibly disabled when executing the `prepare` statement.

{{< copyable "sql" >}}

```sql
prepare stmt from 'select  /*+ IGNORE_PLAN_CACHE() */ * from t where t.id = ?';
```

### STRAIGHT_JOIN()

The `STRAIGHT_JOIN()` hint reminds the optimizer to join tables in the order of table names in the `FROM` clause when generating the join plan.

{{< copyable "sql" >}}

```sql
SELECT /*+ STRAIGHT_JOIN() */ * FROM t t1, t t2 WHERE t1.a = t2.a;
```

> **Note:**
>
> - `STRAIGHT_JOIN` has higher priority over `LEADING`. When both hints are used, `LEADING` does not take effect.
> - It is recommended to use the `LEADING` hint, which is more general than the `STRAIGHT_JOIN` hint.

### NTH_PLAN(N)

The `NTH_PLAN(N)` hint reminds the optimizer to select the `N`th physical plan found during the physical optimization. `N` must be a positive integer.

If the specified `N` is beyond the search range of the physical optimization, TiDB will return a warning and select the optimal physical plan based on the strategy that ignores this hint.

This hint does not take effect when the cascades planner is enabled.

In the following example, the optimizer is forced to select the third physical plan found during the physical optimization:

{{< copyable "sql" >}}

```sql
SELECT /*+ NTH_PLAN(3) */ count(*) from t where a > 5;
```

> **Note:**
>
> `NTH_PLAN(N)` is mainly used for testing, and its compatibility is not guaranteed in later versions. Use this hint **with caution**.
