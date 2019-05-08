---
title: INSERT | TiDB SQL Statement Reference 
summary: An overview of the usage of INSERT for the TiDB database.
category: reference
---

# INSERT

This statement inserts new rows into a table.


## Synopsis

**InsertIntoStmt:**

![InsertIntoStmt](/media/sqlgram/InsertIntoStmt.png)

**PriorityOpt:**

![PriorityOpt](/media/sqlgram/PriorityOpt.png)

**IgnoreOptional:**

![IgnoreOptional](/media/sqlgram/IgnoreOptional.png)

**IntoOpt:**

![IntoOpt](/media/sqlgram/IntoOpt.png)

**TableName:**

![TableName](/media/sqlgram/TableName.png)

**InsertValues:**

![InsertValues](/media/sqlgram/InsertValues.png)

## Examples

```sql
mysql> CREATE TABLE t1 (a int);
Query OK, 0 rows affected (0.11 sec)

mysql> CREATE TABLE t2 LIKE t1;
Query OK, 0 rows affected (0.11 sec)

mysql> INSERT INTO t1 VALUES (1);
Query OK, 1 row affected (0.02 sec)

mysql> INSERT INTO t1 (a) VALUES (1);
Query OK, 1 row affected (0.01 sec)

mysql> INSERT INTO t2 SELECT * FROM t1;
Query OK, 2 rows affected (0.01 sec)
Records: 2  Duplicates: 0  Warnings: 0

mysql> SELECT * FROM t1;
+------+
| a    |
+------+
|    1 |
|    1 |
+------+
2 rows in set (0.00 sec)

mysql> SELECT * FROM t2;
+------+
| a    |
+------+
|    1 |
|    1 |
+------+
2 rows in set (0.00 sec)

mysql> INSERT INTO t2 VALUES (2),(3),(4);
Query OK, 3 rows affected (0.02 sec)
Records: 3  Duplicates: 0  Warnings: 0

mysql> SELECT * FROM t2;
+------+
| a    |
+------+
|    1 |
|    1 |
|    2 |
|    3 |
|    4 |
+------+
5 rows in set (0.00 sec)
```

## MySQL compatibility

This statement is understood to be fully compatible with MySQL. Any compatibility differences should be [reported via an issue](/report-issue.md) on GitHub.

## See also

* [DELETE](/dev/reference/sql/statements/delete.md)
* [SELECT](/dev/reference/sql/statements/select.md)
* [UPDATE](/dev/reference/sql/statements/update.md)
* [REPLACE](/dev/reference/sql/statements/replace.md)
