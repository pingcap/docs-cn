---
title: TiDB 4.0.8 Release Notes
---

# TiDB 4.0.8 Release Notes

发版日期：2020 年 10 月 30 日

TiDB 版本：4.0.8

## 新功能

+ TiDB

    - 支持聚合函数 `APPROX_PERCENTILE` [#20197](https://github.com/pingcap/tidb/pull/20197)

+ TiFlash

    - 支持 `CAST` 函数下推

+ Tools

    + TiCDC

        - 支持快照级别一致性复制 [#932](https://github.com/pingcap/ticdc/pull/932)

## 优化提升

+ TiDB

    - 在挑选索引组合计算表达式选择率的贪心算法里优先使用选择率低的索引 [#20154](https://github.com/pingcap/tidb/pull/20154)
    - 在 Coprocessor 运行状态中记录更多的 RPC 信息 [#19264](https://github.com/pingcap/tidb/pull/19264)
    - 优化读取慢日志的效率，以提升慢查询性能 [#20556](https://github.com/pingcap/tidb/pull/20556)
    - 在挑选执行计划时，优化器会在 Plan Binding 阶段等待超时的执行计划以记录更多的 Debug 信息 [#20530](https://github.com/pingcap/tidb/pull/20530)
    - 在慢查询和慢日志中增加语句的重试时间 [#20495](https://github.com/pingcap/tidb/pull/20495) [#20494](https://github.com/pingcap/tidb/pull/20494)
    - 增加系统表 `table_storage_stats` [#20431](https://github.com/pingcap/tidb/pull/20431)
    - 为 `INSERT`/`UPDATE`/`REPLACE` 语句记录 RPC 相关的运行时信息 [#20430](https://github.com/pingcap/tidb/pull/20430)
    - 在 `EXPLAIN FOR CONNECTION` 语句的结果中新增算子信息 [#20384](https://github.com/pingcap/tidb/pull/20384)
    - 在 TiDB 日志中将客户端的连接建立/断开日志级别调整为 `DEBUG` [#20321](https://github.com/pingcap/tidb/pull/20321)
    - 增加 Coprocessor Cache 的监控信息 [#20293](https://github.com/pingcap/tidb/pull/20293)
    - 在运行时信息中记录更多的悲观锁相关参数 [#20199](https://github.com/pingcap/tidb/pull/20199)
    - 在运行时信息和 Trace 功能中增加两个新的耗时信息 [#20187](https://github.com/pingcap/tidb/pull/20187)
    - 在慢日志中添加事务提交的运行时信息 [#20185](https://github.com/pingcap/tidb/pull/20185)
    - 关闭 Index Merge Join [#20599](https://github.com/pingcap/tidb/pull/20599)
    - 为临时字符串常量增加 ISO 8601 和时区支持 [#20670](https://github.com/pingcap/tidb/pull/20670)

+ TiKV

    - 添加 **Fast-Tune** 监控页辅助性能诊断 [#8804](https://github.com/tikv/tikv/pull/8804)
    - 添加 `security.redact-info-log` 配置，用于从日志中删除用户数据 [#8746](https://github.com/tikv/tikv/pull/8746)
    - 修改 error code 的 metafile 格式 [#8877](https://github.com/tikv/tikv/pull/8877)
    - 开启动态修改 `pessimistic-txn.pipelined` 配置 [#8853](https://github.com/tikv/tikv/pull/8853)
    - 默认开启 memory profile 功能 [#8801](https://github.com/tikv/tikv/pull/8801)

+ PD

    - 生成 error 的 metafile [#3090](https://github.com/pingcap/pd/pull/3090)
    - 为 operator 日志添加更多有用信息 [#3009](https://github.com/pingcap/pd/pull/3009)

+ TiFlash

    - 添加关于 Raft log 的监控
    - 添加关于 `cop` 任务内存使用的监控
    - 在存在删除数据的情况下使 `min`/`max` 索引更加准确
    - 提高小批量数据下的查询性能
    - 添加 `error.toml` 文件以支持标准错误码

+ Tools

    + Backup & Restore (BR)

        - 通过将 `split` 和 `ingest` 流水线来加速恢复 [#427](https://github.com/pingcap/br/pull/427)
        - 支持手动恢复 PD 的调度器 [#530](https://github.com/pingcap/br/pull/530)
        - 将移除 PD 调度器接口改为暂停调度器 [#551](https://github.com/pingcap/br/pull/551)

    + TiCDC

        - 在 MySQL sink 中定期输出统计信息 [#1023](https://github.com/pingcap/ticdc/pull/1023)

    + Dumpling

        - 支持直接导出数据到 S3 存储上 [#155](https://github.com/pingcap/dumpling/pull/155)
        - 支持导出 View 视图 [#158](https://github.com/pingcap/dumpling/pull/158)
        - 支持导出只包含生成列的数据表 [#166](https://github.com/pingcap/dumpling/pull/166)

    + TiDB Lightning

        - 支持多字节的 CSV delimiter 和 separator [#406](https://github.com/pingcap/tidb-lightning/pull/406)
        - 通过禁止一些 PD 调度器加速导入 [#408](https://github.com/pingcap/tidb-lightning/pull/408)
        - 在 v4.0 集群上使用 GC-TTL 接口来防止 checksum 阶段的 GC 报错 [#396](https://github.com/pingcap/tidb-lightning/pull/396)

## Bug 修复

+ TiDB

    - 修复使用分区表时，可能遇到非预期 Panic 的问题 [#20565](https://github.com/pingcap/tidb/pull/20565)
    - 修复外连接时，若外表有过滤条件，Index Merge Join 结果有时不正确的问题 [#20427](https://github.com/pingcap/tidb/pull/20427)
    - 修复 `BIT` 类型进行转换时，由于类型长度溢出而错误地返回 `NULL` 的问题 [#20363](https://github.com/pingcap/tidb/pull/20363)
    - 修复 `ALTER TABLE ...` 语法改变 `BIT` 类型的默认值，可能导致默认值错误的问题 [#20340](https://github.com/pingcap/tidb/pull/20340)
    - 修复 `BIT` 类型转换为 `INT64` 时可能导致长度溢出错误的问题 [#20312](https://github.com/pingcap/tidb/pull/20312)
    - 修复混合类型的列在进行条件传播优化时，可能导致结果错误的问题 [#20297](https://github.com/pingcap/tidb/pull/20297)
    - 修复 Plan Cache 在存储过期执行计划时，可能 Panic 的问题 [#20246](https://github.com/pingcap/tidb/pull/20246)
    - 修复 `FROM_UNIXTIME` 和 `UNION ALL` 一起使用时，返回结果会被错误地截断的问题 [#20240](https://github.com/pingcap/tidb/pull/20240)
    - 修复 `Enum` 类型在转换为 `Float` 类型时可能导致错误结果的问题 [#20235](https://github.com/pingcap/tidb/pull/20235)
    - 修复 `RegionStore` 在某些条件下会 Panic 的问题 [#20210](https://github.com/pingcap/tidb/pull/20210)
    - 修复 `BatchPointGet` 请求对无符号整数的最大值进行排序时，结果错误的问题 [#20205](https://github.com/pingcap/tidb/pull/20205)
    - 修复 `Enum`/`Set` 类型在混合 Collation 的类型判定时，结果 Collation 可能与 MySQL 不兼容的问题 [#20364](https://github.com/pingcap/tidb/pull/20364)
    - 修复将其他类型的 `0` 转换为 `YEAR` 类型时，结果与 MySQL 不兼容的问题 [#20292](https://github.com/pingcap/tidb/pull/20292)
    - 修复 `KV Duration` 监控指标中包含 `store0` 时，上报结果不正确的问题 [#20260](https://github.com/pingcap/tidb/pull/20260)
    - 修复写入 `Float` 类型数据时，由于长度溢出提示 `out of range` 错误后仍然被错误地写入问题 [#20252](https://github.com/pingcap/tidb/pull/20252)
    - 修复 `NOT NULL` 属性生成列允许在某些情况下写入 `NULL` 值的问题 [#20216](https://github.com/pingcap/tidb/pull/20216)
    - 修复 `YEAR` 类型数据写入超过允许范围时，错误提示不准确的问题 [#20170](https://github.com/pingcap/tidb/pull/20170)
    - 修复某些情况下悲观事务重试时，会报错 `invalid auto-id` 的问题 [#20134](https://github.com/pingcap/tidb/pull/20134)
    - 修复 `ALTER TABLE` 更改 `Enum`/`Set` 类型时，未进行重复性约束检查的问题 [#20046](https://github.com/pingcap/tidb/pull/20046)
    - 修复一些算子在并发执行时，记录的 Coprocessor Task 运行时信息错误的问题 [#19947](https://github.com/pingcap/tidb/pull/19947)
    - 修复只读系统变量无法被作为 Session 级变量显式 `SELECT` 的问题 [#19944](https://github.com/pingcap/tidb/pull/19944)
    - 修复重复 `ORDER BY` 条件有时会导致执行计划选择不是最优的问题 [#20333](https://github.com/pingcap/tidb/pull/20333)
    - 修复生成 Metric Profile 时，由于字体超过允许的最大值导致失败的问题 [#20637](https://github.com/pingcap/tidb/pull/20637)

+ TiKV

    - 修复加密功能中锁冲突导致 pd-worker 处理心跳慢的问题 [#8869](https://github.com/tikv/tikv/pull/8869)
    - 修复错误生成 memory profile 的问题 [#8790](https://github.com/tikv/tikv/pull/8790)
    - 修复备份时指定 GCS 储存类别 (storage class) 报错的问题 [#8763](https://github.com/tikv/tikv/pull/8763)
    - 修复了重启或者新 Split 的 Learner 节点找不到 Leader 的问题 [#8864](https://github.com/tikv/tikv/pull/8864)

+ PD

    - 修复了 TiDB Dashboard 在某些场景下引起 PD panic 的错误 [#3096](https://github.com/pingcap/pd/pull/3096)
    - 修复了某个 PD store 下线超过十分钟后可能引起 PD panic 的错误 [#3069](https://github.com/pingcap/pd/pull/3069)

+ TiFlash

    - 修复了日志信息中时间戳错误的问题
    - 修复了使用多盘部署时错误的容量导致创建 TiFlash 副本失败的问题
    - 修复了 TiFlash 重启后可能提示数据文件损坏的问题
    - 修复了 TiFlash 崩溃后磁盘上可能残留损坏文件的问题
    - 修复了在写流量较小情况下，由于 Raft Learner 协议中的状态不能及时更新而导致 `wait index duration` 变长，造成查询慢的问题
    - 修复了在重放过期 Raft 日志时，proxy 会向 key-value 引擎写入大量 Region state 信息的问题

+ Tools

    + Backup & Restore (BR)

        - 修复 Restore 期间可能发生的 `send on closed channel` panic 问题 [#559](https://github.com/pingcap/br/pull/559)

    + TiCDC

        - 修复 owner 因更新 GC safepoint 失败而非预期退出的问题 [#979](https://github.com/pingcap/ticdc/pull/979)
        - 修复非预期的任务信息更新 [#1017](https://github.com/pingcap/ticdc/pull/1017)
        - 修复非预期的空 Maxwell 消息 [#978](https://github.com/pingcap/ticdc/pull/978)

    + TiDB Lightning

        - 修复列信息错误的问题 [#420](https://github.com/pingcap/tidb-lightning/pull/420)
        - 修复 Local 模式下获取 Region 信息出现死循环的问题 [#418](https://github.com/pingcap/tidb-lightning/pull/418)
