---
title: Metrics Schema
summary: Learn the `METRICS_SCHEMA` schema.
aliases: ['/docs/dev/system-tables/system-table-metrics-schema/','/docs/dev/reference/system-databases/metrics-schema/','/tidb/dev/system-table-metrics-schema/']
---

# Metrics Schema

The `METRICS_SCHEMA` is a set of views on top of TiDB metrics that are stored in Prometheus. The source of the PromQL (Prometheus Query Language) for each of the tables is available in [`INFORMATION_SCHEMA.METRICS_TABLES`](/information-schema/information-schema-metrics-tables.md).

{{< copyable "sql" >}}

```sql
USE metrics_schema;
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
SHOW TABLES;
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

The `METRICS_SCHEMA` is used as a data source for monitoring-related summary tables such as ([`metrics_summary`](/information-schema/information-schema-metrics-summary.md), [`metrics_summary_by_label`](/information-schema/information-schema-metrics-summary.md) and [`inspection_summary`](/information-schema/information-schema-inspection-summary.md).

## Additional Examples

Taking the `tidb_query_duration` monitoring table in `metrics_schema` as an example, this section illustrates how to use this monitoring table and how it works. The working principles of other monitoring tables are similar to `tidb_query_duration`.

Query the information related to the `tidb_query_duration` table on `information_schema.metrics_tables`:

{{< copyable "sql" >}}

```sql
SELECT * FROM information_schema.metrics_tables WHERE table_name='tidb_query_duration';
```

```sql
+---------------------+----------------------------------------------------------------------------------------------------------------------------------------------------------+-------------------+----------+----------------------------------------------+
| TABLE_NAME          | PROMQL                                                                                                                                                   | LABELS            | QUANTILE | COMMENT                                      |
+---------------------+----------------------------------------------------------------------------------------------------------------------------------------------------------+-------------------+----------+----------------------------------------------+
| tidb_query_duration | histogram_quantile($QUANTILE, sum(rate(tidb_server_handle_query_duration_seconds_bucket{$LABEL_CONDITIONS}[$RANGE_DURATION])) by (le,sql_type,instance)) | instance,sql_type | 0.9      | The quantile of TiDB query durations(second) |
+---------------------+----------------------------------------------------------------------------------------------------------------------------------------------------------+-------------------+----------+----------------------------------------------+
```

Field description:

* `TABLE_NAME`: Corresponds to the table name in `metrics_schema` . In this example, the table name is `tidb_query_duration`.
* `PROMQL`: The working principle of the monitoring table is to first map SQL statements to `PromQL`, then to request data from Prometheus, and to convert Prometheus results into SQL query results. This field is the expression template of `PromQL`. When you query the data of the monitoring table, the query conditions are used to rewrite the variables in this template to generate the final query expression.
* `LABELS`: The label for the monitoring item. `tidb_query_duration` has two labels: `instance` and `sql_type`.
* `QUANTILE`: The percentile. For monitoring data of the histogram type, a default percentile is specified. If the value of this field is `0`, it means that the monitoring item corresponding to the monitoring table is not a histogram.
* `COMMENT`: Explanations for the monitoring table. You can see that the `tidb_query_duration` table is used to query the percentile time of the TiDB query execution, such as the query time of P999/P99/P90. The unit is second.

To query the schema of the `tidb_query_duration` table, execute the following statement:

{{< copyable "sql" >}}

```sql
SHOW CREATE TABLE metrics_schema.tidb_query_duration;
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

* `time`: The time of the monitoring item.
* `instance` and `sql_type`: The labels of the `tidb_query_duration` monitoring item. `instance` means the monitoring address. `sql_type` means the type of the executed SQL statement.
* `quantile`: The percentile. The monitoring item of the histogram type has this column, which indicates the percentile time of the query. For example, `quantile = 0.9` means to query the time of P90.
* `value`: The value of the monitoring item.

The following statement queries the P99 time within the range of [`2020-03-25 23:40:00`, `2020-03-25 23:42:00`].

{{< copyable "sql" >}}

```sql
SELECT * FROM metrics_schema.tidb_query_duration WHERE value is not null AND time>='2020-03-25 23:40:00' AND time <= '2020-03-25 23:42:00' AND quantile=0.99;
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

The first row of the query result above means that at the time of 2020-03-25 23:40:00, on the TiDB instance `172.16.5.40:10089`, the P99 execution time of the `Insert` type statement is 0.509929485256 seconds. The meanings of other rows are similar. Other values of the `sql_type` column are described as follows:

* `Select`: The `select` type statement is executed.
* `internal`: The internal SQL statement of TiDB, which is used to update the statistical information and get the global variables.

To view the execution plan of the statement above, execute the following statement:

{{< copyable "sql" >}}

```sql
DESC SELECT * FROM metrics_schema.tidb_query_duration WHERE value is not null AND time>='2020-03-25 23:40:00' AND time <= '2020-03-25 23:42:00' AND quantile=0.99;
```

```sql
+------------------+----------+------+---------------------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| id               | estRows  | task | access object             | operator info                                                                                                                                                                                          |
+------------------+----------+------+---------------------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| Selection_5      | 8000.00  | root |                           | not(isnull(Column#5))                                                                                                                                                                                  |
| └─MemTableScan_6 | 10000.00 | root | table:tidb_query_duration | PromQL:histogram_quantile(0.99, sum(rate(tidb_server_handle_query_duration_seconds_bucket{}[60s])) by (le,sql_type,instance)), start_time:2020-03-25 23:40:00, end_time:2020-03-25 23:42:00, step:1m0s |
+------------------+----------+------+---------------------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
```

From the result above, you can see that `PromQL`, `start_time`, `end_time`, and `step` are in the execution plan. During the execution process, TiDB calls the `query_range` HTTP API of Prometheus to query the monitoring data.

You might find that in the range of [`2020-03-25 23:40:00`, `2020-03-25 23:42:00`], each label only has three time values. In the execution plan, the value of `step` is 1 minute, which means that the interval of these values is 1 minute. `step` is determined by the following two session variables:

* `tidb_metric_query_step`: The query resolution step width. To get the `query_range` data from Prometheus, you need to specify `start_time`, `end_time`, and `step`. `step` uses the value of this variable.
* `tidb_metric_query_range_duration`: When the monitoring data is queried, the value of the `$ RANGE_DURATION` field in `PROMQL` is replaced with the value of this variable. The default value is 60 seconds.

To view the values of monitoring items with different granularities, you can modify the two session variables above before querying the monitoring table. For example:

1. Modify the values of the two session variables and set the time granularity to 30 seconds.

    > **Note:**
    >
    > The minimum granularity supported by Prometheus is 30 seconds.

    {{< copyable "sql" >}}

    ```sql
    set @@tidb_metric_query_step=30;
    set @@tidb_metric_query_range_duration=30;
    ```

2. Query the `tidb_query_duration` monitoring item as follows. From the result, you can see that within the 3-minute time range, each label has 6 time values, and the interval between each value is 30 seconds.

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

3. View the execution plan. From the result, you can also see that the values of `PromQL` and `step` in the execution plan have been changed to 30 seconds.

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
