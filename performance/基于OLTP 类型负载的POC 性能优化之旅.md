### 一、POC 背景介绍
某银行的核心系统是跑在 Oracle 上的，应用程序是 C 语言写的。驱动使用的是 Oracle 的 OCI 驱动。为了适配 TiDB，客户挑选了核心系统中比较典型的交易转账交易进行改写。
转账交易，涉及业务 sql 365 个，其中 89.5% 都是 select 语句，是个典型的 read heavy 的场景。交易涉及的表有 80 张，point get 读的表有 37 张，非 point get 读的表有31张。
隔离级别是 RC

### 二、客户现场负载分析

*交易在 TiDB  上端到端延迟 1 并发 1.2s;200 并发 1.57s*

看到这组数据是否惊讶为什么 TiDB 这么慢？慢在了哪里？我们先来温习下 TiDB 延迟的组成，再来一起分析监控

```math
Query Duration ~= Parse Duration + Comiple Duration + Execute Duration
```

```math
Execute Duration ~= TiDB Executor Duration + KV Request Duration + PD TSO Wait Duration 
```
```math
Storage Async Write Duration = Store duration + Apply Duration
```
以上公式适用于 cps by command 只有 1 种的情况，如果出现多个 command 类型，会出现 exectue duaration 比 query duration 还要高的场景，详情会在下文中有相关介绍。

客户现场的监控：
![](/media/performance/3.jpeg)
从图上我们可以发现几点问题
> * 无法命中 plan cache
> * cps by type 有 stmtprepare、stmtexecute、stmtfetch、stmtclose 4种 commands

分析：
1. 无法命中 plan cache 会导致每次执行 sql 都需要重新 compile,延迟在这里就会有一定的损耗。我们也可以看到上图中 Database Time Overview 中看到，的确 compile 的总耗时的确占比比较大，甚至都比 execute 的时间还长。
2. cps by type 有 4 种 command，且接近于 QPS，说明每次执行 sql 的时候都会经过这 4 个 commands,每个 command 就是一次网络往返，我们看到客户现场是有 4 个，就说明往返往返的次数是4次，网络往返延迟 * 4。除此之外客户也有触发 stmtclose，了解到客户在 execute 后会调用 close 来防止内存泄漏。除了客户之外，其实还有很多的应用框架也会这么调用，这样的使用方式在 TiDB 上就会带来无法命中 plan cache 和多次网络往返的问题。

当前可优化的方向很明确
1. 即使调用 close 也能命中缓存
2. 减少 command 次数降低网络往返的延迟

优化能带来多少的收益呢，我们将在内部模拟客户使用的转账交易，来确认优化能带来多少的性能提升。

### 三、live demo 动态展示性能变化及优化分析

为了让每个人都能理解 cps by type 种 command 次数和 plan cache 会带来多少性能上的变化，下面将使用 benchbot 的 playground 基于内部模拟的负载逐步展示每个使用场景之间的差异


#### 场景一：No prepare & No plan cache
```bash
python3 main.py gen-benchbot-case --email "example@pingcap.com" --token 'tcmsp_xxxxx' --testbed_size "2xl" \
--arch arm64 --resource_pool arm64 \
--bench_type hzbank --bench_sub_types "hzbank" \
--duration=10000m --threads 2 \
--versions nightly \
--tidb_configs "{new_collations_enabled_on_first_bootstrap: false}" \
--destroy_on_failure False \
--jdbc "?useServerPrepStmts=false"
```
*jdbc 连接串中的 useServerPrepStmts=false 表示没有使用 prepare 接口（其余均为负载所需参数配置）*

Dashbord TOPSQL 面板:
![](/media/performance/7.jpeg)

> * `SELECT @@session.tx_isolation` 非业务 sql 消耗 cpu 时间非常多,这些都是无用 sql,处理速度非常快，次数非常多

