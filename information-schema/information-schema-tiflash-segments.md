---
title: TIFLASH_SEGMENTS
summary: Learn the `TIFLASH_SEGMENTS` information_schema table.
---

# TIFLASH_SEGMENTS

> **Warning:**
>
> Do not use this table in production environments, as the fields of the table are unstable, and subject to change in new releases of TiDB, without prior notice.

The `TIFLASH_SEGMENTS` table provides statistical information about data tables in TiFlash.

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

Fields in the `TIFLASH_SEGMENTS` table are described as follows:

- `DATABASE`: Database name in TiFlash. The segment belongs to a table in this database.
- `TABLE`: Table name in TiFlash. The segment belongs to this table.
- `TIDB_DATABASE`: Database name in TiDB. The segment belongs to a table in this database.
- `TIDB_TABLE`: Table name in TiDB. The segment belongs to this table.
- `TABLE_ID`: The internal ID of the table to which the segment belongs. This ID is unique within a TiDB cluster.
- `IS_TOMBSTONE`: Indicates whether the table the segment belongs to can be recycled. `1` indicates that the table can be recycled. `0` indicates that the table is in a normal state.
- `SEGMENT_ID`: Segment ID, which is unique within a table.
- `RANGE`: The range of data that the segment contains.
- `EPOCH`: The updated version of the segment. The version number of each segment increases monotonically.
- `ROWS`: The total number of rows in the segment.
- `SIZE`: The total size of the segment data (in bytes).
- `DELTA_RATE`: The ratio of the total number of rows in the Delta layer to that in the segment.
- `DELTA_MEMTABLE_ROWS`: The total number of cached rows in the Delta layer.
- `DELTA_MEMTABLE_SIZE`: The total size of the data cached in the Delta layer (in bytes).
- `DELTA_MEMTABLE_COLUMN_FILES`: The number of Column Files cached in the Delta layer.
- `DELTA_MEMTABLE_DELETE_RANGES`: The number of Delete Ranges cached in the Delta layer.
- `DELTA_PERSISTED_PAGE_ID`: The ID of the data stored on a disk in the Delta layer.
- `DELTA_PERSISTED_ROWS`: The total number of rows of persisted data in the Delta layer.
- `DELTA_PERSISTED_SIZE`: The total size of the persisted data in the Delta layer (in bytes).
- `DELTA_PERSISTED_COLUMN_FILES`: The number of persisted Column Files in the Delta layer.
- `DELTA_PERSISTED_DELETE_RANGES`: The number of persisted Delete Ranges in the Delta layer.
- `DELTA_CACHE_SIZE`: The size of the cache in the Delta layer (in bytes).
- `DELTA_INDEX_SIZE`: The size of the indexes in the Delta layer (in bytes).
- `STABLE_PAGE_ID`: The disk storage ID of the data in the Stable layer.
- `STABLE_ROWS`: The total number of rows in the Stable layer.
- `STABLE_SIZE`: The total size of the data in the Stable layer (in bytes).
- `STABLE_DMFILES`: The number of DMFiles in the Stable layer.
- `STABLE_DMFILES_ID_0`: The disk storage ID of the first DMFile in the Stable layer.
- `STABLE_DMFILES_ROWS`: The total number of rows in the DMFile in the Stable layer.
- `STABLE_DMFILES_SIZE`: The total size of the data in the DMFile in the Stable layer (in bytes).
- `STABLE_DMFILES_SIZE_ON_DISK`: The disk space occupied by the DMFile in the Stable layer (in bytes).
- `STABLE_DMFILES_PACKS`: The number of Packs in the DMFile in the Stable layer.
- `TIFLASH_INSTANCE`: The address of the TiFlash instance.
