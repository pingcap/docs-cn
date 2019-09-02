---
title: TiDB 重要监控指标详解
category: reference
---

# TiDB 重要监控指标详解

使用 Ansible 部署 TiDB 集群时，一键部署监控系统 (Prometheus/Grafana)，监控架构请看 [TiDB 监控框架概述](v3.0/how-to/monitor/overview.md)。

目前 Grafana Dashboard 整体分为 PD、TiDB、TiKV、Node\_exporter、Overview 等，TiDB 分为 TiDB 和 TiDB Summary 面板（其中 TiDB 面板包含 TiDB Summary 面板的内容）。

以下为 TiDB Dashboard 部分监控说明：

## 说明

- Query Summary
    - Duration：SQL 执行的时间
    - QPS：每个 TiDB 上的 SQL 执行结果按照 OK/Error 统计
    - Statement OPS：SQL 执行数量统计（包含 `SELECT`、`INSERT`、`UPDATE` 等）
    - QPS By Instance：每个 TiDB 上的 QPS
    - Failed Query OPM：每个 TiDB 实例上，执行 SQL 语句发生错误按照错误类型的统计（例如语法错误、主键冲突等）
    - Slow query：慢查询处理时间统计（整个慢查询耗时、Coprocessor 耗时、Coprocessor 调度等待时间）
    - 999/99/95/80 Duration：不同类型的 SQL 语句执行耗时统计（不同百分位）

- Query Detail
    - Duration 80/95/99/999 By Instance：每个 TiDB 实例执行 SQL 语句的耗时统计（不同百分位）
    - Failed Query OPM Detail：整个集群执行 SQL 语句发生的错误按照错误类型统计（例如语法错误、主键冲突等）
    - Internal SQL OPS：TiDB 内部 SQL 语句执行数量统计

- Server
    - Uptime：TiDB 运行时间
    - Memory Usage：不同 TiDB 实例的内存使用统计
    - CPU Usage：不同 TiDB 实例的 CPU 使用统计
    - Connection Count：每个 TiDB 的连接数
    - Open FD Count：不同 TiDB 实例的打开的文件描述符统计
    - Goroutine Count：不同 TiDB 实例的 Goroutine 数量
    - Go GC Duration：不同 TiDB 实例的 GC 耗时统计
    - Go Threads：不同 TiDB 实例的线程数量
    - Go GC Count：不同 TiDB 实例的 GC 执行次数统计
    - Go GC CPU Usage：不同 TiDB 实例的 GC CPU 统计
    - Events OPM：统计关键事件，例如 start，close，graceful-shutdown，kill，hang 等
    - Keep Alive OPM：不同 TiDB 实例每分钟刷新监控的次数
    - Prepare Statement Count：不同 TiDB 实例执行 Prepare 语句数以及总数统计
    - Time Jump Back OPS：不同 TiDB 实例上每秒钟时间回跳的次数
    - Heap Memory Usage：每个 TiDB 使用的堆内存大小
    - Uncommon Error OPM：TiDB 非正常错误的统计，包括 panic，binlog 写失败等
    - Handshake Error OPS：不同 TiDB 实例每秒握手错误的次数统计
    - Get Token Duration：建立连接后获取 Token 耗时

- Transaction
    - Transaction OPS：事务执行数量统计
    - Duration：事务执行的时间
    - Transaction Retry Num：事务重试次数
    - Transaction Statement Num：一个事务中的 SQL 语句数量
    - Session Retry Error OPS：事务重试时遇到的错误数量
    - Local Latch Wait Duration：本地事务等待时间

- Executor
    - Parse Duration：SQL 语句解析耗时统计
    - Compile Duration：将 SQL AST 编译成执行计划耗时统计
    - Execution Duration：SQL 语句执行耗时统计
    - Expensive Executor OPS：消耗系统资源比较多的算子统计，包括 Merge Join，Hash Join，Index Look Up Join，Hash Agg，Stream Agg，Sort，TopN 等
    - Queries Using Plan Cache OPS：使用 Plan Cache 的查询数量统计

