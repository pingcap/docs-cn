---
title: TiDB 8.1.2 Release Notes
summary: 了解 TiDB 8.1.2 版本的兼容性变更、改进提升和错误修复。
---

# TiDB 8.1.2 Release Notes

发版日期：2024 年 12 月 26 日

TiDB 版本：8.1.2

试用链接：[快速体验](https://docs.pingcap.com/zh/tidb/v8.1/quick-start-with-tidb) | [生产部署](https://docs.pingcap.com/zh/tidb/v8.1/production-deployment-using-tiup) | [下载离线包](https://cn.pingcap.com/product-community/?version=v8.1.2#version-list)

## 兼容性变更

- 新增 TiKV 配置项 [`server.snap-min-ingest-size`](/tikv-configuration-file.md#snap-min-ingest-size-从-v812-版本开始引入)，用于指定 TiKV 在处理 snapshot 时是否采用 ingest 方式的最小阈值。默认值为 `2MiB`。

    - 当 snapshot 大小超过该阈值时，TiKV 会采用 ingest 方式，即将 snapshot 中的 SST 文件导入 RocksDB。这种方式适合处理大文件，导入速度更快。
    - 当 snapshot 大小不超过该阈值时，TiKV 会采用直接写入方式，即将每一条数据逐条写入 RocksDB。这种方式在处理小文件时更高效。

## 改进提升

+ TiDB

    - 添加 Request Unit (RU) 配置监控指标 [#8444](https://github.com/tikv/pd/issues/8444) @[nolouch](https://github.com/nolouch)

+ TiKV

    - 优化空表和小 Region 场景下 Region Merge 的速度 [#17376](https://github.com/tikv/tikv/issues/17376) @[LykxSassinator](https://github.com/LykxSassinator)
    - 优化 TiKV 的 `DiskFull` 检测使之与 RaftEngine 的配置项 `spill-dir` 兼容，确保该特性能够稳定运行 [#17356](https://github.com/tikv/tikv/issues/17356) @[LykxSassinator](https://github.com/LykxSassinator)
    - 优化存在大量 DELETE 版本时 RocksDB 的 compaction 触发机制，以加快磁盘空间回收 [#17269](https://github.com/tikv/tikv/issues/17269) @[AndreMouche](https://github.com/AndreMouche)
    - 支持在线修改 `import.num-threads` 配置项 [#17807](https://github.com/tikv/tikv/issues/17807) @[RidRisR](https://github.com/RidRisR)
    - 将备份恢复侧用于访问 Amazon S3 等外部存储的 SDK 更新为 AWS Rust SDK，替换掉原有的 Rusoto 库，以更好地兼容 AWS 的 IMDSv2 以及 EKS Pod Identity 等新特性 [#12371](https://github.com/tikv/tikv/issues/12371) @[akoshchiy](https://github.com/akoshchiy)

+ TiFlash

    - 提升聚簇索引表在后台回收过期数据的速度 [#9529](https://github.com/pingcap/tiflash/issues/9529) @[JaySon-Huang](https://github.com/JaySon-Huang)
    - 降低 TiFlash 在开启 TLS 后因更新证书而导致 panic 的概率 [#8535](https://github.com/pingcap/tiflash/issues/8535) @[windtalker](https://github.com/windtalker)
    - 减少处理存算分离请求时创建的线程数，避免 TiFlash 计算节点在处理大量请求时崩溃 [#9334](https://github.com/pingcap/tiflash/issues/9334) @[JinheLin](https://github.com/JinheLin)
    - 改进 JOIN 算子的取消机制，使得 JOIN 算子内部能及时响应取消请求 [#9430](https://github.com/pingcap/tiflash/issues/9430) @[windtalker](https://github.com/windtalker)
    - 优化 `LENGTH()` 和 `ASCII()` 函数执行效率 [#9344](https://github.com/pingcap/tiflash/issues/9344) @[xzhangxian1008](https://github.com/xzhangxian1008)
    - 优化在存算分离架构下，TiFlash 读节点 (Compute Node) 从 Amazon S3 下载文件异常时的重试策略 [#9695](https://github.com/pingcap/tiflash/issues/9695) @[JinheLin](https://github.com/JinheLin)

+ Tools

    + Backup & Restore (BR)

        - 减少备份过程中无效日志的打印 [#55902](https://github.com/pingcap/tidb/issues/55902) @[Leavrth](https://github.com/Leavrth)
        - 在进行全量备份时，默认不计算表级别的 checksum (`--checksum=false`) 以提升备份性能 [#56373](https://github.com/pingcap/tidb/issues/56373) @[Tristan1900](https://github.com/Tristan1900)

    + TiCDC

        - 在给 TiCDC 授予 `SUPER` 权限后，TiCDC 支持查询异步执行的 DDL 任务状态，避免因在同一张表上重复执行 DDL 任务而导致执行错误 [#11521](https://github.com/pingcap/tiflow/issues/11521) @[CharlesCheung96](https://github.com/CharlesCheung96)
        - 当下游为 TiDB 且授予 `SUPER` 权限时，TiCDC 支持从下游数据库查询 `ADD INDEX DDL` 的执行状态，以避免某些情况下因重试执行 DDL 语句超时而导致数据同步失败 [#10682](https://github.com/pingcap/tiflow/issues/10682) @[CharlesCheung96](https://github.com/CharlesCheung96)

## 错误修复

+ TiDB

    - 修复集群从 v6.5 升级到 v7.5 或更高版本后，已有 TTL 任务执行意外频繁的问题 [#56539](https://github.com/pingcap/tidb/issues/56539) @[lcwangchao](https://github.com/lcwangchao)
    - 修复在某些情况下，元数据锁使用不当可能导致使用 plan cache 时写入异常数据的问题 [#53634](https://github.com/pingcap/tidb/issues/53634) @[zimulala](https://github.com/zimulala)
    - 修复当 Region 大小超过 96 MiB 时，启动全局排序后执行 `IMPORT INTO` 卡住的问题 [#55374](https://github.com/pingcap/tidb/issues/55374) @[lance6716](https://github.com/lance6716)
    - 修复在使用 `DUMP STATS` 将统计信息转为 JSON 的过程中，直方图上下界数据受损的问题 [#56083](https://github.com/pingcap/tidb/issues/56083) @[hawkingrei](https://github.com/hawkingrei)
    - 修复无法为带别名的多表删除语句 `DELETE` 创建执行计划绑定的问题 [#56726](https://github.com/pingcap/tidb/issues/56726) @[hawkingrei](https://github.com/hawkingrei)
    - 修复 TTL 表的内存泄漏问题 [#56934](https://github.com/pingcap/tidb/issues/56934) @[lcwangchao](https://github.com/lcwangchao)
    - 修复当分区表达式为 `EXTRACT(YEAR FROM col)` 时没有分区裁剪的问题 [#54210](https://github.com/pingcap/tidb/issues/54210) @[mjonss](https://github.com/mjonss)
    - 修复使用 `PLAN REPLAYER` 导入含有 Placement Rule 的表结构时可能报错的问题 [#54961](https://github.com/pingcap/tidb/issues/54961) @[hawkingrei](https://github.com/hawkingrei)
    - 修复由于查询超出 `tidb_mem_quota_query` 设定的内存使用限制，导致终止查询时可能卡住的问题 [#55042](https://github.com/pingcap/tidb/issues/55042) @[yibin87](https://github.com/yibin87)
    - 修复 TiDB 查询在构造 cop task 期间无法被取消的问题 [#55957](https://github.com/pingcap/tidb/issues/55957) @[yibin87](https://github.com/yibin87)
    - 修复在 TTL 任务执行过程中，减小 `tidb_ttl_delete_worker_count` 的值导致任务无法完成的问题 [#55561](https://github.com/pingcap/tidb/issues/55561) @[lcwangchao](https://github.com/lcwangchao)
    - 修复由于 `CAST` 函数不支持显式设置字符集导致报错的问题 [#55677](https://github.com/pingcap/tidb/issues/55677) @[Defined2014](https://github.com/Defined2014)
    - 修复写冲突时 TTL 任务可能无法取消的问题 [#56422](https://github.com/pingcap/tidb/issues/56422) @[YangKeao](https://github.com/YangKeao)
    - 修复 `IndexNestedLoopHashJoin` 中存在数据竞争的问题 [#49692](https://github.com/pingcap/tidb/issues/49692) @[solotzg](https://github.com/solotzg)
    - 修复 `StreamAggExec` 中的空 `groupOffset` 可能会导致 panic 的问题 [#53867](https://github.com/pingcap/tidb/issues/53867) @[xzhangxian1008](https://github.com/xzhangxian1008)
    - 修复执行一条包含关联子查询和 CTE 的查询时，TiDB 可能卡住或返回错误结果的问题 [#55551](https://github.com/pingcap/tidb/issues/55551) @[guo-shaoge](https://github.com/guo-shaoge)
    - 修复添加索引时重试导致数据索引不一致的问题 [#55808](https://github.com/pingcap/tidb/issues/55808) @[lance6716](https://github.com/lance6716)
    - 修复为整数类型的列指定较小的显示宽度时，除法运算可能出现 `out of range` 的问题 [#55837](https://github.com/pingcap/tidb/issues/55837) @[windtalker](https://github.com/windtalker)
    - 修复 `LOAD DATA ... REPLACE INTO` 导致的数据不一致问题 [#56408](https://github.com/pingcap/tidb/issues/56408) @[fzzf678](https://github.com/fzzf678)
    - 修复 `columnEvaluator` 无法识别输入 chunk 中的列引用，导致执行 SQL 报错 `runtime error: index out of range` 的问题 [#53713](https://github.com/pingcap/tidb/issues/53713) @[AilinKid](https://github.com/AilinKid)
    - 修复当公共表表达式 (CTE) 有多个数据消费者时，如果某个消费者在未读取数据时就退出，可能导致非法内存访问的问题 [#55881](https://github.com/pingcap/tidb/issues/55881) @[windtalker](https://github.com/windtalker)
    - 修复取消 TTL 任务时，没有强制 Kill 对应 SQL 的问题 [#56511](https://github.com/pingcap/tidb/issues/56511) @[lcwangchao](https://github.com/lcwangchao)
    - 修复使用 `IMPORT INTO` 语句导入临时表导致 TiDB 崩溃的问题 [#55970](https://github.com/pingcap/tidb/issues/55970) @[D3Hunter](https://github.com/D3Hunter)
    - 修复当查询条件为 `column IS NULL` 访问唯一索引时，优化器将行数错误地估算为 1 的问题 [#56116](https://github.com/pingcap/tidb/issues/56116) @[hawkingrei](https://github.com/hawkingrei)
    - 修复 information schema 缓存未命中导致 stale read 查询延迟上升的问题 [#53428](https://github.com/pingcap/tidb/issues/53428) @[crazycs520](https://github.com/crazycs520)
    - 修复 `UPDATE` 语句更新 `ENUM` 类型的值时更新错误的问题 [#56832](https://github.com/pingcap/tidb/issues/56832) @[xhebox](https://github.com/xhebox)
    - 修复使用 `PLAN REPLAYER` 导入含有外键的表结构时可能报错的问题 [#56456](https://github.com/pingcap/tidb/issues/56456) @[hawkingrei](https://github.com/hawkingrei)
    - 修复关闭 `tidb_ttl_job_enable` 变量后 TTL 任务未被取消的问题 [#57404](https://github.com/pingcap/tidb/issues/57404) @[YangKeao](https://github.com/YangKeao)
    - 修复当 `UPDATE` 或 `DELETE` 语句包含递归的 CTE 时，语句可能报错或不生效的问题 [#55666](https://github.com/pingcap/tidb/issues/55666) @[time-and-fate](https://github.com/time-and-fate)
    - 修复 `INFORMATION_SCHEMA.STATISTICS` 表中 `SUB_PART` 值为空的问题 [#55812](https://github.com/pingcap/tidb/issues/55812) @[Defined2014](https://github.com/Defined2014)
    - 修复查询 TiFlash 系统表的默认超时时间过短的问题 [#57816](https://github.com/pingcap/tidb/issues/57816) @[JaySon-Huang](https://github.com/JaySon-Huang)
    - 修复 `default_collation_for_utf8mb4` 变量的值对 `SET NAMES` 语句不生效的问题 [#56439](https://github.com/pingcap/tidb/issues/56439) @[Defined2014](https://github.com/Defined2014)
    - 修复手动删除 `mysql.tidb_timer` 表中的定时器时，TTL 内部协程可能 panic 的问题 [#57112](https://github.com/pingcap/tidb/issues/57112) @[lcwangchao](https://github.com/lcwangchao)
    - 修复通过 `tidb_ddl_enable_fast_reorg` 开启添加索引加速功能引可能导致 `Duplicate entry` 报错的问题 [#49233](https://github.com/pingcap/tidb/issues/49233) @[lance6716](https://github.com/lance6716)
    - 修复大表非分布式加索引导致索引时间戳为 `0` 的问题 [#57980](https://github.com/pingcap/tidb/issues/57980) @[lance6716](https://github.com/lance6716)

+ TiKV

    - 修复 `resolved-ts.advance-ts-interval` 配置未生效导致 TiKV 重启时，TiCDC 和 Point-in-time recovery (PITR) 的同步延迟大幅上升的问题 [#17107](https://github.com/tikv/tikv/issues/17107) @[MyonKeminta](https://github.com/MyonKeminta)
    - 修复在触发资源管控时，部分任务等待时间过长的问题 [#17589](https://github.com/tikv/tikv/issues/17589) @[glorv](https://github.com/glorv)
    - 修复 Region 合并后，有极小概率导致 TiKV panic 的问题 [#17840](https://github.com/tikv/tikv/issues/17840) @[glorv](https://github.com/glorv)
    - 修复磁盘卡住时，TiKV 无法向 PD 上报心跳的问题 [#17939](https://github.com/tikv/tikv/issues/17939) @[LykxSassinator](https://github.com/LykxSassinator)
    - 修复当 Raft 和 RocksDB 部署在不同磁盘时，慢磁盘检测对 RocksDB 所在磁盘不生效的问题 [#17884](https://github.com/tikv/tikv/issues/17884) @[LykxSassinator](https://github.com/LykxSassinator)
    - 修复过期副本处理 Raft 快照时，由于分裂操作过慢并且随后立即删除新副本，可能导致 TiKV panic 的问题 [#17469](https://github.com/tikv/tikv/issues/17469) @[hbisheng](https://github.com/hbisheng)
    - 修复使用 `RADIANS()` 或 `DEGREES()` 函数时可能导致 TiKV panic 的问题 [#17852](https://github.com/tikv/tikv/issues/17852) @[gengliqi](https://github.com/gengliqi)
    - 修复当大量事务在排队等待同一个 key 上的锁被释放且该 key 被频繁更新时，TiKV 可能因死锁检测压力过大而出现 OOM 的问题 [#17394](https://github.com/tikv/tikv/issues/17394) @[MyonKeminta](https://github.com/MyonKeminta)
    - 修复 Region Split 后可能无法快速选出 Leader 的问题 [#17602](https://github.com/tikv/tikv/issues/17602) @[LykxSassinator](https://github.com/LykxSassinator)
    - 修复读线程在从 Raft Engine 中的 MemTable 读取过时索引时出现的 panic 问题 [#17383](https://github.com/tikv/tikv/issues/17383) @[LykxSassinator](https://github.com/LykxSassinator)
    - 修复删除大表或分区后可能导致的流量控制问题 [#17304](https://github.com/tikv/tikv/issues/17304) @[Connor1996](https://github.com/Connor1996)

+ PD

    - 修复 PD HTTP 客户端重试逻辑可能无效的问题 [#8499](https://github.com/tikv/pd/issues/8499) @[JmPotato](https://github.com/JmPotato)
    - 将 Gin Web Framework 的版本从 v1.9.1 升级到 v1.10.0 以修复潜在的安全问题 [#8643](https://github.com/tikv/pd/issues/8643) @[JmPotato](https://github.com/JmPotato)
    - 修复在 etcd Leader 切换时，PD 无法快速重新选举的问题 [#8823](https://github.com/tikv/pd/issues/8823) @[rleungx](https://github.com/rleungx)
    - 修复设置 `replication.strictly-match-label` 为 `true` 导致 TiFlash 启动失败的问题 [#8480](https://github.com/tikv/pd/issues/8480) @[rleungx](https://github.com/rleungx)
    - 修复 `evict-leader-scheduler` 在使用相同 Store ID 重复创建后无法正常工作的问题 [#8756](https://github.com/tikv/pd/issues/8756) @[okJiang](https://github.com/okJiang)
    - 修复频繁创建随机数生成器导致性能抖动的问题 [#8674](https://github.com/tikv/pd/issues/8674) @[rleungx](https://github.com/rleungx)
    - 修复热点缓存中可能存在的内存泄露问题 [#8698](https://github.com/tikv/pd/issues/8698) @[lhy1024](https://github.com/lhy1024)
    - 修复 label 统计中的内存泄露问题 [#8700](https://github.com/tikv/pd/issues/8700) @[lhy1024](https://github.com/lhy1024)
    - 修复已删除的资源组仍然出现在监控面板中的问题 [#8716](https://github.com/tikv/pd/issues/8716) @[AndreMouche](https://github.com/AndreMouche)
    - 修复微服务模式下 PD leader 切换时，scheduling server 可能出现数据竞争的问题 [#8538](https://github.com/tikv/pd/issues/8538) @[lhy1024](https://github.com/lhy1024)
    - 修复在 `evict-leader-scheduler` 中使用了错误的参数后，PD 不能正确报错且导致部分 scheduler 不可用的问题 [#8619](https://github.com/tikv/pd/issues/8619) @[rleungx](https://github.com/rleungx)
    - 修复资源组 (Resource Group) 选择器对所有面板都未生效的问题 [#56572](https://github.com/pingcap/tidb/issues/56572) @[glorv](https://github.com/glorv)

+ TiFlash

    - 修复当多个 Region 并发进行副本同步时，可能错误触发 Region overlap 检查失败而导致 TiFlash panic 的问题 [#9329](https://github.com/pingcap/tiflash/issues/9329) @[CalvinNeo](https://github.com/CalvinNeo)
    - 修复当 `SUBSTRING()` 函数的第二个参数为负数时，可能返回错误结果的问题 [#9604](https://github.com/pingcap/tiflash/issues/9604) @[guo-shaoge](https://github.com/guo-shaoge)
    - 修复开启延迟物化后，部分查询可能报错的问题 [#9472](https://github.com/pingcap/tiflash/issues/9472) @[Lloyd-Pottiger](https://github.com/Lloyd-Pottiger)
    - 修复当表里含 Bit 类型列并且带有表示非法字符的默认值时，TiFlash 无法解析表 schema 的问题 [#9461](https://github.com/pingcap/tiflash/issues/9461) @[Lloyd-Pottiger](https://github.com/Lloyd-Pottiger)
    - 修复一些 TiFlash 不支持的 JSON 函数被错误地下推到 TiFlash 的问题 [#9444](https://github.com/pingcap/tiflash/issues/9444) @[windtalker](https://github.com/windtalker)
    - 修复在特定情况下 `CAST AS DECIMAL` 函数的返回结果存在正负号错误的问题 [#9301](https://github.com/pingcap/tiflash/issues/9301) @[guo-shaoge](https://github.com/guo-shaoge)
    - 修复在存算分离架构下，TiFlash 写节点的读快照可能没有被及时释放的问题 [#9298](https://github.com/pingcap/tiflash/issues/9298) @[JinheLin](https://github.com/JinheLin)
    - 修复 `SUBSTRING()` 函数不支持部分整数类型的 `pos` 和 `len` 参数导致查询报错的问题 [#9473](https://github.com/pingcap/tiflash/issues/9473) @[gengliqi](https://github.com/gengliqi)
    - 修复使用 `CAST()` 函数将字符串转换为带时区或非法字符的日期时间时，结果错误的问题 [#8754](https://github.com/pingcap/tiflash/issues/8754) @[solotzg](https://github.com/solotzg)
    - 修复当 `LPAD()` 和 `RPAD()` 函数在某些情况下返回错误结果的问题 [#9465](https://github.com/pingcap/tiflash/issues/9465) @[guo-shaoge](https://github.com/guo-shaoge)
    - 修复在存算分离架构下，查询新增列可能返回错误结果的问题 [#9665](https://github.com/pingcap/tiflash/issues/9665) @[zimulala](https://github.com/zimulala)

+ Tools

    + Backup & Restore (BR)

        - 修复日志可能打印加密信息的问题 [#57585](https://github.com/pingcap/tidb/issues/57585) @[kennytm](https://github.com/kennytm)
        - 修复基于 AWS EBS 的快照备份在准备阶段可能失败导致备份卡住的问题 [#52049](https://github.com/pingcap/tidb/issues/52049) @[YuJuncen](https://github.com/YuJuncen)
        - 修复备份恢复的断点路径在一些外部存储中不兼容的问题 [#55265](https://github.com/pingcap/tidb/issues/55265) @[Leavrth](https://github.com/Leavrth)
        - 升级 `k8s.io/api` 库的版本以修复潜在的安全漏洞 [#57790](https://github.com/pingcap/tidb/issues/57790) @[BornChanger](https://github.com/BornChanger)
        - 修复当集群存在大量表但实际数据量较小时，PITR 数据恢复任务可能出现 `Information schema is out of date` 报错的问题 [#57743](https://github.com/pingcap/tidb/issues/57743) @[Tristan1900](https://github.com/Tristan1900)

    + TiCDC

        - 修复 Puller 模块 Resolved TS 延迟监控显示不正确的问题 [#11561](https://github.com/pingcap/tiflow/issues/11561) @[wlwilliamx](https://github.com/wlwilliamx)
        - 修复开启 `enable-table-across-nodes` 后，Region 发生分裂时，表的某些 Span 同步任务可能丢失的问题 [#11675](https://github.com/pingcap/tiflow/issues/11675) @[wk989898](https://github.com/wk989898)
        - 修复 redo 模块无法正确上报错误的问题 [#11744](https://github.com/pingcap/tiflow/issues/11744) @[CharlesCheung96](https://github.com/CharlesCheung96)
        - 修复 TiDB DDL owner 变更导致 DDL 任务的 schema 版本出现非递增时，TiCDC 错误丢弃 DDL 任务的问题 [#11714](https://github.com/pingcap/tiflow/issues/11714) @[wlwilliamx](https://github.com/wlwilliamx)
        - 修复 Changefeed checkpoint 的 **barrier-ts** 监控指标可能不准确的问题 [#11553](https://github.com/pingcap/tiflow/issues/11553) @[3AceShowHand](https://github.com/3AceShowHand)

    + TiDB Data Migration (DM)

        - 修复多个 DM-master 节点可能同时成为 Leader 导致数据不一致的问题 [#11602](https://github.com/pingcap/tiflow/issues/11602) @[GMHDBJD](https://github.com/GMHDBJD)
