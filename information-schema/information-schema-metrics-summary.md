---
title: METRICS_SUMMARY
summary: 了解 TiDB 系统表 `METRICS_SUMMARY`。
aliases: ['/docs-cn/dev/system-tables/system-table-metrics-summary/','/docs-cn/dev/reference/system-databases/metrics-summary/','/zh/tidb/dev/system-table-metrics-summary/']
---

# METRICS_SUMMARY

由于 TiDB 集群的监控指标数量较多，为了方便用户从众多监控中找出异常的监控项，TiDB 4.0 提供了以下监控汇总表：

* `information_schema.metrics_summary`
* `information_schema.metrics_summary_by_label`

这两张表用于汇总所有监控数据，用户排查各个监控指标会更有效率。其中 `information_schema.metrics_summary_by_label` 会对不同的 label 进行区分统计。

{{< copyable "sql" >}}

```sql
USE information_schema;
DESC metrics_summary;
```

```sql
+--------------+--------------+------+------+---------+-------+
| Field        | Type         | Null | Key  | Default | Extra |
+--------------+--------------+------+------+---------+-------+
| METRICS_NAME | varchar(64)  | YES  |      | NULL    |       |
| QUANTILE     | double       | YES  |      | NULL    |       |
| SUM_VALUE    | double(22,6) | YES  |      | NULL    |       |
| AVG_VALUE    | double(22,6) | YES  |      | NULL    |       |
| MIN_VALUE    | double(22,6) | YES  |      | NULL    |       |
| MAX_VALUE    | double(22,6) | YES  |      | NULL    |       |
| COMMENT      | varchar(256) | YES  |      | NULL    |       |
+--------------+--------------+------+------+---------+-------+
7 rows in set (0.00 sec)
```

字段解释：

* `METRICS_NAME`：监控表名。
* `QUANTILE`：百分位。可以通过 SQL 语句指定 `QUANTILE`，例如：
    * `select * from metrics_summary where quantile=0.99` 指定查看百分位为 0.99 的数据。
    * `select * from metrics_summary where quantile in (0.80, 0.90, 0.99, 0.999)` 同时查看百分位为 0.80, 0.90, 0.99, 0.999 的数据。
* `SUM_VALUE、AVG_VALUE、MIN_VALUE、MAX_VALUE` 分别表示总和、平均值、最小值、最大值。
* `COMMENT`：对应监控的解释。

具体查询示例：

查询 `'2020-03-08 13:23:00', '2020-03-08 13:33:00'` 时间范围内 TiDB 集群中平均耗时最高的三组监控项。可直接查询 `information_schema.metrics_summary` 表，并通过 `/*+ time_range() */` 这个 hint 来指定时间范围，构造的 SQL 语句如下：

{{< copyable "sql" >}}

```sql
SELECT /*+ time_range('2020-03-08 13:23:00','2020-03-08 13:33:00') */ *
FROM information_schema.metrics_summary
WHERE metrics_name LIKE 'tidb%duration'
 AND avg_value > 0
 AND quantile = 0.99
ORDER BY avg_value DESC
LIMIT 3\G
```

```sql
***************************[ 1. row ]***************************
METRICS_NAME | tidb_get_token_duration
QUANTILE     | 0.99
SUM_VALUE    | 8.972509
AVG_VALUE    | 0.996945
MIN_VALUE    | 0.996515
MAX_VALUE    | 0.997458
COMMENT      |  The quantile of Duration (us) for getting token, it should be small until concurrency limit is reached(second)
***************************[ 2. row ]***************************
METRICS_NAME | tidb_query_duration
QUANTILE     | 0.99
SUM_VALUE    | 0.269079
AVG_VALUE    | 0.007272
MIN_VALUE    | 0.000667
MAX_VALUE    | 0.01554
COMMENT      | The quantile of TiDB query durations(second)
***************************[ 3. row ]***************************
METRICS_NAME | tidb_kv_request_duration
QUANTILE     | 0.99
SUM_VALUE    | 0.170232
AVG_VALUE    | 0.004601
MIN_VALUE    | 0.000975
MAX_VALUE    | 0.013
COMMENT      | The quantile of kv requests durations by store
```

类似的，查询 `metrics_summary_by_label` 监控汇总表示例如下：

{{< copyable "sql" >}}

```sql
SELECT /*+ time_range('2020-03-08 13:23:00','2020-03-08 13:33:00') */ *
FROM information_schema.metrics_summary_by_label
WHERE metrics_name LIKE 'tidb%duration'
 AND avg_value > 0
 AND quantile = 0.99
ORDER BY avg_value DESC
LIMIT 10\G
```

```sql
***************************[ 1. row ]***************************
INSTANCE     | 172.16.5.40:10089
METRICS_NAME | tidb_get_token_duration
LABEL        |
QUANTILE     | 0.99
SUM_VALUE    | 8.972509
AVG_VALUE    | 0.996945
MIN_VALUE    | 0.996515
MAX_VALUE    | 0.997458
COMMENT      |  The quantile of Duration (us) for getting token, it should be small until concurrency limit is reached(second)
***************************[ 2. row ]***************************
INSTANCE     | 172.16.5.40:10089
METRICS_NAME | tidb_query_duration
LABEL        | Select
QUANTILE     | 0.99
SUM_VALUE    | 0.072083
AVG_VALUE    | 0.008009
MIN_VALUE    | 0.007905
MAX_VALUE    | 0.008241
COMMENT      | The quantile of TiDB query durations(second)
***************************[ 3. row ]***************************
INSTANCE     | 172.16.5.40:10089
METRICS_NAME | tidb_query_duration
LABEL        | Rollback
QUANTILE     | 0.99
SUM_VALUE    | 0.072083
AVG_VALUE    | 0.008009
MIN_VALUE    | 0.007905
MAX_VALUE    | 0.008241
COMMENT      | The quantile of TiDB query durations(second)
```

