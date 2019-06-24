---
title: TiDB 2.1 Beta Release Notes
category: Releases
---

# TiDB 2.1 Beta Release Notes

On June 29, 2018, TiDB 2.1 Beta is released! Compared with TiDB 2.0, this release has great improvement in stability, SQL optimizer, statistics information, and execution engine.

## TiDB

- SQL Optimizer
    - Optimize the selection range of `Index Join` to improve the execution performance
    - Optimize correlated subquery, push down `Filter`, and extend the index range, to improve the efficiency of some queries by orders of magnitude
    - Support `Index Hint` and `Join Hint` in the `UPDATE` and `DELETE` statements
    - Validate Hint `TIDM_SMJ` when no available index exists
    - Support pushdown of the `ABS`, `CEIL`, `FLOOR`, `IS TRUE`, and `IS FALSE` functions
    - Handle the `IF` and `IFNULL` functions especially in the constant folding process
- SQL Execution Engine
    - Implement parallel `Hash Aggregate` operators and improve the computing performance of `Hash Aggregate` by 350% in some scenarios
    - Implement parallel `Project` operators and improve the performance by 74% in some scenarios 
    - Read the data of the `Inner` table and `Outer` table of `Hash Join` concurrently to improve the execution performance
    - Fix incorrect results of `INSERT … ON DUPLICATE KEY UPDATE …` in some scenarios
    - Fix incorrect results of the `CONCAT_WS`, `FLOOR`, `CEIL`, and `DIV` built-in functions
- Server
    - Add the HTTP API to scatter the distribution of table Regions in the TiKV cluster
    - Add the `auto_analyze_ratio` system variable to control the threshold value of automatic `Analyze` 
    - Add the HTTP API to control whether to open the general log
    - Add the HTTP API to modify the log level online
    - Add the user information in the general log and the slow query log
    - Support the server side cursor
- Compatibility
    - Support more MySQL syntax
    - Make the `bit` aggregate function support the `ALL` parameter
    - Support the `SHOW PRIVILEGES` statement
- DML
    - Decrease the memory usage of the `INSERT INTO SELECT` statement 
    - Fix the performance issue of `PlanCache`
    - Add the `tidb_retry_limit` system variable to control the automatic retry times of transactions
    - Add the `tidb_disable_txn_auto_retry` system variable to control whether the transaction tries automatically
    - Fix the accuracy issue of the written data of the `time` type
    - Support the queue of locally conflicted transactions to optimize the conflicted transaction performance
    - Fix `Affected Rows` of the `UPDATE` statement 
    - Optimize the statement performance of `insert ignore on duplicate key update`
- DDL
    - Optimize the execution speed of the `CreateTable` statement
    - Optimize the execution speed of `ADD INDEX` and improve it greatly in some scenarios
    - Fix the issue that the number of added columns by `Alter table add column` exceeds the limit of the number of table columns 
    - Fix the issue that DDL job retries lead to an increasing pressure on TiKV in abnormal conditions
    - Fix the issue that TiDB continuously reloads the schema information in abnormal conditions
    - Do not output the `FOREIGN KEY` related information in the result of `SHOW CREATE TABLE`
    - Support the `select tidb_is_ddl_owner()` statement to facilitate judging whether TiDB is `DDL Owner`
    - Fix the issue that the index is deleted in the `Year` type in some scenarios
    - Fix the renaming table issue in the concurrent execution scenario
    - Support the `AlterTableForce` syntax
    - Support the `AlterTableRenameIndex` syntax with `FromKey` and `ToKey`
    - Add the table name and database name in the output information of `admin show ddl jobs`

## PD

- Enable Raft PreVote between PD nodes to avoid leader reelection when network recovers after network isolation
- Optimize the issue that Balance Scheduler schedules small Regions frequently
- Optimize the hotspot scheduler to improve its adaptability in traffic statistics information jitters
- Skip the Regions with a large number of rows when scheduling `region merge` 
- Enable `raft learner` by default to lower the risk of unavailable data caused by machine failure during scheduling
- Remove `max-replica` from `pd-recover`
- Add `Filter` metrics
- Fix the issue that Region information is not updated after tikv-ctl unsafe recovery
- Fix the issue that TiKV disk space is used up caused by replica migration in some scenarios
- Compatibility notes
    - Do not support rolling back to v2.0.x or earlier due to update of the new version storage engine
    - Enable `raft learner` by default in the new version of PD. If the cluster is upgraded from 1.x to 2.1, the machine should be stopped before upgrade or a rolling update should be first applied to TiKV and then PD 


## TiKV

- Upgrade Rust to the `nightly-2018-06-14` version
- Enable `Raft PreVote` to avoid leader reelection generated when network recovers after network isolation
- Add a metric to display the number of files and `ingest` related information in each layer of RocksDB
- Print `key` with too many versions when GC works
- Use `static metric` to optimize multi-label metric performance (YCSB `raw get` is improved by 3%)
- Remove `box` in multiple modules and use patterns to improve the operating performance (YCSB `raw get` is improved by 3%)
- Use `asynchronous log` to improve the performance of writing logs 
- Add a metric to collect the thread status
- Decease memory copy times by decreasing `box` used in the application to improve the performance
