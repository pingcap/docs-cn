---
title: CHANGE COLUMN | TiDB SQL Statement Reference
summary: An overview of the usage of CHANGE COLUMN for the TiDB database.
aliases: ['/docs/dev/sql-statements/sql-statement-change-column/','/docs/dev/reference/sql/statements/change-column/']
---

# CHANGE COLUMN

The `ALTER TABLE.. CHANGE COLUMN` statement changes a column on an existing table. The change can include both renaming the column, and changing the data type to a compatible type.

## Synopsis

**AlterTableStmt:**

![AlterTableStmt](/media/sqlgram/AlterTableStmt.png)

**AlterTableSpec:**

![AlterTableSpec](/media/sqlgram/AlterTableSpec.png)

**ColumnName:**

![ColumnName](/media/sqlgram/ColumnName.png)

**ColumnDef:**

![ColumnDef](/media/sqlgram/ColumnDef.png)

**ColumnPosition:**

![ColumnPosition](/media/sqlgram/ColumnPosition.png)

## Examples

```sql
mysql> CREATE TABLE t1 (id int not null primary key AUTO_INCREMENT, col1 INT);
Query OK, 0 rows affected (0.11 sec)

mysql> INSERT INTO t1 (col1) VALUES (1),(2),(3),(4),(5);
Query OK, 5 rows affected (0.02 sec)
Records: 5  Duplicates: 0  Warnings: 0

mysql>
mysql> ALTER TABLE t1 CHANGE col1 col2 INT;
Query OK, 0 rows affected (0.09 sec)

mysql> ALTER TABLE t1 CHANGE col2 col3 BIGINT, ALGORITHM=INSTANT;
Query OK, 0 rows affected (0.08 sec)

mysql>
mysql> ALTER TABLE t1 CHANGE col3 col3 INT;
ERROR 1105 (HY000): unsupported modify column length 11 is less than origin 20
mysql> ALTER TABLE t1 CHANGE col3 col3 BLOB;
ERROR 1105 (HY000): unsupported modify column type 252 not match origin 8
mysql> ALTER TABLE t1 CHANGE col3 col4 BIGINT, CHANGE id id2 INT NOT NULL;
ERROR 1105 (HY000): can't run multi schema change
```

## MySQL compatibility

* Making multiple changes in a single `ALTER TABLE` statement is not currently supported.
* Only certain types of data type changes are supported. For example, an `INTEGER` to `BIGINT` is supported, but the reverse is not possible. Changing from an integer to a string format or blob is not supported.
* Modifying precision of the `DECIMAL` type is not supported.
* Changing the `UNSIGNED` attribute is not supported.

## See also

* [CREATE TABLE](/sql-statements/sql-statement-create-table.md)
* [SHOW CREATE TABLE](/sql-statements/sql-statement-show-create-table.md)
* [ADD COLUMN](/sql-statements/sql-statement-add-column.md)
* [DROP COLUMN](/sql-statements/sql-statement-drop-column.md)
* [MODIFY COLUMN](/sql-statements/sql-statement-modify-column.md)
