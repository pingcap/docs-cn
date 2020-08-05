---
title: STATISTICS
summary: 了解 information_schema 表 `STATISTICS`。
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

`STATISTICS` 表中列的含义如下：

* `TABLE_CATALOG`：包含索引的表所属的目录的名称。这个值总是 `def`。
* `TABLE_SCHEMA`：包含索引的表所属的数据库的名称。
* `TABLE_NAME`：包含索引的表的名称。
* `NON_UNIQUE`：如果索引不能包含重复项，则为 `0`；如果可以，则为 `1`。
* `INDEX_SCHEMA`：索引所属的数据库的名称。
* `INDEX_NAME`：索引的名称。如果索引是主键，那么名称总是 `PRIMARY`。
* `SEQ_IN_INDEX`：索引中的列序号，从 `1` 开始。
* `COLUMN_NAME`：列名。请参见表达式列的说明。
* `COLLATION`：列在索引中的排序方式。取值可以是 `A`（升序）、`D`（降序）或 `NULL`（未排序）。
* `CARDINALITY`：索引中唯一值的数量的估计。要更新这个数字，执行 `ANALYZE TABLE`。
* `SUB_PART`：索引的前缀。如果只对列的部分前缀进行索引，则为索引字符的数量；如果对整个列进行索引，则为 `NULL`。
* `PACKED`：TiDB 未使用该字段。这个值总是 `NULL`。
* `NULLABLE`：如果列可能包含 `NULL` 值，则值为 `YES`；如果不包含，则值为 `''`。
* `INDEX_TYPE`：索引的类型。
* `COMMENT`：其他与索引有关的信息。
* `INDEX_COMMENT`：在创建索引时为索引提供的带有注释属性的任何注释。
* `IS_VISIBLE`：优化器能否使用该索引。
* `Expression` 对于非表达式部分的索引键，这个值为 `NULL`；对于表达式部分的索引键，这个值为表达式本身。可参考[表达式索引](/sql-statements/sql-statement-create-index.md#表达式索引)

下列语句是等价的：

```sql
SELECT * FROM INFORMATION_SCHEMA.STATISTICS
  WHERE table_name = 'tbl_name'
  AND table_schema = 'db_name'

SHOW INDEX
  FROM tbl_name
  FROM db_name
```
