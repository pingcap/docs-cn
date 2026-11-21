---
title: TiDB 监控指标
summary: 了解 Grafana Dashboard 中展示的关键指标。
aliases: ['/docs-cn/dev/grafana-tidb-dashboard/','/docs-cn/dev/reference/key-monitoring-metrics/tidb-dashboard/']
---

# TiDB 重要监控指标详解

使用 TiUP 部署 TiDB 集群时，你可以一键部署监控系统 (Prometheus & Grafana)，参考监控架构 [TiDB 监控框架概述](/tidb-monitoring-framework.md)。

目前 Grafana Dashboard 整体分为 PD、TiDB、TiKV、Node\_exporter、Overview、Performance\_overview 等。TiDB 分为 TiDB 和 TiDB Summary 面板，两个面板的区别如下：

- TiDB 面板：提供尽可能全面的信息，供排查集群异常。
- TiDB Summary 面板：将 TiDB 面板中用户最为关心的部分抽取出来，并做了些许修改。主要用于提供数据库日常运行中用户关心的数据，如 QPS、TPS、响应延迟等，以便作为外部展示、汇报用的监控信息。

以下为 **TiDB Dashboard** 关键监控指标的说明：

## 关键指标说明

### Query Summary

- Duration：执行时间
    - 客户端网络请求发送到 TiDB，到 TiDB 执行结束后返回给客户端的时间。一般情况下，客户端请求都是以 SQL 语句的形式发送，但也可以包含 `COM_PING`、`COM_SLEEP`、`COM_STMT_FETCH`、`COM_SEND_LONG_DATA` 之类的命令执行时间。
    - 由于 TiDB 支持 Multi-Query，因此，客户端可以一次性发送多条 SQL 语句，如 `select 1; select 1; select 1;`。此时的执行时间是所有 SQL 语句执行完之后的总时间。
- Command Per Second：TiDB 按照执行结果成功或失败来统计每秒处理的命令数。
- QPS：按 `SELECT`、`INSERT`、`UPDATE` 类型统计所有 TiDB 实例上每秒执行的 SQL 语句数量。
- CPS By Instance：按照命令和执行结果成功或失败来统计每个 TiDB 实例上的命令。
- Failed Query OPM：每个 TiDB 实例上，对每分钟执行 SQL 语句发生的错误按照错误类型进行统计（例如语法错误、主键冲突等）。包含了错误所属的模块和错误码。
- Affected Rows By Type：按 SQL 类型统计每秒受影响行数。
- Slow query：慢查询的处理时间（整个慢查询耗时、Coprocessor 耗时、Coprocessor 调度等待时间），慢查询分为 internal 和 general SQL 语句。
- Connection Idle Duration：空闲连接的持续时间。
- 999/99/95/80 Duration：不同类型的 SQL 语句执行耗时（不同百分位）。
- 80 Duration：SQL 语句执行耗时的 80% 分位。
- 95 Duration：SQL 语句执行耗时的 95% 分位。
- 99 Duration：SQL 语句执行耗时的 99% 分位。
- 999 Duration：SQL 语句执行耗时的 99.9% 分位。

### Query Detail

- Duration 80/95/99/999 By Instance：每个 TiDB 实例执行 SQL 语句的耗时（不同百分位）。
- Duration 80 By Instance：按实例统计的 80% 分位执行耗时。
- Duration 95 By Instance：按实例统计的 95% 分位执行耗时。
- Duration 99 By Instance：按实例统计的 99% 分位执行耗时。
- Duration 999 By Instance：按实例统计的 99.9% 分位执行耗时。
- Failed Query OPM Detail：每个 TiDB 实例上，对每分钟执行 SQL 语句发生的错误按照错误类型进行统计（例如语法错误、主键冲突等）。
- Internal SQL OPS：整个 TiDB 集群内部 SQL 语句执行的 QPS。内部 SQL 语句是指 TiDB 内部自动执行的 SQL 语句，一般由用户 SQL 语句来触发或者内部定时任务触发。
- Queries In Multi-Statement：一次 Multi-Statement 请求中包含的 SQL 数量（平均值或总量）。

### Server

