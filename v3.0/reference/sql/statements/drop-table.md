---
title: DROP TABLE
summary: TiDB 数据库中 DROP TABLE 的使用概况。
category: reference
---

# DROP TABLE

`DROP TABLE` 语句用于从当前所选的数据库中删除表。如果表不存在则会报错，除非使用 `IF EXISTS` 修饰符。

按照设计，`DROP TABLE` 也会删除视图，因为视图与表共享相同的命名空间。

## 语法图

**DropTableStmt:**

![DropTableStmt](/media/sqlgram/DropTableStmt.png)

**TableOrTables:**

![TableOrTables](/media/sqlgram/TableOrTables.png)

**TableNameList:**

![TableNameList](/media/sqlgram/TableNameList.png)

## 示例

```sql
mysql> CREATE TABLE t1 (a INT);
Query OK, 0 rows affected (0.11 sec)

mysql> DROP TABLE t1;
Query OK, 0 rows affected (0.22 sec)

mysql> DROP TABLE table_not_exists;
ERROR 1051 (42S02): Unknown table 'test.table_not_exists'
mysql> DROP TABLE IF EXISTS table_not_exists;
Query OK, 0 rows affected (0.01 sec)

mysql> CREATE VIEW v1 AS SELECT 1;
Query OK, 0 rows affected (0.10 sec)

mysql> DROP TABLE v1;
Query OK, 0 rows affected (0.23 sec)
```

## MySQL 兼容性

* 在尝试删除不存在的表时，使用 `IF EXISTS` 删除表不会返回警告。[Issue #7867](https://github.com/pingcap/tidb/issues/7867)

## 另请参阅

* [DROP VIEW](/v3.0/reference/sql/statements/drop-view.md)
* [CREATE TABLE](/v3.0/reference/sql/statements/create-table.md)
* [SHOW CREATE TABLE](/v3.0/reference/sql/statements/show-create-table.md)
* [SHOW TABLES](/v3.0/reference/sql/statements/show-tables.md)