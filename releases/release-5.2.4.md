---
title: TiDB 5.2.4 Release Notes
category: Releases
---

# TiDB 5.2.4 Release Notes

Release Date: April 26, 2022

TiDB version: 5.2.4

## Compatibility change(s)

+ TiDB

    - Change the default value of the system variable [`tidb_analyze_version`](/system-variables.md#tidb_analyze_version-new-in-v510) from `2` to `1` [#31748](https://github.com/pingcap/tidb/issues/31748)

+ TiKV

    - Add [`raft-log-compact-sync-interval`](https://docs.pingcap.com/tidb/v5.2/tikv-configuration-file#raft-log-compact-sync-interval-new-in-v524) to control the time interval (`"2s"` by default) to compact unnecessary Raft logs [#11404](https://github.com/tikv/tikv/issues/11404)
    - Change the default value of [`raft-log-gc-tick-interval`](/tikv-configuration-file.md#raft-log-gc-tick-interval) from `"10s"` to `"3s"` [#11404](https://github.com/tikv/tikv/issues/11404)
    - When [`storage.flow-control.enable`](/tikv-configuration-file.md#enable) is set to `true`, the value of [`storage.flow-control.hard-pending-compaction-bytes-limit`](/tikv-configuration-file.md#hard-pending-compaction-bytes-limit) overwrites that of [`rocksdb.(defaultcf|writecf|lockcf).hard-pending-compaction-bytes-limit`](/tikv-configuration-file.md#hard-pending-compaction-bytes-limit-1) [#11424](https://github.com/tikv/tikv/issues/11424)

+ Tools

    + TiDB Lightning

        - Change the default value of `regionMaxKeyCount` from 1_440_000 to 1_280_000, to avoid too many empty Regions after data import [#30018](https://github.com/pingcap/tidb/issues/30018)

## Improvements

+ TiKV

    - Transfer the leadership to CDC observer to reduce latency jitter [#12111](https://github.com/tikv/tikv/issues/12111)
    - Reduce the TiCDC recovery time by reducing the number of the Regions that require the Resolve Locks step [#11993](https://github.com/tikv/tikv/issues/11993)
    - Update the proc filesystem (procfs) to v0.12.0 [#11702](https://github.com/tikv/tikv/issues/11702)
    - Speed up the Garbage Collection (GC) process by increasing the write batch size when performing GC to Raft logs [#11404](https://github.com/tikv/tikv/issues/11404)
    - Increase the speed of inserting SST files by moving the verification process to the `Import` thread pool from the `Apply` thread pool [#11239](https://github.com/tikv/tikv/issues/11239)

+ Tools

    + TiCDC

        - Change the default value of Kafka Sink `partition-num` to 3 so that TiCDC distributes messages across Kafka partitions more evenly [#3337](https://github.com/pingcap/tiflow/issues/3337)
        - Reduce the time for the KV client to recover when a TiKV store is down [#3191](https://github.com/pingcap/tiflow/issues/3191)
        - Add a `Lag analyze` panel in Grafana [#4891](https://github.com/pingcap/tiflow/issues/4891)
        - Expose configuration parameters of the Kafka producer to make them configurable in TiCDC [#4385](https://github.com/pingcap/tiflow/issues/4385)
        - Add the exponential backoff mechanism for restarting a changefeed [#3329](https://github.com/pingcap/tiflow/issues/3329)
        - Reduce the count of "EventFeed retry rate limited" logs [#4006](https://github.com/pingcap/tiflow/issues/4006)
        - Set the default value of `max-message-bytes` to 10M [#4041](https://github.com/pingcap/tiflow/issues/4041)
        - Add more Prometheus and Grafana monitoring metrics and alerts, including `no owner alert`, `mounter row`, `table sink total row`, and `buffer sink total row` [#4054](https://github.com/pingcap/tiflow/issues/4054) [#1606](https://github.com/pingcap/tiflow/issues/1606)
        - Support multiple Kubernetes clusters in Grafana dashboards [#4665](https://github.com/pingcap/tiflow/issues/4665)
        - Add catch-up ETA (Estimated Time of Arrival) to the `changefeed checkpoint` monitoring metric [#5232](https://github.com/pingcap/tiflow/issues/5232)

## Bug fixes

+ TiDB

    - Fix wrong range calculation results for Nulleq function on Enum values [#32428](https://github.com/pingcap/tidb/issues/32428)
    - Fix the issue that INDEX HASH JOIN returns the `send on closed channel` error [#31129](https://github.com/pingcap/tidb/issues/31129)
    - Fix the issue that concurrent column type change causes inconsistency between the schema and the data [#31048](https://github.com/pingcap/tidb/issues/31048)
    - Fix the issue of potential data index inconsistency in optimistic transaction mode [#30410](https://github.com/pingcap/tidb/issues/30410)
    - Fix the issue that a SQL operation is canceled when its JSON type column joins its `CHAR` type column [#29401](https://github.com/pingcap/tidb/issues/29401)
    - Fix the issue that window functions might return different results when using a transaction or not [#29947](https://github.com/pingcap/tidb/issues/29947)
    - Fix the issue that the `Column 'col_name' in field list is ambiguous` error is reported unexpectedly when a SQL statement contains natural join [#25041](https://github.com/pingcap/tidb/issues/25041)
    - Fix the issue that the length information is wrong when casting `Decimal` to `String` [#29417](https://github.com/pingcap/tidb/issues/29417)
    - Fix the issue that the `GREATEST` function returns inconsistent results due to different values of `tidb_enable_vectorized_expression` (set to `on` or `off`) [#29434](https://github.com/pingcap/tidb/issues/29434)
    - Fix wrong results of deleting data of multiple tables using `left join` [#31321](https://github.com/pingcap/tidb/issues/31321)
    - Fix a bug that TiDB may dispatch duplicate tasks to TiFlash [#32814](https://github.com/pingcap/tidb/issues/32814)
    - Fix the MPP task list empty error when executing a query [#31636](https://github.com/pingcap/tidb/issues/31636)
    - Fix wrong results of index join caused by an innerWorker panic [#31494](https://github.com/pingcap/tidb/issues/31494)
    - Fix the issue that executing the `INSERT ... SELECT ... ON DUPLICATE KEY UPDATE` statement gets panic [#28078](https://github.com/pingcap/tidb/issues/28078)
    - Fix wrong query results due to the optimization of `Order By` [#30271](https://github.com/pingcap/tidb/issues/30271)
    - Fix the wrong result that might occur when performing `JOIN` on `ENUM` type columns [#27831](https://github.com/pingcap/tidb/issues/27831)
    - Fix the panic when using the `CASE WHEN` function on the `ENUM` data type [#29357](https://github.com/pingcap/tidb/issues/29357)
    - Fix wrong results of the `microsecond` function in vectorized expressions [#29244](https://github.com/pingcap/tidb/issues/29244)
    - Fix the issue that the window function causes TiDB to panic instead of reporting an error [#30326](https://github.com/pingcap/tidb/issues/30326)
    - Fix the issue that the Merge Join operator gets wrong results in certain cases [#33042](https://github.com/pingcap/tidb/issues/33042)
    - Fix the issue that TiDB gets a wrong result when a correlated subquery returns a constant  [#32089](https://github.com/pingcap/tidb/issues/32089)
    - Fix the issue that TiDB writes wrong data due to the wrong encoding of the `ENUM` or `SET` column [#32302](https://github.com/pingcap/tidb/issues/32302)
    - Fix the issue that the `MAX` or `MIN` function on the `ENUM` or `SET` column returns a wrong result when the new collation is enabled in TiDB [#31638](https://github.com/pingcap/tidb/issues/31638)
    - Fix the issue that the IndexHashJoin operator does not exit successfully [#31062](https://github.com/pingcap/tidb/issues/31062)
    - Fix the issue that TiDB might read wrong data when a table has a virtual column [#30965](https://github.com/pingcap/tidb/issues/30965)
    - Fix the issue that the setting of the log level does not take effect on the slow query log [#30309](https://github.com/pingcap/tidb/issues/30309)
    - Fix the issue that partitioned tables cannot fully use indexes to scan data in some cases [#33966](https://github.com/pingcap/tidb/issues/33966)
    - Fix the issue that the background HTTP service of TiDB might not exit successfully and makes the cluster in an abnormal state [#30571](https://github.com/pingcap/tidb/issues/30571)
    - Fix the issue that TiDB might unexpectedly output many logs of failed authentication [#29709](https://github.com/pingcap/tidb/issues/29709)
    - Fix the issue that the system variable `max_allowed_packet` does not take effect [#31422](https://github.com/pingcap/tidb/issues/31422)
    - Fix the issue that the `REPLACE` statement incorrectly changes other rows when the auto ID is out of range [#29483](https://github.com/pingcap/tidb/issues/29483)
    - Fix the issue that the slow query log cannot output log normally and might consume too much memory [#32656](https://github.com/pingcap/tidb/issues/32656)
    - Fix the issue that the result of NATURAL JOIN might include unexpected columns [#24981](https://github.com/pingcap/tidb/issues/29481)
    - Fix the issue that using `ORDER BY` and `LIMIT` together in one statement might output wrong results if a prefix-column index is used to query data [#29711](https://github.com/pingcap/tidb/issues/29711)
    - Fix the issue that the DOUBLE type auto-increment column might be changed when the optimistic transaction retries [#29892](https://github.com/pingcap/tidb/issues/29892)
    - Fix the issue that the STR_TO_DATE function cannot handle the preceding zero of the microsecond part correctly [#30078](https://github.com/pingcap/tidb/issues/30078)
    - Fix the issue that TiDB gets the wrong result when using TiFlash to scan tables with empty range although TiFlash does not support reading tables with empty range yet [#33083](https://github.com/pingcap/tidb/issues/33083)

+ TiKV

    - Fix a bug that stale messages cause TiKV to panic [#12023](https://github.com/tikv/tikv/issues/12023)
    - Fix the issue of intermittent packet loss and out of memory (OOM) caused by the overflow of memory metrics [#12160](https://github.com/tikv/tikv/issues/12160)
    - Fix the potential panic issue that occurs when TiKV performs profiling on Ubuntu 18.04 [#9765](https://github.com/tikv/tikv/issues/9765)
    - Fix the issue that tikv-ctl returns an incorrect result due to its wrong string match [#12329](https://github.com/tikv/tikv/issues/12329)
    - Fix a bug that replica reads might violate the linearizability [#12109](https://github.com/tikv/tikv/issues/12109)
    - Fix a bug that TiKV might panic if it has been running for 2 years or more [#11940](https://github.com/tikv/tikv/issues/11940)
    - Fix the issue of QPS drop when flow control is enabled and `level0_slowdown_trigger` is set explicitly [#11424](https://github.com/tikv/tikv/issues/11424)
    - Fix the panic issue that occurs when the cgroup controller is not mounted [#11569](https://github.com/tikv/tikv/issues/11569)
    - Fix possible metadata corruption caused by Region merge on a lagging Region peer [#11526](https://github.com/tikv/tikv/issues/11526)
    - Fix the issue that the latency of Resolved TS increases after TiKV stops operating [#11351](https://github.com/tikv/tikv/issues/11351)
    - Fix a panic issue that occurs when Region merge, ConfChange, and Snapshot happen at the same time in extreme conditions [#11475](https://github.com/tikv/tikv/issues/11475)
    - Fix a bug that tikv-ctl cannot return the correct Region-related information [#11393](https://github.com/tikv/tikv/issues/11393)
    - Fix the issue of negative sign when the decimal divide result is zero [#29586](https://github.com/pingcap/tidb/issues/29586)
    - Fix the issue that retrying prewrite requests in the pessimistic transaction mode might cause the risk of data inconsistency in rare cases [#11187](https://github.com/tikv/tikv/issues/11187)
    - Fix a memory leak caused by monitoring data of statistics threads [#11195](https://github.com/tikv/tikv/issues/11195)
    - Fix the issue that the average latency of the by-instance gRPC requests is inaccurate in TiKV metrics [#11299](https://github.com/tikv/tikv/issues/11299)
    - Fix the panic issue caused by deleting snapshot files when the peer status is `Applying` [#11746](https://github.com/tikv/tikv/issues/11746)
    - Fix a bug that TiKV cannot delete a range of data (which means the internal command `unsafe_destroy_range` is executed) when the GC worker is busy [#11903](https://github.com/tikv/tikv/issues/11903)
    - Fix the issue that deleting an uninitialized replica might cause an old replica to be recreated [#10533](https://github.com/tikv/tikv/issues/10533)
    - Fix the issue that TiKV cannot detect the memory lock when TiKV performs a reverse table scan [#11440](https://github.com/tikv/tikv/issues/11440)
    - Fix the deadlock issue that happens occasionally when coroutines run too fast [#11549](https://github.com/tikv/tikv/issues/11549)
    - Fix the issue that destroying a peer might cause high latency [#10210](https://github.com/tikv/tikv/issues/10210)
    - Fix the issue that TiKV panics and destroys peers unexpectedly because the target Region to be merged is invalid [#12232](https://github.com/tikv/tikv/issues/12232)
    - Fix the TiKV panic issue that occurs when the target peer is replaced with the peer that is destroyed without being initialized when merging a Region [#12048](https://github.com/tikv/tikv/issues/12048)
    - Fix the TiKV panic issue that occurs when applying snapshot is aborted [#11618](https://github.com/tikv/tikv/issues/11618)
    - Fix a bug that TiKV cannot correctly calculate the number of snapshots being sent when the operator execution fails [#11341](https://github.com/tikv/tikv/issues/11341)

+ PD

    - Fix the issue that the Region scatterer scheduling lost some peers [#4565](https://github.com/tikv/pd/issues/4565)
    - Fix the issue that the cold hotspot data cannot be deleted from the hotspot statistics [#4390](https://github.com/tikv/pd/issues/4390)

+ TiFlash

    - Fix a bug that MPP tasks might leak threads forever [#4238](https://github.com/pingcap/tiflash/issues/4238)
    - Fix the issue that the result of `IN` is incorrect in multi-value expressions [#4016](https://github.com/pingcap/tiflash/issues/4016)
    - Fix the issue that the date format identifies `'\n'` as an invalid separator [#4036](https://github.com/pingcap/tiflash/issues/4036)
    - Fix the potential query error after adding columns under heavy read workload [#3967](https://github.com/pingcap/tiflash/issues/3967)
    - Fix the bug that invalid storage directory configurations lead to unexpected behaviors [#4093](https://github.com/pingcap/tiflash/issues/4093)
    - Fix the bug that some exceptions are not handled properly [#4101](https://github.com/pingcap/tiflash/issues/4101)
    - Fix the bug that the `STR_TO_DATE()` function incorrectly handles leading zeros when parsing microseconds [#3557](https://github.com/pingcap/tiflash/issues/3557)
    - Fix the issue that casting `INT` to `DECIMAL` might cause overflow [#3920](https://github.com/pingcap/tiflash/issues/3920)
    - Fix the wrong result that occurs when casting `DATETIME` to `DECIMAL` [#4151](https://github.com/pingcap/tiflash/issues/4151)
    - Fix the overflow that occurs when casting `FLOAT` to `DECIMAL` [#3998](https://github.com/pingcap/tiflash/issues/3998)
    - Fix the issue that the `CastStringAsReal` behavior is inconsistent in TiFlash and in TiDB or TiKV [#3475](https://github.com/pingcap/tiflash/issues/3475)
    - Fix the issue that the `CastStringAsDecimal` behavior is inconsistent in TiFlash and in TiDB or TiKV [#3619](https://github.com/pingcap/tiflash/issues/3619)
    - Fix the issue that TiFlash might return the `EstablishMPPConnection` error after it is restarted [#3615](https://github.com/pingcap/tiflash/issues/3615)
    - Fix the issue that obsolete data cannot be reclaimed after setting the number of TiFlash replicas to 0 [#3659](https://github.com/pingcap/tiflash/issues/3659)
    - Fix potential data inconsistency when widening the primary key column with the primary key being `handle` [#3569](https://github.com/pingcap/tiflash/issues/3569)
    - Fix possible parsing errors when an SQL statement contains extremely long nested expressions [#3354](https://github.com/pingcap/tiflash/issues/3354)
    - Fix possible wrong results when a query contains the `where <string>` clause [#3447](https://github.com/pingcap/tiflash/issues/3447)
    - Fix possible wrong results when `new_collations_enabled_on_first_bootstrap` is enabled [#3388](https://github.com/pingcap/tiflash/issues/3388), [#3391](https://github.com/pingcap/tiflash/issues/3391)
    - Fix the panic issue that occurs when TLS is enabled [#4196](https://github.com/pingcap/tiflash/issues/4196)
    - Fix the panic issue that occurs when the memory limit is enabled [#3902](https://github.com/pingcap/tiflash/issues/3902)
    - Fix the issue that TiFlash crashes occasionally when an MPP query is stopped [#3401](https://github.com/pingcap/tiflash/issues/3401)
    - Fix the unexpected error of `Unexpected type of column: Nullable(Nothing)` [#3351](https://github.com/pingcap/tiflash/issues/3351)
    - Fix possible metadata corruption caused by Region merge on a lagging Region peer [#4437](https://github.com/pingcap/tiflash/issues/4437)
    - Fix the issue that a query containing `JOIN` might be hung if an error occurs [#4195](https://github.com/pingcap/tiflash/issues/4195)
    - Fix possible wrong results returned for MPP queries due to incorrect execution plans [#3389](https://github.com/pingcap/tiflash/issues/3389)

+ Tools

    + Backup & Restore (BR)

        - Fix the issue that BR fails to back up RawKV [#32607](https://github.com/pingcap/tidb/issues/32607)

    + TiCDC

        - Fix the issue that default values cannot be replicated [#3793](https://github.com/pingcap/tiflow/issues/3793)
        - Fix a bug that sequence is incorrectly replicated in some cases [#4563](https://github.com/pingcap/tiflow/issues/4552)
        - Fix a bug that a TiCDC node exits abnormally when a PD leader is killed [#4248](https://github.com/pingcap/tiflow/issues/4248)
        - Fix a bug that MySQL sink generates duplicated `replace` SQL statements when `batch-replace-enable` is disabled [#4501](https://github.com/pingcap/tiflow/issues/4501)
        - Fix the issue of panic and data inconsistency that occurs when outputting the default column value [#3929](https://github.com/pingcap/tiflow/issues/3929)
        - Fix the issue that `mq sink write row` does not have monitoring data [#3431](https://github.com/pingcap/tiflow/issues/3431)
        - Fix the issue that replication cannot be performed when `min.insync.replicas` is smaller than `replication-factor` [#3994](https://github.com/pingcap/tiflow/issues/3994)
        - Fix the potential panic issue that occurs when a replication task is removed [#3128](https://github.com/pingcap/tiflow/issues/3128)
        - Fix the bug that HTTP API panics when the required processor information does not exist [#3840](https://github.com/pingcap/tiflow/issues/3840)
        - Fix the issue of potential data loss caused by inaccurate checkpoint [#3545](https://github.com/pingcap/tiflow/issues/3545)
        - Fix the potential issue that the deadlock causes a replication task to get stuck [#4055](https://github.com/pingcap/tiflow/issues/4055)
        - Fix the TiCDC panic issue that occurs when manually cleaning the task status in etcd [#2980](https://github.com/pingcap/tiflow/issues/2980)
        - Fix the issue that special comments in DDL statements cause the replication task to stop [#3755](https://github.com/pingcap/tiflow/issues/3755)
        - Fix the issue of replication stop caused by the incorrect configuration of `config.Metadata.Timeout` [#3352](https://github.com/pingcap/tiflow/issues/3352)
        - Fix the issue that the service cannot be started because of a timezone issue in the RHEL release [#3584](https://github.com/pingcap/tiflow/issues/3584)
        - Fix the issue that `stopped` changefeeds resume automatically after a cluster upgrade [#3473](https://github.com/pingcap/tiflow/issues/3473)
        - Fix the issue of overly frequent warnings caused by MySQL sink deadlock [#2706](https://github.com/pingcap/tiflow/issues/2706)
        - Fix the bug that the `enable-old-value` configuration item is not automatically set to `true` on Canal and Maxwell protocols [#3676](https://github.com/pingcap/tiflow/issues/3676)
        - Fix the issue that Avro sink does not support parsing JSON type columns [#3624](https://github.com/pingcap/tiflow/issues/3624)
        - Fix the negative value error in the changefeed checkpoint lag [#3010](https://github.com/pingcap/tiflow/issues/3010)
        - Fix the OOM issue in the container environment [#1798](https://github.com/pingcap/tiflow/issues/1798)
        - Fix the memory leak issue after processing DDLs [#3174](https://github.com/pingcap/tiflow/issues/3174)
        - Fix the issue that changefeed gets stuck when tables are repeatedly scheduled in the same node [#4464](https://github.com/pingcap/tiflow/issues/4464)
        - Fix a bug that querying status through open API may be blocked when the PD node is abnormal [#4778](https://github.com/pingcap/tiflow/issues/4778)
        - Fix incorrect metrics caused by owner changes [#4774](https://github.com/pingcap/tiflow/issues/4774)
        - Fix a stability problem in workerpool used by Unified Sorter [#4447](https://github.com/pingcap/tiflow/issues/4447)
        - Fix the issue that the `cached region` monitoring metric is negative [#4300](https://github.com/pingcap/tiflow/issues/4300)

    + TiDB Lightning

        - Fix the issue of wrong import result that occurs when TiDB Lightning does not have the privilege to access the `mysql.tidb` table [#31088](https://github.com/pingcap/tidb/issues/31088)
        - Fix the checksum error "GC life time is shorter than transaction duration" [#32733](https://github.com/pingcap/tidb/issues/32733)
        - Fix a bug that TiDB Lightning may not delete the metadata schema when some import tasks do not contain source files [#28144](https://github.com/pingcap/tidb/issues/28144)
        - Fix the issue that TiDB Lightning does not report errors when the S3 storage path does not exist [#28031](https://github.com/pingcap/tidb/issues/28031) [#30709](https://github.com/pingcap/tidb/issues/30709)
        - Fix an error that occurs when iterating more than 1000 keys on GCS [#30377](https://github.com/pingcap/tidb/issues/30377)