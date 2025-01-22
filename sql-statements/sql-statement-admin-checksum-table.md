---
title: ADMIN CHECKSUM TABLE
summary: TiDB 数据库中 ADMIN CHECKSUM TABLE 的使用概况。
---

# ADMIN CHECKSUM TABLE

`ADMIN CHECKSUM TABLE` 语句用于计算表中所有数据和索引的 CRC64 校验和。

[校验和](/tidb-lightning/tidb-lightning-glossary.md#checksum)是通过表数据和 `table_id` 等属性进行计算得出的。这意味着两张 `table_id` 不同的表即使数据相同，校验和也不相同。

当使用 [TiDB Lightning](/tidb-lightning/tidb-lightning-overview.md) 物理模式、[TiDB Data Migration](/dm/dm-overview.md) 或 [`IMPORT INTO`](/sql-statements/sql-statement-import-into.md) 导入完成一张表后，`ADMIN CHECKSUM TABLE <table>` 语句会默认执行以验证数据完整性。

## 语法图

```ebnf+diagram
AdminChecksumTableStmt ::=
    'ADMIN' 'CHECKSUM' 'TABLE' TableNameList

TableNameList ::=
    TableName ( ',' TableName )*
```

## 示例

创建表 `t1`：

```sql
CREATE TABLE t1(id INT PRIMARY KEY);
```

插入一些数据：

```sql
INSERT INTO t1 VALUES (1),(2),(3);
```

计算表 `t1` 的校验和：

```sql
ADMIN CHECKSUM TABLE t1;
```

输出结果示例如下：

```
+---------+------------+----------------------+-----------+-------------+
| Db_name | Table_name | Checksum_crc64_xor   | Total_kvs | Total_bytes |
+---------+------------+----------------------+-----------+-------------+
| test    | t1         | 10909174369497628533 |         3 |          75 |
+---------+------------+----------------------+-----------+-------------+
1 row in set (0.00 sec)
```

## MySQL 兼容性

`ADMIN CHECKSUM TABLE` 语句是 TiDB 对 MySQL 语法的扩展。
