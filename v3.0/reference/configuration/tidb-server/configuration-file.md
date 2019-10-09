---
title: TiDB Configuration File
summary: Learn the TiDB configuration file options that are not involved in command line options.
category: deployment
---

# TiDB Configuration File

<!-- markdownlint-disable MD001 -->

The TiDB configuration file supports more options than command-line parameters. You can find the default configuration file in [here](https://github.com/pingcap/tidb/blob/master/config/config.toml.example) and rename it to `config.toml`.

This document describes the options that are not involved in command line options. For command line options, see [Configuration Flags](/v3.0/reference/configuration/tidb-server/configuration.md).

### `split-table`

- Determines whether to create a separate Region for each table
- Default value: `true`
- It is recommended to set it to `false` if you need to create a large number of tables.

### `oom-action`

- Specifies the operation when out-of-memory occurs in TiDB
- Default value: `log`
- The valid options are `log` and `cancel`. `log` only prints the log without actual processing. `cancel"` cancels the operation and outputs the log.

### `mem-quota-query`

- The maximum memory available for a single SQL statement
- Default value: `34359738368`
- Requests that require more memory than this value are handled based on the behavior defined by `oom-action`.

### `enable-streaming`

- Determines whether to enable the data fetch mode of streaming in Coprocessor
- Default value: `false`

### `lower-case-table-names`

- Configures the value of the `lower_case_table_names` system variable
- Default value: `2`
- For details, see the [MySQL description](https://dev.mysql.com/doc/refman/5.7/en/server-system-variables.html#sysvar_lower_case_table_names) of this variable.

    > **Note:**
    >
    > Currently, TiDB only supports setting the value of this option to `2`. This means it is case-sensitive when you save a table name, but case-insensitive when you compare table names. The comparison is based on the lower case.

### `lease`

+ The timeout of the DDL lease
+ Default value: `45s`
+ Unit: second

### `compatible-kill-query`

+ Determines whether to set the `KILL` statement to be MySQL compatible
+ Default value: `false`
+ The behavior of `KILL xxx` in TiDB differs from the behavior in MySQL. TiDB requires the `TIDB` keyword, namely, `KILL TIDB xxx`. If `compatible-kill-query` is set to `true`, the `TIDB` keyword is not needed.
+ This distinction is important because the default behavior of the MySQL command-line client, when the user hits `Ctrl + C`, is to create a new connection to the backend and execute the `KILL` statement in that new connection. If a load balancer or proxy has sent the new connection to a different TiDB server instance than the original session, the wrong session could be terminated, which could cause interruption to applications using the cluster. Enable `compatible-kill-query` only if you are certain that the connection you refer to in your `KILL` statement is on the same server to which you send the `KILL` statement.

### `check-mb4-value-in-utf8`

- Determines whether to enable the `utf8mb4` character check. When this feature is enabled, if the character set is `utf8` and the `mb4` characters are inserted in `utf8`, an error is returned.
- Default value: `false`

### `treat-old-version-utf8-as-utf8mb4`

- Determines whether to treat the `utf8` character set in old tables as `utf8mb4`
- Default value: `true`

## Log

Configuration items related to log

### `format`

- Specifies the log output format
- Available values: `json`, `text`, `console`
- Default value: `text`

### `disable-timestamp`

- Determines whether to disable timestamp output in the log
- Default value: `false`
- If you set the value to `true`, the log does not output timestamp

### `slow-query-file`

- The file name of the slow query log
- Default value: `tidb-slow.log`
- The format of the slow log is updated in TiDB v2.1.8, so the slow log is output to the slow log file separately. In versions before v2.1.8, this variable is set to "" by default.
- After you set it, the slow query log is output to this file separately

### `slow-threshold`

- Outputs the threshold value of consumed time in the slow log
- Default value: `300ms`
- If the value in a query is larger than the default value, it is a slow query and is output to the slow log

### `expensive-threshold`

- Outputs the threshold value of the number of rows for the `expensive` operation
- Default value: `10000`
- When the number of query rows (including the intermediate results based on statistics) is larger than this value, it is an `expensive` operation and outputs log with the `[EXPENSIVE_QUERY]` prefix.

### `query-log-max-len`

- The maximum length of SQL output
- Default value: `2048`
- When the length of the statement is longer than `query-log-max-len`, the statement is truncated to output.

## log.file

Configuration items related to log files

#### `filename`

- The file name of the general log file
- Default value: ""
- If you set it, the log is output to this file

#### `max-size`

- The size limit of the log file
- Default value: 300MB
- The maximum size is 4GB.

#### `max-days`

- The maximum number of days that the log is retained
- Default value: `0`
- The log is retained by default. If you set the value, the expired log is cleaned up after `max-days`.

#### `max-backups`

- The maximum number of retained logs
- Default value: `0`
- All the log files are retained by default. If you set it to `7`, seven log files are retained at maximum.

#### `log-rotate`

- Determines whether to create a new log file every day
- Default value: `true`
- If you set the parameter to `true`, a new log file is created every day. If you set it to `false`, the log is output to a single log file.

## Security

Configuration items related to security

### `ssl-ca`

- The file path of the trusted CA certificate in the PEM format
- Default value: ""
- If you set this option and `--ssl-cert`, `--ssl-key` at the same time, TiDB authenticates the client certificate based on the list of trusted CAs specified by this option when the client presents the certificate. If the authentication fails, the connection is terminated.
- If you set this option but the client does not present the certificate, the secure connection continues without client certificate authentication.

### `ssl-cert`

- The file path of the SSL certificate in the PEM format
- Default value: ""
- If you set this option and `--ssl-key` at the same time, TiDB allows (but not forces) the client to securely connect to TiDB using TLS
- If the specified certificate or private key is invalid, TiDB starts as usual but cannot receive secure connection

### `ssl-key`

- The file path of the SSL certificate key in the PEM format, that is the private key of the certificate specified by `--ssl-cert`
- Default value: ""
- Currently, TiDB does not support loading the private keys protected by passwords

### `cluster-ssl-ca`

- The CA root certificate used to connect TiKV or PD with TLS
- Default value: ""

### `cluster-ssl-cert`

- The path of the SSL certificate file used to connect TiKV or PD with TLS
- Default value: ""

### `cluster-ssl-key`

- The path of the SSL private key file used to connect TiKV or PD with TLS
- Default value: ""

### `skip-grant-table`

- Determines whether to skip permission check
- Default value: `false`

## Performance

Configuration items related to performance

### `max-procs`

- The number of CPUs used by TiDB
- Default value: `0`
- The default `0` indicates using all the CPUs on the machine. You can also set it to `n`, and then TiDB uses `n` CPUs.

### `max-memory`

- The maximum memory limit for the Prepared Least Recently Used (LRU) caching. If this value exceeds `performance.max-memory * (1 - prepared-plan-cache.memory-guard-ratio)`, the elements in the LRU are removed.
- Default value: `0`
- This configuration only takes effect when `prepared-plan-cache.enabled` is `true`. When the size of the LRU is greater than `prepared-plan-cache.capacity`, the elements in the LRU are also removed.

### `stmt-count-limit`

- The maximum number of statements allowed in a single TiDB transaction
- Default value: `5000`
- If a transaction does not roll back or commit after the number of statements exceeds `stmt-count-limit`, TiDB returns the `statement count 5001 exceeds the transaction limitation, autocommit = false` error.

### `tcp-keep-alive`

- Determines whether to enable `keepalive` in the TCP layer
- Default value: `false`

### `cross-join`

- Default value: `true`
- TiDB supports executing the `JOIN` statement without any condition (the `WHERE` field) of both sides tables by default; if you set the value to `false`, the server refuses to execute when such a `JOIN` statement appears

### `stats-lease`

- The time interval of reloading statistics, updating the number of table rows, checking whether it is needed to perform the automatic analysis, using feedback to update statistics and loading statistics of columns
- Default value: `3s`
    - At intervals of `stats-lease` time, TiDB checks the statistics for updates and updates them to the memory if updates exist
    - At intervals of `20 \* stats-lease` time, TiDB updates the total number of rows generated by DML and the number of modified rows to the system table
    - At intervals of `stats-lease`, TiDB checks for tables and indexes that need to be automatically analyzed
    - At intervals of `stats-lease`, TiDB checks for column statistics that need to be loaded to the memory
    - At intervals of `200 \* stats-lease`, TiDB writes the feedback cached in the memory to the system table
    - At intervals of `5 \* stats-lease`, TiDB reads the feedback in the system table, and updates the statistics cached in the memory
- When `stats-lease` is set to 0, TiDB periodically reads the feedback in the system table, and updates the statistics cached in the memory every three seconds. But TiDB no longer automatically modifies the following statistics-related system tables:
    - `mysql.stats_meta`: TiDB no longer automatically records the number of table rows that are modified by the transaction and updates it to this system table
    - `mysql.stats_histograms`/`mysql.stats_buckets` and `mysql.stats_top_n`: TiDB no longer automatically analyzes and proactively updates statistics
    - `mysql.stats_feedback`: TiDB no longer updates the statistics of the tables and indexes according to a part of statistics returned by the queried data

### `run-auto-analyze`

- Determines whether TiDB executes automatic analysis
- Default value: `true`

### `feedback-probability`

- The probability that TiDB collects the feedback statistics of each query
- Default value: `0.05`
- TiDB collects the feedback of each query at the probability of `feedback-probability`, to update statistics

### `query-feedback-limit`

- The maximum pieces of query feedback that can be cached in memory. Extra pieces of feedback that exceed this limit are discarded.
- Default value: `1024`

### `pseudo-estimate-ratio`

- The ratio of (number of modified rows)/(total number of rows) in a table. If the value is exceeded, the system assumes that the statistics have expired and the pseudo statistics will be used.
- Default value: `0.8`
- The minimum value is `0` and the maximum value is `1`.

### `force-priority`

- Sets the priority for all statements
- Default: `NO_PRIORITY`
- Optional values: `NO_PRIORITY`, `LOW_PRIORITY`, `HIGH_PRIORITY`, `DELAYED`

## prepared-plan-cache

The Plan Cache configuration of the `PREPARE` statement

### `enabled`

- Determines whether to enable Plan Cache of the `PREPARE` statement
- Default value: `false`

### `capacity`

- The number of cached statements
- Default value: `100`

### `memory-guard-ratio`

- It is used to prevent `performance.max-memory` from being exceeded. When `max-proc * (1 - prepared-plan-cache.memory-guard-ratio)` is exceeded, the elements in the LRU are removed.
- Default value: `0.1`
- The minimum value is `0`; the maximum value is `1`

## tikv-client

### `grpc-connection-count`

- The maximum number of connections established with each TiKV
- Default value: `16`

### `grpc-keepalive-time`

- The `keepalive` time interval of the RPC connection between TiDB and TiKV nodes. If there is no network packet within the specified time interval, the gRPC client executes `ping` command to TiKV to see if it is alive.
- Default: `10`
- unit: second

### `grpc-keepalive-timeout`

- The timeout of the RPC `keepalive` check between TiDB and TiKV nodes
- Default value: `3`
- unit: second

### `commit-timeout`

- The maximum timeout when executing a transaction commit
- Default value: `41s`
- It is required to set this value larger than twice of the Raft election timeout.

### `max-txn-time-use`

- The maximum execution time allowed for a single transaction
- Default value: `590`
- unit: second

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

### txn-local-latches

Configuration related to the transaction latch. It is recommended to enable it when many local transaction conflicts occur.

### `enable`

- Determines whether to enable the memory lock of transactions
- Default value: `false`

### `capacity`

- The number of slots corresponding to Hash, which automatically adjusts upward to an exponential multiple of 2. Each slot occupies 32 Bytes of memory. If set too small, it might result in slower running speed and poor performance in the scenario where data writing covers a relatively large range (such as importing data).
- Default value: `1024000`

## binlog

Configurations related to TiDB Binlog

### `enable`

- Enables or disables binlog
- Default value: `false`

### `write-timeout`

- The timeout of writing binlog into Pump. It is recommended not to modify this value.
- Default: `15s`
- unit: second

### `ignore-error`

- Determines whether to ignore errors occurred in the process of writing binlog into Pump. It is recommended not to modify this value.
- Default value: `false`
- When the value is set to `true` and an error occurs, the writing is stopped and `1` is summed to the monitoring item `tidb_server_critical_error_total`. When the value is `false`, the writing fails and the entire TiDB service is stopped.

### `binlog-socket`

- The network address to which binlog is exported
- Default value: ""

### `strategy`

- The strategy of Pump selection when binlog is exported. Currently, only the `hash` and `range` methods are supported.
- Default value: `range`

## status

Configuration related to the status of TiDB service

### `report-status`

- Enables or disables the HTTP API service
- Default value: true

### `record-db-qps`

- Determines whether to transmit the database-related QPS metrics to Prometheus
- Default value: `false`
