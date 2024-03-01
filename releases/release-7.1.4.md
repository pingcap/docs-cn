---
title: TiDB 7.1.4 Release Notes
summary: 了解 TiDB 7.1.4 版本的兼容性变更、改进提升，以及错误修复。
---

# TiDB 7.1.4 Release Notes

发版日期：2023 年 x 月 x 日

TiDB 版本：7.1.4

试用链接：[快速体验](https://docs.pingcap.com/zh/tidb/v7.1/quick-start-with-tidb) | [生产部署](https://docs.pingcap.com/zh/tidb/v7.1/production-deployment-using-tiup) | [下载离线包](https://cn.pingcap.com/product-community/?version=v7.1.4#version-list)

## 兼容性变更

- note [#issue](https://github.com/pingcap/${repo-name}/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
- 为减少日志打印的开销，TiFlash 配置项 `logger.level` 默认值由 `"debug"` 改为 `"info"` [#8641](https://github.com/pingcap/tiflash/issues/8641) @[JaySon-Huang](https://github.com/JaySon-Huang)

## 改进提升

+ TiDB

    - note [#issue](https://github.com/pingcap/tidb/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
    - note [#issue](https://github.com/pingcap/tidb/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
    - (dup): release-7.5.1.md > 改进提升> TiDB - 提升空表加索引的速度 [#49682](https://github.com/pingcap/tidb/issues/49682) @[zimulala](https://github.com/zimulala)
    - (dup): release-7.5.1.md > 改进提升> TiDB - 增强特定情况下 `OUTER JOIN` 转 `INNER JOIN` 的能力 [#49616](https://github.com/pingcap/tidb/issues/49616) @[qw4990](https://github.com/qw4990)

+ TiKV

    - note [#issue](https://github.com/tikv/tikv/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
    - note [#issue](https://github.com/tikv/tikv/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})

+ PD

    - note [#issue](https://github.com/tikv/pd/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
    - note [#issue](https://github.com/tikv/pd/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
    - (dup): release-7.4.0.md > 改进提升> PD - 优化无法连接到备份集群时 PD 自动更新集群状态的速度 [#6883](https://github.com/tikv/pd/issues/6883) @[disksing](https://github.com/disksing)

+ TiFlash

    - note [#issue](https://github.com/pingcap/tiflash/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
    - note [#issue](https://github.com/pingcap/tiflash/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
    - (dup): release-7.5.1.md > 改进提升> TiFlash - 减少后台数据 GC 任务对读、写任务延迟的影响 [#8650](https://github.com/pingcap/tiflash/issues/8650) @[JaySon-Huang](https://github.com/JaySon-Huang)
    - (dup): release-7.5.1.md > 改进提升> TiFlash - 降低磁盘性能抖动对读取延迟的影响 [#8583](https://github.com/pingcap/tiflash/issues/8583) @[JaySon-Huang](https://github.com/JaySon-Huang)

+ Tools

    + Backup & Restore (BR)

        - note [#issue](https://github.com/pingcap/tidb/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
        - note [#issue](https://github.com/pingcap/tidb/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
        - (dup): release-7.5.1.md > 改进提升> Tools> Backup & Restore (BR) - 支持在数据恢复过程中批量创建数据库 [#50767](https://github.com/pingcap/tidb/issues/50767) @[Leavrth](https://github.com/Leavrth)
        - (dup): release-7.5.1.md > 改进提升> Tools> Backup & Restore (BR) - 提升了 `RESTORE` 语句在大数据量表场景下的建表性能 [#48301](https://github.com/pingcap/tidb/issues/48301) @[Leavrth](https://github.com/Leavrth)
        - (dup): release-7.5.1.md > 改进提升> Tools> Backup & Restore (BR) - 使用更优的算法，提升数据恢复过程中 SST 文件合并的速度 [#50613](https://github.com/pingcap/tidb/issues/50613) @[Leavrth](https://github.com/Leavrth)
        - (dup): release-6.5.7.md > 改进提升> Tools> Backup & Restore (BR) - 解决了基于 EBS 的快照备份与 TiDB Lightning 导入的兼容性问题 [#46850](https://github.com/pingcap/tidb/issues/46850) @[YuJuncen](https://github.com/YuJuncen)
        - (dup): release-7.5.1.md > 改进提升> Tools> Backup & Restore (BR) - 支持在数据恢复过程中批量 ingest SST 文件 [#16267](https://github.com/tikv/tikv/issues/16267) @[3pointer](https://github.com/3pointer)
        - (dup): release-7.5.1.md > 改进提升> Tools> Backup & Restore (BR) - 在日志备份过程中，增加了在日志和监控指标中打印影响 global checkpoint 推进的最慢的 Region 的信息 [#51046](https://github.com/pingcap/tidb/issues/51046) @[YuJuncen](https://github.com/YuJuncen)
        - 去除使用 GCS 作为外部存储一个过时的兼容性检查 [#50533](https://github.com/pingcap/tidb/issues/50533) @[lance6716](https://github.com/lance6716)

    + TiCDC

        - note [#issue](https://github.com/pingcap/tiflow/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
        - note [#issue](https://github.com/pingcap/tiflow/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
        - (dup): release-6.5.7.md > 改进提升> Tools> TiCDC - 当下游为 Kafka 时，topic 表达式中允许 `schema` 为可选项，并且支持直接指定 topic 名 [#9763](https://github.com/pingcap/tiflow/issues/9763) @[3AceShowHand](https://github.com/3AceShowHand)
        - (dup): release-7.5.1.md > 改进提升> Tools> TiCDC - 支持[查询 changefeed 的下游同步状态](https://docs.pingcap.com/zh/tidb/v7.1/ticdc-open-api-v2#查询特定同步任务是否完成)，以确认 TiCDC 是否已将所接收到的上游变更完全同步到下游 [#10289](https://github.com/pingcap/tiflow/issues/10289) @[hongyunyan](https://github.com/hongyunyan)
        - (dup): release-7.5.1.md > 改进提升> Tools> TiCDC - 支持在 TiDB Dashboard 中搜索 TiCDC 日志 [#10263](https://github.com/pingcap/tiflow/issues/10263) @[CharlesCheung96](https://github.com/CharlesCheung96)

    + TiDB Data Migration (DM)


    + TiDB Lightning

        - 去除 alter table 时的加锁以提升在多表导入时的性能 [#50105](https://github.com/pingcap/tidb/issues/50105) @[D3Hunter](https://github.com/D3Hunter)

    + Dumpling


    + TiUP

        - note [#issue](https://github.com/pingcap/tiup/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
        - note [#issue](https://github.com/pingcap/tiup/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})

    + TiDB Binlog


## 错误修复

+ TiDB

    - note [#issue](https://github.com/pingcap/tidb/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
    - 修复在 TiFlash 延迟物化在处理关联列时结果可能出错的问题 [#49241](https://github.com/pingcap/tidb/issues/49241) [#51204](https://github.com/pingcap/tidb/issues/51204) @[Lloyd-Pottiger](https://github.com/Lloyd-Pottiger)
    - (dup): release-7.5.1.md > 错误修复> TiDB - 修复开启 `tidb_multi_statement_mode` 模式时，使用索引点查的 `DELETE` 和 `UPDATE` 语句可能会报错的问题 [#50012](https://github.com/pingcap/tidb/issues/50012) @[tangenta](https://github.com/tangenta)
    - (dup): release-7.5.1.md > 错误修复> TiDB - 修复 CTE 查询在重试过程中可能会报错 `type assertion for CTEStorageMap failed` 的问题 [#46522](https://github.com/pingcap/tidb/issues/46522) @[tiancaiamao](https://github.com/tiancaiamao)
    - (dup): release-7.5.1.md > 错误修复> TiDB - 修复构造统计信息时因为 Golang 隐式转换算法导致统计信息误差过大的问题 [#49801](https://github.com/pingcap/tidb/issues/49801) @[qw4990](https://github.com/qw4990)
    - (dup): release-7.6.0.md > 错误修复> TiDB - 修复并发合并分区表的全局统计信息时可能遇到报错的问题 [#48713](https://github.com/pingcap/tidb/issues/48713) @[hawkingrei](https://github.com/hawkingrei)
    - (dup): release-7.5.1.md > 错误修复> TiDB - 修复 TiDB 错误地消除 `group by` 中的常量值导致查询结果出错的问题 [#38756](https://github.com/pingcap/tidb/issues/38756) @[hi-rustin](https://github.com/hi-rustin)
    - (dup): release-7.5.1.md > 错误修复> TiDB - 修复 `BIT` 类型的列在参与一些函数计算时，可能会因为 decode 失败导致查询出错的问题 [#49566](https://github.com/pingcap/tidb/issues/49566) [#50850](https://github.com/pingcap/tidb/issues/50850) [#50855](https://github.com/pingcap/tidb/issues/50855) @[jiyfhust](https://github.com/jiyfhust)
    - (dup): release-7.5.1.md > 错误修复> TiDB - 修复多级嵌套的 `UNION` 查询中 `LIMIT` 无效的问题 [#49874](https://github.com/pingcap/tidb/issues/49874) @[Defined2014](https://github.com/Defined2014)
    - (dup): release-7.5.1.md > 错误修复> TiDB - 修复使用 `AUTO_ID_CACHE=1` 的自增列时，由于并发冲突导致自增 ID 分配报错的问题 [#50519](https://github.com/pingcap/tidb/issues/50519) @[tiancaiamao](https://github.com/tiancaiamao)
    - (dup): release-7.5.1.md > 错误修复> TiDB - 修复查询使用 `NATURAL JOIN` 时可能报错 `Column ... in from clause is ambiguous` 的问题 [#32044](https://github.com/pingcap/tidb/issues/32044) @[AilinKid](https://github.com/AilinKid)
    - (dup): release-7.5.1.md > 错误修复> TiDB - 修复当查询使用了会强制排序的优化器 hint（例如 `STREAM_AGG()`）且其执行计划包含 `IndexMerge` 时，强制排序可能会失效的问题 [#49605](https://github.com/pingcap/tidb/issues/49605) @[AilinKid](https://github.com/AilinKid)
    - (dup): release-7.5.1.md > 错误修复> TiDB - 修复由于 `STREAM_AGG()` 错误处理 CI 导致查询结果有误的问题 [#49902](https://github.com/pingcap/tidb/issues/49902) @[wshwsh12](https://github.com/wshwsh12)
    - (dup): release-7.5.1.md > 错误修复> TiDB - 修复当 `HashJoin` 算子落盘失败时 goroutine 可能泄露的问题 [#50841](https://github.com/pingcap/tidb/issues/50841) @[wshwsh12](https://github.com/wshwsh12)
    - (dup): release-7.5.1.md > 错误修复> TiDB - 修复无法在 `REPLACE INTO` 语句中使用 hint 的问题 [#34325](https://github.com/pingcap/tidb/issues/34325) @[YangKeao](https://github.com/YangKeao)
    - (dup): release-7.5.1.md > 错误修复> TiDB - 修复查询语句包含 `GROUP_CONCANT(ORDER BY)` 语法时，执行可能出错的问题 [#49986](https://github.com/pingcap/tidb/issues/49986) @[AilinKid](https://github.com/AilinKid)
    - (dup): release-7.5.1.md > 错误修复> TiDB - 修复当 JSON 数组为空数组时，使用多值索引访问可能返回错误结果的问题 [#50125](https://github.com/pingcap/tidb/issues/50125) @[YangKeao](https://github.com/YangKeao)
    - (dup): release-7.5.1.md > 错误修复> TiDB - 修复 CTE 查询使用的内存超限时可能会导致 goroutine 泄露的问题 [#50337](https://github.com/pingcap/tidb/issues/50337) @[guo-shaoge](https://github.com/guo-shaoge)
    - (dup): release-7.5.1.md > 错误修复> TiDB - 修复使用旧接口导致表的元信息可能不一致的问题 [#49751](https://github.com/pingcap/tidb/issues/49751) @[hawkingrei](https://github.com/hawkingrei)
    - (dup): release-7.5.1.md > 错误修复> TiDB - 修复执行包含 `ORDER BY` 的 `UNIQUE` 索引点查时可能报错的问题 [#49920](https://github.com/pingcap/tidb/issues/49920) @[jackysp](https://github.com/jackysp)
    - (dup): release-7.5.1.md > 错误修复> TiDB - 修复常见 hint 在 `UNION ALL` 语句中未生效的问题 [#50068](https://github.com/pingcap/tidb/issues/50068) @[hawkingrei](https://github.com/hawkingrei)
    - (dup): release-7.5.1.md > 错误修复> TiDB - 修复包含 IndexHashJoin 算子的查询由于内存超过 `tidb_mem_quota_query` 而卡住的问题 [#49033](https://github.com/pingcap/tidb/issues/49033) @[XuHuaiyu](https://github.com/XuHuaiyu)
    - (dup): release-7.5.1.md > 错误修复> TiDB - 修复包含递归 (`WITH RECURSIVE`) CTE 的 `UPDATE` 或 `DELETE` 语句可能会产生错误结果的问题 [#48969](https://github.com/pingcap/tidb/issues/48969) @[winoros](https://github.com/winoros)
    - (dup): release-7.5.1.md > 错误修复> TiDB - 修复直方图的边界包含 `NULL` 时，直方图统计信息可能无法解析成可读字符串的问题 [#49823](https://github.com/pingcap/tidb/issues/49823) @[AilinKid](https://github.com/AilinKid)
    - (dup): release-7.5.1.md > 错误修复> TiDB - 修复包含 Apply 操作的查询在报错 `fatal error: concurrent map writes` 后导致 TiDB 崩溃的问题 [#50347](https://github.com/pingcap/tidb/issues/50347) @[SeaRise](https://github.com/SeaRise)
    - (dup): release-7.5.1.md > 错误修复> TiDB - 修复使用聚合函数分组计算时可能报错 `Can't find column ...` 的问题 [#50926](https://github.com/pingcap/tidb/issues/50926) @[qw4990](https://github.com/qw4990)
    - (dup): release-7.5.1.md > 错误修复> TiDB - 修复常量传播在处理 `ENUM` 或 `SET` 类型时结果出错的问题 [#49440](https://github.com/pingcap/tidb/issues/49440) @[winoros](https://github.com/winoros)
    - (dup): release-7.5.1.md > 错误修复> TiDB - 修复有依赖关系的两个 DDL 任务的完成时间顺序不正确的问题 [#49498](https://github.com/pingcap/tidb/issues/49498) @[tangenta](https://github.com/tangenta)
    - (dup): release-7.5.1.md > 错误修复> TiDB - 修复如果开启 `tidb_enable_prepared_plan_cache` 变量之后再关闭此变量，使用 `EXECUTE` 语句执行 `PREPARE STMT` 时可能 panic 的问题 [#49344](https://github.com/pingcap/tidb/issues/49344) @[qw4990](https://github.com/qw4990)
    - (dup): release-7.5.1.md > 错误修复> TiDB - 修复在嵌套的 `UNION` 查询中 `LIMIT` 和 `OPRDERBY` 可能无效的问题 [#49377](https://github.com/pingcap/tidb/issues/49377) @[AilinKid](https://github.com/AilinKid)
    - (dup): release-7.5.1.md > 错误修复> TiDB - 修复 `LEADING` hint 在 `UNION ALL` 语句中无法生效的问题 [#50067](https://github.com/pingcap/tidb/issues/50067) @[hawkingrei](https://github.com/hawkingrei)
    - (dup): release-7.5.1.md > 错误修复> TiDB - 修复通过 `COM_STMT_EXECUTE` 方式执行的 `COMMIT` 或 `ROLLBACK` 操作无法结束已超时事务的问题 [#49151](https://github.com/pingcap/tidb/issues/49151) @[zyguan](https://github.com/zyguan)
    - (dup): release-7.5.1.md > 错误修复> TiDB - 缓解当要处理的表的数量或表的分区数量过多时，TiDB 节点 OOM 的问题 [#50077](https://github.com/pingcap/tidb/issues/50077) @[zimulala](https://github.com/zimulala)
    - (dup): release-7.5.1.md > 错误修复> TiDB - 修复不合法的优化器 hint 可能会导致合法 hint 不生效的问题 [#49308](https://github.com/pingcap/tidb/issues/49308) @[hawkingrei](https://github.com/hawkingrei)
    - (dup): release-7.5.1.md > 错误修复> TiDB - 修复在某些时区下夏令时显示有误的问题 [#49586](https://github.com/pingcap/tidb/issues/49586) @[overvenus](https://github.com/overvenus)
    - (dup): release-7.5.1.md > 错误修复> TiDB - 修复使用 `PREPARE` 方式执行 `SELECT INTO OUTFILE` 语句时，应报错却返回执行成功的问题 [#49166](https://github.com/pingcap/tidb/issues/49166) @[qw4990](https://github.com/qw4990)
        - 修复通过 “/upgrade/start” 方式滚动升级时，由于与 PD 交互出现问题从而可能遇到 panic 的问题 [#50152](https://github.com/pingcap/tidb/issues/50152) @[zimulala](https://github.com/zimulala)
        - 修复空表加索引的优化未生效的问题 [#49682](https://github.com/pingcap/tidb/issues/49682) @[zimulala](https://github.com/zimulala)
        - 修复创建大量表或分区时 TiDB OOM 的问题 [#50077](https://github.com/pingcap/tidb/issues/50077) @[zimulala](https://github.com/zimulala)
        - 修复存在网络问题时加索引会导致索引数据不一致的问题 [#49773](https://github.com/pingcap/tidb/issues/49773) @[tangenta](https://github.com/tangenta)
        - 修复 ddl job 执行顺序，避免 TICDC 收到乱序的 ddl [#49498](https://github.com/pingcap/tidb/issues/49498) @[tangenta](https://github.com/tangenta)
        - 修复部分 partition 或者约束的表达式会导致 DDL 卡住的问题 [#50972](https://github.com/pingcap/tidb/issues/50972) @[lcwangchao](https://github.com/lcwangchao)

+ TiKV

    - note [#issue](https://github.com/tikv/tikv/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
    - note [#issue](https://github.com/tikv/tikv/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
    - (dup): release-7.5.1.md > 错误修复> TiKV - 修复 gRPC threads 在检查 `is_shutdown` 时可能出现 panic 的问题 [#16236](https://github.com/tikv/tikv/issues/16236) @[pingyu](https://github.com/pingyu)
    - (dup): release-7.5.1.md > 错误修复> TiKV - 修复 TiDB 和 TiKV 处理 `DECIMAL` 算术乘法截断时结果不一致的问题 [#16268](https://github.com/tikv/tikv/issues/16268) @[solotzg](https://github.com/solotzg)
    - (dup): release-7.5.1.md > 错误修复> TiKV - 修复 `cast_duration_as_time` 可能返回错误结果的问题 [#16211](https://github.com/tikv/tikv/issues/16211) @[gengliqi](https://github.com/gengliqi)
    - (dup): release-7.5.1.md > 错误修复> TiKV - 修复巴西和埃及时区转换错误的问题 [#16220](https://github.com/tikv/tikv/issues/16220) @[overvenus](https://github.com/overvenus)
    - 修复 JSON 整形数值在大于 int64 最大值但是小于 uint64 最大值时会被解析成 float64 导致结果和 TiDB 不一致的问题 [#16537](https://github.com/tikv/tikv/pull/16537) @[YangKeao](https://github.com/YangKeao)

+ PD

    - note [#issue](https://github.com/tikv/pd/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
    - note [#issue](https://github.com/tikv/pd/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
    - (dup): release-7.5.1.md > 错误修复> PD - 修复在不满足副本数量需求时，删除 orphan peer 的问题 [#7584](https://github.com/tikv/pd/issues/7584) @[bufferflies](https://github.com/bufferflies)
    - (dup): release-7.5.0.md > 错误修复> PD - 修复采用自适应同步部署模式 (DR Auto-Sync) 的集群 `available_stores` 计算错误的问题 [#7221](https://github.com/tikv/pd/issues/7221) @[disksing](https://github.com/disksing)
    - (dup): release-7.5.0.md > 错误修复> PD - 修复采用自适应同步部署模式 (DR Auto-Sync) 的集群在 Placement Rule 的配置较复杂时，`canSync` 和 `hasMajority` 可能计算错误的问题 [#7201](https://github.com/tikv/pd/issues/7201) @[disksing](https://github.com/disksing)
    - (dup): release-6.5.6.md > 错误修复> PD - 修复采用自适应同步部署模式 (DR Auto-Sync) 的集群在从 AZ 宕机时主 AZ 不能添加 TiKV 节点的问题 [#7218](https://github.com/tikv/pd/issues/7218) @[disksing](https://github.com/disksing)
    - (dup): release-7.5.1.md > 错误修复> PD - 修复批量查询 Resource Group 可能会导致 PD Panic 的问题 [#7206](https://github.com/tikv/pd/issues/7206) @[nolouch](https://github.com/nolouch)
    - (dup): release-7.5.1.md > 错误修复> PD - 修复使用 `pd-ctl` 查询没有 Leader 的 Region 时可能导致 PD panic 的问题 [#7630](https://github.com/tikv/pd/issues/7630) @[rleungx](https://github.com/rleungx)
    - (dup): release-7.5.1.md > 错误修复> PD - 修复 PD 监控项 `learner-peer-count` 在发生 Leader 切换后未同步旧监控值的问题 [#7728](https://github.com/tikv/pd/issues/7728) @[CabinfeverB](https://github.com/CabinfeverB)
    - (dup): release-7.5.1.md > 错误修复> PD - 修复 PD 在通过 `systemd` 启动时无法读取资源限制的问题 [#7628](https://github.com/tikv/pd/issues/7628) @[bufferflies](https://github.com/bufferflies)

+ TiFlash

    - note [#issue](https://github.com/pingcap/tiflash/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
    - note [#issue](https://github.com/pingcap/tiflash/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
    - (dup): release-7.5.1.md > 错误修复> TiFlash - 修复副本迁移时，因 TiFlash 与 PD 之间网络连接不稳定可能引发的 TiFlash panic 的问题 [#8323](https://github.com/pingcap/tiflash/issues/8323) @[JaySon-Huang](https://github.com/JaySon-Huang)
    - (dup): release-7.5.1.md > 错误修复> TiFlash - 修复 TiFlash 错误处理 `ENUM` 偏移量为 0 的问题 [#8311](https://github.com/pingcap/tiflash/issues/8311) @[solotzg](https://github.com/solotzg)
    - (dup): release-7.5.1.md > 错误修复> TiFlash - 修复 `GREATEST` 或 `LEAST` 函数在包含常量字符串参数时，可能发生的随机无效内存访问的问题 [#8604](https://github.com/pingcap/tiflash/issues/8604) @[windtalker](https://github.com/windtalker)
    - (dup): release-7.5.1.md > 错误修复> TiFlash - 修复 lowerUTF8/upperUTF8 不允许大小写字符占据不同字节数的错误 [#8484](https://github.com/pingcap/tiflash/issues/8484) @[gengliqi](https://github.com/gengliqi)
    - (dup): release-7.5.1.md > 错误修复> TiFlash - 修复成功执行的短查询打印过多信息日志的问题 [#8592](https://github.com/pingcap/tiflash/issues/8592) @[windtalker](https://github.com/windtalker)
    - (dup): release-7.5.1.md > 错误修复> TiFlash - 修复慢查询导致内存使用显著增加的问题 [#8564](https://github.com/pingcap/tiflash/issues/8564) @[JinheLin](https://github.com/JinheLin)
    - (dup): release-7.5.1.md > 错误修复> TiFlash - 修复在执行 `ALTER TABLE ... MODIFY COLUMN ... NOT NULL` 时，将原本可为空的列修改为不可为空之后，导致 TiFlash panic 的问题 [#8419](https://github.com/pingcap/tiflash/issues/8419) @[JaySon-Huang](https://github.com/JaySon-Huang)
    - (dup): release-6.5.8.md > 错误修复> TiFlash - 修复终止查询后 TiFlash 上大量任务被同时取消，由于并发数据冲突导致 TiFlash 崩溃的问题 [#7432](https://github.com/pingcap/tiflash/issues/7432) @[SeaRise](https://github.com/SeaRise)
    - 修复 TiFlash 在有大量远程读时，由于并发数据冲突导致 TiFlash 崩溃的问题 [#8685](https://github.com/pingcap/tiflash/issues/8685) @[zanmato1984](https://github.com/zanmato1984)
    - 修复 anti semi join 在有其他不等值连接条件时，结果可能会出错的问题 [#8791](https://github.com/pingcap/tiflash/issues/8791) @[windtalker](https://github.com/windtalker)

+ Tools

    + Backup & Restore (BR)

        - note [#issue](https://github.com/pingcap/tidb/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
        - note [#issue](https://github.com/pingcap/tidb/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
        - (dup): release-7.5.1.md > 错误修复> Tools> Backup & Restore (BR) - 修复停止日志备份任务导致 TiDB crash 的问题 [#50839](https://github.com/pingcap/tidb/issues/50839) @[YuJuncen](https://github.com/YuJuncen)
        - (dup): release-7.5.1.md > 错误修复> Tools> Backup & Restore (BR) - 修复由于某个 TiKV 节点缺少 Leader 导致数据恢复变慢的问题 [#50566](https://github.com/pingcap/tidb/issues/50566) @[Leavrth](https://github.com/Leavrth)
        - (dup): release-7.5.1.md > 错误修复> Tools> Backup & Restore (BR) - 修复在同一节点上更改 TiKV IP 地址导致日志备份卡住的问题 [#50445](https://github.com/pingcap/tidb/issues/50445) @[3pointer](https://github.com/3pointer)
        - (dup): release-7.5.1.md > 错误修复> Tools> Backup & Restore (BR) - 修复从 S3 读文件内容时出错后无法重试的问题 [#49942](https://github.com/pingcap/tidb/issues/49942) @[Leavrth](https://github.com/Leavrth)
        - (dup): release-7.5.1.md > 错误修复> Tools> Backup & Restore (BR) - 修复从旧版本的备份恢复数据时报错 `Unsupported collation` 的问题 [#49466](https://github.com/pingcap/tidb/issues/49466) @[3pointer](https://github.com/3pointer)
        - 通过加锁避免同时运行多个 log backup truncate 任务 [#49414](https://github.com/pingcap/tidb/issues/49414) @[YuJuncen](https://github.com/YuJuncen)

    + TiCDC

        - note [#issue](https://github.com/pingcap/tiflow/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
        - note [#issue](https://github.com/pingcap/tiflow/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
        - (dup): release-7.5.1.md > 错误修复> Tools> TiCDC - 修复上游表执行了 `TRUNCATE PARTITION` 后 changefeed 报错的问题 [#10522](https://github.com/pingcap/tiflow/issues/10522) @[sdojjy](https://github.com/sdojjy)
        - (dup): release-7.5.1.md > 错误修复> Tools> TiCDC - 修复在极端情况下 changefeed 的 `resolved ts` 不推进的问题 [#10157](https://github.com/pingcap/tiflow/issues/10157) @[sdojjy](https://github.com/sdojjy)
        - (dup): release-7.5.1.md > 错误修复> Tools> TiCDC - 修复 Syncpoint 表可能被错误同步的问题 [#10576](https://github.com/pingcap/tiflow/issues/10576) @[asddongmen](https://github.com/asddongmen)
        - (dup): release-7.5.1.md > 错误修复> Tools> TiCDC - 修复在 `ignore-event` 中设置了过滤掉 `add table partition` 事件后，TiCDC 未将相关分区的其它类型 DML 变更事件同步到下游的问题 [#10524](https://github.com/pingcap/tiflow/issues/10524) @[CharlesCheung96](https://github.com/CharlesCheung96)
        - (dup): release-7.5.1.md > 错误修复> Tools> TiCDC - 修复使用 storage sink 时，在存储服务生成的文件序号可能出现回退的问题 [#10352](https://github.com/pingcap/tiflow/issues/10352) @[CharlesCheung96](https://github.com/CharlesCheung96)
        - (dup): release-7.5.1.md > 错误修复> Tools> TiCDC - 修复并发创建多个 changefeed 时 TiCDC 返回 `ErrChangeFeedAlreadyExists` 错误的问题 [#10430](https://github.com/pingcap/tiflow/issues/10430) @[CharlesCheung96](https://github.com/CharlesCheung96)
        - 修复在 resume changefeed 的时候由于没有检查 changefeed 的 checkpoint-ts 是否小于 TiDB 的 gc safepoint 从而没有及时把 "snapshot lost cased by GC" 错误提示出来 [#10463](https://github.com/pingcap/tiflow/issues/10463) @[sdojjy](https://github.com/sdojjy)
        - 修复 TiCDC 在开启单行数据正确性校验 (Data Integrity Validation for Single-Row Data) 后由于没有正确考虑时区的问题导致 timestamp 类型 checksum 验证失败的问题 [#10573](https://github.com/pingcap/tiflow/issues/10573) @[3AceShowHand](https://github.com/3AceShowHand)

    + TiDB Data Migration (DM)

        - note [#issue](https://github.com/pingcap/tiflow/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
        - note [#issue](https://github.com/pingcap/tiflow/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
        - (dup): release-7.5.1.md > 错误修复> Tools> TiDB Data Migration (DM) - 修复 DM 遇到 `event type truncate not valid` 错误导致升级失败的问题 [#10282](https://github.com/pingcap/tiflow/issues/10282) @[GMHDBJD](https://github.com/GMHDBJD)
        - (dup): release-7.5.1.md > 错误修复> Tools> TiDB Data Migration (DM) - 修复下游表结构包含 `shard_row_id_bits` 时同步任务报错的问题 [#10308](https://github.com/pingcap/tiflow/issues/10308) @[GMHDBJD](https://github.com/GMHDBJD)

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
