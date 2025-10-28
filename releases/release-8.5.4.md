---
title: TiDB 8.5.4 Release Notes
summary: 了解 TiDB 8.5.4 版本的兼容性变更、改进提升，以及错误修复。
---

# TiDB 8.5.4 Release Notes

发版日期：2025 年 x 月 x 日

TiDB 版本：8.5.4

试用链接：[快速体验](https://docs.pingcap.com/zh/tidb/v8.5/quick-start-with-tidb) | [生产部署](https://docs.pingcap.com/zh/tidb/v8.5/production-deployment-using-tiup) | [下载离线包](https://cn.pingcap.com/product-community/?version=v8.5.4#version-list)

## 兼容性变更

- (dup): release-7.5.7.md > 兼容性变更 - TiKV 废弃以下配置项，并由新的 [`gc.auto-compaction`](https://docs.pingcap.com/zh/tidb/v7.5/tikv-configuration-file/#gcauto-compaction) 配置项替代，用于控制自动 compaction 行为 [#18727](https://github.com/tikv/tikv/issues/18727) @[v01dstar](https://github.com/v01dstar)

- 废弃配置项：[`region-compact-check-interval`](https://docs.pingcap.com/zh/tidb/v7.5/tikv-configuration-file#region-compact-check-interval)、[`region-compact-check-step`](https://docs.pingcap.com/zh/tidb/v7.5/tikv-configuration-file#region-compact-check-step)、[`region-compact-min-tombstones`](https://docs.pingcap.com/zh/tidb/v7.5/tikv-configuration-file#region-compact-min-tombstones)、[`region-compact-tombstones-percent`](https://docs.pingcap.com/zh/tidb/v7.5/tikv-configuration-file#region-compact-tombstones-percent)、[`region-compact-min-redundant-rows`](https://docs.pingcap.com/zh/tidb/v7.5/tikv-configuration-file#region-compact-min-redundant-rows-从-v710-版本开始引入) 和 [`region-compact-redundant-rows-percent`](https://docs.pingcap.com/zh/tidb/v7.5/tikv-configuration-file#region-compact-redundant-rows-percent-从-v710-版本开始引入)。

- 新增配置项：[`gc.auto-compaction.check-interval`](https://docs.pingcap.com/zh/tidb/v7.5/tikv-configuration-file#check-interval-从-v757-版本开始引入)、[`gc.auto-compaction.tombstone-num-threshold`](https://docs.pingcap.com/zh/tidb/v7.5/tikv-configuration-file#tombstone-num-threshold-从-v757-版本开始引入)、[`gc.auto-compaction.tombstone-percent-threshold`](https://docs.pingcap.com/zh/tidb/v7.5/tikv-configuration-file#tombstone-percent-threshold-从-v757-版本开始引入)、[`gc.auto-compaction.redundant-rows-threshold`](https://docs.pingcap.com/zh/tidb/v7.5/tikv-configuration-file#redundant-rows-threshold-从-v757-版本开始引入)、[`gc.auto-compaction.redundant-rows-percent-threshold`](https://docs.pingcap.com/zh/tidb/v7.5/tikv-configuration-file#redundant-rows-percent-threshold-从-v757-版本开始引入) 和 [`gc.auto-compaction.bottommost-level-force`](https://docs.pingcap.com/zh/tidb/v7.5/tikv-configuration-file#bottommost-level-force-从-v757-版本开始引入)。

## 改进提升

+ TiDB <!--tw@Oreoxmt: 11 notes-->

    - (dup): release-9.0.0.md(beta.1) > # SQL 功能 * 支持对分区表的非唯一列创建全局索引 [#58650](https://github.com/pingcap/tidb/issues/58650) @[Defined2014](https://github.com/Defined2014) @[mjonss](https://github.com/mjonss)
    - (dup): release-9.0.0.md(beta.1) > 改进提升> TiDB - 支持由 `IN` 子查询而来的 Semi Join 使用 `semi_join_rewrite` 的 Hint [#58829](https://github.com/pingcap/tidb/issues/58829) @[qw4990](https://github.com/qw4990)
    - 微调了参数 tidb_opt_ordering_index_selectivity_ratio 生效时的估算策略 [#62817](https://github.com/pingcap/tidb/issues/62817) @[terry1purcell](https://github.com/terry1purcell)
    - 新增配置项 tidb_opt_enable_semi_join_rewrite 去控制 exists 子查询是否需要被改写 [#44850](https://github.com/pingcap/tidb/issues/44850) @[terry1purcell](https://github.com/terry1purcell)
    - 微调了优化器选择逻辑，在某些情况下新索引更容易被选中 [#57948](https://github.com/pingcap/tidb/issues/57948) @[terry1purcell](https://github.com/terry1purcell)
    - 优化了 NDV 较小的列的查询估算逻辑 [#61792](https://github.com/pingcap/tidb/issues/61792) @[terry1purcell](https://github.com/terry1purcell)
    - 微调了 limit offset 出现在 Index Join 查询中的估算策略 [#45077](https://github.com/pingcap/tidb/issues/45077) @[qw4990](https://github.com/qw4990)
    - 新增 session variable “tidb_opt_enable_no_decorrelate_in_select” 去控制 select list 中的子查询是否需要被解关联  [#51116](https://github.com/pingcap/tidb/issues/51116) @[terry1purcell](https://github.com/terry1purcell)
    - 优化了 Merge join 计算 cost 可能存在遗漏 filter 的情况  [#62917](https://github.com/pingcap/tidb/issues/62917) @[qw4990](https://github.com/qw4990)
    - 优化了在统计信息收集不及时情况下，越界估算的策略 [#58068](https://github.com/pingcap/tidb/issues/58068) @[terry1purcell](https://github.com/terry1purcell)
    - 在执行时间概览中添加 Backoff 时间以便调试 [#61441](https://github.com/pingcap/tidb/issues/61441) @[dbsid](https://github.com/dbsid)
    - 在审计日志插件中添加语句 ID 信息 [#63525](https://github.com/pingcap/tidb/issues/63525) @[YangKeao](https://github.com/YangKeao)
    - 为审计日志插件添加缓冲日志支持：[#63650](https://github.com/pingcap/tidb/issues/63650) @[bb7133](https://github.com/bb7133)
        - instance.plugin_audit_log_flush_interval：刷新缓冲审计日志的时间间隔
        - instance.plugin_audit_log_buffer_size：插件审计日志的缓冲区大小（字节），默认值为 0（不使用缓冲） 

+ TiKV <!--tw@lilin90: 6 notes-->

    - 将部分 BR 模块的可自动恢复的错误的日志级别从ERROR 调整为 WARN [#18493](https://github.com/tikv/tikv/issues/18493) @[YuJuncen](https://github.com/YuJuncen)
    - 将 Raft 模块检查 GC 的流程拆分为两个阶段，提升 Region 冗余 MVCC 版本 GC 的效率。[#18695](https://github.com/tikv/tikv/issues/18695) @[v01dstar](https://github.com/v01dstar)
    - 基于 GC safe point 和 Rocksdb 的统计信息计算 MVCC 的冗余读，提升 compaction 的效率和准确性。[#18697](https://github.com/tikv/tikv/issues/18697) @[v01dstar](https://github.com/v01dstar)
    - 将部分 TiKV 的错误日志从 ERROR 级别调整为 WARN 级别，避免产生过多不必要的告警。[#18745](https://github.com/tikv/tikv/issues/18745) @[exit-code-1](https://github.com/exit-code-1)
    - 将 Region MVCC 的 GC 处理逻辑改由 GC worker 线程执行，统一 GC 的处理逻辑。 [#18727](https://github.com/tikv/tikv/issues/18727) @[v01dstar](https://github.com/v01dstar)
    - 优化 gRPC 线程池线程数量默认值的计算方式，将原来的固定数据调整为根据总的 CPU 配置动态计算，避免 gRPC 线程数量太小产生的性能瓶颈。 [#18613](https://github.com/tikv/tikv/issues/18613) @[LykxSassinator](https://github.com/LykxSassinator)
    - (dup): release-7.5.7.md > 改进提升> TiKV - 优化在存在大量 SST 文件的环境中 async snapshot 和 write 的尾延迟 [#18743](https://github.com/tikv/tikv/issues/18743) @[Connor1996](https://github.com/Connor1996)

+ PD <!--tw@Oreoxmt: 3 notes-->

    - 减少非必要的错误日志 [#9370](https://github.com/tikv/pd/issues/9370) @[bufferflies](https://github.com/bufferflies)
    - 升级 golang 版本到 1.23.12, 同时更新相关依赖 [#9788](https://github.com/tikv/pd/issues/9788) @[JmPotato](https://github.com/JmPotato)
    - 支持按照表级别维度打散 region 数量，使其按照 scatter-role 和 engine 维度进行均衡 #[8986](https://github.com/tikv/pd/issues/8986)  @[bufferflies](https://github.com/bufferflies)

+ TiFlash <!--tw@qiancai: 4 notes-->

    - 跳过不必要读取的数据，优化 TableScan 的读取性能 [#9875](https://github.com/pingcap/tiflash/issues/9875) @[gengliqi](https://github.com/gengliqi)
    - 优化 TiFlash 在宽且稀疏的表上 TableScan 的性能 [#10361](https://github.com/pingcap/tiflash/issues/10361) @[JaySon-Huang](https://github.com/JaySon-Huang)
    - 优化当集群存在大量表时，添加向量索引时的 TiFlash CPU 开销 [#10357](https://github.com/pingcap/tiflash/issues/10357) @[Lloyd-Pottiger](https://github.com/Lloyd-Pottiger)
    - 减少不必要的处理 raft commands 时的日志 [#10467](https://github.com/pingcap/tiflash/issues/10467) @[JaySon-Huang](https://github.com/JaySon-Huang)

+ Tools

    + TiDB Data Migration (DM) <!--tw@hfxsd: 1 note-->

        - 获取上游 `GTID_MODE` 时，支持兼容大小写 [#12167](https://github.com/pingcap/tiflow/issues/12167) @[OliverS929](https://github.com/OliverS929)

## 错误修复

+ TiDB <!--tw@lilin90: the following 14 notes-->

    - 修复当 `tidb_isolation_read_engines` 设置为 "tiflash" 时，`use index` hint 无法生效的问题 [#60869](https://github.com/pingcap/tidb/issues/60869) @[Lloyd-Pottiger](https://github.com/Lloyd-Pottiger)
    - 修复了 `max_execution_time` 对 `SELECT FOR UPDATE` 语句不生效的问题. [#62960](https://github.com/pingcap/tidb/issues/62960) @[ekexium](https://github.com/ekexium)
    - (dup): release-7.5.7.md > 错误修复> TiDB - 修复估算跨月或跨年的行数时，结果可能过分偏大的问题 [#50080](https://github.com/pingcap/tidb/issues/50080) @[terry1purcell](https://github.com/terry1purcell)
    - 修复预处理语句中处理 decimal 与 mysql 不一致的问题 [#62602](https://github.com/pingcap/tidb/issues/62602) @[ChangRui-Ryan](https://github.com/ChangRui-Ryan)
    - 修复 `truncate` 函数中短路径处理错误的问题 [#57608](https://github.com/pingcap/tidb/issues/57608) @[xzhangxian1008](https://github.com/xzhangxian1008)
    - 修复当 `Out Of Quota For Local Temporary Space` 触发时，spill 文件可能未被全部删除的问题 [#63216](https://github.com/pingcap/tidb/issues/63216) @[xzhangxian1008](https://github.com/xzhangxian1008)
    - 修复查询`INFORMATION_SCHEMA`表使用正则表达式过滤结果不正确的问题 [#62347](https://github.com/pingcap/tidb/issues/62347) @[River2000i](https://github.com/River2000i)
    - 修复从 PD 获取 timestamp 异常时没有返回错误的问题 [#58871](https://github.com/pingcap/tidb/issues/58871) @[joechenrh](https://github.com/joechenrh)
    - 修复modify column时，owner TiDB和非ownerTiDB查询数据不一致的问题 [#60264](https://github.com/pingcap/tidb/issues/60264) @[tangenta](https://github.com/tangenta)
    - 修复动态调参后 `ADMIN ALTER DDL JOBS`显示参数不正确的问题 [#63201](https://github.com/pingcap/tidb/issues/63201) @[fzzf678](https://github.com/fzzf678)
    - 修复通过事务加索引时GC savepoint 不推进的问题 [#62424](https://github.com/pingcap/tidb/issues/62424) @[wjhuang2016](https://github.com/wjhuang2016)
    - 修复过大的 SST 文件 ingest 到 L0 中导致流控的问题 [#63466](https://github.com/pingcap/tidb/issues/63466) @[CbcWestwolf](https://github.com/CbcWestwolf)
    - 修复当 CPU 和 memory 比例为 1:2 时阻塞 global sort 的问题 [#60951](https://github.com/pingcap/tidb/issues/60951) @[wjhuang2016](https://github.com/wjhuang2016)
    - 修复超过 16 个 DXF 任务上限时无法 cancel pending 任务的问题 [#63896](https://github.com/pingcap/tidb/issues/63896) @[D3Hunter](https://github.com/D3Hunter)
    - 修复cancel DXF任务后，其他任务无法退出的问题 [#63927](https://github.com/pingcap/tidb/issues/63927) @[D3Hunter](https://github.com/D3Hunter) <!--tw@hfxsd: the following 14 notes-->
    - 修复 apply 并发设置后，query 带 index join 导致无法生成 plan 的问题 [#59863](https://github.com/pingcap/tidb/issues/59863) @[hawkingrei](https://github.com/hawkingrei)
    - 修复查询使用 `ATAN2` 函数可能导致结果错误的问题 [#60093](https://github.com/pingcap/tidb/issues/60093) @[guo-shaoge](https://github.com/guo-shaoge)
    - 修复 `select 1 from duml` 无法使用实例级别的计划缓存的问题 [#63075](https://github.com/pingcap/tidb/issues/63075) @[time-and-fate](https://github.com/time-and-fate)
    - 修复 Join Order 变更顺序后可能导致无法规划的问题 [#61715](https://github.com/pingcap/tidb/issues/61715) @[hawkingrei](https://github.com/hawkingrei)
    - 修复 `set_var hint` 使用 Binding 导致无法恢复回原始变量设置的问题 [#59822](https://github.com/pingcap/tidb/issues/59822) @[wddevries](https://github.com/wddevries)
    - 修复 `ONLY_FULL_GROUP_BY` 取值为负数时导致检查失败的问题 [#62617](https://github.com/pingcap/tidb/issues/62617) @[AilinKid](https://github.com/AilinKid)
    - 修复 `ONLY_FULL_GROUP_BY` 检查时大小写不敏感的问题 [#62672](https://github.com/pingcap/tidb/issues/62672) @[AilinKid](https://github.com/AilinKid)
    - 修复 DP Join Order 算法可能产生错误 Plan 的问题 [#63353](https://github.com/pingcap/tidb/issues/63353) @[winoros](https://github.com/winoros)
    - 修复 Outer Join 改写为 Inner Join 可能出错的问题 [#61327](https://github.com/pingcap/tidb/issues/61327) @[hawkingrei](https://github.com/hawkingrei)
    - 修复查询执行可能导致内部 panic 的问题 [#58600](https://github.com/pingcap/tidb/issues/58600) @[Defined2014](https://github.com/Defined2014)
    - 修复全局索引在某些 `ALTER PARTITION` 状态下获取错误数据的问题 [#64084](https://github.com/pingcap/tidb/pull/64084) @[mjonss](https://github.com/mjonss)
    - 修复全局索引在某些情况下返回错误结果的问题 [#61083](https://github.com/pingcap/tidb/issues/61083) @[Defined2014](https://github.com/Defined2014)
    - 修复 `character_set_results` 在遇到错误字符时进行截断而不是进行替换的问题 [#61085](https://github.com/pingcap/tidb/issues/61085) @[xhebox](https://github.com/xhebox)
    - 修复 `ADD COLUMN` 与 `UPDATE` 并发执行时出错的问题 [#60047](https://github.com/pingcap/tidb/issues/60047) @[L-maple](https://github.com/L-maple)

+ PD <!--tw@qiancai: 8 notes-->

    - 修复 PD Client 重试策略没有正确初始化的问题 [#9013](https://github.com/tikv/pd/issues/9013) @[rleungx](https://github.com/rleungx)
    - 修复 /config 和 /members API 的错误输出 [#9797](https://github.com/tikv/pd/issues/9797) @[lhy1024](https://github.com/lhy1024) 
    - 修复 tso proxy 错误处理 #[9188](https://github.com/tikv/pd/issues/9188) @[Tema](https://github.com/Tema)
    - 修复在关闭 bucket 上报后， split bucket 依然生效 #[9726](https://github.com/tikv/pd/issues/9726) @[bufferflies](https://github.com/bufferflies)
    - 修复 resource manager 错误分配 token 问题 #[9455](https://github.com/tikv/pd/issues/9455)  @[JmPotato](https://github.com/JmPotato)
    - 修复 pd leader 变更后, placement rule 不生效问题 #[9602](https://github.com/tikv/pd/issues/9602) @[okJiang](https://github.com/okJiang)
    - 修复 backoff 初始化错误问题 #[9013](https://github.com/tikv/pd/issues/9013)  @[rleungx](https://github.com/rleungx)
    - 修复 ttl 配置不生效问题 #[9343](https://github.com/tikv/pd/issues/9343) @[lhy1024](https://github.com/lhy1024)

+ TiFlash <!--tw@hfxsd: 5 notes-->

    - 修复当查询的列存储大量 `NULL` 值时，可能导致查询失败的问题 [#10340](https://github.com/pingcap/tiflash/issues/10340) @[Lloyd-Pottiger](https://github.com/Lloyd-Pottiger)
    - 修复 TiFlash 消耗 RU 的统计数据不准确的问题 [#10380](https://github.com/pingcap/tiflash/issues/10380) @[JinheLin](https://github.com/JinheLin)
    - 修复在存算分离架构下，在存在慢查询时 TiFlash 容易发生 OOM 的问题 [#10278](https://github.com/pingcap/tiflash/issues/10278) @[JaySon-Huang](https://github.com/JaySon-Huang)
    - 修复在存算分离架构下，TiFlash 遇到与 S3 网络分区时可能无限重试的问题 [#10424](https://github.com/pingcap/tiflash/issues/10424) @[JaySon-Huang](https://github.com/JaySon-Huang)
    - 修复当参数为 `DECIMAL` 类型时，`FLOOR()` 和 `CEIL()` 函数结果可能不正确的问题 [#10365](https://github.com/pingcap/tiflash/issues/10365) @[ChangRui-Ryan](https://github.com/ChangRui-Ryan) 

+ Tools

    + Backup & Restore (BR) <!--tw@qiancai: 7 notes-->

        - Fix the issue where Zstd compression did not take effect in log backup, resulting in uncompressed output. [#18836](https://github.com/tikv/tikv/issues/18836) @[3pointer](https://github.com/3pointer)
        - Fixed a bug that may cause flush operation slow in azure blob storage. [#18410](https://github.com/tikv/tikv/issues/18410) @[YuJuncen](https://github.com/YuJuncen)
        - Fixed a bug that may cause `log truncate` panic when failed to delete file. [#63358](https://github.com/pingcap/tidb/issues/63358) @[YuJuncen](https://github.com/YuJuncen)
        - Fixed a bug that may cause `stats_meta` be zero when checksumming disabled. [#60978](https://github.com/pingcap/tidb/issues/60978) @[Leavrth](https://github.com/Leavrth)
        - Reduced chance of BR restore failure from S3-compatible storage when the S3 server limits bandwidth through traffic shaping. [#18846](https://github.com/tikv/tikv/issues/18846) @[kennytm](https://github.com/kennytm)
        - Fix the issue that the log backup observer loses observation of a region. [#18243](https://github.com/tikv/tikv/issues/18243) @[Leavrth](https://github.com/Leavrth)
        - Fixed a bug that may cause `restore point` fail when there are some special sized table schemas [#63663](https://github.com/pingcap/tidb/issues/63663) @[RidRisR](https://github.com/RidRisR)

    + TiCDC <!--tw@Oreoxmt: 7 notes-->

        - 修复在配置包含虚拟列的 column 类型 partition 分发器时可能导致的 panic 问题 [#12241](https://github.com/pingcap/tiflow/issues/12241) @[wk989898](https://github.com/wk989898)
        - 修复在关闭 ddl puller 时可能引发的 panic 问题 [#12244](https://github.com/pingcap/tiflow/issues/12244) @[wk989898](https://github.com/wk989898)
        - 支持在 filter 中通过设置 `ignore-txn-start-ts` 来过滤不支持的 DDL 类型 [#12286](https://github.com/pingcap/tiflow/issues/12286) @[asddongmen](https://github.com/asddongmen)
        - 修复使用 Azure 下游时可能引起的卡住问题 [#12277] (https://github.com/pingcap/tiflow/issues/12277) @[zurakutsia](https://github.com/zurakutsia)
        - 修复 `drop foreign key` DDL 没有同步到下游的问题 [#12328](https://github.com/pingcap/tiflow/issues/12328) @[3AceShowHand](https://github.com/3AceShowHand)
        - 修复订阅 region 时遇到回滚和预写条目导致的 panic 问题 [#19048](https://github.com/tikv/tikv/issues/19048) @[3AceShowHand](https://github.com/3AceShowHand)
        - 修复 TiKV 断言错误导致的 panic 问题 [#18498](https://github.com/tikv/tikv/issues/18498) @[tharanga](https://github.com/tharanga)
