---
title: TiFlash MinTSO Scheduler
summary: 介绍 TiFlash MinTSO 调度器。
---

# TiFlash MinTSO Scheduler

本文介绍 TiFlash MinTSO scheduler 的原理与实现。

## 背景
在 TiDB 中，对于 MPP query，TiDB 会将 query 拆成一个或多个 MPPTask，并将 MPPTask 发送给对应的 TiFlash 节点。而在 TiFlash 节点内部，对每个 MPPTask 进行编译与执行。在 TiFlash 使用 [pipeline 执行模型](/tiflash/tiflash-pipeline-model.md) 之前，对于每个 MPPTask，TiFlash 都需要使用若干个线程（具体线程数取决于 MPPTask 的复杂度以及 TiFlash 并发参数的设置）来执行。在高并发场景中，TiFlash 节点会同时接受到多个 MPPTask，如果 TiFlash 不对 MPPTask 的执行有所控制，则 TiFlash 需要向系统申请的线程数会随着 MPPTask 数量的增加而线性增加。过多的线程一方面会影响 TiFlash 的执行效率，另一方面操作系统本身支持的线程数也是有限的，当 TiFlash 申请的线程数超过操作系统的限制时，TiFlash 就会碰到无法申请线程的错误。

为了提升在高并发场景下 TiFlash 的处理能力，我们需要在 TiFlash 中引入一个 task 的 scheduler。

## 设计实现

如背景所述，TiFlash task scheudler 引入的初衷是控制运行时使用的线程数。一个简单的想法是指定 TiFlash 可以申请的最大线程数，对于每个 MPPTask，调度器根据当前系统已经使用的线程数以及该 MPPTask 预期使用的线程数，决定该 MPPTask 是否能够被调度：

<img src="/media/tiflash/tiflash_mintso_v1.png" width=50%></img>

尽管上述调度策略能有效控制系统的线程数，但是 MPPTask 并不是一个最小的独立执行单元，不同 MPPTask 之间会有依赖关系:
```
mysql> explain select count(*) from t0 a join t0 b on a.id = b.id;
+--------------------------------------------+----------+--------------+---------------+----------------------------------------------------------+
| id                                         | estRows  | task         | access object | operator info                                            |
+--------------------------------------------+----------+--------------+---------------+----------------------------------------------------------+
| HashAgg_44                                 | 1.00     | root         |               | funcs:count(Column#8)->Column#7                          |
| └─TableReader_46                           | 1.00     | root         |               | MppVersion: 2, data:ExchangeSender_45                    |
|   └─ExchangeSender_45                      | 1.00     | mpp[tiflash] |               | ExchangeType: PassThrough                                |
|     └─HashAgg_13                           | 1.00     | mpp[tiflash] |               | funcs:count(1)->Column#8                                 |
|       └─Projection_43                      | 12487.50 | mpp[tiflash] |               | test.t0.id                                               |
|         └─HashJoin_42                      | 12487.50 | mpp[tiflash] |               | inner join, equal:[eq(test.t0.id, test.t0.id)]           |
|           ├─ExchangeReceiver_22(Build)     | 9990.00  | mpp[tiflash] |               |                                                          |
|           │ └─ExchangeSender_21            | 9990.00  | mpp[tiflash] |               | ExchangeType: Broadcast, Compression: FAST               |
|           │   └─Selection_20               | 9990.00  | mpp[tiflash] |               | not(isnull(test.t0.id))                                  |
|           │     └─TableFullScan_19         | 10000.00 | mpp[tiflash] | table:a       | pushed down filter:empty, keep order:false, stats:pseudo |
|           └─Selection_24(Probe)            | 9990.00  | mpp[tiflash] |               | not(isnull(test.t0.id))                                  |
|             └─TableFullScan_23             | 10000.00 | mpp[tiflash] | table:b       | pushed down filter:empty, keep order:false, stats:pseudo |
+--------------------------------------------+----------+--------------+---------------+----------------------------------------------------------+
```
上面的 query 会在每个 TiFlash 节点中生成 2 个 MPPTask，其中 `ExchangeSender_21` 所在的 MPPTask 依赖于 `ExchangeSender_45` 所在的 MPPTask。假设这个 query 高并发的情况下，调度器调度了每个 query 中 `ExchangeSender_45` 所在的 MPPTask，则系统就会进入死锁的状态。

