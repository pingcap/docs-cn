---
title: TIDB_INDEXES
summary: Learn the `TIDB_INDEXES` information_schema table.
---

# TIDB_INDEXES

The `TIDB_INDEXES` table provides the INDEX information of all tables.

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

`INDEX_ID` is the unique ID that TiDB allocates for each index. It can be used to do a join operation with `INDEX_ID` obtained from another table or API.

For example, you can obtain `TABLE_ID` and `INDEX_ID` that are involved in some slow query in the [`SLOW_QUERY` table](/information-schema/information-schema-slow-query.md) and then obtain the specific index information using the following SQL statements:

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

Fields in the `TIDB_INDEXES` table are described as follows:

* `TABLE_SCHEMA`: The name of the schema to which the index belongs.
* `TABLE_NAME`: The name of the table to which the index belongs.
* `NON_UNIQUE`: If the index is unique, the value is `0`; otherwise, the value is `1`.
* `KEY_NAME`: The index name. If the index is the primary key, the name is `PRIMARY`.
* `SEQ_IN_INDEX`: The sequential number of columns in the index, which starts from `1`.
* `COLUMN_NAME`: The name of the column where the index is located.
* `SUB_PART`: The prefix length of the index. If the column is partly indexed, the `SUB_PART` value is the count of the indexed characters; otherwise, the value is `NULL`.
* `INDEX_COMMENT`: The comment of the index, which is made when the index is created.
* `INDEX_ID`: The index ID.
* `IS_VISIBLE`: Whether the index is visible.
* `CLUSTERED`: Whether it is a [clustered index](/clustered-indexes.md).
