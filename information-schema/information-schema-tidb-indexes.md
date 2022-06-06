---
title: TIDB_INDEXES
summary: 了解 information_schema 表 `TIDB_INDEXES`。
---

# TIDB_INDEXES

`TIDB_INDEXES` 记录了所有表中的 INDEX 信息。

{{< copyable "sql" >}}

```sql
USE information_schema;
DESC tidb_indexes;
```

```sql
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
+---------------+---------------+------+------+---------+-------+
10 rows in set (0.00 sec)
```

`INDEX_ID` 是 TiDB 为每个索引分配的唯一 ID。它可以与从另一个表或 API 获得的 `INDEX_ID` 一起执行 `join` 操作。

例如，你可以在 [`SLOW_QUERY` 表](/information-schema/information-schema-slow-query.md) 中获取某些慢查询所涉及的 `TABLE_ID` 和 `INDEX_ID`，然后使用以下 SQL 语句获取特定索引信息：

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

`TIDB_INDEXES` 表中列的含义如下：

* `TABLE_SCHEMA`：索引所在表的所属数据库的名称。
* `TABLE_NAME`：索引所在表的名称。
* `NON_UNIQUE`：如果索引是唯一的，则为 `0`，否则为 `1`。
* `KEY_NAME`：索引的名称。如果索引是主键，则名称为 `PRIMARY`。
* `SEQ_IN_INDEX`：索引中列的顺序编号，从 `1` 开始。
* `COLUMN_NAME`：索引所在的列名。
* `SUB_PART`：索引前缀长度。如果列是部分被索引，则该值为被索引的字符数量，否则为 `NULL`。
* `INDEX_COMMENT`：创建索引时以 `COMMENT` 标注的注释。
* `INDEX_ID`：索引的 ID。
