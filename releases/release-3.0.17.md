---
title: TiDB 3.0.17 Release Notes
---

# TiDB 3.0.17 Release Notes

Release date: Aug 3, 2020

TiDB version: 3.0.17

## Improvements

+ TiDB

    - Decrease the default value of the `query-feedback-limit` configuration item from 1024 to 512, and improve the statistics feedback mechanism to ease its impact on the cluster [#18770](https://github.com/pingcap/tidb/pull/18770)
    - Limit batch split count for one request [#18694](https://github.com/pingcap/tidb/pull/18694)
    - Accelerate `/tiflash/replica` HTTP API when there are many history DDL jobs in the TiDB cluster [#18386](https://github.com/pingcap/tidb/pull/18386)
    - Improve row count estimation for index equal condition [#17609](https://github.com/pingcap/tidb/pull/17609)
    - Speed up the execution of `kill tidb conn_id` [#18506](https://github.com/pingcap/tidb/pull/18506)

+ TiKV

    - Add the `hibernate-timeout` configuration that delays region hibernation to improve rolling update performance [#8207](https://github.com/tikv/tikv/pull/8207)

+ Tools

    + TiDB Lightning

        - `[black-white-list]` has been deprecated with a newer, easier-to-understand filter format [#332](https://github.com/pingcap/tidb-lightning/pull/332)

## Bug Fixes

+ TiDB

    - Return the actual error message instead of an empty set when a query which contains `IndexHashJoin` or `IndexMergeJoin` encounters a panic [#18498](https://github.com/pingcap/tidb/pull/18498)
    - Fix the unknown column error for SQL statements like `SELECT a FROM t HAVING t.a` [#18432](https://github.com/pingcap/tidb/pull/18432)
    - Forbid adding a primary key for a table when the table has no primary key or when the table already has an integer primary key [#18342](https://github.com/pingcap/tidb/pull/18342)
    - Return an empty set when executing `EXPLAIN FORMAT="dot" FOR CONNECTION` [#17157](https://github.com/pingcap/tidb/pull/17157)
    - Fix `STR_TO_DATE`'s handling for format token '%r', '%h' [#18725](https://github.com/pingcap/tidb/pull/18725)

+ TiKV

    - Fix a bug that might read stale data during region merging [#8111](https://github.com/tikv/tikv/pull/8111)
    - Fix the issue of memory leak during the scheduling process [#8355](https://github.com/tikv/tikv/pull/8355)

+ Tools

    + TiDB Lightning

        - Fix the issue that the `log-file` flag is ignored [#345](https://github.com/pingcap/tidb-lightning/pull/345)
