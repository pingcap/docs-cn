---
title: WITH | TiDB SQL Statement Reference
summary: An overview of the usage of WITH (Common Table Expression) for the TiDB database.
---

# WITH

A Common Table Expression (CTE) is a temporary result set that can be referred multiple times within a SQL statement to improve the statement's readability and execution efficiency. You can apply the `WITH` statement to use Common Table Expressions.

## Synopsis

**WithClause:**

``` ebnf
WithClause ::=
        "WITH" WithList
|       "WITH" recursive WithList
```

**WithList:**

``` ebnf
WithList ::=
        WithList ',' CommonTableExpr
|       CommonTableExpr
```

**CommonTableExpr:**

``` ebnf
CommonTableExpr ::=
        Identifier IdentListWithParenOpt "AS" SubSelect
```

**IdentListWithParenOpt:**

``` ebnf
IdentListWithParenOpt ::=

|       '(' IdentList ')'
```

## Examples

Non-recursive CTE:

{{< copyable "sql" >}}

```sql
WITH CTE AS (SELECT 1, 2) SELECT * FROM cte t1, cte t2;
```

```
+---+---+---+---+
| 1 | 2 | 1 | 2 |
+---+---+---+---+
| 1 | 2 | 1 | 2 |
+---+---+---+---+
1 row in set (0.00 sec)
```

Recursive CTE:

{{< copyable "sql" >}}

```sql
WITH RECURSIVE cte(a) AS (SELECT 1 UNION SELECT a+1 FROM cte WHERE a < 5) SELECT * FROM cte;
```

```
+---+
| a |
+---+
| 1 |
| 2 |
| 3 |
| 4 |
| 5 |
+---+
5 rows in set (0.00 sec)
```

## MySQL compatibility

* In strict mode, when the data length recursively calculated exceeds the data length of the seed part, TiDB returns a warning while MySQL returns an error. In non-strict mode, the behavior of TiDB is consistent with that of MySQL.
* The data type for recursive CTE is determined by the seed part. The data type of the seed part is not completely consistent with MySQL in some cases (such as functions).
* In the case of multiple `UNION` / `UNION ALL` operators, MySQL does not allow `UNION` to be followed by `UNION ALL`, but TiDB does.
* If there is a problem with the definition of a CTE, TiDB will report an error, while MySQL will not if the CTE is not referred.

## See also

* [SELECT](/sql-statements/sql-statement-select.md)
* [INSERT](/sql-statements/sql-statement-insert.md)
* [DELETE](/sql-statements/sql-statement-delete.md)
* [UPDATE](/sql-statements/sql-statement-update.md)
* [REPLACE](/sql-statements/sql-statement-replace.md)
