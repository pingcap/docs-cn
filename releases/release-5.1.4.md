---
title: TiDB 5.1.4 Release Notes
summary: TiDB 5.1.4 发布日期为 2022 年 2 月 22 日。此版本包含兼容性更改、提升改进和 Bug 修复。兼容性更改包括系统变量 `tidb_analyze_version` 默认值修改为 `1`，以及 TiKV 在开启 `storage.enable-ttl` 后拒绝 TiDB 请求。提升改进方面，TiDB 支持在 Range 类型分区表中对 `IN` 表达式进行分区裁剪，TiKV 升级了 proc filesystem 版本。Bug 修复方面，修复了多个 TiDB 和 TiKV 的问题，包括内存泄露、配置项不生效、panic 等。Tools 方面也有多个修复和改进，包括 TiCDC、Backup & Restore、TiDB Binlog 和 TiDB Lightning。
---

# TiDB 5.1.4 Release Notes

发版日期：2022 年 2 月 22 日

TiDB 版本：5.1.4

## 兼容性更改

+ TiDB

    - 将系统变量 [`tidb_analyze_version`](/system-variables.md#tidb_analyze_version-从-v510-版本开始引入) 的默认值从 `2` 修改为 `1` [#31748](https://github.com/pingcap/tidb/issues/31748)
    - 自 v5.1.4 起，TiKV 在开启 `storage.enable-ttl` 后会拒绝 TiDB 的请求，因为 TiKV 的 TTL 功能[仅支持 RawKV 模式](https://tikv.org/docs/5.1/concepts/explore-tikv-features/ttl/) [#27303](https://github.com/pingcap/tidb/issues/27303)

+ Tools

    + TiCDC

        - 将 `max-message-bytes` 默认值设置为 10M [#4041](https://github.com/pingcap/tiflow/issues/4041)

## 提升改进

+ TiDB

    - 支持在 Range 类型分区表中对 `IN` 表达式进行分区裁剪 [#26739](https://github.com/pingcap/tidb/issues/26739)
    - 提高在 `IndexJoin` 执行过程中追踪内存占用的准确度 [#28650](https://github.com/pingcap/tidb/issues/28650)

+ TiKV

    - 将 proc filesystem (procfs) 升级至 0.12.0 版本 [#11702](https://github.com/tikv/tikv/issues/11702)
    - 优化 Raft client 错误日志的收集 [#11959](https://github.com/tikv/tikv/issues/11959)
    - 将插入 SST 文件时的校验操作从 Apply 线程池移动到 Import 线程池，从而提高 SST 文件的插入速度 [#11239](https://github.com/tikv/tikv/issues/11239)

+ PD

    - 优化调度器退出的速度 [#4146](https://github.com/tikv/pd/issues/4146)

+ TiFlash

    - 添加 `ADDDATE()` 和 `DATE_ADD()` 到 TiFlash 的下推支持
    - 添加 `INET6_ATON()` 和 `INET6_NTOA()` 到 TiFlash 的下推支持
    - 添加 `INET_ATON()` 和 `INET_NTOA()` 到 TiFlash 的下推支持
    - 把 DAG Request 中表达式或者执行计划树的最大深度限制从 100 提升到 200

+ Tools

    + TiCDC

        - 为 changefeed 重启操作添加指数退避机制 [#3329](https://github.com/pingcap/tiflow/issues/3329)
        - 降低在同步大量表时的同步延时 [#3900](https://github.com/pingcap/tiflow/issues/3900)
        - 增加观察 incremental scan 剩余时间的指标 [#2985](https://github.com/pingcap/tiflow/issues/2985)
        - 减少 "EventFeed retry rate limited" 日志的数量 [#4006](https://github.com/pingcap/tiflow/issues/4006)
        - 增加更多 Prometheus 和 Grafana 监控告警参数，包括 `no owner alert`、`mounter row`、`table sink total row` 和 `buffer sink total row` [#4054](https://github.com/pingcap/tiflow/issues/4054) [#1606](https://github.com/pingcap/tiflow/issues/1606)
        - 优化 TiKV 重新加载时的速率限制控制，缓解 changefeed 初始化时 gPRC 的拥堵问题 [#3110](https://github.com/pingcap/tiflow/issues/3110)
        - 减少 TiKV 节点宕机后 KV client 恢复的时间 [#3191](https://github.com/pingcap/tiflow/issues/3191)

## Bug 修复

+ TiDB

    - 修复当系统变量 `@@tidb_analyze_version = 2` 时出现的内存泄露问题 [#32499](https://github.com/pingcap/tidb/issues/32499)
    - 修复 `MaxDays` 和 `MaxBackups` 配置项对慢日志不生效的问题 [#25716](https://github.com/pingcap/tidb/issues/25716)
    - 修复 `INSERT ... SELECT ... ON DUPLICATE KEY UPDATE` 语句 panic 的问题 [#28078](https://github.com/pingcap/tidb/issues/28078)
    - 修复使用 `ENUM` 类型的列进行 Join 时结果可能不正确的问题 [#27831](https://github.com/pingcap/tidb/issues/27831)
    - 修复 INDEX HASH JOIN 报 `send on closed channel` 的问题 [#31129](https://github.com/pingcap/tidb/issues/31129)
    - 修复使用 [`BatchCommands`](/tidb-configuration-file.md#max-batch-size) API 时，少数情况下 TiDB 数据请求无法及时发送到 TiKV 的问题 [#32500](https://github.com/pingcap/tidb/issues/32500)
    - 修复乐观事务下数据索引可能不一致的问题 [#30410](https://github.com/pingcap/tidb/issues/30410)
    - 修复窗口函数在使用事务时，计算结果与不使用事务时的计算结果不一致的问题 [#29947](https://github.com/pingcap/tidb/issues/29947)
    - 修复将 `Decimal` 转为 `String` 时长度信息错误的问题 [#29417](https://github.com/pingcap/tidb/issues/29417)
    - 修复将向量化表达式 `tidb_enable_vectorized_expression` 设置为 `off` 时，`GREATEST` 函数返回结果可能不正确的问题 [#29434](https://github.com/pingcap/tidb/issues/29434)
    - 修复在某些情况下优化器可能缓存无效 `join` 计划的问题 [#28087](https://github.com/pingcap/tidb/issues/28087)
    - 修复向量化表达式设置为 `on` 时，`microsecond` 和 `hour` 函数返回结果可能不正确的问题 [#29244](https://github.com/pingcap/tidb/issues/29244) [#28643](https://github.com/pingcap/tidb/issues/28643)
    - 修复在某些场景下执行 `ALTER TABLE.. ADD INDEX` 语句时 TiDB panic 的问题 [#27687](https://github.com/pingcap/tidb/issues/27687)
    - 修复 MPP 节点的可用性检测在某些边界场景中无法工作的问题 [#3118](https://github.com/pingcap/tics/issues/3118)
    - 修复分配 `MPP task ID` 时出现 `DATA RACE` 的问题 [#27952](https://github.com/pingcap/tidb/issues/27952)
    - 修复删除空的 `dual table` 后 MPP 查询出现 `index out of range` 报错的问题 [#28250](https://github.com/pingcap/tidb/issues/28250)
    - 修复运行 MPP 查询时出现 `invalid cop task execution summaries length` 相关日志的问题 [#1791](https://github.com/pingcap/tics/issues/1791)
    - 修复 SET GLOBAL tidb_skip_isolation_level_check=1 无法在新会话中生效的问题 [#27897](https://github.com/pingcap/tidb/issues/27897)
    - 修复 `tiup bench` 命令运行时间过长导致的 `index out of range` 问题 [#26832](https://github.com/pingcap/tidb/issues/26832)

+ TiKV

    - 修复 GC worker 繁忙后无法执行范围删除（即执行 `unsafe_destroy_range` 参数）的问题 [#11903](https://github.com/tikv/tikv/issues/11903)
    - 修复删除 Peer 可能造成高延迟的问题 [#10210](https://github.com/tikv/tikv/issues/10210)
    - 修复 Region 没有数据时 `any_value` 函数结果错误的问题 [#11735](https://github.com/tikv/tikv/issues/11735)
    - 修复删除未初始化的副本可能会造成旧副本被重新创建的问题 [#10533](https://github.com/tikv/tikv/issues/10533)
    - 修复在已完成重新选举但没有通知被隔离的 Peer 的情况下执行 `Prepare Merge` 会导致元数据损坏的问题 [#11526](https://github.com/tikv/tikv/issues/11526)
    - 修复协程的执行速度太快时偶尔出现的死锁问题 [#11549](https://github.com/tikv/tikv/issues/11549)
    - 修复分析火焰图时潜在的死锁和内存泄漏的问题 [#11108](https://github.com/tikv/tikv/issues/11108)
    - 修复悲观事务中 prewrite 请求重试在极少数情况下影响数据一致性的风险 [#11187](https://github.com/tikv/tikv/issues/11187)
    - 修复 `resource-metering.enabled` 配置不生效的问题 [#11235](https://github.com/tikv/tikv/issues/11235)
    - 修复 `resolved_ts` 中协程泄漏的问题 [#10965](https://github.com/tikv/tikv/issues/10965)
    - 修复在低写入流量下误报 "GC can not work" 错误的问题 [#9910](https://github.com/tikv/tikv/issues/9910)
    - 修复 tikv-ctl 无法正确输出 Region 相关信息的问题 [#11393](https://github.com/tikv/tikv/issues/11393)
    - 修复某个 TiKV 节点停机会导致 Resolved Timestamp 进度落后的问题 [#11351](https://github.com/tikv/tikv/issues/11351)
    - 修复在极端情况下同时进行 Region Merge、ConfChange 和 Snapshot 时，TiKV 会出现 Panic 的问题 [#11475](https://github.com/tikv/tikv/issues/11475)
    - 修复逆序扫表时 TiKV 无法正确读到内存锁的问题 [#11440](https://github.com/tikv/tikv/issues/11440)
    - 修复 Decimal 除法计算的结果为 0 时符号为负的问题 [#29586](https://github.com/pingcap/tidb/issues/29586)
    - 修复因统计线程监控数据导致的内存泄漏 [#11195](https://github.com/tikv/tikv/issues/11195)
    - 修复在缺失下游数据库时出现 TiCDC Panic 的问题 [#11123](https://github.com/tikv/tikv/issues/11123)
    - 修复因 Congest 错误而导致的 TiCDC 频繁增加 scan 重试的问题 [#11082](https://github.com/tikv/tikv/issues/11082)
    - 修复 Raft client 中 batch 消息过大的问题 [#9714](https://github.com/tikv/tikv/issues/9714)
    - 折叠了 Grafana Dashboard 中与 Storage 相关的不常用的监控指标 [#11681](https://github.com/tikv/tikv/issues/11681)

+ PD

    - 修复了 region scatter 生成的调度可能导致 peer 数量减少的问题 [#4565](https://github.com/tikv/pd/issues/4565)
    - 修复 Region 统计不受 `flow-round-by-digit` 影响的问题 [#4295](https://github.com/tikv/pd/issues/4295)
    - 修复因 Region syncer 卡住而导致 leader 选举慢的问题 [#3936](https://github.com/tikv/pd/issues/3936)
    - 允许 Evict Leader 调度器调度拥有不健康副本的 Region [#4093](https://github.com/tikv/pd/issues/4093)
    - 修复热点统计中无法剔除冷热点数据的问题 [#4390](https://github.com/tikv/pd/issues/4390)
    - 修复 TiKV 节点缩容后可能导致 Panic 的问题 [#4344](https://github.com/tikv/pd/issues/4344)
    - 修复调度 Operator 因为目标 Store 处于 Down 的状态而无法快速失败的问题 [#3353](https://github.com/tikv/pd/issues/3353)

+ TiFlash

    - 修复 `str_to_date()` 函数对微秒前导零的错误解析
    - 修复启用内存限制后 TiFlash 崩溃的问题
    - 修复输入早于 1970-01-01 00:00:01 UTC 时，`unix_timestamp` 行为与 TiDB/MySQL 不一致的问题
    - 修复当主键为 handle 时，扩宽主键列可能导致的数据不一致问题
    - 修复 Decimal 类型比较时可能出现的数据溢出问题和 `Can't compare` 报错
    - 修复非预期的 `3rd arguments of function substringUTF8 must be constants.` 报错
    - 修复在没有 `nsl` 库的平台上 TiFlash 无法启动的问题
    - 修复 Decimal 类型转换时的数据溢出问题
    - 修复在 TiFlash 与 TiDB/TiKV 之间 `castStringAsReal` 行为不一致的问题
    - 修复 TiFlash 重启时偶发的 `EstablishMPPConnection` 错误
    - 修复当设置 TiFlash 副本数为 0（即删除数据）后数据无法回收的问题
    - 修复在 TiFlash 与 TiDB/TiKV 之间 `CastStringAsDecimal` 行为不一致的问题
    - 修复 `where <string>` 查询结果出错的问题
    - 修复当 MPP 查询被终止时，TiFlash 偶发的崩溃问题
    - 修复非预期的 `Unexpected type of column: Nullable(Nothing)` 报错

+ Tools

    + TiCDC

        - 修复 MySQL sink 在禁用 `batch-replace-enable` 参数时生成重复 `replace` SQL 语句的错误 [#4501](https://github.com/pingcap/tiflow/issues/4501)
        - 修复 `cached region` 监控指标为负数的问题 [#4300](https://github.com/pingcap/tiflow/issues/4300)
        - 修复当 `min.insync.replicas` 小于 `replication-factor` 时不能同步的问题 [#3994](https://github.com/pingcap/tiflow/issues/3994)
        - 修复在移除同步任务后潜在的 panic 问题 [#3128](https://github.com/pingcap/tiflow/issues/3128)
        - 修复因 checkpoint 不准确导致的潜在的数据丢失问题 [#3545](https://github.com/pingcap/tiflow/issues/3545)
        - 修复潜在的同步流控死锁问题 [#4055](https://github.com/pingcap/tiflow/issues/4055)
        - 修复 DDL 特殊注释导致的同步停止的问题 [#3755](https://github.com/pingcap/tiflow/issues/3755)
        - 修复 EtcdWorker 可能阻塞 owner 和 processor 的问题 [#3750](https://github.com/pingcap/tiflow/issues/3750)
        - 修复集群升级后 `stopped` 状态的 changefeed 自动恢复的问题 [#3473](https://github.com/pingcap/tiflow/issues/3473)
        - 修复不支持同步默认值的问题 [#3793](https://github.com/pingcap/tiflow/issues/3793)
        - 修复 TiCDC 默认值填充异常导致的数据不一致问题 [#3918](https://github.com/pingcap/tiflow/issues/3918) [#3929](https://github.com/pingcap/tiflow/issues/3929)
        - 修复当 PD leader 故障后转移到其他节点时 owner 卡住的问题 [#3615](https://github.com/pingcap/tiflow/issues/3615)
        - 修复人为删除 etcd 任务的状态时导致 TiCDC panic 的问题 [#2980](https://github.com/pingcap/tiflow/issues/2980)
        - 修复在某些 RHEL 发行版上因时区问题导致服务无法启动的问题 [#3584](https://github.com/pingcap/tiflow/issues/3584)
        - 修复 MySQL sink 模块出现死锁时告警过于频繁的问题 [#2706](https://github.com/pingcap/tiflow/issues/2706)
        - 修复 Canal 协议下 TiCDC 没有自动开启 `enable-old-value` 选项的问题 [#3676](https://github.com/pingcap/tiflow/issues/3676)
        - 修复 Avro sink 模块不支持解析 JSON 类型列的问题 [#3624](https://github.com/pingcap/tiflow/issues/3624)
        - 修复监控 checkpoint lag 出现负值的问题 [#3010](https://github.com/pingcap/tiflow/issues/3010)
        - 修复在容器环境中 OOM 的问题 [#1798](https://github.com/pingcap/tiflow/issues/1798)
        - 修复在多个 TiKV 崩溃或强制重启时可能遇到复制中断的问题 [#3288](https://github.com/pingcap/tiflow/issues/3288)
        - 修复执行 DDL 后的内存泄漏的问题 [#3174](https://github.com/pingcap/tiflow/issues/3174)
        - 修复当发生 ErrGCTTLExceeded 错误时，changefeed 不快速失败的问题 [#3111](https://github.com/pingcap/tiflow/issues/3111)
        - 修复当上游 TiDB 实例意外退出时，TiCDC 同步任务推进可能停滞的问题 [#3061](https://github.com/pingcap/tiflow/issues/3061)
        - 修复当 TiKV 向同一 Region 发送重复请求时，TiCDC 进程 Panic 的问题 [#2386](https://github.com/pingcap/tiflow/issues/2386)
        - 将参数 `max-message-bytes` 的默认值设置为 `10M`，减少 Kafka 发送过大消息的概率 [#3081](https://github.com/pingcap/tiflow/issues/3081)
        - 修复当写入 Kafka 消息发生错误时，TiCDC 同步任务推进可能停滞的问题 [#2978](https://github.com/pingcap/tiflow/issues/2978)

    + Backup & Restore (BR)

        + 修复当恢复完成后，Region 有可能分布不均的问题 [#30425](https://github.com/pingcap/tidb/issues/30425) [#31034](https://github.com/pingcap/tidb/issues/31034)

    + TiDB Binlog

        修复 `strict-format` 为 `true` 且 CSV 文件大小为 256 MB 时，CSV 文件导入报 `InvalidRange` 的问题 [#27763](https://github.com/pingcap/tidb/issues/27763)

    + TiDB Lightning

        + 修复 S3 存储路径不存在时 TiDB Lightning 不报错的问题 [#28031](https://github.com/pingcap/tidb/issues/28031) [#30709](https://github.com/pingcap/tidb/issues/30709)
