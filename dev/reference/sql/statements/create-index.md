---
title: CREATE INDEX
summary: CREATE INDEX 在 TiDB 中的使用概况
category: reference
---

# CREATE INDEX

`CREATE INDEX` 语句用于在已有表中添加新索引，功能等同于 `ALTER TABLE .. ADD INDEX`。包含该语句提供了 MySQL 兼容性。

## 语法图

**CreateIndexStmt:**

![CreateIndexStmt](/media/sqlgram/CreateIndexStmt.png)

**CreateIndexStmtUnique:**

![CreateIndexStmtUnique](/media/sqlgram/CreateIndexStmtUnique.png)

**Identifier:**

![Identifier](/media/sqlgram/Identifier.png)

**IndexTypeOpt:**

![IndexTypeOpt](/media/sqlgram/IndexTypeOpt.png)

**TableName:**

![TableName](/media/sqlgram/TableName.png)

**IndexColNameList:**

![IndexColNameList](/media/sqlgram/IndexColNameList.png)

**IndexOptionList:**

![IndexOptionList](/media/sqlgram/IndexOptionList.png)

**IndexOption:**

![IndexOption](/media/sqlgram/IndexOption.png)

## 示例

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

## 相关 session 变量

和 `CREATE INDEX` 语句相关的全局变量有 `tidb_ddl_reorg_worker_cnt`，`tidb_ddl_reorg_batch_size` 和 `tidb_ddl_reorg_priority`，具体可以参考 [TiDB 特定系统变量](/dev/reference/configuration/tidb-server/tidb-specific-variables.md#tidb_ddl_reorg_worker_cnt)。

## MySQL 兼容性

* 不支持 `FULLTEXT`，`HASH` 和 `SPATIAL` 索引。
* 不支持降序索引 （类似于 MySQL 5.7）。
* 无法向表中添加 `PRIMARY KEY`。

## 另请参阅

* [ADD INDEX](/dev/reference/sql/statements/add-index.md)
* [DROP INDEX](/dev/reference/sql/statements/drop-index.md)
* [RENAME INDEX](/dev/reference/sql/statements/rename-index.md)
* [ADD COLUMN](/dev/reference/sql/statements/add-column.md)
* [CREATE TABLE](/dev/reference/sql/statements/create-table.md)
* [EXPLAIN](/dev/reference/sql/statements/explain.md)
