---
title: TiDB 5.4.2 Release Notes
summary: TiDB 5.4.2 发布日期为 2022 年 7 月 8 日。该版本存在 bug，建议升级至 v5.4.3。此版本提升了 TiDB、TiKV、PD 和 Tools 的稳定性和可用性，并修复了多个 bug。
---

# TiDB 5.4.2 Release Notes

发版日期：2022 年 7 月 8 日

TiDB 版本：5.4.2

> **警告：**
>
> 不建议使用 v5.4.2，因为该版本已知存在 bug，详情参见 [#12934](https://github.com/tikv/tikv/issues/12934)。该 bug 已在 v5.4.3 中修复，建议升级至 [v5.4.3](/releases/release-5.4.3.md)。

## 提升改进

+ TiDB

    - 避免向非健康状态的 TiKV 节点发送请求，以提升可用性 [#34906](https://github.com/pingcap/tidb/issues/34906)

+ TiKV

    - 当 TLS 证书更新时自动重新加载，以提升可用性 [#12546](https://github.com/tikv/tikv/issues/12546)
    - 健康检查可以检测到无法正常工作的 Raftstore，使得 TiKV client 可以及时更新 Region Cache [#12398](https://github.com/tikv/tikv/issues/12398)
    - 通过将 leader 转让给 CDC observer 减少延迟抖动 [#12111](https://github.com/tikv/tikv/issues/12111)

+ PD

    - 默认关闭编译 swagger server [#4932](https://github.com/tikv/pd/issues/4932)

+ Tools

    + TiDB Lightning

        - 优化 Scatter Region 为批量模式，提升 Scatter Region 过程的稳定性 [#33618](https://github.com/pingcap/tidb/issues/33618)

## Bug 修复

+ TiDB

    - 修复在 binary protocol 下 Plan Cache 有时会缓存错误的 TableDual 计划的问题 [#34690](https://github.com/pingcap/tidb/issues/34690) [#34678](https://github.com/pingcap/tidb/issues/34678)
    - 修复了执行计划在 EqualAll 的情况下，把 TiFlash 的 `firstrow` 聚合函数的 null flag 设错的问题 [#34584](https://github.com/pingcap/tidb/issues/34584)
    - 修复了执行处理器为 TiFlash 生成错误的两阶段 aggregate 计划的问题 [#34682](https://github.com/pingcap/tidb/issues/34682)
    - 修复了 `tidb_opt_agg_push_down` 和 `tidb_enforce_mpp` 启用时执行处理器的错误行为 [#34465](https://github.com/pingcap/tidb/issues/34465)
    - 修复了 Plan Cache 在被 evict 时使用了错误的 memory usage 指标的问题 [#34613](https://github.com/pingcap/tidb/issues/34613)
    - 修复了 `LOAD DATA` 语句中列的列表不生效的问题 [#35198](https://github.com/pingcap/tidb/issues/35198)
    - 避免在悲观事务中报出 `Write Conflict` 错误 [#11612](https://github.com/tikv/tikv/issues/11612)
    - 修复了在遇到 Region error 和网络问题时 prewrite 请求不幂等的问题 [#34875](https://github.com/pingcap/tidb/issues/34875)
    - 修复了回滚 async commit 事务可能导致事务不满足原子性的问题 [#33641](https://github.com/pingcap/tidb/issues/33641)
    - 如果发生网络连接问题，TiDB 并不总是能正确释放已断开会话所占有的资源。该修复可以确保 TiDB 回滚打开的事务以及释放其他相关资源。[#34722](https://github.com/pingcap/tidb/issues/34722)
    - 修复在查询包含 CTE 的视图时，可能误报 `references invalid table` 的问题 [#33965](https://github.com/pingcap/tidb/issues/33965)
    - 修复 TiDB 由于 `fatal error: concurrent map read and map write` 发生崩溃的问题 [#35340](https://github.com/pingcap/tidb/issues/35340)

+ TiKV

    - 修复 `max_sample_size` 为 `0` 时 ANALYZE 可能导致 panic 的问题 [#11192](https://github.com/tikv/tikv/issues/11192)
    - 修复 TiKV 在退出时可能误报 panic 的问题 [#12231](https://github.com/tikv/tikv/issues/12231)
    - 修复在 Region merge 时 source peer 通过 snapshot 追日志时可能导致 panic 的问题 [#12663](https://github.com/tikv/tikv/issues/12663)
    - 修复同时分裂和销毁一个 peer 时可能导致 panic 的问题 [#12825](https://github.com/tikv/tikv/issues/12825)
    - 修复了 PD 客户端遇到报错时频繁重连的问题 [#12345](https://github.com/tikv/tikv/issues/12345)
    - 修复了 `DATETIME` 类型的数据包含小数部分和 `Z` 后缀导致检查报错的问题 [#12739](https://github.com/tikv/tikv/issues/12739)
    - 修复了对空字符串进行类型转换导致 TiKV panic 的问题 [#12673](https://github.com/tikv/tikv/issues/12673)
    - 修复了在悲观事务中使用 Async Commit 导致重复提交记录的问题 [#12615](https://github.com/tikv/tikv/issues/12615)
    - 修复进行 Follower Read 时，可能会报 `invalid store ID 0` 错误的问题 [#12478](https://github.com/tikv/tikv/issues/12478)
    - 修复销毁 peer 和批量分裂 Region 之间的竞争导致的 TiKV panic [#12368](https://github.com/tikv/tikv/issues/12368)
    - 修复 tikv-ctl 对 `bad-ssts` 结果字符串进行错误匹配的问题 [#12329](https://github.com/tikv/tikv/issues/12329)
    - 修复在 aufs 上启动 TiKV 报错的问题 [#12543](https://github.com/tikv/tikv/issues/12543)

+ PD
    - 修复 `not leader` 的 status code 有误的问题 [#4797](https://github.com/tikv/pd/issues/4797)
    - 修复由于 Hot Region 没有 leader 导致 PD Panic 的问题 [#5005](https://github.com/tikv/pd/issues/5005)
    - 修复 PD leader 转移后调度不能立即启动的问题 [#4769](https://github.com/tikv/pd/issues/4769)
    - 修复在某些特殊情况下 TSO fallback 的问题 [#4884](https://github.com/tikv/pd/issues/4884)

+ TiFlash

    - 修复在 clustered index 表删除列导致 TiFlash 崩溃的问题 [#5154](https://github.com/pingcap/tiflash/issues/5154)
    - 修复大量 INSERT 和 DELETE 操作后可能导致 TiFlash 数据不一致的问题 [#4956](https://github.com/pingcap/tiflash/issues/4956)
    - 修复极端情况下 decimal 比较结果可能有误的问题 [#4512](https://github.com/pingcap/tiflash/issues/4512)

+ Tools

    + Backup & Restore (BR)

        - 修复了 RawKV 模式下 BR 报 `ErrRestoreTableIDMismatch` 错误的问题 [#35279](https://github.com/pingcap/tidb/issues/35279)
        - 修复了出现保存文件错误时 BR 没有重试的问题 [#34865](https://github.com/pingcap/tidb/issues/34865)
        - 修复了 BR 运行时 panic 的问题 [#34956](https://github.com/pingcap/tidb/issues/34956)
        - 修复 BR 无法处理 S3 内部错误的问题 [#34350](https://github.com/pingcap/tidb/issues/34350)
        - 修复了当恢复操作遇到一些无法恢复的错误时，BR 被卡住的问题 [#33200](https://github.com/pingcap/tidb/issues/33200)

    + TiCDC

        - 修复了增量扫描特殊场景下的数据丢失问题 [#5468](https://github.com/pingcap/tiflow/issues/5468)
        - 修复 redo log manager 提前 flush log 的问题 [#5486](https://github.com/pingcap/tiflow/issues/5486)
        - 修复当一部分表没有被 redo writer 管理时 resolved ts 提前推进的问题 [#5486](https://github.com/pingcap/tiflow/issues/5486)
        - 添加 UUID 作为 redo log file 的后缀以解决文件名冲突引起的数据丢失问题 [#5486](https://github.com/pingcap/tiflow/issues/5486)
        - 修复了 Region Leader 丢失时重试超过次数上限后同步中断的问题 [#5230](https://github.com/pingcap/tiflow/issues/5230)
        - 修复 MySQL Sink 可能会保存错误的 checkpointTs 的问题 [#5107](https://github.com/pingcap/tiflow/issues/5107)
        - 修复了 HTTP server 中潜在的 goroutine 泄露问题 [#5303](https://github.com/pingcap/tiflow/issues/5303)
        - 修复了元信息所在 Region 发生变化时可能导致延迟上升的问题 [#4756](https://github.com/pingcap/tiflow/issues/4756) [#4762](https://github.com/pingcap/tiflow/issues/4762)

    + TiDB Data Migration (DM)

        - 修复了任务自动恢复后 DM 会占用更大的磁盘空间的问题 [#5344](https://github.com/pingcap/tiflow/issues/5344)
        - 修复在未设置 `case-sensitive: true` 时无法同步大写表的问题 [#5255](https://github.com/pingcap/tiflow/issues/5255)
