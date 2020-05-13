---
title: TiDB 1.1 Alpha Release Notes
category: Releases
---

# TiDB 1.1 Alpha Release Notes

2018 年 1 月 19 日，TiDB 发布 1.1 Alpha 版。该版本对 MySQL 兼容性、SQL 优化器、系统稳定性、性能做了大量的工作。

## TiDB

- SQL parser
    - 兼容更多语法
- SQL 查询优化器
    - 统计信息减小内存占用
    - 优化统计信息启动时载入的时间
    - 更精确的代价估算
    - 使用 `Count-Min Sketch` 更精确地估算点查的代价
    - 支持更复杂的条件，更充分使用索引
- SQL 执行器
    - 使用 Chunk 结构重构所有执行器算子，提升分析型语句执行性能，减少内存占用
    - 优化 `INSERT IGNORE` 语句性能
    - 下推更多的类型和函数
    - 支持更多的 `SQL_MODE`
    - 优化 `Load Data` 性能，速度提升 10 倍
    - 优化 `Use Database` 性能
    - 支持对物理算子内存使用进行统计
- Server
    - 支持 PROXY protocol

## PD

- 增加更多的 API
- 支持 TLS
- 给 Simulator 增加更多的 case
- 调度适应不同的 Region size
- Fix 了一些调度的 bug

## TiKV

- 支持 Raft learner
- 优化 Raft Snapshot，减少 I/O 开销
- 支持 TLS
- 优化 RocksDB 配置，提升性能
- 优化 Coprocessor `count (*)` 和点查 unique index 的性能
- 增加更多的 Failpoint 以及稳定性测试 case
- 解决 PD 和 TiKV 之间重连的问题
- 增强数据恢复工具 `tikv-ctl` 的功能
- Region 支持按 table 进行分裂
- 支持 `Delete Range` 功能
- 支持设置 snapshot 导致的 I/O 上限
- 完善流控机制
