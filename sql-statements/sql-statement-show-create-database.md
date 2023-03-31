---
title: SHOW CREATE DATABASE
summary: TiDB 数据库中 SHOW CREATE DATABASE 的使用概况。
---

# SHOW CREATE DATABASE

`SHOW CREATE DATABASE` 语句用于显示用 SQL 重新创建已有库的确切语句。`SHOW CREATE SCHEMA` 与其同义。

## 语法图

**ShowCreateDatabaseStmt:**

```ebnf+diagram
ShowCreateDatabaseStmt ::=
    "SHOW" "CREATE" "DATABASE" | "SCHEMA" ("IF" "NOT" "EXISTS")? DBName
```

## 示例

{{< copyable "sql" >}}

```sql
CREATE DATABASE test;
```

```
Query OK, 0 rows affected (0.12 sec)
```

{{< copyable "sql" >}}

```sql
SHOW CREATE DATABASE test;
```

```
+----------+------------------------------------------------------------------+
| Database | Create Database                                                  |
+----------+------------------------------------------------------------------+
| test     | CREATE DATABASE `test` /*!40100 DEFAULT CHARACTER SET utf8mb4 */ |
+----------+------------------------------------------------------------------+
1 row in set (0.00 sec)
```

{{< copyable "sql" >}}

```sql
SHOW CREATE SCHEMA IF NOT EXISTS test;
```

```
+----------+-------------------------------------------------------------------------------------------+
| Database | Create Database                                                                           |
+----------+-------------------------------------------------------------------------------------------+
| test     | CREATE DATABASE /*!32312 IF NOT EXISTS*/ `test` /*!40100 DEFAULT CHARACTER SET utf8mb4 */ |
+----------+-------------------------------------------------------------------------------------------+
1 row in set (0.00 sec)
```

## MySQL 兼容性

`SHOW CREATE DATABASE` 语句与 MySQL 完全兼容。如发现任何兼容性差异，请在 GitHub 上提交 [issue](https://github.com/pingcap/tidb/issues/new/choose)。

## 另请参阅

* [CREATE TABLE](/sql-statements/sql-statement-create-table.md)
* [DROP TABLE](/sql-statements/sql-statement-drop-table.md)
* [SHOW TABLES](/sql-statements/sql-statement-show-tables.md)
* [SHOW COLUMNS FROM](/sql-statements/sql-statement-show-columns-from.md)
