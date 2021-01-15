---
title: TiDB 4.0.10 Release Notes
---

# TiDB 4.0.10 Release Notes

发版日期：2021 年 1 月 15 日

TiDB 版本：4.0.10

## 新功能

+ PD

    - 添加了配置项 `enable-redact-log`，可以设置将日志中的用户数据脱敏 [#3266](https://github.com/pingcap/pd/pull/3266)

+ TiFlash

    - 添加了配置项 `security.redact_info_log`，可以设置将日志中的用户数据脱敏

## 改进提升

+ TiDB

    - 添加 `txn-entry-size-limit` 配置项，用于限制事务中单个 key-value 记录的大小 [#21843](https://github.com/pingcap/tidb/pull/21843)

+ PD

    - 优化了 `store-state-filter` 的监控，可以显示更加具体的原因 [#3100](https://github.com/tikv/pd/pull/3100)
    - 更新 `go.etcd.io/bbolt` 依赖至 v1.3.5 [#3331](https://github.com/tikv/pd/pull/3331)

+ Tools

    + TiCDC

        - 为 `maxwell` 协议默认开启 old value 特性 [#1144](https://github.com/pingcap/ticdc/pull/1144)
        - 默认启用 unified sorter 特性 [#1230](https://github.com/pingcap/ticdc/pull/1230)

    + Dumpling

        - 支持检查未定义的参数，支持输出导出的进度 [#228](https://github.com/pingcap/dumpling/pull/228)

    + TiDB Lightning

        - 支持重试读 S3 遇到的错误 [#533](https://github.com/pingcap/tidb-lightning/pull/533)

## Bug 修复

+ TiDB

    - 修复由于并发导致的 batch client 超时问题 [#22336](https://github.com/pingcap/tidb/pull/22336)
    - 修复由于并发地自动捕获 SQL 绑定而导致的重复绑定问题 [#22295](https://github.com/pingcap/tidb/pull/22295)
    - 当日志级别为 `'debug'` 时，让 SQL 语句绑定的自动捕获正确运行 [#22293](https://github.com/pingcap/tidb/pull/22293)
    - 当 Region 合并正在发生时，正确地释放锁 [#22267](https://github.com/pingcap/tidb/pull/22267)
    - 对 `Datetime` 类型的用户变量返回正确的值 [#22143](https://github.com/pingcap/tidb/pull/22143)
    - 修复错误使用 Index Merge 访问方式的问题 [#22124](https://github.com/pingcap/tidb/pull/22124)
    - 修复由于执行计划缓存导致 TiFlash 报 `wrong precision` 错误的问题 [#21960](https://github.com/pingcap/tidb/pull/21960)
    - 修复由于 schema 变更导致的错误结果 [#21596](https://github.com/pingcap/tidb/pull/21596)
    - 避免在 `ALTER TABLE` 中不必要地更改 column flag [#21474](https://github.com/pingcap/tidb/pull/21474)
    - 让包含子查询块别名的 optimizer hint 生效 [#21380](https://github.com/pingcap/tidb/pull/21380)
    - 为 `IndexHashJoin` 和 `IndexMergeJoin` 生成正确的 optimizer hint [#21020](https://github.com/pingcap/tidb/pull/21020)

+ TiKV

    - 修复了 peer 和 ready 之间的错误映射 [#9409](https://github.com/tikv/tikv/pull/9409)
    - 修复一些日志信息在 `security.redact-info-log` 设置为 `true` 时未脱敏的问题 [#9314](https://github.com/tikv/tikv/pull/9314)

+ PD

    - 修复 ID 分配不是单调递增的问题 [#3308](https://github.com/tikv/pd/pull/3308) [#3323](https://github.com/tikv/pd/pull/3323)
    - 修复 PD client 在某些情况下可能卡住的问题 [#3285](https://github.com/pingcap/pd/pull/3285)

+ TiFlash

    - 修复了 TiFlash 解析老版本 TiDB 表结构失败导致 TiFlash 无法启动的问题
    - 修复了在 RedHat 系统中 TiFlash 会对 `cpu_time` 进行错误处理导致 TiFlash 无法启动的问题
    - 修复了将配置项 `path_realtime_mode` 设置为 `true` 时 TiFlash 无法启动的问题
    - 修复了当调用有三个参数的 `substr` 函数时，返回结果错误的问题
    - 修复了当 TiDB 对 `Enum` 枚举进行无损修改时，TiFlash 无法读取修改后的值的问题

+ Tools

    + TiCDC

        - 修复 `maxwell` 协议的问题，包括 `base64` 数据输出和将 TSO 转换成 unix timestamp [#1173](https://github.com/pingcap/ticdc/pull/1173)
        - 修复过期的元数据可能引发新创建的 changefeed 异常的问题 [#1184](https://github.com/pingcap/ticdc/pull/1184)
        - 修复在关闭的 notifier 上创建 receiver 的问题[#1199](https://github.com/pingcap/ticdc/pull/1199)
        - 修复在 etcd 更新缓慢时导致内存访问量增长的问题 [#1227](https://github.com/pingcap/ticdc/pull/1227)
        - 修复 `max-batch-size` 不生效的问题 [#1253](https://github.com/pingcap/ticdc/pull/1253)
        - 修复清理过期任务信息的问题 [#1280](https://github.com/pingcap/ticdc/pull/1280)
        - 修复 MySQL sink 中由于没有调用 `rollback` 而导致回收 db conn 卡住的问题 [#1285](https://github.com/pingcap/ticdc/pull/1285)

    + Dumpling

        - 修改默认设置的 `tidb_mem_quota_query` 的行为以避免 TiDB 内存溢出 [#233](https://github.com/pingcap/dumpling/pull/233)

    + Backup & Restore (BR)

        - 修复 BR v4.0.9 无法恢复 BR v4.0.8 保存在 GCS 上的备份 [#688](https://github.com/pingcap/br/pull/688)
        - 修复在恢复 GCS 上的备份时可能发生的 panic 问题 [#673](https://github.com/pingcap/br/pull/673)
        - 默认禁用备份统计信息以避免 BR 内存溢出 [#693](https://github.com/pingcap/br/pull/693)

    + TiDB Binlog

        - 修复在启用 `AMEND TRANSACTION` 特性时，Drainer 可能会使用错误 schema 来生成 SQL 语句的问题 [#1033](https://github.com/pingcap/tidb-binlog/pull/1033)

    + TiDB Lightning

        - 修复未正确编码 Region key 而导致分裂 Region 失败问题 [#531](https://github.com/pingcap/tidb-lightning/pull/531)
        - 修复可能丢失 `CREATE TABLE` 失败的错误 [#530](https://github.com/pingcap/tidb-lightning/pull/530)
        - 修复使用 TiDB-backend 时遇到的 `column count mismatch` 问题 [#535](https://github.com/pingcap/tidb-lightning/pull/535)
