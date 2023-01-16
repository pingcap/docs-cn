---
title: TIFLASH_TABLES
summary: Learn the `TIFLASH_TABLES` information_schema table.
---

# TIFLASH_TABLES

> **Warning:**
>
> Do not use this table in production environments, as the fields of the table are unstable, and subject to change in new releases of TiDB, without prior notice.

The `TIFLASH_TABLES` table provides statistical information about data tables in TiFlash.

```sql
USE information_schema;
DESC tiflash_tables;
```

```sql
+-------------------------------------------+--------------+------+------+---------+-------+
| Field                                     | Type         | Null | Key  | Default | Extra |
+-------------------------------------------+--------------+------+------+---------+-------+
| DATABASE                                  | varchar(64)  | YES  |      | NULL    |       |
| TABLE                                     | varchar(64)  | YES  |      | NULL    |       |
| TIDB_DATABASE                             | varchar(64)  | YES  |      | NULL    |       |
| TIDB_TABLE                                | varchar(64)  | YES  |      | NULL    |       |
| TABLE_ID                                  | bigint(64)   | YES  |      | NULL    |       |
| IS_TOMBSTONE                              | bigint(64)   | YES  |      | NULL    |       |
| SEGMENT_COUNT                             | bigint(64)   | YES  |      | NULL    |       |
| TOTAL_ROWS                                | bigint(64)   | YES  |      | NULL    |       |
| TOTAL_SIZE                                | bigint(64)   | YES  |      | NULL    |       |
| TOTAL_DELETE_RANGES                       | bigint(64)   | YES  |      | NULL    |       |
| DELTA_RATE_ROWS                           | double       | YES  |      | NULL    |       |
| DELTA_RATE_SEGMENTS                       | double       | YES  |      | NULL    |       |
| DELTA_PLACED_RATE                         | double       | YES  |      | NULL    |       |
| DELTA_CACHE_SIZE                          | bigint(64)   | YES  |      | NULL    |       |
| DELTA_CACHE_RATE                          | double       | YES  |      | NULL    |       |
| DELTA_CACHE_WASTED_RATE                   | double       | YES  |      | NULL    |       |
| DELTA_INDEX_SIZE                          | bigint(64)   | YES  |      | NULL    |       |
| AVG_SEGMENT_ROWS                          | double       | YES  |      | NULL    |       |
| AVG_SEGMENT_SIZE                          | double       | YES  |      | NULL    |       |
| DELTA_COUNT                               | bigint(64)   | YES  |      | NULL    |       |
| TOTAL_DELTA_ROWS                          | bigint(64)   | YES  |      | NULL    |       |
| TOTAL_DELTA_SIZE                          | bigint(64)   | YES  |      | NULL    |       |
| AVG_DELTA_ROWS                            | double       | YES  |      | NULL    |       |
| AVG_DELTA_SIZE                            | double       | YES  |      | NULL    |       |
| AVG_DELTA_DELETE_RANGES                   | double       | YES  |      | NULL    |       |
| STABLE_COUNT                              | bigint(64)   | YES  |      | NULL    |       |
| TOTAL_STABLE_ROWS                         | bigint(64)   | YES  |      | NULL    |       |
| TOTAL_STABLE_SIZE                         | bigint(64)   | YES  |      | NULL    |       |
| TOTAL_STABLE_SIZE_ON_DISK                 | bigint(64)   | YES  |      | NULL    |       |
| AVG_STABLE_ROWS                           | double       | YES  |      | NULL    |       |
| AVG_STABLE_SIZE                           | double       | YES  |      | NULL    |       |
| TOTAL_PACK_COUNT_IN_DELTA                 | bigint(64)   | YES  |      | NULL    |       |
| MAX_PACK_COUNT_IN_DELTA                   | bigint(64)   | YES  |      | NULL    |       |
| AVG_PACK_COUNT_IN_DELTA                   | double       | YES  |      | NULL    |       |
| AVG_PACK_ROWS_IN_DELTA                    | double       | YES  |      | NULL    |       |
| AVG_PACK_SIZE_IN_DELTA                    | double       | YES  |      | NULL    |       |
| TOTAL_PACK_COUNT_IN_STABLE                | bigint(64)   | YES  |      | NULL    |       |
| AVG_PACK_COUNT_IN_STABLE                  | double       | YES  |      | NULL    |       |
| AVG_PACK_ROWS_IN_STABLE                   | double       | YES  |      | NULL    |       |
| AVG_PACK_SIZE_IN_STABLE                   | double       | YES  |      | NULL    |       |
| STORAGE_STABLE_NUM_SNAPSHOTS              | bigint(64)   | YES  |      | NULL    |       |
| STORAGE_STABLE_OLDEST_SNAPSHOT_LIFETIME   | double       | YES  |      | NULL    |       |
| STORAGE_STABLE_OLDEST_SNAPSHOT_THREAD_ID  | bigint(64)   | YES  |      | NULL    |       |
| STORAGE_STABLE_OLDEST_SNAPSHOT_TRACING_ID | varchar(128) | YES  |      | NULL    |       |
| STORAGE_DELTA_NUM_SNAPSHOTS               | bigint(64)   | YES  |      | NULL    |       |
| STORAGE_DELTA_OLDEST_SNAPSHOT_LIFETIME    | double       | YES  |      | NULL    |       |
| STORAGE_DELTA_OLDEST_SNAPSHOT_THREAD_ID   | bigint(64)   | YES  |      | NULL    |       |
| STORAGE_DELTA_OLDEST_SNAPSHOT_TRACING_ID  | varchar(128) | YES  |      | NULL    |       |
| STORAGE_META_NUM_SNAPSHOTS                | bigint(64)   | YES  |      | NULL    |       |
| STORAGE_META_OLDEST_SNAPSHOT_LIFETIME     | double       | YES  |      | NULL    |       |
| STORAGE_META_OLDEST_SNAPSHOT_THREAD_ID    | bigint(64)   | YES  |      | NULL    |       |
| STORAGE_META_OLDEST_SNAPSHOT_TRACING_ID   | varchar(128) | YES  |      | NULL    |       |
| BACKGROUND_TASKS_LENGTH                   | bigint(64)   | YES  |      | NULL    |       |
| TIFLASH_INSTANCE                          | varchar(64)  | YES  |      | NULL    |       |
+-------------------------------------------+--------------+------+------+---------+-------+
54 rows in set (0.00 sec)
```

