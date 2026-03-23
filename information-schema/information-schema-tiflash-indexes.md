---
title: TIFLASH_INDEXES
summary: 了解 INFORMATION_SCHEMA 表 `TIFLASH_INDEXES`。
---

# TIFLASH_INDEXES

> **警告：**
>
> 该表目前为实验特性，不建议在生产环境中使用。该表的字段目前尚未稳定，未来 TiDB 版本中可能发生变更。如果发现 bug，请在 GitHub 上提 [issue](https://github.com/pingcap/tidb/issues) 反馈。

`TIFLASH_INDEXES` 表提供有关 TiFlash 副本上索引构建的统计信息。

```sql
USE INFORMATION_SCHEMA;
DESC TIFLASH_INDEXES;
```

输出结果如下：

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
- `COLUMN_NAME`：索引所在的列名。
- `INDEX_NAME`：索引的名称。
- `COLUMN_ID`：索引所在的列 ID。
- `INDEX_ID`：索引的 ID。
- `INDEX_KIND`：索引的类型。
- `ROWS_STABLE_INDEXED`：TiFlash 副本中 Stable 层已完成索引构建的行数。
- `ROWS_STABLE_NOT_INDEXED`：TiFlash 副本中 Stable 层尚未构建索引的行数。
- `ROWS_DELTA_INDEXED`：TiFlash 副本中 Delta 层已完成索引构建的行数。
- `ROWS_DELTA_NOT_INDEXED`：TiFlash 副本中 Delta 层尚未构建索引的行数。
- `ERROR_MESSAGE`：索引构建过程中出现的不可恢复错误的信息。
- `TIFLASH_INSTANCE`：执行索引构建任务的 TiFlash 实例地址。
