---
title: DROP DATABASE
summary: TiDB 数据库中 DROP DATABASE 的使用概况。
category: reference
---

# DROP DATABASE

`DROP DATABASE` 语句用于永久删除指定的数据库 schema，以及删除所有在 schema 中创建的表和视图。与被删数据库相关联的用户权限不受影响。

## 语法图

**DropDatabaseStmt:**

![DropDatabaseStmt](/media/sqlgram/DropDatabaseStmt.png)

**DatabaseSym:**

![DatabaseSym](/media/sqlgram/DatabaseSym.png)

**IfExists:**

![IfExists](/media/sqlgram/IfExists.png)

**DBName:**

![DBName](/media/sqlgram/DBName.png)

## 示例

```sql
mysql> SHOW DATABASES;
+--------------------+
| Database           |
+--------------------+
| INFORMATION_SCHEMA |
| PERFORMANCE_SCHEMA |
| mysql              |
| test               |
+--------------------+
4 rows in set (0.00 sec)

mysql> DROP DATABASE test;
Query OK, 0 rows affected (0.25 sec)

mysql> SHOW DATABASES;
+--------------------+
| Database           |
+--------------------+
| INFORMATION_SCHEMA |
| PERFORMANCE_SCHEMA |
| mysql              |
+--------------------+
3 rows in set (0.00 sec)
```

## MySQL 兼容性

`DROP DATABASE` 语句与 MySQL 完全兼容。如有任何兼容性差异，请在 GitHub 上提交 [issue](/v2.1/report-issue.md)。

## 另请参阅

* [CREATE DATABASE](/v2.1/reference/sql/statements/create-database.md)
* [ALTER DATABASE](/v2.1/reference/sql/statements/alter-database.md)
