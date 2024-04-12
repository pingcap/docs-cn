---
title: TiDB 6.5.9 Release Notes
summary: 了解 TiDB 6.5.9 版本的兼容性变更、改进提升，以及错误修复。
---

# TiDB 6.5.9 Release Notes

发版日期：2024 年 4 月 12 日

TiDB 版本：6.5.9

试用链接：[快速体验](https://docs.pingcap.com/zh/tidb/v6.5/quick-start-with-tidb) | [生产部署](https://docs.pingcap.com/zh/tidb/v6.5/production-deployment-using-tiup) | [下载离线包](https://cn.pingcap.com/product-community/?version=v6.5.9#version-list)

## 兼容性变更

- 在 TiKV 中提供 RocksDB [`track-and-verify-wals-in-manifest`](https://docs.pingcap.com/zh/tidb/v6.5/tikv-configuration-file#track-and-verify-wals-in-manifest-从-v659-版本开始引入) 配置，用于调查 WAL (Write Ahead Log) 可能损坏问题 [#16549](https://github.com/tikv/tikv/issues/16549) @[v01dstar](https://github.com/v01dstar)
- DR Auto-Sync 支持设置 [`wait-recover-timeout`](https://docs.pingcap.com/zh/tidb/v6.5/two-data-centers-in-one-city-deployment#启用自适应同步模式)，用于控制当网络恢复后切换回 `sync-recover` 状态的等待时间 [#6295](https://github.com/tikv/pd/issues/6295) @[disksing](https://github.com/disksing)

## 改进提升

+ TiDB

    - 当设置 `force-init-stats` 为 `true` 时，即 TiDB 启动时等待统计信息初始化完成后再对外提供服务，这一设置不再影响 HTTP server 提供服务，用户仍可查看监控 [#50854](https://github.com/pingcap/tidb/issues/50854) @[hawkingrei](https://github.com/hawkingrei)
    - 优化 `ANALYZE` 语句卡住元数据锁的问题 [#47475](https://github.com/pingcap/tidb/issues/47475) @[wjhuang2016](https://github.com/wjhuang2016)

+ TiKV

    - 删除非必要的 async block 以减少内存使用 [#16540](https://github.com/tikv/tikv/issues/16540) @[overvenus](https://github.com/overvenus)
    - 在 raftstore 线程中避免进行快照文件的 IO 操作，提高 TiKV 稳定性 [#16564](https://github.com/tikv/tikv/issues/16564) @[Connor1996](https://github.com/Connor1996)
    - 增加 peer 和 store 消息的 slow log [#16600](https://github.com/tikv/tikv/issues/16600) @[Connor1996](https://github.com/Connor1996)

+ Tools

    + Backup & Restore (BR)

        - 优化滚动重启场景下日志备份的 Recovery Point Objective (RPO)。现在，在滚动重启期间，日志备份任务的 checkpoint lag 将更小 [#15410](https://github.com/tikv/tikv/issues/15410) @[YuJuncen](https://github.com/YuJuncen)
        - 提高日志备份对 Merge 的容忍度，如果遇到合理的长时间 Merge 操作，日志备份任务不容易进入 Error 状态 [#16554](https://github.com/tikv/tikv/issues/16554) @[YuJuncen](https://github.com/YuJuncen)
        - 在遇到较大的 checkpoint lag 时，日志备份支持自动放弃任务，以避免日志备份长时间阻塞 GC，从而防止集群出现问题 [#50803](https://github.com/pingcap/tidb/issues/50803) @[RidRisR](https://github.com/RidRisR)
        - 缓解了 Region leadership 迁移导致 PITR 日志备份进度延迟变高的问题 [#13638](https://github.com/tikv/tikv/issues/13638) @[YuJuncen](https://github.com/YuJuncen)
        - 使用更优的算法，提升数据恢复过程中 SST 文件合并的速度 [#50613](https://github.com/pingcap/tidb/issues/50613) @[Leavrth](https://github.com/Leavrth)
        - 支持在数据恢复过程中批量 ingest SST 文件 [#16267](https://github.com/tikv/tikv/issues/16267) @[3pointer](https://github.com/3pointer)
        - 移除使用 Google Cloud Storage (GCS) 作为外部存储时一个过时的兼容性检查 [#50533](https://github.com/pingcap/tidb/issues/50533) @[lance6716](https://github.com/lance6716)
        - 在日志备份过程中，增加了在日志和监控指标中打印影响 global checkpoint 推进的最慢的 Region 的信息 [#51046](https://github.com/pingcap/tidb/issues/51046) @[YuJuncen](https://github.com/YuJuncen)
        - 重构 BR 异常处理机制，提高对未知错误的容忍度 [#47656](https://github.com/pingcap/tidb/issues/47656) @[3pointer](https://github.com/3pointer)

## 错误修复

+ TiDB

    - 修复大量创建表时，新表可能缺失 `stats_meta` 信息导致后续的查询估算无法获取准确行数信息的问题 [#36004](https://github.com/pingcap/tidb/issues/36004) @[xuyifangreeneyes](https://github.com/xuyifangreeneyes)
    - 修复已删除的表仍然会计入到 Grafana 的 `Stats Healthy Distribution` 面板的问题 [#39349](https://github.com/pingcap/tidb/issues/39349) @[xuyifangreeneyes](https://github.com/xuyifangreeneyes)
    - 修复当查询涉及 `MemTableScan` 算子时，TiDB 没有处理 SQL 语句中 `WHERE <column_name>` 过滤条件的问题 [#40937](https://github.com/pingcap/tidb/issues/40937) @[zhongzc](https://github.com/zhongzc)
    - 修复当子查询中的 `HAVING` 子句包含关联列时，查询结果可能出错的问题 [#51107](https://github.com/pingcap/tidb/issues/51107) @[hawkingrei](https://github.com/hawkingrei)
    - 修复当使用 CTE（公共表达式）访问缺少统计信息的分区表时，查询结果可能出错的问题 [#51873](https://github.com/pingcap/tidb/issues/51873) @[qw4990](https://github.com/qw4990)
    - 修复当 SQL 语句中包含 `JOIN` 且 `SELECT` 列表只包含常量时，使用 MPP 执行查询可能导致查询结果出错的问题 [#50358](https://github.com/pingcap/tidb/issues/50358) @[yibin87](https://github.com/yibin87)
    - 修复 `AUTO_INCREMENT` 属性在分配自增 ID 时，由于不必要的事务冲突导致 ID 不连续的问题 [#50819](https://github.com/pingcap/tidb/issues/50819) @[tiancaiamao](https://github.com/tiancaiamao)
    - 修复 Grafana 监控指标 `tidb_statistics_auto_analyze_total` 没有显示为整数的问题 [#51051](https://github.com/pingcap/tidb/issues/51051) @[hawkingrei](https://github.com/hawkingrei)
    - 修复并发合并分区表的全局统计信息时可能遇到报错的问题 [#48713](https://github.com/pingcap/tidb/issues/48713) @[hawkingrei](https://github.com/hawkingrei)
    - 修复当列的默认值被删除时，获取该列的默认值会报错的问题 [#50043](https://github.com/pingcap/tidb/issues/50043) [#51324](https://github.com/pingcap/tidb/issues/51324) @[crazycs520](https://github.com/crazycs520)
    - 修复了当列处于 write-only 状态时 `INSERT ignore` 语句无法正确填充默认值的问题 [#40192](https://github.com/pingcap/tidb/issues/40192) @[YangKeao](https://github.com/YangKeao)
    - 修复 `shuffleExec` 意外退出导致 TiDB 崩溃的问题 [#48230](https://github.com/pingcap/tidb/issues/48230) @[wshwsh12](https://github.com/wshwsh12)
    - 修复当 `HashJoin` 算子落盘失败时 goroutine 可能泄露的问题 [#50841](https://github.com/pingcap/tidb/issues/50841) @[wshwsh12](https://github.com/wshwsh12)
    - 修复在一个事务中提交多条语句时重命名表不生效的问题 [#39664](https://github.com/pingcap/tidb/issues/39664) @[tiancaiamao](https://github.com/tiancaiamao)
    - 修复 `IN()` 谓词中包含 `NULL` 时，查询结果错误的问题 [#51560](https://github.com/pingcap/tidb/issues/51560) @[winoros](https://github.com/winoros)
    - 修复一些情况下查询 `BINARY` 类型的 JSON 可能会报错的问题 [#51547](https://github.com/pingcap/tidb/issues/51547) @[YangKeao](https://github.com/YangKeao)
    - 修复并行 Apply 在表为聚簇索引时可能导致结果错误的问题 [#51372](https://github.com/pingcap/tidb/issues/51372) @[guo-shaoge](https://github.com/guo-shaoge)
    - 修复 `init-stats` 流程可能导致 TiDB panic 以及 `load stats` 流程直接退出的问题 [#51581](https://github.com/pingcap/tidb/issues/51581) @[hawkingrei](https://github.com/hawkingrei)
    - 修复 `auto analyze` 在处理分区表时，`tidb_merge_partition_stats_concurrency` 变量未生效的问题 [#47594](https://github.com/pingcap/tidb/issues/47594) @[hawkingrei](https://github.com/hawkingrei)
    - 修复设置统计信息自动更新的时间窗口后，时间窗口外统计信息仍然可能更新的问题 [#49552](https://github.com/pingcap/tidb/issues/49552) @[hawkingrei](https://github.com/hawkingrei)
    - 修复 `approx_percentile` 函数可能导致 TiDB panic 的问题 [#40463](https://github.com/pingcap/tidb/issues/40463) @[xzhangxian1008](https://github.com/xzhangxian1008)
    - 修复 `BIT` 类型的列在参与一些函数计算时，可能会因为 decode 失败导致查询出错的问题 [#49566](https://github.com/pingcap/tidb/issues/49566) [#50850](https://github.com/pingcap/tidb/issues/50850) [#50855](https://github.com/pingcap/tidb/issues/50855) @[jiyfhust](https://github.com/jiyfhust)
    - 修复 CTE 查询使用的内存超限时可能会导致 goroutine 泄露的问题 [#50337](https://github.com/pingcap/tidb/issues/50337) @[guo-shaoge](https://github.com/guo-shaoge)
    - 修复在配置 `force-init-stats` 的情况下，TiDB 没有监听对应端口的问题 [#51473](https://github.com/pingcap/tidb/issues/51473) @[hawkingrei](https://github.com/hawkingrei)
    - 修复主键类型是 `VARCHAR` 时，执行 `ALTER TABLE ... COMPACT TIFLASH REPLICA` 可能会错误地提前结束的问题 [#51810](https://github.com/pingcap/tidb/issues/51810) @[breezewish](https://github.com/breezewish)
    - 修复修改变量 `tidb_server_memory_limit` 后，`tidb_gogc_tuner_threshold` 未进行相应调整的问题 [#48180](https://github.com/pingcap/tidb/issues/48180) @[hawkingrei](https://github.com/hawkingrei)
    - 修复使用聚合函数分组计算时可能报错 `Can't find column ...` 的问题 [#50926](https://github.com/pingcap/tidb/issues/50926) @[qw4990](https://github.com/qw4990)
    - 修复 `REVERSE` 函数在处理 `BIT` 类型列时报错的问题 [#50850](https://github.com/pingcap/tidb/issues/50850) [#50855](https://github.com/pingcap/tidb/issues/50855) @[jiyfhust](https://github.com/jiyfhust)
    - 修复 `INSERT IGNORE` 向正在执行 DDL 的表中批量插入数据时报错的问题 [#50993](https://github.com/pingcap/tidb/issues/50993) @[YangKeao](https://github.com/YangKeao)
    - 修复 TiDB Server 通过 HTTP 接口添加 label 返回成功但不生效的问题 [#51427](https://github.com/pingcap/tidb/issues/51427) @[you06](https://github.com/you06)
    - 修复 `IFNULL` 函数返回的类型和 MySQL 不一致的问题 [#51765](https://github.com/pingcap/tidb/issues/51765) @[YangKeao](https://github.com/YangKeao)
    - 修复 TiDB Server 在初始化完成之前就标记为 Health 的问题 [#51596](https://github.com/pingcap/tidb/issues/51596) @[shenqidebaozi](https://github.com/shenqidebaozi)
    - 修复查询 `TIDB_HOT_REGIONS` 表时结果返回内存表的问题 [#50810](https://github.com/pingcap/tidb/issues/50810) @[Defined2014](https://github.com/Defined2014)
    - 修复 `EXCHANGE PARTITION` 在处理外键时判断错误的问题 [#51807](https://github.com/pingcap/tidb/issues/51807) @[YangKeao](https://github.com/YangKeao)
    - 修复包含 CTE 的查询会导致 TiDB panic 的问题 [#41688](https://github.com/pingcap/tidb/issues/41688) @[srstack](https://github.com/srstack)

+ TiKV

    - 修复 Peer 销毁过程被 apply snapshot 操作中断后，没有在 apply snapshot 完成后继续执行销毁操作的问题 [#16561](https://github.com/tikv/tikv/issues/16561) @[tonyxuqqi](https://github.com/tonyxuqqi)
    - 修复 RocksDB 中非活跃的 WAL (Write Ahead Log) 可能损毁数据的问题 [#16705](https://github.com/tikv/tikv/issues/16705) @[Connor1996](https://github.com/Connor1996)
    - 修复巴西和埃及时区转换错误的问题 [#16220](https://github.com/tikv/tikv/issues/16220) @[overvenus](https://github.com/overvenus)
    - 修复监控指标 `tikv_unified_read_pool_thread_count` 有时没有数据的问题 [#16629](https://github.com/tikv/tikv/issues/16629) @[YuJuncen](https://github.com/YuJuncen)
    - 修复 JSON 整型数值在大于 `INT64` 最大值但小于 `UINT64` 最大值时会被 TiKV 解析成 `FLOAT64` 导致结果和 TiDB 不一致的问题 [#16512](https://github.com/tikv/tikv/issues/16512) @[YangKeao](https://github.com/YangKeao)
    - 修复乐观事务在执行期间被其它事务发起 resolve lock 时，如果事务的 primary key 上之前有通过异步提交 (Async Commit) 或一阶段提交 (1PC) 模式提交的数据，事务的原子性可能有小概率被破坏问题 [#16620](https://github.com/tikv/tikv/issues/16620) @[MyonKeminta](https://github.com/MyonKeminta)

+ PD

    - 修复扩缩容进度显示不准确的问题 [#7726](https://github.com/tikv/pd/issues/7726) @[CabinfeverB](https://github.com/CabinfeverB)
    - 修复调用 `MergeLabels` 函数时存在数据竞争的问题 [#7535](https://github.com/tikv/pd/issues/7535) @[lhy1024](https://github.com/lhy1024)
    - 修复 PD 监控项 `learner-peer-count` 在发生 Leader 切换后未同步旧监控值的问题 [#7728](https://github.com/tikv/pd/issues/7728) @[CabinfeverB](https://github.com/CabinfeverB)
    - 修复 `SHOW CONFIG` 的查询结果包含已废弃的 `trace-region-flow` 配置项的问题 [#7917](https://github.com/tikv/pd/issues/7917) @[rleungx](https://github.com/rleungx)

+ TiFlash

    - 修复副本迁移时，因 TiFlash 与 PD 之间网络连接不稳定可能引发的 TiFlash panic 的问题 [#8323](https://github.com/pingcap/tiflash/issues/8323) @[JaySon-Huang](https://github.com/JaySon-Huang)
    - 修复 TiFlash 发生远程读时可能会 crash 的问题 [#8685](https://github.com/pingcap/tiflash/issues/8685) @[solotzg](https://github.com/solotzg)
    - 修复 `ENUM` 列在 chunk encode 时可能会导致 TiFlash crash 的问题 [#8674](https://github.com/pingcap/tiflash/issues/8674) @[yibin87](https://github.com/yibin87)
    - 修复在非严格 `sql_mode` 下查询带有异常默认值的列可能导致 TiFlash panic 的问题 [#8803](https://github.com/pingcap/tiflash/issues/8803) @[Lloyd-Pottiger](https://github.com/Lloyd-Pottiger)
    - 修复 `TIME` 类型的列在精度修改后，如果发生 Region 迁移、分裂或合并，可能会导致查询出错的问题 [#8601](https://github.com/pingcap/tiflash/issues/8601) @[JaySon-Huang](https://github.com/JaySon-Huang)

+ Tools

    + Backup & Restore (BR)

        - 修复全量备份失败时打印过多日志的问题 [#51572](https://github.com/pingcap/tidb/issues/51572) @[Leavrth](https://github.com/Leavrth)
        - 修复在日志备份任务被暂停后，移除任务无法立即恢复 GC safepoint 的问题 [#52082](https://github.com/pingcap/tidb/issues/52082) @[3pointer](https://github.com/3pointer)
        - 修复在包含 `AUTO_RANDOM` 列的联合聚簇索引中，BR 无法备份 `AUTO_RANDOM` ID 分配进度的问题 [#52255](https://github.com/pingcap/tidb/issues/52255) @[Leavrth](https://github.com/Leavrth)
        - 修复停止日志备份任务导致 TiDB crash 的问题 [#50839](https://github.com/pingcap/tidb/issues/50839) @[YuJuncen](https://github.com/YuJuncen)
        - 修复在某些极端情况下，全量备份因找不到 peer 导致 TiKV panic 的问题 [#16394](https://github.com/tikv/tikv/issues/16394) @[Leavrth](https://github.com/Leavrth)

    + TiCDC

        - 修复恢复 changefeed 时 changefeed 的 `checkpoint-ts` 小于 TiDB 的 GC safepoint，没有及时报错 `snapshot lost caused by GC` 的问题 [#10463](https://github.com/pingcap/tiflow/issues/10463) @[sdojjy](https://github.com/sdojjy)
        - 修复在频繁执行 DDL 的场景中，由于错误的 BarrierTS 导致数据被写入到错误的 CSV 文件的问题 [#10668](https://github.com/pingcap/tiflow/issues/10668) @[lidezhu](https://github.com/lidezhu)
        - 修复 Syncpoint 表可能被错误同步的问题 [#10576](https://github.com/pingcap/tiflow/issues/10576) @[asddongmen](https://github.com/asddongmen)
        - 修复在调度表的同步任务时 TiCDC panic 的问题 [#10613](https://github.com/pingcap/tiflow/issues/10613) @[CharlesCheung96](https://github.com/CharlesCheung96)
        - 修复 KV Client 数据争用导致 TiCDC panic 的问题 [#10718](https://github.com/pingcap/tiflow/issues/10718) @[asddongmen](https://github.com/asddongmen)
        - 修复使用 storage sink 时，在存储服务生成的文件序号可能出现回退的问题 [#10352](https://github.com/pingcap/tiflow/issues/10352) @[CharlesCheung96](https://github.com/CharlesCheung96)
        - 修复 storage sink 场景下无法正常访问 Azure 和 GCS 对象存储的问题 [#10592](https://github.com/pingcap/tiflow/issues/10592) @[CharlesCheung96](https://github.com/CharlesCheung96)
        - 修复 `open-protocol` 的 old value 部分错误地按照 `STRING` 类型而非真正类型输出默认值的问题 [#10803](https://github.com/pingcap/tiflow/issues/10803) @[3AceShowHand](https://github.com/3AceShowHand)
        - 修复当对象存储遇到暂时故障时，启用了最终一致性功能的 changefeed 可能直接失败的问题 [#10710](https://github.com/pingcap/tiflow/issues/10710) @[CharlesCheung96](https://github.com/CharlesCheung96)

    + TiDB Data Migration (DM)

        - 修复上游为 binary 类型主键时丢失数据的问题 [#10672](https://github.com/pingcap/tiflow/issues/10672) @[GMHDBJD](https://github.com/GMHDBJD)

    + TiDB Lightning

        - 修复在扫描数据文件时，遇到不合法符号链接文件而报错的问题 [#49423](https://github.com/pingcap/tidb/issues/49423) @[lance6716](https://github.com/lance6716)