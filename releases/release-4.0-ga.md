---
title: TiDB 4.0 GA Release Notes
aliases: ['/docs/dev/releases/release-4.0-ga/']
---

# TiDB 4.0 GA Release Notes

Release date: May 28, 2020

TiDB version: 4.0.0

## Compatibility Changes

* TiDB
    - Optimize the error message of the large-sized transactions for easier troubleshooting [#17219](https://github.com/pingcap/tidb/pull/17219)

* TiCDC
    - Optimize the structure of the `Changefeed` configuration file to improve usability [#588](https://github.com/pingcap/tiflow/pull/588)
    - Add the `ignore-txn-start-ts` configuration item, and change the condition from `commit_ts` to `start_ts` during transactions filtering [#589](https://github.com/pingcap/tiflow/pull/589)

## Important Bug Fixes

* TiKV
    - Fix the `DefaultNotFound` error that occurs when backing up using Backup & Restore (BR) [#7937](https://github.com/tikv/tikv/pull/7937)
    - Fix system panics caused by the out-of-order `ReadIndex` packages [#7930](https://github.com/tikv/tikv/pull/7930)
    - Fix system panics caused by incorrectly removing snapshot files after TiKV is restarted [#7927](https://github.com/tikv/tikv/pull/7927)

* TiFlash
    - Fix the possible data loss issue that occurs when the system panics because of incorrect processing logic of `Raft Admin Command`

## New Features

* TiDB
    - Add the `committer-concurrency` configuration item to control the number of `goroutines` in the retry-commit phase [#16849](https://github.com/pingcap/tidb/pull/16849)
    - Support the `show table partition regions` syntax [#17294](https://github.com/pingcap/tidb/pull/17294)
    - Add the `tmp-storage-quota` configuration item to limit the temporary disk space used by the TiDB server [#15700](https://github.com/pingcap/tidb/pull/15700)
    - Support checking whether the partitioned table uses a unique prefix index when creating and changing tables [#17213](https://github.com/pingcap/tidb/pull/17213)
    - Support the `insert/replace into tbl_name partition`(`partition_name_list`) statement [#17313](https://github.com/pingcap/tidb/pull/17313)
    - Support checking the value of `collations` when using the `Distinct` function [#17240](https://github.com/pingcap/tidb/pull/17240)
    - Support the `is null` filter condition during the Hash partition pruning [#17310](https://github.com/pingcap/tidb/pull/17310)
    - Support `admin check index`, `admin cleanup index`, and `admin recover index` in partitioned tables [#17392](https://github.com/pingcap/tidb/pull/17392) [#17405](https://github.com/pingcap/tidb/pull/17405) [#17317](https://github.com/pingcap/tidb/pull/17317)
    - Support range partition pruning for the `in` expressions  [#17320](https://github.com/pingcap/tidb/pull/17320)

* TiFlash
    - Support filtering out the data corresponding to the qualified `TSO` through the `min commit ts` value of the `Lock CF` when the Learner reads the data
    - Add the feature that the system explicitly reports an error to avoid incorrect calculation results when the value of `TIMESTAMP` type is less than `1970-01-01 00:00:00`
    - Support using flags in regular expressions when searching logs

* TiKV
    - Support collation rules of `ascii_bin` and `latin1_bin` encoding [#7919](https://github.com/tikv/tikv/pull/7919)

* PD
    - Support specifying the reverse proxy resource prefix for built-in TiDB Dashboard [#2457](https://github.com/pingcap/pd/pull/2457)
    - Support returning the `pending peer` and `down peer` information in interfaces of the PD client Region [#2443](https://github.com/pingcap/pd/pull/2443)
    - Add monitoring items such as `Direction of hotspot move leader`, `Direction of hotspot move peer`, and `Hot cache read entry number` [#2448](https://github.com/pingcap/pd/pull/2448)

* Tools
    + Backup & Restore (BR)
        - Support the backup and restore of `Sequence` and `View` [#242](https://github.com/pingcap/br/pull/242)
    + TiCDC
        - Support checking the validity of `Sink URI` when creating `Changefeed` [#561](https://github.com/pingcap/tiflow/pull/561)
        - Support checking whether the PD and TiKV versions meet the system requirements during system startup [#570](https://github.com/pingcap/tiflow/pull/570)
        - Support scheduling multiple tables in the same scheduling task generation cycle [#572](https://github.com/pingcap/tiflow/pull/572)
        - Add information about node roles in HTTP API [#591](https://github.com/pingcap/tiflow/pull/591)

## Bug Fixes

* TiDB

    - Fix the issue of unexpected timeouts when sending and receiving messages by disabling TiDB to send batch commands to TiFlash [#17307](https://github.com/pingcap/tidb/pull/17307)
    - Fix the issue of incorrectly distinguishing signed and unsigned integers during partition pruning, which improves performance [#17230](https://github.com/pingcap/tidb/pull/17230)
    - Fix the issue of upgrade failure from v3.1.1 to v4.0 because of the incompatible `mysql.user` table [#17300](https://github.com/pingcap/tidb/pull/17300)
    - Fix the issue of incorrect selection of the partition in the `update` statement [#17305](https://github.com/pingcap/tidb/pull/17305)
    - Fix system panics when receiving an unknown error message from TiKV [#17380](https://github.com/pingcap/tidb/pull/17380)
    - Fix system panics caused by incorrect processing logic when creating the table that is `key` partitioned [#17242](https://github.com/pingcap/tidb/pull/17242)
    - Fix the issue that the wrong `Index Merge Join` plan is selected because of incorrect optimizer processing logic [#17365](https://github.com/pingcap/tidb/pull/17365)
    - Fix the issue of inaccurate `duration` monitoring metric of the `SELECT` statement in Grafana [#16561](https://github.com/pingcap/tidb/pull/16561)
    - Fix the issue that the GC worker is blocked when the system error occurs [#16915](https://github.com/pingcap/tidb/pull/16915)
    - Fix the issue that the `UNIQUE` constraint on a boolean column results in an incorrect result in a comparison [#17306](https://github.com/pingcap/tidb/pull/17306)
    - Fix system panics caused by incorrect processing logic when `tidb_opt_agg_push_down` is enabled and the aggregation function pushes down the partitioned table [#17328](https://github.com/pingcap/tidb/pull/17328)
    - Fix the issue of accessing failed TiKV nodes in some cases [#17342](https://github.com/pingcap/tidb/pull/17342)
    - Fix the issue that the `isolation-read` configuration item in `tidb.toml` does not take effect [#17322](https://github.com/pingcap/tidb/pull/17322)
    - Fix the issue of incorrect order of output results due to incorrect processing logic when `hint` is used to enforce the stream aggregation [#17347](https://github.com/pingcap/tidb/pull/17347)
    - Fix the behavior that `insert` processes DIV under different `SQL_MODE` [#17314](https://github.com/pingcap/tidb/pull/17314)

* TiFlash

    - Fix the issue that the matching behavior of regular expressions in the search log feature is inconsistent with other components
    - Fix the issue of excessive restart time when nodes write large amounts of data by disabling the delay processing optimization of `Raft Compact Log Command` by default
    - Fix the issue that the system fails to start because TiDB incorrectly processes the `DROP DATABASE` statement in some scenarios
    - Fix the issue that the method of collecting CPU information in `Server_info` is different from that in other components
    - Fix the issue that the error `Too Many Pings` is reported when the `Query` statement is executed if `batch coprocessor` is enabled
    - Fix the issue that Dashboard fails to display the correct `deploy path` information because TiFlash does not report the related information

* TiKV

    - Fix the `DefaultNotFound` error that occurs when backing up using BR  [#7937](https://github.com/tikv/tikv/pull/7937)
    - Fix system panics caused by out-of-order `ReadIndex` packets [#7930](https://github.com/tikv/tikv/pull/7930)
    - Fix the issue that an unexpected error is returned because the read request callback function is not called [#7921](https://github.com/tikv/tikv/pull/7921)
    - Fix system panics caused by incorrectly removing snapshot files when TiKV is restarted [#7927](https://github.com/tikv/tikv/pull/7927)
    - Fix the issue that the `master key` cannot be rotated due to incorrect processing logic in storage encryption [#7898](https://github.com/tikv/tikv/pull/7898)
    - Fix the issue that the received `lock cf` file of the snapshot is not encrypted when the storage encryption is enabled [#7922](https://github.com/tikv/tikv/pull/7922)

* PD

    - Fix the 404 error when deleting `evict-leader-scheduler` or `grant-leader-scheduler` using pd-ctl [#2446](https://github.com/pingcap/pd/pull/2446)
    - Fix the issue that the `presplit` feature might not work properly when the TiFlash replica exists [#2447](https://github.com/pingcap/pd/pull/2447)

* Tools

    + Backup & Restore (BR)
        - Fix the issue that the data restoration fails due to network issues when BR restores data from cloud storage [#298](https://github.com/pingcap/br/pull/298)
    + TiCDC
        - Fix system panics caused by data race [#565](https://github.com/pingcap/tiflow/pull/565) [#566](https://github.com/pingcap/tiflow/pull/566)
        - Fix resource leaks or system blockages caused by incorrect processing logic [#574](https://github.com/pingcap/tiflow/pull/574) [#586](https://github.com/pingcap/tiflow/pull/586)
        - Fix the issue that the command line gets stuck because CLI cannot connect to PD [#579](https://github.com/pingcap/tiflow/pull/579)
