---
title: Metrics Schema
category: reference
---

# Metrics Schema

为了能够动态地观察并对比不同时间段的集群情况，TiDB 4.0 诊断系统添加了集群监控系统表。所有表都在 `metrics_schema` 中，可以通过 SQL 的方式查询监控。SQL 查询监控的优点在于用户可以对整个集群的所有监控进行关联查询，并对比不同时间段的结果，迅速找出性能瓶颈。由于目前添加的系统表数量较多，用户可以通过 `information_schema.metrics_tables` 查询这些表的相关信息。

## `tidb_query_duration` 表

系统表数量较多，这里挑出比较典型的 `tidb_query_duration` 表来作为示例。

`tidb_query_duration` 的表结构如下。从表的 `COMMENT` 中可以看出，这个表的是用来查询 TiDB query 执行的百分位时间，如 P999/P99/P90 的查询耗时，单位是秒。

{{< copyable "sql" >}}

```sql
show create table tidb_query_duration;
```

```
+---------------------+--------------------------------------------------------------------------------------------------------------------+
| Table               | Create Table                                                                                                       |
+---------------------+--------------------------------------------------------------------------------------------------------------------+
| tidb_query_duration | CREATE TABLE `tidb_query_duration` (                                                                               |
|                     |   `time` datetime unsigned DEFAULT NULL,                                                                           |
|                     |   `instance` varchar(512) DEFAULT NULL,                                                                            |
|                     |   `sql_type` varchar(512) DEFAULT NULL,                                                                            |
|                     |   `quantile` double unsigned DEFAULT NULL,                                                                         |
|                     |   `value` double unsigned DEFAULT NULL                                                                             |
|                     | ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin COMMENT='The quantile of TiDB query durations(second)' |
+---------------------+--------------------------------------------------------------------------------------------------------------------+
```

比如 `tikv_admin_apply` 有三个 label，对应的表也会有三个额外的列。

{{< copyable "sql" >}}

```sql
desc metrics_schema.tikv_admin_apply;
```

```
+----------+-------------------+------+------+---------+-------+
| Field    | Type              | Null | Key  | Default | Extra |
+----------+-------------------+------+------+---------+-------+
| time     | datetime unsigned | YES  |      | NULL    |       |
| instance | varchar(512)      | YES  |      | NULL    |       |
| type     | varchar(512)      | YES  |      | NULL    |       |
| status   | varchar(512)      | YES  |      | NULL    |       |
| value    | double unsigned   | YES  |      | NULL    |       |
+----------+-------------------+------+------+---------+-------+
5 rows in set (0.00 sec)
```

下面是查询当前时间的 P90 的 TiDB Query 耗时，可以看出，`Select` Query 类型的 P90 耗时是 0.0384 秒，`internal` 类型的 P90 耗时是 0.00327。`instance` 字段是 TiDB 示例的地址。

{{< copyable "sql" >}}

```sql
metrics_schema> select * from tidb_query_duration where value is not null and time=now() and quantile=0.90;
```

```
+---------------------+-------------------+----------+----------+------------------+
| time                | instance          | sql_type | quantile | value            |
+---------------------+-------------------+----------+----------+------------------+
| 2020-03-08 13:34:40 | 172.16.5.40:10089 | Select   | 0.9      | 0.0384           |
| 2020-03-08 13:34:40 | 172.16.5.40:10089 | internal | 0.9      | 0.00327692307692 |
+---------------------+-------------------+----------+----------+------------------+
```

监控表 session 变量：

* `tidb_metric_query_step`：查询的分辨率步长。从 Prometheus 的 `query_range` 数据时需要指定 `start`，`end` 和 `step`，其中 `step` 会使用该变量的值。
* `tidb_metric_query_range_duration`：查询监控时，会将 `PROMQL` 中的 `$RANGE_DURATION` 替换成该变量的值，默认值是 60 秒。