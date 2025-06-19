---
title: TABLE_STORAGE_STATS
summary: 了解 `TABLE_STORAGE_STATS` INFORMATION_SCHEMA 表。
---

# TABLE_STORAGE_STATS

`TABLE_STORAGE_STATS` 表提供了存储引擎（TiKV）中表大小的相关信息。

```sql
USE INFORMATION_SCHEMA;
DESC TABLE_STORAGE_STATS;
```

输出结果如下：

```sql
+--------------------+-------------+------+------+---------+-------+
| Field              | Type        | Null | Key  | Default | Extra |
+--------------------+-------------+------+------+---------+-------+
| TABLE_SCHEMA       | varchar(64) | YES  |      | NULL    |       |
| TABLE_NAME         | varchar(64) | YES  |      | NULL    |       |
| TABLE_ID           | bigint(21)  | YES  |      | NULL    |       |
| PEER_COUNT         | bigint(21)  | YES  |      | NULL    |       |
| REGION_COUNT       | bigint(21)  | YES  |      | NULL    |       |
| EMPTY_REGION_COUNT | bigint(21)  | YES  |      | NULL    |       |
| TABLE_SIZE         | bigint(64)  | YES  |      | NULL    |       |
| TABLE_KEYS         | bigint(64)  | YES  |      | NULL    |       |
+--------------------+-------------+------+------+---------+-------+
8 rows in set (0.00 sec)
```

```sql
CREATE TABLE test.t1 (id INT);
INSERT INTO test.t1 VALUES (1);
SELECT * FROM TABLE_STORAGE_STATS WHERE table_schema = 'test' AND table_name = 't1'\G
```

输出结果如下：

```sql
*************************** 1. row ***************************
      TABLE_SCHEMA: test
        TABLE_NAME: t1
          TABLE_ID: 56
        PEER_COUNT: 1
      REGION_COUNT: 1
EMPTY_REGION_COUNT: 1
        TABLE_SIZE: 1
        TABLE_KEYS: 0
1 row in set (0.00 sec)
```

`TABLE_STORAGE_STATS` 表中的字段说明如下：

* `TABLE_SCHEMA`：表所属的 schema 名称。
* `TABLE_NAME`：表名。
* `TABLE_ID`：表的 ID。
* `PEER_COUNT`：表的副本数量。
* `REGION_COUNT`：Region 的数量。
* `EMPTY_REGION_COUNT`：此表中不包含数据的 Region 数量。
* `TABLE_SIZE`：表的总大小，单位为 MiB。
* `TABLE_KEYS`：表中的总记录数。
