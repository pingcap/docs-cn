---
title: DROP DATABASE
summary: TiDB 数据库中 DROP DATABASE 的使用概况。
aliases: ['/docs-cn/dev/sql-statements/sql-statement-drop-database/','/docs-cn/dev/reference/sql/statements/drop-database/']
---

# DROP DATABASE

`DROP DATABASE` 语句用于永久删除指定的数据库 schema，以及删除所有在 schema 中创建的表和视图。与被删数据库相关联的用户权限不受影响。

## 语法图

```ebnf+diagram
DropDatabaseStmt ::=
    'DROP' 'DATABASE' IfExists DBName

IfExists ::= ( 'IF' 'EXISTS' )?
```

## 示例

{{< copyable "sql" >}}

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

{{< copyable "sql" >}}

```sql
DROP DATABASE test;
```

```
Query OK, 0 rows affected (0.25 sec)
```

{{< copyable "sql" >}}

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
+--------------------+
3 rows in set (0.00 sec)
```

## MySQL 兼容性

`DROP DATABASE` 语句与 MySQL 完全兼容。如发现任何兼容性差异，请在 GitHub 上提交 [issue](https://github.com/pingcap/tidb/issues/new/choose)。

## 另请参阅

* [CREATE DATABASE](/sql-statements/sql-statement-create-database.md)
* [ALTER DATABASE](/sql-statements/sql-statement-alter-database.md)
