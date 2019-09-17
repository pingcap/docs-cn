---
title: CREATE INDEX | TiDB SQL Statement Reference
summary: An overview of the usage of CREATE INDEX for the TiDB database.
category: reference
---

# CREATE INDEX

This statement adds a new index to an existing table. It is an alternative syntax to `ALTER TABLE .. ADD INDEX`, and included for MySQL compatibility.

## Synopsis

**CreateIndexStmt:**

![CreateIndexStmt](/media/sqlgram-v2.1/CreateIndexStmt.png)

**CreateIndexStmtUnique:**

![CreateIndexStmtUnique](/media/sqlgram-v2.1/CreateIndexStmtUnique.png)

**Identifier:**

![Identifier](/media/sqlgram-v2.1/Identifier.png)

**IndexTypeOpt:**

![IndexTypeOpt](/media/sqlgram-v2.1/IndexTypeOpt.png)

**TableName:**

![TableName](/media/sqlgram-v2.1/TableName.png)

**IndexColNameList:**

![IndexColNameList](/media/sqlgram-v2.1/IndexColNameList.png)

**IndexOptionList:**

![IndexOptionList](/media/sqlgram-v2.1/IndexOptionList.png)

**IndexOption:**

![IndexOption](/media/sqlgram-v2.1/IndexOption.png)

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

mysql> CREATE UNIQUE INDEX c1 ON t1 (c1);
Query OK, 0 rows affected (0.31 sec)
```

## Associated session variables

The global variables associated with the `CREATE INDEX` statement are `tidb_ddl_reorg_worker_cnt`, `tidb_ddl_reorg_batch_size` and `tidb_ddl_reorg_priority`. Refer to [TiDB-specific system variables](/v2.1/reference/configuration/tidb-server/tidb-specific-variables.md#tidb_ddl_reorg_worker_cnt) for details.

## MySQL compatibility

* `FULLTEXT`, `HASH` and `SPATIAL` indexes are not supported.
* Descending indexes are not supported (similar to MySQL 5.7).
* It is not possible to add a `PRIMARY KEY` to a table.

## See also

* [ADD INDEX](/v2.1/reference/sql/statements/add-index.md)
* [DROP INDEX](/v2.1/reference/sql/statements/drop-index.md)
* [RENAME INDEX](/v2.1/reference/sql/statements/rename-index.md)
* [ADD COLUMN](/v2.1/reference/sql/statements/add-column.md)
* [CREATE TABLE](/v2.1/reference/sql/statements/create-table.md)
* [EXPLAIN](/v2.1/reference/sql/statements/explain.md)
