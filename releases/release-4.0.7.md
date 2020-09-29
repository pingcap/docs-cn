---
title: TiDB 4.0.7 Release Notes
---

# TiDB 4.0.7 Release Notes

Release date: September 29, 2020

TiDB version: 4.0.7

## New Features

+ PD

    - Add the `GetAllMembers` function in the PD client to get PD member information [#2980](https://github.com/pingcap/pd/pull/2980)

+ TiDB Dashboard

    - Support generating the metrics relationship graph [#760](https://github.com/pingcap-incubator/tidb-dashboard/pull/760)

## Improvements

+ TiDB

    - Add more runtime information for the `join` operator [#20093](https://github.com/pingcap/tidb/pull/20093)
    - Add the hit ratio information of coprocessor cache in `EXPLAIN ANALYZE` [#19972](https://github.com/pingcap/tidb/pull/19972)
    - Support pushing down the `ROUND` function to TiFlash [#19967](https://github.com/pingcap/tidb/pull/19967)
    - Add the default value of `CMSketch` for `ANALYZE` [#19927](https://github.com/pingcap/tidb/pull/19927)
    - Refine error message desensitization [#20004](https://github.com/pingcap/tidb/pull/20004)
    - Accept connections from clients using connectors from MySQL 8.0 [#19959](https://github.com/pingcap/tidb/pull/19959)

+ TiKV

    - Support the JSON log format [#8382](https://github.com/tikv/tikv/pull/8382)

+ PD

    - Count schedule operators when they are finished rather than added [#2983](https://github.com/pingcap/pd/pull/2983)
    - Set the `make-up-replica` operator to high priority [#2977](https://github.com/pingcap/pd/pull/2977)

+ TiFlash

    - Improve the error handling of the Region meta change that occurs during reads

+ Tools

    + TiCDC

        - Support translating more execution-efficient SQL statements in MySQL sink when the old value feature is enabled [#955](https://github.com/pingcap/ticdc/pull/955)

    + Backup & Restore (BR)

        - Add connection retry when the connection is broken during backup [#508](https://github.com/pingcap/br/pull/508)

    + TiDB Lightning

        - Support dynamically updating the log level via the HTTP interface [#393](https://github.com/pingcap/tidb-lightning/pull/393)

## Bug Fixes

+ TiDB

    - Fix a vectorization bug from `and`/`or`/`COALESCE` caused by shortcut [#20092](https://github.com/pingcap/tidb/pull/20092)
    - Fix the issue that plan digests are the same when the cop task stores are of different types [#20076](https://github.com/pingcap/tidb/pull/20076)
    - Fix the wrong behavior of the `!= any()` function [#20062](https://github.com/pingcap/tidb/pull/20062)
    - Fix the query error that occurs when the `slow-log` file does not exist [#20051](https://github.com/pingcap/tidb/pull/20051)
    - Fix the issue that Region requests continue to retry when the context is canceled [#20031](https://github.com/pingcap/tidb/pull/20031)
    - Fix the issue that querying the time type of the `cluster_slow_query` table in streaming request might result in an error [#19943](https://github.com/pingcap/tidb/pull/19943)
    - Fix the issue that DML statements using `case when` might cause schema change [#20095](https://github.com/pingcap/tidb/pull/20095)
    - Fix the issue that the `prev_stmt` information in slow log is not desensitized [#20048](https://github.com/pingcap/tidb/pull/20048)
    - Fix the issue that tidb-server does not release the table lock when it exits abnormally [#20020](https://github.com/pingcap/tidb/pull/20020)
    - Fix the incorrect error message that occurs when inserting data of the `ENUM` and `SET` type [#19950](https://github.com/pingcap/tidb/pull/19950)
    - Fix the wrong behavior of the `IsTrue` function in some situations [#19903](https://github.com/pingcap/tidb/pull/19903)
    - Fix the issue that the `CLUSTER_INFO` system table might not work normally after PD is scaled in or out [#20026](https://github.com/pingcap/tidb/pull/20026)
    - Avoid unnecessary warnings or errors when folding constants in `control` expressions [#19910](https://github.com/pingcap/tidb/pull/19910)
    - Update the method of updating statistics to avoid Out of Memory (OOM) [#20013](https://github.com/pingcap/tidb/pull/20013)

+ TiKV

    - Fix the issue of unavailable Status API when TLS handshake fails [#8649](https://github.com/tikv/tikv/pull/8649)
    - Fix the potential undefined behaviors [#7782](https://github.com/tikv/tikv/pull/7782)
    - Fix the possible panic caused by generating snapshots when executing `UnsafeDestroyRange` [#8681](https://github.com/tikv/tikv/pull/8681)

+ PD

    - Fix the bug that PD might panic if some Regions have no Leader when `balance-region` is enabled [#2994](https://github.com/pingcap/pd/pull/2994)
    - Fix the statistical deviation of Region size and Region keys after Region merge [#2985](https://github.com/pingcap/pd/pull/2985)
    - Fix the incorrect hotspot statistics [#2991](https://github.com/pingcap/pd/pull/2991)
    - Fix the issue that there is no `nil` check in `redirectSchedulerDelete` [#2974](https://github.com/pingcap/pd/pull/2974)

+ TiFlash

    - Fix the wrong result of right outer join

+ Tools

    + Backup & Restore (BR)

        - Fix a bug that causes the TiDB configuration to change after the restore process [#509](https://github.com/pingcap/br/pull/509)

    + Dumpling

        - Fix the issue that Dumpling fails to parse metadata when some variables are `NULL` [#150](https://github.com/pingcap/dumpling/pull/150)
