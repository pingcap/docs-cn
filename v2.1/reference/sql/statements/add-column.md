---
title: ADD COLUMN | TiDB SQL Statement Reference
summary: An overview of the usage of ADD COLUMN for the TiDB database.
category: reference
---

# ADD COLUMN

The `ALTER TABLE.. ADD COLUMN` statement adds a column to an existing table. This operation is online in TiDB, which means that neither reads or writes to the table are blocked by adding a column.

## Synopsis

**AlterTableStmt:**

![AlterTableStmt](/media/sqlgram-v2.1/AlterTableStmt.png)

**AlterTableSpec:**

![AlterTableSpec](/media/sqlgram-v2.1/AlterTableSpec.png)

**ColumnKeywordOpt:**

![ColumnKeywordOpt](/media/sqlgram-v2.1/ColumnKeywordOpt.png)

**ColumnDef:**

![ColumnDef](/media/sqlgram-v2.1/ColumnDef.png)

**ColumnPosition:**

![ColumnPosition](/media/sqlgram-v2.1/ColumnPosition.png)

## Examples

```sql
mysql> CREATE TABLE t1 (id INT NOT NULL PRIMARY KEY auto_increment);
Query OK, 0 rows affected (0.11 sec)

mysql> INSERT INTO t1 VALUES (NULL);
Query OK, 1 row affected (0.02 sec)

mysql> SELECT * FROM t1;
+----+
| id |
+----+
|  1 |
+----+
1 row in set (0.00 sec)

mysql> ALTER TABLE t1 ADD COLUMN c1 INT NOT NULL;
Query OK, 0 rows affected (0.28 sec)

mysql> SELECT * FROM t1;
+----+----+
| id | c1 |
+----+----+
|  1 |  0 |
+----+----+
1 row in set (0.00 sec)

mysql> ALTER TABLE t1 ADD c2 INT NOT NULL AFTER c1;
Query OK, 0 rows affected (0.28 sec)

mysql> SELECT * FROM t1;
+----+----+----+
| id | c1 | c2 |
+----+----+----+
|  1 |  0 |  0 |
+----+----+----+
1 row in set (0.00 sec)
```

## MySQL compatibility

* Adding multiple columns at the same time is currently not supported.
* Adding a new column and setting it to the `PRIMARY KEY` is not supported.
* Adding a new column and setting it to `AUTO_INCREMENT` is not supported.

## See also

* [ADD INDEX](/reference/sql/statements/add-index.md)
* [CREATE TABLE](/reference/sql/statements/create-table.md)
