---
title: METRICS_TABLES
summary: 了解 TiDB 系统表 `METRICS_TABLES`。
---

# METRICS_TABLES

`METRICS_TABLES` 表为 [metrics_schema](/metrics-schema.md) 数据库中的每个视图提供 PromQL（Prometheus 查询语言）定义。

{{< copyable "sql" >}}

```sql
USE information_schema;
DESC metrics_tables;
```

```sql
+------------+--------------+------+------+---------+-------+
| Field      | Type         | Null | Key  | Default | Extra |
+------------+--------------+------+------+---------+-------+
| TABLE_NAME | varchar(64)  | YES  |      | NULL    |       |
| PROMQL     | varchar(64)  | YES  |      | NULL    |       |
| LABELS     | varchar(64)  | YES  |      | NULL    |       |
| QUANTILE   | double       | YES  |      | NULL    |       |
| COMMENT    | varchar(256) | YES  |      | NULL    |       |
+------------+--------------+------+------+---------+-------+
```

表 `metrics_tables` 的字段解释：

* `TABLE_NAME`：对应于 `metrics_schema` 中的表名。
* `PROMQL`：监控表的主要原理是将 SQL 映射成 `PromQL`，并将 Prometheus 结果转换成 SQL 查询结果。这个字段是 `PromQL` 的表达式模板，查询监控表数据时使用查询条件改写模板中的变量，生成最终的查询表达式。
* `LABELS`：监控定义的 label，每一个 label 对应监控表中的一列。SQL 中如果包含对应列的过滤，对应的 `PromQL` 也会改变。
* `QUANTILE`：百分位。对于直方图类型的监控数据，指定一个默认百分位。如果值为 `0`，表示该监控表对应的监控不是直方图。
* `COMMENT`：对这个监控表的注释。

{{< copyable "sql" >}}

```sql
SELECT * FROM metrics_tables LIMIT 5\G
```

```sql
*************************** 1. row ***************************
TABLE_NAME: abnormal_stores
    PROMQL: sum(pd_cluster_status{ type=~"store_disconnected_count|store_unhealth_count|store_low_space_count|store_down_count|store_offline_count|store_tombstone_count"})
    LABELS: instance,type
  QUANTILE: 0
   COMMENT: 
*************************** 2. row ***************************
TABLE_NAME: etcd_disk_wal_fsync_rate
    PROMQL: delta(etcd_disk_wal_fsync_duration_seconds_count{$LABEL_CONDITIONS}[$RANGE_DURATION])
    LABELS: instance
  QUANTILE: 0
   COMMENT: The rate of writing WAL into the persistent storage
*************************** 3. row ***************************
TABLE_NAME: etcd_wal_fsync_duration
    PROMQL: histogram_quantile($QUANTILE, sum(rate(etcd_disk_wal_fsync_duration_seconds_bucket{$LABEL_CONDITIONS}[$RANGE_DURATION])) by (le,instance))
    LABELS: instance
  QUANTILE: 0.99
   COMMENT: The quantile time consumed of writing WAL into the persistent storage
*************************** 4. row ***************************
TABLE_NAME: etcd_wal_fsync_total_count
    PROMQL: sum(increase(etcd_disk_wal_fsync_duration_seconds_count{$LABEL_CONDITIONS}[$RANGE_DURATION])) by (instance)
    LABELS: instance
  QUANTILE: 0
   COMMENT: The total count of writing WAL into the persistent storage
*************************** 5. row ***************************
TABLE_NAME: etcd_wal_fsync_total_time
    PROMQL: sum(increase(etcd_disk_wal_fsync_duration_seconds_sum{$LABEL_CONDITIONS}[$RANGE_DURATION])) by (instance)
    LABELS: instance
  QUANTILE: 0
   COMMENT: The total time of writing WAL into the persistent storage
5 rows in set (0.00 sec)
```
