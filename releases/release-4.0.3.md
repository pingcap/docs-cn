---
title: TiDB 4.0.3 Release Notes
---

# TiDB 4.0.3 Release Notes

Release date: July 24, 2020

TiDB version: 4.0.3

## New Features

+ TiDB Dashboard

    - Display detailed TiDB Dashboard version information [#679](https://github.com/pingcap-incubator/tidb-dashboard/pull/679)
    - Show browser compatibility notice for unsupported browsers or outdated browsers [#654](https://github.com/pingcap-incubator/tidb-dashboard/pull/654)
    - Support searching in the **SQL Statements** page [#658](https://github.com/pingcap-incubator/tidb-dashboard/pull/658)

+ TiFlash

    - Implement file encryption in TiFlash proxy

+ Tools

    + Backup & Restore (BR)

        - Support compressing backup files using zstd, lz4 or snappy [#404](https://github.com/pingcap/br/pull/404)

    + TiCDC

        - Support configuring `kafka-client-id` in MQ sink-uri [#706](https://github.com/pingcap/ticdc/pull/706)
        - Support updating `changefeed` configuration offline [#699](https://github.com/pingcap/ticdc/pull/699)
        - Support setting customized `changefeed` name [#727](https://github.com/pingcap/ticdc/pull/727)
        - Support TLS and MySQL SSL connection [#347](https://github.com/pingcap/ticdc/pull/347)
        - Support outputting changes in the Avro format [#753](https://github.com/pingcap/ticdc/pull/753)
        - Support the Apache Pulsar sink [#751](https://github.com/pingcap/ticdc/pull/751)

    + Dumpling

        - Support the specialized CSV separator and delimiter [#116](https://github.com/pingcap/dumpling/pull/116)
        - Support specifying the format of the output file name [#122](https://github.com/pingcap/dumpling/pull/122)

## Improvements

+ TiDB

    - Add the `tidb_log_desensitization` global variable to control whether to do desensitization when logging SQL queries [#18581](https://github.com/pingcap/tidb/pull/18581)
    - Enable `tidb_allow_batch_cop` by default [#18552](https://github.com/pingcap/tidb/pull/18552)
    - Speed up canceling a query [#18505](https://github.com/pingcap/tidb/pull/18505)
    - Add a header for the `tidb_decode_plan` result [#18501](https://github.com/pingcap/tidb/pull/18501)
    - Make the configuration checker compatible with earlier versions of the configuration file [#18046](https://github.com/pingcap/tidb/pull/18046)
    - Enable collecting the execution information by default [#18518](https://github.com/pingcap/tidb/pull/18518)
    - Add the `tiflash_tables` and `tiflash_segments` system tables [#18536](https://github.com/pingcap/tidb/pull/18536)
    - Move `AUTO RANDOM` out of experimental features and announce its general availability. The improvements and compatibility changes are as follows:
        - Deprecate `experimental.allow-auto-random` in the configuration file. No matter how this item is configured, you can always define the `AUTO RANDOM` feature on columns. [#18613](https://github.com/pingcap/tidb/pull/18613) [#18623](https://github.com/pingcap/tidb/pull/18623)
        - Add the `tidb_allow_auto_random_explicit_insert` session variable to control the explicit writes on `AUTO RANDOM` columns. The default value is `false`. This is to avoid the unexpected `AUTO_RANDOM_BASE` update caused by explicit writes on columns. [#18508](https://github.com/pingcap/tidb/pull/18508)
        - Allow defining `AUTO_RANDOM` only on `BIGINT` and `UNSIGNED BIGINT` columns and restrict the maximum number of shard bits to `15`, which avoids the allocatable space being consumed too quickly [#18538](https://github.com/pingcap/tidb/pull/18538)
        - Do not trigger the `AUTO_RANDOM_BASE` update when defining the `AUTO_RANDOM` attribute on the `BIGINT` column and inserting the negative value into the primary key [#17987](https://github.com/pingcap/tidb/pull/17987)
        - Use the highest bit of an integer for ID allocation when defining the `AUTO_RANDOM` attribute on `UNSIGNED BIGINT` columns, which gets more allocable space [#18404](https://github.com/pingcap/tidb/pull/18404)
        - Support updating the `AUTO_RANDOM` attribute in the result of `SHOW CREATE TABLE` [#18316](https://github.com/pingcap/tidb/pull/18316)

+ TiKV

    - Introduce the new `backup.num-threads` configuration to control the size of the backup thread pool [#8199](https://github.com/tikv/tikv/pull/8199)
    - Do not send store heartbeats when receiving snapshots [#8136](https://github.com/tikv/tikv/pull/8136)
    - Support dynamically changing the shared block cache's capacity [#8232](https://github.com/tikv/tikv/pull/8232)

+ PD

    - Support the JSON formatted log [#2565](https://github.com/pingcap/pd/pull/2565)

+ TiDB Dashboard

    - Improve the Key Visualizer bucket merge for cold logical ranges [#674](https://github.com/pingcap-incubator/tidb-dashboard/pull/674)
    - Rename the configuration item of `disable-telemetry` to `enable-telemetry` for consistency [#684](https://github.com/pingcap-incubator/tidb-dashboard/pull/684)
    - Show the progress bar when switching pages [#661](https://github.com/pingcap-incubator/tidb-dashboard/pull/661)
    - Ensure that the slow log search now follows the same behavior as log search when there are space separators [#682](https://github.com/pingcap-incubator/tidb-dashboard/pull/682)

+ TiFlash

    - Change the unit of the **DDL Jobs** panel in Grafana to `operations per minute`
    - Add a new dashboard in Grafana to show more metrics about **TiFlash-Proxy**
    - Reduce IOPS in TiFlash proxy

+ Tools

    + TiCDC

        - Replace table ID with table name in metrics [#695](https://github.com/pingcap/ticdc/pull/695)

    + Backup & Restore (BR)

        - Support outputting JSON logs [#336](https://github.com/pingcap/br/issues/336)
        - Support enabling pprof during runtime [#372](https://github.com/pingcap/br/pull/372)
        - Speed up DDL executions by sending DDL concurrently during restore [#377](https://github.com/pingcap/br/pull/377)

    + TiDB Lightning

        - Deprecate `black-white-list` with a newer and easier-to-understand filter format [#332](https://github.com/pingcap/tidb-lightning/pull/332)

## Bug Fixes

+ TiDB

    - Return an error instead of an empty set for `IndexHashJoin` when an error occurs during execution [#18586](https://github.com/pingcap/tidb/pull/18586)
    - Fix the recurring panic when gRPC transportReader is broken [#18562](https://github.com/pingcap/tidb/pull/18562)
    - Fix the issue that Green GC does not scan locks on offline stores which might cause data incompleteness [#18550](https://github.com/pingcap/tidb/pull/18550)
    - Forbid processing a non-read-only statement using TiFlash engine [#18534](https://github.com/pingcap/tidb/pull/18534)
    - Return the actual error message when a query connection panics [#18500](https://github.com/pingcap/tidb/pull/18500)
    - Fix the issue that the `ADMIN REPAIR TABLE` execution fails to reload the table metadata on the TiDB node [#18323](https://github.com/pingcap/tidb/pull/18323)
    - Fix the data inconsistency issue occurred because the lock of a written and deleted primary key in one transaction is resolved by another transaction [#18291](https://github.com/pingcap/tidb/pull/18291)
    - Make spilling disk work well [#18288](https://github.com/pingcap/tidb/pull/18288)
    - Fix the error reported when the `REPLACE INTO` statement works on the table that contains generated columns [#17907](https://github.com/pingcap/tidb/pull/17907)
    - Return the OOM error when the `IndexHashJoin` and `IndexMergeJoin` workers panic [#18527](https://github.com/pingcap/tidb/pull/18527)
    - Fix the bug that the execution of `Index Join` might return wrong results in special cases when the index used by `Index Join` contains the integer primary key [#18565](https://github.com/pingcap/tidb/pull/18565)
    - Fix the issue that when the new collation is enabled on the cluster, the data updated on columns with the new collation in a transaction cannot be read through the unique index [#18703](https://github.com/pingcap/tidb/pull/18703)

+ TiKV

    - Fix the issue that reads might get stale data during merging [#8113](https://github.com/tikv/tikv/pull/8113)
    - Fix the issue that collation does not work on the `min`/`max` function when aggregation is pushed down to TiKV [#8108](https://github.com/tikv/tikv/pull/8108)

+ PD

    - Fix the issue that creating TSO stream might be blocked for a while if the server crashes [#2648](https://github.com/pingcap/pd/pull/2648)
    - Fix the issue that `getSchedulers` might cause a data race [#2638](https://github.com/pingcap/pd/pull/2638)
    - Fix the issue that deleting the scheduler might cause deadlocks [#2637](https://github.com/pingcap/pd/pull/2637)
    - Fix the bug that placement rules are not considered when `balance-leader-scheduler` is enabled [#2636](https://github.com/pingcap/pd/pull/2636)
    - Fix the issue that sometimes service `safepoint` cannot be set properly, which might make BR and dumpling fail [#2635](https://github.com/pingcap/pd/pull/2635)
    - Fix the issue that the target store in `hot region scheduler` is incorrectly selected [#2627](https://github.com/pingcap/pd/pull/2627)
    - Fix the issue that the TSO request might take too long when PD leader is switched [#2622](https://github.com/pingcap/pd/pull/2622)
    - Fix the issue of stale scheduler after leader change [#2608](https://github.com/pingcap/pd/pull/2608)
    - Fix the issue that sometimes replicas of a Region cannot be adjusted to the best location when placement rules are enabled [#2605](https://github.com/pingcap/pd/pull/2605)
    - Fix the issue that the deployment path of the store is not updated according to the change of deployment directory [#2600](https://github.com/pingcap/pd/pull/2600)
    - Prevent `store limit` from changing to zero [#2588](https://github.com/pingcap/pd/pull/2588)

+ TiDB Dashboard

    - Fix the TiDB connection error when TiDB is scaled out [#689](https://github.com/pingcap-incubator/tidb-dashboard/pull/689)
    - Fix the issue that TiFlash instances are not displayed in the log searching page [#680](https://github.com/pingcap-incubator/tidb-dashboard/pull/680)
    - Fix the issue of metric selection reset after refreshing the overview page [#663](https://github.com/pingcap-incubator/tidb-dashboard/pull/663)
    - Fix a connection issue in some TLS scenarios [#660](https://github.com/pingcap-incubator/tidb-dashboard/pull/660)
    - Fix the issue that the language dropdown box is not displayed correctly in some cases [#677](https://github.com/pingcap-incubator/tidb-dashboard/pull/677)

+ TiFlash

    - Fix the issue that TiFlash crashes after renaming the primary key column
    - Fix the issue that concurrent `Learner Read` and `Remove Region` might cause deadlocks

+ Tools

    + TiCDC

        - Fix the issue that TiCDC leaks memory in some cases [#704](https://github.com/pingcap/ticdc/pull/704)
        - Fix the issue that unquoted table name causes the SQL syntax error [#676](https://github.com/pingcap/ticdc/pull/676)
        - Fix the issue that the processor does not fully exit after `p.stop` is called [#693](https://github.com/pingcap/ticdc/pull/693)

    + Backup & Restore (BR)

        - Fix the issue that the backup time might be negative [#405](https://github.com/pingcap/br/pull/405)

    + Dumpling

        - Fix the issue that Dumpling omits the `NULL` value when `--r` is specified [#119](https://github.com/pingcap/dumpling/pull/119)
        - Fix the bug that flushing tables might not work for tables to dump [#117](https://github.com/pingcap/dumpling/pull/117)

    + TiDB Lightning

        - Fix the issue that `--log-file` does not take effect [#345](https://github.com/pingcap/tidb-lightning/pull/345)

    + TiDB Binlog

        - Fix the issue that when TiDB Binlog replicates data to the downstream with TLS enabled, Drainer cannot be started which occurs because TLS is not enabled on the database driver used to update the checkpoint [#988](https://github.com/pingcap/tidb-binlog/pull/988)
