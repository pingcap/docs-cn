---
title: TiDB 6.1.1 Release Notes
---

# TiDB 6.1.1 Release Notes

发版日期：2022 年 9 月 1 日

TiDB 版本：6.1.1

试用链接：[快速体验](https://docs.pingcap.com/zh/tidb/v6.1/quick-start-with-tidb) | [生产部署](https://docs.pingcap.com/zh/tidb/v6.1/production-deployment-using-tiup) | [下载离线包](https://cn.pingcap.com/product-community/?version=v6.1.1#version-list)

## 兼容性变更

+ TiDB

    - `SHOW DATABASES LIKE …` 语句不再大小写敏感 [#34766](https://github.com/pingcap/tidb/issues/34766) @[e1ijah1](https://github.com/e1ijah1)
    - 将 [`tidb_enable_outer_join_reorder`](/system-variables.md#tidb_enable_outer_join_reorder-从-v610-版本开始引入) 的默认值由 `1` 改为 `0`，即默认关闭 Join Reorder 对外连接的支持。

+ Diagnosis

    - 默认关闭持续性能分析 (Continuous Profiling) 特性，以避免开启该特性后 TiFlash 可能会崩溃的问题，详情参见 [#5687](https://github.com/pingcap/tiflash/issues/5687) @[mornyx](https://github.com/mornyx)

## 其他变更

- 在 `TiDB-community-toolkit` 二进制包中新增了以下内容，详情参见 [TiDB 离线包](/binary-package.md)。

    - `server-{version}-linux-amd64.tar.gz`
    - `grafana-{version}-linux-amd64.tar.gz`
    - `alertmanager-{version}-linux-amd64.tar.gz`
    - `prometheus-{version}-linux-amd64.tar.gz`
    - `blackbox_exporter-{version}-linux-amd64.tar.gz`
    - `node_exporter-{version}-linux-amd64.tar.gz`

- 针对不同操作系统和 CPU 架构的组合，引入不同级别质量标准的支持，见[操作系统及平台要求](https://docs.pingcap.com/zh/tidb/v6.1/hardware-and-software-requirements#操作系统及平台要求)。

## 提升改进

+ TiDB

    - 引入新的优化器提示 `SEMI_JOIN_REWRITE` 改善 `EXISTS` 查询性能 [#35323](https://github.com/pingcap/tidb/issues/35323) @[winoros](https://github.com/winoros)

+ TiKV

    - 支持通过 gzip 压缩 metrics 响应减少 HTTP body 大小 [#12355](https://github.com/tikv/tikv/issues/12355) @[winoros](https://github.com/winoros)
    - 支持使用 [`server.simplify-metrics`](https://docs.pingcap.com/zh/tidb/v6.1/tikv-configuration-file#simplify-metrics-从-v611-版本开始引入) 配置项过滤部分 Metrics 采样数据以减少每次请求返回的 Metrics 数据量 [#12355](https://github.com/tikv/tikv/issues/12355) @[glorv](https://github.com/glorv)
    - 支持动态调整 RocksDB 进行 subcompaction 的并发个数 (`rocksdb.max-sub-compactions`) [#13145](https://github.com/tikv/tikv/issues/13145) @[ethercflow](https://github.com/ethercflow)

+ PD

    - 提升 Balance Region 在特定阶段的调度速度 [#4990](https://github.com/tikv/pd/issues/4990) @[bufferflies](https://github.com/bufferflies)

+ Tools

    + TiDB Lightning

        - 针对 `stale command` 等错误增加自动重试机制，提升导入成功率 [#36877](https://github.com/pingcap/tidb/issues/36877) @[D3Hunter](https://github.com/D3Hunter)

    + TiDB Data Migration (DM)

        - 用户可手动设置 Lightning Loader 并发数 [#5505](https://github.com/pingcap/tiflow/issues/5505) @[buchuitoudegou](https://github.com/buchuitoudegou)

    + TiCDC

        - 在 changefeed 的配置中增加参数 `transaction-atomicity` 来控制是否拆分大事务，从而大幅减少大事务的延时和内存消耗 [#5231](https://github.com/pingcap/tiflow/issues/5231) @[CharlesCheung96](https://github.com/CharlesCheung96)
        - 优化了多 Region 场景下，runtime 上下文切换带来过多性能开销的问题 [#5610](https://github.com/pingcap/tiflow/issues/5610) @[hicqu](https://github.com/hicqu)
        - 优化 MySQL sink，实现自动关闭 safe mode [#5611](https://github.com/pingcap/tiflow/issues/5611) @[overvenus](https://github.com/overvenus)

## Bug 修复

+ TiDB

    - 修复 `INL_HASH_JOIN` 和 `LIMIT` 一起使用时可能会卡住的问题 [#35638](https://github.com/pingcap/tidb/issues/35638) @[guo-shaoge](https://github.com/guo-shaoge)
    - 修复 TiDB 在执行 `UPDATE` 语句时可能会 panic 的问题 [#32311](https://github.com/pingcap/tidb/issues/32311) @[Yisaer](https://github.com/Yisaer)
    - 修复 TiDB 在执行 `SHOW COLUMNS` 时会发出协处理器请求的问题 [#36496](https://github.com/pingcap/tidb/issues/36496) @[tangenta](https://github.com/tangenta)
    - 修复执行 `SHOW WARNINGS` 时可能会报 `invalid memory address or nil pointer dereference` 的问题 [#31569](https://github.com/pingcap/tidb/issues/31569) @[zyguan](https://github.com/zyguan)
    - 修复 Static Partition Prune 模式下带聚合条件的 SQL 语句在表为空时结果错误的问题 [#35295](https://github.com/pingcap/tidb/issues/35295) @[tiancaiamao](https://github.com/tiancaiamao)
    - 修复执行 Join Reorder 操作时会错误地下推 Outer Join 条件的问题 [#37238](https://github.com/pingcap/tidb/issues/37238) @[winoros](https://github.com/winoros)
    - 修复了 CTE 被引用多次时 schema hash code 被错误克隆导致的 `Can't find column ... in schema ...` 错误 [#35404](https://github.com/pingcap/tidb/issues/35404) @[AilinKid](https://github.com/AilinKid)
    - 修复了某些 Right Outer Join 场景下 Join Reorder 错误导致查询结果错误的问题 [#36912](https://github.com/pingcap/tidb/issues/36912) @[winoros](https://github.com/winoros)
    - 修复了执行计划在 EqualAll 的情况下，把 TiFlash 的 `firstrow` 聚合函数的 null flag 设错的问题 [#34584](https://github.com/pingcap/tidb/issues/34584) @[fixdb](https://github.com/fixdb)
    - 修复了当查询创建了带 `IGNORE_PLAN_CACHE` hint 的 binding 后，无法再使用 Plan Cache 的问题 [#34596](https://github.com/pingcap/tidb/issues/34596) @[fzzf678](https://github.com/fzzf678)
    - 修复了 hash-partition window 和 single-partition window 之间缺少 `EXCHANGE` 算子的问题 [#35990](https://github.com/pingcap/tidb/issues/35990) @[LittleFall](https://github.com/LittleFall)
    - 修复某些情况下分区表无法充分利用索引来扫描数据的问题 [#33966](https://github.com/pingcap/tidb/issues/33966) @[mjonss](https://github.com/mjonss)
    - 修复了聚合运算下推后为 partial aggregation 设置了错误的默认值导致结果错误的问题 [#35295](https://github.com/pingcap/tidb/issues/35295) @[tiancaiamao](https://github.com/tiancaiamao)
    - 修复了在某些情况下查询分区表可能返回 `index-out-of-range` 错误的问题 [#35181](https://github.com/pingcap/tidb/issues/35181) @[mjonss](https://github.com/mjonss)
    - 修复了在查询分区表中如果查询条件中有分区键且两者使用了不同的 COLLATE 时会错误的进行分区裁剪的问题 [#32749](https://github.com/pingcap/tidb/issues/32749) @[mjonss](https://github.com/mjonss)
    - 修复了在开启 TiDB Binlog 时，TiDB 执行 `ALTER SEQUENCE` 会产生错误的元信息版本号，进而导致 Drainer 报错退出的问题 [#36276](https://github.com/pingcap/tidb/issues/36276) @[AilinKid](https://github.com/AilinKid)
    - 修复了在极端情况下，启动 TiDB 可能进入错误状态的问题 [#36791](https://github.com/pingcap/tidb/issues/36791) @[xhebox](https://github.com/xhebox)
    - 修复了在 TiDB Dashboard 中查询分区表的执行计划时，有可能出现 `UnkownPlanID` 的问题 [#35153](https://github.com/pingcap/tidb/issues/35153) @[time-and-fate](https://github.com/time-and-fate)
    - 修复了 `LOAD DATA` 语句中列的列表不生效的问题 [#35198](https://github.com/pingcap/tidb/issues/35198) @[SpadeA-Tang](https://github.com/SpadeA-Tang)
    - 修复开启 TiDB Binlog 后插入重复数据导致 data and columnID count not match 错误的问题 [#33608](https://github.com/pingcap/tidb/issues/33608) @[zyguan](https://github.com/zyguan)
    - 去除 `tidb_gc_life_time` 设置时间检查限制 [#35392](https://github.com/pingcap/tidb/issues/35392) @[TonsnakeLin](https://github.com/TonsnakeLin)
    - 修复空分隔符使用情况下，`LOAD DATA` 出现死循环的问题 [#33298](https://github.com/pingcap/tidb/issues/33298) @[zyguan](https://github.com/zyguan)
    - 避免向非健康状态的 TiKV 节点发送请求，以提升可用性 [#34906](https://github.com/pingcap/tidb/issues/34906) @[sticnarf](https://github.com/sticnarf)

+ TiKV

    - 修复 Raftstore 线程繁忙时，可能会出现 Region 重叠的问题 [#13160](https://github.com/tikv/tikv/issues/13160) @[5kbpers](https://github.com/5kbpers)
    - 修复 PD Region heartbeat 连接异常中断后未重新连接的问题 [#12934](https://github.com/tikv/tikv/issues/12934) @[bufferflies](https://github.com/bufferflies)
    - 修复了对空字符串进行类型转换导致 TiKV panic 的问题 [#12673](https://github.com/tikv/tikv/issues/12673) @[wshwsh12](https://github.com/wshwsh12)
    - 修复了 TiKV 和 PD 配置文件中 Region size 不一致的问题 [#12518](https://github.com/tikv/tikv/issues/12518) @[5kbpers](https://github.com/5kbpers)
    - 修复了启用 Raft Engine 时未清理加密密钥的问题 [#12890](https://github.com/tikv/tikv/issues/12890) @[tabokie](https://github.com/tabokie)
    - 修复同时分裂和销毁一个 peer 时可能导致 panic 的问题 [#12825](https://github.com/tikv/tikv/issues/12825) @[BusyJay](https://github.com/BusyJay)
    - 修复在 Region merge 时 source peer 通过 snapshot 追日志时可能导致 panic 的问题 [#12663](https://github.com/tikv/tikv/issues/12663) @[BusyJay](https://github.com/BusyJay)
    - 修复了 PD 客户端遇到报错时频繁重连的问题 [#12345](https://github.com/tikv/tikv/issues/12345) @[Connor1996](https://github.com/Connor1996)
    - 修复了开启 Raft Engine 并发恢复时 TiKV 可能会 panic 的问题 [#13123](https://github.com/tikv/tikv/issues/13123) @[tabokie](https://github.com/tabokie)
    - 修复了新创建的 Region Commit Log Duration 较高导致 QPS 下降的问题 [#13077](https://github.com/tikv/tikv/issues/13077) @[Connor1996](https://github.com/Connor1996)
    - 修复启用 Raft Engine 后特殊情况下 TiKV 会 panic 的问题 [#12698](https://github.com/tikv/tikv/issues/12698) @[tabokie](https://github.com/tabokie)
    - 修复无法找到 proc filesystem (procfs) 时警告级别日志过多的问题 [#13116](https://github.com/tikv/tikv/issues/13116) @[tabokie](https://github.com/tabokie)
    - 修复 Dashboard 中 Unified Read Pool CPU 表达式错误的问题 [#13086](https://github.com/tikv/tikv/issues/13086) @[glorv](https://github.com/glorv)
    - 修复 Region 较大时，默认 [`region-split-check-diff`](/tikv-configuration-file.md#region-split-check-diff) 可能会大于 bucket 大小的问题 [#12598](https://github.com/tikv/tikv/issues/12598) @[tonyxuqqi](https://github.com/tonyxuqqi)
    - 修复启用 Raft Engine 后，中止 Apply Snapshot 时可能会 panic 的问题 [#12470](https://github.com/tikv/tikv/issues/12470) @[tabokie](https://github.com/tabokie)
    - 修复 PD 客户端可能会出现死锁的问题 [#13191](https://github.com/tikv/tikv/issues/13191) @[bufferflies](https://github.com/bufferflies) [#12933](https://github.com/tikv/tikv/issues/12933) @[BurtonQin](https://github.com/BurtonQin)

+ PD

    - 修复当集群中节点的 label 设置异常时，store 上线进度评估不准确的问题 [#5234](https://github.com/tikv/pd/issues/5234) @[rleungx](https://github.com/rleungx)
    - 修复开启 `enable-forwarding` 时 gRPC 处理返回错误不恰当导致 PD panic 的问题 [#5373](https://github.com/tikv/pd/issues/5373) @[bufferflies](https://github.com/bufferflies)
    - 修复 `/regions/replicated` 返回状态错误的问题 [#5095](https://github.com/tikv/pd/issues/5095) @[rleungx](https://github.com/rleungx)

+ TiFlash

    - 修复在 clustered index 表删除列导致 TiFlash 崩溃的问题 [#5154](https://github.com/pingcap/tiflash/issues/5154) @[hongyunyan](https://github.com/hongyunyan)
    - 修复 `format` 函数可能会报 `Data truncated` 错误的问题 [#4891](https://github.com/pingcap/tiflash/issues/4891) @[xzhangxian1008](https://github.com/xzhangxian1008)
    - 修复存储中残留过期数据且无法删除的问题 [#5659](https://github.com/pingcap/tiflash/issues/5659) @[lidezhu](https://github.com/lidezhu)
    - 修复个别场景消耗不必要 CPU 的问题 [#5409](https://github.com/pingcap/tiflash/issues/5409) @[breezewish](https://github.com/breezewish)
    - 修复 TiFlash 无法在使用 IPv6 的集群运行的问题 [#5247](https://github.com/pingcap/tiflash/issues/5247) @[solotzg](https://github.com/solotzg)
    - 修复并行聚合出错时可能导致 TiFlash crash 的问题 [#5356](https://github.com/pingcap/tiflash/issues/5356) @[gengliqi](https://github.com/gengliqi)
    - 修复 `MinTSOScheduler` 在查询出错时可能会泄露线程资源问题 [#5556](https://github.com/pingcap/tiflash/issues/5556) @[windtalker](https://github.com/windtalker)

+ Tools

    + TiDB Lightning

        - 修复了使用 IPv6 host 时无法连接到 TiDB 的问题 [#35880](https://github.com/pingcap/tidb/issues/35880) @[D3Hunter](https://github.com/D3Hunter)
        - 修复 `read index not ready` 问题，增加重试机制 [#36566](https://github.com/pingcap/tidb/issues/36566) @[D3Hunter](https://github.com/D3Hunter)
        - 修复服务器模式下日志敏感信息被打印的问题 [#36374](https://github.com/pingcap/tidb/issues/36374) @[lichunzhu](https://github.com/lichunzhu)
        - 修复 TiDB Lightning 不支持 Parquet 文件中以斜线 (`/`)、数字、非 ASCII 字符开头的特殊列名的问题 [#36980](https://github.com/pingcap/tidb/issues/36980) @[D3Hunter](https://github.com/D3Hunter)
        - 修复极端情况下去重可能会导致 TiDB Lightning panic 的问题 [#34163](https://github.com/pingcap/tidb/issues/34163) @[ForwardStar](https://github.com/ForwardStar)

    + TiDB Data Migration (DM)

        - 修复 `txn-entry-size-limit` 在 DM 不生效的问题 [#6161](https://github.com/pingcap/tiflow/issues/6161) @[ForwardStar](https://github.com/ForwardStar)
        - 修复 `check-task` 命令不能处理特殊编码的问题 [#5895](https://github.com/pingcap/tiflow/issues/5895) @[Ehco1996](https://github.com/Ehco1996)
        - 修复 `query-status` 内可能存在 data race 的问题 [#4811](https://github.com/pingcap/tiflow/issues/4811) @[lyzx2001](https://github.com/lyzx2001)
        - 修复 `operate-schema` 显示不一致问题 [#5688](https://github.com/pingcap/tiflow/issues/5688) @[ForwardStar](https://github.com/ForwardStar)
        - 修复 relay 报错时可能导致 goroutine 泄露问题 [#6193](https://github.com/pingcap/tiflow/issues/6193) @[lance6716](https://github.com/lance6716)
        - 修复 DM Worker 因 DB Conn 获取可能卡住的问题 [#3733](https://github.com/pingcap/tiflow/issues/3733) @[lance6716](https://github.com/lance6716)
        - 修复 DM IPv6 支持问题 [#6249](https://github.com/pingcap/tiflow/issues/6249) @[D3Hunter](https://github.com/D3Hunter)

    + TiCDC

        - 修复最大兼容版本错误的问题 [#6039](https://github.com/pingcap/tiflow/issues/6039) @[hi-rustin](https://github.com/Rustin170506)
        - 修复 cdc server 启动未完成接受请求时出现 panic 的问题 [#5639](https://github.com/pingcap/tiflow/issues/5639) @[asddongmen](https://github.com/asddongmen)
        - 修复打开 sync-point 时 ddl sink 可能出现 panic 的问题 [#4934](https://github.com/pingcap/tiflow/issues/4934) @[asddongmen](https://github.com/asddongmen)
        - 修复打开 sync-point 功能在某些特殊场景下出现卡住 changefeed 的问题 [#6827](https://github.com/pingcap/tiflow/issues/6827) @[hicqu](https://github.com/hicqu)
        - 修复 cdc server 重启时 API 工作不正常的问题 [#5837](https://github.com/pingcap/tiflow/issues/5837) @[asddongmen](https://github.com/asddongmen)
        - 修复 black hole sink 场景下出现 data race 问题 [#6206](https://github.com/pingcap/tiflow/issues/6206) @[asddongmen](https://github.com/asddongmen)
        - 修复 `enable-old-value = false` 时可能出现的 cdc panic 问题 [#6198](https://github.com/pingcap/tiflow/issues/6198) @[hi-rustin](https://github.com/Rustin170506)
        - 修复在开启 redo 功能时可能出现数据不一致问题 [#6189](https://github.com/pingcap/tiflow/issues/6189) [#6368](https://github.com/pingcap/tiflow/issues/6368) [#6277](https://github.com/pingcap/tiflow/issues/6277) [#6456](https://github.com/pingcap/tiflow/issues/6456) [#6695](https://github.com/pingcap/tiflow/issues/6695) [#6764](https://github.com/pingcap/tiflow/issues/6764) [#6859](https://github.com/pingcap/tiflow/issues/6859) @[asddongmen](https://github.com/asddongmen)
        - 修复了 redo log 的性能问题，采取异步写的方式提升 redo 吞吐 [#6011](https://github.com/pingcap/tiflow/issues/6011) @[CharlesCheung96](https://github.com/CharlesCheung96)
        - 修复 MySQL sink 无法连接 IPv6 地址的问题 [#6135](https://github.com/pingcap/tiflow/issues/6135) @[hi-rustin](https://github.com/Rustin170506)

    + Backup & Restore (BR)

        - 修复了 RawKV 模式下 BR 报 `ErrRestoreTableIDMismatch` 错误的问题 [#35279](https://github.com/pingcap/tidb/issues/35279) @[3pointer](https://github.com/3pointer)
        - 优化了全量备份数据组织形式，解决大规模集群备份时遇到的 S3 限流问题 [#30087](https://github.com/pingcap/tidb/issues/30087) @[MoCuishle28](https://github.com/MoCuishle28)
        - 修复日志中统计备份耗时不正确的问题 [#35553](https://github.com/pingcap/tidb/issues/35553) @[ixuh12](https://github.com/ixuh12)

    + Dumpling

        - 修复 GetDSN 方法不支持 IPv6 的问题 [#36112](https://github.com/pingcap/tidb/issues/36112) @[D3Hunter](https://github.com/D3Hunter)

    + TiDB Binlog

        - 修复 `compressor` 设为 `gzip` 时 Drainer 无法正确发送请求至 Pump 的问题 [#1152](https://github.com/pingcap/tidb-binlog/issues/1152) @[lichunzhu](https://github.com/lichunzhu)
