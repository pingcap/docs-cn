---
title: CREATE TABLE LIKE | TiDB SQL 语句参考
summary: TiDB 数据库中 CREATE TABLE LIKE 的使用概述。
---

# CREATE TABLE LIKE

此语句用于复制现有表的定义，但不复制任何数据。

## 语法

```ebnf+diagram
CreateTableLikeStmt ::=
    'CREATE' OptTemporary 'TABLE' IfNotExists TableName LikeTableWithOrWithoutParen OnCommitOpt

OptTemporary ::=
    ( 'TEMPORARY' | ('GLOBAL' 'TEMPORARY') )?

LikeTableWithOrWithoutParen ::=
    'LIKE' TableName
|   '(' 'LIKE' TableName ')'

OnCommitOpt ::=
    ('ON' 'COMMIT' 'DELETE' 'ROWS')?
```

## 示例

```sql
mysql> CREATE TABLE t1 (a INT NOT NULL);
Query OK, 0 rows affected (0.13 sec)

mysql> INSERT INTO t1 VALUES (1),(2),(3),(4),(5);
Query OK, 5 rows affected (0.02 sec)
Records: 5  Duplicates: 0  Warnings: 0

mysql> SELECT * FROM t1;
+---+
| a |
+---+
| 1 |
| 2 |
| 3 |
| 4 |
| 5 |
+---+
5 rows in set (0.00 sec)

mysql> CREATE TABLE t2 LIKE t1;
Query OK, 0 rows affected (0.10 sec)

mysql> SELECT * FROM t2;
Empty set (0.00 sec)
```

## 预切分 Region

如果要复制的表定义了 `PRE_SPLIT_REGIONS` 属性，使用 `CREATE TABLE LIKE` 语句创建的表会继承这个属性，并且新表上的 Region 会被切分。关于 `PRE_SPLIT_REGIONS` 的详细信息，请参见 [`CREATE TABLE` 语句](/sql-statements/sql-statement-create-table.md)。

## MySQL 兼容性

TiDB 中的 `CREATE TABLE LIKE` 语句与 MySQL 完全兼容。如果发现任何兼容性差异，请[报告问题](https://docs.pingcap.com/tidb/stable/support)。

## 另请参阅

* [CREATE TABLE](/sql-statements/sql-statement-create-table.md)
* [SHOW CREATE TABLE](/sql-statements/sql-statement-show-create-table.md)
