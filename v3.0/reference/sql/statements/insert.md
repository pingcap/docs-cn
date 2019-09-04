---
title: INSERT | TiDB SQL Statement Reference
summary: An overview of the usage of INSERT for the TiDB database.
category: reference
---

# INSERT

This statement inserts new rows into a table.

## Synopsis

**InsertIntoStmt:**

![InsertIntoStmt](/media/sqlgram-v3.0/InsertIntoStmt.png)

**PriorityOpt:**

![PriorityOpt](/media/sqlgram-v3.0/PriorityOpt.png)

**IgnoreOptional:**

![IgnoreOptional](/media/sqlgram-v3.0/IgnoreOptional.png)

**IntoOpt:**

![IntoOpt](/media/sqlgram-v3.0/IntoOpt.png)

**TableName:**

![TableName](/media/sqlgram-v3.0/TableName.png)

**InsertValues:**

![InsertValues](/media/sqlgram-v3.0/InsertValues.png)

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

This statement is understood to be fully compatible with MySQL. Any compatibility differences should be [reported via an issue](/v3.0/report-issue.md) on GitHub.

## See also

* [DELETE](/v3.0/reference/sql/statements/delete.md)
* [SELECT](/v3.0/reference/sql/statements/select.md)
* [UPDATE](/v3.0/reference/sql/statements/update.md)
* [REPLACE](/v3.0/reference/sql/statements/replace.md)
