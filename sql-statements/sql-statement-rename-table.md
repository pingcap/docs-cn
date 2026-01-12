---
title: RENAME TABLE
summary: TiDB 数据库中 RENAME TABLE 的使用概况。
aliases: ['/docs-cn/dev/sql-statements/sql-statement-rename-table/','/docs-cn/dev/reference/sql/statements/rename-table/']
---

# RENAME TABLE

`RENAME TABLE` 语句用于重命名现有表和视图，支持同时重命名多个表及跨数据库重命名。

## 语法图

```ebnf+diagram
RenameTableStmt ::=
    'RENAME' 'TABLE' TableToTable ( ',' TableToTable )*

TableToTable ::=
    TableName 'TO' TableName
```

## 示例

```sql
CREATE TABLE t1 (a int);
```

```
Query OK, 0 rows affected (0.12 sec)
```

```sql
SHOW TABLES;
```

```
+----------------+
| Tables_in_test |
+----------------+
| t1             |
+----------------+
1 row in set (0.00 sec)
```

```sql
RENAME TABLE t1 TO t2;
```

```
Query OK, 0 rows affected (0.08 sec)
```

```sql
SHOW TABLES;
```

```
+----------------+
| Tables_in_test |
+----------------+
| t2             |
+----------------+
1 row in set (0.00 sec)
```

以下示例演示了如何跨数据库重命名多个表（假设数据库 `db1`、`db2`、`db3` 和 `db4` 已存在，表 `db1.t1` 和 `db3.t3` 已存在）：

```sql
RENAME TABLE db1.t1 To db2.t2, db3.t3 To db4.t4;
```

```
Query OK, 0 rows affected (0.08 sec)
```

```sql
USE db1; SHOW TABLES;
```

```
Database changed
Empty set (0.00 sec)
```

```sql
USE db2; SHOW TABLES;
```

```
Database changed
+---------------+
| Tables_in_db2 |
+---------------+
| t2            |
+---------------+
1 row in set (0.00 sec)
```

```sql
USE db3; SHOW TABLES;
```

```
Database changed
Empty set (0.00 sec)
```

```sql
USE db4; SHOW TABLES;
```

```
Database changed
+---------------+
| Tables_in_db4 |
+---------------+
| t4            |
+---------------+
1 row in set (0.00 sec)
```

原子重命名可以确保在交换表时，表始终存在。

```sql
CREATE TABLE t1(id int PRIMARY KEY);
```

```
Query OK, 0 rows affected (0.04 sec)
```

```sql
CREATE TABLE t1_new(id int PRIMARY KEY, n CHAR(0));
````

```
Query OK, 0 rows affected (0.04 sec)
```

```sql
RENAME TABLE t1 TO t1_old, t1_new TO t1;
```

```
Query OK, 0 rows affected (0.07 sec)
```

```sql
SHOW CREATE TABLE t1\G
```

```
*************************** 1. row ***************************
       Table: t1
Create Table: CREATE TABLE `t1` (
  `id` int NOT NULL,
  `n` char(0) DEFAULT NULL,
  PRIMARY KEY (`id`) /*T![clustered_index] CLUSTERED */
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin
1 row in set (0.00 sec)
```

## MySQL 兼容性

`RENAME TABLE` 语句与 MySQL 完全兼容。如发现任何兼容性差异，请尝试 [TiDB 支持资源](/support.md)。

## 另请参阅

* [CREATE TABLE](/sql-statements/sql-statement-create-table.md)
* [SHOW TABLES](/sql-statements/sql-statement-show-tables.md)
* [ALTER TABLE](/sql-statements/sql-statement-alter-table.md)
