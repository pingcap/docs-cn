---
title: TiDB 3.0.16 Release Notes
aliases: ['/docs/dev/releases/release-3.0.16/']
summary: TiDB 3.0.16 was released on July 03, 2020. The release includes improvements such as support for 'is null' filter condition, handling of SQL timeout issues, and removal of sensitive information in slow query logs. Bug fixes include resolving data inconsistency issues, fixing panic issues, and addressing errors in JSON comparison and query results. TiKV and PD also received bug fixes for issues related to store heartbeats, peer removal, and error handling.
---

# TiDB 3.0.16 Release Notes

Release date: July 03, 2020

TiDB version: 3.0.16

## Improvements

+ TiDB

    - Support the `is null` filter condition in hash partition pruning [#17308](https://github.com/pingcap/tidb/pull/17308)
    - Assign different `Backoffer`s to each Region to avoid the SQL timeout issue when multiple Region requests fail at the same time [#17583](https://github.com/pingcap/tidb/pull/17583)
    - Split separate Regions for the newly added partition [#17668](https://github.com/pingcap/tidb/pull/17668)
    - Discard feedbacks generated from the `delete` or `update` statement [#17841](https://github.com/pingcap/tidb/pull/17841)
    - Correct the usage of `json.Unmarshal` in `job.DecodeArgs` to be compatible with future Go versions [#17887](https://github.com/pingcap/tidb/pull/17887)
    - Remove sensitive information in the slow query log and the statement summary table [#18128](https://github.com/pingcap/tidb/pull/18128)
    - Match the MySQL behavior with `DateTime` delimiters [#17499](https://github.com/pingcap/tidb/pull/17499)
    - Handle `%h` in date formats in the range that is consistent with MySQL [#17496](https://github.com/pingcap/tidb/pull/17496)

+ TiKV

    - Avoid sending store heartbeats to PD after snapshots are received [#8145](https://github.com/tikv/tikv/pull/8145)
    - Improve the PD client log [#8091](https://github.com/tikv/tikv/pull/8091)

## Bug Fixes

+ TiDB

    - Fix the data inconsistency issue occurred because the lock of a written and deleted primary key in one transaction is resolved by another transaction [#18248](https://github.com/pingcap/tidb/pull/18248)
    - Fix the `Got too many pings` gRPC error log in the PD server-side followers [#17944](https://github.com/pingcap/tidb/pull/17944)
    - Fix the panic issue that might occur when the child of HashJoin returns the `TypeNull` column [#17935](https://github.com/pingcap/tidb/pull/17935)
    - Fix the error message when access is denied [#17722](https://github.com/pingcap/tidb/pull/17722)
    - Fix JSON comparison issue for the `int` and `float` types [#17715](https://github.com/pingcap/tidb/pull/17715)
    - Update the failpoint which causes data race [#17710](https://github.com/pingcap/tidb/pull/17710)
    - Fix the issue that the timeout pre-split Regions might not work when creating tables [#17617](https://github.com/pingcap/tidb/pull/17617)
    - Fix the panic caused by ambiguous error messages after the sending failure [#17378](https://github.com/pingcap/tidb/pull/17378)
    - Fix the issue that `FLASHBACK TABLE` might fail in some special cases [#17165](https://github.com/pingcap/tidb/pull/17165)
    - Fix the issue of inaccurate range calculation results when statements only have string columns [#16658](https://github.com/pingcap/tidb/pull/16658)
    - Fix the query error occurred when the `only_full_group_by` SQL mode is set [#16620](https://github.com/pingcap/tidb/pull/16620)
    - Fix the issue that the field length of results returned from the `case when` function is inaccurate [#16562](https://github.com/pingcap/tidb/pull/16562)
    - Fix the type inference for the decimal property in the `count` aggregate function [#17702](https://github.com/pingcap/tidb/pull/17702)

+ TiKV

    - Fix the potential wrong result read from ingested files [#8039](https://github.com/tikv/tikv/pull/8039)
    - Fix the issue that a peer cannot be removed when its store is isolated during multiple merge processes [#8005](https://github.com/tikv/tikv/pull/8005)

+ PD

    - Fix the `404` error when querying Region keys in PD Control [#2577](https://github.com/pingcap/pd/pull/2577)
