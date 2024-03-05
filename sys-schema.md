---
title: sys Schema
summary: 了解 TiDB `sys` 系统数据库。
---

# `sys` Schema

TiDB 从 v8.0.0 开始提供 `sys` Schema。你可以通过查看 `sys` 系统数据库中的表或视图理解 TiDB 的系统表、[`INFORMATION_SCHEMA`](/information-schema/information-schema.md) 表和 [`PERFORMANCE SCHEMA`](/performance-schema/performance-schema.md) 表内的数据。

## 手动创建 `sys` Schema 和视图

对于从 v8.0.0 之前版本升级的集群，`sys` Schema 和其中的视图不会自动创建。你可以通过以下 SQL 语句手动创建：

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

## `schema_unused_index`

`schema_unused_index` 用于记录自 TiDB 上次启动以来未被使用的索引信息，包括如下列：

- `OBJECT_SCHEMA`：索引所在表的所属数据库的名称。
- `OBJECT_NAME`：索引所在表的名称。
- `INDEX_NAME`：索引的名称。

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
