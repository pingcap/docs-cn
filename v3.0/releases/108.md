---
title: TiDB 1.0.8 Release Notes
category: Releases
aliases: ['/docs/releases/108/']
---

# TiDB 1.0.8 Release Notes

On February 11, 2018, TiDB 1.0.8 is released with the following updates:

## TiDB

- [Fix issues in the `Outer Join` result in some scenarios](https://github.com/pingcap/tidb/pull/5712)
- [Optimize the performance of the `InsertIntoIgnore` statement](https://github.com/pingcap/tidb/pull/5738)
- [Fix the issue in the `ShardRowID` option](https://github.com/pingcap/tidb/pull/5751)
- [Add limitation (Configurable, the default value is 5000) to the DML statements number within a transaction](https://github.com/pingcap/tidb/pull/5754)
- [Fix an issue in the Table/Column aliases returned by the `Prepare` statement](https://github.com/pingcap/tidb/pull/5776)
- [Fix an issue in updating statistics delta](https://github.com/pingcap/tidb/pull/5787)
- [Fix a panic error in the `Drop Column` statement](https://github.com/pingcap/tidb/pull/5805)
- [Fix an DML issue when running the `Add Column After` statement](https://github.com/pingcap/tidb/pull/5818)
- [Improve the stability of the GC process by ignoring the regions with GC errors](https://github.com/pingcap/tidb/pull/5815)
- [Run GC concurrently to accelerate the GC process](https://github.com/pingcap/tidb/pull/5850)
- [Provide syntax support for the `CREATE INDEX` statement](https://github.com/pingcap/tidb/pull/5853)

## PD

- [Reduce the lock overheat of the region heartbeats](https://github.com/pingcap/pd/pull/932)
- [Fix the issue that a hot region scheduler selects the wrong Leader](https://github.com/pingcap/pd/pull/939)

## TiKV

- [Use `DeleteFilesInRanges` to clear stale data and improve the TiKV starting speed](https://github.com/pingcap/tikv/pull/2740)
- [Using `Decimal` in Coprocessor sum](https://github.com/pingcap/tikv/pull/2754)
- [Sync the metadata of the received Snapshot compulsorily to ensure its safety](https://github.com/pingcap/tikv/pull/2758)

To upgrade from 1.0.7 to 1.0.8, follow the rolling upgrade order of PD -> TiKV -> TiDB.
