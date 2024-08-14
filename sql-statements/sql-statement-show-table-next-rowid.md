---
title: SHOW TABLE NEXT_ROW_ID
summary: TiDB 数据库中 SHOW TABLE NEXT_ROW_ID 的使用概况。
aliases: ['/docs-cn/dev/sql-statements/sql-statement-show-table-next-rowid/']
---

# SHOW TABLE NEXT_ROW_ID

`SHOW TABLE NEXT_ROW_ID` 语句用于显示用户表中某些特殊列的详情，主要包含以下几种类型：

* TiDB 创建的 [`AUTO_INCREMENT`](/auto-increment.md) 类型列，即 `_tidb_rowid` 列
* 用户创建的 `AUTO_INCREMENT` 类型列
* 用户创建的 [`AUTO_RANDOM`](/auto-random.md) 类型列
* 用户创建的 [`SEQUENCE`](/sql-statements/sql-statement-create-sequence.md) 对象信息

## 语法图

```ebnf+diagram
ShowTableNextRowIDStmt ::=
    "SHOW" "TABLE" (SchemaName ".")? TableName "NEXT_ROW_ID"
```

## 示例

下面示例中，对于新建的表，由于没有任何的 Row ID 分配，NEXT_GLOBAL_ROW_ID 值为 `1`。

{{< copyable "sql" >}}

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

下面示例中，表中写入了数据，负责写入的 TiDB Server 一次性向存储层请求了 30000 个 ID 缓存起来，NEXT_GLOBAL_ROW_ID 值为 `30001`。ID 的数量由 [`AUTO_ID_CACHE`](/auto-increment.md#auto_id_cache) 控制。

{{< copyable "sql" >}}

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

该语句是 TiDB 对 MySQL 语法的扩展。

## 另请参阅

* [CREATE TABLE](/sql-statements/sql-statement-create-table.md)
* [AUTO_RANDOM](/auto-random.md)
* [CREATE_SEQUENCE](/sql-statements/sql-statement-create-sequence.md)