为了避免系统陷入死锁的状态，我们引入了两层 thread 的限制：
* threads_soft_limit
* threads_hard_limit
其中 soft limit 主要用来限制系统使用的线程数，但是对于特定的 MPPTask，为了避免死锁可以打破这个限制，而 hard limit 则是为了保护系统，一旦超过 hard limit，TiFlash 可以通过报错来避免系统陷入死锁状态。

利用 soft limit 来避免死锁的思想很简单，系统中存在一个特殊的 query，该 query 的所有 MPPTask 在调度时都可以突破 soft limit 的限制，这样只要系统的 thread 不超过 hard limit，系统中就必定存在一个 query 的所有 MPPTask 都可以正常执行，这样系统就不会出现死锁。

MinTSO Scheduler 的目标就是在控制系统线程数的同时，确保系统中始终有一个特殊的 query，其所有的 MPPTask 都可以被调度到。 MinTSO Scheduler 是一个完全分布式的调度器，每个 TiFlash 仅根据自身信息对 MPPTask 进行调度，这样每个 TiFlash 的 MinTSO Scheduler 需要找到同一个“特殊”的 query。在 TiDB 中，每个 query 都会带有一个读的时间戳(TiDB 中称之为 start_ts)，MinTSO Scheduler 定义“特殊” query 的标准即为当前 TiFlash 节点上 start_ts 最小的 query，根据全局最小一定是局部最小的原理，所有的 TiFlash 选出的“特殊” query 必然是同一个。我们称之为 MinTSO query。MinTSO scheduler 的调度流程如下：

<img src="/media/tiflash/tiflash_mintso_v2.png" width=50%></img>


线程调度模型存在两个缺陷：

- 在高并发场景下，过多的线程会引起较多上下文切换，导致较高的线程调度代价。

- 线程调度模型无法精准计量查询的资源使用量以及做细粒度的资源管控。

在新的执行模型 Pipeline Model 中进行了以下优化：

- 查询会被划分为多个 pipeline 并依次执行。在每个 pipeline 中，数据块会被尽可能保留在缓存中，从而实现更好的时间局部性，从而提高整个执行过程的效率。

- 为了摆脱操作系统原生的线程调度模型，实现更加精细的调度机制，每个 pipeline 会被实例化成若干个 task，使用 task 调度模型，同时使用固定线程池，减少了操作系统申请和调度线程的开销。

TiFlash Pipeline Model 的架构如下：

![TiFlash Pipeline Model Design](/media/tiflash/tiflash-pipeline-model.png)

如上图所示，Pipeline Model 中有两个主要组成部分：Pipeline Query Executor 和 Task Scheduler。

- Pipeline Query Executor

    负责将从 TiDB 节点发过来的查询请求转换为 pipeline dag。

    它会找到查询中的 pipeline breaker 算子，以 pipeline breaker 为边界将查询切分成若干个 pipeline，根据 pipeline 之间的依赖关系，将 pipeline 组装成一个有向无环图。

    pipeline breaker 用于指代存在停顿/阻塞逻辑的算子，这一类算子会持续接收上游算子传来的数据块，直到所有数据块都被接收后，才会将处理结果返回给下游算子。这类算子会破坏数据处理流水线，所以被称为 pipeline breaker。pipeline breaker 的代表有 Aggregation，它会将上游算子的数据都写入到哈希表后，才对哈希表中的数据做计算返回给下游算子。

    在查询被转换为 pipeline dag 后，Pipeline Query Executor 会按照依赖关系依次执行每个 pipeline。pipeline 会根据查询并发度被实例化成若干个 task 提交给 Task Scheduler 执行。

- Task Scheduler

    负责执行由 Pipeline Query Executor 提交过来的 task。task 会根据执行的逻辑的不同，在 Task Scheduler 里的不同组件中动态切换执行。

    - CPU Task Thread Pool

      执行 task 中 CPU 密集型的计算逻辑，比如数据过滤、函数计算等。

    - IO Task Thread Pool

      执行 task 中 IO 密集型的计算逻辑，比如计算中间结果落盘等。

    - Wait Reactor

      执行 task 中的等待逻辑，比如等待网络层将数据包传输给计算层等。
