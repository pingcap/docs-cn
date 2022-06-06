---
title: Metrics Schema
summary: 了解 TiDB `METRICS SCHEMA` 系统数据库。
---

# Metrics Schema

`METRICS_SCHEMA` 是基于 Prometheus 中 TiDB 监控指标的一组视图。每个表的 PromQL（Prometheus 查询语言）的源均可在 [`INFORMATION_SCHEMA.METRICS_TABLES`](/information-schema/information-schema-metrics-tables.md) 表中找到。

{{< copyable "sql" >}}

```sql
use metrics_schema;
SELECT * FROM uptime;
SELECT * FROM information_schema.metrics_tables WHERE table_name='uptime'\G
```

```sql
+----------------------------+-----------------+------------+--------------------+
| time                       | instance        | job        | value              |
+----------------------------+-----------------+------------+--------------------+
| 2020-07-06 15:26:26.203000 | 127.0.0.1:10080 | tidb       | 123.60300016403198 |
| 2020-07-06 15:27:26.203000 | 127.0.0.1:10080 | tidb       | 183.60300016403198 |
| 2020-07-06 15:26:26.203000 | 127.0.0.1:20180 | tikv       | 123.60300016403198 |
| 2020-07-06 15:27:26.203000 | 127.0.0.1:20180 | tikv       | 183.60300016403198 |
| 2020-07-06 15:26:26.203000 | 127.0.0.1:2379  | pd         | 123.60300016403198 |
| 2020-07-06 15:27:26.203000 | 127.0.0.1:2379  | pd         | 183.60300016403198 |
| 2020-07-06 15:26:26.203000 | 127.0.0.1:9090  | prometheus | 123.72300004959106 |
| 2020-07-06 15:27:26.203000 | 127.0.0.1:9090  | prometheus | 183.72300004959106 |
+----------------------------+-----------------+------------+--------------------+
8 rows in set (0.00 sec)
*************************** 1. row ***************************
TABLE_NAME: uptime
    PROMQL: (time() - process_start_time_seconds{$LABEL_CONDITIONS})
    LABELS: instance,job
  QUANTILE: 0
   COMMENT: TiDB uptime since last restart(second)
1 row in set (0.00 sec)
```

{{< copyable "sql" >}}

```sql
show tables;
```

```sql
+---------------------------------------------------+
| Tables_in_metrics_schema                          |
+---------------------------------------------------+
| abnormal_stores                                   |
| etcd_disk_wal_fsync_rate                          |
| etcd_wal_fsync_duration                           |
| etcd_wal_fsync_total_count                        |
| etcd_wal_fsync_total_time                         |
| go_gc_count                                       |
| go_gc_cpu_usage                                   |
| go_gc_duration                                    |
| go_heap_mem_usage                                 |
| go_threads                                        |
| goroutines_count                                  |
| node_cpu_usage                                    |
| node_disk_available_size                          |
| node_disk_io_util                                 |
| node_disk_iops                                    |
| node_disk_read_latency                            |
| node_disk_size                                    |
..
| tikv_storage_async_request_total_time             |
| tikv_storage_async_requests                       |
| tikv_storage_async_requests_total_count           |
| tikv_storage_command_ops                          |
| tikv_store_size                                   |
| tikv_thread_cpu                                   |
| tikv_thread_nonvoluntary_context_switches         |
| tikv_thread_voluntary_context_switches            |
| tikv_threads_io                                   |
| tikv_threads_state                                |
| tikv_total_keys                                   |
| tikv_wal_sync_duration                            |
| tikv_wal_sync_max_duration                        |
| tikv_worker_handled_tasks                         |
| tikv_worker_handled_tasks_total_num               |
| tikv_worker_pending_tasks                         |
| tikv_worker_pending_tasks_total_num               |
| tikv_write_stall_avg_duration                     |
| tikv_write_stall_max_duration                     |
| tikv_write_stall_reason                           |
| up                                                |
| uptime                                            |
+---------------------------------------------------+
626 rows in set (0.00 sec)
```

