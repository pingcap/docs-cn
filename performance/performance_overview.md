---
title: TiDB 性能分析和优化手册
---

# TiDB 性能分析和优化手册

## 目标
对于分布式数据库 TiDB 用户来说, 数据库性能分析和优化是一件困难的事情。本文的目标是介绍基于数据库时间的系统优化方法论，使得 TiDB 用户可以从全局、自顶向下的角度看待用户响应时间和数据库时间，并进行可靠的性能分析和优化。

## 用户响应时间和数据库时间
### 用户响应时间
用户响应时间是指应用系统为用户返回请求结果所花的时间。一个典型的用户请求的处理时序图如下，包含了用户和应用系统的网络延迟，应用的处理时间，应用和数据库的交互次数和网络延迟，数据库时间等。用户响应时间受到请求链路上所有子系统的影响，比如网络延迟和带宽，系统并发用户数和请求类型，服务器 CPU和IO和资源使用率等。只有知道用户响应时间的的瓶颈，才能对整个系统进行有效的优化。
`ΔT` 时间内总的用户响应时间等于平均 TPS 乘以平均的用户响应时间乘以 `ΔT`

```
ΔT Total user response time = TPS × user avg reponse time × ΔT
```
![用户响应时间](/media/performance/performance-overview/user_response_time_cn.png)

### 数据库时间
`ΔT` 时间内数据库时间为数据库处理所有应用请求的时间和。数据库时间可以通过多种方式求得：

1. QPS 乘以 平均 query 延迟 乘以 ΔT
2. 平均活跃会话数 乘以 ΔT
3. 通过 TiDB 内部的 Promtheus 指标 TiDB_server_handle_query_duration_seconds_sum 求得

```
ΔT DB Time = QPS × avg latency × ΔT
ΔT DB Time = avg active connections × ΔT 
ΔT DB Time = rate(TiDB_server_handle_query_duration_seconds_sum) × ΔT 
```
TiDB 内部对 SQL 的处理路径进行了完善的测量，方便定位数据库内部的性能瓶颈。

## 基于数据库时间的性能优化方法论

现实世界中，应用系统架构复杂，系统设计和实现时，很可能没有对用户响应时间进行完整的测量，系统往往无法提供基于用户响应时间的分解性能数据，这给整个系统的性能分析和优化带来了困难。得益于 TiDB 对于数据库时间的完善度测量和记录，普通用户通过对比用户响应时间和数据库时间，可以回答两个问题：
1. 整个系统的瓶颈是否在 TiDB 中
2. 如果瓶颈在 TiDB 内部，具体在整个分布式系统的哪个位置

### 整个系统的瓶颈是否在 TiDB 中
如果数据库时间占用户响应时间比例小，可以确认瓶颈不在数据库中，需要关注数据库外面的组件，比如应用服务器硬件资源是否存在瓶颈，网络延迟是否过高等。反之，如果数据库时间占用户响应时间比例大，可以确认瓶颈在数据库中，需要在数据库内部进行性能分析和优化。对于 TiDB 用户来说，最便捷的方式是对比 SQL 处理平均延迟和事务中 TiDB 连接的空闲时间。如果 TiDB 连接在事务中平均空闲时间比 SQL 处理延迟高，说明应用的事务中，主要的延迟不在数据库中。如果 SQL 平均处理延迟高，说明事务中主要的瓶颈在 TiDB 内部。

### 如果瓶颈在 TiDB 内部，如何定位
一个典型的 SQL 的处理流程如下所以，TiDB 的性能指标覆盖了绝大部分的处理路径。
![数据库时间分解图](/media/dashboard/dashboard-diagnostics-time-relation.png)

