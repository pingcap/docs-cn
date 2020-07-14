---
title: ALTER INDEX
summary: An overview of the usage of ALTER INDEX for the TiDB database.
aliases: ['/docs/dev/sql-statements/sql-statement-alter-index/']
---

# ALTER INDEX

The `ALTER INDEX` statement is used to modify the visibility of the index to `Visible` or `Invisible`. When the visibility of an index is set to `Invisible`, this index cannot be used by the optimizer.

## Synopsis

**AlterTableStmt:**

![AlterTableStmt](/media/sqlgram/AlterTableStmt.png)

**AlterTableSpec:**

![AlterTableSpec](/media/sqlgram/AlterTableSpec.png)

**IndexInvisible:**

![IndexInvisible](/media/sqlgram/IndexInvisible.png)

## Syntax

{{< copyable "sql" >}}

```sql
ALTER TABLE [table_name] ALTER INDEX [index_name] {VISIBLE | INVISIBLE}
```

## Example

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

## Invisible index

Invisible indexes are a new feature introduced in MySQL 8.0 that sets an index to invisible so that the optimizer no longer uses this index. Using this feature, you can easily check whether to use or not to use the query plan of an index, and avoid resource-consuming operations such as `DROP INDEX` or `ADD INDEX`.

{{< copyable "sql" >}}

```sql
CREATE TABLE t1 (c1 INT, c2 INT, UNIQUE(c2));
CREATE UNIQUE INDEX c1 ON t1 (c1) INVISIBLE;
```

You can check an invisible index using the `CREATE TABLE` statement. The invisible index is identified with `/*!80000 INVISIBLE */`:

{{< copyable "sql" >}}

```sql
SHOW CREATE TABLE t1;
```

```sql
+-------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| Table | Create Table
                                                              |
+-------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| t1    | CREATE TABLE `t1` (
  `c1` int(11) DEFAULT NULL,
  `c2` int(11) DEFAULT NULL,
  UNIQUE KEY `c2` (`c2`),
  UNIQUE KEY `c1` (`c1`) /*!80000 INVISIBLE */
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin |
+-------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
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

### Restriction

There is a restriction on invisible indexes in MySQL: the **primary key** cannot be set to `Invisible`. TiDB is compatible with this restriction. If you set the primary key to `Invisible` in TiDB, an error is returned.

{{< copyable "sql" >}}

```sql
CREATE TABLE t2(c1 INT, PRIMARY KEY(c1) INVISIBLE);
```

```sql
ERROR 3522 (HY000): A primary key index cannot be invisible
```

The **primary key** above includes both the explicit primary key (specified using the `PRIMARY KEY` keyword) and the implicit primary key.

If the explicit primary key does not exist in the table, the first `UNIQUE` index (every column of the index must be `NOT NULL`) automatically becomes the implicit index.

This means that you cannot set this implicit primary key to `Invisible`.

> **Note:**
>
> TiDB does not actually create an **implicit primary key**. TiDB is compatible with this MySQL restriction only in behaviors.

{{< copyable "sql" >}}

```sql
CREATE TABLE t2(c1 INT NOT NULL, UNIQUE(c1) INVISIBLE);
```

```
ERROR 3522 (HY000): A primary key index cannot be invisible
```

## See also

* [CREATE TABLE](/sql-statements/sql-statement-create-table.md)
* [CREATE INDEX](/sql-statements/sql-statement-create-index.md)
* [ADD INDEX](/sql-statements/sql-statement-add-index.md)
* [DROP INDEX](/sql-statements/sql-statement-drop-index.md)
* [RENAME INDEX](/sql-statements/sql-statement-rename-index.md)
