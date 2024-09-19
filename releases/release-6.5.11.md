---
title: TiDB 6.5.11 Release Notes
summary: 了解 TiDB 6.5.11 版本的兼容性变更、改进提升，以及错误修复。
---

# TiDB 6.5.11 Release Notes

发版日期：2024 年 9 月 20 日

TiDB 版本：6.5.11

试用链接：[快速体验](https://docs.pingcap.com/zh/tidb/v6.5/quick-start-with-tidb) | [生产部署](https://docs.pingcap.com/zh/tidb/v6.5/production-deployment-using-tiup) | [下载离线包](https://cn.pingcap.com/product-community/?version=v6.5.11#version-list)

## 改进提升

+ TiDB

    - 通过批量删除 TiFlash placement rule 的方式，提升对分区表执行 `TRUNCATE`、`DROP` 后数据 GC 的处理速度 [#54068](https://github.com/pingcap/tidb/issues/54068) @[Lloyd-Pottiger](https://github.com/Lloyd-Pottiger)

+ TiKV

    - 优化存在大量 DELETE 版本时 RocksDB 的 compaction 触发机制，以加快磁盘空间回收 [#17269](https://github.com/tikv/tikv/issues/17269) @[AndreMouche](https://github.com/AndreMouche)

+ TiFlash

    - 减少数据高并发读取下的锁冲突，优化短查询性能 [#9125](https://github.com/pingcap/tiflash/issues/9125) @[JinheLin](https://github.com/JinheLin)
    - 优化 `LENGTH()` 和 `ASCII()` 函数执行效率 [#9344](https://github.com/pingcap/tiflash/issues/9344) @[xzhangxian1008](https://github.com/xzhangxian1008)

+ Tools

    + TiCDC

        - 当下游为 TiDB 且授予 `SUPER` 权限时，TiCDC 支持从下游数据库查询 `ADD INDEX DDL` 的执行状态，以避免某些情况下因重试执行 DDL 语句超时而导致数据同步失败 [#10682](https://github.com/pingcap/tiflow/issues/10682) @[CharlesCheung96](https://github.com/CharlesCheung96)

## 错误修复

+ TiDB

    - 修复递归的 CTE 算子错误地跟踪内存使用的问题 [#54181](https://github.com/pingcap/tidb/issues/54181) @[guo-shaoge](https://github.com/guo-shaoge)
    - 通过重置 `PipelinedWindow` 的 `Open` 方法中的参数，修复当 `PipelinedWindow` 作为 apply 的子节点使用时，由于重复的打开和关闭操作导致重用之前的参数值而发生的意外错误 [#53600](https://github.com/pingcap/tidb/issues/53600) @[XuHuaiyu](https://github.com/XuHuaiyu)
    - 修复事务占用的内存可能被多次重复统计的问题 [#53984](https://github.com/pingcap/tidb/issues/53984) @[ekexium](https://github.com/ekexium)
    - 修复在 `HashJoin` 或 `IndexLookUp` 算子作为 `Apply` 算子的被驱动侧子节点时，由于 `memTracker` 未被析构而导致的内存异常高的问题 [#54005](https://github.com/pingcap/tidb/issues/54005) @[XuHuaiyu](https://github.com/XuHuaiyu)
    - 修复当 SQL 异常中断时，`INDEX_HASH_JOIN` 无法正常退出的问题 [#54688](https://github.com/pingcap/tidb/issues/54688) @[wshwsh12](https://github.com/wshwsh12)
    - 修复来自 DM 同步的表超过索引列最大长度 `max-index-length` 时，同步失败的问题 [#55138](https://github.com/pingcap/tidb/issues/55138) @[lance6716](https://github.com/lance6716)
    - 修复在 `GROUP BY` 语句中引用间接占位符 `?` 无法找到列的问题 [#53872](https://github.com/pingcap/tidb/issues/53872) @[qw4990](https://github.com/qw4990)
    - 修复某些情况下可以创建非法的 `DECIMAL(0,0)` 列类型的问题 [#53779](https://github.com/pingcap/tidb/issues/53779) @[tangenta](https://github.com/tangenta)
    - 修复当 SQL 查询的过滤条件中包含虚拟列，且执行条件中包含 `UnionScan` 时，谓词无法正常下推的问题 [#54870](https://github.com/pingcap/tidb/issues/54870) @[qw4990](https://github.com/qw4990)
    - 修复执行 `SELECT DISTINCT CAST(col AS DECIMAL), CAST(col AS SIGNED) FROM ...` 查询时结果出错的问题 [#53726](https://github.com/pingcap/tidb/issues/53726) @[hawkingrei](https://github.com/hawkingrei)
    - 修复针对 `SELECT ... FOR UPDATE` 复用了错误点查询计划的问题 [#54652](https://github.com/pingcap/tidb/issues/54652) @[qw4990](https://github.com/qw4990)
    - 修复可以创建非严格自增的 RANGE 分区表的问题 [#54829](https://github.com/pingcap/tidb/issues/54829) @[Defined2014](https://github.com/Defined2014)
    - 修复当第一个参数是 `month` 并且第二个参数是负数时，`TIMESTAMPADD()` 函数会进入无限循环的问题 [#54908](https://github.com/pingcap/tidb/issues/54908) @[xzhangxian1008](https://github.com/xzhangxian1008)
    - 修复使用 `auth_socket` 认证插件时，TiDB 在某些情况下未能拒绝不符合身份认证的用户连接的问题 [#54031](https://github.com/pingcap/tidb/issues/54031) @[lcwangchao](https://github.com/lcwangchao)
    - 修复使用分布式框架添加索引期间出现网络分区可能导致数据索引不一致的问题 [#54897](https://github.com/pingcap/tidb/issues/54897) @[tangenta](https://github.com/tangenta)
    - 修复由于查询超出 `tidb_mem_quota_query` 设定的内存使用限制，导致终止查询时可能卡住的问题 [#55042](https://github.com/pingcap/tidb/issues/55042) @[yibin87](https://github.com/yibin87)
    - 修复在某些情况下，元数据锁使用不当可能导致使用 plan cache 时写入异常数据的问题 [#53634](https://github.com/pingcap/tidb/issues/53634) @[zimulala](https://github.com/zimulala)
    - 修复递归 CTE 查询可能导致无效指针的问题 [#54449](https://github.com/pingcap/tidb/issues/54449) @[hawkingrei](https://github.com/hawkingrei)
    - 修复 `mysql.stats_histograms` 表的 `tot_col_size` 列可能为负数的潜在风险 [#55126](https://github.com/pingcap/tidb/issues/55126) @[qw4990](https://github.com/qw4990)
    - 修复当视图定义中使用子查询作为列定义时，通过 `information_schema.columns` 获取列信息返回告警 Warning 1356 的问题 [#54343](https://github.com/pingcap/tidb/issues/54343) @[lance6716](https://github.com/lance6716)
    - 修复 TiDB 关闭连接时，在某些情况下会在日志中报错的问题 [#53689](https://github.com/pingcap/tidb/issues/53689) @[jackysp](https://github.com/jackysp)
    - 修复 `SELECT ... WHERE ... ORDER BY ...` 语句在某些情况下执行效率低的性能问题 [#54969](https://github.com/pingcap/tidb/issues/54969) @[tiancaiamao](https://github.com/tiancaiamao)
    - 修复 `INFORMATION_SCHEMA.STATISTICS` 表中 `SUB_PART` 值为空的问题 [#55812](https://github.com/pingcap/tidb/issues/55812) @[Defined2014](https://github.com/Defined2014)
    - 修复查询被 kill 之后可能返回错误结果而非报错的问题 [#50089](https://github.com/pingcap/tidb/issues/50089) @[D3Hunter](https://github.com/D3Hunter)
    - 修复查询 `INFORMATION_SCHEMA.CLUSTER_SLOW_QUERY` 表可能导致 TiDB panic 的问题 [#54324](https://github.com/pingcap/tidb/issues/54324) @[tiancaiamao](https://github.com/tiancaiamao)
    - 修复 `StreamAggExec` 中的空 `groupOffset` 可能会导致 panic 的问题 [#53867](https://github.com/pingcap/tidb/issues/53867) @[xzhangxian1008](https://github.com/xzhangxian1008)
    - 修复 `Sort` 算子发生落盘且查询出错后，磁盘文件可能没被删除的问题 [#55061](https://github.com/pingcap/tidb/issues/55061) @[wshwsh12](https://github.com/wshwsh12)
    - 修复 `IndexNestedLoopHashJoin` 中存在数据竞争的问题 [#49692](https://github.com/pingcap/tidb/issues/49692) @[solotzg](https://github.com/solotzg)
    - 修复使用 `SHOW COLUMNS` 查看视图中的列时报错的问题 [#54964](https://github.com/pingcap/tidb/issues/54964) @[lance6716](https://github.com/lance6716)
    - 修复 DML 语句中包含嵌套的生成列时报错的问题 [#53967](https://github.com/pingcap/tidb/issues/53967) @[wjhuang2016](https://github.com/wjhuang2016)

+ TiKV

    - 修复当主密钥存储于 KMS (Key Management Service) 时无法轮换主密钥的问题 [#17410](https://github.com/tikv/tikv/issues/17410) @[hhwyt](https://github.com/hhwyt)
    - 修复删除大表或分区后可能导致的流量控制问题 [#17304](https://github.com/tikv/tikv/issues/17304) @[Connor1996](https://github.com/Connor1996)
    - 修复导入已被删除的 `sst_importer` SST 文件导致 TiKV panic 的问题 [#15053](https://github.com/tikv/tikv/issues/15053) @[lance6716](https://github.com/lance6716)
    - 修复处理 Raft 快照时，如果副本分裂操作过慢并且随后立即删除新副本，过期副本可能导致 TiKV panic 的问题 [#17469](https://github.com/tikv/tikv/issues/17469) @[hbisheng](https://github.com/hbisheng)
    - 修复 TiKV 在应用损坏的 Raft 数据快照时反复 panic 的问题 [#15292](https://github.com/tikv/tikv/issues/15292) @[LykxSassinator](https://github.com/LykxSassinator)
    - 修复设置 gRPC 消息的压缩算法 (`grpc-compression-type`) 对 TiKV 发送到 TiDB 的消息不起作用的问题 [#17176](https://github.com/tikv/tikv/issues/17176) @[ekexium](https://github.com/ekexium)
    - 修复 `advance-ts-interval` 配置未被用于限制 CDC 和 log-backup 模块中 `check_leader` 操作的 timeout，导致在某些情况下 TiKV 正常重启时 `resolved_ts` lag 过大的问题 [#17107](https://github.com/tikv/tikv/issues/17107) @[MyonKeminta](https://github.com/MyonKeminta)

+ PD

    - 修复部分日志未脱敏的问题 [#8419](https://github.com/tikv/pd/issues/8419) @[rleungx](https://github.com/rleungx)
    - 修复将 TiKV 配置项 [`coprocessor.region-split-size`](/tikv-configuration-file.md#region-split-size) 设置为小于 1 MiB 的值会导致 PD panic 的问题 [#8323](https://github.com/tikv/pd/issues/8323) @[JmPotato](https://github.com/JmPotato)
    - 修复设置 `replication.strictly-match-label` 为 `true` 导致 TiFlash 启动失败的问题 [#8480](https://github.com/tikv/pd/issues/8480) @[rleungx](https://github.com/rleungx)
    - 修复 PD 在进行 operator 检查时遇到的数据竞争问题 [#8263](https://github.com/tikv/pd/issues/8263) @[lhy1024](https://github.com/lhy1024)

+ TiFlash

    - 修复使用 `CAST()` 函数将字符串转换为带时区或非法字符的日期时间时，结果错误的问题 [#8754](https://github.com/pingcap/tiflash/issues/8754) @[solotzg](https://github.com/solotzg)
    - 修复数据库创建后短时间内被删除时，TiFlash 可能 panic 的问题 [#9266](https://github.com/pingcap/tiflash/issues/9266) @[JaySon-Huang](https://github.com/JaySon-Huang)
    - 修复将 TiFlash 中 SSL 证书配置项设置为空字符串会错误开启 TLS 并导致 TiFlash 启动失败的问题 [#9235](https://github.com/pingcap/tiflash/issues/9235) @[JaySon-Huang](https://github.com/JaySon-Huang)
    - 修复 TiFlash 与任意 PD 之间发生网络分区（即网络连接断开），可能导致读请求超时报错的问题 [#9243](https://github.com/pingcap/tiflash/issues/9243) @[Lloyd-Pottiger](https://github.com/Lloyd-Pottiger)
    - 修复 TiFlash 在处理包含 Outer Join 的查询时可能会 crash 的问题 [#9190](https://github.com/pingcap/tiflash/issues/9190) @[windtalker](https://github.com/windtalker)
    - 修复在一些极端情况下，将数据类型转换为 `DECIMAL` 类型可能导致查询结果出错的问题 [#53892](https://github.com/pingcap/tidb/issues/53892) @[guo-shaoge](https://github.com/guo-shaoge)
    - 修复当集群中长时间频繁执行 `EXCHANGE PARTITION` 和 `DROP TABLE` 操作时，可能导致 TiFlash 表元信息同步缓慢以及查询性能下降的问题 [#9227](https://github.com/pingcap/tiflash/issues/9227) @[JaySon-Huang](https://github.com/JaySon-Huang)

+ Tools

    + Backup & Restore (BR)

        - 修复备份恢复的断点路径在一些外部存储中不兼容的问题 [#55265](https://github.com/pingcap/tidb/issues/55265) @[Leavrth](https://github.com/Leavrth)
        - 修复增量备份过程中扫描 DDL 作业的效率较低的问题 [#54139](https://github.com/pingcap/tidb/issues/54139) @[3pointer](https://github.com/3pointer)
        - 修复断点备份过程中查找 Region leader 中断导致备份性能受影响问题 [#17168](https://github.com/tikv/tikv/issues/17168) @[Leavrth](https://github.com/Leavrth)
        - 修复增量恢复过程中 `ADD INDEX`、`MODIFY COLUMN` 等需要回填的 DDL 可能无法正确恢复的问题 [#54426](https://github.com/pingcap/tidb/issues/54426) @[3pointer](https://github.com/3pointer)
        - 修复当 PITR 日志备份任务失败时，用户停止了该任务后，PD 中与该任务相关的 safepoint 未被正确清除的问题 [#17316](https://github.com/tikv/tikv/issues/17316) @[Leavrth](https://github.com/Leavrth)
        - 修复备份过程中由于 TiKV 没有响应导致备份任务无法结束的问题 [#53480](https://github.com/pingcap/tidb/issues/53480) @[Leavrth](https://github.com/Leavrth)
        - 修复开启日志备份时，BR 日志可能打印权限凭证敏感信息的问题 [#55273](https://github.com/pingcap/tidb/issues/55273) @[RidRisR](https://github.com/RidRisR)

    + TiCDC

        - 修复 Sorter 模块读取磁盘数据时 TiCDC 可能 Panic 的问题 [#10853](https://github.com/pingcap/tiflow/issues/10853) @[hicqu](https://github.com/hicqu)
        - 修复当下游 Kafka 无法访问时，Processor 模块可能卡住的问题 [#11340](https://github.com/pingcap/tiflow/issues/11340) @[asddongmen](https://github.com/asddongmen)

    + TiDB Data Migration (DM)

        - 修复当索引长度超过 `max-index-length` 默认值时数据同步中断的问题 [#11459](https://github.com/pingcap/tiflow/issues/11459) @[michaelmdeng](https://github.com/michaelmdeng)
        - 修复 schema tracker 无法正确处理 LIST 分区表导致 DM 报错的问题 [#11408](https://github.com/pingcap/tiflow/issues/11408) @[lance6716](https://github.com/lance6716)
        - 修复 DM 在同步针对 LIST 分区表的 `ALTER TABLE ... DROP PARTITION` 语句时报错的问题 [#54760](https://github.com/pingcap/tidb/issues/54760) @[lance6716](https://github.com/lance6716)
        - 修复 DM 在处理 `ALTER DATABASE` 语句时未设置默认数据库导致同步报错的问题 [#11503](https://github.com/pingcap/tiflow/issues/11503) @[lance6716](https://github.com/lance6716)

    + TiDB Lightning

        - 修复使用 TiDB Lightning 导入数据时报事务冲突的问题 [#49826](https://github.com/pingcap/tidb/issues/49826) @[lance6716](https://github.com/lance6716)
        - 修复在关闭 TiDB Lightning 的导入模式后进行数据导入时，TiKV 数据可能损坏的问题 [#15003](https://github.com/tikv/tikv/issues/15003) [#47694](https://github.com/pingcap/tidb/issues/47694) @[lance6716](https://github.com/lance6716)
        - 修复使用 TiDB Lightning 导入数据时，重启 TiKV 报错的问题 [#15912](https://github.com/tikv/tikv/issues/15912) @[lance6716](https://github.com/lance6716)