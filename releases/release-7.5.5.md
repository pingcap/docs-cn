---
title: TiDB 7.5.5 Release Notes
summary: 了解 TiDB 7.5.5 版本的兼容性变更、改进提升，以及错误修复。
---

# TiDB 7.5.5 Release Notes

发版日期：2024 年 12 月 31 日

TiDB 版本：7.5.5

试用链接：[快速体验](https://docs.pingcap.com/zh/tidb/v7.5/quick-start-with-tidb) | [生产部署](https://docs.pingcap.com/zh/tidb/v7.5/production-deployment-using-tiup) | [下载离线包](https://cn.pingcap.com/product-community/?version=v7.5.5#version-list)

## 兼容性变更

- 新增系统变量 [`tidb_ddl_reorg_max_write_speed`](https://docs.pingcap.com/zh/tidb/v7.5/system-variables#tidb_ddl_reorg_max_write_speed-从-v6512-和-v755-版本开始引入)，用于限制加索引时 ingest 阶段速度的上限 [#57156](https://github.com/pingcap/tidb/issues/57156) @[CbcWestwolf](https://github.com/CbcWestwolf)
- TiKV 配置项 [`raft-client-queue-size`](/tikv-configuration-file.md#raft-client-queue-size) 默认值从 `8192` 修改为 `16384` [#17101](https://github.com/tikv/tikv/issues/17101) @[Connor1996](https://github.com/Connor1996)

## 改进提升

+ TiDB

    - 当某个统计信息完全由 TopN 构成，且对应表的统计信息中修改行数不为 0 时，对于未命中 TopN 的等值条件，估算结果从 0 调整为 1 [#47400](https://github.com/pingcap/tidb/issues/47400) @[terry1purcell](https://github.com/terry1purcell)

+ TiKV

    - 提升在 raft log 部署在独立磁盘情况下，磁盘出现故障时 TiKV 服务的 SLA [#17884](https://github.com/tikv/tikv/issues/17884) @[LykxSassinator](https://github.com/LykxSassinator)
    - 增加 peer 和 store 消息的 slow log [#16600](https://github.com/tikv/tikv/issues/16600) @[Connor1996](https://github.com/Connor1996)
    - 优化 TiKV 重启时由于需要等待应用之前的日志而造成访问延时抖动的情况，提升了 TiKV 的稳定性 [#15874](https://github.com/tikv/tikv/issues/15874) @[LykxSassinator](https://github.com/LykxSassinator)

+ TiFlash

    - 降低 TiFlash 在开启 TLS 后因更新证书而导致 panic 的概率 [#8535](https://github.com/pingcap/tiflash/issues/8535) @[windtalker](https://github.com/windtalker)
    - 提升聚簇索引表在后台回收过期数据的速度 [#9529](https://github.com/pingcap/tiflash/issues/9529) @[JaySon-Huang](https://github.com/JaySon-Huang)
    - 优化在存算分离架构下，读节点从 S3 下载文件异常时的重试策略 [#9695](https://github.com/pingcap/tiflash/issues/9695) @[JinheLin](https://github.com/JinheLin)

+ Tools

    + Backup & Restore (BR)

        - 减少备份过程中无效日志的打印 [#55902](https://github.com/pingcap/tidb/issues/55902) @[Leavrth](https://github.com/Leavrth)

    + TiDB Data Migration (DM)

        - 调低输出无法识别的 MariaDB binlog 事件时的日志级别 [#10204](https://github.com/pingcap/tiflow/issues/10204) @[dveeden](https://github.com/dveeden)

## 错误修复

+ TiDB

    - 修复 DDL owner 节点切换后，无法按照切换前的进度继续执行 Reorg DDL 任务的问题 [#56506](https://github.com/pingcap/tidb/issues/56506) @[tangenta](https://github.com/tangenta)
    - 修复在非严格模式下 (`sql_mode = ''`) ，非法空值能被插入的问题 [#56381](https://github.com/pingcap/tidb/issues/56381) @[joechenrh](https://github.com/joechenrh)
    - 修复 Grafana 中 **Stats Healthy Distribution** 面板的数据可能错误的问题 [#57176](https://github.com/pingcap/tidb/issues/57176) @[hawkingrei](https://github.com/hawkingrei)
    - 修复当公共表表达式 (CTE) 有多个数据消费者时，如果某个消费者在未读取数据时就退出，可能导致非法内存访问的问题 [#55881](https://github.com/pingcap/tidb/issues/55881) @[windtalker](https://github.com/windtalker)
    - 修复集群从 v6.5 升级到 v7.5 或更高版本后，已有 TTL 任务执行意外频繁的问题 [#56539](https://github.com/pingcap/tidb/issues/56539) @[lcwangchao](https://github.com/lcwangchao)
    - 修复关闭 `tidb_ttl_job_enable` 变量后 TTL 任务未被取消的问题 [#57404](https://github.com/pingcap/tidb/issues/57404) @[YangKeao](https://github.com/YangKeao)
    - 修复 information schema 缓存未命中导致 stale read 查询延迟上升的问题 [#53428](https://github.com/pingcap/tidb/issues/53428) @[crazycs520](https://github.com/crazycs520)
    - 修复由于 stale read 未对读操作的时间戳进行严格校验，导致 TSO 和真实物理时间存在偏移，有小概率影响事务一致性的问题 [#56809](https://github.com/pingcap/tidb/issues/56809) @[MyonKeminta](https://github.com/MyonKeminta)
    - 修复通过 `IMPORT INTO` 导入数据后，`AUTO_INCREMENT` 字段没有正确设置的问题 [#56476](https://github.com/pingcap/tidb/issues/56476) @[D3Hunter](https://github.com/D3Hunter)
    - 修复可能同时存在两个 DDL Owner 的问题 [#54689](https://github.com/pingcap/tidb/issues/54689) @[joccau](https://github.com/joccau)
    - 修复 TTL 在未选用 TiKV 作为存储引擎时可能失败的问题 [#56402](https://github.com/pingcap/tidb/issues/56402) @[YangKeao](https://github.com/YangKeao)
    - 修复执行 `ADD INDEX` 时，未检查索引长度限制的问题 [#56930](https://github.com/pingcap/tidb/issues/56930) @[fzzf678](https://github.com/fzzf678)
    - 修复取消 TTL 任务时，没有强制 Kill 对应 SQL 的问题 [#56511](https://github.com/pingcap/tidb/issues/56511) @[lcwangchao](https://github.com/lcwangchao)
    - 修复无法为带别名的多表删除语句 `DELETE` 创建执行计划绑定的问题 [#56726](https://github.com/pingcap/tidb/issues/56726) @[hawkingrei](https://github.com/hawkingrei)
    - 修复使用 `ANALYZE` 收集表的统计信息时，如果该表包含虚拟生成列的表达式索引，执行会报错的问题 [#57079](https://github.com/pingcap/tidb/issues/57079) @[hawkingrei](https://github.com/hawkingrei)
    - 修复使用 `PLAN REPLAYER` 导入含有 Placement Rule 的表结构时可能报错的问题 [#54961](https://github.com/pingcap/tidb/issues/54961) @[hawkingrei](https://github.com/hawkingrei)
    - 修复在 CTE 中解析数据库名时，返回错误的数据库名的问题 [#54582](https://github.com/pingcap/tidb/issues/54582) @[hawkingrei](https://github.com/hawkingrei)
    - 修复 `INSERT ... ON DUPLICATE KEY` 语句不兼容 `mysql_insert_id` 的问题 [#55965](https://github.com/pingcap/tidb/issues/55965) @[tiancaiamao](https://github.com/tiancaiamao)
    - 修复在某些情况下，元数据锁使用不当可能导致使用 plan cache 时写入异常数据的问题 [#53634](https://github.com/pingcap/tidb/issues/53634) @[zimulala](https://github.com/zimulala)
    - 修复使用全局排序添加索引时性能不稳定的问题 [#54147](https://github.com/pingcap/tidb/issues/54147) @[tangenta](https://github.com/tangenta)
    - 修复使用 `PLAN REPLAYER` 导入含有外键的表结构时可能报错的问题 [#56456](https://github.com/pingcap/tidb/issues/56456) @[hawkingrei](https://github.com/hawkingrei)
    - 修复同时使用 `RANGE COLUMNS` 分区函数和 `utf8mb4_0900_ai_ci` 排序规则时，查询结果错误的问题 [#57261](https://github.com/pingcap/tidb/issues/57261) @[Defined2014](https://github.com/Defined2014)
    - 修复使用 `NATURAL JOIN` 或者 `USING` 子句之后，再使用子查询可能会报错的问题 [#53766](https://github.com/pingcap/tidb/issues/53766) @[dash12653](https://github.com/dash12653)
    - 修复写冲突时 TTL 任务可能无法取消的问题 [#56422](https://github.com/pingcap/tidb/issues/56422) @[YangKeao](https://github.com/YangKeao)
    - 修复如果 CTE 包含 `ORDER BY`、`LIMIT`、`SELECT DISTINCT` 子句，并且被另外一个 CTE 的递归部分所引用时，可能被错误地 inline 导致执行报错的问题 [#56603](https://github.com/pingcap/tidb/issues/56603) @[elsa0520](https://github.com/elsa0520)
    - 修复 `UPDATE` 语句更新 `ENUM` 类型的值时更新错误的问题 [#56832](https://github.com/pingcap/tidb/issues/56832) @[xhebox](https://github.com/xhebox)
    - 修复执行 `RECOVER TABLE BY JOB JOB_ID;` 可能导致 panic 的问题 [#55113](https://github.com/pingcap/tidb/issues/55113) @[crazycs520](https://github.com/crazycs520)
    - 修复当一个查询有索引合并 (Index Merge) 执行计划可用时，`read_from_storage` hint 可能不生效的问题 [#56217](https://github.com/pingcap/tidb/issues/56217) @[AilinKid](https://github.com/AilinKid)
    - 修复 `INDEX_HASH_JOIN` 在异常退出时可能卡住的问题 [#54055](https://github.com/pingcap/tidb/issues/54055) @[wshwsh12](https://github.com/wshwsh12)
    - 修复查询分布式执行框架相关的系统表可能导致升级异常的问题 [#49263](https://github.com/pingcap/tidb/issues/49263) @[D3Hunter](https://github.com/D3Hunter)
    - 修复 DDL 内部事务报错 `GC life time is shorter than transaction duration`，导致添加索引失败的问题 [#57043](https://github.com/pingcap/tidb/issues/57043) @[tangenta](https://github.com/tangenta)
    - 修复当执行 `EXCHANGE PARTITION` 遇到不合法的行时，导致 InfoSchema 全量加载并报错 `failed to load schema diff` 的问题 [#56685](https://github.com/pingcap/tidb/issues/56685) @[D3Hunter](https://github.com/D3Hunter)
    - 修复当 `tidb_ddl_enable_fast_reorg` 和 `new_collations_enabled_on_first_bootstrap` 开启时，未正确处理排序规则，导致数据索引不一致的问题 [#58036](https://github.com/pingcap/tidb/issues/58036) @[djshow832](https://github.com/djshow832)
    - 修复添加索引期间，计划缓存使用了错误的 schema 导致数据索引不一致的问题 [#56733](https://github.com/pingcap/tidb/issues/56733) @[wjhuang2016](https://github.com/wjhuang2016)
    - 修复在升级期间执行 `ALTER TABLE TIFLASH REPLICA` 导致 TiDB 节点宕机的问题 [#57863](https://github.com/pingcap/tidb/issues/57863) @[tangenta](https://github.com/tangenta)
    - 修复 `INFORMATION_SCHEMA.columns` 查询性能下降的问题 [#58184](https://github.com/pingcap/tidb/issues/58184) @[lance6716](https://github.com/lance6716)
    - 修复查询 TiFlash 系统表中默认超时时间过短的问题 [#57816](https://github.com/pingcap/tidb/issues/57816) @[JaySon-Huang](https://github.com/JaySon-Huang)
    - 修复 `default_collation_for_utf8mb4` 变量的值没有对 `SET NAMES` 语法生效的问题 [#56439](https://github.com/pingcap/tidb/issues/56439) @[Defined2014](https://github.com/Defined2014)
    - 修复手动删除 `mysql`.`timer` 表中的定时器时，TTL 内部协程可能 panic 的问题 [#57112](https://github.com/pingcap/tidb/issues/57112) @[lcwangchao](https://github.com/lcwangchao)
    - 修复使用 `ALTER TABLE` 语句将普通表转换为分区表时，由于检查不充分可能导致数据出现错误的问题 [#55721](https://github.com/pingcap/tidb/issues/55721) @[mjonss](https://github.com/mjonss)
    - 修复设置 `tidb_gogc_tuner_max_value` 和 `tidb_gogc_tuner_min_value` 时，由于最大值为空导致出现错误的 warning 信息的问题 [#57889](https://github.com/pingcap/tidb/issues/57889) @[hawkingrei](https://github.com/hawkingrei)
    - 修复 TiDB 内部协程可能出现数据竞争的问题 [#57798](https://github.com/pingcap/tidb/issues/57798) [#56053](https://github.com/pingcap/tidb/issues/56053) @[fishiu](https://github.com/fishiu) @[tiancaiamao](https://github.com/tiancaiamao)
    - 更新 `golang-jwt` 和 `jwt` 以规避潜在的安全风险 [#57135](https://github.com/pingcap/tidb/issues/57135) @[hawkingrei](https://github.com/hawkingrei)
    - 修复使用 `ALTER TABLE` 语句将聚簇索引表转换为分区表时，并发写入可能会导致重复数据的问题 [#57510](https://github.com/pingcap/tidb/issues/57510) @[mjonss](https://github.com/mjonss)

+ TiKV

    - 修复 TiKV 处理 destroyed peer 时可能遇到的 panic 的问题 [#17840](https://github.com/tikv/tikv/issues/17840) @[glorv](https://github.com/glorv))
    - 提升在 raft log 部署在独立磁盘情况下，磁盘出现故障时 TiKV 服务的 SLA [#17884](https://github.com/tikv/tikv/issues/17884) @[LykxSassinator](https://github.com/LykxSassinator)
    - 修复当 `log-file` 参数未指定时 jprof 的输出内容没有被正确捕获和处理的问题 [#17607](https://github.com/tikv/tikv/issues/17607) @[Hexilee](https://github.com/Hexilee)
    - 修复在唤醒休眠 Region 时可能出现延迟上升的问题 [#17101](https://github.com/tikv/tikv/issues/17101) @[Connor1996](https://github.com/Connor1996)
    - 修复使用 `RADIANS()` 或 `DEGREES()` 函数时可能导致 TiKV panic 的问题 [#17852](https://github.com/tikv/tikv/issues/17852) @[gengliqi](https://github.com/gengliqi)
    - 修复读线程在从 Raft Engine 中的 MemTable 读取过时索引时出现的 panic 问题 [#17383](https://github.com/tikv/tikv/issues/17383) @[LykxSassinator](https://github.com/LykxSassinator)
    - 修复当大量事务在排队等待同一个 key 上的锁被释放且该 key 被频繁更新时，TiKV 可能因死锁检测压力过大而出现 OOM 的问题 [#17394](https://github.com/tikv/tikv/issues/17394) @[MyonKeminta](https://github.com/MyonKeminta)
    - 修复所有休眠的 Region 被集中唤醒时，可能导致写入抖动的问题 [#17101](https://github.com/tikv/tikv/issues/17101) @[hhwyt](https://github.com/hhwyt)
    - 修复巴西和埃及时区转换错误的问题 [#16220](https://github.com/tikv/tikv/issues/16220) @[overvenus](https://github.com/overvenus)
    - 修复 Online Unsafe Recovery 时无法处理 merge abort 的问题 [#15580](https://github.com/tikv/tikv/issues/15580) @[v01dstar](https://github.com/v01dstar)
    - 修复 CPU profiling flag 在出现错误时没有正确重置的问题 [#17234](https://github.com/tikv/tikv/issues/17234) @[Connor1996](https://github.com/Connor1996)
    - 修复 `raft-entry-max-size` 设置过高时，写入 batch 可能过大引起性能抖动的问题 [#17701](https://github.com/tikv/tikv/issues/17701) @[SpadeA-Tang](https://github.com/SpadeA-Tang)
    - 修复 import 模块的冲突检测接口由于错误处理不当可能导致 TiKV panic 的问题 [#17830](https://github.com/tikv/tikv/issues/17830) @[joccau](https://github.com/joccau)

+ PD

    - 修复创建 `evict-leader-scheduler` 或 `grant-leader-scheduler` 遇到错误时，未能将错误信息返回到 pd-ctl 的问题 [#8759](https://github.com/tikv/pd/issues/8759) @[okJiang](https://github.com/okJiang)
    - 修复 etcd Leader 切换时 PD 不能快速重新选举的问题 [#8823](https://github.com/tikv/pd/issues/8823) @[rleungx](https://github.com/rleungx)
    - 修复 label 统计中的内存泄露问题 [#8700](https://github.com/tikv/pd/issues/8700) @[lhy1024](https://github.com/lhy1024)
    - 修复 `evict-leader-scheduler` 在使用相同 Store ID 重复创建后无法正常工作的问题 [#8756](https://github.com/tikv/pd/issues/8756) @[okJiang](https://github.com/okJiang)
    - 修复资源组 (Resource Group) 客户端中未完全删除的 slot 导致分配 token 低于给定值的问题 [#7346](https://github.com/tikv/pd/issues/7346) @[guo-shaoge](https://github.com/guo-shaoge)
    - 修复在 `evict-leader-scheduler` 中使用了错误的参数后，PD 不能正确报错且导致部分 scheduler 不可用的问题 [#8619](https://github.com/tikv/pd/issues/8619) @[rleungx](https://github.com/rleungx)
    - 修复热点缓存中可能存在的内存泄露问题 [#8698](https://github.com/tikv/pd/issues/8698) @[lhy1024](https://github.com/lhy1024)
    - 修复频繁创建随机数生成器导致性能抖动的问题 [#8674](https://github.com/tikv/pd/issues/8674) @[rleungx](https://github.com/rleungx)

+ TiFlash

    - 修复在 TiDB 执行并发 DDL 遇到冲突时 TiFlash panic 的问题 [#8578](https://github.com/pingcap/tiflash/issues/8578) @[JaySon-Huang](https://github.com/JaySon-Huang)
    - 修复当 `LPAD()` 和 `RPAD()` 函数在某些情况下返回错误结果的问题 [#9465](https://github.com/pingcap/tiflash/issues/9465) @[guo-shaoge](https://github.com/guo-shaoge)
    - 修复当 `SUBSTRING()` 函数的第二个参数为负数时，可能返回错误结果的问题 [#9604](https://github.com/pingcap/tiflash/issues/9604) @[guo-shaoge](https://github.com/guo-shaoge)
    - 修复当表里含 Bit 类型列并且带有表示非法字符的默认值时，TiFlash 无法解析表 schema 的问题 [#9461](https://github.com/pingcap/tiflash/issues/9461) @[Lloyd-Pottiger](https://github.com/Lloyd-Pottiger)
    - 修复在存算分离架构下，对新增的列进行查询可能返回错误结果的问题 [#9665](https://github.com/pingcap/tiflash/issues/9665) @[zimulala](https://github.com/zimulala)

+ Tools

    + Backup & Restore (BR)

        - 修复数据恢复失败后，使用断点重启报错 `the target cluster is not fresh` 的问题 [#50232](https://github.com/pingcap/tidb/issues/50232) @[Leavrth](https://github.com/Leavrth)
        - 修复日志备份不能及时解决残留锁导致 Checkpoint 无法推进的问题 [#57134](https://github.com/pingcap/tidb/issues/57134) @[3pointer](https://github.com/3pointer)
        - 修复日志可能打印加密信息的问题 [#57585](https://github.com/pingcap/tidb/issues/57585) @[kennytm](https://github.com/kennytm)
        - 修复测试用例 `TestStoreRemoved` 不稳定的问题 [#52791](https://github.com/pingcap/tidb/issues/52791) @[YuJuncen](https://github.com/YuJuncen)
        - 升级 `k8s.io/api` 库的版本以修复潜在的安全漏洞 [#57790](https://github.com/pingcap/tidb/issues/57790) @[BornChanger](https://github.com/BornChanger)
        - 修复当集群存在大量表但实际数据量较小时，PITR 数据恢复任务可能出现 `Information schema is out of date` 报错的问题 [#57743](https://github.com/pingcap/tidb/issues/57743) @[Tristan1900](https://github.com/Tristan1900)

    + TiCDC

        - 修复同步 `TRUNCATE TABLE` DDL 并且该表没有有效索引时，TiCDC 可能会报错的问题 [#11765](https://github.com/pingcap/tiflow/issues/11765) @[asddongmen](https://github.com/asddongmen)
        - 修复 Simple Protocol 消息中分区表的 `tableID` 未正确设置的问题 [#11846](https://github.com/pingcap/tiflow/issues/11846) @[3AceShowHand](https://github.com/3AceShowHand)
        - 修复 redo 模块无法正确上报错误的问题 [#11744](https://github.com/pingcap/tiflow/issues/11744) @[CharlesCheung96](https://github.com/CharlesCheung96)
        - 修复在 `ignore-event` 中设置了过滤掉 `add table partition` 事件后，TiCDC 未将相关分区的其它类型 DML 变更事件同步到下游的问题 [#10524](https://github.com/pingcap/tiflow/issues/10524) @[CharlesCheung96](https://github.com/CharlesCheung96)
        - 修复 TiDB DDL owner 变更导致 DDL 任务的 schema 版本出现非递增时，TiCDC 错误丢弃 DDL 任务的问题 [#11714](https://github.com/pingcap/tiflow/issues/11714) @[wlwilliamx](https://github.com/wlwilliamx)

    + TiDB Data Migration (DM)

        - 修复通过物理导入模式导入数据后，表中自动生成的 ID 可能会出现大范围的跳变的问题 [#11768](https://github.com/pingcap/tiflow/issues/11768) @[D3Hunter](https://github.com/D3Hunter)"
        - 修复当同时配置 TLS 和 `shard-mode` 时，`start-task` 会在前置检查中报错的问题 [#11842](https://github.com/pingcap/tiflow/issues/11842) @[sunxiaoguang](https://github.com/sunxiaoguang)
        - 修复当密码长度超过 19 个字符时无法连接 MySQL 8.0 的问题 [#11603](https://github.com/pingcap/tiflow/issues/11603) @[fishiu](https://github.com/fishiu)

    + TiDB Lightning

        - 修复 TiDB Lightning 因 TiKV 发送的消息过大而接收失败的问题 [#56114](https://github.com/pingcap/tidb/issues/56114) @[fishiu](https://github.com/fishiu)
        - 修复使用物理导入模式导入数据后，`AUTO_INCREMENT` 值设置过大的问题 [#56814](https://github.com/pingcap/tidb/issues/56814) @[D3Hunter](https://github.com/D3Hunter)
        - 修复 TiDB Lightning 在更新任务元数据时遇到 `Lock wait timeout` 错误未自动重试的问题 [#53042](https://github.com/pingcap/tidb/issues/53042) @[guoshouyan](https://github.com/guoshouyan)
        - 修复在高并发场景下，从云存储导入数据时性能下降的问题 [#57413](https://github.com/pingcap/tidb/issues/57413) @[xuanyu66](https://github.com/xuanyu66)
        - 修复在导入大量 Parquet 文件时，TiDB Lightning 可能会在导入的准备阶段长时间卡住的问题 [#56104](https://github.com/pingcap/tidb/issues/56104) @[zeminzhou](https://github.com/zeminzhou)
        - 修复使用 TiDB Lightning 导入数据时，错误报告输出被截断的问题 [#58085](https://github.com/pingcap/tidb/issues/58085) @[lance6716](https://github.com/lance6716)

    + Dumpling

        - 修复当 Google Cloud Storage (GCS) 返回 503 错误时 Dumpling 未正确重试的问题 [#56127](https://github.com/pingcap/tidb/issues/56127) @[OliverS929](https://github.com/OliverS929)
