---
title: TiDB 3.0.15 Release Notes
aliases: ['/docs/dev/releases/release-3.0.15/']
---

# TiDB 3.0.15 Release Notes

Release date: June 5, 2020

TiDB version: 3.0.15

## New Features

+ TiDB

    - Forbid the query in partitioned tables to use the plan cache feature [#16759](https://github.com/pingcap/tidb/pull/16759)
    - Support the `admin recover index` and `admin check index` statements on partitioned tables [#17315](https://github.com/pingcap/tidb/pull/17315) [#17390](https://github.com/pingcap/tidb/pull/17390)
    - Support partition pruning of the `in` condition for Range partitioned tables [#17318](https://github.com/pingcap/tidb/pull/17318)
    - Optimize the output of `SHOW CREATE TABLE`, and add quotation marks to the partition name [#16315](https://github.com/pingcap/tidb/pull/16315)
    - Support the `ORDER BY` clause in the `GROUP_CONCAT` function [#16988](https://github.com/pingcap/tidb/pull/16988)
    - Optimize the memory allocation mechanism of `CMSketch` statistics to reduce the impact of garbage collection (GC) on performance [#17543](https://github.com/pingcap/tidb/pull/17543)

+ PD

    - Add a policy in which PD performs scheduling in terms of the number of Leaders [#2479](https://github.com/pingcap/pd/pull/2479)

## Bug Fixes

+ TiDB

    - Use deep copy to copy the `enum` and `set` type data in the `Hash` aggregate function; fix an issue of correctness [#16890](https://github.com/pingcap/tidb/pull/16890)
    - Fix the issue that `PointGet` returns incorrect results because of the wrong processing logic of integer overflow [#16753](https://github.com/pingcap/tidb/pull/16753)
    - Fix the issue of incorrect results caused by incorrect processing logic when the `CHAR()` function is used in the query predicate [#16557](https://github.com/pingcap/tidb/pull/16557)
    - Fix the issue of inconsistent results in the storage layer and calculation layer of the `IsTrue` and `IsFalse` functions [#16627](https://github.com/pingcap/tidb/pull/16627)
    - Fix the incorrect `NotNull` flags in some expressions, such as `case when` [#16993](https://github.com/pingcap/tidb/pull/16993)
    - Fix the issue that the optimizer cannot find a physical plan for `TableDual` in some scenarios [#17014](https://github.com/pingcap/tidb/pull/17014)
    - Fix the issue that the syntax for partition selection does not take effect correctly in the Hash partitioned table [#17051](https://github.com/pingcap/tidb/pull/17051)
    - Fix the inconsistent results between TiDB and MySQL when XOR operates on a floating-point number [#16976](https://github.com/pingcap/tidb/pull/16976)
    - Fix the error that occurs when executing DDL statement in the prepared manner [#17415](https://github.com/pingcap/tidb/pull/17415)
    - Fix the incorrect processing logic of computing the batch size in the ID allocator [#17548](https://github.com/pingcap/tidb/pull/17548)
    - Fix the issue that the `MAX_EXEC_TIME` SQL hint does not take effect when the time exceeds the expensive threshold [#17534](https://github.com/pingcap/tidb/pull/17534)

+ TiKV

    - Fix the issue that memory defragmentation is not effective after running for a long time [#7790](https://github.com/tikv/tikv/pull/7790)
    - Fix the panic issue caused by incorrectly removing snapshot files after TiKV is restarted accidentally [#7925](https://github.com/tikv/tikv/pull/7925)
    - Fix the gRPC disconnection caused by too large message packages [#7822](https://github.com/tikv/tikv/pull/7822)
