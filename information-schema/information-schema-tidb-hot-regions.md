---
title: TIDB_HOT_REGIONS
summary: 了解 information_schema 表 `TIDB_HOT_REGIONS`。
---

# TIDB_HOT_REGIONS

`TIDB_HOT_REGIONS` 表提供了关于热点 Region 的相关信息。

{{< copyable "sql" >}}

```sql
USE information_schema;
DESC tidb_hot_regions;
```

```sql
+----------------+-------------+------+------+---------+-------+
| Field          | Type        | Null | Key  | Default | Extra |
+----------------+-------------+------+------+---------+-------+
| TABLE_ID       | bigint(21)  | YES  |      | NULL    |       |
| INDEX_ID       | bigint(21)  | YES  |      | NULL    |       |
| DB_NAME        | varchar(64) | YES  |      | NULL    |       |
| TABLE_NAME     | varchar(64) | YES  |      | NULL    |       |
| INDEX_NAME     | varchar(64) | YES  |      | NULL    |       |
| REGION_ID      | bigint(21)  | YES  |      | NULL    |       |
| TYPE           | varchar(64) | YES  |      | NULL    |       |
| MAX_HOT_DEGREE | bigint(21)  | YES  |      | NULL    |       |
| REGION_COUNT   | bigint(21)  | YES  |      | NULL    |       |
| FLOW_BYTES     | bigint(21)  | YES  |      | NULL    |       |
+----------------+-------------+------+------+---------+-------+
10 rows in set (0.00 sec)
```

`TIDB_HOT_REGIONS` 表各列字段含义如下：

* TABLE_ID：热点 Region 所在表的 ID。
* INDEX_ID：热点 Region 所在索引的 ID。
* DB_NAME：热点 Region 所在数据库对象的数据库名。
* TABLE_NAME：热点 Region 所在表的名称。
* INDEX_NAME：热点 Region 所在索引的名称。
* REGION_ID：热点 Region 的 ID。
* TYPE：热点 Region 的类型。
* MAX_HOT_DEGREE：该 Region 的最大热度。
* REGION_COUNT：所在实例的 Region 数量。
* FLOW_BYTES：该 Region 内读写的字节数量。
