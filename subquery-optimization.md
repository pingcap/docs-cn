---
title: Subquery Related Optimizations
summary: Understand optimizations related to subqueries.
---

# Subquery Related Optimizations

This article mainly introduces subquery related optimizations.

Subqueries usually appear in the following situations:

- `NOT IN (SELECT ... FROM ...)`
- `NOT EXISTS (SELECT ... FROM ...)`
- `IN (SELECT ... FROM ..)`
- `EXISTS (SELECT ... FROM ...)`
- `... >/>=/</<=/=/!= (SELECT ... FROM ...)`

Sometimes a subquery contains non-subquery columns, such as `select * from t where t.a in (select * from t2 where t.b=t2.b)`. The `t.b` column in the subquery does not belong to the subquery, it is introduced from the outside of the subquery. This kind of subquery is usually called a "correlated subquery", and the externally introduced column is called a "correlated column". For optimizations about correlated subquery, see [Decorrelation of correlated subquery](/correlated-subquery-optimization.md). This article focuses on subqueries that do not involve correlated columns.

By default, subqueries use `semi join` mentioned in [Understanding TiDB Execution Plan](/explain-overview.md) as the execution method. For some special subqueries, TiDB do some logical rewrite to get better performance.

## `... < ALL (SELECT ... FROM ...)` or `... > ANY (SELECT ... FROM ...)`

In this case, `ALL` and `ANY` can be replaced by `MAX` and `MIN`. When the table is empty, the result of `MAX(EXPR)` and `MIN(EXPR)` is NULL. It works the same when the result of `EXPR` contains `NULL`. Whether the result of `EXPR` contains `NULL` may affect the final result of the expression, so the complete rewrite is given in the following form:

- `t.id < all (select s.id from s)` is rewritten as `t.id < min(s.id) and if(sum(s.id is null) != 0, null, true)`
- `t.id < any (select s.id from s)` is rewritten as `t.id < max(s.id) or if(sum(s.id is null) != 0, null, false)`

## `... != ANY (SELECT ... FROM ...)`

In this case, if all the values from the subquery are distinct, it is enough to compare the query with them. If the number of different values in the subquery is more than one, then there must be inequality. Therefore, such subqueries can be rewritten as follows:

- `select * from t where t.id != any (select s.id from s)` is rewritten as `select t.* from t, (select s.id, count(distinct s.id) as cnt_distinct from s) where (t.id != s.id or cnt_distinct > 1)`

## `... = ALL (SELECT ... FROM ...)`

In this case, when the number of different values in the subquery is more than one, then the result of this expression must be false. Therefore, such subquery is rewritten into the following form in TiDB:

- `select * from t where t.id = all (select s.id from s)` is rewritten as `select t.* from t, (select s.id, count(distinct s.id) as cnt_distinct from s ) where (t.id = s.id and cnt_distinct <= 1)`

## `... IN (SELECT ... FROM ...)`

In this case, the subquery of `IN` is rewritten into `SELECT ... FROM ... GROUP ...`, and then rewritten into the normal form of `JOIN`.

For example, `select * from t1 where t1.a in (select t2.a from t2)` is rewritten as `select t1.* from t1, (select distinct(a) a from t2) t2 where t1.a = t2. The form of a`. The `DISTINCT` attribute here can be eliminated automatically if `t2.a` has the `UNIQUE` attribute.

{{< copyable "sql" >}}

```sql
explain select * from t1 where t1.a in (select t2.a from t2);
```

```sql
+------------------------------+---------+-----------+------------------------+----------------------------------------------------------------------------+
| id                           | estRows | task      | access object          | operator info                                                              |
+------------------------------+---------+-----------+------------------------+----------------------------------------------------------------------------+
| IndexJoin_12                 | 9990.00 | root      |                        | inner join, inner:TableReader_11, outer key:test.t2.a, inner key:test.t1.a |
| ├─HashAgg_21(Build)          | 7992.00 | root      |                        | group by:test.t2.a, funcs:firstrow(test.t2.a)->test.t2.a                   |
| │ └─IndexReader_28           | 9990.00 | root      |                        | index:IndexFullScan_27                                                     |
| │   └─IndexFullScan_27       | 9990.00 | cop[tikv] | table:t2, index:idx(a) | keep order:false, stats:pseudo                                             |
| └─TableReader_11(Probe)      | 7992.00 | root      |                        | data:TableRangeScan_10                                                     |
|   └─TableRangeScan_10        | 7992.00 | cop[tikv] | table:t1               | range: decided by [test.t2.a], keep order:false, stats:pseudo              |
+------------------------------+---------+-----------+------------------------+----------------------------------------------------------------------------+
```

This rewrite gets better performance when the `IN` subquery is relatively small and the external query is relatively large, because without rewriting, using `index join` with t2 as the driving table is impossible. However, the disadvantage is that when the aggregation cannot be automatically eliminated during the rewrite and the `t2` table is relatively large, this rewrite affects the performance of the query. Currently, the variable [tidb\_opt\_insubq\_to\_join\_and\_agg](/system-variables.md#tidb_opt_insubq_to_join_and_agg) is used to control this optimization. When this optimization is not suitable, you can manually disable it.

## `EXISTS` subquery and `... >/>=/</<=/=/!= (SELECT ... FROM ...)`

At present, for a subquery in such scenarios, if the subquery is not a correlated subquery, TiDB evaluates it in advance in the optimization stage, and directly replaces it with a result set. As shown in the figure below, the `EXISTS` subquery is evaluated to `TRUE` in the optimization stage in advance, so it does not show in the final execution result.

{{< copyable "sql" >}}

```sql
create table t1(a int);
create table t2(a int);
insert into t2 values(1);
explain select * from t1 where exists (select * from t2);
```

```sql
+------------------------+----------+-----------+---------------+--------------------------------+
| id                     | estRows  | task      | access object | operator info                  |
+------------------------+----------+-----------+---------------+--------------------------------+
| TableReader_12         | 10000.00 | root      |               | data:TableFullScan_11          |
| └─TableFullScan_11     | 10000.00 | cop[tikv] | table:t1      | keep order:false, stats:pseudo |
+------------------------+----------+-----------+---------------+--------------------------------+
```

In the preceding optimization, the optimizer automatically optimizes the statement execution. In addition, you can also add the [`SEMI_JOIN_REWRITE`](/optimizer-hints.md#semi_join_rewrite) hint to further rewrite the statement.

If this hint is not used to rewrite the query, when the hash join is selected in the execution plan, the semi-join query can only use the subquery to build a hash table. In this case, when the result of the subquery is bigger than that of the outer query, the execution speed might be slower than expected.

Similarly, when the index join is selected in the execution plan, the semi-join query can only use the outer query as the driving table. In this case, when the result of the subquery is smaller than that of the outer query, the execution speed might be slower than expected.

When `SEMI_JOIN_REWRITE()` is used to rewrite the query, the optimizer can extend the selection range to select a better execution plan.
