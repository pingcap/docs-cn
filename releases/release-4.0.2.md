---
title: TiDB 4.0.2 Release Notes
category: Releases
---

# TiDB 4.0.2 Release Notes

发版日期：2020 年 6 月 30 日

TiDB 版本：4.0.2

## 兼容性

+ TiFlash
    - 提升从旧版本升级时的兼容性. [#786](https://github.com/pingcap/tics/pull/786)

## 新功能

+ TiDB



+ TiKV



+ PD



+ TiFlash
    - Coprocessor 支持新的聚合函数 `APPROX_COUNT_DISTINCT`. [#798](https://github.com/pingcap/tics/pull/798)
    - 存储引擎中的粗糙索引默认开启. [#777](https://github.com/pingcap/tics/pull/777)
    - 支持运行在 ARM 架构. [#769](https://github.com/pingcap/tics/pull/769)
    - 降低 delta index 的内存使用量. [#787](https://github.com/pingcap/tics/pull/787)
    - 使用更高效的 delta index update 算法. [#794](https://github.com/pingcap/tics/pull/794)
    - Coprocessor 支持 `JSON_LENGTH` 函数下推. [#742](https://github.com/pingcap/tics/pull/742)


+ Tools



## Bug 修复

+ TiDB



+ TiKV



+ PD



+ TiFlash
    - 修正 proxy 遇到 region not found 时可能的 panic 的问题. [#807](https://github.com/pingcap/tics/pull/807)
    - 修正 schema 同步遇到 I/O exception 时可能无法继续同步的问题. [#791](https://github.com/pingcap/tics/pull/791)


+ Tools
