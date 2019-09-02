---
title: INSERT
summary: TiDB 数据库中 INSERT 的使用概况。
category: reference
---

# INSERT

使用 `INSERT` 语句在表中插入新行。

## 语法图

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

## 示例

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

## MySQL 兼容性

`INSERT` 语句与 MySQL 完全兼容。如有任何兼容性差异，请在 GitHub 上提交 [issue](v2.1/report-issue.md)。

## 另请参阅

* [DELETE](v2.1/reference/sql/statements/delete.md)
* [SELECT](v2.1/reference/sql/statements/select.md)
* [UPDATE](v2.1/reference/sql/statements/update.md)
* [REPLACE](v2.1/reference/sql/statements/replace.md)
