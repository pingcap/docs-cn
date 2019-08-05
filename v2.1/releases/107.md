---
title: TiDB 1.0.7 Release Notes
category: Releases
---

# TiDB 1.0.7 Release Notes

On January 22, 2018, TiDB 1.0.7 is released with the following updates:

## TiDB

- [Optimize the `FIELD_LIST` command](https://github.com/pingcap/tidb/pull/5679)
- [Fix data race of the information schema](https://github.com/pingcap/tidb/pull/5676)
- [Avoid adding read-only statements to history](https://github.com/pingcap/tidb/pull/5661)
- [Add the `session` variable to control the log query](https://github.com/pingcap/tidb/pull/5659)
- [Fix the resource leak issue in statistics](https://github.com/pingcap/tidb/pull/5657)
- [Fix the goroutine leak issue](https://github.com/pingcap/tidb/pull/5624)
- [Add schema info API for the http status server](https://github.com/pingcap/tidb/pull/5256)
- [Fix an issue about `IndexJoin`](https://github.com/pingcap/tidb/pull/5623)
- [Update the behavior when `RunWorker` is false in DDL](https://github.com/pingcap/tidb/pull/5604)
- [Improve the stability of test results in statistics](https://github.com/pingcap/tidb/pull/5609)
- [Support `PACK_KEYS` syntax for the `CREATE TABLE` statement](https://github.com/pingcap/tidb/pull/5602)
- [Add `row_id` column for the null pushdown schema to optimize performance](https://github.com/pingcap/tidb/pull/5447)

## PD

- [Fix possible scheduling loss issue in abnormal conditions](https://github.com/pingcap/pd/pull/921)
- [Fix the compatibility issue with proto3](https://github.com/pingcap/pd/pull/919)
- [Add the log](https://github.com/pingcap/pd/pull/917)

## TiKV

- [Support `Table Scan`](https://github.com/pingcap/tikv/pull/2657)
- [Support the remote mode in tikv-ctl](https://github.com/pingcap/tikv/pull/2377)
- [Fix the format compatibility issue of tikv-ctl proto](https://github.com/pingcap/tikv/pull/2668)
- [Fix the loss of scheduling command from PD](https://github.com/pingcap/tikv/pull/2669)
- [Add timeout in Push metric](https://github.com/pingcap/tikv/pull/2686)

To upgrade from 1.0.6 to 1.0.7, follow the rolling upgrade order of PD -> TiKV -> TiDB.