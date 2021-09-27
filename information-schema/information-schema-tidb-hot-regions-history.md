---
title: TIDB_HOT_REGIONS_HISTORY
summary: 了解 information_schema 表 `TIDB_HOT_REGIONS_HISTORY`。
---

# TIDB_HOT_REGIONS_HISTORY

`TIDB_HOT_REGIONS_HISTORY` 表提供了关于历史热点 Region 的相关信息, 这些信息由PD定期存储在本地，存储间隔为 [`hot-regions-write-interval`](/pd-configuration-file.md#hot-regions-write-interval)的值（默认值为10m)，历史热点信息保持的期限为[`hot-regions-reserved-days`](/pd-configuration-file.md#hot-regions-write-interval)的值（默认值为7days），详情参见[PD 配置文件描述](/pd-configuration-file.md#hot-regions-write-interval)。

```sql
USE information_schema;
DESC tidb_hot_regions_history;
```

```sql
+-------------+--------------+------+------+---------+-------+
| Field       | Type         | Null | Key  | Default | Extra |
+-------------+--------------+------+------+---------+-------+
| UPDATE_TIME | timestamp(6) | YES  |      | NULL    |       |
| DB_NAME     | varchar(64)  | YES  |      | NULL    |       |
| TABLE_NAME  | varchar(64)  | YES  |      | NULL    |       |
| TABLE_ID    | bigint(21)   | YES  |      | NULL    |       |
| INDEX_NAME  | varchar(64)  | YES  |      | NULL    |       |
| INDEX_ID    | bigint(21)   | YES  |      | NULL    |       |
| REGION_ID   | bigint(21)   | YES  |      | NULL    |       |
| STORE_ID    | bigint(21)   | YES  |      | NULL    |       |
| PEER_ID     | bigint(21)   | YES  |      | NULL    |       |
| IS_LEARNER  | tinyint(1)   | NO   |      | 0       |       |
| IS_LEADER   | tinyint(1)   | NO   |      | 0       |       |
| TYPE        | varchar(64)  | YES  |      | NULL    |       |
| HOT_DEGREE  | bigint(21)   | YES  |      | NULL    |       |
| FLOW_BYTES  | double       | YES  |      | NULL    |       |
| KEY_RATE    | double       | YES  |      | NULL    |       |
| QUERY_RATE  | double       | YES  |      | NULL    |       |
+-------------+--------------+------+------+---------+-------+
16 rows in set (0.00 sec)
```

`TIDB_HOT_REGIONS_HISTORY` 表各列字段含义如下：

* UPDATE_TIME：热点Region更新时间。
* DB_NAME：热点 Region 所在数据库对象的数据库名。
* TABLE_ID：热点 Region 所在表的 ID。
* TABLE_NAME：热点 Region 所在表的名称。
* INDEX_NAME：热点 Region 所在索引的名称。

* INDEX_ID：热点 Region 所在索引的 ID。

* REGION_ID：热点 Region 的 ID。
* STORE_ID：热点Region所在TiKV Store的ID。
* PEER_ID：热点Region对应的副本 Peer 的 ID。
* IS_LEARNER：PEER 是否是 LEARNER。
* IS_LEADER：PEER 是否是 LEADER。

* TYPE：热点 Region 的类型。
* HOT_DEGREE：该 热点Region 的热度。

* FLOW_BYTES：该 Region 内读写的字节数量。
* KEY_RATE：该 Region内读写的key数量。
* QUERY_RATE：该 Region内读写的query数量。

> **注意：**
>
> + TIDB_HOT_REGIONS_HISTORY表的UPDATE_TIME, REGION_ID, STORE_ID, PEER_ID, IS_LEARNER, IS_LEADER, TYPE字段会下推到PD服务器过滤，所以为了降低使用该表的开销，必须指定搜索关键字以及时间范围，然后尽可能地指定更多的条件。例如 `select * from tidb_hot_regions_history where store_id = 11 and update_time > '2020-05-18 20:40:00' and update_time < '2020-05-18 21:40:00' and type='write'`。

下面是一些常见的应用场景：

* 查询一段时间内的所有热点regions，替换update_time即可。

  {{< copyable "sql" >}}

  ```sql
  SELECT * FROM INFORMATION_SCHEMA.TIDB_HOT_REGIONS_HISTORY WHERE update_time >'2021-08-18 21:40:00' and update_time <'2021-09-19 00:00:00';
  ```

* 查询某张表指定时间内的热点regions，替换update_time, table_name 即可。

  {{< copyable "sql" >}}

  ```SQL
  SELECT * FROM INFORMATION_SCHEMA.TIDB_HOT_REGIONS_HISTORY WHERE update_time >'2021-08-18 21:40:00' and update_time <'2021-09-19 00:00:00' and TABLE_NAME = 'table_name';
  ```

* 查询某张表指定时间内热点regions 的分布，替换update_time, table_name 即可。

  {{< copyable "sql" >}}

  ```sql
  SELECT count(region_id) cnt, store_id FROM INFORMATION_SCHEMA.TIDB_HOT_REGIONS_HISTORY WHERE update_time >'2021-08-18 21:40:00' and update_time <'2021-09-19 00:00:00'  and table_name = 'table_name' GROUP BY STORE_ID ORDER BY cnt DESC;
  ```

* 查询某张表指定时间内热点leader regions的分布，替换update_time, table_name 即可。

  {{< copyable "sql" >}}

  ```sql
  SELECT count(region_id) cnt, store_id FROM INFORMATION_SCHEMA.TIDB_HOT_REGIONS_HISTORY WHERE update_time >'2021-08-18 21:40:00' and update_time <'2021-09-19 00:00:00'  and table_name = 'table_name' and is_leader=1 GROUP BY STORE_ID ORDER BY cnt DESC;
  ```

* 查询某张表指定时间内热点index regions的分布，替换update_time, table_name 即可。

  {{< copyable "sql" >}}

  ```sql
  SELECT count(region_id) cnt, index_name, store_id FROM INFORMATION_SCHEMA.TIDB_HOT_REGIONS_HISTORY WHERE update_time >'2021-08-18 21:40:00' and update_time <'2021-09-19 00:00:00' and table_name = 'table_name' group by index_name, store_id order by index_name,cnt desc;
  ```

* 查询某张表指定时间内热点index leader regions的分布，替换update_time, table_name 即可。

  {{< copyable "sql" >}}

  ```sql
  SELECT count(region_id) cnt, index_name, store_id FROM INFORMATION_SCHEMA.TIDB_HOT_REGIONS_HISTORY WHERE update_time >'2021-08-18 21:40:00' and update_time <'2022-09-19 00:00:00' and table_name = 'table_name' and is_leader=1 group by index_name, store_id order by index_name,cnt desc;
  ```

  