⚠️ [TOPSQL](https://docs.pingcap.com/tidb/stable/top-sql) 在 v6.0.0 开始使用，默认关闭。可在部署集群时打开，也可在部署完成后在 dashbord 中打开。TOPSQL 可查看 sql 的 cpu 消耗时间、执行计划及执行次数。
* * *

火焰图:
![](/media/performance/7.1.png)
> * ExecuteStmt cpu = 38% cpu time = 24.06s
> * Compile cpu = 27%  cpu time = 17.17s
> * Optimize cpu = 26% cpu time = 16.41s
* * *
⚠️ [Continuous Profiling](https://docs.pingcap.com/tidb/dev/continuous-profiling)

监控：
![](/media/performance/new/j-1.png)
> * Database Time by SQL Type 中 select 语句耗时最多
> * Database Time by SQL Phase 中 exectue 和 compile 占比最多
> * SQL Execute Time Overview 中 占比最多的分别是cop、get 和 tso wait
> * cps by type 只有 query 1 种 command
> * 无法命中 plan cache
> * execute 和 compile 的延迟在 tidb duration 中占比最高
> * avg QPS = 56.3k
* * *

![](/media/performance/5.png)

> * avg tidb cpu = 925%
* * *

![](/media/performance/6.png)
> * avg tidb duration = 479μs
> * avg parse duration = 37.2μs
> * avg compile duration = 166μs
> * avg execution duration = 251μs
> * connection idle duration avg-in-txn = 225μs

分析：
无用 sql 数量太大
建议：屏蔽这些大量无用的 sql

* * *

#### 场景二：No prepare & No plan cache & No useless sql
```bash
python3 main.py case-injection --token 'tcmsp_yjBpAK6esbssaUYjIPZE' --testbed benchbot-amd64-2xl-hzbank-edf1f69-tps-781088-1-698 --threads 2 --bench_type hzbank --bench_sub_types hzbank \
--jdbc "?useServerPrepStmts=false&useConfigs=maxPerformance"
```
*和场景一的 jdbc 连接串相比多一个参数 `useConfigs=maxPerformance`,这个参数是用来屏蔽 JDBC 向数据库发送的一些查询设置类的 SQL 语句（例如 `select @@session.transaction_read_only`）*

Dashbord分析：
![](/media/performance/10.png)
> *  从上图中我们可以看到原本占比最多的 `SELECT @@session.tx_isolation` 消失了
* * *

火焰图分析：
![](/media/performance/11.1.png)

> * ExecuteStmt cpu = 43% cpu time =35.63s 
> * Compile cpu = 31% cpu time =25.45s 
> * Optimize cpu = 30% cpu time = 24.64s 
* * *

监控分析：
![](/media/performance/new/j-2.png)
> * Database Time by SQL Type 中 select 语句耗时最多
> * Database Time by SQL Phase 中 exectue 和 compile 占比最多
> * SQL Execute Time Overview 中 占比最多的分别是cop、get 和 tso wait
> * execute 和 compile 的延迟在 tidb duration 中占比最高
> * cps by type 仍然只有 query 1 种 command
> * avg QPS = 24.2k (56.3k->24.2k))
> * 无法命中 plan cache
* * *

![](/media/performance/9.1.1.png)
> * tidb cpu = 874% (925%->874%)
* * *

![](/media/performance/9.2.2.png)
![](/media/performance/new/j-2-pd.png)
> * avg tidb duration = 1.12ms (479μs->1.12ms)
> * avg parse duration = 84.7μs (37.2μs->84.7μs)
> * avg compile duration = 370μs (166μs->370μs)
> * avg execution duration = 626μs (251μs->626μs)
> * connection idle duration avg-in-txn = 540μs (225μs->540μs)

分析：和场景一相比，QPS 下降明显，这是因为屏蔽了大量像 `select @@session.transaction_read_only`类型的无用 sql，这种类型的 sql 次数非常多并且处理时间非常快，屏蔽后所以 QPS 才会下降；tidb duration 上升一部分是因为原有的这些 sql 处理速度非常快从而拉低了平均值，屏蔽后只剩下纯业务 sql 所以 tidb duration 平均值上升；另一部分是因为 屏蔽这些速度很快的 sql 导致 connection idle duration avg-in-txn 时间变长（avg-in-txn 指的应用连接提交 sql 语句到 TiDB 的间隔时间，由于原先无用 sql 处理时间很快，所以提交 sql 间隔会很短，现在只剩纯业务 sql 所以 avg-in-txn 时间变长）。综上，所以是看起来“慢”了。
connect

建议：使用 prepare 预编译接口且能命中 plan cache 来降低 compile 带来的延迟消耗
* * *

#### 场景三：3 commands & no plan cache 
```bash
python3 main.py case-injection --token 'tcmsp_yjBpAK6esbssaUYjIPZE' --testbed benchbot-amd64-2xl-hzbank-8525365-tps-751355-1-117 --threads 2 --bench_type hzbank --bench_sub_types hzbank \
--jdbc "?useServerPrepStmts=true&useConfigs=maxPerformance"
```
*和场景二对比，jdbc 串不同的是 `useServerPrepStmts=true`,表示启用了预编译语句的接口*
Dashbord 分析：
![](/media/performance/13.png)
> * 没有无用 sql
* * *

火焰图分析：
![](/media/performance/3.1.1.png)
> * ExecutePreparedStmt cpu = 29%  cpu time = 22.47s 
> * preparedStmtExec cpu = 29% cpu time = 22.31s 
> * CompileExecutePreparedStmt cpu = 23% cpu time = 17.96s 
> * Optimize cpu = 23%  cpu time = 17.55s 
* * *

监控分析：
![](/media/performance/new/j-3.png)
> * Database Time by SQL Type 中 select 语句耗时最多
> * Database Time by SQL Phase 中 exectue 和 compile 占比最多
> * SQL Execute Time Overview 中 占比最多的分别是cop、get 和 tso wait
> * cps by type 变成 3 种 command:stmtprepare、stmtexecute、smtmclose
> * avg QPS = 19.7k (24.4k->19.7k)
> * 无法命中 plan cache
> * database time overview 出现了 general time
> * connection idle duration avg-in-txn = 250μs (540μs->250μs)
* * *
![](/media/performance/3-2.png)

> * avg tidb cpu = 936%（874%->936%）
* * *
![](/media/performance/3.4.png)
![](/media/performance/new/j-3-pd.png)
> * avg tidb duration = 528μs (1.12ms->528μs)
> * avg parse duration = 14.8μs (84.7μs->14.8μs)
> * avg compile duration = 374μs (370μs->374μs)
> * avg execution duration = 649μs (626μs->649μs)
> * connection idle duration avg-in-txn = 260μs (540μs->260μs)
> * avg pd tso wait = 121μs (103us->121us)

分析：
和场景二不同的是场景三启用了 prepare 预编译接口但是又无法命中缓存所以我们可以看到 cps by type 多 3 种 command 类型：stmtprepare、stmtexecute、smtmclose，这个与前文中客户现场使用场景几乎相近，是多了 3 种 command 就会多三次网络往返的延迟，stmtprepare 和 stmtclose 我们称之为非常规类型 command，这些不会统计在tidb duration 中，会统一统计在 general 中，所以我们可以看到 database over view 中多了 general 的时间，且占比在 database time 的 ¼ 之多
1. tidb duration 降低一部分的原因来自于启用预编译接口后 parse duration 降低的部分；一部分来自于 connection idle duration avg-in-txn 降低(事务中发送 sql 的间隔变短,原因是 stmtprapare 和 stmtclose 处理速度很快，所以avg-in-txn 平均值被拉低)；
2. QPS 的降低是因为 从 1 command -> 3 commands 后多了3次网络往返，且 QPS 只会统计 stmtexecute 和 query 这种常规类型 command，而 stmtprepare 和 stmtclose 非常规类型 command 不会统计在列，所以我们看到的 QPS 是“降低”了

建议：虽然场景三使用了 prepare 预编译接口但是因为出现了 stmtclose 导致缓存失效，上文也提到过除了客户很多应用框架也会在 execute 后调用 close 方法来防止内存，为了让客户在 TiDB 上有更好的体验，在 v6.0.0后，通过参数设置可以让客户即使调用 close 方法也能命中缓存。

#### 场景四：3 commands &  plan cache
```bash
python3 main.py case-injection --token 'tcmsp_yjBpAK6esbssaUYjIPZE' --testbed benchbot-amd64-2xl-hzbank-8525365-tps-751355-1-117 --threads 2 --bench_type hzbank --bench_sub_types hzbank \
--tidb_globals  "set global tidb_ignore_prepared_cache_close_stmt=on;" \
--tidb_configs "{prepared-plan-cache: {enabled: true}}" \
--jdbc "?useServerPrepStmts=true&useConfigs=maxPerformance" 
```
*jdbc 连接串和场景三一致，在这里新增了 tidb_globals: `set global tidb_ignore_prepared_cache_close_stmt=on;`是解决了即使客户触发 stmtclose 而无法命中缓存(v6.0.0 起正式使用，默认关闭)；tidb configs: `prepared-plan-cache: {enabled: true}`打开 plan cache 功能*

Dashbord 分析：
![](/media/performance/new/j-3.png)

> * 没有无用 sql
* * *

火焰图分析：
![](/media/performance/4.2.png)
> * PrepareStmt cpu = 25% cpu time = 12.75s 
> * PrepareExec cpu = 24% cpu time = 12.58s

* * *
监控分析：
![](/media/performance/new/j-4.png)
> * Database Time by SQL Type 中 select 语句耗时最多
> * Database Time by SQL Phase 中 exectue 和 compile 占比最多
> * SQL Execute Time Overview 中 占比最多的分别是 tso wait、cop 和 get 
> * 命中 plan cache
> * cps by type 仍然是 3 种 command
> * general time 相比场景三变长
> * avg QPS = 22.1k (19.7k->22.1k)
* * *

![](/media/performance/4.4.png)

> * avg tidb cpu = 827%（936%->827%）
* * *

![](/media/performance/4.5.png)
![](/media/performance/new/j-4-pd.png)
> * avg tidb duration = 426μs (528μs->426μs)
> * avg parse duration = 12.3μs (14.8μs->12.3μs)
> * avg compile duration = 53.3μs (374μs->53.3μs)
> * avg execution duration = 699μs (649μs->699us)
> * connection idle duration avg-in-txn = 261μs (250μs->261μs)
> * avg pd tso wait = 224μs (121us->224μs)

分析：
和场景三相比同样也是 cps by type 多了 3 种 command，不同的是场景四可以命中 plan cache 所以 compile duration 被大大降低 -> tidb duration 降低 -> QPS 上升

建议：从SQL Execute Time Overview 中 可以看到占比最大的部分变成了 tso wait,除了 QPS 上升会带来 tso cmd 上升之外，我们可以看到 pd tso wait 几乎也是翻倍。所以当下可以优化部分是
1. 减少 cps by type command 次数
2. 降低 tso cmd 次数或者降低 pd tso wait duration

* * *

#### 场景五：1 commands &  plan cache
```python
python3 main.py case-injection --token 'tcmsp_yjBpAK6esbssaUYjIPZE' --testbed benchbot-amd64-2xl-hzbank-8525365-tps-751355-1-117 --threads 2 --bench_type hzbank --bench_sub_types hzbank \
--jdbc "?useServerPrepStmts=true&cachePrepStmts=true&prepStmtCacheSize=1000&prepStmtCacheSqlLimit=2048&useConfigs=maxPerformance"
```
*jdbc 连接串和场景四相比，多了`prepStmtCacheSize=1000&prepStmtCacheSqlLimit=2048`，场景四的 jdbc 连接串中只有useServerPrepStmts=true 单独使用这个参数不会生效，须同时具备：*
1. cachePrepStmts = true
2. prepStmtCacheSize > 0
3. prepStmtCacheSqlLimit > sql.length()

Dashbord ：
![](/media/performance/5.2.png)
> * 没有无用 sql
* * *

火焰图：
![](/media/performance/5.1.1.png)
> * ExecutePreparedStmt cpu = 22% cpu time = 8.4s
> * preparedStmtExe cpu = 21% cpu time = 8.22s
> * preparedStmtExe cpu= 8.2% cpu time = 3.14s
* * *

监控：
![](/media/performance/new/j-5.png)
> * Database Time by SQL Type 中 select 语句耗时最多
> * Database Time by SQL Phase 中 exectue 和 compile 占比最多
> * SQL Execute Time Overview 中 占比最多的分别是 tso wait、cop 和 get 
> * 命中 plan cache
> * cps by type 只有 1种 command
> * general time 消失
> * avg QPS = 30.9k (22.1k->30.9k)
* * *

![](/media/performance/new/j-5-cpu.png)
> * avg tidb cpu = 577% (827%->577%)

![](/media/performance/new/j-5-duration.png)
> * avg tidb duration = 690μs (426->690μs)
> * avg parse duration = 13.5μs (12.3μs->13.5μs )
> * avg compile duration = 49.7μs (53.3μs->49.7μs)
> * avg execution duration = 623μs (699us->623μs)
> * avg pd tso wait duration = 196μs (224μs->196μs)
> * connection idle duration avg-in-txn = 608μs (250μs->608μs)

分析：
1. 和场景四相比，场景5的 cps by type 只有一种 command stmtexecute，减少了2次的网络往返 -> QPS 上升 
2. 从 parse duration、compile duration、execution durationy 以及 pd tso wait duration 来看延迟是降低的，为什么 tidb duration 反而上升的呢？我们看下 connection idle duration 的 avg-in-txn 是变长很多，原因是stmtprepare 和 stmtclose 处理的速度非常快，消除这2个 command 类型后，sql 发送间隔的平均值就被拉高很多，所以导致 tidb duration 上升
3. Database Time by SQL Phase 中 exectue 占比非常高接近于 database time，同时SQL Execute Time Overview 中占比最多的是 tso wait，这2者有什么关系呢？前文的公式也有提到过，在只有 1 种 command 的情况下 Execute Duration ~= TiDB Executor Duration + KV Request Duration + PD TSO Wait Duration 是可以成立的，也就是说 execute duration 中 包含了 tso wait，tso wait duration 越高 execute duration 也就是越大。
   ```math
   tso wait = tso cmd * pd tso wait duration
   ```
   pd tso wait duration 我们可以看到 是 196μs，5 个场景中，这个值不算高，可以来看下 tso cmd 次数
   ![](/media/performance/new/j-5-cmd.png)
   通过监控我们可以看到 tso cmd 的次数几乎接近 QPS，也就说几乎执行每条 sql 都会去 pd 获取 tso。在内部我们测试相同负载分别使用 RR 隔离别和 RC 隔离级别结果发现 RR 隔离级别端到端延迟比 RC 要快了22%左右，其中差距最大的就是在 tso wait，pd tso wait duration 差不多，而 tso cmd 分别是 9.3k 和 175k,这个差距是无论你怎么减少pd tso wait duration 都无法改变的。所以如何减少在 RC 隔离级别下的 tso cmd 次数

建议：减少 tso cmd 次数，不要执行每一句 sql 都要去 pd 获取 start-ts 和 commit-ts，事务中的语句拿 start-ts 去读，后台并发从 pd 取 tso，如果读到大于 start-ts 的数据，直接使用 pd tso 重新读一遍就可以了。后续的 for update ts 使用 latest pd tso


#### 场景六：1 rc read &  plan cache
```python
python3 main.py case-injection --token 'tcmsp_yjBpAK6esbssaUYjIPZE' --testbed benchbot-amd64-2xl-hzbank-8525365-tps-751355-1-117 --threads 2 --bench_type hzbank --bench_sub_types hzbank \
--jdbc "?useServerPrepStmts=true&cachePrepStmts=true&prepStmtCacheSize=1000&prepStmtCacheSqlLimit=2048&useConfigs=maxPerformance" \
--tidb_globals "set global tidb_rc_read_check_ts=on;"
```
*和场景五不同的是加了 `--tidb_globals "set global tidb_rc_read_check_ts=on;"`，意思是事务中的语句拿 start-ts 去读，后台并发从 pd 取 tso，如果读到大于 start-ts 的数据，直接使用 pd  tso重新读一遍就可以了。后续的 for update ts使用 latest pd tso,从而降低 tso cmd 次数*

Dashbord：
![](/media/performance/6.1.png)
> * 没有无用 sql
*** 

火焰图：
![](/media/performance/6.2.2.png)
> * ExecutePreparedStmt cpu = 22% cpu time = 8.4s
> * preparedStmtExec cpu = 21% cpu time = 8.22s
> * CompileExecutePreparedStmt cpu = 8.2% cpu time = 3.14s
*** 
监控：
![](/media/performance/new/j-6.png)
> * Database Time by SQL Type 中 select 语句耗时最多
> * Database Time by SQL Phase 中 exectue 和 compile 占比最多
> * SQL Execute Time Overview 中 占比最多的分别是 get、cop 和 prewrite 
> * 命中 plan cache
> * cps by type 只有 1种 command
> * general time 消失
> * avg QPS = 34.9k (30.9k->34.9k)
> 
![](/media/performance/new/j-6-cmd.png)
> * tso cmd =2.7k (28.3k->2.7k)
* * *

![](/media/performance/new/j-6-cpu.png)
> * avg tidb cpu = 603% (577%->603%)
****

![](/media/performance/new/j-6-duration.png)
> * avg tidb duration = 533μs (690μs->533μs)
> * avg parse duration = 13.4μs (13.5μs->13.4μs )
> * avg compile duration = 50.3μs (49.7μs->50.3μs)
> * avg execution duration = 466μs (623μs->466μs)
> * avg pd tso wait duration = 171μs (196μs->171μs)
> * connection idle duration avg-in-txn = 614μs (608μs->614μs)

分析：
加上 `--tidb_globals "set global tidb_rc_read_check_ts=on;"`后可以看到各个延迟其实都没有明显的降低，明显降低的就是 tso cmd 次数从而降低了 tso wait 以及 tidb duration，所以 QPS 上升。
建议：基于当前的监控能还能优化的地方是 avg-in-txn 大于 tidb duration 说明瓶颈不在 tidb 内部，而是在 tidb 外部 如负载均衡或应用。可以扩容负载均衡或者应用服务器。(live demo 中暂不支持在线扩容，故不展示)


#### 场景七：table cache & 1 command & plan cache
```python
python3 main.py case-injection --token 'tcmsp_yjBpAK6esbssaUYjIPZE' --testbed benchbot-amd64-2xl-hzbank-8525365-tps-751355-1-117 --threads 2 --bench_type hzbank --bench_sub_types hzbank \
--jdbc "?useServerPrepStmts=true&cachePrepStmts=true&prepStmtCacheSize=1000&prepStmtCacheSqlLimit=2048&useConfigs=maxPerformance" \
--tidb_globals "alter table t1 cache; ....alter table tn cache;"
```
*和场景六相比不同在场景六的基础上设置了`alter table t1 cache;`将所有只读表都进行了缓存
Dashbord：
![](/media/performance/7.1.1.png)

> * 没有无用 sql

火焰图：
![](/media/performance/7.2.png)
> * ExecutePreparedStmt cpu= 33% cpu time = 18.09s
> * preparedStmtExec cpu = 32% cpu time = 17.68s
> * CompileExecutePreparedStmt cpu = 12% cpu time = 6.65s
*** 

监控：
![](/media/performance/new/j-7.png)
> * Database Time by SQL Type 中 select 语句耗时最多
> * Database Time by SQL Phase 中 exectue 和 compile 占比最多
> * SQL Execute Time Overview 中 占比最多的分别是 prewrite、commit 和 get 
> * 命中 plan cache
> * cps by type 只有 1种 command
> * general time 消失
> * avg QPS = 40.9k (34.9k->40.9k)
*** 

![](/media/performance/new/j-7-cpu.png)
> * avg tidb cpu = 478%% (603%->478%)
***

![](/media/performance/new/j-7-duration.png)
> * avg tidb duration = 313μs (533μs->313μs)
> * avg parse duration = 12.0μs (13.4μs->12.0μs)
> * avg compile duration = 47.7μs (50.3μs->47.7μs)
> * avg execution duration = 250μs (466μs->250μs)
> * avg pd tso wait duration = 184μs (171μs->184μs)
> * connection idle duration avg-in-txn = 655μs (614μs->655μs)


分析：
将所有只读表进行缓存后，我们可以很看到 execute duration 下降非常明显原因是所有只读表都缓存在 tidb 中，不再需要到 tikv 来查询数据，所以 tidb duration 下降，QPS 上升。这个结果是比较乐观的结果，小表缓存对于写操作来说需要等3秒，对于对延迟要求比较高的应用，可能暂时不太友好。
***

通过下面表格我们具体来看下不同场景的性能表现如何
|   |   场景一 | 场景二   | 场景三 | 场景四 |场景五  | 场景六 | 场景七 | Diff 场景七 vs 场景一 | Diff 场景七 vs 场景三｜
| --- | --- | --- | --- | --- | --- | --- | --- | --- |  --- |
| tidb duration  | 479μs | 1120μs | 528μs | 426μs |690μs  | 533μs | 313μs | -34.66% | -50.95%
| QPS | 56.3k  |  24.2k  | 19.7k  | 22.1k | 30.9k | 34.9k | 40.9k  | -27.35% | +107.61% |

场景三是接近客户现场使用场景，我们可以看到通过减少 command 次数、命中缓存、rc read、小表缓存延迟可以减少50.95% 同时 QPS 提升 107.61%(乐观结果。对于使用场景不同负载不同，收益不同)














