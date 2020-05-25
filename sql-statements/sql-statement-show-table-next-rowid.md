---
title: SHOW TABLE NEXT_ROW_ID
summary: TiDB 数据库中 SHOW TABLE NEXT_ROW_ID 的使用概况。
category: reference
aliases: ['/docs-cn/dev/reference/sql/statements/show-status/']
---

# SHOW TABLE NEXT_ROW_ID

`SHOW TABLE NEXT_ROW_ID` 语句用于查看 TiDB 中一张表的隐式分配的全局 Row ID 情况：

- 对于大多数表，TiDB 会为每一条记录分配一个表内唯一的数字作为 ID，ID 最大分配值被持久化在存储层，每个 TiDB Server 会按需向持久层申请一段空间缓存在内存中，用于 ID 的分配。该语法用于查询存储层的所记录的下一个分配值。
- 对于主键被定义为整数类型的表，由于 TiDB 进行了优化，将整数主键映射为了 Row ID，因此对于该类型的表，`SHOW TABLE NEXT_ROW_ID` 的值没有意义。

## 语法图

**ShowTableNextRowIDStmt:**

![ShowTableNextRowIDStmt](/media/sqlgram/ShowTableNextRowIDStmt.png)

**TableName:**

![TableName](/media/sqlgram/TableName.png)

## 示例

{{< copyable "sql" >}}

```sql
create table t(a int);
Query OK, 0 rows affected (0.06 sec)
```

```sql
# 对于新建的表，由于没有任何的 Row ID 分配，NEXT_GLOBAL_ROW_ID 值为 1
show table t next_row_id;
+---------+------------+-------------+--------------------+
| DB_NAME | TABLE_NAME | COLUMN_NAME | NEXT_GLOBAL_ROW_ID |
+---------+------------+-------------+--------------------+
| test    | t          | _tidb_rowid |                  1 |
+---------+------------+-------------+--------------------+
1 row in set (0.00 sec)
```

```sql
insert into t values (), (), ();
Query OK, 3 rows affected (0.02 sec)
Records: 3  Duplicates: 0  Warnings: 0
```

```sql
show table t next_row_id;
# 表中写入了数据，负责写入的 TiDB Server 一次性向存储层请求了 30000 个 ID 缓存起来，NEXT_GLOBAL_ROW_ID 值为 30001
+---------+------------+-------------+--------------------+
| DB_NAME | TABLE_NAME | COLUMN_NAME | NEXT_GLOBAL_ROW_ID |
+---------+------------+-------------+--------------------+
| test    | t          | _tidb_rowid |              30001 |
+---------+------------+-------------+--------------------+
1 row in set (0.00 sec)
```

## MySQL 兼容性

`SHOW TABLE NEXT_ROW_ID` 语句是 TiDB 特有的语法。