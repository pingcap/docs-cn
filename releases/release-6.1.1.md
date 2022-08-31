---
title: TiDB 6.1.1 Release Notes
---

# TiDB 6.1.1 Release Notes

发版日期：2022 年 x 月 x 日

TiDB 版本：6.1.1

## 兼容性变更

+ TiDB

    (dup: release-6.2.0.md > Bug fixes> TiDB)- `SHOW DATABASES LIKE …` 语句不再大小写敏感 [#34766](https://github.com/pingcap/tidb/issues/34766)
    - 将 [`tidb_enable_outer_join_reorder`](/system-variables.md#tidb_enable_outer_join_reorder-new-in-v610) 的默认值由 `1` 改为 `0`，即默认关闭 Join Reorder 对外连接的支持。

+ Diagnosis

    - 默认关闭持续性能分析 (Continuous Profiling) 特性，以避免开启该特性后 TiFlash 可能会崩溃的问题，详情参见 [#5687](https://github.com/pingcap/tiflash/issues/5687)

## 其他变更

- 在 `TiDB-community-toolkit` 二进制包中新增了以下内容，详情参见 [TiDB 离线包](/binary-package.md)。

    - `server-{version}-linux-amd64.tar.gz`
    - `grafana-{version}-linux-amd64.tar.gz`
    - `alertmanager-{version}-linux-amd64.tar.gz`
    - `prometheus-{version}-linux-amd64.tar.gz`
    - `blackbox_exporter-{version}-linux-amd64.tar.gz`
    - `node_exporter-{version}-linux-amd64.tar.gz`

- 引入对不同操作系统或平台的差异化支持，见 []

## 提升改进

+ TiDB

    <!-- <planner> -->
    (dup: release-6.2.0.md > # Performance) - 引入新的优化器提示 `SEMI_JOIN_REWRITE` 改善 `EXISTS` 查询性能 [#35323](https://github.com/pingcap/tidb/issues/35323)

+ TiKV

    (dup: release-6.2.0.md > Improvements> TiKV)- 支持通过 gzip 压缩 metrics 响应减少 HTTP body 大小 [#12355](https://github.com/tikv/tikv/issues/12355)
    - 支持使用 [`server.simplify-metrics`](/tikv-configuration-file.md#simplify-metrics-从-v620-版本开始引入) 配置项过滤部分 Metrics 采样数据以减少每次请求返回的 Metrics 数据量 [#12355](https://github.com/tikv/tikv/issues/12355)
    (dup: release-6.2.0.md > Improvements> TiKV)- 支持动态调整 RocksDB 进行 subcompaction 的并发个数 (`rocksdb.max-sub-compactions`) [#13145](https://github.com/tikv/tikv/issues/13145)

+ PD

    - 提升 Balance Region 在特定阶段的调度速度 [#4990](https://github.com/tikv/pd/issues/4990)

+ Tools

    + TiDB Lightning

        - 针对 `stale command` 等错误增加自动重试机制，提升导入成功率 [#36877](https://github.com/pingcap/tidb/issues/36877)

    + TiDB Data Migration (DM)

        - 用户可手动设置 Lightning Loader 并发数 [#5505](https://github.com/pingcap/tiflow/issues/5505)

    + TiCDC

        - 在 changefeed 的配置中增加参数 `transaction-atomicity` 来控制是否拆分大事务，从而大幅减少大事务的延时和内存消耗 [#5231](https://github.com/pingcap/tiflow/issues/5231)
        - (dup: release-6.2.0.md > 改进提升> Tools> TiCDC)- 优化了多 Region 场景下，runtime 上下文切换带来过多性能开销的问题 [#5610](https://github.com/pingcap/tiflow/issues/5610)
        - 优化 MySQL sink，实现自动关闭 safe mode。[#5611](https://github.com/pingcap/tiflow/issues/5611)

## Bug 修复

+ TiDB

    <!-- <execution> -->
    - 修复 `INL_HASH_JOIN` 和 `LIMIT` 一起使用时可能会卡住的问题 [#35638](https://github.com/pingcap/tidb/issues/35638)
    - 修复 TiDB 在执行 `UPDATE` 语句时可能会 panic 的问题 [#32311](https://github.com/pingcap/tidb/issues/32311)
    - 修复 TiDB 在执行 `SHOW COLUMNS` 时会发出协处理器请求的问题 [#36496](https://github.com/pingcap/tidb/issues/36496)
    - 修复执行 `SHOW WARNINGS` 时可能会报 `invalid memory address or nil pointer dereference` 的问题 [#31569](https://github.com/pingcap/tidb/issues/31569)
    - 修复 Static Partition Prune 模式下带聚合条件的 SQL 语句在表为空时结果错误的问题 [#35295](https://github.com/pingcap/tidb/issues/35295)

    <!-- <planner> -->
    - 修复执行 Join Reorder 操作时会错误地下推 Outer Join 条件的问题 [#37238](https://github.com/pingcap/tidb/issues/37238)
    - 修复了 CTE 被引用多次时 schema hash code 被错误克隆导致的 `Can't find column ... in schema ...` 错误 [#35404](https://github.com/pingcap/tidb/issues/35404)
    - 修复了某些 Right Outer Join 场景下 Join Reorder 错误导致查询结果错误的问题 [#36912](https://github.com/pingcap/tidb/issues/36912)
    (dup: release-5.4.2.md > Bug 修复> TiDB)- 修复了执行计划在 EqualAll 的情况下，把 TiFlash 的 `firstrow` 聚合函数的 null flag 设错的问题 [#34584](https://github.com/pingcap/tidb/issues/34584)
    - 修复了当查询创建了带 `IGNORE_PLAN_CACHE` hint 的 binding 后，无法再使用 Plan Cache 的问题 [#34596](https://github.com/pingcap/tidb/issues/34596)
    - 修复了 hash-partition window 和 single-partition window 之间缺少 `EXCHANGE` 算子的问题 [#35990](https://github.com/pingcap/tidb/issues/35990)
    (dup: release-5.2.4.md > Bug 修复> TiDB)- 修复某些情况下分区表无法充分利用索引来扫描数据的问题 [#33966](https://github.com/pingcap/tidb/issues/33966)
    - 修复了聚合运算下推后为 partial aggregation 设置了错误的默认值导致结果错误的问题 [#35295](https://github.com/pingcap/tidb/issues/35295)

    <!-- <sql-infra> -->
    (dup: release-6.2.0.md > Bug fixes> TiDB)- 修复了在某些情况下查询分区表可能返回 `index-out-of-range` and `non used index` 错误的问题 [#35181](https://github.com/pingcap/tidb/issues/35181)
    (dup: release-6.2.0.md > Bug fixes> TiDB)- 修复了在查询分区表中如果查询条件中有分区键且两者使用了不同的 COLLATE 时会错误的进行分区裁剪的问题 [#32749](https://github.com/pingcap/tidb/issues/32749) @[mjonss](https://github.com/mjonss)
    - 修复了在开启 TiDB Binlog 时，TiDB 执行 `ALTER SEQUENCE` 会产生错误的元信息版本号，进而导致 Drainer 报错退出的问题 [#36276](https://github.com/pingcap/tidb/issues/36276)
    - 修复了在极端情况下，启动 TiDB 可能进入错误状态的问题 [#36791](https://github.com/pingcap/tidb/issues/36791)
    - 修复了在 TiDB Dashboard 中查询分区表的执行计划时，有可能出现 `UnkownPlanID` 的问题 [#35153](https://github.com/pingcap/tidb/issues/35153)

    <!-- <transaction> -->
    (dup: release-6.2.0.md > Bug fixes> TiDB)- 修复了 `LOAD DATA` 语句中列的列表不生效的问题 [#35198](https://github.com/pingcap/tidb/issues/35198) @[SpadeA-Tang](https://github.com/SpadeA-Tang)
    (dup: release-5.3.2.md > Bug Fixes> TiDB)- 修复开启 TiDB Binlog 后插入重复数据导致 data and columnID count not match 错误的问题 [#33608](https://github.com/pingcap/tidb/issues/33608)
    - 去除 `tidb_gc_life_time` 设置时间检查限制 [#35392](https://github.com/pingcap/tidb/issues/35392)
    - 修复空分隔符使用情况下，`LOAD DATA` 出现死循环的问题 [#33298](https://github.com/pingcap/tidb/issues/33298)
    (dup: release-6.2.0.md > 错误修复> TiDB)- 避免向非健康状态的 TiKV 节点发送请求，以提升可用性 [#34906](https://github.com/pingcap/tidb/issues/34906)

+ TiKV

    - 修复 Raftstore 线程繁忙时，可能会出现 Region 重叠的问题 [#13160](https://github.com/tikv/tikv/issues/13160)
    (dup: release-6.2.0.md > Bug fixes> TiKV)- 修复 PD Region heartbeat 连接异常中断后未重新连接的问题 [#12934](https://github.com/tikv/tikv/issues/12934)
    (dup: release-5.3.2.md > Bug Fixes> TiKV)- 修复了对空字符串进行类型转换导致 TiKV panic 的问题 [#12673](https://github.com/tikv/tikv/issues/12673)
    (dup: release-6.2.0.md > Bug fixes> TiKV)- 修复了 TiKV 和 PD 配置文件中 Region size 不一致的问题 [#12518](https://github.com/tikv/tikv/issues/12518)
    (dup: release-6.2.0.md > Bug fixes> TiKV)- 修复了启用 Raft Engine 时未清理加密密钥的问题 [#12890](https://github.com/tikv/tikv/issues/12890)
    (dup: release-6.2.0.md > Bug fixes> TiKV)- 修复同时分裂和销毁一个 peer 时可能导致 panic 的问题 [#12825](https://github.com/tikv/tikv/issues/12825)
    (dup: release-6.2.0.md > Bug fixes> TiKV)- 修复在 Region merge 时 source peer 通过 snapshot 追日志时可能导致 panic 的问题 [#12663](https://github.com/tikv/tikv/issues/12663)
    (dup: release-5.3.2.md > Bug Fixes> TiKV)- 修复了 PD 客户端遇到报错时频繁重连的问题 [#12345](https://github.com/tikv/tikv/issues/12345)
    - 修复了开启 Raft Engine 并发恢复时 TiKV 可能会 panic 的问题 [#13123](https://github.com/tikv/tikv/issues/13123)
    (dup: release-6.2.0.md > Bug fixes> TiKV)- 修复了新创建的 Region Commit Log Duration 较高导致 QPS 下降的问题 [#13077](https://github.com/tikv/tikv/issues/13077)
    - 修复启用 Raft Engine 后特殊情况下 TiKV 会 panic 的问题 [#12698](https://github.com/tikv/tikv/issues/12698)
    - 修复无法找到 proc filesystem (procfs) 时警告级别日志过多的问题 [#13116](https://github.com/tikv/tikv/issues/13116)
    - 修复 Dashboard 中 Unified Read Pool CPU 表达式错误的问题 [#13086](https://github.com/tikv/tikv/issues/13086)
    - 修复 Region 较大时，默认 [`region-split-check-diff`](/tikv-configuration-file.md#region-split-check-diff) 可能会大于 bucket 大小的问题 [#12598](https://github.com/tikv/tikv/issues/12598)
    - 修复启用 Raft Engine 后，中止 Apply Snapshot 时可能会 panic 的问题 [#12470](https://github.com/tikv/tikv/issues/12470)
    - 修复 PD 客户端可能会出现死锁的问题 [#13191](https://github.com/tikv/tikv/issues/13191) [#12933](https://github.com/tikv/tikv/issues/12933)

+ PD

    - 修复当集群中节点的 label 设置异常时，store 上线进度评估不准确的问题 [#5234](https://github.com/tikv/pd/issues/5234)
    - 修复开启 `enable-forwarding` 时 gRPC 处理返回错误不恰当导致 PD panic 的问题 [#5373](https://github.com/tikv/pd/issues/5373)
    - 修复 `/regions/replicated` 返回状态错误的问题 [#5095](https://github.com/tikv/pd/issues/5095)

+ TiFlash

    (dup: release-5.4.2.md > Bug Fixes> TiFlash)- 修复在 clustered index 表删除列导致 TiFlash 崩溃的问题 [#5154](https://github.com/pingcap/tiflash/issues/5154)
    - 修复 `format` 函数可能会报 `Data truncated` 错误的问题 [#4891](https://github.com/pingcap/tiflash/issues/4891)
    - 修复存储中残留过期数据且无法删除的问题 [#5659](https://github.com/pingcap/tiflash/issues/5659)
    - 修复个别场景消耗不必要 CPU 的问题 [#5409](https://github.com/pingcap/tiflash/issues/5409)
    - 修复 TiFlash 无法在使用 IPv6 的集群运行的问题 [#5247](https://github.com/pingcap/tiflash/issues/5247)
    - 修复并行聚合出错时可能导致 TiFlash crash 的问题 [#5356](https://github.com/pingcap/tiflash/issues/5356)
    - 修复 `MinTSOScheduler` 在查询出错时可能会泄露线程资源问题 [#5556](https://github.com/pingcap/tiflash/issues/5556)

+ Tools

    + TiDB Lightning

        - 修复了使用 IPv6 host 时无法连接到 TiDB 的问题 [#35880](https://github.com/pingcap/tidb/issues/35880)
        - 修复 `read index not ready` 问题，增加重试机制 [#36566](https://github.com/pingcap/tidb/issues/36566)
        - 修复服务器模式下日志敏感信息被打印的问题 [#36374](https://github.com/pingcap/tidb/issues/36374)
        - 修复 TiDB Lightning 不支持 Parquet 文件中以斜线 (`/`)、数字、非 ASCII 字符开头的特殊列名的问题 [#36980](https://github.com/pingcap/tidb/issues/36980)
        - 修复极端情况下重复去重可能会 panic 的问题 [#34163](https://github.com/pingcap/tidb/issues/34163)

    + TiDB Data Migration (DM)

        - 修复 `txn-entry-size-limit` 在 DM 不生效的问题 [#6161](https://github.com/pingcap/tiflow/issues/6161)
        - 修复 `check-task` 命令不能处理特殊编码的问题 [#5895](https://github.com/pingcap/tiflow/issues/5895)
        - 修复 `query-status` 内可能存在 data race 的问题 [#4811](https://github.com/pingcap/tiflow/issues/4811)
        - 修复 `operate-schema` 显示不一致问题 [#5688](https://github.com/pingcap/tiflow/issues/5688)
        - 修复 relay 报错时可能导致 goroutine 泄露问题 [#6193](https://github.com/pingcap/tiflow/issues/6193)
        - 修复 DM Worker 因 DB Conn 获取可能卡住的问题 [#3733](https://github.com/pingcap/tiflow/issues/3733)
        - 修复 DM IPv6 支持问题 [#6249](https://github.com/pingcap/tiflow/issues/6249)

    + TiCDC

        - 修复最大兼容版本错误的问题 [#6039](https://github.com/pingcap/tiflow/issues/6039)
        - 修复 cdc server 启动未完成接受请求时出现 panic 的问题 [#5639](https://github.com/pingcap/tiflow/issues/5639)
        - 修复打开 sync-point 时 ddl sink 可能出现 panic 的问题 [#4934](https://github.com/pingcap/tiflow/issues/4934)
        - 修复打开 sync-point 功能在某些特殊场景下出现卡住 changefeed 的问题 [#6827](https://github.com/pingcap/tiflow/issues/6827)
        - 修复 cdc server 重启时 API 工作不正常的问题 [#5837](https://github.com/pingcap/tiflow/issues/5837)
        - 修复 black hole sink 场景下出现 data race 问题 [#6206](https://github.com/pingcap/tiflow/issues/6206)
        - 修复 `enable-old-value = false` 时可能出现的 cdc panic 问题 [#6198](https://github.com/pingcap/tiflow/issues/6198)
        - 修复在开启 redo 功能时可能出现数据不一致问题 [#6189](https://github.com/pingcap/tiflow/issues/6189) [#6368](https://github.com/pingcap/tiflow/issues/6368) [#6277](https://github.com/pingcap/tiflow/issues/6277) [#6456](https://github.com/pingcap/tiflow/issues/6456) [#6695](https://github.com/pingcap/tiflow/issues/6695) [#6764](https://github.com/pingcap/tiflow/issues/6764) [#6859](https://github.com/pingcap/tiflow/issues/6859)
        - 修复了 redo log 的性能问题，采取异步写的方式提升 redo 吞吐 [#6011](https://github.com/pingcap/tiflow/issues/6011)
        - 修复 MySQL sink 无法连接 IPv6 地址的问题 [#6135](https://github.com/pingcap/tiflow/issues/6135)

    + Backup & Restore (BR)

        (dup: release-5.4.2.md > Bug Fixes> Tools> Backup & Restore (BR))- 修复了 RawKV 模式下 BR 报 `ErrRestoreTableIDMismatch` 错误的问题 [#35279](https://github.com/pingcap/tidb/issues/35279)
        (dup: release-6.2.0.md > 改进提升> Tools> Backup & Restore (BR))- 优化了全量备份数据组织形式，解决大规模集群备份时遇到的 S3 限流问题 [#30087](https://github.com/pingcap/tidb/issues/30087)
        - 修复日志中统计备份耗时不正确的问题 [#35553](https://github.com/pingcap/tidb/issues/35553)

    + Dumpling

        - 修复 GetDSN 方法不支持 IPv6 的问题 [#36112](https://github.com/pingcap/tidb/issues/36112)

    + TiDB Binlog

        - 修复 `compressor` 设为 `gzip` 时 Drainer 无法正确发送请求至 Pump 的问题 [#1152](https://github.com/pingcap/tidb-binlog/issues/1152)
