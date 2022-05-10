---
title: TiDB 5.4.1 Release Notes
---


# TiDB 5.4.1 Release Notes

发版日期：2022 年 5 月 xx 日

TiDB 版本：5.4.1

## 兼容性更改

+ TiDB

    - note 1
    - note 2

+ TiKV

    - note 1
    - note 2

## 提升改进

+ TiDB

    - (dup: release-6.0.0-dmr.md > 提升改进> TiDB)- 支持读取 `_tidb_rowid` 列的查询能够使用 PointGet 计划 [#31543](https://github.com/pingcap/tidb/issues/31543)
    - 为 `Apply` 算子添加了一些调试信息 [#33887](https://github.com/pingcap/tidb/issues/33887)
    - 对于统计信息使用的 Analyze Version 2，优化了 `TopN` 裁剪的逻辑 [#34256](https://github.com/pingcap/tidb/issues/34256)
    - 在 Grafana 的仪表盘中支持显示多个 Kubernetes 集群 [#32593](https://github.com/pingcap/tidb/issues/32593)

+ TiKV

    - 使 Grafana 支持 multi-k8s 的监控[#12104](https://github.com/tikv/tikv/issues/12104)

+ PD

    - 使 Grafana 支持 multi-k8s 的监控 [#4673](https://github.com/tikv/pd/issues/4673)

+ TiFlash

    - Grafana 面板支持 multi-k8s 展示 [#4129](https://github.com/pingcap/tiflash/issues/4129)

+ Tools

    + TiCDC

        - (dup: release-5.2.4.md > 提升改进> Tools> TiCDC)- 在 Grafana 监控面板中支持多个 Kubernetes 集群 [#4665](https://github.com/pingcap/tiflow/issues/4665)
        - (dup: release-5.2.4.md > 提升改进> Tools> TiCDC)- 暴露 Kafka producer 配置参数，使之在 TiCDC 中可配置 [#4385](https://github.com/pingcap/tiflow/issues/4385)

    + TiDB Data Migration (DM)

        - (dup: release-6.0.0-dmr.md > 提升改进> Tools> TiDB Data Migration (DM))- 支持 Syncer 使用 DM-worker 的工作目录写内部文件，不再使用 /tmp 目录。任务停止后会清理掉该目录 [#4107](https://github.com/pingcap/tiflow/issues/4107)

## Bug 修复

+ TiDB

    - (dup: release-6.0.0-dmr.md > Bug 修复> TiDB)- 修复查询报错时可能阻塞 CTE 的问题 [#31302](https://github.com/pingcap/tidb/issues/31302)
    - (dup: release-5.2.4.md > Bug 修复> TiDB)- 修复 Nulleq 函数作用在 Enum 类型上可能出现结果错误的问题 [#32428](https://github.com/pingcap/tidb/issues/32428)
    - (dup: release-6.0.0-dmr.md > Bug 修复> TiDB)- 修复使用 ChunkRPC 导出数据时可能造成 TiDB OOM 的问题 [#31981](https://github.com/pingcap/tidb/issues/31981) [#30880](https://github.com/pingcap/tidb/issues/30880)
    - (dup: release-6.0.0-dmr.md > Bug 修复> TiDB)- 修复 date_format 对 `'\n'` 的处理与 MySQL 不兼容的问题 [#32232](https://github.com/pingcap/tidb/issues/32232)
    - (dup: release-6.0.0-dmr.md > Bug 修复> TiDB)- 修复当恢复完成后，Region 有可能分布不均的问题 [#31034](https://github.com/pingcap/tidb/issues/31034)
    - (dup: release-5.3.1.md > Bug 修复> TiDB)- 修复开启 `tidb_restricted_read_only` 后 `tidb_super_read_only` 没有自动开启的问题 [#31745](https://github.com/pingcap/tidb/issues/31745)
    - (dup: release-6.0.0-dmr.md > Bug 修复> TiDB)- 修复带有 collation 的 `greatest` 或 `least` 函数结果出错的问题 [#31789](https://github.com/pingcap/tidb/issues/31789)
    - (dup: release-6.0.0-dmr.md > Bug 修复> TiDB)- 修复 LOAD DATA 语句处理转义字符时可能 panic 的问题 [#31589](https://github.com/pingcap/tidb/issues/31589)
    - (dup: release-6.0.0-dmr.md > Bug 修复> TiDB)- 修复查询时用到 index lookup join 导致 `invalid transaction` 报错的问题 [#30468](https://github.com/pingcap/tidb/issues/30468)
    - (dup: release-5.2.4.md > Bug 修复> TiDB)- 修复使用 left join 同时删除多张表数据时可能出现错误结果的问题 [#31321](https://github.com/pingcap/tidb/issues/31321)
    - (dup: release-5.2.4.md > Bug 修复> TiDB)- 修复 TiDB 可能向 TiFlash 发送重复任务的问题 [#32814](https://github.com/pingcap/tidb/issues/32814)
    - 修复了集群从 4.0 版本升级后，为用户授予 `all` 权限时报错的问题 [#33588](https://github.com/pingcap/tidb/issues/33588)
    - 修复了在 MySQL binary 协议下，当 schema 变更后，执行 prepared statement 会导致会话崩溃的问题 [#33509](https://github.com/pingcap/tidb/issues/33509)
    - 修复了一处 `compress()` 表达式在 `tidb_enable_vectorized_expression` 开启时，执行会报错的问题 [#33397](https://github.com/pingcap/tidb/issues/33397)
    - 修复了 `reArrangeFallback()` 函数使用 CPU 资源过多的问题 [#30353](https://github.com/pingcap/tidb/issues/30353)
    - 修复对于新加入的分区，表属性 (table attributes) 无法被检索到，以及分区更新后，表的 range 信息不会被更新的问题 [#33929](https://github.com/pingcap/tidb/issues/33929)
    - 修复了表的 `TopN` 统计信息在初始化时未正确排序的问题 [#34216](https://github.com/pingcap/tidb/issues/34216)
    - 修复了读取 `INFORMATION_SCHEMA.ATTRIBUTES` 表报错的问题，对于无法识别的 attributes 会做跳过处理 [#33665](https://github.com/pingcap/tidb/issues/33665)
    - 修复了当查询要求结果有序的情况下，即使设置了 `@@tidb_enable_parallel_apply`，`Apply` 算子依然不使用并行模式执行的问题 [#34237](https://github.com/pingcap/tidb/issues/34237)
    - 修复了在 sql_mode 为 `NO_ZERO_DATE` 的限制下，用户依然可以插入数据 `'0000-00-00 00:00:00'` 到 `datetime` 列的问题 [#34099](https://github.com/pingcap/tidb/issues/34099)
    - 修复了查询 `INFORMATION_SCHEMA.CLUSTER_SLOW_QUERY` 表导致 TiDB 服务器 OOM 的问题，在 Grafana dashboard 中查看慢查询记录的时候可能会触发该问题 [#33893](https://github.com/pingcap/tidb/issues/33893)
    - 修复了在 `NOWAIT` 语句中，事务执行遇到了锁后，并不会立刻返回的问题 [#32754](https://github.com/pingcap/tidb/issues/32754)

+ TiKV

    - (dup: release-5.2.4.md > Bug 修复> TiKV)- 修复待 merge 的 Region 无效会导致 TiKV panic 且非预期地销毁 peer 的问题 [#12232](https://github.com/tikv/tikv/issues/12232)
    - (dup: release-5.2.4.md > Bug 修复> TiKV)- 修复旧信息造成 TiKV panic 的问题 [#12023](https://github.com/tikv/tikv/issues/12023)
    - (dup: release-5.2.4.md > Bug 修复> TiKV)- 修复因内存统计指标溢出而造成的间歇性丢包和内存不足 (OOM) 的问题 [#12160](https://github.com/tikv/tikv/issues/12160)
    - (dup: release-5.2.4.md > Bug 修复> TiKV)- 修复在 Ubuntu 18.04 下进行性能分析会造成 TiKV panic 的问题 [#9765](https://github.com/tikv/tikv/issues/9765)
    - (dup: release-5.2.4.md > Bug 修复> TiKV)- 修复 replica read 可能违反线性一致性的问题 [#12109](https://github.com/tikv/tikv/issues/12109)
    - (dup: release-5.2.4.md > Bug 修复> TiKV)- 修复合并 Region 时因 target peer 被一个未进行初始化就被销毁的 peer 所替换，从而引起 TiKV panic 的问题 [#12048](https://github.com/tikv/tikv/issues/12048)
    - (dup: release-5.2.4.md > Bug 修复> TiKV)- 修复 TiKV 运行 2 年以上可能 panic 的问题 [#11940](https://github.com/tikv/tikv/issues/11940)
    - (dup: release-5.2.4.md > 提升改进> TiKV)- 通过减少需要进行清理锁 (Resolve Locks) 步骤的 Region 数量来减少 TiCDC 恢复时间 [#11993](https://github.com/tikv/tikv/issues/11993)
    - (dup: release-5.2.4.md > Bug 修复> TiKV)- 修复 Peer 状态为 Applying 时快照文件被删除会造成 panic 的问题 [#11746](https://github.com/tikv/tikv/issues/11746)
    - (dup: release-5.2.4.md > Bug 修复> TiKV)- 修复删除 Peer 可能造成高延迟的问题 [#10210](https://github.com/tikv/tikv/issues/10210)
    - 修复资源管理不正确断言导致 panic 的问题[#12234](https://github.com/tikv/tikv/issues/12234)
    - 修复部分情况下 slow score 计算不准确的问题 [#12254](https://github.com/tikv/tikv/issues/12254)
    - 修复 resolved_ts 模块内存管理不合理导致的 OOM 问题，增加更多监控指标 [#12159](https://github.com/tikv/tikv/issues/12159)
    - 修复网络出现问题情况下，已成功提交的乐观事务可能报 WriteConflict 错误的问题 [#34066](https://github.com/pingcap/tidb/issues/34066)
    - 修复 replica read 启用时，在网络出现问题情况下可能出现 TiKV panic 的问题 [#12046](https://github.com/tikv/tikv/issues/12046)

+ PD

    - (dup: release-6.0.0-dmr.md > Bug 修复> PD)- 修复不能动态设置 `dr-autosync` 的 `Duration` 字段的问题 [#4651](https://github.com/tikv/pd/issues/4651)
    - 修复存在大 store（例如 2T）时，无法检测到空间满的小 store，从而无法生成调度的问题 [#4805](https://github.com/tikv/pd/issues/4805)
    - 修复监控信息未重置上报导致的监控中残留已删除的 label 的问题 [#4825](https://github.com/tikv/pd/issues/4825)

+ TiFlash

    - (dup: release-5.2.4.md > Bug 修复> TiFlash)- 修复启用 TLS 时可能导致的崩溃 [#4196](https://github.com/pingcap/tiflash/issues/4196)
    - (dup: release-5.2.4.md > Bug 修复> TiFlash)- 修复在滞后的 Region peer 上执行 Region Merge 导致的元数据损坏问题 [#4437](https://github.com/pingcap/tiflash/issues/4437)
    - (dup: release-5.2.4.md > Bug 修复> TiFlash)- 修复在执行带有 `JOIN` 的查询遇到错误时可能被挂起的问题 [#4195](https://github.com/pingcap/tiflash/issues/4195)
    - (dup: release-5.2.4.md > Bug 修复> TiFlash)- 修复启用内存限制后 TiFlash 崩溃的问题 [#3902](https://github.com/pingcap/tiflash/issues/3902)
    - (dup: release-5.2.4.md > Bug 修复> TiFlash)- 修复 MPP 任务可能永远泄漏线程的问题 [#4238](https://github.com/pingcap/tiflash/issues/4238)
    - (dup: release-5.2.4.md > Bug 修复> TiFlash)- 修复将 `FLOAT` 类型转换为 `DECIMAL` 类型可能造成溢出的问题 [#3998](https://github.com/pingcap/tiflash/issues/3998)
    - (dup: release-6.0.0-dmr.md > Bug 修复> TiFlash)- 修复过期数据回收缓慢的问题 [#4146](https://github.com/pingcap/tiflash/issues/4146)
    - (dup: release-6.0.0-dmr.md > Bug 修复> TiFlash)- 修复启用本地隧道时取消 MPP 查询可能导致任务永远挂起的问题 [#4229](https://github.com/pingcap/tiflash/issues/4229)
    - (dup: release-6.0.0-dmr.md > Bug 修复> TiFlash)- 修复查询被取消时出现的内存泄露问题 [#4098](https://github.com/pingcap/tiflash/issues/4098)
    - (dup: release-6.0.0-dmr.md > Bug 修复> TiFlash)- 修复查询被取消时出现的内存泄露问题 [#4098](https://github.com/pingcap/tiflash/issues/4098)
    - (dup: release-5.2.4.md > Bug 修复> TiFlash)- 修复将 `DATETIME` 转换为 `DECIMAL` 时结果错误的问题 [#4151](https://github.com/pingcap/tiflash/issues/4151)
    - (dup: release-6.0.0-dmr.md > Bug 修复> TiFlash)- 修复并发执行多个 DDL 操作和 Apply Snapshot 操作时 TiFlash 可能会崩溃问题 [#4072](https://github.com/pingcap/tiflash/issues/4072)
    - (dup: release-5.2.4.md > Bug 修复> TiFlash)- 修复错误地配置存储目录会导致非预期行为的问题 [#4093](https://github.com/pingcap/tiflash/issues/4093)
    - (dup: release-5.2.4.md > Bug 修复> TiFlash)- 修复一些异常没有被正确地处理的问题 [#4101](https://github.com/pingcap/tiflash/issues/4101)
    - (dup: release-5.2.4.md > Bug 修复> TiFlash)- 修复将 `INT` 类型转换为 `DECIMAL` 类型可能造成溢出的问题 [#3920](https://github.com/pingcap/tiflash/issues/3920)
    - (dup: release-5.2.4.md > Bug 修复> TiFlash)- 修复 `IN` 函数的结果在多值表达式中不正确的问题 [#4016](https://github.com/pingcap/tiflash/issues/4016)
    - (dup: release-5.2.4.md > Bug 修复> TiFlash)- 修复日期格式将 `'\n'` 处理为非法分隔符的问题 [#4036](https://github.com/pingcap/tiflash/issues/4036)
    - (dup: release-5.2.4.md > Bug 修复> TiFlash)- 修复在读取工作量大时添加列后可能出现的查询错误 [#3967](https://github.com/pingcap/tiflash/issues/3967)
    - (dup: release-5.2.4.md > Bug 修复> TiFlash)- 修复启用内存限制后 TiFlash 崩溃的问题 [#3902](https://github.com/pingcap/tiflash/issues/3902)
    - 修复 DTFile 中可能的数据损坏问题 [#4778](https://github.com/pingcap/tiflash/issues/4778)
    - 修复对有很多 delete 操作的表进行时报错的潜在问题 [#4747](https://github.com/pingcap/tiflash/issues/4747)
    - 修复 TiFlash 随机报错 keepalive timeout 的问题 [#4192](https://github.com/pingcap/tiflash/issues/4192)
    - 修复 TiFlash 节点错误地遗留非法数据的问题 [#4414](https://github.com/pingcap/tiflash/issues/4414)
    - 修复空 segments 在 GC 后无法合并的问题 [#4511](https://github.com/pingcap/tiflash/issues/4511)

+ Tools

    + Backup & Restore (BR)
        - (dup: release-5.2.4.md > Bug 修复> Tools> Backup & Restore (BR))- 修复 BR 无法备份 RawKV 的问题 [#32607](https://github.com/pingcap/tidb/issues/32607)
        - 修复增量恢复期间某些情况下遇到的重复主键的问题. [#33596](https://github.com/pingcap/tidb/issues/33596)
        - 增量恢复期间，过滤某些不兼容的 DDL.[#33322](https://github.com/pingcap/tidb/issues/33322)
        - 修复某些情况下，恢复后 region 分布不均的问题.[#31034](https://github.com/pingcap/tidb/issues/31034)
        - 增加足够的重试，确保 region 一致性检查可以通过.[#33419](https://github.com/pingcap/tidb/issues/33419)
        - 修复在某些情况下，恢复过程中开启 merge 小文件功能导致的 panic 的问题.[#33801](https://github.com/pingcap/tidb/issues/33801)
        - 修复了在异常退出的时候，scheduler 没有重置的问题 [#33546](https://github.com/pingcap/tidb/issues/33546)

    + TiCDC

        - (dup: release-5.2.4.md > Bug 修复> Tools> TiCDC)- 修复切换 owner 会导致其 metrics 数据不正确的问题 [#4774](https://github.com/pingcap/tiflow/issues/4774)
        - (dup: release-5.2.4.md > Bug 修复> Tools> TiCDC)- 修复切换 owner 会导致其 metrics 数据不正确的问题 [#4774](https://github.com/pingcap/tiflow/issues/4774)
        - (dup: release-6.0.0-dmr.md > Bug 修复> Tools> TiCDC)- 修复 `Canal-JSON` 不支持 nil 可能导致的 TiCDC panic 问题 [#4736](https://github.com/pingcap/tiflow/issues/4736)
        - (dup: release-5.2.4.md > Bug 修复> Tools> TiCDC)- 修复 Unified Sorter 的 workerpool 稳定性问题 [#4447](https://github.com/pingcap/tiflow/issues/4447)
        - (dup: release-5.2.4.md > Bug 修复> Tools> TiCDC)- 修复某些情况下序列对象被错误同步的问题 [#4552](https://github.com/pingcap/tiflow/issues/4552)
        - (dup: release-6.0.0-dmr.md > Bug 修复> Tools> TiCDC)- 修复 `Canal-JSON` 错误处理 `string` 格式可能导致的 TiCDC panic 问题 [#4635](https://github.com/pingcap/tiflow/issues/4635)
        - (dup: release-5.2.4.md > Bug 修复> Tools> TiCDC)- 修复了 TiCDC 进程在 PD leader 被杀死时的异常退出问题 [#4248](https://github.com/pingcap/tiflow/issues/4248)
        - (dup: release-5.2.4.md > Bug 修复> Tools> TiCDC)- 修复 MySQL sink 在禁用 `batch-replace-enable` 参数时生成重复 `replace` SQL 语句的错误 [#4501](https://github.com/pingcap/tiflow/issues/4501)
        - 修复`rename tables` DDL 导致的生成 DML 错误的问题. [#5059](https://github.com/pingcap/tiflow/issues/5059)
        - 修复了在某些极端情况下，开启 new scheduler 时更新 owner 导致同步卡住的问题 (disabled by default). [#4963](https://github.com/pingcap/tiflow/issues/4963)
        - 修复了在开启 new scheduler 时 ErrProcessorDuplicateOperations 报错问题 (disabled by default) [#4769](https://github.com/pingcap/tiflow/issues/4769)
        -修复了在开启 TLS 后，第一个 PD 无法连接导致的 CDC 无法启动的问题。[#4777](https://github.com/pingcap/tiflow/issues/4777)
        - 修复了在表被调度时 checkpoint 监控不对的问题. [#4714](https://github.com/pingcap/tiflow/issues/4714)

    + TiDB Lightning

        - (dup: release-5.2.4.md > Bug 修复> Tools> TiDB Lightning)- 修复了 checksum 报错 “GC life time is shorter than transaction duration” [#32733](https://github.com/pingcap/tidb/issues/32733)
        - (dup: release-6.0.0-dmr.md > Bug 修复> Tools> TiDB Lightning)- 修复了检查空表失败导致 TiDB Lightning 卡住的问题 [#31797](https://github.com/pingcap/tidb/issues/31797)
        - (dup: release-5.2.4.md > Bug 修复> Tools> TiDB Lightning)- 修复在某些导入操作没有包含源文件时，TiDB Lightning 不会删除 metadata schema 的问题 [#28144](https://github.com/pingcap/tidb/issues/28144)
        - 修复前置检查中没有检查本地磁盘空间以及集群是否可用的问题.[#34213](https://github.com/pingcap/tidb/issues/34213)

    + TiDB Data Migration (DM)

        - (dup: release-6.0.0-dmr.md > Bug 修复> Tools> TiDB Data Migration (DM))- 修复了日志中出现数百条 "checkpoint has no change, skip sync flush checkpoint" 以及迁移性能下降的问题 [#4619](https://github.com/pingcap/tiflow/issues/4619)
        - (dup: release-6.0.0-dmr.md > Bug 修复> Tools> TiDB Data Migration (DM))- 修复了 varchar 类型值长度过长时的 `Column length too big` 错误 [#4637](https://github.com/pingcap/tiflow/issues/4637)
        - (dup: release-6.0.0-dmr.md > Bug 修复> Tools> TiDB Data Migration (DM))- 修复了 UPDATE 语句在安全模式下执行错误会导致 DM 进程挂掉的问题 [#4317](https://github.com/pingcap/tiflow/issues/4317)
        - 修复了某些情况下，过滤 DDL 并在下游手动执行会导致同步任务不能自动重试恢复 [#5272](https://github.com/pingcap/tiflow/issues/5272)
        - 修复了在上游没有开启 binlog，query-status 返回空的问题 [#5121](https://github.com/pingcap/tiflow/issues/5121)
        - 修复了当下游主键表同步落后时导致的 tracker panic 的问题 [#5159](https://github.com/pingcap/tiflow/issues/5159)
        - 修复了 GTID 同步开始后以及任务自动恢复时，可能出现一段时间 CPU 占用高并打印大量日志的问题 [#5063](https://github.com/pingcap/tiflow/issues/5063)