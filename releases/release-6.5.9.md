---
title: TiDB 6.5.9 Release Notes
summary: 了解 TiDB 6.5.9 版本的兼容性变更、改进提升，以及错误修复。
---

# TiDB 6.5.9 Release Notes

发版日期：2024 年 x 月 x 日

TiDB 版本：6.5.9

试用链接：[快速体验](https://docs.pingcap.com/zh/tidb/v6.5/quick-start-with-tidb) | [生产部署](https://docs.pingcap.com/zh/tidb/v6.5/production-deployment-using-tiup) | [下载离线包](https://cn.pingcap.com/product-community/?version=v6.5.9#version-list)

## 兼容性变更

- note [#issue](https://github.com/pingcap/${repo-name}/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})

## 改进提升

+ TiDB

    - note [#issue](https://github.com/pingcap/tidb/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
    - note [#issue](https://github.com/pingcap/tidb/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
    - (dup): release-8.0.0.md > 改进提升> TiDB - 当设置 `force-init-stats` 为 `true` 时，即 TiDB 启动时等待统计信息初始化完成后再对外提供服务，这一设置不再影响 HTTP server 提供服务，用户仍可查看监控 [#50854](https://github.com/pingcap/tidb/issues/50854) @[hawkingrei](https://github.com/hawkingrei)
- 优化了 Analyze 语句卡住 Metadata Lock 的问题。[#47475](https://github.com/pingcap/tidb/issues/47475) @[wjhuang2016](https://github.com/wjhuang2016)

+ TiKV

    - note [#issue](https://github.com/tikv/tikv/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
    - note [#issue](https://github.com/tikv/tikv/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
    - (dup): release-8.0.0.md > 改进提升> TiKV - 增加 peer 和 store 消息的 slow log [#16600](https://github.com/tikv/tikv/issues/16600) @[Connor1996](https://github.com/Connor1996)

+ PD

    - DR Auto-Sync 支持设置 `wait-recover-timeout` [#6295](https://github.com/tikv/pd/issues/6295) @[disksing](https://github.com/disksing)

+ TiFlash

    - note [#issue](https://github.com/pingcap/tiflash/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
    - note [#issue](https://github.com/pingcap/tiflash/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})

+ Tools

    + Backup & Restore (BR)

- 优化了在滚动重启场景 Log Backup 的备份时间点目标（RPO），现在滚动重启时 Log Backup Task 会有更小的 Checkpoint Lag。 [#15410](https://github.com/tikv/tikv/issues/15410) @[YuJuncen](https://github.com/YuJuncen)
- 优化了 Log Backup 对 Merge 的容忍度，现在在遇到合理的长时间 Merge 的时候 Log Backup Task 不容易进入 Error 状态。[#16554](https://github.com/tikv/tikv/issues/16554) @[YuJuncen](https://github.com/YuJuncen)
- 新增了 Log Backup 在遇到较大的 Checkpoint Lag 的时候自动放弃任务的功能，这样可以防止 Log Backup 意外长时间阻塞 GC 导致集群出现问题。[#50803](https://github.com/pingcap/tidb/issues/50803) @[RidRisR](https://github.com/RidRisR) 
        - (dup): release-7.4.0.md > 改进提升> Tools> Backup & Restore (BR) - 缓解了 Region leadership 迁移导致 PITR 日志备份进度延迟变高的问题 [#13638](https://github.com/tikv/tikv/issues/13638) @[YuJuncen](https://github.com/YuJuncen)
        - (dup): release-7.5.1.md > 改进提升> Tools> Backup & Restore (BR) - 使用更优的算法，提升数据恢复过程中 SST 文件合并的速度 [#50613](https://github.com/pingcap/tidb/issues/50613) @[Leavrth](https://github.com/Leavrth)
        - (dup): release-7.5.1.md > 改进提升> Tools> Backup & Restore (BR) - 支持在数据恢复过程中批量 ingest SST 文件 [#16267](https://github.com/tikv/tikv/issues/16267) @[3pointer](https://github.com/3pointer)
        - (dup): release-7.1.4.md > 改进提升> Tools> Backup & Restore (BR) - 移除使用 Google Cloud Storage (GCS) 作为外部存储时一个过时的兼容性检查 [#50533](https://github.com/pingcap/tidb/issues/50533) @[lance6716](https://github.com/lance6716)
        - (dup): release-7.5.1.md > 改进提升> Tools> Backup & Restore (BR) - 在日志备份过程中，增加了在日志和监控指标中打印影响 global checkpoint 推进的最慢的 Region 的信息 [#51046](https://github.com/pingcap/tidb/issues/51046) @[YuJuncen](https://github.com/YuJuncen)
        - (dup): release-7.5.1.md > 改进提升> Tools> Backup & Restore (BR) - 重构 BR 异常处理机制，提高对未知错误的容忍度 [#47656](https://github.com/pingcap/tidb/issues/47656) @[3pointer](https://github.com/3pointer)

    + TiCDC

        - note [#issue](https://github.com/pingcap/tiflow/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})

    + TiDB Data Migration (DM)

        - note [#issue](https://github.com/pingcap/tiflow/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
        - note [#issue](https://github.com/pingcap/tiflow/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})

    + TiDB Lightning

        - note [#issue](https://github.com/pingcap/tidb/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
        - note [#issue](https://github.com/pingcap/tidb/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})

    + Dumpling

        - note [#issue](https://github.com/pingcap/tidb/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
        - note [#issue](https://github.com/pingcap/tidb/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})

    + TiUP

        - note [#issue](https://github.com/pingcap/tiup/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
        - note [#issue](https://github.com/pingcap/tiup/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})

    + TiDB Binlog

        - note [#issue](https://github.com/pingcap/tidb-binlog/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
        - note [#issue](https://github.com/pingcap/tidb-binlog/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})

## 错误修复

+ TiDB

    - note [#issue](https://github.com/pingcap/tidb/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
    - note [#issue](https://github.com/pingcap/tidb/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
    - 修复大量创建表时，新表可能缺失 stats_meta 信息导致后续估算无法获取准确行数信息的问题 [#36004](https://github.com/pingcap/tidb/issues/36004) @[xuyifangreeneyes](https://github.com/xuyifangreeneyes)
    - 修复已经 drop 的表依然会被计入 Grafana 的 Stats Healthy Distribution 面板的问题 [#39349](https://github.com/pingcap/tidb/issues/39349) @[xuyifangreeneyes](https://github.com/xuyifangreeneyes)
    - 修复涉及 `MemTableScan` 算子的查询丢失 SQL 中形如 `WHERE column_name` 的过滤条件的问题 [#40937](https://github.com/pingcap/tidb/issues/40937) @[zhongzc](https://github.com/zhongzc)
    - 修复子查询中的 `HAVING` 子句包含关联列时查询结果可能错误的问题 [#51107](https://github.com/pingcap/tidb/issues/51107) @[hawkingrei](https://github.com/hawkingrei)
    - 修复在 CTE 中访问分区表，且该分区表缺少统计信息时，查询结果可能错误的问题 [#51873](https://github.com/pingcap/tidb/issues/51873) @[qw4990](https://github.com/qw4990)
    - 修复当 SQL 中包含 `JOIN` 且 `SELECT` 列表只包含常量，且使用 MPP 执行时，查询结果可能错误的问题 [#50358](https://github.com/pingcap/tidb/issues/50358) @[yibin87](https://github.com/yibin87)
    - (dup): release-8.0.0.md > 错误修复> TiDB - 修复 `AUTO_INCREMENT` 属性在分配自增 ID 时，由于不必要的事务冲突导致 ID 不连续的问题 [#50819](https://github.com/pingcap/tidb/issues/50819) @[tiancaiamao](https://github.com/tiancaiamao)
    - (dup): release-8.0.0.md > 错误修复> TiDB - 修复 Grafana 监控指标 `tidb_statistics_auto_analyze_total` 没有显示为整数的问题 [#51051](https://github.com/pingcap/tidb/issues/51051) @[hawkingrei](https://github.com/hawkingrei)
    - (dup): release-7.1.4.md > 错误修复> TiDB - 修复并发合并分区表的全局统计信息时可能遇到报错的问题 [#48713](https://github.com/pingcap/tidb/issues/48713) @[hawkingrei](https://github.com/hawkingrei)
    - (dup): release-8.0.0.md > 错误修复> TiDB - 修复当列的默认值被删除时，获取该列的默认值会报错的问题 [#50043](https://github.com/pingcap/tidb/issues/50043) [#51324](https://github.com/pingcap/tidb/issues/51324) @[crazycs520](https://github.com/crazycs520)
    - (dup): release-6.6.0.md > 错误修复> TiDB - 修复了当列处于 write-only 状态时 `INSERT ignore` 语句无法正确填充默认值的问题 [#40192](https://github.com/pingcap/tidb/issues/40192) @[YangKeao](https://github.com/YangKeao)
    - (dup): release-7.6.0.md > 错误修复> TiDB - 修复 `shuffleExec` 意外退出导致 TiDB 崩溃的问题 [#48230](https://github.com/pingcap/tidb/issues/48230) @[wshwsh12](https://github.com/wshwsh12)
    - (dup): release-7.5.1.md > 错误修复> TiDB - 修复当 `HashJoin` 算子落盘失败时 goroutine 可能泄露的问题 [#50841](https://github.com/pingcap/tidb/issues/50841) @[wshwsh12](https://github.com/wshwsh12)
    - (dup): release-7.1.0.md > 错误修复> TiDB - 修复在一个事务中提交多条语句时重命名表不生效的问题 [#39664](https://github.com/pingcap/tidb/issues/39664) @[tiancaiamao](https://github.com/tiancaiamao)
    - (dup): release-8.0.0.md > 错误修复> TiDB - 修复 `IN()` 谓词中包含 `NULL` 时，查询结果错误的问题 [#51560](https://github.com/pingcap/tidb/issues/51560) @[winoros](https://github.com/winoros)
    - (dup): release-8.0.0.md > 错误修复> TiDB - 修复一些情况下查询 `BINARY` 类型的 JSON 可能会报错的问题 [#51547](https://github.com/pingcap/tidb/issues/51547) @[YangKeao](https://github.com/YangKeao)
    - (dup): release-8.0.0.md > 错误修复> TiDB - 修复并行 Apply 在表为聚簇索引时可能导致结果错误的问题 [#51372](https://github.com/pingcap/tidb/issues/51372) @[guo-shaoge](https://github.com/guo-shaoge)
    - (dup): release-8.0.0.md > 错误修复> TiDB - 修复 `init-stats` 流程可能导致 TiDB panic 以及 `load stats` 流程直接退出的问题 [#51581](https://github.com/pingcap/tidb/issues/51581) @[hawkingrei](https://github.com/hawkingrei)
    - (dup): release-7.1.4.md > 错误修复> TiDB - 修复 `auto analyze` 在处理分区表时，`tidb_merge_partition_stats_concurrency` 变量未生效的问题 [#47594](https://github.com/pingcap/tidb/issues/47594) @[hawkingrei](https://github.com/hawkingrei)
    - (dup): release-7.5.1.md > 错误修复> TiDB - 修复设置统计信息自动更新的时间窗口后，时间窗口外统计信息仍然可能更新的问题 [#49552](https://github.com/pingcap/tidb/issues/49552) @[hawkingrei](https://github.com/hawkingrei)
    - (dup): release-7.5.1.md > 错误修复> TiDB - 修复 `approx_percentile` 函数可能导致 TiDB panic 的问题 [#40463](https://github.com/pingcap/tidb/issues/40463) @[xzhangxian1008](https://github.com/xzhangxian1008)
    - (dup): release-7.5.1.md > 错误修复> TiDB - 修复 `BIT` 类型的列在参与一些函数计算时，可能会因为 decode 失败导致查询出错的问题 [#49566](https://github.com/pingcap/tidb/issues/49566) [#50850](https://github.com/pingcap/tidb/issues/50850) [#50855](https://github.com/pingcap/tidb/issues/50855) @[jiyfhust](https://github.com/jiyfhust)
    - (dup): release-7.5.1.md > 错误修复> TiDB - 修复 CTE 查询使用的内存超限时可能会导致 goroutine 泄露的问题 [#50337](https://github.com/pingcap/tidb/issues/50337) @[guo-shaoge](https://github.com/guo-shaoge)
    - (dup): release-8.0.0.md > 错误修复> TiDB - 修复在配置 `force-init-stats` 的情况下，TiDB 没有监听对应端口的问题 [#51473](https://github.com/pingcap/tidb/issues/51473) @[hawkingrei](https://github.com/hawkingrei)
    - (dup): release-8.0.0.md > 错误修复> TiDB - 修复主键类型是 `VARCHAR` 时，执行 `ALTER TABLE ... COMPACT TIFLASH REPLICA` 可能会错误地提前结束的问题 [#51810](https://github.com/pingcap/tidb/issues/51810) @[breezewish](https://github.com/breezewish)
    - (dup): release-8.0.0.md > 错误修复> TiDB - 修复修改变量 `tidb_server_memory_limit` 后，`tidb_gogc_tuner_threshold` 未进行相应调整的问题 [#48180](https://github.com/pingcap/tidb/issues/48180) @[hawkingrei](https://github.com/hawkingrei)
    - (dup): release-7.5.1.md > 错误修复> TiDB - 修复使用聚合函数分组计算时可能报错 `Can't find column ...` 的问题 [#50926](https://github.com/pingcap/tidb/issues/50926) @[qw4990](https://github.com/qw4990)
    - 修复 `reverse` 函数在处理 `bit` 类型列时报错的问题 [#50850](https://github.com/pingcap/tidb/issues/50850), [#50855](https://github.com/pingcap/tidb/issues/50855) @[jiyfhust](https://github.com/jiyfhust)
    - 修复 `insert ignore` 向正在执行 ddl 的表中批量插入时报错的问题 [#50993](https://github.com/pingcap/tidb/issues/50993) @[YangKeao](https://github.com/YangKeao)
    - 修复 TiDB Server 通过 HTTP 接口添加 label 返回成功但不生效的问题 [#51427](https://github.com/pingcap/tidb/issues/51427) @[you06](https://github.com/you06)
    - 修复 `ifnull` 函数返回的类型和 MySQL 不一致的问题 [#51765](https://github.com/pingcap/tidb/issues/51765) @[YangKeao](https://github.com/YangKeao)
    - 修复 TiDB Server 在初始化完成之前就标记为 Health 的问题 [#51596](https://github.com/pingcap/tidb/issues/51596) @[shenqidebaozi](https://github.com/shenqidebaozi)
    - 修复查询 `TIDB_HOT_REGIONS` 表结果会返回内存表的问题 [#50810](https://github.com/pingcap/tidb/issues/50810) @[Defined2014](https://github.com/Defined2014)
    - 修复 `exchange partition` 在处理外键时判断错误的问题 [#51807](https://github.com/pingcap/tidb/issues/51807) @[YangKeao](https://github.com/YangKeao)
    - 修复执行 CTE 函数会 panic 的问题 [#41688](https://github.com/pingcap/tidb/issues/41688) @[srstack](https://github.com/srstack)

+ TiKV

    - note [#issue](https://github.com/tikv/tikv/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
    - note [#issue](https://github.com/tikv/tikv/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
    - (dup): release-7.5.1.md > 错误修复> TiKV - 修复巴西和埃及时区转换错误的问题 [#16220](https://github.com/tikv/tikv/issues/16220) @[overvenus](https://github.com/overvenus)
    - (dup): release-8.0.0.md > 错误修复> TiKV - 修复监控指标 `tikv_unified_read_pool_thread_count` 有时没有数据的问题 [#16629](https://github.com/tikv/tikv/issues/16629) @[YuJuncen](https://github.com/YuJuncen)
    - (dup): release-8.0.0.md > 错误修复> TiKV - 修复 JSON 整型数值在大于 `INT64` 最大值但小于 `UINT64` 最大值时会被 TiKV 解析成 `FLOAT64` 导致结果和 TiDB 不一致的问题 [#16512](https://github.com/tikv/tikv/issues/16512) @[YangKeao](https://github.com/YangKeao)
    - 修复乐观事务被 resolve lock 时，如果事务的 primary 上之前有通过 Async Commit 或 1PC 模式提交的数据，可能有小概率被破坏事务原子性的问题 [#16620](https://github.com/tikv/tikv/issues/16620) @[MyonKeminta](https://github.com/MyonKeminta)

+ PD

    - 修复扩缩容进度展示不准确的问题 [#7726](https://github.com/tikv/pd/issues/7726@[CabinfeverB](https://github.com/CabinfeverB)
    - 修复调用 `MergeLabels` 函数时存在数据竞争的问题 [#7535](https://github.com/tikv/pd/issues/7535) @[lhy1024](https://github.com/lhy1024)
    - (dup): release-7.5.1.md > 错误修复> PD - 修复 PD 监控项 `learner-peer-count` 在发生 Leader 切换后未同步旧监控值的问题 [#7728](https://github.com/tikv/pd/issues/7728) @[CabinfeverB](https://github.com/CabinfeverB)
    - 修复执行 SQL `show config` 时错误显示 `trace-region-flow` 的问题 [#7917](https://github.com/tikv/pd/issues/7917) @[rleungx](https://github.com/rleungx)

+ TiFlash

    - note [#issue](https://github.com/pingcap/tiflash/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
    - note [#issue](https://github.com/pingcap/tiflash/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
    - (dup): release-7.5.1.md > 错误修复> TiFlash - 修复副本迁移时，因 TiFlash 与 PD 之间网络连接不稳定可能引发的 TiFlash panic 的问题 [#8323](https://github.com/pingcap/tiflash/issues/8323) @[JaySon-Huang](https://github.com/JaySon-Huang)
    - 修复 TiFlash 发生远程读时可能会 crash 的问题 [#8685](https://github.com/pingcap/tiflash/issues/8685) @[solotzg](https://github.com/solotzg)
    - (dup): release-8.0.0.md > 错误修复> TiFlash - 修复 `ENUM` 列在 chunk encode 时可能会导致 TiFlash crash 的问题 [#8674](https://github.com/pingcap/tiflash/issues/8674) @[yibin87](https://github.com/yibin87)
    - 修复在非严格 sql_mode 下创建带异常默认值的列可能导致 TiFlash panic 的问题 [#8803](https://github.com/pingcap/tiflash/issues/8803) @[Lloyd-Pottiger](https://github.com/Lloyd-Pottiger)
    - 修复在 `TIME` 类型的列精度修改之后，当 Region 迁移、分裂或者合并后，可能导致查询出错的问题 [#8601](https://github.com/pingcap/tiflash/issues/8601) @[JaySon-Huang](https://github.com/JaySon-Huang)

+ Tools

    + Backup & Restore (BR)

- 修复了使用 Coarse-grained Split Region 策略 Restore 失败时日志太过繁冗的问题。 [#51572](https://github.com/pingcap/tidb/issues/51572) @[Leavrth](https://github.com/Leavrth)
- 修复了在 Log Backup Task 被暂停之后，移除 Task 不能马上恢复 GC Safepoint 的问题。 [#52082](https://github.com/pingcap/tidb/issues/52082) @[3pointer](https://github.com/3pointer)
- 修复了在联合聚簇索引中包含 AUTO_RANDOM 列的时候，BR 不会备份 AUTO_RANDOM ID 分配进度的问题。[#52255](https://github.com/pingcap/tidb/issues/52255) @[Leavrth](https://github.com/Leavrth)
        - (dup): release-7.5.1.md > 错误修复> Tools> Backup & Restore (BR) - 修复停止日志备份任务导致 TiDB crash 的问题 [#50839](https://github.com/pingcap/tidb/issues/50839) @[YuJuncen](https://github.com/YuJuncen)
        - (dup): release-8.0.0.md > 错误修复> Tools> Backup & Restore (BR) - 修复在某些极端情况下，全量备份因找不到 peer 导致 TiKV panic 的问题 [#16394](https://github.com/tikv/tikv/issues/16394) @[Leavrth](https://github.com/Leavrth)

    + TiCDC

        - note [#issue](https://github.com/pingcap/tiflow/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
        - note [#issue](https://github.com/pingcap/tiflow/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
        - (dup): release-8.0.0.md > 错误修复> Tools> TiCDC - 修复恢复 changefeed 时 changefeed 的 `checkpoint-ts` 小于 TiDB 的 GC safepoint，没有及时报错 `snapshot lost caused by GC` 的问题 [#10463](https://github.com/pingcap/tiflow/issues/10463) @[sdojjy](https://github.com/sdojjy)
        - (dup): release-8.0.0.md > 错误修复> Tools> TiCDC - 修复在频繁执行 DDL 的场景中，由于错误的 BarrierTS 导致数据被写入到错误的 CSV 文件的问题 [#10668](https://github.com/pingcap/tiflow/issues/10668) @[lidezhu](https://github.com/lidezhu)
        - (dup): release-7.5.1.md > 错误修复> Tools> TiCDC - 修复 Syncpoint 表可能被错误同步的问题 [#10576](https://github.com/pingcap/tiflow/issues/10576) @[asddongmen](https://github.com/asddongmen)
        - (dup): release-8.0.0.md > 错误修复> Tools> TiCDC - 修复在调度表的同步任务时 TiCDC panic 的问题 [#10613](https://github.com/pingcap/tiflow/issues/10613) @[CharlesCheung96](https://github.com/CharlesCheung96)
        - (dup): release-8.0.0.md > 错误修复> Tools> TiCDC - 修复 KV Client 数据争用导致 TiCDC panic 的问题 [#10718](https://github.com/pingcap/tiflow/issues/10718) @[asddongmen](https://github.com/asddongmen)
        - (dup): release-7.5.1.md > 错误修复> Tools> TiCDC - 修复使用 storage sink 时，在存储服务生成的文件序号可能出现回退的问题 [#10352](https://github.com/pingcap/tiflow/issues/10352) @[CharlesCheung96](https://github.com/CharlesCheung96)
        - 修复 storage sink 场景下无法正常访问 azure 和 gcs 对象存储的问题 [#10592](https://github.com/pingcap/tiflow/issues/10592) @[CharlesCheung96](https://github.com/CharlesCheung96)
        - 修复 open-protocol 的 old value 部分错误的按照 string 类型而非真正类型输出默认值的问题 [#10803](https://github.com/pingcap/tiflow/issues/10803)，@[3AceShowHand](https://github.com/3AceShowHand)
        - 修复了当对象存储遇到暂时故障时，启用了最终一致性功能的 changefeed 可能直接失败的问题，[#10710](https://github.com/pingcap/tiflow/issues/10710) @[CharlesCheung96](https://github.com/CharlesCheung96)

    + TiDB Data Migration (DM)

        - note [#issue](https://github.com/pingcap/tiflow/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
        - note [#issue](https://github.com/pingcap/tiflow/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
        - (dup): release-8.0.0.md > 错误修复> Tools> TiDB Data Migration (DM) - 修复上游为 binary 类型主键时丢失数据的问题 [#10672](https://github.com/pingcap/tiflow/issues/10672) @[GMHDBJD](https://github.com/GMHDBJD)

    + TiDB Lightning

        - note [#issue](https://github.com/pingcap/tidb/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
        - note [#issue](https://github.com/pingcap/tidb/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
        - (dup): release-8.0.0.md > 错误修复> Tools> TiDB Lightning - 修复在扫描数据文件时，遇到不合法符号链接文件而报错的问题 [#49423](https://github.com/pingcap/tidb/issues/49423) @[lance6716](https://github.com/lance6716)

    + Dumpling

        - note [#issue](https://github.com/pingcap/tidb/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
        - note [#issue](https://github.com/pingcap/tidb/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})

    + TiUP

        - note [#issue](https://github.com/pingcap/tiup/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
        - note [#issue](https://github.com/pingcap/tiup/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})

    + TiDB Binlog

        - note [#issue](https://github.com/pingcap/tidb-binlog/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
        - note [#issue](https://github.com/pingcap/tidb-binlog/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
