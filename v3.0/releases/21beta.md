---
title: TiDB 2.1 Beta Release Notes
category: Releases
aliases: ['/docs-cn/releases/21beta/']
---

# TiDB 2.1 Beta Release Notes

2018 年 6 月 29 日，TiDB 发布 2.1 Beta 版。相比 2.0 版本，该版本对系统稳定性、优化器、统计信息以及执行引擎做了很多改进。

## TiDB

- SQL 优化器
    - 优化 `Index Join` 选择范围，提升执行性能
    - 优化关联子查询，下推 Filter 和扩大索引选择范围，部分查询的效率有数量级的提升
    - 在 `UPDATE`、`DELETE` 语句中支持 `Index Hint` 和 `Join Hint`
    - 优化器 Hint `TIDM_SMJ` 在没有索引可用的情况下可生效
    - 支持更多函数下推：`ABS`/`CEIL`/`FLOOR`/`IS TRUE`/`IS FALSE`
    - 在常量折叠过程中特殊处理函数 `IF` 和 `IFNULL`
    - 优化 `EXPLAIN` 语句输出格式
- SQL 执行引擎
    - 实现并行 `Hash Aggregate` 算子，部分场景下能提高 `Hash Aggregate` 计算性能 350%
    - 实现并行 `Project` 算子，部分场景下性能提升达 74%
    - 并发地读取 `Hash Join` 的 `Inner` 表和 `Outer` 表的数据，提升执行性能
    - 修复部分场景下 `INSERT … ON DUPLICATE KEY UPDATE …` 结果不正确的问题
    - 修复 `CONCAT_WS`/`FLOOR`/`CEIL`/`DIV` 内建函数的结果不正确的问题
- Server
    - 添加 HTTP API 打散 table 的 Regions 在 TiKV 集群中的分布
    - 添加 `auto_analyze_ratio` 系统变量控制自动 analyze 的阈值
    - 添加 HTTP API 控制是否打开 `general log`
    - 添加 HTTP API 在线修改日志级别
    - 在 `general log` 和 `slow query log`  中添加 user 信息
    - 支持 Server side cursor
- 兼容性
    - 支持更多 MySQL 语法
    - `BIT` 聚合函数支持 `ALL` 参数
    - 支持 `SHOW PRIVILEGES` 语句
- DML
    - 减少 `INSERT INTO SELECT` 语句的内存占用
    - 修复 Plan Cache 的性能问题
    - 添加 `tidb_retry_limit` 系统变量控制事务自动重试的次数
    - 添加 `tidb_disable_txn_auto_retry` 系统变量控制事务是否自动重试
    - 修复写入 `time` 类型的数据精度问题
    - 支持本地冲突事务排队，优化冲突事务性能
    - 修复 `UPDATE` 语句的 `Affected Rows`
    - 优化 `insert ignore on duplicate key update` 语句性能
    - 优化 `Create Table` 语句的执行速度
    - 优化 `Add index` 的速度，在某些场景下速度大幅提升
    - 修复 `Alter table add column` 增加列超过表的列数限制的问题
    - 修复在某些异常情况下 DDL 任务重试导致 TiKV 压力增加的问题
    - 修复在某些异常情况下 TiDB 不断重载 Schema 信息的问题
- DDL
    - `Show Create Table` 不再输出外键相关的内容
    - 支持 `select tidb_is_ddl_owner()` 语句，方便判断 TiDB 是否为 `DDL Owner`
    - 修复某些场景下 `YEAR` 类型删除索引的问题
    - 修复并发执行场景下的 `Rename table` 的问题
    - 支持 `ALTER TABLE FORCE` 语法
    - 支持 `ALTER TABLE RENAME KEY TO` 语法
    - `admin show ddl jobs` 输出信息中添加表名、库名等信息

## PD

- PD 节点间开启 `Raft PreVote`，避免网络隔离后恢复时产生的重新选举
- 优化 Balance Scheduler 频繁调度小 Region 的问题
- 优化热点调度器，在流量统计信息抖动时适应性更好
- `region merge` 调度时跳过数据行数较多的 Region
- 默认开启 `raft learner` 功能，降低调度时出现宕机导致数据不可用的风险
- `pd-recover` 移除 max-replica 参数
- 增加 `Filter` 相关的 metrics
- 修复 tikv-ctl unsafe recovery 之后 Region 信息没更新的问题
- 修复某些场景下副本迁移导致 TiKV 磁盘空间耗尽的问题
- 兼容性提示
    - 由于新版本存储引擎更新，不支持在升级后回退至 2.0.x 或更旧版本
    - 新版本默认开启 `raft learner` 功能，如果从 1.x 版本集群升级至 2.1 版本，须停机升级或者先滚动升级 TiKV，完成后再滚动升级 PD

## TiKV

- 升级 Rust 到 `nightly-2018-06-14` 版本
- 开启 `PreVote`，避免网络隔离后恢复时产生的重新选举
- 添加 metric，显示 RocksDB 内部每层的文件数和 `ingest` 相关的信息
- GC 运行时打印版本太多的 `key`
- 使用 `static metric` 优化多 label metric 性能（YCSB raw get 提升 3%）
- 去掉多个模块的 `box`，使用范型提升运行时性能（YCSB raw get 提升 3%）
- 使用 `asynchronous log` 提升写日志性能
- 增加收集线程状态的 metric
- 通过减少程序中 `box` 的使用来减少内存拷贝的次数，提升性能
