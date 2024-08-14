---
title: TiDB 5.2.1 Release Notes
summary: TiDB 5.2.1 发布日期为 2021 年 9 月 9 日。此版本修复了 TiDB 在分区中下推聚合算子时的执行计划和执行报错问题。同时，TiKV 修复了 Region 迁移时出现的死锁导致 TiKV 不可用的问题。用户可通过关闭调度并重启出问题的 TiKV 来临时应对。
---

# TiDB 5.2.1 Release Notes

发版日期：2021 年 9 月 9 日

TiDB 版本：5.2.1

## Bug 修复

+ TiDB

    - 修复在分区中下推聚合算子时，因浅拷贝 schema 列导致执行计划出错，进而导致执行时报错的问题 [#27797](https://github.com/pingcap/tidb/issues/27797) [#26554](https://github.com/pingcap/tidb/issues/26554)

+ TiKV

    - 修复 Region 迁移时 Raftstore 模块出现死锁导致 TiKV 不可用的问题。用户可通过关闭调度并重启出问题的 TiKV 来临时应对。[#10909](https://github.com/tikv/tikv/issues/10909)
