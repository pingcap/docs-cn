---
title: TiDB 重要监控指标详解
category: reference
---

# TiDB 重要监控指标详解

使用 Ansible 部署 TiDB 集群时，一键部署监控系统 (Prometheus/Grafana)，监控架构请看 [TiDB 监控框架概述](v2.1/how-to/monitor/overview.md)。

目前 Grafana Dashboard 整体分为 PD、TiDB、TiKV、Node\_exporter、Overview 等。

以下为 TiDB Dashboard 部分监控说明：

## 说明

- Query Summary
    - Duration：SQL 执行的时间
    - Statement OPS：SQL 执行数量统计（包含 `SELECT`、`INSERT`、`UPDATE` 等）
    - QPS By Instance：每个 TiDB 上的 QPS

- Query Detail
    - Internal SQL OPS：TiDB 内部 SQL 语句执行数量统计

- Server
    - Connection count：每个 TiDB 的连接数
    - Failed Query OPM：失败 SQL 的统计，例如语法错误、主键冲突等
    - Heap Memory Usage：每个 TiDB 使用的堆内存大小
    - Events OPM：统计关键事件，例如 start，close，graceful-shutdown，kill，hang 等
    - Uncommon Error OPM：TiDB 非正常错误的统计，包括 panic，binlog 写失败等

- Transaction
    - Transaction OPS：事务执行数量统计
    - Transaction Duration：事务执行的时间
    - Session Retry Error OPS：事务重试时遇到的错误数量

- Executor
    - Expensive Executor OPS：消耗系统资源比较多的算子统计，包括 Merge Join，Hash Join，Index Look Up Join，Hash Agg，Stream Agg，Sort，TopN 等
    - Queries Using Plan Cache OPS：使用 Plan Cache 的查询数量统计

- Distsql
    - Distsql Duration：Distsql 处理的时长
    - Distsql QPS：Distsql 的数量统计

- KV Errors
    - KV Retry Duration：KV 重试请求的时间
    - TiClient Region Error OPS：TiKV 返回 Region 相关错误信息的数量
    - KV Backoff OPS：TiKV 返回错误信息的数量（事务冲突等）
    - Lock Resolve OPS：事务冲突相关的数量
    - Other Errors OPS：其他类型的错误数量，包括清锁和更新 SafePoint

- KV Duration
    - KV Cmd Duration 99：KV 命令执行的时间

- KV Count
    - KV Cmd OPS：KV 命令执行数量统计
    - Txn OPS：启动事务的数量统计
    - Load SafePoint OPS：更新 SafePoint 的数量统计

- PD Client
    - PD TSO OPS：TiDB 从 PD 获取 TSO 的数量
    - PD TSO Wait Duration：TiDB 从 PD 获取 TSO 的时间
    - PD Client CMD OPS：PD Client 执行命令数量统计
    - PD Client CMD Duration: PD Client 执行命令耗时
    - PD Client CMD Fail OPS：PD Client 执行命令失败统计

- Schema Load
    - Load Schema Duration：TiDB 从 TiKV 获取 Schema 的时间
    - Load Schema OPS：TiDB 从 TiKV 获取 Schema 的数量统计
    - Schema Lease Error OPM：Schema Lease 出错，包括 change 和 outdate 两种，出现 outdate 错误时会报警

- DDL
    - DDL Duration 95：DDL 语句处理时间统计
    - DDL Batch Add Index Duration 100：创建索引时每个 Batch 所花费的时间统计
    - DDL Deploy Syncer Duration：Schema Version Syncer 初始化，重启，清空等操作耗时
    - Owner Handle Syncer Duration：DDL Owner 在执行更新，获取以及检查 Schema Version 的耗时
    - Update Self Version Duration：Schema Version Syncer 更新版本信息耗时

- Statistics
    - Auto Analyze Duration 95：自动 ANALYZE 耗时统计
    - Auto Analyze QPS：自动 ANALYZE 数量统计
    - Stats Inaccuracy Rate：统计信息不准确度统计
    - Pseudo Estimation OPS：使用假的统计信息优化 SQL 的数量统计
    - Dump Feedback OPS：存储统计信息 Feedback 的数量统计
    - Update Stats OPS：利用 Feedback 更新统计信息的数量统计

- Meta
    - AutoID QPS：AutoID 相关操作的数量统计，包括全局 ID 分配、单个 Table AutoID 分配、单个 Table AutoID Rebase 三种操作
    - AutoID Duration：AutoID 相关操作的耗时

- GC
    - Worker Action OPM：GC 相关操作的数量统计，包括 run\_job，resolve\_lock，delete\_range 等操作
    - Duration 99：GC 相关操作的耗时统计
    - GC Failure OPM：GC 相关操作失败数量统计
    - Too Many Locks Error OPM：GC 清锁过多错误的数量统计
