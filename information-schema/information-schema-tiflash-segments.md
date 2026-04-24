---
title: TIFLASH_SEGMENTS
summary: 了解 information_schema 表 `TIFLASH_SEGMENTS`。
---

# TIFLASH_SEGMENTS

> **警告：**
>
> 请不要在生产环境中使用该系统表，因为该表字段信息尚未固定下来，可能会在 TiDB 未来版本中发生变化。

`TIFLASH_SEGMENTS` 表提供 TiFlash 内部数据表内分片 (Segment) 的统计信息。

```sql
USE information_schema;
DESC tiflash_segments;
```

```sql
+-------------------------------+-------------+------+------+---------+-------+
| Field                         | Type        | Null | Key  | Default | Extra |
+-------------------------------+-------------+------+------+---------+-------+
| TIDB_DATABASE                 | varchar(64) | YES  |      | NULL    |       |
| TIDB_TABLE                    | varchar(64) | YES  |      | NULL    |       |
| TABLE_ID                      | bigint      | YES  |      | NULL    |       |
| IS_TOMBSTONE                  | bigint      | YES  |      | NULL    |       |
| SEGMENT_ID                    | bigint      | YES  |      | NULL    |       |
| RANGE                         | varchar(64) | YES  |      | NULL    |       |
| EPOCH                         | bigint      | YES  |      | NULL    |       |
| ROWS                          | bigint      | YES  |      | NULL    |       |
| SIZE                          | bigint      | YES  |      | NULL    |       |
| DELTA_RATE                    | double      | YES  |      | NULL    |       |
| DELTA_MEMTABLE_ROWS           | bigint      | YES  |      | NULL    |       |
| DELTA_MEMTABLE_SIZE           | bigint      | YES  |      | NULL    |       |
| DELTA_MEMTABLE_COLUMN_FILES   | bigint      | YES  |      | NULL    |       |
| DELTA_MEMTABLE_DELETE_RANGES  | bigint      | YES  |      | NULL    |       |
| DELTA_PERSISTED_PAGE_ID       | bigint      | YES  |      | NULL    |       |
| DELTA_PERSISTED_ROWS          | bigint      | YES  |      | NULL    |       |
| DELTA_PERSISTED_SIZE          | bigint      | YES  |      | NULL    |       |
| DELTA_PERSISTED_COLUMN_FILES  | bigint      | YES  |      | NULL    |       |
| DELTA_PERSISTED_DELETE_RANGES | bigint      | YES  |      | NULL    |       |
| DELTA_CACHE_SIZE              | bigint      | YES  |      | NULL    |       |
| DELTA_INDEX_SIZE              | bigint      | YES  |      | NULL    |       |
| STABLE_PAGE_ID                | bigint      | YES  |      | NULL    |       |
| STABLE_ROWS                   | bigint      | YES  |      | NULL    |       |
| STABLE_SIZE                   | bigint      | YES  |      | NULL    |       |
| STABLE_DMFILES                | bigint      | YES  |      | NULL    |       |
| STABLE_DMFILES_ID_0           | bigint      | YES  |      | NULL    |       |
| STABLE_DMFILES_ROWS           | bigint      | YES  |      | NULL    |       |
| STABLE_DMFILES_SIZE           | bigint      | YES  |      | NULL    |       |
| STABLE_DMFILES_SIZE_ON_DISK   | bigint      | YES  |      | NULL    |       |
| STABLE_DMFILES_PACKS          | bigint      | YES  |      | NULL    |       |
| TIFLASH_INSTANCE              | varchar(64) | YES  |      | NULL    |       |
+-------------------------------+-------------+------+------+---------+-------+
```

`TIFLASH_SEGMENTS` 表中各列的字段含义如下：

- `TIDB_DATABASE`：Segment 所属表所属的数据库的名称。
- `TIDB_TABLE`：Segment 所属表的名称。
- `TABLE_ID`：Segment 所属表的内部 ID，该 ID 在一个 TiDB 集群内部唯一。
- `IS_TOMBSTONE`：表示该 Segment 所属表是否处于待回收状态，为 1 表示该表处于待回收状态，为 0 则表示处于正常状态。
- `SEGMENT_ID`：Segment ID，该 ID 在每张表内部唯一。
- `RANGE`：Segment 包含数据的范围。
- `EPOCH`：Segment 的更新版本号，每个 Segment 的版本号单调递增。
- `ROWS`：Segment 的数据总行数。
- `SIZE`：Segment 的数据总大小（单位：字节）。
- `DELTA_RATE`：Delta 层的数据总行数占 Segment 数据总行数的比例。
- `DELTA_MEMTABLE_ROWS`：Delta 层缓存中的数据总行数。
- `DELTA_MEMTABLE_SIZE`：Delta 层缓存中的数据总大小（单位：字节）。
- `DELTA_MEMTABLE_COLUMN_FILES`：Delta 层缓存中 Column File 数量。
- `DELTA_MEMTABLE_DELETE_RANGES`：Delta 层缓存中 Delete Range 数量。
- `DELTA_PERSISTED_PAGE_ID`：Delta 层数据在磁盘上存储的 ID。
- `DELTA_PERSISTED_ROWS`：Delta 层已落盘的数据总行数。
- `DELTA_PERSISTED_SIZE`：Delta 层已落盘的数据总大小（单位：字节）。
- `DELTA_PERSISTED_COLUMN_FILES`：Delta 层已落盘 Column File 数量。
- `DELTA_PERSISTED_DELETE_RANGES`：Delta 层已落盘 Delete Range 数量。
- `DELTA_CACHE_SIZE`：Delta 层缓存大小（单位：字节）。
- `DELTA_INDEX_SIZE`：Delta 层索引大小（单位：字节）。
- `STABLE_PAGE_ID`：Stable 层数据在磁盘上存储的标识。
- `STABLE_ROWS`：Stable 层的数据总行数。
- `STABLE_SIZE`：Stable 层的数据总大小（单位：字节）。
- `STABLE_DMFILES`：Stable 层 DMFile 数量。
- `STABLE_DMFILES_ID_0`：Stable 层第一个 DMFile 在磁盘上存储的 ID。
- `STABLE_DMFILES_ROWS`：Stable 层 DMFile 中的数据总行数。
- `STABLE_DMFILES_SIZE`：Stable 层 DMFile 中的数据总大小（单位：字节）。
- `STABLE_DMFILES_SIZE_ON_DISK`：Stable 层 DMFile 中的数据在磁盘占据的空间大小（单位：字节）。
- `STABLE_DMFILES_PACKS`：Stable 层 DMFile 中包含的 Pack 数量。
- `TIFLASH_INSTANCE`：TiFlash 实例地址。
