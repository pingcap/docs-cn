---
title: INSPECTION_RESULT
summary: Learn the `INSPECTION_RESULT` diagnostic result table.
aliases: ['/docs/dev/system-tables/system-table-inspection-result/','/docs/dev/reference/system-databases/inspection-result/','/tidb/dev/system-table-inspection-result/']
---

# INSPECTION_RESULT

TiDB has some built-in diagnostic rules for detecting faults and hidden issues in the system.

The `INSPECTION_RESULT` diagnostic feature can help you quickly find problems and reduce your repetitive manual work. You can use the `select * from information_schema.inspection_result` statement to trigger the internal diagnostics.

The structure of the `information_schema.inspection_result` diagnostic result table `information_schema.inspection_result` is as follows:

{{< copyable "sql" >}}

```sql
USE information_schema;
DESC inspection_result;
```

```sql
+----------------+--------------+------+------+---------+-------+
| Field          | Type         | Null | Key  | Default | Extra |
+----------------+--------------+------+------+---------+-------+
| RULE           | varchar(64)  | YES  |      | NULL    |       |
| ITEM           | varchar(64)  | YES  |      | NULL    |       |
| TYPE           | varchar(64)  | YES  |      | NULL    |       |
| INSTANCE       | varchar(64)  | YES  |      | NULL    |       |
| STATUS_ADDRESS | varchar(64)  | YES  |      | NULL    |       |
| VALUE          | varchar(64)  | YES  |      | NULL    |       |
| REFERENCE      | varchar(64)  | YES  |      | NULL    |       |
| SEVERITY       | varchar(64)  | YES  |      | NULL    |       |
| DETAILS        | varchar(256) | YES  |      | NULL    |       |
+----------------+--------------+------+------+---------+-------+
9 rows in set (0.00 sec)
```

Field description:

* `RULE`: The name of the diagnostic rule. Currently, the following rules are available:
    * `config`: Checks whether the configuration is consistent and proper. If the same configuration is inconsistent on different instances, a `warning` diagnostic result is generated.
    * `version`: The consistency check of version. If the same version is inconsistent on different instances, a `warning` diagnostic result is generated.
    * `node-load`: Checks the server load. If the current system load is too high, the corresponding `warning` diagnostic result is generated.
    * `critical-error`: Each module of the system defines critical errors. If a critical error exceeds the threshold within the corresponding time period, a warning diagnostic result is generated.
    * `threshold-check`: The diagnostic system checks the thresholds of key metrics. If a threshold is exceeded, the corresponding diagnostic information is generated.
* `ITEM`: Each rule diagnoses different items. This field indicates the specific diagnostic items corresponding to each rule.
* `TYPE`: The instance type of the diagnostics. The optional values are `tidb`, `pd`, and `tikv`.
* `INSTANCE`: The specific address of the diagnosed instance.
* `STATUS_ADDRESS`: The HTTP API service address of the instance.
* `VALUE`: The value of a specific diagnostic item.
* `REFERENCE`: The reference value (threshold value) for this diagnostic item. If `VALUE` exceeds the threshold, the corresponding diagnostic information is generated.
* `SEVERITY`: The severity level. The optional values are `warning` and `critical`.
* `DETAILS`: Diagnostic details, which might also contain SQL statement(s) or document links for further diagnostics.

## Diagnostics example

Diagnose issues currently existing in the cluster.

{{< copyable "sql" >}}

```sql
SELECT * FROM information_schema.inspection_result\G
```

```sql
***************************[ 1. row ]***************************
RULE      | config
ITEM      | log.slow-threshold
TYPE      | tidb
INSTANCE  | 172.16.5.40:4000
VALUE     | 0
REFERENCE | not 0
SEVERITY  | warning
DETAILS   | slow-threshold = 0 will record every query to slow log, it may affect performance
***************************[ 2. row ]***************************
RULE      | version
ITEM      | git_hash
TYPE      | tidb
INSTANCE  |
VALUE     | inconsistent
REFERENCE | consistent
SEVERITY  | critical
DETAILS   | the cluster has 2 different tidb version, execute the sql to see more detail: select * from information_schema.cluster_info where type='tidb'
***************************[ 3. row ]***************************
RULE      | threshold-check
ITEM      | storage-write-duration
TYPE      | tikv
INSTANCE  | 172.16.5.40:23151
VALUE     | 130.417
REFERENCE | < 0.100
SEVERITY  | warning
DETAILS   | max duration of 172.16.5.40:23151 tikv storage-write-duration was too slow
***************************[ 4. row ]***************************
RULE      | threshold-check
ITEM      | rocksdb-write-duration
TYPE      | tikv
INSTANCE  | 172.16.5.40:20151
VALUE     | 108.105
REFERENCE | < 0.100
SEVERITY  | warning
DETAILS   | max duration of 172.16.5.40:20151 tikv rocksdb-write-duration was too slow
```

The following issues can be detected from the diagnostic result above:

