---
title: ANALYZE TABLE | TiDB SQL Statement Reference 
summary: An overview of the usage of ANALYZE TABLE for the TiDB database.
category: reference
---

# ANALYZE TABLE 

This statement updates the statistics that TiDB builds on tables and indexes. It is recommended to run `ANALYZE TABLE` after performing a large batch update or import of records, or when you notice that query execution plans are sub-optimal.

TiDB will also automatically update its statistics over time as it discovers that they are inconsistent with its own estimates.

## Synopsis

**AnalyzeTableStmt:**

![AnalyzeTableStmt](/media/sqlgram/AnalyzeTableStmt.png)

**TableNameList:**

![TableNameList](/media/sqlgram/TableNameList.png)

**TableName:**

![TableName](/media/sqlgram/TableName.png)

## Examples

```sql
mysql> CREATE TABLE t1 (id INT NOT NULL PRIMARY KEY auto_increment, c1 INT NOT NULL);
Query OK, 0 rows affected (0.11 sec)

mysql> INSERT INTO t1 (c1) VALUES (1),(2),(3),(4),(5);
Query OK, 5 rows affected (0.03 sec)
Records: 5  Duplicates: 0  Warnings: 0

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

mysql> analyze table t1;
Query OK, 0 rows affected (0.13 sec)

mysql> EXPLAIN SELECT * FROM t1 WHERE c1 = 3;
+-------------------+-------+------+---------------------------------------------------+
| id                | count | task | operator info                                     |
+-------------------+-------+------+---------------------------------------------------+
| IndexReader_6     | 1.00  | root | index:IndexScan_5                                 |
| └─IndexScan_5     | 1.00  | cop  | table:t1, index:c1, range:[3,3], keep order:false |
+-------------------+-------+------+---------------------------------------------------+
2 rows in set (0.00 sec)
```

## MySQL compatibility

This statement is syntactically similar with MySQL. However, `ANALYZE TABLE` may take significantly longer to execute on TiDB, as internally it operates in a different manner.

## See also

* [EXPLAIN](/dev/reference/sql/statements/explain.md)
* [EXPLAIN ANALYZE](/dev/reference/sql/statements/explain-analyze.md)
