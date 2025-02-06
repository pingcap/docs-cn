---
title: SHOW DATABASES
summary: TiDB 数据库中 SHOW DATABASES 的使用概况。
aliases: ['/docs-cn/dev/sql-statements/sql-statement-show-databases/','/docs-cn/dev/reference/sql/statements/show-databases/']
---

# SHOW DATABASES

`SHOW DATABASES` 语句用于显示当前用户有权访问的数据库列表。当前用户无权访问的数据库将从列表中隐藏。`information_schema` 数据库始终出现在列表的最前面。

`SHOW SCHEMAS` 是 `SHOW DATABASES` 语句的别名。

## 语法图

**ShowDatabasesStmt:**

```ebnf+diagram
ShowDatabasesStmt ::=
    "SHOW" "DATABASES" ShowLikeOrWhere?

ShowLikeOrWhere ::=
    "LIKE" SimpleExpr
|   "WHERE" Expression
```

## 示例

```sql
SHOW DATABASES;
```

```
+--------------------+
| Database           |
+--------------------+
| INFORMATION_SCHEMA |
| PERFORMANCE_SCHEMA |
| mysql              |
| test               |
+--------------------+
4 rows in set (0.00 sec)
```

```sql
CREATE DATABASE mynewdb;
```

```
Query OK, 0 rows affected (0.10 sec)
```

```sql
SHOW DATABASES;
```

```
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

`SHOW DATABASES` 语句与 MySQL 完全兼容。如发现任何兼容性差异，请尝试 [TiDB 支持资源](/support.md)。

## 另请参阅

* [SHOW SCHEMAS](/sql-statements/sql-statement-show-schemas.md)
* [DROP DATABASE](/sql-statements/sql-statement-drop-database.md)
* [CREATE DATABASE](/sql-statements/sql-statement-create-database.md)
* [`INFORMATION_SCHEMA.SCHEMATA`](/information-schema/information-schema-schemata.md)
