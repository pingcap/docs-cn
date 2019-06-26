---
title: DELETE | TiDB SQL Statement Reference 
summary: An overview of the usage of DELETE for the TiDB database.
category: reference
---

# DELETE

The `DELETE` statement removes rows from a specified table.

## Synopsis

**DeleteFromStmt:**

![DeleteFromStmt](/media/sqlgram-dev/DeleteFromStmt.png)

## Examples

```sql
mysql> CREATE TABLE t1 (id INT NOT NULL PRIMARY KEY auto_increment, c1 INT NOT NULL);
Query OK, 0 rows affected (0.11 sec)

mysql> INSERT INTO t1 (c1) VALUES (1),(2),(3),(4),(5);
Query OK, 5 rows affected (0.03 sec)
Records: 5  Duplicates: 0  Warnings: 0

mysql> SELECT * FROM t1;
+----+----+
| id | c1 |
+----+----+
|  1 |  1 |
|  2 |  2 |
|  3 |  3 |
|  4 |  4 |
|  5 |  5 |
+----+----+
5 rows in set (0.00 sec)

mysql> DELETE FROM t1 WHERE id = 4;
Query OK, 1 row affected (0.02 sec)

mysql> SELECT * FROM t1;
+----+----+
| id | c1 |
+----+----+
|  1 |  1 |
|  2 |  2 |
|  3 |  3 |
|  5 |  5 |
+----+----+
4 rows in set (0.00 sec)
```

## MySQL compatibility

This statement is understood to be fully compatible with MySQL. Any compatibility differences should be [reported via an issue](/report-issue.md) on GitHub.

## See also

* [INSERT](/reference/sql/statements/insert.md)
* [SELECT](/reference/sql/statements/select.md)
* [UPDATE](/reference/sql/statements/update.md)
* [REPLACE](/reference/sql/statements/replace.md)
