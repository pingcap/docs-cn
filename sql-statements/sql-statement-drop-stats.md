---
title: DROP STATS
summary: TiDB 数据库中 DROP STATS 的使用概况。
---

# DROP STATS

`DROP STATS` 语句用于从当前所选定的数据库中删除选定表的统计信息。

## 语法图

```ebnf+diagram
DropStatsStmt ::=
    'DROP' 'STATS' TableName  ("PARTITION" partition | "GLOBAL")? ( ',' TableName )*

TableName ::=
    Identifier ('.' Identifier)?
```

## 使用

以下语句用于删除 `TableName` 的所有统计信息。如果指定了分区表，则此语句还会删除该表中所有分区的统计信息以及[动态裁剪模式下的分区表统计信息](/statistics.md#收集动态裁剪模式下的分区表统计信息)。

```sql
DROP STATS TableName
```

```
Query OK, 0 rows affected (0.00 sec)
```

以下语句只删除 `PartitionNameList` 中指定分区的统计信息：

```sql
DROP STATS TableName PARTITION PartitionNameList;
```

```
Query OK, 0 rows affected (0.00 sec)
```

以下语句只删除指定表在动态裁剪模式下生成的全局统计信息：

```sql
DROP STATS TableName GLOBAL;
```

```
Query OK, 0 rows affected (0.00 sec)
```

## 示例

```sql
CREATE TABLE t(a INT);
```

```
Query OK, 0 rows affected (0.01 sec)
```

```sql
SHOW STATS_META WHERE db_name='test' and table_name='t';
```

```
+---------+------------+----------------+---------------------+--------------+-----------+
| Db_name | Table_name | Partition_name | Update_time         | Modify_count | Row_count |
+---------+------------+----------------+---------------------+--------------+-----------+
| test    | t          |                | 2020-05-25 20:34:33 |            0 |         0 |
+---------+------------+----------------+---------------------+--------------+-----------+
1 row in set (0.00 sec)
```

```sql
DROP STATS t;
```

```
Query OK, 0 rows affected (0.00 sec)
```

```sql
SHOW STATS_META WHERE db_name='test' and table_name='t';
```

```
Empty set (0.00 sec)
```

## MySQL 兼容性

该语句是 TiDB 对 MySQL 语法的扩展。

## 另请参阅

* [常规统计信息](/statistics.md)