- Uptime：每个 TiDB 实例的运行时间。
- Memory Usage：每个 TiDB 实例的内存使用，分为进程占用内存和 Golang 在堆上申请的内存。
- CPU Usage：每个 TiDB 实例的 CPU 使用。
- Connection Count：每个 TiDB 的连接数。
- TiDB Server Status：TiDB 实例存活状态统计（up/down）。
- Open FD Count：每个 TiDB 实例的打开的文件描述符数量。
- Disconnection Count：每个 TiDB 实例断开连接的数量。
- Events OPM：每个 TiDB 实例关键事件，例如 start，close，graceful-shutdown，kill，hang 等。
- Goroutine Count：每个 TiDB 实例的 Goroutine 数量。
- Prepare Statement Count：每个 TiDB 实例现存的 `Prepare` 语句数以及总数。
- Runtime GC Rate And GOMEMLIMIT：Golang GC 周期速率与 `GOMEMLIMIT` 配置值。
- Keep Alive OPM：每个 TiDB 实例每分钟刷新监控的次数，通常不需要关注。
- Panic And Critical Error：TiDB 中出现的 Panic、Critical Error 数量。
- Panic And Critial Error：TiDB 中出现的 Panic、Critical Error 数量（与面板命名保持一致）。
- Time Jump Back OPS：每个 TiDB 实例上每秒操作系统时间回跳的次数。
- Get Token Duration：每个连接获取 Token 的耗时。
- Skip Binlog Count：TiDB 写入 Binlog 失败的数量。从 v8.4.0 开始，TiDB Binlog 已移除，该指标不再有计数。
- Client Data Traffic：TiDB 和客户端的数据流量。
- RCCheckTS WriteConflict Num：RC CheckTS 导致的写冲突次数（按类型统计）。
- Handshake Error OPS：客户端握手失败的每秒次数。
- Internal Sessions：TiDB 内部会话数量。
- Active Users：活跃用户数量。
- Connections Per TLS Cipher：按 TLS Cipher 统计的连接速率。
- Connections Per TLS Version：按 TLS 版本统计的连接速率。

### TiDB Runtime

- Memory Usage：TiDB 进程内存使用情况。
- CPU Usage：TiDB 进程 CPU 使用情况。
- Estimated Live Objects：估算的存活对象数量。
- GC STW Duration: Last 256 GC Cycles：最近 256 次 GC 的 STW 时长分布。
- Allocator Throughput：内存分配吞吐量。
- Goroutine Count：Goroutine 数量。
- KV RPC Latency：与 TiKV 交互的 RPC 延迟。
- TSO RPC Latency：获取 TSO 的 RPC 延迟。
- Requests Batch Size：批量请求大小。
- Pending Requests：待处理请求数量。
- Request Enqueue Duration：请求入队等待时长。
- Batch Enqueue Duration：批量请求入队等待时长。
- Goroutine Scheduler Latency：Goroutine 调度延迟。
- GC STW Latency(>=go1.22.0)：Go 1.22+ 的 GC STW 延迟指标。
- Estimated Portion Of CPU Time：估算的 CPU 时间占比。
- Golang GC：Golang GC 相关统计。
- Sync Mutex Wait：互斥锁等待时间。
- GOGC & GOMEMLIMIT：`GOGC` 与 `GOMEMLIMIT` 配置及其影响。
- Heap Alloc：堆内存分配量。
- Heap Free：堆内存空闲量。

### Transaction

- Transaction OPS：每秒事务的执行数量
- Duration：事务执行时间
- Transaction Statement Num：事务中的 SQL 语句数量
- Transaction Retry Num：事务重试次数
- Session Retry Error OPS：事务重试时每秒遇到的错误数量，分为重试失败和超过最大重试次数两种类型
- Commit Token Wait Duration：事务提交时的流控队列等待时间。当出现较长等待时，代表提交事务过大，正在限流。如果系统还有资源可以使用，可以通过增大系统变量 `tidb_committer_concurrency` 的值来加速提交
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
- Transaction Types Per Second：每秒采用两阶段提交 (2PC)、异步提交 （Async Commit) 和一阶段提交 (1PC) 机制的事务数量，提供成功和失败两种数量
- Transaction Commit P99 Backoff：事务提交阶段的 P99 Backoff 等待时长。
- SafeTS Update Conuter：SafeTS 更新次数（按结果与 store 维度）。
- Max SafeTS Gap：SafeTS 与当前时间的最大时间差（安全时间滞后）。
- Assertion：Prewrite 断言（assertion）触发次数（按类型统计）。
- Transaction Execution States Duration：事务各执行状态的耗时分布。
- Transaction With Lock Execution States Duration：带锁事务各执行状态的耗时分布。
- Transaction Enter State：事务进入各状态的次数。
- Transaction Leave State：事务离开各状态的次数。
- Transaction State Count Change：事务状态数量变化。
- Fair Locking Usage：公平加锁机制使用情况（按类型统计）。
- Fair Locking Keys：公平加锁涉及的 Key 数量（按类型统计）。
- Pipelined Flush Keys：Pipelined Flush 批量刷新的 Key 数量分布。
- Pipelined Flush Size：Pipelined Flush 批量刷新的数据量分布。
- Pipelined Flush Duration：Pipelined Flush 批量刷新的耗时分布。
- Statement Shared Lock Keys：单条语句加共享锁的 Key 数量。

