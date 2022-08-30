---
title: TiDB 5.1.4 Release Notes
---

# TiDB 5.1.4 Release Notes

Release Date: February 22, 2022

TiDB version: 5.1.4

## Compatibility changes

+ TiDB

    - Change the default value of the system variable [`tidb_analyze_version`](/system-variables.md#tidb_analyze_version-new-in-v510) from `2` to `1` [#31748](https://github.com/pingcap/tidb/issues/31748)
    - Since v5.1.4, if TiKV is configured with `storage.enable-ttl = true`, the requests from TiDB are rejected, because the TTL feature of TiKV only supports the [RawKV mode](https://tikv.org/docs/5.1/concepts/explore-tikv-features/ttl/) [#27303](https://github.com/pingcap/tidb/issues/27303)

+ Tools

    + TiCDC

        - Set the default value of `max-message-bytes` to 10M [#4041](https://github.com/pingcap/tiflow/issues/4041)

## Improvements

+ TiDB

    - Support partition pruning for the built-in `IN` expression in Range partition tables [#26739](https://github.com/pingcap/tidb/issues/26739)
    - Improve the accuracy of tracking memory usage when `IndexJoin` is executed [#28650](https://github.com/pingcap/tidb/issues/28650)

+ TiKV

    - Update the proc filesystem (procfs) to v0.12.0 [#11702](https://github.com/tikv/tikv/issues/11702)
    - Improve the error log report in the Raft client [#11959](https://github.com/tikv/tikv/issues/11959)
    - Increase the speed of inserting SST files by moving the verification process to the `Import` thread pool from the `Apply` thread pool [#11239](https://github.com/tikv/tikv/issues/11239)

+ PD

    - Speed up the exit process of schedulers [#4146](https://github.com/tikv/pd/issues/4146)

+ TiFlash

    - Support pushing down `ADDDATE()` and `DATE_ADD()` to TiFlash
    - Support pushing down `INET6_ATON()` and `INET6_NTOA()` to TiFlash
    - Support pushing down `INET_ATON()` and `INET_NTOA()` to TiFlash
    - Increase the max supported depth of an expression or a plan tree in a DAG request from `100` to `200`

+ Tools

    + TiCDC

        - Add the exponential backoff mechanism for restarting a changefeed. [#3329](https://github.com/pingcap/tiflow/issues/3329)
        - Reduce the replication latency when replicating many tables [#3900](https://github.com/pingcap/tiflow/issues/3900)
        - Add metrics for observing the remaining time of incremental scan [#2985](https://github.com/pingcap/tiflow/issues/2985)
        - Reduce the count of "EventFeed retry rate limited" logs [#4006](https://github.com/pingcap/tiflow/issues/4006)
        - Add more Prometheus and Grafana monitoring metrics and alerts, including `no owner alert`, `mounter row`, `table sink total row`, and `buffer sink total row` [#4054](https://github.com/pingcap/tiflow/issues/4054) [#1606](https://github.com/pingcap/tiflow/issues/1606)
        - Optimize rate limiting control on TiKV reloads to reduce gPRC congestion during changefeed initialization [#3110](https://github.com/pingcap/ticdc/issues/3110)
        - Reduce the time for the KV client to recover when a TiKV store is down [#3191](https://github.com/pingcap/tiflow/issues/3191)

## Bug fixes

+ TiDB

    - Fix a memory leak bug that occurs when the system variable `tidb_analyze_version` is set to `2` [#32499](https://github.com/pingcap/tidb/issues/32499)
    - Fix the issue that the `MaxDays` and `MaxBackups` configurations do not take effect for the slow log [#25716](https://github.com/pingcap/tidb/issues/25716)
    - Fix the issue that executing the `INSERT ... SELECT ... ON DUPLICATE KEY UPDATE` statement gets panic [#28078](https://github.com/pingcap/tidb/issues/28078)
    - Fix the wrong result that might occur when performing `JOIN` on `ENUM` type columns [#27831](https://github.com/pingcap/tidb/issues/27831)
    - Fix the issue that INDEX HASH JOIN returns the `send on closed channel` error [#31129](https://github.com/pingcap/tidb/issues/31129)
    - Fix the issue that using the [`BatchCommands`](/tidb-configuration-file.md#max-batch-size) API might block sending TiDB requests to TiKV in some rare cases [#32500](https://github.com/pingcap/tidb/issues/32500)
    - Fix the issue of potential data index inconsistency in optimistic transaction mode [#30410](https://github.com/pingcap/tidb/issues/30410)
    - Fix the issue that window functions might return different results when using a transaction or not [#29947](https://github.com/pingcap/tidb/issues/29947)
    - Fix the issue that the length information is wrong when casting `Decimal` to `String` [#29417](https://github.com/pingcap/tidb/issues/29417)
    - Fix the issue that the `GREATEST` function returns incorrect result that occurs when setting the `tidb_enable_vectorized_expression` vectorized expression to `off` [#29434](https://github.com/pingcap/tidb/issues/29434)
    - Fix the issue that the optimizer might cache invalid plans for `join` in some cases [#28087](https://github.com/pingcap/tidb/issues/28087)
    - Fix wrong results of the `microsecond` and `hour` functions in vectorized expressions [#29244](https://github.com/pingcap/tidb/issues/29244) [#28643](https://github.com/pingcap/tidb/issues/28643)
    - Fix the TiDB panic when executing the `ALTER TABLE.. ADD INDEX` statement in some cases [#27687](https://github.com/pingcap/tidb/issues/27687)
    - Fix a bug that the availability detection of MPP node does not work in some corner cases [#3118](https://github.com/pingcap/tics/issues/3118)
    - Fix the `DATA RACE` issue when assigning `MPP task ID` [#27952](https://github.com/pingcap/tidb/issues/27952)
    - Fix the `INDEX OUT OF RANGE` error for a MPP query after deleting an empty `dual table` [#28250](https://github.com/pingcap/tidb/issues/28250)
    - Fix the issue of false positive error log `invalid cop task execution summaries length` for MPP queries [#1791](https://github.com/pingcap/tics/issues/1791)
    - Fix the issue that SET GLOBAL tidb_skip_isolation_level_check=1 doesn't affect new session settings [#27897](https://github.com/pingcap/tidb/issues/27897)
    - Fix the `index out of range` issue that occurs when `tiup bench` runs for a long time [#26832](https://github.com/pingcap/tidb/issues/26832)

+ TiKV

    - Fix a bug that TiKV cannot delete a range of data (`unsafe_destroy_range` cannot be executed) when the GC worker is busy [#11903](https://github.com/tikv/tikv/issues/11903)
    - Fix the issue that destroying a peer might cause high latency [#10210](https://github.com/tikv/tikv/issues/10210)
    - Fix a bug that the `any_value` function returns a wrong result when regions are empty [#11735](https://github.com/tikv/tikv/issues/11735)
    - Fix the issue that deleting an uninitialized replica might cause an old replica to be recreated [#10533](https://github.com/tikv/tikv/issues/10533)
    - Fix the metadata corruption issue when `Prepare Merge` is triggered after a new election is finished but the isolated peer is not informed [#11526](https://github.com/tikv/tikv/issues/11526)
    - Fix the deadlock issue that happens occasionally when coroutines run too fast [#11549](https://github.com/tikv/tikv/issues/11549)
    - Fix the potential deadlock and memory leak issues when profiling flame graphs [#11108](https://github.com/tikv/tikv/issues/11108)
    - Fix the rare data inconsistency issue when retrying a prewrite request in pessimistic transactions [#11187](https://github.com/tikv/tikv/issues/11187)
    - Fix a bug that the configuration `resource-metering.enabled` does not work [#11235](https://github.com/tikv/tikv/issues/11235)
    - Fix the issue that some coroutines leak in `resolved_ts` [#10965](https://github.com/tikv/tikv/issues/10965)
    - Fix the issue of reporting false "GC can not work" alert under low write flow [#9910](https://github.com/tikv/tikv/issues/9910)
    - Fix a bug that tikv-ctl cannot return the correct Region-related information [#11393](https://github.com/tikv/tikv/issues/11393)
    - Fix the issue that a down TiKV node causes the resolved timestamp to lag [#11351](https://github.com/tikv/tikv/issues/11351)
    - Fix a panic issue that occurs when Region merge, ConfChange, and Snapshot happen at the same time in extreme conditions [#11475](https://github.com/tikv/tikv/issues/11475)
    - Fix the issue that TiKV cannot detect the memory lock when TiKV performs a reverse table scan [#11440](https://github.com/tikv/tikv/issues/11440)
    - Fix the issue of negative sign when the decimal divide result is zero [#29586](https://github.com/pingcap/tidb/issues/29586)
    - Fix a memory leak caused by the monitoring data of statistics threads [#11195](https://github.com/tikv/tikv/issues/11195)
    - Fix the issue of TiCDC panic that occurs when the downstream database is missing [#11123](https://github.com/tikv/tikv/issues/11123)
    - Fix the issue that TiCDC adds scan retries frequently due to the Congest error [#11082](https://github.com/tikv/tikv/issues/11082)
    - Fix the issue that batch messages are too large in Raft client implementation [#9714](https://github.com/tikv/tikv/issues/9714)
    - Collapse some uncommon storage-related metrics in Grafana dashboard [#11681](https://github.com/tikv/tikv/issues/11681)

+ PD

    - Fix a bug that the schedule generated by the region scatterer might decrease the number of peers [#4565](https://github.com/tikv/pd/issues/4565)
    - Fix the issue that Region statistics are not affected by `flow-round-by-digit` [#4295](https://github.com/tikv/pd/issues/4295)
    - Fix slow leader election caused by stucked region syncer [#3936](https://github.com/tikv/pd/issues/3936)
    - Support that the evict leader scheduler can schedule regions with unhealthy peers [#4093](https://github.com/tikv/pd/issues/4093)
    - Fix the issue that the cold hotspot data cannot be deleted from the hotspot statistics [#4390](https://github.com/tikv/pd/issues/4390)
    - Fix a panic issue that occurs after the TiKV node is removed [#4344](https://github.com/tikv/pd/issues/4344)
    - Fix the issue that the scheduling operator cannot fail fast because the target store is down [#3353](https://github.com/tikv/pd/issues/3353)

+ TiFlash

    - Fix the issue that the `str_to_date()` function incorrectly handles leading zeros when parsing microseconds
    - Fix the TiFlash crash problem when the memory limit is enabled
    - Fix the issue that when an input time is earlier than 1970-01-01 00:00:01 UTC, the behavior of `unix_timestamp` is inconsistent with that of TiDB or MySQL
    - Fix the potential data inconsistency caused by widening the primary key column when the primary key is handle
    - Fix the overflow bug and the issue of reporting `Can't compare` error when comparing data in the `DECIMAL` data type
    - Fix the unexpected error of `3rd arguments of function substringUTF8 must be constants.`
    - Fix the issue that TiFlash fails to start on platforms without the `nsl` library
    - Fix the overflow bug when casting data to the `DECIMAL` data type
    - Fix the issue that the `castStringAsReal` behavior is inconsistent in TiFlash and in TiDB/TiKV
    - Fix the issue that TiFlash might return the `EstablishMPPConnection` error after it is restarted
    - Fix the issue that obsolete data cannot be reclaimed after setting the number of TiFlash replicas to 0
    - Fix the issue that the `CastStringAsDecimal` behavior is inconsistent in TiFlash and in TiDB/TiKV
    - Fix the issue that queries with the `where <string>` clause return wrong results
    - Fix the issue that TiFlash might panic when an MPP query is stopped
    - Fix the unexpected error of `Unexpected type of column: Nullable(Nothing)`

+ Tools

    + TiCDC

        - Fix a bug that MySQL sink generates duplicated `replace` SQL statements if `batch-replace-enable` is disabled [#4501](https://github.com/pingcap/tiflow/issues/4501)
        - Fix the issue that the `cached region` monitoring metric is negative [#4300](https://github.com/pingcap/tiflow/issues/4300)
        - Fix the issue that replication cannot be performed when `min.insync.replicas` is smaller than `replication-factor` [#3994](https://github.com/pingcap/tiflow/issues/3994)
        - Fix the potential panic issue that occurs when a replication task is removed [#3128](https://github.com/pingcap/tiflow/issues/3128)
        - Fix the issue of potential data loss caused by inaccurate checkpoint [#3545](https://github.com/pingcap/tiflow/issues/3545)
        - Fix the potential issue that the deadlock causes a replication task to get stuck [#4055](https://github.com/pingcap/tiflow/issues/4055)
        - Fix the issue that special comments in DDL statements cause the replication task to stop [#3755](https://github.com/pingcap/tiflow/issues/3755)
        - Fix a bug that EtcdWorker might hang the owner and processor [#3750](https://github.com/pingcap/tiflow/issues/3750)
        - Fix the issue that `stopped` changefeeds resume automatically after a cluster upgrade [#3473](https://github.com/pingcap/tiflow/issues/3473)
        - Fix the issue that default values cannot be replicated [#3793](https://github.com/pingcap/tiflow/issues/3793)
        - Fix data inconsistency caused by TiCDC default value padding exceptions [#3918](https://github.com/pingcap/tiflow/issues/3918) [#3929](https://github.com/pingcap/tiflow/issues/3929)
        - Fix a bug that an owner gets stuck when a PD leader shuts down and transfers to a new node [#3615](https://github.com/pingcap/tiflow/issues/3615)
        - Fix the TiCDC panic issue that occurs when manually cleaning the task status in etcd [#2980](https://github.com/pingcap/tiflow/issues/2980)
        - Fix the issue that the service cannot be started because of a timezone issue in the RHEL release [#3584](https://github.com/pingcap/tiflow/issues/3584)
        - Fix the issue of overly frequent warnings caused by MySQL sink deadlock [#2706](https://github.com/pingcap/tiflow/issues/2706)
        - Fix the bug that the `enable-old-value` configuration item is not automatically set to `true` on Canal and Maxwell protocols [#3676](https://github.com/pingcap/tiflow/issues/3676)
        - Fix the issue that Avro sink does not support parsing JSON type columns [#3624](https://github.com/pingcap/tiflow/issues/3624)
        - Fix the negative value error in the changefeed checkpoint lag [#3010](https://github.com/pingcap/ticdc/issues/3010)
        - Fix the OOM issue in the container environment [#1798](https://github.com/pingcap/tiflow/issues/1798)
        - Fix the TiCDC replication interruption issue when multiple TiKVs crash or during a forced restart [#3288](https://github.com/pingcap/ticdc/issues/3288)
        - Fix the memory leak issue after processing DDLs [#3174](https://github.com/pingcap/ticdc/issues/3174)
        - Fix the issue that changefeed does not fail fast enough when the ErrGCTTLExceeded error occurs [#3111](https://github.com/pingcap/ticdc/issues/3111)
        - Fix the issue that TiCDC replication task might terminate when the upstream TiDB instance unexpectedly exits [#3061](https://github.com/pingcap/tiflow/issues/3061)
        - Fix the issue that TiCDC process might panic when TiKV sends duplicate requests to the same Region [#2386](https://github.com/pingcap/tiflow/issues/2386)
        - Fix the issue that Kafka may send excessively large messages by setting the default value of `max-message-bytes` to `10M` [#3081](https://github.com/pingcap/tiflow/issues/3081)
        - Fix the issue that TiCDC sync task might pause when an error occurs during writing a Kafka message [#2978](https://github.com/pingcap/tiflow/issues/2978)

    + Backup & Restore (BR)

        - Fix the potential issue that Regions might be unevenly distributed after a restore operation is finished [#30425](https://github.com/pingcap/tidb/issues/30425) [#31034](https://github.com/pingcap/tidb/issues/31034)

    + TiDB Binlog

        - Fix the issue that DBaaS importing CSV fails with InvalidRange if CSV file size is about 256MB and `strict-format` is `true` [#27763](https://github.com/pingcap/tidb/issues/27763)

    + TiDB Lightning

        - Fix the issue that TiDB Lightning does not report errors when the S3 storage path does not exist [#28031](https://github.com/pingcap/tidb/issues/28031) [#30709](https://github.com/pingcap/tidb/issues/30709)
