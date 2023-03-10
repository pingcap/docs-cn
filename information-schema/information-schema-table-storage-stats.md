---
title: TABLE_STORAGE_STATS
summary: Learn the `TABLE_STORAGE_STATS` INFORMATION_SCHEMA table.
---

# TABLE_STORAGE_STATS

The `TABLE_STORAGE_STATS` table provides information about table sizes as stored by the storage engine (TiKV).

```sql
USE INFORMATION_SCHEMA;
DESC TABLE_STORAGE_STATS;
```

The output is as follows:

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

The output is as follows:

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

Fields in the `TABLE_STORAGE_STATS` table are described as follows:

* `TABLE_SCHEMA`: The name of the schema to which the table belongs.
* `TABLE_NAME`: The name of the table.
* `TABLE_ID`: The ID of the table.
* `PEER_COUNT`: The number of replicas of the table.
* `REGION_COUNT`: The number of Regions.
* `EMPTY_REGION_COUNT`: The number of Regions that do not contain data in this table.
* `TABLE_SIZE`: The total size of the table, in the unit of MiB.
* `TABLE_KEYS`: The total number of records in the table.
