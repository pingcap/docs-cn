---
title: TiDB 3.0.20 Release Notes
---

# TiDB 3.0.20 Release Notes

Release date: December 25, 2020

TiDB version: 3.0.20

## Compatibility Change

+ TiDB

    - Deprecate the `enable-streaming` configuration item [#21054](https://github.com/pingcap/tidb/pull/21054)

## Improvements

+ TiDB

    - Raise an error when preparing the `LOAD DATA` statement [#21222](https://github.com/pingcap/tidb/pull/21222)

+ TiKV

    - Add the `end_point_slow_log_threshold` configuration item [#9145](https://github.com/tikv/tikv/pull/9145)

## Bug Fixes

+ TiDB

    - Fix the incorrect cache of the transaction status for pessimistic transactions [#21706](https://github.com/pingcap/tidb/pull/21706)
    - Fix the issue of inaccurate statistics that occurs when querying `INFORMATION_SCHEMA.TIDB_HOT_REGIONS` [#21319](https://github.com/pingcap/tidb/pull/21319)
    - Fix the issue that `DELETE` might not delete data correctly when the database name is not in a pure lower representation [#21205](https://github.com/pingcap/tidb/pull/21205)
    - Fix the issue of stack overflow that occurs when building the recursive view [#21000](https://github.com/pingcap/tidb/pull/21000)
    - Fix the issue of goroutine leak in TiKV client [#20863](https://github.com/pingcap/tidb/pull/20863)
    - Fix the wrong default zero value for the `year` type [#20828](https://github.com/pingcap/tidb/pull/20828)
    - Fix the issue of goroutine leak in index lookup join [#20791](https://github.com/pingcap/tidb/pull/20791)
    - Fix the issue that executing `INSERT SELECT FOR UPDATE` returns the malformed packet in the pessimistic transaction [#20681](https://github.com/pingcap/tidb/pull/20681)
    - Fix the unknown time zone `'posixrules'` [#20605](https://github.com/pingcap/tidb/pull/20605)
    - Fix the issue that occurs when converting the unsigned integer type to the bit type [#20362](https://github.com/pingcap/tidb/pull/20362)
    - Fix the corrupted default value of the bit type column [#20339](https://github.com/pingcap/tidb/pull/20339)
    - Fix the potentially incorrect results when one of the equal condition is the `Enum` or `Set` type [#20296](https://github.com/pingcap/tidb/pull/20296)
    - Fix a wrong behavior of `!= any()` [#20061](https://github.com/pingcap/tidb/pull/20061)
    - Fix the issue that type conversion in `BETWEEN...AND...` returns invalid results [#21503](https://github.com/pingcap/tidb/pull/21503)
    - Fix a compatibility issue with the `ADDDATE` function [#21008](https://github.com/pingcap/tidb/pull/21008)
    - Set the correct default value for newly added `Enum` column [#20999](https://github.com/pingcap/tidb/pull/20999)
    - Fix the result of SQL statements like `SELECT DATE_ADD('2007-03-28 22:08:28',INTERVAL "-2.-2" SECOND)` to be compatible with MySQL [#20627](https://github.com/pingcap/tidb/pull/20627)
    - Fix the incorrect default value when modifying the column type [#20532](https://github.com/pingcap/tidb/pull/20532)
    - Fix the issue that the `timestamp` function gets wrong result when the input argument is the `float` or `decimal` type [#20469](https://github.com/pingcap/tidb/pull/20469)
    - Fix a potential deadlock issue in statistics [#20424](https://github.com/pingcap/tidb/pull/20424)
    - Fix the issue that the overflown float type data is inserted [#20251](https://github.com/pingcap/tidb/pull/20251)

+ TiKV

    - Fix the issue that an error is returned indicating that a key exists when this key is locked and deleted in a committed transaction [#8931](https://github.com/tikv/tikv/pull/8931)

+ PD

    - Fix the issue that too many logs are printed when starting PD and when there are too many stale Regions [#3064](https://github.com/pingcap/pd/pull/3064)
