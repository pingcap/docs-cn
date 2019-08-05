---
title: PREPARE | TiDB SQL Statement Reference
summary: An overview of the usage of PREPARE for the TiDB database.
category: reference
aliases: ['/docs/sql/prepare/']
---

# PREPARE

The `PREPARE` statement provides an SQL interface to server-side prepared statements.

## Synopsis

**PreparedStmt:**

![PreparedStmt](/media/sqlgram-v3.0/PreparedStmt.png)

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

This statement is understood to be fully compatible with MySQL. Any compatibility differences should be [reported via an issue](/report-issue.md) on GitHub.

## See also

* [EXECUTE](/reference/sql/statements/execute.md)
* [DEALLOCATE](/reference/sql/statements/deallocate.md)
