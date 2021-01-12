---
title: TIKV_REGION_PEERS
summary: 了解 information_schema 表 `TIKV_REGION_PEERS`。
---

# TIKV_REGION_PEERS

`TIKV_REGION_PEERS` 表提供了 TiKV 中单个 Region 节点的详细信息，比如它是一个 learner 还是一个 leader。

{{< copyable "sql" >}}

```sql
USE information_schema;
DESC tikv_region_peers;
```

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

例如，使用以下 SQL 语句，你可以查询 `WRITTEN_BYTES` 最大的前 3 个 Region 所在的 TiKV 地址：

```sql
SELECT
 address,
 tikv.address,
 region.region_id
FROM
 tikv_store_status tikv,
 tikv_region_peers peer,
 (SELECT * FROM tikv_region_status ORDER BY written_bytes DESC LIMIT 3) region
WHERE
  region.region_id = peer.region_id
 AND peer.is_leader = 1
 AND peer.store_id = tikv.store_id;
```

`TIKV_REGION_PEERS` 表各列含义如下：

* REGION_ID：REGION 的 ID。
* PEER_ID：REGION 中对应的副本 PEER 的 ID。
* STORE_ID：REGION 所在 TiKV Store 的 ID。
* IS_LEARNER：PEER 是否是 LEARNER。
* IS_LEADER：PEER 是否是 LEADER。
* STATUS：PEER 的状态，一共有 3 种状态：
    * PENDING：暂时不可用状态。
    * DOWN：下线转态，该 PEER 不再提供服务。
    * NORMAL: 正常状态。
* DOWN_SECONDS：处于下线状态的时间，单位是秒。
