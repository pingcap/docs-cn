---
title: TRUNCATE | TiDB SQL Statement Reference
summary: An overview of the usage of TRUNCATE for the TiDB database.
category: reference
---

# TRUNCATE

The `TRUNCATE` statement removes all data from the table in a non-transactional way. `TRUNCATE` can be thought of as semantically the same as `DROP TABLE` + `CREATE TABLE` with the previous definition.

Both `TRUNCATE TABLE tableName` and `TRUNCATE tableName` are valid syntax.

## Synopsis

**TruncateTableStmt:**

![TruncateTableStmt](/media/sqlgram-v3.0/TruncateTableStmt.png)

**OptTable:**

![OptTable](/media/sqlgram-v3.0/OptTable.png)

**TableName:**

![TableName](/media/sqlgram-v3.0/TableName.png)

## Examples

```sql
mysql> CREATE TABLE t1 (a INT NOT NULL PRIMARY KEY);
Query OK, 0 rows affected (0.11 sec)

mysql> INSERT INTO t1 VALUES (1),(2),(3),(4),(5);
Query OK, 5 rows affected (0.01 sec)
Records: 5  Duplicates: 0  Warnings: 0

mysql> SELECT * FROM t1;
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

mysql> TRUNCATE t1;
Query OK, 0 rows affected (0.11 sec)

mysql> SELECT * FROM t1;
Empty set (0.00 sec)

mysql> INSERT INTO t1 VALUES (1),(2),(3),(4),(5);
Query OK, 5 rows affected (0.01 sec)
Records: 5  Duplicates: 0  Warnings: 0

mysql> TRUNCATE TABLE t1;
Query OK, 0 rows affected (0.11 sec)
```

## MySQL compatibility

This statement is understood to be fully compatible with MySQL. Any compatibility differences should be [reported via an issue](/v3.0/report-issue.md) on GitHub.

## See also

* [DROP TABLE](/v3.0/reference/sql/statements/drop-table.md)
* [DELETE](/v3.0/reference/sql/statements/delete.md)
* [CREATE TABLE](/v3.0/reference/sql/statements/create-table.md)
* [SHOW CREATE TABLE](/v3.0/reference/sql/statements/show-create-table.md)
