---
title: CHANGE COLUMN
summary: TiDB 数据库中 CHANGE COLUMN 的使用概况。
category: reference
---

# CHANGE COLUMN

`ALTER TABLE.. CHANGE COLUMN` 语句用于在已有表上更改列，包括对列进行重命名，和将数据改为兼容类型。

## 语法图

**AlterTableStmt:**

![AlterTableStmt](/media/sqlgram/AlterTableStmt.png)

**AlterTableSpec:**

![AlterTableSpec](/media/sqlgram/AlterTableSpec.png)

**ColumnKeywordOpt:**

![ColumnKeywordOpt](/media/sqlgram/ColumnKeywordOpt.png)

**ColumnName:**

![ColumnName](/media/sqlgram/ColumnName.png)

**ColumnDef:**

![ColumnDef](/media/sqlgram/ColumnDef.png)

**ColumnPosition:**

![ColumnPosition](/media/sqlgram/ColumnPosition.png)

## 示例

```sql
mysql> CREATE TABLE t1 (id int not null primary key auto_increment, col1 INT);
Query OK, 0 rows affected (0.11 sec)

mysql> INSERT INTO t1 (col1) VALUES (1),(2),(3),(4),(5);
Query OK, 5 rows affected (0.02 sec)
Records: 5  Duplicates: 0  Warnings: 0

mysql>
mysql> ALTER TABLE t1 CHANGE col1 col2 INT;
Query OK, 0 rows affected (0.09 sec)

mysql> ALTER TABLE t1 CHANGE col2 col3 BIGINT, ALGORITHM=INSTANT;
Query OK, 0 rows affected (0.08 sec)

mysql>
mysql> ALTER TABLE t1 CHANGE col3 col3 INT;
ERROR 1105 (HY000): unsupported modify column length 11 is less than origin 20
mysql> ALTER TABLE t1 CHANGE col3 col3 BLOB;
ERROR 1105 (HY000): unsupported modify column type 252 not match origin 8
mysql> ALTER TABLE t1 CHANGE col3 col4 BIGINT, CHANGE id id2 INT NOT NULL;
ERROR 1105 (HY000): can't run multi schema change
```

## MySQL 兼容性

* 目前尚不支持在单个 `ALTER TABLE` 语句中进行多个更改。
* 仅支持特定的数据类型更改。例如，支持将 `INTEGER` 更改为 `BIGINT`，但不支持将 `BIGINT` 更改为 `INTEGER`。不支持从整数更改为字符串格式或 BLOB 类型。

## 另请参阅

* [CREATE TABLE](/v2.1/reference/sql/statements/create-table.md)
* [SHOW CREATE TABLE](/v2.1/reference/sql/statements/show-create-table.md)
* [ADD COLUMN](/v2.1/reference/sql/statements/add-column.md)
* [DROP COLUMN](/v2.1/reference/sql/statements/drop-column.md)
* [MODIFY COLUMN](/v2.1/reference/sql/statements/modify-column.md)
