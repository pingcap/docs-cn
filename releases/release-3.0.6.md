---
title: TiDB 3.0.6 Release Notes
aliases: ['/docs/dev/releases/release-3.0.6/','/docs/dev/releases/3.0.6/']
---

# TiDB 3.0.6 Release Notes

Release date: November 28, 2019

TiDB version: 3.0.6

TiDB Ansible version: 3.0.6

## TiDB

+ SQL Optimizer
    - Fix the issue that the result is incorrect after the window function AST restores SQL text, for example, `over w` being mistakenly restored to `over (w)` [#12933](https://github.com/pingcap/tidb/pull/12933)
    - Fix the issue of pushing down `STREAM AGG()` to `doubleRead` [#12690](https://github.com/pingcap/tidb/pull/12690)
    - Fix the issue that quotes are incorrectly handled for SQL binding [#13117](https://github.com/pingcap/tidb/pull/13117)
    - Optimize the `select max(_tidb_rowid) from t` scenario to avoid full table scans [#13095](https://github.com/pingcap/tidb/pull/13095)
    - Fix the issue that the query result is incorrect when the query statement contains a variable assignment expression [#13231](https://github.com/pingcap/tidb/pull/13231)
    - Fix the issue that the result is incorrect when the `UPDATE` statement contains both a sub-query and a generated column; fix the `UPDATE` statement execution error when this statement contains two same-named tables from different source databases [#13350](https://github.com/pingcap/tidb/pull/13350)
    - Support `_tidb_rowid` for point queries [#13416](https://github.com/pingcap/tidb/pull/13416)
    - Fix the issue that the generated query execution plan is incorrect, caused by incorrect usage of partitioned table statistics [#13628](https://github.com/pingcap/tidb/pull/13628)
+ SQL Execution Engine
    - Fix the issue that TiDB is incompatible with MySQL when handling invalid values of the year type [#12745](https://github.com/pingcap/tidb/pull/12745)
    - Reuse `Chunk` in the `INSERT ON DUPLICATE UPDATE` statement to reduce the memory overhead [#12998](https://github.com/pingcap/tidb/pull/12998)
    - Add the support for the `JSON_VALID` built-in function [#13133](https://github.com/pingcap/tidb/pull/13133)
    - Support executing `ADMIN CHECK TABLE` on partitioned tables [#13140](https://github.com/pingcap/tidb/pull/13140)
    - Fix the panic issue when `FAST ANALYZE` is executed on empty tables [#13343](https://github.com/pingcap/tidb/pull/13343)
    - Fix the panic issue when executing `FAST ANALYZE` on an empty table that contains multi-column indexes [#13394](https://github.com/pingcap/tidb/pull/13394)
    - Fix the issue that the estimated number of rows is greater than 1 when the `WHERE` clause contains an equal condition on the unique key [#13382](https://github.com/pingcap/tidb/pull/13382)
    - Fix the issue that the returned data might be duplicated when `Streaming` is enabled in TiDB [#13254](https://github.com/pingcap/tidb/pull/13254)
    - Extract the top N values from the count-min sketch to improve the estimation accuracy [#13429](https://github.com/pingcap/tidb/pull/13429)
+ Server
    - Make requests sent to TiKV fail quickly when the gRPC dial times out [#12926](https://github.com/pingcap/tidb/pull/12926)
    - Add the following virtual tables: [#13009](https://github.com/pingcap/tidb/pull/13009)
        - `performance_schema.tidb_profile_allocs`
        - `performance_schema.tidb_profile_block`
        - `performance_schema.tidb_profile_cpu`
        - `performance_schema.tidb_profile_goroutines`
    - Fix the issue that the `kill` command does not work when the query is waiting for pessimistic locking [#12989](https://github.com/pingcap/tidb/pull/12989)
    - Do not do asynchronous rollback when acquiring pessimistic locking fails and the transaction only involves modifying a single key [#12707](https://github.com/pingcap/tidb/pull/12707)
    - Fix the panic issue when the response for the request of splitting Regions is empty [#13092](https://github.com/pingcap/tidb/pull/13092)
    - Avoid unnecessary backoff when `PessimisticLock` returns a locking error [#13116](https://github.com/pingcap/tidb/pull/13116)
    - Modify the TiDB behavior for checking configurations by printing a warning log for unrecognized configuration option [#13272](https://github.com/pingcap/tidb/pull/13272)
    - Support obtaining the binlog status of all TiDB nodes via the `/info/all` interface [#13187](https://github.com/pingcap/tidb/pull/13187)
    - Fix the issue that goroutine might leak when TiDB kills connections [#13251](https://github.com/pingcap/tidb/pull/13251)
    - Make the `innodb_lock_wait_timeout` parameter work in pessimistic transactions to control the lock wait timeout for pessimistic locking [#13165](https://github.com/pingcap/tidb/pull/13165)
    - Stop updating pessimistic transaction TTL when pessimistic transactional queries are killed to prevent other transactions from waiting unnecessarily [#13046](https://github.com/pingcap/tidb/pull/13046)
+ DDL
    - Fix the issue that the execution result of `SHOW CREATE VIEW` in TiDB is inconsistent with that in MySQL [#12912](https://github.com/pingcap/tidb/pull/12912)
    - Support creating `View` based on `union`, for example, `create view v as select * from t1 union select * from t2` [#12955](https://github.com/pingcap/tidb/pull/12955)
    - Add more transaction-related fields for the `slow_query` table: [#13072](https://github.com/pingcap/tidb/pull/13072)
        - `Prewrite_time`
        - `Commit_time`
        - `Get_commit_ts_time`
        - `Commit_backoff_time`
        - `Backoff_types`
        - `Resolve_lock_time`
        - `Local_latch_wait_time`
        - `Write_key`
        - `Write_size`
        - `Prewrite_region`
        - `Txn_retry`
    - Use the table’s `COLLATE` instead of the system’s default charset in the column when a table is created and the table contains `COLLATE` [#13174](https://github.com/pingcap/tidb/pull/13174)
    - Limit the length of the index name when creating a table [#13310](https://github.com/pingcap/tidb/pull/13310)
    - Fix the issue that the table name length is not checked when a table is renamed [#13346](https://github.com/pingcap/tidb/pull/13346)
    - Add the `alter-primary-key` configuration (disabled by default) to support adding/dropping the primary key in TiDB [#13522](https://github.com/pingcap/tidb/pull/13522)

## TiKV

- Fix the issue that the `acquire_pessimistic_lock` interface returns a wrong `txn_size` [#5740](https://github.com/tikv/tikv/pull/5740)
- Limit the writes for GC worker per second to reduce the impact on the performance [#5735](https://github.com/tikv/tikv/pull/5735)
- Make `lock_manager` accurate [#5845](https://github.com/tikv/tikv/pull/5845)
- Support `innodb_lock_wait_timeout` for pessimistic locking [#5848](https://github.com/tikv/tikv/pull/5848)
- Add the configuration check for Titan [#5720](https://github.com/tikv/tikv/pull/5720)
- Support using tikv-ctl to dynamically modify the GC I/O limit: `tikv-ctl --host=ip:port modify-tikv-config -m server -n gc.max_write_bytes_per_sec -v 10MB` [#5957](https://github.com/tikv/tikv/pull/5957)
- Reduce useless `clean up` requests to decrease the pressure on the deadlock detector [#5965](https://github.com/tikv/tikv/pull/5965)
- Avoid reducing TTL in pessimistic locking prewrite requests [#6056](https://github.com/tikv/tikv/pull/6056)
- Fix the issue that a missing blob file might occur in Titan [#5968](https://github.com/tikv/tikv/pull/5968)
- Fix the issue that `RocksDBOptions` might not take effect in Titan [#6009](https://github.com/tikv/tikv/pull/6009)

## PD

- Add an `ActOn` dimension for each filter to indicate that each scheduler and checker is affected by the filter, and delete two unused filters: `disconnectFilter` and `rejectLeaderFilter` [#1911](https://github.com/pingcap/pd/pull/1911)
- Print a warning log when it takes more than 5 milliseconds to generate a timestamp in PD [#1867](https://github.com/pingcap/pd/pull/1867)
- Lower the client log level when passing unavailable endpoint to the client [#1856](https://github.com/pingcap/pd/pull/1856)
- Fix the issue that the gRPC message package might exceed the maximum size in the `region_syncer` replication process [#1952](https://github.com/pingcap/pd/pull/1952)

## Tools

+ TiDB Binlog
    - Obtain the initial replication timestamp from PD when `initial-commit-ts` is set to “-1” in Drainer [#788](https://github.com/pingcap/tidb-binlog/pull/788)
    - Decouple Drainer’s `Checkpoint` storage from the downstream and support saving `Checkpoint` in MySQL or local files [#790](https://github.com/pingcap/tidb-binlog/pull/790)
    - Fix the Drainer panic issue caused by using empty values when configuring replication database/table filtering [#801](https://github.com/pingcap/tidb-binlog/pull/801)
    - Fix the issue that processes get into the deadlock status instead of exiting after a panic occurs because Drainer fails to apply binlog files to the downstream [#807](https://github.com/pingcap/tidb-binlog/pull/807)
    - Fix the issue that Pump blocks when it exits because of gRPC’s `GracefulStop` [#817](https://github.com/pingcap/tidb-binlog/pull/817)
    - Fix the issue that Drainer fails when it receives a binlog which misses a column during the execution of a `DROP COLUMN` statement in TiDB (v3.0.6 or later) [#827](https://github.com/pingcap/tidb-binlog/pull/827)
+ TiDB Lightning
    - Add the `max-allowed-packet` configuration (64 M by default) for the TiDB backend [#248](https://github.com/pingcap/tidb-lightning/pull/248)
