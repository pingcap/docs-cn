---
title: 分析慢查询
summary: 学习如何定位和分析慢查询。
---

# 分析慢查询

处理慢查询分为两步：

1. 从大量查询中定位出哪一类查询比较慢
2. 分析这类慢查询的原因

第一步可以通过 [慢日志](/identify-slow-queries.md)、[statement-summary](/statement-summary-tables.md) 方便地定位，推荐直接使用 [TiDB Dashboard](/dashboard/dashboard-overview.md)，它整合了这两个功能，且能方便直观地在浏览器中展示出来。本文聚焦第二步。

首先将慢查询归因成两大类：

- 优化器问题：如选错索引，选错 Join 类型或顺序
- 系统性问题：将非优化器问题都归结于此类，如：某个 TiKV 实例忙导致处理请求慢，Region 信息过期导致查询变慢

实际中，优化器问题可能造成系统性问题，如对于某类查询，优化器应使用索引，但却使用了全表扫，这可能导致这类 SQL 消耗大量资源，造成某些 KV 实例 CPU 飚高等，表现上看就是一个系统性问题，但本质是优化器问题。

分析优化器问题需要有判断执行计划是否合理的能力，而系统性问题的定位相对简单，因此面对慢查询推荐的分析过程如下：

1. 定位查询瓶颈：即查询过程中耗时多的部分
2. 分析系统性问题：根据瓶颈点，结合当时的监控/日志等信息，分析可能的原因
3. 分析优化器问题：分析是否有更好的执行计划

接下来会分别介绍上面几点。

## 定位查询瓶颈

定位查询瓶颈需要对查询过程有一个大致理解，TiDB 处理查询过程的关键阶段都在 [performance-map](/media/performance-map.png) 图中了。

查询的耗时信息可以从下面几种方式获得：

- [慢日志](/identify-slow-queries.md)（推荐直接在 [TiDB Dashboard](/dashboard/dashboard-overview.md) 中查看）
- [`explain analyze` 语句](/sql-statements/sql-statement-explain-analyze.md)

他们的侧重点不同：

- 慢日志记录了 SQL 从解析到返回，几乎所有阶段的耗时，较为全面（在 TiDB Dashboard 中可以直观地查询和分析慢日志）；
- `explain analyze` 可以拿到 SQL 实际执行中每个执行算子的耗时，对执行耗时有更细分的统计；

总的来说，利用慢日志和 `explain analyze` 可以比较准确地定位查询的瓶颈点，帮助你判断这条 SQL 慢在哪个模块（TiDB/TiKV），慢在哪个阶段，下面会有一些例子。

另外在 4.0.3 之后，慢日志中的 `Plan` 字段也会包含 SQL 的执行信息，也就是 `explain analyze` 的结果，这样一来 SQL 的所有耗时信息都可以在慢日志中找到。

## 分析系统性问题

对于系统性问题，我们根据执行阶段，分成三个大类：

1. TiKV 处理慢：如 coprocessor 处理数据慢
2. TiDB 执行慢：主要指执行阶段，如某个 Join 算子处理数据慢
3. 其他关键阶段慢：如取时间戳慢

拿到一个慢查询，我们应该先根据已有信息判断大致是哪个大类，再具体分析。

### TiKV 处理慢

如果是 TiKV 处理慢，可以很明显的通过 `explain analyze` 中看出来，如下面这个例子，可以看到 `StreamAgg_8` 和 `TableFullScan_15` 这两个 `tikv-task` （在 `task` 列可以看出这两个任务类型是 `cop[tikv]`） 花费了 `170ms`，而 TiDB 部分的算子耗时，减去这 `170ms` 后，耗时占比非常小，说明瓶颈在 TiKV。

```sql
+----------------------------+---------+---------+-----------+---------------+------------------------------------------------------------------------------+---------------------------------+-----------+------+
| id                         | estRows | actRows | task      | access object | execution info                                                               | operator info                   | memory    | disk |
+----------------------------+---------+---------+-----------+---------------+------------------------------------------------------------------------------+---------------------------------+-----------+------+
| StreamAgg_16               | 1.00    | 1       | root      |               | time:170.08572ms, loops:2                                                     | funcs:count(Column#5)->Column#3 | 372 Bytes | N/A  |
| └─TableReader_17           | 1.00    | 1       | root      |               | time:170.080369ms, loops:2, rpc num: 1, rpc time:17.023347ms, proc keys:28672 | data:StreamAgg_8                | 202 Bytes | N/A  |
|   └─StreamAgg_8            | 1.00    | 1       | cop[tikv] |               | time:170ms, loops:29                                                          | funcs:count(1)->Column#5        | N/A       | N/A  |
|     └─TableFullScan_15     | 7.00    | 28672   | cop[tikv] | table:t       | time:170ms, loops:29                                                          | keep order:false, stats:pseudo  | N/A       | N/A  |
+----------------------------+---------+---------+-----------+---------------+------------------------------------------------------------------------------+---------------------------------+-----------+------
```

