---
title: OLTP 负载性能优化之旅
---

# OLTP 负载性能优化之旅

## 文本目的
TiDB 提供完善的性能分析和诊断功能。本文讲通过演示一个 OLTP 负载的优化过程，展示如何综合利用 TiDB Dashboard 和 Performance Overview Grafana 面板，进行性能分析和优化。本文会使用 5 种不同配置运行同一个应用，观察应用和数据库交互方式的不同，如何影响系统整体的性能。通过对比，读者可以了解应用程序使用 TiDB 的[最佳实践](https://docs.pingcap.com/zh/tidb/v6.0/java-app-best-practices)。

## 负载背景和介绍
文本使用一个银行交易系统 OLTP 仿真模拟负载进行演示。该负载使用 JAVA 程序开发，涉及业务 sql 365 个，其中 89.5% 都是 select 语句，是个典型的 read heavy OLTP 场景。交易涉及的表有 80 张，存在修改操作的表为 12 张，其余 68 张表只读。应用程序使用的隔离级别是 `read committed`。测试集群包含 3 TiDB 和 3 TiKV，每个 16 CPU。客户端服务器配置 36 CPU。

## 场景一：使用 Query 命令

### 应用配置
应用使用以下 jdbc 配置，使用 Query 接口连接数据库。
```
useServerPrepStmts=false
```
### 性能分析

#### Dashboard
从以下 Dashboard 的 TopSQL 页面可以观察到，`SELECT @@session.tx_isolation` 非业务 SQL 消耗最多, 虽然处理速度快，但是执行次数最多，总体 CPU 耗时最多。

![](/media/performance/7.jpeg)

观察以下 TiDB 的火焰图，可以发现，在 SQL 的执行过程中，Compile 和 Optimize 等函数的 CPU 消耗占比明显。因为应用使用了 Query 命令，无法使用执行计划缓存，每个 SQL 都需要编译生成执行计划。

- ExecuteStmt cpu = 38% cpu time = 24.06s
- Compile cpu = 27%  cpu time = 17.17s
- Optimize cpu = 26% cpu time = 16.41s

![](/media/performance/7.1.png)

> - [TOPSQL](https://docs.pingcap.com/tidb/stable/top-sql) 是在 v6.0.0 GA 功能，默认关闭。可在部署集群时打开，也可在部署完成后在 dashbord 中打开。TOPSQL 页面可查看 sql 实时和历史的 cpu 消耗时间、执行计划及执行次数。
>️ [Continuous Profiling](https://docs.pingcap.com/tidb/dev/continuous-profiling) 也是 v6.0.0 GA 的功能，在后台持续对 TiDB 集群生成火焰图，方便对系统进行实时和历史的性能分析。

#### Performance Overview 面板
观察以下 Performance Overview 面板中数据库时间概览和 QPS 的数据：
- Database Time by SQL Type 中 Select 语句耗时最多
- Database Time by SQL Phase 中 exectue 和 compile 占比最多
- SQL Execute Time Overview 中 占比最多的分别是 Get、Cop 和 tso wait
- CPS By Type 只有 query 1 种 command
- Queries Using Plan Cache OPS 没有数据，说明无法命中执行计划缓存
- execute 和 compile 的延迟在 query duration 中占比最高
- avg QPS = 56.3k

![](/media/performance/new/j-1.png)

观察集群的资源消耗，平均 TiDB CPU 的利用率为 925%，平均 TiKV 利用率为 201%，平均 TiKV IO 吞吐为 18.7 MB/s。TiDB 的资源消耗明显更高。
![](/media/performance/5.png)

### 分析结论
需要屏蔽这些大量无用的非业务 SQL

* * *

## 场景二：使用 maxPerformance 配置

### 应用配置
场景一的 jdbc 连接串相比多一个参数 `useConfigs=maxPerformance`，这个参数是用来屏蔽 JDBC 向数据库发送的一些查询设置类的 SQL 语句（例如 `select @@session.transaction_read_only`，完整配置如下：
```
useServerPrepStmts=false&useConfigs=maxPerformance
```
### 性能分析

#### Dashboard
从 TopSQL 页面可以看到原本占比最多的 `SELECT @@session.tx_isolation` 消失了

![](/media/performance/10.png)

从 TiDB 火焰图中可以观察到 SQL语句执行中 Compile 和 Optimize 等函数 CPU 消耗占比高：
- ExecuteStmt cpu = 43% cpu time =35.63s 
- Compile cpu = 31% cpu time =25.45s 
- Optimize cpu = 30% cpu time = 24.64s 

![](/media/performance/11.1.png)

#### Performance Overview 面板
数据库时间概览和 QPS 的数据如下：
- Database Time by SQL Type 中 select 语句耗时最多
- Database Time by SQL Phase 中 exectue 和 compile 占比最多
- SQL Execute Time Overview 中 占比最多的分别是 Get、Cop、Prewrite 和 tso_wait
- execute 和 compile 的延迟在 db time 中占比最高
- CPS By Type 只有 query 1 种 command
- avg QPS = 24.2k (56.3k->24.2k))
- 无法命中 plan cache

![](/media/performance/new/j-2.png)

从场景一到场景二，TiDB  平均 CPU 利用率下降为 874%，TiKV 平均 CPU 上升为 250% 左右。
![](/media/performance/9.1.1.png)

关键延迟指标变化如下：
- avg query duration = 1.12ms (479μs->1.12ms)
- avg parse duration = 84.7μs (37.2μs->84.7μs)
- avg compile duration = 370μs (166μs->370μs)
- avg execution duration = 626μs (251μs->626μs)

![](/media/performance/9.2.2.png)


### 分析结论

和场景一相比，QPS 下降明显，这是因为屏蔽了大量像 `select @@session.transaction_read_only` 这类 sql，因为这类 SQL 执行次数非常多并且处理时间非常快，屏蔽后所以 QPS 才会下降；平均 query duration 和 parse、compile 以及 execute duration 明显 上升也是因为同样的原因，原有的这些 sql 处理速度非常快从而拉低了平均值，屏蔽后只剩下纯业务 sql，所以 duration 平均值上升。

目前应用使用 query 命令，无法使用执行计划缓存，编译执行计划消耗高，建议使用 Prepared Statement 预编译接口，利用 TiDB 的执行计划缓存来降低 compile 带来 TiDB CPU 消耗，降低延迟。

## 场景三：应用使用 Prepared Statement 接口

### 应用配置
应用使用以下连接配置，和场景二对比，jdbc 串不同的是 `useServerPrepStmts=true`,表示启用了预编译语句的接口
```
useServerPrepStmts=true&useConfigs=maxPerformance"
```

### 性能分析

#### Dashboard

TiDB 火焰图如下， 启用 Prepared Statement 接口之后，CompileExecutePreparedStmt 和 Optimize 的 CPU 占比依然明显。

- ExecutePreparedStmt cpu = 29%  cpu time = 22.47s 
- preparedStmtExec cpu = 29% cpu time = 22.31s 
- CompileExecutePreparedStmt cpu = 23% cpu time = 17.96s 
- Optimize cpu = 23%  cpu time = 17.55s 

![](/media/performance/3.1.1.png)

#### Performance Overview 面板

数据库时间概览和 QPS 的数据如下，Prepared Statement 之后，QPS 从 24.4k 下降为 19.7k，从 CPS By Type 面板确认了应用确实使用了三种 Prepared 命令。Database Time Overview 出现了 general 的语句类型，占比排名第二, general 语句类型包含了 StmtPrepare 和 StmtClose 等命令的执行耗时。即使使用了 Prepared Statement 接口，执行计划缓存也没有命中，原因在于 TiDB 内部处理 StmtClose 命令时，会清理改语句的执行计划缓存。
- Database Time by SQL Type 中 select 语句耗时最多，general 语句类型占比命令第二
- Database Time by SQL Phase 中 exectue 和 compile 占比最多
- SQL Execute Time Overview 中 占比最多的分别是 Get、Cop、Prewrite 和 tso_wait
- CPS By Type 变成 3 种 command: StmtPrepare、StmtExecute、SmtmClose
- avg QPS = 19.7k (24.4k->19.7k)
- 无法命中 plan cache

![](/media/performance/new/j-3.png)

平均 TIDB CPU 利用率上升到 936%

![](/media/performance/3-2.png)


主要延迟数据如下：
- avg query duration = 528μs (1.12ms->528μs)
- avg parse duration = 14.8μs (84.7μs->14.8μs)
- avg compile duration = 374μs (370μs->374μs)
- avg execution duration = 649μs (626μs->649μs)

![](/media/performance/3.4.png)


### 分析结论
和场景二不同的是场景三启用了 prepare 预编译接口但是又无法命中缓存。所以我们可以看到 CPS By Type 多 3 种 command 类型：stmtprepare、stmtexecute、smtmclose，与使用 query 接口相比，相当于多了两次网络往返的延迟，stmtprepare 和 stmtclose 我们称之为非常规类型 command，会统一统计在 general sql 类型中，所以我们可以看到 database over view 中多了 general 的时间，且占比在 database time 的 ¼ 之多
1. QPS 的降低是因为 从 1 command 变成  3 commands，多了两次网络往返，且 QPS 只会统计 stmtexecute 和 query 这种常规类型 command，而 stmtprepare 和 stmtclose 非常规类型 command 不会统计在列，所以我们看到的 QPS 是“降低”了
2. 平均 query duration 明显降低原因在于，新增了 stmtprepare 和 smtmclose 命令，TiDB 内部处理时，query duration 也会单独计算， 这两类命令处理速度很快，所以平均 query duration 明显被*拉低*。

虽然场景三使用了 Prepare 预编译接口但是因为出现了 stmtclose 导致缓存失效，很多应用框架也会在 execute 后调用 close 方法来防止内存，为了让客户在 TiDB 上有更好的体验，从 v6.0.0 版本开始，通过全局变量 `tidb_ignore_prepared_cache_close_stmt` 的设置，可以应用即使调用 StmtClose 方法时，不清除缓存的执行计划，使得下一次的 SQL 执行能重用现有的执行计划，避免重复编译执行计划。

## 场景四：3 commands 和命中执行计划缓存

### 应用配置

应用配置不变，通过设置 TiDB 全局变量 `set global tidb_ignore_prepared_cache_close_stmt=on;` 解决了即使客户触发 stmtclose 而无法命中缓存(v6.0.0 起正式使用，默认关闭)；TiDB 配置: `prepared-plan-cache: {enabled: true}` 打开 plan cache 功能``

#### Dashbord

观察 TiDB 的 CPU 火焰图，对于场景四 TiDB 的火焰图，没有看到 CompileExecutePreparedStmt 和 Optimize 明显的 CPU 消耗。Prepare 命令的 CPU 占比 25%，包含了 PlanBuilder 和 parseSQL 等 Prepare 解析相关的函数。
- PreparseStmt cpu = 25% cpu time = 12.75s 

![](/media/performance/4.2.png)

#### Performance Overview 面板

最显著的变化来自于 Compile 阶段的占比，从场景三每秒消耗 8.95 秒降低为 1.18 秒。执行计划缓存的命中次数大致等于 StmtExecute 次数。QPS 上升的前提下每秒 Select 语句消耗的数据库时间降低了，general 类型的语句消耗时间边长。
- Database Time by SQL Type 中 select 语句耗时最多
- Database Time by SQL Phase 中 exectue 占比最多
- SQL Execute Time Overview 中 占比最多的分别是 tso wait、Get 和 Cop 
- 命中 plan cache，Queries Using Plan Cache OPS 大致等于 StmtExecute 每秒的次数
- CPS By Type 仍然是 3 种 command
- general time 相比场景三变长，因为 qps 上升了
- avg QPS = 22.1k (19.7k->22.1k)

![](/media/performance/new/j-4.png)

平均 TiDB CPU 利用率从 936% 下降为 827%
![](/media/performance/4.4.png)

平均 Compile 时间显著下降，从 374us 下降到 53.3us，因为 QPS 的上升，平均 execute 时间有锁上升。
- avg query duration = 426μs (528μs->426μs)
- avg parse duration = 12.3μs (14.8μs->12.3μs)
- avg compile duration = 53.3μs (374μs->53.3μs)
- avg execution duration = 699μs (649μs->699us)

![](/media/performance/4.5.png)


### 分析结论
和场景三相比同样存在 3 种 command，不同的是场景四可以命中执行计划缓存，所以 compile duration 被大大降低，query duration 也降低 了，并且 QPS 上升了。因为 StmtPrepare 和 StmtClose 两种命令消耗的数据库时间明显，并且增加了应用每执行一条 SQL 语句需要跟 TIDB 交互的次数，下一个场景，我们将通过 jdbc 配置，把这两种命令优化掉。

## 场景五：1 command 和 命中执行计划缓存

### 应用配置
jdbc 连接串和场景四相比，多了三个配置 `cachePrepStmts=true&prepStmtCacheSize=1000&prepStmtCacheSqlLimit=20480`，解释如下：
1. cachePrepStmts = true，在客户端缓存 prepared statement 对象，消除 StmtPrepare 和 StmtClose 调用
2. prepStmtCacheSize 需要配置大于 0
3. prepStmtCacheSqlLimit 大于 SQL 文本的长度

```
useServerPrepStmts=true&cachePrepStmts=true&prepStmtCacheSize=1000&prepStmtCacheSqlLimit=20480&useConfigs=maxPerformance
```

### 性能分析

#### Dashbord
TiDB 火焰图 中，Prepare 命令高 CPU 消耗没有再出现。

- ExecutePreparedStmt cpu = 22% cpu time = 8.4s

![](/media/performance/5.1.1.png)


#### Performance Overview 面板

最显著的变化来自于三种 command 变成一种，第一个图数据库时间按 SQL 语句类型分解中，general 语句类型消失了。QPS 上升到 30.9k。
- Database Time by SQL Type 中 select 语句耗时最多，general 语句类型消失了
- Database Time by SQL Phase 中 主要为 exectue
- SQL Execute Time Overview 中 占比最多的分别是 tso wait、Get 和 Cop
- 命中 plan cache，Queries Using Plan Cache OPS 大致等于 StmtExecute 每秒的次数
- CPS By Type 只有一种 command，stmtExecute
- avg QPS = 30.9k (22.1k->30.9k)

![](/media/performance/new/j-5.png)

平均 TiDB CPU 利用率从 827% 下降为 577%，随着 QPS 的上升，平均 TiKV CPU 利用率上升为 313%。
![](/media/performance/new/j-5-cpu.png)


关键的延迟指标如下：
- avg query duration = 690μs (426->690μs)
- avg parse duration = 13.5μs (12.3μs->13.5μs )
- avg compile duration = 49.7μs (53.3μs->49.7μs)
- avg execution duration = 623μs (699us->623μs)
- avg pd tso wait duration = 196μs (224μs->196μs)
- connection idle duration avg-in-txn = 608μs (250μs->608μs)

![](/media/performance/new/j-5-duration.png)

### 分析结论
1. 和场景四相比，场景五的 CPS By Type 只有一种 command stmtexecute，减少了2次的网络往返，系统总体 QPS 上升 
2. QPS 上升的情况下，从 parse duration、compile duration、execution durationy 来看延迟是降低的，为什么 query duration 反而上升的呢？原因是stmtprepare 和 stmtclose 处理的速度非常快，消除这两种 command 类型之后，query duration 上升
3. Database Time by SQL Phase 中 exectue 占比非常高接近于 database time，同时 SQL Execute Time Overview 中占比最多的是 tso wait，超过四分之一的 execute 时间是在等待 tso。
4. 每秒的 tso wait 总时间为 5.46s。平均 tso wait 时间为 196us，每秒的 tso cmd 次数为 28k，非常接近于 QPS 的 30.9k。因为在 TiDB 对于隔离级别 `read committed` 的实现中，事务中的每个 SQL 语句都需要都到 PD 请求 tso。

TiDB v6.0 提供了 `rc read`, 针对 `read committed` 隔离级别进行了减少 tso cmd 的优化。 该功能由全局变量控制 `set global tidb_rc_read_check_ts=on;`，启用之后，默认行为和 `repeatable-read` 隔离级别一致，只有 start-ts 和 commit-ts 跟 pd 获取，事务中的语句首先拿 start-ts 到 TiKV 进行数据读取，如果读到的数据小于 start-ts，则直接返回数据；如果读到大于 start-ts 的数据，则需要丢弃数据，先向 pd 请求 tso 再进行重试。后续语句的 for update ts 使用最新的 pd tso。


## 场景六：rc read

### 应用配置
应用配置不变，和场景五不同的是,数据库增加了 `set global tidb_rc_read_check_ts=on;` 减少 tso 请求。

### 性能分析

#### Dashbord
TiDB 的 CPU 火焰图没有明显变化
- ExecutePreparedStmt cpu = 22% cpu time = 8.4s

![](/media/performance/6.2.2.png)

#### Performance Overview 面板

使用 RC read 之后，QPS 从 30.9k 上升为 34.9k，每秒消耗的 tso wait 时间从 5.46s 下降为 456ms。
- Database Time by SQL Type 中 select 语句耗时最多
- Database Time by SQL Phase 中 exectue 占比最高
- SQL Execute Time Overview 中 占比最多的分别是 Get、Cop 和 Prewrite 
- 命中 plan cache，Queries Using Plan Cache OPS 大致等于 StmtExecute 每秒的次数
- CPS By Type 只有一种 command
- avg QPS = 34.9k (30.9k->34.9k)

![](/media/performance/new/j-6.png)


每秒 tso cmd 从 28.3k 下降为 2.7k
![](/media/performance/new/j-6-cmd.png)

平均 TiDB CPU 上升为 603% (577%->603%)
![](/media/performance/new/j-6-cpu.png)

关键延迟指标如下：
- avg query duration = 533μs (690μs->533μs)
- avg parse duration = 13.4μs (13.5μs->13.4μs )
- avg compile duration = 50.3μs (49.7μs->50.3μs)
- avg execution duration = 466μs (623μs->466μs)
- avg pd tso wait duration = 171μs (196μs->171μs)

![](/media/performance/new/j-6-duration.png)

### 分析结论
启用 RC Read 之后 `set global tidb_rc_read_check_ts=on;` 明显降低了 tso cmd 次数从而降低了 tso wait 以及 平均 query duration，以及 QPS 上升。

当前数据库时间和延迟瓶颈都在 execute 阶段，而 execute 阶段占比最高的为 Get 和 Cop 读请求。这个负载中，大部分表时只读或者很少修改，可以使用 v6.0.0 GA 的小表缓存功能，在 TiDB 缓存这些小表的数据，降低 kv 读请求的等待时间和资源消耗。

## 场景七：小表缓存

### 应用配置
应用配置不变，在场景六的基础上设置了对业务的只读表进行缓存 `alter table t1 cache;`


### 性能分析

#### Dashbord：

TiDB CPU 火焰图没有明显变化
![](/media/performance/7.2.png)

#### Performance Overview 面板

QPS 从 34.9k 上升到 40.9k，Execute 时间中占比最高的 kv 请求类型变成了 Prewrite 和 Commit。Get 每秒的时间从 5.33 秒下降为 1.75秒，Cop 每秒的时间从 3.87 下降为 1.09 秒

- Database Time by SQL Type 中 select 语句耗时最多
- Database Time by SQL Phase 中 exectue 和 compile 占比最多
- SQL Execute Time Overview 中 占比最多的分别是 Prewrite、Commit 和 Get 
- 命中 plan cache，Queries Using Plan Cache OPS 大致等于 StmtExecute 每秒的次数
- CPS By Type 只有 1种 command
- avg QPS = 40.9k (34.9k->40.9k)

![](/media/performance/new/j-7.png)


平均 TiDB CPU 利用率从 603% 下降 为 478%，平均 TiKV CPU 利用率从 346% 下降为 256%。

![](/media/performance/new/j-7-cpu.png)

 平均 Query 延迟从 533us 下降为 313us。平均 execute 延迟从 466us 下降为 250us。
- avg query duration = 313μs (533μs->313μs)
- avg parse duration = 12.0μs (13.4μs->12.0μs)
- avg compile duration = 47.7μs (50.3μs->47.7μs)
- avg execution duration = 250μs (466μs->250μs)

![](/media/performance/new/j-7-duration.png)


### 分析总结
将所有只读表进行缓存后，我们可以很看到 execute duration 下降非常明显，原因是所有只读表都缓存在 tidb 中，不再需要到 tikv 来查询数据，所以 query duration 下降，QPS 上升。
这个结果是比较乐观的结果，真的业务中可能只读表的数据量较大无法全部在 TiDB 中进行缓存，另一个限制是，当前小表缓存的 feature 虽然支持写操作，但是写操作默认需要等3秒，确保所有 TiDB 节点的缓存失效，对于对延迟要求比较高的应用，可能暂时不太友好。

## 总结

以下表格展示了七个不同场景的性能表现
|   |   场景一 | 场景二   | 场景三 | 场景四 |场景五  | 场景六 | 场景七 | Diff 场景五 vs 场景二(%) | Diff 场景七 vs 场景三(%)
| --- | --- | --- | --- | --- | --- | --- | --- | --- |  --- |
| uery duration  | 479μs | 1120μs | 528μs | 426μs |690μs  | 533μs | 313μs | -38% | -51%
| QPS | 56.3k  |  24.2k  | 19.7k  | 22.1k | 30.9k | 34.9k | 40.9k  | +28% | +108% |

场景二是应用使用 query 接口的常见场景，场景五是应用使用 Prepared Statement 接口的理想场景。
- 对比场景二和场景五，通过使用最佳的应用开发实践，通过客户端缓存 Prepared Statement 对象，每条 SQL 只需要一次命令和数据库交互，并且能命中执行计划缓存，Query 延迟下降了 38%，QPS 上升 28%，同时，TiDB CPU 利用率 从 936% 下降 577% 
- 对比场景二和场景七，在场景五的基础上使用了 rc read、小表缓存等 TiDB 最新的优化 feature，延迟可以减少51% 同时 QPS 提升 108%。同时，TiDB CPU 利用率 从 936% 下降 478%。

文本通过对同一个负载，七个不同的运行场景进行分析，读者展示了 JAVA 应用程序的[最佳实践](https://docs.pingcap.com/zh/tidb/v6.0/java-app-best-practices)， 虽然 TiDB 兼容 MySQL 协议的不同命令，最佳的性能表现来自于应用程序使用 Prepared Statement 接口，并设置以下 JDBC 连接参数:
```
useServerPrepStmts=true&cachePrepStmts=true&prepStmtCacheSize=1000&prepStmtCacheSqlLimit=20480&useConfigs=maxPerformance
```
同时，我们展示了 TiDB 的执行计划缓存对于 OLTP 发挥着至关重要的作用，同时，v6.0.0 GA 的 `RC Read` 和小表缓存，在本文的负载的深度优化中，发挥了重要的作用。









