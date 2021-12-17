---
title: TiDB 4.0.16 Release Notes
---

# TiDB 4.0.16 Release Notes

Release date: December 17, 2021

TiDB version: 4.0.16

## Compatibility changes

+ TiKV

    - Before v4.0.16, when TiDB converts an illegal UTF-8 string to a Real type, an error is reported directly. Starting from v4.0.16, TiDB processes the conversion according to the legal UTF-8 prefix in the string [#11466](https://github.com/tikv/tikv/issues/11466)

+ Tools

    + TiCDC

        - Change the default value of Kafka Sink `max-message-bytes` to 1 MB to prevent TiCDC from sending too large messages to Kafka clusters [#2962](https://github.com/pingcap/ticdc/issues/2962)
        - Change the default value of Kafka Sink `partition-num` to 3 so that TiCDC distributes messages across Kafka partitions more evenly [#3337](https://github.com/pingcap/ticdc/issues/3337)

## Improvements

+ TiDB

    - Upgrade the Grafana version from 7.5.7 to 7.5.11

+ TiKV

    - Reduce disk space consumption by adopting the zstd algorithm to compress SST files when restoring data using Backup & Restore or importing data using Local-backend of TiDB Lightning [#11469](https://github.com/tikv/tikv/issues/11469)

+ Tools

    + Backup & Restore (BR)

        - Improve the robustness of restoring [#27421](https://github.com/pingcap/tidb/issues/27421)

    + TiCDC

        - Add a tick frequency limit to EtcdWorker to prevent frequent etcd writes from affecting PD services [#3112](https://github.com/pingcap/ticdc/issues/3112)
        - Optimize rate limiting control on TiKV reloads to reduce gPRC congestion during changefeed initialization [#3110](https://github.com/pingcap/ticdc/issues/3110)

## Bug fixes

+ TiDB

    - Fix the query panic caused by overflow in the statistics module when converting a range to points for cost estimation [#23625](https://github.com/pingcap/tidb/issues/23625)
    - Fix wrong results of the control functions (such as `IF` and `CASE WHEN`) when using the `ENUM` type data as parameters of such functions [#23114](https://github.com/pingcap/tidb/issues/23114)
    - Fix the issue that the `GREATEST` function returns inconsistent results due to different values of `tidb_enable_vectorized_expression` (`on` or `off`) [#29434](https://github.com/pingcap/tidb/issues/29434)
    - Fix the panic when applying index join on prefix indexes in some cases [#24547](https://github.com/pingcap/tidb/issues/24547)
    - Fix the issue that planner might cache invalid plans for `join` in some cases [#28087](https://github.com/pingcap/tidb/issues/28087)
    - Fix a bug that TiDB cannot insert `null` into a non-null column when `sql_mode` is empty [#11648](https://github.com/pingcap/tidb/issues/11648)
    - Fix the wrong result type of the `GREATEST` and `LEAST` functions [#29019](https://github.com/pingcap/tidb/issues/29019)
    - Fix the `privilege check fail` error when performing the `grant` and `revoke` operations to grant and revoke global level privileges [#29675](https://github.com/pingcap/tidb/issues/29675)
    - Fix the panic when using the `CASE WHEN` function on the `ENUM` data type [#29357](https://github.com/pingcap/tidb/issues/29357)
    - Fix wrong results of the `microsecond` function in vectorized expressions [#29244](https://github.com/pingcap/tidb/issues/29244)
    - Fix wrong results of the `hour` function in vectorized expression [#28643](https://github.com/pingcap/tidb/issues/28643)
    - Fix the issue that optimistic transaction conflicts might cause transactions to block each other [#11148](https://github.com/tikv/tikv/issues/11148)
    - Fix the issue of incomplete log information from the `auto analyze` result [#29188](https://github.com/pingcap/tidb/issues/29188)
    - Fix the issue that using an invalid default date does not report an error when the `SQL_MODE` is 'NO_ZERO_IN_DATE' [#26766](https://github.com/pingcap/tidb/issues/26766)
    - Fix the issue that the Coprocessor Cache panel in Grafana does not display metrics. Now, Grafana displays the number of `hits`/`miss`/`evict` [#26338](https://github.com/pingcap/tidb/issues/26338)
    - Fix the issue that concurrently truncating the same partition causes DDL statements to stuck [#26229](https://github.com/pingcap/tidb/issues/26229)
    - Fix the issue that the length information is wrong when converting `Decimal` to `String` [#29417](https://github.com/pingcap/tidb/issues/29417)
    - Fix the issue of an extra column in the query result when `NATURAL JOIN` is used to join multiple tables [#29481](https://github.com/pingcap/tidb/issues/29481)
    - Fix the issue that `TopN` is wrongly pushed down to `indexPlan` when `IndexScan` uses a prefix index [#29711](https://github.com/pingcap/tidb/issues/29711)
    - Fix the issue that retrying transactions with the auto-increment columns of `DOUBLE` type causes data corruption [#29892](https://github.com/pingcap/tidb/issues/29892)

+ TiKV

    - Fix a panic issue that occurs when Region merge, ConfChange, and Snapshot happen at the same time in extreme conditions [#11475](https://github.com/tikv/tikv/issues/11475)
    - Fix the issue of negative sign when the decimal divide result is zero [#29586](https://github.com/pingcap/tidb/issues/29586)
    - Fix the issue that the average latency of the by-instance gRPC requests is inaccurate in TiKV metrics [#11299](https://github.com/tikv/tikv/issues/11299)
    - Fix the issue of TiCDC panic that occurs when the downstream database is missing [#11123](https://github.com/tikv/tikv/issues/11123)
    - Fix the issue that the Raft connection is broken when the channel is full [#11047](https://github.com/tikv/tikv/issues/11047)
    - Fix the issue that TiDB cannot correctly identify whether the `Int64` types in `Max`/`Min` functions are a signed integer or not, which causes the wrong calculation result of `Max`/`Min` [#10158](https://github.com/tikv/tikv/issues/10158)
    - Fix the issue that CDC adds scan retries frequently due to the Congest error [#11082](https://github.com/tikv/tikv/issues/11082)

+ PD

    - Fix a panic issue that occurs after the TiKV node is removed [#4344](https://github.com/tikv/pd/issues/4344)
    - Fix slow leader election caused by stucked region syncer [#3936](https://github.com/tikv/pd/issues/3936)
    - Support that the evict leader scheduler can schedule regions with unhealthy peers [#4093](https://github.com/tikv/pd/issues/4093)

+ TiFlash

    - Fix the issue that TiFlash fails to start up on some platforms due to the absence of library `nsl`

+ Tools

    + TiDB Binlog

        - Fix the bug that Drainer exits when transporting a transaction greater than 1 GB [#28659](https://github.com/pingcap/tidb/issues/28659)

    + TiCDC

        - Fix the negative value error in the changefeed checkpoint lag [#3010](https://github.com/pingcap/ticdc/issues/3010)
        - Fix OOM in container environments [#1798](https://github.com/pingcap/ticdc/issues/1798)
        - Fix the TiCDC replication interruption issue when multiple TiKVs crash or during a forced restart [#3288](https://github.com/pingcap/ticdc/issues/3288)
        - Fix the memory leak issue after processing DDLs [#3174](https://github.com/pingcap/ticdc/issues/3174)
        - Fix the issue that changefeed does not fail fast enough when the ErrGCTTLExceeded error occurs [#3111](https://github.com/pingcap/ticdc/issues/3111)
        - Fix the issue that TiCDC replication task might terminate when the upstream TiDB instance unexpectedly exits [#3061](https://github.com/pingcap/ticdc/issues/3061)
        - Fix the issue that TiCDC process might panic when TiKV sends duplicate requests to the same Region [#2386](https://github.com/pingcap/ticdc/issues/2386)
        - Fix the issue that the volume of Kafka messages generated by TiCDC is not constrained by `max-message-size` [#2962](https://github.com/pingcap/ticdc/issues/2962)
        - Fix the issue that `tikv_cdc_min_resolved_ts_no_change_for_1m` keeps alerting when there is no changefeed [#11017](https://github.com/tikv/tikv/issues/11017)
        - Fix the issue that TiCDC sync task might pause when an error occurs during writing a Kafka message [#2978](https://github.com/pingcap/ticdc/issues/2978)
        - Fix the issue that some partitioned tables without valid indexes might be ignored when `force-replicate` is enabled [#2834](https://github.com/pingcap/ticdc/issues/2834)
        - Fix the memory leak issue when creating a new changefeed [#2389](https://github.com/pingcap/ticdc/issues/2389)
        - Fix the issue that might cause inconsistent data due to Sink components advancing resolved ts early [#3503](https://github.com/pingcap/ticdc/issues/3503)
        - Fix the issue that scanning stock data might fail due to TiKV performing GC when scanning stock data takes too long [#2470](https://github.com/pingcap/ticdc/issues/2470)
        - Fix the issue that the changefeed update command does not recognize global command line parameters [#2803](https://github.com/pingcap/ticdc/issues/2803)
