---
title: TiDB 2.0.8 Release Notes
category: Releases
aliases: ['/docs/releases/208/']
---

# TiDB 2.0.8 Release Notes

On October 16, 2018, TiDB 2.0.8 is released. Compared with TiDB 2.0.7, this release has great improvement in system compatibility and stability.

## TiDB

+ Improvement
    - Slow down the AUTO-ID increasing speed when the `Update` statement does not modify the corresponding AUTO-INCREMENT column [#7846](https://github.com/pingcap/tidb/pull/7846)
+ Bug fixes
    - Quickly create a new etcd session to recover the service when the PD leader goes down [#7810](https://github.com/pingcap/tidb/pull/7810)
    - Fix the issue that the time zone is not considered when the default value of the `DateTime` type is calculated [#7672](https://github.com/pingcap/tidb/pull/7672)
    - Fix the issue that `duplicate key update` inserts values incorrectly in some conditions [#7685](https://github.com/pingcap/tidb/pull/7685)
    - Fix the issue that the predicate conditions of `UnionScan` are not pushed down [#7726](https://github.com/pingcap/tidb/pull/7726)
    - Fix the issue that the time zone is not correctly handled when you add the `TIMESTAMP` index [#7812](https://github.com/pingcap/tidb/pull/7812)
    - Fix the memory leak issue caused by the statistics module in some conditions [#7864](https://github.com/pingcap/tidb/pull/7864)
    - Fix the issue that the results of `ANALYZE` cannot be obtained in some abnormal conditions [#7871](https://github.com/pingcap/tidb/pull/7871)
    - Do not fold the function `SYSDATE`, to ensure the returned results are correct [#7894](https://github.com/pingcap/tidb/pull/7894)
    - Fix the `substring_index` panic issue in some conditions [#7896](https://github.com/pingcap/tidb/pull/7896)
    - Fix the issue that `OUTER JOIN` is mistakenly converted to `INNER JOIN` in some conditions [#7899](https://github.com/pingcap/tidb/pull/7899)

## TiKV

+ Bug fix
    - Fix the issue that the memory consumed by Raftstore `EntryCache` keeps increasing when a node goes down [#3529](https://github.com/tikv/tikv/pull/3529)
