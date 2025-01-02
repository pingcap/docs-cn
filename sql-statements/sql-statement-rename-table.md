---
title: RENAME TABLE
summary: TiDB 数据库中 RENAME TABLE 的使用概况。
aliases: ['/docs-cn/dev/sql-statements/sql-statement-rename-table/','/docs-cn/dev/reference/sql/statements/rename-table/']
---

# RENAME TABLE

`RENAME TABLE` 语句用于对已有表进行重命名，支持同时重命名多个表并跨数据库进行重命名。

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

```sql
RENAME TABLE db1.t1 To db2.t2, db3.t3 To db4.t4;
```

## MySQL 兼容性

`RENAME TABLE` 语句与 MySQL 完全兼容。如发现任何兼容性差异，请尝试 [TiDB 支持资源](/support.md)。

## 另请参阅

* [CREATE TABLE](/sql-statements/sql-statement-create-table.md)
* [SHOW TABLES](/sql-statements/sql-statement-show-tables.md)
* [ALTER TABLE](/sql-statements/sql-statement-alter-table.md)
