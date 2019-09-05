---
title: DELETE
summary: TiDB 数据库中 DELETE 的使用概况。
category: reference
---

# DELETE

`DELETE` 语句用于从指定的表中删除行。

## 语法图

**DeleteFromStmt:**

![DeleteFromStmt](/media/sqlgram/DeleteFromStmt.png)

## 示例

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

## MySQL 兼容性

`DELETE` 语句与 MySQL 完全兼容。如有任何兼容性差异，请在 GitHub 上提交 [issue](/v3.0/report-issue.md)。

## 另请参阅

* [INSERT](/v3.0/reference/sql/statements/insert.md)
* [SELECT](/v3.0/reference/sql/statements/select.md)
* [UPDATE](/v3.0/reference/sql/statements/update.md)
* [REPLACE](/v3.0/reference/sql/statements/replace.md)