---
title: TIFLASH_REPLICA
summary: 了解 `TIFLASH_REPLICA` INFORMATION_SCHEMA 表。
---

# TIFLASH_REPLICA

`TIFLASH_REPLICA` 表提供了可用的 TiFlash 副本信息。

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

`TIFLASH_REPLICA` 表中各字段的描述如下：

- `TABLE_SCHEMA`：表所属的数据库名称。
- `TABLE_NAME`：表的名称。
- `TABLE_ID`：表的内部 ID，在 TiDB 集群中是唯一的。
- `REPLICA_COUNT`：TiFlash 副本的数量。
- `LOCATION_LABELS`：创建 TiFlash 副本时设置的 LocationLabelList。
- `AVAILABLE`：表示表的 TiFlash 副本是否可用。当值为 `1`（可用）时，TiDB 优化器可以根据查询成本智能地选择将查询下推到 TiKV 或 TiFlash。当值为 `0`（不可用）时，TiDB 不会将查询下推到 TiFlash。一旦该字段的值变为 `1`（可用），就不会再改变。
- `PROGRESS`：TiFlash 副本的复制进度，精确到小数点后两位，以分钟为单位。该字段的范围是 `[0, 1]`。当 `AVAILABLE` 字段为 `1` 且 `PROGRESS` 小于 1 时，表示 TiFlash 副本远落后于 TiKV，下推到 TiFlash 的查询可能会因等待数据复制超时而失败。
