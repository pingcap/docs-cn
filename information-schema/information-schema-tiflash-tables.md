---
title: TIFLASH_TABLES
summary: 了解 information_schema 表 `TIFLASH_TABLES`。
---

# TIFLASH_TABLES

> **警告：**
>
> 请不要在生产环境中使用该系统表，因为该表字段信息尚未固定下来，可能会在 TiDB 未来版本中发生变化。

`TIFLASH_TABLES` 表提供了 TiFlash 内部数据表的统计信息。

```sql
USE information_schema;
DESC tiflash_tables;
```

```sql
+-------------------------------------------+--------------+------+------+---------+-------+
| Field                                     | Type         | Null | Key  | Default | Extra |
+-------------------------------------------+--------------+------+------+---------+-------+
| TIDB_DATABASE                             | varchar(64)  | YES  |      | NULL    |       |
| TIDB_TABLE                                | varchar(64)  | YES  |      | NULL    |       |
| TABLE_ID                                  | bigint       | YES  |      | NULL    |       |
| IS_TOMBSTONE                              | bigint       | YES  |      | NULL    |       |
| SEGMENT_COUNT                             | bigint       | YES  |      | NULL    |       |
| TOTAL_ROWS                                | bigint       | YES  |      | NULL    |       |
| TOTAL_SIZE                                | bigint       | YES  |      | NULL    |       |
| TOTAL_DELETE_RANGES                       | bigint       | YES  |      | NULL    |       |
| DELTA_RATE_ROWS                           | double       | YES  |      | NULL    |       |
| DELTA_RATE_SEGMENTS                       | double       | YES  |      | NULL    |       |
| DELTA_PLACED_RATE                         | double       | YES  |      | NULL    |       |
| DELTA_CACHE_SIZE                          | bigint       | YES  |      | NULL    |       |
| DELTA_CACHE_RATE                          | double       | YES  |      | NULL    |       |
| DELTA_CACHE_WASTED_RATE                   | double       | YES  |      | NULL    |       |
| DELTA_INDEX_SIZE                          | bigint       | YES  |      | NULL    |       |
| AVG_SEGMENT_ROWS                          | double       | YES  |      | NULL    |       |
| AVG_SEGMENT_SIZE                          | double       | YES  |      | NULL    |       |
| DELTA_COUNT                               | bigint       | YES  |      | NULL    |       |
| TOTAL_DELTA_ROWS                          | bigint       | YES  |      | NULL    |       |
| TOTAL_DELTA_SIZE                          | bigint       | YES  |      | NULL    |       |
| AVG_DELTA_ROWS                            | double       | YES  |      | NULL    |       |
| AVG_DELTA_SIZE                            | double       | YES  |      | NULL    |       |
| AVG_DELTA_DELETE_RANGES                   | double       | YES  |      | NULL    |       |
| STABLE_COUNT                              | bigint       | YES  |      | NULL    |       |
| TOTAL_STABLE_ROWS                         | bigint       | YES  |      | NULL    |       |
| TOTAL_STABLE_SIZE                         | bigint       | YES  |      | NULL    |       |
| TOTAL_STABLE_SIZE_ON_DISK                 | bigint       | YES  |      | NULL    |       |
| AVG_STABLE_ROWS                           | double       | YES  |      | NULL    |       |
| AVG_STABLE_SIZE                           | double       | YES  |      | NULL    |       |
| TOTAL_PACK_COUNT_IN_DELTA                 | bigint       | YES  |      | NULL    |       |
| MAX_PACK_COUNT_IN_DELTA                   | bigint       | YES  |      | NULL    |       |
| AVG_PACK_COUNT_IN_DELTA                   | double       | YES  |      | NULL    |       |
| AVG_PACK_ROWS_IN_DELTA                    | double       | YES  |      | NULL    |       |
| AVG_PACK_SIZE_IN_DELTA                    | double       | YES  |      | NULL    |       |
| TOTAL_PACK_COUNT_IN_STABLE                | bigint       | YES  |      | NULL    |       |
| AVG_PACK_COUNT_IN_STABLE                  | double       | YES  |      | NULL    |       |
| AVG_PACK_ROWS_IN_STABLE                   | double       | YES  |      | NULL    |       |
| AVG_PACK_SIZE_IN_STABLE                   | double       | YES  |      | NULL    |       |
| STORAGE_STABLE_NUM_SNAPSHOTS              | bigint       | YES  |      | NULL    |       |
| STORAGE_STABLE_OLDEST_SNAPSHOT_LIFETIME   | double       | YES  |      | NULL    |       |
| STORAGE_STABLE_OLDEST_SNAPSHOT_THREAD_ID  | bigint       | YES  |      | NULL    |       |
| STORAGE_STABLE_OLDEST_SNAPSHOT_TRACING_ID | varchar(128) | YES  |      | NULL    |       |
| STORAGE_DELTA_NUM_SNAPSHOTS               | bigint       | YES  |      | NULL    |       |
| STORAGE_DELTA_OLDEST_SNAPSHOT_LIFETIME    | double       | YES  |      | NULL    |       |
| STORAGE_DELTA_OLDEST_SNAPSHOT_THREAD_ID   | bigint       | YES  |      | NULL    |       |
| STORAGE_DELTA_OLDEST_SNAPSHOT_TRACING_ID  | varchar(128) | YES  |      | NULL    |       |
| STORAGE_META_NUM_SNAPSHOTS                | bigint       | YES  |      | NULL    |       |
| STORAGE_META_OLDEST_SNAPSHOT_LIFETIME     | double       | YES  |      | NULL    |       |
| STORAGE_META_OLDEST_SNAPSHOT_THREAD_ID    | bigint       | YES  |      | NULL    |       |
| STORAGE_META_OLDEST_SNAPSHOT_TRACING_ID   | varchar(128) | YES  |      | NULL    |       |
| BACKGROUND_TASKS_LENGTH                   | bigint       | YES  |      | NULL    |       |
| TIFLASH_INSTANCE                          | varchar(64)  | YES  |      | NULL    |       |
+-------------------------------------------+--------------+------+------+---------+-------+
```

