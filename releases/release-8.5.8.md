---
title: TiDB 8.5.8 Release Notes
summary: 了解 TiDB 8.5.8 的改进和错误修复。
---

# TiDB 8.5.8 Release Notes

发版日期：2026 年 xx 月 xx 日

TiDB 版本：8.5.8

试用链接：[快速体验](https://docs.pingcap.com/zh/tidb/v8.5/quick-start-with-tidb) | [生产部署](https://docs.pingcap.com/zh/tidb/v8.5/production-deployment-using-tiup) | [下载离线包](https://pingkai.cn/download#tidb-community)

## 提升改进

+ TiDB

    - 优化包含虚拟列的复合索引的优化器行数估算：当列统计信息不可用时，回退使用索引统计信息，帮助 TiDB 更准确地选择索引 [#69134](https://github.com/pingcap/tidb/issues/69134) @[qw4990](https://github.com/qw4990) <!-- component: planner --> <!-- pr: https://github.com/pingcap/tidb/pull/70327 -->

+ 工具

    + TiCDC

        - 优化 TiCDC Changefeed 在忽略删除事件时的扫描性能，减少包含大量删除操作的工作负载在追赶历史数据期间不必要的 DML 解码 [#5430](https://github.com/pingcap/ticdc/issues/5430) @[asddongmen](https://github.com/asddongmen) <!-- component: cdc --> <!-- pr: https://github.com/pingcap/ticdc/pull/5767 -->
        - 支持同时按事件数量和总字节数配置 TiCDC Changefeed 的事件收集器批处理，使不同工作负载和下游场景下的批次大小更加稳定 [#3237](https://github.com/pingcap/ticdc/issues/3237) @[3AceShowHand](https://github.com/3AceShowHand) <!-- component: cdc --> <!-- pr: https://github.com/pingcap/ticdc/pull/5942 -->
        - 引入自适应扫描窗口算法，提升 TiCDC Event Service 在内存压力下的稳定性和吞吐量，减少 DDL 或同步点场景中的 Dispatcher 饥饿和重置事件 [#4172](https://github.com/pingcap/ticdc/issues/4172) @[asddongmen](https://github.com/asddongmen) <!-- component: cdc --> <!-- pr: https://github.com/pingcap/ticdc/pull/5761 -->
        - 优化 TiCDC Kafka Sink 校验流程，使校验更加轻量和完整：避免在校验期间执行仅在启动阶段需要的操作，对已有 Topic 也会检查 Schema Registry 等编码器依赖，并且仅在 TiCDC 需要创建 Topic 时校验 `replication-factor` [#5618](https://github.com/pingcap/ticdc/issues/5618) [#5720](https://github.com/pingcap/ticdc/issues/5720) @[3AceShowHand](https://github.com/3AceShowHand) <!-- component: cdc --> <!-- pr: https://github.com/pingcap/ticdc/pull/5811 -->
        - 优化启用 Claim-Check 时 TiCDC Kafka Sink 的资源使用，由同一 Sink 中的所有 Encoder 共享一个 `ClaimCheck` 实例，减少外部存储客户端和连接的资源开销 [#5719](https://github.com/pingcap/ticdc/issues/5719) @[3AceShowHand](https://github.com/3AceShowHand) <!-- component: cdc --> <!-- pr: https://github.com/pingcap/ticdc/pull/5811 -->
        - 简化并统一 TiCDC Kafka Sink 的错误处理，对配置错误、Admin API 错误和 Producer 错误采用一致的分类和封装方式，使重试判断和问题排查更加容易 [#5790](https://github.com/pingcap/ticdc/issues/5790) @[3AceShowHand](https://github.com/3AceShowHand) <!-- component: cdc --> <!-- pr: https://github.com/pingcap/ticdc/pull/5811 -->

## 错误修复

+ TiDB

    - 修复包含 `MODIFY COLUMN` 的多 Schema 变更会回退到事务模式回填，而未能使用 Ingest 或分布式回填的问题 [#70136](https://github.com/pingcap/tidb/issues/70136) @[joechenrh](https://github.com/joechenrh) <!-- component: ddl --> <!-- pr: https://github.com/pingcap/tidb/pull/70188 -->
    - 修复对分区表添加索引时，重组过程中进度可能倒退的问题 [#62496](https://github.com/pingcap/tidb/issues/62496) @[GMHDBJD](https://github.com/GMHDBJD) <!-- component: ddl --> <!-- pr: https://github.com/pingcap/tidb/pull/68782 -->
    - 修复 `ADMIN ALTER DDL JOBS` 无法动态调整正在运行的事务模式回填任务的线程数或批次大小的问题 [#70138](https://github.com/pingcap/tidb/issues/70138) @[joechenrh](https://github.com/joechenrh) <!-- component: ddl --> <!-- pr: https://github.com/pingcap/tidb/pull/70256 -->
    - 修复某个查询将 `IN` 子查询用作嵌套 `NOT IN` 表达式的操作数时，TiDB 可能 panic 并终止用户会话的问题 [#64854](https://github.com/pingcap/tidb/issues/64854) @[hawkingrei](https://github.com/hawkingrei) <!-- component: planner --> <!-- pr: https://github.com/pingcap/tidb/pull/70259 -->
    - 修复原本可安全使用执行计划缓存的查询在使用 `JSON_EXTRACT()` 时，无法利用预处理或非预处理执行计划缓存的问题 [#69522](https://github.com/pingcap/tidb/issues/69522) @[winoros](https://github.com/winoros) <!-- component: planner --> <!-- pr: https://github.com/pingcap/tidb/pull/70257 -->
    - 修复通过 `ALTER TABLE ADD COLUMN` 添加的虚拟生成列的统计信息可能初始化不正确，导致 `SHOW STATS_HISTOGRAMS` 输出不准确并产生不必要的占位统计信息加载的问题 [#69160](https://github.com/pingcap/tidb/issues/69160) @[qw4990](https://github.com/qw4990) <!-- component: planner --> <!-- pr: https://github.com/pingcap/tidb/pull/70325 -->
    - 修复 TiDB 在收到针对预处理语句的重复 `COM_STMT_SEND_LONG_DATA` 请求，但这些语句一直未执行或重置时，连接内存使用量可能无限增长的问题 [#70349](https://github.com/pingcap/tidb/issues/70349) @[djshow832](https://github.com/djshow832) <!-- component: sql-infra --> <!-- pr: https://github.com/pingcap/tidb/pull/70369 -->
    - 修复解析包含过深嵌套括号的 SQL 语句或优化器 Hint 时，TiDB 可能崩溃的问题 [#70192](https://github.com/pingcap/tidb/issues/70192) @[Debra-He](https://github.com/Debra-He) <!-- component: sql-infra --> <!-- pr: https://github.com/pingcap/tidb/pull/70264 -->
    - 修复批量 TSO 请求期间，由于 PD Client 生成了无效的嵌套 Runtime Trace 区域，可能导致 TiDB Runtime Trace 解析失败的问题 [#69743](https://github.com/pingcap/tidb/issues/69743) @[YangKeao](https://github.com/YangKeao) <!-- component: sql-infra --> <!-- pr: https://github.com/pingcap/tidb/pull/70310 -->
    - 修复 `COM_CHANGE_USER` 认证失败后，连接可能处于不一致的会话状态的问题 [#69691](https://github.com/pingcap/tidb/issues/69691) @[bb7133](https://github.com/bb7133) <!-- component: sql-infra --> <!-- pr: https://github.com/pingcap/tidb/pull/70229 -->
    - 修复 `COM_STMT_SEND_LONG_DATA` 可为单个预处理语句无限累积参数数据的问题。TiDB 现在使用会话级 `max_allowed_packet` 限制累积数据大小，并在超限时返回数据包过大的错误 [#69693](https://github.com/pingcap/tidb/issues/69693) @[bb7133](https://github.com/bb7133) <!-- component: sql-infra --> <!-- pr: https://github.com/pingcap/tidb/pull/70231 -->
    - 修复 `UNCOMPRESS()` 处理特制的压缩输入时，可能消耗大量未跟踪的内存并超过查询内存配额的问题 [#70198](https://github.com/pingcap/tidb/issues/70198) @[Debra-He](https://github.com/Debra-He) <!-- component: sql-infra --> <!-- pr: https://github.com/pingcap/tidb/pull/70279 -->
    - 修复无权限用户可通过 `INFORMATION_SCHEMA.USER_ATTRIBUTES` 读取其他用户属性的问题 [#70277](https://github.com/pingcap/tidb/issues/70277) @[djshow832](https://github.com/djshow832) <!-- component: sql-infra --> <!-- pr: https://github.com/pingcap/tidb/pull/70317 -->
    - 修复内存使用量频繁超过告警阈值时，记录 OOM 诊断 Goroutine Profile 可能延长 Stop-the-World 暂停时间并增加查询延迟的问题 [#62080](https://github.com/pingcap/tidb/issues/62080) @[YangKeao](https://github.com/YangKeao) <!-- component: sql-infra --> <!-- pr: https://github.com/pingcap/tidb/pull/70228 -->
    - 修复在悲观事务中执行 `LOAD DATA LOCAL INFILE` 时，遇到可重试的锁冲突后可能会在内部重试，从而导致客户端连接状态不同步，并返回无效序列错误而非原始死锁错误的问题 [#69793](https://github.com/pingcap/tidb/issues/69793) @[lance6716](https://github.com/lance6716) <!-- component: transaction, sql-infra, execution --> <!-- pr: https://github.com/pingcap/tidb/pull/70194 -->
    - 修复执行 `ALTER TABLE ... REORGANIZE PARTITION` 时，重建的全局索引可能缺少对应索引项（这些索引项本应来自分区顺序位于重组分区之后、但未参与重组的分区中的行），从而导致使用这些索引的查询漏掉数据行，并且受影响的值无法正确执行唯一性约束的问题 [#70023](https://github.com/pingcap/tidb/issues/70023) @[mjonss](https://github.com/mjonss) <!-- component: ddl --> <!-- pr: https://github.com/pingcap/tidb/pull/70479 -->
    - 修复 Join 操作、`UPDATE` 语句和 `DELETE` 语句可能为初始 Chunk 分配过多内存的问题，该问题在高并发或处理宽行的场景下尤为明显 [#68545](https://github.com/pingcap/tidb/issues/68545) @[solotzg](https://github.com/solotzg) <!-- component: execution --> <!-- pr: https://github.com/pingcap/tidb/pull/69965 -->

+ TiKV

    - 修复 TiKV 会对快速处理完成的 Raftstore 消息批次执行不必要的慢日志消息格式化，造成额外 CPU 开销的问题 [#19861](https://github.com/tikv/tikv/issues/19861) @[pingyu](https://github.com/pingyu) <!-- component: tikv --> <!-- pr: https://github.com/tikv/tikv/pull/19910 -->
    - 修复 TiKV Coprocessor 计算下推的 `LIKE` 表达式时，如果涉及格式错误的 UTF-8 输入或模式、`BIT` 值或某些排序规则，可能导致 TiKV panic 的问题 [#66597](https://github.com/pingcap/tidb/issues/66597) [#67082](https://github.com/pingcap/tidb/issues/67082) [#19811](https://github.com/tikv/tikv/issues/19811) @[jebter](https://github.com/jebter) <!-- component: execution, tikv --> <!-- pr: https://github.com/tikv/tikv/pull/19893 --> <!-- pr: https://github.com/tikv/tikv/pull/19894 -->
    - 修复外部 SST Ingest 与前台写入并发竞争时，TiKV 可能生成不一致的 MVCC 状态，进而导致事务状态检查发生 panic 的问题 [#19891](https://github.com/tikv/tikv/issues/19891) @[gengliqi](https://github.com/gengliqi) <!-- component: tikv --> <!-- pr: https://github.com/tikv/tikv/pull/19916 -->
    - 修复在 FIPS 环境中无法使用 `ENABLE_FIPS=1` 构建 TiKV 的问题 [#19743](https://github.com/tikv/tikv/issues/19743) @[LykxSassinator](https://github.com/LykxSassinator) <!-- component: tikv --> <!-- pr: https://github.com/tikv/tikv/pull/19753 --> <!-- pr: https://github.com/tikv/tikv/pull/19904 --> <!-- pr: https://github.com/tikv/tikv/pull/19754 -->
    - 修复仅启用后台任务资源管控时，TiKV 会不必要地将事务调度器切换为优先级调度，可能导致写密集型工作负载出现 5% 到 10% 性能下降的问题 [#19858](https://github.com/tikv/tikv/issues/19858) @[glorv](https://github.com/glorv) <!-- component: tikv --> <!-- pr: https://github.com/tikv/tikv/pull/19895 -->
    - 修复在 `tidb` 模式下使用 TiDB Lightning 导入数据时，TiKV 可能崩溃的问题 [#18671](https://github.com/tikv/tikv/issues/18671) @[Dog-Du](https://github.com/Dog-Du) <!-- component: tikv --> <!-- pr: https://github.com/tikv/tikv/pull/19907 -->
    - 修复 TiKV In-Memory Engine 在发生 etcd compaction 错误后可能停止更新 Region Label，导致 Label Watch 无限重试的问题 [#19792](https://github.com/tikv/tikv/issues/19792) @[akashchakrabortymsc-cmd](https://github.com/akashchakrabortymsc-cmd) <!-- component: tikv --> <!-- pr: https://github.com/tikv/tikv/pull/19898 -->
    - 修复当内存引擎缓存预热卡住，且在 ACK 截止时间前重复收到 Leader Transfer 请求时，Region Leader 转移可能被无限阻塞的问题 [#19776](https://github.com/tikv/tikv/issues/19776) @[overvenus](https://github.com/overvenus) <!-- component: tikv --> <!-- pr: https://github.com/tikv/tikv/pull/19921 -->
    - 修复 RocksDB Compaction 短暂出现峰值时，TiKV 可能执行不必要的写入流控的问题 [#19667](https://github.com/tikv/tikv/issues/19667) @[hbisheng](https://github.com/hbisheng) <!-- component: tikv --> <!-- pr: https://github.com/tikv/tikv/pull/19828 -->

+ PD

    - 修复 PD `/metric/query` 和 `/metric/query_range` 接口可能被用于发起 SSRF 攻击或泄露上游响应详细信息的问题 @[rleungx](https://github.com/rleungx) <!-- component: pd --> <!-- pr: https://github.com/tikv/pd/pull/11107 -->
    - 修复同一资源组内各 TiDB 实例请求速率不均衡时，RU Token 可能分配不均，导致高需求实例的 RU 等待时间过长和延迟升高的问题 [#9605](https://github.com/tikv/pd/issues/9605) @[JmPotato](https://github.com/JmPotato) <!-- component: pd --> <!-- pr: https://github.com/tikv/pd/pull/10024 -->
    - 修复客户端指定任意 `ConfigPath` 或类似路径的配置名称时，PD GlobalConfig gRPC API 可能访问预期命名空间之外的 etcd Key 的问题 [#11079](https://github.com/tikv/pd/issues/11079) @[rleungx](https://github.com/rleungx) <!-- component: pd --> <!-- pr: https://github.com/tikv/pd/pull/11075 -->
    - 修复 PD 可能与调用方通过 `pd-forwarded-host` 指定的任意地址建立出站 gRPC 连接，而没有将转发目标限制为当前 PD Leader 公布的客户端 URL 的问题 [#11070](https://github.com/tikv/pd/issues/11070) @[rleungx](https://github.com/rleungx) <!-- component: pd --> <!-- pr: https://github.com/tikv/pd/pull/11091 -->
    - 修复新创建的资源组控制器与周期性状态更新发生竞争时，资源组客户端可能持续发送 `NaN` Token 请求的问题 [#11022](https://github.com/tikv/pd/issues/11022) @[JmPotato](https://github.com/JmPotato) <!-- component: pd --> <!-- pr: https://github.com/tikv/pd/pull/11028 -->

+ 工具

    + 备份恢复 (BR)

        - 修复 BR 在时间点恢复期间进行日志恢复时未执行配置的限速，导致日志 Apply 下载速度超过限制的问题 [#63505](https://github.com/pingcap/tidb/issues/63505) @[Leavrth](https://github.com/Leavrth) <!-- component: br --> <!-- pr: https://github.com/pingcap/tidb/pull/69153 -->
        - 修复使用 BR 对设置了 `AUTO_ID_CACHE=1` 的表执行时间点恢复后，首次执行 `INSERT` 可能出现重复键错误的问题 [#69485](https://github.com/pingcap/tidb/issues/69485) @[vldmit](https://github.com/vldmit) <!-- component: br --> <!-- pr: https://github.com/pingcap/tidb/pull/70253 -->
        - 修复停止日志备份任务后，BR 日志备份会残留过期的 GC Safepoint，可能影响清理和 Safepoint 管理的问题 [#19832](https://github.com/tikv/tikv/issues/19832) @[Leavrth](https://github.com/Leavrth) <!-- component: br --> <!-- pr: https://github.com/tikv/tikv/pull/19911 -->
        - 修复多个恢复任务并发运行时，BR 无法正确更新 SST 下载限速，可能导致其中某个任务的限速变更不生效的问题 [#19454](https://github.com/tikv/tikv/issues/19454) @[Leavrth](https://github.com/Leavrth) <!-- component: br --> <!-- pr: https://github.com/tikv/tikv/pull/19924 -->

    + TiCDC

        - 修复 Maintainer 故障转移期间 TiCDC 可能创建重复的 Dispatcher，导致下游写入冲突的问题 [#5083](https://github.com/pingcap/ticdc/issues/5083) @[hongyunyan](https://github.com/hongyunyan) <!-- component: cdc --> <!-- pr: https://github.com/pingcap/ticdc/pull/5788 --> <!-- pr: https://github.com/pingcap/ticdc/pull/5792 --> <!-- pr: https://github.com/pingcap/ticdc/pull/5791 -->
        - 修复 Kafka Controller 故障后，TiCDC 上下游数据可能不一致的问题 [#5437](https://github.com/pingcap/ticdc/issues/5437) @[3AceShowHand](https://github.com/3AceShowHand) <!-- component: cdc --> <!-- pr: https://github.com/pingcap/ticdc/pull/5773 -->
        - 修复升级 TiCDC 后，已有 Changefeed ID 的 JSON 元数据使用旧版 `namespace` 字段而非 `keyspace` 时，Changefeed 可能消失的问题 [#4079](https://github.com/pingcap/ticdc/issues/4079) @[wlwilliamx](https://github.com/wlwilliamx) <!-- component: cdc --> <!-- pr: https://github.com/pingcap/ticdc/pull/5332 -->
        - 修复复制 `CREATE TABLE ... LIKE ...` 时，如果 Changefeed 过滤掉了被引用的源表，TiCDC Checkpoint 推进可能卡住的问题 [#5150](https://github.com/pingcap/ticdc/issues/5150) @[lidezhu](https://github.com/lidezhu) <!-- component: cdc --> <!-- pr: https://github.com/pingcap/ticdc/pull/5951 -->
        - 修复 Changefeed 已完成、停止、删除或迁移到其他 Owner 后，TiCDC Owner 的 Checkpoint 时间戳和延迟指标仍保留旧值的问题 [#5490](https://github.com/pingcap/ticdc/issues/5490) @[asddongmen](https://github.com/asddongmen) <!-- component: cdc --> <!-- pr: https://github.com/pingcap/ticdc/pull/5766 -->
        - 修复在 TiCDC 新架构中发生故障转移或 Dispatcher 重置后，Changefeed 可能卡住的问题 [#5553](https://github.com/pingcap/ticdc/issues/5553) @[asddongmen](https://github.com/asddongmen) <!-- component: cdc --> <!-- pr: https://github.com/pingcap/ticdc/pull/5769 -->
        - 修复 TiCDC Maintainer 被移除且已开始执行关闭交接后，仍可能继续重新调度或重新创建 Dispatcher 的问题 [#4827](https://github.com/pingcap/ticdc/issues/4827) @[wlwilliamx](https://github.com/wlwilliamx) <!-- component: cdc --> <!-- pr: https://github.com/pingcap/ticdc/pull/5403 -->
        - 修复 TiCDC 清理残留的 Async Commit 锁时，`ScanLock` 的目标时间戳可能将 TiKV 本地 MaxTS 推进到最新 PD TSO 之后，导致过期锁清理失败的问题 [#5418](https://github.com/pingcap/ticdc/issues/5418) @[tenfyzhong](https://github.com/tenfyzhong) <!-- component: cdc --> <!-- pr: https://github.com/pingcap/ticdc/pull/5753 -->
        - 修复表被删除后，TiCDC Event Service 可能重复扫描同一个 Raw Event，导致扫描进度停滞的问题 [#5040](https://github.com/pingcap/ticdc/issues/5040) @[asddongmen](https://github.com/asddongmen) <!-- component: cdc --> <!-- pr: https://github.com/pingcap/ticdc/pull/5765 -->
        - 修复 Maintainer 故障转移可能使正在执行的调度或 Merge Operator 处于不一致状态，导致 TiCDC 的表调度无法自动收敛的问题 [#4763](https://github.com/pingcap/ticdc/issues/4763) @[wlwilliamx](https://github.com/wlwilliamx) <!-- component: cdc --> <!-- pr: https://github.com/pingcap/ticdc/pull/5817 -->
        - 修复 Region Event 推送因流控而暂停时，TiCDC 在优雅退出过程中可能卡住的问题 [#5608](https://github.com/pingcap/ticdc/issues/5608) @[lidezhu](https://github.com/lidezhu) <!-- component: cdc --> <!-- pr: https://github.com/pingcap/ticdc/pull/5754 -->
        - 修复在 Maintainer 确认到达之前，TiCDC Table Trigger 的 Checkpoint 可能越过 Add Table DDL，导致新添加表的 Dispatcher 跳过后续表 DDL 的问题 [#5401](https://github.com/pingcap/ticdc/issues/5401) @[hongyunyan](https://github.com/hongyunyan) <!-- component: cdc --> <!-- pr: https://github.com/pingcap/ticdc/pull/5787 -->
        - 修复同一次 Maintainer Heartbeat 中 Checkpoint 有所推进时，TiCDC 可能忽略不可重试的 Changefeed 错误，导致 Changefeed 仍保持正常状态而未进入失败状态的问题 [#5246](https://github.com/pingcap/ticdc/issues/5246) @[3AceShowHand](https://github.com/3AceShowHand) <!-- component: cdc --> <!-- pr: https://github.com/pingcap/ticdc/pull/5771 -->
        - 修复使用 Avro 或 Debezium-Avro 的 TiCDC Changefeed 在 Schema Registry 返回 HTTP 500 错误时可能仍报告健康状态的问题。修复后，受影响的 Changefeed 会报告 Warning 状态，并在 `last_warning` 中记录 Schema Registry 错误 [#5653](https://github.com/pingcap/ticdc/issues/5653) @[wk989898](https://github.com/wk989898) <!-- component: cdc --> <!-- pr: https://github.com/pingcap/ticdc/pull/5823 -->
        - 修复批量创建大量空闲 Changefeed 时，Coordinator 未遵循配置的 Scheduler 并发限制，导致 TiCDC 内存和 CPU 使用出现峰值的问题 [#4831](https://github.com/pingcap/ticdc/issues/4831) @[wlwilliamx](https://github.com/wlwilliamx) <!-- component: cdc --> <!-- pr: https://github.com/pingcap/ticdc/pull/5396 -->
        - 修复 Capture 替换后，已删除的 View 被错误地作为物理表进行调度并遗留孤立的 Dispatcher，导致 TiCDC Changefeed Checkpoint 可能停止推进的问题 [#5710](https://github.com/pingcap/ticdc/issues/5710) @[asddongmen](https://github.com/asddongmen) <!-- component: cdc --> <!-- pr: https://github.com/pingcap/ticdc/pull/5770 -->
        - 修复 TiCDC 新架构中因硬编码最高兼容版本，可能导致 TiCDC 错误拒绝较新版本 PD、TiKV 或 TiCDC 的问题 [#4681](https://github.com/pingcap/ticdc/issues/4681) @[wlwilliamx](https://github.com/wlwilliamx) <!-- component: cdc --> <!-- pr: https://github.com/pingcap/ticdc/pull/5327 -->
        - 修复创建 Changefeed 后 Consumer 立即启动时，TiCDC Kafka Changefeed 可能使用 Broker 默认分区配置创建 Topic，导致消息投递失败并增加复制延迟的问题 [#5896](https://github.com/pingcap/ticdc/issues/5896) @[3AceShowHand](https://github.com/3AceShowHand) <!-- component: cdc --> <!-- pr: https://github.com/pingcap/ticdc/pull/5897 -->
        - 修复过期的 TiCDC Capture 在丢失其 etcd Session 后仍可能继续向下游写入，导致故障转移期间出现重复或不安全的下游写入的问题 [#5202](https://github.com/pingcap/ticdc/issues/5202) @[asddongmen](https://github.com/asddongmen) <!-- component: cdc --> <!-- pr: https://github.com/pingcap/ticdc/pull/5764 -->
        - 修复共享下游连接池耗尽后，如果 DDL 和元数据操作被 DML Session 阻塞，TiCDC MySQL Sink 可能卡住的问题 [#5360](https://github.com/pingcap/ticdc/issues/5360) @[hongyunyan](https://github.com/hongyunyan) <!-- component: cdc --> <!-- pr: https://github.com/pingcap/ticdc/pull/5763 -->
        - 修复所有底层 Region 尚未完成初始扫描时，TiCDC 可能提前将 Subscription Span 标记为已初始化，导致依赖初始化完成的操作过早触发的问题 [#5658](https://github.com/pingcap/ticdc/issues/5658) @[lidezhu](https://github.com/lidezhu) <!-- component: cdc --> <!-- pr: https://github.com/pingcap/ticdc/pull/5757 -->
        - 修复 `cdc cli changefeed resume` 对正在运行的 Changefeed 错误报告成功，并为无效的 Resume 请求创建不必要的临时 Resume GC Guard 的问题 [#4893](https://github.com/pingcap/ticdc/issues/4893) @[wlwilliamx](https://github.com/wlwilliamx) <!-- component: cdc --> <!-- pr: https://github.com/pingcap/ticdc/pull/5328 -->
        - 修复 Sink URI 校验失败时，TiCDC 可能在 OpenAPI 错误信息和日志中泄露敏感 Sink URI 信息的问题 [#5094](https://github.com/pingcap/ticdc/issues/5094) @[asddongmen](https://github.com/asddongmen) <!-- component: cdc --> <!-- pr: https://github.com/pingcap/ticdc/pull/5762 -->
        - 修复 Checkpoint 推进后，TiCDC Kafka、Pulsar 和 Storage Consumer 可能忽略乱序重放的 DML 事件，导致下游数据不一致的问题 [#5713](https://github.com/pingcap/ticdc/issues/5713) @[wk989898](https://github.com/wk989898) <!-- component: cdc --> <!-- pr: https://github.com/pingcap/ticdc/pull/5833 -->
        - 修复故障转移或消息乱序期间，TiCDC 下游 Consumer 可能在对应 DDL 处理完成前应用 DML 事件，导致 `Unknown column` 等错误的问题 [#5587](https://github.com/pingcap/ticdc/issues/5587) @[wk989898](https://github.com/wk989898) <!-- component: cdc --> <!-- pr: https://github.com/pingcap/ticdc/pull/5778 -->
        - 修复上游 GC 已清理初始 Schema Snapshot 时，TiCDC Schema Store 初始化可能无限重试，导致 Changefeed 在从网络分区等故障恢复后持续卡住的问题 [#3249](https://github.com/pingcap/ticdc/issues/3249) @[asddongmen](https://github.com/asddongmen) <!-- component: cdc --> <!-- pr: https://github.com/pingcap/ticdc/pull/5768 -->
        - 修复 TiCDC 收到格式错误的 Heartbeat 或拥塞控制消息时，可能泄漏 Changefeed 扫描配额或发生 panic 的问题 [#5642](https://github.com/pingcap/ticdc/issues/5642) @[lidezhu](https://github.com/lidezhu) <!-- component: cdc --> <!-- pr: https://github.com/pingcap/ticdc/pull/5752 -->
        - 修复在 DR Auto-Sync 场景中发生网络分区时，由于 tiflow 依赖版本过旧，TiCDC 可能触发 TiKV panic 的问题 [#5774](https://github.com/pingcap/ticdc/issues/5774) @[wk989898](https://github.com/wk989898) <!-- component: cdc --> <!-- pr: https://github.com/pingcap/ticdc/pull/5780 -->
        - 修复多次执行 Redo Apply 时 TiCDC 可能耗尽内存的问题。修复后，事件收集器支持同时按事件数量和总字节数进行批处理，并支持在 Changefeed 配置中覆盖批处理设置 [#5950](https://github.com/pingcap/ticdc/issues/5950) @[3AceShowHand](https://github.com/3AceShowHand) <!-- component: cdc --> <!-- pr: https://github.com/pingcap/ticdc/pull/5942 -->
        - 修复对分区表执行 `TRUNCATE TABLE` 后，当 Event Service 扫描窗口被固定且 DDL Barrier 无法推进时，TiCDC Changefeed 可能卡住的问题 [#4365](https://github.com/pingcap/ticdc/issues/4365) @[asddongmen](https://github.com/asddongmen) <!-- component: cdc --> <!-- pr: https://github.com/pingcap/ticdc/pull/5761 -->
        - 修复全局扫描窗口被固定且某个 Dispatcher 存在待处理的同步点 Barrier 时，TiCDC Event Service 扫描进度可能停滞的问题 [#5546](https://github.com/pingcap/ticdc/issues/5546) @[asddongmen](https://github.com/asddongmen) <!-- component: cdc --> <!-- pr: https://github.com/pingcap/ticdc/pull/5761 -->

    + TiDB Lightning

        - 修复发生临时的冲突删除提交错误后，`IMPORT INTO` 可能在索引不一致的情况下仍报告成功的问题 [#69792](https://github.com/pingcap/tidb/issues/69792) @[D3Hunter](https://github.com/D3Hunter) <!-- component: lightning --> <!-- pr: https://github.com/pingcap/tidb/pull/70254 -->
        - 修复导入出错或重试后，本地 Engine 文件未正确清理时，`IMPORT INTO` 可能因 `lock held by current process` 错误而失败的问题 [#65645](https://github.com/pingcap/tidb/issues/65645) @[D3Hunter](https://github.com/D3Hunter) <!-- component: lightning --> <!-- pr: https://github.com/pingcap/tidb/pull/69478 -->
        - 修复 `IMPORT INTO` 对重复的字典编码 Parquet `DECIMAL` 值可能静默写入错误数据的问题 [#70365](https://github.com/pingcap/tidb/issues/70365) @[joechenrh](https://github.com/joechenrh) <!-- component: lightning --> <!-- pr: https://github.com/pingcap/tidb/pull/70461 -->
        - 修复任务生成被取消时，`IMPORT INTO` 或相关的 Local Backend Ingest 任务可能卡住的问题 [#69240](https://github.com/pingcap/tidb/issues/69240) @[D3Hunter](https://github.com/D3Hunter) <!-- component: lightning, dxf --> <!-- pr: https://github.com/pingcap/tidb/pull/70234 -->