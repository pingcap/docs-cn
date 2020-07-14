---
title: INSERT | TiDB SQL Statement Reference
summary: An overview of the usage of INSERT for the TiDB database.
aliases: ['/docs/dev/sql-statements/sql-statement-insert/','/docs/dev/reference/sql/statements/insert/']
---

# INSERT

This statement inserts new rows into a table.

## Synopsis

**InsertIntoStmt:**

![InsertIntoStmt](/media/sqlgram/InsertIntoStmt.png)

**TableOptimizerHints**

![TableOptimizerHints](/media/sqlgram/TableOptimizerHints.png)

**PriorityOpt:**

![PriorityOpt](/media/sqlgram/PriorityOpt.png)

**IgnoreOptional:**

![IgnoreOptional](/media/sqlgram/IgnoreOptional.png)

**IntoOpt:**

![IntoOpt](/media/sqlgram/IntoOpt.png)

**TableName:**

![TableName](/media/sqlgram/TableName.png)

**PartitionNameListOpt:**

![PartitionNameListOpt](/media/sqlgram/PartitionNameListOpt.png)

**InsertValues:**

![InsertValues](/media/sqlgram/InsertValues.png)

**OnDuplicateKeyUpdate:**

![OnDuplicateKeyUpdate](/media/sqlgram/OnDuplicateKeyUpdate.png)

## Examples

```sql
mysql> CREATE TABLE t1 (a INT);
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

* [DELETE](/sql-statements/sql-statement-delete.md)
* [SELECT](/sql-statements/sql-statement-select.md)
* [UPDATE](/sql-statements/sql-statement-update.md)
* [REPLACE](/sql-statements/sql-statement-replace.md)
