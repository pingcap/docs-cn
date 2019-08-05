---
title: REPLACE | TiDB SQL Statement Reference
summary: An overview of the usage of REPLACE for the TiDB database.
category: reference
---

# REPLACE

The `REPLACE` statement is semantically a combined `DELETE`+`INSERT` statement. It can be used to simplify application code.

## Synopsis

**ReplaceIntoStmt:**

![ReplaceIntoStmt](/media/sqlgram-v2.1/ReplaceIntoStmt.png)

**PriorityOpt:**

![PriorityOpt](/media/sqlgram-v2.1/PriorityOpt.png)

**IntoOpt:**

![IntoOpt](/media/sqlgram-v2.1/IntoOpt.png)

**TableName:**

![TableName](/media/sqlgram-v2.1/TableName.png)

**InsertValues:**

![InsertValues](/media/sqlgram-v2.1/InsertValues.png)

## Examples

```sql
mysql> CREATE TABLE t1 (id INT NOT NULL PRIMARY KEY auto_increment, c1 INT NOT NULL);
Query OK, 0 rows affected (0.12 sec)

mysql> INSERT INTO t1 (c1) VALUES (1), (2), (3);
Query OK, 3 rows affected (0.02 sec)
Records: 3  Duplicates: 0  Warnings: 0

mysql> SELECT * FROM t1;
+----+----+
| id | c1 |
+----+----+
|  1 |  1 |
|  2 |  2 |
|  3 |  3 |
+----+----+
3 rows in set (0.00 sec)

mysql> REPLACE INTO t1 (id, c1) VALUES(3, 99);
Query OK, 2 rows affected (0.01 sec)

mysql> SELECT * FROM t1;
+----+----+
| id | c1 |
+----+----+
|  1 |  1 |
|  2 |  2 |
|  3 | 99 |
+----+----+
3 rows in set (0.00 sec)
```

## MySQL compatibility

This statement is understood to be fully compatible with MySQL. Any compatibility differences should be [reported via an issue](/report-issue.md) on GitHub.

## See also

* [DELETE](/reference/sql/statements/delete.md)
* [INSERT](/reference/sql/statements/insert.md)
* [SELECT](/reference/sql/statements/select.md)
* [UPDATE](/reference/sql/statements/update.md)
