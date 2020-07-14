---
title: SHOW DATABASES | TiDB SQL Statement Reference
summary: An overview of the usage of SHOW DATABASES for the TiDB database.
aliases: ['/docs/dev/sql-statements/sql-statement-show-databases/','/docs/dev/reference/sql/statements/show-databases/']
---

# SHOW DATABASES

This statement shows a list of databases that the current user has privileges to. Databases which the current user does not have access to will appear hidden from the list. The `information_schema` database always appears first in the list of databases.

`SHOW SCHEMAS` is an alias of this statement.

## Synopsis

**ShowDatabasesStmt:**

![ShowDatabasesStmt](/media/sqlgram/ShowDatabasesStmt.png)

**ShowLikeOrWhereOpt:**

![ShowLikeOrWhereOpt](/media/sqlgram/ShowLikeOrWhereOpt.png)

## Examples

```sql
mysql> SHOW DATABASES;
+--------------------+
| Database           |
+--------------------+
| INFORMATION_SCHEMA |
| PERFORMANCE_SCHEMA |
| mysql              |
| test               |
+--------------------+
4 rows in set (0.00 sec)

mysql> CREATE DATABASE mynewdb;
Query OK, 0 rows affected (0.10 sec)

mysql> SHOW DATABASES;
+--------------------+
| Database           |
+--------------------+
| INFORMATION_SCHEMA |
| PERFORMANCE_SCHEMA |
| mynewdb            |
| mysql              |
| test               |
+--------------------+
5 rows in set (0.00 sec)
```

## MySQL compatibility

This statement is understood to be fully compatible with MySQL. Any compatibility differences should be [reported via an issue](/report-issue.md) on GitHub.

## See also

* [SHOW SCHEMAS](/sql-statements/sql-statement-show-schemas.md)
* [DROP DATABASE](/sql-statements/sql-statement-drop-database.md)
* [CREATE DATABASE](/sql-statements/sql-statement-create-database.md)
