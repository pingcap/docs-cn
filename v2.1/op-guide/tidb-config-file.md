---
title: TiDB Configuration File Description
summary: Learn the TiDB configuration file options that are not involved in command line options.
category: deployment
---

# TiDB Configuration File Description

The TiDB configuration file supports more options than command line options. You can find the default configuration file in [config/config.toml.example](https://github.com/pingcap/tidb/blob/master/config/config.toml.example) and rename it to `config.toml`.

This document describes the options that are not involved in command line options. For command line options, see [here](../op-guide/configuration.md).

### `split-table`

- To create a separate Region for each table
- Default: true
- It is recommended to set it to false if you need to create a large number of tables

### `oom-action`

- To specify the operation when out-of-memory occurs in TiDB
- Default: "log"
- The valid options are "log" and "cancel"; "log" only prints the log, without actual processing; "cancel" cancels the operation and outputs the log

### `enable-streaming`

- To enable the data fetch mode of streaming in Coprocessor
- Default: false

### `lower-case-table-names`

- To configure the value of the `lower_case_table_names` system variable
- Default: 2
- For details, you can see the [MySQL description](https://dev.mysql.com/doc/refman/5.7/en/server-system-variables.html#sysvar_lower_case_table_names) of this variable
- Currently, TiDB only supports setting the value of this option to 2. This means it is case-sensitive when you save a table name, but case-insensitive when you compare table names. The comparison is based on the lower case.

### `compatible-kill-query`

+ To set the "kill" statement to be MySQL compatible
+ Default: false
+ In TiDB, the behavior of "kill xxx" is not compatible with MySQL. A query is killed only when you are executing "kill tidb xxx". If `compatible-kill-query` is set to true, the "kill xxx" is compatible with MySQL, so no additional "tidb" is needed.

## Log

Configuration about log.

### `format`

- To specify the log output format
- The valid options are "json", "text" and "console"
- Default: "text"

### `disable-timestamp`

- Whether to disable outputting timestamp in the log
- Default: false
- If you set the value to true, the log does not output timestamp

### `slow-query-file`

- The file name of the slow query log
- Default: ""
- After you set it, the slow query log is output to this file separately

### `slow-threshold`

- To output the threshold value of consumed time in the slow log
- Default: 300ms
- If the value in a query is larger than the default value, it is a slow query and is output to the slow log

### `expensive-threshold`

- To output the threshold value of the number of rows for the `expensive` operation
- Default: 10000
- When the number of query rows (including the intermediate results based on statistics) is larger than this value, it is an `expensive` operation and outputs log with the `[EXPENSIVE_QUERY]` prefix.

### `query-log-max-len`

- The maximum length of SQL output
- Default: 2048
- When the length of the statement is longer than `query-log-max-len`, the statement is truncated to output

### log.file

#### `filename`

- The file name of the general log file
- Default: ""
- If you set it, the log is output to this file

#### `max-size`

- The size limit of the log file
- Default: 300MB
- The maximum size is 4GB

#### `max-days`

- The maximum number of days that the log is retained
- Default: 0
- The log is retained by default; if you set the value, the expired log is cleaned up after `max-days`

#### `max-backups`

- The maximum number of retained logs
- Default: 0
- All the log files are retained by default; if you set it to 7, 7 log files are retained at maximum

#### `log-rotate`

- Whether to create a new log file every day
- Default: true
- If you set it to true, a new log file is created every day; if you set it to false, the log is output to a single log file

## Security

Configuration about security.

### `ssl-ca`

- The file path of the trusted CA certificate in the PEM format
- Default: ""
- If you set this option and `--ssl-cert`, `--ssl-key` at the same time, TiDB authenticates the client certificate based on the list of trusted CAs specified by this option when the client presents the certificate. If the authentication fails, the connection is terminated.
- If you set this option but the client does not present the certificate, the secure connection continues without client certificate authentication.

### `ssl-cert`

- The file path of the SSL certificate in the PEM format
- Default: ""
- If you set this option and `--ssl-key` at the same time, TiDB allows (but not forces) the client to securely connect to TiDB using TLS
- If the specified certificate or private key is invalid, TiDB starts as usual but cannot receive secure connection

### `ssl-key`

- The file path of the SSL certificate key in the PEM format, that is the private key of the certificate specified by `--ssl-cert`
- Default: ""
- Currently, TiDB does not support loading the private keys protected by passwords

## Performance

Configuration about performance.

### `max-procs`

- The number of CPUs used by TiDB
- Default: 0
- The default "0" indicates using all CPUs in the machine; you can also set it to `max-procs`, and then TiDB uses `max-procs` CPUs

### `stmt-count-limit`

- The maximum number of statements allowed in a single TiDB transaction
- Default: 5000
- If a transaction does not roll back or commit after the number of statements exceeds `stmt-count-limit`, TiDB returns the `statement count 5001 exceeds the transaction limitation, autocommit = false` error

### `tcp-keep-alive`

- To enable `keepalive` in the TCP layer
- Default: false

### `retry-limit`

- The number of retries that TiDB makes when it encounters a `key` conflict or other errors while committing a transaction
- Default: 10
- If the number of retries exceeds `retry-limit` but the transaction still fails, TiDB returns an error

### `cross-join`

- Default: true
- TiDB supports executing the `join` statement without any condition (the `where` field) of both sides tables by default; if you set the value to false, the server refuses to execute when such a `join` statement appears

### `stats-lease`

- The time interval between analyzing TiDB statistics and reloading statistics
- Default: 3s
    - At intervals of `stats-lease` time, TiDB checks the statistics for updates and updates them to the memory if updates exist
    - At intervals of `5 * stats-lease` time, TiDB persists the total number of rows generated by DML and the number of modified rows
    - At intervals of `stats-lease`, TiDB checks for tables and indexes that need to be automatically analyzed
    - At intervals of `stats-lease`, TiDB checks for column statistics that need to be loaded to the memory

### `run-auto-analyze`

- Whether TiDB executes automatic analysis
- Default: true

### `feedback-probability`

- The probability that TiDB collects the feedback statistics of each query
- Default: 0.0
- TiDB collects the feedback of each query at the probability of `feedback-probability`, to update statistics

## prepared-plan-cache

The Plan Cache configuration of the `prepare` statement.

### `enabled`

- To enable Plan Cache of the `prepare` statement
- Default: false

### `capacity`

- The number of cached statements
- Default: 100

## tikv-client

### `grpc-connection-count`

- The maximum number of connections established with each TiKV
- Default: 16

### `commit-timeout`

- The maximum timeout time when executing a transaction commit
- Default: 41s
- It is required to set this value larger than twice of the Raft election timeout time

### txn-local-latches

Configuration about the transaction latch. It is recommended to enable it when many local transaction conflicts occur.

### `enable`

- To enable
- Default: false

### `capacity`

- The number of slots corresponding to Hash, which automatically adjusts upward to an exponential multiple of 2. Each slot occupies 32 Bytes of memory. If set too small, it might result in slower running speed and poor performance in the scenario where data writing covers a relatively large range (such as importing data).
- Default: 1024000
