---
title: TiDB 5.1.1 Release Notes
---

# TiDB 5.1.1 Release Notes

Release Date: July 30, 2021

TiDB version: 5.1.1

## Compatibility changes

+ TiDB

    - For TiDB clusters upgrade from v4.0 to v5.1, the default value of `tidb_multi_statement_mode` is `OFF`. It is recommended to use the multi-statement feature of your client library instead. See [the documentation on `tidb_multi_statement_mode`](/system-variables.md#tidb_multi_statement_mode-new-in-v4011) for details. [#25751](https://github.com/pingcap/tidb/pull/25751)
    - Change the default value of the `tidb_stmt_summary_max_stmt_count` variable from `200` to `3000` [#25874](https://github.com/pingcap/tidb/pull/25874)
    - Require the `SUPER` privilege to access the `table_storage_stats` table [#26352](https://github.com/pingcap/tidb/pull/26352)
    - Require the `SELECT` privilege on `mysql.user` to access the `information_schema.user_privileges` table to show other user's privileges [#26311](https://github.com/pingcap/tidb/pull/26311)
    - Require the `CONFIG` privilege to access the `information_schema.cluster_hardware` table [#26297](https://github.com/pingcap/tidb/pull/26297)
    - Require the `PROCESS` privilege to access the `information_schema.cluster_info` table [#26297](https://github.com/pingcap/tidb/pull/26297)
    - Require the `PROCESS` privilege to access the `information_schema.cluster_load` table [#26297](https://github.com/pingcap/tidb/pull/26297)
    - Require the `PROCESS` privilege to access the `information_schema.cluster_systeminfo` table [#26297](https://github.com/pingcap/tidb/pull/26297)
    - Require the `PROCESS` privilege to access the `information_schema.cluster_log` table [#26297](https://github.com/pingcap/tidb/pull/26297)
    - Require the `CONFIG` privilege to access the `information_schema.cluster_config` table [#26150](https://github.com/pingcap/tidb/pull/26150)

## Feature enhancements

+ TiDB Dashboard

    - Support OIDC SSO. By setting the OIDC-compatible SSO services (such as Okta and Auth0), users can log into TiDB Dashboard without entering the SQL password. [#3883](https://github.com/tikv/pd/pull/3883)

+ TiFlash

    - Support the `HAVING()` function in DAG requests

## Improvements

+ TiDB

    - Announce the general availability (GA) of the Stale Read feature
    - Avoid allocation for `paramMarker` to speed up data insertion [#26076](https://github.com/pingcap/tidb/pull/26076)
    - Support the stable result mode to make the query results more stable [#25995](https://github.com/pingcap/tidb/pull/25995)
    - Support pushing down the built-in function `json_unquote()` to TiKV [#26265](https://github.com/pingcap/tidb/pull/26265)
    - Support retrying MPP queries [#26480](https://github.com/pingcap/tidb/pull/26480)
    - Change the `LOCK` record into the `PUT` record for the index keys using `point get` or `batch point get` for `UPDATE` reads [#26225](https://github.com/pingcap/tidb/pull/26225)
    - Forbid creating views from stale queries [#26200](https://github.com/pingcap/tidb/pull/26200)
    - Thoroughly push down the `COUNT(DISTINCT)` aggregation function in the MPP mode [#26194](https://github.com/pingcap/tidb/pull/26194)
    - Check the availability of TiFlash before launching MPP queries [#26192](https://github.com/pingcap/tidb/pull/26192)
    - Do not allow setting the read timestamp to a future time [#25763](https://github.com/pingcap/tidb/pull/25763)
    - Print log warnings when aggregation functions cannot be pushed down in `EXPLAIN` statements [#25737](https://github.com/pingcap/tidb/pull/25737)
    - Add the `statements_summary_evicted` table to record the evicted count information of a cluster [#25587](https://github.com/pingcap/tidb/pull/25587)
    - Improve the MySQL compatibility of the built-in function `str_to_date` for the format specifiers `%b/%M/%r/%T` [#25768](https://github.com/pingcap/tidb/pull/25768)

+ TiKV

    - Make the prewrite requests as idempotent as possible to reduce the chance of undetermined errors [#10586](https://github.com/tikv/tikv/pull/10586)
    - Prevent the risk of stack overflow when handling many expired commands [#10502](https://github.com/tikv/tikv/pull/10502)
    - Avoid excessive commit request retrying by not using the Stale Read request's `start_ts` to update `max_ts` [#10451](https://github.com/tikv/tikv/pull/10451)
    - Handle read ready and write ready separately to reduce read latency [#10592](https://github.com/tikv/tikv/pull/10592)
    - Reduce the impact on data import speed when the I/O rate limiting is enabled [#10390](https://github.com/tikv/tikv/pull/10390)
    - Improve the load balance between Raft gRPC connections [#10495](https://github.com/tikv/tikv/pull/10495)

+ Tools

    + TiCDC

        - Remove `file sorter` [#2327](https://github.com/pingcap/ticdc/pull/2327)
        - Improve the error message returned when a PD endpoint misses the certificate [#1973](https://github.com/pingcap/ticdc/issues/1973)

    + TiDB Lightning

        - Add a retry mechanism for restoring schemas [#1294](https://github.com/pingcap/br/pull/1294)

    + Dumpling

        - Always split tables using `_tidb_rowid` when the upstream is a TiDB v3.x cluster, which helps reduce TiDB's memory usage [#295](https://github.com/pingcap/dumpling/issues/295)
        - Reduce the frequency of accessing the database metadata to improve Dumpling's performance and stability [#315](https://github.com/pingcap/dumpling/pull/315)

## Bug fixes

+ TiDB

    - Fix the data loss issue that might occur when changing the column type with `tidb_enable_amend_pessimistic_txn=on` [#26203](https://github.com/pingcap/tidb/issues/26203)
    - Fix the issue that the behavior of the `last_day` function is incompatible in the SQL mode [#26001](https://github.com/pingcap/tidb/pull/26001)
    - Fix the panic issue that might occur when `LIMIT` is on top of window functions [#25344](https://github.com/pingcap/tidb/issues/25344)
    - Fix the issue that committing pessimistic transactions might cause write conflict [#25964](https://github.com/pingcap/tidb/issues/25964)
    - Fix the issue that the result of index join in correlated subqueries is wrong [#25799](https://github.com/pingcap/tidb/issues/25799)
    - Fix a bug that the successfully committed optimistic transactions might report commit errors [#10468](https://github.com/tikv/tikv/issues/10468)
    - Fix the issue that an incorrect result is returned when using merge join on the `SET` type column [#25669](https://github.com/pingcap/tidb/issues/25669)
    - Fix a bug that the index keys in a pessimistic transaction might be repeatedly committed [#26359](https://github.com/pingcap/tidb/issues/26359)
    - Fix the risk of integer overflow when the optimizer is locating partitions [#26227](https://github.com/pingcap/tidb/issues/26227)
    - Fix the issue that invalid values might be written when casting `DATE` to timestamp [#26292](https://github.com/pingcap/tidb/issues/26292)
    - Fix the issue that the Coprocessor Cache metrics are not displayed on Grafana [#26338](https://github.com/pingcap/tidb/issues/26338)
    - Fix the issue of annoying logs caused by telemetry [#25760](https://github.com/pingcap/tidb/issues/25760) [#25785](https://github.com/pingcap/tidb/issues/25785)
    - Fix a bug on the query range of prefix index [#26029](https://github.com/pingcap/tidb/issues/26029)
    - Fix the issue that concurrently truncating the same partition hangs DDL executions [#26229](https://github.com/pingcap/tidb/issues/26229)
    - Fix the issue of duplicate `ENUM` items [#25955](https://github.com/pingcap/tidb/issues/25955)
    - Fix a bug that the CTE iterator is not correctly closed [#26112](https://github.com/pingcap/tidb/issues/26112)
    - Fix the issue that the `LOAD DATA` statement might abnormally import non-utf8 data [#25979](https://github.com/pingcap/tidb/issues/25979)
    - Fix the panic issue that might occur when using the window function on the unsigned integer columns [#25956](https://github.com/pingcap/tidb/issues/25956)
    - Fix the issue that TiDB might panic when resolving async commit locks [#25778](https://github.com/pingcap/tidb/issues/25778)
    - Fix the issue that Stale Read is not fully compatible with the `PREPARE` statements [#25800](https://github.com/pingcap/tidb/pull/25800)
    - Fix the issue that the ODBC-styled constant (for example, `{d '2020-01-01'}`) cannot be used as the expression [#25531](https://github.com/pingcap/tidb/issues/25531)
    - Fix an error that occurs when running TiDB alone [#25555](https://github.com/pingcap/tidb/pull/25555)

+ TiKV

    - Fix the issue that the duration calculation might panic on certain platforms [#10569](https://github.com/tikv/tikv/pull/10569)
    - Fix the issue that Load Base Split mistakenly uses the unencoded keys of `batch_get_command` [#10542](https://github.com/tikv/tikv/issues/10542)
    - Fix the issue that changing the `resolved-ts.advance-ts-interval` configuration online cannot take effect immediately [#10426](https://github.com/tikv/tikv/issues/10426)
    - Fix the issue of follower metadata corruption in rare cases with more than 4 replicas [#10225](https://github.com/tikv/tikv/issues/10225)
    - Fix the panic issue that occurs when building a snapshot twice if encryption is enabled [#9786](https://github.com/tikv/tikv/issues/9786) [#10407](https://github.com/tikv/tikv/issues/10407)
    - Fix the wrong `tikv_raftstore_hibernated_peer_state` metric [#10330](https://github.com/tikv/tikv/issues/10330)
    - Fix the wrong arguments type of the `json_unquote()` function in the coprocessor [#10176](https://github.com/tikv/tikv/issues/10176)
    - Fix a bug that the index keys in a pessimistic transaction might be repeatedly committed [#10468](https://github.com/tikv/tikv/issues/10468#issuecomment-869491061)
    - Fix the issue that the `ReadIndex` request returns stale result right after the leader is transferred [#9351](https://github.com/tikv/tikv/issues/9351)

+ PD

    - Fix the issue the expected scheduling cannot be generated when the conflict occurs due to multiple schedulers running at the same time [#3807](https://github.com/tikv/pd/issues/3807) [#3778](https://github.com/tikv/pd/issues/3778)
    - Fix the issue that the scheduler might appear again even if the scheduler is already deleted [#2572](https://github.com/tikv/pd/issues/2572)

+ TiFlash

    - Fix the potential panic issue that occurs when running table scan tasks
    - Fix a bug that TiFlash raises the error about `duplicated region` when handling DAQ requests
    - Fix the panic issue that occurs when the read load is heavy
    - Fix the potential panic issue that occurs when executing the `DateFormat` function
    - Fix the potential memory leak issue that occurs when executing MPP tasks
    - Fix the issue of unexpected results when executing the aggregation functions `COUNT` or `COUNT DISTINCT`
    - Fix a potential bug that TiFlash cannot restore data when deployed on multiple disks
    - Fix the issue that TiDB Dashboard cannot display the disk information of TiFlash correctly
    - Fix the potential panic issue that occurs when deconstructing `SharedQueryBlockInputStream`
    - Fix the potential panic issue that occurs when deconstructing `MPPTask`
    - Fix the potential issue of data inconsistency after synchronizing data via snapshot

+ Tools

    + TiCDC

        - Fix the support for the new collation feature [#2301](https://github.com/pingcap/ticdc/issues/2301)
        - Fix the issue that an unsynchronized access to a shared map at runtime might cause panic [#2300](https://github.com/pingcap/ticdc/pull/2300)
        - Fix the potential DDL loss issue that occurs when the owner crashes while executing the DDL statement [#2290](https://github.com/pingcap/ticdc/pull/2290)
        - Fix the issue of trying to resolve locks in TiDB prematurely [#2188](https://github.com/pingcap/ticdc/issues/2188)
        - Fix a bug that might cause data loss if a TiCDC node is killed immediately after a table migration [#2033](https://github.com/pingcap/ticdc/pull/2033)
        - Fix the handling logic of `changefeed update` on `--sort-dir` and `--start-ts` [#1921](https://github.com/pingcap/ticdc/pull/1921)

    + Backup & Restore (BR)

        - Fix the issue that the size of the data to restore is incorrectly calculated [#1270](https://github.com/pingcap/br/issues/1270)
        - Fix the issue of missed DDL events that occurs when restoring from cdclog [#870](https://github.com/pingcap/br/issues/870)

    + TiDB Lightning

        - Fix the issue that TiDB fails to parse the `DECIMAL` type data in Parquet files [#1275](https://github.com/pingcap/br/pull/1275)
        - Fix the issue of integer overflow when calculating key intervals [#1291](https://github.com/pingcap/br/issues/1291) [#1290](https://github.com/pingcap/br/issues/1290)
