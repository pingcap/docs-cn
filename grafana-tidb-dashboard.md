---
title: TiDB 监控指标
summary: 了解一些Grafana TiDB Dashboard展示的关键指标
aliases: ['/docs-cn/dev/grafana-tidb-dashboard/','/docs-cn/dev/reference/key-monitoring-metrics/tidb-dashboard/']
---

# TiDB 重要监控指标详解

使用 TiUP 部署 TiDB 集群时，你可以一键部署监控系统 (Prometheus & Grafana)，参考监控架构 [TiDB 监控框架概述](/tidb-monitoring-framework.md)。

目前 Grafana Dashboard 整体分为 PD、TiDB、TiKV、Node\_exporter、Overview 等。TiDB 分为 TiDB 和 TiDB Summary 面板，两个面板的区别如下：

- TiDB 面板：提供尽可能全面的信息，供排查集群异常。
- TiDB Summary 面板：将 TiDB 面板中用户最为关心的部分抽取出来，并做了些许修改。主要用于提供数据库日常运行中用户关心的数据，如 QPS、TPS、响应延迟等，以便作为外部展示、汇报用的监控信息。

以下为 **TiDB Dashboard** 关键监控指标的说明：

## 关键指标说明

- Query Summary
    - Duration：执行时间
        - 客户端网络请求发送到 TiDB，到 TiDB 执行结束后返回给客户端的时间。一般情况下，客户端请求都是以 SQL 语句的形式发送，但也可以包含 `COM_PING`、`COM_SLEEP`、`COM_STMT_FETCH`、`COM_SEND_LONG_DATA` 之类的命令执行时间。
        - 由于 TiDB 支持 Multi-Query，因此，客户端可以一次性发送多条 SQL 语句，如 `select 1; select 1; select 1;`。此时的执行时间是所有 SQL 语句执行完之后的总时间。
    - Command Per Second：TiDB 按照执行结果成功或失败来统计每秒处理的命令数。
    - QPS：按 `SELECT`、`INSERT`、`UPDATE` 类型统计所有 TiDB 实例上每秒执行的 SQL 语句数量。
    - CPS By Instance：按照命令和执行结果成功或失败来统计每个 TiDB 实例上的命令。
    - Failed Query OPM：每个 TiDB 实例上，对每秒钟执行 SQL 语句发生的错误按照错误类型进行统计（例如语法错误、主键冲突等）。包含了错误所属的模块和错误码。
    - Slow query：慢查询的处理时间（整个慢查询耗时、Coprocessor 耗时、Coprocessor 调度等待时间），慢查询分为 internal 和 general SQL 语句。
    - Connection Idle Duration：空闲连接的持续时间。
    - 999/99/95/80 Duration：不同类型的 SQL 语句执行耗时（不同百分位）。

- Query Detail
    - Duration 80/95/99/999 By Instance：每个 TiDB 实例执行 SQL 语句的耗时（不同百分位）。
    - Failed Query OPM Detail：每个 TiDB 实例执行 SQL 语句发生的错误按照错误类型（例如语法错误、主键冲突等）。
    - Internal SQL OPS：整个 TiDB 集群内部 SQL 语句执行的 QPS。内部 SQL 语句是指 TiDB 内部自动执行的 SQL 语句，一般由用户 SQL 语句来触发或者内部定时任务触发。

- Server
    - Uptime：每个 TiDB 实例的运行时间。
    - Memory Usage：每个 TiDB 实例的内存使用，分为进程占用内存和 Golang 在堆上申请的内存。
    - CPU Usage：每个 TiDB 实例的 CPU 使用。
    - Connection Count：每个 TiDB 的连接数。
    - Open FD Count：每个 TiDB 实例的打开的文件描述符数量。
    - Disconnection Count：每个 TiDB 实例断开连接的数量。
    - Event OPM：每个 TiDB 实例关键事件，例如 start，close，graceful-shutdown，kill，hang 等。
    - Goroutine Count：每个 TiDB 实例的 Goroutine 数量。
    - Prepare Statement Count：每个 TiDB 实例现存的 `Prepare` 语句数以及总数。
    - Keep Alive OPM：每个 TiDB 实例每分钟刷新监控的次数，通常不需要关注。
    - Panic And Critical Error：TiDB 中出现的 Panic、Critical Error 数量。
    - Time Jump Back OPS：每个 TiDB 实例上每秒操作系统时间回跳的次数。
    - Get Token Duration：每个连接获取 Token 的耗时  。
    - Skip Binlog Count：TiDB 写入 Binlog 失败的数量。
    - Client Data Traffic：TiDB 和客户端的数据流量。

