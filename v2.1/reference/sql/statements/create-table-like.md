---
title: CREATE TABLE LIKE | TiDB SQL Statement Reference 
summary: An overview of the usage of CREATE TABLE AS for the TiDB database.
category: reference
---

# CREATE TABLE LIKE

This statement copies the definition of an existing table, without copying any data.

## Synopsis

**CreateTableStmt:**

![CreateTableStmt](/media/sqlgram/CreateTableStmt.png)

**LikeTableWithOrWithoutParen:**

![LikeTableWithOrWithoutParen](/media/sqlgram/LikeTableWithOrWithoutParen.png)

**TableName:**

![TableName](/media/sqlgram/TableName.png)

## Examples

```sql
mysql> CREATE TABLE t1 (a INT NOT NULL);
Query OK, 0 rows affected (0.13 sec)

mysql> INSERT INTO t1 VALUES (1),(2),(3),(4),(5);
Query OK, 5 rows affected (0.02 sec)
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

mysql> CREATE TABLE t2 LIKE t1;
Query OK, 0 rows affected (0.10 sec)

mysql> SELECT * FROM t2;
Empty set (0.00 sec)
```

## MySQL compatibility

This statement is understood to be fully compatible with MySQL. Any compatibility differences should be [reported via an issue](/report-issue.md) on GitHub.

## See also

* [CREATE TABLE](/reference/sql/statements/create-table.md)
* [SHOW CREATE TABLE](/reference/sql/statements/show-create-table.md)
