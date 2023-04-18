---
title: TIFLASH_REPLICA
summary: 了解 INFORMATION_SCHEMA 表 `TIFLASH_REPLICA`。
---

# TIFLASH_REPLICA

`TIFLASH_REPLICA` 表提供了有关可用的 TiFlash 副本的信息。

```sql
USE INFORMATION_SCHEMA;
DESC TIFLASH_REPLICA;
```

输出结果如下：

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

`TIFLASH_REPLICA` 表中各列的字段含义如下：

- `TABLE_SCHEMA`：表所属的数据库的名称。
- `TABLE_NAME`：表的名称。
- `TABLE_ID`：表的内部 ID，该 ID 在一个 TiDB 集群内部唯一。
- `REPLICA_COUNT`：TiFlash 副本数。
- `LOCATION_LABELS`：设置 TiFlash 副本时设置的 LocationLabelList。
- `AVAILABLE`：表的 TiFlash 副本是否可用。`1` 代表可用，TiDB 优化器将依据查询代价智能选择下推查询到 TiKV 或 TiFlash；`0` 代表不可用，TiDB 将不会下推查询到 TiFlash。副本状态变为可用之后就不再改变。
- `PROGRESS`：TiFlash 副本同步进度，范围是 `[0, 1]`，精确到小数点后两位，刷新的精度为分钟级。当 `AVAILABLE` 字段为 1 时，如果 `PROGRESS` 小于 1，表示 TiFlash 副本落后 TiKV 较多，下推到 TiFlash 的查询很可能会因为等待数据同步超时而失败。