- Transaction
    - Transaction OPS：每秒事务的执行数量
    - Duration：事务执行时间
    - Transaction Statement Num：事务中的 SQL 语句数量
    - Transaction Retry Num：事务重试次数
    - Session Retry Error OPS：事务重试时每秒遇到的错误数量，分为重试失败和超过最大重试次数两种类型
    - Commit Token Wait Duration：事务提交时的流控队列等待时间。当出现较长等待时，代表提交事务过大，正在限流。如果系统还有资源可以使用，可以通过增大 TiDB 配置文件中 `committer-concurrency` 值来加速提交
    - KV Transaction OPS：每个 TiDB 内部每秒执行的事务数量
        - 一个用户的事务，在 TiDB 内部可能会触发多次事务执行，其中包含，内部元数据的读取，用户事务原子性地多次重试执行等
        - TiDB 内部的定时任务也会通过事务来操作数据库，这部分也包含在这个面板里
    - KV Transaction Duration：每个 TiDB 内部执行事务的耗时
    - Transaction Regions Num：事务操作的 Region 数量  
    - Transaction Write KV Num Rate and Sum：事务写入 KV 的速率总和
    - Transaction Write KV Num：事务操作的 KV 数量
    - Statement Lock Keys：单个语句的加锁个数
    - Send HeartBeat Duration：事务发送心跳的时间间隔
    - Transaction Write Size Bytes Rate and sum：事务写入字节数的速率总和
    - Transaction Write Size Bytes：事务写入的数据大小
    - Acquire Pessimistic Locks Duration：加锁所消耗的时间
    - TTL Lifetime Reach Counter：事务的 TTL 寿命上限。TTL 上限默认值 1 小时，它的含义是从悲观事务第一次加锁，或者乐观事务的第一个 prewrite 开始，超过了 1 小时。可以通过修改 TiDB 配置文件中 `max-txn-ttl` 来改变 TTL 寿命上限
    - Load Safepoint OPS：加载 Safepoint 的次数。Safepoint 作用是在事务读数据时，保证不读到 Safepoint 之前的数据，保证数据安全。因为，Safepoint 之前的数据有可能被 GC 清理掉    
    - Pessimistic Statement Retry OPS：悲观语句重试次数。当语句尝试加锁时，可能遇到写入冲突，此时，语句会重新获取新的 snapshot 并再次加锁
    - Async Commit Transaction Counter：启用 Async commit 机制的事务数量，分为成功、失败两种

- Executor
    - Parse Duration：SQL 语句解析耗时统计。
    - Compile Duration：将解析后的 SQL AST 编译成执行计划的耗时。
    - Execution Duration：执行 SQL 语句执行计划耗时。
    - Expensive Executor OPS：每秒消耗系统资源比较多的算子。包括 Merge Join、Hash Join、Index Look Up Join、Hash Agg、Stream Agg、Sort、TopN 等。
    - Queries Using Plan Cache OPS：每秒使用 Plan Cache 的查询数量。

- Distsql
    - Distsql Duration：Distsql 处理的时长
    - Distsql QPS：每秒Distsql 的数量
    - Distsql Partial QPS：每秒 Partial Results 的数量
    - Scan Keys Num：每个 Query 扫描的 Key 的数量
    - Scan Keys Partial Num：每一个 Partial Result 扫描的 Key 的数量
    - Partial Num：每个 SQL 语句 Partial Results 的数量

- KV Errors
    - KV Backoff Duration：KV 每个请求重试的总时间。TiDB 向 TiKV 的请求都有重试机制，这里统计的是向 TiKV 发送请求时遇到错误重试的总时间
    - TiClient Region Error OPS：TiKV 返回 Region 相关错误信息的数量
    - KV Backoff OPS：TiKV 返回错误信息的数量
    - Lock Resolve OPS：TiDB 清理锁操作的数量。当 TiDB 的读写请求遇到锁时，会尝试进行锁清理
    - Other Errors OPS：其他类型的错误数量，包括清锁和更新 SafePoint

- KV Request
    - KV Request OPS：KV Request 根据 TiKV 显示执行次数
    - KV Request Duration 99 by store：根据 TiKV 显示KV Request 执行时间
    - KV Request Duration 99 by type：根据类型显示KV Request 执行时间

