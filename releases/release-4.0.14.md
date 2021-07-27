---
title: TiDB 4.0.14 Release Notes
---

# TiDB 4.0.14 Release Notes

Release date: July 27, 2021

TiDB version: 4.0.14

## Compatibility changes

+ TiDB

    - Change the default value of `tidb_multi_statement_mode` from `WARN` to `OFF` in v4.0. It is recommended to use the multi-statement feature of your client library instead. See [the documentation on `tidb_multi_statement_mode`](/system-variables.md#tidb_multi_statement_mode-new-in-v4011) for details. [#25749](https://github.com/pingcap/tidb/pull/25749)
    - Upgrade Grafana dashboard from v6.1.16 to v7.5.7 to solve two security vulnerabilities. See the [Grafana blog post](https://grafana.com/blog/2020/06/03/grafana-6.7.4-and-7.0.2-released-with-important-security-fix/) for details.
    - Change the default value of the `tidb_stmt_summary_max_stmt_count` variable from `200` to `3000` [#25872](https://github.com/pingcap/tidb/pull/25872)

+ TiKV

    - Change the default value of `merge-check-tick-interval` from `10` to `2` to speed up the Region merge process [#9676](https://github.com/tikv/tikv/pull/9676)

## Feature enhancements

+ TiKV

    - Add a metric `pending` to monitor the number of pending PD heartbeats, which helps locate the issue of slow PD threads [#10008](https://github.com/tikv/tikv/pull/10008)
    - Support using the virtual-host addressing mode to make BR support the S3-compatible storage [#10242](https://github.com/tikv/tikv/pull/10242)

+ TiDB Dashboard

    - Support OIDC SSO. By setting the OIDC-compatible SSO services (such as Okta and Auth0), users can log into TiDB Dashboard without entering the SQL password. [#960](https://github.com/pingcap/tidb-dashboard/pull/960)
    - Add the **Debug API** UI, which is an alternative method to the command line to call several common TiDB and PD internal APIs for advanced debugging [#927](https://github.com/pingcap/tidb-dashboard/pull/927)

## Improvements

+ TiDB

    - Change the `LOCK` record into the `PUT` record for the index keys using `point get` or `batch point get` for `UPDATE` reads [#26223](https://github.com/pingcap/tidb/pull/26223)
    - Support the MySQL system variable `init_connect` and its associated features [#26031](https://github.com/pingcap/tidb/pull/26031)
    - Support the stable result mode to make the query results more stable [#26003](https://github.com/pingcap/tidb/pull/26003)
    - Support pushing down the built-in function `json_unquote()` to TiKV [#25721](https://github.com/pingcap/tidb/pull/25721)
    - Make the SQL Plan Management (SPM) not affected by the character set [#23295](https://github.com/pingcap/tidb/pull/23295)

+ TiKV

    - Shutdown the status server first to make sure that the client can correctly check the shutdown status [#10504](https://github.com/tikv/tikv/pull/10504)
    - Always respond to stale peers to make sure that these peers are cleared quicker [#10400](https://github.com/tikv/tikv/pull/10400)
    - Limit the TiCDC sink's memory consumption [#10147](https://github.com/tikv/tikv/pull/10147)
    - When a Region is too large, use the even split to speed up the split process [#10275](https://github.com/tikv/tikv/pull/10275)

+ PD

    - Reduce the conflicts among multiple schedulers that run at the same time [#3858](https://github.com/pingcap/pd/pull/3858) [#3854](https://github.com/tikv/pd/pull/3854)

+ TiDB Dashboard

    - Update TiDB Dashboard to v2021.07.17.1 [#3882](https://github.com/pingcap/pd/pull/3882)
    - Support sharing the current session as a read-only session to avoid further modification to it [#960](https://github.com/pingcap/tidb-dashboard/pull/960)

+ Tools

    + Backup & Restore (BR)

        - Speed up restore by merging small backup files [#655](https://github.com/pingcap/br/pull/655)

    + Dumpling

        - Always split tables using `_tidb_rowid` when the upstream is a TiDB v3.x cluster, which helps reduce TiDB's memory usage [#306](https://github.com/pingcap/dumpling/pull/306)

    + TiCDC

        - Improve the error message returned when a PD endpoint misses the certificate [#2184](https://github.com/pingcap/ticdc/pull/2184)
        - Make the sorter I/O errors more user-friendly [#1976](https://github.com/pingcap/ticdc/pull/1976)
        - Add a concurrency limit on the Region incremental scan in the KV client to reduce the pressure of TiKV [#1926](https://github.com/pingcap/ticdc/pull/1926)
        - Add metrics for the table memory consumption [#1884](https://github.com/pingcap/ticdc/pull/1884)
        - Add `capture-session-ttl` to the TiCDC server configuration [#2169](https://github.com/pingcap/ticdc/pull/2169)

## Bug fixes

+ TiDB

    - Fix the issue that the `SELECT` result is incompatible with MySQL when joining a subquery with a `WHERE` clause evaluated to `false` [#24865](https://github.com/pingcap/tidb/issues/24865)
    - Fix the calculation error of the `ifnull` function that occurs when the argument is the `ENUM` or `SET` type [#24944](https://github.com/pingcap/tidb/issues/24944)
    - Fix the wrong aggregate pruning in some cases [#25202](https://github.com/pingcap/tidb/issues/25202)
    - Fix the incorrect result of the merge join operation that might occur when the column is the `SET` type [#25669](https://github.com/pingcap/tidb/issues/25669)
    - Fix the issue that TiDB returns wrong results for cartesian join [#25591](https://github.com/pingcap/tidb/issues/25591)
    - Fix the panic issue that occurs when `SELECT ... FOR UPDATE` works on a join operation and the join uses a partitioned table [#20028](https://github.com/pingcap/tidb/issues/20028)
    - Fix the issue that the cached `prepared` plan is incorrectly used for `point get` [#24741](https://github.com/pingcap/tidb/issues/24741)
    - Fix the issue that the `LOAD DATA` statement can abnormally import non-utf8 data [#25979](https://github.com/pingcap/tidb/issues/25979)
    - Fix a potential memory leak issue that occurs when accessing the statistics via an HTTP API [#24650](https://github.com/pingcap/tidb/pull/24650)
    - Fix a security issue that occurs when executing the `ALTER USER` statement [#25225](https://github.com/pingcap/tidb/issues/25225)
    - Fix a bug that the `TIKV_REGION_PEERS` table cannot correctly handle the `DOWN` status [#24879](https://github.com/pingcap/tidb/issues/24879)
    - Fix the issue that invalid strings are not truncated when parsing `DateTime` [#22231](https://github.com/pingcap/tidb/issues/22231)
    - Fix the issue that the `select into outfile` statement might have no result when the column type is `YEAR` [#22159](https://github.com/pingcap/tidb/issues/22159)
    - Fix the issue that the query result might be wrong when `NULL` is in the `UNION` subquery [#26532](https://github.com/pingcap/tidb/issues/26532)
    - Fix the issue that the projection operator in execution might cause panic in some cases [#26534](https://github.com/pingcap/tidb/pull/26534)

+ TiKV

    - Fix the issue that the duration calculation might panic on certain platforms [#related-issue](https://github.com/rust-lang/rust/issues/86470#issuecomment-877557654)
    - Fix the wrong function that casts `DOUBLE` to `DOUBLE` [#25200](https://github.com/pingcap/tidb/issues/25200)
    - Fix the issue that the panic log might be lost when using the async logger [#8998](https://github.com/tikv/tikv/issues/8998)
    - Fix the panic issue that occurs when building a snapshot twice if encryption is enabled [#9786](https://github.com/tikv/tikv/issues/9786) [#10407](https://github.com/tikv/tikv/issues/10407)
    - Fix the wrong arguments type of the `json_unquote()` function in the coprocessor [#10176](https://github.com/tikv/tikv/issues/10176)
    - Fix the issues of suspicious warnings during shutdown and the non-deterministic response from Raftstore [#10353](https://github.com/tikv/tikv/issues/10353) [#10307](https://github.com/tikv/tikv/issues/10307)
    - Fix the issue of backup threads leak [#10287](https://github.com/tikv/tikv/issues/10287)
    - Fix the issue that Region split might panic and corrupt the metadata if the split process is too slow and Region merge is on-going [#8456](https://github.com/tikv/tikv/issues/8456) [#8783](https://github.com/tikv/tikv/issues/8783)
    - Fix the issue that the Region heartbeats prevent TiKV from splitting large Regions in some situations [#10111](https://github.com/tikv/tikv/issues/10111)
    - Fix the wrong statistics caused by the format inconsistency of CM Sketch between TiKV and TiDB [#25638](https://github.com/pingcap/tidb/issues/25638)
    - Fix the wrong statistics of the `apply wait duration` metric [#9893](https://github.com/tikv/tikv/issues/9893)
    - Fix the "Missing Blob" error after using `delete_files_in_range` in Titan [#10232](https://github.com/tikv/tikv/pull/10232)

+ PD

    - Fix a bug that the scheduler might reappear after executing the delete operation [#2572](https://github.com/tikv/pd/issues/2572)
    - Fix the data race issue that might occur when the scheduler is started before the temporary configuration is loaded [#3771](https://github.com/tikv/pd/issues/3771)
    - Fix a PD panic issue that might occur during the Region scattering operation [#3761](https://github.com/pingcap/pd/pull/3761)
    - Fix the issue that the priority of some operators is not set correctly [#3703](https://github.com/pingcap/pd/pull/3703)
    - Fix a PD panic issue that might occur when deleting the `evict-leader` scheduler from a non-existent store [#3660](https://github.com/tikv/pd/issues/3660)
    - Fix the issue that the PD Leader re-election is slow when there are many stores [#3697](https://github.com/tikv/pd/issues/3697)

+ TiDB Dashboard

    - Fix the issue that the **Profiling** UI cannot profile all TiDB instances [#944](https://github.com/pingcap/tidb-dashboard/pull/944)
    - Fix the issue that the **Statements** UI does not display "Plan Count" [#939](https://github.com/pingcap/tidb-dashboard/pull/939)
    - Fix the issue that the **Slow Query** UI might display the "unknown field" error after cluster upgrade [#902](https://github.com/pingcap/tidb-dashboard/issues/902)

+ TiFlash

    - Fix the potential panic issue that occurs when compiling DAG requests
    - Fix the panic issue that occurs when the read load is heavy
    - Fix the issue that TiFlash keeps restarting because of the split failure in column storage
    - Fix a potential bug that TiFlash cannot delete the delta data
    - Fix the incorrect results that occur when cloning the shared delta index concurrently
    - Fix a bug that TiFlash fails to restart in the case of incomplete data
    - Fix the issue that the old dm files cannot be removed automatically
    - Fix the panic issue that occurs when executing the `SUBSTRING` function with specific arguments
    - Fix the issue of incorrect results when casting the `INTEGER` type to the `TIME` type

+ Tools

    + Backup & Restore (BR)

        - Fix the issue that the data restore from the `mysql` schema might fail [#1142](https://github.com/pingcap/br/pull/1142)

    + TiDB Lightning

        - Fix the issue that TiDB Lightning fails to parse the `DECIMAL` type data in Parquet files [#1276](https://github.com/pingcap/br/pull/1276)
        - Fix the EOF error reported when TiDB Lightning splits the imported large CSV files [#1133](https://github.com/pingcap/br/issues/1133)
        - Fix a bug that an excessively large base value is generated when TiDB Lightning imports tables with the `auto_increment` column of the `FLOAT` or `DOUBLE` type [#1185](https://github.com/pingcap/br/pull/1185)
        - Fix the issue of TiDB Lightning panic that occurs when generating KV data larger than 4 GB [#1128](https://github.com/pingcap/br/pull/1128)

    + Dumpling

        - When using Dumpling to export data to the S3 storage, the `s3:ListBucket` permission is no longer required on the entire bucket. The permission is required only on the data source prefix. [#898](https://github.com/pingcap/br/issues/898)

    + TiCDC

        - Fix the issue of extra partition dispatching after adding new table partitions [#2205](https://github.com/pingcap/ticdc/pull/2205)
        - Fix the panic issue that occurs when TiCDC fails to read `/proc/meminfo` [#2023](https://github.com/pingcap/ticdc/pull/2023)
        - Reduce TiCDC's runtime memory consumption [#2011](https://github.com/pingcap/ticdc/pull/2011) [#1957](https://github.com/pingcap/ticdc/pull/1957)
        - Fix a bug that some MySQL connection might leak after MySQL sink meets the error and pauses [#1945](https://github.com/pingcap/ticdc/pull/1945)
        - Fix the issue that TiCDC changefeed cannot be created when start TS is less than current TS minus GC TTL [#1839](https://github.com/pingcap/ticdc/issues/1839)
        - Reduce memory `malloc` in sort heap to avoid too much CPU overhead [#1853](https://github.com/pingcap/ticdc/issues/1853)
        - Fix a bug that the replication task might stop when moving a table [#1827](https://github.com/pingcap/ticdc/pull/1827)
