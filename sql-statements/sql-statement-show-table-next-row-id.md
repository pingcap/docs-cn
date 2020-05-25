---
title: SHOW TABLE NEXT_ROW_ID
summary: TiDB 数据库中 SHOW TABLE NEXT_ROW_ID 的使用概况。
category: reference
---

# SHOW TABLE NEXT_ROW_ID

`SHOW TABLE NEXT_ROW_ID` 语句用于显示用表中某些特殊列的详情，主要包含以下几种类型：

* TiDB 创建的 `AUTO_INCREMENT` 类型列，即 `_tidb_rowid` 列
* 用户创建的 `AUTO_INCREMENT` 类型列
* 用户创建的 [`AUTO_RANDOM`](/auto-random.md) 类型列
* 用户创建的 [`SEQUENCE`](/sql-statements/sql-statement-create-sequence.md) 对象信息

## 语法图

**ShowStmt:**

![ShowStmt](/media/sqlgram/ShowStmt.png)

## 示例

+ 创建一张表

{{< copyable "sql" >}}

```sql
CREATE TABLE t1 (a INT);
```

```
Query OK, 0 rows affected (0.12 sec)
```

+ 执行SHOW 语句

{{< copyable "sql" >}}

```sql
SHOW TABLE T1 NEXT_ROW_ID;
```

```
+---------+------------+-------------+--------------------+----------------+
| DB_NAME | TABLE_NAME | COLUMN_NAME | NEXT_GLOBAL_ROW_ID | ID_TYPE        |
+---------+------------+-------------+--------------------+----------------+
| test    | T1         | _tidb_rowid |                  1 | AUTO_INCREMENT |
+---------+------------+-------------+--------------------+----------------+
1 row in set (0.01 sec)
```

## 另请参阅

* [CREATE TABLE](/sql-statements/sql-statement-create-table.md)
* [AUTO_RANDOM](/auto-random.md)
* [CREATE_SEQUENCE](/sql-statements/sql-statement-create-sequence.md)
