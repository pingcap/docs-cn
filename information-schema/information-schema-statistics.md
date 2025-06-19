---
title: STATISTICS
summary: 了解 `STATISTICS` information_schema 表。
---

# STATISTICS

`STATISTICS` 表提供了关于表索引的信息。

{{< copyable "sql" >}}

```sql
USE information_schema;
DESC statistics;
```

```sql
+---------------+---------------+------+------+---------+-------+
| Field         | Type          | Null | Key  | Default | Extra |
+---------------+---------------+------+------+---------+-------+
| TABLE_CATALOG | varchar(512)  | YES  |      | NULL    |       |
| TABLE_SCHEMA  | varchar(64)   | YES  |      | NULL    |       |
| TABLE_NAME    | varchar(64)   | YES  |      | NULL    |       |
| NON_UNIQUE    | varchar(1)    | YES  |      | NULL    |       |
| INDEX_SCHEMA  | varchar(64)   | YES  |      | NULL    |       |
| INDEX_NAME    | varchar(64)   | YES  |      | NULL    |       |
| SEQ_IN_INDEX  | bigint(2)     | YES  |      | NULL    |       |
| COLUMN_NAME   | varchar(21)   | YES  |      | NULL    |       |
| COLLATION     | varchar(1)    | YES  |      | NULL    |       |
| CARDINALITY   | bigint(21)    | YES  |      | NULL    |       |
| SUB_PART      | bigint(3)     | YES  |      | NULL    |       |
| PACKED        | varchar(10)   | YES  |      | NULL    |       |
| NULLABLE      | varchar(3)    | YES  |      | NULL    |       |
| INDEX_TYPE    | varchar(16)   | YES  |      | NULL    |       |
| COMMENT       | varchar(16)   | YES  |      | NULL    |       |
| INDEX_COMMENT | varchar(1024) | YES  |      | NULL    |       |
| IS_VISIBLE    | varchar(3)    | YES  |      | NULL    |       |
| Expression    | varchar(64)   | YES  |      | NULL    |       |
+---------------+---------------+------+------+---------+-------+
18 rows in set (0.00 sec)
```

`STATISTICS` 表中各字段的描述如下：

* `TABLE_CATALOG`：包含索引的表所属的目录名称。该值始终为 `def`。
* `TABLE_SCHEMA`：包含索引的表所属的数据库名称。
* `TABLE_NAME`：包含索引的表名。
* `NON_UNIQUE`：如果索引不能包含重复值，则值为 `0`；如果索引允许重复值，则值为 `1`。
* `INDEX_SCHEMA`：索引所属的数据库名称。
* `INDEX_NAME`：索引的名称。如果该索引是主键，则值始终为 `PRIMARY`。
* `SEQ_IN_INDEX`：索引中的列序号，从 `1` 开始。
* `COLUMN_NAME`：列名。请参见 `Expression` 列的描述。
* `COLLATION`：索引中列的排序方式。值可以是 `A`（升序），`D`（降序）或 `NULL`（未排序）。
* `CARDINALITY`：TiDB 不使用此字段。字段值始终为 `0`。
* `SUB_PART`：索引的前缀。如果只对列的部分前缀进行索引，则值为已索引的字符数；如果对整列进行索引，则值为 `NULL`。
* `PACKED`：TiDB 不使用此字段。该值始终为 `NULL`。
* `NULLABLE`：如果列可能包含 `NULL` 值，则值为 `YES`；如果不可能，则值为 `''`。
* `INDEX_TYPE`：索引的类型。
* `COMMENT`：与索引相关的其他信息。
* `INDEX_COMMENT`：创建索引时为索引提供的任何带有注释属性的注释。
* `IS_VISIBLE`：优化器是否可以使用此索引。
* `Expression`：对于非表达式部分的索引键，该值为 `NULL`；对于表达式部分的索引键，该值为表达式本身。参考[表达式索引](/sql-statements/sql-statement-create-index.md#expression-index)。

以下语句是等价的：

```sql
SELECT * FROM INFORMATION_SCHEMA.STATISTICS
  WHERE table_name = 'tbl_name'
  AND table_schema = 'db_name'

SHOW INDEX
  FROM tbl_name
  FROM db_name
```
