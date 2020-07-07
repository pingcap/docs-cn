---
title: ALTER TABLE
summary: TiDB 数据库中 ALTER TABLE 的使用概况。
category: reference
aliases: ['/docs-cn/dev/reference/sql/statements/alter-table/']
---

# ALTER TABLE

`ALTER TABLE` 语句用于对已有表进行修改，以符合新表结构。`ALTER TABLE` 语句可用于：

* [`ADD`](/sql-statements/sql-statement-add-index.md)，[`DROP`](/sql-statements/sql-statement-drop-index.md)，或 [`RENAME`](/sql-statements/sql-statement-rename-index.md) 索引
* [`ADD`](/sql-statements/sql-statement-add-column.md)，[`DROP`](/sql-statements/sql-statement-drop-column.md)，[`MODIFY`](/sql-statements/sql-statement-modify-column.md) 或 [`CHANGE`](/sql-statements/sql-statement-change-column.md) 列

## 语法图

**AlterTableStmt:**

![AlterTableStmt](/media/sqlgram/AlterTableStmt.png)

**TableName:**

![TableName](/media/sqlgram/TableName.png)

**AlterTableSpec:**

![AlterTableSpec](/media/sqlgram/AlterTableSpec.png)

## 示例

{{< copyable "sql" >}}

```sql
CREATE TABLE t1 (id INT NOT NULL PRIMARY KEY AUTO_INCREMENT, c1 INT NOT NULL);
```

```
Query OK, 0 rows affected (0.11 sec)
```

{{< copyable "sql" >}}

```sql
INSERT INTO t1 (c1) VALUES (1),(2),(3),(4),(5);
```

```
Query OK, 5 rows affected (0.03 sec)
Records: 5  Duplicates: 0  Warnings: 0
```

{{< copyable "sql" >}}

```sql
EXPLAIN SELECT * FROM t1 WHERE c1 = 3;
```

```
+-------------------------+----------+-----------+---------------+--------------------------------+
| id                      | estRows  | task      | access object | operator info                  |
+-------------------------+----------+-----------+---------------+--------------------------------+
| TableReader_7           | 10.00    | root      |               | data:Selection_6               |
| └─Selection_6           | 10.00    | cop[tikv] |               | eq(test.t1.c1, 3)              |
|   └─TableFullScan_5     | 10000.00 | cop[tikv] | table:t1      | keep order:false, stats:pseudo |
+-------------------------+----------+-----------+---------------+--------------------------------+
3 rows in set (0.00 sec)
```

{{< copyable "sql" >}}

```sql
ALTER TABLE t1 ADD INDEX (c1);
```

```
Query OK, 0 rows affected (0.30 sec)
```

{{< copyable "sql" >}}

```sql
EXPLAIN SELECT * FROM t1 WHERE c1 = 3;
```

```
+------------------------+---------+-----------+------------------------+---------------------------------------------+
| id                     | estRows | task      | access object          | operator info                               |
+------------------------+---------+-----------+------------------------+---------------------------------------------+
| IndexReader_6          | 10.00   | root      |                        | index:IndexRangeScan_5                      |
| └─IndexRangeScan_5     | 10.00   | cop[tikv] | table:t1, index:c1(c1) | range:[3,3], keep order:false, stats:pseudo |
+------------------------+---------+-----------+------------------------+---------------------------------------------+
2 rows in set (0.00 sec)
```

## MySQL 兼容性

* 支持除空间类型外的所有数据类型。其它不支持的情况可参考：[DDL 语句与 MySQL 的兼容性情况](/mysql-compatibility.md#ddl-的限制)。

## 另请参阅

* [ADD COLUMN](/sql-statements/sql-statement-add-column.md)
* [DROP COLUMN](/sql-statements/sql-statement-drop-column.md)
* [ADD INDEX](/sql-statements/sql-statement-add-index.md)
* [DROP INDEX](/sql-statements/sql-statement-drop-index.md)
* [RENAME INDEX](/sql-statements/sql-statement-rename-index.md)
* [ALTER INDEX](/sql-statements/sql-statement-alter-index.md)
* [CREATE TABLE](/sql-statements/sql-statement-create-table.md)
* [DROP TABLE](/sql-statements/sql-statement-drop-table.md)
* [SHOW CREATE TABLE](/sql-statements/sql-statement-show-create-table.md)