数据库时间是所有 SQL 处理时间的总和。通过对数据库时间进行以下三个维度的分解，可以快速的的对 TiDB 内部瓶颈进行定位
1. 按 SQL 处理类型分解，可知哪种类型的 SQL 语句消耗数据库时间最多
2. 按 SQL 处理的 4 个步骤分解，可知哪个步骤 get_token/parse/compile/execute 消耗时间最多
3. 对于 execute 耗时，按照 TiDB 执行器本身的时间、TSO 等待时间和 kv 请求时间分解，可知执行阶段的瓶颈

这三种分解对应三个公式：
```
DB Time = Select Time + Insert Time + Update Time + Delete Time + Commit Time + ...
DB Time = Get Token Time + Parse Time + Comiple Time + Execute Time
Execute Time = TiDB Executor Time + KV Request Time + PD TSO Wait Time 
```

## 利用 Performance Overview 面板进行性能分析和优化
Performance Overview Grafana 面板从版本 v6.0.0 发布。本章会介绍利用这个面板，TiDB 用户如何快速进行基于数据库时间的性能分析和优化。
Performance Overview 包含三种数据：
1. 数据库时间和 SQL 执行时间分解
2. TiDB 关键指标和资源利用率
3. Query 延迟分解

### 数据库时间和 SQL 执行时间概览
DB time 指标为 TiDB 每秒处理 SQL 的延迟总和，等于 TiDB 集群每秒并发处理应用 SQL 请求的总时间(等于活跃连接数)。通过三个面积堆叠图，用户可以了解数据库负载的类型，可以快速定位在数据库的瓶颈集中在哪个执行阶段，主要是处理什么语句，SQL 执行阶段主要等待 TiKV 或者 PD 什么请求类型。 以下举例说明：

#### 例子 1 TPC-C 负载
- 第一个图，Database Time by SQL Type， 主要消耗时间的语句为 commit、update、select 和 insert 语句。
- 第二个图，Ddatabase Time By SQL Phase，主要消耗时间的为 execute 阶段。
- 第三个图，execute 阶段，主要消耗时间为 kv 请求 Prewrite 和 Commit。
    > **注意：**
    >
    > kv request 时间比的总和大于 execute 时间长是正常的，因为 TiDB 执行器可能并发向多个 TiKV 发送 kv 请求，导致总的 kv 请求等待时间大于执行时间。TPC-C 负载中，事务提交时，TiDB 会向多个 TiKV 并行发送 Prewrite 和 Commit，所以这个例子中 Prewrite、Commit 和 PessimisticsLock 请求的总和明显大于 execute 时间。

![TPC-C](/media/performance/performance-overview/tpcc_db_time.png)

#### 例子 2 OLTP 读密集负载
- 第一个图，Database Time by SQL Type， 主要消耗时间的语句为 select、commit、update和 insert 语句。select 占据绝大部分的数据库时间。
- 第二个图，Ddatabase Time By SQL Phase，主要消耗时间的为 execute 阶段。
- 第三个图，execute 阶段，主要消耗时间为 pd tso_wait 和 kv Get、Prewrite 和 Commit。

![OLTP](/media/performance/performance-overview/oltp_normal_db_time.png)

#### 例子 3 只读 OLTP 负载
1. 第一个图，Database Time by SQL Type， 几乎所有语句为 select。
1. 第二个图，Ddatabase Time By SQL Phase，主要消耗时间的为 compile 和 execute 阶段。
1. 第三个图，execute 阶段，主要消耗时间为 kv 请求 BatchGet。

![OLTP](/media/performance/performance-overview/oltp_long_compile_db_time.png)
    > **注意：**
    >
    > BatchGet 请求的总时间远大于 execute 时间，是因为 select 语句需要从多个 TiKV 并行读取几千行数据。

### TiDB 关键指标和资源利用率

#### Query Per Second，Command Per Second, Prepared-Plan-Cache
 第一个图 QPS 面板包含应用的 SQL 语句类型执行次数分布。第二图 CPS 表示 Command Per Second，这里的 Command 代表着 MySQL 协议的命令类型。同样一个查询语句可以通过 query 或者 prepared statement 的命令类型发送到 TiDB。第三个图 Queries Using Plan Cache OPS TiDB 集群每秒命中执行计划缓存的次数。通过观察这三个面板，可以了解应用的负载类型，与 TiDB 的交互方式，以及是否能有效的利用 TiDB 的执行计划缓存。 
