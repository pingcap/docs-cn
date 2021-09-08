---
title: TiDB 5.2.1 Release Notes
---

# TiDB 5.2.1 Release Notes

发版日期：2021 年 9 月 x 日

TiDB 版本：5.2.1

## Bug 修复

+ TiDB

    - 修复在分区中下推聚合算子时，因浅拷贝 schema 列导致执行计划出错的问题 [#27839](https://github.com/pingcap/tidb/pull/27839)

+ TiKV

    - 修复 Region 迁移时 Raftstore 模块出现死锁的问题 [#10909](https://github.com/tikv/tikv/issues/10909)
