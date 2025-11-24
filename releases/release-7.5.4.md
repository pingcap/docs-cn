---
title: TiDB 7.5.4 Release Notes
summary: 了解 TiDB 7.5.4 版本的兼容性变更、改进提升，以及错误修复。
---

# TiDB 7.5.4 Release Notes

发版日期：2024 年 10 月 15 日

TiDB 版本：7.5.4

试用链接：[快速体验](https://docs.pingcap.com/zh/tidb/v7.5/quick-start-with-tidb) | [生产部署](https://docs.pingcap.com/zh/tidb/v7.5/production-deployment-using-tiup)

## 兼容性变更

- 通过 [TiDB HTTP API](https://github.com/pingcap/tidb/blob/release-7.5/docs/tidb_http_api.md) 获取 DDL 历史任务时，默认获取任务数量的上限为 2048，以避免历史任务数量过多导致 OOM 的问题 [#55711](https://github.com/pingcap/tidb/issues/55711) @[joccau](https://github.com/joccau)

## 改进提升

+ TiDB 

    - `EXPLAIN` 语句支持应用 `tidb_redact_log`，并进一步优化了日志记录的处理逻辑 [#54565](https://github.com/pingcap/tidb/issues/54565) @[hawkingrei](https://github.com/hawkingrei)
    - 优化 TiDB 慢查询的查询速度 [#54630](https://github.com/pingcap/tidb/pull/54630) @[yibin87](https://github.com/yibin87)

+ TiKV

    - 优化存在大量 DELETE 版本时 RocksDB 的 compaction 触发机制，以加快磁盘空间回收 [#17269](https://github.com/tikv/tikv/issues/17269) @[AndreMouche](https://github.com/AndreMouche)
    - 减少 peer message channel 的内存使用 [#16229](https://github.com/tikv/tikv/issues/16229) @[Connor1996](https://github.com/Connor1996)
    - 优化 TiKV 重启时由于需要等待应用之前的日志而造成访问延时抖动的情况，提升了 TiKV 的稳定性 [#15874](https://github.com/tikv/tikv/issues/15874) @[LykxSassinator](https://github.com/LykxSassinator)
    - 优化 TiKV 的 `DiskFull` 检测使之与 RaftEngine 的配置项 `spill-dir` 兼容，确保该特性能够稳定运行 [#17356](https://github.com/tikv/tikv/issues/17356) @[LykxSassinator](https://github.com/LykxSassinator)

+ TiFlash

    - 优化 `LENGTH()` 和 `ASCII()` 函数执行效率 [#9344](https://github.com/pingcap/tiflash/issues/9344) @[xzhangxian1008](https://github.com/xzhangxian1008)
    - 降低 TiFlash 在开启 TLS 后因更新证书而导致 panic 的概率 [#8535](https://github.com/pingcap/tiflash/issues/8535) @[windtalker](https://github.com/windtalker)
    - 改进 JOIN 算子的取消机制，使得 JOIN 算子内部能及时响应取消请求 [#9430](https://github.com/pingcap/tiflash/issues/9430) @[windtalker](https://github.com/windtalker)

+ Tools

    + Backup & Restore (BR)

        - 在 TiKV 下载每个 SST 文件之前，新增对 TiKV 是否有足够磁盘空间的检查；如果空间不足，BR 会终止恢复并返回错误 [#17224](https://github.com/tikv/tikv/issues/17224) @[RidRisR](https://github.com/RidRisR)

    + TiCDC

        - 当下游为 TiDB 且授予 `SUPER` 权限时，TiCDC 支持从下游数据库查询 `ADD INDEX DDL` 的执行状态，以避免某些情况下因重试执行 DDL 语句超时而导致数据同步失败 [#10682](https://github.com/pingcap/tiflow/issues/10682) @[CharlesCheung96](https://github.com/CharlesCheung96)

## 错误修复

+ TiDB

    - 修复表较多的情况下 `FLASHBACK DATABASE` 失败的问题 [#54415](https://github.com/pingcap/tidb/issues/54415) @[lance6716](https://github.com/lance6716)
    - 修复可以创建非严格自增的 RANGE 分区表的问题 [#54829](https://github.com/pingcap/tidb/issues/54829) @[Defined2014](https://github.com/Defined2014)
    - 修复包含 `UNION` 的查询语句可能返回错误结果的问题 [#52985](https://github.com/pingcap/tidb/issues/52985) @[XuHuaiyu](https://github.com/XuHuaiyu)
    - 修复当 SQL 异常中断时，`INDEX_HASH_JOIN` 无法正常退出的问题 [#54688](https://github.com/pingcap/tidb/issues/54688) @[wshwsh12](https://github.com/wshwsh12)
    - 通过重置 `PipelinedWindow` 的 `Open` 方法中的参数，修复当 `PipelinedWindow` 作为 apply 的子节点使用时，由于重复的打开和关闭操作导致重用之前的参数值而发生的意外错误 [#53600](https://github.com/pingcap/tidb/issues/53600) @[XuHuaiyu](https://github.com/XuHuaiyu)
    - 修复 information schema 缓存未命中导致 stale read 查询延迟上升的问题 [#53428](https://github.com/pingcap/tidb/issues/53428) @[crazycs520](https://github.com/crazycs520)
    - 修复 `Sort` 算子发生落盘且查询出错后，磁盘文件可能没被删除的问题 [#55061](https://github.com/pingcap/tidb/issues/55061) @[wshwsh12](https://github.com/wshwsh12)
    - 修复查询被 kill 之后可能返回错误结果而非报错的问题 [#50089](https://github.com/pingcap/tidb/issues/50089) @[D3Hunter](https://github.com/D3Hunter)
    - 修复来自 DM 同步的表超过索引列最大长度 `max-index-length` 时，同步失败的问题 [#55138](https://github.com/pingcap/tidb/issues/55138) @[lance6716](https://github.com/lance6716)
    - 修复 `INFORMATION_SCHEMA.STATISTICS` 表中 `SUB_PART` 值为空的问题 [#55812](https://github.com/pingcap/tidb/issues/55812) @[Defined2014](https://github.com/Defined2014)
    - 修复 DML 语句中包含嵌套的生成列时报错的问题 [#53967](https://github.com/pingcap/tidb/issues/53967) @[wjhuang2016](https://github.com/wjhuang2016)
    - 修复 `mysql.stats_histograms` 表的 `tot_col_size` 列可能为负数的潜在风险 [#55126](https://github.com/pingcap/tidb/issues/55126) @[qw4990](https://github.com/qw4990)
    - 修复 `IndexNestedLoopHashJoin` 中存在数据竞争的问题 [#49692](https://github.com/pingcap/tidb/issues/49692) @[solotzg](https://github.com/solotzg)
    - 修复由于查询超出 `tidb_mem_quota_query` 设定的内存使用限制，导致终止查询时可能卡住的问题 [#55042](https://github.com/pingcap/tidb/issues/55042) @[yibin87](https://github.com/yibin87)
    - 修复 `columnEvaluator` 无法识别输入 chunk 中的列引用，导致执行 SQL 报错 `runtime error: index out of range` 的问题 [#53713](https://github.com/pingcap/tidb/issues/53713) @[AilinKid](https://github.com/AilinKid)
    - 修复 `SELECT ... WHERE ... ORDER BY ...` 语句在某些情况下执行效率低的性能问题 [#54969](https://github.com/pingcap/tidb/issues/54969) @[tiancaiamao](https://github.com/tiancaiamao)
    - 修复 `StreamAggExec` 中的空 `groupOffset` 可能会导致 panic 的问题 [#53867](https://github.com/pingcap/tidb/issues/53867) @[xzhangxian1008](https://github.com/xzhangxian1008)
    - 修复 TiDB 查询在构造 cop task 期间无法被取消的问题 [#55957](https://github.com/pingcap/tidb/issues/55957) @[yibin87](https://github.com/yibin87)
    - 修复为整数类型的列指定较小的显示宽度时，除法运算可能出现 `out of range` 的问题 [#55837](https://github.com/pingcap/tidb/issues/55837) @[windtalker](https://github.com/windtalker)
    - 修复添加唯一索引时可能遇到 `duplicate entry` 的问题 [#56161](https://github.com/pingcap/tidb/issues/56161) @[tangenta](https://github.com/tangenta)
    - 修复使用 `IMPORT INTO` 语句导入临时表导致 TiDB 崩溃的问题 [#55970](https://github.com/pingcap/tidb/issues/55970) @[D3Hunter](https://github.com/D3Hunter)
    - 修复添加索引时重试导致数据索引不一致的问题 [#55808](https://github.com/pingcap/tidb/issues/55808) @[lance6716](https://github.com/lance6716)

+ TiKV

    - 修复过期副本处理 Raft 快照时，由于分裂操作过慢并且随后立即删除新副本，可能导致 TiKV panic 的问题 [#17469](https://github.com/tikv/tikv/issues/17469) @[hbisheng](https://github.com/hbisheng)
    - 修复删除大表或分区后可能导致的流量控制问题 [#17304](https://github.com/tikv/tikv/issues/17304) @[Connor1996](https://github.com/Connor1996)
    - 修复早期版本（早于 v7.1）和之后的版本的 bloom filter 无法兼容的问题 [#17272](https://github.com/tikv/tikv/issues/17272) @[v01dstar](https://github.com/v01dstar)
    - 修复当主密钥存储于 KMS (Key Management Service) 时无法轮换主密钥的问题 [#17410](https://github.com/tikv/tikv/issues/17410) @[hhwyt](https://github.com/hhwyt)
    - 修复 Grafana 上 TiKV 面板的 **Storage async write duration** 监控指标不准确的问题 [#17579](https://github.com/tikv/tikv/issues/17579) @[overvenus](https://github.com/overvenus)
    - 修复当大量事务在排队等待同一个 key 上的锁被释放且该 key 被频繁更新时，TiKV 可能因死锁检测压力过大而出现 OOM 的问题 [#17394](https://github.com/tikv/tikv/issues/17394) @[MyonKeminta](https://github.com/MyonKeminta)

+ PD

    - 修复存在大量 Region 时，无法请求 PD 的 Region API 的问题 [#55872](https://github.com/pingcap/tidb/issues/55872) @[rleungx](https://github.com/rleungx)
    - 修复在 `evict-leader-scheduler` 中使用了错误的参数后，PD 不能正确报错且导致部分 scheduler 不可用的问题 [#8619](https://github.com/tikv/pd/issues/8619) @[rleungx](https://github.com/rleungx)
    - 修复微服务模式下 PD leader 切换时，scheduling server 可能出现数据竞争的问题 [#8538](https://github.com/tikv/pd/issues/8538) @[lhy1024](https://github.com/lhy1024)
    - 修复资源组 (Resource Group) 客户端中未完全删除的 slot 导致分配 token 低于给定值的问题 [#7346](https://github.com/tikv/pd/issues/7346) @[guo-shaoge](https://github.com/guo-shaoge)
    - 修复 `INFORMATION_SCHEMA.RUNAWAY_WATCHES` 表中时间类型不正确的问题 [#54770](https://github.com/pingcap/tidb/issues/54770) @[HuSharp](https://github.com/HuSharp)
    - 修复设置 `replication.strictly-match-label` 为 `true` 导致 TiFlash 启动失败的问题 [#8480](https://github.com/tikv/pd/issues/8480) @[rleungx](https://github.com/rleungx)

+ TiFlash

    - 修复在存算分离架构下，TiFlash 写节点可能重启失败的问题 [#9282](https://github.com/pingcap/tiflash/issues/9282) @[JaySon-Huang](https://github.com/JaySon-Huang)
    - 修复 TiFlash 与任意 PD 之间发生网络分区（即网络连接断开），可能导致读请求超时报错的问题 [#9243](https://github.com/pingcap/tiflash/issues/9243) @[Lloyd-Pottiger](https://github.com/Lloyd-Pottiger)
    - 修复使用 `CAST()` 函数将字符串转换为带时区或非法字符的日期时间时，结果错误的问题 [#8754](https://github.com/pingcap/tiflash/issues/8754) @[solotzg](https://github.com/solotzg)
    - 修复在存算分离架构下，TiFlash 写节点的读快照可能没有被及时释放的问题 [#9298](https://github.com/pingcap/tiflash/issues/9298) @[JinheLin](https://github.com/JinheLin)
    - 修复当表里含 Bit 类型列并且带有表示非法字符的默认值时，TiFlash 无法解析表 schema 的问题 [#9461](https://github.com/pingcap/tiflash/issues/9461) @[Lloyd-Pottiger](https://github.com/Lloyd-Pottiger)
    - 修复开启延迟物化后，部分查询可能报错的问题 [#9472](https://github.com/pingcap/tiflash/issues/9472) @[Lloyd-Pottiger](https://github.com/Lloyd-Pottiger)
    - 修复在一些极端情况下，将数据类型转换为 `DECIMAL` 类型可能导致查询结果出错的问题 [#53892](https://github.com/pingcap/tidb/issues/53892) @[guo-shaoge](https://github.com/guo-shaoge)

+ Tools

    + Backup & Restore (BR)

        - 修复备份过程中由于 TiKV 没有响应导致备份任务无法结束的问题 [#53480](https://github.com/pingcap/tidb/issues/53480) @[Leavrth](https://github.com/Leavrth)
        - 修复备份恢复的断点路径在一些外部存储中不兼容的问题 [#55265](https://github.com/pingcap/tidb/issues/55265) @[Leavrth](https://github.com/Leavrth)
        - 修复当 PITR 日志备份任务失败时，用户停止了该任务后，PD 中与该任务相关的 safepoint 未被正确清除的问题 [#17316](https://github.com/tikv/tikv/issues/17316) @[Leavrth](https://github.com/Leavrth)
        - 修复开启日志备份时，BR 日志可能打印权限凭证敏感信息的问题 [#55273](https://github.com/pingcap/tidb/issues/55273) @[RidRisR](https://github.com/RidRisR)
        - 修复 BR 集成测试用例不稳定的问题，并新增用于模拟快照或者日志备份文件损坏的测试用例 [#53835](https://github.com/pingcap/tidb/issues/53835) @[Leavrth](https://github.com/Leavrth)

    + TiCDC

        - 修复 Changefeed checkpoint 的 **barrier-ts** 监控指标可能不准确的问题 [#11553](https://github.com/pingcap/tiflow/issues/11553) @[3AceShowHand](https://github.com/3AceShowHand)

    + TiDB Data Migration (DM)

        - 修复当索引长度超过 `max-index-length` 默认值时数据同步中断的问题 [#11459](https://github.com/pingcap/tiflow/issues/11459) @[michaelmdeng](https://github.com/michaelmdeng)
        - 修复 DM 在处理 `ALTER DATABASE` 语句时未设置默认数据库导致同步报错的问题 [#11503](https://github.com/pingcap/tiflow/issues/11503) @[lance6716](https://github.com/lance6716)
        - 修复多个 DM-master 节点可能同时成为 Leader 导致数据不一致的问题 [#11602](https://github.com/pingcap/tiflow/issues/11602) @[GMHDBJD](https://github.com/GMHDBJD)

    + TiDB Lightning

        - 修复使用 TiDB Lightning 导入数据时报事务冲突的问题 [#49826](https://github.com/pingcap/tidb/issues/49826) @[lance6716](https://github.com/lance6716)
