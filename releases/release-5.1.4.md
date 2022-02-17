---
title: TiDB 5.1.4 Release Note
---

# TiDB 5.1.4 Release Note

发版日期：2022 年 2 月 22 日

TiDB 版本：5.1.4

## 兼容性更改

+ TiDB

    - 将系统变量 [`tidb_analyze_version`](/system-variables.md#tidb_analyze_version-从-v510-版本开始引入) 的默认值从 `2` 修改`1` [#31748](https://github.com/pingcap/tidb/issues/31748)

+ TiKV

    - 开启了 `storage.enable-ttl` 的 TiKV 会拒绝 TiDB 的请求 [#27303](https://github.com/pingcap/tidb/issues/27303)

+ Tools

    + TiCDC

        - 将 `max-message-bytes` 默认值设置为 10M [#4041](https://github.com/pingcap/tiflow/issues/4041)

## 功能增强

+ TiDB

    - 支持在 Range 类型分区表中对 `IN` 表达式进行分区裁剪 [#26739](https://github.com/pingcap/tidb/issues/26739)
    - 提高在 `IndexJoin` 执行过程中追踪内存占用的准确度 [#28650](https://github.com/pingcap/tidb/issues/28650)

+ TiKV

    - Update procfs to 0.12.0 [#11702](https://github.com/tikv/tikv/issues/11702)
    - Improve raft client error log report [#11959](https://github.com/tikv/tikv/issues/11959)
    - Avoid false "GC can not work" alert under low write flow. [#10664](https://github.com/tikv/tikv/pull/10664)

+ TiFlash

    - 添加了 `ADDDATE()` 和 `DATE_ADD()` 到 TiFlash 的下推支持
    - 添加了 `INET6_ATON()` 和 `INET6_NTOA()` 到 TiFlash 的下推支持
    - 添加了 `INET_ATON()` 和 `INET_NTOA()` 到 TiFlash 的下推支持
    - 把 DAG Request 中表达式或者执行计划树的最大深度限制从 100 提升到 200

+ PD

    (dup) - Speed up the exit process of schedulers [#4146](https://github.com/tikv/pd/issues/4146)

+ Tools

    + TiCDC

        - 为 changefeed 重启操作添加指数退避机制 [#3329](https://github.com/pingcap/tiflow/issues/3329)
        - 优化多表场景下的 checkpoint 同步延迟 [#3900](https://github.com/pingcap/tiflow/issues/3900)
        - 增加观察 incremental scan 剩余时间的指标 [#2985](https://github.com/pingcap/tiflow/issues/2985)
        - 降低 TiKV 遇到 OOM 错误时，TiCDC 打印 "EventFeed retry rate limited" 日志的频率 [#4006](https://github.com/pingcap/tiflow/issues/4006)

        (dup) - Reduce the frequency of CDC reporting "EventFeed retry rate limited" logs when TiKV encounters OOM error [#4006](https://github.com/pingcap/tiflow/issues/4006)
        (dup) - Optimize checkpoint lag when capturing many tables [#3900](https://github.com/pingcap/tiflow/issues/3900)
        (dup) - Add more Promethous and Grafana monitoring metrics and alerts, including `no owner alert`, `mounter row`, `table sink total row`, and `buffer sink total row` [#4054](https://github.com/pingcap/tiflow/issues/4054) [#1606](https://github.com/pingcap/tiflow/issues/1606)
        (dup) - Optimize rate limiting control on TiKV reloads to reduce gPRC congestion during changefeed initialization [#3110](https://github.com/pingcap/ticdc/issues/3110)

## Bug 修复

+ TiDB

    - 修复当系统变量 `@@tidb_analyze_version = 2` 时出现的内存泄露问题 [#29305](https://github.com/pingcap/tidb/pull/29305)
    - 修复 `MaxDays` 和 `MaxBackups` 配置项对慢日志不生效的问题 [#25716](https://github.com/pingcap/tidb/issues/25716)
    - 修复使用 `ON DUPLICATE KEY UPDATE` 语法时，TiDB Server 可能 panic 的问题 [#28078](https://github.com/pingcap/tidb/issues/28078)
    - 修复使用 `ENUM` 类型的列进行 Join 时结果可能不正确的问题 [#27831](https://github.com/pingcap/tidb/issues/27831)
    - 修复使用 `IndexHashJoin` 时可能报错 `send on closed channel` 的问题 [#31129](https://github.com/pingcap/tidb/issues/31129)
    - 修复使用 [`BatchCommands`](/tidb-configuration-file.md#max-batch-size) 时，少数情况下 TiDB 数据请求无法及时发送到 TiKV 的问题 [#27678](https://github.com/pingcap/tidb/pull/27678)
    (dup) - Fix the data inconsistency issue caused by incorrect usage of lazy existence check and untouched key optimization [#30410](https://github.com/pingcap/tidb/issues/30410)
    (dup) - Fix the issue that window functions might return different results when using a transaction or not [#29947](https://github.com/pingcap/tidb/issues/29947)
    (dup) - Fix the issue that the length information is wrong when casting `Decimal` to `String` [#29417](https://github.com/pingcap/tidb/issues/29417)
    (dup) - Fix the issue that the `GREATEST` function returns inconsistent results due to different values of `tidb_enable_vectorized_expression` (set to `on` or `off`) [#29434](https://github.com/pingcap/tidb/issues/29434)
    (dup) - Fix the issue that the planner might cache invalid plans for `join` in some cases [#28087](https://github.com/pingcap/tidb/issues/28087)
    (dup) - Fix wrong results of the `microsecond` function in vectorized expressions [#29244](https://github.com/pingcap/tidb/issues/29244)
    (dup) - Fix the TiDB panic when executing the `ALTER TABLE.. ADD INDEX` statement in some cases [#27687](https://github.com/pingcap/tidb/issues/27687)
    (dup) - Fix wrong results of the `hour` function in vectorized expression [#28643](https://github.com/pingcap/tidb/issues/28643)
    (dup) - Fix a bug that the availability detection of MPP node does not work in some corner cases [#3118](https://github.com/pingcap/tics/issues/3118)
    (dup) - Fix the `DATA RACE` issue when assigning `MPP task ID` [#27952](https://github.com/pingcap/tidb/issues/27952)
    (dup) - Fix the `INDEX OUT OF RANGE` error for a MPP query after deleting an empty `dual table` [#28250](https://github.com/pingcap/tidb/issues/28250)
    (dup) - Fix the issue of false positive error log `invalid cop task execution summaries length` for MPP queries [#1791](https://github.com/pingcap/tics/issues/1791)

+ TiFlash

    - 修复了 `str_to_date()` 函数对微秒前导零的错误解析
    - 修复了 TiFlash 在内存限制打开时的崩溃
    - 对齐了 TiFlash 与 TiDB/MySQL 的当时间早于 1970-01-01 00:00:01 UTC 时函数 `unix_timestamp` 的行为
    - 修复了扩宽为 handle 的主键列时潜在的数据不一致性问题
    - 修复了 Decimal 之间比较时可能导致的溢出问题和 `Can't compare` 报错
    - 修复了非预期错误 `3rd arguments of function substringUTF8 must be constants.`
    - 修复了在没有 `nsl` 库的平台上 TiFlash 无法启动的问题
    - 修复了到 Decimal 类型转换时的溢出问题
    - 修复了 TiFlash 上 `CastStringAsReal` 函数与 TiDB/TiKV 行为不一致的问题
    - 修复了 TiFlash 重启后随机的 `EstablishMPPConnection` 失败错误
    - 修复了当设置 TiFlash 副本数为 0（即删除数据）后数据无法回收的问题
    - 修复了 TiFlash 上 `CastStringAsDecimal` 函数与 TiDB/TiKV 行为不一致的问题
    - 修复了 TiFlash 上 `where <string>` 中因为字符串被转换为整数类型导致错误结果的问题
    - 修复了当 MPP 查询被终止后 TiFlash 随机奔溃的问题
    - 修复了非预期的 `Unexpected type of column: Nullable(Nothing)` 报错

+ TiKV

    - 修复了 GC worker 繁忙后无法执行范围删除的问题 [#11903](https://github.com/tikv/tikv/issues/11903)
    - 避免删除 peer 造成潜在的高延迟 [#10210](https://github.com/tikv/tikv/issues/10210)
    - 修复了 region 没有数据时 `any_value` 函数结果错误 [#11735](https://github.com/tikv/tikv/issues/11735)
    - 修复了删除未初始化的副本可能会造成旧副本被重新创建的问题 [#10533](https://github.com/tikv/tikv/issues/10533)
    - 修复了在新选举但未能通知隔离了的 peer 后 prepare merge 造成元数据损坏的问题 [#11526](https://github.com/tikv/tikv/issues/11526)
    - 修复了协程执行太快时偶尔出现的死锁问题 [#11549](https://github.com/tikv/tikv/issues/11549)
    - 避免抓取火焰图时潜在的死锁和内存泄漏 [#11108](https://github.com/tikv/tikv/issues/11108)
    - 修复了悲观事务中重试 prewrite 有可能破坏数据一致性的问题 [#11187](https://github.com/tikv/tikv/issues/11187)
    - 修复了 resource-metering.enabled 配置不生效的问题 [#11235](https://github.com/tikv/tikv/issues/11235)
    - 修复了 resolved_ts 模块中的协程泄漏.  [#10965](https://github.com/tikv/tikv/issues/10965)
    - 避免低写入流量时误报 GC can not work 警告 [#9910](https://github.com/tikv/tikv/issues/9910)
    - 修复了 tikv-ctl 无法正确输出 region 相关信息的问题 [#11393](https://github.com/tikv/tikv/issues/11393)

    (dup) - Fix the issue that a down TiKV node causes the resolved timestamp to lag [#11351](https://github.com/tikv/tikv/issues/11351)
    (dup) - Fix a panic issue that occurs when Region merge, ConfChange, and Snapshot happen at the same time in extreme conditions [#11475](https://github.com/tikv/tikv/issues/11475)
    (dup) - Fix the issue that TiKV cannot detect the memory lock when TiKV perform a reverse table scan [#11440](https://github.com/tikv/tikv/issues/11440)
    (dup) - Fix the issue of negative sign when the decimal divide result is zero [#29586](https://github.com/pingcap/tidb/issues/29586)
    (dup) - Increase the speed of inserting SST files by moving the verification process to the `Import` thread pool from the `Apply` thread pool [#11239](https://github.com/tikv/tikv/issues/11239)
    (dup) - Fix a memory leak caused by monitoring data of statistics threads [#11195](https://github.com/tikv/tikv/issues/11195)
    (dup) - Fix the issue of TiCDC panic that occurs when the downstream database is missing [#11123](https://github.com/tikv/tikv/issues/11123)
    (dup) - Fix the issue that TiCDC adds scan retries frequently due to the Congest error [#11082](https://github.com/tikv/tikv/issues/11082)
    (dup) - Fix the issue that batch messages are too large in Raft client implementation [#9714](https://github.com/tikv/tikv/issues/9714)
    (dup) - Collapse some uncommon storage-related metrics in Grafana dashboard [#11681](https://github.com/tikv/tikv/issues/11681)

+ PD

    - Fix the bug that the region scatterer may generate the schedule with too few peers. [#4565](https://github.com/tikv/pd/issues/4565)
    - Fix the bug that region statistics are not updated after `flow-round-by-digit` change. [#4295](https://github.com/tikv/pd/issues/4295)

    (dup) - Fix slow leader election caused by stucked region syncer [#3936](https://github.com/tikv/pd/issues/3936)
    (dup) - Support that the evict leader scheduler can schedule regions with unhealthy peers [#4093](https://github.com/tikv/pd/issues/4093)
    (dup) - Fix the issue that the hotspot cache cannot be cleared when the Region heartbeat is less than 60 seconds [#4390](https://github.com/tikv/pd/issues/4390)
    (dup) - Fix a panic issue that occurs after the TiKV node is removed [#4344](https://github.com/tikv/pd/issues/4344)
    (dup) - Fix the issue that operator can get blocked due to down store [#3353](https://github.com/tikv/pd/issues/3353)

+ Tools

    + TiCDC

        - 修复 MySQL sink 在禁用 `batch-replace-enable` 参数时生成重复 `replace` SQL 语句的错误 [#4501](https://github.com/pingcap/tiflow/issues/4501)
        - 修复 `kv client cached regions` 指标可能为负数的问题 [#4300](https://github.com/pingcap/tiflow/issues/4300)
(dup)- 修复当 `min.insync.replicas` 小于 `replication-factor` 时不能同步的问题 [#3994](https://github.com/pingcap/tiflow/issues/3994)
(dup)- 修复在移除同步任务后潜在的 panic 问题 [#3128](https://github.com/pingcap/tiflow/issues/3128)
(dup) - 修复因 checkpoint 不准确导致的潜在的数据丢失问题 [#3545](https://github.com/pingcap/tiflow/issues/3545)
(dup) - 修复潜在的同步流控死锁问题 [#4055](https://github.com/pingcap/tiflow/issues/4055)
(dup) - 修复 DDL 特殊注释导致的同步停止的问题 [#3755](https://github.com/pingcap/tiflow/issues/3755)
        - 修复 EtcdWorker 可能阻塞 owner 和 processor 的问题 [#3750](https://github.com/pingcap/tiflow/issues/3750)
        - 修复集群升级后处于 `stopped` 状态的 changefeed 自动恢复的问题 [#3473](https://github.com/pingcap/tiflow/issues/3473)
        - 修复 TiCDC 与 TiDB amend 机制在数据类型上的兼容性问题 [#3793](https://github.com/pingcap/tiflow/issues/3793)
        - 修复 TiCDC 默认值填充异常导致的数据不一致问题 [#3918](https://github.com/pingcap/tiflow/issues/3918) [#3929](https://github.com/pingcap/tiflow/issues/3929)
        - 修复当 PD leader 故障后转移到其他节点时 owner 卡住的问题 [#3615](https://github.com/pingcap/tiflow/issues/3615)
        - 修复在 TiKV 部分节点故障后 TiCDC `kv client` 恢复时间过长的问题 [#3191](https://github.com/pingcap/tiflow/issues/3191)
        - Nond [#2983](https://github.com/pingcap/tiflow/issues/2983)

        (dup) - Fix the TiCDC panic issue that occurs when manually cleaning the task status in etcd [#2980](https://github.com/pingcap/tiflow/issues/2980)
        (dup) - Fix the timezone error that occurs when the `cdc server` command runs on some Red Hat Enterprise Linux releases (such as 6.8 and 6.9) [#3584](https://github.com/pingcap/tiflow/issues/3584)
        (dup) - Fix the issue of overly frequent warnings caused by MySQL sink deadlock [#2706](https://github.com/pingcap/tiflow/issues/2706)
        (dup) - Fix the bug that the `enable-old-value` configuration item is not automatically set to `true` on Canal and Maxwell protocols [#3676](https://github.com/pingcap/tiflow/issues/3676)
        (dup) - Fix the issue that Avro sink does not support parsing JSON type columns [#3624](https://github.com/pingcap/tiflow/issues/3624)
        (dup) - Fix the negative value error in the changefeed checkpoint lag [#3010](https://github.com/pingcap/ticdc/issues/3010)
        (dup) - Fix OOM in container environments [#1798](https://github.com/pingcap/ticdc/issues/1798)
        (dup) - Fix the TiCDC replication interruption issue when multiple TiKVs crash or during a forced restart [#3288](https://github.com/pingcap/ticdc/issues/3288)
        (dup) - Fix the memory leak issue after processing DDLs [#3174](https://github.com/pingcap/ticdc/issues/3174)
        (dup) - Fix the issue that changefeed does not fail fast enough when the ErrGCTTLExceeded error occurs [#3111](https://github.com/pingcap/ticdc/issues/3111)
        (dup) - Fix the issue that TiCDC replication task might terminate when the upstream TiDB instance unexpectedly exits [#3061](https://github.com/pingcap/tiflow/issues/3061)
        (dup) - Fix the issue that TiCDC process might panic when TiKV sends duplicate requests to the same Region [#2386](https://github.com/pingcap/tiflow/issues/2386)
        (dup) - Fix the issue that the volume of Kafka messages generated by TiCDC is not constrained by `max-message-size` [#2962](https://github.com/pingcap/tiflow/issues/2962)
        (dup) - Fix the issue that Kafka may send excessively large messages by setting the default value of `max-message-bytes` to `10M` [#3081](https://github.com/pingcap/tiflow/issues/3081)
        (dup) - Fix the issue that TiCDC sync task might pause when an error occurs during writing a Kafka message [#2978](https://github.com/pingcap/tiflow/issues/2978)

    + Backup & Restore (BR)

        + 修复 restoring 后可能出现的 Region 不平衡的问题 [#30425](https://github.com/pingcap/tidb/issues/30425) [#31034](https://github.com/pingcap/tidb/issues/31034)

    + TiDB Lightning

        + 修复 S3 存储路径不存在时 TiDB Lightning 不报错的问题 [#28031](https://github.com/pingcap/tidb/issues/28031) [#30709](https://github.com/pingcap/tidb/issues/30709)