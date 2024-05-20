---
title: TiDB 5.0.5 Release Note
summary: TiDB 5.0.5 发布日期为 2021 年 12 月 3 日，修复了 TiKV 中的 `GcKeys` 任务被多个键调用时无法正常进行的问题。这可能导致 Compaction Filter GC 不删除 MVCC deletion 信息。详细信息请查看 issue #11217。
---

# TiDB 5.0.5 Release Note

发版日期：2021 年 12 月 3 日

TiDB 版本：5.0.5

## Bug 修复

+ TiKV

    - 修复 `GcKeys` 任务被多个键调用时无法正常进行，导致 Compaction Filter GC 可能不删除 MVCC deletion 信息的问题 [#11217](https://github.com/tikv/tikv/issues/11217)
