---
title: TiDB 4.0.2 Release Notes
aliases: ['/docs/dev/releases/release-4.0.2/']
summary: TiDB 4.0.2 was released on July 1, 2020. The new version includes compatibility changes, new features, improvements, bug fixes, and new changes. Some highlights include support for new aggregate functions, improvements in query latency, and bug fixes related to execution plan, runtime errors, and data replication. Additionally, there are new features and improvements in TiKV, PD, TiFlash, and Tools.
---

# TiDB 4.0.2 Release Notes

Release date: July 1, 2020

TiDB version: 4.0.2

## Compatibility Changes

+ TiDB

    - Remove sensitive information in the slow query log and the statement summary table [#18130](https://github.com/pingcap/tidb/pull/18130)
    - Forbid negative value in the sequence cache [#18103](https://github.com/pingcap/tidb/pull/18103)
    - Remove tombstone TiKV and TiFlash stores from the `CLUSTER_INFO` table [#17953](https://github.com/pingcap/tidb/pull/17953)
    - Change the diagnostic rule from `current-load` to `node-check` [#17660](https://github.com/pingcap/tidb/pull/17660)

+ PD

    - Persist `store-limit` and remove `store-balance-rate` [#2557](https://github.com/pingcap/pd/pull/2557)

## New Change

- By default, TiDB and TiDB Dashboard share usage details with PingCAP to help understand how to improve the product [#18180](https://github.com/pingcap/tidb/pull/18180). For details about what is shared and how to disable the sharing, see [Telemetry](/telemetry.md).

## New Features

+ TiDB

    - Support the `MEMORY_QUOTA()` hint in `INSERT` statements [#18101](https://github.com/pingcap/tidb/pull/18101)
    - Support authentication based on the `SAN` field of TLS certificate [#17698](https://github.com/pingcap/tidb/pull/17698)
    - Support collation for the `REGEXP()` function [#17581](https://github.com/pingcap/tidb/pull/17581)
    - Support the `sql_select_limit` session and global variable [#17604](https://github.com/pingcap/tidb/pull/17604)
    - Support splitting the Region for the newly added partition by default [#17665](https://github.com/pingcap/tidb/pull/17665)
    - Support pushing the `IF()`/`BITXOR()`/`BITNEG()`/`JSON_LENGTH()` functions to the TiFlash Coprocessor [#17651](https://github.com/pingcap/tidb/pull/17651) [#17592](https://github.com/pingcap/tidb/pull/17592)
    - Support a new aggregate function `APPROX_COUNT_DISTINCT()` to calculate the approximate result of `COUNT(DISTINCT)` [#18120](https://github.com/pingcap/tidb/pull/18120)
    - Support collation in TiFlash and pushing collation-related functions to TiFlash [#17705](https://github.com/pingcap/tidb/pull/17705)
    - Add the `STATUS_ADDRESS` column in the `INFORMATION_SCHEMA.INSPECTION_RESULT` table to indicate the status address of servers [#17695](https://github.com/pingcap/tidb/pull/17695)
    - Add the `SOURCE` column in the `MYSQL.BIND_INFO` table to indicate the how the bindings are created [#17587](https://github.com/pingcap/tidb/pull/17587)
    - Add the `PLAN_IN_CACHE` and `PLAN_CACHE_HITS` columns in the `PERFORMANCE_SCHEMA.EVENTS_STATEMENTS_SUMMARY_BY_DIGEST` table to indicate the plan cache usage of SQL statements [#17493](https://github.com/pingcap/tidb/pull/17493)
    - Add the `enable-collect-execution-info` configuration item and the `tidb_enable_collect_execution_info` session variable to control whether to collect execution information of each operator and record the information in the slow query log [#18073](https://github.com/pingcap/tidb/pull/18073) [#18072](https://github.com/pingcap/tidb/pull/18072)
    - Add the `tidb_slow_log_masking` global variable to control whether to desensitize the queries in slow query log [#17694](https://github.com/pingcap/tidb/pull/17694)
    - Add a diagnostic rule in the `INFORMATION_SCHEMA.INSPECTION_RESULT` table for the `storage.block-cache.capacity` TiKV configuration item [#17671](https://github.com/pingcap/tidb/pull/17671)
    - Add the `BACKUP` and `RESTORE` SQL statements to back up and restore data [#15274](https://github.com/pingcap/tidb/pull/15274)

+ TiKV

    - Support the `encryption-meta` command in TiKV Control [#8103](https://github.com/tikv/tikv/pull/8103)
    - Add a perf context metric for `RocksDB::WriteImpl` [#7991](https://github.com/tikv/tikv/pull/7991)

+ PD

    - Support the operator to fail immediately when trying to remove a leader peer [#2551](https://github.com/pingcap/pd/pull/2551)
    - Set a suitable default store limit for TiFlash stores [#2559](https://github.com/pingcap/pd/pull/2559)

+ TiFlash

    - Support new aggregation function `APPROX_COUNT_DISTINCT` in Coprocessor
    - Enable the `rough set filter` feature by default
    - Enable TiFlash to run on the ARM architecture
    - Support pushing down the `JSON_LENGTH` function in Coprocessor

+ Tools

    - TiCDC

        - Support migrating sub-tasks to new `capture`s [#665](https://github.com/pingcap/tiflow/pull/665)
        - Add a `cli` command to delete the TiCDC GC TTL [#652](https://github.com/pingcap/tiflow/pull/652)
        - Support canal protocol in MQ sink [#649](https://github.com/pingcap/tiflow/pull/649)

## Improvements

+ TiDB

    - Reduce the query latency caused by the Golang memory allocation when CM-Sketch consumes too much memory [#17545](https://github.com/pingcap/tidb/pull/17545)
    - Reduce the QPS recovery duration of a cluster when a TiKV server is in the failure recovery process [#17681](https://github.com/pingcap/tidb/pull/17681)
    - Support pushing aggregate functions to TiKV/TiFlash Coprocessor on partition tables [#17655](https://github.com/pingcap/tidb/pull/17655)
    - Improve the accuracy of row count estimation for index equal conditions [#17611](https://github.com/pingcap/tidb/pull/17611)

+ TiKV

    - Improve the PD client panic log [#8093](https://github.com/tikv/tikv/pull/8093)
    - Add back the `process_cpu_seconds_total` and `process_start_time_seconds` monitoring metrics [#8029](https://github.com/tikv/tikv/pull/8029)

+ TiFlash

    - Improve backward compatibility when upgrading from an older version [#786](https://github.com/pingcap/tics/pull/786)
    - Reduce memory consumption of delta index [#787](https://github.com/pingcap/tics/pull/787)
    - Use the more efficient update algorithm for delta index [#794](https://github.com/pingcap/tics/pull/794)

+ Tools

    - Backup & Restore (BR)

        - Improve the performance by pipelining the restore process [#266](https://github.com/pingcap/br/pull/266)

## Bug Fixes

+ TiDB

    - Fix the issue of incorrect execution plan obtained from the plan cache after `tidb_isolation_read_engines` is changed [#17570](https://github.com/pingcap/tidb/pull/17570)
    - Fix the occasional runtime error that occurs when executing the `EXPLAIN FOR CONNECTION` statement [#18124](https://github.com/pingcap/tidb/pull/18124)
    - Fix the incorrect result of the `last_plan_from_cache` session variable in some cases [#18111](https://github.com/pingcap/tidb/pull/18111)
    - Fix the runtime error that occurs when executing the `UNIX_TIMESTAMP()` function from the plan cache [#18002](https://github.com/pingcap/tidb/pull/18002) [#17673](https://github.com/pingcap/tidb/pull/17673)
    - Fix the runtime error when the child of `HashJoin` executor returns the `NULL` column [#17937](https://github.com/pingcap/tidb/pull/17937)
    - Fix the runtime error caused by concurrently executing the `DROP DATABASE` statement and other DDL statements in the same database [#17659](https://github.com/pingcap/tidb/pull/17659)
    - Fix the incorrect result of the `COERCIBILITY()` function on user variables [#17890](https://github.com/pingcap/tidb/pull/17890)
    - Fix the issue that the `IndexMergeJoin` executor occasionally gets stuck [#18091](https://github.com/pingcap/tidb/pull/18091)
    - Fix the hang issue of the `IndexMergeJoin` executor when out of memory quota and query cancelling is triggered [#17654](https://github.com/pingcap/tidb/pull/17654)
    - Fix the excessive counting memory usage of the `Insert` and `Replace` executors [#18062](https://github.com/pingcap/tidb/pull/18062)
    - Fix the issue that the data replication to TiFlash storage is stopped when `DROP DATABASE` and `DROP TABLE` are executed concurrently in the same database [#17901](https://github.com/pingcap/tidb/pull/17901)
    - Fix the `BACKUP`/`RESTORE` failure between TiDB and the object storage service [#17844](https://github.com/pingcap/tidb/pull/17844)
    - Fix the incorrect error message of privilege check failure when access is denied [#17724](https://github.com/pingcap/tidb/pull/17724)
    - Discard the query feedbacks generated from the `DELETE`/`UPDATE` statement [#17843](https://github.com/pingcap/tidb/pull/17843)
    - Forbid altering `AUTO_RANDOM_BASE` for a table without `AUTO_RANDOM` property [#17828](https://github.com/pingcap/tidb/pull/17828)
    - Fix the issue that the `AUTO_RANDOM` column is allocated wrong results when the table is moved between databases by `ALTER TABLE ... RENAME` [#18243](https://github.com/pingcap/tidb/pull/18243)
    - Fix the issue that some system tables cannot be accessed when setting the value of `tidb_isolation_read_engines` without `tidb` [#17719](https://github.com/pingcap/tidb/pull/17719)
    - Fix the inaccurate result of JSON comparison on large integers and float values [#17717](https://github.com/pingcap/tidb/pull/17717)
    - Fix the incorrect decimal property for the result of the `COUNT()` function [#17704](https://github.com/pingcap/tidb/pull/17704)
    - Fix the incorrect result of the `HEX()` function when the type of input is the binary string [#17620](https://github.com/pingcap/tidb/pull/17620)
    - Fix the issue that an empty result is returned when querying the `INFORMATION_SCHEMA.INSPECTION_SUMMARY` table without filter condition [#17697](https://github.com/pingcap/tidb/pull/17697)
    - Fix the issue that the hashed password used by the `ALTER USER` statement to update user information is unexpected [#17646](https://github.com/pingcap/tidb/pull/17646)
    - Support collation for `ENUM` and `SET` values [#17701](https://github.com/pingcap/tidb/pull/17701)
    - Fix the issue that the timeout mechanism for pre-splitting Regions does not work when creating a table [#17619](https://github.com/pingcap/tidb/pull/17619)
    - Fix the issue that the schema is unexpectedly updated when a DDL job is retried, which might break the atomicity of DDL jobs [#17608](https://github.com/pingcap/tidb/pull/17608)
    - Fix the incorrect result of the `FIELD()` function when the argument contains the column [#17562](https://github.com/pingcap/tidb/pull/17562)
    - Fix the issue that the `max_execution_time` hint does not work occasionally [#17536](https://github.com/pingcap/tidb/pull/17536)
    - Fix the issue that the concurrency information is redundantly printed in the result of `EXPLAIN ANALYZE` [#17350](https://github.com/pingcap/tidb/pull/17350)
    - Fix the incompatible behavior of `%h` on the `STR_TO_DATE` function [#17498](https://github.com/pingcap/tidb/pull/17498)
    - Fix the issue that the follower/learner keeps retrying when `tidb_replica_read` is set to `follower` and there is a network partition between the leader and the follower/learner [#17443](https://github.com/pingcap/tidb/pull/17443)
    - Fix the issue that TiDB sends too many pings to PD follower in some cases [#17947](https://github.com/pingcap/tidb/pull/17947)
    - Fix the issue that the range partition table of older versions cannot be loaded in TiDB v4.0 [#17983](https://github.com/pingcap/tidb/pull/17983)
    - Fix the SQL statement timeout issue when multiple Region requests fail at the same time by assigning different `Backoffer` for each Region [#17585](https://github.com/pingcap/tidb/pull/17585)
    - Fix the MySQL incompatible behavior when parsing `DateTime` delimiters [#17501](https://github.com/pingcap/tidb/pull/17501)
    - Fix the issue that TiKV requests are occasionally sent to the TiFlash server [#18105](https://github.com/pingcap/tidb/pull/18105)
    - Fix the data inconsistency issue occurred because the lock of a written and deleted primary key in one transaction is resolved by another transaction [#18250](https://github.com/pingcap/tidb/pull/18250)

+ TiKV

    - Fix a memory safety issue for the status server [#8101](https://github.com/tikv/tikv/pull/8101)
    - Fix the issue of lost precision in JSON numeric comparison [#8087](https://github.com/tikv/tikv/pull/8087)
    - Fix the wrong query slow log [#8050](https://github.com/tikv/tikv/pull/8050)
    - Fix the issue that a peer cannot be removed when its store is isolated during multiple merge processes [#8048](https://github.com/tikv/tikv/pull/8048)
    - Fix the issue that `tikv-ctl recover-mvcc` does not remove invalid pessimistic locks [#8047](https://github.com/tikv/tikv/pull/8047)
    - Fix the issue that some Titan histogram metrics are missing [#7997](https://github.com/tikv/tikv/pull/7997)
    - Fix the issue that TiKV returns `duplicated error` to TiCDC [#7887](https://github.com/tikv/tikv/pull/7887)

+ PD

    - Check the correctness of the `pd-server.dashboard-address` configuration item [#2517](https://github.com/pingcap/pd/pull/2517)
    - Fix the panic issue of PD when setting `store-limit-mode` to `auto` [#2544](https://github.com/pingcap/pd/pull/2544)
    - Fix the issue that hotspots cannot be identified in some cases [#2463](https://github.com/pingcap/pd/pull/2463)
    - Fix the issue that placement rules prevent the store from changing to `tombstone` in some cases [#2546](https://github.com/pingcap/pd/pull/2546)
    - Fix the panic issue of PD when upgrading from earlier versions in some cases [#2564](https://github.com/pingcap/pd/pull/2564)

+ TiFlash

    - Fix the issue that the proxy might panic when the `region not found` error occurs
    - Fix the issue that the I/O exception thrown in `drop table` might lead to synchronization failure of TiFlash schema
