---
title: TiDB 4.0 RC Release Notes
aliases: ['/docs/dev/releases/release-4.0.0-rc/','/docs/dev/releases/4.0.0-rc/']
---

# TiDB 4.0 RC Release Notes

Release date: April 8, 2020

TiDB version: 4.0.0-rc

TiUP version: 0.0.3

> **Warning:**
>
> Some known issues are found in this version, and these issues are fixed in new versions. It is recommended that you use the latest 4.0.x version.

## Compatibility Changes

+ TiDB

    - Refuse to get started instead of returning an alert log when the tidb-server status port is occupied [#15177](https://github.com/pingcap/tidb/pull/15177)

+ TiKV

    - Support the `pipelined` feature in pessimistic transactions, which improves the TPC-C performance by 20%. The risk is that the transaction commit might fail because of lock failure during the execution [#6984](https://github.com/tikv/tikv/pull/6984)
    - Enable the `unify-read-pool` configuration item in new clusters by default and use the previous setting of this item in old clusters [#7059](https://github.com/tikv/tikv/pull/7059)

+ Tools

    - TiDB Binlog

        * Add the configuration item for verifying Common Name [#934](https://github.com/pingcap/tidb-binlog/pull/934)

## Important Bug Fixes

+ TiDB

    - Fix the issue that replication between the upstream and downstream might go wrong when the DDL job is executed using the `PREPARE` statement because of the incorrect job query in the internal records [#15435](https://github.com/pingcap/tidb/pull/15435)
    - Fix the issue of incorrect subquery result in the `Read Commited` isolation level [#15471](https://github.com/pingcap/tidb/pull/15471)
    - Fix the issue of incorrect results caused by the Inline Projection optimization [#15411](https://github.com/pingcap/tidb/pull/15411)
    - Fix the issue that the SQL Hint `INL_MERGE_JOIN` is executed incorrectly in some cases [#15515](https://github.com/pingcap/tidb/pull/15515)
    - Fix the issue that columns with the `AutoRandom` attribute are rebased when the negative number is explicitly written to these columns [#15397](https://github.com/pingcap/tidb/pull/15397)

## New Features

+ TiDB

    - Add the case-sensitive collation so that users can enable `utf8mb4_general_ci` and `utf8_general_ci` in a new cluster [#33](https://github.com/pingcap/tidb/projects/33)
    - Enhance the `RECOVER TABLE` syntax to support recovering truncated tables [#15398](https://github.com/pingcap/tidb/pull/15398)
    - Refuse to get started instead of returning an alert log when the the tidb-server status port is occupied [#15177](https://github.com/pingcap/tidb/pull/15177)
    - Optimize the write performance of using a sequence as the default column values [#15216](https://github.com/pingcap/tidb/pull/15216)
    - Add the `DDLJobs` system table to query the details of DDL jobs [#14837](https://github.com/pingcap/tidb/pull/14837)
    - Optimize the `aggFuncSum` performance [#14887](https://github.com/pingcap/tidb/pull/14887)
    - Optimize the output of `EXPLAIN` [#15507](https://github.com/pingcap/tidb/pull/15507)

+ TiKV

    - Support the `pipelined` feature in pessimistic transactions, which improves the TPC-C performance by 20%. The risk is that the transaction commit might fail because of lock failure during the execution [#6984](https://github.com/tikv/tikv/pull/6984)
    - Support TLS in the HTTP port [#5393](https://github.com/tikv/tikv/pull/5393)
    - Enable the `unify-read-pool` configuration item in new clusters by default and use the previous setting of this item in old clusters [#7059](https://github.com/tikv/tikv/pull/7059)

+ PD

    - Support getting the default PD configuration information through the HTTP API [#2258](https://github.com/pingcap/pd/pull/2258)

+ Tools

    - TiDB Binlog

        * Add the configuration item for verifying Common Name [#934](https://github.com/pingcap/tidb-binlog/pull/934)

    - TiDB Lightning

        * Optimize the performance of TiDB Lightning [#281](https://github.com/pingcap/tidb-lightning/pull/281) [#275](https://github.com/pingcap/tidb-lightning/pull/275)

## Bug Fixes

+ TiDB

    - Fix the issue that replication between the upstream and downstream might go wrong when the DDL job is executed using the `PREPARE` statement because of the incorrect job query in the internal records [#15435](https://github.com/pingcap/tidb/pull/15435)
    - Fix the issue of incorrect subquery result in the `Read Commited` isolation level [#15471](https://github.com/pingcap/tidb/pull/15471)
    - Fix the issue of possible wrong behavior when using `INSERT ... VALUES` to specify the `BIT(N)` data type [#15350](https://github.com/pingcap/tidb/pull/15350)
    - Fix the issue that the DDL Job internal retry does not fully achieve the expected outcomes because the values of `ErrorCount` fail to be summed correctly [#15373](https://github.com/pingcap/tidb/pull/15373)
    - Fix the issue that Garbage Collection might work abnormally when TiDB connects to TiFlash [#15505](https://github.com/pingcap/tidb/pull/15505)
    - Fix the issue of incorrect result caused by the Inline Projection optimization [#15411](https://github.com/pingcap/tidb/pull/15411)
    - Fix the issue that the SQL Hint `INL_MERGE_JOIN` is executed incorrectly in some cases [#15515](https://github.com/pingcap/tidb/pull/15515)
    - Fix the issue that columns with the `AutoRandom` attribute are rebased when the negative number is explicitly written to these columns [#15397](https://github.com/pingcap/tidb/pull/15397)

+ TiKV
    - Fix the possible panic caused by transferring the leader when the Follower Read feature is enabled [#7101](https://github.com/tikv/tikv/pull/7101)

+ Tools

    - TiDB Lightning

        * Fix the issue of data error caused by the error of character conversion when the backend is TiDB [#283](https://github.com/pingcap/tidb-lightning/pull/283)

    - TiCDC

        * Fix the issue that an error is returned if the `test` schema does not exist in the downstream when MySQL sink is executing the DDL statement [#353](https://github.com/pingcap/tiflow/pull/353)
        * Support the real-time interactive mode in CDC cli [#351](https://github.com/pingcap/tiflow/pull/351)
        * Support checking whether the table in the upstream can be replicated during data replication [#368](https://github.com/pingcap/tiflow/pull/368)
        * Support asynchronous write to Kafka [#344](https://github.com/pingcap/tiflow/pull/344)
