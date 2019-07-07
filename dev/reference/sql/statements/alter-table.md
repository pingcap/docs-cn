---
title: ALTER TABLE
summary: TiDB 数据库中 ALTER TABLE 的使用概况。
category: reference
---

# ALTER TABLE

`ALTER TABLE` 语句用于对已有表进行修改，以符合新表结构。`ALTER TABLE` 语句可用于：

* [`ADD`](/reference/sql/statements/add-index.md)，[`DROP`](/reference/sql/statements/drop-index.md)，或 [`RENAME`](/reference/sql/statements/rename-index.md) 索引
* [`ADD`](/reference/sql/statements/add-column.md)，[`DROP`](/reference/sql/statements/drop-column.md)，[`MODIFY`](/reference/sql/statements/modify-column.md) 或 [`CHANGE`](/reference/sql/statements/change-column.md) 列

## 语法图

**AlterTableStmt:**

![AlterTableStmt](/media/sqlgram/AlterTableStmt.png)

**TableName:**

![TableName](/media/sqlgram/TableName.png)

**AlterTableSpec:**

![AlterTableSpec](/media/sqlgram/AlterTableSpec.png)

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

* 支持除空间类型外的所有数据类型。
* 不支持 `FULLTEXT`，`HASH` 和 `SPATIAL` 索引。

## 另请参阅

* [ADD COLUMN](/reference/sql/statements/add-column.md)
* [DROP COLUMN](/reference/sql/statements/drop-column.md)
* [RENAME COLUMN](/reference/sql/statements/rename-column.md)
* [ADD INDEX](/reference/sql/statements/add-index.md)
* [DROP INDEX](/reference/sql/statements/drop-index.md)
* [RENAME INDEX](/reference/sql/statements/rename-index.md)
* [CREATE TABLE](/reference/sql/statements/create-table.md)
* [DROP TABLE](/reference/sql/statements/drop-table.md)
* [SHOW CREATE TABLE](/reference/sql/statements/show-create-table.md)
