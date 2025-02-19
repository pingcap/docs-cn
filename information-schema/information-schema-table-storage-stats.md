---
title: TABLE_STORAGE_STATS
summary: 了解 INFORMATION_SCHEMA 表 `TABLE_STORAGE_STATS`。
---

# TABLE_STORAGE_STATS

`TABLE_STORAGE_STATS` 表提供有关由存储引擎 (TiKV) 存储的表大小的信息。

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

`TABLE_STORAGE_STATS` 表各列字段含义如下：

* `TABLE_SCHEMA`：表所在 schema 名字
* `TABLE_NAME`：表名
* `TABLE_ID`：表 ID
* `PEER_COUNT`：副本个数
* `REGION_COUNT`：表所在的 Region 个数
* `EMPTY_REGION_COUNT`：没有该表数据的 Region 个数
* `TABLE_SIZE`：数据量大小，单位 MiB
* `TABLE_KEYS`：表记录个数