### Executor

- Parse Duration：SQL 语句解析耗时统计。
- Compile Duration：将解析后的 SQL AST 编译成执行计划的耗时。
- Execution Duration：执行 SQL 语句执行计划耗时。
- Expensive Executors OPS：每秒消耗系统资源比较多的算子。包括 Merge Join、Hash Join、Index Look Up Join、Hash Agg、Stream Agg、Sort、TopN 等。
- Queries Using Plan Cache OPS：每秒使用 Plan Cache 的查询数量。
- Plan Cache Miss OPS：每秒出现 Plan Cache Miss 的数量。
- Plan Cache Memory Usage：每个 TiDB 实例上所有 Plan Cache 缓存的执行计划占用的总内存。
- Plan Cache Plan Num：每个 TiDB 实例上所有 Plan Cache 缓存的执行计划总数。
- Read From Table Cache OPS：每秒命中 Table Cache 的读请求数量。
- Plan Cache Process Duration：Plan Cache 相关处理的耗时分布。
- Mpp Coordinator Counter：MPP Coordinator 执行次数统计。
- Mpp Coordinator Latency：MPP Coordinator 执行延迟。
- IndexLookUp OPS：Index Look Up 的每秒执行次数。
- IndexLookUp Duration：Index Look Up 执行耗时。
- IndexLookUp Rows：Index Look Up 返回的行数统计。
- IndexLookUp Row Num With PushDown Enabled：开启下推时 Index Look Up 返回的行数统计。

### Distsql

- Distsql Duration：Distsql 处理的时长
- Distsql QPS：每秒 Distsql 的数量
- Distsql Partial QPS：每秒 Partial Results 的数量
- Scan Keys Num：每个 Query 扫描的 Key 的数量
- Scan Keys Partial Num：每一个 Partial Result 扫描的 Key 的数量
- Partial Num：每个 SQL 语句 Partial Results 的数量
- Coprocessor Cache：Coprocessor 缓存的命中与使用情况。
- Coprocessor Seconds 999：Coprocessor 执行耗时的 99.9 分位。

### KV Errors

- KV Backoff Duration：KV 每个请求重试的总时间。TiDB 向 TiKV 的请求都有重试机制，这里统计的是向 TiKV 发送请求时遇到错误重试的总时间
- TiClient Region Error OPS：TiKV 返回 Region 相关错误信息的数量
- KV Backoff OPS：TiKV 返回错误信息的数量
- Lock Resolve OPS：TiDB 清理锁操作的数量。当 TiDB 的读写请求遇到锁时，会尝试进行锁清理
- Other Errors OPS：其他类型的错误数量，包括清锁和更新 SafePoint
- Replica Selector Failure Per Second：副本选择失败的每秒次数。

### KV Request

下面的监控指标与发送给 TiKV 的请求相关。重试请求会被多次计数。

- KV Request OPS：KV Request 根据 TiKV 显示执行次数
- KV Request Duration 99 by store：根据 TiKV 显示 KV Request 执行时间
- KV Request Duration 99 by type：根据类型显示 KV Request 的执行时间
- KV Request Forwarding OPS：KV Request 转发次数。
- KV Request Forwarding OPS By Type：按请求类型统计的 KV Request 转发次数。
- Successful KV Request Wait Duration：成功 KV Request 的等待时长。
- Region Cache OK OPS：Region Cache 命中次数。
- Load Region Duration：加载 Region 的耗时分布。
- RPC Layer Latency：RPC 网络层延迟。
- Stale Read Hit/Miss Ops
    - **hit**：每秒成功执行 Stale Read 的请求数量
    - **miss**：每秒尝试执行 Stale Read 但失败的请求数量
