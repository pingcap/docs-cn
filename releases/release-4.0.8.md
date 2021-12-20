---
title: TiDB 4.0.8 Release Notes
---

# TiDB 4.0.8 Release Notes

Release date: October 30, 2020

TiDB version: 4.0.8

## New Features

+ TiDB

    - Support the new aggregate function `APPROX_PERCENTILE` [#20197](https://github.com/pingcap/tidb/pull/20197)

+ TiFlash

    - Support pushing down `CAST` functions

+ Tools

    + TiCDC

        - Support snapshot-level consistent replication [#932](https://github.com/pingcap/tiflow/pull/932)

## Improvements

+ TiDB

    - Prioritize low-selectivity indexes in the greedy search procedure of `Selectivity()` [#20154](https://github.com/pingcap/tidb/pull/20154)
    - Record more RPC runtime information in Coprocessor runtime statistics [#19264](https://github.com/pingcap/tidb/pull/19264)
    - Speed up parsing the slow log to improve query performance [#20556](https://github.com/pingcap/tidb/pull/20556)
    - Wait for timeout execution plans during the plan binding stage to record more debug information when the SQL optimizer is verifying potential new plans [#20530](https://github.com/pingcap/tidb/pull/20530)
    - Add the execution retry time in the slow log and the slow query result [#20495](https://github.com/pingcap/tidb/pull/20495) [#20494](https://github.com/pingcap/tidb/pull/20494)
    - Add the `table_storage_stats` system table [#20431](https://github.com/pingcap/tidb/pull/20431)
    - Add the RPC runtime statistical information for the `INSERT`/`UPDATE`/`REPLACE` statement [#20430](https://github.com/pingcap/tidb/pull/20430)
    - Add the operator information in the result of `EXPLAIN FOR CONNECTION` [#20384](https://github.com/pingcap/tidb/pull/20384)
    - Adjust the TiDB error log to the `DEBUG` level for the client connection/disconnection activities [#20321](https://github.com/pingcap/tidb/pull/20321)
    - Add monitoring metrics for Coprocessor Cache [#20293](https://github.com/pingcap/tidb/pull/20293)
    - Add the runtime information of pessimistic lock keys [#20199](https://github.com/pingcap/tidb/pull/20199)
    - Add two extra sections of time consumption information in the runtime information and `trace` span [#20187](https://github.com/pingcap/tidb/pull/20187)
    - Add the runtime information of transaction commit in the slow log [#20185](https://github.com/pingcap/tidb/pull/20185)
    - Disable the index merge join [#20599](https://github.com/pingcap/tidb/pull/20599)
    - Add the ISO 8601 and timezone supports for temporal string literals [#20670](https://github.com/pingcap/tidb/pull/20670)

+ TiKV

    - Add the **Fast-Tune** panel page to assist performance diagnostics [#8804](https://github.com/tikv/tikv/pull/8804)
    - Add the `security.redact-info-log` configuration item, which redacts user data from logs [#8746](https://github.com/tikv/tikv/pull/8746)
    - Reformat the metafile of error codes [#8877](https://github.com/tikv/tikv/pull/8877)
    - Enable dynamically changing the `pessimistic-txn.pipelined` configuration [#8853](https://github.com/tikv/tikv/pull/8853)
    - Enable the memory profiling features by default [#8801](https://github.com/tikv/tikv/pull/8801)

+ PD

    - Generate the metafile of errors [#3090](https://github.com/pingcap/pd/pull/3090)
    - Add the additional information for the operator [#3009](https://github.com/pingcap/pd/pull/3009)

+ TiFlash

    - Add monitoring metrics of Raft logs
    - Add monitoring metrics of memory usage for `cop` tasks
    - Make the `min`/`max` index more accurate when data is deleted
    - Improve query performance in the case of a small data volume
    - Add the `errors.toml` file to support the standard error code

+ Tools

    + Backup and Restore (BR)

        - Speed up the restore process by pipelining `split` and `ingest` [#427](https://github.com/pingcap/br/pull/427)
        - Support manually restoring PD schedulers [#530](https://github.com/pingcap/br/pull/530)
        - Use `pause` schedulers instead of `remove` schedulers [#551](https://github.com/pingcap/br/pull/551)

    + TiCDC

        - Print statistics in MySQL sink periodically [#1023](https://github.com/pingcap/tiflow/pull/1023)

    + Dumpling

        - Support dumpling data directly to S3 storages [#155](https://github.com/pingcap/dumpling/pull/155)
        - Support dumping views [#158](https://github.com/pingcap/dumpling/pull/158)
        - Support dumping the table that only contains generated columns [#166](https://github.com/pingcap/dumpling/pull/166)

    + TiDB Lightning

        - Support multi-byte CSV delimiters and separators [#406](https://github.com/pingcap/tidb-lightning/pull/406)
        - Speed up the restore process by disabling some PD schedulers [#408](https://github.com/pingcap/tidb-lightning/pull/408)
        - Use the GC-TTL API for checksum GC safepoint in the v4.0 cluster to avoid the GC error [#396](https://github.com/pingcap/tidb-lightning/pull/396)

## Bug Fixes

+ TiDB

    - Fix the unexpected panic that occurs when using partitioned tables [#20565](https://github.com/pingcap/tidb/pull/20565)
    - Fix the wrong result of outer join when filtering the outer side using index merge join [#20427](https://github.com/pingcap/tidb/pull/20427)
    - Fix the issue that the `NULL` value is returned when converting data to the `BIT` type if the data is too long [#20363](https://github.com/pingcap/tidb/pull/20363)
    - Fix the corrupted default value for the `BIT` type column [#20340](https://github.com/pingcap/tidb/pull/20340)
    - Fix the overflow error that might occur when converting the `BIT` type to the `INT64` type [#20312](https://github.com/pingcap/tidb/pull/20312)
    - Fix the possible wrong result of the propagate column optimization for the hybrid type column [#20297](https://github.com/pingcap/tidb/pull/20297)
    - Fix the panic that might occur when storing outdated plans from the plan cache [#20246](https://github.com/pingcap/tidb/pull/20246)
    - Fix the bug that the returned result is mistakenly truncated if `FROM_UNIXTIME` and `UNION ALL` are used together [#20240](https://github.com/pingcap/tidb/pull/20240)
    - Fix the issue that wrong results might be returned when the `Enum` type value is converted to the `Float` type [#20235](https://github.com/pingcap/tidb/pull/20235)
    - Fix the possible panic of `RegionStore.accessStore` [#20210](https://github.com/pingcap/tidb/pull/20210)
    - Fix the wrong result returned when sorting the maximum unsigned integer in `BatchPointGet` [#20205](https://github.com/pingcap/tidb/pull/20205)
    - Fix the bug that the coercibilities of `Enum` and `Set` are wrong [#20364](https://github.com/pingcap/tidb/pull/20364)
    - Fix an issue of ambiguous `YEAR` conversion [#20292](https://github.com/pingcap/tidb/pull/20292)
    - Fix the issue of wrong reported result that occurs when the **KV duration** panel contains `store0` [#20260](https://github.com/pingcap/tidb/pull/20260)
    - Fix the issue that the `Float` type data is mistakenly inserted regardless of the `out of range` error [#20252](https://github.com/pingcap/tidb/pull/20252)
    - Fix the bug that the generated column does not handle bad `NULL` values [#20216](https://github.com/pingcap/tidb/pull/20216)
    - Fix the inaccurate error information for the `YEAR` type data that is out of range [#20170](https://github.com/pingcap/tidb/pull/20170)
    - Fix the unexpected `invalid auto-id` error that might occur during the pessimistic transaction retry [#20134](https://github.com/pingcap/tidb/pull/20134)
    - Fix the issue that the constraint is not checked when using `ALTER TABLE` to change the `Enum`/`Set` type [#20046](https://github.com/pingcap/tidb/pull/20046)
    - Fix the wrong runtime information of `cop` tasks recorded when multiple operators are used for concurrency [#19947](https://github.com/pingcap/tidb/pull/19947)
    - Fix the issue that read-only system variables cannot be explicitly selected as the session variables [#19944](https://github.com/pingcap/tidb/pull/19944)
    - Fix the issue that the duplicate `ORDER BY` condition might cause sub-optimal execution plans [#20333](https://github.com/pingcap/tidb/pull/20333)
    - Fix the issue that the generated metric profile might fail if the font size exceeds the maximum allowable value [#20637](https://github.com/pingcap/tidb/pull/20637)

+ TiKV

    - Fix the bug that the mutex conflict in encryption causes pd-worker to process heartbeats slowly [#8869](https://github.com/tikv/tikv/pull/8869)
    - Fix the issue that the memory profile is mistakenly generated [#8790](https://github.com/tikv/tikv/pull/8790)
    - Fix the failure to back up databases on GCS when the storage class is specified [#8763](https://github.com/tikv/tikv/pull/8763)
    - Fix the bug that a learner cannot find a leader when the Region is restarted or newly split [#8864](https://github.com/tikv/tikv/pull/8864)

+ PD

    - Fix a bug that Key Visualizer of TiDB Dashboard might cause PD panic in some cases [#3096](https://github.com/pingcap/pd/pull/3096)
    - Fix the bug that PD might panic if a PD store is down for more than 10 minutes [#3069](https://github.com/pingcap/pd/pull/3069)

+ TiFlash

    - Fix the issue of wrong timestamp in the log message
    - Fix the issue that during the multi-disk TiFlash deployment, the wrong capacity causes the creation of TiFlash replicas to fail
    - Fix the bug that TiFlash might throw errors about broken data files after restart
    - Fix the issue that broken files might be left on disk after TiFlash crashes
    - Fix the bug that it might take a long time to wait for index during learner reads if the proxy cannot catch up with the latest Raft lease information
    - Fix the bug that the proxy writes too much Region state information to the key-value engine while replaying the outdated Raft log

+ Tools

    + Backup and Restore (BR)

        - Fix the `send on closed channel` panic during restore [#559](https://github.com/pingcap/br/pull/559)

    + TiCDC

        - Fix the unexpected exit caused by the failure to update the GC safepoint [#979](https://github.com/pingcap/tiflow/pull/979)
        - Fix the issue that the task status is unexpectedly flushed because of the incorrect mod revision cache [#1017](https://github.com/pingcap/tiflow/pull/1017)
        - Fix the unexpected empty Maxwell messages [#978](https://github.com/pingcap/tiflow/pull/978)

    + TiDB Lightning

        - Fix the issue of wrong column information [#420](https://github.com/pingcap/tidb-lightning/pull/420)
        - Fix the infinity loop that occurs when retrying to get Region information in the local mode [#418](https://github.com/pingcap/tidb-lightning/pull/418)
