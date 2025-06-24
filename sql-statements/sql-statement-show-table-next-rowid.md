---
title: SHOW TABLE NEXT_ROW_ID
summary: 了解在 TiDB 中 `SHOW TABLE NEXT_ROW_ID` 的用法。
---

# SHOW TABLE NEXT_ROW_ID

`SHOW TABLE NEXT_ROW_ID` 用于显示表中某些特殊列的详细信息，包括：

* TiDB 自动创建的 [`AUTO_INCREMENT`](/auto-increment.md) 列，即 `_tidb_rowid` 列。
* 用户创建的 `AUTO_INCREMENT` 列。
* 用户创建的 [`AUTO_RANDOM`](/auto-random.md) 列。
* 用户创建的 [`SEQUENCE`](/sql-statements/sql-statement-create-sequence.md)。

## 语法概要

```ebnf+diagram
ShowTableNextRowIDStmt ::=
    "SHOW" "TABLE" (SchemaName ".")? TableName "NEXT_ROW_ID"
```

## 示例

对于新创建的表，由于尚未分配行 ID，`NEXT_GLOBAL_ROW_ID` 为 `1`。

```sql
CREATE TABLE t(a int);
Query OK, 0 rows affected (0.06 sec)
```

```sql
SHOW TABLE t NEXT_ROW_ID;
+---------+------------+-------------+--------------------+
| DB_NAME | TABLE_NAME | COLUMN_NAME | NEXT_GLOBAL_ROW_ID |
+---------+------------+-------------+--------------------+
| test    | t          | _tidb_rowid |                  1 |
+---------+------------+-------------+--------------------+
1 row in set (0.00 sec)
```

数据已写入表中。插入数据的 TiDB 服务器一次性分配并缓存了 30000 个 ID。因此，NEXT_GLOBAL_ROW_ID 现在是 30001。ID 的数量由 [`AUTO_ID_CACHE`](/auto-increment.md#auto_id_cache) 控制。

```sql
INSERT INTO t VALUES (), (), ();
Query OK, 3 rows affected (0.02 sec)
Records: 3  Duplicates: 0  Warnings: 0
```

```sql
SHOW TABLE t NEXT_ROW_ID;
+---------+------------+-------------+--------------------+
| DB_NAME | TABLE_NAME | COLUMN_NAME | NEXT_GLOBAL_ROW_ID |
+---------+------------+-------------+--------------------+
| test    | t          | _tidb_rowid |              30001 |
+---------+------------+-------------+--------------------+
1 row in set (0.00 sec)
```

## MySQL 兼容性

此语句是 TiDB 对 MySQL 语法的扩展。

## 另请参阅

* [CREATE TABLE](/sql-statements/sql-statement-create-table.md)
* [AUTO_RANDOM](/auto-random.md)
* [CREATE_SEQUENCE](/sql-statements/sql-statement-create-sequence.md)
