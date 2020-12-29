---
title: TiDB 4.0 RC Release Notes
---

# TiDB 4.0 RC Release Notes

发版日期：2020 年 4 月 8 日

TiDB 版本：4.0.0-rc

TiUP 版本：0.0.3

> **警告：**
>
> 该版本存在一些已知问题，已在新版本中修复，建议使用 4.0.x 的最新版本。

## 兼容性变化

+ TiDB

    - 当 tidb-server 状态端口被占用时由原来打印一条告警日志改成拒绝启动 [#15177](https://github.com/pingcap/tidb/pull/15177)

+ TiKV

    - 悲观事务支持 pipelined 功能，TPC-C 性能提升 20%， 风险：pipelined 功能可能会在执行阶段加锁不成功导致事务提交失败 [#6984](https://github.com/tikv/tikv/pull/6984)
    - 调整 unify-read-pool 配置项的方式，仅在新部署的集群时默认启用，旧集群保持原来的方式 [#7059](https://github.com/tikv/tikv/pull/7059)

+ Tools

    - TiDB Binlog

        * 新增验证 Common Name 配置项目的功能 [#934](https://github.com/pingcap/tidb-binlog/pull/934)

## 重点修复的 Bug

+ TiDB

    - 修复 DDL 采用 `PREPARE` 语句执行时，由于内部记录的 job query 不正确，导致上下游同步可能出错的问题 [#15435](https://github.com/pingcap/tidb/pull/15435)
    - 修复 Read Committed 隔离级别下，子查询的输出结果可能不正确的问题 [#15471](https://github.com/pingcap/tidb/pull/15471)
    - 修复 Inline Projection 优化所导致的结果错误问题 [#15411](https://github.com/pingcap/tidb/pull/15411)
    - 修复某些情况下 SQL Hint `INL_MERGE_JOIN` 未正确执行的问题 [#15515](https://github.com/pingcap/tidb/pull/15515)
    - 修复向 `AutoRandom` 列显式写入负数时，`AutoRandom` 列会 Rebase 的问题 [#15397](https://github.com/pingcap/tidb/pull/15397)

## 新功能

+ TiDB

    - 新增大小写敏感的排序规则，用户可在新集群上启用 `utf8mb4_general_ci` 和 `utf8_general_ci` [#33](https://github.com/pingcap/tidb/projects/33)
    - 增强 `RECOVER TABLE` 语法，现在该语法支持恢复被 Truncate 的表 [#15398](https://github.com/pingcap/tidb/pull/15398)
    - 当 tidb-server 状态端口被占用时由原来打印一条告警日志改成拒绝启动 [#15177](https://github.com/pingcap/tidb/pull/15177)
    - 优化使用 Sequence 作为列的默认值时的写入性能 [#15216](https://github.com/pingcap/tidb/pull/15216)
    - 新增 `DDLJobs` 系统表，用于查询 DDL 任务详细信息 [#14837](https://github.com/pingcap/tidb/pull/14837)
    - 优化 `aggFuncSum` 的性能 [#14887](https://github.com/pingcap/tidb/pull/14887)
    - 优化 `EXPLAIN` 的输出结果 [#15507](https://github.com/pingcap/tidb/pull/15507)

+ TiKV

    - 悲观事务支持 pipelined 功能，TPC-C 性能提升 20%，风险：pipelined 功能可能会在执行阶段加锁不成功导致事务提交失败 [#6984](https://github.com/tikv/tikv/pull/6984)
    - HTTP 端口支持 TLS [#5393](https://github.com/tikv/tikv/pull/5393)
    - 调整 unify-read-pool 配置项的方式，仅在新部署的集群时默认启用，旧集群保持原来的方式 [#7059](https://github.com/tikv/tikv/pull/7059)

+ PD

    - 新增通过 HTTP 接口获取 PD 默认配置信息功能 [#2258](https://github.com/pingcap/pd/pull/2258)

+ Tools

    - TiDB Binlog

        * 新增验证 Common Name 配置项目的功能 [#934](https://github.com/pingcap/tidb-binlog/pull/934)

    - TiDB Lightning

        * 优化 TiDB Lightning 的性能 [#281](https://github.com/pingcap/tidb-lightning/pull/281) [#275](https://github.com/pingcap/tidb-lightning/pull/275)

## Bug 修复

+ TiDB

    - 修复 DDL 采用 `PREPARE` 语句执行时，由于内部记录的 job query 不正确，导致上下游同步可能出错的问题 [#15435](https://github.com/pingcap/tidb/pull/15435)
    - 修复 Read Committed 隔离级别下，子查询的输出结果可能不正确的问题 [#15471](https://github.com/pingcap/tidb/pull/15471)
    - 修复 `INSERT ... VALUES` 指定 `BIT(N)` 类型数据时可能报错的问题 [#15350](https://github.com/pingcap/tidb/pull/15350)
    - 修复 DDL Job 内部重试时，`ErrorCount` 的值没有被正确累加导致未完全达到重试预期的问题 [#15373](https://github.com/pingcap/tidb/pull/15373)
    - 修复 TiDB 连接 TiFlash 时，垃圾回收可能工作不正常的问题 [#15505](https://github.com/pingcap/tidb/pull/15505)
    - 修复 Inline Projection 优化所导致的结果错误问题 [#15411](https://github.com/pingcap/tidb/pull/15411)
    - 修复某些情况下 SQL Hint `INL_MERGE_JOIN` 未正确执行的问题 [#15515](https://github.com/pingcap/tidb/pull/15515)
    - 修复向 AutoRandom 列显式写入负数时，AutoRandom 列会 Rebase 的问题 [#15397](https://github.com/pingcap/tidb/pull/15397)

+ TiKV

    - 修复启用 Follower Read 功能，由于 transfer leader 导致系统 Panic 的问题 [#7101](https://github.com/tikv/tikv/pull/7101)

+ Tools

    - TiDB Lightning

        * 修复 backend 是 TiDB 时由于字符转换错误导致数据错误的问题 [#283](https://github.com/pingcap/tidb-lightning/pull/283)

    - TiCDC
        * 修复 MySQL sink 执行 DDL 时，若下游没有 test 库系统报错的问题 [#353](https://github.com/pingcap/ticdc/pull/353)
        * CDC cli 新增实时交互模式功能 [#351](https://github.com/pingcap/ticdc/pull/351)
        * 同步数据时增加对上游表是否可同步的检查 [#368](https://github.com/pingcap/ticdc/pull/368)
        * 新增异步写入 Kafka 的功能 [#344](https://github.com/pingcap/ticdc/pull/344)
