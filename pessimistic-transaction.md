---
title: TiDB 悲观事务模型
summary: 了解 TiDB 的悲观事务模型。
category: reference
aliases: ['/docs-cn/dev/reference/transactions/transaction-pessimistic/']
---

# TiDB 悲观事务模型

为了使 TiDB 的使用方式更加贴近传统数据库，降低用户迁移的成本，TiDB 自 v3.0 版本开始在乐观事务模型的基础上支持了悲观事务模型。本文将介绍 TiDB 悲观事务的相关特性。

> **注意：**
>
> 自 v3.0.8 开始，新创建的 TiDB 集群默认使用悲观事务模型。但如果从 v3.0.7 版本及之前创建的集群升级到 >= v3.0.8 的版本，则不会改变默认的事务模型，即**只有新创建的集群才会默认使用悲观事务模型**。

## 事务模式的修改方法

你可以使用 [`tidb_txn_mode`](/tidb-specific-system-variables.md#tidb_txn_mode) 系统变量设置事务模式。执行以下命令，即可使整个集群中所有新创建 session 执行的所有显示事务（即非 autocommit 的事务）进入悲观事务模式：

{{< copyable "sql" >}}

```sql
set @@global.tidb_txn_mode = 'pessimistic';
```

除此之外，还可以执行以下 SQL 语句显式地开启悲观事务：

{{< copyable "sql" >}}

```sql
BEGIN PESSIMISTIC;
```

{{< copyable "sql" >}}

```
BEGIN /*!90000 PESSIMISTIC */;
```

`BEGIN PESSIMISTIC;` 和 `BEGIN OPTIMISTIC;` 等语句的优先级高于 `tidb_txn_mode` 系统变量。使用这两个语句开启的事务，会忽略系统变量，从而支持悲观、乐观事务混合使用。

## 悲观事务模式的行为

悲观事务的行为和 MySQL 基本一致（不一致之处详见[和 MySQL InnoDB 的差异](#和-mysql-innodb-的差异)）：

- `SELECT FOR UPDATE` 会读取已提交的**最新**数据，并对读取到的数据加悲观锁。

- `UPDATE`、`DELETE` 和 `INSERT` 语句都会读取已提交的**最新**的数据来执行，并对修改的数据加悲观锁。

- 当一行数据被加了悲观锁以后，其他尝试修改这一行的写事务会被阻塞，等待悲观锁的释放。

- 当一行数据被加了悲观锁以后，其他尝试读取这一行的事务不会被阻塞，可以读到已提交的数据。

- 事务提交或回滚的时候，会释放所有的锁。

- 当有多个事务同时等待同一个锁释放时，会尽可能按照事务 start ts 顺序获取锁，但不能严格保证。

- 如果并发事务出现死锁，会被死锁检测器检测到，随机终止掉其中一个事务并返回兼容 MySQL 的错误码 `1213`。

- 乐观事务和悲观事务可以共存，事务可以任意指定使用乐观模式或悲观模式来执行。

- 通过设置 `innodb_lock_wait_timeout` 变量，设置等锁超时时间，等锁超时后返回兼容 MySQL 的错误码 `1205`。

- 支持 `FOR UPDATE NOWAIT` 语法，遇到锁时不会阻塞等锁，而是返回兼容 MySQL 的错误码 `3572`。

- 如果 `Point Get` 和 `Batch Point Get` 算子没有读到数据，依然会对给定的主键或者唯一键加锁，阻塞其他事务对相同主键唯一键加锁或者进行写入操作。

## 和 MySQL InnoDB 的差异

1. TiDB 使用 range 作为 WHERE 条件，执行 DML 和 `SELECT FOR UPDATE` 语句时不会阻塞范围内并发的 `INSERT` 语句的执行。

    InnoDB 通过实现 gap lock，支持阻塞 range 内并发的 `INSERT` 语句的执行，其主要目的是为了支持 statement based binlog，因此有些业务会通过将隔离级别降低至 Read Committed 来避免 gap lock 导致的并发性能问题。TiDB 不支持 gap lock，也就不需要付出相应的并发性能的代价。

2. TiDB 不支持 `SELECT LOCK IN SHARE MODE`。

    使用这个语句执行的时候，效果和没有加锁是一样的，不会阻塞其他事务的读写。

3. DDL 可能会导致悲观事务提交失败。

    MySQL 在执行 DDL 时会被正在执行的事务阻塞住，而在 TiDB 中 DDL 操作会成功，造成悲观事务提交失败：`ERROR 1105 (HY000): Information schema is changed. [try again later]`。TiDB 事务执行过程中并发执行 `TRUNCATE TABLE` 语句，可能会导致事务报错 `table dosen't exist`。

4. `START TRANSACTION WITH CONSISTENT SNAPSHOT` 之后，MySQL 仍然可以读取到之后在其他事务创建的表，而 TiDB 不能。

5. autocommit 事务不支持悲观锁。

    所有自动提交的语句都不会加悲观锁，该类语句在用户侧感知不到区别，因为悲观事务的本质是把整个事务的重试变成了单个 DML 的重试，autocommit 事务即使在 TiDB 关闭重试时也会自动重试，效果和悲观事务相同。

    自动提交的 select for update 语句也不会等锁。

6. 对语句中 `EMBEDDED SELECT` 读到的相关数据不会加锁。

## 隔离级别

TiDB 在悲观事务模式下支持了 2 种隔离级别：

1. 默认使用与 MySQL 行为相同的[可重复读隔离级别 (Repeatable Read)](/transaction-isolation-levels.md#可重复读隔离级别-repeatable-read)。

    > **注意：**
    >
    > 在这种隔离级别下，DML 操作会基于已提交的最新数据来执行，行为与 MySQL 相同，但与 TiDB 乐观事务不同，请参考[与 MySQL 可重复读隔离级别的区别](/transaction-isolation-levels.md#与-mysql-可重复读隔离级别的区别)。

2. 使用 [`SET TRANSACTION`](/sql-statements/sql-statement-set-transaction.md) 语句可将隔离级别设置为[读已提交隔离级别 (Read Committed)](/transaction-isolation-levels.md#读已提交隔离级别-read-committed)。

## Pipelined 加锁流程

加悲观锁需要向 TiKV 写入数据，要经过 Raft 提交并 apply 后才能返回，相比于乐观事务，不可避免的会增加部分延迟。为了降低加锁的开销，TiKV 实现了 pipelined 加锁流程：当数据满足加锁要求时，TiKV 立刻通知 TiDB 执行后面的请求，并异步写入悲观锁，从而降低大部分延迟，显著提升悲观事务的性能。但有较低概率悲观锁异步写入失败，可能会导致悲观事务提交失败。

![Pipelined pessimistic lock](/media/pessimistic-transaction-pipelining.png)

该功能默认关闭，可修改 TiKV 配置启用：

```toml
[pessimistic-txn]
pipelined = true
```

## 常见问题

1. TiDB 日志出现 `pessimistic write conflict, retry statement`。

    当发生 write conflict 时，乐观事务会直接终止，而悲观事务会尝试用最新数据重试该语句直到没有 write conflict，每次重试都会打印该 log，不用特别关注。

2. 执行 DML 时报错 `pessimistic lock retry limit reached`。

    悲观事务每个语句有重试次数限制，当因 write conflict 重试超过该限制时会报该错误，默认为 256 次，可通过 TiDB 配置文件 `[pessimistic-txn]` 类别下的 `max-retry-limit` 修改。

3. 悲观事务执行时间限制。

    在 v4.0 中，GC 已不会影响到正在运行的事务，但悲观事务的执行时间仍有上限，默认为 10 分钟，可通过 TiDB 配置文件 `[performance]` 类别下的 `max-txn-ttl` 修改。
