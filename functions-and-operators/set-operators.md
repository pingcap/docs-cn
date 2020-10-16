---
title: Set Operations
summary: Learn the supported set operations in TiDB.
---

# Set Operations

TiDB supports three set operations using the UNION, EXCEPT, and INTERSECT operators. The smallest unit of a set is a [`SELECT` statement](/sql-statements/sql-statement-select.md).

## UNION operator

In mathematics, the union of two sets A and B consists of all elements that are in A or in B. For example:

```sql
select 1 union select 2;
+---+
| 1 |
+---+
| 2 |
| 1 |
+---+
2 rows in set (0.00 sec)
```

TiDB supports both `UNION DISTINCT` and `UNION ALL` operators. `UNION DISTINCT` removes duplicate records from the result set, while `UNION ALL` keeps all records including duplicates. `UNION DISTINCT` is used by default in TiDB.

{{< copyable "sql" >}}

```sql
create table t1 (a int);
create table t2 (a int);
insert into t1 values (1),(2);
insert into t2 values (1),(3);
```

Examples for `UNION DISTINCT` and `UNION ALL` queries are respectively as follows:

```sql
select * from t1 union distinct select * from t2;
+---+
| a |
+---+
| 1 |
| 2 |
| 3 |
+---+
3 rows in set (0.00 sec)
select * from t1 union all select * from t2;
+---+
| a |
+---+
| 1 |
| 2 |
| 1 |
| 3 |
+---+
4 rows in set (0.00 sec)
```

## EXCEPT operator

If A and B are two sets, EXCEPT returns the difference set of A and B which consists of elements that are in A but not in B.

```sql
select * from t1 except select * from t2;
+---+
| a |
+---+
| 2 |
+---+
1 rows in set (0.00 sec)
```

`EXCEPT ALL` operator is not yet supported.

## INTERSECT operator

In mathematics, the intersection of two sets A and B consists of all elements that are both in A and B, and no other elements.

```sql
select * from t1 intersect select * from t2;
+---+
| a |
+---+
| 1 |
+---+
1 rows in set (0.00 sec)
```

`INTERSECT ALL` operator is not yet supported. INTERSECT operator has higher precedence over EXCEPT and UNION operators.

```sql
select * from t1 union all select * from t1 intersect select * from t2;
+---+
| a |
+---+
| 1 |
| 1 |
| 2 |
+---+
3 rows in set (0.00 sec)
```

## Parentheses

TiDB supports using parentheses to specify the precedence of set operations. Expressions in parentheses are processed first.

```sql
(select * from t1 union all select * from t1) intersect select * from t2;
+---+
| a |
+---+
| 1 |
+---+
1 rows in set (0.00 sec)
```

## Use `Order By` and `Limit`

TiDB supports using [`ORDER BY`](/media/sqlgram/OrderByOptional.png) or [`LIMIT`](/media/sqlgram/LimitClause.png) clause in set operations. These two clauses must be at the end of the entire statement.

```sql
(select * from t1 union all select * from t1 intersect select * from t2) order by a limit 2;
+---+
| a |
+---+
| 1 |
| 1 |
+---+
2 rows in set (0.00 sec)
```
