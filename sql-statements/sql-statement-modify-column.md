---
title: MODIFY COLUMN | TiDB SQL Statement Reference
summary: An overview of the usage of MODIFY COLUMN for the TiDB database.
aliases: ['/docs/dev/sql-statements/sql-statement-modify-column/','/docs/dev/reference/sql/statements/modify-column/']
---

# MODIFY COLUMN

The `ALTER TABLE.. MODIFY COLUMN` statement modifies a column on an existing table. The modification can include changing the data type and attributes. To rename at the same time, use the [`CHANGE COLUMN`](/sql-statements/sql-statement-change-column.md) statement instead.

## Synopsis

**AlterTableStmt:**

![AlterTableStmt](/media/sqlgram/AlterTableStmt.png)

**AlterTableSpec:**

![AlterTableSpec](/media/sqlgram/AlterTableSpec.png)

**ColumnKeywordOpt:**

![ColumnKeywordOpt](/media/sqlgram/ColumnKeywordOpt.png)

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

mysql> ALTER TABLE t1 MODIFY col1 BIGINT;
Query OK, 0 rows affected (0.09 sec)

mysql> SHOW CREATE TABLE t1\G
*************************** 1. row ***************************
       Table: t1
Create Table: CREATE TABLE `t1` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `col1` bigint(20) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin AUTO_INCREMENT=30001
1 row in set (0.00 sec)
```

## MySQL compatibility

* Does not support modifying multiple columns in a single `ALTER TABLE` statement. For example:

    ```sql
    ALTER TABLE t1 MODIFY col1 BIGINT, MODIFY id BIGINT NOT NULL;
    ERROR 1105 (HY000): Unsupported multi schema change
    ```

* Does not support changes of lossy data types and some other types (including changes from integer to string or to `BLOB`). For example:

    ```sql
    CREATE TABLE t1 (col1 BIGINT);
    ALTER TABLE t1 MODIFY col1 INT;
    ERROR 8200 (HY000): Unsupported modify column length 11 is less than origin 20
    ```

* Does not support modifying the precision of the `DECIMAL` data type. For example:

    ```sql
    CREATE TABLE t (a DECIMAL(5, 3));
    ALTER TABLE t MODIFY COLUMN a DECIMAL(6, 3);
    ERROR 8200 (HY000): Unsupported modify column: can't change decimal column precision
    ```

## See also

* [CREATE TABLE](/sql-statements/sql-statement-create-table.md)
* [SHOW CREATE TABLE](/sql-statements/sql-statement-show-create-table.md)
* [ADD COLUMN](/sql-statements/sql-statement-add-column.md)
* [DROP COLUMN](/sql-statements/sql-statement-drop-column.md)
* [CHANGE COLUMN](/sql-statements/sql-statement-change-column.md)
