---
title: CREATE DATABASE
summary: TiDB 数据库中 CREATE DATABASE 的使用概况。
category: reference
---

# CREATE DATABASE

`CREATE DATABASE` 语句用于在 TiDB 上创建新数据库。按照 SQL 标准，“数据库” 一词在 MySQL 术语中最接近 “schema”。

## 总览

**CreateDatabaseStmt:**

![CreateDatabaseStmt](/media/sqlgram/CreateDatabaseStmt.png)

**DatabaseSym:**

![DatabaseSym](/media/sqlgram/DatabaseSym.png)

**IfNotExists:**

![IfNotExists](/media/sqlgram/IfNotExists.png)

**DBName:**

![DBName](/media/sqlgram/DBName.png)

**DatabaseOptionListOpt:**

![DatabaseOptionListOpt](/media/sqlgram/DatabaseOptionListOpt.png)

## 实例

```sql
mysql> CREATE DATABASE mynewdatabase;
Query OK, 0 rows affected (0.09 sec)

mysql> USE mynewdatabase;
Database changed
mysql> CREATE TABLE t1 (a int);
Query OK, 0 rows affected (0.11 sec)

mysql> SHOW TABLES;
+-------------------------+
| Tables_in_mynewdatabase |
+-------------------------+
| t1                      |
+-------------------------+
1 row in set (0.00 sec)
```

## MySQL 兼容性

`CREATE DATABASE` 语句可视为与 MySQL 完全兼容。如有任何兼容性差异，请在 GitHub 上 提交 [issue](/report-issue.md)。

## 另请参阅

* [USE](/dev/reference/sql/statements/use.md)
* [ALTER DATABASE](/dev/reference/sql/statements/alter-database.md)
* [DROP DATABASE](/dev/reference/sql/statements/drop-database.md)
* [SHOW CREATE DATABASE](/dev/reference/sql/statements/show-create-database.md)