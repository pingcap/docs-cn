---
title: TiDB 5.4.2 Release Notes
---

# TiDB 5.4.2 Release Notes

发版日期：2022 年 x 月 x 日

TiDB 版本：5.4.2

## 兼容性更改

## 提升改进

+ TiKV

    - Reload TLS certificate automatically when it changes. [#12546](https://github.com/tikv/tikv/issues/12546)
    - Improve the health check to detect unavailable Raftstore, so that the TiKV client can update Region Cache in time [#12398](https://github.com/tikv/tikv/issues/12398)
    - Use `posix_fallocate` for space reservation. [#12543](https://github.com/tikv/tikv/issues/12543)
    - Transfer the leadership to CDC observer to reduce latency jitter [#12111](https://github.com/tikv/tikv/issues/12111)

+ PD
    - 默认关闭编译 swagger server [#4932](https://github.com/tikv/pd/issues/4932)

## Bug 修复

+ TiKV

    - Fix the issue of unexpected `panic` on analyzed statistics when `max_sample_size` is set to `0`. [#11192](https://github.com/tikv/tikv/issues/11192)
    - Fix the potential issue of mistakenly reporting TiKV panics when exiting TiKV [#12231](https://github.com/tikv/tikv/issues/12231)
    - Fix possible panic when source peer catch up logs by snapshot in merge [#12663](https://github.com/tikv/tikv/issues/12663)
    - Fix potential panic when a peer is being split and destroyed at the same time [#12825](https://github.com/tikv/tikv/issues/12825)
    - Fix bug which causes frequent pd client reconnection [#12345](https://github.com/tikv/tikv/issues/12345)
    - Fix a wrong check in datetime when the datetime has a fraction and 'Z' [#12739](https://github.com/tikv/tikv/issues/12739)
    - Fix tikv crash when conv empty string [#12673](https://github.com/tikv/tikv/issues/12673)
    - Fix possible duplicate commit record in async-commit pessimistic transactions. [#12615](https://github.com/tikv/tikv/issues/12615)
    - Fix the issue that TiKV reports the `invalid store ID 0` error when using Follower Read [#12478](https://github.com/tikv/tikv/issues/12478)
    - Fix the issue of TiKV panic caused by the race between destroying peers and batch splitting Regions [#12368](https://github.com/tikv/tikv/issues/12368)
    - Fix the issue that tikv-ctl returns an incorrect result due to its wrong string match [#12329](https://github.com/tikv/tikv/issues/12329)

+ PD
    - 修复 `not leader` 的 gRPC 状态码 [#4797](https://github.com/tikv/pd/issues/4797)
    - 修复因为 region 没有 leader 而导致热点调度 panic 的问题 [#5005](https://github.com/tikv/pd/issues/5005)
    - 修复 PD leader 切换后无法立刻产生调度的问题 [#4769](https://github.com/tikv/pd/issues/4769)
    - 修复 TSO 在某些极端情况下会退的问题 [#4884](https://github.com/tikv/pd/issues/4884)

+ PingCAP/TiFlash
    <!--compute-->
    - 修复因为溢出导致的 Decimal 比较结果错误. [#4512](https://github.com/pingcap/tiflash/issues/4512)
