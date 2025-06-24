---
title: TiDB 悲观事务模式
summary: 了解 TiDB 中的悲观事务模式。
---

# TiDB 悲观事务模式

为了让 TiDB 的使用方式更接近传统数据库并降低迁移成本，从 v3.0 开始，TiDB 在乐观事务模型的基础上支持悲观事务模式。本文介绍 TiDB 悲观事务模式的特点。

> **注意：**
>
> 从 v3.0.8 开始，新创建的 TiDB 集群默认使用悲观事务模式。但是，如果你将集群从 v3.0.7 或更早版本升级到 v3.0.8 或更高版本，这不会影响你现有的集群。换句话说，**只有新创建的集群默认使用悲观事务模式**。

## 切换事务模式

你可以通过配置 [`tidb_txn_mode`](/system-variables.md#tidb_txn_mode) 系统变量来设置事务模式。以下命令将集群中新创建会话的所有显式事务（即非自动提交事务）设置为悲观事务模式：

{{< copyable "sql" >}}

```sql
SET GLOBAL tidb_txn_mode = 'pessimistic';
```

你也可以通过执行以下 SQL 语句显式启用悲观事务模式：

{{< copyable "sql" >}}

```sql
BEGIN PESSIMISTIC;
```

{{< copyable "sql" >}}

```sql
BEGIN /*T! PESSIMISTIC */;
```

`BEGIN PESSIMISTIC;` 和 `BEGIN OPTIMISTIC;` 语句的优先级高于 `tidb_txn_mode` 系统变量。使用这两个语句启动的事务会忽略系统变量，并支持同时使用悲观和乐观事务模式。

## 行为特征

TiDB 中的悲观事务行为与 MySQL 类似。请参见[与 MySQL InnoDB 的差异](#与-mysql-innodb-的差异)了解细微差别。

- 对于悲观事务，TiDB 引入了快照读和当前读。

    - 快照读：是一种无锁读取，读取事务开始前已提交的版本。`SELECT` 语句中的读取是快照读。
    - 当前读：是一种加锁读取，读取最新已提交的版本。`UPDATE`、`DELETE`、`INSERT` 或 `SELECT FOR UPDATE` 语句中的读取是当前读。

    以下示例详细说明了快照读和当前读。

    | 会话 1 | 会话 2 | 会话 3 |
    | :----| :---- | :---- |
    | CREATE TABLE t (a INT); |  |  |
    | INSERT INTO T VALUES(1); |  |  |
    | BEGIN PESSIMISTIC; |  |
    | UPDATE t SET a = a + 1; |  |  |
    |  | BEGIN PESSIMISTIC; |  |
    |  | SELECT * FROM t;  -- 使用快照读读取当前事务开始前已提交的版本。结果返回 a=1。 |  |
    |  |  | BEGIN PESSIMISTIC;
    |  |  | SELECT * FROM t FOR UPDATE; -- 使用当前读。等待锁释放。  |
    | COMMIT; -- 释放锁。会话 3 的 SELECT FOR UPDATE 操作获得锁，TiDB 使用当前读读取最新已提交的版本。结果返回 a=2。 |  |  |
    |  | SELECT * FROM t; -- 使用快照读读取当前事务开始前已提交的版本。结果返回 a=1。 |  |

- 执行 `UPDATE`、`DELETE` 或 `INSERT` 语句时，会读取**最新**的已提交数据，修改数据，并对修改的行应用悲观锁。

- 对于 `SELECT FOR UPDATE` 语句，会对最新已提交数据的版本应用悲观锁，而不是对修改的行应用。

- 锁会在事务提交或回滚时释放。其他尝试修改数据的事务会被阻塞，必须等待锁释放。尝试**读取**数据的事务不会被阻塞，因为 TiDB 使用多版本并发控制（MVCC）。

- 你可以通过设置系统变量 [`tidb_constraint_check_in_place_pessimistic`](/system-variables.md#tidb_constraint_check_in_place_pessimistic-new-in-v630) 来控制是否跳过带有唯一约束检查的悲观锁。详情请参见[约束](/constraints.md#悲观事务)。

- 如果多个事务试图获取彼此的锁，就会发生死锁。这种情况会被自动检测到，其中一个事务会被随机终止，并返回 MySQL 兼容的错误代码 `1213`。

- 事务最多等待 `innodb_lock_wait_timeout` 秒（默认：50）来获取新锁。当达到此超时时间时，会返回 MySQL 兼容的错误代码 `1205`。如果多个事务在等待同一个锁，优先级顺序大致基于事务的 `start ts`。

- TiDB 支持在同一集群中同时使用乐观事务模式和悲观事务模式。你可以为事务执行指定任一模式。

- TiDB 支持 `FOR UPDATE NOWAIT` 语法，不会阻塞等待锁释放。相反，会返回 MySQL 兼容的错误代码 `3572`。

- 如果 `Point Get` 和 `Batch Point Get` 算子不读取数据，它们仍会锁定给定的主键或唯一键，这会阻止其他事务锁定或写入相同的主键或唯一键。

- TiDB 支持 `FOR UPDATE OF TABLES` 语法。对于连接多个表的语句，TiDB 只对 `OF TABLES` 中的表的相关行应用悲观锁。

## 与 MySQL InnoDB 的差异

1. 当 TiDB 执行 WHERE 子句中使用范围的 DML 或 `SELECT FOR UPDATE` 语句时，范围内的并发 DML 语句不会被阻塞。

    例如：

    ```sql
    CREATE TABLE t1 (
     id INT NOT NULL PRIMARY KEY,
     pad1 VARCHAR(100)
    );
    INSERT INTO t1 (id) VALUES (1),(5),(10);
    ```

    ```sql
    BEGIN /*T! PESSIMISTIC */;
    SELECT * FROM t1 WHERE id BETWEEN 1 AND 10 FOR UPDATE;
    ```

    ```sql
    BEGIN /*T! PESSIMISTIC */;
    INSERT INTO t1 (id) VALUES (6); -- 仅在 MySQL 中阻塞
    UPDATE t1 SET pad1='new value' WHERE id = 5; -- 在 MySQL 和 TiDB 中都等待阻塞
    ```

    这种行为是因为 TiDB 目前不支持**间隙锁定**。

2. TiDB 不支持 `SELECT LOCK IN SHARE MODE`。

    当执行 `SELECT LOCK IN SHARE MODE` 时，其效果与不带锁的效果相同，因此不会阻塞其他事务的读取或写入操作。

3. DDL 可能导致悲观事务提交失败。

    在 MySQL 中执行 DDL 时，可能会被正在执行的事务阻塞。然而，在 TiDB 中，DDL 操作不会被阻塞，这会导致悲观事务提交失败：`ERROR 1105 (HY000): Information schema is changed. [try again later]`。TiDB 在事务执行期间执行 `TRUNCATE TABLE` 语句可能会导致 `table doesn't exist` 错误。

4. 执行 `START TRANSACTION WITH CONSISTENT SNAPSHOT` 后，MySQL 仍然可以读取其他事务中后来创建的表，而 TiDB 不能。

5. 自动提交事务倾向于使用乐观锁定。

    在使用悲观模式时，自动提交事务首先尝试使用开销较小的乐观模式提交语句。如果发生写冲突，则使用悲观模式重试事务。因此，如果将 `tidb_retry_limit` 设置为 `0`，当发生写冲突时，自动提交事务仍会报告 `Write Conflict` 错误。

    自动提交的 `SELECT FOR UPDATE` 语句不会等待锁。

6. 语句中 `EMBEDDED SELECT` 读取的数据不会被锁定。

7. TiDB 中的打开事务不会阻止垃圾回收（GC）。默认情况下，这将悲观事务的最大执行时间限制为 1 小时。你可以通过编辑 TiDB 配置文件中 `[performance]` 下的 `max-txn-ttl` 来修改此限制。

## 隔离级别

TiDB 在悲观事务模式下支持以下两种隔离级别：

- 默认为[可重复读](/transaction-isolation-levels.md#可重复读隔离级别)，与 MySQL 相同。

    > **注意：**
    >
    > 在此隔离级别下，DML 操作基于最新已提交的数据执行。这种行为与 MySQL 相同，但与 TiDB 的乐观事务模式不同。请参见 [TiDB 与 MySQL 可重复读的区别](/transaction-isolation-levels.md#tidb-与-mysql-可重复读的区别)。

- [读已提交](/transaction-isolation-levels.md#读已提交隔离级别)。你可以使用 [`SET TRANSACTION`](/sql-statements/sql-statement-set-transaction.md) 语句设置此隔离级别。

## 悲观事务提交流程

在事务提交流程中，悲观事务和乐观事务具有相同的逻辑。两种事务都采用两阶段提交（2PC）模式。悲观事务的重要改动是 DML 执行。

![TiDB 悲观事务提交流程](/media/pessimistic-transaction-commit.png)

悲观事务在 2PC 之前添加了一个 `获取悲观锁` 阶段。此阶段包括以下步骤：

1. （与乐观事务模式相同）TiDB 接收来自客户端的 `begin` 请求，当前时间戳是此事务的 start_ts。
2. 当 TiDB 服务器接收到来自客户端的写入请求时，TiDB 服务器向 TiKV 服务器发起悲观锁请求，并将锁持久化到 TiKV 服务器。
3. （与乐观事务模式相同）当客户端发送提交请求时，TiDB 开始执行类似于乐观事务模式的两阶段提交。

![TiDB 中的悲观事务](/media/pessimistic-transaction-in-tidb.png)

## 流水线锁定流程

添加悲观锁需要向 TiKV 写入数据。只有在通过 Raft 提交和应用后，才能将成功添加锁的响应返回给 TiDB。因此，与乐观事务相比，悲观事务模式不可避免地具有更高的延迟。

为了减少锁定的开销，TiKV 实现了流水线锁定流程：当数据满足锁定要求时，TiKV 立即通知 TiDB 执行后续请求，并异步写入悲观锁。这个过程减少了大部分延迟，显著提高了悲观事务的性能。但是，当 TiKV 发生网络分区或 TiKV 节点宕机时，异步写入悲观锁可能会失败，并影响以下方面：

* 其他修改相同数据的事务无法被阻塞。如果应用逻辑依赖于锁定或锁等待机制，则会影响应用逻辑的正确性。

* 事务提交有较低概率失败，但不影响事务的正确性。

<CustomContent platform="tidb">

如果应用逻辑依赖于锁定或锁等待机制，或者你希望即使在 TiKV 集群异常的情况下也尽可能保证事务提交的成功率，你应该禁用流水线锁定功能。

![流水线悲观锁](/media/pessimistic-transaction-pipelining.png)

此功能默认启用。要禁用它，请修改 TiKV 配置：

```toml
[pessimistic-txn]
pipelined = false
```

如果 TiKV 集群是 v4.0.9 或更高版本，你也可以通过[动态修改 TiKV 配置](/dynamic-config.md#动态修改-tikv-配置)来动态禁用此功能：

{{< copyable "sql" >}}

```sql
set config tikv pessimistic-txn.pipelined='false';
```

</CustomContent>

<CustomContent platform="tidb-cloud">

如果应用逻辑依赖于锁定或锁等待机制，或者你希望即使在 TiKV 集群异常的情况下也尽可能保证事务提交的成功率，你可以[联系 TiDB Cloud 支持](/tidb-cloud/tidb-cloud-support.md)来禁用流水线锁定功能。

</CustomContent>

## 内存悲观锁

在 v6.0.0 中，TiKV 引入了内存悲观锁功能。启用此功能后，悲观锁通常只存储在 Region leader 的内存中，不会持久化到磁盘或通过 Raft 复制到其他副本。此功能可以大大减少获取悲观锁的开销，提高悲观事务的吞吐量。

当内存悲观锁的内存使用超过 Region 或 TiKV 节点的内存阈值时，获取悲观锁会转为[流水线锁定流程](#流水线锁定流程)。当 Region 合并或 leader 转移时，为避免悲观锁丢失，TiKV 会将内存悲观锁写入磁盘并复制到其他副本。

内存悲观锁的表现与流水线锁定流程类似，在集群健康时不影响锁的获取。但是，当 TiKV 发生网络隔离或 TiKV 节点宕机时，已获取的悲观锁可能会丢失。

如果应用逻辑依赖于锁获取或锁等待机制，或者你希望即使在集群异常状态下也尽可能保证事务提交的成功率，你需要**禁用**内存悲观锁功能。

此功能默认启用。要禁用它，请修改 TiKV 配置：

```toml
[pessimistic-txn]
in-memory = false
```

要动态禁用此功能，请动态修改 TiKV 配置：

{{< copyable "sql" >}}

```sql
set config tikv pessimistic-txn.in-memory='false';
```
