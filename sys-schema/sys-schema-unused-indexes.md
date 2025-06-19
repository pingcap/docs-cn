---
title: schema_unused_indexes
summary: 了解 `sys` schema 中的 `schema_unused_indexes` 表。
---

# `schema_unused_indexes`

`schema_unused_indexes` 记录了自 TiDB 上次启动以来未被使用过的索引。它包含以下列：

- `OBJECT_SCHEMA`：包含索引的表所属的数据库名称。
- `OBJECT_NAME`：包含索引的表名。
- `INDEX_NAME`：索引名称。

```sql
USE SYS;
DESC SCHEMA_UNUSED_INDEXES;
```

输出结果如下：

```sql
+---------------+-------------+------+------+---------+-------+
| Field         | Type        | Null | Key  | Default | Extra |
+---------------+-------------+------+------+---------+-------+
| object_schema | varchar(64) | YES  |      | NULL    |       |
| object_name   | varchar(64) | YES  |      | NULL    |       |
| index_name    | varchar(64) | YES  |      | NULL    |       |
+---------------+-------------+------+------+---------+-------+
3 rows in set (0.00 sec)
```

## 手动创建 `schema_unused_indexes` 视图

对于从 v8.0.0 之前版本升级的集群，`sys` schema 及其中的视图不会自动创建。你可以使用以下 SQL 语句手动创建它们：

```sql
CREATE DATABASE IF NOT EXISTS sys;
CREATE OR REPLACE VIEW sys.schema_unused_indexes AS
  SELECT
    table_schema as object_schema,
    table_name as object_name,
    index_name
  FROM information_schema.cluster_tidb_index_usage
  WHERE
    table_schema not in ('sys', 'mysql', 'INFORMATION_SCHEMA', 'PERFORMANCE_SCHEMA') and
    index_name != 'PRIMARY'
  GROUP BY table_schema, table_name, index_name
  HAVING
    sum(last_access_time) is null;
```

## 更多信息

- [`INFORMATION_SCHEMA.TIDB_INDEX_USAGE`](/information-schema/information-schema-tidb-index-usage.md)
