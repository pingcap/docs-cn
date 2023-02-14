---
title: TiDB Monitoring Metrics
summary: Learn some key metrics displayed on the Grafana TiDB dashboard.
aliases: ['/docs/dev/grafana-tidb-dashboard/','/docs/dev/reference/key-monitoring-metrics/tidb-dashboard/']
---

# TiDB Monitoring Metrics

If you use TiUP to deploy the TiDB cluster, the monitoring system (Prometheus & Grafana) is deployed at the same time. For the monitoring architecture, see [TiDB Monitoring Framework Overview](/tidb-monitoring-framework.md).

The Grafana dashboard is divided into a series of sub dashboards which include Overview, PD, TiDB, TiKV, Node\_exporter, Disk Performance, and Performance\_overview. The TiDB dashboard consists of the TiDB panel and the TiDB Summary panel. The differences between the two panels are different in the following aspects:

- TiDB panel: provides as comprehensive information as possible for troubleshooting cluster anomalies.
- TiDB Summary Panel: extracts parts of the TiDB panel information with which users are most concerned, with some modifications. It provides data (such as QPS, TPS, response delay) that users care about in the daily database operations, which serves as the monitoring information to be displayed or reported.

This document describes some key monitoring metrics displayed on the TiDB dashboard.

## Key metrics description

To understand the key metrics displayed on the TiDB dashboard, check the following sections:

### Query Summary

- Duration: execution time
    - The duration between the time that the client's network request is sent to TiDB and the time that the request is returned to the client after TiDB has executed it. In general, client requests are sent in the form of SQL statements, but can also include the execution time of commands such as `COM_PING`, `COM_SLEEP`, `COM_STMT_FETCH`, and `COM_SEND_LONG_DATA`
    - Because TiDB supports Multi-Query, it supports sending multiple SQL statements at one time, such as `select 1; select 1; select 1;`. In this case, the total execution time of this query includes the execution time of all SQL statements
- Command Per Second: the number of commands processed by TiDB per second, which is classified according to the success or failure of command execution results
- QPS: the number of SQL statements executed per second on all TiDB instances, which is counted according to `SELECT`, `INSERT`, `UPDATE`, and other types of statements
- CPS By Instance: the command statistics on each TiDB instance, which is classified according to the success or failure of command execution results
- Failed Query OPM: the statistics of error types (such as syntax errors and primary key conflicts) according to the errors occurred when executing SQL statements per minute on each TiDB instance. It contains the module in which the error occurs and the error code
- Slow query: the statistics of the processing time of slow queries (the time cost of the entire slow query, the time cost of Coprocessor, and the waiting time for Coprocessor scheduling). Slow queries are classified into internal and general SQL statements
- Connection Idle Duration: the duration of idle connections
- 999/99/95/80 Duration: the statistics of the execution time for different types of SQL statements (different percentiles)

### Query Detail

- Duration 80/95/99/999 By Instance: the statistics of the execution time for SQL statements on each TiDB instance (different percentiles)
- Failed Query OPM Detail: the statistics of error types (such as syntax errors and primary key conflicts) according to the errors occurred when executing SQL statements per minute on each TiDB instance
- Internal SQL OPS: the internal SQL statements executed per second in the entire TiDB cluster. The internal SQL statements are internally executed and are generally triggered by user SQL statements or internally scheduled tasks.

### Server

- Uptime: the runtime of each TiDB instance
- Memory Usage: the memory usage statistics of each TiDB instance, which is divided into the memory occupied by processes and the memory applied by Golang on the heap
- CPU Usage: the statistics of CPU usage of each TiDB instance
- Connection Count: the number of clients connected to each TiDB instance
- Open FD Count: the statistics of opened file descriptors of each TiDB instance
- Disconnection Count: the number of clients disconnected to each TiDB instance
- Events OPM: the statistics of key events, such as "start", "close", "graceful-shutdown","kill", and "hang"
- Goroutine Count: the number of Goroutines on each TiDB instance
- Prepare Statement Count: the number of `Prepare` statements that are executed on each TiDB instance and the total count of them
- Keep Alive OPM: the number of times that the metrics are refreshed every minute on each TiDB instance. It usually needs no attention.
- Panic And Critical Error: the number of panics and critical errors occurred in TiDB
- Time Jump Back OPS: the number of times that the operating system rewinds every second on each TiDB instance
- Get Token Duration: the time cost of getting Token on each connection
- Skip Binlog Count: the number of binlog write failures in TiDB
- Client Data Traffic: data traffic statistics of TiDB and the client

### Transaction

