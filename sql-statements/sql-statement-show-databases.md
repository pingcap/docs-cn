---
title: SHOW DATABASES | TiDB SQL 语句参考
summary: TiDB 数据库中 SHOW DATABASES 的使用概览。
---

# SHOW DATABASES

该语句显示当前用户具有权限的数据库列表。当前用户无权访问的数据库将在列表中隐藏。`information_schema` 数据库始终在数据库列表中首先显示。

`SHOW SCHEMAS` 是该语句的别名。

## 语法图

```ebnf+diagram
ShowDatabasesStmt ::=
    "SHOW" "DATABASES" ShowLikeOrWhere?

ShowLikeOrWhere ::=
    "LIKE" SimpleExpr
|   "WHERE" Expression
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

mysql> CREATE DATABASE mynewdb;
Query OK, 0 rows affected (0.10 sec)

mysql> SHOW DATABASES;
+--------------------+
| Database           |
+--------------------+
| INFORMATION_SCHEMA |
| PERFORMANCE_SCHEMA |
| mynewdb            |
| mysql              |
| test               |
+--------------------+
5 rows in set (0.00 sec)
```

## MySQL 兼容性

TiDB 中的 `SHOW DATABASES` 语句与 MySQL 完全兼容。如果发现任何兼容性差异，请[报告问题](https://docs.pingcap.com/tidb/stable/support)。

## 另请参阅

* [SHOW SCHEMAS](/sql-statements/sql-statement-show-schemas.md)
* [DROP DATABASE](/sql-statements/sql-statement-drop-database.md)
* [CREATE DATABASE](/sql-statements/sql-statement-create-database.md)
* [`INFORMATION_SCHEMA.SCHEMATA`](/information-schema/information-schema-schemata.md)
