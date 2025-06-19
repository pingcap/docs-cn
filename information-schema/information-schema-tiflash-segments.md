---
title: TIFLASH_SEGMENTS
summary: 了解 `TIFLASH_SEGMENTS` information_schema 表。
---

# TIFLASH_SEGMENTS

> **警告：**
>
> 请勿在生产环境中使用此表，因为表中的字段不稳定，可能会在新版本的 TiDB 中发生变更，且不会提前通知。

`TIFLASH_SEGMENTS` 表提供了 TiFlash 中数据表的统计信息。

```sql
USE information_schema;
DESC tiflash_segments;
```

```sql
+-------------------------------+-------------+------+------+---------+-------+
| Field                         | Type        | Null | Key  | Default | Extra |
+-------------------------------+-------------+------+------+---------+-------+
| DATABASE                      | varchar(64) | YES  |      | NULL    |       |
| TABLE                         | varchar(64) | YES  |      | NULL    |       |
| TIDB_DATABASE                 | varchar(64) | YES  |      | NULL    |       |
| TIDB_TABLE                    | varchar(64) | YES  |      | NULL    |       |
| TABLE_ID                      | bigint(64)  | YES  |      | NULL    |       |
| IS_TOMBSTONE                  | bigint(64)  | YES  |      | NULL    |       |
| SEGMENT_ID                    | bigint(64)  | YES  |      | NULL    |       |
| RANGE                         | varchar(64) | YES  |      | NULL    |       |
| EPOCH                         | bigint(64)  | YES  |      | NULL    |       |
| ROWS                          | bigint(64)  | YES  |      | NULL    |       |
| SIZE                          | bigint(64)  | YES  |      | NULL    |       |
| DELTA_RATE                    | double      | YES  |      | NULL    |       |
| DELTA_MEMTABLE_ROWS           | bigint(64)  | YES  |      | NULL    |       |
| DELTA_MEMTABLE_SIZE           | bigint(64)  | YES  |      | NULL    |       |
| DELTA_MEMTABLE_COLUMN_FILES   | bigint(64)  | YES  |      | NULL    |       |
| DELTA_MEMTABLE_DELETE_RANGES  | bigint(64)  | YES  |      | NULL    |       |
| DELTA_PERSISTED_PAGE_ID       | bigint(64)  | YES  |      | NULL    |       |
| DELTA_PERSISTED_ROWS          | bigint(64)  | YES  |      | NULL    |       |
| DELTA_PERSISTED_SIZE          | bigint(64)  | YES  |      | NULL    |       |
| DELTA_PERSISTED_COLUMN_FILES  | bigint(64)  | YES  |      | NULL    |       |
| DELTA_PERSISTED_DELETE_RANGES | bigint(64)  | YES  |      | NULL    |       |
| DELTA_CACHE_SIZE              | bigint(64)  | YES  |      | NULL    |       |
| DELTA_INDEX_SIZE              | bigint(64)  | YES  |      | NULL    |       |
| STABLE_PAGE_ID                | bigint(64)  | YES  |      | NULL    |       |
| STABLE_ROWS                   | bigint(64)  | YES  |      | NULL    |       |
| STABLE_SIZE                   | bigint(64)  | YES  |      | NULL    |       |
| STABLE_DMFILES                | bigint(64)  | YES  |      | NULL    |       |
| STABLE_DMFILES_ID_0           | bigint(64)  | YES  |      | NULL    |       |
| STABLE_DMFILES_ROWS           | bigint(64)  | YES  |      | NULL    |       |
| STABLE_DMFILES_SIZE           | bigint(64)  | YES  |      | NULL    |       |
| STABLE_DMFILES_SIZE_ON_DISK   | bigint(64)  | YES  |      | NULL    |       |
| STABLE_DMFILES_PACKS          | bigint(64)  | YES  |      | NULL    |       |
| TIFLASH_INSTANCE              | varchar(64) | YES  |      | NULL    |       |
+-------------------------------+-------------+------+------+---------+-------+
33 rows in set (0.00 sec)
```

`TIFLASH_SEGMENTS` 表中的字段说明如下：

- `DATABASE`：TiFlash 中的数据库名称。该段所属的表在此数据库中。
- `TABLE`：TiFlash 中的表名。该段属于此表。
- `TIDB_DATABASE`：TiDB 中的数据库名称。该段所属的表在此数据库中。
- `TIDB_TABLE`：TiDB 中的表名。该段属于此表。
- `TABLE_ID`：该段所属表的内部 ID。此 ID 在 TiDB 集群内唯一。
- `IS_TOMBSTONE`：表示该段所属的表是否可以被回收。`1` 表示表可以被回收，`0` 表示表处于正常状态。
- `SEGMENT_ID`：段 ID，在表内唯一。
- `RANGE`：该段包含的数据范围。
- `EPOCH`：该段的更新版本。每个段的版本号单调递增。
- `ROWS`：该段中的总行数。
- `SIZE`：该段数据的总大小（以字节为单位）。
- `DELTA_RATE`：Delta 层中的总行数与该段中总行数的比率。
- `DELTA_MEMTABLE_ROWS`：Delta 层中缓存的总行数。
- `DELTA_MEMTABLE_SIZE`：Delta 层中缓存的数据总大小（以字节为单位）。
- `DELTA_MEMTABLE_COLUMN_FILES`：Delta 层中缓存的 Column Files 数量。
- `DELTA_MEMTABLE_DELETE_RANGES`：Delta 层中缓存的 Delete Ranges 数量。
- `DELTA_PERSISTED_PAGE_ID`：Delta 层中存储在磁盘上的数据的 ID。
- `DELTA_PERSISTED_ROWS`：Delta 层中持久化数据的总行数。
- `DELTA_PERSISTED_SIZE`：Delta 层中持久化数据的总大小（以字节为单位）。
- `DELTA_PERSISTED_COLUMN_FILES`：Delta 层中持久化的 Column Files 数量。
- `DELTA_PERSISTED_DELETE_RANGES`：Delta 层中持久化的 Delete Ranges 数量。
- `DELTA_CACHE_SIZE`：Delta 层中缓存的大小（以字节为单位）。
- `DELTA_INDEX_SIZE`：Delta 层中索引的大小（以字节为单位）。
- `STABLE_PAGE_ID`：Stable 层中数据的磁盘存储 ID。
- `STABLE_ROWS`：Stable 层中的总行数。
- `STABLE_SIZE`：Stable 层中数据的总大小（以字节为单位）。
- `STABLE_DMFILES`：Stable 层中的 DMFiles 数量。
- `STABLE_DMFILES_ID_0`：Stable 层中第一个 DMFile 的磁盘存储 ID。
- `STABLE_DMFILES_ROWS`：Stable 层中 DMFile 的总行数。
- `STABLE_DMFILES_SIZE`：Stable 层中 DMFile 数据的总大小（以字节为单位）。
- `STABLE_DMFILES_SIZE_ON_DISK`：Stable 层中 DMFile 占用的磁盘空间（以字节为单位）。
- `STABLE_DMFILES_PACKS`：Stable 层中 DMFile 的 Packs 数量。
- `TIFLASH_INSTANCE`：TiFlash 实例的地址。
