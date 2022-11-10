---
title: TiDB 5.0.6 Release Notes
category: Releases
---

# TiDB 5.0.6 Release Notes

Release date: December 31, 2021

TiDB version: 5.0.6

## Compatibility changes

+ Tools

    + TiCDC

        - Change the output of the `cdc server` command error from stdout to stderr [#3133](https://github.com/pingcap/tiflow/issues/3133)
        - Set the default value of Kafka sink `max-message-bytes` to `10M` [#3081](https://github.com/pingcap/tiflow/issues/3081)
        - Change the default value of Kafka Sink `partition-num` to 3 so that TiCDC distributes messages across Kafka partitions more evenly [#3337](https://github.com/pingcap/ticdc/issues/3337)

## Improvements

+ TiDB

    - Show the affected SQL statements in the debug log when the coprocessor encounters a lock, which is helpful in diagnosing problems [#27718](https://github.com/pingcap/tidb/issues/27718)

+ TiKV

    - Increase the speed of inserting SST files by moving the verification process to the `Import` thread pool from the `Apply` thread pool [#11239](https://github.com/tikv/tikv/issues/11239)
    - Add more metrics for the garbage collection module of Raft logs to locate performance problems in the module [#11374](https://github.com/tikv/tikv/issues/11374)
    - Collapse some uncommon storage-related metrics in Grafana dashboard [#11681](https://github.com/tikv/tikv/issues/11681)

+ PD

    - Speed up the exit process of schedulers [#4146](https://github.com/tikv/pd/issues/4146)
    - Make the scheduling results of the `scatter-range-scheduler` scheduler more even by allowing the scheduler to schedule empty Regions and fix the configurations of the scheduler [#4497](https://github.com/tikv/pd/issues/4497)
    - Support that the evict leader scheduler can schedule Regions with unhealthy peers [#4093](https://github.com/tikv/pd/issues/4093)

+ Tools

    + TiCDC

        - Optimize rate limiting control on TiKV reloads to reduce gPRC congestion during changefeed initialization [#3110](https://github.com/pingcap/ticdc/issues/3110)
        - Add a tick frequency limit to EtcdWorker to prevent frequent etcd writes from affecting PD services [#3112](https://github.com/pingcap/ticdc/issues/3112)
        - Add the default configuration for `config.Metadata.Timeout` in Kafka sink [#3352](https://github.com/pingcap/tiflow/issues/3352)
        - Set the default value of `max-message-bytes` to `10M`, to reduce the probability that Kafka messages cannot be sent [#3081](https://github.com/pingcap/tiflow/issues/3081)
        - Add more Prometheus and Grafana monitoring metrics and alerts, including `no owner alert`, `mounter row`, `table sink total row`, and `buffer sink total row` [#4054](https://github.com/pingcap/tiflow/issues/4054) [#1606](https://github.com/pingcap/tiflow/issues/1606) 

    + Backup & Restore (BR)

        - Retry BR tasks when encountering the PD request error or the TiKV I/O timeout error [#27787](https://github.com/pingcap/tidb/issues/27787)
        - Improve the robustness of restoring [#27421](https://github.com/pingcap/tidb/issues/27421)

    + TiDB Lightning

        - Support importing data into tables that have expression index or the index that depends on virtual generated columns [#1404](https://github.com/pingcap/br/issues/1404)

## Bug fixes

+ TiDB

    - Fix the issue that optimistic transaction conflicts might cause transactions to block each other [#11148](https://github.com/tikv/tikv/issues/11148)
    - Fix the issue of false positive error log `invalid cop task execution summaries length` for MPP queries [#1791](https://github.com/pingcap/tics/issues/1791)
    - Fix the panic that might occur when DML and DDL statements are executed concurrently [#30940](https://github.com/pingcap/tidb/issues/30940)
    - Fix the `privilege check fail` error when performing the `grant` and `revoke` operations to grant and revoke global level privileges [#29675](https://github.com/pingcap/tidb/issues/29675)
    - Fix the TiDB panic when executing the `ALTER TABLE.. ADD INDEX` statement in some cases [#27687](https://github.com/pingcap/tidb/issues/27687)
    - Fix the issue that the `enforce-mpp` configuration does not take effect in v5.0.4 [#29252](https://github.com/pingcap/tidb/issues/29252)
    - Fix the panic when using the `CASE WHEN` function on the `ENUM` data type [#29357](https://github.com/pingcap/tidb/issues/29357)
    - Fix wrong results of the `microsecond` function in vectorized expressions [#29244](https://github.com/pingcap/tidb/issues/29244)
    - Fix the issue of incomplete log information from the `auto analyze` result [#29188](https://github.com/pingcap/tidb/issues/29188)
    - Fix wrong results of the `hour` function in vectorized expression [#28643](https://github.com/pingcap/tidb/issues/28643)
    - Fix the unexpected error like `tidb_cast to Int32 is not supported` when the unsupported `cast` is pushed down to TiFlash [#23907](https://github.com/pingcap/tidb/issues/23907)
    - Fix a bug that the availability detection of MPP node does not work in some corner cases [#3118](https://github.com/pingcap/tics/issues/3118)
    - Fix the `DATA RACE` issue when assigning `MPP task ID` [#27952](https://github.com/pingcap/tidb/issues/27952)
    - Fix the `INDEX OUT OF RANGE` error for a MPP query after deleting an empty `dual table` [#28250](https://github.com/pingcap/tidb/issues/28250)
    - Fix the TiDB panic when inserting invalid date values concurrently [#25393](https://github.com/pingcap/tidb/issues/25393)
    - Fix the unexpected `can not found column in Schema column` error for queries in the MPP mode [#30980](https://github.com/pingcap/tidb/issues/30980)
    - Fix the issue that TiDB might panic when TiFlash is shuting down [#28096](https://github.com/pingcap/tidb/issues/28096)
    - Fix the unexpected `index out of range` error when the planner is doing join reorder [#24095](https://github.com/pingcap/tidb/issues/24095)
    - Fix wrong results of the control functions (such as `IF` and `CASE WHEN`) when using the `ENUM` type data as parameters of such functions [#23114](https://github.com/pingcap/tidb/issues/23114)
    - Fix the wrong result of `CONCAT(IFNULL(TIME(3))` [#29498](https://github.com/pingcap/tidb/issues/29498)
    - Fix wrong results of `GREATEST` and `LEAST` when passing in unsigned `BIGINT` arguments [#30101](https://github.com/pingcap/tidb/issues/30101)
    - Fix the issue that a SQL operation is canceled when its JSON type column joins its `CHAR` type column [#29401](https://github.com/pingcap/tidb/issues/29401)
    - Fix the data inconsistency issue caused by incorrect usage of lazy existence check and untouched key optimization [#30410](https://github.com/pingcap/tidb/issues/30410)
    - Fix the issue that window functions might return different results when using a transaction or not [#29947](https://github.com/pingcap/tidb/issues/29947)
    - Fix the issue that the SQL statements that contain `cast(integer as char) union string` return wrong results [#29513](https://github.com/pingcap/tidb/issues/29513)
    - Fix the issue that the length information is wrong when casting `Decimal` to `String` [#29417](https://github.com/pingcap/tidb/issues/29417)
    - Fix the issue that the `Column 'col_name' in field list is ambiguous` error is reported unexpectedly when a SQL statement contains natural join [#25041](https://github.com/pingcap/tidb/issues/25041)
    - Fix the issue that the `GREATEST` function returns inconsistent results due to different values of `tidb_enable_vectorized_expression` (set to `on` or `off`) [#29434](https://github.com/pingcap/tidb/issues/29434)
    - Fix the issue that the planner might cache invalid plans for `join` in some cases [#28087](https://github.com/pingcap/tidb/issues/28087)
    - Fix the issue that the `index out of range [1] with length 1` error is reported when a SQL statement evaluates an aggregation result on the result of join in some cases [#1978](https://github.com/pingcap/tics/issues/1978)

+ TiKV

    - Fix the issue that a down TiKV node causes the resolved timestamp to lag [#11351](https://github.com/tikv/tikv/issues/11351)
    - Fix the issue that batch messages are too large in Raft client implementation [#9714](https://github.com/tikv/tikv/issues/9714)
    - Fix a panic issue that occurs when Region merge, ConfChange, and Snapshot happen at the same time in extreme conditions [#11475](https://github.com/tikv/tikv/issues/11475)
    - Fix the issue that TiKV cannot detect the memory lock when TiKV perform a reverse table scan [#11440](https://github.com/tikv/tikv/issues/11440)
    - Fix the issue of negative sign when the decimal divide result is zero [#29586](https://github.com/pingcap/tidb/issues/29586)
    - Fix the issue that the accumulation of GC tasks might cause TiKV to be OOM (out of memory) [#11410](https://github.com/tikv/tikv/issues/11410)
    - Fix the issue that the average latency of the by-instance gRPC requests is inaccurate in TiKV metrics [#11299](https://github.com/tikv/tikv/issues/11299)
    - Fix a memory leak caused by monitoring data of statistics threads [#11195](https://github.com/tikv/tikv/issues/11195)
    - Fix the issue of TiCDC panic that occurs when the downstream database is missing [#11123](https://github.com/tikv/tikv/issues/11123)
    - Fix the issue that TiCDC adds scan retries frequently due to the Congest error [#11082](https://github.com/tikv/tikv/issues/11082)
    - Fix the issue that the Raft connection is broken when the channel is full [#11047](https://github.com/tikv/tikv/issues/11047)
    - Fix the issue of TiKV panic that occurs when the files do not exist when TiDB Lightning imports data [#10438](https://github.com/tikv/tikv/issues/10438)
    - Fix the issue that TiDB cannot correctly identify whether the `Int64` types in `Max`/`Min` functions are a signed integer or not, which causes the wrong calculation result of `Max`/`Min` [#10158](https://github.com/tikv/tikv/issues/10158)
    - Fix the issue that the node of a TiKV replica is down after the node gets snapshots because TiKV cannot modify the metadata accurately [#10225](https://github.com/tikv/tikv/issues/10225)
    - Fix the leak issue of the backup thread pool [#10287](https://github.com/tikv/tikv/issues/10287)
    - Fix the issue of casting illegal strings into floating-point numbers [#23322](https://github.com/pingcap/tidb/issues/23322)

+ PD

    - Fix a panic issue that occurs after the TiKV node is removed [#4344](https://github.com/tikv/pd/issues/4344)
    - Fix the issue that operator can get blocked due to down store [#3353](https://github.com/tikv/pd/issues/3353)
    - Fix slow leader election caused by stucked Region syncer [#3936](https://github.com/tikv/pd/issues/3936)
    - Fix the issue that the speed of removing peers is limited when repairing the down nodes [#4090](https://github.com/tikv/pd/issues/4090)
    - Fix the issue that the hotspot cache cannot be cleared when the Region heartbeat is less than 60 seconds [#4390](https://github.com/tikv/pd/issues/4390)

+ TiFlash

    - Fix potential data inconsistency after altering a primary key column to a larger int data type
    - Fix the issue that TiFlash fails to start up on some platforms, such as ARM, due to the absence of the `libnsl.so` library
    - Fix the issue that the `Store size` metric does not match the actual data size on a disk
    - Fix the issue that TiFlash crashes due to a `Cannot open file` error
    - Fix occasional crashes of TiFlash when an MPP query is killed
    - Fix the unexpected error `3rd arguments of function substringUTF8 must be constants`
    - Fix query failures caused by excessive `OR` conditions
    - Fix the bug that results of `where <string>` are wrong
    - Fix inconsistent behaviors of `CastStringAsDecimal` between TiFlash and TiDB/TiKV
    - Fix query failures caused by the error `different types: expected Nullable(Int64), got Int64`
    - Fix query failures caused by the error `Unexpected type of column: Nullable(Nothing)`
    - Fix query failures caused by overflow when comparing data in the `DECIMAL` data type

+ Tools

    + TiCDC

        - Fix the issue that some partitioned tables without valid indexes might be ignored when `force-replicate` is enabled [#2834](https://github.com/pingcap/tiflow/issues/2834)
        - Fix the issue that `cdc cli` silently truncates user parameters when receiving unexpected parameters, causing the user input parameters to be lost [#2303](https://github.com/pingcap/tiflow/issues/2303)
        - Fix the issue that TiCDC sync task might pause when an error occurs during writing a Kafka message [#2978](https://github.com/pingcap/tiflow/issues/2978)
        - Fix a possible panic issue when encoding some types of columns into Open Protocol format [#2758](https://github.com/pingcap/tiflow/issues/2758)
        - Fix the issue that Kafka may send excessively large messages by setting the default value of `max-message-bytes` to `10M` [#3081](https://github.com/pingcap/tiflow/issues/3081)
        - Fix the issue that TiCDC replication task might terminate when the upstream TiDB instance unexpectedly exits [#3061](https://github.com/pingcap/tiflow/issues/3061)
        - Fix the issue that TiCDC process might panic when TiKV sends duplicate requests to the same Region [#2386](https://github.com/pingcap/tiflow/issues/2386)
        - Fix the TiCDC replication interruption issue when multiple TiKVs crash or during a forced restart [#3288](https://github.com/pingcap/ticdc/issues/3288)
        - Fix the negative value error in the changefeed checkpoint lag [#3010](https://github.com/pingcap/ticdc/issues/3010)
        - Fix the issue of overly frequent warnings caused by MySQL sink deadlock [#2706](https://github.com/pingcap/tiflow/issues/2706)
        - Fix the issue that Avro sink does not support parsing JSON type columns [#3624](https://github.com/pingcap/tiflow/issues/3624)
        - Fix the bug that TiCDC reads the incorrect schema snapshot from TiKV when the TiKV owner restarts [#2603](https://github.com/pingcap/tiflow/issues/2603)
        - Fix the memory leak issue after processing DDLs [#3174](https://github.com/pingcap/ticdc/issues/3174)
        - Fix the bug that the `enable-old-value` configuration item is not automatically set to `true` on Canal and Maxwell protocols [#3676](https://github.com/pingcap/tiflow/issues/3676)
        - Fix the timezone error that occurs when the `cdc server` command runs on some Red Hat Enterprise Linux releases (such as 6.8 and 6.9) [#3584](https://github.com/pingcap/tiflow/issues/3584)
        - Fix the issue of the inaccurate `txn_batch_size` monitoring metric for Kafka sink [#3431](https://github.com/pingcap/tiflow/issues/3431)
        - Fix the issue that `tikv_cdc_min_resolved_ts_no_change_for_1m` keeps alerting when there is no changefeed [#11017](https://github.com/tikv/tikv/issues/11017)
        - Fix the TiCDC panic issue that occurs when manually cleaning the task status in etcd [#2980](https://github.com/pingcap/tiflow/issues/2980)
        - Fix the issue that changefeed does not fail fast enough when the ErrGCTTLExceeded error occurs [#3111](https://github.com/pingcap/ticdc/issues/3111)
        - Fix the issue that scanning stock data might fail due to TiKV performing GC when scanning stock data takes too long [#2470](https://github.com/pingcap/tiflow/issues/2470)
        - Fix OOM in container environments [#1798](https://github.com/pingcap/ticdc/issues/1798)

    + Backup & Restore (BR)

        - Fix a bug that the average speed is inaccurately calculated for backup and restore [#1405](https://github.com/pingcap/br/issues/1405)

    + Dumpling

        - Fix the bug that Dumpling becomes very slow when dumping tables with the composite primary key or unique key [#29386](https://github.com/pingcap/tidb/issues/29386)