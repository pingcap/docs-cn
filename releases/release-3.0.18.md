---
title: TiDB 3.0.18 Release Notes
aliases: ['/docs-cn/dev/releases/release-3.0.18/']
---

# TiDB 3.0.18 Release Notes

发版日期：2020 年 8 月 21 日

TiDB 版本：3.0.18

## Bug 修复

+ TiDB

    - 修复 [#19185](https://github.com/pingcap/tidb/pull/19185)
    - 修复 [#19172](https://github.com/pingcap/tidb/pull/19172)

+ TiKV

    - 将 GC 的失败日志从 Error 级别改成 Warning 级别 [#8444](https://github.com/tikv/tikv/pull/8444)

+ TiDB Lightning

    - 修复 [#345](https://github.com/pingcap/tidb-lightning/pull/345)
    - 修复 [#357](https://github.com/pingcap/tidb-lightning/pull/357)
    - 修复 [#368](https://github.com/pingcap/tidb-lightning/pull/368)

## 优化

+ TiDB Binlog

    - 支持 [#996](https://github.com/pingcap/tidb-binlog/pull/996)