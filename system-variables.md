---
title: System Variables
summary: Use system variables to optimize performance or alter running behavior.
aliases: ['/tidb/dev/tidb-specific-system-variables','/docs/dev/system-variables/','/docs/dev/reference/configuration/tidb-server/mysql-variables/', '/docs/dev/tidb-specific-system-variables/','/docs/dev/reference/configuration/tidb-server/tidb-specific-variables/']
---

# System Variables

TiDB system variables behave similar to MySQL with some differences, in that settings might apply on a `SESSION`, `INSTANCE`, or `GLOBAL` scope, or on a scope that combines `SESSION`, `INSTANCE`, or `GLOBAL`.

- Changes to `GLOBAL` scoped variables **only apply to new connection sessions with TiDB**. Currently active connection sessions are not affected. These changes are persisted and valid after restarts.
- Changes to `INSTANCE` scoped variables apply to all active or new connection sessions with the current TiDB instance immediately after the changes are made. Other TiDB instances are not affected. These changes are not persisted and become invalid after TiDB restarts.

Variables can be set with the [`SET` statement](/sql-statements/sql-statement-set-variable.md) on a per-session, instance or global basis:

```sql
# These two identical statements change a session variable
SET tidb_distsql_scan_concurrency = 10;
SET SESSION tidb_distsql_scan_concurrency = 10;

# These two identical statements change a global variable
SET @@global.tidb_distsql_scan_concurrency = 10;
SET  GLOBAL tidb_distsql_scan_concurrency = 10;
```

