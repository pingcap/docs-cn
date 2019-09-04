---
title: RENAME TABLE | TiDB SQL Statement Reference
summary: An overview of the usage of RENAME TABLE for the TiDB database.
category: reference
---

# RENAME TABLE

This statement renames an existing table to a new name.

## Synopsis

**RenameTableStmt:**

![RenameTableStmt](/media/sqlgram-dev/RenameTableStmt.png)

**TableToTable:**

![TableToTable](/media/sqlgram-dev/TableToTable.png)

## Examples

```sql
mysql> CREATE TABLE t1 (a int);
Query OK, 0 rows affected (0.12 sec)

mysql> SHOW TABLES;
+----------------+
| Tables_in_test |
+----------------+
| t1             |
+----------------+
1 row in set (0.00 sec)

mysql> RENAME TABLE t1 TO t2;
Query OK, 0 rows affected (0.08 sec)

mysql> SHOW TABLES;
+----------------+
| Tables_in_test |
+----------------+
| t2             |
+----------------+
1 row in set (0.00 sec)
```

## MySQL compatibility

This statement is understood to be fully compatible with MySQL. Any compatibility differences should be [reported via an issue](/dev/report-issue.md) on GitHub.

## See also

* [CREATE TABLE](/dev/reference/sql/statements/create-table.md)
* [SHOW TABLES](/dev/reference/sql/statements/show-tables.md)
* [ALTER TABLE](/dev/reference/sql/statements/alter-table.md)