- Stale Read Hit/Miss OPS：Stale Read 命中/未命中的每秒请求数量。
- Stale Read Req Ops
    - **cross-zone**：每秒尝试在远程可用区执行 Stale Read 的请求数量
    - **local**：每秒尝试在本地可用区执行 Stale Read 的请求数量
- Stale Read Req OPS：Stale Read 请求的每秒数量。
- Stale Read Req Traffic
    - **cross-zone-in**：尝试在远程可用区执行 Stale Read 的请求的响应的传入流量
    - **cross-zone-out**：尝试在远程可用区执行 Stale Read 的请求的响应的传出流量
    - **local-in**：尝试在本地可用区执行 Stale Read 的请求的响应的传入流量
    - **local-out**：尝试在本地可用区执行 Stale Read 的请求的响应的传出流量
- Stale Read Req Traffic：Stale Read 请求的流量统计。
- Read Req Traffic
    - **leader-local**：Leader Read 在本地可用区处理读请求产生的流量
    - **leader-cross-zone**：Leader Read 在远程可用区处理读请求产生的流量
    - **follower-local**：Follower Read 在本地可用区处理读请求产生的流量
    - **follower-cross-zone**：Follower Read 在远程可用区处理读请求产生的流量
- Read Req Traffic：读请求流量统计。
- Client-side Slow Score：客户端侧慢速评分（按 store）。
- TiKV-side Slow Score：TiKV 侧慢速评分（按 store）。
- Store Liveness Check Faults：Store 活性检查失败次数。

### PD Client

- PD Client CMD OPS：PD Client 每秒执行命令的数量
- PD Client CMD Duration：PD Client 执行命令耗时
- PD Client CMD Fail OPS：PD Client 每秒执行命令失败的数量
- PD TSO OPS：TiDB 每秒向 PD 发送获取 TSO 的 gRPC 请求的数量 (cmd) 和实际的 TSO 请求数量 (request)；每个 gRPC 请求包含一批 TSO 请求
- PD TSO Wait Duration：TiDB 等待从 PD 返回 TSO 的时间
- PD TSO RPC Duration：TiDB 从向 PD 发送获取 TSO 的 gRPC 请求到接收到 TSO gRPC 请求响应的耗时
- Async TSO Duration：TiDB 从准备获取 TSO 到实际开始等待 TSO 返回的时间
- Estimate TSO RTT Latency：估算的 TSO 往返时延。
- Request Forwarded Status：请求被转发的状态统计。
- PD HTTP Request Duration：TiDB 发往 PD 的 HTTP 请求耗时。
- PD HTTP Request OPS：TiDB 发往 PD 的 HTTP 请求次数。
- PD HTTP Request Fail OPS：TiDB 发往 PD 的 HTTP 请求失败次数。
- Stale Region From PD：从 PD 获取的 stale region 次数。
- Circuit Breaker Event：请求熔断事件统计。
- TiDB Wait TSO Future Duration：TiDB 等待 TSO 进入未来时间的耗时。

### Schema Load

- Load Schema Duration：TiDB 从 TiKV 获取 Schema 的时间
- Load Schema OPS：TiDB 从 TiKV 每秒获取 Schema 的数量
- Schema Lease Error OPM：Schema Lease 出错统计，包括 change 和 outdate 两种，change 代表 schema 发生了变化，outdate 代表无法更新 schema，属于较严重错误，出现 outdate 错误时会报警
- Load Privilege OPS：TiDB 从 TiKV 每秒获取权限信息的数量
- Load Schema Action Duration：按加载动作统计的 Schema 加载耗时。
- Load Data From Cached Table Duration：从 Table Cache 加载数据的耗时。
- Schema Cache OPS：Schema Cache 的读写次数（按 action/type）。
- Lease Duration：Schema lease 剩余时长。
- Infoschema V2 Cache Operation：Infoschema V2 缓存操作次数与命中率。
- Infoschema V2 Cache Size：Infoschema V2 缓存使用量与上限。
- Infoschema V2 Cache Table Count：Infoschema V2 缓存表数量。
- TableByName API Duration：Infoschema `TableByName` API 调用耗时。

### DDL

