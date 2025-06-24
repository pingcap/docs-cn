---
title: SHOW CREATE TABLE | TiDB SQL 语句参考
summary: TiDB 数据库中 SHOW CREATE TABLE 的使用概述。
---

# SHOW CREATE TABLE

此语句显示使用 SQL 重新创建现有表的确切语句。

## 语法图

```ebnf+diagram
ShowCreateTableStmt ::=
    "SHOW" "CREATE" "TABLE" (SchemaName ".")? TableName
```

## 示例

```sql
mysql> CREATE TABLE t1 (a INT);
Query OK, 0 rows affected (0.12 sec)

mysql> SHOW CREATE TABLE t1\G
*************************** 1. row ***************************
       Table: t1
Create Table: CREATE TABLE `t1` (
  `a` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin
1 row in set (0.00 sec)
```

## MySQL 兼容性

TiDB 中的 `SHOW CREATE TABLE` 语句与 MySQL 完全兼容。如果发现任何兼容性差异，请[报告问题](https://docs.pingcap.com/tidb/stable/support)。

## 另请参阅

* [CREATE TABLE](/sql-statements/sql-statement-create-table.md)
* [DROP TABLE](/sql-statements/sql-statement-drop-table.md)
* [SHOW TABLES](/sql-statements/sql-statement-show-tables.md)
* [SHOW COLUMNS FROM](/sql-statements/sql-statement-show-columns-from.md)
