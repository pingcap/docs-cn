---
title: RENAME INDEX | TiDB SQL 语句参考
summary: TiDB 数据库中 RENAME INDEX 的使用概述。
---

# RENAME INDEX

`ALTER TABLE .. RENAME INDEX` 语句将现有索引重命名为新名称。在 TiDB 中，此操作是即时的，只需要进行元数据更改。

## 语法

```ebnf+diagram
AlterTableStmt
         ::= 'ALTER' 'IGNORE'? 'TABLE' TableName RenameIndexSpec ( ',' RenameIndexSpec )*

RenameIndexSpec
         ::= 'RENAME' ( 'KEY' | 'INDEX' ) Identifier 'TO' Identifier
```

## 示例

```sql
mysql> CREATE TABLE t1 (id INT NOT NULL PRIMARY KEY AUTO_INCREMENT, c1 INT NOT NULL, INDEX col1 (c1));
Query OK, 0 rows affected (0.11 sec)

mysql> SHOW CREATE TABLE t1\G
*************************** 1. row ***************************
       Table: t1
Create Table: CREATE TABLE `t1` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `c1` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `col1` (`c1`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin
1 row in set (0.00 sec)

mysql> ALTER TABLE t1 RENAME INDEX col1 TO c1;
Query OK, 0 rows affected (0.09 sec)

mysql> SHOW CREATE TABLE t1\G
*************************** 1. row ***************************
       Table: t1
Create Table: CREATE TABLE `t1` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `c1` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `c1` (`c1`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin
1 row in set (0.00 sec)
```

## MySQL 兼容性

TiDB 中的 `RENAME INDEX` 语句与 MySQL 完全兼容。如果发现任何兼容性差异，请[报告问题](https://docs.pingcap.com/tidb/stable/support)。

## 另请参阅

* [SHOW CREATE TABLE](/sql-statements/sql-statement-show-create-table.md)
* [CREATE INDEX](/sql-statements/sql-statement-create-index.md)
* [DROP INDEX](/sql-statements/sql-statement-drop-index.md)
* [SHOW INDEXES](/sql-statements/sql-statement-show-indexes.md)
* [ALTER INDEX](/sql-statements/sql-statement-alter-index.md)
