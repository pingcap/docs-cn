---
title: TIFLASH_REPLICA
summary: Learn the `TIFLASH_REPLICA` INFORMATION_SCHEMA table.
---

# TIFLASH_REPLICA

The `TIFLASH_REPLICA` table provides information about TiFlash replicas available.

```sql
USE INFORMATION_SCHEMA;
DESC TIFLASH_REPLICA;
```

The output is as follows:

```sql
+-----------------+-------------+------+------+---------+-------+
| Field           | Type        | Null | Key  | Default | Extra |
+-----------------+-------------+------+------+---------+-------+
| TABLE_SCHEMA    | varchar(64) | YES  |      | NULL    |       |
| TABLE_NAME      | varchar(64) | YES  |      | NULL    |       |
| TABLE_ID        | bigint(21)  | YES  |      | NULL    |       |
| REPLICA_COUNT   | bigint(64)  | YES  |      | NULL    |       |
| LOCATION_LABELS | varchar(64) | YES  |      | NULL    |       |
| AVAILABLE       | tinyint(1)  | YES  |      | NULL    |       |
| PROGRESS        | double      | YES  |      | NULL    |       |
+-----------------+-------------+------+------+---------+-------+
7 rows in set (0.01 sec)
```

Fields in the `TIFLASH_REPLICA` table are described as follows:

- `TABLE_SCHEMA`: the name of the database to which the table belongs.
- `TABLE_NAME`: the name of the table.
- `TABLE_ID`: the internal ID of the table, which is unique within a TiDB cluster.
- `REPLICA_COUNT`: the number of TiFlash replicas.
- `LOCATION_LABELS`: the LocationLabelList that is set when a TiFlash replica is created.
- `AVAILABLE`: indicates whether the TiFlash replica of the table is available. When the value is `1` (available), the TiDB optimizer can intelligently choose to push down queries to TiKV or TiFlash based on query cost. When the value is `0` (unavailable), TiDB will not push down queries to TiFlash. Once the value of this field becomes `1` (available), it will not change anymore.
- `PROGRESS`: the replication progress of TiFlash replicas, with the accuracy to two decimal places and at the minute level. The scope of this field is `[0, 1]`. When the `AVAILABLE` field is `1` and `PROGRESS` is less than 1, the TiFlash replica is far behind TiKV, and the queries pushed down to TiFlash will probably fail due to timeout of waiting for data replication.
