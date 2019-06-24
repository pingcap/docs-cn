---
title: TiDB Monitoring Metrics
summary: Learn some key metrics displayed on the Grafana TiDB dashboard.
category: reference
---

# TiDB Monitoring Metrics

If you use Ansible to deploy the TiDB cluster, the monitoring system is deployed at the same time. For more information, see [TiDB Monitoring Framework Overview](/how-to/monitor/overview.md).

The Grafana dashboard is divided into a series of sub dashboards which include Overview, PD, TiDB, TiKV, Node\_exporter, Disk Performance, and so on. A lot of metrics are there to help you diagnose.

This document describes some key monitoring metrics displayed on the TiDB dashboard.

## Key metrics description

To understand the key metrics displayed on the TiDB dashboard, check the following list:

- Query Summary
    - Duration: the execution time of a SQL statement
    - Statement OPS: the statistics of executed SQL statements (including `SELECT`, `INSERT`, `UPDATE` and so on)
    - QPS By Instance: the QPS on each TiDB instance

- Query Detail
    - Internal SQL OPS: the statistics of the executed SQL statements within TiDB

- Server
    - Connection Count: the number of clients connected to each TiDB instance
    - Failed Query OPM: the statistics of failed SQL statements, such as grammar mistake, primary key, and so on
    - Heap Memory Usage: the heap memory size used by each TiDB instance
    - Events OPM: the statistics of key events, such as "start", "close", "graceful-shutdown","kill", "hang", and so on
    - Uncommon Error OPM: the statistics of abnormal TiDB errors, including panic, binlog write failure, and so on

- Transaction
    - Transaction OPS: the statistics of executed transactions
    - Transaction Duration: the execution time of a transaction
    - Session Retry Error OPS: the number of errors encountered during the transaction retry

- Executor
    - Expensive Executor OPS: the statistics of the operators that consume many system resources, including `Merge Join`, `Hash Join`, `Index Look Up Join`, `Hash Agg`, `Stream Agg`, `Sort`, `TopN`, and so on
    - Queries Using Plan Cache OPS: the statistics of queries using the Plan Cache

- Distsql
    - Distsql Duration: the processing time of Distsql statements
    - Distsql QPS: the statistics of Distsql statements

- KV Errors
    - KV Retry Duration: the time that a KV retry request lasts
    - TiClient Region Error OPS: the number of Region related error messages returned by TiKV
    - KV Backoff OPS: the number of error messages (transaction conflicts and so on) returned by TiKV
    - Lock Resolve OPS: the number of errors related to transaction conflicts
    - Other Errors OPS: the number of other types of errors, including clearing locks and updating SafePoint

- KV Duration
    - KV Cmd Duration 99: the execution time of KV commands

- KV Count
    - KV Cmd OPS: the statistics of executed KV commands
    - Txn OPS: the statistics of started transactions
    - Load SafePoint OPS: the statistics of operations that update SafePoint

- PD Client
    - PD TSO OPS: the number of TSO that TiDB obtains from PD
    - PD TSO Wait Duration: the time it takes TiDB to obtain TSO from PD
    - PD Client CMD OPS: the statistics of commands executed by PD Client
    - PD Client CMD Duration: the time it takes PD Client to execute commands
    - PD Client CMD Fail OPS: the statistics of failed commands executed by PD Client

- Schema Load
    - Load Schema Duration: the time it takes TiDB to obtain the schema from TiKV
    - Load Schema OPS: the statistics of the schemas that TiDB obtains from TiKV
    - Schema Lease Error OPM: the Schema Lease error, including two types named "change" and "outdate"; an alarm is triggered when an "outdate" error occurs

- DDL
    - DDL Duration 95: the statistics of DDL statements processing time
    - DDL Batch Add Index Duration 100: the statistics of the time that it takes each Batch to create the index
    - DDL Deploy Syncer Duration: the time consumed by Schema Version Syncer initialization, restart, and clearing up operations
    - Owner Handle Syncer Duration: the time that it takes the DDL Owner to update, obtain, and check the Schema Version
    - Update Self Version Duration: the time consumed by updating the version information of Schema Version Syncer

- Statistics
    - Auto Analyze Duration 95: the time consumed by automatic `ANALYZE`
    - Auto Analyze QPS: the statistics of automatic `ANALYZE`
    - Stats Inaccuracy Rate: the information of the statistics inaccuracy rate
    - Pseudo Estimation OPS: the number of the SQL statements optimized using pseudo statistics
    - Dump Feedback OPS: the number of stored statistical Feedbacks
    - Update Stats OPS: the statistics of using Feedback to update the statistics information

- Meta
    - AutoID QPS: AutoID related statistics, including three operations (global ID allocation, a single table AutoID allocation, a single table AutoID Rebase)
    - AutoID Duration: the time consumed by AutoID related operations

- GC
    - Worker Action OPM: the statistics of GC related operations, including `run_job`, `resolve_lock`, and `delete\_range`
    - Duration 99: the time consumed by GC related operations
    - GC Failure OPM: the number of failed GC related operations
    - Too Many Locks Error OPM: the number of the error that GC clears up too many locks
