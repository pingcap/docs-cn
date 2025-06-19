---
title: TIDB_INDEXES
summary: 了解 `TIDB_INDEXES` information_schema 表。
---

# TIDB_INDEXES

`TIDB_INDEXES` 表提供了所有表的索引信息。

{{< copyable "sql" >}}

```sql
USE information_schema;
DESC tidb_indexes;
```

```
+---------------+---------------+------+------+---------+-------+
| Field         | Type          | Null | Key  | Default | Extra |
+---------------+---------------+------+------+---------+-------+
| TABLE_SCHEMA  | varchar(64)   | YES  |      | NULL    |       |
| TABLE_NAME    | varchar(64)   | YES  |      | NULL    |       |
| NON_UNIQUE    | bigint(21)    | YES  |      | NULL    |       |
| KEY_NAME      | varchar(64)   | YES  |      | NULL    |       |
| SEQ_IN_INDEX  | bigint(21)    | YES  |      | NULL    |       |
| COLUMN_NAME   | varchar(64)   | YES  |      | NULL    |       |
| SUB_PART      | bigint(21)    | YES  |      | NULL    |       |
| INDEX_COMMENT | varchar(2048) | YES  |      | NULL    |       |
| Expression    | varchar(64)   | YES  |      | NULL    |       |
| INDEX_ID      | bigint(21)    | YES  |      | NULL    |       |
| IS_VISIBLE    | varchar(64)   | YES  |      | NULL    |       |
| CLUSTERED     | varchar(64)   | YES  |      | NULL    |       |
+---------------+---------------+------+------+---------+-------+
12 rows in set (0.00 sec)
```

`INDEX_ID` 是 TiDB 为每个索引分配的唯一 ID。它可以用于与从其他表或 API 获取的 `INDEX_ID` 进行联接操作。

例如，你可以在 [`SLOW_QUERY` 表](/information-schema/information-schema-slow-query.md)中获取某些慢查询涉及的 `TABLE_ID` 和 `INDEX_ID`，然后使用以下 SQL 语句获取具体的索引信息：

```sql
SELECT
 tidb_indexes.*
FROM
 tidb_indexes,
 tables
WHERE
  tidb_indexes.table_schema = tables.table_schema
 AND tidb_indexes.table_name = tidb_indexes.table_name
 AND tables.tidb_table_id = ?
 AND index_id = ?
```

`TIDB_INDEXES` 表中各字段的描述如下：

* `TABLE_SCHEMA`：索引所属的数据库（schema）名称。
* `TABLE_NAME`：索引所属的表名。
* `NON_UNIQUE`：如果索引是唯一的，则值为 `0`；否则值为 `1`。
* `KEY_NAME`：索引名称。如果该索引是主键，则名称为 `PRIMARY`。
* `SEQ_IN_INDEX`：索引中列的顺序号，从 `1` 开始。
* `COLUMN_NAME`：索引所在列的名称。
* `SUB_PART`：索引的前缀长度。如果列是部分索引，则 `SUB_PART` 值是已索引字符的数量；否则值为 `NULL`。
* `INDEX_COMMENT`：创建索引时的索引注释。
* `INDEX_ID`：索引 ID。
* `IS_VISIBLE`：索引是否可见。
* `CLUSTERED`：是否为[聚簇索引](/clustered-indexes.md)。
