---
title: CHANGE COLUMN | TiDB SQL Statement Reference
summary: An overview of the usage of CHANGE COLUMN for the TiDB database.
category: reference
---

# CHANGE COLUMN

The `ALTER TABLE.. CHANGE COLUMN` statement changes a column on an existing table. The change can include both renaming the column, and changing the data type to a compatible type.

## Synopsis

**AlterTableStmt:**

![AlterTableStmt](/media/sqlgram-dev/AlterTableStmt.png)

**AlterTableSpec:**

![AlterTableSpec](/media/sqlgram-dev/AlterTableSpec.png)

**ColumnKeywordOpt:**

![ColumnKeywordOpt](/media/sqlgram-dev/ColumnKeywordOpt.png)

**ColumnName:**

![ColumnName](/media/sqlgram-dev/ColumnName.png)

**ColumnDef:**

![ColumnDef](/media/sqlgram-dev/ColumnDef.png)

**ColumnPosition:**

![ColumnPosition](/media/sqlgram-dev/ColumnPosition.png)

## Examples

```sql
mysql> CREATE TABLE t1 (id int not null primary key auto_increment, col1 INT);
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

## See also

* [CREATE TABLE](/dev/reference/sql/statements/create-table.md)
* [SHOW CREATE TABLE](/dev/reference/sql/statements/show-create-table.md)
* [ADD COLUMN](/dev/reference/sql/statements/add-column.md)
* [DROP COLUMN](/dev/reference/sql/statements/drop-column.md)
* [MODIFY COLUMN](/dev/reference/sql/statements/modify-column.md)