- Transaction OPS: the number of transactions executed per second
- Duration: the execution duration of a transaction
- Transaction Statement Num: the number of SQL statements in a transaction
- Transaction Retry Num: the number of times that a transaction retries
- Session Retry Error OPS: the number of errors encountered during the transaction retry per second. This metric includes two error types: retry failure and exceeding the maximum number of retries
- Commit Token Wait Duration: the wait duration in the flow control queue during the transaction commit. If the wait duration is long, it means that the transaction to commit is too large and the flow is controlled. If the system still has resources available, you can speed up the commit process by increasing the system variable `tidb_committer_concurrency`.
- KV Transaction OPS: the number of transactions executed per second within each TiDB instance
    - A user transaction might trigger multiple transaction executions in TiDB, including reading internal metadata and atomic retries of the user transaction
    - TiDB's internally scheduled tasks also operate on the database through transactions, which are also included in this panel
- KV Transaction Duration: the time spent on executing transactions within each TiDB
- Transaction Regions Num: the number of Regions operated in the transaction
- Transaction Write KV Num Rate and Sum: the rate at which KVs are written and the sum of these written KVs in the transaction
- Transaction Write KV Num: the number of KVs operated in the transaction
- Statement Lock Keys: the number of locks for a single statement
- Send HeartBeat Duration: the duration for the transaction to send heartbeats
- Transaction Write Size Bytes Rate and sum: the rate at which bytes are written and the sum of these written bytes in the transaction
- Transaction Write Size Bytes: the size of the data written in the transaction
- Acquire Pessimistic Locks Duration: the time consumed by adding locks
- TTL Lifetime Reach Counter: the number of transactions that reach the upper limit of TTL. The default value of the TTL upper limit is 1 hour. It means that 1 hour has passed since the first lock of a pessimistic transaction or the first prewrite of an optimistic transaction. The default value of the upper limit of TTL is 1 hour. The upper limit of TTL life can be changed by modifying `max-txn-TTL` in the TiDB configuration file
- Load Safepoint OPS: the number of times that `Safepoint` is loaded. `Safepoint` is to ensure that the data before `Safepoint` is not read when the transaction reads data, thus ensuring data safety. The data before `Safepoint` might be cleaned up by the GC
- Pessimistic Statement Retry OPS: the number of retry attempts for pessimistic statements. When the statement tries to add lock, it might encounter a write conflict. At this time, the statement will acquire a new snapshot and add lock again
- Transaction Types Per Seconds: the number of transactions committed per second using the two-phase commit (2PC), async commit, and one-phase commit (1PC) mechanisms, including both success and failure transactions

### Executor

- Parse Duration: the statistics of the parsing time of SQL statements
- Compile Duration: the statistics of the time of compiling the parsed SQL AST to the execution plan
- Execution Duration: the statistics of the execution time for SQL statements
- Expensive Executor OPS: the statistics of the operators that consume many system resources per second, including `Merge Join`, `Hash Join`, `Index Look Up Join`, `Hash Agg`, `Stream Agg`, `Sort`, and `TopN`
- Queries Using Plan Cache OPS: the statistics of queries using the Plan Cache per second
- Plan Cache Miss OPS: the statistics of the number of times that the Plan Cache is missed per second
- Plan Cache Memory Usage: the total memory consumed by the execution plan cached in each TiDB instance
- Plan Cache Plan Num: the total number of execution plans cached in each TiDB instance

### Distsql

- Distsql Duration: the processing time of Distsql statements
- Distsql QPS: the statistics of Distsql statements
- Distsql Partial QPS: the number of Partial results every second
- Scan Keys Num: the number of keys that each query scans
- Scan Keys Partial Num: the number of keys that each Partial result scans
- Partial Num: the number of Partial results for each SQL statement

### KV Errors

- KV Backoff Duration: the total duration that a KV retry request lasts. TiDB might encounter an error when sending a request to TiKV. TiDB has a retry mechanism for every request to TiKV. This `KV Backoff Duration` item records the total time of a request retry.
- TiClient Region Error OPS: the number of Region related error messages returned by TiKV
- KV Backoff OPS: the number of error messages returned by TiKV
- Lock Resolve OPS: the number of TiDB operations to resolve locks. When TiDB's read or write request encounters a lock, it tries to resolve the lock
- Other Errors OPS: the number of other types of errors, including clearing locks and updating `SafePoint`

### KV Request

- KV Request OPS: the execution times of a KV request, displayed according to TiKV
- KV Request Duration 99 by store: the execution time of a KV request, displayed according to TiKV
- KV Request Duration 99 by type: the execution time of a KV request, displayed according to the request type

### PD Client

