---
title: TiDB 6.1.1 Release Notes
---

# TiDB 6.1.1 Release Notes

发版日期：2022 年 x 月 x 日

TiDB 版本：6.1.1

## 兼容性变更

+ TiDB

    (dup: release-6.2.0.md > Bug fixes> TiDB)- 修复了 `SHOW DATABASES LIKE …` 大小写敏感的问题 [#34766](https://github.com/pingcap/tidb/issues/34766)
    - [tidb_enable_outer_join_reorder](https://github.com/system-variables.md#tidb_enable_outer_join_reorder-new-in-v610) 从 6.1.0 的默认 ON 变为默认 OFF。

+ Diagnosis

    - Continuous Profiling 现在默认被关闭。

## 提升改进

- 在 `TiDB-community-toolkit` 二进制包中新增了一些内容，详情参见 [TiDB 离线包](/binary-package.md)。
- Add a document to introduce TiDB's support for different operating systems. See [].
- 新增 TiDB 对不同操作系统支持的说明文档，见

+ TiDB

    <!-- <planner> -->
    (dup: release-6.2.0.md > # Performance) - 引入新的优化器提示 `SEMI_JOIN_REWRITE` 改善 `EXISTS` 查询性能 [#35323](https://github.com/pingcap/tidb/issues/35323)
    (dup: release-5.2.4.md > Bug fixes> TiDB)- 修复某些情况下分区表无法充分利用索引来扫描数据的问题 [#33966](https://github.com/pingcap/tidb/issues/33966)

    <!-- <transaction> -->
    (dup: release-6.2.0.md > Bug fixes> TiDB)- 避免向非健康状态的 TiKV 节点发送请求，以提升可用性 [#34906](https://github.com/pingcap/tidb/issues/34906)

+ TiKV

    (dup: release-6.2.0.md > Improvements> TiKV)- 支持通过 gzip 压缩 metrics 响应减少 HTTP body 大小 [#12355](https://github.com/tikv/tikv/issues/12355)
    - 支持过滤不常用 metrics 以减少流量 [#12698](https://github.com/tikv/tikv/issues/12698)
    (dup: release-6.2.0.md > Improvements> TiKV)- 支持动态调整 RocksDB 进行 subcompaction 的并发个数 (`rocksdb.max-sub-compactions`) [#13145](https://github.com/tikv/tikv/issues/13145)

+ PD

    - 改进 balance region 在空间快均衡阶段的调度速度 [#5320](https://github.com/tikv/pd/pull/5320)

+ Tools

    + TiDB Lightning

        - 针对 Stale Command 增加自动重试机制，提升导入成功率 [#36877](https://github.com/pingcap/tidb/issues/36877)

    + TiDB Data Migration

        - 用户可手动设置 Lightning Loader 并发数 [#5505](https://github.com/pingcap/tiflow/issues/5505)

    + TiCDC

        - 在 changefeed 的配置中增加参数来控制是否拆分大事务。 [#5231](https://github.com/pingcap/tiflow/issues/5231)
        (dup: release-6.2.0.md > 改进提升> Tools> TiCDC)- 优化了多 Region 场景下，runtime 上下文切换带来过多性能开销的问题 [#5610](https://github.com/pingcap/tiflow/issues/5610)
        - 优化 mysql sink 自动关闭 safe mode 的方式。[#5611](https://github.com/pingcap/tiflow/issues/5611)

## Bug 修复

+ TiDB

    <!-- <execution> -->
    - Fix the issue that IndexLookupHashJoin may hangs when used with limit [#35638](https://github.com/pingcap/tidb/issues/35638)
    - Fix the issue that TiDB may panic during update stmt [#32311](https://github.com/pingcap/tidb/issues/32311)
    - Fix the bug that `show columns` may send cop request [#36496](https://github.com/pingcap/tidb/issues/36496)
    - Fix bug that `show warnings` may return `invalid memory address or nil pointer dereference` error [#31569](https://github.com/pingcap/tidb/issues/31569)
    - Fix bug that static partition prune may return wrong result for agg query if the table is empty [#35295](https://github.com/pingcap/tidb/issues/35295)

    <!-- <planner> -->
    - 修复了 join reorder 时会错误地下推 outer join condition 的问题 [#37238](https://github.com/pingcap/tidb/issues/37238)
    - 修复了 CTE 被引用多次时 schema hashcode 被错误复用导致的 cannot find column [#35404](https://github.com/pingcap/tidb/issues/35404)
    - 修复了某些 outer join 场景下 join reorder 错误导致的查询结果错误 [#36912] (https://github.com/pingcap/tidb/issues/36912)
    (dup: release-5.4.2.md > Bug 修复> TiDB)- 修复了执行计划在 EqualAll 的情况下，把 TiFlash 的 `firstrow` 聚合函数的 null flag 设错的问题 [#34584](https://github.com/pingcap/tidb/issues/34584)
    - 修复了当查询创建了带 ignore_plan_cache hint 的 binding 后，无法再使用 plan cache 的问题 [#34596](https://github.com/pingcap/tidb/issues/34596)
    - 修复了 hash-partition window 和 single-partition window 之间缺少 exchange 算子的问题 [#35990](https://github.com/pingcap/tidb/issues/35990)
    (dup: release-5.2.4.md > Bug 修复> TiDB)- 修复某些情况下分区表无法充分利用索引来扫描数据的问题 [#33966](https://github.com/pingcap/tidb/issues/33966)
    - 修复了在某些场景下错误地设置了 partial agg 的默认值导致结果错误的问题 [#35295](https://github.com/pingcap/tidb/issues/35295)

    <!-- <sql-infra> -->
    (dup: release-6.2.0.md > Bug fixes> TiDB)- 修复了在查询分区表中如果查询条件中有分区键且两者使用了不同的 COLLATE 时会错误的进行分区裁剪的问题 [#32749](https://github.com/pingcap/tidb/issues/32749)
    (dup: release-6.2.0.md > 错误修复> TiDB)- 修复了在查询分区表中如果查询条件中有分区键且两者使用了不同的 COLLATE 时会错误的进行分区裁剪的问题 [#32749](https://github.com/pingcap/tidb/issues/32749) @[mjonss](https://github.com/mjonss)
    - 修复当 TiDB 开启 Binlog 时，执行 `ALTER SEQUENCE` 会产生错误的元信息版本号，进而导致 Drainer 报错退出的问题 [#36276](https://github.com/pingcap/tidb/issues/36276)
    - 修复了在极端情况情况下，TiDB 在启动时可能进入错误状态的问题 [#36791](https://github.com/pingcap/tidb/issues/36791)
    - 修复了在 Dashboard 中查询涉及分区表的执行计划时，有可能产生 `UnkownPlanID` 的问题 [#35153](https://github.com/pingcap/tidb/issues/35153)

    <!-- <transaction> -->
    (dup: release-6.2.0.md > Bug fixes> TiDB)- 修复了 `LOAD DATA` 语句中列的列表不生效的问题 [#35198](https://github.com/pingcap/tidb/issues/35198) @[SpadeA-Tang](https://github.com/SpadeA-Tang)
    (dup: release-5.3.2.md > Bug Fixes> TiDB)- 修复开启 TiDB Binlog 后插入重复数据导致 data and columnID count not match 错误的问题 [#33608](https://github.com/pingcap/tidb/issues/33608)
    - 去除 `tidb_gc_life_time` 设置时间检查限制 [#35392](https://github.com/pingcap/tidb/issues/35392)
    - 修复空分隔符使用情况下，load data 出现死循环的问题 [#33298](https://github.com/pingcap/tidb/issues/33298)
    (dup: release-6.2.0.md > 错误修复> TiDB)- 避免向非健康状态的 TiKV 节点发送请求，以提升可用性 [#34906](https://github.com/pingcap/tidb/issues/34906)

+ TiKV

    - 修复 raftstore 线程过于繁忙时，可能会出现重叠 region 的问题 [#13160](https://github.com/tikv/tikv/issues/13160)
    (dup: release-6.2.0.md > Bug fixes> TiKV)- 修复 PD Region heartbeat 连接异常中断后未重新连接的问题 [#12934](https://github.com/tikv/tikv/issues/12934)
    (dup: release-5.3.2.md > Bug Fixes> TiKV)- 修复了对空字符串进行类型转换导致 TiKV panic 的问题 [#12673](https://github.com/tikv/tikv/issues/12673)
    (dup: release-6.2.0.md > Bug fixes> TiKV)- 修复了 TiKV 和 PD 配置文件中 Region size 不一致的问题 [#12518](https://github.com/tikv/tikv/issues/12518)
    (dup: release-6.2.0.md > Bug fixes> TiKV)- 修复了启用 Raft Engine 时未清理加密密钥的问题 [#12890](https://github.com/tikv/tikv/issues/12890)
    (dup: release-6.2.0.md > Bug fixes> TiKV)- 修复同时分裂和销毁一个 peer 时可能导致 panic 的问题 [#12825](https://github.com/tikv/tikv/issues/12825)
    (dup: release-6.2.0.md > Bug fixes> TiKV)- 修复在 Region merge 时 source peer 通过 snapshot 追日志时可能导致 panic 的问题 [#12663](https://github.com/tikv/tikv/issues/12663)
    (dup: release-5.3.2.md > Bug Fixes> TiKV)- Fix the issue of frequent PD client reconnection that occurs when the PD client meets an error [#12345](https://github.com/tikv/tikv/issues/12345)
    - 修复开启 raft engine 以后，加密密钥不会被清理的问题 [#13123](https://github.com/tikv/tikv/issues/13123)
    (dup: release-6.2.0.md > Bug fixes> TiKV)- 修复了新创建的 Region Commit Log Duration 较高导致 QPS 下降的问题 [#13077](https://github.com/tikv/tikv/issues/13077)
    - 修复开启 raft-engine 后特殊情况下会 panic 的问题 [#12698](https://github.com/tikv/tikv/issues/12698)
    - 修复找不到 procfs 时无用警告级别日志过多的的问题 [#13116](https://github.com/tikv/tikv/issues/13116)
    - 修复 dashboard 中 "Unified Read Pool CPU" 表达式错误的问题 [#13086](https://github.com/tikv/tikv/issues/13086)
    - 修复默认 region-split-check-diff 可能会大于 bucket 大小的问题 [#12598](https://github.com/tikv/tikv/issues/12598)
    - 修复开启 raft engine 以后，中止 apply snapshot 时可能会 panic 的问题 [#12470](https://github.com/tikv/tikv/issues/12470)
    - 修复 pd client 可能会死锁的问题 [#13191](https://github.com/tikv/tikv/issues/13191) [#12933](https://github.com/tikv/tikv/issues/12933)

+ PD

    - 修复在有异常标记的节点的集群里面，上下线进度评估不工作的问题 [#5234](https://github.com/tikv/pd/issues/5234)
    - 修复 gRPC 处理返回错误不恰当的问题 [#5373](https://github.com/tikv/pd/issues/5373)
    - 修复`/regions/replicated` 返回错误状态的问题 [#5095](https://github.com/tikv/pd/issues/5095)

+ TiFlash

    (dup: release-5.4.2.md > Bug Fixes> TiFlash)- 修复在 clustered index 表删除列导致 TiFlash 崩溃的问题 [#5154](https://github.com/pingcap/tiflash/issues/5154)
    - Fix the issue that format throw data truncated error [#4891](https://github.com/pingcap/tiflash/issues/4891)
    - fix the problem that there may be some obsolete data left in storage which cannot be deleted [#5659](https://github.com/pingcap/tiflash/issues/5659)
    - Reduce unnecessary CPU usage in some edge cases [#5409](https://github.com/pingcap/tiflash/issues/5409)
    - Fix a bug that TiFlash can not work in a cluster using ipv6 [#5247](https://github.com/pingcap/tiflash/issues/5247)
    - Fix a panic issue in parallel aggregation when an exception is thrown. [#5356](https://github.com/pingcap/tiflash/issues/5356)

+ Tools

    + TiCDC

        - 修复版本兼容性问题 [#6039](https://github.com/pingcap/tiflow/issues/6039)
        - 修复cdc server 启动未完成接受请求出现 panic 问题 [#5639](https://github.com/pingcap/tiflow/issues/5639)
        - 修复 sync-point 打开时 ddl sink 可能出现 panic 的问题. [#4934](https://github.com/pingcap/tiflow/issues/4934)
        - 修复 cdc server 重启时 API 工作不正常的问题. [#5837](https://github.com/pingcap/tiflow/issues/5837)
        - 修复 black hole sink 场景下出现的 data race 问题. [#6206](https://github.com/pingcap/tiflow/issues/6206)
        - 修复disable old value 时可能出现的 cdc panic 问题 。 [#6198](https://github.com/pingcap/tiflow/issues/6198)
        - 修复在打开 redo 功能时，可能出现的一些数据不一致问题。[#6189](https://github.com/pingcap/tiflow/issues/6189) [#6368](https://github.com/pingcap/tiflow/issues/6368) [#6277](https://github.com/pingcap/tiflow/issues/6277) [#6456](https://github.com/pingcap/tiflow/issues/6456) [#6695](https://github.com/pingcap/tiflow/issues/6695) [#6764](https://github.com/pingcap/tiflow/issues/6764) [#6859](https://github.com/pingcap/tiflow/issues/6859)
        - 采取异步写的方式提升 Redo 吞吐。 [#6011](https://github.com/pingcap/tiflow/issues/6011)
        -修复打开 sync-point 功能在某些特殊场景下出现卡住 changefeed 的问题 。 [#6827](https://github.com/pingcap/tiflow/issues/6827)
        - 修复 mysql sink 链接 ipv6 的问题。[#6135](https://github.com/pingcap/tiflow/issues/6135)

    + Backup & Restore (BR)

        (dup: release-5.4.2.md > Bug Fixes> Tools> Backup & Restore (BR))- 修复了 RawKV 模式下 BR 报 `ErrRestoreTableIDMismatch` 错误的问题 [#35279](https://github.com/pingcap/tidb/issues/35279)
        (dup: release-6.2.0.md > 改进提升> Tools> Backup & Restore (BR))- 优化了全量备份数据组织形式，解决大规模集群备份时遇到的 S3 限流问题 [#30087](https://github.com/pingcap/tidb/issues/30087)
        - 修复日志中统计备份耗时不正确的问题 [#35553](https://github.com/pingcap/tidb/issues/35553)

    + Dumpling

        - 使用 net.JoinHostPort 拼接 Host、Port，提供更好的 IPv6 兼容 [#36112](https://github.com/pingcap/tidb/issues/36112)

    + TiDB Lightning

        - 修复 IPv6 支持 [#35880](https://github.com/pingcap/tidb/issues/35880)
        - 修复 read index not ready 问题，增加重试机制 [#36566](https://github.com/pingcap/tidb/issues/36566)
        - 移除日志中的敏感信息 [#36374](https://github.com/pingcap/tidb/issues/36374) 
        - 支持 Parquet 格式带`_`的特殊列名[#36980](https://github.com/pingcap/tidb/issues/36980)
        - 修复极端情况下重复去重可能会 panic 的问题 [#36163](https://github.com/pingcap/tidb/issues/34163)

    + TiDB Binlog

        - [#1152](https://github.com/pingcap/tidb-binlog/issues/1152)

    + TiDB Data Migration

        - 修复 `txn-entry-size-limit` 在 DM 不生效的问题 [#6161](https://github.com/pingcap/tiflow/issues/6161)
        - 修复 `check-task` 不能处理特殊编码的问题 [#5895](https://github.com/pingcap/tiflow/issues/5895)
        - 修复乐观模式下频繁重启 Master/Worker 会导致同步数据失败的问题 [#5489](https://github.com/pingcap/tiflow/issues/5489)
        - 修复 `query-status` 内 data race 问题 [#4811](https://github.com/pingcap/tiflow/issues/4811)
        - 修复 `operate-schema` 显示不一致问题 [#5688](https://github.com/pingcap/tiflow/issues/5688)
        - 修复 relay 报错时可能导致 goroutine 泄露问题 [#6193](https://github.com/pingcap/tiflow/issues/6193)
        - 修复 DM Worker 因 DB Conn 获取 可能 Stuck 的问题 [#6193](https://github.com/pingcap/tiflow/issues/6193)
        - 修复 DM IPv6 支持问题 [#6249](https://github.com/pingcap/tiflow/issues/6249)
        - 修复 invalid table ID 问题 [6526](https://github.com/pingcap/tiflow/issues/6526)
