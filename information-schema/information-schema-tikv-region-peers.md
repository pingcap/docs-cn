---
title: TIKV_REGION_PEERS
summary: 了解 `TIKV_REGION_PEERS` INFORMATION_SCHEMA 表。
---

# TIKV_REGION_PEERS

`TIKV_REGION_PEERS` 表显示了 TiKV 中单个 Region 节点的详细信息，例如它是否是 learner 或 leader。

> **注意：**
>
> 此表在 [TiDB Cloud Serverless](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-serverless) 集群上不可用。

```sql
USE INFORMATION_SCHEMA;
DESC TIKV_REGION_PEERS;
```

输出如下：

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

例如，你可以使用以下 SQL 语句查询 `WRITTEN_BYTES` 值最大的前 3 个 Region 对应的具体 TiKV 地址：

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

`TIKV_REGION_PEERS` 表中的字段说明如下：

* REGION_ID：Region 的 ID。
* PEER_ID：Region peer 的 ID。
* STORE_ID：Region 所在 TiKV store 的 ID。
* IS_LEARNER：peer 是否为 learner。
* IS_LEADER：peer 是否为 leader。
* STATUS：peer 的状态：
    * PENDING：暂时不可用。
    * DOWN：离线且已转换。该 peer 不再提供服务。
    * NORMAL：正常运行。
* DOWN_SECONDS：离线持续时间，单位为秒。
