---
title: DROP STATS
summary: An overview of the usage of DROP STATS for the TiDB database.
aliases: ['/docs/dev/sql-statements/sql-statement-drop-stats/']
---

# DROP STATS

The `DROP STATS` statement is used to delete the statistics of the selected table from the selected database.

## Synopsis

```ebnf+diagram
DropStatsStmt ::=
    'DROP' 'STATS' TableName

TableName ::=
    Identifier ('.' Identifier)?
```

## Examples

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

## MySQL compatibility

This statement is a TiDB extension to MySQL syntax.

## See also

* [Introduction to Statistics](/statistics.md)
