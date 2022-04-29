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

    (dup: release-6.0.0-dmr.md > 提升改进> TiDB)- 支持读取 `_tidb_rowid` 列的查询能够使用 PointGet 计划 [#31543](https://github.com/pingcap/tidb/issues/31543)

+ TiKV

    - note 1

+ PD

    - note 1

+ TiDB Dashboard

    - note 1

+ TiFlash

    - note 1

+ Tools

    + Backup & Restore (BR)

        - note 1

    + TiCDC

        (dup: release-5.2.4.md > 提升改进> Tools> TiCDC)- 在 Grafana 监控面板中支持多个 Kubernetes 集群 [#4665](https://github.com/pingcap/tiflow/issues/4665)
        (dup: release-5.2.4.md > 提升改进> Tools> TiCDC)- 暴露 Kafka producer 配置参数，使之在 TiCDC 中可配置 [#4385](https://github.com/pingcap/tiflow/issues/4385)

    + Dumpling

        - note 1

    + TiDB Lightning

        - note 1

    + TiDB Data Migration (DM)

        (dup: release-6.0.0-dmr.md > 提升改进> Tools> TiDB Data Migration (DM))- 支持 Syncer 使用 DM-worker 的工作目录写内部文件，不再使用 /tmp 目录。任务停止后会清理掉该目录 [#4107](https://github.com/pingcap/tiflow/issues/4107)

## Bug 修复

+ TiDB

    (dup: release-6.0.0-dmr.md > Bug 修复> TiDB)- 修复查询报错时可能阻塞 CTE 的问题 [#31302](https://github.com/pingcap/tidb/issues/31302)
    (dup: release-5.2.4.md > Bug 修复> TiDB)- 修复 Nulleq 函数作用在 Enum 类型上可能出现结果错误的问题 [#32428](https://github.com/pingcap/tidb/issues/32428)
    (dup: release-6.0.0-dmr.md > Bug 修复> TiDB)- 修复使用 ChunkRPC 导出数据时可能造成 TiDB OOM 的问题 [#31981](https://github.com/pingcap/tidb/issues/31981) [#30880](https://github.com/pingcap/tidb/issues/30880)
    (dup: release-6.0.0-dmr.md > Bug 修复> TiDB)- 修复 date_format 对 `'
'` 的处理与 MySQL 不兼容的问题 [#32232](https://github.com/pingcap/tidb/issues/32232)
    (dup: release-6.0.0-dmr.md > Bug 修复> TiDB)- 修复当恢复完成后，Region 有可能分布不均的问题 [#31034](https://github.com/pingcap/tidb/issues/31034)
    (dup: release-5.3.1.md > Bug 修复> TiDB)- 修复开启 `tidb_restricted_read_only` 后 `tidb_super_read_only` 没有自动开启的问题 [#31745](https://github.com/pingcap/tidb/issues/31745)
    (dup: release-6.0.0-dmr.md > Bug 修复> TiDB)- 修复带有 collation 的 `greatest` 或 `least` 函数结果出错的问题 [#31789](https://github.com/pingcap/tidb/issues/31789)
    (dup: release-6.0.0-dmr.md > Bug 修复> TiDB)- 修复 LOAD DATA 语句处理转义字符时可能 panic 的问题 [#31589](https://github.com/pingcap/tidb/issues/31589)
    (dup: release-6.0.0-dmr.md > Bug 修复> TiDB)- 修复查询时用到 index lookup join 导致 `invalid transaction` 报错的问题 [#30468](https://github.com/pingcap/tidb/issues/30468)
    (dup: release-5.2.4.md > Bug 修复> TiDB)- 修复使用 left join 同时删除多张表数据时可能出现错误结果的问题 [#31321](https://github.com/pingcap/tidb/issues/31321)
    (dup: release-5.2.4.md > Bug 修复> TiDB)- 修复 TiDB 可能向 TiFlash 发送重复任务的问题 [#32814](https://github.com/pingcap/tidb/issues/32814)
    - Fix a bug of duplicate primary key when insert record into table after incremental restoration. [#33596](https://github.com/pingcap/tidb/issues/33596)
    - Fix the issue that the schedulers won't be resumed after BR/Lightning exits abnormally. [#33546](https://github.com/pingcap/tidb/issues/33546)
    - Fix the issue that privilege-related operations may fail for upgraded clusters. [#33588](https://github.com/pingcap/tidb/issues/33588)
    - fix bug #33509 [#33509](https://github.com/pingcap/tidb/issues/33509)
    - fix a bug that compress function may report error [#33397](https://github.com/pingcap/tidb/issues/33397)
    - Fix the issue that NewCollationEnable config not checked during restoration. [#33422](https://github.com/pingcap/tidb/issues/33422)
    - Fix a bug that BR incremental restore return error by mistake caused by ddl job with empty query. [#33322](https://github.com/pingcap/tidb/issues/33322)
    - Fix the issue that BR not retry enough when region not consistency during restoration. [#33419](https://github.com/pingcap/tidb/issues/33419)
    - Fix the problem of high use of reArrangeFallback cpu. [#30353](https://github.com/pingcap/tidb/issues/30353)
    - Fix the issue that the table attributes don't support index and won't be updated when the partition changes [#33929](https://github.com/pingcap/tidb/issues/33929)

+ TiKV

    (dup: release-5.2.4.md > Bug 修复> TiKV)- 修复待 merge 的 Region 无效会导致 TiKV panic 且非预期地销毁 peer 的问题 [#12232](https://github.com/tikv/tikv/issues/12232)
    (dup: release-5.2.4.md > Bug 修复> TiKV)- 修复旧信息造成 TiKV panic 的问题 [#12023](https://github.com/tikv/tikv/issues/12023)
    (dup: release-5.2.4.md > Bug 修复> TiKV)- 修复因内存统计指标溢出而造成的间歇性丢包和内存不足 (OOM) 的问题 [#12160](https://github.com/tikv/tikv/issues/12160)
    (dup: release-5.2.4.md > Bug 修复> TiKV)- 修复在 Ubuntu 18.04 下进行性能分析会造成 TiKV panic的问题 [#9765](https://github.com/tikv/tikv/issues/9765)
    (dup: release-6.0.0-dmr.md > 提升改进> TiKV)- 使 Grafana 支持 multi-k8s 的监控 [#12104](https://github.com/tikv/tikv/issues/12104)
    (dup: release-5.2.4.md > Bug 修复> TiKV)- 修复 Replica Read 可能违反线性一致性的问题 [#12109](https://github.com/tikv/tikv/issues/12109)
    (dup: release-5.2.4.md > Bug 修复> TiKV)- 修复合并 Region 时因 target peer 被一个未进行初始化就被销毁的 peer 所替换，从而引起 TiKV panic 的问题 [#12048](https://github.com/tikv/tikv/issues/12048)
    (dup: release-5.2.4.md > Bug 修复> TiKV)- 修复 TiKV 运行 2 年以上可能 panic 的问题 [#11940](https://github.com/tikv/tikv/issues/11940)
    (dup: release-5.2.4.md > 提升改进> TiKV)- 通过减少需要进行清理锁 (Resolve Locks) 步骤的 Region 数量来减少 TiCDC 恢复时间 [#11993](https://github.com/tikv/tikv/issues/11993)
    (dup: release-5.2.4.md > Bug 修复> TiKV)- 修复 Peer 状态为 Applying 时快照文件被删除会造成 panic 的问题 [#11746](https://github.com/tikv/tikv/issues/11746)
    (dup: release-5.2.4.md > Bug 修复> TiKV)- 修复删除 Peer 可能造成高延迟的问题 [#10210](https://github.com/tikv/tikv/issues/10210)

+ PD

    (dup: release-6.0.0-dmr.md > Bug 修复> PD)- 修复不能动态设置 `dr-autosync` 的 `Duration` 字段的问题 [#4651](https://github.com/tikv/pd/issues/4651)

+ TiFlash

    (dup: release-5.2.4.md > Bug 修复> TiFlash)- 修复启用 TLS 时可能导致的崩溃 [#4196](https://github.com/pingcap/tiflash/issues/4196)
    (dup: release-5.2.4.md > Bug 修复> TiFlash)- 修复在滞后的 Region peer 上执行 Region Merge 导致的元数据损坏问题 [#4437](https://github.com/pingcap/tiflash/issues/4437)
    (dup: release-5.2.4.md > Bug 修复> TiFlash)- 修复在执行带有 `JOIN` 的查询遇到错误时可能被挂起的问题 [#4195](https://github.com/pingcap/tiflash/issues/4195)
    (dup: release-5.2.4.md > Bug 修复> TiFlash)- 修复启用内存限制后 TiFlash 崩溃的问题 [#3902](https://github.com/pingcap/tiflash/issues/3902)
    (dup: release-5.2.4.md > Bug 修复> TiFlash)- 修复 MPP 任务可能永远泄漏线程的问题 [#4238](https://github.com/pingcap/tiflash/issues/4238)
    (dup: release-5.2.4.md > Bug 修复> TiFlash)- 修复将 `FLOAT` 类型转换为 `DECIMAL` 类型可能造成溢出的问题 [#3998](https://github.com/pingcap/tiflash/issues/3998)
    (dup: release-6.0.0-dmr.md > Bug 修复> TiFlash)- 修复过期数据回收缓慢的问题 [#4146](https://github.com/pingcap/tiflash/issues/4146)
    (dup: release-6.0.0-dmr.md > Bug 修复> TiFlash)- 修复启用本地隧道时取消 MPP 查询可能导致任务永远挂起的问题 [#4229](https://github.com/pingcap/tiflash/issues/4229)
    (dup: release-6.0.0-dmr.md > Bug 修复> TiFlash)- 修复查询被取消时出现的内存泄露问题 [#4098](https://github.com/pingcap/tiflash/issues/4098)
    (dup: release-6.0.0-dmr.md > Bug 修复> TiFlash)- 修复查询被取消时出现的内存泄露问题 [#4098](https://github.com/pingcap/tiflash/issues/4098)
    (dup: release-5.2.4.md > Bug 修复> TiFlash)- 修复将 `DATETIME` 转换为 `DECIMAL` 时结果错误的问题 [#4151](https://github.com/pingcap/tiflash/issues/4151)
    (dup: release-6.0.0-dmr.md > Bug 修复> TiFlash)- 修复并发执行多个 DDL 操作和 Apply Snapshot 操作时 TiFlash 可能会崩溃问题 [#4072](https://github.com/pingcap/tiflash/issues/4072)
    (dup: release-5.2.4.md > Bug 修复> TiFlash)- 修复错误地配置存储目录会导致非预期行为的问题 [#4093](https://github.com/pingcap/tiflash/issues/4093)
    (dup: release-5.2.4.md > Bug 修复> TiFlash)- 修复一些异常没有被正确地处理的问题 [#4101](https://github.com/pingcap/tiflash/issues/4101)
    (dup: release-5.2.4.md > Bug 修复> TiFlash)- 修复将 `INT` 类型转换为 `DECIMAL` 类型可能造成溢出的问题 [#3920](https://github.com/pingcap/tiflash/issues/3920)
    (dup: release-5.2.4.md > Bug 修复> TiFlash)- 修复 `IN` 函数的结果在多值表达式中不正确的问题 [#4016](https://github.com/pingcap/tiflash/issues/4016)
    - Fix the issue that the date format identifies `'
'` as an invalid separator [#4036](https://github.com/pingcap/tiflash/issues/4036)
    (dup: release-5.2.4.md > Bug 修复> TiFlash)- 修复在读取工作量大时添加列后可能出现的查询错误 [#3967](https://github.com/pingcap/tiflash/issues/3967)
    (dup: release-5.2.4.md > Bug 修复> TiFlash)- 修复启用内存限制后 TiFlash 崩溃的问题 [#3902](https://github.com/pingcap/tiflash/issues/3902)

+ Tools

    + Backup & Restore (BR)
        (dup: release-5.2.4.md > Bug 修复> Tools> Backup & Restore (BR))- 修复 BR 无法备份 RawKV 的问题 [#32607](https://github.com/pingcap/tidb/issues/32607)

    + TiCDC

        (dup: release-5.2.4.md > Bug 修复> Tools> TiCDC)- 修复切换 owner 会导致其 metrics 数据不正确的问题 [#4774](https://github.com/pingcap/tiflow/issues/4774)
        (dup: release-5.2.4.md > Bug 修复> Tools> TiCDC)- 修复切换 owner 会导致其 metrics 数据不正确的问题 [#4774](https://github.com/pingcap/tiflow/issues/4774)
        (dup: release-6.0.0-dmr.md > Bug 修复> Tools> TiCDC)- 修复 `Canal-JSON` 不支持 nil 可能导致的 TiCDC panic 问题 [#4736](https://github.com/pingcap/tiflow/issues/4736)
        (dup: release-5.2.4.md > Bug 修复> Tools> TiCDC)- 修复 Unified Sorter 的 workerpool 稳定性问题 [#4447](https://github.com/pingcap/tiflow/issues/4447)
        (dup: release-5.2.4.md > Bug 修复> Tools> TiCDC)- 修复某些情况下序列对象被错误同步的问题 [#4552](https://github.com/pingcap/tiflow/issues/4552)
        (dup: release-6.0.0-dmr.md > Bug 修复> Tools> TiCDC)- 修复 `Canal-JSON` 错误处理 `string` 格式可能导致的 TiCDC panic 问题 [#4635](https://github.com/pingcap/tiflow/issues/4635)
        (dup: release-5.2.4.md > Bug 修复> Tools> TiCDC)- 修复了 TiCDC 进程在 PD leader 被杀死时的异常退出问题 [#4248](https://github.com/pingcap/tiflow/issues/4248)
        (dup: release-5.2.4.md > Bug 修复> Tools> TiCDC)- 修复 MySQL sink 在禁用 `batch-replace-enable` 参数时生成重复 `replace` SQL 语句的错误 [#4501](https://github.com/pingcap/tiflow/issues/4501)

    + TiDB Lightning

        (dup: release-5.2.4.md > Bug 修复> Tools> TiDB Lightning)- 修复了 checksum 报错 “GC life time is shorter than transaction duration” [#32733](https://github.com/pingcap/tidb/issues/32733)
        (dup: release-6.0.0-dmr.md > Bug 修复> Tools> TiDB Lightning)- 修复了检查空表失败导致 TiDB Lightning 卡住的问题 [#31797](https://github.com/pingcap/tidb/issues/31797)
        (dup: release-5.2.4.md > Bug 修复> Tools> TiDB Lightning)- 修复在某些导入操作没有包含源文件时，TiDB Lightning 不会删除 metadata schema 的问题 [#28144](https://github.com/pingcap/tidb/issues/28144)

    + Dumpling

        - note 1

    + TiDB Data Migration (DM)

        (dup: release-6.0.0-dmr.md > Bug 修复> Tools> TiDB Data Migration (DM))- 修复了日志中出现数百条 "checkpoint has no change, skip sync flush checkpoint" 以及迁移性能下降的问题 [#4619](https://github.com/pingcap/tiflow/issues/4619)
        (dup: release-6.0.0-dmr.md > Bug 修复> Tools> TiDB Data Migration (DM))- 修复了 varchar 类型值长度过长时的 `Column length too big` 错误 [#4637](https://github.com/pingcap/tiflow/issues/4637)
        (dup: release-6.0.0-dmr.md > Bug 修复> Tools> TiDB Data Migration (DM))- 修复了 UPDATE 语句在安全模式下执行错误会导致 DM 进程挂掉的问题 [#4317](https://github.com/pingcap/tiflow/issues/4317)

## __unsorted

+ PingCAP/TiDB

    - release-note [#33887](https://github.com/pingcap/tidb/issues/33887)
    - release-note [#27937](https://github.com/pingcap/tidb/issues/27937)
    - release-note [#34216](https://github.com/pingcap/tidb/issues/34216)
    - release-note [#34256](https://github.com/pingcap/tidb/issues/34256)
    - release-note [#33665](https://github.com/pingcap/tidb/issues/33665)
    - release-note [#34237](https://github.com/pingcap/tidb/issues/34237)
    - lightning: split and scatter regions in batches [#33618](https://github.com/pingcap/tidb/issues/33618)
    - release-note [#32459](https://github.com/pingcap/tidb/issues/32459)
    - release-note [#34099](https://github.com/pingcap/tidb/issues/34099)
    - release-note [#34213](https://github.com/pingcap/tidb/issues/34213)
    - release-note [#34180](https://github.com/pingcap/tidb/issues/34180)
    - release-note [#34139](https://github.com/pingcap/tidb/pull/34139)
    - release-note [#33801](https://github.com/pingcap/tidb/issues/33801)
    - release-note [#33893](https://github.com/pingcap/tidb/issues/33893)
    - Support multi k8s in grafana dashboards [#32593](https://github.com/pingcap/tidb/issues/32593)
    - Fix the bug that locking with NOWAIT does not return immediately when encountering a lock. [#32754](https://github.com/pingcap/tidb/issues/32754)

+ TiKV/TiKV

    - Fix that successfully committed optimistic transactions may report false WriteConflict on network errors. [#34066](https://github.com/pingcap/tidb/issues/34066)
    - Fix panicking when replica read is enabled and there is a long time network condition [#12046](https://github.com/tikv/tikv/issues/12046)

+ PingCAP/TiFlash

    - fix potential data corruption for large indices [#4778](https://github.com/pingcap/tiflash/issues/4778)
    - Fix potential query error when select on a table with many delete operations [#4747](https://github.com/pingcap/tiflash/issues/4747)
    - Fix bug that TiFlash query will meet keepalive timeout error randomly. [#4192](https://github.com/pingcap/tiflash/issues/4192)
    - Avoid leaving data on tiflash node which doesn't corresponding to any region range [#4414](https://github.com/pingcap/tiflash/issues/4414)
    - Fix the problem that empty segments cannot be merged after gc [#4511](https://github.com/pingcap/tiflash/issues/4511)
    - metrics: support multi-k8s in grafana dashboards [#4129](https://github.com/pingcap/tiflash/issues/4129)

+ PD

    - None. [#4805](https://github.com/tikv/pd/issues/4805)
    - Fix the issue that the label distribution has residual labels [#4825](https://github.com/tikv/pd/issues/4825)
    - metrics: support multi-k8s in grafana dashboards [#4673](https://github.com/tikv/pd/issues/4673)
    - None. [#4808](https://github.com/tikv/pd/issues/4808)

+ Tools

    + PingCAP/TiCDC

        - `None`. [#4784](https://github.com/pingcap/tiflow/issues/4784)
        - save table checkpoint after a DDL is filtered [#5272](https://github.com/pingcap/tiflow/issues/5272)
        - Fix a bug that no data is return by `query-status` when upstream doesn't turn on binlog [#5121](https://github.com/pingcap/tiflow/issues/5121)
        - `None`. [#5197](https://github.com/pingcap/tiflow/issues/5197)
        - Fix a bug that checkpoint flushing will be called too frequently [#5063](https://github.com/pingcap/tiflow/issues/5063)
        - fix tracker panic when pk of downstream table orders behind [#5159](https://github.com/pingcap/tiflow/issues/5159)
        - `None`. [#5136](https://github.com/pingcap/tiflow/issues/5136)
        - send one heartbeat for successive skipped GTID when enable relay log [#5063](https://github.com/pingcap/tiflow/issues/5063)
        - fix DML construct error issue caused by `rename tables` DDL. [#5059](https://github.com/pingcap/tiflow/issues/5059)
        - Fix a rare likelihood that replication be stuck if the owner is changed when the new scheduler is enabled (disabled by default). [#4963](https://github.com/pingcap/tiflow/issues/4963)
        - `None`. [#4858](https://github.com/pingcap/tiflow/issues/4858)
        - Fix ErrProcessorDuplicateOperations when new scheduler is enabled (disabled by default) [#4769](https://github.com/pingcap/tiflow/issues/4769)
        - fix the issue that ticdc failed to start when connects to  multiple pd endpoints with tls-enabled and the 1st endpoint is not available [#4777](https://github.com/pingcap/tiflow/issues/4777)
        - Fix checkpoint metrics when tables are being scheduled. [#4714](https://github.com/pingcap/tiflow/issues/4714)
        - `None`. [#4554](https://github.com/pingcap/tiflow/issues/4554)
        - Please add a release note. `None`. [#4565](https://github.com/pingcap/tiflow/issues/4565)
        - `None`. [#4607](https://github.com/pingcap/tiflow/issues/4607)
        - `None`. [#4588](https://github.com/pingcap/tiflow/issues/4588)
        - `None`. [#4561](https://github.com/pingcap/tiflow/issues/4561)
        - Please add a release note. If you don't think this PR needs a release note then fill it with `None`. [#4287](https://github.com/pingcap/tiflow/issues/4287)
        - `None`. [#4128](https://github.com/pingcap/tiflow/issues/4128)
        - None. [#4353](https://github.com/pingcap/tiflow/issues/4353)