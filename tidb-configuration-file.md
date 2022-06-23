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
- It is recommended to set it to `false` if you need to create a large number of tables (for example, more than 100 thousand tables).

### `token-limit`

+ The number of sessions that can execute requests concurrently.
+ Type: Integer
+ Default value: `1000`
+ Minimum value: `1`
+ Maximum Value (64-bit platforms): `18446744073709551615`
+ Maximum Value (32-bit platforms): `4294967295`

### `oom-use-tmp-storage`

+ Controls whether to enable the temporary storage for some operators when a single SQL statement exceeds the memory quota specified by the system variable [`tidb_mem_quota_query`](/system-variables.md#tidb_mem_quota_query).
+ Default value:  `true`

### `tmp-storage-path`

+ Specifies the temporary storage path for some operators when a single SQL statement exceeds the memory quota specified by the system variable [`tidb_mem_quota_query`](/system-variables.md#tidb_mem_quota_query).
+ Default value: `<temporary directory of OS>/<OS user ID>_tidb/MC4wLjAuMDo0MDAwLzAuMC4wLjA6MTAwODA=/tmp-storage`. `MC4wLjAuMDo0MDAwLzAuMC4wLjA6MTAwODA=` is the `Base64` encoding result of `<host>:<port>/<statusHost>:<statusPort>`.
+ This configuration takes effect only when `oom-use-tmp-storage` is `true`.

### `tmp-storage-quota`

+ Specifies the quota for the storage in `tmp-storage-path`. The unit is byte.
+ When a single SQL statement uses a temporary disk and the total volume of the temporary disk of the TiDB server exceeds this configuration value, the current SQL operation is cancelled and the `Out of Global Storage Quota!` error is returned.
+ When the value of this configuration is smaller than `0`, the above check and limit do not apply.
+ Default value: `-1`
+ When the remaining available storage in `tmp-storage-path` is lower than the value defined by `tmp-storage-quota`, the TiDB server reports an error when it is started, and exits.

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

### `alter-primary-key` (Deprecated)

- Determines whether to add or remove the primary key constraint to or from a column.
- Default value: `false`
- With this default setting, adding or removing the primary key constraint is not supported. You can enable this feature by setting `alter-primary-key` to `true`. However, if a table already exists before the switch is on, and the data type of its primary key column is an integer, dropping the primary key from the column is not possible even if you set this configuration item to `true`.

> **Note:**
>
> This configuration item has been deprecated, and currently takes effect only when the value of `@tidb_enable_clustered_index` is `INT_ONLY`. If you need to add or remove the primary key, use the `NONCLUSTERED` keyword instead when creating the table. For more details about the primary key of the `CLUSTERED` type, refer to [clustered index](/clustered-indexes.md).

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
- Default value: `true`
- Note: This configuration takes effect only for the TiDB cluster that is first initialized. After the initialization, you cannot use this configuration item to enable or disable the new collation support. When a TiDB cluster is upgraded to v4.0 or later, because the cluster has been initialized before, both `true` and `false` values of this configuration item are taken as `false`.

### `max-server-connections`

- The maximum number of concurrent client connections allowed in TiDB. It is used to control resources.
- Default value: `0`
- By default, TiDB does not set limit on the number of concurrent client connections. When the value of this configuration item is greater than `0` and the number of actual client connections reaches this value, the TiDB server rejects new client connections.

### `max-index-length`

- Sets the maximum allowable length of the newly created index.
- Default value: `3072`
- Unit: byte
- Currently, the valid value range is `[3072, 3072*4]`. MySQL and TiDB (version < v3.0.11) do not have this configuration item, but both limit the length of the newly created index. This limit in MySQL is `3072`. In TiDB (version =< 3.0.7), this limit is `3072*4`. In TiDB (3.0.7 < version < 3.0.11), this limit is `3072`. This configuration is added to be compatible with MySQL and earlier versions of TiDB.

### `table-column-count-limit` <span class="version-mark">New in v5.0</span>

- Sets the limit on the number of columns in a single table.
- Default value: `1017`
- Currently, the valid value range is `[1017, 4096]`.

### `index-limit` <span class="version-mark">New in v5.0</span>

- Sets the limit on the number of indexes in a single table.
- Default value: `64`
- Currently, the valid value range is `[64, 512]`.

### `enable-telemetry` <span class="version-mark">New in v4.0.2</span>

- Enables or disables the telemetry collection in TiDB.
- Default value: `true`
- When this configuration is set to `false` on all TiDB instances, the telemetry collection in TiDB is disabled and the [`tidb_enable_telemetry`](/system-variables.md#tidb_enable_telemetry-new-in-v402) system variable does not take effect. See [Telemetry](/telemetry.md) for details.

### `enable-tcp4-only` <span class="version-mark">New in v5.0</span>

- Enables or disables listening on TCP4 only.
- Default value: `false`
- Enabling this option is useful when TiDB is used with LVS for load balancing because the [real client IP from the TCP header](https://github.com/alibaba/LVS/tree/master/kernel/net/toa) can be correctly parsed by the "tcp4" protocol.

### `enable-enum-length-limit` <span class="version-mark">New in v5.0</span>

+ Determines whether to limit the maximum length of a single `ENUM` element and a single `SET` element.
+ Default value: `true`
+ When this configuration value is `true`, the maximum length of a single `ENUM` element and a single `SET` element is 255 characters, which is compatible with [MySQL 8.0](https://dev.mysql.com/doc/refman/8.0/en/string-type-syntax.html). When this configuration value is `false`, there is no limit on the length of a single element, which is compatible with TiDB (earlier than v5.0).

### `graceful-wait-before-shutdown` <span class="version-mark">New in v5.0</span>

- Specifies the number of seconds that TiDB waits when you shut down the server, which allows the clients to disconnect.
- Default value: `0`
- When TiDB is waiting for shutdown (in the grace period), the HTTP status will indicate a failure, which allows the load balancers to reroute traffic.

### `enable-global-kill` <span class="version-mark">New in v6.1.0</span>

+ Controls whether to enable the Global Kill (terminating queries or connections across instances) feature.
+ Default value: `true`
+ When the value is `true`, both `KILL` and `KILL TIDB` statements can terminate queries or connections across instances so you do not need to worry about erroneously terminating queries or connections. When you use a client to connect to any TiDB instance and execute the `KILL` or `KILL TIDB` statement, the statement will be forwarded to the target TiDB instance. If there is a proxy between the client and the TiDB cluster, the `KILL` and `KILL TIDB` statements will also be forwarded to the target TiDB instance for execution. Currently, using the MySQL command line <kbd>ctrl</kbd>+<kbd>c</kbd> to terminate a query or connection in TiDB is not supported when `enable-global-kill` is `true`. For more information on the `KILL` statement, see [KILL](/sql-statements/sql-statement-kill.md).

## Log

Configuration items related to log.

### `level`

+ Specifies the log output level.
+ Value options: `debug`, `info`, `warn`, `error`, and `fatal`.
+ Default value: `info`

### `format`

- Specifies the log output format.
- Value options: `json` and `text`.
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

## log.file

Configuration items related to log files.

#### `filename`

- The file name of the general log file.
- Default value: ""
- If you set it, the log is output to this file.

#### `max-size`

- The size limit of the log file.
- Default value: 300
- Unit: MB
- The maximum value is 4096.

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

### `enable-sem`

- Enables the Security Enhanced Mode (SEM).
- Default value: `false`
- The status of SEM is available via the system variable [`tidb_enable_enhanced_security`](/system-variables.md#tidb_enable_enhanced_security).

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

### `auto-tls`

- Determines whether to automatically generate the TLS certificates on startup.
- Default value: `false`

### `tls-version`

- Set the minimum TLS version for MySQL Protocol connections.
- Default value: "", which allows TLSv1.1 or higher.
- Optional values: `"TLSv1.0"`, `"TLSv1.1"`, `"TLSv1.2"` and `"TLSv1.3"`

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

### `max-txn-ttl`

- The longest time that a single transaction can hold locks. If this time is exceeded, the locks of a transaction might be cleared by other transactions so that this transaction cannot be successfully committed.
- Default value: `3600000`
- Unit: Millisecond
- The transaction that holds locks longer than this time can only be committed or rolled back. The commit might not be successful.

### `stmt-count-limit`

- The maximum number of statements allowed in a single TiDB transaction.
- Default value: `5000`
- If a transaction does not roll back or commit after the number of statements exceeds `stmt-count-limit`, TiDB returns the `statement count 5001 exceeds the transaction limitation, autocommit = false` error. This configuration takes effect **only** in the retryable optimistic transaction. If you use the pessimistic transaction or have disabled the transaction retry, the number of statements in a transaction is not limited by this configuration.

### `txn-entry-size-limit` <span class="version-mark">New in v5.0</span>

- The size limit of a single row of data in TiDB.
- Default value: `6291456` (in bytes)
- The size limit of a single key-value record in a transaction. If the size limit is exceeded, TiDB returns the `entry too large` error. The maximum value of this configuration item does not exceed `125829120` (120 MB).
- Note that TiKV has a similar limit. If the data size of a single write request exceeds [`raft-entry-max-size`](/tikv-configuration-file.md#raft-entry-max-size), which is 8 MB by default, TiKV refuses to process this request. When a table has a row of large size, you need to modify both configurations at the same time.

### `txn-total-size-limit`

- The size limit of a single transaction in TiDB.
- Default value: `104857600` (in bytes)
- In a single transaction, the total size of key-value records cannot exceed this value. The maximum value of this parameter is `1099511627776` (1 TB). Note that if you have used the binlog to serve the downstream consumer Kafka (such as the `arbiter` cluster), the value of this parameter must be no more than `1073741824` (1 GB). This is because 1 GB is the upper limit of a single message size that Kafka can process. Otherwise, an error is returned if this limit is exceeded.

### `tcp-keep-alive`

- Determines whether to enable `keepalive` in the TCP layer.
- Default value: `true`

### `tcp-no-delay`

- Determines whether to enable TCP_NODELAY at the TCP layer. After it is enabled, TiDB disables the Nagle algorithm in the TCP/IP protocol and allows sending small data packets to reduce network latency. This is suitable for latency-sensitive applications with a small transmission volume of data.
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
- When `stats-lease` is set to 0s, TiDB periodically reads the feedback in the system table, and updates the statistics cached in the memory every three seconds. But TiDB no longer automatically modifies the following statistics-related system tables:
    - `mysql.stats_meta`: TiDB no longer automatically records the number of table rows that are modified by the transaction and updates it to this system table.
    - `mysql.stats_histograms`/`mysql.stats_buckets` and `mysql.stats_top_n`: TiDB no longer automatically analyzes and proactively updates statistics.
    - `mysql.stats_feedback`: TiDB no longer updates the statistics of the tables and indexes according to a part of statistics returned by the queried data.

### `feedback-probability`

- The probability that TiDB collects the feedback statistics of each query.
- Default value: `0`
- This feature is disabled by default, and it is not recommended to enable this feature. If it is enabled, TiDB collects the feedback of each query at the probability of `feedback-probability`, to update statistics.

### `query-feedback-limit`

- The maximum pieces of query feedback that can be cached in memory. Extra pieces of feedback that exceed this limit are discarded.
- Default value: `1024`

### `pseudo-estimate-ratio`

- The ratio of (number of modified rows)/(total number of rows) in a table. If the value is exceeded, the system assumes that the statistics have expired and the pseudo statistics will be used.
- Default value: `0.8`
- The minimum value is `0` and the maximum value is `1`.

### `force-priority`

- Sets the priority for all statements.
- Default value: `NO_PRIORITY`
- Optional values: `NO_PRIORITY`, `LOW_PRIORITY`, `HIGH_PRIORITY` and `DELAYED`.

### `distinct-agg-push-down`

- Determines whether the optimizer executes the operation that pushes down the aggregation function with `Distinct` (such as `select count(distinct a) from t`) to Coprocessors.
- Default: `false`
- This variable is the initial value of the system variable [`tidb_opt_distinct_agg_push_down`](/system-variables.md#tidb_opt_distinct_agg_push_down).

### `enforce-mpp`

+ Determines whether to ignore the optimizer's cost estimation and to forcibly use TiFlash's MPP mode for query execution.
+ Default value: `false`
+ This configuration item controls the initial value of [`tidb_enforce_mpp`](/system-variables.md#tidb_enforce_mpp-new-in-v51). For example, when this configuration item is set to `true`, the default value of `tidb_enforce_mpp` is `ON`.

### `enable-stats-cache-mem-quota` <span class="version-mark">New in v6.1.0</span>

> **Warning:**
>
> This variable is an experimental feature. It is not recommended to use it in production environments.

+ Controls whether to enable the memory quota for the statistics cache.
+ Default value: `false`

### `stats-load-concurrency` <span class="version-mark">New in v5.4.0</span>

> **WARNING:**
>
> Currently, synchronously loading statistics is an experimental feature. It is not recommended that you use it in production environments.

+ The maximum number of columns that the TiDB synchronously loading statistics feature can process concurrently.
+ Default value: `5`
+ Currently, the valid value range is `[1, 128]`.

### `stats-load-queue-size` <span class="version-mark">New in v5.4.0</span>

> **WARNING:**
>
> Currently, synchronously loading statistics is an experimental feature. It is not recommended that you use it in production environments.

+ The maximum number of column requests that the TiDB synchronously loading statistics feature can cache.
+ Default value: `1000`
+ Currently, the valid value range is `[1, 100000]`.

## opentracing

Configuration items related to opentracing.

### `enable`

+ Enables opentracing to trace the call overhead of some TiDB components. Note that enabling opentracing causes some performance loss.
+ Default value: `false`

### `rpc-metrics`

+ Enables RPC metrics.
+ Default value: `false`

## opentracing.sampler

Configuration items related to opentracing.sampler.

### `type`

+ Specifies the type of the opentracing sampler.
+ Default value: `"const"`
+ Value options: `"const"`, `"probabilistic"`, `"rateLimiting"`, `"remote"`

### `param`

+ The parameter of the opentracing sampler.
    - For the `const` type, the value can be `0` or `1`, which indicates whether to enable the `const` sampler.
    - For the `probabilistic` type, the parameter specifies the sampling probability, which can be a float number between `0` and `1`.
    - For the `rateLimiting` type, the parameter specifies the number of spans sampled per second.
    - For the `remote` type, the parameter specifies the sampling probability, which can be a float number between `0` and `1`.
+ Default value: `1.0`

### `sampling-server-url`

+ The HTTP URL of the jaeger-agent sampling server.
+ Default value: `""`

### `max-operations`

+ The maximum number of operations that the sampler can trace. If an operation is not traced, the default probabilistic sampler is used.
+ Default value: `0`

### `sampling-refresh-interval`

+ Controls the frequency of polling the jaeger-agent sampling policy.
+ Default value: `0`

## opentracing.reporter

Configuration items related to opentracing.reporter.

### `queue-size`

+ The queue size with which the reporter records spans in memory.
+ Default value: `0`

### `buffer-flush-interval`

+ The interval at which the reporter flushes the spans in memory to the storage.
+ Default value: `0`

### `log-spans`

+ Determines whether to print the log for all submitted spans.
+ Default value: `false`

### `local-agent-host-port`

+ The address at which the reporter sends spans to the jaeger-agent.
+ Default value: `""`

## tikv-client

### `grpc-connection-count`

- The maximum number of connections established with each TiKV.
- Default value: `4`

### `grpc-keepalive-time`

- The `keepalive` time interval of the RPC connection between TiDB and TiKV nodes. If there is no network packet within the specified time interval, the gRPC client executes `ping` command to TiKV to see if it is alive.
- Default: `10`
- Unit: second

### `grpc-keepalive-timeout`

- The timeout of the RPC `keepalive` check between TiDB and TiKV nodes.
- Default value: `3`
- Unit: second

### `grpc-compression-type`

- Specifies the compression type used for data transfer between TiDB and TiKV nodes. The default value is `"none"`, which means no compression. To enable the gzip compression, set this value to `"gzip"`.
- Default value: `"none"`
- Value options: `"none"`, `"gzip"`

### `commit-timeout`

- The maximum timeout when executing a transaction commit.
- Default value: `41s`
- It is required to set this value larger than twice of the Raft election timeout.

### `max-batch-size`

- The maximum number of RPC packets sent in batch. If the value is not `0`, the `BatchCommands` API is used to send requests to TiKV, and the RPC latency can be reduced in the case of high concurrency. It is recommended that you do not modify this value.
- Default value: `128`

### `max-batch-wait-time`

- Waits for `max-batch-wait-time` to encapsulate the data packets into a large packet in batch and send it to the TiKV node. It is valid only when the value of `tikv-client.max-batch-size` is greater than `0`. It is recommended not to modify this value.
- Default value: `0`
- Unit: nanoseconds

### `batch-wait-size`

- The maximum number of packets sent to TiKV in batch. It is recommended not to modify this value.
- Default value: `8`
- If the value is `0`, this feature is disabled.

### `overload-threshold`

- The threshold of the TiKV load. If the TiKV load exceeds this threshold, more `batch` packets are collected to relieve the pressure of TiKV. It is valid only when the value of `tikv-client.max-batch-size` is greater than `0`. It is recommended not to modify this value.
- Default value: `200`

## tikv-client.copr-cache <span class="version-mark">New in v4.0.0</span>

This section introduces configuration items related to the Coprocessor Cache feature.

### `capacity-mb`

- The total size of the cached data. When the cache space is full, old cache entries are evicted. When the value is `0.0`, the Coprocessor Cache feature is disabled.
- Default value: `1000.0`
- Unit: MB
- Type: Float

## txn-local-latches

Configuration related to the transaction latch. It is recommended to enable it when many local transaction conflicts occur.

### `enabled`

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

## pessimistic-txn

For pessimistic transaction usage, refer to [TiDB Pessimistic Transaction Mode](/pessimistic-transaction.md).

### max-retry-count

- The maximum number of retries of each statement in pessimistic transactions. If the number of retries exceeds this limit, an error occurs.
- Default value: `256`

### deadlock-history-capacity

+ The maximum number of deadlock events that can be recorded in the [`INFORMATION_SCHEMA.DEADLOCKS`](/information-schema/information-schema-deadlocks.md) table of a single TiDB server. If this table is in full volume and an additional deadlock event occurs, the earliest record in the table will be removed to make place for the newest error.
+ Default value: `10`
+ Minimum value: `0`
+ Maximum value: `10000`

### deadlock-history-collect-retryable

+ Controls whether the [`INFORMATION_SCHEMA.DEADLOCKS`](/information-schema/information-schema-deadlocks.md) table collects the information of retryable deadlock errors. For the description of retryable deadlock errors, see [Retryable deadlock errors](/information-schema/information-schema-deadlocks.md#retryable-deadlock-errors).
+ Default value: `false`

### pessimistic-auto-commit (New in v6.0.0)

+ Determines the transaction mode that the auto-commit transaction uses when the pessimistic transaction mode is globally enabled (`tidb_txn_mode='pessimistic'`). By default, even if the pessimistic transaction mode is globally enabled, the auto-commit transaction still uses the optimistic transaction mode. After enabling `pessimistic-auto-commit` (set to `true`), the auto-commit transaction also uses pessimistic mode, which is consistent with the other explicitly committed pessimistic transactions.
+ For scenarios with conflicts, after enabling this configuration, TiDB includes auto-commit transactions into the global lock-waiting management, which avoids deadlocks and mitigates the latency spike brought by deadlock-causing conflicts.
+ For scenarios with no conflicts, if there are many auto-commit transactions (the specific number is determined by the real scenarios. For example, the number of auto-commit transactions accounts for more than half of the total number of applications), and a single transaction operates a large data volume, enabling this configuration causes performance regression. For example, the auto-commit `INSERT INTO SELECT` statement.
+ Default value: `false`

## experimental

The `experimental` section, introduced in v3.1.0, describes the configurations related to the experimental features of TiDB.

### `allow-expression-index` <span class="version-mark">New in v4.0.0</span>

+ Controls whether an expression index can be created. Since TiDB v5.2.0, if the function in an expression is safe, you can create an expression index directly based on this function without enabling this configuration. If you want to create an expression index based on other functions, you can enable this configuration, but correctness issues might exist. By querying the `tidb_allow_function_for_expression_index` variable, you can get the functions that are safe to be directly used for creating an expression.
+ Default value: `false`
