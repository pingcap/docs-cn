---
title: TiDB Monitoring Metrics
summary: Learn some key metrics displayed on the Grafana TiDB dashboard.
category: reference
aliases: ['/docs/op-guide/tidb-dashboard-info/','/docs/dev/reference/key-monitoring-metrics/tidb/']
---

# TiDB Monitoring Metrics

If you use Ansible to deploy the TiDB cluster, the monitoring system is deployed at the same time. For more information, see [TiDB Monitoring Framework Overview](/how-to/monitor/overview.md).

The Grafana dashboard is divided into a series of sub dashboards which include Overview, PD, TiDB, TiKV, Node\_exporter, Disk Performance, and so on. The TiDB dashboard consists of the TiDB panel and the TiDB Summary panel, and what displays on the TiDB Summary panel also displays on the TiDB panel. A lot of metrics are there to help you diagnose.

This document describes some key monitoring metrics displayed on the TiDB dashboard.

## Key metrics description

To understand the key metrics displayed on the TiDB dashboard, check the following list:

- Query Summary
    - Duration: the execution time of a SQL statement
    - QPS: the statistics of OKs and Errors according to the SQL execution result on each TiDB instance
    - Statement OPS: the statistics of executed SQL statements (including `SELECT`, `INSERT`, `UPDATE` and so on)
    - QPS By Instance: the QPS on each TiDB instance
    - Failed Query OPM: the statistics of error types (such as syntax errors and primary key conflicts) according to the errors happening when executing SQL statements on each TiDB instance
    - Slow query: the statistics of the processing time of slow queries (the time cost of the entire slow query, the time cost of Coprocessor，and the waiting time for Coprocessor scheduling)
    - 999/99/95/80 Duration: the statistics of the execution time for different types of SQL statements (different percentiles)

- Query Detail
    - Duration 80/95/99/999 By Instance: the statistics of the execution time for SQL statements on each TiDB instance (different percentiles)
    - Failed Query OPM Detail: the statistics of error types (such as syntax errors and primary key conflicts) according to the errors happening when executing SQL statements in the entire cluster
    - Internal SQL OPS: the statistics of the executed SQL statements within TiDB

- Server
    - Uptime: the runtime of TiDB
    - Memory Usage: the statistics of memory usage of different TiDB instances
    - CPU Usage: the statistics of CPU usage of different TiDB instances
    - Connection Count: the number of clients connected to each TiDB instance
    - Open FD Count: the statistics of opened file descriptors of different TiDB instances
    - Goroutine Count: the number of Goroutines of different TiDB instances
    - Go GC Duration: the statistics of GC time of different TiDB instances
    - Go Threads: the number of threads of different TiDB instances
    - Go GC Count: the number of times that GC is executed on different TiDB instances
    - Go GC CPU Usage: the statistics of GC CPU usage of different TiDB instances
    - Events OPM: the statistics of key events, such as "start", "close", "graceful-shutdown","kill", "hang", and so on
    - Keep Alive OPM: the number of times that the metrics are refreshed every minute on different TiDB instances
    - Prepare Statement Count: the number of `Prepare` statements that are executed on each TiDB instance and the total count of them
    - Time Jump Back OPS: the number of times that the time rewinds every second on different TiDB instances
    - Heap Memory Usage: the heap memory size used by each TiDB instance
    - Uncommon Error OPM: the statistics of abnormal TiDB errors, including panic, binlog write failure, and so on
    - Handshake Error OPS: the number of times that a handshake error occurs every second on different TiDB instances
    - Get Token Duration: the time cost of getting Token after establishing the connection

- Transaction
    - Transaction OPS: the statistics of executed transactions
    - Duration: the execution time of a transaction
    - Transaction Retry Num: the number of times that a transaction retries
    - Transaction Statement Num: the number of SQL statements in a transaction
    - Session Retry Error OPS: the number of errors encountered during the transaction retry
    - Local Latch Wait Duration: the waiting time of a local transaction

- Executor
    - Parse Duration: the statistics of the parsing time of SQL statements
    - Compile Duration: the statistics of the time of compiling an SQL AST to the execution plan
    - Execution Duration: the statistics of the execution time for SQL statements
    - Expensive Executor OPS: the statistics of the operators that consume many system resources, including `Merge Join`, `Hash Join`, `Index Look Up Join`, `Hash Agg`, `Stream Agg`, `Sort`, `TopN`, and so on
    - Queries Using Plan Cache OPS: the statistics of queries using the Plan Cache

