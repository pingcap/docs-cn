---
title: 删除视图 | TiDB SQL Statement Reference
summary: 视图删除使用方法概览。
category: reference
---

# 删除视图

`DROP VIEW` 语句用来删除指定数据库下的视图。对视图的删除不影响其引用到的表。

## 语法图

**DropViewStmt:**

![DropViewStmt](/media/sqlgram/DropViewStmt.png)

**TableNameList:**

![TableNameList](/media/sqlgram/TableNameList.png)

**TableName:**

![TableName](/media/sqlgram/TableName.png)

## 样例

```sql
mysql> CREATE TABLE t1 (id INT NOT NULL PRIMARY KEY auto_increment, c1 INT NOT NULL);
Query OK, 0 rows affected (0.11 sec)

mysql> INSERT INTO t1 (c1) VALUES (1),(2),(3),(4),(5);
Query OK, 5 rows affected (0.03 sec)
Records: 5  Duplicates: 0  Warnings: 0

mysql> CREATE VIEW v1 AS SELECT * FROM t1 WHERE c1 > 2;
Query OK, 0 rows affected (0.11 sec)

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

mysql> SELECT * FROM v1;
+----+----+
| id | c1 |
+----+----+
|  3 |  3 |
|  4 |  4 |
|  5 |  5 |
+----+----+
3 rows in set (0.00 sec)

mysql> DROP VIEW v1;
Query OK, 0 rows affected (0.23 sec)

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
```

## 与 MySQL 的兼容性

该特性与 MySQL 完全兼容。如遇到与 MySQL 不兼容性的问题，请在 GitHub 上 [创建一个 issue](/report-issue.md) 反馈给我们。

## 扩展阅读

* [DROP TABLE](/dev/reference/sql/statements/drop-table.md)
* [CREATE VIEW](/dev/reference/sql/statements/create-view.md)