前文提到 `metrics_summary_by_label` 表结构相对于 `metrics_summary` 多了一列 `LABEL`。以上面查询结果的第 2、3 行分别表示 `tidb_query_duration` 的 `Select` 和 `Rollback` 类型的语句平均耗时非常高。

除以上示例之外，监控汇总表可以通过对比两个时间段的全链路监控，迅速找出监控数据中变化最大的模块，快速定位瓶颈。以下示例对比两个时间段的所有监控（其中 t1 为 baseline），并按照差别最大的监控排序：

* 时间段 t1：`("2020-03-03 17:08:00", "2020-03-03 17:11:00")`
* 时间段 t2：`("2020-03-03 17:18:00", "2020-03-03 17:21:00")`

对两个时间段的监控按照 `METRICS_NAME` 进行 join，并按照差异值大小排序。其中 `TIME_RANGE` 是用于指定查询时间的 hint。

{{< copyable "sql" >}}

```sql
SELECT GREATEST(t1.avg_value,t2.avg_value)/LEAST(t1.avg_value,
         t2.avg_value) AS ratio,
         t1.metrics_name,
         t1.avg_value as t1_avg_value,
         t2.avg_value as t2_avg_value,
         t2.comment
FROM
    (SELECT /*+ time_range("2020-03-03 17:08:00", "2020-03-03 17:11:00")*/ *
    FROM information_schema.metrics_summary ) t1
JOIN
    (SELECT /*+ time_range("2020-03-03 17:18:00", "2020-03-03 17:21:00")*/ *
    FROM information_schema.metrics_summary ) t2
    ON t1.metrics_name = t2.metrics_name
ORDER BY ratio DESC LIMIT 10;
```

```sql
+----------------+------------------------------------------+----------------+------------------+---------------------------------------------------------------------------------------------+
| ratio          | metrics_name                             | t1_avg_value   | t2_avg_value     | comment                                                                                     |
+----------------+------------------------------------------+----------------+------------------+---------------------------------------------------------------------------------------------+
| 5865.59537065  | tidb_slow_query_cop_process_total_time   |       0.016333 |        95.804724 | The total time of TiDB slow query statistics with slow query total cop process time(second) |
| 3648.74109023  | tidb_distsql_partial_scan_key_total_num  |   10865.666667 |  39646004.4394   | The total num of distsql partial scan key numbers                                           |
|  267.002351165 | tidb_slow_query_cop_wait_total_time      |       0.003333 |         0.890008 | The total time of TiDB slow query statistics with slow query total cop wait time(second)    |
|  192.43267836  | tikv_cop_total_response_total_size       | 2515333.66667  | 484032394.445    |                                                                                             |
|  192.43267836  | tikv_cop_total_response_size_per_seconds |   41922.227778 |   8067206.57408  |                                                                                             |
|  152.780296296 | tidb_distsql_scan_key_total_num          |    5304.333333 |    810397.618317 | The total num of distsql scan numbers                                                       |
|  126.042290167 | tidb_distsql_execution_total_time        |       0.421622 |        53.142143 | The total time of distsql execution(second)                                                 |
|  105.164020657 | tikv_cop_scan_details                    |     134.450733 |     14139.379665 |                                                                                             |
|  105.164020657 | tikv_cop_scan_details_total              |    8067.043981 |    848362.77991  |                                                                                             |
|  101.635495394 | tikv_cop_scan_keys_num                   |    1070.875    |    108838.91113  |                                                                                             |
+----------------+------------------------------------------+----------------+------------------+---------------------------------------------------------------------------------------------+
```

上面查询结果表示：

* t2 时间段内的 `tidb_slow_query_cop_process_total_time`（TiDB 慢查询中的 `cop process` 耗时）比 t1 时间段高了 5865 倍。
* t2 时间段内的 `tidb_distsql_partial_scan_key_total_num`（TiDB 的 `distsql` 请求扫描 key 的数量）比 t1 时间段高了 3648 倍。
* t2 时间段内的 `tidb_slow_query_cop_wait_total_time`（TiDB 慢查询中的 cop 请求排队等待的耗时）比 t1 时间段高了 267 倍。
* t2 时间段内的 `tikv_cop_total_response_size`（TiKV 的 cop 请求结果的大小）比 t1 时间段高了 192 倍。
* t2 时间段内的 `tikv_cop_scan_details`（TiKV 的 cop 请求的 scan）比 t1 时间段高了 105 倍。

综上，可以马上知道 t2 时间段的 cop 请求要比 t2 时间段高很多，导致 TiKV 的 Coprocessor 过载，出现了 `cop task` 等待，可以猜测可能是 t2 时间段出现了一些大查询，或者是查询较多的负载。

实际上，在 t1 ~ t2 整个时间段内都在跑 `go-ycsb` 的压测，然后在 t2 时间段跑了 20 个 `tpch` 的查询，所以是因为 `tpch` 大查询导致了出现很多的 cop 请求。
