---
title: 视图创建 | TiDB SQL Statement Reference
summary: 视图创建使用方法概览。
category: reference
---

# 视图创建

视图类似于一个虚拟表，通过 `CREATE VIEW` 语句可以创建一个视图。TiDB 当前仅支持非物化的视图。当对一个视图进行查询时，TiDB 会隐式地将创建该视图时所定义的 `SELECT` 语句嵌入查询中。

## 语法图

**CreateViewStmt:**

![CreateViewStmt](/media/sqlgram/CreateViewStmt.png)

**OrReplace:**

![OrReplace](/media/sqlgram/OrReplace.png)

**ViewAlgorithm:**

![ViewAlgorithm](/media/sqlgram/ViewAlgorithm.png)

**ViewDefiner:**

![ViewDefiner](/media/sqlgram/ViewDefiner.png)

**ViewSQLSecurity:**

![ViewSQLSecurity](/media/sqlgram/ViewSQLSecurity.png)

**ViewName:**

![ViewName](/media/sqlgram/ViewName.png)

**ViewFieldList:**

![ViewFieldList](/media/sqlgram/ViewFieldList.png)

**ViewCheckOption:**

![ViewCheckOption](/media/sqlgram/ViewCheckOption.png)

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

mysql> INSERT INTO t1 (c1) VALUES (6);
Query OK, 1 row affected (0.01 sec)

mysql> SELECT * FROM v1;
+----+----+
| id | c1 |
+----+----+
|  3 |  3 |
|  4 |  4 |
|  5 |  5 |
|  6 |  6 |
+----+----+
4 rows in set (0.00 sec)

mysql> INSERT INTO v1 (c1) VALUES (7);
ERROR 1105 (HY000): insert into view v1 is not supported now.
```

## 与 MySQL 的兼容性

* TiDB 中目前不支持视图的插入与更新操作。

## 扩展阅读

* [CREATE TABLE](/dev/reference/sql/statements/create-table.md)
* [SHOW CREATE TABLE](/dev/reference/sql/statements/show-create-table.md)
* [DROP TABLE](/dev/reference/sql/statements/drop-table.md)
