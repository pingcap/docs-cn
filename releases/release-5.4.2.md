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
    (dup: release-6.1.0.md > 改进提升> TiKV)- 健康检查可以检测到无法正常工作的 Raftstore，使得 TiKV client 可以及时更新 Region Cache [#12398](https://github.com/tikv/tikv/issues/12398)
    - Use `posix_fallocate` for space reservation. [#12543](https://github.com/tikv/tikv/issues/12543)
    (dup: release-5.2.4.md > 提升改进> TiKV)- 通过将 leader 转让给 CDC observer 减少延迟抖动 [#12111](https://github.com/tikv/tikv/issues/12111)

+ PD
    (dup: release-6.1.0.md > 改进提升> PD)- 默认关闭编译 swagger server [#4932](https://github.com/tikv/pd/issues/4932)

## Bug 修复

+ TiDB

    - 修复在网络断连时，断连的会话资源可能没有清理的问题。[#34722](https://github.com/pingcap/tidb/issues/34722)
    - 修复在查询包含 CTE 的视图时，可能误报 `references invalid table` 的问题。[#33965](https://github.com/pingcap/tidb/issues/33965)

+ TiKV

    - Fix the issue of unexpected `panic` on analyzed statistics when `max_sample_size` is set to `0`. [#11192](https://github.com/tikv/tikv/issues/11192)
    (dup: release-6.0.0-dmr.md > Bug 修复> TiKV)- 修复 TiKV 在退出时可能误报 panic 的问题 [#12231](https://github.com/tikv/tikv/issues/12231)
    - Fix possible panic when source peer catch up logs by snapshot in merge [#12663](https://github.com/tikv/tikv/issues/12663)
    - Fix potential panic when a peer is being split and destroyed at the same time [#12825](https://github.com/tikv/tikv/issues/12825)
    - Fix bug which causes frequent pd client reconnection [#12345](https://github.com/tikv/tikv/issues/12345)
    - Fix a wrong check in datetime when the datetime has a fraction and 'Z' [#12739](https://github.com/tikv/tikv/issues/12739)
    - Fix tikv crash when conv empty string [#12673](https://github.com/tikv/tikv/issues/12673)
    - Fix possible duplicate commit record in async-commit pessimistic transactions. [#12615](https://github.com/tikv/tikv/issues/12615)
    (dup: release-6.1.0.md > 错误修复> TiKV)- 修复进行 Follower Read 时，可能会报 `invalid store ID 0` 错误的问题 [#12478](https://github.com/tikv/tikv/issues/12478)
    (dup: release-6.1.0.md > 错误修复> TiKV)- 修复销毁 peer 和批量分裂 Region 之间的竞争导致的 TiKV panic [#12368](https://github.com/tikv/tikv/issues/12368)
    (dup: release-5.2.4.md > Bug 修复> TiKV)- 修复 tikv-ctl 对 `bad-ssts` 结果字符串进行错误匹配的问题 [#12329](https://github.com/tikv/tikv/issues/12329)

+ PD
    (dup: release-6.1.0.md > 错误修复> PD)- 修复 `not leader` 的 status code 有误的问题 [#4797](https://github.com/tikv/pd/issues/4797)
    - 修复因为 region 没有 leader 而导致热点调度 panic 的问题 [#5005](https://github.com/tikv/pd/issues/5005)
    (dup: release-6.1.0.md > 错误修复> PD)- 修复 PD leader 转移后调度不能立即启动的问题 [4769](https://github.com/tikv/pd/issues/4769)
    (dup: release-6.1.0.md > 错误修复> PD)- 修复在某些特殊情况下 TSO fallback 的问题 [#4884](https://github.com/tikv/pd/issues/4884)

+ PingCAP/TiFlash
    <!--compute-->
    - 修复因为溢出导致的 Decimal 比较结果错误. [#4512](https://github.com/pingcap/tiflash/issues/4512)
