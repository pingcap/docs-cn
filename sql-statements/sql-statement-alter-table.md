---
title: ALTER TABLE | TiDB SQL Statement Reference
summary: An overview of the usage of ALTER TABLE for the TiDB database.
aliases: ['/docs/dev/sql-statements/sql-statement-alter-table/','/docs/dev/reference/sql/statements/alter-table/']
---

# ALTER TABLE

This statement modifies an existing table to conform to a new table structure. The statement `ALTER TABLE` can be used to:

* [`ADD`](/sql-statements/sql-statement-add-index.md), [`DROP`](/sql-statements/sql-statement-drop-index.md), or [`RENAME`](/sql-statements/sql-statement-rename-index.md) indexes
* [`ADD`](/sql-statements/sql-statement-add-column.md), [`DROP`](/sql-statements/sql-statement-drop-column.md), [`MODIFY`](/sql-statements/sql-statement-modify-column.md) or [`CHANGE`](/sql-statements/sql-statement-change-column.md) columns

## Synopsis

**AlterTableStmt:**

![AlterTableStmt](/media/sqlgram/AlterTableStmt.png)

**TableName:**

![TableName](/media/sqlgram/TableName.png)

**AlterTableSpec:**

![AlterTableSpec](/media/sqlgram/AlterTableSpec.png)

## Examples

Create a table with some initial data:

{{< copyable "sql" >}}

```sql
CREATE TABLE t1 (id INT NOT NULL PRIMARY KEY AUTO_INCREMENT, c1 INT NOT NULL);
INSERT INTO t1 (c1) VALUES (1),(2),(3),(4),(5);
```

```sql
Query OK, 0 rows affected (0.11 sec)

Query OK, 5 rows affected (0.03 sec)
Records: 5  Duplicates: 0  Warnings: 0
```

The following query requires a full table scan because the column c1 is not indexed:

{{< copyable "sql" >}}

```sql
EXPLAIN SELECT * FROM t1 WHERE c1 = 3;
```

```sql
+-------------------------+----------+-----------+---------------+--------------------------------+
| id                      | estRows  | task      | access object | operator info                  |
+-------------------------+----------+-----------+---------------+--------------------------------+
| TableReader_7           | 10.00    | root      |               | data:Selection_6               |
| └─Selection_6           | 10.00    | cop[tikv] |               | eq(test.t1.c1, 3)              |
|   └─TableFullScan_5     | 10000.00 | cop[tikv] | table:t1      | keep order:false, stats:pseudo |
+-------------------------+----------+-----------+---------------+--------------------------------+
3 rows in set (0.00 sec)
```

The statement [`ALTER TABLE .. ADD INDEX`](/sql-statements/sql-statement-add-index.md) can be used to add an index on the table t1. `EXPLAIN` confirms that the original query now uses an index range scan, which is more efficient:

{{< copyable "sql" >}}

```sql
ALTER TABLE t1 ADD INDEX (c1);
EXPLAIN SELECT * FROM t1 WHERE c1 = 3;
```

```sql
Query OK, 0 rows affected (0.30 sec)

+------------------------+---------+-----------+------------------------+---------------------------------------------+
| id                     | estRows | task      | access object          | operator info                               |
+------------------------+---------+-----------+------------------------+---------------------------------------------+
| IndexReader_6          | 10.00   | root      |                        | index:IndexRangeScan_5                      |
| └─IndexRangeScan_5     | 10.00   | cop[tikv] | table:t1, index:c1(c1) | range:[3,3], keep order:false, stats:pseudo |
+------------------------+---------+-----------+------------------------+---------------------------------------------+
2 rows in set (0.00 sec)
```

TiDB supports the ability to assert that DDL changes will use a particular `ALTER` algorithm. This is only an assertion, and does not change the actual algorithm which will be used to modify the table. It can be useful if you only want to permit instant DDL changes during the peak hours of your cluster:

{{< copyable "sql" >}}

```sql
ALTER TABLE t1 DROP INDEX c1, ALGORITHM=INSTANT;
```

```sql
Query OK, 0 rows affected (0.24 sec)
```

Using the `ALGORITHM=INSTANT` assertion on an operation that requires the `INPLACE` algorithm results in a statement error:

{{< copyable "sql" >}}

```sql
ALTER TABLE t1 ADD INDEX (c1), ALGORITHM=INSTANT;
```

```sql
ERROR 1846 (0A000): ALGORITHM=INSTANT is not supported. Reason: Cannot alter table by INSTANT. Try ALGORITHM=INPLACE.
```

However, using the `ALGORITHM=COPY` assertion for an `INPLACE` operation generates a warning instead of an error. This is because TiDB interprets the assertion as _this algorithm or better_. This behavior difference is useful for MySQL compatibility because the algorithm TiDB uses might differ from MySQL:

{{< copyable "sql" >}}

```sql
ALTER TABLE t1 ADD INDEX (c1), ALGORITHM=COPY;
SHOW WARNINGS;
```

```sql
Query OK, 0 rows affected, 1 warning (0.25 sec)

+-------+------+---------------------------------------------------------------------------------------------+
| Level | Code | Message                                                                                     |
+-------+------+---------------------------------------------------------------------------------------------+
| Error | 1846 | ALGORITHM=COPY is not supported. Reason: Cannot alter table by COPY. Try ALGORITHM=INPLACE. |
+-------+------+---------------------------------------------------------------------------------------------+
1 row in set (0.00 sec)
```

## MySQL compatibility

The following major restrictions apply to `ALTER TABLE` in TiDB:

* Multiple operations cannot be completed in a single `ALTER TABLE` statement.

* Lossy changes such as changing from `BIGINT` to `INT` are currently not supported.

* Spatial data types are not supported.

For further restrictions, see [MySQL Compatibility](/mysql-compatibility.md#ddl).

## See also

* [MySQL Compatibility](/mysql-compatibility.md#ddl)
* [ADD COLUMN](/sql-statements/sql-statement-add-column.md)
* [DROP COLUMN](/sql-statements/sql-statement-drop-column.md)
* [ADD INDEX](/sql-statements/sql-statement-add-index.md)
* [DROP INDEX](/sql-statements/sql-statement-drop-index.md)
* [RENAME INDEX](/sql-statements/sql-statement-rename-index.md)
* [ALTER INDEX](/sql-statements/sql-statement-alter-index.md)
* [CREATE TABLE](/sql-statements/sql-statement-create-table.md)
* [DROP TABLE](/sql-statements/sql-statement-drop-table.md)
* [SHOW CREATE TABLE](/sql-statements/sql-statement-show-create-table.md)
