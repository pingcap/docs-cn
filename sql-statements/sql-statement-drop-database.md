---
title: DROP DATABASE | TiDB SQL Statement Reference
summary: An overview of the usage of DROP DATABASE for the TiDB database.
aliases: ['/docs/dev/sql-statements/sql-statement-drop-database/','/docs/dev/reference/sql/statements/drop-database/']
---

# DROP DATABASE

The `DROP DATABASE` statement permanently removes a specified database schema, and all of the tables and views that were created inside. User privileges that are associated with the dropped database remain unaffected.

## Synopsis

```ebnf+diagram
DropDatabaseStmt ::=
    'DROP' 'DATABASE' IfExists DBName

IfExists ::= ( 'IF' 'EXISTS' )?
```

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

mysql> DROP DATABASE test;
Query OK, 0 rows affected (0.25 sec)

mysql> SHOW DATABASES;
+--------------------+
| Database           |
+--------------------+
| INFORMATION_SCHEMA |
| PERFORMANCE_SCHEMA |
| mysql              |
+--------------------+
3 rows in set (0.00 sec)
```

## MySQL compatibility

The `DROP DATABASE` statement in TiDB is fully compatible with MySQL. If you find any compatibility differences, [report a bug](https://docs.pingcap.com/tidb/stable/support).

## See also

* [CREATE DATABASE](/sql-statements/sql-statement-create-database.md)
* [ALTER DATABASE](/sql-statements/sql-statement-alter-database.md)
