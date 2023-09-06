---
title: EXECUTE | TiDB SQL Statement Reference
summary: An overview of the usage of EXECUTE for the TiDB database.
aliases: ['/docs/dev/sql-statements/sql-statement-execute/','/docs/dev/reference/sql/statements/execute/']
---

# EXECUTE

The `EXECUTE` statement provides an SQL interface to server-side prepared statements.

## Synopsis

```ebnf+diagram
ExecuteStmt ::=
    'EXECUTE' Identifier ( 'USING' UserVariable ( ',' UserVariable )* )?
```

## Examples

```sql
mysql> PREPARE mystmt FROM 'SELECT ? as num FROM DUAL';
Query OK, 0 rows affected (0.00 sec)

mysql> SET @number = 5;
Query OK, 0 rows affected (0.00 sec)

mysql> EXECUTE mystmt USING @number;
+------+
| num  |
+------+
| 5    |
+------+
1 row in set (0.00 sec)

mysql> DEALLOCATE PREPARE mystmt;
Query OK, 0 rows affected (0.00 sec)
```

## MySQL compatibility

The `EXECUTE` statement in TiDB is fully compatible with MySQL. If you find any compatibility differences, [report a bug](https://docs.pingcap.com/tidb/stable/support).

## See also

* [PREPARE](/sql-statements/sql-statement-prepare.md)
* [DEALLOCATE](/sql-statements/sql-statement-deallocate.md)
