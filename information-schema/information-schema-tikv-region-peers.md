---
title: TIKV_REGION_PEERS
summary: Learn the `TIKV_REGION_PEERS` INFORMATION_SCHEMA table.
---

# TIKV_REGION_PEERS

The `TIKV_REGION_PEERS` table shows detailed information of a single Region node in TiKV, such as whether it is a learner or leader.

```sql
USE INFORMATION_SCHEMA;
DESC TIKV_REGION_PEERS;
```

The output is as follows:

```sql
+--------------+-------------+------+------+---------+-------+
| Field        | Type        | Null | Key  | Default | Extra |
+--------------+-------------+------+------+---------+-------+
| REGION_ID    | bigint(21)  | YES  |      | NULL    |       |
| PEER_ID      | bigint(21)  | YES  |      | NULL    |       |
| STORE_ID     | bigint(21)  | YES  |      | NULL    |       |
| IS_LEARNER   | tinyint(1)  | NO   |      | 0       |       |
| IS_LEADER    | tinyint(1)  | NO   |      | 0       |       |
| STATUS       | varchar(10) | YES  |      | 0       |       |
| DOWN_SECONDS | bigint(21)  | YES  |      | 0       |       |
+--------------+-------------+------+------+---------+-------+
7 rows in set (0.01 sec)
```

For example, you can query the specific TiKV addresses for the top 3 Regions with the maximum value of `WRITTEN_BYTES` using the following SQL statement:

```sql
SELECT
  address,
  tikv.address,
  region.region_id
FROM
  TIKV_STORE_STATUS tikv,
  TIKV_REGION_PEERS peer,
  (SELECT * FROM tikv_region_status ORDER BY written_bytes DESC LIMIT 3) region
WHERE
  region.region_id = peer.region_id
  AND peer.is_leader = 1
  AND peer.store_id = tikv.store_id;
```

Fields in the `TIKV_REGION_PEERS` table are described as follows:

* REGION_ID: The Region ID.
* PEER_ID: The ID of the Region peer.
* STORE_ID: The ID of the TiKV store where the Region is located.
* IS_LEARNER: Whether the peer is learner.
* IS_LEADER: Whether the peer is leader.
* STATUS: The statuses of a peer:
    * PENDING: Temporarily unavailable.
    * DOWN: Offline and converted. This peer no longer provides service.
    * NORMAL: Running normally.
* DOWN_SECONDS: The duration of being offline, in seconds.
