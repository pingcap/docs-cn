---
title: TiDB 1.0.3 Release Notes
category: Releases
---

# TiDB 1.0.3 Release Notes

On November 28, 2017, TiDB 1.0.3 is released with the following updates:

## TiDB

- [Optimize the performance in transaction conflicts scenario](https://github.com/pingcap/tidb/pull/5051)
- [Add the `TokenLimit` option in the config file](https://github.com/pingcap/tidb/pull/5107)
- [Output the default database in slow query logs](https://github.com/pingcap/tidb/pull/5107)
- [Remove the DDL statement from query duration metrics](https://github.com/pingcap/tidb/pull/5107)
- [Optimize the query cost estimation](https://github.com/pingcap/tidb/pull/5140)
- [Fix the index prefix issue when creating tables](https://github.com/pingcap/tidb/pull/5149)
- [Support pushing down the expressions for the Float type to TiKV](https://github.com/pingcap/tidb/pull/5153)
- [Fix the issue that it is slow to add index for tables with discrete integer primary index](https://github.com/pingcap/tidb/pull/5155)
- [Reduce the unnecessary statistics updates](https://github.com/pingcap/tidb/pull/5164)
- [Fix a potential issue during the transaction retry](https://github.com/pingcap/tidb/pull/5219)

## PD

- Support adding more types of schedulers using API

## TiKV

- Fix the deadlock issue with the PD client
- Fix the issue that the wrong leader value is prompted for `NotLeader`
- Fix the issue that the chunk size is too large in the coprocessor

To upgrade from 1.0.2 to 1.0.3, follow the rolling upgrade order of PD -> TiKV -> TiDB.
