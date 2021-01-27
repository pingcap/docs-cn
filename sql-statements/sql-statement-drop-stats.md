---
title: DROP STATS
summary: TiDB 数据库中 DROP STATS 的使用概况。
aliases: ['/docs-cn/dev/sql-statements/sql-statement-drop-stats/']
---

# DROP STATS

`DROP STATS` 语句用于从当前所选定的数据库中删除选定表的统计信息。

## 语法图

```ebnf+diagram
DropStatsStmt ::=
    'DROP' 'STATS' TableName

TableName ::=
    Identifier ('.' Identifier)?
```

## 示例

{{< copyable "sql" >}}

```sql
CREATE TABLE t(a INT);
```

```sql
Query OK, 0 rows affected (0.01 sec)
```

{{< copyable "sql" >}}

```sql
SHOW STATS_META WHERE db_name='test' and table_name='t';
```

```sql
+---------+------------+----------------+---------------------+--------------+-----------+
| Db_name | Table_name | Partition_name | Update_time         | Modify_count | Row_count |
+---------+------------+----------------+---------------------+--------------+-----------+
| test    | t          |                | 2020-05-25 20:34:33 |            0 |         0 |
+---------+------------+----------------+---------------------+--------------+-----------+
1 row in set (0.00 sec)
```

{{< copyable "sql" >}}

```sql
DROP STATS t;
```

```sql
Query OK, 0 rows affected (0.00 sec)
```

{{< copyable "sql" >}}

```sql
SHOW STATS_META WHERE db_name='test' and table_name='t';
```

```sql
Empty set (0.00 sec)
```

## MySQL 兼容性

该语句是 TiDB 对 MySQL 语法的扩展。

## 另请参阅

* [统计信息简介](/statistics.md)