- Distsql
    - Distsql Duration：Distsql 处理的时长
    - Distsql QPS：Distsql 的数量统计
    - Distsql Partial QPS：每秒 Partial Results 的数量
    - Scan Keys Num：每个 Query 扫描的 Key 的数量
    - Scan Keys Partial Num：每一个 Partial Result 扫描的 Key 的数量
    - Partial Num：每个 SQL 语句 Partial Results 的数量

- KV Errors
    - KV Retry Duration：KV 重试请求的时间
    - TiClient Region Error OPS：TiKV 返回 Region 相关错误信息的数量
    - KV Backoff OPS：TiKV 返回错误信息的数量（事务冲突等）
    - Lock Resolve OPS：事务冲突相关的数量
    - Other Errors OPS：其他类型的错误数量，包括清锁和更新 SafePoint

- KV Duration
    - KV Request Duration 999 by store：KV Request 执行时间，根据 TiKV 显示
    - KV Request Duration 999 by type：KV Request 执行时间，根据请求类型显示
    - KV Cmd Duration 99/999：KV 命令执行的时间

- KV Count
    - KV Cmd OPS：KV 命令执行数量统计
    - KV Txn OPS：启动事务的数量统计
    - Txn Regions Num 90：事务使用的 Region 数量统计
    - Txn Write Size Bytes 100：事务写入的字节数统计
    - Txn Write KV Num 100：事务写入的 KV 数量统计
    - Load SafePoint OPS：更新 SafePoint 的数量统计

- PD Client
    - PD Client CMD OPS：PD Client 执行命令数量统计
    - PD Client CMD Duration: PD Client 执行命令耗时
    - PD Client CMD Fail OPS：PD Client 执行命令失败统计
    - PD TSO OPS：TiDB 从 PD 获取 TSO 的数量
    - PD TSO Wait Duration：TiDB 从 PD 获取 TSO 的时间
    - PD TSO RPC Duration：TiDB 从调用 PD 获取 TSO gRPC 接口花费的时间

- Schema Load
    - Load Schema Duration：TiDB 从 TiKV 获取 Schema 的时间
    - Load Schema OPS：TiDB 从 TiKV 获取 Schema 的数量统计
    - Schema Lease Error OPM：Schema Lease 出错，包括 change 和 outdate 两种，出现 outdate 错误时会报警

- DDL
    - DDL Duration 95：DDL 语句处理时间统计
    - Batch Add Index Duration 100：创建索引时每个 Batch 所花费的时间统计
    - DDL Waiting Jobs Count：等待的 DDL 任务数量
    - DDL META OPM：DDL 每分钟获取 META 的次数
    - Deploy Syncer Duration：Schema Version Syncer 初始化，重启，清空等操作耗时
    - Owner Handle Syncer Duration：DDL Owner 在执行更新，获取以及检查 Schema Version 的耗时
    - Update Self Version Duration：Schema Version Syncer 更新版本信息耗时

- Statistics
    - Auto Analyze Duration 95：自动 ANALYZE 耗时统计
    - Auto Analyze QPS：自动 ANALYZE 数量统计
    - Stats Inaccuracy Rate：统计信息不准确度统计
    - Pseudo Estimation OPS：使用假的统计信息优化 SQL 的数量统计
    - Dump Feedback OPS：存储统计信息 Feedback 的数量统计
    - Update Stats OPS：利用 Feedback 更新统计信息的数量统计
    - Significant Feedback：重要的 Feedback 更新统计信息的数量统计

- Meta
    - AutoID QPS：AutoID 相关操作的数量统计，包括全局 ID 分配、单个 Table AutoID 分配、单个 Table AutoID Rebase 三种操作
    - AutoID Duration：AutoID 相关操作的耗时
    - Meta Operations Duration 99：Meta 操作延迟

- GC
    - Worker Action OPM：GC 相关操作的数量统计，包括 run\_job，resolve\_lock，delete\_range 等操作
    - Duration 99：GC 相关操作的耗时统计
    - GC Failure OPM：GC 相关操作失败数量统计
    - Action Result OPM：GC 相关操作结果数量统计
    - Too Many Locks Error OPM：GC 清锁过多错误的数量统计

- Batch Client
    - Pending Request Count by TiKV：等待处理的 Batch 消息数量统计
    - Wait Duration 95：等待处理的 Batch 消息延迟统计
    - Batch Client Unavailable Duration 95：Batch 客户端不可用的时间统计
