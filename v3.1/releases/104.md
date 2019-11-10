---
title: TiDB 1.0.4 Release Notes
category: Releases
---

# TiDB 1.0.4 Release Notes

On December 11, 2017, TiDB 1.0.4 is released with the following updates:

## TiDB

- [Speed up the loading of the statistics when starting the `tidb-server`](https://github.com/pingcap/tidb/pull/5362)
- [Improve the performance of the `show variables` statement](https://github.com/pingcap/tidb/pull/5363)
- [Fix a potential issue when using the `Add Index` statement to handle the combined indexes](https://github.com/pingcap/tidb/pull/5323)
- [Fix a potential issue when using the `Rename Table` statement to move a table to another database](https://github.com/pingcap/tidb/pull/5314)
- [Accelerate the effectiveness for the `Alter/Drop User` statement](https://github.com/pingcap/tidb/pull/5226)

## TiKV

- [Fix a possible performance issue when a snapshot is applied](https://github.com/pingcap/tikv/pull/2559)
- [Fix the performance issue for reverse scan after removing a lot of data](https://github.com/pingcap/tikv/pull/2559)
- [Fix the wrong encoded result for the Decimal type under special circumstances](https://github.com/pingcap/tikv/pull/2571)

To upgrade from 1.0.3 to 1.0.4, follow the rolling upgrade order of PD -> TiKV -> TiDB.
