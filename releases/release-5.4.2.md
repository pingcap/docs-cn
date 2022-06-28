---
title: TiDB 5.4.2 Release Notes
---

# TiDB 5.4.2 Release Notes

发版日期：2022 年 x 月 x 日

TiDB 版本：5.4.2

## 兼容性更改

## 提升改进

## Bug 修复

+ PingCAP/TiFlash
    <!--compute-->
    - 修复因为溢出导致的 Decimal 比较结果错误. [#4512](https://github.com/pingcap/tiflash/issues/4512)
    
+ PD
    - 修复 `not leader` 的 gRPC 状态码 [#4797](https://github.com/tikv/pd/issues/4797)
    - 修复因为 region 没有 leader 而导致热点调度 panic 的问题 [#5005](https://github.com/tikv/pd/issues/5005)
    - 修复 PD leader 切换后无法立刻产生调度的问题 [#4769](https://github.com/tikv/pd/issues/4769)
    - 修复 TSO 在某些极端情况下会退的问题 [#4884](https://github.com/tikv/pd/issues/4884)