- PD Client
    - PD Client CMD OPS：PD Client 每秒执行命令数量
    - PD Client CMD Duration：PD Client 执行命令耗时
    - PD Client CMD Fail OPS：PD Client 每秒执行命令失败数量
    - PD TSO OPS：TiDB 每秒从 PD 获取 TSO 的数量
    - PD TSO Wait Duration：TiDB 等待从 PD 返回 TSO 的时间
    - PD TSO RPC Duration：TiDB 从向 PD 发送获取 TSO 的请求到接收到 TSO 的耗时
    - Start TSO Wait Duration：TiDB 从向 PD 发送获取 start tso 请求开始到开始等待 tso 返回的时间

- Schema Load
    - Load Schema Duration：TiDB 从 TiKV 获取 Schema 的时间
    - Load Schema OPS：TiDB 从 TiKV 每秒获取 Schema 的数量
    - Schema Lease Error OPM：Schema Lease 出错统计，包括 change 和 outdate 两种，change 代表 schema 发生了变化，outdate 代表无法更新 schema，属于较严重错误，出现 outdate 错误时会报警
    - Load Privilege OPS：TiDB 从 TiKV 每秒获取权限信息的数量

- DDL
    - DDL Duration 95：DDL 语句处理时间的 95% 分位
    - Batch Add Index Duration 100：创建索引时每个 Batch 所花费的最大时间
    - DDL Waiting Jobs Count：等待的 DDL 任务数量
    - DDL META OPM：DDL 每分钟获取 META 的次数
    - DDL Worker Duration 99：每个 DDL worker 执行时间的 99% 分位
    - Deploy Syncer Duration：Schema Version Syncer 初始化，重启，清空等操作耗时
    - Owner Handle Syncer Duration：DDL Owner 在执行更新，获取以及检查 Schema Version 的耗时
    - Update Self Version Duration：Schema Version Syncer 更新版本信息耗时
    - DDL OPM：DDL 语句的每秒执行次数
    - DDL add index progress in percentage：添加索引的进度展示

- Statistics
    - Auto Analyze Duration 95：自动 ANALYZE 耗时
    - Auto Analyze QPS：自动 ANALYZE 数量
    - Stats Inaccuracy Rate：统计信息不准确度
    - Pseudo Estimation OPS：使用假的统计信息优化 SQL 的数量
    - Dump Feedback OPS：存储统计信息 Feedback 的数量
    - Store Query Feedback QPS：存储合并查询的 Feedback 信息的每秒操作数量，该操作在 TiDB 内存中进行
    - Significant Feedback：重要的 Feedback 更新统计信息的数量
    - Update Stats OPS：利用 Feedback 更新统计信息的数量
    - Fast Analyze Status 100：快速收集统计信息的状态

- Owner
    - New ETCD Session Duration 95：创建一个新的 etcd 会话花费的时间。TiDB 通过 etcd client 连接 PD 中的 etcd 保存/读取部分元数据信息。这里记录了创建会话花费的时间
    - Owner Watcher OPS：DDL owner watch PD 的 etcd 的元数据的 goroutine 的每秒操作次数

- Meta
    - AutoID QPS：AutoID 相关操作的数量统计，包括全局 ID 分配、单个 Table AutoID 分配、单个 Table AutoID Rebase 三种操作
    - AutoID Duration：AutoID 相关操作的耗时
    - Region Cache Error OPS：TiDB 缓存的 region 信息每秒遇到的错误次数
    - Meta Operations Duration 99：元数据操作延迟

- GC
    - Worker Action OPM：GC 相关操作的数量，包括 run\_job，resolve\_lock，delete\_range 等操作
    - Duration 99：GC 相关操作的耗时
    - Config：GC 的数据保存时长 (life time) 和 GC 运行间隔 (run interval) 配置
    - GC Failure OPM：GC 相关操作失败数量
    - Delete Range Failure OPM：Delete range 失败的次数
    - Too Many Locks Error OPM：GC 清锁过多错误的数量
    - Action Result OPM：GC 相关操作结果数量
    - Delete Range Task Status：Delete range 的任务状态，包含完成和失败状态
    - Push Task Duration 95：将 GC 子任务推送给 GC worker 的耗时

- Batch Client
    - Pending Request Count by TiKV： TiKV 批量消息处理等待数量
    - Wait Duration 95: 批量消息处理等待时间。
    - Batch Client Unavailable Duration 95： 批处理客户端不可用时长。
    - No Available Connection Counter：批处理客户端不可用连接数。
