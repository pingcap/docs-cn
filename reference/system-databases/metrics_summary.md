---
title: METRICS_SUMMARY
category: reference
---

# METRICS_SUMMARY

由于 TiDB 集群的监控指标数量较大，因此为了方便用户能更加便捷地从众多监控中找出异常的监控项，TiDB 4.0 提供了监控汇总表：

* `information_schema.metrics_summary`。
* `information_schema.metrics_summary_by_label`。

这两张表用于汇总所有监控数据，以提升用户对各个监控指标进行排查的效率。两者不同在于 information_schema.metrics_summary_by_label 会对不同的 label 使用区分统计。

{{< copyable "sql" >}}

```sql
mysql> desc metrics_summary;
```

```
+--------------+-----------------------+------+------+---------+-------+
| Field        | Type                  | Null | Key  | Default | Extra |
+--------------+-----------------------+------+------+---------+-------+
| METRICS_NAME | varchar(64)           | YES  |      | NULL    |       |
| QUANTILE     | double unsigned       | YES  |      | NULL    |       |
| SUM_VALUE    | double(22,6) unsigned | YES  |      | NULL    |       |
| AVG_VALUE    | double(22,6) unsigned | YES  |      | NULL    |       |
| MIN_VALUE    | double(22,6) unsigned | YES  |      | NULL    |       |
| MAX_VALUE    | double(22,6) unsigned | YES  |      | NULL    |       |
| COMMENT      | varchar(256)          | YES  |      | NULL    |       |
+--------------+-----------------------+------+------+---------+-------+
7 rows in set (0.00 sec)
```

字段解释：

* `METRICS_NAME`：监控表名
* `QUANTILE`：百分位，可以通过 SQL 语句指定 `QUANTILE`，例如
    * `select * from metrics_summary where quantile=0.99` 指定查看百分位为 0.99 的数据。
    * `select * from metrics_summary where quantile in (0.80, 0.99, 0.99, 0.999)` 同时查看百分位为 0.80, 0.99, 0.99, 0.999 的数据。
* `SUM_VALUE、AVG_VALUE、MIN_VALUE、MAX_VALUE`：分别表示总和，平均值，最小值，最大值。
* `COMMENT`：对应监控的解释。

具体查询示例：
以查询 ['2020-03-08 13:23:00', '2020-03-08 13:33:00'] 时间范围内 TiDB 集群中平均耗时最高的 3 组监控项为例。通过直接查询 `information_schema.metrics_summary` 表，并通过 `/*+ time_range() */` 这个 hint 来指定时间范围来构造以下 SQL：

{{< copyable "sql" >}}

```sql
select /*+ time_range('2020-03-08 13:23:00','2020-03-08 13:33:00') */ *
from information_schema.`METRICS_SUMMARY`
where metrics_name like 'tidb%duration'
 and avg_value > 0
 and quantile = 0.99
order by avg_value desc
limit 3\G
```

```
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

类似的，查询 `metrics_summary_by_label` 监控汇总表结果如下：

{{< copyable "sql" >}}

```sql
select /*+ time_range('2020-03-08 13:23:00','2020-03-08 13:33:00') */ *
from information_schema.`METRICS_SUMMARY_BY_LABEL`
where metrics_name like 'tidb%duration'
 and avg_value > 0
 and quantile = 0.99
order by avg_value desc
limit 10\G
```

```
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

前文提到 `metrics_summary_by_label` 表结构相对于 `metrics_summary` 多了一列 LABEL, 以上面查询结果的第 2, 3 行为例：分别表示 `tidb_query_duration` 的 Select 和 Rollback 类型的语句平均耗时非常高。

除以上示例之外，监控汇总表可以通过两个时间段的全链路监控对比，迅速找出监控数据变化最大的模块，快速定位瓶颈，以下对比两个时间段的所有监控（其中 t1 为 baseline），并按照差别最大的监控排序：

* 时间段 t1 : ("2020-03-03 17:08:00", "2020-03-03 17:11:00")。
* 时间段 t2 : ("2020-03-03 17:18:00", "2020-03-03 17:21:00")  。
对两个时间段的监控按照 `METRICS_NAME` 进行 join，并按照差值排序。其中 `TIME_RANGE` 是用于指定查询时间的 Hint。

查询 `t1.avg_value` / `t2.avg_value` 差异最大的 10 个监控项:

{{< copyable "sql" >}}

```sql
SELECT
 t1.avg_value / t2.avg_value AS ratio,
 t1.metrics_name,
 t1.avg_value,
 t2.avg_value,
 t2.comment
FROM
 (
   SELECT /*+ time_range("2020-03-03 17:08:00", "2020-03-03 17:11:00")*/
     *
   FROM information_schema.metrics_summary
 ) t1
 JOIN
 (
   SELECT /*+ time_range("2020-03-03 17:18:00", "2020-03-03 17:21:00")*/
     *
   FROM information_schema.metrics_summary
 ) t2
 ON t1.metrics_name = t2.metrics_name
ORDER BY
 ratio DESC limit 10;
```