- DDL Duration 95：DDL 语句处理时间的 95% 分位
- Batch Add Index Duration 100：创建索引时每个 Batch 所花费的最大时间
- Waiting Job Count：等待的 DDL 任务数量
- DDL META OPM：DDL 每分钟获取 META 的次数
- DDL Worker Duration 99：每个 DDL worker 执行时间的 99% 分位
- OPS：按类型统计 DDL 处理次数/速率。
- Execute Duration：DDL 作业执行耗时分布。
- Job Worker Operations Duration：DDL worker 操作耗时分布（按类型、动作与结果）。
- Sync Schema Version Operations Duration：同步 Schema Version 的操作耗时分布。
- System Table Operations Duration：系统表相关操作耗时分布。
- Running Job Count By Worker Pool：按 worker 池统计运行中的 DDL 作业数量。
- Deploy Syncer Duration：Schema Version Syncer 初始化，重启，清空等操作耗时
- Owner Handle Syncer Duration：DDL Owner 在执行更新，获取以及检查 Schema Version 的耗时
- Update Self Version Duration：Schema Version Syncer 更新版本信息耗时
- DDL OPM：DDL 语句的每秒执行次数
- Backfill Progress In Percentage：backfill DDL 任务的进度展示
- Backfill Data Rate：回填数据速率。
- Add Index Scan Rate：Add Index 扫描速率分布。
- Retryable Error：可重试错误次数。
- Add Index Backfill Import Speed：Add Index 回填导入速率。

### Dist Execute Framework

- Task Status：分布式执行框架任务状态统计。
- Completed/Total Subtask Count：已完成/总子任务数量。
- Pending Subtask Count：等待中的子任务数量。
- SubTask Running Duration：子任务运行时长分布。
- Subtask Pending Duration：子任务等待时长分布。
- Uncompleted Subtask Distribution On TiDB Nodes：未完成子任务在 TiDB 节点上的分布。
- Slots Usage：分布式执行框架 slot 使用情况。

### Statistics & Plan Management

- Auto Analyze Duration 95：自动 ANALYZE 耗时
- Auto Analyze QPS：自动 ANALYZE 数量
- Stats Inaccuracy Rate：统计信息不准确度
- Pseudo Estimation OPS：使用假的统计信息优化 SQL 的数量
- Dump Feedback OPS：存储统计信息 Feedback 的数量
- Store Query Feedback QPS：存储合并查询的 Feedback 信息的每秒操作数量，该操作在 TiDB 内存中进行
- Significant Feedback：重要的 Feedback 更新统计信息的数量
- Update Stats OPS：利用 Feedback 更新统计信息的数量
- Auto/Manual Analyze Duration：自动/手动 ANALYZE 的耗时分布。
- Auto/Manual Analyze Queries Per Minute：自动/手动 ANALYZE 每分钟的执行次数。
- Stats Healthy Distribution：统计信息健康度分布。
- Sync Load QPS：统计信息同步加载的 QPS。
- Sync Load Latency P9999：统计信息同步加载的 P9999 延迟。
- Stats Cache Cost：统计信息缓存容量与使用情况。
- Stats Cache OPS：统计信息缓存操作次数。
- Plan Replayer Task OPM：Plan Replayer 任务每分钟执行次数。
- Historical Stats OPM：历史统计信息任务每分钟执行次数。
- Stats Loading Duration：统计信息加载耗时。
- Stats Meta/Usage Updating Duration：统计信息元数据与使用情况更新耗时。
- Binding Cache Memory Usage：Plan Binding 缓存内存占用。
- Binding Cache Hit / Miss OPS：Plan Binding 缓存命中/未命中次数。
- Number Of Bindings In Cache：Plan Binding 缓存中的绑定数量。

### Owner

- New ETCD Session Duration 95：创建一个新的 etcd 会话花费的时间。TiDB 通过 etcd client 连接 PD 中的 etcd 保存/读取部分元数据信息。这里记录了创建会话花费的时间
- Owner Watcher OPS：DDL owner watch PD 的 etcd 的元数据的 goroutine 的每秒操作次数

### Meta

- AutoID QPS：AutoID 相关操作的数量统计，包括全局 ID 分配、单个 Table AutoID 分配、单个 Table AutoID Rebase 三种操作
- AutoID Duration：AutoID 相关操作的耗时
- AutoID Client Conn Reset Counter：AutoID 客户端连接重置次数。
- Region Cache Error OPS：TiDB 缓存的 region 信息每秒遇到的错误次数
- Meta Operations Duration 99：元数据操作延迟

### GC

