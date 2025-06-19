---
title: TIKV_REGION_STATUS
summary: 了解 `TIKV_REGION_STATUS` information_schema 表。
---

# TIKV_REGION_STATUS

`TIKV_REGION_STATUS` 表通过 PD 的 API 显示了 TiKV Region 的一些基本信息，如 Region ID、起始和结束键值、读写流量等。

> **注意：**
>
> 此表在 [TiDB Cloud Serverless](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-serverless) 集群上不可用。

```sql
USE INFORMATION_SCHEMA;
DESC TIKV_REGION_STATUS;
```

输出结果如下：

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
| IS_PARTITION              | tinyint(1)  | NO   |      | 0       |       |
| PARTITION_ID              | bigint(21)  | YES  |      | NULL    |       |
| PARTITION_NAME            | varchar(64) | YES  |      | NULL    |       |
| EPOCH_CONF_VER            | bigint(21)  | YES  |      | NULL    |       |
| EPOCH_VERSION             | bigint(21)  | YES  |      | NULL    |       |
| WRITTEN_BYTES             | bigint(21)  | YES  |      | NULL    |       |
| READ_BYTES                | bigint(21)  | YES  |      | NULL    |       |
| APPROXIMATE_SIZE          | bigint(21)  | YES  |      | NULL    |       |
| APPROXIMATE_KEYS          | bigint(21)  | YES  |      | NULL    |       |
| REPLICATIONSTATUS_STATE   | varchar(64) | YES  |      | NULL    |       |
| REPLICATIONSTATUS_STATEID | bigint(21)  | YES  |      | NULL    |       |
+---------------------------+-------------+------+------+---------+-------+
20 rows in set (0.00 sec)
```

`TIKV_REGION_STATUS` 表中各列的描述如下：

* `REGION_ID`：Region 的 ID。
* `START_KEY`：Region 的起始键值。
* `END_KEY`：Region 的结束键值。
* `TABLE_ID`：Region 所属表的 ID。
* `DB_NAME`：`TABLE_ID` 所属的数据库名称。
* `TABLE_NAME`：Region 所属的表名。
* `IS_INDEX`：Region 数据是否为索引。0 表示不是索引，1 表示是索引。如果当前 Region 同时包含表数据和索引数据，将会有多行记录，`IS_INDEX` 分别为 0 和 1。
* `INDEX_ID`：Region 所属索引的 ID。如果 `IS_INDEX` 为 0，则该列值为 NULL。
* `INDEX_NAME`：Region 所属索引的名称。如果 `IS_INDEX` 为 0，则该列值为 NULL。
* `IS_PARTITION`：Region 所属的表是否为分区表。
* `PARTITION_ID`：如果 Region 所属的表是分区表，该列显示 Region 所属分区的 ID。
* `PARTITION_NAME`：如果 Region 所属的表是分区表，该列显示 Region 所属分区的名称。
* `EPOCH_CONF_VER`：Region 配置的版本号。当添加或删除节点时，版本号会增加。
* `EPOCH_VERSION`：Region 的当前版本号。当 Region 发生分裂或合并时，版本号会增加。
* `WRITTEN_BYTES`：写入 Region 的数据量（字节）。
* `READ_BYTES`：从 Region 读取的数据量（字节）。
* `APPROXIMATE_SIZE`：Region 的近似数据大小（MB）。
* `APPROXIMATE_KEYS`：Region 中近似的键数量。
* `REPLICATIONSTATUS_STATE`：Region 当前的复制状态。状态可能为 `UNKNOWN`、`SIMPLE_MAJORITY` 或 `INTEGRITY_OVER_LABEL`。
* `REPLICATIONSTATUS_STATEID`：与 `REPLICATIONSTATUS_STATE` 对应的标识符。

此外，你可以通过对 `EPOCH_CONF_VER`、`WRITTEN_BYTES` 和 `READ_BYTES` 列执行 `ORDER BY X LIMIT Y` 操作来实现 pd-ctl 中的 `top confver`、`top read` 和 `top write` 操作。

你可以使用以下 SQL 语句查询写入数据最多的前 3 个 Region：

```sql
SELECT * FROM tikv_region_status ORDER BY written_bytes DESC LIMIT 3;
```
