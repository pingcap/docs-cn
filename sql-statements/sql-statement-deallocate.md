---
title: DEALLOCATE | TiDB SQL Statement Reference
summary: An overview of the usage of DEALLOCATE for the TiDB database.
aliases: ['/docs/dev/sql-statements/sql-statement-deallocate/','/docs/dev/reference/sql/statements/deallocate/']
---

# DEALLOCATE

The `DEALLOCATE` statement provides an SQL interface to server-side prepared statements.

## Synopsis

```ebnf+diagram
DeallocateStmt ::=
    DeallocateSym 'PREPARE' Identifier

DeallocateSym ::=
    'DEALLOCATE'
|   'DROP'

Identifier ::=
    identifier
|   UnReservedKeyword
|   NotKeywordToken
|   TiDBKeyword
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

The `DEALLOCATE` statement in TiDB is fully compatible with MySQL. If you find any compatibility differences, [report a bug](https://docs.pingcap.com/tidb/stable/support).

## See also

* [PREPARE](/sql-statements/sql-statement-prepare.md)
* [EXECUTE](/sql-statements/sql-statement-execute.md)
