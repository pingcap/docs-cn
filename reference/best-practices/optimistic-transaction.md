---
title: 乐观锁事务最佳实践
summary: 了解 TiDB 的乐观事务模型。
category: reference
---

# 乐观锁事务最佳实践

本文介绍 TiDB 乐观锁机制的实现原理，并通过分析乐观锁在多种场景下的应用为业务提供最佳实践。本文假定你对 [TiDB 的整体架构](/architecture.md#tidb-整体架构)和 [Percolator](https://www.usenix.org/legacy/event/osdi10/tech/full_papers/Peng.pdf) 事务模型都有一定了解，相关核心概念如下：

- [ACID](/glossary.md#acid)
- [事务](/glossary.md#事务)
- [乐观事务](/glossary.md#乐观事务)
- [悲观事务](/glossary.md#悲观事务)
- [显式事务/隐式事务](/glossary.md#显式事务隐式事务)

## 乐观事务原理

TiDB 中事务使用两阶段提交，流程如下：

![TiDB 中的两阶段提交](/media/best-practices/2pc-in-tidb.png)

1. 客户端开始一个事务。

    TiDB 从 PD 获取一个全局唯一递增的版本号作为当前事务的开始版本号，这里定义为该事务的 `start_ts` 版本。

2. 客户端发起读请求。

    a. TiDB 从 PD 获取数据路由信息，即数据具体存在哪个 TiKV 节点上。

    b. TiDB 从 TiKV 获取 `start_ts` 版本下对应的数据信息。

3. 客户端发起写请求。

    TiDB 校验写入数据是否符合一致性约束（如数据类型是否正确、是否符合唯一索引约束等）。**校验通过的数据将存放在内存里。**

4. 客户端发起 commit。

5. TiDB 开始两阶段提交，保证分布式事务的原子性，让数据真正落盘。

    a. TiDB 从当前要写入的数据中选择一个 Key 作为当前事务的 Primary Key。

    b. TiDB 从 PD 获取所有数据的写入路由信息，并将所有的 Key 按照所有的路由进行分类。

    c. TiDB 并发地向所有涉及的 TiKV 发起 prewrite 请求。TiKV 收到 prewrite 数据后，检查数据版本信息是否存在冲突或已过期。符合条件的数据会被加锁。

    d. TiDB 成功收到所有 prewrite 请求。

    e. TiDB 向 PD 获取第二个全局唯一递增版本号，定义为本次事务的 `commit_ts`。

    f. TiDB 向 Primary Key 所在 TiKV 发起第二阶段提交。TiKV 收到 commit 操作后，检查数据合法性，清理 prewrite 阶段留下的锁。

    g. TiDB 收到 f 成功信息。

6. TiDB 向客户端返回事务提交成功的信息。

7. TiDB 异步清理本次事务遗留的锁信息。

## 优缺点分析

通过分析 TiDB 中事务的处理流程，可以发现 TiDB 事务有如下优点：

* 实现原理简单，易于理解。
* 基于单实例事务实现了跨节点事务。
* 锁管理实现了去中心化。

但 TiDB 事务也存在以下缺点：

* 两阶段提交使网络交互增多。
* 缺少一个中心化的版本管理服务。
* 事务数据量过大时易导致内存暴涨。

## 事务大小

对于 TiDB 乐观事务而言，事务太大或者太小，都会影响事务性能。为了克服上述事务在处理过程中的不足，在实际应用中可以根据事务大小进行针对性处理。

### 小事务

在自动提交状态 (`autocommit = 1`) 下，下面三条语句各为一个事务：

```sql
# 使用自动提交的原始版本。
UPDATE my_table SET a ='new_value' WHERE id = 1;
UPDATE my_table SET a ='newer_value' WHERE id = 2;
UPDATE my_table SET a ='newest_value' WHERE id = 3;
```

此时每一条语句都需要经过两阶段提交，频繁的网络交互致使小事务延迟率高。为提升事务执行效率，可以选择使用显式事务，即在一个事务内执行三条语句：

```sql
# 优化后版本。
START TRANSACTION;
UPDATE my_table SET a ='new_value' WHERE id = 1;
UPDATE my_table SET a ='newer_value' WHERE id = 2;
UPDATE my_table SET a ='newest_value' WHERE id = 3;
COMMIT;
```

同理，执行 `INSERT` 语句时，建议使用显式事务。

### 大事务

通过分析两阶段提交的过程，可以发现单个事务过大时会存在以下问题：

* 客户端在提交之前，数据都写在内存中，而数据量过多时易导致 OOM (Out of Memory) 错误。
* 在第一阶段写入数据时，与其他事务出现冲突的概率会指数级增长，使事务之间相互阻塞影响。
* 最终导致事务完成提交的耗时增加。

因此，TiDB 特意对事务的大小做了一些限制：

* 单个事务包含的 SQL 语句不超过 5000 条（默认）
* 每个键值对不超过 6 MB
* 键值对的总数不超过 300000
* 键值对的总大小不超过 100 MB

为了使性能达到最优，建议每 100～500 行写入一个事务。

## 事务冲突

事务的冲突，主要指事务并发执行时对相同的 Key 进行了读写操作。冲突主要有两种形式：

* 读写冲突：部分事务进行读操作时，有事务在同一时间对相同的 Key 进行写操作。
* 写写冲突：不同事务同时对相同的 Key 进行写操作。

在 TiDB 的乐观锁机制中，只有在客户端执行 `commit` 时，才会触发两阶段提交并检测是否存在写写冲突。也就是说，在乐观事务下，如果存在写写冲突，在事务提交阶段就会暴露出来，因而更容易被用户感知。

### 默认冲突行为

乐观事务下，默认在最终提交时才会进行冲突检测。当两个事务同时更新同一行数据，即并发事务存在冲突时，不同时间点的执行结果如下：

![并发事务冲突流程](/media/best-practices/optimistic-transaction-table1.png)

根据乐观锁检测写写冲突的设定，该实例的执行逻辑分析如下：

![并发事务冲突逻辑](/media/best-practices/optimistic-transaction-case1.png)

1. 如上图，事务 A 在时间点 `t1` 开始，事务 B 在 `t2` 开始。

2. 事务 A、事务 B 同时更新同一行数据。

3. `t4` 时，事务 A 更新 `id = 1` 的同一行数据。 虽然 `t3` 时，事务 B 已经更新了这一行数据，但是乐观事务只有在事务 commit 时才检测冲突，因此 `t4` 的操作执行成功了。

4. `t5` 时，事务 B 成功提交，数据落盘。

5. `t6` 时，事务 A 尝试提交，检测冲突时发现 `t1` 之后有新的数据写入，因此返回错误，提示客户端重试，事务 A 提交失败。

### 重试机制

TiDB 中默认使用乐观事务模型，因而在高冲突率的场景中，事务很容易提交失败。而 MySQL 内部使用的是悲观事务模型，对应到上面的实例中，事务 A 在 `t4` 时就会返回错误，提示客户端根据需求去重试。

换言之，MySQL 在执行 SQL 语句的过程中进行冲突检测，所以提交时很难出现异常。由于 TiDB 使用乐观锁机制造成了两边行为不一致，要兼容 MySQL 的悲观事务行为，需要在客户端修改大量的代码。为了便于广大 MySQL 用户使用，TiDB 提供了重试机制。当事务提交后，如果发现冲突，TiDB 内部重新执行包含写操作的 SQL 语句。你可以通过设置 `tidb_disable_txn_auto_retry` 和 `tidb_retry_limit` 开启自动重试：

```toml
# 用于设置是否禁用自动重试，默认不重试。
tidb_disable_txn_auto_retry = on
# 用来控制重试次数。只有自动重试启用时该参数才会生效。
# 当 “tidb_retry_limit= 0” 时，也会禁用自动重试。
tidb_retry_limit = 10
```

推荐通过以下两种方式进行参数设置：

1. Session 级别设置：

    {{< copyable "sql" >}}

    ```sql
    set @@tidb_disable_txn_auto_retry = off;
    set @@tidb_retry_limit = 10;
    ```

2. Global 级别设置：

    {{< copyable "sql" >}}

    ```sql
    set @@global.tidb_disable_txn_auto_retry = off;
    set @@global.tidb_retry_limit = 10;
    ```

### 重试的局限性

基于重试机制的原理，可将重试过程概括为以下三个步骤：

1. 重新获取 `start_ts`。

2. 重新执行包含写操作的 SQL 语句。

3. 两阶段提交。

根据第二步，重试时仅重新执行包含写操作的 SQL 语句，并不涉及读操作的 SQL 语句。这会引发以下问题：

1. `start_ts` 发生了变更。当前事务中，读到数据的时间与事务真正开始的时间发生了变化。同理，写入的版本变成了重试时获取的 `start_ts` 而非事务一开始时获取的 `start_ts`。

2. 当前事务中，如果存在依赖查询结果来更新的语句，结果将变得不可控。

以下实例来具体说明了重试的局限性。开启自动重试后，当同时更新同一行数据时，Session A 和 Session B 在不同时间点的执行结果如下：

![自动重试流程](/media/best-practices/optimistic-transaction-table2.png)

该实例的执行逻辑分析如下：

![自动重试逻辑](/media/best-practices/optimistic-transaction-case2.png)

1. 如图，Session B 在 `t2` 时开始事务 2，`t5` 时提交成功。Session A 的事务 1 在事务 2 之前开始，在事务 2 提交完成后提交。

2. 事务 1、事务 2 同时更新同一行数据。

3. Session A 提交事务 1 时发现冲突，TiDB 内部重试事务 1。
    1. 重新取得新的 `start_ts` 为 `t8’`。
    2. 重新执行更新语句 `update tidb set name='pd' where id =1 and status=1`。
        1. 发现当前版本 `t8’` 下并不存在符合条件的语句，不需要更新。
        2. 没有数据更新，返回上层成功。

4. TiDB 认为事务 1 重试成功，返回客户端成功。

5. Session A 认为事务执行成功。如果在不存在其他更新，此时查询结果会发现数据与预想的不一致。

由上述分析可知，对于重试事务，当事务中更新语句需要依赖查询结果时，会重新取版本号作为 `start_ts`，所以无法保证事务原本可重复读的隔离级别，最终可能导致结果与预期出现不一致。

因此，如果存在依赖查询结果来更新 SQL 语句的事务，建议不要打开 TiDB 乐观锁的重试机制。

### 冲突预检

由上文可以知道，检测底层数据是否存在写写冲突是一个很重要的操作。具体而言，TiKV 在 prewrite 阶段就需要读取数据进行检测。为了优化这一块性能，TiDB 集群会在内存里面进行一次冲突预检测。

作为一个分布式系统，TiDB 在内存中的冲突检测主要在两个模块进行：

* TiDB 层。如果发现 TiDB 实例本身就存在写写冲突，那么第一个写入发出后，后面的写入已经清楚地知道自己冲突了，无需再往下层 TiKV 发送请求去检测冲突。
* TiKV 层。主要发生在 prewrite 阶段。因为 TiDB 集群是一个分布式系统，TiDB 实例本身无状态，实例之间无法感知到彼此的存在，也就无法确认自己的写入与别的 TiDB 实例是否存在冲突，所以会在 TiKV 这一层检测具体的数据是否有冲突。

其中 TiDB 层的冲突检测可以选择关闭，具体配置项如下：

```toml
# 事务内存锁相关配置，当本地事务冲突比较多时建议开启。
[txn-local-latches]
# 是否开启内存锁，默认为关闭。
enabled = false
# Hash 对应的 slot 数，会自动向上调整为 2 的指数倍。
# 每个 slot 占 32 Bytes 内存。当写入数据的范围比较广时（如导数据），
# 设置过小会导致变慢，性能下降。（默认为 2048000）
capacity = 2048000
```

配置项 `capacity` 主要影响到冲突判断的正确性。在实现冲突检测时，不可能把所有的 Key 都存到内存里，所以真正存下来的是每个 Key 的 Hash 值。有 Hash 算法就有碰撞也就是误判的概率，这里可以通过配置 `capacity` 来控制 Hash 取模的值：

* `capacity` 值越小，占用内存小，误判概率越大。
* `capacity` 值越大，占用内存大，误判概率越小。

实际应用时，如果业务场景能够预判断写入不存在冲突（如导入数据操作），建议关闭冲突检测。

相应地，在 TiKV 层检测内存中是否存在冲突也有类似的机制。不同的是，TiKV 层的检测会更严格且不允许关闭，仅支持对 Hash 取模值进行配置：

```toml
# scheduler 内置一个内存锁机制，防止同时对一个 Key 进行操作。
# 每个 Key hash 到不同的 slot。（默认为 2048000）
scheduler-concurrency = 2048000
```

此外，TiKV 支持监控等待 latch 的时间：

![Scheduler latch wait duration](/media/best-practices/optimistic-transaction-metric.png)

当 `Scheduler latch wait duration` 的值特别高时，说明大量时间消耗在等待锁的请求上。如果不存在底层写入慢的问题，基本上可以判断该段时间内冲突比较多。