##### 例子 1 TPC-C 负载
TPC-C 负载类型主要已 Update、Select 和 Insert 语句为主。总的 QPS 等于 每秒 StmtExecute 次数，并且 StmtExecute 每秒的数据基本等于 Queries Using Plan Cache OPS. 这是 OLTP 负载理想的情况，客户端执行使用 prepared statement，并且在客户端缓存了 prepared statement 对象，执行每条 SQL 语句时直接调用 Statement Execute。执行执行时都命中执行计划缓存，不需要重新 compile 生成执行计划.
![TPC-C](/media/performance/performance-overview/tpcc_qps.png)
##### 例子 2 只读 OLTP 负载，使用 query 命令无法使用执行计划缓存
这个负载中 Commit = Rollback = Select，应用开启了 auto-commit 并发每次从连接池获取连接都会执行 rollback，所以这三种语句的次数是相同的。 图中出现红色加粗的线为 Failed Query，坐标的值为右边的 Y 轴。非 0 代表这负载中存在少量的错误语句。总的 QPS 等于 CPS 面板中的 Query。说明应用使用 query 命令，Queries Using Plan Cache OPS 面板没有数据，因为不使用 prepared statement 接口，无法使用 TiDB 的执行计划缓存， 意味着应用的每一条 query，TiDB 都需要重新解析，重新生成执行计划。通常会导致 compile 时间变长以及 TiDB CPU 消耗的增加。
![OLTP-Query](/media/performance/performance-overview/oltp_long_compile_qps.png)

#### 例子 3 OLTP 负载，使用 prepared statement  接口无法使用执行计划缓存
StmtPreare 次数 = StmtExecute 次数 = StmtClose 次数 ~= StmtFetch, 应用使用了 prepare -> execute -> fetch -> close 的 loop，很多框架都会在 execute 之后调用 close，确保资源不会泄露。这会带来两个问题
- 执行每条 sql 语句 网络往返次数 X4 
- Queries Using Plan Cache OPS 为 0， 无法命中执行计划缓存。StmtClose 命令在版本 默认会清理缓存的执行计划，导致下一次 StmtPreare 命令需要重新生成执行计划。
    > **注意：**
    >
    > TiDB v6.0.0版本开始，可以通过全局变量控制 StmtClose 命令不清理已被缓存的执行计划，使得下一次的 SQL 的执行不需要重新生成执行计划 `set global tidb_ignore_prepared_cache_close_stmt=on;`。

![OLTP-Prepared](/media/performance/performance-overview/oltp_long_compile_qps.png)

####
#### KV/TSO Request OPS 和连接信息
kv 和 tso 每秒请求数据统计，其中 kv request total 是 tidb 到 tikv 所有请求的总和，观察 TiDB 到 PD 和 TiKV 的请求类型，可以了解集群内部的负载特征。除了常规的总的连接数和每个 tidb 连接数，可以判断连接总数是否正常，每个 tidb 的连接数是否不均衡。active connections 记录着活跃连接数，等于每秒的数据库时间。

##### 例子 1 繁忙的负载
下图 TPC-C 负载中，每秒总的 kv 请求的数量是 104.2k。最高的请求类型是 PessimisticsLock、Prewrite、Commit 和 BatchGet 等。总的连接数 810，三个 TiDB 实例的连接数大体均衡。活跃的连接数为 787.1， 对比活跃连接数和总连接数，97% 的连接都是活跃的，通常意味这数据库是这个应用系统的瓶颈。
![TPC-C](/media/performance/performance-overview/tpcc_kv_conn.png)

