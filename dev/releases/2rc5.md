---
title: TiDB 2.0 RC5 Release Notes
category: Releases
---

# TiDB 2.0 RC5 Release Notes

2018 年 4 月 17 日，TiDB 发布 2.0 RC5 版。该版本在 RC4 版的基础上，对 MySQL 兼容性、系统稳定性和优化器做了很多改进。

## TiDB

- 修复应用 `Top-N` 下推规则的问题
- 修复对包含 NULL 值的列的行数估算
- 修复 Binary 类型的 0 值
- 修复事务内的 `BatchGet` 问题
- 回滚 `Add Index` 操作的时候，清除清除已写入的数据，减少空间占用
- 优化 `insert on duplicate key update` 语句性能，提升 10 倍以上
- 修复 `UNIX_TIMESTAMP` 函数返回结果类型问题返回结果类型问题
- 修复在添加 NOT NULL 列的过程中，插入 NULL 值的问题
- `Show Process List` 语句支持显示执行语句的内存占用
- 修复极端情况下 `Alter Table Modify Column` 出错问题
- 支持通过 `Alter` 语句设置 table comment

## PD

- 添加 Raft Learner 支持
- 优化 Balance Region Scheduler，减少调度开销
- 调整默认 `schedule-limit` 配置
- 修复频繁分配 ID 问题
- 修复添加调度兼容性问题

## TiKV

- `tikv-ctl` 支持 compact 指定的 Region
- Raw KV 支持 Batch Put、Batch Get、Batch Delete 和 Batch Scan
- 解决太多 snapshot 导致的 OOM 问题
- Coprocessor 返回更详细的错误信息
- 支持通过 `tikv-ctl` 动态修改 TiKV 的 `block-cache-size`
- 进一步完善 importer 功能
- 简化 `ImportSST::Upload` 接口
- 设置 gRPC 的 `keepalive` 属性
- `tikv-importer` 作为独立的 binary 从 TiKV 中分离出来
- 统计 Coprocessor 每个 scan range 命令扫描了多少行数据
- 解决在 macOS 系统上的编译问题
- 优化 metric 相关的内容
- 解决 snapshot 相关的一个潜在 bug
- 解决误用了一个 RocksDB metric 的问题
- Coprocessor 支持 `overflow as warning` 选项