`TIFLASH_TABLES` 表中各列的字段含义如下：

- `TIDB_DATABASE`：表所属的数据库的名称。
- `TIDB_TABLE`：表的名称。
- `TABLE_ID`：表的内部 ID，该 ID 在一个 TiDB 集群内部唯一。
- `IS_TOMBSTONE`：表示该表是否处于待回收状态，为 1 表示该表处于待回收状态，为 0 则表示处于正常状态。
- `SEGMENT_COUNT`：表的 Segment 数量，其中 Segment 为 TiFlash 内部管理数据的单元。
- `TOTAL_ROWS`：表的总行数。
- `TOTAL_SIZE`：表的总大小（单位：字节）。
- `TOTAL_DELETE_RANGES`：表当前 Delete Range 的数量。
- `DELTA_RATE_ROWS`：表 Delta 层数据总行数占该表总行数的比例。
- `DELTA_RATE_SEGMENTS`：表所有 Segment 中包含非空 Delta 层的 Segment 的比例。
- `DELTA_PLACED_RATE`：表 Delta 层数据行中已经完成 Index 构建的比例。
- `DELTA_CACHE_SIZE`：表 Delta 层缓存大小（单位：字节）。
- `DELTA_CACHE_RATE`：表 Delta 层数据的缓存比例。
- `DELTA_CACHE_WASTED_RATE`：表 Delta 层缓存中无效数据的比例。
- `DELTA_INDEX_SIZE`：Delta Index 占用的内存大小（单位：字节）。
- `AVG_SEGMENT_ROWS`：表所有 Segment 的平均行数。
- `AVG_SEGMENT_SIZE`：表所有 Segment 的平均大小（单位：字节）。
- `DELTA_COUNT`：表中包含 Delta 层的 Segment 的个数。
- `TOTAL_DELTA_ROWS`：所有 Delta 层的数据总行数。
- `TOTAL_DELTA_SIZE`：所有 Delta 层的数据总大小（单位：字节）。
- `AVG_DELTA_ROWS`：所有 Delta 层的平均数据行数。
- `AVG_DELTA_SIZE`：所有 Delta 层的平均数据大小（单位：字节）。
- `AVG_DELTA_DELETE_RANGES`：所有 Delta 层的平均 Delete Range 操作个数。
- `STABLE_COUNT`：表中包含非空 Stable 层的 Segment 的个数。
- `TOTAL_STABLE_ROWS`：所有 Stable 层的数据总行数。
- `TOTAL_STABLE_SIZE`：所有 Stable 层的数据总大小（单位：字节）。
- `TOTAL_STABLE_SIZE_ON_DISK`：所有 Stable 层的数据在磁盘占据的空间大小（单位：字节）。
- `AVG_STABLE_ROWS`：所有 Stable 层的平均数据行数。
- `AVG_STABLE_SIZE`：所有 Stable 层的平均数据大小（单位：字节）。
- `TOTAL_PACK_COUNT_IN_DELTA`：所有 Delta 层的 Column File 总数量。
- `MAX_PACK_COUNT_IN_DELTA`：单个 Delta 层包含 Column File 数量的最大值。
- `AVG_PACK_COUNT_IN_DELTA`：所有 Delta 层的平均 Column File 数量。
- `AVG_PACK_ROWS_IN_DELTA`：Delta 层所有 Column File 的平均数据行数。
- `AVG_PACK_SIZE_IN_DELTA`：Delta 层所有 Column File 的平均数据大小（单位：字节）。
- `TOTAL_PACK_COUNT_IN_STABLE`：所有 Stable 层的 Pack 总数量。
- `AVG_PACK_COUNT_IN_STABLE`：所有 Stable 层的平均 Pack 数量。
- `AVG_PACK_ROWS_IN_STABLE`：Stable 层所有 Pack 的平均数据行数。
- `AVG_PACK_SIZE_IN_STABLE`：Stable 层所有 Pack 的平均数据大小（单位：字节）。
- `STORAGE_STABLE_NUM_SNAPSHOTS`：Stable 层 Snapshot 数量。
- `STORAGE_STABLE_OLDEST_SNAPSHOT_LIFETIME`：Stable 层最早 Snapshot 的持续时间（单位：秒）。
- `STORAGE_STABLE_OLDEST_SNAPSHOT_THREAD_ID`：Stable 层最早 Snapshot 对应的线程 ID。
- `STORAGE_STABLE_OLDEST_SNAPSHOT_TRACING_ID`：Stable 层最早 Snapshot 对应的跟踪 ID。
- `STORAGE_DELTA_NUM_SNAPSHOTS`：Delta 层 Snapshot 数量。
- `STORAGE_DELTA_OLDEST_SNAPSHOT_LIFETIME`：Delta 层最早 Snapshot 的持续时间（单位：秒）。
- `STORAGE_DELTA_OLDEST_SNAPSHOT_THREAD_ID`：Delta 层最早 Snapshot 对应的线程 ID。
- `STORAGE_DELTA_OLDEST_SNAPSHOT_TRACING_ID`：Delta 层最早 Snapshot 对应的跟踪 ID。
- `STORAGE_META_NUM_SNAPSHOTS`：Meta 元信息 Snapshot 数量。
- `STORAGE_META_OLDEST_SNAPSHOT_LIFETIME`：Meta 元信息最早 Snapshot 的持续时间。（单位：秒）
- `STORAGE_META_OLDEST_SNAPSHOT_THREAD_ID`：Meta 元信息最早 Snapshot 对应的线程 ID。
- `STORAGE_META_OLDEST_SNAPSHOT_TRACING_ID`：Meta 元信息最早 Snapshot 对应的跟踪 ID。
- `BACKGROUND_TASKS_LENGTH`：后台任务队列长度。
- `TIFLASH_INSTANCE`：TiFlash 实例地址。
