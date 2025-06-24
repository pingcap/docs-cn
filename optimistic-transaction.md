---
title: TiDB 乐观事务模型
summary: 了解 TiDB 中的乐观事务模型。
---

# TiDB 乐观事务模型

在乐观事务中，冲突检测是在事务提交时进行的。当并发事务不经常修改相同行时，这有助于提高性能，因为可以跳过获取行锁的过程。但在并发事务频繁修改相同行（发生冲突）的情况下，乐观事务的性能可能比[悲观事务](/pessimistic-transaction.md)差。

在启用乐观事务之前，请确保你的应用程序能够正确处理 `COMMIT` 语句可能返回错误的情况。如果你不确定应用程序如何处理这种情况，建议改用悲观事务。

> **注意：**
>
> 从 v3.0.8 开始，TiDB 默认使用[悲观事务模式](/pessimistic-transaction.md)。但是，如果你将集群从 v3.0.7 或更早版本升级到 v3.0.8 或更高版本，这不会影响你现有的集群。换句话说，**只有新创建的集群默认使用悲观事务模式**。

## 乐观事务原理

为了支持分布式事务，TiDB 在乐观事务中采用两阶段提交（2PC）。具体过程如下：

![TiDB 中的 2PC](/media/2pc-in-tidb.png)

1. 客户端开始一个事务。

    TiDB 从 PD 获取一个时间戳（单调递增且全局唯一）作为当前事务的唯一事务 ID，称为 `start_ts`。TiDB 实现了多版本并发控制，因此 `start_ts` 也作为此事务获取的数据库快照的版本。这意味着该事务只能读取数据库在 `start_ts` 时刻的数据。

2. 客户端发出读取请求。

    1. TiDB 从 PD 接收路由信息（数据在 TiKV 节点间的分布情况）。
    2. TiDB 从 TiKV 接收 `start_ts` 版本的数据。

3. 客户端发出写入请求。

    TiDB 检查写入的数据是否满足约束（确保数据类型正确，满足 NOT NULL 约束）。**有效数据存储在 TiDB 中该事务的私有内存中**。

4. 客户端发出提交请求。

5. TiDB 开始 2PC，并在保证事务原子性的同时将数据持久化到存储中。

    1. TiDB 从要写入的数据中选择一个主键（Primary Key）。
    2. TiDB 从 PD 接收 Region 分布信息，并相应地按 Region 对所有键进行分组。
    3. TiDB 向所有涉及的 TiKV 节点发送预写请求。然后，TiKV 检查是否存在冲突或过期版本。有效数据被锁定。
    4. TiDB 接收预写阶段的所有响应，预写成功。
    5. TiDB 从 PD 接收提交版本号并标记为 `commit_ts`。
    6. TiDB 向主键（Primary Key）所在的 TiKV 节点发起第二次提交。TiKV 检查数据，并清理预写阶段遗留的锁。
    7. TiDB 接收到报告第二阶段成功完成的消息。

6. TiDB 向客户端返回消息，通知事务成功提交。

7. TiDB 异步清理此事务中遗留的锁。

## 优点和缺点

从上述 TiDB 事务过程可以看出，TiDB 事务具有以下优点：

* 易于理解
* 基于单行事务实现跨节点事务
* 去中心化的锁管理

然而，TiDB 事务也有以下缺点：

* 由于 2PC 导致的事务延迟
* 需要中心化的时间戳分配服务
* 当大量数据写入内存时可能发生 OOM（内存溢出）

## 事务重试

> **注意：**
>
> 从 v8.0.0 开始，[`tidb_disable_txn_auto_retry`](/system-variables.md#tidb_disable_txn_auto_retry) 系统变量已弃用，TiDB 不再支持乐观事务的自动重试。建议使用[悲观事务模式](/pessimistic-transaction.md)。如果遇到乐观事务冲突，你可以在应用程序中捕获错误并重试事务。

在乐观事务模型中，在高竞争场景下，事务可能因写-写冲突而提交失败。TiDB 默认使用乐观并发控制，而 MySQL 采用悲观并发控制。这意味着 MySQL 在执行写类型的 SQL 语句时添加锁，并且其可重复读隔离级别允许当前读，因此提交通常不会遇到异常。为了降低应用程序适配的难度，TiDB 提供了内部重试机制。

### 自动重试

如果在事务提交时发生写-写冲突，TiDB 会自动重试包含写操作的 SQL 语句。你可以通过将 `tidb_disable_txn_auto_retry` 设置为 `OFF` 来启用自动重试，并通过配置 `tidb_retry_limit` 设置重试限制：

```toml
# 是否禁用自动重试（默认为 "on"）
tidb_disable_txn_auto_retry = OFF
# 设置最大重试次数（默认为 "10"）
# 当 "tidb_retry_limit = 0" 时，自动重试完全禁用
tidb_retry_limit = 10
```

你可以在会话级别或全局级别启用自动重试：

1. 会话级别：

    {{< copyable "sql" >}}

    ```sql
    SET tidb_disable_txn_auto_retry = OFF;
    ```

    {{< copyable "sql" >}}

    ```sql
    SET tidb_retry_limit = 10;
    ```

2. 全局级别：

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
> `tidb_retry_limit` 变量决定最大重试次数。当此变量设置为 `0` 时，所有事务都不会自动重试，包括自动提交的隐式单语句事务。这是在 TiDB 中完全禁用自动重试机制的方法。禁用自动重试后，所有冲突的事务都会以最快的方式向应用层报告失败（包括 `try again later` 消息）。

### 重试的限制

默认情况下，TiDB 不会重试事务，因为这可能导致更新丢失和破坏 [`REPEATABLE READ` 隔离](/transaction-isolation-levels.md)。

原因可以从重试的过程中观察到：

1. 分配新的时间戳并标记为 `start_ts`。
2. 重试包含写操作的 SQL 语句。
3. 执行两阶段提交。

在步骤 2 中，TiDB 只重试包含写操作的 SQL 语句。但是，在重试期间，TiDB 接收新的版本号来标记事务的开始。这意味着 TiDB 使用新的 `start_ts` 版本的数据重试 SQL 语句。在这种情况下，如果事务使用其他查询结果更新数据，结果可能不一致，因为违反了 `REPEATABLE READ` 隔离。

如果你的应用程序可以容忍更新丢失，并且不需要 `REPEATABLE READ` 隔离一致性，你可以通过设置 `tidb_disable_txn_auto_retry = OFF` 来启用此功能。

## 冲突检测

作为分布式数据库，TiDB 在 TiKV 层执行内存中的冲突检测，主要在预写阶段进行。TiDB 实例是无状态的，彼此不知道对方的存在，这意味着它们无法知道它们的写入是否在整个集群中产生冲突。因此，冲突检测在 TiKV 层执行。

配置如下：

```toml
# 控制槽位数量（默认为 "2048000"）
scheduler-concurrency = 2048000
```

此外，TiKV 支持监控调度器中等待锁存器的时间。

![调度器锁存器等待时间](/media/optimistic-transaction-metric.png)

当 `Scheduler latch wait duration` 较高且没有慢写入时，可以安全地得出结论，此时存在许多写冲突。
