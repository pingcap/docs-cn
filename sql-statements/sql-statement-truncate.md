---
title: TRUNCATE | TiDB SQL 语句参考
summary: TiDB 数据库中 TRUNCATE 的使用概览。
---

# TRUNCATE

`TRUNCATE` 语句以非事务方式删除表中的所有数据。`TRUNCATE` 在语义上可以被理解为等同于 `DROP TABLE` + 使用之前的定义 `CREATE TABLE`。

`TRUNCATE TABLE tableName` 和 `TRUNCATE tableName` 都是有效的语法。

## 语法

```ebnf+diagram
TruncateTableStmt ::=
    "TRUNCATE" ( "TABLE" )? TableName

TableName ::=
    (Identifier ".")? Identifier
```

## 示例

```sql
mysql> CREATE TABLE t1 (a INT NOT NULL PRIMARY KEY);
Query OK, 0 rows affected (0.11 sec)

mysql> INSERT INTO t1 VALUES (1),(2),(3),(4),(5);
Query OK, 5 rows affected (0.01 sec)
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

mysql> TRUNCATE t1;
Query OK, 0 rows affected (0.11 sec)

mysql> SELECT * FROM t1;
Empty set (0.00 sec)

mysql> INSERT INTO t1 VALUES (1),(2),(3),(4),(5);
Query OK, 5 rows affected (0.01 sec)
Records: 5  Duplicates: 0  Warnings: 0

mysql> TRUNCATE TABLE t1;
Query OK, 0 rows affected (0.11 sec)
```

## MySQL 兼容性

TiDB 中的 `TRUNCATE` 语句与 MySQL 完全兼容。如果发现任何兼容性差异，请[报告问题](https://docs.pingcap.com/tidb/stable/support)。

## 另请参阅

* [DROP TABLE](/sql-statements/sql-statement-drop-table.md)
* [DELETE](/sql-statements/sql-statement-delete.md)
* [CREATE TABLE](/sql-statements/sql-statement-create-table.md)
* [SHOW CREATE TABLE](/sql-statements/sql-statement-show-create-table.md)
