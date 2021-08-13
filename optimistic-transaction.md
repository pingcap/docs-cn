---
title: TiDB 乐观事务模型
summary: 了解 TiDB 的乐观事务模型。
---

# TiDB 乐观事务模型

乐观事务模型下，将修改冲突视为事务提交的一部分。因此并发事务不常修改同一行时，可以跳过获取行锁的过程进而提升性能。但是并发事务频繁修改同一行（冲突）时，乐观事务的性能可能低于[悲观事务](/pessimistic-transaction.md)。

启用乐观事务前，请确保应用程序可正确处理 `COMMIT` 语句可能返回的错误。如果不确定应用程序将会如何处理，建议改为使用悲观事务。

> **注意：**
>
> 自 v3.0.8 开始，TiDB 集群默认使用[悲观事务模型](/pessimistic-transaction.md)。但如果从 3.0.7 及之前版本创建的集群升级到 3.0.8 及之后的版本，不会改变默认事务模型，即**只有新创建的集群才会默认使用悲观事务模型**。

## 乐观事务原理

为支持分布式事务，TiDB 中乐观事务使用两阶段提交协议，流程如下：

![TiDB 中的两阶段提交](/media/2pc-in-tidb.png)

1. 客户端开始一个事务。

    TiDB 从 PD 获取一个全局唯一递增的时间戳作为当前事务的唯一事务 ID，这里称为该事务的 `start_ts`。TiDB 实现了多版本并发控制 (MVCC)，因此 `start_ts` 同时也作为该事务获取的数据库快照版本。该事务只能读到此 `start_ts` 版本可以读到的数据。

2. 客户端发起读请求。

    1. TiDB 从 PD 获取数据路由信息，即数据具体存在哪个 TiKV 节点上。
    2. TiDB 从 TiKV 获取 `start_ts` 版本下对应的数据。

3. 客户端发起写请求。

    TiDB 校验写入数据是否符合约束（如数据类型是否正确、是否符合非空约束等）。**校验通过的数据将存放在 TiDB 中该事务的私有内存里。**

4. 客户端发起 commit。

5. TiDB 开始两阶段提交，在保证事务原子性的前提下，进行数据持久化。

    1. TiDB 从当前要写入的数据中选择一个 Key 作为当前事务的 Primary Key。
    2. TiDB 从 PD 获取所有数据的写入路由信息，并将所有的 Key 按照所有的路由进行分类。
    3. TiDB 并发地向所有涉及的 TiKV 发起 prewrite 请求。TiKV 收到 prewrite 数据后，检查数据版本信息是否存在冲突或已过期。符合条件的数据会被加锁。
    4. TiDB 收到所有 prewrite 响应且所有 prewrite 都成功。
    5. TiDB 向 PD 获取第二个全局唯一递增版本号，定义为本次事务的 `commit_ts`。
    6. TiDB 向 Primary Key 所在 TiKV 发起第二阶段提交。TiKV 收到 commit 操作后，检查数据合法性，清理 prewrite 阶段留下的锁。
    7. TiDB 收到两阶段提交成功的信息。

6. TiDB 向客户端返回事务提交成功的信息。

7. TiDB 异步清理本次事务遗留的锁信息。

## 优缺点分析

通过分析 TiDB 中事务的处理流程，可以发现 TiDB 事务有如下优点：

* 实现原理简单，易于理解。
* 基于单实例事务实现了跨节点事务。
* 锁管理实现了去中心化。

但 TiDB 事务也存在以下缺点：

* 两阶段提交使网络交互增多。
* 需要一个中心化的分配时间戳服务。
* 事务数据量过大时易导致内存暴涨。

## 事务的重试

使用乐观事务模型时，在高冲突率的场景中，事务容易发生写写冲突而导致提交失败。MySQL 使用悲观事务模型，在执行写入类型的 SQL 语句的过程中进行加锁并且在 Repeatable Read 隔离级下使用了当前读的机制，能够读取到最新的数据，所以提交时一般不会出现异常。为了降低应用改造难度，TiDB 提供了数据库内部自动重试机制。

