---
title: REPLACE
summary: TiDB 数据库中 REPLACE 的使用概况。
category: reference
---

# REPLACE

从语义上看，`REPLACE` 语句是 `DELETE` 语句和 `INSERT` 语句的结合，可用于简化应用程序代码。

## 语法图

**ReplaceIntoStmt:**

![ReplaceIntoStmt](/media/sqlgram/ReplaceIntoStmt.png)

**PriorityOpt:**

![PriorityOpt](/media/sqlgram/PriorityOpt.png)

**IntoOpt:**

![IntoOpt](/media/sqlgram/IntoOpt.png)

**TableName:**

![TableName](/media/sqlgram/TableName.png)

**InsertValues:**

![InsertValues](/media/sqlgram/InsertValues.png)

## 示例

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

## MySQL 兼容性

`REPLACE` 语句与 MySQL 完全兼容。如有任何兼容性差异，请在 GitHub 上提交 [issue](v3.0/report-issue.md)。

## 另请参阅

* [DELETE](v3.0/reference/sql/statements/delete.md)
* [INSERT](v3.0/reference/sql/statements/insert.md)
* [SELECT](v3.0/reference/sql/statements/select.md)
* [UPDATE](v3.0/reference/sql/statements/update.md)