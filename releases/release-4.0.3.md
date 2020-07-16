---
title: TiDB 4.0.3 Release Notes
category: Releases
---

# TiDB 4.0.3 Release Notes

发版日期：2020 年 7 月 22 日

TiDB 版本：4.0.3

## 新功能

+ TiDB



+ TiKV



+ PD



+ TiFlash



+ Tools

    - Backup & Restore (BR)



    - Dumpling



+ TiCDC


## 改进提升

+ TiDB



+ TiKV

  - 添加了新的配置项 `backup.num-threads` 用语控制 backup 线程池的大小 [#8199](https://github.com/tikv/tikv/pull/8199)
  - 收取 snapshot 时不再发送 store heartbeat [#8136](https://github.com/tikv/tikv/pull/8136)
  - 支持动态调整 shared block cache 的大小 [#8232](https://github.com/tikv/tikv/pull/8232)

+ PD



+ TiFlash



+ Tools

     

## Bug 修复

+ TiDB



+ TiKV

  - 修复 merge 期间可能读到过期数据的问题 [#8113](https://github.com/tikv/tikv/pull/8113)
  - 修复聚合函数 min/max 下推到 TiKV 时，collation 不能正确工作的问题 [#8108](https://github.com/tikv/tikv/pull/8108)

+ PD



+ TiFlash



+ Tools


