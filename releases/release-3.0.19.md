---
title: TiDB 3.0.19 Release Notes
---

# TiDB 3.0.19 Release Notes

Release date: September 25, 2020

TiDB version: 3.0.19

## Compatibility Changes

+ PD

    - Change the import path from `pingcap/pd` to `tikv/pd` [#2779](https://github.com/pingcap/pd/pull/2779)
    - Change the copyright information from `PingCAP, Inc` to `TiKV Project Authors` [#2777](https://github.com/pingcap/pd/pull/2777)

## Improvements

+ TiDB

    - Mitigate the impact of failure recovery on QPS performance [#19764](https://github.com/pingcap/tidb/pull/19764)
    - Support adjusting the concurrency of the `union` operator [#19885](https://github.com/pingcap/tidb/pull/19885)

+ TiKV

    - Set `sync-log` to `true` as a nonadjustable value [#8636](https://github.com/tikv/tikv/pull/8636)

+ PD

    - Add an alert rule for PD restart [#2789](https://github.com/pingcap/pd/pull/2789)

## Bug Fixes

+ TiDB

    - Fix the query error that occurs when the `slow-log` file does not exist [#20050](https://github.com/pingcap/tidb/pull/20050)
    - Add the privilege check for `SHOW STATS_META` and `SHOW STATS_BUCKET` [#19759](https://github.com/pingcap/tidb/pull/19759)
    - Forbid changing the decimal type to the integer type [#19681](https://github.com/pingcap/tidb/pull/19681)
    - Fix the issue that the constraint is not checked when altering the `ENUM`/`SET` type column [#20045](https://github.com/pingcap/tidb/pull/20045)
    - Fix the bug that tidb-server does not release table locks after a panic [#20021](https://github.com/pingcap/tidb/pull/20021)
    - Fix the bug that the `OR` operator is not handled correctly in the `WHERE` clause [#19901](https://github.com/pingcap/tidb/pull/19901)

+ TiKV

    - Fix the bug that TiKV panics when parsing responses with missing reason phrases [#8540](https://github.com/tikv/tikv/pull/8540)

+ Tools

    + TiDB Lightning

        - Fix the issue that the TiDB Lightning process does not exit in time when encountering illegal UTF characters in CSV in the strict mode [#378](https://github.com/pingcap/tidb-lightning/pull/378)
