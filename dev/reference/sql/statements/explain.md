---
title: EXPLAIN | TiDB SQL Statement Reference 
summary: An overview of the usage of EXPLAIN for the TiDB database.
category: reference
---

# EXPLAIN

The `EXPLAIN` statement shows the execution plan for a query without executing it. It is complimented by `EXPLAIN ANALYZE` which will execute the query. If the output of `EXPLAIN` does not match the expected result, consider executing `ANALYZE TABLE` on each table in the query.

The statements `DESC` and `DESCRIBE` are aliases of this statement. The alternative usage of `EXPLAIN <tableName>` is documented under [`SHOW [FULL] COLUMNS FROM`](/dev/reference/sql/statements/show-columns-from.md).

## Synopsis

**ExplainSym:**

![ExplainSym](/media/sqlgram/ExplainSym.png)

**ExplainStmt:**

![ExplainStmt](/media/sqlgram/ExplainStmt.png)

**ExplainableStmt:**

![ExplainableStmt](/media/sqlgram/ExplainableStmt.png)

## Examples

```sql
mysql> EXPLAIN SELECT 1;
+-------------------+-------+------+---------------+
| id                | count | task | operator info |
+-------------------+-------+------+---------------+
| Projection_3      | 1.00  | root | 1             |
| └─TableDual_4     | 1.00  | root | rows:1        |
+-------------------+-------+------+---------------+
2 rows in set (0.00 sec)

mysql> CREATE TABLE t1 (id INT NOT NULL PRIMARY KEY auto_increment, c1 INT NOT NULL);
Query OK, 0 rows affected (0.10 sec)

mysql> INSERT INTO t1 (c1) VALUES (1), (2), (3);
Query OK, 3 rows affected (0.02 sec)
Records: 3  Duplicates: 0  Warnings: 0

mysql> EXPLAIN SELECT * FROM t1 WHERE id = 1;
+-------------+-------+------+--------------------+
| id          | count | task | operator info      |
+-------------+-------+------+--------------------+
| Point_Get_1 | 1.00  | root | table:t1, handle:1 |
+-------------+-------+------+--------------------+
1 row in set (0.00 sec)

mysql> DESC SELECT * FROM t1 WHERE id = 1;
+-------------+-------+------+--------------------+
| id          | count | task | operator info      |
+-------------+-------+------+--------------------+
| Point_Get_1 | 1.00  | root | table:t1, handle:1 |
+-------------+-------+------+--------------------+
1 row in set (0.00 sec)

mysql> DESCRIBE SELECT * FROM t1 WHERE id = 1;
+-------------+-------+------+--------------------+
| id          | count | task | operator info      |
+-------------+-------+------+--------------------+
| Point_Get_1 | 1.00  | root | table:t1, handle:1 |
+-------------+-------+------+--------------------+
1 row in set (0.00 sec)

mysql> EXPLAIN INSERT INTO t1 (c1) VALUES (4);
ERROR 1105 (HY000): Unsupported type *core.Insert

mysql> EXPLAIN UPDATE t1 SET c1=5 WHERE c1=3;
+---------------------+----------+------+-------------------------------------------------------------+
| id                  | count    | task | operator info                                               |
+---------------------+----------+------+-------------------------------------------------------------+
| TableReader_6       | 10.00    | root | data:Selection_5                                            |
| └─Selection_5       | 10.00    | cop  | eq(test.t1.c1, 3)                                           |
|   └─TableScan_4     | 10000.00 | cop  | table:t1, range:[-inf,+inf], keep order:false, stats:pseudo |
+---------------------+----------+------+-------------------------------------------------------------+
3 rows in set (0.00 sec)

mysql> EXPLAIN DELETE FROM t1 WHERE c1=3;
+---------------------+----------+------+-------------------------------------------------------------+
| id                  | count    | task | operator info                                               |
+---------------------+----------+------+-------------------------------------------------------------+
| TableReader_6       | 10.00    | root | data:Selection_5                                            |
| └─Selection_5       | 10.00    | cop  | eq(test.t1.c1, 3)                                           |
|   └─TableScan_4     | 10000.00 | cop  | table:t1, range:[-inf,+inf], keep order:false, stats:pseudo |
+---------------------+----------+------+-------------------------------------------------------------+
3 rows in set (0.00 sec)
```

## MySQL compatibility

* Both the format of `EXPLAIN` and the potential execution plans in TiDB differ substaintially from MySQL.
* TiDB does not support the `EXPLAIN FORMAT=JSON` as in MySQL.
* TiDB does not currently support `EXPLAIN` for insert statements.

## See also

* [Understanding the Query Execution Plan](/sql/understanding-the-query-execution-plan.md)
* [EXPLAIN ANALYZE](/dev/reference/sql/statements/explain-analyze.md)
* [ANALYZE TABLE](/dev/reference/sql/statements/analyze-table.md)