* The first row indicates that TiDB's `log.slow-threshold` value is configured to `0`, which might affect performance.
* The second row indicates that two different TiDB versions exist in the cluster.
* The third and fourth rows indicate that the TiKV write delay is too long. The expected delay is no more than 0.1 second, while the actual delay is far longer than expected.

You can also diagnose issues existing within a specified range, such as from "2020-03-26 00:03:00" to "2020-03-26 00:08:00". To specify the time range, use the SQL Hint of `/*+ time_range() */`. See the following query example:

{{< copyable "sql" >}}

```sql
select /*+ time_range("2020-03-26 00:03:00", "2020-03-26 00:08:00") */ * from information_schema.inspection_result\G
```

```sql
***************************[ 1. row ]***************************
RULE      | critical-error
ITEM      | server-down
TYPE      | tidb
INSTANCE  | 172.16.5.40:4009
VALUE     |
REFERENCE |
SEVERITY  | critical
DETAILS   | tidb 172.16.5.40:4009 restarted at time '2020/03/26 00:05:45.670'
***************************[ 2. row ]***************************
RULE      | threshold-check
ITEM      | get-token-duration
TYPE      | tidb
INSTANCE  | 172.16.5.40:10089
VALUE     | 0.234
REFERENCE | < 0.001
SEVERITY  | warning
DETAILS   | max duration of 172.16.5.40:10089 tidb get-token-duration is too slow
```

The following issues can be detected from the diagnostic result above:

* The first row indicates that the `172.16.5.40:4009` TiDB instance is restarted at `2020/03/26 00:05:45.670`.
* The second row indicates that the maximum `get-token-duration` time of the `172.16.5.40:10089` TiDB instance is 0.234s, but the expected time is less than 0.001s.

You can also specify conditions, for example, to query the `critical` level diagnostic results:

{{< copyable "sql" >}}

```sql
select * from information_schema.inspection_result where severity='critical';
```

Query only the diagnostic result of the `critical-error` rule:

{{< copyable "sql" >}}

```sql
select * from information_schema.inspection_result where rule='critical-error';
```

## Diagnostic rules

The diagnostic module contains a series of rules. These rules compare the results with the thresholds after querying the existing monitoring tables and cluster information tables. If the results exceed the thresholds, the diagnostics of `warning` or `critical` is generated and the corresponding information is provided in the `details` column.

You can query the existing diagnostic rules by querying the `inspection_rules` system table:

{{< copyable "sql" >}}

```sql
select * from information_schema.inspection_rules where type='inspection';
```

```sql
+-----------------+------------+---------+
| NAME            | TYPE       | COMMENT |
+-----------------+------------+---------+
| config          | inspection |         |
| version         | inspection |         |
| node-load       | inspection |         |
| critical-error  | inspection |         |
| threshold-check | inspection |         |
+-----------------+------------+---------+
```

### `config` diagnostic rule

In the `config` diagnostic rule, the following two diagnostic rules are executed by querying the `CLUSTER_CONFIG` system table:

* Check whether the configuration values of the same component are consistent. Not all configuration items has this consistency check. The white list of consistency check is as follows:

    ```go
    // The whitelist of the TiDB configuration consistency check
    port
    status.status-port
    host
    path
    advertise-address
    status.status-port
    log.file.filename
    log.slow-query-file
    tmp-storage-path

    // The whitelist of the PD configuration consistency check
    advertise-client-urls
    advertise-peer-urls
    client-urls
    data-dir
    log-file
    log.file.filename
    metric.job
    name
    peer-urls

    // The whitelist of the TiKV configuration consistency check
    server.addr
    server.advertise-addr
    server.status-addr
    log-file
    raftstore.raftdb-path
    storage.data-dir
    storage.block-cache.capacity
    ```

* Check whether the values of the following configuration items are as expected.

    |  Component  | Configuration item | Expected value |
    |  ----  | ----  |  ----  |
    | TiDB | log.slow-threshold | larger than `0` |
    | TiKV | raftstore.sync-log | `true` |

### `version` diagnostic rule

The `version` diagnostic rule checks whether the version hash of the same component is consistent by querying the `CLUSTER_INFO` system table. See the following example:

{{< copyable "sql" >}}

```sql
SELECT * FROM information_schema.inspection_result WHERE rule='version'\G
```

```sql
***************************[ 1. row ]***************************
RULE      | version
ITEM      | git_hash
TYPE      | tidb
INSTANCE  |
VALUE     | inconsistent
REFERENCE | consistent
SEVERITY  | critical
DETAILS   | the cluster has 2 different tidb versions, execute the sql to see more detail: SELECT * FROM information_schema.cluster_info WHERE type='tidb'
```

### `critical-error` diagnostic rule

In `critical-error` diagnostic rule, the following two diagnostic rules are executed:

