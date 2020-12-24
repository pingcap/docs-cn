---
title: TiDB Configuration File
summary: Learn the TiDB configuration file options that are not involved in command line options.
aliases: ['/docs/dev/tidb-configuration-file/','/docs/dev/reference/configuration/tidb-server/configuration-file/']
---

<!-- markdownlint-disable MD001 -->
<!-- markdownlint-disable MD024 -->

# TiDB Configuration File

The TiDB configuration file supports more options than command-line parameters. You can download the default configuration file [`config.toml.example`](https://github.com/pingcap/tidb/blob/master/config/config.toml.example) and rename it to `config.toml`. This document describes only the options that are not involved in [command line options](/command-line-flags-for-tidb-configuration.md).

### `split-table`

- Determines whether to create a separate Region for each table.
- Default value: `true`
- It is recommended to set it to `false` if you need to create a large number of tables.

### `token-limit`

+ The number of sessions that can execute requests concurrently.
+ Default value: `1000`

### `mem-quota-query`

- The maximum memory available for a single SQL statement.
- Default value: `1073741824` (in bytes)
- Note: When you upgrade the cluster from v2.0.x or v3.0.x to v4.0.9 or later versions, the default value of this configuration is `34359738368`.
- Requests that require more memory than this value are handled based on the behavior defined by `oom-action`.
- This value is the initial value of the system variable [`tidb_mem_quota_query`](/system-variables.md#tidb_mem_quota_query).

### `oom-use-tmp-storage`

+ Controls whether to enable the temporary storage for some operators when a single SQL statement exceeds the memory quota specified by `mem-quota-query`.
+ Default value:  `true`

### `tmp-storage-path`

+ Specifies the temporary storage path for some operators when a single SQL statement exceeds the memory quota specified by `mem-quota-query`.
+ Default value: `<temporary directory of OS>/<OS user ID>_tidb/MC4wLjAuMDo0MDAwLzAuMC4wLjA6MTAwODA=/tmp-storage`. `MC4wLjAuMDo0MDAwLzAuMC4wLjA6MTAwODA=` is the `Base64` encoding result of `<host>:<port>/<statusHost>:<statusPort>`.
+ This configuration takes effect only when `oom-use-tmp-storage` is `true`.

### `tmp-storage-quota`

+ Specifies the quota for the storage in `tmp-storage-path`. The unit is byte.
+ When a single SQL statement uses a temporary disk and the total volume of the temporary disk of the TiDB server exceeds this configuration value, the current SQL operation is cancelled and the `Out of Global Storage Quota!` error is returned.
+ When the value of this configuration is smaller than `0`, the above check and limit do not apply.
+ Default value: `-1`
+ When the remaining available storage in `tmp-storage-path` is lower than the value defined by `tmp-storage-quota`, the TiDB server reports an error when it is started, and exits.

### `oom-action`

- Specifies what operation TiDB performs when a single SQL statement exceeds the memory quota specified by `mem-quota-query` and cannot be spilled over to disk.
- Default value: `"cancel"` (In TiDB v4.0.2 and earlier versions, the default value is `"log"`)
- The valid options are `"log"` and `"cancel"`. When `oom-action="log"`, it prints the log only. When `oom-action="cancel"`, it cancels the operation and outputs the log.

### `lower-case-table-names`

- Configures the value of the `lower-case-table-names` system variable.
- Default value: `2`
- For details, see the [MySQL description](https://dev.mysql.com/doc/refman/5.7/en/server-system-variables.html#sysvar_lower_case_table_names) of this variable.

    > **Note:**
    >
    > Currently, TiDB only supports setting the value of this option to `2`. This means it is case-sensitive when you save a table name, but case-insensitive when you compare table names. The comparison is based on the lower case.

### `lease`

+ The timeout of the DDL lease.
+ Default value: `45s`
+ Unit: second

### `compatible-kill-query`

+ Determines whether to set the `KILL` statement to be MySQL compatible.
+ Default value: `false`
+ The behavior of `KILL xxx` in TiDB differs from the behavior in MySQL. TiDB requires the `TIDB` keyword, namely, `KILL TIDB xxx`. If `compatible-kill-query` is set to `true`, the `TIDB` keyword is not needed.
+ This distinction is important because the default behavior of the MySQL command-line client, when the user hits <kbd>Ctrl</kbd>+<kbd>C</kbd>, is to create a new connection to the backend and execute the `KILL` statement in that new connection. If a load balancer or proxy has sent the new connection to a different TiDB server instance than the original session, the wrong session could be terminated, which could cause interruption to applications using the cluster. Enable `compatible-kill-query` only if you are certain that the connection you refer to in your `KILL` statement is on the same server to which you send the `KILL` statement.

### `check-mb4-value-in-utf8`

- Determines whether to enable the `utf8mb4` character check. When this feature is enabled, if the character set is `utf8` and the `mb4` characters are inserted in `utf8`, an error is returned.
- Default value: `false`

### `treat-old-version-utf8-as-utf8mb4`

- Determines whether to treat the `utf8` character set in old tables as `utf8mb4`.
- Default value: `true`

### `alter-primary-key`

- Determines whether to add or remove the primary key constraint to or from a column.
- Default value: `false`
- With this default setting, adding or removing the primary key constraint is not supported. You can enable this feature by setting `alter-primary-key` to `true`. However, if a table already exists before the switch is on, and the data type of its primary key column is an integer, dropping the primary key from the column is not possible even if you set this configuration item to `true`.

### `server-version`

+ Modifies the version string returned by TiDB in the following situations:
    - When the built-in `VERSION()` function is used.
    - When TiDB establishes the initial connection to the client and returns the initial handshake packet with version string of the server. For details, see [MySQL Initial Handshake Packet](https://dev.mysql.com/doc/internals/en/connection-phase-packets.html#packet-Protocol::Handshake).
+ Default value: ""
+ By default, the format of the TiDB version string is `5.7.${mysql_latest_minor_version}-TiDB-${tidb_version}`.

### `repair-mode`

- Determines whether to enable the untrusted repair mode. When the `repair-mode` is set to `true`, bad tables in the `repair-table-list` cannot be loaded.
- Default value: `false`
- The `repair` syntax is not supported by default. This means that all tables are loaded when TiDB is started.

### `repair-table-list`

- `repair-table-list` is only valid when [`repair-mode`](#repair-mode) is set to `true`. `repair-table-list` is a list of bad tables that need to be repaired in an instance. An example of the list is: ["db.table1","db.table2"...].
- Default value: []
- The list is empty by default. This means that there are no bad tables that need to be repaired.

### `new_collations_enabled_on_first_bootstrap`

- Enables or disables the new collation support.
- Default value: `false`
- Note: This configuration takes effect only for the TiDB cluster that is first initialized. After the initialization, you cannot use this configuration item to enable or disable the new collation support. When a TiDB cluster is upgraded to v4.0, because the cluster has been initialized before, both `true` and `false` values of this configuration item are taken as `false`.

### `max-server-connections`

- The maximum number of concurrent client connections allowed in TiDB. It is used to control resources.
- Default value: `0`
- By default, TiDB does not set limit on the number of concurrent client connections. When the value of this configuration item is greater than `0` and the number of actual client connections reaches this value, the TiDB server rejects new client connections.

### `max-index-length`

- Sets the maximum allowable length of the newly created index.
- Default value: `3072`
- Unit: byte
- Currently, the valid value range is `[3072, 3072*4]`. MySQL and TiDB (version < v3.0.11) do not have this configuration item, but both limit the length of the newly created index. This limit in MySQL is `3072`. In TiDB (version =< 3.0.7), this limit is `3072*4`. In TiDB (3.0.7 < version < 3.0.11), this limit is `3072`. This configuration is added to be compatible with MySQL and earlier versions of TiDB.

### `enable-telemetry` <span class="version-mark">New in v4.0.2</span>

- Enables or disables the telemetry collection in TiDB.
- Default value: `true`
- When this configuration is set to `false` on all TiDB instances, the telemetry collection in TiDB is disabled and the [`tidb_enable_telemetry`](/system-variables.md#tidb_enable_telemetry-new-in-v402-version) system variable does not take effect. See [Telemetry](/telemetry.md) for details.

## Log

Configuration items related to log.

### `level`

+ Specifies the log output level.
+ Value options: `debug`, `info`, `warn`, `error`, and `fatal`.
+ Default value: `info`

### `format`

- Specifies the log output format.
- Value options: `json`, `text` and `console`.
- Default value: `text`

### `enable-timestamp`

- Determines whether to enable timestamp output in the log.
- Default value: `true`
- If you set the value to `false`, the log does not output timestamp.

> **Note:**
>
> To be backward compatible, the initial `disable-timestamp` configuration item remains valid. But if the value of `disable-timestamp` semantically conflicts with the value of `enable-timestamp` (for example, if both `enable-timestamp` and `disable-timestamp` are set to `true`), TiDB ignores the value for `disable-timestamp`. In later versions, the `disable-timestamp` configuration will be removed.
>
> Discard `disable-timestamp` and use `enable-timestamp` which is semantically easier to understand.

### `enable-slow-log`

- Determines whether to enable the slow query log.
- Default value: `true`
- To enable the slow query log, set `enable-slow-log` to `true`. Otherwise, set it to `false`.

### `slow-query-file`

- The file name of the slow query log.
- Default value: `tidb-slow.log`
- The format of the slow log is updated in TiDB v2.1.8, so the slow log is output to the slow log file separately. In versions before v2.1.8, this variable is set to "" by default.
- After you set it, the slow query log is output to this file separately.

### `slow-threshold`

- Outputs the threshold value of consumed time in the slow log.
- Default value: `300ms`
- If the value in a query is larger than the default value, it is a slow query and is output to the slow log.

### `record-plan-in-slow-log`

+ Determines whether to record execution plans in the slow log.
+ Default value: `1`
+ `0` means to disable, and `1` (by default) means to enable. The value of this parameter is the initial value of the [`tidb_record_plan_in_slow_log`](/system-variables.md#tidb_record_plan_in_slow_log) system variable.

### `expensive-threshold`

- Outputs the threshold value of the number of rows for the `expensive` operation.
- Default value: `10000`
- When the number of query rows (including the intermediate results based on statistics) is larger than this value, it is an `expensive` operation and outputs log with the `[EXPENSIVE_QUERY]` prefix.

### `query-log-max-len`

- The maximum length of SQL output.
- Default value: `4096`
- When the length of the statement is longer than `query-log-max-len`, the statement is truncated to output.

## log.file

Configuration items related to log files.

#### `filename`

- The file name of the general log file.
- Default value: ""
- If you set it, the log is output to this file.

#### `max-size`

- The size limit of the log file.
- Default value: 300MB
- The maximum size is 4GB.

#### `max-days`

- The maximum number of days that the log is retained.
- Default value: `0`
- The log is retained by default. If you set the value, the expired log is cleaned up after `max-days`.

#### `max-backups`

- The maximum number of retained logs.
- Default value: `0`
- All the log files are retained by default. If you set it to `7`, seven log files are retained at maximum.

## Security

Configuration items related to security.

### `ssl-ca`

- The file path of the trusted CA certificate in the PEM format.
- Default value: ""
- If you set this option and `--ssl-cert`, `--ssl-key` at the same time, TiDB authenticates the client certificate based on the list of trusted CAs specified by this option when the client presents the certificate. If the authentication fails, the connection is terminated.
- If you set this option but the client does not present the certificate, the secure connection continues without client certificate authentication.

### `ssl-cert`

- The file path of the SSL certificate in the PEM format.
- Default value: ""
- If you set this option and `--ssl-key` at the same time, TiDB allows (but not forces) the client to securely connect to TiDB using TLS.
- If the specified certificate or private key is invalid, TiDB starts as usual but cannot receive secure connection.

### `ssl-key`

- The file path of the SSL certificate key in the PEM format, that is, the private key of the certificate specified by `--ssl-cert`.
- Default value: ""
- Currently, TiDB does not support loading the private keys protected by passwords.

### `cluster-ssl-ca`

- The CA root certificate used to connect TiKV or PD with TLS.
- Default value: ""

### `cluster-ssl-cert`

- The path of the SSL certificate file used to connect TiKV or PD with TLS.
- Default value: ""

### `cluster-ssl-key`

- The path of the SSL private key file used to connect TiKV or PD with TLS.
- Default value: ""

### `spilled-file-encryption-method`

+ Determines the encryption method used for saving the spilled files to disk.
+ Default value: `"plaintext"`, which disables encryption.
+ Optional values: `"plaintext"` and `"aes128-ctr"`

## Performance

Configuration items related to performance.

### `max-procs`

- The number of CPUs used by TiDB.
- Default value: `0`
- The default `0` indicates using all the CPUs on the machine. You can also set it to n, and then TiDB uses n CPUs.

### `server-memory-quota` <span class="version-mark">New in v4.0.9</span>

> **Warning:**
>
> `server-memory-quota` is still an experimental feature. It is **NOT** recommended that you use it in a production environment.

+ The memory usage limit of tidb-server instances. <!-- New in TiDB v5.0 --> This configuration item completely supersedes the previous [`max-memory`](https://docs.pingcap.com/tidb/stable/tidb-configuration-file#max-memory).
+ Default value: `0` (in bytes), which means no memory limit.

### `memory-usage-alarm-ratio` <span class="version-mark">New in v4.0.9</span>

+ TiDB triggers an alarm when the memory usage of tidb-server instance exceeds a certain threshold. The valid value for this configuration item ranges from `0` to `1`. If it is configured as `0` or `1`, this alarm feature is disabled.
+ Default value: `0.8`
+ When the memory usage alarm is enabled, if [`server-memory-quota`](/tidb-configuration-file.md#server-memory-quota-new-in-v409) is not set, then the threshold of memory usage is ```the `memory-usage-alarm-ratio` value * the system memory size```; if `server-memory-quota` is set to a value greater than 0, then the threshold of memory usage is ```the `memory-usage-alarm-ratio` value * the `server-memory-quota` value```.
+ When TiDB detects that the memory usage of the tidb-server instance exceeds the threshold, it considers that there might be a risk of OOM. Therefore, it records ten SQL statements with the highest memory usage, ten SQL statements with the longest running time, and the heap profile among all SQL statements currently being executed to the directory [`tmp-storage-path/record`](/tidb-configuration-file.md#tmp-storage-path) and outputs a log containing the keyword `tidb-server has the risk of OOM`.
+ The value of this configuration item is the initial value of the system variable [`tidb_memory_usage_alarm_ratio`](/system-variables.md#tidb_memory_usage_alarm_ratio).

### `stmt-count-limit`

- The maximum number of statements allowed in a single TiDB transaction.
- Default value: `5000`
- If a transaction does not roll back or commit after the number of statements exceeds `stmt-count-limit`, TiDB returns the `statement count 5001 exceeds the transaction limitation, autocommit = false` error. This configuration takes effect **only** in the retriable optimistic transaction. If you use the pessimistic transaction or have disabled the transaction retry, the number of statements in a transaction is not limited by this configuration.

### `txn-total-size-limit`

- The size limit of a single transaction in TiDB.
- Default value: `104857600` (in bytes)
- In a single transaction, the total size of key-value records cannot exceed this value. The maximum value of this parameter is `10737418240` (10 GB). Note that if you have used the binlog to serve the downstream consumer Kafka (such as the `arbiter` cluster), the value of this parameter must be no more than `1073741824` (1 GB). This is because 1 GB is the upper limit of a single message size that Kafka can process. Otherwise, an error is returned if this limit is exceeded.

### `tcp-keep-alive`

- Determines whether to enable `keepalive` in the TCP layer.
- Default value: `true`

### `cross-join`

- Default value: `true`
- TiDB supports executing the `JOIN` statement without any condition (the `WHERE` field) of both sides tables by default; if you set the value to `false`, the server refuses to execute when such a `JOIN` statement appears.

### `stats-lease`

- The time interval of reloading statistics, updating the number of table rows, checking whether it is needed to perform the automatic analysis, using feedback to update statistics and loading statistics of columns.
- Default value: `3s`
    - At intervals of `stats-lease` time, TiDB checks the statistics for updates and updates them to the memory if updates exist.
    - At intervals of `20 * stats-lease` time, TiDB updates the total number of rows generated by DML and the number of modified rows to the system table.
    - At intervals of `stats-lease`, TiDB checks for tables and indexes that need to be automatically analyzed.
    - At intervals of `stats-lease`, TiDB checks for column statistics that need to be loaded to the memory.
    - At intervals of `200 * stats-lease`, TiDB writes the feedback cached in the memory to the system table.
    - At intervals of `5 * stats-lease`, TiDB reads the feedback in the system table, and updates the statistics cached in the memory.
- When `stats-lease` is set to 0, TiDB periodically reads the feedback in the system table, and updates the statistics cached in the memory every three seconds. But TiDB no longer automatically modifies the following statistics-related system tables:
    - `mysql.stats_meta`: TiDB no longer automatically records the number of table rows that are modified by the transaction and updates it to this system table.
    - `mysql.stats_histograms`/`mysql.stats_buckets` and `mysql.stats_top_n`: TiDB no longer automatically analyzes and proactively updates statistics.
    - `mysql.stats_feedback`: TiDB no longer updates the statistics of the tables and indexes according to a part of statistics returned by the queried data.

### `run-auto-analyze`

- Determines whether TiDB executes automatic analysis.
- Default value: `true`

### `feedback-probability`

- The probability that TiDB collects the feedback statistics of each query.
- Default value: `0.05`
- TiDB collects the feedback of each query at the probability of `feedback-probability`, to update statistics.

### `query-feedback-limit`

- The maximum pieces of query feedback that can be cached in memory. Extra pieces of feedback that exceed this limit are discarded.
- Default value: `1024`

### `pseudo-estimate-ratio`

- The ratio of (number of modified rows)/(total number of rows) in a table. If the value is exceeded, the system assumes that the statistics have expired and the pseudo statistics will be used.
- Default value: `0.8`
- The minimum value is `0` and the maximum value is `1`.

### `force-priority`

- Sets the priority for all statements.
- Default: `NO_PRIORITY`
- Optional values: `NO_PRIORITY`, `LOW_PRIORITY`, `HIGH_PRIORITY` and `DELAYED`.

### `distinct-agg-push-down`

- Determines whether the optimizer executes the operation that pushes down the aggregation function with `Distinct` (such as `select count(distinct a) from t`) to Coprocessors.
- Default: `false`
- This variable is the initial value of the system variable [`tidb_opt_distinct_agg_push_down`](/system-variables.md#tidb_opt_distinct_agg_push_down).

### `nested-loop-join-cache-capacity`

+ The maximum memory usage for the Least Recently Used (LRU) algorithm of the nested loop join cache (in bytes).
+ Default value: `20971520`
+ When `nested-loop-join-cache-capacity` is set to `0`, nested loop join cache is disabled by default. When the LRU size is larger than the value of `nested-loop-join-cache-capacity`, the elements in the LRU are removed.

## prepared-plan-cache

The Plan Cache configuration of the `PREPARE` statement.

### `enabled`

- Determines whether to enable Plan Cache of the `PREPARE` statement.
- Default value: `true`

### `capacity`

- The number of cached statements.
- Default value: `100`
- The type is `uint`. Values less than `0` are converted to large integers.

### `memory-guard-ratio`

- It is used to prevent `performance.max-memory` from being exceeded. When `max-memory * (1 - prepared-plan-cache.memory-guard-ratio)` is exceeded, the elements in the LRU are removed.
- Default value: `0.1`
- The minimum value is `0`; the maximum value is `1`.

## tikv-client

### `grpc-connection-count`

- The maximum number of connections established with each TiKV.
- Default value: `16`

### `grpc-keepalive-time`

- The `keepalive` time interval of the RPC connection between TiDB and TiKV nodes. If there is no network packet within the specified time interval, the gRPC client executes `ping` command to TiKV to see if it is alive.
- Default: `10`
- unit: second

### `grpc-keepalive-timeout`

- The timeout of the RPC `keepalive` check between TiDB and TiKV nodes.
- Default value: `3`
- unit: second

### `commit-timeout`

- The maximum timeout when executing a transaction commit.
- Default value: `41s`
- It is required to set this value larger than twice of the Raft election timeout.

### `max-txn-ttl`

- The longest time that a single transaction can hold locks. If this time is exceeded, the locks of a transaction might be cleared by other transactions so that this transaction cannot be successfully committed.
- Default value: `600000`
- Unit: Millisecond
- The transaction that holds locks longer than this time can only be committed or rolled back. The commit might not be successful.

### `max-batch-size`

- The maximum number of RPC packets sent in batch. If the value is not `0`, the `BatchCommands` API is used to send requests to TiKV, and the RPC latency can be reduced in the case of high concurrency. It is recommended that you do not modify this value.
- Default value: `128`

### `max-batch-wait-time`

- Waits for `max-batch-wait-time` to encapsulate the data packets into a large packet in batch and send it to the TiKV node. It is valid only when the value of `tikv-client.max-batch-size` is greater than `0`. It is recommended not to modify this value.
- Default value: `0`
- unit: nanoseconds

### `batch-wait-size`

- The maximum number of packets sent to TiKV in batch. It is recommended not to modify this value.
- Default value: `8`
- If the value is `0`, this feature is disabled.

### `overload-threshold`

- The threshold of the TiKV load. If the TiKV load exceeds this threshold, more `batch` packets are collected to relieve the pressure of TiKV. It is valid only when the value of `tikv-client.max-batch-size` is greater than `0`. It is recommended not to modify this value.
- Default value: `200`

### `enable-one-pc` <!-- New in v5.0 -->

- Specifies whether to use the one-phase commit feature for transactions that involve only one Region. Compared with the two-phase commit, the one-phase commit feature can greatly reduce the commit latency and increase throughput.
- Default value: `false`

> **Warning:**
>
> This is still an experimental feature. It is **NOT** recommended that you use it in a production environment. Currently, the following issues are found, and be aware of them if you need to use this feature:
>
> - This feature is incompatible with [TiCDC](/ticdc/ticdc-overview.md) and might cause TiCDC to run abnormally.
>
> - This feature is incompatible with [Follower Read](/follower-read.md) and [TiFlash](/tiflash/tiflash-overview.md), and snapshot isolation cannot be guaranteed.
>
> - External consistency cannot be guaranteed.
>
> - If the transaction commit is interrupted abnormally by the machine crash when the DDL operation is executed, the data format might be incorrect.

## tikv-client.async-commit <!-- New in v5.0 -->

### `enable`

- Enables or disables the async commit feature for the second phase of the two-phase transaction commit to perform asynchronously in the background. Enabling this feature can reduce the latency of transaction commit. This feature is not compatible with [TiDB Binlog](/tidb-binlog/tidb-binlog-overview.md) and does not take effect when Binlog is enabled.
- Default value: `false`

### `keys-limit`

- Specifies the upper limit of the number of keys in an async commit transaction. The async commit feature is **NOT** suitable for transactions that are too large. Transactions that exceed this limit will use the two-phase commit.
- Default value: `256`

### `total-key-size-limit`

- Specifies the upper limit of the total size of keys in an async commit transaction. The async commit feature is **NOT** suitable for transactions in which the involved key ranges are too long. Transactions that exceed this limit will use the two-phase commit.
- Default value: `4096`
- Unit: byte

> **Warning:**
>
> This is still an experimental feature. It is **NOT** recommended that you use it in a production environment. Currently, the following issues are found, and be aware of them if you need to use this feature:
>
> - This feature is incompatible with [Follower Read](/follower-read.md) and [TiFlash](/tiflash/tiflash-overview.md), and snapshot isolation cannot be guaranteed.
>
> - External consistency cannot be guaranteed.
>
> - If the transaction commit is interrupted abnormally by the machine crash when the DDL operation is executed, the data format might be incorrect.

## tikv-client.copr-cache <span class="version-mark">New in v4.0.0</span>

This section introduces configuration items related to the Coprocessor Cache feature.

### `enable`

- Determines whether to enable [Coprocessor Cache](/coprocessor-cache.md).
- Default value: `false` (which means that Coprocessor Cache is disabled by default)

### `capacity-mb`

- The total size of the cached data. When the cache space is full, old cache entries are evicted.
- Default value: `1000.0`
- Unit: MB

### `admission-max-result-mb`

- Specifies the largest single push-down calculation result set that can be cached. If the result set of a single push-down calculation returned on the Coprocessor is larger than the result set specified by this parameter, the result set is cached. Increasing this value means that more types of push-down requests are cached, but also cause the cache space to be occupied more easily. Note that the size of each push-down calculation result set is generally smaller than the size of the Region. Therefore, it is meaningless to set this value far beyond the size of a Region.
- Default value: `10.0`
- Unit: MB

### `admission-min-process-ms`

- Specifies the minimum calculation time for a single push-down calculation result set that can be cached. If the calculation time of a single push-down calculation on the Coprocessor is less than the time specified by this parameter, the result set is not cached. Requests that are processed quickly do not need to be cached, and only the requests that take a long time to process need to be cached, which makes the cache less likely to be evicted.
- Default value: `5`
- Unit: ms

### txn-local-latches

Configuration related to the transaction latch. It is recommended to enable it when many local transaction conflicts occur.

### `enable`

- Determines whether to enable the memory lock of transactions.
- Default value: `false`

### `capacity`

- The number of slots corresponding to Hash, which automatically adjusts upward to an exponential multiple of 2. Each slot occupies 32 Bytes of memory. If set too small, it might result in slower running speed and poor performance in the scenario where data writing covers a relatively large range (such as importing data).
- Default value: `2048000`

## binlog

Configurations related to TiDB Binlog.

### `enable`

- Enables or disables binlog.
- Default value: `false`

### `write-timeout`

- The timeout of writing binlog into Pump. It is not recommended to modify this value.
- Default: `15s`
- unit: second

### `ignore-error`

- Determines whether to ignore errors occurred in the process of writing binlog into Pump. It is not recommended to modify this value.
- Default value: `false`
- When the value is set to `true` and an error occurs, TiDB stops writing binlog and add `1` to the count of the `tidb_server_critical_error_total` monitoring item. When the value is set to `false`, the binlog writing fails and the entire TiDB service is stopped.

### `binlog-socket`

- The network address to which binlog is exported.
- Default value: ""

### `strategy`

- The strategy of Pump selection when binlog is exported. Currently, only the `hash` and `range` methods are supported.
- Default value: `range`

## status

Configuration related to the status of TiDB service.

### `report-status`

- Enables or disables the HTTP API service.
- Default value: `true`

### `record-db-qps`

- Determines whether to transmit the database-related QPS metrics to Prometheus.
- Default value: `false`

## stmt-summary <span class="version-mark">New in v3.0.4</span>

Configurations related to the `events_statement_summary_by_digest` table.

### max-stmt-count

- The maximum number of SQL categories allowed to be saved in the `events_statement_summary_by_digest` table.
- Default value: `100`

### max-sql-length

- The longest display length for the `DIGEST_TEXT` and `QUERY_SAMPLE_TEXT` columns in the `events_statement_summary_by_digest` table.
- Default value: `4096`

## pessimistic-txn

For pessimistic transaction usage, refer to [TiDB Pessimistic Transaction Mode](/pessimistic-transaction.md).

### max-retry-count

- The maximum number of retries of each statement in pessimistic transactions. If the number of retries exceeds this limit, an error occurs.
- Default value: `256`

## experimental

The `experimental` section, introduced in v3.1.0, describes configurations related to the experimental features of TiDB.

### `allow-expression-index` <span class="version-mark">New in v4.0.0</span>

- Determines whether to create the expression index.
- Default value: false