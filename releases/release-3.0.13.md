---
title: TiDB 3.0.13 Release Notes
---

# TiDB 3.0.13 Release Notes

发版日期：2020 年 04 月 22 日

TiDB 版本：3.0.13

## Bug 修复

+ TiDB

    - 修复由于未检查 `MemBuffer`，事务内执行 `INSERT ... ON DUPLICATE KEY UPDATE` 语句插入多行重复数据可能出错的问题 [#16690](https://github.com/pingcap/tidb/pull/16690)

+ TiKV

    - 修复重复多次执行 `Region Merge` 导致系统被阻塞的问题，阻塞期间服务不可用 [#7612](https://github.com/tikv/tikv/pull/7612)
