---
title: SHOW DATABASES
summary: TiDB 数据库中 SHOW DATABASES 的使用概况。
---

# SHOW DATABASES

`SHOW DATABASES` 语句用于显示当前用户有权访问的数据库列表。当前用户无权访问的数据库将从列表中隐藏。`information_schema` 数据库始终出现在列表的最前面。

`SHOW SCHEMAS` 是 `SHOW DATABASES` 语句的别名。

## 语法图

**ShowDatabasesStmt:**

![ShowDatabasesStmt](/media/sqlgram/ShowDatabasesStmt.png)

**ShowLikeOrWhereOpt:**

![ShowLikeOrWhereOpt](/media/sqlgram/ShowLikeOrWhereOpt.png)

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
CREATE DATABASE mynewdb;
```

```
Query OK, 0 rows affected (0.10 sec)
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
| mynewdb            |
| mysql              |
| test               |
+--------------------+
5 rows in set (0.00 sec)
```

## MySQL 兼容性

`SHOW DATABASES` 语句与 MySQL 完全兼容。如发现任何兼容性差异，请在 GitHub 上提交 [issue](https://github.com/pingcap/tidb/issues/new/choose)。

## 另请参阅

* [SHOW SCHEMAS](/sql-statements/sql-statement-show-schemas.md)
* [DROP DATABASE](/sql-statements/sql-statement-drop-database.md)
* [CREATE DATABASE](/sql-statements/sql-statement-create-database.md)
