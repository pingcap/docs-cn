---
title: ALTER INDEX
summary: An overview of the usage of ALTER INDEX for the TiDB database.
aliases: ['/docs/dev/sql-statements/sql-statement-alter-index/']
---

# ALTER INDEX

The `ALTER INDEX` statement is used to modify the visibility of the index to `Visible` or `Invisible`. Invisible indexes are maintained by DML statements, but will not be used by the query optimizer. This is useful in scenarios where you want to double-check before removing an index permanently.

## Synopsis

```ebnf+diagram
AlterTableStmt
         ::= 'ALTER' 'IGNORE'? 'TABLE' TableName AlterIndexSpec ( ',' AlterIndexSpec )*

AlterIndexSpec
         ::= 'ALTER' 'INDEX' Identifier ( 'VISIBLE' | 'INVISIBLE' )
```

## Examples

You can modify the visibility of an index using the `ALTER TABLE ... ALTER INDEX ...` statement.

{{< copyable "sql" >}}

```sql
CREATE TABLE t1 (c1 INT, UNIQUE(c1));
ALTER TABLE t1 ALTER INDEX c1 INVISIBLE;
```

```sql
Query OK, 0 rows affected (0.02 sec)
```

{{< copyable "sql" >}}

```sql
SHOW CREATE TABLE t1;
```

```sql
+-------+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| Table | Create Table
                                    |
+-------+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| t1    | CREATE TABLE `t1` (
  `c1` int(11) DEFAULT NULL,
  UNIQUE KEY `c1` (`c1`) /*!80000 INVISIBLE */
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin |
+-------+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
1 row in set (0.00 sec)
```

The optimizer cannot use the **invisible index** of `c1`.

{{< copyable "sql" >}}

```sql
EXPLAIN SELECT c1 FROM t1 ORDER BY c1;
```

```sql
+-------------------------+----------+-----------+---------------+--------------------------------+
| id                      | estRows  | task      | access object | operator info                  |
+-------------------------+----------+-----------+---------------+--------------------------------+
| Sort_4                  | 10000.00 | root      |               | test.t1.c1:asc                 |
| └─TableReader_8         | 10000.00 | root      |               | data:TableFullScan_7           |
|   └─TableFullScan_7     | 10000.00 | cop[tikv] | table:t1      | keep order:false, stats:pseudo |
+-------------------------+----------+-----------+---------------+--------------------------------+
3 rows in set (0.00 sec)
```

By comparison, `c2` is a **visible index** and can be used by the optimizer.

{{< copyable "sql" >}}

```sql
EXPLAIN SELECT c2 FROM t1 ORDER BY c2;
```

```sql
+------------------------+----------+-----------+------------------------+-------------------------------+
| id                     | estRows  | task      | access object          | operator info                 |
+------------------------+----------+-----------+------------------------+-------------------------------+
| IndexReader_13         | 10000.00 | root      |                        | index:IndexFullScan_12        |
| └─IndexFullScan_12     | 10000.00 | cop[tikv] | table:t1, index:c2(c2) | keep order:true, stats:pseudo |
+------------------------+----------+-----------+------------------------+-------------------------------+
2 rows in set (0.00 sec)
```

Even if you use the `USE INDEX` SQL hint to forcibly use indexes, the optimizer still cannot use invisible indexes; otherwise, an error is returned.

{{< copyable "sql" >}}

```sql
SELECT * FROM t1 USE INDEX(c1);
```

```sql
ERROR 1176 (42000): Key 'c1' doesn't exist in table 't1'
```

> **Note:**
>
> "Invisible" here means invisible only to the optimizer. You can still modify or delete invisible indexes.

{{< copyable "sql" >}}

```sql
ALTER TABLE t1 DROP INDEX c1;
```

```sql
Query OK, 0 rows affected (0.02 sec)
```

## MySQL compatibility

* Invisible indexes in TiDB are modeled on the equivalent feature from MySQL 8.0.
* Similiar to MySQL, TiDB does not permit `PRIMARY KEY` indexes to be made invisible.
* MySQL provides an optimizer switch `use_invisible_indexes=on` to make all invisible indexes _visible_ again. This functionality is not available in TiDB.

## See also

* [CREATE TABLE](/sql-statements/sql-statement-create-table.md)
* [CREATE INDEX](/sql-statements/sql-statement-create-index.md)
* [ADD INDEX](/sql-statements/sql-statement-add-index.md)
* [DROP INDEX](/sql-statements/sql-statement-drop-index.md)
* [RENAME INDEX](/sql-statements/sql-statement-rename-index.md)
