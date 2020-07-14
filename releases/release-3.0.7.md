---
title: TiDB 3.0.7 Release Notes
aliases: ['/docs/dev/releases/release-3.0.7/','/docs/dev/releases/3.0.7/']
---

# TiDB 3.0.7 Release Notes

Release date: December 4, 2019

TiDB version: 3.0.7

TiDB Ansible version: 3.0.7

## TiDB

- Fix the issue that the lock TTL’s value is too large because the TiDB server’s local time is behind PD’s timestamp [#13868](https://github.com/pingcap/tidb/pull/13868)
- Fix the issue that the timezone is incorrect after parsing the date from strings using `gotime.Local` [#13793](https://github.com/pingcap/tidb/pull/13793)
- Fix the issue that the result might be incorrect because the `binSearch` function does not return an error in the implementation of `builtinIntervalRealSig` [#13767](https://github.com/pingcap/tidb/pull/13767)
- Fix the issue that data is incorrect because the precision is lost when an integer is converted to an unsigned floating point or decimal type [#13755](https://github.com/pingcap/tidb/pull/13755)
- Fix the issue that the result is incorrect because the `not null` flag is not properly reset when the `USING` clause is used in Natural Outer Join and Outer Join [#13739](https://github.com/pingcap/tidb/pull/13739)
- Fix the issue that the statistics are not accurate because a data race occurs when statistics are updated [#13687](https://github.com/pingcap/tidb/pull/13687)

## TiKV

- Make the deadlock detector only observe valid Regions to make sure the deadlock manager is in a valid Region [#6110](https://github.com/tikv/tikv/pull/6110)
- Fix a potential memory leak issue [#6128](https://github.com/tikv/tikv/pull/6128)
