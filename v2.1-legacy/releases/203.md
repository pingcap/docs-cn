---
title: TiDB 2.0.3 release notes
category: Releases
---

# TiDB 2.0.3 Release Notes

2018 年 6 月 1 日，TiDB 发布 2.0.3 版。该版本在 2.0.2 版的基础上，对系统兼容性、稳定性做出了改进。

## TiDB

- 支持在线更改日志级别
- 支持 `COM_CHANGE_USER` 命令
- 支持二进制协议情况下使用时间类型参数
- 优化带 `BETWEEN` 表达式的查询条件代价估算
- 在 `SHOW CREATE TABLE` 里不显示 `FOREIGN KEY` 信息
- 优化带 `LIMIT` 子句的查询代价估算
- 修复 `YEAR` 类型作为唯一索引的问题
- 修复在没有唯一索引的情况下 `ON DUPLICATE KEY UPDATE` 的问题
- 修复 `CEIL` 函数的兼容性问题
- 修复 `DECIMAL` 类型计算 `DIV` 的精度问题
- 修复 `ADMIN CHECK TABLE` 误报的问题
- 修复 `MAX`/`MIN` 在特定表达式参数下 panic 的问题
- 修复特殊情况下 `JOIN` 结果为空的问题
- 修复 `IN` 表达式构造查询 `Range` 的问题
- 修复使用 `Prepare` 方式进行查询且启用 `Plan Cache` 情况下的 Range 计算问题
- 修复异常情况下频繁加载 Schema 信息的问题

## PD

- 修复在特定条件下收集 hot-cache metrics 会 panic 的问题
- 修复对旧的 Region 产生调度的问题

## TiKV

- 修复 learner flag 错误上报给 PD 的 bug
- 在 `do_div_mod` 中 `divisor/dividend` 为 0 时返回错误
