---
title: TIFLASH_INDEXES
summary: 了解 information_schema 表 `TIFLASH_INDEXES`。
---

# TIFLASH_INDEXES

> **警告：**
>
> 请不要在生产环境中使用该系统表，因为该表字段信息尚未固定下来，可能会在 TiDB 未来版本中发生变化。

`TIFLASH_INDEXES` 表提供有关 TiFlash 副本上索引构建的的统计信息。

```sql
USE information_schema;
DESC tiflash_indexes;
```

```sql
+-------------------------+---------------+------+------+---------+-------+
| Field                   | Type          | Null | Key  | Default | Extra |
+-------------------------+---------------+------+------+---------+-------+
| TIDB_DATABASE           | varchar(64)   | YES  |      | NULL    |       |
| TIDB_TABLE              | varchar(64)   | YES  |      | NULL    |       |
| TABLE_ID                | bigint        | YES  |      | NULL    |       |
| COLUMN_NAME             | varchar(64)   | YES  |      | NULL    |       |
| INDEX_NAME              | varchar(64)   | YES  |      | NULL    |       |
| COLUMN_ID               | bigint        | YES  |      | NULL    |       |
| INDEX_ID                | bigint        | YES  |      | NULL    |       |
| INDEX_KIND              | varchar(64)   | YES  |      | NULL    |       |
| ROWS_STABLE_INDEXED     | bigint        | YES  |      | NULL    |       |
| ROWS_STABLE_NOT_INDEXED | bigint        | YES  |      | NULL    |       |
| ROWS_DELTA_INDEXED      | bigint        | YES  |      | NULL    |       |
| ROWS_DELTA_NOT_INDEXED  | bigint        | YES  |      | NULL    |       |
| ERROR_MESSAGE           | varchar(1024) | YES  |      | NULL    |       |
| TIFLASH_INSTANCE        | varchar(64)   | YES  |      | NULL    |       |
+-------------------------+---------------+------+------+---------+-------+
```

`TIFLASH_INDEXES` 表中各列的字段含义如下：

- `TIDB_DATABASE`：表所属的数据库的名称。
- `TIDB_TABLE`：表的名称。
- `TABLE_ID`：表的内部 ID，该 ID 在一个 TiDB 集群内部唯一。
- `COLUMN_NAME`：索引所在的列名
- `INDEX_NAME`：索引的名称
- `COLUMN_ID`：索引所在的列 ID
- `INDEX_ID`：索引的 ID
- `INDEX_KIND`：索引的类型
- `ROWS_STABLE_INDEXED`：TiFlash 副本中 Stable 层已经构建完索引的行数
- `ROWS_STABLE_NOT_INDEXED`：TiFlash 副本中 Stable 层未构建索引的行数
- `ROWS_DELTA_INDEXED`：TiFlash 副本中 Delta 层已经构建完索引的行数
- `ROWS_DELTA_NOT_INDEXED`：TiFlash 副本中 Delta 层未构建索引的行数
- `ERROR_MESSAGE`：索引构建过程中遇到不可恢复的错误信息
- `TIFLASH_INSTANCE`：TiFlash 实例地址。
