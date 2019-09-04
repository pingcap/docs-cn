---
title: ADD INDEX | TiDB SQL Statement Reference
summary: An overview of the usage of ADD INDEX for the TiDB database.
category: reference
---

# ADD INDEX

The `ALTER TABLE.. ADD INDEX` statement adds an index to an existing table. This operation is online in TiDB, which means that neither reads or writes to the table are blocked by adding an index.

## Synopsis

**AlterTableStmt:**

![AlterTableStmt](/media/sqlgram-dev/AlterTableStmt.png)

**AlterTableSpec:**

![AlterTableSpec](/media/sqlgram-dev/AlterTableSpec.png)

**ColumnKeywordOpt:**

![ColumnKeywordOpt](/media/sqlgram-dev/ColumnKeywordOpt.png)

**ColumnDef:**

![ColumnDef](/media/sqlgram-dev/ColumnDef.png)

**ColumnPosition:**

![ColumnPosition](/media/sqlgram-dev/ColumnPosition.png)

## Examples

```sql
mysql> CREATE TABLE t1 (id INT NOT NULL PRIMARY KEY auto_increment, c1 INT NOT NULL);
Query OK, 0 rows affected (0.11 sec)

mysql> INSERT INTO t1 (c1) VALUES (1),(2),(3),(4),(5);
Query OK, 5 rows affected (0.03 sec)
Records: 5  Duplicates: 0  Warnings: 0

mysql> EXPLAIN SELECT * FROM t1 WHERE c1 = 3;
+---------------------+----------+------+-------------------------------------------------------------+
| id                  | count    | task | operator info                                               |
+---------------------+----------+------+-------------------------------------------------------------+
| TableReader_7       | 10.00    | root | data:Selection_6                                            |
| └─Selection_6       | 10.00    | cop  | eq(test.t1.c1, 3)                                           |
|   └─TableScan_5     | 10000.00 | cop  | table:t1, range:[-inf,+inf], keep order:false, stats:pseudo |
+---------------------+----------+------+-------------------------------------------------------------+
3 rows in set (0.00 sec)

mysql> ALTER TABLE t1 ADD INDEX (c1);
Query OK, 0 rows affected (0.30 sec)

mysql> EXPLAIN SELECT * FROM t1 WHERE c1 = 3;
+-------------------+-------+------+-----------------------------------------------------------------+
| id                | count | task | operator info                                                   |
+-------------------+-------+------+-----------------------------------------------------------------+
| IndexReader_6     | 10.00 | root | index:IndexScan_5                                               |
| └─IndexScan_5     | 10.00 | cop  | table:t1, index:c1, range:[3,3], keep order:false, stats:pseudo |
+-------------------+-------+------+-----------------------------------------------------------------+
2 rows in set (0.00 sec)
```

## MySQL compatibility

* `FULLTEXT`, `HASH` and `SPATIAL` indexes are not supported.
* Descending indexes are not supported (similar to MySQL 5.7).
* Adding multiple indexes at the same time is currently not supported.
* It is not possible to add a `PRIMARY KEY` to a table.

## See also

* [CREATE INDEX](/dev/reference/sql/statements/create-index.md)
* [DROP INDEX](/dev/reference/sql/statements/drop-index.md)
* [RENAME INDEX](/dev/reference/sql/statements/rename-index.md)
* [ADD COLUMN](/dev/reference/sql/statements/add-column.md)
* [CREATE TABLE](/dev/reference/sql/statements/create-table.md)
* [EXPLAIN](/dev/reference/sql/statements/explain.md)
