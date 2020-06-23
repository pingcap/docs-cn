---
title: TiDB 4.0.2 Release Notes
category: Releases
---

# TiDB 4.0.2 Release Notes

发版日期：2020 年 6 月 30 日

TiDB 版本：4.0.2

## 兼容性

+ TiFlash
    - Improve backward compatibility when upgrading from the older version. [#786](https://github.com/pingcap/tics/pull/786)

## 新功能

+ TiDB



+ TiKV



+ PD



+ TiFlash
    - Support new aggregation function `APPROX_COUNT_DISTINCT` in Coprocessor. [#798](https://github.com/pingcap/tics/pull/798)
    - Enable rough set filter feature by default. [#777](https://github.com/pingcap/tics/pull/777)
    - Enable TiFlash running on ARM architecture. [#769](https://github.com/pingcap/tics/pull/769)
    - Reduce memory consumption of delta index. [#787](https://github.com/pingcap/tics/pull/787)
    - Use more efficient update algorithm for delta index. [#794](https://github.com/pingcap/tics/pull/794)
    - Support function `JSON_LENGTH` in Coprocessor. [#742](https://github.com/pingcap/tics/pull/742)


+ Tools



## Bug 修复

+ TiDB



+ TiKV



+ PD



+ TiFlash
    - Fix the issue that proxy may panic when meet region not found [#807](https://github.com/pingcap/tics/pull/807)
    - Fix the issue that I/O exception thrown in drop table may lead to TiFlash schema sync failure. [#791](https://github.com/pingcap/tics/pull/791)


+ Tools