- Worker Action OPM：GC 相关操作的数量，包括 run\_job，resolve\_lock，delete\_range 等操作
- Duration 99：GC 相关操作的耗时
- GC Duration By Stage：GC 各阶段耗时分布。
- Config：GC 的数据保存时长 (life time) 和 GC 运行间隔 (run interval) 配置
- GC Failure OPM：GC 相关操作失败的数量
- Delete Range Failure OPM：Delete range 失败的次数
- Too Many Locks Error OPM：GC 清锁过多错误的数量
- Action Result OPM：GC 相关操作结果数量
- Delete Range Task Status：Delete range 的任务状态，包含完成和失败状态
- Push Task Duration 95：将 GC 子任务推送给 GC worker 的耗时
- Resolve Locks Range Tasks Status：Resolve Locks range 任务状态。
- Resolve Locks Range Tasks Push Task Duration 95：推送 Resolve Locks range 任务的耗时。
- Ongoing User Transaction Duration：进行中的用户事务持续时间。
- Ongoing Internal Transaction Duration：进行中的内部事务持续时间。

### Batch Client

- Pending Request Count by TiKV：TiKV 批量消息处理的等待数量
- Wait Duration 95: 批量消息处理的等待时间。
- Batch Client Unavailable Duration 95：批处理客户端的不可用时长。
- No Available Connection Counter：批处理客户端不可用的连接数。
- Wait Connection Establish Duration：批处理客户端建立连接的等待时间。
- Batch Receive Average Duration：批处理接收数据的平均耗时。

### TopSQL

- Ignore Event Per Minute：TopSQL 忽略事件的每分钟数量。
- 99 Report Duration：TopSQL 上报耗时的 99 分位。
- Report Data Count Per Minute：TopSQL 每分钟上报的数据量。
- Total Report Count：TopSQL 上报总次数（含不同结果类型）。
- CPU Profiling OPS：CPU Profiling 相关操作的每秒次数。
- TiKV Stat Task OPS：TiKV 资源统计任务的每秒次数。

### TTL

- TiDB CPU Usage: 每个 TiDB 实例的 CPU 使用。
- TiDB CPU Usage：每个 TiDB 实例的 CPU 使用。
- TiKV IO MBps: 每个 TiKV 实例的 I/O 吞吐量。
- TiKV IO MBps：每个 TiKV 实例的 I/O 吞吐量。
- TiKV CPU: 每个 TiKV 实例的 CPU 使用。
- TiKV CPU：每个 TiKV 实例的 CPU 使用。
- TTL QPS By Type：TTL 任务产生的不同类型语句的 QPS 信息。
- TTL Insert Rows Per Second: 每秒钟向 TTL 表插入的数据行数。
- TTL Insert Rows Per Second：每秒钟向 TTL 表插入的数据行数。
- TTL Processed Rows Per Second：TTL 任务每秒处理的过期数据的行数。
- TTL Insert Rows Per Hour: 每小时总共向 TTL 表插入的行数。
- TTL Insert Rows Per Hour：每小时总共向 TTL 表插入的行数。
- TTL Delete Rows Per Hour: 每小时总共删除的过期行数。
- TTL Delete Rows Per Hour：每小时总共删除的过期行数。
- TTL Scan Query Duration：TTL 扫描语句的执行时间。
- TTL Delete Query Duration：TTL 删除语句的执行时间。
- Scan Worker Time By Phase：TTL 扫描 worker 各阶段耗时。
- Delete Worker Time By Phase：TTL 删除 worker 各阶段耗时。
- TTL Job Count By Status：当前正在执行的 TTL 任务的数量。
- TTL Task Count By Status：当前正在执行的 TTL 子任务的数量。
- Table Count By TTL Schedule Delay：按 TTL 调度延迟统计的表数量。
- TTL Insert/Delete Rows By Day：按天统计 TTL 插入/删除行数。
- TTL Event Count Per Minute：TTL 事件每分钟数量（含调度与运行时事件）。

### Resource Manager

- GOGC：TiDB 资源管理相关的 `GOGC` 配置值。
- EMA CPU Usage：资源管理器估算的 CPU 使用率（EMA）。

### Follower Read

- Closest Replica Hit Count Per Second：最近副本命中次数（每秒）。
- Coprocessor Response Size Per Instance And TiKV：按 TiDB 实例与 TiKV 维度统计的 Coprocessor 响应大小。
- Coprocessor Response Size：Coprocessor 响应大小分布。

### Import Into

