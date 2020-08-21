---
title: TiDB 3.0.18 Release Notes
---

# TiDB 3.0.18 Release Notes

Release date: August 21, 2020

TiDB version: 3.0.18

## Improvements

+ Tools

    + TiDB Binlog

        - Support the time duration format of Go for the Pump GC configuration [#996](https://github.com/pingcap/tidb-binlog/pull/996)

## Bug Fixes

+ TiDB

    - Fix the issue that the wrong handling of the `decimal` type by the `Hash` function causes the wrong HashJoin result [#19185](https://github.com/pingcap/tidb/pull/19185)
    - Fix the issue that the wrong handling of the `set` and `enum` types by the `Hash` function causes the wrong HashJoin result [#19175](https://github.com/pingcap/tidb/pull/19175)
    - Fix the issue that the check for duplicate keys fails in the pessimistic locking mode [#19236](https://github.com/pingcap/tidb/pull/19236)
    - Fix the issue that the `Apply` and `Union Scan` operators cause the wrong execution result [#19297](https://github.com/pingcap/tidb/pull/19297)
    - Fix the issue that some cached execution plans are incorrectly executed in transaction [#19274](https://github.com/pingcap/tidb/pull/19274)

+ TiKV

    - Change the GC failure log from `error` to the `warning` level [#8444](https://github.com/tikv/tikv/pull/8444)

+ Tools

    + TiDB Lightning

        - Fix the issue that the `--log-file` argument does not take effect [#345](https://github.com/pingcap/tidb-lightning/pull/345)
        - Fix the syntax error on empty binary/hex literals when using TiDB-backend [#357](https://github.com/pingcap/tidb-lightning/pull/357)
        - Fix the unexpected `switch-mode` call when using TiDB-backend [#368](https://github.com/pingcap/tidb-lightning/pull/368)
