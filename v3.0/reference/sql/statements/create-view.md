---
title: CREATE VIEW
summary: TiDB 数据库中 CREATE VIEW 的使用概况。
category: reference
---

# CREATE VIEW

使用 `CREATE VIEW` 语句将 `SELECT` 语句保存为类似于表的可查询对象。TiDB 中的视图是非物化的，这意味着在查询视图时，TiDB 将在内部重写查询，以将视图定义与 SQL 查询结合起来。

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

## 示例

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

## MySQL 兼容性

* 目前 TiDB 中的视图不可插入且不可更新。

## 另请参阅

* [CREATE TABLE](/v3.0/reference/sql/statements/create-table.md)
* [SHOW CREATE TABLE](/v3.0/reference/sql/statements/show-create-table.md)
* [DROP TABLE](/v3.0/reference/sql/statements/drop-table.md)