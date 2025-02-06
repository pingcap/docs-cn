---
title: TiDB 3.0.13 Release Notes
aliases: ['/docs-cn/dev/releases/release-3.0.13/','/docs-cn/dev/releases/3.0.13/']
summary: TiDB 3.0.13 发布日期为 2020 年 04 月 22 日。此版本修复了 TiDB 和 TiKV 中的一些 bug。其中 TiDB 修复了由于未检查 `MemBuffer`，事务内执行 `INSERT ... ON DUPLICATE KEY UPDATE` 语句插入多行重复数据可能出错的问题。TiKV 修复了重复多次执行 `Region Merge` 导致系统被阻塞的问题，阻塞期间服务不可用。
---

# TiDB 3.0.13 Release Notes

发版日期：2020 年 04 月 22 日

TiDB 版本：3.0.13

## Bug 修复

+ TiDB

    - 修复由于未检查 `MemBuffer`，事务内执行 `INSERT ... ON DUPLICATE KEY UPDATE` 语句插入多行重复数据可能出错的问题 [#16690](https://github.com/pingcap/tidb/pull/16690)

+ TiKV

    - 修复重复多次执行 `Region Merge` 导致系统被阻塞的问题，阻塞期间服务不可用 [#7612](https://github.com/tikv/tikv/pull/7612)
