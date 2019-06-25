---
title: TiDB 2.0 RC4 Release Notes
category: Releases
aliases: ['/docs-cn/releases/2rc4/']
---

# TiDB 2.0 RC4 Release Notes

2018 年 3 月 30 日，TiDB 发布 2.0 RC4 版。该版本在 2.0 RC3 版的基础上，对 MySQL 兼容性、系统稳定性和优化器做了很多改进。

## TiDB

- 支持 `SHOW GRANTS FOR CURRENT_USER();`
- 修复 `UnionScan` 里的 `Expression` 没有 Clone 的问题
- 支持 `SET TRANSACTION` 语法
- 修复 `copIterator` 中潜在的 goroutine 泄露问题
- 修复 `admin check table` 对包含 null 的 unique index 误判的问题
- 支持用科学计数法显示浮点数
- 修复 binary literal 计算时的类型推导
- 修复解析 `CREATE VIEW` 语句的问题
- 修复语句中同时包含 `ORDER BY` 和 `LIMIT 0` 时 panic 的问题
- 提升 `DecodeBytes` 执行性能
- 优化 `LIMIT 0` 为 `TableDual`，避免无用的执行计划构建

## PD

- 支持手动 split Region，可用于处理单 Region 热点的问题
- 修复 `pdctl` 运行 `config show all` 不显示 label property 的问题
- metrics 及代码结构相关的优化

## TiKV

- 限制接收 snapshot 时的内存使用，解决极端情况下的 OOM
- 可以配置 Coprocessor 在遇到 warnings 时的行为
- TiKV 支持导数据模式
- 支持 Region 从正中间分裂
- 提升 CI test 的速度
- 使用 `crossbeam channel`
- 改善 TiKV 在被隔离的情况下由于 leader missing 输出太多日志的问题
