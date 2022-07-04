---
title: TiDB 5.4.2 Release Notes
---

# TiDB 5.4.2 Release Notes

发版日期：2022 年 x 月 x 日

TiDB 版本：5.4.2

## 兼容性更改

## 提升改进

+ TiKV

    - 当 TLS 证书更新时自动重新加载 [#12546](https://github.com/tikv/tikv/issues/12546)
    (dup: release-6.1.0.md > 改进提升> TiKV)- 健康检查可以检测到无法正常工作的 Raftstore，使得 TiKV client 可以及时更新 Region Cache [#12398](https://github.com/tikv/tikv/issues/12398)
    (dup: release-5.2.4.md > 提升改进> TiKV)- 通过将 leader 转让给 CDC observer 减少延迟抖动 [#12111](https://github.com/tikv/tikv/issues/12111)

+ PD
    (dup: release-6.1.0.md > 改进提升> PD)- 默认关闭编译 swagger server [#4932](https://github.com/tikv/pd/issues/4932)

## Bug 修复

+ TiDB

    <!--planner-->
    - 修复在 binary protocol 下 Plan Cache 有时会缓存错误的 TableDual 计划的问题。[#34690] (https://github.com/pingcap/tidb/issues/34690) [#34678] (https://github.com/pingcap/tidb/issues/34678)
    - 修复了执行计划在 EqualAll 的情况下，把 TiFlash 的 firstrow agg func 的 null flag 设错的问题。[#34584](https://github.com/pingcap/tidb/issues/34584)
    - 修复了执行计划在 TiFlash 下 aggregate 下推过 join 时，两阶段 aggregate 处理错误的问题。[#34682](https://github.com/pingcap/tidb/issues/34682)
    - 修复了执行计划在 aggregate 下推过 outer join 时，final aggregate 的 null flag 被设错的问题。[#34465](https://github.com/pingcap/tidb/issues/34465)
    - 修复了 Plan Cache 在 evict 时使用了错误的 memory usage 指标的问题。[#34613](https://github.com/pingcap/tidb/issues/34613)

    <!--transaction-->
    - 通过不向非健康状态的 TiKV 发送请求提升可用性 [#34609](https://github.com/pingcap/tidb/pull/34609) 
    - 避免在悲观事务中报出 Write Conflict 错误 [#11612](https://github.com/tikv/tikv/issues/11612)
    - 修复了在遇到 region error 和网络问题时 prewrite 请求不幂等的问题[#34875](https://github.com/pingcap/tidb/issues/34875)
    - 修复了回滚 async commit 事务可能导致事务不满足原子性的问题 [#33641](https://github.com/pingcap/tidb/issues/33641)
    <!--sql-infra-->
    - 修复在网络断连时，断连的会话资源可能没有清理的问题。[#34722](https://github.com/pingcap/tidb/issues/34722)
    - 修复在查询包含 CTE 的视图时，可能误报 `references invalid table` 的问题。[#33965](https://github.com/pingcap/tidb/issues/33965)

    <!--diagnosis-->
    - 修复在 SQL 语句分析中并发读写 map 的问题。[#35340](https://github.com/pingcap/tidb/issues/35340)

+ TiKV

    - 修复 `max_sample_size` 为 `0` 时 analyze 可能导致 panic 的问题 [#11192](https://github.com/tikv/tikv/issues/11192)
    (dup: release-6.0.0-dmr.md > Bug 修复> TiKV)- 修复 TiKV 在退出时可能误报 panic 的问题 [#12231](https://github.com/tikv/tikv/issues/12231)
    - 修复 merge source peer 通过 snapshot 追日志时可能导致 panic 的问题 [#12663](https://github.com/tikv/tikv/issues/12663)
    - 修复一个 peer 同时进行 split 和 destroy 时可能导致 panic 的问题 [#12825](https://github.com/tikv/tikv/issues/12825)
    - 修复 pd client 可能频繁重连的问题 [#12345](https://github.com/tikv/tikv/issues/12345)
    - 修复查询 datatime 中包含小数以及 'Z' 时误报格式错误的问题 [#12739](https://github.com/tikv/tikv/issues/12739)
    - 修复查询中 conv 有空字符串时 panic 的问题 [#12673](https://github.com/tikv/tikv/issues/12673)
    - 修复 async commit 悲观事务中可能导致有重复的 commit record 的问题 [#12615](https://github.com/tikv/tikv/issues/12615)
    (dup: release-6.1.0.md > 错误修复> TiKV)- 修复进行 Follower Read 时，可能会报 `invalid store ID 0` 错误的问题 [#12478](https://github.com/tikv/tikv/issues/12478)
    (dup: release-6.1.0.md > 错误修复> TiKV)- 修复销毁 peer 和批量分裂 Region 之间的竞争导致的 TiKV panic [#12368](https://github.com/tikv/tikv/issues/12368)
    (dup: release-5.2.4.md > Bug 修复> TiKV)- 修复 tikv-ctl 对 `bad-ssts` 结果字符串进行错误匹配的问题 [#12329](https://github.com/tikv/tikv/issues/12329)
     - 修复在 aufs 文件系统上启动 TiKV 报错的问题 [#12543](https://github.com/tikv/tikv/issues/12543)


+ PD
    (dup: release-6.1.0.md > 错误修复> PD)- 修复 `not leader` 的 status code 有误的问题 [#4797](https://github.com/tikv/pd/issues/4797)
    - 修复由于 Hot Region 没有 leader 导致 PD Panic 的问题 [#5005](https://github.com/tikv/pd/issues/5005)
    (dup: release-6.1.0.md > 错误修复> PD)- 修复 PD leader 转移后调度不能立即启动的问题 [4769](https://github.com/tikv/pd/issues/4769)
    (dup: release-6.1.0.md > 错误修复> PD)- 修复在某些特殊情况下 TSO fallback 的问题 [#4884](https://github.com/tikv/pd/issues/4884)

+ PingCAP/TiFlash

    <!--storage-->
    - 修复在 clustered index 表删除列导致 TiFlash 进程退出的问题 [#5154](https://github.com/pingcap/tiflash/issues/5154)
    - 修复大量 INSERT 和 DELETE 操作后可能导致 TiFlash 数据不一致的问题 [#4956](https://github.com/pingcap/tiflash/issues/4956)
    <!--compute-->
    - 修复因为溢出导致的 Decimal 比较结果错误. [#4512](https://github.com/pingcap/tiflash/issues/4512)

+ Tools

  + TiCDC

    - 修复了一个特殊情况下增量扫可能造成数据丢失的问题 [#5468](https://github.com/pingcap/tiflow/issues/5468)
    - 修复了 cdc 可能在 redo 日志写完之前错误地刷盘的问题 [#5486](https://github.com/pingcap/tiflow/issues/5486)
    - 修复了 cdc 可能在 redo 日志写完之前过早推进 resolved ts 的问题 [#5486](https://github.com/pingcap/tiflow/issues/5486)
    - 为 redo 日志增加了基于 uuid 的后缀，以免潜在的名字冲突造成数据丢失 [#5486](https://github.com/pingcap/tiflow/issues/5486)
    - 修复了 Region Leader 丢失不断重试直到超过次数上限后同步中断的问题 [#5230](https://github.com/pingcap/tiflow/issues/5230)
    - 修复了 MySQL Sink 可能上报错误地 checkpoint 时间戳的问题 [#5107](https://github.com/pingcap/tiflow/issues/5107)
    - 修复了 http server 中潜在的 goroutine 泄露问题 [#5303](https://github.com/pingcap/tiflow/issues/5303)
