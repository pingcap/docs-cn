---
title: TIKV_STORE_STATUS
summary: 了解 INFORMATION_SCHEMA 表 `TIKV_STORE_STATUS`。
---

# TIKV_STORE_STATUS

`TIKV_STORE_STATUS` 表通过 PD 的 API 显示了 TiKV 节点的一些基本信息，例如在集群中分配的 ID、地址和端口、状态、容量以及当前节点的 Region leader 的数量。

```sql
USE INFORMATION_SCHEMA;
DESC TIKV_STORE_STATUS;
```

输出结果如下：

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

`TIKV_STORE_STATUS` 表中列的含义如下：

* `STORE_ID`：Store 的 ID。
* `ADDRESS`：Store 的地址。
* `STORE_STATE`：Store 状态的标识符，与 `STORE_STATE_NAME` 相对应。
* `STORE_STATE_NAME`：Store 状态的名字，为 `Up`、`Offline`、`Tombstone` 中的一种。
* `LABEL`：给 Store 设置的标签。
* `VERSION`：Store 的版本号。
* `CAPACITY`：Store 的存储容量。
* `AVAILABLE`：Store 的剩余存储空间。
* `LEADER_COUNT`：Store 上的 leader 的数量。
* `LEADER_WEIGHT`：Store 的 leader 权重。
* `LEADER_SCORE`：Store 的 leader 评分。
* `LEADER_SIZE`：Store 上的所有 leader 的近似总数据量 (MB)。
* `REGION_COUNT`：Store 上的 Region 总数。
* `REGION_WEIGHT`：Store 的 Region 权重。
* `REGION_SCORE`：Store 的 Region 评分。
* `REGION_SIZE`：Store 上的所有 Region 的近似总数据量 (MB)。
* `START_TS`：Store 启动时的时间戳。
* `LAST_HEARTBEAT_TS`：Store 上次发出心跳的时间戳。
* `UPTIME`：Store 启动以来的总时间。
