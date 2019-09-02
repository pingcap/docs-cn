---
title: ADD INDEX
summary: TiDB 数据库中 ADD INDEX 的使用概况。
category: reference
---

# ADD INDEX

`ALTER TABLE.. ADD INDEX` 语句用于在已有表中添加一个索引。在 TiDB 中，`ADD INDEX` 为在线操作，不会阻塞表中的数据读写。

## 语法图

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

## 示例

```sql
mysql> CREATE TABLE t1 (id INT NOT NULL PRIMARY KEY auto_increment, c1 INT NOT NULL);
Query OK, 0 rows affected (0.11 sec)

mysql> INSERT INTO t1 (c1) VALUES (1),(2),(3),(4),(5);
Query OK, 5 rows affected (0.03 sec)
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
```

## MySQL 兼容性

* 不支持 `FULLTEXT`，`HASH` 和 `SPATIAL` 索引。
* 不支持降序索引（类似于 MySQL 5.7）。
* 目前尚不支持同时添加多个索引。
* 无法向表中添加 `PRIMARY KEY`。

## 另请参阅

* [CREATE INDEX](/v3.0/reference/sql/statements/create-index.md)
* [DROP INDEX](/v3.0/reference/sql/statements/drop-index.md)
* [RENAME INDEX](/v3.0/reference/sql/statements/rename-index.md)
* [ADD COLUMN](/v3.0/reference/sql/statements/add-column.md)
* [CREATE TABLE](/v3.0/reference/sql/statements/create-table.md)
* [EXPLAIN](/v3.0/reference/sql/statements/explain.md)