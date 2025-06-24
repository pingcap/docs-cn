---
title: SHOW CREATE DATABASE
summary: TiDB 数据库中 SHOW CREATE DATABASE 的使用概览。
---

# SHOW CREATE DATABASE

`SHOW CREATE DATABASE` 用于显示重新创建现有数据库所需的精确 SQL 语句。`SHOW CREATE SCHEMA` 是它的同义词。

## 语法图

**ShowCreateDatabaseStmt:**

```ebnf+diagram
ShowCreateDatabaseStmt ::=
    "SHOW" "CREATE" ("DATABASE" | "SCHEMA") ("IF" "NOT" "EXISTS")? DBName
```

## 示例

```sql
CREATE DATABASE test;
```

```sql
Query OK, 0 rows affected (0.12 sec)
```

```sql
SHOW CREATE DATABASE test;
```

```sql
+----------+------------------------------------------------------------------+
| Database | Create Database                                                  |
+----------+------------------------------------------------------------------+
| test     | CREATE DATABASE `test` /*!40100 DEFAULT CHARACTER SET utf8mb4 */ |
+----------+------------------------------------------------------------------+
1 row in set (0.00 sec)
```

```sql
SHOW CREATE SCHEMA IF NOT EXISTS test;
```

```sql
+----------+-------------------------------------------------------------------------------------------+
| Database | Create Database                                                                           |
+----------+-------------------------------------------------------------------------------------------+
| test     | CREATE DATABASE /*!32312 IF NOT EXISTS*/ `test` /*!40100 DEFAULT CHARACTER SET utf8mb4 */ |
+----------+-------------------------------------------------------------------------------------------+
1 row in set (0.00 sec)
```

## MySQL 兼容性

`SHOW CREATE DATABASE` 预期与 MySQL 完全兼容。如果发现任何兼容性差异，请[报告问题](https://docs.pingcap.com/tidb/stable/support)。

## 另请参阅

* [CREATE TABLE](/sql-statements/sql-statement-create-table.md)
* [DROP TABLE](/sql-statements/sql-statement-drop-table.md)
* [SHOW TABLES](/sql-statements/sql-statement-show-tables.md)
* [SHOW COLUMNS FROM](/sql-statements/sql-statement-show-columns-from.md)