`METRICS_SCHEMA` 是监控相关的 summary 表的数据源，例如 [`metrics_summary`](/information-schema/information-schema-metrics-summary.md)、[`metrics_summary_by_label`](/information-schema/information-schema-metrics-summary.md) 和 [`inspection_summary`](/information-schema/information-schema-inspection-summary.md)。

## 更多例子

下面以 `metrics_schema` 中的 `tidb_query_duration` 监控表为例，介绍监控表相关的使用和原理，其他的监控表原理均类似。

查询 `information_schema.metrics_tables` 中关于 `tidb_query_duration` 表相关的信息如下：

{{< copyable "sql" >}}

```sql
select * from information_schema.metrics_tables where table_name='tidb_query_duration';
```

```sql
+---------------------+----------------------------------------------------------------------------------------------------------------------------------------------------------+-------------------+----------+----------------------------------------------+
| TABLE_NAME          | PROMQL                                                                                                                                                   | LABELS            | QUANTILE | COMMENT                                      |
+---------------------+----------------------------------------------------------------------------------------------------------------------------------------------------------+-------------------+----------+----------------------------------------------+
| tidb_query_duration | histogram_quantile($QUANTILE, sum(rate(tidb_server_handle_query_duration_seconds_bucket{$LABEL_CONDITIONS}[$RANGE_DURATION])) by (le,sql_type,instance)) | instance,sql_type | 0.9      | The quantile of TiDB query durations(second) |
+---------------------+----------------------------------------------------------------------------------------------------------------------------------------------------------+-------------------+----------+----------------------------------------------+
```

* `TABLE_NAME`：对应于 `metrics_schema` 中的表名，这里表名是 `tidb_query_duration`。
* `PROMQL`：因为监控表的原理是将 SQL 映射成 `PromQL` 后向 Prometheus 请求数据，并将 Prometheus 返回的结果转换成 SQL 查询结果。该字段是 `PromQL` 的表达式模板，查询监控表数据时使用查询条件改写模板中的变量，生成最终的查询表达式。
* `LABELS`：监控项定义的 label，`tidb_query_duration` 有两个 label，分别是 `instance` 和 `sql_type`。
* `QUANTILE`：百分位。直方图类型的监控数据会指定一个默认百分位。如果值为 `0`，表示该监控表对应的监控不是直方图。`tidb_query_duration` 默认查询 0.9 ，也就是 P90 的监控值。
* `COMMENT`：对这个监控表的解释。可以看出 `tidb_query_duration` 表是用来查询 TiDB query 执行的百分位时间，如 P999/P99/P90 的查询耗时，单位是秒。

再来看 `tidb_query_duration` 的表结构：

{{< copyable "sql" >}}

```sql
show create table metrics_schema.tidb_query_duration;
```

```sql
+---------------------+--------------------------------------------------------------------------------------------------------------------+
| Table               | Create Table                                                                                                       |
+---------------------+--------------------------------------------------------------------------------------------------------------------+
| tidb_query_duration | CREATE TABLE `tidb_query_duration` (                                                                               |
|                     |   `time` datetime unsigned DEFAULT CURRENT_TIMESTAMP,                                                              |
|                     |   `instance` varchar(512) DEFAULT NULL,                                                                            |
|                     |   `sql_type` varchar(512) DEFAULT NULL,                                                                            |
|                     |   `quantile` double unsigned DEFAULT '0.9',                                                                        |
|                     |   `value` double unsigned DEFAULT NULL                                                                             |
|                     | ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin COMMENT='The quantile of TiDB query durations(second)' |
+---------------------+--------------------------------------------------------------------------------------------------------------------+
```

* `time`：监控项的时间。
* `instance` 和 `sql_type`：是 `tidb_query_duration` 这个监控项的 label。`instance` 表示监控的地址，`sql_type` 表示执行 SQL 的类似。
* `quantile`，百分位，直方图类型的监控都会有该列，表示查询的百分位时间，如 `quantile=0.9` 就是查询 P90 的时间。
* `value`：监控项的值。

