---
title: DROP INDEX | TiDB SQL Statement Reference
summary: An overview of the usage of DROP INDEX for the TiDB database.
category: reference
---

# DROP INDEX

This statement removes an index from a specified table, marking space as free in TiKV.

## Synopsis

**AlterTableStmt:**

![AlterTableStmt](/media/sqlgram-v3.0/AlterTableStmt.png)

**AlterTableSpec:**

![AlterTableSpec](/media/sqlgram-v3.0/AlterTableSpec.png)

**KeyOrIndex:**

![KeyOrIndex](/media/sqlgram-v3.0/KeyOrIndex.png)

**Identifier:**

![Identifier](/media/sqlgram-v3.0/Identifier.png)

## Examples

```sql
mysql> CREATE TABLE t1 (id INT NOT NULL PRIMARY KEY auto_increment, c1 INT NOT NULL);
Query OK, 0 rows affected (0.10 sec)

mysql> INSERT INTO t1 (c1) VALUES (1),(2),(3),(4),(5);
Query OK, 5 rows affected (0.02 sec)
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

mysql> CREATE INDEX c1 ON t1 (c1);
Query OK, 0 rows affected (0.30 sec)

mysql> EXPLAIN SELECT * FROM t1 WHERE c1 = 3;
+-------------------+-------+------+-----------------------------------------------------------------+
| id                | count | task | operator info                                                   |
+-------------------+-------+------+-----------------------------------------------------------------+
| IndexReader_6     | 10.00 | root | index:IndexScan_5                                               |
| └─IndexScan_5     | 10.00 | cop  | table:t1, index:c1, range:[3,3], keep order:false, stats:pseudo |
+-------------------+-------+------+-----------------------------------------------------------------+
2 rows in set (0.00 sec)

mysql> ALTER TABLE t1 DROP INDEX c1;
Query OK, 0 rows affected (0.30 sec)
```

## MySQL compatibility

* Dropping the `PRIMARY KEY` is not supported.

## See also

* [SHOW INDEX](/v3.0/reference/sql/statements/show-index.md)
* [CREATE INDEX](/v3.0/reference/sql/statements/create-index.md)
* [ADD INDEX](/v3.0/reference/sql/statements/add-index.md)
* [RENAME INDEX](/v3.0/reference/sql/statements/rename-index.md)
