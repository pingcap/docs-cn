---
title: STATISTICS
summary: Learn the `STATISTICS` information_schema table.
---

# STATISTICS

The `STATISTICS` table provides information about table indexes.

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

Fields in the `STATISTICS` table are described as follows:

* `TABLE_CATALOG`: The name of the catalog to which the table containing the index belongs. This value is always `def`.
* `TABLE_SCHEMA`: The name of the database to which the table containing the index belongs.
* `TABLE_NAME`: The name of the table containing the index.
* `NON_UNIQUE`: If the index must not contain duplicate values, the value is `0`; if duplicate values are allowed in the index, the value is `1`.
* `INDEX_SCHEMA`: The name of the database to which the index belongs.
* `INDEX_NAME`: The name of the index. If the index is the primary key, then the value is always `PRIMARY`.
* `SEQ_IN_INDEX`: The column number in the index, starting from `1`.
* `COLUMN_NAME`: The column name. See the description of the `Expression` column.
* `COLLATION`: The sorting method of the columns in the index. The value can be `A` (ascending order), `D` (descending order) or `NULL` (unsorted).
* `CARDINALITY`: The estimated number of unique values ​​in the index. To update this value, execute `ANALYZE TABLE`.
* `SUB_PART`: The prefix of the index. If only part of the prefix of the column is indexed, the value is the number of indexed characters; if the entire column is indexed, the value is `NULL`.
* `PACKED`: TiDB does not use this field. This value is always `NULL`.
* `NULLABLE`: If the column might contain a `NULL` value, the value is `YES`; if not, the value is `''`.
* `INDEX_TYPE`: The type of the index.
* `COMMENT`: Other information related to the index.
* `INDEX_COMMENT`: Any comment with comment attribute provided for the index when creating the index.
* `IS_VISIBLE`: Whether the optimizer can use this index.
* `Expression` For the index key of the non-expression part, this value is `NULL`; for the index key of the expression part, this value is the expression itself. Refer to [Expression Index](/sql-statements/sql-statement-create-index.md#expression-index).

The following statements are equivalent:

```sql
SELECT * FROM INFORMATION_SCHEMA.STATISTICS
  WHERE table_name = 'tbl_name'
  AND table_schema = 'db_name'

SHOW INDEX
  FROM tbl_name
  FROM db_name
```