- Total Encode/Deliver/Import-kv Speed：Import 任务编码/投递/导入的总速率。
- Encoded/Delivered/Imported Data Size：Import 任务已编码/已投递/已导入的数据量。
- Delivered KV Count：已投递的 KV 数量。
- Data Read/Encode/Deliver Average Duration：数据读取/编码/投递的平均耗时。
- Import/Normal Mode：Import/Normal 模式状态（与相关阈值配置关联）。

### Global Sort

- Write To Cloud Storage Duration：写入云存储的耗时分布。
- Write To Cloud Storage Rate：写入云存储的速率分布。
- Read From Cloud Storage Duration：从云存储读取的耗时分布。
- Read From Cloud Storage Rate：从云存储读取的速率分布。
- Ingest Worker Count：Ingest worker 数量。
- Active Parallel Upload Worker Count：并行上传 worker 数量。

### Network Transmission

- Query Network Trasmission Bytes：查询相关的网络传输字节数（按类型）。

### Memory Arbitrator

- Work Mode：内存仲裁器工作模式。
- Arbitration Exec：内存仲裁任务执行次数（按类型）。
- Events：内存仲裁事件统计（按类型与实例）。
- Mem Quota Stats：内存配额统计。
- Mem Quota Arbitration Duration：内存配额仲裁耗时分布。
- Mem Pool Stats：内存池使用统计。
- Runtime Mem Pressure：运行时内存压力指标。
- Waiting Tasks Stats：等待仲裁任务统计。

### Resource Control

- RU Config：资源单元（RU）配置。
- RU：资源单元（RU）消耗。
- RU Max(Max Cost During 20s Period)：20 秒窗口内 RU 最大消耗。
- RU Per Query：单次查询的 RU 消耗。
- RRU：读资源单元（RRU）消耗。
- RRU Per Query：单次查询的 RRU 消耗。
- WRU：写资源单元（WRU）消耗。
- WRU Per Query：单次查询的 WRU 消耗。
- KV Request Count：KV 请求数量。
- KV Request Count Per Query：单次查询的 KV 请求数量。
- Bytes Read：读取字节数。
- Bytes Read Per Query：单次查询读取字节数。
- Bytes Written：写入字节数。
- Bytes Written Per Query：单次查询写入字节数。
- KV CPU Time：KV 层 CPU 时间消耗。
- SQL CPU Time：SQL 层 CPU 时间消耗。
- Cross AZ Traffic Bytes(Read)：跨可用区读流量。
- Cross AZ Traffic Bytes(Write)：跨可用区写流量。
- Active Resource Groups：活跃资源组数量。
- Total KV Request Count：KV 请求总数。
- Failed KV Request Count：KV 请求失败数量。
- Successful KV Request Wait Duration：成功 KV 请求等待耗时。
- Successful KV Request Count：成功 KV 请求数量。
- Token Request Handle Duration：令牌请求处理耗时。
- Token Request Count：令牌请求数量。
- Query Max Duration：Runaway 查询最大耗时。
- Runaway Event：Runaway 事件统计。
- Runaway Flusher Flush OPS：Runaway Flusher 刷新次数。
- Runaway Flusher Add OPS：Runaway Flusher 追加次数。
- Runaway Flusher Batch Size：Runaway Flusher 批大小。
- Runaway Flusher Duration：Runaway Flusher 执行耗时。
- Runaway Flusher Interval：Runaway Flusher 执行间隔。
- Runaway Syncer OPS：Runaway Syncer 同步次数。
- Runaway Syncer Duration：Runaway Syncer 同步耗时。
- Runaway Syncer Interval：Runaway Syncer 同步间隔。
- Runaway Syncer Checkpoint：Runaway Syncer 检查点。
- CPU Time By Priority：按优先级统计 CPU 时间消耗。
- CPU Quota Limit By Priority：按优先级统计 CPU 配额上限。
- Tasks Wait QPS By Priority：按优先级统计任务等待 QPS。
- Priority Task Wait Duration：按优先级统计任务等待耗时。
- Background Task RU：后台任务 RU 消耗。
- Background Task Resource Utilization：后台任务资源利用率。
- Background Task IO Limit：后台任务 IO 限制。
- Background Task CPU Consumption：后台任务 CPU 消耗。
- Background Task CPU Limit：后台任务 CPU 限制。
- Background Task IO Consumption：后台任务 IO 消耗。
- Background Task Total Wait Duration：后台任务总等待耗时。