下面是查询时间 [`2020-03-25 23:40:00`, `2020-03-25 23:42:00`] 范围内的 P99 的 TiDB Query 耗时：

{{< copyable "sql" >}}

```sql
select * from metrics_schema.tidb_query_duration where value is not null and time>='2020-03-25 23:40:00' and time <= '2020-03-25 23:42:00' and quantile=0.99;
```

```sql
+---------------------+-------------------+----------+----------+----------------+
| time                | instance          | sql_type | quantile | value          |
+---------------------+-------------------+----------+----------+----------------+
| 2020-03-25 23:40:00 | 172.16.5.40:10089 | Insert   | 0.99     | 0.509929485256 |
| 2020-03-25 23:41:00 | 172.16.5.40:10089 | Insert   | 0.99     | 0.494690793986 |
| 2020-03-25 23:42:00 | 172.16.5.40:10089 | Insert   | 0.99     | 0.493460506934 |
| 2020-03-25 23:40:00 | 172.16.5.40:10089 | Select   | 0.99     | 0.152058493415 |
| 2020-03-25 23:41:00 | 172.16.5.40:10089 | Select   | 0.99     | 0.152193879678 |
| 2020-03-25 23:42:00 | 172.16.5.40:10089 | Select   | 0.99     | 0.140498483232 |
| 2020-03-25 23:40:00 | 172.16.5.40:10089 | internal | 0.99     | 0.47104        |
| 2020-03-25 23:41:00 | 172.16.5.40:10089 | internal | 0.99     | 0.11776        |
| 2020-03-25 23:42:00 | 172.16.5.40:10089 | internal | 0.99     | 0.11776        |
+---------------------+-------------------+----------+----------+----------------+
```

以上查询结果的第一行意思是，在 `2020-03-25 23:40:00` 时，在 TiDB 实例 `172.16.5.40:10089` 上，`Insert` 类型的语句的 P99 执行时间是 0.509929485256 秒。其他各行的含义类似，`sql_type` 列的其他值含义如下：

* `Select`：表示执行的 `select` 类型的语句。
* `internal`：表示 TiDB 的内部 SQL 语句，一般是统计信息更新，获取全局变量相关的内部语句。

进一步再查看上面语句的执行计划如下：

{{< copyable "sql" >}}

```sql
desc select * from metrics_schema.tidb_query_duration where value is not null and time>='2020-03-25 23:40:00' and time <= '2020-03-25 23:42:00' and quantile=0.99;
```

```sql
+------------------+----------+------+---------------------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| id               | estRows  | task | access object             | operator info                                                                                                                                                                                          |
+------------------+----------+------+---------------------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| Selection_5      | 8000.00  | root |                           | not(isnull(Column#5))                                                                                                                                                                                  |
| └─MemTableScan_6 | 10000.00 | root | table:tidb_query_duration | PromQL:histogram_quantile(0.99, sum(rate(tidb_server_handle_query_duration_seconds_bucket{}[60s])) by (le,sql_type,instance)), start_time:2020-03-25 23:40:00, end_time:2020-03-25 23:42:00, step:1m0s |
+------------------+----------+------+---------------------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
```

可以发现执行计划中有一个 `PromQL`, 以及查询监控的 `start_time` 和 `end_time`，还有 `step` 值，在实际执行时，TiDB 会调用 Prometheus 的 `query_range` HTTP API 接口来查询监控数据。

从以上结果可知，在 [`2020-03-25 23:40:00`, `2020-03-25 23:42:00`] 时间范围内，每个 label 只有三个时间的值，间隔时间是 1 分钟，即执行计划中的 `step` 值。该间隔时间由以下两个 session 变量决定：

* `tidb_metric_query_step`：查询的分辨率步长。从 Prometheus 的 `query_range` 接口查询数据时需要指定 `start_time`，`end_time` 和 `step`，其中 `step` 会使用该变量的值。
* `tidb_metric_query_range_duration`：查询监控时，会将 `PROMQL` 中的 `$RANGE_DURATION` 替换成该变量的值，默认值是 60 秒。

