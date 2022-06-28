---
title: TiDB 5.3.2 Release Notes
---

# TiDB 5.3.2 Release Notes

发版日期：2022 年 6 月 x 日

TiDB 版本：5.3.2

## 兼容性更改

+ TiDB

    (dup: release-5.2.4.md > Bug 修复> TiDB)- 修复当 auto ID 超出范围时，`REPLACE` 语句错误地修改了其它行的问题 [#29483](https://github.com/pingcap/tidb/issues/29483)

+ PD

     (dup: release-6.1.0.md > 改进提升> PD)- 默认关闭编译 swagger server [#4932](https://github.com/tikv/pd/issues/4932)

## 提升改进

+ TiKV

    (dup: release-5.4.0.md > Improvements> TiKV)- 减少 Raft 客户端的系统调用并提高 CPU 效率 [#11309](https://github.com/tikv/tikv/issues/11309)
    (dup: release-6.1.0.md > 改进提升> TiKV)- 健康检查可以检测到无法正常工作的 Raftstore，使得 TiKV client 可以及时更新 Region Cache [#12398](https://github.com/tikv/tikv/issues/12398)
    (dup: release-5.2.4.md > 提升改进> TiKV)- 通过将 leader 转让给 CDC observer 减少延迟抖动 [#12111](https://github.com/tikv/tikv/issues/12111)
    (dup: release-5.3.0.md > 提升改进> TiKV> 增强磁盘空间防护能力，提升存储稳定性。)- 降低写入延迟，从 Raftstore 线程池中分离出 IO 线程池（默认不开启）。具体调优操作，请参考 [TiKV 线程池性能调优](/tune-tikv-thread-performance.md) [#10540](https://github.com/tikv/tikv/issues/10540)
    (dup: release-5.0.6.md > 提升改进> TiKV)- 在 Raft 日志垃圾回收模块中添加了更多监控指标，从而定位该模块中出现的性能问题 [#11374](https://github.com/tikv/tikv/issues/11374)

+ PD

    (dup: release-6.1.0.md > Improvements> PD)- Disable compiling swagger server by default [#4932](https://github.com/tikv/pd/issues/4932)

+ Tools

    + TiDB Data Migration (DM)

        (dup: release-5.4.1.md > 提升改进> Tools> TiDB Data Migration (DM))- 支持 Syncer 使用 DM-worker 的工作目录写内部文件，不再使用 /tmp 目录。任务停止后会清理掉该目录 [#4107](https://github.com/pingcap/tiflow/issues/4107)

    + TiDB Lightning

        (dup: release-6.1.0.md > Improvements> Tools> TiDB Lightning)- 优化 Scatter Region 为批量模式，提升 Scatter Region 过程的稳定性 [#33618](https://github.com/pingcap/tidb/issues/33618)

## Bug 修复

+ TiDB

    (dup: release-6.0.0-dmr.md > Bug fixes> Tools> Dumpling)- 修复了 Amazon S3 无法正确计算压缩数据大小的问题 [#30534](https://github.com/pingcap/tidb/issues/30534)
    (dup: release-5.4.0.md > Bug 修复> TiDB)- 修复乐观事务下数据索引可能不一致的问题 [#30410](https://github.com/pingcap/tidb/issues/30410)
    (dup: release-5.2.4.md > Bug 修复> TiDB)- 修复当 SQL 语句中存在 JSON 类型列与 `CHAR` 类型列连接时，SQL 出错的问题 [#29401](https://github.com/pingcap/tidb/issues/29401)
    - 如果发生网络连接问题，TiDB 并不总是能正确释放已断开会话所占有的资源。该修复可以确保 TiDB 回滚打开的事务以及释放其他相关资源。[#34722](https://github.com/pingcap/tidb/issues/34722)
    - 修复开启 TiDB Binlog 后插入重复数据导致 `data and columnID count not match` 错误的问题 [#33608](https://github.com/pingcap/tidb/issues/33608)
    (dup: release-6.1.0.md > 错误修复> TiDB)- 修复在 RC 隔离情况下 Plan Cache 启用时可能导致查询结果错误的问题 [#34447](https://github.com/pingcap/tidb/issues/34447)
    (dup: release-5.4.1.md > Bug 修复> TiDB)- 修复了在 MySQL binary 协议下，当 schema 变更后，执行 prepared statement 会导致会话崩溃的问题 [#33509](https://github.com/pingcap/tidb/issues/33509)
    (dup: release-5.4.1.md > Bug 修复> TiDB)- 修复对于新加入的分区，表属性 (table attributes) 无法被检索到，以及分区更新后，表的 range 信息不会被更新的问题 [#33929](https://github.com/pingcap/tidb/issues/33929)
    (dup: release-5.4.1.md > Bug 修复> TiDB)- 修复了查询 `INFORMATION_SCHEMA.CLUSTER_SLOW_QUERY` 表导致 TiDB 服务器 OOM 的问题，在 Grafana dashboard 中查看慢查询记录的时候可能会触发该问题 [#33893](https://github.com/pingcap/tidb/issues/33893)
    (dup: release-6.1.0.md > 错误修复> TiDB)- 修复集群的 PD 节点被替换后一些 DDL 语句会卡住一段时间的问题 [#33908](https://github.com/pingcap/tidb/issues/33908)
    (dup: release-5.4.1.md > Bug 修复> TiDB)- 修复了集群从 4.0 版本升级后，为用户授予 `all` 权限时报错的问题 [#33588](https://github.com/pingcap/tidb/issues/33588)
    (dup: release-5.4.1.md > Bug 修复> TiDB)- 修复使用 left join 同时删除多张表数据时可能出现错误结果的问题 [#31321](https://github.com/pingcap/tidb/issues/31321)
    (dup: release-5.4.1.md > Bug 修复> TiDB)- 修复 TiDB 可能向 TiFlash 发送重复任务的问题 [#32814](https://github.com/pingcap/tidb/issues/32814)
    (dup: release-5.2.4.md > Bug 修复> TiDB)- 修复 TiDB 的后台 HTTP 服务可能没有正确关闭导致集群状态异常的问题 [#30571](https://github.com/pingcap/tidb/issues/30571)
    (dup: release-5.3.1.md > Bug 修复> TiDB)- 修复 TiDB 由于 `fatal error: concurrent map read and map write` 发生崩溃的问题 [#35340](https://github.com/pingcap/tidb/issues/35340)

+ TiKV

    - 修复了 PD 客户端遇到报错时频繁重连的问题 [#12345](https://github.com/tikv/tikv/issues/12345)
    - 修复了 `DATETIME` 类型的数据包含小数部分和 `Z` 后缀导致检查报错的问题 [#12739](https://github.com/tikv/tikv/issues/12739)
    - 修复了对空字符串进行类型转换导致 TiKV panic 的问题 [#12673](https://github.com/tikv/tikv/issues/12673)
    - 修复了在悲观事务中使用 Async Commit 导致重复提交记录的问题 [#12615](https://github.com/tikv/tikv/issues/12615)
    (dup: release-6.1.0.md > 错误修复> TiKV)- 修复进行 Follower Read 时，可能会报 `invalid store ID 0` 错误的问题 [#12478](https://github.com/tikv/tikv/issues/12478)
    (dup: release-6.1.0.md > 错误修复> TiKV)- 修复销毁 peer 和批量分裂 Region 之间的竞争导致的 TiKV panic [#12368](https://github.com/tikv/tikv/issues/12368)
    (dup: release-5.4.1.md > Bug 修复> TiKV)- 修复网络出现问题的情况下，已成功提交的乐观事务可能报 `Write Conflict` 错误的问题 [#34066](https://github.com/pingcap/tidb/issues/34066)
    (dup: release-5.4.1.md > Bug 修复> TiKV)- 修复待 merge 的 Region 无效会导致 TiKV panic 且非预期地销毁 peer 的问题 [#12232](https://github.com/tikv/tikv/issues/12232)
    (dup: release-5.4.1.md > Bug 修复> TiKV)- 修复旧信息造成 TiKV panic 的问题 [#12023](https://github.com/tikv/tikv/issues/12023)
    (dup: release-5.4.1.md > Bug 修复> TiKV)- 修复因内存统计指标溢出而造成的间歇性丢包和内存不足 (OOM) 的问题 [#12160](https://github.com/tikv/tikv/issues/12160)
    (dup: release-5.4.1.md > Bug 修复> TiKV)- 修复在 Ubuntu 18.04 下进行性能分析会造成 TiKV panic 的问题 [#9765](https://github.com/tikv/tikv/issues/9765)
    (dup: release-5.2.4.md > Bug 修复> TiKV)- 修复 tikv-ctl 对 `bad-ssts` 结果字符串进行错误匹配的问题 [#12329](https://github.com/tikv/tikv/issues/12329)
    (dup: release-5.4.1.md > Bug 修复> TiKV)- 修复 replica read 可能违反线性一致性的问题 [#12109](https://github.com/tikv/tikv/issues/12109)
    (dup: release-5.4.1.md > Bug 修复> TiKV)- 修复合并 Region 时因 target peer 被一个未进行初始化就被销毁的 peer 所替换，从而引起 TiKV panic 的问题 [#12048](https://github.com/tikv/tikv/issues/12048)
    (dup: release-5.4.1.md > Bug 修复> TiKV)- 修复 TiKV 运行 2 年以上可能 panic 的问题 [#11940](https://github.com/tikv/tikv/issues/11940)

+ PD
    - 修复由于 Hot Region 没有 leader 导致 PD Panic 的问题 [#5005](https://github.com/tikv/pd/issues/5005)
    (dup: release-6.1.0.md > 错误修复> PD)- 修复 PD leader 转移后调度不能立即启动的问题 [#4769](https://github.com/tikv/pd/issues/4769)
    (dup: release-6.1.0.md > Bug fixes> PD)- Fix the issue that a removed tombstone store appears again after the PD leader transfer ​​[#4941](https://github.com/tikv/pd/issues/4941)
    (dup: release-6.1.0.md > 错误修复> PD)- 修复在某些特殊情况下 TSO fallback 的问题 [#4884](https://github.com/tikv/pd/issues/4884)
    (dup: release-5.4.1.md > Bug 修复> PD)- 修复存在较大空间 Store 时（例如 2T），无法检测满的小空间 Store，从而无法进行平衡调度的问题 [#4805](https://github.com/tikv/pd/issues/4805)
    - 修复 `SchedulerMaxWaitingOperator ` 设置为 1 时，不产生调度的问题 [#4946](https://github.com/tikv/pd/issues/4946)
    (dup: release-5.4.1.md > Bug Fixes> PD)- Fix the issue that the label distribution has residual labels in the metrics [#4825](https://github.com/tikv/pd/issues/4825)

+ TiFlash

    (dup: release-5.4.1.md > Bug 修复> TiFlash)- 修复错误地配置存储目录会导致非预期行为的问题 [#4093](https://github.com/pingcap/tiflash/issues/4093)
    (dup: release-5.4.1.md > Bug 修复> TiFlash)- 修复 TiFlash 节点上遗留了与 Region range 不匹配的数据的问题 [#4414](https://github.com/pingcap/tiflash/issues/4414)
    - 修复在添加一些 `NOT NULL` 的列时报 `TiFlash_schema_error` 的问题 [#4596](https://github.com/pingcap/tiflash/issues/4596)
    - 修复由于 `commit state jump backward` 错误导致 TiFlash 反复崩溃的问题 [#2576](https://github.com/pingcap/tiflash/issues/2576)
    (dup: release-6.1.0.md > 错误修复> TiFlash)- 修复大量 INSERT 和 DELETE 操作后可能导致 TiFlash 数据不一致的问题 [#4956](https://github.com/pingcap/tiflash/issues/4956</span>)
    (dup: release-5.4.1.md > Bug 修复> TiFlash)- 修复启用本地隧道时取消 MPP 查询可能导致任务永远挂起的问题 [#4229](https://github.com/pingcap/tiflash/issues/4229)
    - 修复 TiFlash 使用远程读时可能会误报集群 TiFlash 版本不一致的问题 [#3713](https://github.com/pingcap/tiflash/issues/3713)
    - 修复 MPP query 会随机碰到 gRPC keepalive timeout 导致 query 失败的问题 [#4662](https://github.com/pingcap/tiflash/issues/4662)
    - 修复 MPP exchange receiver 如果出现大量重试可能会导致 query hang 的问题 [#3473](https://github.com/pingcap/tiflash/pull/3473)
    (dup: release-5.4.1.md > Bug 修复> TiFlash)- 修复将 `DATETIME` 转换为 `DECIMAL` 时结果错误的问题 [#4151](https://github.com/pingcap/tiflash/issues/4151)
    (dup: release-5.4.1.md > Bug 修复> TiFlash)- 修复将 `FLOAT` 类型转换为 `DECIMAL` 类型可能造成溢出的问题 [#3998](https://github.com/pingcap/tiflash/issues/3998)
    - 修复 `json_length` 对空字符串可能会报 `index out of bounds` 错误的问题 [#2705](https://github.com/pingcap/tiflash/issues/2705)
    - 修复极端情况下 decimal 比较可能会结果不对的问题 [#4942](https://github.com/pingcap/tiflash/pull/4942)
    (dup: release-5.4.1.md > Bug 修复> TiFlash)- 修复在执行带有 `JOIN` 的查询遇到错误时可能被挂起的问题 [#4195](https://github.com/pingcap/tiflash/issues/4195)
    (dup: release-5.2.4.md > Bug 修复> TiFlash)- 修复查询语句包含 `where <string>` 时查询结果出错的问题 [#3447](https://github.com/pingcap/tiflash/issues/3447)
    (dup: release-5.2.4.md > Bug 修复> TiFlash)- 修复 `CastStringAsReal` 在 TiFlash 的行为与在 TiDB、TiKV 的行为不一致的问题 [#3475](https://github.com/pingcap/tiflash/issues/3475)
    - 修复 cast string to datetime 时，`microsecond` 结果可能不对的问题 [#3556](https://github.com/pingcap/tiflash/issues/3556)
    (dup: release-5.4.1.md > Bug Fixes> TiFlash)- Fix potential errors when querying on a table with many delete operations [#4747](https://github.com/pingcap/tiflash/issues/4747)
    (dup: release-5.4.1.md > Bug Fixes> TiFlash)- Fix a bug that TiFlash reports many "Keepalive watchdog fired" errors randomly [#4192](https://github.com/pingcap/tiflash/issues/4192)
    (dup: release-5.4.1.md > Bug Fixes> TiFlash)- Fix a bug that data not matching any region range remains on a TiFlash node [#4414](https://github.com/pingcap/tiflash/issues/4414)
    (dup: release-5.4.1.md > Bug Fixes> TiFlash)- Fix a bug that MPP tasks might leak threads forever [#4238](https://github.com/pingcap/tiflash/issues/4238)
    (dup: release-5.4.1.md > Bug Fixes> TiFlash)- Fix a bug that empty segments cannot be merged after GC [#4511](https://github.com/pingcap/tiflash/issues/4511)
    (dup: release-5.4.1.md > Bug Fixes> TiFlash)- Fix the panic issue that occurs when TLS is enabled [#4196](https://github.com/pingcap/tiflash/issues/4196)
    (dup: release-5.4.1.md > Bug Fixes> TiFlash)- Fix the issue that expired data is recycled slowly [#4146](https://github.com/pingcap/tiflash/issues/4146)
    (dup: release-5.4.1.md > Bug Fixes> TiFlash)- Fix the bug that invalid storage directory configurations lead to unexpected behaviors [#4093](https://github.com/pingcap/tiflash/issues/4093)
    (dup: release-5.4.1.md > Bug Fixes> TiFlash)- Fix the bug that some exceptions are not handled properly [#4101](https://github.com/pingcap/tiflash/issues/4101)
    (dup: release-5.4.1.md > Bug Fixes> TiFlash)- Fix the potential query error after adding columns under heavy read workload [#3967](https://github.com/pingcap/tiflash/issues/3967)
    (dup: release-5.2.4.md > Bug fixes> TiFlash)- Fix the bug that the `STR_TO_DATE()` function incorrectly handles leading zeros when parsing microseconds [#3557](https://github.com/pingcap/tiflash/issues/3557)
    (dup: release-5.2.4.md > Bug fixes> TiFlash)- Fix the issue that TiFlash might return the `EstablishMPPConnection` error after it is restarted [#3615](https://github.com/pingcap/tiflash/issues/3615)

+ Tools

    + Backup & Restore (BR)

        (dup: release-5.4.1.md > Bug Fixes> Tools> Backup & Restore (BR))- Fix duplicate primary keys when inserting a record into a table after incremental restoration [#33596](https://github.com/pingcap/tidb/issues/33596)
        (dup: release-5.4.1.md > Bug Fixes> Tools> Backup & Restore (BR))- Fix the issue that schedulers do not resume after BR or TiDB Lightning exits abnormally [#33546](https://github.com/pingcap/tidb/issues/33546)
        (dup: release-5.4.1.md > Bug Fixes> Tools> Backup & Restore (BR))- Fix a bug that BR incremental restore returns errors mistakenly due to DDL jobs with empty query [#33322](https://github.com/pingcap/tidb/issues/33322)
        (dup: release-5.4.1.md > Bug Fixes> Tools> Backup & Restore (BR))- Fix the issue that BR does not retry enough times when Regions are not consistent during restoration [#33419](https://github.com/pingcap/tidb/issues/33419)
        (dup: release-6.0.0-dmr.md > Bug fixes> Tools> Backup & Restore (BR))- Fix a bug that BR gets stuck when the restore operation meets some unrecoverable errors [#33200](https://github.com/pingcap/tidb/issues/33200)
        (dup: release-5.4.1.md > Bug Fixes> Tools> Backup & Restore (BR))- Fix the issue that BR fails to back up RawKV [#32607](https://github.com/pingcap/tidb/issues/32607)
        - 修复 BR 无法处理 S3 内部错误的问题 [#34350](https://github.com/pingcap/tidb/issues/34350)

    + TiCDC

        (dup: release-5.4.1.md > Bug 修复> Tools> TiCDC)- 修复切换 owner 会导致其 metrics 数据不正确的问题 [#4774](https://github.com/pingcap/tiflow/issues/4774)
        - 修复 redo log manager 提前 flush log 的问题 [#5486](https://github.com/pingcap/tiflow/issues/5486)
        - 修复当一部分表没有被 redo writer 管理时 resolved ts 提前推进的问题 [#5486](https://github.com/pingcap/tiflow/issues/5486)
        - 添加uuid 作为 redo log file 的后缀以解决文件名冲突引起的数据丢失问题 [#5486](https://github.com/pingcap/tiflow/issues/5486)
        - 修复 mysql sink 可能会保存错误的 checkpointTs 的问题 [#5107](https://github.com/pingcap/tiflow/issues/5107)
        - 修复 TiCDC 集群升级后可能后 panic 的问题 [#5266](https://github.com/pingcap/tiflow/issues/5266)
        (dup: release-5.2.4.md > Bug 修复> Tools> TiCDC)- 修复在同一节点反复调入调出一张表可能会导致同步任务 (changefeed) 被卡住的问题 [#4464](https://github.com/pingcap/tiflow/issues/4464)
        (dup: release-5.4.1.md > Bug 修复> Tools> TiCDC)- 修复了在开启 TLS 后，`--pd` 中设置的第一个 PD 不可用导致 TiCDC 无法启动的问题 [#4777](https://github.com/pingcap/tiflow/issues/4777)
        (dup: release-5.2.4.md > Bug 修复> Tools> TiCDC)- 修复当 PD 状态不正常时 OpenAPI 可能会卡住的问题 [#4778](https://github.com/pingcap/tiflow/issues/4778)
        (dup: release-5.4.1.md > Bug 修复> Tools> TiCDC)- 修复 Unified Sorter 的 workerpool 稳定性问题 [#4447](https://github.com/pingcap/tiflow/issues/4447)
        (dup: release-5.4.1.md > Bug 修复> Tools> TiCDC)- 修复某些情况下序列对象被错误同步的问题 [#4552](https://github.com/pingcap/tiflow/issues/4552)

    + TiDB Data Migration (DM)

        (dup: release-6.1.0.md > 错误修复> Tools> TiDB Data Migration (DM))- 修复任务自动恢复后，DM 会占用更多磁盘空间的问题 [#3734](https://github.com/pingcap/tiflow/issues/3734)，[#5344](https://github.com/pingcap/tiflow/issues/5344)
        (dup: release-6.1.0.md > 错误修复> Tools> TiDB Data Migration (DM))- 修复在未设置 `case-sensitive: true` 时无法同步大写表的问题 [#5255](https://github.com/pingcap/tiflow/issues/5255)
        (dup: release-5.4.1.md > Bug 修复> Tools> TiDB Data Migration (DM))- 修复了某些情况下，过滤 DDL 并在下游手动执行会导致同步任务不能自动重试恢复的问题 [#5272](https://github.com/pingcap/tiflow/issues/5272)
        (dup: release-5.4.1.md > Bug 修复> Tools> TiDB Data Migration (DM))- 修复了在 `SHOW CREATE TABLE` 语句返回的索引中，主键没有排在第一位导致的 DM worker panic 的问题 [#5159](https://github.com/pingcap/tiflow/issues/5159)
        (dup: release-5.4.1.md > Bug 修复> Tools> TiDB Data Migration (DM))- 修复了当开启 GTID 模式或者任务自动恢复时，可能出现一段时间 CPU 占用高并打印大量日志的问题 [#5063](https://github.com/pingcap/tiflow/issues/5063)
        - 修复了 v5.3.1 中重启 master 后 relay log 可能会被关闭的问题 [#4803](https://github.com/pingcap/tiflow/issues/4803)

    + TiDB Lightning

        (dup: release-6.1.0.md > Bug fixes> Tools> TiDB Lightning)- 修复由 `auto_increment` 列的数据越界导致 local 模式导入失败的问题 [#29737](https://github.com/pingcap/tidb/issues/27937)
        (dup: release-5.4.1.md > Bug Fixes> Tools> TiDB Lightning)- 修复前置检查中没有检查本地磁盘空间以及集群是否可用的问题 [#34213](https://github.com/pingcap/tidb/issues/34213)
        (dup: release-5.4.1.md > Bug Fixes> Tools> TiDB Lightning)- 修复了 checksum 报错 “GC life time is shorter than transaction duration” [#32733](https://github.com/pingcap/tidb/issues/32733)