### 重试机制

当事务提交时，如果发现写写冲突，TiDB 内部重新执行包含写操作的 SQL 语句。你可以通过设置 `tidb_disable_txn_auto_retry = OFF` 开启自动重试，并通过 `tidb_retry_limit` 设置重试次数：

```toml
# 设置是否禁用自动重试，默认为 “on”，即不重试。
tidb_disable_txn_auto_retry = OFF
# 控制重试次数，默认为 “10”。只有自动重试启用时该参数才会生效。
# 当 “tidb_retry_limit= 0” 时，也会禁用自动重试。
tidb_retry_limit = 10
```

你也可以修改当前 Session 或 Global 的值：

- Session 级别设置：

    {{< copyable "sql" >}}

    ```sql
    SET tidb_disable_txn_auto_retry = OFF;
    ```

    {{< copyable "sql" >}}

    ```sql
    SET tidb_retry_limit = 10;
    ```

- Global 级别设置：

    {{< copyable "sql" >}}

    ```sql
    SET GLOBAL tidb_disable_txn_auto_retry = OFF;
    ```

    {{< copyable "sql" >}}

    ```sql
    SET GLOBAL tidb_retry_limit = 10;
    ```

> **注意：**
>
> `tidb_retry_limit` 变量决定了事务重试的最大次数。当它被设置为 0 时，所有事务都不会自动重试，包括自动提交的单语句隐式事务。这是彻底禁用 TiDB 中自动重试机制的方法。禁用自动重试后，所有冲突的事务都会以最快的方式上报失败信息（包含 `try again later`）给应用层。

### 重试的局限性

TiDB 默认不进行事务重试，因为重试事务可能会导致更新丢失，从而破坏[可重复读的隔离级别](/transaction-isolation-levels.md)。

事务重试的局限性与其原理有关。事务重试可概括为以下三个步骤：

1. 重新获取 `start_ts`。
2. 重新执行包含写操作的 SQL 语句。
3. 再次进行两阶段提交。

第二步中，重试时仅重新执行包含写操作的 SQL 语句，并不涉及读操作的 SQL 语句。但是当前事务中读到数据的时间与事务真正开始的时间发生了变化，写入的版本变成了重试时获取的 `start_ts` 而非事务一开始时获取的 `start_ts`。因此，当事务中存在依赖查询结果来更新的语句时，重试将无法保证事务原本可重复读的隔离级别，最终可能导致结果与预期出现不一致。

如果业务可以容忍事务重试导致的异常，或并不关注事务是否以可重复读的隔离级别来执行，则可以开启自动重试。

## 冲突检测

作为一个分布式系统，TiDB 在内存中的冲突检测是在 TiKV 中进行，主要发生在 prewrite 阶段。因为 TiDB 集群是一个分布式系统，TiDB 实例本身无状态，实例之间无法感知到彼此的存在，也就无法确认自己的写入与别的 TiDB 实例是否存在冲突，所以会在 TiKV 这一层检测具体的数据是否有冲突。

具体配置如下：

```toml
# scheduler 内置一个内存锁机制，防止同时对一个 Key 进行操作。
# 每个 Key hash 到不同的 slot。（默认为 2048000）
scheduler-concurrency = 2048000
```

此外，TiKV 支持监控等待 latch 的时间：

![Scheduler latch wait duration](/media/optimistic-transaction-metric.png)

当 `Scheduler latch wait duration` 的值特别高时，说明大量时间消耗在等待锁的请求上。如果不存在底层写入慢的问题，基本上可以判断该段时间内冲突比较多。

## 更多阅读

- [Percolator 和 TiDB 事务算法](https://pingcap.com/blog-cn/percolator-and-txn/)
