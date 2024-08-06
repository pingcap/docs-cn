---
title: TiDB 7.5.3 Release Notes
summary: 了解 TiDB 7.5.3 版本的兼容性变更、改进提升，以及错误修复。
---

# TiDB 7.5.3 Release Notes

发版日期：2024 年 8 月 5 日

TiDB 版本：7.5.3

试用链接：[快速体验](https://docs.pingcap.com/zh/tidb/v7.5/quick-start-with-tidb) | [生产部署](https://docs.pingcap.com/zh/tidb/v7.5/production-deployment-using-tiup) | [下载离线包](https://cn.pingcap.com/product-community/?version=v7.5.3#version-list)

## 兼容性变更

- 新增系统表 [`INFORMATION_SCHEMA.KEYWORDS`](/information-schema/information-schema-keywords.md) 用来展示 TiDB 支持的所有关键字的信息 [#48801](https://github.com/pingcap/tidb/issues/48801) @[dveeden](https://github.com/dveeden)

## 改进提升

+ TiDB

    - 通过批量删除 TiFlash placement rule 的方式，提升对分区表执行 `TRUNCATE`、`DROP` 后数据 GC 的处理速度 [#54068](https://github.com/pingcap/tidb/issues/54068) @[Lloyd-Pottiger](https://github.com/Lloyd-Pottiger)

+ TiFlash

    - 降低 TiFlash 在开启 TLS 后因更新证书而导致 panic 的概率 [#8535](https://github.com/pingcap/tiflash/issues/8535) @[windtalker](https://github.com/windtalker)
    - 减少数据高并发读取下的锁冲突，优化短查询性能 [#9125](https://github.com/pingcap/tiflash/issues/9125) @[JinheLin](https://github.com/JinheLin)

+ Tools

    + Backup & Restore (BR)

        - 去掉除了 `br log restore` 子命令之外其它 `br log` 子命令对 TiDB `domain` 数据结构的载入，降低内存消耗 [#52088](https://github.com/pingcap/tidb/issues/52088) @[Leavrth](https://github.com/Leavrth)
        - 在遇到较大的 checkpoint lag 时，日志备份支持自动放弃任务，以避免日志备份长时间阻塞 GC，从而防止集群出现问题 [#50803](https://github.com/pingcap/tidb/issues/50803) @[RidRisR](https://github.com/RidRisR)
        - 增加由于 DNS 错误而导致的失败的重试次数 [#53029](https://github.com/pingcap/tidb/issues/53029) @[YuJuncen](https://github.com/YuJuncen)
        - 增加 PITR 集成测试用例，覆盖对日志备份与添加索引加速功能的兼容性测试 [#51987](https://github.com/pingcap/tidb/issues/51987) @[Leavrth](https://github.com/Leavrth)
        - 增加因 Region 没有 leader 导致的失败重试次数 [#54017](https://github.com/pingcap/tidb/issues/54017) @[Leavrth](https://github.com/Leavrth)
        - 支持通过环境变量设置阿里云访问身份 [#45551](https://github.com/pingcap/tidb/issues/45551) @[RidRisR](https://github.com/RidRisR)

    + TiCDC

        - 支持当下游为消息队列 (Message Queue, MQ) 或存储服务时直接输出原始事件 [#11211](https://github.com/pingcap/tiflow/issues/11211) @[CharlesCheung96](https://github.com/CharlesCheung96)

## 错误修复

+ TiDB

    - 修复加载索引统计信息可能会造成内存泄漏的问题 [#54022](https://github.com/pingcap/tidb/issues/54022) @[hi-rustin](https://github.com/hi-rustin)
    - 修复 `UPDATE` 操作在多表场景下导致 TiDB OOM 的问题 [#53742](https://github.com/pingcap/tidb/issues/53742) @[hawkingrei](https://github.com/hawkingrei)
    - 修复在 `GROUP BY` 语句中引用间接占位符 `?` 无法找到列的问题 [#53872](https://github.com/pingcap/tidb/issues/53872) @[qw4990](https://github.com/qw4990)
    - 修复当排序规则为 `utf8_bin` 或 `utf8mb4_bin` 时意外消除 `LENGTH()` 条件的错误 [#53730](https://github.com/pingcap/tidb/issues/53730) @[elsa0520](https://github.com/elsa0520)
    - 修复插入过大的科学计数法表示的数字时，返回 Warning 而非 Error 的问题，使其与 MySQL 保持一致 [#47787](https://github.com/pingcap/tidb/issues/47787) @[qw4990](https://github.com/qw4990)
    - 修复递归 CTE 查询可能导致无效指针的问题 [#54449](https://github.com/pingcap/tidb/issues/54449) @[hawkingrei](https://github.com/hawkingrei)
    - 修复统计数据在遇到主键重复时没有更新 `stats_history` 表的问题 [#47539](https://github.com/pingcap/tidb/issues/47539) @[Defined2014](https://github.com/Defined2014)
    - 修复当查询包含非关联子查询和 `LIMIT` 子句时，列剪裁可能不完善导致计划不优的问题 [#54213](https://github.com/pingcap/tidb/issues/54213) @[qw4990](https://github.com/qw4990)
    - 修复在 `HashJoin` 或 `IndexLookUp` 算子作为 `Apply` 算子的被驱动侧子节点时，由于 `memTracker` 未被析构而导致的内存异常高的问题 [#54005](https://github.com/pingcap/tidb/issues/54005) @[XuHuaiyu](https://github.com/XuHuaiyu)
    - 修复递归的 CTE 算子错误地跟踪内存使用的问题 [#54181](https://github.com/pingcap/tidb/issues/54181) @[guo-shaoge](https://github.com/guo-shaoge)
    - 修复事务占用的内存可能被多次重复统计的问题 [#53984](https://github.com/pingcap/tidb/issues/53984) @[ekexium](https://github.com/ekexium)
    - 修复使用 `SHOW WARNINGS;` 获取警告时可能导致 panic 的问题 [#48756](https://github.com/pingcap/tidb/issues/48756) @[xhebox](https://github.com/xhebox)
    - 修复在 `sql_mode=''` 时，将 `UNSIGNED` 类型的字段更新为 `-1` 会得到 `null` 而不是 `0` 的问题 [#47816](https://github.com/pingcap/tidb/issues/47816) @[lcwangchao](https://github.com/lcwangchao)
    - 修复当第一个参数是 `month` 并且第二个参数是负数时，`TIMESTAMPADD()` 函数会进入无限循环的问题 [#54908](https://github.com/pingcap/tidb/issues/54908) @[xzhangxian1008](https://github.com/xzhangxian1008)
    - 修复某些连接在握手完成之前退出导致 Grafana 监控指标中的连接数 (Connection Count) 不正确的问题 [#54428](https://github.com/pingcap/tidb/issues/54428) @[YangKeao](https://github.com/YangKeao)
    - 修复使用 TiProxy 和资源组 (Resource Group) 功能时，每个资源组的连接数 (Connection Count) 显示不正确的问题 [#54545](https://github.com/pingcap/tidb/issues/54545) @[YangKeao](https://github.com/YangKeao)
    - 修复并发执行 `CREATE OR REPLACE VIEW` 可能报错 `table doesn't exist` 的问题 [#53673](https://github.com/pingcap/tidb/issues/53673) @[tangenta](https://github.com/tangenta)
    - 修复在包含数据修改操作的事务中查询带有虚拟列的表时，查询结果可能错误的问题 [#53951](https://github.com/pingcap/tidb/issues/53951) @[qw4990](https://github.com/qw4990)
    - 修复执行 `SELECT DISTINCT CAST(col AS DECIMAL), CAST(col AS SIGNED) FROM ...` 查询时结果出错的问题 [#53726](https://github.com/pingcap/tidb/issues/53726) @[hawkingrei](https://github.com/hawkingrei)
    - 修复使用 Optimizer Hints 时，可能输出错误的 WARNINGS 信息的问题 [#53767](https://github.com/pingcap/tidb/issues/53767) @[hawkingrei](https://github.com/hawkingrei)
    - 修复某些情况下可以创建非法的 `DECIMAL(0,0)` 列类型的问题 [#53779](https://github.com/pingcap/tidb/issues/53779) @[tangenta](https://github.com/tangenta)
    - 修复 `memory_quota` Hint 在子查询中可能不生效的问题 [#53834](https://github.com/pingcap/tidb/issues/53834) @[qw4990](https://github.com/qw4990)
    - 修复 JSON 相关函数在某些情况下报错信息与 MySQL 不一致的问题 [#53799](https://github.com/pingcap/tidb/issues/53799) @[dveeden](https://github.com/dveeden)
    - 修复在某些情况下，元数据锁使用不当可能导致使用 plan cache 时写入异常数据的问题 [#53634](https://github.com/pingcap/tidb/issues/53634) @[zimulala](https://github.com/zimulala)
    - 修复查询中的某些过滤条件可能导致 planner 模块发生 `invalid memory address or nil pointer dereference` 报错的问题 [#53582](https://github.com/pingcap/tidb/issues/53582) [#53580](https://github.com/pingcap/tidb/issues/53580) [#53594](https://github.com/pingcap/tidb/issues/53594) [#53603](https://github.com/pingcap/tidb/issues/53603) @[YangKeao](https://github.com/YangKeao)
    - 修复在事务内的语句被 OOM 终止之后，如果在当前事务内继续执行下一条语句，可能报错 `Trying to start aggressive locking while it's already started` 并发生 panic 的问题 [#53540](https://github.com/pingcap/tidb/issues/53540) @[MyonKeminta](https://github.com/MyonKeminta)
    - 修复执行 `ALTER TABLE ... REMOVE PARTITIONING` 后可能导致数据丢失的问题 [#53385](https://github.com/pingcap/tidb/issues/53385) @[mjonss](https://github.com/mjonss)
    - 修复使用 `PREPARE`/`EXECUTE` 方式执行带 `CONV` 表达式的语句，且 `CONV` 表达式包含 `?` 参数时，多次执行可能导致查询结果错误的问题 [#53505](https://github.com/pingcap/tidb/issues/53505) @[qw4990](https://github.com/qw4990)
    - 修复使用 `auth_socket` 认证插件时，TiDB 在某些情况下未能拒绝不符合身份认证的用户连接的问题 [#54031](https://github.com/pingcap/tidb/issues/54031) @[lcwangchao](https://github.com/lcwangchao)
    - 修复 information schema 缓存未命中导致 stale read 查询延迟上升的问题 [#53428](https://github.com/pingcap/tidb/issues/53428) @[crazycs520](https://github.com/crazycs520)
    - 修复 `INFORMATION_SCHEMA.TIDB_TRX` 表中 `STATE` 字段的 `size` 未定义导致 `STATE` 显示为空的问题 [#53026](https://github.com/pingcap/tidb/issues/53026) @[cfzjywxk](https://github.com/cfzjywxk)
    - 修复在自动收集统计信息时，系统变量 `tidb_enable_async_merge_global_stats` 和 `tidb_analyze_partition_concurrency` 未生效的问题 [#53972](https://github.com/pingcap/tidb/issues/53972) @[hi-rustin](https://github.com/hi-rustin)
    - 修复使用 `CURRENT_DATE()` 作为列默认值时查询结果错误的问题 [#53746](https://github.com/pingcap/tidb/issues/53746) @[tangenta](https://github.com/tangenta)
    - 修复针对 `SELECT ... FOR UPDATE` 复用了错误点查询计划的问题 [#54652](https://github.com/pingcap/tidb/issues/54652) @[qw4990](https://github.com/qw4990)

+ TiKV

    - 修复设置 gRPC 消息的压缩算法 (`grpc-compression-type`) 对 TiKV 发送到 TiDB 的消息不起作用的问题 [#17176](https://github.com/tikv/tikv/issues/17176) @[ekexium](https://github.com/ekexium)
    - 修复高并发的 Coprocessor 请求可能导致 TiKV OOM 的问题 [#16653](https://github.com/tikv/tikv/issues/16653) @[overvenus](https://github.com/overvenus)
    - 修复 `advance-ts-interval` 配置未被用于限制 CDC 和 log-backup 模块中 `check_leader` 操作的 timeout，导致在某些情况下 TiKV 正常重启时 `resolved_ts` lag 过大的问题 [#17107](https://github.com/tikv/tikv/issues/17107) @[MyonKeminta](https://github.com/MyonKeminta)
    - 修复 TiKV 在应用损坏的 Raft 数据快照时反复 panic 的问题 [#15292](https://github.com/tikv/tikv/issues/15292) @[LykxSassinator](https://github.com/LykxSassinator)

+ PD

    - 修复资源组 (Resource Group) 客户端中未完全删除的 slot 导致分配 token 低于给定值的问题 [#7346](https://github.com/tikv/pd/issues/7346) @[guo-shaoge](https://github.com/guo-shaoge)
    - 修复资源组在请求 token 超过 500 ms 时遇到超出配额限制的问题 [#8349](https://github.com/tikv/pd/issues/8349) @[nolouch](https://github.com/nolouch)
    - 修复资源组遇到的数据竞争问题 [#8267](https://github.com/tikv/pd/issues/8267) @[HuSharp](https://github.com/HuSharp)
    - 修复 PD 在进行 operator 检查时遇到的数据竞争问题 [#8263](https://github.com/tikv/pd/issues/8263) @[lhy1024](https://github.com/lhy1024)
    - 修复 etcd client 中已经删除的节点仍然出现在候选连接列表中的问题 [#8286](https://github.com/tikv/pd/issues/8286) @[JmPotato](https://github.com/JmPotato)
    - 修复将 TiKV 配置项 [`coprocessor.region-split-size`](/tikv-configuration-file.md#region-split-size) 设置为小于 1 MiB 的值会导致 PD panic 的问题 [#8323](https://github.com/tikv/pd/issues/8323) @[JmPotato](https://github.com/JmPotato)
    - 修复加密管理器在使用前未初始化的问题 [#8384](https://github.com/tikv/pd/issues/8384) @[releungx](https://github.com/releungx)
    - 修复 PD 配置项 [`security.redact-info-log`](/pd-configuration-file.md#redact-info-log-从-v50-版本开始引入) 开启时 PD 日志未完全脱敏的问题 [#8419](https://github.com/tikv/pd/issues/8419) @[releungx](https://github.com/releungx)
    - 修复将角色 (role) 绑定到资源组时未报错的问题 [#54417](https://github.com/pingcap/tidb/issues/54417) @[JmPotato](https://github.com/JmPotato)

+ TiFlash

    - 修复通过 BR 或 TiDB Lightning 导入数据后，FastScan 模式下可能读到大量重复行数据的问题 [#9118](https://github.com/pingcap/tiflash/issues/9118) @[JinheLin](https://github.com/JinheLin)
    - 修复函数 `SUBSTRING_INDEX()` 可能导致 TiFlash Crash 的问题 [#9116](https://github.com/pingcap/tiflash/issues/9116) @[wshwsh12](https://github.com/wshwsh12)
    - 修复将 TiFlash 中 SSL 证书配置项设置为空字符串会错误开启 TLS 并导致 TiFlash 启动失败的问题 [#9235](https://github.com/pingcap/tiflash/issues/9235) @[JaySon-Huang](https://github.com/JaySon-Huang)
    - 修复开启延迟物化后，部分查询在执行时可能报列类型不匹配错误的问题 [#9175](https://github.com/pingcap/tiflash/issues/9175) @[JinheLin](https://github.com/JinheLin)
    - 修复开启延迟物化后，带有虚拟生成列的查询可能返回错误结果的问题 [#9188](https://github.com/pingcap/tiflash/issues/9188) @[JinheLin](https://github.com/JinheLin)
    - 修复跨数据库对含空分区的分区表执行 `RENAME TABLE ... TO ...` 后，TiFlash 可能 panic 的问题 [#9132](https://github.com/pingcap/tiflash/issues/9132) @[JaySon-Huang](https://github.com/JaySon-Huang)
    - 修复数据库创建后短时间内被删除时，TiFlash 可能 panic 的问题 [#9266](https://github.com/pingcap/tiflash/issues/9266) @[JaySon-Huang](https://github.com/JaySon-Huang)

+ Tools

    + Backup & Restore (BR)

        - 修复日志备份在 advancer owner 发生迁移后可能被暂停的问题 [#53561](https://github.com/pingcap/tidb/issues/53561) @[RidRisR](https://github.com/RidRisR)
        - 修复在恢复过程中，由于多层重试导致 BR 无法正确识别错误的问题 [#54053](https://github.com/pingcap/tidb/issues/54053) @[RidRisR](https://github.com/RidRisR)
        - 修复增量备份过程中扫描 DDL 作业的效率较低的问题 [#54139](https://github.com/pingcap/tidb/issues/54139) @[3pointer](https://github.com/3pointer)
        - 修复断点备份过程中查找 Region leader 中断导致备份性能受影响问题 [#17168](https://github.com/tikv/tikv/issues/17168) @[Leavrth](https://github.com/Leavrth)
        - 修复日志备份在暂停、停止、再重建任务操作后，虽然任务状态显示正常，但 Checkpoint 不推进的问题 [#53047](https://github.com/pingcap/tidb/issues/53047) @[RidRisR](https://github.com/RidRisR)
        - 修复增量恢复过程中 `ADD INDEX`、`MODIFY COLUMN` 等需要回填的 DDL 可能无法正确恢复的问题 [#54426](https://github.com/pingcap/tidb/issues/54426) @[3pointer](https://github.com/3pointer)

    + TiCDC

        - 修复拆分 `UPDATE` 事件后校验码未正确设置为 `0` 的问题 [#11402](https://github.com/pingcap/tiflow/issues/11402) @[3AceShowHand](https://github.com/3AceShowHand)
        - 修复当下游 Kafka 无法访问时，Processor 模块可能卡住的问题 [#11340](https://github.com/pingcap/tiflow/issues/11340) @[asddongmen](https://github.com/asddongmen)

    + Dumpling

        - 修复 Dumpling 在同时导出表和视图时报错的问题 [#53682](https://github.com/pingcap/tidb/issues/53682) @[tangenta](https://github.com/tangenta)
