---
title: ADD INDEX | TiDB SQL Statement Reference
summary: An overview of the usage of ADD INDEX for the TiDB database.
aliases: ['/docs/dev/sql-statements/sql-statement-add-index/','/docs/dev/reference/sql/statements/add-index/']
---

# ADD INDEX

The `ALTER TABLE.. ADD INDEX` statement adds an index to an existing table. This operation is online in TiDB, which means that neither reads or writes to the table are blocked by adding an index.

## Synopsis

**AlterTableStmt:**

![AlterTableStmt](/media/sqlgram/AlterTableStmt.png)

**AlterTableSpec:**

![AlterTableSpec](/media/sqlgram/AlterTableSpec.png)

**Constraint:**

![Constraint](/media/sqlgram/Constraint.png)

**ConstraintKeywordOpt:**

![ConstraintKeywordOpt](/media/sqlgram/ConstraintKeywordOpt.png)

**ConstraintElem:**

![ConstraintElem](/media/sqlgram/ConstraintElem.png)

**IndexNameAndTypeOpt:**

![IndexNameAndTypeOpt](/media/sqlgram/IndexNameAndTypeOpt.png)

**IndexPartSpecificationList:**

![IndexPartSpecificationList](/media/sqlgram/IndexPartSpecificationList.png)

**IndexPartSpecification:**

![IndexPartSpecification](/media/sqlgram/IndexPartSpecification.png)

**IndexOptionList:**

![IndexOptionList](/media/sqlgram/IndexOptionList.png)

**IndexOption:**

![IndexOption](/media/sqlgram/IndexOption.png)

**KeyOrIndex:**

![KeyOrIndex](/media/sqlgram/KeyOrIndex.png)

**IndexKeyTypeOpt:**

![IndexKeyTypeOpt](/media/sqlgram/IndexKeyTypeOpt.png)

**IndexInvisible:**

![IndexInvisible](/media/sqlgram/IndexInvisible.png)

**IndexTypeName:**

![IndexTypeName](/media/sqlgram/IndexTypeName.png)

## Examples

```sql
mysql> CREATE TABLE t1 (id INT NOT NULL PRIMARY KEY AUTO_INCREMENT, c1 INT NOT NULL);
Query OK, 0 rows affected (0.11 sec)

mysql> INSERT INTO t1 (c1) VALUES (1),(2),(3),(4),(5);
Query OK, 5 rows affected (0.03 sec)
Records: 5  Duplicates: 0  Warnings: 0

mysql> EXPLAIN SELECT * FROM t1 WHERE c1 = 3;
+-------------------------+----------+-----------+---------------+--------------------------------+
| id                      | estRows  | task      | access object | operator info                  |
+-------------------------+----------+-----------+---------------+--------------------------------+
| TableReader_7           | 10.00    | root      |               | data:Selection_6               |
| └─Selection_6           | 10.00    | cop[tikv] |               | eq(test.t1.c1, 3)              |
|   └─TableFullScan_5     | 10000.00 | cop[tikv] | table:t1      | keep order:false, stats:pseudo |
+-------------------------+----------+-----------+---------------+--------------------------------+
3 rows in set (0.00 sec)

mysql> ALTER TABLE t1 ADD INDEX (c1);
Query OK, 0 rows affected (0.30 sec)

mysql> EXPLAIN SELECT * FROM t1 WHERE c1 = 3;
+------------------------+---------+-----------+------------------------+---------------------------------------------+
| id                     | estRows | task      | access object          | operator info                               |
+------------------------+---------+-----------+------------------------+---------------------------------------------+
| IndexReader_6          | 0.01    | root      |                        | index:IndexRangeScan_5                      |
| └─IndexRangeScan_5     | 0.01    | cop[tikv] | table:t1, index:c1(c1) | range:[3,3], keep order:false, stats:pseudo |
+------------------------+---------+-----------+------------------------+---------------------------------------------+
2 rows in set (0.00 sec)
```

## MySQL compatibility

* `FULLTEXT`, `HASH` and `SPATIAL` indexes are not supported.
* `VISIBLE/INVISIBLE` index is not supported (currently only the master branch actually supports this feature).
* Descending indexes are not supported (similar to MySQL 5.7).
* Adding multiple indexes at the same time is currently not supported.
* Adding the primary key constraint to a table is not supported by default. You can enable the feature by setting the `alter-primary-key` configuration item to `true`. For details, see [alter-primary-key](/tidb-configuration-file.md#alter-primary-key).

## See also

* [Index Selection](/choose-index.md)
* [Wrong Index Solution](/wrong-index-solution.md)
* [CREATE INDEX](/sql-statements/sql-statement-create-index.md)
* [DROP INDEX](/sql-statements/sql-statement-drop-index.md)
* [RENAME INDEX](/sql-statements/sql-statement-rename-index.md)
* [ALTER INDEX](/sql-statements/sql-statement-alter-index.md)
* [ADD COLUMN](/sql-statements/sql-statement-add-column.md)
* [CREATE TABLE](/sql-statements/sql-statement-create-table.md)
* [EXPLAIN](/sql-statements/sql-statement-explain.md)
