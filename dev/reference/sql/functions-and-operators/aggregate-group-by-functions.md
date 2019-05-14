---
title: Aggregate (GROUP BY) Functions
summary: Learn about the supported aggregate functions in TiDB.
category: reference
aliases: ['/docs/sql/aggregate-group-by-functions/']
---

# Aggregate (GROUP BY) Functions

This document describes details about the supported aggregate functions in TiDB.

## Supported aggregate functions

This section describes the supported MySQL group (aggregate) functions in TiDB.

| Name                                                                                                        | Description                                       |
|:--------------------------------------------------------------------------------------------------------------|:--------------------------------------------------|
| [`COUNT()`](https://dev.mysql.com/doc/refman/5.7/en/group-by-functions.html#function_count)                   | Return a count of the number of rows returned     |
| [`COUNT(DISTINCT)`](https://dev.mysql.com/doc/refman/5.7/en/group-by-functions.html#function_count-distinct)  | Return the count of a number of different values  |
| [`SUM()`](https://dev.mysql.com/doc/refman/5.7/en/group-by-functions.html#function_sum)                       | Return the sum                                    |
| [`AVG()`](https://dev.mysql.com/doc/refman/5.7/en/group-by-functions.html#function_avg)                       | Return the average value of the argument          |
| [`MAX()`](https://dev.mysql.com/doc/refman/5.7/en/group-by-functions.html#function_max)                       | Return the maximum value                          |
| [`MIN()`](https://dev.mysql.com/doc/refman/5.7/en/group-by-functions.html#function_min)                       | Return the minimum value                          |
| [`GROUP_CONCAT()`](https://dev.mysql.com/doc/refman/5.7/en/group-by-functions.html#function_group-concat)     | Return a concatenated string                      |

- Unless otherwise stated, group functions ignore `NULL` values.
- If you use a group function in a statement containing no `GROUP BY` clause, it is equivalent to grouping on all rows.

## GROUP BY modifiers

TiDB does not currently support `GROUP BY` modifiers such as `WITH ROLLUP`. We plan to add support in the future. See [TiDB #4250](https://github.com/pingcap/tidb/issues/4250).

## SQL mode support

TiDB supports the SQL Mode `ONLY_FULL_GROUP_BY`, and when enabled TiDB will refuse queries with ambiguous non-aggregated columns. For example, this query is illegal with `ONLY_FULL_GROUP_BY` enabled because the non-aggregated column "b" in the `SELECT` list does not appear in the `GROUP BY` statement:

```sql
drop table if exists t;
create table t(a bigint, b bigint, c bigint);
insert into t values(1, 2, 3), (2, 2, 3), (3, 2, 3);

mysql> select a, b, sum(c) from t group by a;
+------+------+--------+
| a    | b    | sum(c) |
+------+------+--------+
|    1 |    2 |      3 |
|    2 |    2 |      3 |
|    3 |    2 |      3 |
+------+------+--------+
3 rows in set (0.01 sec)

mysql> set sql_mode = 'ONLY_FULL_GROUP_BY';
Query OK, 0 rows affected (0.00 sec)

mysql> select a, b, sum(c) from t group by a;
ERROR 1055 (42000): Expression #2 of SELECT list is not in GROUP BY clause and contains nonaggregated column 'b' which is not functionally dependent on columns in GROUP BY clause; this is incompatible with sql_mode=only_full_group_by
```

TiDB does not currently enable the [`ONLY_FULL_GROUP_BY`](/dev/reference/mysql-compatibility.md#default-differences) mode by default.

### Differences from MySQL

The current implementation of `ONLY_FULL_GROUP_BY` is less strict than that in MySQL 5.7. For example, suppose that we execute the following query, expecting the results to be ordered by "c":

```sql
drop table if exists t;
create table t(a bigint, b bigint, c bigint);
insert into t values(1, 2, 1), (1, 2, 2), (1, 3, 1), (1, 3, 2);
select distinct a, b from t order by c;
```

To order the result, duplicates must be eliminated first. But to do so, which row should we keep? This choice influences the retained value of "c", which in turn influences ordering and makes it arbitrary as well.

In MySQL, a query that has `DISTINCT` and `ORDER BY` is rejected as invalid if any `ORDER BY` expression does not satisfy at least one of these conditions:

- The expression is equal to one in the `SELECT` list
- All columns referenced by the expression and belonging to the query's selected tables are elements of the `SELECT` list

But in TiDB, the above query is legal, for more information see [#4254](https://github.com/pingcap/tidb/issues/4254).

Another TiDB extension to standard SQL permits references in the `HAVING` clause to aliased expressions in the `SELECT` list. For example, the following query returns "name" values that occur only once in table "orders":

```sql
select name, count(name) from orders
group by name
having count(name) = 1;
```

The TiDB extension permits the use of an alias in the `HAVING` clause for the aggregated column:

```sql
select name, count(name) as c from orders
group by name
having c = 1;
```

Standard SQL permits only column expressions in `GROUP BY` clauses, so a statement such as this is invalid because "FLOOR(value/100)" is a noncolumn expression:

```sql
select id, floor(value/100)
from tbl_name
group by id, floor(value/100);
```

TiDB extends standard SQL to permit noncolumn expressions in `GROUP BY` clauses and considers the preceding statement valid.

Standard SQL also does not permit aliases in `GROUP BY` clauses. TiDB extends standard SQL to permit aliases, so another way to write the query is as follows:

```sql
select id, floor(value/100) as val
from tbl_name
group by id, val;
```

## Unsupported aggregate functions

The following aggregate functions are currently unsupported in TiDB. You can track our progress in [TiDB #7623](https://github.com/pingcap/tidb/issues/7623):

- `STD`, `STDDEV`, `STDDEV_POP`
- `STDDEV_SAMP`
- `VARIANCE`, `VAR_POP`
- `VAR_SAMP`
- `JSON_ARRAYAGG`
- `JSON_OBJECTAGG`
