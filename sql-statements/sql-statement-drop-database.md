---
title: DROP DATABASE | TiDB SQL 语句参考
summary: TiDB 数据库中 DROP DATABASE 的使用概述。
---

# DROP DATABASE

`DROP DATABASE` 语句永久删除指定的数据库架构，以及其中创建的所有表和视图。与被删除数据库相关联的用户权限不受影响。

## 语法概要

```ebnf+diagram
DropDatabaseStmt ::=
    'DROP' 'DATABASE' IfExists DBName

IfExists ::= ( 'IF' 'EXISTS' )?
```

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

TiDB 中的 `DROP DATABASE` 语句与 MySQL 完全兼容。如果发现任何兼容性差异，请[报告 bug](https://docs.pingcap.com/tidb/stable/support)。

## 另请参阅

* [CREATE DATABASE](/sql-statements/sql-statement-create-database.md)
* [ALTER DATABASE](/sql-statements/sql-statement-alter-database.md)
