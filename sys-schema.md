---
title: sys Schema
summary: 了解 sys 库中的系统表。
---

# `sys` Schema

> **注意：**
>
> 从 v8.0.0 及之前版本升级的集群将不包含 `sys` Schema 和其中的 View。它们可以通过以下 SQL 语句创建：
>
> {{< copyable "sql" >}}
>
> ```sql
> CREATE DATABASE IF NOT EXISTS sys;
> CREATE OR REPLACE VIEW sys.schema_unused_indexes AS
>   SELECT
>     table_schema as object_schema,
>     table_name as object_name,
>     index_name
>   FROM information_schema.cluster_tidb_index_usage
>   WHERE
>     table_schema not in ('sys', 'mysql', 'INFORMATION_SCHEMA', 'PERFORMANCE_SCHEMA') and
>     index_name != 'PRIMARY'
>   GROUP BY table_schema, table_name, index_name
>   HAVING
>     sum(last_access_time) is null;
> ```

`sys` 库里的表或视图被用于帮助用户理解 TiDB 的系统表、`INFORMATION_SCHEMA` 表和 `Performance Schema` 表内的数据。

- `schema_unused_index` 用于记录自从 TiDB 上一次重启以来未使用的索引。
    - `OBJECT_SCHEMA`：索引所在表的所属数据库的名称。
    - `OBJECT_NAME`：索引所在表的名称。
    - `INDEX_NAME`：索引的名称。