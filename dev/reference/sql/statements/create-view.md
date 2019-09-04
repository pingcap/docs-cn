---
title: CREATE VIEW | TiDB SQL Statement Reference
summary: An overview of the usage of CREATE VIEW for the TiDB database.
category: reference
---

# CREATE VIEW

The `CREATE VIEW` statement saves a `SELECT` statement as a queryable object, similar to a table. Views in TiDB are non-materialized. This means that as a view is queried, TiDB will internally rewrite the query to combine the view definition with the SQL query.

## Synopsis

**CreateViewStmt:**

![CreateViewStmt](/media/sqlgram-dev/CreateViewStmt.png)

**OrReplace:**

![OrReplace](/media/sqlgram-dev/OrReplace.png)

**ViewAlgorithm:**

![ViewAlgorithm](/media/sqlgram-dev/ViewAlgorithm.png)

**ViewDefiner:**

![ViewDefiner](/media/sqlgram-dev/ViewDefiner.png)

**ViewSQLSecurity:**

![ViewSQLSecurity](/media/sqlgram-dev/ViewSQLSecurity.png)

**ViewName:**

![ViewName](/media/sqlgram-dev/ViewName.png)

**ViewFieldList:**

![ViewFieldList](/media/sqlgram-dev/ViewFieldList.png)

**ViewCheckOption:**

![ViewCheckOption](/media/sqlgram-dev/ViewCheckOption.png)

## Examples

```sql
mysql> CREATE TABLE t1 (id INT NOT NULL PRIMARY KEY auto_increment, c1 INT NOT NULL);
Query OK, 0 rows affected (0.11 sec)

mysql> INSERT INTO t1 (c1) VALUES (1),(2),(3),(4),(5);
Query OK, 5 rows affected (0.03 sec)
Records: 5  Duplicates: 0  Warnings: 0

mysql> CREATE VIEW v1 AS SELECT * FROM t1 WHERE c1 > 2;
Query OK, 0 rows affected (0.11 sec)

mysql> SELECT * FROM t1;
+----+----+
| id | c1 |
+----+----+
|  1 |  1 |
|  2 |  2 |
|  3 |  3 |
|  4 |  4 |
|  5 |  5 |
+----+----+
5 rows in set (0.00 sec)

mysql> SELECT * FROM v1;
+----+----+
| id | c1 |
+----+----+
|  3 |  3 |
|  4 |  4 |
|  5 |  5 |
+----+----+
3 rows in set (0.00 sec)

mysql> INSERT INTO t1 (c1) VALUES (6);
Query OK, 1 row affected (0.01 sec)

mysql> SELECT * FROM v1;
+----+----+
| id | c1 |
+----+----+
|  3 |  3 |
|  4 |  4 |
|  5 |  5 |
|  6 |  6 |
+----+----+
4 rows in set (0.00 sec)

mysql> INSERT INTO v1 (c1) VALUES (7);
ERROR 1105 (HY000): insert into view v1 is not supported now.
```

## MySQL compatibility

* Views in TiDB are not currently insertable or updatable.

## See also

* [CREATE TABLE](/dev/reference/sql/statements/create-table.md)
* [SHOW CREATE TABLE](/dev/reference/sql/statements/show-create-table.md)
* [DROP TABLE](/dev/reference/sql/statements/drop-table.md)