* Detect whether the cluster has the following errors by querying the related monitoring system tables in the metrics schema:

    |  Component  | Error name | Monitoring table | Error description |
    |  ----  | ----  |  ----  |  ----  |
    | TiDB | panic-count | tidb_panic_count_total_count | Panic occurs in TiDB. |
    | TiDB | binlog-error | tidb_binlog_error_total_count | An error occurs when TiDB writes binlog. |
    | TiKV | critical-error | tikv_critical_error_total_coun | The critical error of TiKV. |
    | TiKV | scheduler-is-busy       | tikv_scheduler_is_busy_total_count | The TiKV scheduler is too busy, which makes TiKV temporarily unavailable. |
    | TiKV | coprocessor-is-busy | tikv_coprocessor_is_busy_total_count | The TiKV Coprocessor is too busy. |
    | TiKV | channel-is-full | tikv_channel_full_total_count | The "channel full" error occurs in TiKV. |
    | TiKV | tikv_engine_write_stall | tikv_engine_write_stall | The "stall" error occurs in TiKV. |

* Check whether any component is restarted by querying the `metrics_schema.up` monitoring table and the `CLUSTER_LOG` system table.

### `threshold-check` diagnostic rule

The `threshold-check` diagnostic rule checks whether the following metrics in the cluster exceed the threshold by querying the related monitoring system tables in the metrics schema:

|  Component  | Monitoring metric | Monitoring table | Expected value |  Description  |
|  :----  | :----  |  :----  |  :----  |  :----  |
| TiDB | tso-duration              | pd_tso_wait_duration                | < 50ms  |   The wait duration of getting the TSO of transaction. |
| TiDB | get-token-duration        | tidb_get_token_duration             | < 1ms   |  Queries the time it takes to get the token. The related TiDB configuration item is [`token-limit`](/command-line-flags-for-tidb-configuration.md#--token-limit).  |
| TiDB | load-schema-duration      | tidb_load_schema_duration           | < 1s    |   The time it takes for TiDB to update the schema metadata.|
| TiKV | scheduler-cmd-duration    | tikv_scheduler_command_duration     | < 0.1s  |  The time it takes for TiKV to execute the KV `cmd` request. |
| TiKV | handle-snapshot-duration  | tikv_handle_snapshot_duration       | < 30s   |  The time it takes for TiKV to handle the snapshot. |
| TiKV | storage-write-duration    | tikv_storage_async_request_duration | < 0.1s  |  The write latency of TiKV. |
| TiKV | storage-snapshot-duration | tikv_storage_async_request_duration | < 50ms  |  The time it takes for TiKV to get the snapshot. |
| TiKV | rocksdb-write-duration    | tikv_engine_write_duration          | < 100ms |  The write latency of TiKV RocksDB. |
| TiKV | rocksdb-get-duration | tikv_engine_max_get_duration | < 50ms |   The read latency of TiKV RocksDB. |
| TiKV | rocksdb-seek-duration | tikv_engine_max_seek_duration | < 50ms |  The latency of TiKV RocksDB to execute `seek`.   |
| TiKV | scheduler-pending-cmd-coun | tikv_scheduler_pending_commands  | < 1000 |  The number of commands stalled in TiKV.  |
| TiKV | index-block-cache-hit | tikv_block_index_cache_hit | > 0.95 |  The hit rate of index block cache in TiKV. |
| TiKV | filter-block-cache-hit | tikv_block_filter_cache_hit | > 0.95 |  The hit rate of filter block cache in TiKV. |
| TiKV | data-block-cache-hit | tikv_block_data_cache_hit | > 0.80 |  The hit rate of data block cache in TiKV. |
| TiKV | leader-score-balance | pd_scheduler_store_status  | < 0.05 |  Checks whether the leader score of each TiKV instance is balanced. The expected difference between instances is less than 5%. |
| TiKV | region-score-balance | pd_scheduler_store_status  | < 0.05 |  Checks whether the Region score of each TiKV instance is balanced. The expected difference between instances is less than 5%. |
| TiKV | store-available-balance | pd_scheduler_store_status  | < 0.2 | Checks whether the available storage of each TiKV instance is balanced. The expected difference between instances is less than 20%. |
| TiKV | region-count | pd_scheduler_store_status  | < 20000 |  Checks the number of Regions on each TiKV instance. The expected number of Regions in a single instance is less than 20,000. |
| PD | region-health | pd_region_health | < 100  |  Detects the number of Regions that are in the process of scheduling in the cluster. The expected number is less than 100 in total. |

In addition, this rule also checks whether the CPU usage of the following threads in a TiKV instance is too high:

* scheduler-worker-cpu
* coprocessor-normal-cpu
* coprocessor-high-cpu
* coprocessor-low-cpu
* grpc-cpu
* raftstore-cpu
* apply-cpu
* storage-readpool-normal-cpu
* storage-readpool-high-cpu
* storage-readpool-low-cpu
* split-check-cpu

The built-in diagnostic rules are constantly being improved. If you have more diagnostic rules, welcome to create a PR or an issue in the [`tidb` repository](https://github.com/pingcap/tidb).