```
+----------------+-----------------------------------+-------------------+-------------------+--------------------------------------------------------------------------+
| ratio          | metrics_name                      | avg_value         | avg_value         | comment                                                                  |
+----------------+-----------------------------------+-------------------+-------------------+--------------------------------------------------------------------------+
| 17.6439787379  | tikv_region_average_written_bytes |   30816827.0953   |    1746591.71568  | The average rate of writing bytes to Regions per TiKV instance           |
|  8.88407551364 | tikv_region_average_written_keys  |     108557.034612 |      12219.283193 | The average rate of written keys to Regions per TiKV instance            |
|  6.4105335594  | tidb_kv_write_num                 |       4493.293654 |        700.923505 | The quantile of kv write times per transaction execution                 |
|  2.99993333333 | tidb_gc_total_count               |          1.0      |          0.333341 | The total count of kv storage garbage collection time durations          |
|  2.66412165823 | tikv_engine_avg_seek_duration     |       6569.879007 |       2466.05818  | The time consumed when executing seek operation, the unit is microsecond |
|  2.66412165823 | tikv_engine_max_seek_duration     |       6569.879007 |       2466.05818  | The time consumed when executing seek operation, the unit is microsecond |
|  2.49994444321 | tikv_region_change                |         -0.277778 |         -0.111114 | The count of region change per TiKV instance                             |
|  2.16063829787 | etcd_wal_fsync_duration           |          0.002539 |          0.001175 | The quantile time consumed of writing WAL into the persistent storage    |
|  2.06089264604 | node_memory_free                  | 4541448192.0      | 2203631616.0      |                                                                          |
|  1.96749064186 | tidb_kv_write_size                |     514489.28     |     261495.159902 | The quantile of kv write size per transaction execution                  |
+----------------+-----------------------------------+-------------------+-------------------+--------------------------------------------------------------------------+
```

查询结果表示：

* t1 时间段内的 `tikv_region_average_written_bytes` region 的平均写入字节数）比 t2 时间段高了 17.6 倍。
* t1 时间段内的 `tikv_region_average_written_keys`（region 的平均写入 keys 数）比 t2 时间段高了 8.8 倍。
* t1 时间段内的 `tidb_kv_write_size`（tidb 每个事务写入的 kv 大小）比 t2 时间段高了 1.96 倍。

通过以上结果可以轻易看出 t1 时间段的写入要比 t2 时间段高。

反过来，查询 t2.avg_value / t1.avg_value 差异最大的 10 个监控项:

{{< copyable "sql" >}}

```sql
SELECT
 t2.avg_value / t1.avg_value AS ratio,
 t1.metrics_name,
 t1.avg_value,
 t2.avg_value,
 t2.comment
FROM
 (
   SELECT /*+ time_range("2020-03-03 17:08:00", "2020-03-03 17:11:00")*/
     *
   FROM information_schema.metrics_summary
 ) t1
 JOIN
 (
   SELECT /*+ time_range("2020-03-03 17:18:00", "2020-03-03 17:21:00")*/
     *
   FROM information_schema.metrics_summary
 ) t2
 ON t1.metrics_name = t2.metrics_name
ORDER BY
 ratio DESC limit 10;
```

```
+----------------+-----------------------------------------+----------------+------------------+---------------------------------------------------------------------------------------------+
| ratio          | metrics_name                            | avg_value      | avg_value        | comment                                                                                     |
+----------------+-----------------------------------------+----------------+------------------+---------------------------------------------------------------------------------------------+
| 5865.59537065  | tidb_slow_query_cop_process_total_time  |       0.016333 |        95.804724 | The total time of TiDB slow query statistics with slow query total cop process time(second) |
| 3648.74109023  | tidb_distsql_partial_scan_key_total_num |   10865.666667 |  39646004.4394   | The total num of distsql partial scan key numbers                                          |
|  267.002351165 | tidb_slow_query_cop_wait_total_time     |       0.003333 |         0.890008 | The total time of TiDB slow query statistics with slow query total cop wait time(second)    |
|  192.43267836  | tikv_cop_total_response_total_size      | 2515333.66667  | 484032394.445    |                                                                                             |
|  192.43267836  | tikv_cop_total_response_size            |   41922.227778 |   8067206.57408  |                                                                                             |
|  152.780296296 | tidb_distsql_scan_key_total_num         |    5304.333333 |    810397.618317 | The total num of distsql scan numbers                                                      |
|  126.042290167 | tidb_distsql_execution_total_time       |       0.421622 |        53.142143 | The total time of distsql execution(second)                                                 |
|  105.164020657 | tikv_cop_scan_details                   |     134.450733 |     14139.379665 |                                                                                             |
|  105.164020657 | tikv_cop_scan_details_total             |    8067.043981 |    848362.77991  |                                                                                             |
|  10``1.635495394 | tikv_cop_total_kv_cursor_operations     |    1070.875    |    108838.91113  |                                                                                             |
+----------------+-----------------------------------------+----------------+------------------+---------------------------------------------------------------------------------------------+
```

上面查询结果表示：

* t2 时间段内的 `tidb_slow_query_cop_process_total_time`（tidb 慢查询中的 `cop process` 耗时 ）比 t1 时间段高了 5865 倍。
* t2 时间段内的 `tidb_distsql_partial_scan_key_total_num`（tidb 的 `distsql` 请求扫描key 的数量）比 t1 时间段高了 3648 倍。
* t2 时间段内的 `tikv_cop_total_response_size`（tikv 的 cop 请求结果的大小 ）比 t1 时间段高了 192 倍。
* t2 时间段内的 `tikv_cop_scan_details`（tikv 的 cop 请求的 scan ）比 t1 时间段高了 105 倍。

对比上面两个时间段的查询，可以大致了解集群在这两个时间段的负载情况。t2 时间段的 Cop 请求要比 t2 时间段高很多，导致 TiKV 的 `Copprocessor` 过载，出现了 `cop task` 等待，可以猜测可能是 t2 时间段出现了一些大查询，或者是查询较多的负载。

实际上，在 t1 ~ t2 整个时间段内都在跑 `go-ycsb` 的压测，然后在 t2 时间段跑了 20 个 `tpch` 的查询，所以是因为 `tpch` 大查询导致了很多的 cop 请求。
