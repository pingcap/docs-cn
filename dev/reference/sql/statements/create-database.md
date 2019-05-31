---
title: CREATE DATABASE | TiDB SQL Statement Reference 
summary: An overview of the usage of CREATE DATABASE for the TiDB database.
category: reference
---

# CREATE DATABASE

This statement creates a new database in TiDB. The MySQL terminology for 'database' most closely maps to a schema in the SQL standard.

## Synopsis

**CreateDatabaseStmt:**

![CreateDatabaseStmt](/media/sqlgram/CreateDatabaseStmt.png)

**DatabaseSym:**

![DatabaseSym](/media/sqlgram/DatabaseSym.png)

**IfNotExists:**

![IfNotExists](/media/sqlgram/IfNotExists.png)

**DBName:**

![DBName](/media/sqlgram/DBName.png)

**DatabaseOptionListOpt:**

![DatabaseOptionListOpt](/media/sqlgram/DatabaseOptionListOpt.png)

## Examples

```sql
mysql> CREATE DATABASE mynewdatabase;
Query OK, 0 rows affected (0.09 sec)

mysql> USE mynewdatabase;
Database changed
mysql> CREATE TABLE t1 (a int);
Query OK, 0 rows affected (0.11 sec)

mysql> SHOW TABLES;
+-------------------------+
| Tables_in_mynewdatabase |
+-------------------------+
| t1                      |
+-------------------------+
1 row in set (0.00 sec)
```

## MySQL compatibility

This statement is understood to be fully compatible with MySQL. Any compatibility differences should be [reported via an issue](/report-issue.md) on GitHub.

## See also

* [USE](/dev/reference/sql/statements/use.md)
* [DROP DATABASE](/dev/reference/sql/statements/drop-database.md)
