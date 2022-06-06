---
title: TIKV_REGION_STATUS
summary: 了解 information_schema 表 `TIKV_REGION_STATUS`。
---

# TIKV_REGION_STATUS

`TIKV_REGION_STATUS` 表通过 PD 的 API 展示 TiKV Region 的基本信息，比如 Region ID、开始和结束键值以及读写流量。

{{< copyable "sql" >}}

```sql
USE information_schema;
DESC tikv_region_status;
```

```sql
+---------------------------+-------------+------+------+---------+-------+
| Field                     | Type        | Null | Key  | Default | Extra |
+---------------------------+-------------+------+------+---------+-------+
| REGION_ID                 | bigint(21)  | YES  |      | NULL    |       |
| START_KEY                 | text        | YES  |      | NULL    |       |
| END_KEY                   | text        | YES  |      | NULL    |       |
| TABLE_ID                  | bigint(21)  | YES  |      | NULL    |       |
| DB_NAME                   | varchar(64) | YES  |      | NULL    |       |
| TABLE_NAME                | varchar(64) | YES  |      | NULL    |       |
| IS_INDEX                  | tinyint(1)  | NO   |      | 0       |       |
| INDEX_ID                  | bigint(21)  | YES  |      | NULL    |       |
| INDEX_NAME                | varchar(64) | YES  |      | NULL    |       |
| EPOCH_CONF_VER            | bigint(21)  | YES  |      | NULL    |       |
| EPOCH_VERSION             | bigint(21)  | YES  |      | NULL    |       |
| WRITTEN_BYTES             | bigint(21)  | YES  |      | NULL    |       |
| READ_BYTES                | bigint(21)  | YES  |      | NULL    |       |
| APPROXIMATE_SIZE          | bigint(21)  | YES  |      | NULL    |       |
| APPROXIMATE_KEYS          | bigint(21)  | YES  |      | NULL    |       |
| REPLICATIONSTATUS_STATE   | varchar(64) | YES  |      | NULL    |       |
| REPLICATIONSTATUS_STATEID | bigint(21)  | YES  |      | NULL    |       |
+---------------------------+-------------+------+------+---------+-------+
17 rows in set (0.00 sec)
```

`TIKV_REGION_STATUS` 表中列的含义如下：

* `REGION_ID`：Region 的 ID。
* `START_KEY`：Region 的起始 key 的值。
* `END_KEY`：Region 的末尾 key 的值。
* `TABLE_ID`：Region 所属的表的 ID。
* `DB_NAME`：`TABLE_ID` 所属的数据库的名称。
* `TABLE_NAME`：Region 所属的表的名称。
* `IS_INDEX`：Region 数据是否是索引，0 代表不是索引，1 代表是索引。如果当前 Region 同时包含表数据和索引数据，会有多行记录，`IS_INDEX` 分别是 0 和 1。
* `INDEX_ID`：Region 所属的索引的 ID。如果 `IS_INDEX` 为 0，这一列的值就为 NULL。
* `INDEX_NAME`：Region 所属的索引的名称。如果 `IS_INDEX` 为 0，这一列的值就为 NULL。
* `EPOCH_CONF_VER`：Region 的配置的版本号，在增加或减少 peer 时版本号会递增。
* `EPOCH_VERSION`：Region 的当前版本号，在分裂或合并时版本号会递增。
* `WRITTEN_BYTES`：已经往 Region 写入的数据量 (bytes)。
* `READ_BYTES`：已经从 Region 读取的数据量 (bytes)。
* `APPROXIMATE_SIZE`：Region 的近似数据量 (MB)。
* `APPROXIMATE_KEYS`：Region 中 key 的近似数量。
* `REPLICATIONSTATUS_STATE`：Region 当前的同步状态，可能为 `UNKNOWN` / `SIMPLE_MAJORITY` / `INTEGRITY_OVER_LABEL` 其中一种状态。
* `REPLICATIONSTATUS_STATEID`：`REPLICATIONSTATUS_STATE` 对应的标识符。

通过在 `EPOCH_CONF_VER`、`WRITTEN_BYTES` 和 `READ_BYTES` 列上执行 `ORDER BY X LIMIT Y` 操作，你可以在 pd-ctl 中实现 `top confver`、`top read` 和 `top write` 操作。

你可以使用以下 SQL 语句查询写入数据最多的前 3 个 Region：

{{< copyable "sql" >}}

```sql
SELECT * FROM tikv_region_status ORDER BY written_bytes DESC LIMIT 3;
```
