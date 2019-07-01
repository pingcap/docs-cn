---
title: CREATE TABLE
summary: TiDB 数据库中 CREATE TABLE 的使用概况
category: reference
---

# CREATE TABLE 

`CREATE TABLE` 语句用于在当前所选数据库中创建新表。另可参阅单独的 `CREATE TABLE LIKE` 文档。

## 语法图

**CreateTableStmt:**

![CreateTableStmt](/media/sqlgram/CreateTableStmt.png)

**IfNotExists:**

![IfNotExists](/media/sqlgram/IfNotExists.png)

**TableName:**

![TableName](/media/sqlgram/TableName.png)

**TableElementListOpt:**

![TableElementListOpt](/media/sqlgram/TableElementListOpt.png)

**TableElement:**

![TableElement](/media/sqlgram/TableElement.png)

**PartitionOpt:**

![PartitionOpt](/media/sqlgram/PartitionOpt.png)

**ColumnDef:**

![ColumnDef](/media/sqlgram/ColumnDef.png)

**ColumnName:**

![ColumnName](/media/sqlgram/ColumnName.png)

**Type:**

![Type](/media/sqlgram/Type.png)

**ColumnOptionListOpt:**

![ColumnOptionListOpt](/media/sqlgram/ColumnOptionListOpt.png)

**TableOptionListOpt:**

![TableOptionListOpt](/media/sqlgram/TableOptionListOpt.png)

## 示例

```sql
mysql> CREATE TABLE t1 (a int);
Query OK, 0 rows affected (0.11 sec)

mysql> CREATE TABLE t2 LIKE t1;
Query OK, 0 rows affected (0.10 sec)

mysql> DESC t1;
+-------+---------+------+------+---------+-------+
| Field | Type    | Null | Key  | Default | Extra |
+-------+---------+------+------+---------+-------+
| a     | int(11) | YES  |      | NULL    |       |
+-------+---------+------+------+---------+-------+
1 row in set (0.00 sec)

mysql> INSERT INTO t1 VALUES (1);
Query OK, 1 row affected (0.02 sec)

mysql> SELECT * FROM t1;
+------+
| a    |
+------+
|    1 |
+------+
1 row in set (0.00 sec)
```

## MySQL 兼容性

* TiDB 不支持 `CREATE TEMPORARY TABLE` 语法。
* 支持除空间类型以外的所有数据类型。
* 不支持 `FULLTEXT`，`HASH` 和 `SPATIAL` 索引。
* `KEY_BLOCK_SIZE` 和 `ENGINE` 属性可被解析，但会被忽略。
* `index_col_name` 属性支持 length 选项，最大长度限制为 3072 字节。此长度限制不会更改，具体取决于存储引擎和建表时使用的字符集。
* `index_col_name` 属性支持 `ASC` 和 `DESC` 的索引排序选项。
* `COMMENT` 属性最多支持 1024 个字符，不支持 `WITH PARSER` 选项。
* TiDB 在单个表中最多支持 512 列。InnoDB 中相应的数量限制为 1017，MySQL 中的硬限制为 4096。

## 另请参阅

* [DROP TABLE](/reference/sql/statements/drop-table.md)
* [CREATE TABLE LIKE](/reference/sql/statements/create-table-like.md)
* [SHOW CREATE TABLE](/reference/sql/statements/show-create-table.md)