如果想要查看不同时间粒度的监控项的值，用户可以修改上面两个 session 变量后查询监控表，示例如下：

首先修改两个 session 变量的值，将时间粒度设置为 30 秒。

> **注意：**
>
> Prometheus 支持查询的最小粒度为 30 秒。

{{< copyable "sql" >}}

```sql
set @@tidb_metric_query_step=30;
set @@tidb_metric_query_range_duration=30;
```

再查询 `tidb_query_duration` 监控如下，可以发现在三分钟时间范围内，每个 label 有六个时间的值，每个值时间间隔是 30 秒。

{{< copyable "sql" >}}

```sql
select * from metrics_schema.tidb_query_duration where value is not null and time>='2020-03-25 23:40:00' and time <= '2020-03-25 23:42:00' and quantile=0.99;
```

```sql
+---------------------+-------------------+----------+----------+-----------------+
| time                | instance          | sql_type | quantile | value           |
+---------------------+-------------------+----------+----------+-----------------+
| 2020-03-25 23:40:00 | 172.16.5.40:10089 | Insert   | 0.99     | 0.483285651924  |
| 2020-03-25 23:40:30 | 172.16.5.40:10089 | Insert   | 0.99     | 0.484151462113  |
| 2020-03-25 23:41:00 | 172.16.5.40:10089 | Insert   | 0.99     | 0.504576        |
| 2020-03-25 23:41:30 | 172.16.5.40:10089 | Insert   | 0.99     | 0.493577384561  |
| 2020-03-25 23:42:00 | 172.16.5.40:10089 | Insert   | 0.99     | 0.49482474311   |
| 2020-03-25 23:40:00 | 172.16.5.40:10089 | Select   | 0.99     | 0.189253402185  |
| 2020-03-25 23:40:30 | 172.16.5.40:10089 | Select   | 0.99     | 0.184224951851  |
| 2020-03-25 23:41:00 | 172.16.5.40:10089 | Select   | 0.99     | 0.151673410553  |
| 2020-03-25 23:41:30 | 172.16.5.40:10089 | Select   | 0.99     | 0.127953838989  |
| 2020-03-25 23:42:00 | 172.16.5.40:10089 | Select   | 0.99     | 0.127455434547  |
| 2020-03-25 23:40:00 | 172.16.5.40:10089 | internal | 0.99     | 0.0624          |
| 2020-03-25 23:40:30 | 172.16.5.40:10089 | internal | 0.99     | 0.12416         |
| 2020-03-25 23:41:00 | 172.16.5.40:10089 | internal | 0.99     | 0.0304          |
| 2020-03-25 23:41:30 | 172.16.5.40:10089 | internal | 0.99     | 0.06272         |
| 2020-03-25 23:42:00 | 172.16.5.40:10089 | internal | 0.99     | 0.0629333333333 |
+---------------------+-------------------+----------+----------+-----------------+
```

最后查看执行计划，也会发现执行计划中的 `PromQL` 以及 `step` 的值都已经变成了 30 秒。

{{< copyable "sql" >}}

```sql
desc select * from metrics_schema.tidb_query_duration where value is not null and time>='2020-03-25 23:40:00' and time <= '2020-03-25 23:42:00' and quantile=0.99;
```

```sql
+------------------+----------+------+---------------------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| id               | estRows  | task | access object             | operator info                                                                                                                                                                                         |
+------------------+----------+------+---------------------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| Selection_5      | 8000.00  | root |                           | not(isnull(Column#5))                                                                                                                                                                                 |
| └─MemTableScan_6 | 10000.00 | root | table:tidb_query_duration | PromQL:histogram_quantile(0.99, sum(rate(tidb_server_handle_query_duration_seconds_bucket{}[30s])) by (le,sql_type,instance)), start_time:2020-03-25 23:40:00, end_time:2020-03-25 23:42:00, step:30s |
+------------------+----------+------+---------------------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
```
