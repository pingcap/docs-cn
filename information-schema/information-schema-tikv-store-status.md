---
title: TIKV_STORE_STATUS
summary: Learn the `TIKV_STORE_STATUS` INFORMATION_SCHEMA table.
---

# TIKV_STORE_STATUS

The `TIKV_STORE_STATUS` table shows some basic information of TiKV nodes via PD's API, like the ID allocated in the cluster, address and port, and status, capacity, and the number of Region leaders of the current node.

```sql
USE INFORMATION_SCHEMA;
DESC TIKV_STORE_STATUS;
```

The output is as follows:

```sql
+-------------------+-------------+------+------+---------+-------+
| Field             | Type        | Null | Key  | Default | Extra |
+-------------------+-------------+------+------+---------+-------+
| STORE_ID          | bigint(21)  | YES  |      | NULL    |       |
| ADDRESS           | varchar(64) | YES  |      | NULL    |       |
| STORE_STATE       | bigint(21)  | YES  |      | NULL    |       |
| STORE_STATE_NAME  | varchar(64) | YES  |      | NULL    |       |
| LABEL             | json        | YES  |      | NULL    |       |
| VERSION           | varchar(64) | YES  |      | NULL    |       |
| CAPACITY          | varchar(64) | YES  |      | NULL    |       |
| AVAILABLE         | varchar(64) | YES  |      | NULL    |       |
| LEADER_COUNT      | bigint(21)  | YES  |      | NULL    |       |
| LEADER_WEIGHT     | double      | YES  |      | NULL    |       |
| LEADER_SCORE      | double      | YES  |      | NULL    |       |
| LEADER_SIZE       | bigint(21)  | YES  |      | NULL    |       |
| REGION_COUNT      | bigint(21)  | YES  |      | NULL    |       |
| REGION_WEIGHT     | double      | YES  |      | NULL    |       |
| REGION_SCORE      | double      | YES  |      | NULL    |       |
| REGION_SIZE       | bigint(21)  | YES  |      | NULL    |       |
| START_TS          | datetime    | YES  |      | NULL    |       |
| LAST_HEARTBEAT_TS | datetime    | YES  |      | NULL    |       |
| UPTIME            | varchar(64) | YES  |      | NULL    |       |
+-------------------+-------------+------+------+---------+-------+
19 rows in set (0.00 sec)
```

The descriptions of the columns in the `TIKV_STORE_STATUS` table are as follows:

* `STORE_ID`: The ID of the Store.
* `ADDRESS`: The address of the Store.
* `STORE_STATE`: The identifier of the Store state, which corresponds to `STORE_STATE_NAME`.
* `STORE_STATE_NAME`: The name of the Store state. The name is `Up`, `Offline`, or `Tombstone`.
* `LABEL`: The label set for the Store.
* `VERSION`: The version number of the Store.
* `CAPACITY`: The storage capacity of the Store.
* `AVAILABLE`: The remaining storage space of the Store.
* `LEADER_COUNT`: The number of leaders on the Store.
* `LEADER_WEIGHT`: The leader weight of the Store.
* `LEADER_SCORE`: The leader score of the Store.
* `LEADER_SIZE`: The approximate total data size (MB) of all leaders on the Store.
* `REGION_COUNT`: The number of Regions on the Store.
* `REGION_WEIGHT`: The Region weight of the Store.
* `REGION_SCORE`: The Region score of the Store.
* `REGION_SIZE`: The approximate total data size (MB) of all Regions on the Store.
* `START_TS`: The timestamp when the Store is started.
* `LAST_HEARTBEAT_TS`: The timestamp of the last heartbeat sent by the Store.
* `UPTIME`: The total time since the Store starts.