> **Note:**
>
> TiDB differs from MySQL in that `GLOBAL` scoped variables **persist** through TiDB server restarts. Changes are also propagated to other TiDB servers every 2 seconds [TiDB #14531](https://github.com/pingcap/tidb/issues/14531).
> Additionally, TiDB presents several MySQL variables from MySQL 5.7 as both readable and settable. This is required for compatibility, since it is common for both applications and connectors to read MySQL variables. For example: JDBC connectors both read and set query cache settings, despite not relying on the behavior.

## Variable Reference

### autocommit

- Scope: SESSION | GLOBAL
- Default value: ON
- Controls whether statements should automatically commit when not in an explicit transaction. See [Transaction Overview](/transaction-overview.md#autocommit) for more information.

### `allow_auto_random_explicit_insert` <span class="version-mark">New in v4.0.3</span>

- Scope: SESSION (since v4.0.5: SESSION | GLOBAL)
- Default value: 0
- Determines whether to allow explicitly specifying the values of the column with the `AUTO_RANDOM` attribute in the `INSERT` statement. `1` means to allow and `0` means to disallow.

### ddl_slow_threshold

- Scope: INSTANCE
- Default value: 300
- DDL operations whose execution time exceeds the threshold value are output to the log. The unit is millisecond.

### foreign_key_checks

- Scope: NONE
- Default value: OFF
- For compatibility, TiDB returns foreign key checks as OFF.

### hostname

- Scope: NONE
- Default value: (system hostname)
- The hostname of the TiDB server as a read-only variable.

### innodb_lock_wait_timeout

- Scope: SESSION | GLOBAL
- Default value: 50
- The lock wait timeout for pessimistic transactions (default) in seconds.

### last_plan_from_cache <span class="version-mark">New in v4.0</span>

- Scope: SESSION
- Default value: 0
- This variable is used to show whether the execution plan used in the previous `execute` statement is taken directly from the plan cache.

### last_plan_from_binding <span class="version-mark">New in v4.0</span>

- Scope: SESSION
- Default value: 0
- This variable is used to show whether the execution plan used in the previous statement was influenced by a [plan binding](/sql-plan-management.md)

### max_execution_time

- Scope: SESSION | GLOBAL
- Default value: 0
- The maximum execution time of a statement in milliseconds. The default value is unlimited (zero).

> **Note:**
>
> Unlike in MySQL, the `max_execution_time` system variable currently works on all kinds of statements in TiDB, not only restricted to the `SELECT` statement. The precision of the timeout value is roughly 100ms. This means the statement might not be terminated in accurate milliseconds as you specify.

### interactive_timeout

- Scope: SESSION | GLOBAL
- Default value: 28800
- This variable represents the idle timeout of the interactive user session, which is measured in seconds. Interactive user session refers to the session established by calling [`mysql_real_connect()`](https://dev.mysql.com/doc/c-api/5.7/en/mysql-real-connect.html) API using the `CLIENT_INTERACTIVE` option (for example, MySQL shell client). This variable is fully compatible with MySQL.

### sql_mode

- Scope: SESSION | GLOBAL
- Default value: `ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION`
- This variable controls a number of MySQL compatibility behaviors. See [SQL Mode](/sql-mode.md) for more information.

### sql_select_limit <span class="version-mark">New in v4.0.2 version</span>

- Scope: SESSION | GLOBAL
- Default value: `2^64 - 1` (18446744073709551615)
- The maximum number of rows returned by the `SELECT` statements.

### tidb_allow_batch_cop <span class="version-mark">New in v4.0 version</span>

- Scope: SESSION | GLOBAL
- Default value: 0
- This variable is used to control how TiDB sends a coprocessor request to TiFlash. It has the following values:

    * `0`: Never send requests in batches
    * `1`: Aggregation and join requests are sent in batches
    * `2`: All coprocessor requests are sent in batches

### tidb_allow_remove_auto_inc <span class="version-mark">New in v2.1.18 and v3.0.4</span>

- Scope: SESSION
- Default value: 0
- This variable is used to set whether the `AUTO_INCREMENT` property of a column is allowed to be removed by executing `ALTER TABLE MODIFY` or `ALTER TABLE CHANGE` statements. It is not allowed by default.

### tidb_auto_analyze_end_time

- Scope: GLOBAL
- Default value: 23:59 +0000
- This variable is used to restrict the time window that the automatic update of statistics is permitted. For example, to only allow automatic statistics updates between 1AM and 3AM, set `tidb_auto_analyze_start_time='01:00 +0000'` and `tidb_auto_analyze_end_time='03:00 +0000'`.

### tidb_auto_analyze_ratio

- Scope: GLOBAL
- Default value: 0.5
- This variable is used to set the threshold when TiDB automatically executes [`ANALYZE TABLE`](/sql-statements/sql-statement-analyze-table.md) in a background thread to update table statistics. For example, a value of 0.5 means that auto-analyze is triggered when greater than 50% of the rows in a table have been modified. Auto-analyze can be restricted to only execute during certain hours of the day by specifying `tidb_auto_analyze_start_time` and `tidb_auto_analyze_end_time`.

> **Note:**
>
> Only when the `run-auto-analyze` option is enabled in the starting configuration file of TiDB, the `auto_analyze` feature can be triggered.

### tidb_auto_analyze_start_time

- Scope: GLOBAL
- Default value: 00:00 +0000
- This variable is used to restrict the time window that the automatic update of statistics is permitted. For example, to only allow automatic statistics updates between 1AM and 3AM, set `tidb_auto_analyze_start_time='01:00 +0000'` and `tidb_auto_analyze_end_time='03:00 +0000'`.

### tidb_backoff_lock_fast

- Scope: SESSION | GLOBAL
- Default value: 100
- This variable is used to set the `backoff` time when the read request meets a lock.

### tidb_backoff_weight

- Scope: SESSION | GLOBAL
- Default value: 2
- This variable is used to increase the weight of the maximum time of TiDB `backoff`, that is, the maximum retry time for sending a retry request when an internal network or other component (TiKV, PD) failure is encountered. This variable can be used to adjust the maximum retry time and the minimum value is 1.

    For example, the base timeout for TiDB to take TSO from PD is 15 seconds. When `tidb_backoff_weight = 2`, the maximum timeout for taking TSO is: *base time \* 2 = 30 seconds*.

    In the case of a poor network environment, appropriately increasing the value of this variable can effectively alleviate error reporting to the application end caused by timeout. If the application end wants to receive the error information more quickly, minimize the value of this variable.

### tidb_build_stats_concurrency

- Scope: SESSION
- Default value: 4
- This variable is used to set the concurrency of executing the `ANALYZE` statement.
- When the variable is set to a larger value, the execution performance of other queries is affected.

### tidb_capture_plan_baselines <span class="version-mark">New in v4.0</span>

- Scope: SESSION | GLOBAL
- Default value: off
- This variable is used to control whether to enable the [baseline capturing](/sql-plan-management.md#baseline-capturing) feature. This feature depends on the statement summary, so you need to enable the statement summary before you use baseline capturing.
- After this feature is enabled, the historical SQL statements in the statement summary are traversed periodically, and bindings are automatically created for SQL statements that appear at least twice.

### tidb_check_mb4_value_in_utf8

- Scope: INSTANCE
- Default value: 1, indicating check the validity of UTF-8 data. This default behavior is compatible with MySQL.
- This variable is used to set whether to check the validity of UTF-8 data.
- To upgrade an earlier version (TiDB v2.1.1 or earlier), you may need to disable this option. Otherwise, you can successfully write invalid strings in an earlier version but fail to do this in a later version, because there is no data validity check in the earlier version. For details, see [FAQs After Upgrade](/faq/upgrade-faq.md).

### tidb_checksum_table_concurrency

- Scope: SESSION
- Default value: 4
- This variable is used to set the scan index concurrency of executing the `ADMIN CHECKSUM TABLE` statement.
- When the variable is set to a larger value, the execution performance of other queries is affected.

### tidb_config

- Scope: SESSION
- Default value: ""
- This variable is read-only. It is used to obtain the configuration information of the current TiDB server.

### tidb_constraint_check_in_place

- Scope: SESSION | GLOBAL
- Default value: 0
- This setting only applies to optimistic transactions. When this variable is set to zero, checking for duplicate values in UNIQUE indexes is deferred until the transaction commits. This helps improve performance, but might be an unexpected behavior for some applications. See [Constraints](/constraints.md) for details.

    - When set to zero and using optimistic transactions:

        ```sql
        tidb> create table t (i int key);
        tidb> insert into t values (1);
        tidb> begin optimistic;
        tidb> insert into t values (1);
        Query OK, 1 row affected
        tidb> commit; -- Check only when a transaction is committed.
        ERROR 1062 : Duplicate entry '1' for key 'PRIMARY'
        ```

    - When set to 1 and using optimistic transactions:

        ```sql
        tidb> set @@tidb_constraint_check_in_place=1;
        tidb> begin optimistic;
        tidb> insert into t values (1);
        ERROR 1062 : Duplicate entry '1' for key 'PRIMARY'
        ```

Constraint checking is always performed in place for pessimistic transactions (default).

### tidb_current_ts

- Scope: SESSION
- Default value: 0
- This variable is read-only. It is used to obtain the timestamp of the current transaction.

### tidb_ddl_error_count_limit

- Scope: GLOBAL
- Default value: 512
- This variable is used to set the number of retries when the DDL operation fails. When the number of retries exceeds the parameter value, the wrong DDL operation is canceled.

### tidb_ddl_reorg_batch_size

- Scope: GLOBAL
- Default value: 256
- This variable is used to set the batch size during the `re-organize` phase of the DDL operation. For example, when TiDB executes the `ADD INDEX` operation, the index data needs to backfilled by `tidb_ddl_reorg_worker_cnt` (the number) concurrent workers. Each worker backfills the index data in batches.
    - If many updating operations such as `UPDATE` and `REPLACE` exist during the `ADD INDEX` operation, a larger batch size indicates a larger probability of transaction conflicts. In this case, you need to adjust the batch size to a smaller value. The minimum value is 32.
    - If the transaction conflict does not exist, you can set the batch size to a large value. The maximum value is 10240. This can increase the speed of the backfilling data, but the write pressure on TiKV also becomes higher.

### tidb_ddl_reorg_priority

- Scope: SESSION | GLOBAL
- Default value: `PRIORITY_LOW`
- This variable is used to set the priority of executing the `ADD INDEX` operation in the `re-organize` phase.
- You can set the value of this variable to `PRIORITY_LOW`, `PRIORITY_NORMAL` or `PRIORITY_HIGH`.

### tidb_ddl_reorg_worker_cnt

- Scope: GLOBAL
- Default value: 4
- This variable is used to set the concurrency of the DDL operation in the `re-organize` phase.

### tidb_disable_txn_auto_retry

- Scope: SESSION | GLOBAL
- Default: on
- This variable is used to set whether to disable the automatic retry of explicit transactions. The default value of `on` means that transactions will not automatically retry in TiDB and `COMMIT` statements might return errors that need to be handled in the application layer.

    Setting the value to `off` means that TiDB will automatically retry transactions, resulting in fewer errors from `COMMIT` statements. Be careful when making this change, because it might result in lost updates.

    This variable does not affect automatically committed implicit transactions and internally executed transactions in TiDB. The maximum retry count of these transactions is determined by the value of `tidb_retry_limit`.

    For more details, see [limits of retry](/optimistic-transaction.md#limits-of-retry).

### tidb_distsql_scan_concurrency

- Scope: SESSION | GLOBAL
- Default value: 15
- This variable is used to set the concurrency of the `scan` operation.
- Use a bigger value in OLAP scenarios, and a smaller value in OLTP scenarios.
- For OLAP scenarios, the maximum value cannot exceed the number of CPU cores of all the TiKV nodes.

### tidb_dml_batch_size

- Scope: SESSION | GLOBAL
- Default value: 0
- When this value is greater than `0`, TiDB will batch commit statements such as `INSERT` or `LOAD DATA` into smaller transactions. This reduces memory usage and helps ensure that the `txn-total-size-limit` is not reached by bulk modifications.
- Only the value `0` provides ACID compliance. Setting this to any other value will break the atomicity and isolation guarantees of TiDB.

### tidb_enable_cascades_planner

- Scope: SESSION | GLOBAL
- Default value: 0
- This variable is used to control whether to enable the cascades planner, which is currently considered experimental.

### tidb_enable_clustered_index <!-- New in v5.0 -->

- Scope: SESSION | GLOBAL
- Default value: 1
- This variable is used to control whether to enable the clustered index feature.
    - This feature is only applicable to newly created tables and does not affect the existing old tables.
    - This feature is only applicable to tables whose primary key is the single-column non-integer type or the multi-column type. It does not affect the tables without a primary key or tables with the primary key of the single-column non-integer type.
    - You can execute `select tidb_pk_type from information_schema.tables where table_name ='{table_name}'` to check whether the clustered index feature has been enabled on a table.
- After you enable this feature, rows are stored directly on the primary key instead of on the internally allocated `rows_id` to which the extra primary key index is created to point.

    This feature impacts performance in the following aspects:
    - For each `INSERT` operation, there is one less index key written into each row.
    - When you make a query using the primary key as the equivalent condition, one read request can be saved.
    - When you make a query using the primary key as the range condition, multiple read requests can be saved.
    - When you make a query using the prefix of the multi-column primary key as the equivalent condition or range condition, multiple read requests can be saved.

### tidb_enable_chunk_rpc <span class="version-mark">New in v4.0</span>

- Scope: SESSION
- Default value: 1
- This variable is used to control whether to enable the `Chunk` data encoding format in Coprocessor.

### tidb_enable_fast_analyze

- Scope: SESSION | GLOBAL
- Default value: 0, indicating not enabling the statistics fast `Analyze` feature.
- This variable is used to set whether to enable the statistics `Fast Analyze` feature.
- If the statistics `Fast Analyze` feature is enabled, TiDB randomly samples about 10,000 rows of data as statistics. When the data is distributed unevenly or the data size is small, the statistics accuracy is low. This might lead to a non-optimal execution plan, for example, selecting a wrong index. If the execution time of the regular `Analyze` statement is acceptable, it is recommended to disable the `Fast Analyze` feature.

### tidb_enable_index_merge <span class="version-mark">New in v4.0</span>

- Scope: SESSION | GLOBAL
- Default value: 0
- This variable is used to control whether to enable the index merge feature.

### tidb_enable_noop_functions <span class="version-mark">New in v4.0</span>

- Scope: SESSION | GLOBAL
- Default value: 0
- By default, TiDB returns an error when you attempt to use the syntax for functionality that is not yet implemented. When the variable value is set to `1`, TiDB silently ignores such cases of unavailable functionality, which is helpful if you cannot make changes to the SQL code.
- Enabling `noop` functions controls the following behaviors:
    * `get_lock` and `release_lock` functions
    * `LOCK IN SHARE MODE` syntax
    * `SQL_CALC_FOUND_ROWS` syntax

> **Note:**
>
> Only the default value of `0` can be considered safe. Setting `tidb_enable_noop_functions=1` might lead to unexpected behaviors in your application, because it permits TiDB to ignore certain syntax without providing an error.

### tidb_enable_slow_log

- Scope: INSTANCE
- Default value: `1`
- This variable is used to control whether to enable the slow log feature. It is enabled by default.

### tidb_enable_stmt_summary <span class="version-mark">New in v3.0.4</span>

- Scope: SESSION | GLOBAL
- Default value: 1 (the value of the default configuration file)
- This variable is used to control whether to enable the statement summary feature. If enabled, SQL execution information like time consumption is recorded to the `information_schema.STATEMENTS_SUMMARY` system table to identify and troubleshoot SQL performance issues.

### tidb_enable_streaming

- Scope: SERVER
- Default value: 0
- This variable is used to set whether to enable streaming.

### tidb_enable_table_partition

- Scope: SESSION | GLOBAL
- Default value: "on"
- This variable is used to set whether to enable the `TABLE PARTITION` feature.
    - `off` indicates disabling the `TABLE PARTITION` feature. In this case, the syntax that creates a partition table can be executed, but the table created is not a partitioned one.
    - `on` indicates enabling the `TABLE PARTITION` feature for the supported partition types. Currently, it indicates enabling range partition, hash partition and range column partition with one single column.
    - `auto` functions the same way as `on` does.

- Currently, TiDB only supports range partition and hash partition.

### tidb_enable_telemetry <span class="version-mark">New in v4.0.2 version</span>

- Scope: GLOBAL
- Default value: 1
- This variable is used to dynamically control whether the telemetry collection in TiDB is enabled. By setting the value to `0`, the telemetry collection is disabled. If the [`enable-telemetry`](/tidb-configuration-file.md#enable-telemetry-new-in-v402) TiDB configuration item is set to `false` on all TiDB instances, the telemetry collection is always disabled and this system variable will not take effect. See [Telemetry](/telemetry.md) for details.

### tidb_enable_vectorized_expression <span class="version-mark">New in v4.0</span>

- Scope: SESSION | GLOBAL
- Default value: 1
- This variable is used to control whether to enable vectorized execution.

### tidb_enable_window_function

- Scope: SESSION | GLOBAL
- Default value: 1, indicating enabling the window function feature.
- This variable is used to control whether to enable the support for window functions. Note that window functions may use reserved keywords. This might cause SQL statements that could be executed normally cannot be parsed after upgrading TiDB. In this case, you can set `tidb_enable_window_function` to `0`.

### tidb_evolve_plan_baselines <span class="version-mark">New in v4.0</span>

- Scope: SESSION | GLOBAL
- Default value: off
- This variable is used to control whether to enable the baseline evolution feature. For detailed introduction or usage , see [Baseline Evolution](/sql-plan-management.md#baseline-evolution).
- To reduce the impact of baseline evolution on the cluster, use the following configurations:
    - Set `tidb_evolve_plan_task_max_time` to limit the maximum execution time of each execution plan. The default value is 600s.
    - Set `tidb_evolve_plan_task_start_time` and `tidb_evolve_plan_task_end_time` to limit the time window. The default values are respectively `00:00 +0000` and `23:59 +0000`.

### tidb_evolve_plan_task_end_time <span class="version-mark">New in v4.0</span>

- Scope: GLOBAL
- Default value: 23:59 +0000
- This variable is used to set the end time of baseline evolution in a day.

### tidb_evolve_plan_task_max_time <span class="version-mark">New in v4.0</span>

- Scope: GLOBAL
- Default value: 600
- This variable is used to limit the maximum execution time of each execution plan in the baseline evolution feature. The unit is second.

### tidb_evolve_plan_task_start_time <span class="version-mark">New in v4.0</span>

- Scope: GLOBAL
- Default value: 00:00 +0000
- This variable is used to set the start time of baseline evolution in a day.

### tidb_expensive_query_time_threshold

- Scope: INSTANCE
- Default value: 60
- This variable is used to set the threshold value that determines whether to print expensive query logs. The unit is second. The difference between expensive query logs and slow query logs is:
    - Slow logs are printed after the statement is executed.
    - Expensive query logs print the statements that are being executed, with execution time exceeding the threshold value, and their related information.

### tidb_force_priority

- Scope: INSTANCE
- Default value: `NO_PRIORITY`
- This variable is used to change the default priority for statements executed on a TiDB server. A use case is to ensure that a particular user that is performing OLAP queries receives lower priority than users performing OLTP queries.
- You can set the value of this variable to `NO_PRIORITY`, `LOW_PRIORITY`, `DELAYED` or `HIGH_PRIORITY`.

### tidb_general_log

- Scope: INSTANCE
- Default value: 0
- This variable is used to set whether to record all the SQL statements in the log.

### tidb_hash_join_concurrency

- Scope: SESSION | GLOBAL
- Default value: 5
- This variable is used to set the concurrency of the `hash join` algorithm.

### tidb_hashagg_final_concurrency

- Scope: SESSION | GLOBAL
- Default value: 4
- This variable is used to set the concurrency of executing the concurrent `hash aggregation` algorithm in the `final` phase.
- When the parameter of the aggregate function is not distinct, `HashAgg` is run concurrently and respectively in two phases - the `partial` phase and the `final` phase.

### tidb_hashagg_partial_concurrency

- Scope: SESSION | GLOBAL
- Default value: 4
- This variable is used to set the concurrency of executing the concurrent `hash aggregation` algorithm in the `partial` phase.
- When the parameter of the aggregate function is not distinct, `HashAgg` is run concurrently and respectively in two phases - the `partial` phase and the `final` phase.

### tidb_index_join_batch_size

- Scope: SESSION | GLOBAL
- Default value: 25000
- This variable is used to set the batch size of the `index lookup join` operation.
- Use a bigger value in OLAP scenarios, and a smaller value in OLTP scenarios.

### tidb_index_lookup_concurrency

- Scope: SESSION | GLOBAL
- Default value: 4
- This variable is used to set the concurrency of the `index lookup` operation.
- Use a bigger value in OLAP scenarios, and a smaller value in OLTP scenarios.

### tidb_index_lookup_join_concurrency

- Scope: SESSION | GLOBAL
- Default value: 4
- This variable is used to set the concurrency of the `index lookup join` algorithm.

### tidb_index_lookup_size

- Scope: SESSION | GLOBAL
- Default value: 20000
- This variable is used to set the batch size of the `index lookup` operation.
- Use a bigger value in OLAP scenarios, and a smaller value in OLTP scenarios.

### tidb_index_serial_scan_concurrency

- Scope: SESSION | GLOBAL
- Default value: 1
- This variable is used to set the concurrency of the `serial scan` operation.
- Use a bigger value in OLAP scenarios, and a smaller value in OLTP scenarios.

### tidb_init_chunk_size

- Scope: SESSION | GLOBAL
- Default value: 32
- Range: 1 - 32
- This variable is used to set the number of rows for the initial chunk during the execution process.

### tidb_isolation_read_engines <span class="version-mark">New in v4.0</span>

- Scope: SESSION
- Default value: tikv, tiflash, tidb
- This variable is used to set the storage engine list that TiDB can use when reading data.

### tidb_low_resolution_tso

- Scope: SESSION
- Default value: 0
- This variable is used to set whether to enable the low precision TSO feature. After this feature is enabled, new transactions use a timestamp updated every 2 seconds to read data.
- The main applicable scenario is to reduce the overhead of acquiring TSO for small read-only transactions when reading old data is acceptable.

### tidb_max_chunk_size

- Scope: SESSION | GLOBAL
- Default value: 1024
- Minimum value: 32
- This variable is used to set the maximum number of rows in a chunk during the execution process. Setting to too large of a value may cause cache locality issues.

### tidb_max_delta_schema_count <span class="version-mark">New in v2.1.18 and v3.0.5</span>

- Scope: GLOBAL
- Default value: 1024
- This variable is used to set the maximum number of schema versions (the table IDs modified for corresponding versions) allowed to be cached. The value range is 100 ~ 16384.

### tidb_mem_quota_query

- Scope: SESSION
- Default value: 1 GB
- This variable is used to set the threshold value of memory quota for a query.
- If the memory quota of a query during execution exceeds the threshold value, TiDB performs the operation designated by the OOMAction option in the configuration file. The initial value of this variable is configured by [`mem-quota-query`](/tidb-configuration-file.md#mem-quota-query).

### tidb_metric_query_range_duration <span class="version-mark">New in v4.0</span>

- Scope: SESSION
- Default value: 60
- This variable is used to set the range duration of the Prometheus statement generated when querying METRIC_SCHEMA. The unit is second.

### tidb_metric_query_step <span class="version-mark">New in v4.0</span>

- Scope: SESSION
- Default value: 60
- This variable is used to set the step of the Prometheus statement generated when querying `METRIC_SCHEMA`. The unit is second.

### tidb_opt_agg_push_down

- Scope: SESSION
- Default value: 0
- This variable is used to set whether the optimizer executes the optimization operation of pushing down the aggregate function to the position before Join.
- When the aggregate operation is slow in query, you can set the variable value to 1.

### tidb_opt_correlation_exp_factor

- Scope: SESSION | GLOBAL
- Default value: 1
- When the method that estimates the number of rows based on column order correlation is not available, the heuristic estimation method is used. This variable is used to control the behavior of the heuristic method.
    - When the value is 0, the heuristic method is not used.
    - When the value is greater than 0:
        - A larger value indicates that an index scan will probably be used in the heuristic method.
        - A smaller value indicates that a table scan will probably be used in the heuristic method.

### tidb_opt_correlation_threshold

- Scope: SESSION | GLOBAL
- Default value: 0.9
- This variable is used to set the threshold value that determines whether to enable estimating the row count by using column order correlation. If the order correlation between the current column and the `handle` column exceeds the threshold value, this method is enabled.

### tidb_opt_distinct_agg_push_down

- Scope: SESSION
- Default value: 0
- This variable is used to set whether the optimizer executes the optimization operation of pushing down the aggregate function with `distinct` (such as `select count(distinct a) from t`) to Coprocessor.
- When the aggregate function with the `distinct` operation is slow in the query, you can set the variable value to `1`.

In the following example, before `tidb_opt_distinct_agg_push_down` is enabled, TiDB needs to read all data from TiKV and execute `distinct` on the TiDB side. After `tidb_opt_distinct_agg_push_down` is enabled, `distinct a` is pushed down to Coprocessor, and a `group by` column `test.t.a` is added to `HashAgg_5`.

```sql
mysql> desc select count(distinct a) from test.t;
+-------------------------+----------+-----------+---------------+------------------------------------------+
| id                      | estRows  | task      | access object | operator info                            |
+-------------------------+----------+-----------+---------------+------------------------------------------+
| StreamAgg_6             | 1.00     | root      |               | funcs:count(distinct test.t.a)->Column#4 |
| └─TableReader_10        | 10000.00 | root      |               | data:TableFullScan_9                     |
|   └─TableFullScan_9     | 10000.00 | cop[tikv] | table:t       | keep order:false, stats:pseudo           |
+-------------------------+----------+-----------+---------------+------------------------------------------+
3 rows in set (0.01 sec)

mysql> set session tidb_opt_distinct_agg_push_down = 1;
Query OK, 0 rows affected (0.00 sec)

mysql> desc select count(distinct a) from test.t;
+---------------------------+----------+-----------+---------------+------------------------------------------+
| id                        | estRows  | task      | access object | operator info                            |
+---------------------------+----------+-----------+---------------+------------------------------------------+
| HashAgg_8                 | 1.00     | root      |               | funcs:count(distinct test.t.a)->Column#3 |
| └─TableReader_9           | 1.00     | root      |               | data:HashAgg_5                           |
|   └─HashAgg_5             | 1.00     | cop[tikv] |               | group by:test.t.a,                       |
|     └─TableFullScan_7     | 10000.00 | cop[tikv] | table:t       | keep order:false, stats:pseudo           |
+---------------------------+----------+-----------+---------------+------------------------------------------+
4 rows in set (0.00 sec)
```

### tidb_opt_insubq_to_join_and_agg

- Scope: SESSION | GLOBAL
- Default value: 1
- This variable is used to set whether to enable the optimization rule that converts a subquery to join and aggregation.
- For example, after you enable this optimization rule, the subquery is converted as follows:

    ```sql
    select * from t where t.a in (select aa from t1)
    ```

    The subquery is converted to join as follows:

    ```sql
    select * from t, (select aa from t1 group by aa) tmp_t where t.a = tmp_t.aa
    ```

    If `t1` is limited to be `unique` and `not null` in the `aa` column. You can use the following statement, without aggregation.

    ```sql
    select * from t, t1 where t.a=t1.a
    ```

### tidb_opt_write_row_id

- Scope: SESSION
- Default value: 0
- This variable is used to set whether to allow `insert`, `replace` and `update` statements to operate on the column `_tidb_rowid`. It is not allowed by default. This variable can be used only when importing data with TiDB tools.

### tidb_projection_concurrency

- Scope: SESSION | GLOBAL
- Default value: 4
- This variable is used to set the concurrency of the `Projection` operator.

### tidb_query_log_max_len

- Scope: INSTANCE
- Default value: 4096 (bytes)
- The maximum length of the SQL statement output. When the output length of a statement is larger than the `tidb_query-log-max-len` value, the statement is truncated to output.

Usage example:

```sql
set tidb_query_log_max_len = 20
```

### tidb_pprof_sql_cpu <span class="version-mark">New in v4.0</span>

- Scope: INSTANCE
- Default value: 0
- This variable is used to control whether to mark the corresponding SQL statement in the profile output to identify and troubleshoot performance issues.

### tidb_record_plan_in_slow_log

- Scope: INSTANCE
- Default value: `1`
- This variable is used to control whether to include the execution plan of slow queries in the slow log.

### tidb_replica_read <span class="version-mark">New in v4.0</span>

- Scope: SESSION
- Default value: leader
- This variable is used to control where TiDB reads data. Here are three options:
    - leader: Read only from leader node
    - follower: Read only from follower node
    - leader-and-follower: Read from leader or follower node
- See [follower reads](/follower-read.md) for additional details.

### tidb_retry_limit

- Scope: SESSION | GLOBAL
- Default value: 10
- This variable is used to set the maximum number of the retries. When a transaction encounters retryable errors (such as transaction conflicts, very slow transaction commit, or table schema changes), this transaction is re-executed according to this variable. Note that setting `tidb_retry_limit` to `0` disables the automatic retry.

### tidb_row_format_version

- Scope: GLOBAL
- Default value: `2`
- Controls the format version of the newly saved data in the table. In TiDB v4.0, the [new storage row format](https://github.com/pingcap/tidb/blob/master/docs/design/2018-07-19-row-format.md) version `2` is used by default to save new data.
- If you upgrade from a TiDB version earlier than 4.0.0 to 4.0.0, the format version is not changed, and TiDB continues to use the old format of version `1` to write data to the table, which means that **only newly created clusters use the new data format by default**.
- Note that modifying this variable does not affect the old data that has been saved, but applies the corresponding version format only to the newly written data after modifying this variable.

### tidb_scatter_region

- Scope: GLOBAL
- Default value: 0
- By default, Regions are split for a new table when it is being created in TiDB. After this variable is enabled, the newly split Regions are scattered immediately during the execution of the `CREATE TABLE` statement. This applies to the scenario where data need to be written in batches right after the tables are created in batches, because the newly split Regions can be scattered in TiKV beforehand and do not have to wait to be scheduled by PD. To ensure the continuous stability of writing data in batches, the `CREATE TABLE` statement returns success only after the Regions are successfully scattered. This makes the statement's execution time multiple times longer than that when you disable this variable.

### tidb_skip_isolation_level_check

- Scope: SESSION
- Default value: 0
- After this switch is enabled, if an isolation level unsupported by TiDB is assigned to `tx_isolation`, no error is reported. This helps improve compatibility with applications that set (but do not depend on) a different isolation level.

```sql
tidb> set tx_isolation='serializable';
ERROR 8048 (HY000): The isolation level 'serializable' is not supported. Set tidb_skip_isolation_level_check=1 to skip this error
tidb> set tidb_skip_isolation_level_check=1;
Query OK, 0 rows affected (0.00 sec)

tidb> set tx_isolation='serializable';
Query OK, 0 rows affected, 1 warning (0.00 sec)
```

### tidb_skip_utf8_check

- Scope: SESSION | GLOBAL
- Default value: 0
- This variable is used to set whether to skip UTF-8 validation.
- Validating UTF-8 characters affects the performance. When you are sure that the input characters are valid UTF-8 characters, you can set the variable value to 1.

### tidb_slow_log_threshold

- Scope: INSTANCE
- Default value: 300ms
- This variable is used to output the threshold value of the time consumed by the slow log. When the time consumed by a query is larger than this value, this query is considered as a slow log and its log is output to the slow query log.

Usage example:

```sql
SET tidb_slow_log_threshold = 200;
```

### tidb_enable_collect_execution_info

- Scope: INSTANCE
- Default value: 1
- This variable controls whether to record the execution information of each operator in the slow query log.

### tidb_log_desensitization

- Scope: GLOBAL
- Default value: 0
- This variable controls whether to hide user information in the SQL statement being recorded into the TiDB log and slow log.
- When you set the variable to `1`, user information is hidden. For example, if the executed SQL statement is `insert into t values (1,2)`, the statement is recorded as `insert into t values (?,?)` in the log.

### tidb_slow_query_file

- Scope: SESSION
- Default value: ""
- When `INFORMATION_SCHEMA.SLOW_QUERY` is queried, only the slow query log name set by `slow-query-file` in the configuration file is parsed. The default slow query log name is "tidb-slow.log". To parse other logs, set the `tidb_slow_query_file` session variable to a specific file path, and then query `INFORMATION_SCHEMA.SLOW_QUERY` to parse the slow query log based on the set file path. For details, see [Identify Slow Queries](/identify-slow-queries.md).

### tidb_snapshot

- Scope: SESSION
- Default value: ""
- This variable is used to set the time point at which the data is read by the session. For example, when you set the variable to "2017-11-11 20:20:20" or a TSO number like "400036290571534337", the current session reads the data of this moment.

### tidb_stmt_summary_history_size <span class="version-mark">New in v4.0</span>

- Scope: SESSION | GLOBAL
- Default value: 24 (the value of the default configuration file)
- This variable is used to set the history capacity of the statement summary.

### tidb_stmt_summary_internal_query <span class="version-mark">New in v4.0</span>

- Scope: SESSION | GLOBAL
- Default value: 0 (the value of the default configuration file)
- This variable is used to control whether to include the SQL information of TiDB in the statement summary.

### tidb_stmt_summary_max_sql_length <span class="version-mark">New in v4.0</span>

- Scope: SESSION | GLOBAL
- Default value: 4096 (the value of the default configuration file)
- This variable is used to control the length of the SQL string in the statement summary.

### tidb_stmt_summary_max_stmt_count <span class="version-mark">New in v4.0</span>

- Scope: SESSION | GLOBAL
- Default value: 200 (the value of the default configuration file)
- This variable is used to set the maximum number of statements that the statement summary stores in memory.

### tidb_stmt_summary_refresh_interval <span class="version-mark">New in v4.0</span>

- Scope: SESSION | GLOBAL
- Default value: 1800 (the value of the default configuration file)
- This variable is used to set the refresh time of the statement summary. The unit is second.

### tidb_store_limit <span class="version-mark">New in v3.0.4 and v4.0</span>

- Scope: INSTANCE | GLOBAL
- Default value: 0
- This variable is used to limit the maximum number of requests TiDB can send to TiKV at the same time. 0 means no limit.

### tidb_txn_mode

- Scope: SESSION | GLOBAL
- Default value: "pessimistic"
- This variable is used to set the transaction mode. TiDB 3.0 supports the pessimistic transactions. Since TiDB 3.0.8, the [pessimistic transaction mode](/pessimistic-transaction.md) is enabled by default.
- If you upgrade TiDB from v3.0.7 or earlier versions to v3.0.8 or later versions, the default transaction mode does not change. **Only the newly created clusters use the pessimistic transaction mode by default**.
- If this variable is set to "optimistic" or "", TiDB uses the [optimistic transaction mode](/optimistic-transaction.md).

### tidb_use_plan_baselines <span class="version-mark">New in v4.0</span>

- Scope: SESSION | GLOBAL
- Default value: on
- This variable is used to control whether to enable the execution plan binding feature. It is enabled by default, and can be disabled by assigning the `off` value. For the use of the execution plan binding, see [Execution Plan Binding](/sql-plan-management.md#create-a-binding).

### tidb_wait_split_region_finish

- Scope: SESSION
- Default value: 1, indicating returning the result after all Regions are scattered.
- It usually takes a long time to scatter Regions, which is determined by PD scheduling and TiKV loads. This variable is used to set whether to return the result to the client after all Regions are scattered completely when the `SPLIT REGION` statement is being executed. Value `0` indicates returning the value before finishing scattering all Regions.
- Note that when scattering Regions, the write and read performances for the Region that is being scattered might be affected. In batch-write or data importing scenarios, it is recommended to import data after Regions scattering is finished.

### tidb_wait_split_region_timeout

- Scope: SESSION
- Default value: 300
- This variable is used to set the timeout for executing the `SPLIT REGION` statement. The unit is second. If a statement is not executed completely within the specified time value, a timeout error is returned.

### tidb_window_concurrency <span class="version-mark">New in v4.0</span>

- Scope: SESSION | GLOBAL
- Default value: 4
- This variable is used to set the concurrency degree of the window operator.

### time_zone

- Scope: SESSION | GLOBAL
- Default value: SYSTEM
- This variable sets the system time zone. Values can be specified as either an offset such as '-8:00' or a named zone 'America/Los_Angeles'.

### transaction_isolation

- Scope: SESSION | GLOBAL
- Default value: REPEATABLE-READ
- This variable sets the transaction isolation. TiDB advertises `REPEATABLE-READ` for compatibility with MySQL, but the actual isolation level is Snapshot Isolation. See [transaction isolation levels](/transaction-isolation-levels.md) for further details.

### tx_isolation

This variable is an alias for _transaction_isolation_.

### version

- Scope: NONE
- Default value: 5.7.25-TiDB-(tidb version)
- This variable returns the MySQL version, followed by the TiDB version. For example '5.7.25-TiDB-v4.0.0-beta.2-716-g25e003253'.

### version_comment

- Scope: NONE
- Default value: (string)
- This variable returns additional details about the TiDB version. For example, 'TiDB Server (Apache License 2.0) Community Edition, MySQL 5.7 compatible'.

### wait_timeout

- Scope: SESSION | GLOBAL
- Default value: 0
- This variable controls the idle timeout of user sessions in seconds. A zero-value means unlimited.

### windowing_use_high_precision

- Scope: SESSION | GLOBAL
- Default value: ON
- This variable controls whether to use the high precision mode when computing the window functions.