##### 例子 2  空闲的负载
 下图负载中 每秒总的 kv 请求数据是2.6k，tso 请求次数是每秒 1.1k。总的连接数为 410，连接数在三个 tidb 中相对均衡。活跃连接数只有 2.5，说明数据库系统非常空闲。
![OLTP](/media/performance/performance-overview/cloud_long_idle_kv_conn.png)

#### TiDB 和 TiKV CPU 和 IO 使用情况
这两个面板可以观察到 TiDB 和 TiKV 的逻辑 CPU 使用率和 IO 吞吐，包含平均、最大和 Delta(最大 cpu利用率 减去 最小 cpu 使用率），可以用来判定 TiDB 和 Tikv 总体的 cpu 利用率；Detal 值可用来判断 TiDB 是否存在 CPU 使用负载不均衡(通常伴随着应用连接不均衡)，TiKV 是否存在热点。用户通过 TiDB 和 TiKV 的资源使用概览，可以快速的判断集群是否存在资源瓶颈，最需要扩容的组件是 TiDB 还是 TiKV。

##### 例子 1 TiDB 资源使用率高
下图负载中，每个 TiDB 和 TiKV 配置 8 CPU。TiDB 平均 CPU 为 575%。最大 CPU 为 643%，Delta CPU 为 136%。 TiKV 平均 CPU 为 146%，最大 CPU 215%。Delta CPU 为 118%。TIKV 的平均 IO 吞吐为 9.06 MB/s，最大 IO 吞吐为 19.7 MB/s，Delta IO 吞吐 为 17.1 MB/s。TiDB 的 CPU 消耗明显更高，并接近于 8 CPU 的瓶颈，可以考虑扩容 TiDB。
![TPC-C](/media/performance/performance-overview/tidb_high_cpu.png)

##### 例子 2 TiKV 资源使用率高
下图 TPC-C 负载中，每个 TiDB 和 TiKV 配置 16 CPU。TiDB 平均 CPU 为 883%。最大 CPU 为 962%，Delta CPU 为 153%。 TiKV 平均 CPU 为 1288%，最大 CPU 1360%。Delta CPU 为 126%。TIKV 的平均 IO 吞吐为130 MB/s，最大 IO 吞吐为 153 MB/s，Delta IO 吞吐 为 53.7 MB/s。可以看到 TiKV 的 CPU 消耗更高，因为 TPC-C 是一个写密集场景，这是正常的现象，可以考虑扩容 TiKV 节点提升性能。
![TPC-C](/media/performance/performance-overview/tpcc_cpu_io.png)

### Query 延迟分解和关键的延迟指标

延迟面板通常包含平均值和 99 分位数，平均值用来定位总体的瓶颈，99 分位数用来判断是否存在延迟严重抖动的情况。判断性能抖动范围时，可能还需要需要借助 999 分位数。

#### Duration 和 Connection Idle Duration

Duration 面板包含了所有语句 99 延迟和每种 SQL 类型的平均延迟。Connection Idle Duration 面板包含连接空闲的平均和 99 延迟:
- in-txn：代表事务中连接的空闲时间，当连接处于事务中时，处理完上一条 SQL 之后，收到下一条 SQL 语句的间隔时间。
- not-in-txn：当连接没有处于事务中，处理完上一条 SQL 之后，收到下一条 SQL 语句的间隔时间。 

通过对比 query  的平均延迟和 connection idle duration的延迟，可以判断整个系统性能瓶颈或者用户响应时间的抖动是否因为 TiDB 导致的。应用负载不是只读的，包含事务，应该使用 query 平均延迟和 `avg-in-txn` 进行比较，因为通常应用进行数据库事务时，使用同一个数据库连接。对比平均的 query 延迟和 `avg-in-txn`，可以判断应用处理事务时，主要的时间是花在数据库内部还是在数据库外面，借此定位用户响应时间的瓶颈。 如果数据库是一个只读负载，不存在 `avg-in-txn` 指标，可以换成 `avg-not-in-txn` 指标。

现实的客户负载中，瓶颈在数据库外面的情况并不少见，列举几个例子：
- 客户端服务器配置过低，CPU 资源不够
- 使用 HAProxy 作为 TiDB 集群代理，但是 CPU 资源不够
- 使用 HaProxy 作为 TiDB 集群代理，但是高负载下网络流量打满
- 应用服务器到数据库延迟过高，比如公有云环境应用和 TiDB 集群不在一个地区，比如数据库的 DNS 均衡器和 TiDB 集群不在一个地区
- 客户端程序存在瓶颈，无法充分利用服务器的多CPU 或者多 Numa 资源，比如应用只使用一个 JVM 向 TiDB 建立上千个 JDBC 连接 

##### 例子 1 用户响应时间的瓶颈在 TiDB 中
下图 TPC-C 负载中，所有 SQL 语句的平均延迟 477 us，99 延迟 3.13ms。平均 commit 语句 2.02ms，平均 insert 语句 609ms，平均查询语句 468us。事务中连接空闲时间 `avg-in-txn` 171 us。平均的 query 延迟明显大于 `avg-in-txn`，说明事务处理中，主要的瓶颈在数据库内部。
![TiDB is the Bottleneck](/media/performance/performance-overview/tpcc_duration_idle.png)

##### 例子 2 用户响应时间的瓶颈不在 TiDB 中
下午负载中，平均 query 延迟为 1.69ms，事务中连接空闲时间 `avg-in-txn` 为 18ms。说明事务中，TiDB 平均花了 1.69ms 处理完一个 SQL 语句之后，需要等待 18ms 才能收到下一条语句。用户响应时间的瓶颈不在 TiDB 中。这个例子中，超高的连接空闲时间是因为这是一个公有云环境，应用和数据库不在一个地址，网络延迟高导致了连接空闲时间高。
![TiDB is the Bottleneck](/media/performance/performance-overview/cloud_query_long_idle.png)


#### Parse、Compile 和 Execute Duration
在 TiDB 中，从输入的查询文本到返回结果的[`典型处理流程`](/sql-optimization-concepts.md)。
SQL 的在 TiDB 内部的处理分为四个阶段，get token、parse、compile 和 execute
- get token 通常只有几微秒的时间，可以忽略
- parse 阶段 query 语句解析为抽象语法树 abstract syntax tree (AST)
- compile 阶段，基于成本的优化器， 根据 Parse 阶段输出的 AST 和统计信息，编译出执行计划。整个过程还会被分为逻辑优化与物理优化，前者通过一些规则对查询计划进行优化，例如基于关系代数的列裁剪等，后者则通过具体物理实现的时间复杂度、资源消耗和物理属性等统计信息来确定代价，并选择整体成本最小的物理执行计划。
- execute 执行器根据执行计划中的算子，执行 sql 语句，包含等待 tso、kv 请求的时间和 tidb 执行器本身处理数据的时间

如果应用统一使用 query 或者 StmtExecute MySQL 命令接口，可以使用以下公式来定位平均延迟的瓶颈。
```
avg Query Duration = avg Get Token + avg Parse Duration + avg Comiple Duration + avg Execute Duration
```

通常 execute 会占 query 延迟的主要部分，有两种情况 parser 和 compile 也会占比明显
- parser 延迟占比明显，比如 query 语句很长，文本解析消耗大量的 CPU。
- compile 延迟占比明显，如果应用没有用上 执行计划缓存，每个语句都需要生成执行计划。compile 的延迟达到几毫秒或者几十毫秒。compile 过程是 CPU 和  内存密集的操作，如果 OLTP 应用无法使用，tidb 的 runtime、gc 的压力可能很大。进一步影响执行器的性能。*OLTP 负载在 TIDB 中是否能高效的运行，执行计划缓存在扮演了重要的角色*。

##### 例子 1 数据库瓶颈在 compile 阶段
下图中平均的 parse、compile 和 execute 分别为 17.1us、729us 和 681us。因为应用使用 query 命令接口，无法使用执行计划缓存，所以 compile 延迟高。
![Compile](/media/performance/performance-overview/long_compile.png)

##### 例子 2 数据库瓶颈在 execute 阶段
下图 TPC-C 负载中，平均的 parse、compile 和 execute 分别为 7.39us、38.1us 和 12.8ms。query 延迟的瓶颈在于 execute 阶段。
![Execute](/media/performance/performance-overview/long_execute.png)

#### KV 和 TSO Request Duration
execute 阶段 TiDB 需要跟 PD 和 TiKV 进行交互，如下图所示，当 TiDB 处理 SQL 语句请求时，先进行 parse 和 compile 之前，如果需要获取 TSO，会先请求生成 TSO。PD Client 不会阻塞调用者，而是直接返回一个 `TSFuture`，并在后台异步处理 TSO 请求的收发，一旦完成立即返回给 TSFuture，TSFuture 的持有者则需要调用 Wait 来获得最终的 TSO 结果。当 TiDB 完成 parse 和 compile 之后， 进入 execute 阶段，此时存在两个情况：
- 如果 TSO 请求已经完成，Wait 会立刻返回一个可用的 TSO 或 error
- 如果 TSO 请求还未完成，Wait 会 block 住等待一个可用的 TSO 或 error（说明 gRPC 请求在途，网络延迟较高）
TSO 等待的时间 记录为 TSO WAIT，TSO 请求的网络时间记录为 TSO RPC。

TiDB TSO 等待完成之后，执行过程中通常需要和 TiKV 进行读写交互
- 读的 KV 请求常见类型：Get、BatchGet 和 Cop
- 写的 KV 请求常见类型：PessimisticLock，二阶段提交的 Prewrite 和 Commit

![Execute](/media/performance/performance-overview/execute_phase.png)

这一部分包含三个面板：
- Avg TiDB KV Request Duration 面板记录了 TiDB 测量的 KV 请求的平均延迟
- Avg TiKV GRPC Duration 面板记录 TiKV 内部 GRPC 消息处理的平均延迟
- PD TSO Wait/RPC Duration 记录了 TiDB 执行器等待 TSO 延迟(wait) 和 TSO 请求的网络延迟(rpc)。
Avg TiDB KV Request Duration 和 Avg TiKV GRPC Duration 的关系如下
```
Avg TiDB KV Request Duration = Avg TiKV GRPC Duration + TiDB 和 TiKV 的网络延迟 + TiKV GRPC 处理时间和 + TiDB GRPC 和处理时间和调度延迟。
```
Avg TiDB KV Request Duration 和 Avg TiKV GRPC Duration 的差值跟网络流量和延迟，TiDB 和 TiKV 的资源使用情况密切相关。
- 同一个机房内，Avg TiDB KV Request Duration 和 Avg TiKV GRPC Duration 的差值通常应该小于 2 毫秒
- 同一地区的不同可用区，Avg TiDB KV Request Duration 和 Avg TiKV GRPC Duration 的差值通常应该小于 5 毫秒

##### 例子 1 同机器低负载的集群
如下图所示，TiDB 侧平均 Prewrite 请求延迟 925us，TiKV 内部 kv_prewrite 平均处理延迟 720us，相差 200us 左右，是同机房内正常的延迟。TSO wait 平均延迟 206us，rpc 时间为 144us。
![Same Data Center](/media/performance/performance-overview/oltp_kv_tso.png)

##### 例子 2 公有云集群，负载正常的例子
下图的 TiDB 集群部署在同一个地区的不同机房，TiDB 侧平均 Commit 请求延迟 12.7ms，TiKV 内部 kv_commit 平均处理延迟 10.2ms，相差 2.5ms 左右。TSO wait 平均延迟为 3.12ms，rpc 时间为 693us。
![Cloud Env ](/media/performance/performance-overview/cloud_kv_tso.png)

##### 例子 3 公有云集群，资源严重过载例子
下图的 TiDB 集群部署在同一个地区的不同机房，TiDB 网络和 CPU 资源严重过载。TiDB 侧平均 BatchGet 请求延迟 38.6 ms，TiKV 内部 kv_batch_get 平均处理延迟 6.15ms，相差超过 32 ms，远高于正常值。TSO wait 平均延迟为 9.45ms，rpc 时间为 14.3ms。
![Cloud Env, TiDB Overloaded](/media/performance/performance-overview/cloud_kv_tso_overloaded.png)

#### Storage Async Write Duration、Store Duration 和 Apply Duration

TiKV 对于写请求的处理流程如下图
- `scheduler worker` 首先会处理写请求，进行事务一致性检查，并把写请求转化成键值对，发送到 `raftstore` 模块。
- `raftstore` 为 TiKV 的 共识模块，使用 Raft 共识算法，使多个 TiKV 组成的存储层可以容错。Raftstore 分为两种线程：
  *  store 线程和 apply 线程。store 线程负载处理 Raft 消息和新的 `proposals`。 当收到新的 `proposals` 时，leader 节点的 store 线程会写入本地 Raft db，并将消息复制到多个 follower 节点。当这个 `proposals` 在多数实例持久化成功之后，`proposals` 成功的被提交。
  * apply 线程会负载将提交的内容写入到 KV DB 中。当写操作的内容被成功的写入到 kv 数据库中，apply 线程会通知外层请求写请求已经完成。

![TiKV Write](/media/performance/performance-overview/store_apply.png)

Storage Async Write Duration 指标记录写请求进入 raftstore 之后的延迟，采集的粒度是具体是针对每个请求的级别。Storage Async Write Duration 分为 Store Duration 和 Apply Duration。
可以通过以下公式定位写请求的瓶颈主要是 Store 还是 Apply 步骤。
```
avg Storage Async Write Duration  = avg Store Duration + avg Apply Duration
```

##### 例子 1  同一个 OLTP 负载在 v5.3.0 和 v5.4.0 版本的对比
v5.4.0 版本，一个写密集的 OLTP 负载 QPS 比 v5.3.0 提升了 14%。应用以上公式
- v5.3.0: 24.4ms ~= 17.7ms + 6.59ms
- v5.4.0: 21.4ms ~= 14.0ms + 7.33ms

因为 v5.4.0 版本中, TiKV 对 gRPC 模块进行了优化，优化了 Raft 日志复制速度， 相比 v5.3.0 降低了 Store Duration。
v5.3.0
![v5.3.0](/media/performance/performance-overview/v5.3.0_store_apply.png)
v5.4.0
![v5.4.0](/media/performance/performance-overview/v5.4.0_store_apply.png)

##### 例子 2 Store Duration 瓶颈明显的例子
应用以上公式: 10.1ms ~= 9.81ms + 0.304，写请求的延迟瓶颈在 Store Duration。
![Store](/media/performance/performance-overview/cloud_store_apply.png)

#### Commit Log Duration、Append Log Duration 和 Apply Log Duration
Commit Log Duration、Append Log Duration 和 Apply Log Duration 三这个延迟是 raftstore 内部关键操作的延迟记录，采集的粒度是 batch 操作，每个操作会把多个写请求合并在一起，不能直接和上文的 store duration 和 apply duration 直接对应起来。
Commit Log Duration 和 Append Log Duration 为 store  线程的操作; Commit Log Duration 包含复制 Raft 日志到其他 TiKV 节点，保证 raft-log 的持久化，Commit Log Duration 一般包含两次 Append Log Duration, 一次 leader，一次 follower 的。Commit Log Duration 延迟通常会明显高于 Append Log Duration，因为包含了通过网络复制 Raft 日志到其他 tikv 的时间。 Apply Log Duration  记录了 apply 线程 Apply Raft 日志 的延迟。

Commit Log Duration 慢的常见场景：
- TiKV CPU 资源存在瓶颈，调度延迟高
- `raftstore.store-pool-sizS` 设置过小或者过大（是的，过大也可能导致性能下降）
- IO 延迟高，导致 Append Log Duration 延迟高
- TiKV 之间的网络延迟比较高
- TiKV 的 gRPC 线程数设置过小或者多个 gRPC CPU 资源使用不均衡

Apply Log Duration 慢的常见场景：
- TiKV CPU 资源存在瓶颈，调度延迟高
- `raftstore.apply-pool-size` 设置过小或者过大（是的，过大也可能导致性能下降）
- IO 延迟比较高

##### 例子 1  同一个 OLTP 负载在 v5.3.0 和 v5.4.0 版本的对比
v5.4.0 版本，一个写密集的 OLTP 负载 QPS 比 v5.3.0 提升了 14%。 对比这三个关键延迟：
| Avg Duration   | v5.3.0(ms)   |    v5.4.0(ms)  |
|:----------|:----------|:----------|
| Append Log Duration  | 0.27 | 0.303|
| Commit Log Duration  | 13   | 8.68 |
| Apply Log Duration   | 0.457|0.514  |

因为 v5.4.0 版本中, TiKV 对 gRPC 模块进行了优化，优化了 Raft 日志复制速度， 相比 v5.3.0 降低了 Store Duration。
v5.3.0
![v5.3.0](/media/performance/performance-overview/v5.3.0_commit_append_apply.png)
v5.4.0
![v5.4.0](/media/performance/performance-overview/v5.4.0_commit_append_apply.png)

##### 例子 2 Store Duration 瓶颈明显的例子

 如下图：
 - 平均 Append Log Duration = 4.38ms
 - 平均 Commit Log Duration = 7.92ms
 - 平均 Apply Log Duration = 172us。

Store 线程的 Commit Log Duration 明显比 Apply Log Duration 高，并且 Append Log Duration 比 Apply Log Duration 明显的高，说明 Store 线程在 CPU 和 IO 都可能都存在瓶颈。可能降低 Commit Log Duration 和 Append Log Duration 的方式如下：
- 如果 TiKV CPU 资源充足，考虑增加 Store 线程，`raftstore.store-pool-size`
- 版本 >= v5.4.0，考虑启用 [`Raft Engine`](https://docs.pingcap.com/zh/tidb/stable/tikv-configuration-file#raft-engine), Raft Engine 具有更轻量的执行路径，在一些场景下显著减少 IO 写入量和 写入请求的尾延迟，请启用方式：`raft-engine.enable: true`
- 如果 TiKV CPU 资源充足，版本 >= v5.3.0，考虑启用 [`StoreWriter`](https://docs.pingcap.com/zh/tidb/stable/tune-tikv-thread-performance#tikv-%E7%BA%BF%E7%A8%8B%E6%B1%A0%E8%B0%83%E4%BC%98)，启用方式：`raftstore.store-io-pool-size: 1`

![Store](/media/performance/performance-overview/cloud_append_commit_apply.png)

## 总结
本文介绍了用户响应时间和数据库时间的概念， 以及基于数据库时间进行系统优化的方法论。借助 TiDB Performance Overview 面板，TiDB 用户可以进行高效性能分析，确认用户响应时间的瓶颈是否在数据库中；如果数据库是整个系统的瓶颈，通过数据库时间概览和 SQL 延迟的分解， 定位数据库内部的瓶颈点，并进行针对性的优化。

## 老版本如何使用 Performance overview 面板
Performance Overview 面板在 >= v6.0.0 版本内置。发版 <= v5.4.0 的集群，需要手工导入 [`performance_overview.json`](https://github.com/pingcap/tidb/blob/master/metrics/grafana/performance_overview.json)

导入方法如图所示：
![Store](/media/performance/performance-overview/import_dashboard.png)
