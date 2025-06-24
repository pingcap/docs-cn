---
title: DROP TABLE | TiDB SQL 语句参考
summary: TiDB 数据库中 DROP TABLE 的使用概览。
---

# DROP TABLE

此语句从当前选择的数据库中删除一个表。如果表不存在，将返回错误，除非使用 `IF EXISTS` 修饰符。

## 语法

```ebnf+diagram
DropTableStmt ::=
    'DROP' OptTemporary TableOrTables IfExists TableNameList RestrictOrCascadeOpt

OptTemporary ::=
    ( 'TEMPORARY' | ('GLOBAL' 'TEMPORARY') )?

TableOrTables ::=
    'TABLE'
|   'TABLES'

TableNameList ::=
    TableName ( ',' TableName )*
```

## 删除临时表

你可以使用以下语法来删除普通表和临时表：

- 使用 `DROP TEMPORARY TABLE` 删除本地临时表。
- 使用 `DROP GLOBAL TEMPORARY TABLE` 删除全局临时表。
- 使用 `DROP TABLE` 删除普通表或临时表。

## 示例

```sql
mysql> CREATE TABLE t1 (a INT);
Query OK, 0 rows affected (0.11 sec)

mysql> DROP TABLE t1;
Query OK, 0 rows affected (0.22 sec)

mysql> DROP TABLE table_not_exists;
ERROR 1051 (42S02): Unknown table 'test.table_not_exists'

mysql> DROP TABLE IF EXISTS table_not_exists;
Query OK, 0 rows affected, 1 warning (0.01 sec)

mysql> SHOW WARNINGS;
+-------+------+---------------------------------------+
| Level | Code | Message                               |
+-------+------+---------------------------------------+
| Note  | 1051 | Unknown table 'test.table_not_exists' |
+-------+------+---------------------------------------+
1 row in set (0.01 sec)

mysql> CREATE VIEW v1 AS SELECT 1;
Query OK, 0 rows affected (0.10 sec)

mysql> DROP TABLE v1;
Query OK, 0 rows affected (0.23 sec)
```

## MySQL 兼容性

目前，`RESTRICT` 和 `CASCADE` 仅在语法上支持。

## 另请参阅

* [CREATE TABLE](/sql-statements/sql-statement-create-table.md)
* [SHOW CREATE TABLE](/sql-statements/sql-statement-show-create-table.md)
* [SHOW TABLES](/sql-statements/sql-statement-show-tables.md)