- PD Client CMD OPS: the statistics of commands executed by PD Client per second
- PD Client CMD Duration: the time it takes for PD Client to execute commands
- PD Client CMD Fail OPS: the statistics of failed commands executed by PD Client per second
- PD TSO OPS: the number of TSO that TiDB obtains from PD per second
- PD TSO Wait Duration: the time that TiDB waits for PD to return TSO
- PD TSO RPC duration: the duration from the time that TiDB sends request to PD (to get TSO) to the time that TiDB receives TSO
- Start TSO Wait Duration: the duration from the time that TiDB sends request to PD (to get `start TSO`) to the time that TiDB receives `start TSO`

### Schema Load

- Load Schema Duration: the time it takes TiDB to obtain the schema from TiKV
- Load Schema OPS: the statistics of the schemas that TiDB obtains from TiKV per second
- Schema Lease Error OPM: the Schema Lease errors include two types: `change` and `outdate`. `change` means that the schema has changed, and `outdate` means that the schema cannot be updated, which is a more serious error and triggers an alert.
- Load Privilege OPS: the statistics of the number of privilege information obtained by TiDB from TiKV per second

### DDL

- DDL Duration 95: 95% quantile of DDL statement processing time
- Batch Add Index Duration 100: statistics of the maximum time spent by each Batch on creating an index
- DDL Waiting Jobs Count: the number of DDL tasks that are waiting
- DDL META OPM: the number of times that a DDL obtains META every minute
- DDL Worker Duration 99: 99% quantile of the execution time of each DDL worker
- Deploy Syncer Duration: the time consumed by Schema Version Syncer initialization, restart, and clearing up operations
- Owner Handle Syncer Duration: the time that it takes the DDL Owner to update, obtain, and check the Schema Version
- Update Self Version Duration: the time consumed by updating the version information of Schema Version Syncer
- DDL OPM: the number of DDL executions per second
- DDL Add Index Progress In Percentage: the progress of adding an index

### Statistics

- Auto Analyze Duration 95: the time consumed by automatic `ANALYZE`
- Auto Analyze QPS: the statistics of automatic `ANALYZE`
- Stats Inaccuracy Rate: the information of the statistics inaccuracy rate
- Pseudo Estimation OPS: the number of the SQL statements optimized using pseudo statistics
- Dump Feedback OPS: the number of stored statistical feedbacks
- Store Query Feedback QPS: the number of operations per second to store the feedback information of the union query, which is performed in TiDB memory
- Significant Feedback: the number of significant feedback pieces that update the statistics information
- Update Stats OPS: the number of operations of updating statistics with feedback
- Fast Analyze Status 100: the status for quickly collecting statistical information

### Owner

- New ETCD Session Duration 95: the time it takes to create a new etcd session. TiDB connects to etcd in PD through etcd client to save/read some metadata information. This records the time spent creating the session
- Owner Watcher OPS: the number of Goroutine operations per second of DDL owner watch PD's etcd metadata

### Meta

- AutoID QPS: AutoID related statistics, including three operations (global ID allocation, a single table AutoID allocation, a single table AutoID Rebase)
- AutoID Duration: the time consumed by AutoID related operations
- Region Cache Error OPS: the number of errors encountered per second by the cached Region information in TiDB
- Meta Operations Duration 99: the latency of Meta operations

### GC

- Worker Action OPM: the number of GC related operations, including `run_job`, `resolve_lock`, and `delete_range`
- Duration 99: the time consumed by GC related operations
- Config: the configuration of GC data life time and GC running interval
- GC Failure OPM: the number of failed GC related operations
- Delete Range Failure OPM: the number of times the `Delete Range` has failed
- Too Many Locks Error OPM: the number of the error that GC clears up too many locks
- Action Result OPM: the number of results of GC-related operations
- Delete Range Task Status: the task status of `Delete Range`, including completion and failure
- Push Task Duration 95: the time spent pushing GC subtasks to GC workers

### Batch Client

- Pending Request Count by TiKV: the number of Batch messages that are pending processing
- Batch Client Unavailable Duration 95: the unavailable time of the Batch client
- No Available Connection Counter: the number of times the Batch client cannot find an available link

### TTL

- TTL QPS By Type: the QPS information of different types of statements generated by TTL jobs.
- TTL Processed Rows Per Second: the number of expired rows processed by TTL jobs per second.
- TTL Scan/Delete Query Duration: the execution time of TTL scan/delete statements.
- TTL Scan/Delete Worker Time By Phase: the time consumed by different phases of TTL internal worker threads.
- TTL Job Count By Status: the number of TTL jobs currently being executed.