- Distsql
    - Distsql Duration: the processing time of Distsql statements
    - Distsql QPS: the statistics of Distsql statements
    - Distsql Partial QPS: the number of Partial results every second
    - Scan Keys Num: the number of keys that each query scans
    - Scan Keys Partial Num: the number of keys that each Partial result scans
    - Partial Num: the number of Partial results for each SQL statement

- KV Errors
    - KV Retry Duration: the time that a KV retry request lasts
    - TiClient Region Error OPS: the number of Region related error messages returned by TiKV
    - KV Backoff OPS: the number of error messages (transaction conflicts and so on) returned by TiKV
    - Lock Resolve OPS: the number of errors related to transaction conflicts
    - Other Errors OPS: the number of other types of errors, including clearing locks and updating SafePoint

- KV Duration
    - KV Request Duration 999 by store: the execution time of a KV request, displayed according to TiKV
    - KV Request Duration 999 by type: the execution time of a KV request, displayed according to the request type
    - KV Cmd Duration 99/999: the execution time of KV commands

- KV Count
    - KV Cmd OPS: the statistics of executed KV commands
    - KV Txn OPS: the statistics of started transactions
    - Txn Regions Num 90: the statistics of Regions used by the transaction
    - Txn Write Size Bytes 100: the statistics of bytes written by the transaction
    - Txn Write KV Num 100: the statistics of KVs written by the transaction
    - Load SafePoint OPS: the statistics of operations that update SafePoint

- PD Client
    - PD Client CMD OPS: the statistics of commands executed by PD Client
    - PD Client CMD Duration: the time it takes PD Client to execute commands
    - PD Client CMD Fail OPS: the statistics of failed commands executed by PD Client
    - PD TSO OPS: the number of TSO that TiDB obtains from PD
    - PD TSO Wait Duration: the time it takes TiDB to obtain TSO from PD
    - PD TSO RPC Duration: the time it takes TiDB to obtain TSO gRPC interface from PD

- Schema Load
    - Load Schema Duration: the time it takes TiDB to obtain the schema from TiKV
    - Load Schema OPS: the statistics of the schemas that TiDB obtains from TiKV
    - Schema Lease Error OPM: the Schema Lease error, including two types named "change" and "outdate"; an alarm is triggered when an "outdate" error occurs

- DDL
    - DDL Duration 95: the statistics of DDL statements processing time
    - Batch Add Index Duration 100: the statistics of the time that it takes each Batch to create the index
    - DDL Waiting Jobs Count: the number of DDL tasks that are waiting
    - DDL META OPM: the number of times that a DDL obtains META every minute
    - Deploy Syncer Duration: the time consumed by Schema Version Syncer initialization, restart, and clearing up operations
    - Owner Handle Syncer Duration: the time that it takes the DDL Owner to update, obtain, and check the Schema Version
    - Update Self Version Duration: the time consumed by updating the version information of Schema Version Syncer

- Statistics
    - Auto Analyze Duration 95: the time consumed by automatic `ANALYZE`
    - Auto Analyze QPS: the statistics of automatic `ANALYZE`
    - Stats Inaccuracy Rate: the information of the statistics inaccuracy rate
    - Pseudo Estimation OPS: the number of the SQL statements optimized using pseudo statistics
    - Dump Feedback OPS: the number of stored statistical Feedbacks
    - Update Stats OPS: the statistics of using Feedback to update the statistics information
    - Significant Feedback: the number of significant Feedback pieces that update the statistics information

- Meta
    - AutoID QPS: AutoID related statistics, including three operations (global ID allocation, a single table AutoID allocation, a single table AutoID Rebase)
    - AutoID Duration: the time consumed by AutoID related operations
    - Meta Operations Duration 99: the latency of Meta operations

- GC
    - Worker Action OPM: the statistics of GC related operations, including `run_job`, `resolve_lock`, and `delete\_range`
    - Duration 99: the time consumed by GC related operations
    - GC Failure OPM: the number of failed GC related operations
    - Action Result OPM: the number of results of GC-related operations
    - Too Many Locks Error OPM: the number of the error that GC clears up too many locks

- Batch Client
    - Pending Request Count by TiKV: the number of Batch messages that are pending processing
    - Wait Duration 95: the waiting time of Batch messages that are pending processing
    - Batch Client Unavailable Duration 95: the unavailable time of the Batch client
