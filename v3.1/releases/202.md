---
title: TiDB 2.0.2 release notes
category: Releases
---

# TiDB 2.0.2 Release Notes

2018 年 5 月 21 日，TiDB 发布 2.0.2 版。该版本在 2.0.1 版的基础上，对系统稳定性做出了改进。

## TiDB

- 修复 Decimal 除法内置函数下推的问题
- 支持 `Delete` 语句中使用 `USE INDEX` 的语法
- 禁止在带有 `Auto-Increment` 的列中使用 `shard_row_id_bits` 特性
- 增加写入 Binlog 的超时机制

## PD

- 使 balance leader scheduler 过滤失连节点
- 更改 transfer leader operator 的超时时间为 10 秒
- 修复 label scheduler 在集群 Regions 不健康状态下不调度的问题
- 修复 evict leader scheduler 调度不当的问题

## TiKV

- 修复 Raft 日志没有打出来的问题
- 支持配置更多 gRPC 相关参数
- 支持配置选举超时的取值范围
- 修复过期 learner 没有删掉的问题
- 修复 snapshot 中间文件被误删的问题