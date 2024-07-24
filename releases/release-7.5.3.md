---
title: TiDB 7.5.3 Release Notes
summary: 了解 TiDB 7.5.3 版本的兼容性变更、改进提升，以及错误修复。
---

# TiDB 7.5.3 Release Notes

发版日期：2024 年 x 月 x 日

TiDB 版本：7.5.3

试用链接：[快速体验](https://docs.pingcap.com/zh/tidb/v7.5/quick-start-with-tidb) | [生产部署](https://docs.pingcap.com/zh/tidb/v7.5/production-deployment-using-tiup) | [下载离线包](https://cn.pingcap.com/product-community/?version=v7.5.3#version-list)

## 兼容性变更

- 新增系统表 [`INFORMATION_SCHEMA.KEYWORDS`](/information-schema/information-schema-keywords.md) 用来展示 TiDB 支持的所有关键字的信息 [#48801](https://github.com/pingcap/tidb/issues/48801) @[dveeden](https://github.com/dveeden)

## 改进提升

+ TiDB

    - note [#issue](https://github.com/pingcap/tidb/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
    - note [#issue](https://github.com/pingcap/tidb/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
    - (dup): release-8.2.0.md > 改进提升> TiDB - 通过批量删除 TiFlash placement rule 的方式，提升对分区表执行 `TRUNCATE`、`DROP` 后数据 GC 的处理速度 [#54068](https://github.com/pingcap/tidb/issues/54068) @[Lloyd-Pottiger](https://github.com/Lloyd-Pottiger)

+ TiKV

    - note [#issue](https://github.com/tikv/tikv/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
    - note [#issue](https://github.com/tikv/tikv/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
    - 删除非必要的 async block 以减少内存使用 [#16540](https://github.com/tikv/tikv/issues/16540) @[overvenus](https://github.com/overvenus)

+ PD

    - note [#issue](https://github.com/tikv/pd/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
    - note [#issue](https://github.com/tikv/pd/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})

+ TiFlash

    - note [#issue](https://github.com/pingcap/tiflash/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
    - note [#issue](https://github.com/pingcap/tiflash/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
    - (dup): release-8.1.0.md > 改进提升> TiFlash - 降低 TiFlash 在开启 TLS 后因更新证书而导致 panic 的概率 [#8535](https://github.com/pingcap/tiflash/issues/8535) @[windtalker](https://github.com/windtalker)
    - (dup): release-8.2.0.md > 改进提升> TiFlash - 减少数据高并发读取下的锁冲突，优化短查询性能 [#9125](https://github.com/pingcap/tiflash/issues/9125) @[JinheLin](https://github.com/JinheLin)

+ Tools

    + Backup & Restore (BR)

        - note [#issue](https://github.com/pingcap/tidb/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
        - note [#issue](https://github.com/pingcap/tidb/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
        - (dup): release-8.2.0.md > 改进提升> Tools> Backup & Restore (BR) - 去掉除了 `br log restore` 子命令之外其它 `br log` 子命令对 TiDB `domain` 数据结构的载入，降低内存消耗 [#52088](https://github.com/pingcap/tidb/issues/52088) @[Leavrth](https://github.com/Leavrth)
        - (dup): release-6.5.9.md > 改进提升> Tools> Backup & Restore (BR) - 在遇到较大的 checkpoint lag 时，日志备份支持自动放弃任务，以避免日志备份长时间阻塞 GC，从而防止集群出现问题 [#50803](https://github.com/pingcap/tidb/issues/50803) @[RidRisR](https://github.com/RidRisR)
        - (dup): release-6.5.10.md > 改进提升> Tools> Backup & Restore (BR) - 增加由于 DNS 错误而导致的失败的重试次数 [#53029](https://github.com/pingcap/tidb/issues/53029) @[YuJuncen](https://github.com/YuJuncen)
        - (dup): release-8.1.0.md > 改进提升> Tools> Backup & Restore (BR) - 增加 PITR 集成测试用例，覆盖对日志备份与添加索引加速功能的兼容性测试 [#51987](https://github.com/pingcap/tidb/issues/51987) @[Leavrth](https://github.com/Leavrth)
        - 增加对阿里云使用环境变量设置访问身份的支持 [#45551](https://github.com/pingcap/tidb/issues/45551) @[RidRisR](https://github.com/RidRisR)

    + TiCDC

        - note [#issue](https://github.com/pingcap/tiflow/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
        - (dup): release-6.5.10.md > 改进提升> Tools> TiCDC - 支持当下游为消息队列 (Message Queue, MQ) 或存储服务时直接输出原始事件 [#11211](https://github.com/pingcap/tiflow/issues/11211) @[CharlesCheung96](https://github.com/CharlesCheung96)

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
    - 修复加载 index 统计信息可能会造成内存泄漏的问题 [#54022](https://github.com/pingcap/tidb/issues/54022) @[hi-rustin](https://github.com/hi-rustin)
    - 修复了 update 操作可以触发 stats cache的淘汰机制 [#53742](https://github.com/pingcap/tidb/issues/53742) @[hawkingrei](https://github.com/hawkingrei)
    - 修复了在 Group By 语句中的引用间接占位符 ？会无法找到列的问题 [#53872] https://github.com/pingcap/tidb/issues/53872 @[qw4990](https://github.com/qw4990)
    - 修复当排序规则为 utf8_bin 或 utf8mb4_bin 时意外消除“length()”条件的错误 [#53730](https://github.com/pingcap/tidb/issues/53730) @[elsa0520](https://github.com/elsa0520)
    - 修复插入大科学记数法数字时的行为，使其与 mysql 保持一致 [#47787](https://github.com/pingcap/tidb/issues/47787) @[qw4990](https://github.com/qw4990)
    - 修复递归 CTE 查询中可能会导致的无效指针 [#54449](https://github.com/pingcap/tidb/issues/54449) @[hawkingrei](https://github.com/hawkingrei)
    - 修复统计数据在遇到重复时应该更新 stats_history 表，而不是现实插入 duplicate 错误 [#47539](https://github.com/pingcap/tidb/issues/47539) @[Defined2014](https://github.com/Defined2014)
    - 修复了包含 Limit 的非关联子查询列剪裁不完善导致产生不必要回表的问题 [#54213](https://github.com/pingcap/tidb/issues/54213) @[qw4990](https://github.com/qw4990)
    - Fixed the issue of abnormally high memory usage caused by memTracker not being detached in HashJoin and IndexLookUp operators when used as the inner side of the Apply operator. [#54005](https://github.com/pingcap/tidb/issues/54005) @[XuHuaiyu](https://github.com/XuHuaiyu)
    - Fix the issue that recursive CTE operator tracks memory usage incorrectly. [#54181](https://github.com/pingcap/tidb/issues/54181) @[guo-shaoge](https://github.com/guo-shaoge)
    - 修复了一些事务 buffer 内存被重复统计的问题 [#53984](https://github.com/pingcap/tidb/issues/53984) @[ekexium](https://github.com/ekexium)
    - note [#issue](https://github.com/pingcap/tidb/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
    - note [#issue](https://github.com/pingcap/tidb/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
    - (dup): release-6.5.10.md > 错误修复> TiDB - 修复并发执行 `CREATE OR REPLACE VIEW` 可能报错 `table doesn't exist` 的问题 [#53673](https://github.com/pingcap/tidb/issues/53673) @[tangenta](https://github.com/tangenta)
    - (dup): release-8.2.0.md > 错误修复> TiDB - 修复在包含数据修改操作的事务中查询带有虚拟列的表时，查询结果可能错误的问题 [#53951](https://github.com/pingcap/tidb/issues/53951) @[qw4990](https://github.com/qw4990)
    - (dup): release-8.2.0.md > 错误修复> TiDB - 修复执行 `SELECT DISTINCT CAST(col AS DECIMAL), CAST(col AS SIGNED) FROM ...` 查询时结果出错的问题 [#53726](https://github.com/pingcap/tidb/issues/53726) @[hawkingrei](https://github.com/hawkingrei)
    - (dup): release-6.5.10.md > 错误修复> TiDB - 修复使用 Optimizer Hints 时，可能输出错误的 WARNINGS 信息的问题 [#53767](https://github.com/pingcap/tidb/issues/53767) @[hawkingrei](https://github.com/hawkingrei)
    - (dup): release-8.2.0.md > 错误修复> TiDB - 修复某些情况下可以创建非法的 `DECIMAL(0,0)` 列类型的问题 [#53779](https://github.com/pingcap/tidb/issues/53779) @[tangenta](https://github.com/tangenta)
    - (dup): release-8.2.0.md > 错误修复> TiDB - 修复 `memory_quota` Hint 在子查询中可能不生效的问题 [#53834](https://github.com/pingcap/tidb/issues/53834) @[qw4990](https://github.com/qw4990)
    - (dup): release-8.2.0.md > 错误修复> TiDB - 修复 JSON 相关函数在某些情况下报错信息与 MySQL 不一致的问题 [#53799](https://github.com/pingcap/tidb/issues/53799) @[dveeden](https://github.com/dveeden)
    - (dup): release-8.2.0.md > 错误修复> TiDB - 修复在某些情况下，元数据锁使用不当可能导致使用 plan cache 时写入异常数据的问题 [#53634](https://github.com/pingcap/tidb/issues/53634) @[zimulala](https://github.com/zimulala)
    - (dup): release-6.5.10.md > 错误修复> TiDB - 修复查询中的某些过滤条件可能导致 planner 模块发生 `invalid memory address or nil pointer dereference` 报错的问题 [#53582](https://github.com/pingcap/tidb/issues/53582) [#53580](https://github.com/pingcap/tidb/issues/53580) [#53594](https://github.com/pingcap/tidb/issues/53594) [#53603](https://github.com/pingcap/tidb/issues/53603) @[YangKeao](https://github.com/YangKeao)
    - (dup): release-8.2.0.md > 错误修复> TiDB - 修复在事务内的语句被 OOM 终止之后，如果在当前事务内继续执行下一条语句，可能报错 `Trying to start aggressive locking while it's already started` 并发生 panic 的问题 [#53540](https://github.com/pingcap/tidb/issues/53540) @[MyonKeminta](https://github.com/MyonKeminta)
    - (dup): release-8.2.0.md > 错误修复> TiDB - 修复执行 `ALTER TABLE ... REMOVE PARTITIONING` 后可能导致数据丢失的问题 [#53385](https://github.com/pingcap/tidb/issues/53385) @[mjonss](https://github.com/mjonss)
    - (dup): release-6.5.10.md > 错误修复> TiDB - 修复使用 `PREPARE`/`EXECUTE` 方式执行带 `CONV` 表达式的语句，且 `CONV` 表达式包含 `?` 参数时，多次执行可能导致查询结果错误的问题 [#53505](https://github.com/pingcap/tidb/issues/53505) @[qw4990](https://github.com/qw4990)
    - (dup): release-8.2.0.md > 错误修复> TiDB - 修复使用 `auth_socket` 认证插件时，TiDB 在某些情况下未能拒绝不符合身份认证的用户连接的问题 [#54031](https://github.com/pingcap/tidb/issues/54031) @[lcwangchao](https://github.com/lcwangchao)
    - (dup): release-6.5.10.md > 错误修复> TiDB - 修复 information schema 缓存未命中导致 stale read 查询延迟上升的问题 [#53428](https://github.com/pingcap/tidb/issues/53428) @[crazycs520](https://github.com/crazycs520)
    - (dup): release-6.5.10.md > 错误修复> TiDB - 修复 `INFORMATION_SCHEMA.TIDB_TRX` 表中 `STATE` 字段的 `size` 未定义导致 `STATE` 显示为空的问题 [#53026](https://github.com/pingcap/tidb/issues/53026) @[cfzjywxk](https://github.com/cfzjywxk)
    - (dup): release-8.2.0.md > 错误修复> TiDB - 修复在自动收集统计信息时，系统变量 `tidb_enable_async_merge_global_stats` 和 `tidb_analyze_partition_concurrency` 未生效的问题 [#53972](https://github.com/pingcap/tidb/issues/53972) @[hi-rustin](https://github.com/hi-rustin)
    - (dup): release-8.2.0.md > 错误修复> TiDB - 修复使用 `CURRENT_DATE()` 作为列默认值时查询结果错误的问题 [#53746](https://github.com/pingcap/tidb/issues/53746) @[tangenta](https://github.com/tangenta)

+ TiKV

    - note [#issue](https://github.com/tikv/tikv/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
    - note [#issue](https://github.com/tikv/tikv/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
    - (dup): release-8.2.0.md > 错误修复> TiKV - 修复设置 gRPC 消息的压缩算法 (`grpc-compression-type`) 对 TiKV 发送到 TiDB 的消息不起作用的问题 [#17176](https://github.com/tikv/tikv/issues/17176) @[ekexium](https://github.com/ekexium)
    - (dup): release-8.2.0.md > 错误修复> TiKV - 修复高并发的 Coprocessor 请求可能导致 TiKV OOM 的问题 [#16653](https://github.com/tikv/tikv/issues/16653) @[overvenus](https://github.com/overvenus)
    - (dup): release-8.2.0.md > 错误修复> TiKV - 修复 `advance-ts-interval` 配置未被用于限制 CDC 和 log-backup 模块中 `check_leader` 操作的 timeout，导致在某些情况下 TiKV 正常重启时 `resolved_ts` lag 过大的问题 [#17107](https://github.com/tikv/tikv/issues/17107) @[MyonKeminta](https://github.com/MyonKeminta)
    - 解决了 TiKV 应用损坏的 Raft 数据快照时不断 panic 的问题 [#15292](https://github.com/tikv/tikv/issues/15292) @[LykxSassinator](https://github.com/LykxSassinator)

+ PD

    - note [#issue](https://github.com/tikv/pd/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
    - note [#issue](https://github.com/tikv/pd/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
    - (dup): release-7.1.4.md > 错误修复> PD - 修复资源组 (Resource Group) 客户端中未完全删除的 slot 导致分配 token 低于给定值的问题 [#7346](https://github.com/tikv/pd/issues/7346) @[guo-shaoge](https://github.com/guo-shaoge)

+ TiFlash

    - note [#issue](https://github.com/pingcap/tiflash/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
    - note [#issue](https://github.com/pingcap/tiflash/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
    - (dup): release-8.2.0.md > 错误修复> TiFlash - 修复通过 BR 或 TiDB Lightning 导入数据后，FastScan 模式下可能读到大量重复行数据的问题 [#9118](https://github.com/pingcap/tiflash/issues/9118) @[JinheLin](https://github.com/JinheLin)
    - (dup): release-6.5.10.md > 错误修复> TiFlash - 修复函数 `SUBSTRING_INDEX()` 可能导致 TiFlash Crash 的问题 [#9116](https://github.com/pingcap/tiflash/issues/9116) @[wshwsh12](https://github.com/wshwsh12)
    - 修复以空字符串作为 TiFlash 中 SSL 证书配置项的值，会意外地开启 TLS 并导致 TiFlash 启动失败的问题 [#9235](https://github.com/pingcap/tiflash/issues/9235) @[JaySon-Huang](https://github.com/JaySon-Huang)
    - Fix a bug that empty SSL config strings will enable TLS for tiflash [#9235](https://github.com/pingcap/tiflash/issues/9235) @[JaySon-Huang](https://github.com/JaySon-Huang)
    - 修复开启延迟物化后，部分查询可能在执行时报类型不匹配的错误 [#9175](https://github.com/pingcap/tiflash/issues/9175) @[JinheLin](https://github.com/JinheLin)
    - 修复开启延迟物化后，带有虚拟生成列的查询可能导致返回错误结果的问题 [#9188](https://github.com/pingcap/tiflash/issues/9188) @[JinheLin](https://github.com/JinheLin)
    - 修复跨数据库对带有空分区的分区表执行 `RENAME TABLE ... TO ...` 之后，可能导致 TiFlash panic 的问题 [#9132](https://github.com/pingcap/tiflash/issues/9132) @[JaySon-Huang](https://github.com/JaySon-Huang)

+ Tools

    + Backup & Restore (BR)

        - note [#issue](https://github.com/pingcap/tidb/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
        - note [#issue](https://github.com/pingcap/tidb/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
        - (dup): release-6.5.10.md > 错误修复> Tools> Backup & Restore (BR) - 修复日志备份在 advancer owner 发生迁移后可能被暂停的问题 [#53561](https://github.com/pingcap/tidb/issues/53561) @[RidRisR](https://github.com/RidRisR)
        - (dup): release-6.5.10.md > 错误修复> Tools> Backup & Restore (BR) - 修复在恢复过程中，由于多层重试导致 BR 无法正确识别错误的问题 [#54053](https://github.com/pingcap/tidb/issues/54053) @[RidRisR](https://github.com/RidRisR)
        - (dup): release-8.2.0.md > 错误修复> Tools> Backup & Restore (BR) - 修复增量备份过程中扫描 DDL 作业的效率较低的问题 [#54139](https://github.com/pingcap/tidb/issues/54139) @[3pointer](https://github.com/3pointer)
        - (dup): release-8.2.0.md > 错误修复> Tools> Backup & Restore (BR) - 修复断点备份过程中查找 Region leader 中断导致备份性能受影响问题 [#17168](https://github.com/tikv/tikv/issues/17168) @[Leavrth](https://github.com/Leavrth)
        - (dup): release-8.1.0.md > 错误修复> Tools> Backup & Restore (BR) - 修复日志备份在暂停、停止、再重建任务操作后，虽然任务状态显示正常，但 Checkpoint 不推进的问题 [#53047](https://github.com/pingcap/tidb/issues/53047) @[RidRisR](https://github.com/RidRisR)
        - 修复增量备份恢复中回放 add index, modify column 等需要回填的 ddl 可能出错的问题[#54426](https://github.com/pingcap/tidb/issues/54426) @[3pointer](https://github.com/3pointer)

    + TiCDC

        - 修复拆分 Update 事件后校验码没有正确设置为 0 的问题 [#11402](https://github.com/pingcap/tiflow/issues/11402) @[3AceShowHand](https://github.com/3AceShowHand)
        - 修复当下游 Kafka 无法访问时，Processor 模块可能卡住的问题 [#11340](https://github.com/pingcap/tiflow/issues/11340) @[asddongmen](https://github.com/asddongmen)

    + TiDB Data Migration (DM)

        - note [#issue](https://github.com/pingcap/tiflow/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
        - note [#issue](https://github.com/pingcap/tiflow/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})

    + TiDB Lightning

        - note [#issue](https://github.com/pingcap/tidb/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
        - note [#issue](https://github.com/pingcap/tidb/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})

    + Dumpling

        - note [#issue](https://github.com/pingcap/tidb/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
        - note [#issue](https://github.com/pingcap/tidb/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
        - (dup): release-6.5.10.md > 错误修复> Tools> Dumpling - 修复 Dumpling 在同时导出表和视图时报错的问题 [#53682](https://github.com/pingcap/tidb/issues/53682) @[tangenta](https://github.com/tangenta)

    + TiUP

        - note [#issue](https://github.com/pingcap/tiup/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
        - note [#issue](https://github.com/pingcap/tiup/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})

    + TiDB Binlog

        - note [#issue](https://github.com/pingcap/tidb-binlog/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
        - note [#issue](https://github.com/pingcap/tidb-binlog/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