另外在慢日志中，`Cop_process` 和 `Cop_wait` 字段也可以帮助判断，如下面这个例子，查询整个耗时是 180.85ms 左右，而最大的那个 `coptask` 就消耗了 `171ms`，可以说明对这个查询而言，瓶颈在 TiKV 侧。

慢日志中的各个字段的说明可以参考慢查询日志中的[字段含义说明](/identify-slow-queries.md#字段含义说明)

```log
# Query_time: 0.18085
...
# Num_cop_tasks: 1
# Cop_process: Avg_time: 170ms P90_time: 170ms Max_time: 170ms Max_addr: 10.6.131.78
# Cop_wait: Avg_time: 1ms P90_time: 1ms Max_time: 1ms Max_Addr: 10.6.131.78
```

根据上述方式判断是 TiKV 慢后，可以依次排查 TiKV 慢的原因。

#### TiKV 实例忙

一条 SQL 可能会去从多个 TiKV 上拿数据，如果某个 TiKV 响应慢，可能拖慢整个 SQL 的处理速度。

慢日志中的 `Cop_wait` 可以帮忙判断这个问题：

```log
# Cop_wait: Avg_time: 1ms P90_time: 2ms Max_time: 110ms Max_Addr: 10.6.131.78
```

如上图，发给 `10.6.131.78` 的一个 `cop-task` 等待了 110ms 才被执行，可以判断是当时该实例忙，此时可以打开当时的 CPU 监控辅助判断。

#### 过期 key 多

如果 TiKV 上过期的数据比较多，在扫描的时候则需要处理这些不必要的数据，影响处理速度。

这可以通过 `Total_keys` 和 `Processed_keys` 判断，如果两者相差较大，则说明旧版本的 key 太多：

```
...
# Total_keys: 2215187529 Processed_keys: 1108056368
...
```

### 其他关键阶段慢

#### 取 TS 慢

可以对比慢日志中的 `Wait_TS` 和 `Query_time` ，因为 TS 有预取操作，通常来说 `Wait_TS` 应该很低。

```
# Query_time: 0.0300000
...
# Wait_TS: 0.02500000
```

#### Region 信息过期

TiDB 侧 Region 信息可能过期，此时 TiKV 可能返回 `regionMiss` 的错误，然后 TiDB 会从 PD 去重新获取 Region 信息，这些信息会被反应在 `Cop_backoff` 信息内，失败的次数和总耗时都会被记录下来。

```
# Cop_backoff_regionMiss_total_times: 200 Cop_backoff_regionMiss_total_time: 0.2 Cop_backoff_regionMiss_max_time: 0.2 Cop_backoff_regionMiss_max_addr: 127.0.0.1 Cop_backoff_regionMiss_avg_time: 0.2 Cop_backoff_regionMiss_p90_time: 0.2
# Cop_backoff_rpcPD_total_times: 200 Cop_backoff_rpcPD_total_time: 0.2 Cop_backoff_rpcPD_max_time: 0.2 Cop_backoff_rpcPD_max_addr: 127.0.0.1 Cop_backoff_rpcPD_avg_time: 0.2 Cop_backoff_rpcPD_p90_time: 0.2
```

#### 子查询被提前执行

对于带有非关联子查询的语句，子查询部分可能被提前执行，如：`select * from t1 where a = (select max(a) from t2)` ，`select max(a) from t2` 部分可能在优化阶段被提前执行，这种查询用 `explain analyze` 看不到对应的耗时，如下：

```sql
mysql> explain analyze select count(*) from t where a=(select max(t1.a) from t t1, t t2 where t1.a=t2.a);
+------------------------------+----------+---------+-----------+---------------+--------------------------+----------------------------------+-----------+------+
| id                           | estRows  | actRows | task      | access object | execution info           | operator info                    | memory    | disk |
+------------------------------+----------+---------+-----------+---------------+--------------------------+----------------------------------+-----------+------+
| StreamAgg_59                 | 1.00     | 1       | root      |               | time:4.69267ms, loops:2  | funcs:count(Column#10)->Column#8 | 372 Bytes | N/A  |
| └─TableReader_60             | 1.00     | 1       | root      |               | time:4.690428ms, loops:2 | data:StreamAgg_48                | 141 Bytes | N/A  |
|   └─StreamAgg_48             | 1.00     |         | cop[tikv] |               | time:0ns, loops:0        | funcs:count(1)->Column#10        | N/A       | N/A  |
|     └─Selection_58           | 16384.00 |         | cop[tikv] |               | time:0ns, loops:0        | eq(test.t.a, 1)                  | N/A       | N/A  |
|       └─TableFullScan_57     | 16384.00 | -1      | cop[tikv] | table:t       | time:0s, loops:0         | keep order:false                 | N/A       | N/A  |
+------------------------------+----------+---------+-----------+---------------+--------------------------+----------------------------------+-----------+------+
5 rows in set (7.77 sec)
```

不过可以从慢日志中排查这种情况：

```
# Query_time: 7.770634843
...
# Rewrite_time: 7.765673663 Preproc_subqueries: 1 Preproc_subqueries_time: 7.765231874
```

可以看到有 1 个子查询被提前执行，花费了 `7.76s`。

### TiDB 执行慢

这里我们假设 TiDB 的执行计划正确（不正确的情况在[分析优化器问题](#分析优化器问题)这一节中说明），但是执行上很慢；

解决这类问题主要靠调整参数或利用 hint，并结合 `explain analyze` 对 SQL 进行调整。

#### 并发太低

如果发现瓶颈在有并发的算子上，可以通过调整并发度来尝试提速，如下面的执行计划中：

```sql
mysql> explain analyze select sum(t1.a) from t t1, t t2 where t1.a=t2.a;
+----------------------------------+--------------+-----------+-----------+---------------+-------------------------------------------------------------------------------------+------------------------------------------------+------------------+---------+
| id                               | estRows      | actRows   | task      | access object | execution info                                                                      | operator info                                  | memory           | disk    |
+----------------------------------+--------------+-----------+-----------+---------------+-------------------------------------------------------------------------------------+------------------------------------------------+------------------+---------+
| HashAgg_11                       | 1.00         | 1         | root      |               | time:9.666832189s, loops:2, PartialConcurrency:4, FinalConcurrency:4                | funcs:sum(Column#6)->Column#5                  | 322.125 KB       | N/A     |
| └─Projection_24                  | 268435456.00 | 268435456 | root      |               | time:9.098644711s, loops:262145, Concurrency:4                                      | cast(test.t.a, decimal(65,0) BINARY)->Column#6 | 199 KB           | N/A     |
|   └─HashJoin_14                  | 268435456.00 | 268435456 | root      |               | time:6.616773501s, loops:262145, Concurrency:5, probe collision:0, build:881.404µs  | inner join, equal:[eq(test.t.a, test.t.a)]     | 131.75 KB        | 0 Bytes |
|     ├─TableReader_21(Build)      | 16384.00     | 16384     | root      |               | time:6.553717ms, loops:17                                                           | data:Selection_20                              | 33.6318359375 KB | N/A     |
|     │ └─Selection_20             | 16384.00     |           | cop[tikv] |               | time:0ns, loops:0                                                                   | not(isnull(test.t.a))                          | N/A              | N/A     |
|     │   └─TableFullScan_19       | 16384.00     | -1        | cop[tikv] | table:t2      | time:0s, loops:0                                                                    | keep order:false                               | N/A              | N/A     |
|     └─TableReader_18(Probe)      | 16384.00     | 16384     | root      |               | time:6.880923ms, loops:17                                                           | data:Selection_17                              | 33.6318359375 KB | N/A     |
|       └─Selection_17             | 16384.00     |           | cop[tikv] |               | time:0ns, loops:0                                                                   | not(isnull(test.t.a))                          | N/A              | N/A     |
|         └─TableFullScan_16       | 16384.00     | -1        | cop[tikv] | table:t1      | time:0s, loops:0                                                                    | keep order:false                               | N/A              | N/A     |
+----------------------------------+--------------+-----------+-----------+---------------+-------------------------------------------------------------------------------------+------------------------------------------------+------------------+---------+
9 rows in set (9.67 sec)
```

发现耗时主要在 `HashJoin_14` 和 `Projection_24`，可以酌情通过 SQL 变量来提高他们的并发度进行提速。

[system-variables](/system-variables.md) 中有所有的系统变量，如想提高 `HashJoin_14` 的并发度，则可以修改变量 `tidb_hash_join_concurrency`。

#### 产生了落盘

执行慢的另一个原因是执行过程中，因为到达内存限制，产生了落盘，这点在执行计划和慢日志中都能看到：

```sql
+-------------------------+-----------+---------+-----------+---------------+------------------------------+----------------------+-----------------------+----------------+
| id                      | estRows   | actRows | task      | access object | execution info               | operator info        | memory                | disk           |
+-------------------------+-----------+---------+-----------+---------------+------------------------------+----------------------+-----------------------+----------------+
| Sort_4                  | 462144.00 | 462144  | root      |               | time:2.02848898s, loops:453  | test.t.a             | 149.68795776367188 MB | 219.3203125 MB |
| └─TableReader_8         | 462144.00 | 462144  | root      |               | time:616.211272ms, loops:453 | data:TableFullScan_7 | 197.49601364135742 MB | N/A            |
|   └─TableFullScan_7     | 462144.00 | -1      | cop[tikv] | table:t       | time:0s, loops:0             | keep order:false     | N/A                   | N/A            |
+-------------------------+-----------+---------+-----------+---------------+------------------------------+----------------------+-----------------------+----------------+
```

```
...
# Disk_max: 229974016
...
```

#### 做了笛卡尔积的 Join

做笛卡尔积的 Join 会产生 `左边孩子行数 * 右边孩子行数` 这么多数据，效率较低，应该尽量避免；

目前对于产生笛卡尔积的 Join 会在执行计划中显示的标明 `CARTESIAN`，如下：

```sql
mysql> explain select * from t t1, t t2 where t1.a>t2.a;
+------------------------------+-------------+-----------+---------------+---------------------------------------------------------+
| id                           | estRows     | task      | access object | operator info                                           |
+------------------------------+-------------+-----------+---------------+---------------------------------------------------------+
| HashJoin_8                   | 99800100.00 | root      |               | CARTESIAN inner join, other cond:gt(test.t.a, test.t.a) |
| ├─TableReader_15(Build)      | 9990.00     | root      |               | data:Selection_14                                       |
| │ └─Selection_14             | 9990.00     | cop[tikv] |               | not(isnull(test.t.a))                                   |
| │   └─TableFullScan_13       | 10000.00    | cop[tikv] | table:t2      | keep order:false, stats:pseudo                          |
| └─TableReader_12(Probe)      | 9990.00     | root      |               | data:Selection_11                                       |
|   └─Selection_11             | 9990.00     | cop[tikv] |               | not(isnull(test.t.a))                                   |
|     └─TableFullScan_10       | 10000.00    | cop[tikv] | table:t1      | keep order:false, stats:pseudo                          |
+------------------------------+-------------+-----------+---------------+---------------------------------------------------------+
```

## 分析优化器问题

分析优化问题需要有判断执行计划是否合理的能力，这需要对优化过程和各算子有一定了解。

下面是一组例子，假设表结构为 `create table t (id int, a int, b int, c int, primary key(id), key(a), key(b, c))`：

1. `select * from t`: 没有过滤条件，会扫全表，所以会用 `TableFullScan` 算子读取数据；
2. `select a from t where a=2`：有过滤条件且只读索引列，所以会用 `IndexReader` 算子读取数据；
3. `select * from t where a=2`：在 `a` 有过滤条件，但索引 `a` 不能完全覆盖需要读取的内容，因此会采用 `IndexLookup`；
4. `select b from t where c=3`：多列索引没有前缀条件就用不上，所以会用 `IndexFullScan`；
5. ...

上面举例了数据读入相关的算子，在 [理解 TiDB 执行计划](/explain-overview.md) 中描述了更多算子的情况；

另外阅读 [SQL 性能调优](/sql-tuning-overview.md) 整个小节能增加你对 TiDB 优化器的了解，帮助判断执行计划是否合理。

由于大多数优化器问题在 [SQL 性能调优](/sql-tuning-overview.md) 已经有解释，这里就直接列举出来跳转过去：

1. [索引选择错误](/wrong-index-solution.md)
2. [Join 顺序错误](/join-reorder.md)
3. [表达式未下推](/blocklist-control-plan.md)