Fields in the `TIFLASH_TABLES` table are described as follows:

- `DATABASE`: The name of the database that the table belongs to in TiFlash.
- `TABLE`: The name of the table in TiFlash.
- `TIDB_DATABASE`: The name of the database that the table belongs to in TiDB.
- `TIDB_TABLE`: The name of the table in TiDB.
- `TABLE_ID`: The internal ID of the table, which is unique within a TiDB cluster.
- `IS_TOMBSTONE`: Indicates whether the table can be recycled. `1` indicates that the table can be recycled, and `0` indicates that the table is in a normal state.
- `SEGMENT_COUNT`: The number of segments in the table. A segment is a data management unit in TiFlash.
- `TOTAL_ROWS`: The total number of rows in the table.
- `TOTAL_SIZE`: The total size of the table (in bytes).
- `TOTAL_DELETE_RANGES`: The total number of Delete Ranges in the table.
- `DELTA_RATE_ROWS`: The ratio of the total rows of the table in the Delta layer to the total rows of that table.
- `DELTA_RATE_SEGMENTS`: The proportion of segments that contain a non-empty Delta layer in the table.
- `DELTA_PLACED_RATE`: The proportion of rows that have completed index construction of the table in the Delta layer.
- `DELTA_CACHE_SIZE`: The size of the cache of the table in the Delta layer (in bytes).
- `DELTA_CACHE_RATE`: The proportion of cache data of the table in the Delta layer.
- `DELTA_CACHE_WASTED_RATE`: The proportion of invalid cache data of the table in the Delta layer.
- `DELTA_INDEX_SIZE`: The size of the memory occupied by indexes in the Delta layer (in bytes).
- `AVG_SEGMENT_ROWS`: The average number of rows in all segments of the table.
- `AVG_SEGMENT_SIZE`: The average size of all segments of the table (in bytes).
- `DELTA_COUNT`: The number of segments that contain a non-empty Delta layer in the table.
- `TOTAL_DELTA_ROWS`: The total number of rows in the Delta layer.
- `TOTAL_DELTA_SIZE`: The total size of the data in the Delta layer (in bytes).
- `AVG_DELTA_ROWS`: The average number of rows of data in all Delta layers.
- `AVG_DELTA_SIZE`: The average size of data in all Delta layers (in bytes).
- `AVG_DELTA_DELETE_RANGES`: The average number of Delete Range operations in all Delta layers.
- `STABLE_COUNT`: The number of segments that contain a non-empty Stable layer in the table.
- `TOTAL_STABLE_ROWS`: The total number of rows in all Stable layers.
- `TOTAL_STABLE_SIZE`: The total size of the data in all Stable layers (in bytes).
- `TOTAL_STABLE_SIZE_ON_DISK`: The disk space occupied by the data in all Stable layers (in bytes).
- `AVG_STABLE_ROWS`: The average number of rows of data in all Stable layers.
- `AVG_STABLE_SIZE`: The average size of data in all Stable layers (in bytes).
- `TOTAL_PACK_COUNT_IN_DELTA`: The total number of Column Files in all Delta layers.
- `MAX_PACK_COUNT_IN_DELTA`: The maximum number of Column Files in a single Delta layer.
- `AVG_PACK_COUNT_IN_DELTA`: The average number of Column Files in all Delta layers.
- `AVG_PACK_ROWS_IN_DELTA`: The average number of rows in all Column Files in all Delta layers.
- `AVG_PACK_SIZE_IN_DELTA`: The average size of data in all Column Files in all Delta layers (in bytes).
- `TOTAL_PACK_COUNT_IN_STABLE`: The total number of Packs in all Stable layers.
- `AVG_PACK_COUNT_IN_STABLE`: The average number of Packs in all Stable layers.
- `AVG_PACK_ROWS_IN_STABLE`: The average number of rows in all Packs in all Stable layers.
- `AVG_PACK_SIZE_IN_STABLE`: The average size of data in all Packs in the Stable layer (in bytes).
- `STORAGE_STABLE_NUM_SNAPSHOTS`: The number of snapshots in the Stable layer.
- `STORAGE_STABLE_OLDEST_SNAPSHOT_LIFETIME`: The duration of the earliest snapshot in the Stable layer (in seconds).
- `STORAGE_STABLE_OLDEST_SNAPSHOT_THREAD_ID`: The thread ID of the earliest snapshot in the Stable layer.
- `STORAGE_STABLE_OLDEST_SNAPSHOT_TRACING_ID`: The tracing ID of the earliest snapshot in the Stable layer.
- `STORAGE_DELTA_NUM_SNAPSHOTS`: The number of snapshots in the Delta layer.
- `STORAGE_DELTA_OLDEST_SNAPSHOT_LIFETIME`: The duration of the earliest snapshot in the Delta layer (in seconds).
- `STORAGE_DELTA_OLDEST_SNAPSHOT_THREAD_ID`: The thread ID of the earliest snapshot in the Delta layer.
- `STORAGE_DELTA_OLDEST_SNAPSHOT_TRACING_ID`: The tracing ID of the earliest snapshot in the Delta layer.
- `STORAGE_META_NUM_SNAPSHOTS`: The number of snapshots in the meta information.
- `STORAGE_META_OLDEST_SNAPSHOT_LIFETIME`: The duration of the earliest snapshot in the meta information (in seconds).
- `STORAGE_META_OLDEST_SNAPSHOT_THREAD_ID`: The thread ID of the earliest snapshot in the meta information.
- `STORAGE_META_OLDEST_SNAPSHOT_TRACING_ID`: The tracing ID of the earliest snapshot in the meta information.
- `BACKGROUND_TASKS_LENGTH`: The length of the task queue in the background.
- `TIFLASH_INSTANCE`: The address of the TiFlash instance.
