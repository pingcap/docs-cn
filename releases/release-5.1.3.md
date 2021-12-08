---
title: TiDB 5.1.3 Release Note
---

# TiDB 5.1.3 Release Note

发版日期：2021 年 12 月 3 日

TiDB 版本：5.1.3

## Bug 修复

+ TiKV

    - 修复 `GcKeys` 任务被多个键调用时无法正常进行，导致 Compaction Filter GC 可能不删除 MVCC deletion 信息的问题 [#11217](https://github.com/tikv/tikv/issues/11217)
